#!/usr/bin/env python3
"""Prepare, launch, finalize, and verify Humanize branch research artifacts."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path("/Users/wangweiyang/GitHub/weiyangzen")
LEARN_ROOT = REPO_ROOT / "learn_humanize"
HUMANIZE_REPO = Path("/Users/wangweiyang/GitHub/humanize")
SOURCE_EXPORT_ROOT = Path("/Users/wangweiyang/GitHub/humanize_branch_worktrees")
RUN_ID = "2026-06-19_humanize_branch_1to1"
MAIN_REUSED_RUN_ID = "2026-06-19_humanize_core_1to1"
OH_MY_HUMANIZE_RUN_ID = "2026-06-19_oh_my_humanize_branch_1to1"
MODEL = "gpt-5.5"
EFFORT = "xhigh"
WORKER_SLOT_COUNT = 30
AGENT_COUNT = WORKER_SLOT_COUNT
ACTIVE_WORKER_TARGET = 25
REPLENISH_INTERVAL_SECONDS = 120
TIMEOUT_SECONDS = 7200

REPO_CONFIGS = {
    "humanize": {
        "repo_id": "humanize",
        "title": "Humanize",
        "source_remote": "https://github.com/PolyArch/humanize.git",
        "local_repo": HUMANIZE_REPO,
        "branch_root": LEARN_ROOT / "branches",
        "source_export_root": SOURCE_EXPORT_ROOT,
        "run_id": RUN_ID,
        "tmux_prefix": "humanize",
    },
    "oh-my-humanize": {
        "repo_id": "oh-my-humanize",
        "title": "oh-my-humanize",
        "source_remote": "https://github.com/PolyArch/oh-my-humanize.git",
        "local_repo": Path("/Users/wangweiyang/GitHub/oh-my-humanize"),
        "branch_root": LEARN_ROOT / "repos" / "oh-my-humanize" / "branches",
        "source_export_root": Path("/Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees"),
        "run_id": OH_MY_HUMANIZE_RUN_ID,
        "tmux_prefix": "ohmyhumanize",
    },
}
ACTIVE_REPO_ID = os.environ.get("LEARN_REPO_ID", "humanize")


def active_repo() -> dict[str, object]:
    if ACTIVE_REPO_ID not in REPO_CONFIGS:
        raise KeyError(f"unknown LEARN_REPO_ID={ACTIVE_REPO_ID!r}; expected one of {sorted(REPO_CONFIGS)}")
    return REPO_CONFIGS[ACTIVE_REPO_ID]


def set_active_repo(repo_id: str) -> None:
    global ACTIVE_REPO_ID
    if repo_id not in REPO_CONFIGS:
        raise KeyError(f"unknown repo id: {repo_id}")
    ACTIVE_REPO_ID = repo_id


def repo_id() -> str:
    return str(active_repo()["repo_id"])


def repo_title() -> str:
    return str(active_repo()["title"])


def repo_path() -> Path:
    return Path(active_repo()["local_repo"])


def rel_to_repo(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc


def branch_safe_name(branch: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "__", branch).strip("_")


def tmux_session_name(branch: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", branch_safe_name(branch)).strip("_")
    prefix = str(active_repo()["tmux_prefix"])
    return f"{prefix}_{safe[:24]}_1to1_20260619"


def agent_name(index: int, total: int | None = None) -> str:
    width = max(2, len(str(total or index)))
    return f"agent_{index:0{width}d}"


def agent_sort_key(agent: str) -> tuple[int, str]:
    suffix = agent.split("_", 1)[1] if "_" in agent else agent
    try:
        return (int(suffix), agent)
    except ValueError:
        return (10**9, agent)


def branch_dir(branch: str) -> Path:
    return Path(active_repo()["branch_root"]) / branch_safe_name(branch)


def run_id_for(branch: str) -> str:
    # Main was completed before the unified multi-branch layout existed.
    # Keep its original run id so verification works after moving it under branches/main.
    if repo_id() == "humanize" and branch == "main" and (branch_dir(branch) / "research_runs" / MAIN_REUSED_RUN_ID).exists():
        return MAIN_REUSED_RUN_ID
    return str(active_repo()["run_id"])


def run_dir(branch: str) -> Path:
    return branch_dir(branch) / "research_runs" / run_id_for(branch)


def source_dir(branch: str) -> Path:
    return Path(active_repo()["source_export_root"]) / branch_safe_name(branch)


def commit_for(branch: str) -> str:
    return run(["git", "rev-parse", f"origin/{branch}"], cwd=repo_path()).stdout.strip()


def tree_for(branch: str) -> str:
    return run(["git", "rev-parse", f"origin/{branch}^{{tree}}"], cwd=repo_path()).stdout.strip()


def export_branch(branch: str) -> None:
    dst = source_dir(branch)
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    archive = subprocess.Popen(
        ["git", "archive", f"origin/{branch}"],
        cwd=repo_path(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    tar = subprocess.Popen(["tar", "-x", "-C", str(dst)], stdin=archive.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert archive.stdout is not None
    archive.stdout.close()
    tar_out, tar_err = tar.communicate()
    archive_err = archive.stderr.read().decode() if archive.stderr else ""
    archive_rc = archive.wait()
    if archive_rc != 0 or tar.returncode != 0:
        raise RuntimeError(
            f"failed to export origin/{branch}: git={archive_rc}, tar={tar.returncode}\n{archive_err}\n{tar_err.decode()}"
        )


def classify_file(path: str) -> tuple[bool, str]:
    name = Path(path).name
    lower = name.lower()
    suffix = Path(path).suffix.lower()
    if path == ".gitignore":
        return False, "metadata only; not algorithm behavior"
    if path in ("Cargo.lock", "bun.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"):
        return False, "dependency lockfile; skipped as generated/package metadata"
    if lower.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".icns", ".woff", ".woff2", ".ttf", ".otf", ".mp4", ".mov", ".zip", ".gz", ".tar", ".wasm")):
        return False, "binary or generated asset; no algorithm text/code to research"
    if path.startswith(".github/"):
        return False, "CI workflow; not core algorithm runtime or specification"
    if path.startswith(".claude-plugin/"):
        return False, "plugin packaging metadata; not core algorithm runtime or specification"
    if path.startswith(".claude/"):
        return False, "local assistant instruction surface; not repository algorithm behavior"
    if path in ("README.md", "AGENTS.md", "docs/usage.md", "docs/bitlesson.md"):
        return True, "behavior-defining documentation for workflow/state-machine algorithms"
    if path.startswith("assets/") or path.startswith("docs/images/"):
        return False, "visual/binary asset; no algorithm text/code to research"
    if path.startswith("docs/install-"):
        return False, "installation guide; skipped as non-core algorithm content"
    if path.startswith("docs/"):
        if repo_id() == "oh-my-humanize" and any(
            token in path
            for token in (
                "architecture",
                "runtime",
                "tool",
                "protocol",
                "pipeline",
                "schema",
                "memory",
                "mcp",
                "natives",
                "session",
                "tui",
                "task-agent",
                "slash-command",
                "rulebook",
                "compaction",
            )
        ):
            return True, "architecture/runtime documentation defining core algorithms"
        return False, "documentation outside the core algorithm subset"
    if repo_id() == "oh-my-humanize" and lower.endswith((".md", ".mdx")) and path not in ("README.md", "AGENTS.md"):
        return False, "package README/changelog prose; skipped outside core algorithm subset"
    if path.startswith(".omp/"):
        return True, "oh-my-humanize command or skill instruction defining workflow behavior"
    if path.startswith("agents/"):
        return True, "agent prompt/policy file defining review or planning behavior"
    if path.startswith("commands/"):
        return True, "command workflow definition for plan/RLCR algorithms"
    if path.startswith("config/"):
        return True, "runtime configuration or hook schema participating in gates/routing"
    if path.startswith("hooks/"):
        return True, "hook or validator implementation for the RLCR state machine"
    if path.startswith("prompt-template/"):
        return True, "prompt/block template defining algorithmic transitions, gates, or review contracts"
    if path.startswith("scripts/"):
        if name.startswith("install-"):
            return False, "installer utility; skipped as non-core algorithm content"
        return True, "runtime script implementing workflow, routing, monitor, validation, or state behavior"
    if path.startswith("skills/"):
        return True, "skill instruction defining algorithmic workflow behavior"
    if path.startswith("templates/"):
        return True, "template consumed by core workflow/memory algorithm"
    if path.startswith("tests/fixtures/") or path.startswith("tests/mocks/"):
        return False, "fixture/mock data; not a core algorithm file"
    if path.startswith("tests/"):
        return True, "executable specification for core algorithm behavior"
    if repo_id() == "oh-my-humanize":
        if any(part in path for part in ("/public/", "/assets/", "/examples/", "/fixtures/", "/__snapshots__/")):
            return False, "asset/example/fixture surface; skipped as non-core algorithm content"
        if path.startswith(("assets/", "patches/", "docs/skills/examples/")):
            return False, "asset, patch, or example content; skipped as non-core algorithm content"
        if "vendored" in path:
            return False, "vendored third-party source; skipped as non-project algorithm content"
        if name in ("package.json", "tsconfig.json", "tsconfig.publish.json", "tsconfig.client.json", "tailwind.config.js", "vite.config.ts", "vitest.config.ts"):
            return False, "package-level build metadata; skipped unless workspace-level"
        if path.startswith(("crates/", "packages/", "python/", "types/")):
            if "/node_modules/" in path or "/dist/" in path or "/build/" in path or "/target/" in path:
                return False, "generated dependency/build output; skipped"
            if path.startswith("python/robomp/web/") and not path.startswith("python/robomp/web/src/"):
                return False, "web packaging or asset surface; skipped outside runtime source"
            if suffix in (".rs", ".ts", ".tsx", ".js", ".jsx", ".py", ".sh"):
                return True, "oh-my-humanize package/crate/runtime source defining core behavior"
        if path in (
            "Cargo.toml",
            "package.json",
            "tsconfig.json",
            "tsconfig.base.json",
            "tsconfig.tools.json",
            "biome.json",
            "bunfig.toml",
            ".fallowrc.jsonc",
            "rust-toolchain.toml",
            "rustfmt.toml",
            "rust-analyzer.toml",
        ):
            return True, "workspace configuration participating in build/runtime/tooling algorithms"
        if path.startswith("infra/") and suffix in (".sh", ".ts", ".js", ".md", ".toml", ".json", ".yml", ".yaml"):
            return True, "infrastructure runtime script or configuration"
    return False, "outside the core algorithm subset"


def file_sha16(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def collect_inventory(branch: str) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    src = source_dir(branch)
    files = sorted(p.relative_to(src).as_posix() for p in src.rglob("*") if p.is_file())
    dirs = ["."] + sorted(p.relative_to(src).as_posix() for p in src.rglob("*") if p.is_dir())

    file_records: list[dict[str, object]] = []
    included_files: set[str] = set()
    for f in files:
        inc, reason = classify_file(f)
        full = src / f
        rec: dict[str, object] = {
            "path": f,
            "path_type": "file",
            "included": inc,
            "reason": reason,
            "bytes": full.stat().st_size,
            "sha16": file_sha16(full),
            "depth": f.count("/") + 1 if "/" in f else 0,
            "core_descendant_files": "",
        }
        file_records.append(rec)
        if inc:
            included_files.add(f)

    def classify_dir(d: str) -> tuple[bool, str]:
        if d in (".github", ".github/workflows", ".claude", ".claude-plugin", "docs/images", "tests/fixtures", "tests/mocks"):
            return False, "directory only contains skipped non-core files"
        prefix = "" if d == "." else d.rstrip("/") + "/"
        if any(f == d or f.startswith(prefix) for f in included_files):
            return True, "directory contains included core algorithm descendant(s)"
        return False, "no included core algorithm descendants"

    dir_records: list[dict[str, object]] = []
    for d in dirs:
        inc, reason = classify_dir(d)
        prefix = "" if d == "." else d.rstrip("/") + "/"
        desc = file_records if d == "." else [r for r in file_records if str(r["path"]).startswith(prefix)]
        core_desc = [r for r in desc if r["included"]]
        rec = {
            "path": d,
            "path_type": "directory",
            "included": inc,
            "reason": reason,
            "bytes": sum(int(r["bytes"]) for r in core_desc),
            "sha16": "-",
            "depth": 0 if d == "." else d.count("/") + 1,
            "core_descendant_files": len(core_desc),
        }
        dir_records.append(rec)

    all_records = sorted(dir_records + file_records, key=lambda r: (str(r["path"]).count("/"), r["path_type"] != "directory", str(r["path"])))
    included = [r for r in all_records if r["included"]]
    skipped = [r for r in all_records if not r["included"]]
    prefix_base = branch_safe_name(branch).upper().replace("-", "_").replace(".", "_")
    prefix_repo = repo_id().upper().replace("-", "_").replace(".", "_")
    prefix = prefix_base if repo_id() == "humanize" else f"{prefix_repo}_{prefix_base}"
    for i, rec in enumerate(included, 1):
        rec["item_id"] = f"{prefix}-HZ-{i:03d}"
    for i, rec in enumerate(skipped, 1):
        rec["item_id"] = f"{prefix}-SKIP-{i:03d}"
    return all_records, included, skipped


def write_tsv(path: Path, headers: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: str(row.get(k, "")).replace("\t", " ").replace("\n", " ") for k in headers})


def distribute_items(included: list[dict[str, object]]) -> list[list[dict[str, object]]]:
    batches: list[list[dict[str, object]]] = [[item] for item in included]
    for idx, batch in enumerate(batches, 1):
        agent = agent_name(idx, len(batches))
        for item in batch:
            item["assigned_agent"] = agent
    return batches


def write_blueprint(path: Path, branch: str, commit: str, tree: str, included: list[dict[str, object]], state: str) -> None:
    done = state == "final"
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# {repo_title()} Branch `{branch}` 1:1 Research Blueprint\n\n")
        f.write("This is the authoritative per-branch checklist. Every included core algorithm file or directory has exactly one checklist item.\n\n")
        f.write("## Run Metadata\n\n")
        f.write(f"- repo: `{repo_id()}`\n- branch: `{branch}`\n- source_commit: `{commit}`\n- source_tree: `{tree}`\n")
        worker_jobs = len({str(item.get("assigned_agent", "")) for item in included if item.get("assigned_agent")})
        f.write(f"- model: `{MODEL}`\n- reasoning_effort: `{EFFORT}`\n- worker_slots: `{WORKER_SLOT_COUNT}`\n- worker_jobs: `{worker_jobs}`\n\n")
        f.write("## Dual-Cursor State\n\n")
        if done:
            f.write(f"- `[ ]`: 0\n- `[_]`: 0\n- `[x]`: {len(included)}\n\n")
        else:
            f.write(f"- `[ ]`: {len(included)}\n- `[_]`: 0\n- `[x]`: 0\n\n")
        f.write("## Authoritative Checklist\n\n")
        mark = "[x]" if done else "[ ]"
        status = "accepted after complete status, output existence, and item-id coverage verification" if done else "pending worker evidence"
        for item in included:
            agent = item.get("assigned_agent", "")
            f.write(f"- {mark} {item['item_id']} `{item['path_type']}` `{item['path']}`\n")
            f.write(f"  - assigned_agent: `{agent}`\n")
            f.write(f"  - owned_path_scope: `{item['path']}`\n")
            f.write("  - dependencies: `none`\n")
            f.write(f"  - inclusion_reason: {item['reason']}\n")
            f.write(f"  - worker_evidence: `research_runs/{run_id_for(branch)}/agents/{agent}/output.md`\n")
            f.write(f"  - master_status: {status}\n")


def write_todo(path: Path, branch: str, commit: str, included: list[dict[str, object]], assignment_rows: list[dict[str, object]], state: str) -> None:
    done = state == "final"
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# todos_20260619 - {repo_title()} `{branch}` 1:1 Research\n\n")
        f.write(f"- Repo: `{repo_id()}`\n- Branch: `{branch}`\n- Source commit: `{commit}`\n- Model: `{MODEL}`\n- Reasoning effort: `{EFFORT}`\n")
        f.write(f"- Worker slots: `{WORKER_SLOT_COUNT}`\n")
        f.write(f"- Worker jobs: `{len(assignment_rows)}`\n")
        f.write(f"- Active worker refill target: `{ACTIVE_WORKER_TARGET}` checked every `{REPLENISH_INTERVAL_SECONDS}` seconds\n")
        if done:
            f.write(f"- Counts: `[ ]` 0, `[_]` 0, `[x]` {len(included)}, Unfinished 0\n\n")
            f.write("## Worker Claim Frontier\n\nNo unclaimed work remains.\n\n")
            f.write("## Main-Session Integration Frontier\n\nAll worker outputs were verified and master accepted.\n\n")
        else:
            f.write(f"- Counts: `[ ]` {len(included)}, `[_]` 0, `[x]` 0, Unfinished {len(included)}\n\n")
            f.write("## Worker Claim Frontier\n\n")
            for row in assignment_rows:
                f.write(f"- {row['agent']}: claim {row['item_count']} item(s): `{row['item_ids']}`\n")
            f.write("\n## Main-Session Integration Frontier\n\nNo `[_]` items yet.\n\n")
        f.write("## Claim Ledger\n\n")
        f.write(f"- Ledger: `research_runs/{run_id_for(branch)}/claim_ledger.tsv`\n")
        f.write(f"- Assignment: `research_runs/{run_id_for(branch)}/assignment.tsv`\n")
        f.write(f"- Full inventory: `research_runs/{run_id_for(branch)}/path_inventory.tsv`\n")


def write_launcher_files(branch: str) -> None:
    rdir = run_dir(branch)
    session = tmux_session_name(branch)
    worker_jobs = sorted((rdir / "agents").glob("agent_*/run.sh"), key=lambda p: agent_sort_key(p.parent.name))
    worker_job_count = len(worker_jobs)

    replenisher = rdir / "replenish_tmux_codex_workers.sh"
    replenisher.write_text(
        f"""#!/usr/bin/env bash
set -euo pipefail

RUN_DIR={str(rdir)!r}
SESSION={session!r}
WORKER_SLOT_COUNT="${{WORKER_SLOT_COUNT:-{WORKER_SLOT_COUNT}}}"
AGENT_COUNT="${{AGENT_COUNT:-$WORKER_SLOT_COUNT}}"
WORKER_JOB_COUNT="${{WORKER_JOB_COUNT:-{worker_job_count}}}"
ACTIVE_WORKER_TARGET="${{ACTIVE_WORKER_TARGET:-{ACTIVE_WORKER_TARGET}}}"
CHECK_INTERVAL_SECONDS="${{CHECK_INTERVAL_SECONDS:-{REPLENISH_INTERVAL_SECONDS}}}"
STARTED_DIR="$RUN_DIR/started"
STATUS_DIR="$RUN_DIR/status"
LOG="$RUN_DIR/worker_replenish.log"

mkdir -p "$STARTED_DIR" "$STATUS_DIR"
touch "$LOG"

log() {{
  printf '%s %s\\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >> "$LOG"
}}

active_workers() {{
  local names
  names="$(tmux list-windows -t "$SESSION" -F '#W' 2>/dev/null || true)"
  printf '%s\\n' "$names" | awk '/^agent[0-9]+$/ {{ count++ }} END {{ print count + 0 }}'
}}

complete_count() {{
  local count=0
  local status_file
  shopt -s nullglob
  for status_file in "$STATUS_DIR"/agent_*.status; do
    if [[ "$(cat "$status_file" 2>/dev/null || true)" == "complete" ]]; then
      count=$((count + 1))
    fi
  done
  shopt -u nullglob
  printf '%s' "$count"
}}

failed_count() {{
  local count=0
  local status_file value
  shopt -s nullglob
  for status_file in "$STATUS_DIR"/agent_*.status; do
    value="$(cat "$status_file" 2>/dev/null || true)"
    if [[ "$value" == failed:* ]]; then
      count=$((count + 1))
    fi
  done
  shopt -u nullglob
  printf '%s' "$count"
}}

agent_window_active() {{
  local id="$1"
  local name="agent$id"
  tmux list-windows -t "$SESSION" -F '#W' 2>/dev/null | awk -v name="$name" '$0 == name {{ found=1 }} END {{ exit found ? 0 : 1 }}'
}}

next_claimable_agent() {{
  local runner agent id status_file status
  while IFS= read -r runner; do
    agent="$(basename "$(dirname "$runner")")"
    id="${{agent#agent_}}"
    status_file="$STATUS_DIR/$agent.status"
    status=""
    if [[ -f "$status_file" ]]; then
      status="$(cat "$status_file" 2>/dev/null || true)"
    fi
    [[ "$status" == "complete" ]] && continue
    agent_window_active "$id" && continue
    printf '%s\\n' "$id"
    return 0
  done < <(find "$RUN_DIR/agents" -mindepth 2 -maxdepth 2 -type f -name run.sh | sort -V)
  return 1
}}

start_agent() {{
  local id="$1"
  local agent="agent_$id"
  local runner="$RUN_DIR/agents/$agent/run.sh"
  local attempt_file="$STARTED_DIR/$agent.attempts"
  local attempt=1
  if [[ ! -x "$runner" ]]; then
    log "missing runner for $agent: $runner"
    return 1
  fi
  if [[ -f "$attempt_file" ]]; then
    attempt="$(cat "$attempt_file" 2>/dev/null || echo 0)"
    attempt=$((attempt + 1))
  fi
  printf '%s\\n' "$attempt" > "$attempt_file"
  rm -f "$STATUS_DIR/$agent.status" "$RUN_DIR/agents/$agent/output.md"
  tmux new-window -t "$SESSION:" -n "agent$id" "bash '$runner'; tmux kill-window -t '$SESSION:agent$id' 2>/dev/null || true"
  touch "$STARTED_DIR/$agent.started"
  log "started $agent attempt=$attempt"
}}

replenish() {{
  local active next_id
  active="$(active_workers)"
  local target="$ACTIVE_WORKER_TARGET"
  if [[ "$target" -gt "$WORKER_SLOT_COUNT" ]]; then
    target="$WORKER_SLOT_COUNT"
  fi
  while [[ "$active" -lt "$target" ]]; do
    if ! next_id="$(next_claimable_agent)"; then
      break
    fi
    start_agent "$next_id"
    active="$(active_workers)"
  done
}}

log "controller started session=$SESSION worker_slots=$WORKER_SLOT_COUNT worker_jobs=$WORKER_JOB_COUNT active_target=$ACTIVE_WORKER_TARGET interval=$CHECK_INTERVAL_SECONDS"
while true; do
  replenish
  active="$(active_workers)"
  complete="$(complete_count)"
  failed="$(failed_count)"
  log "tick active_workers=$active complete_statuses=$complete failed_statuses=$failed worker_jobs=$WORKER_JOB_COUNT"
  if [[ "$complete" -ge "$WORKER_JOB_COUNT" && "$active" -eq 0 ]]; then
    log "all worker jobs completed"
    break
  fi
  sleep "$CHECK_INTERVAL_SECONDS"
done
""",
        encoding="utf-8",
    )
    replenisher.chmod(replenisher.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    launcher = rdir / "launch_tmux_codex_research.sh"
    launcher.write_text(
        f"""#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
SESSION="${{SESSION:-{session}}}"
WORKER_SLOT_COUNT="${{WORKER_SLOT_COUNT:-{WORKER_SLOT_COUNT}}}"
AGENT_COUNT="${{AGENT_COUNT:-$WORKER_SLOT_COUNT}}"
WORKER_JOB_COUNT="${{WORKER_JOB_COUNT:-{worker_job_count}}}"
ACTIVE_WORKER_TARGET="${{ACTIVE_WORKER_TARGET:-{ACTIVE_WORKER_TARGET}}}"
CHECK_INTERVAL_SECONDS="${{CHECK_INTERVAL_SECONDS:-{REPLENISH_INTERVAL_SECONDS}}}"
if ! command -v tmux >/dev/null 2>&1; then echo "tmux is required" >&2; exit 1; fi
if ! command -v codex >/dev/null 2>&1; then echo "codex is required" >&2; exit 1; fi
if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already exists: $SESSION" >&2
  exit 1
fi
rm -f "$RUN_DIR/status"/*.status
rm -rf "$RUN_DIR/started"
mkdir -p "$RUN_DIR/status" "$RUN_DIR/started"
tmux new-session -d -s "$SESSION" -n "controller" "WORKER_SLOT_COUNT='$WORKER_SLOT_COUNT' AGENT_COUNT='$AGENT_COUNT' WORKER_JOB_COUNT='$WORKER_JOB_COUNT' ACTIVE_WORKER_TARGET='$ACTIVE_WORKER_TARGET' CHECK_INTERVAL_SECONDS='$CHECK_INTERVAL_SECONDS' bash '$RUN_DIR/replenish_tmux_codex_workers.sh'"
echo "launched replenishing codex research controller in tmux session: $SESSION"
echo "worker slots: $WORKER_SLOT_COUNT"
echo "worker jobs: $WORKER_JOB_COUNT"
echo "active worker refill target: $ACTIVE_WORKER_TARGET"
echo "check interval seconds: $CHECK_INTERVAL_SECONDS"
echo "status dir: $RUN_DIR/status"
echo "controller log: $RUN_DIR/worker_replenish.log"
""",
        encoding="utf-8",
    )
    launcher.chmod(launcher.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def write_runner_files(branch: str, commit: str, tree: str, batches: list[list[dict[str, object]]]) -> None:
    bdir = branch_dir(branch)
    rdir = run_dir(branch)
    prompts = rdir / "prompts"
    agents = rdir / "agents"
    status_dir = rdir / "status"
    for p in (prompts, agents, status_dir):
        p.mkdir(parents=True, exist_ok=True)
    session = tmux_session_name(branch)
    src = source_dir(branch)

    for idx, batch in enumerate(batches, 1):
        agent = agent_name(idx, len(batches))
        adir = agents / agent
        adir.mkdir(parents=True, exist_ok=True)
        (adir / "metadata.env").write_text(
            f"branch={branch}\nagent={agent}\nsource_commit={commit}\nsource_tree={tree}\n"
            f"model={MODEL}\nreasoning_effort={EFFORT}\nitem_count={len(batch)}\nstatus=prepared\n",
            encoding="utf-8",
        )
        rows = "\n".join(
            f"| {item['item_id']} | {item['path_type']} | `{item['path']}` | {item['bytes']} | {item['reason']} |"
            for item in batch
        )
        if not rows:
            rows = "| none | none | `none` | 0 | no included item assigned to this worker |"
        prompt = f"""You are worker {agent} in an execution-cron style branch research run.

Repository root: {src}
Work only inside this read-only branch export: {src}
Do not edit the scheduler's authoritative checkout directly: {REPO_ROOT}
Do not modify files. Produce research notes only.

Run metadata:
- Branch: {branch}
- Source commit: {commit}
- Source tree: {tree}
- Model requested by scheduler: {MODEL}
- Reasoning effort requested by scheduler: {EFFORT}
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
{rows}

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# {agent} {branch} 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: {len(batch)}
- source_commit: `{commit}`

## Item Evidence

### <ITEM_ID> `<type>` `<path>`
- cursor: `[_]`
- core_role:
- algorithmic_behavior:
- inputs_outputs_state:
- gates_or_invariants:
- dependencies_and_callers:
- edge_cases_or_failure_modes:
- validation_or_tests:
- skip_candidate: `no` or `yes: reason`

## Worker Self-Test
- assigned_items_seen:
- missing_items:
- duplicate_items:
- final_worker_status: `complete`
"""
        (prompts / f"{agent}.md").write_text(prompt, encoding="utf-8")
        timeout_py = adir / "timeout_run.py"
        timeout_py.write_text(
            """#!/usr/bin/env python3
import os, signal, subprocess, sys
if len(sys.argv) < 3:
    print("usage: timeout_run.py SECONDS COMMAND...", file=sys.stderr)
    sys.exit(2)
timeout = int(sys.argv[1])
proc = subprocess.Popen(sys.argv[2:], preexec_fn=os.setsid)
try:
    sys.exit(proc.wait(timeout=timeout))
except subprocess.TimeoutExpired:
    os.killpg(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
    sys.exit(124)
""",
            encoding="utf-8",
        )
        timeout_py.chmod(timeout_py.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        run_sh = adir / "run.sh"
        run_sh.write_text(
            f"""#!/usr/bin/env bash
set -euo pipefail
RUN_DIR={str(rdir)!r}
BRANCH={branch!r}
AGENT={agent!r}
AGENT_DIR="$RUN_DIR/agents/$AGENT"
PROMPT="$RUN_DIR/prompts/$AGENT.md"
OUTPUT="$AGENT_DIR/output.md"
ERRLOG="$AGENT_DIR/stderr.log"
STATUS="$RUN_DIR/status/$AGENT.status"
META="$AGENT_DIR/metadata.env"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'branch=%s\\nagent=%s\\nsource_commit=%s\\nsource_tree=%s\\nmodel=%s\\nreasoning_effort=%s\\nitem_count=%s\\nstatus=running\\nstarted_utc=%s\\n' "$BRANCH" "$AGENT" {commit!r} {tree!r} {MODEL!r} {EFFORT!r} {len(batch)!r} "$STARTED" > "$META"
rm -f "$ERRLOG"
set +e
"$AGENT_DIR/timeout_run.py" {TIMEOUT_SECONDS} codex -a never exec -m {MODEL} -c model_reasoning_effort={EFFORT} -C {str(src)!r} --skip-git-repo-check -s read-only --ephemeral -o "$OUTPUT" - < "$PROMPT" 2> "$ERRLOG"
rc=$?
set -e
ENDED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ "$rc" -eq 0 ]; then
  echo complete > "$STATUS"
  final_status=complete
else
  echo failed:$rc > "$STATUS"
  final_status=failed
fi
printf 'branch=%s\\nagent=%s\\nsource_commit=%s\\nsource_tree=%s\\nmodel=%s\\nreasoning_effort=%s\\nitem_count=%s\\nstatus=%s\\nstarted_utc=%s\\nended_utc=%s\\nexit_code=%s\\n' "$BRANCH" "$AGENT" {commit!r} {tree!r} {MODEL!r} {EFFORT!r} {len(batch)!r} "$final_status" "$STARTED" "$ENDED" "$rc" > "$META"
exit "$rc"
""",
            encoding="utf-8",
        )
        run_sh.chmod(run_sh.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    write_launcher_files(branch)


def prepare(branch: str) -> None:
    commit = commit_for(branch)
    tree = tree_for(branch)
    bdir = branch_dir(branch)
    if bdir.exists():
        shutil.rmtree(bdir)
    export_branch(branch)
    all_records, included, skipped = collect_inventory(branch)
    batches = distribute_items(included)
    bdir.mkdir(parents=True, exist_ok=True)
    rdir = run_dir(branch)
    rdir.mkdir(parents=True, exist_ok=True)

    assignment_rows = []
    for idx, batch in enumerate(batches, 1):
        agent = agent_name(idx, len(batches))
        assignment_rows.append(
            {
                "agent": agent,
                "item_count": len(batch),
                "total_bytes": sum(int(item["bytes"]) for item in batch),
                "item_ids": ",".join(str(item["item_id"]) for item in batch),
                "paths": "; ".join(str(item["path"]) for item in batch),
            }
        )

    inventory_headers = ["item_id", "path_type", "path", "included", "assigned_agent", "bytes", "sha16", "depth", "core_descendant_files", "reason"]
    inv_rows = []
    for rec in all_records:
        row = dict(rec)
        row["included"] = "yes" if rec["included"] else "no"
        row["assigned_agent"] = rec.get("assigned_agent", "")
        inv_rows.append(row)
    research_headers = ["item_id", "path_type", "path", "assigned_agent", "bytes", "sha16", "depth", "core_descendant_files", "reason"]

    for base in (bdir, rdir):
        write_tsv(base / "path_inventory.tsv", inventory_headers, inv_rows)
        write_tsv(base / "research_list.tsv", research_headers, included)
        write_tsv(base / "assignment.tsv", ["agent", "item_count", "total_bytes", "item_ids", "paths"], assignment_rows)
    write_tsv(rdir / "skipped_paths.tsv", ["item_id", "path_type", "path", "bytes", "sha16", "depth", "reason"], skipped)

    ledger_headers = ["item_id", "checkbox_state", "claim_state", "assigned_agent", "tmux_session", "slot", "path_type", "path", "dependencies", "owned_path_scope", "worker_output", "master_status"]
    session = tmux_session_name(branch)
    ledger = []
    for item in included:
        agent = str(item["assigned_agent"])
        ledger.append(
            {
                "item_id": item["item_id"],
                "checkbox_state": "[ ]",
                "claim_state": "unclaimed",
                "assigned_agent": agent,
                "tmux_session": session,
                "slot": agent.split("_")[1],
                "path_type": item["path_type"],
                "path": item["path"],
                "dependencies": "",
                "owned_path_scope": item["path"],
                "worker_output": f"research_runs/{run_id_for(branch)}/agents/{agent}/output.md",
                "master_status": "pending",
            }
        )
    write_tsv(rdir / "claim_ledger.initial.tsv", ledger_headers, ledger)
    write_tsv(rdir / "claim_ledger.tsv", ledger_headers, ledger)

    write_blueprint(bdir / "execution_blueprint.initial.md", branch, commit, tree, included, "initial")
    write_blueprint(bdir / "execution_blueprint.md", branch, commit, tree, included, "initial")
    write_todo(bdir / "todos_20260619.md", branch, commit, included, assignment_rows, "initial")

    bdir.joinpath("README.md").write_text(
        f"""# {repo_title()} Branch `{branch}` Research

This folder contains the per-branch 1:1 core-algorithm research artifact.

- Repo: `{repo_id()}`
- Source remote: `{active_repo()["source_remote"]}`
- Branch: `{branch}`
- Safe folder: `{branch_safe_name(branch)}`
- Source commit: `{commit}`
- Source tree: `{tree}`
- Local read-only export: `{source_dir(branch)}`
- Model: `{MODEL}`
- Reasoning effort: `{EFFORT}`
- Worker slots: `{WORKER_SLOT_COUNT}`
- Worker jobs: `{len(batches)}`
- Active worker refill target: `{ACTIVE_WORKER_TARGET}`
- Worker refill interval seconds: `{REPLENISH_INTERVAL_SECONDS}`
- Included algorithm items: `{len(included)}`
- Skipped non-core paths: `{len(skipped)}`

Main deliverables:

- `research_list.tsv`
- `path_inventory.tsv`
- `coverage_matrix.tsv`
- `core_algorithm_1to1_report.md`
- `research_runs/{run_id_for(branch)}/agents/agent_*/output.md`
""",
        encoding="utf-8",
    )
    rdir.joinpath("README.md").write_text(
        f"""# {run_id_for(branch)} - `{branch}`

This run uses `{WORKER_SLOT_COUNT}` Codex worker slots with model `{MODEL}` and reasoning effort `{EFFORT}`.
It has `{len(batches)}` worker jobs. The tmux controller checks every `{REPLENISH_INTERVAL_SECONDS}` seconds and refills active worker windows up to `{ACTIVE_WORKER_TARGET}` until all jobs finish.

```text
codex -a never exec -m {MODEL} -c model_reasoning_effort={EFFORT} -C {source_dir(branch)} -s read-only --ephemeral -o <agent>/output.md -
```
""",
        encoding="utf-8",
    )
    rdir.joinpath("run_manifest.env").write_text(
        f"""run_started_utc={dt.datetime.utcnow().replace(microsecond=0).isoformat()}Z
repo_id={repo_id()}
source_remote={active_repo()["source_remote"]}
branch={branch}
safe_branch={branch_safe_name(branch)}
source_root={source_dir(branch)}
source_commit={commit}
source_tree={tree}
tmux_session={session}
model={MODEL}
reasoning_effort={EFFORT}
worker_slot_count={WORKER_SLOT_COUNT}
agent_count={WORKER_SLOT_COUNT}
worker_job_count={len(batches)}
active_worker_target={ACTIVE_WORKER_TARGET}
replenish_interval_seconds={REPLENISH_INTERVAL_SECONDS}
included_items={len(included)}
skipped_items={len(skipped)}
timeout_seconds={TIMEOUT_SECONDS}
protocol=execution_cron_branch_1to1_research
""",
        encoding="utf-8",
    )
    rdir.joinpath("source_commit.txt").write_text(commit + "\n", encoding="utf-8")
    write_runner_files(branch, commit, tree, batches)
    bdir.joinpath("core_algorithm_1to1_report.md").write_text("# Pending\n\nWorkers have not been finalized yet.\n", encoding="utf-8")
    print(json.dumps({"branch": branch, "commit": commit, "included": len(included), "skipped": len(skipped), "dir": str(bdir)}, indent=2))


def verify(branch: str) -> dict[str, object]:
    bdir = branch_dir(branch)
    rdir = run_dir(branch)
    items = []
    with (bdir / "research_list.tsv").open() as f:
        items = list(csv.DictReader(f, delimiter="\t"))
    problems = []
    required_agents = sorted(
        {item["assigned_agent"] for item in items if item.get("assigned_agent")},
        key=agent_sort_key,
    )
    for item in items:
        agent = item["assigned_agent"]
        out = rdir / "agents" / agent / "output.md"
        status = rdir / "status" / f"{agent}.status"
        if not status.exists() or status.read_text().strip() != "complete":
            problems.append({"item_id": item["item_id"], "problem": "status_not_complete", "agent": agent})
        if not out.exists():
            problems.append({"item_id": item["item_id"], "problem": "missing_output", "agent": agent})
            continue
        text = out.read_text(errors="replace")
        if not re.search(r"(?<![A-Z0-9_-])" + re.escape(item["item_id"]) + r"(?![A-Z0-9_-])", text):
            problems.append({"item_id": item["item_id"], "problem": "item_id_missing_from_output", "agent": agent, "path": item["path"]})
    status_files = list((rdir / "status").glob("*.status"))
    output_files = list((rdir / "agents").glob("agent_*/output.md"))
    for agent in required_agents:
        status = rdir / "status" / f"{agent}.status"
        out = rdir / "agents" / agent / "output.md"
        if not status.exists():
            problems.append({"agent": agent, "problem": "required_agent_status_missing"})
        if not out.exists():
            problems.append({"agent": agent, "problem": "required_agent_output_missing"})
    return {
        "branch": branch,
        "research_items": len(items),
        "required_worker_jobs": len(required_agents),
        "status_files": len(status_files),
        "complete_status_files": sum(1 for p in status_files if p.read_text().strip() == "complete"),
        "output_files": len(output_files),
        "problems": len(problems),
        "problem_details": problems[:200],
    }


def finalize(branch: str) -> None:
    bdir = branch_dir(branch)
    rdir = run_dir(branch)
    commit = commit_for(branch)
    tree = tree_for(branch)
    verification = verify(branch)
    if verification["problems"]:
        print(json.dumps(verification, indent=2))
        raise SystemExit(1)
    with (bdir / "research_list.tsv").open() as f:
        included = list(csv.DictReader(f, delimiter="\t"))
    with (rdir / "skipped_paths.tsv").open() as f:
        skipped = list(csv.DictReader(f, delimiter="\t"))
    with (bdir / "path_inventory.tsv").open() as f:
        inventory = list(csv.DictReader(f, delimiter="\t"))
    with (bdir / "assignment.tsv").open() as f:
        assignments = list(csv.DictReader(f, delimiter="\t"))
    worker_job_count = len(assignments)

    coverage_rows = []
    for item in included:
        agent = item["assigned_agent"]
        out = rdir / "agents" / agent / "output.md"
        text = out.read_text(errors="replace")
        mentions = len(re.findall(r"(?<![A-Z0-9_-])" + re.escape(item["item_id"]) + r"(?![A-Z0-9_-])", text))
        coverage_rows.append(
            {
                **item,
                "status": "complete",
                "master_state": "[x]",
                "output_rel": f"research_runs/{run_id_for(branch)}/agents/{agent}/output.md",
                "item_id_mentions": mentions,
                "has_item_heading": "yes" if re.search(r"^###\s+" + re.escape(item["item_id"]) + r"\b", text, re.M) else "no",
                "master_evidence": "status complete; output exists; item_id present in assigned output",
            }
        )
    headers = ["item_id", "path_type", "path", "assigned_agent", "status", "master_state", "output_rel", "item_id_mentions", "has_item_heading", "bytes", "sha16", "depth", "core_descendant_files", "reason", "master_evidence"]
    for base in (bdir, rdir):
        write_tsv(base / "coverage_matrix.tsv", headers, coverage_rows)

    ledger_headers = ["item_id", "checkbox_state", "claim_state", "assigned_agent", "tmux_session", "slot", "path_type", "path", "dependencies", "owned_path_scope", "worker_output", "master_status"]
    session = tmux_session_name(branch)
    ledger = []
    for item in included:
        agent = item["assigned_agent"]
        ledger.append(
            {
                "item_id": item["item_id"],
                "checkbox_state": "[x]",
                "claim_state": "finished",
                "assigned_agent": agent,
                "tmux_session": session,
                "slot": agent.split("_")[1],
                "path_type": item["path_type"],
                "path": item["path"],
                "dependencies": "",
                "owned_path_scope": item["path"],
                "worker_output": f"research_runs/{run_id_for(branch)}/agents/{agent}/output.md",
                "master_status": "accepted",
            }
        )
    write_tsv(rdir / "claim_ledger.tsv", ledger_headers, ledger)
    write_blueprint(bdir / "execution_blueprint.md", branch, commit, tree, included, "final")
    write_todo(bdir / "todos_20260619.md", branch, commit, included, assignments, "final")

    verify_py = rdir / "verify_coverage.py"
    verify_py.write_text(
        f"""#!/usr/bin/env python3
import subprocess, sys
proc = subprocess.run([sys.executable, '{Path(__file__).resolve()}', 'verify', {branch!r}], text=True)
sys.exit(proc.returncode)
""",
        encoding="utf-8",
    )
    verify_py.chmod(0o755)

    by_area: dict[str, dict[str, int]] = {}
    for item in included:
        area = item["path"].split("/")[0] if item["path"] != "." else "."
        bucket = by_area.setdefault(area, {"items": 0, "files": 0, "dirs": 0, "bytes": 0})
        bucket["items"] += 1
        bucket["files"] += 1 if item["path_type"] == "file" else 0
        bucket["dirs"] += 1 if item["path_type"] == "directory" else 0
        bucket["bytes"] += int(item["bytes"] or 0)

    report = bdir / "core_algorithm_1to1_report.md"
    with report.open("w", encoding="utf-8") as f:
        f.write(f"# {repo_title()} `{branch}` Core Algorithm 1:1 Research Report\n\n")
        f.write("## Executive Result\n\n")
        f.write("This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.\n\n")
        f.write("## Run Facts\n\n")
        facts = [
            ("Branch", branch),
            ("Repo", repo_id()),
            ("Source remote", str(active_repo()["source_remote"])),
            ("Source commit", commit),
            ("Source tree", tree),
            ("Read-only source export", str(source_dir(branch))),
            ("Codex model", MODEL),
            ("Reasoning effort", EFFORT),
            ("Worker slots", str(WORKER_SLOT_COUNT)),
            ("Worker jobs", str(worker_job_count)),
            ("Active worker refill target", str(ACTIVE_WORKER_TARGET)),
            ("Refill interval seconds", str(REPLENISH_INTERVAL_SECONDS)),
            ("Recursive source files excluding .git", str(sum(1 for r in inventory if r["path_type"] == "file"))),
            ("Recursive source directories excluding .git", str(sum(1 for r in inventory if r["path_type"] == "directory"))),
            ("Included core algorithm items", str(len(included))),
            ("Skipped non-core paths", str(len(skipped))),
            ("Status files complete", f"{verification['complete_status_files']} / {worker_job_count}"),
            ("Output files", f"{verification['output_files']} / {worker_job_count}"),
        ]
        for k, v in facts:
            f.write(f"- {k}: `{v}`\n")
        f.write("\n## Included Paths By Top-Level Area\n\n")
        f.write("| Area | Items | Files | Directories | Bytes represented |\n|---|---:|---:|---:|---:|\n")
        for area, c in sorted(by_area.items()):
            f.write(f"| `{area}` | {c['items']} | {c['files']} | {c['dirs']} | {c['bytes']} |\n")
        f.write("\n## Core Algorithm Synthesis\n\n")
        f.write("The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.\n\n")
        f.write("## Worker Assignment Summary\n\n")
        f.write("| Worker | Items | Bytes | Evidence |\n|---|---:|---:|---|\n")
        for row in assignments:
            f.write(f"| `{row['agent']}` | {row['item_count']} | {row['total_bytes']} | `research_runs/{run_id_for(branch)}/agents/{row['agent']}/output.md` |\n")
        f.write("\n## Verification\n\n")
        compact = {k: v for k, v in verification.items() if k != "problem_details"}
        f.write("```json\n" + json.dumps(compact, indent=2) + "\n```\n")
    print(json.dumps({k: v for k, v in verification.items() if k != "problem_details"}, indent=2))


def launch(branch: str) -> None:
    launcher = run_dir(branch) / "launch_tmux_codex_research.sh"
    run([str(launcher)], cwd=REPO_ROOT)


def refresh_launchers(branch: str | None = None) -> None:
    branches = [branch] if branch else remote_branches()
    refreshed = []
    missing = []
    for name in branches:
        rdir = run_dir(name)
        if not rdir.exists():
            missing.append(name)
            continue
        write_launcher_files(name)
        refreshed.append(name)
    print(json.dumps({"refreshed": refreshed, "missing_run_dirs": missing}, indent=2))


def remote_branches() -> list[str]:
    out = run(["git", "branch", "-r"], cwd=repo_path()).stdout
    branches = []
    for line in out.splitlines():
        item = line.strip()
        if not item.startswith("origin/") or item.startswith("origin/HEAD"):
            continue
        branches.append(item.removeprefix("origin/"))
    return sorted(branches)


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def branch_progress(branch: str) -> dict[str, object]:
    safe = branch_safe_name(branch)
    bdir = branch_dir(branch)
    commit = commit_for(branch)
    tree = tree_for(branch)
    research_rows = read_tsv(bdir / "research_list.tsv")
    path_rows = read_tsv(bdir / "path_inventory.tsv")
    run_path = run_dir(branch)
    skipped_rows = read_tsv(run_path / "skipped_paths.tsv")

    algorithm_items = len(research_rows)
    algorithm_directories = sum(1 for r in research_rows if r.get("path_type") == "directory")
    algorithm_files = sum(1 for r in research_rows if r.get("path_type") == "file")
    skipped_paths = len(skipped_rows) if skipped_rows else sum(1 for r in path_rows if r.get("included") == "no")

    if not bdir.exists():
        status = "not_started"
        status_files = 0
        complete_status_files = 0
        output_files = 0
        problems: int | str = ""
        notes = "Remote branch discovered; no branch folder prepared."
    else:
        verification = verify(branch) if research_rows else {
            "status_files": 0,
            "complete_status_files": 0,
            "output_files": 0,
            "problems": 1,
        }
        status_files = int(verification["status_files"])
        complete_status_files = int(verification["complete_status_files"])
        output_files = int(verification["output_files"])
        problems = int(verification["problems"])
        if problems == 0 and algorithm_items > 0:
            status = "complete"
            notes = "Completed 1:1 algorithm-subset learning report."
        else:
            status = "prepared_not_complete"
            notes = "Algorithm list and dynamic worker-job scaffolding prepared; worker outputs not complete."

    if branch == "h2-dev" and status != "complete":
        notes = "Only 2-series-looking remote branch name; prepared but not complete."

    return {
        "repo_id": repo_id(),
        "source_remote": active_repo()["source_remote"],
        "branch": branch,
        "safe_folder": safe,
        "source_commit": commit,
        "source_tree": tree,
        "research_status": status,
        "algorithm_items": algorithm_items,
        "algorithm_directories": algorithm_directories,
        "algorithm_files": algorithm_files,
        "skipped_paths": skipped_paths,
        "status_files": status_files,
        "complete_status_files": complete_status_files,
        "output_files": output_files,
        "verification_problems": problems,
        "report_path": rel_to_repo(bdir / "core_algorithm_1to1_report.md"),
        "notes": notes,
    }


def refresh_index() -> None:
    rows = []
    for rid in REPO_CONFIGS:
        set_active_repo(rid)
        for branch in remote_branches():
            rows.append(branch_progress(branch))

    branches_headers = [
        "repo_id",
        "source_remote",
        "branch",
        "safe_folder",
        "source_commit",
        "source_tree",
        "research_status",
        "algorithm_items",
        "algorithm_directories",
        "algorithm_files",
        "skipped_paths",
        "status_files",
        "complete_status_files",
        "output_files",
        "verification_problems",
        "report_path",
        "notes",
    ]
    write_tsv(LEARN_ROOT / "branches.tsv", branches_headers, rows)
    write_tsv(LEARN_ROOT / "progress.tsv", branches_headers, rows)

    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[str(row["research_status"])] = status_counts.get(str(row["research_status"]), 0) + 1

    prepared_count = sum(1 for row in rows if row["research_status"] in ("complete", "prepared_not_complete"))
    complete_rows = [row for row in rows if row["research_status"] == "complete"]
    incomplete_rows = [row for row in rows if row["research_status"] != "complete"]
    h2 = next((row for row in rows if row["repo_id"] == "humanize" and row["branch"] == "h2-dev"), None)
    two_three = run(
        ["git", "ls-remote", "--heads", "origin", "2.0", "3.0", "v2*", "v3*", "h2-dev", "h3*"],
        cwd=Path(REPO_CONFIGS["humanize"]["local_repo"]),
        check=False,
    ).stdout.strip()
    if not two_three:
        two_three = "(none)"
    repos_text = "\n".join(
        f"- `{rid}`: `{cfg['source_remote']}` local `{cfg['local_repo']}`"
        for rid, cfg in REPO_CONFIGS.items()
    )
    queue_headers = [
        "queue_status",
        "repo_id",
        "branch",
        "safe_folder",
        "algorithm_items",
        "algorithm_directories",
        "algorithm_files",
        "skipped_paths",
        "status_files",
        "complete_status_files",
        "output_files",
        "verification_problems",
        "source_commit",
        "source_tree",
        "report_path",
        "notes",
    ]
    queue_rows = []
    for row in rows:
        queue_row = dict(row)
        queue_row["queue_status"] = "done" if row["research_status"] == "complete" else "todo"
        queue_rows.append(queue_row)
    write_tsv(LEARN_ROOT / "research_queue.tsv", queue_headers, queue_rows)

    readme = LEARN_ROOT / "README.md"
    readme.write_text(
        f"""# Unified Humanize Research Index

This directory is the unified learning and research workspace for `PolyArch/humanize` plus `PolyArch/oh-my-humanize`.

## Current State

- Source repositories:
{repos_text}
- Target repository: `https://github.com/weiyangzen/weiyangzen.git`
- Local research root: `{LEARN_ROOT}`
- Remote repo/branch entries discovered on 2026-06-19: `{len(rows)}`
- Branch folders with algorithm research lists: `{prepared_count}`
- Completed 1:1 algorithm learning branches: `{len(complete_rows)}`
- Branches still needing worker completion: `{len(incomplete_rows)}`

## 2.0 / 3.0 Branch Check

`git ls-remote --heads origin '2.0' '3.0' 'v2*' 'v3*' 'h2-dev' 'h3*'` returned:

```text
{two_three}
```

There is no remote branch named `2.0` or `3.0` at this snapshot. `h2-dev` exists and is the only 2-series-looking branch name found.

## What Counts As Research Here

This is algorithm-subset learning research, not full repository documentation. Each branch folder contains:

- `path_inventory.tsv`: full path inventory with included/skipped decisions.
- `research_list.tsv`: locked algorithm/core subset for 1:1 learning.
- `assignment.tsv`: worker-job assignment plan.
- `execution_blueprint.md`: dual-cursor checklist.
- `todos_20260619.md`: current todo snapshot.
- `research_runs/.../agents/agent_*/output.md`: worker learning output when complete.
- `coverage_matrix.tsv` and `core_algorithm_1to1_report.md`: final accepted branch output when complete.

Non-core installation docs, binary/visual assets, CI-only files, fixtures, and mock data are skipped with explicit reasons in each branch's `skipped_paths.tsv`.

## Status Counts

```text
{os.linesep.join(f"{status}: {count}" for status, count in sorted(status_counts.items()))}
```

## Index Files

- `branches.tsv`: all discovered remote branches and current research status.
- `progress.tsv`: same schema as `branches.tsv`, regenerated for progress polling.
- `research_queue.tsv`: unified cross-repo todo/done queue for worker claiming.
- `cross_branch_summary.md`: human-readable cross-branch status and scope notes.
- `tools/branch_research.py`: preparation, launch, verify, finalize, and index helper.
""",
        encoding="utf-8",
    )

    summary = LEARN_ROOT / "cross_branch_summary.md"
    complete_names = ", ".join(f"`{row['repo_id']}/{row['branch']}`" for row in complete_rows) or "none"
    next_names = ", ".join(f"`{row['repo_id']}/{row['branch']}`" for row in incomplete_rows[:10])
    if len(incomplete_rows) > 10:
        next_names += f", ... ({len(incomplete_rows)} total incomplete)"
    h2_line = "not present"
    if h2:
        h2_line = f"{h2['research_status']} with {h2['algorithm_items']} algorithm items"
    summary.write_text(
        f"""# Unified Humanize Cross-Repo Research Summary

Snapshot date: 2026-06-19

## Direct Answers

- Source remotes:
{repos_text}
- Remote repo/branch entries discovered: `{len(rows)}`.
- Branch folders with algorithm lists: `{prepared_count}`.
- Completed branch research count: `{len(complete_rows)}`.
- Completed branches: {complete_names}.
- Research scope: algorithm-related subset only.
- `2.0` branch researched: no. `origin/2.0` does not exist in the fetched remote branch list.
- `3.0` branch researched: no. `origin/3.0` does not exist in the fetched remote branch list.
- `h2-dev`: {h2_line}.

## Status Counts

```text
{os.linesep.join(f"{status}: {count}" for status, count in sorted(status_counts.items()))}
```

## Current Next Branches Needing Worker Completion

{next_names}

## Scope Rule

The current research scope is the fuzzy `algorithm subset`, resolved per branch into:

- Included: behavior-defining docs, commands, agents, config, hooks, prompt templates, runtime scripts, skills, templates, and tests.
- Skipped: CI-only files, installation-only docs, local assistant/plugin metadata, binary/visual assets, fixtures, mocks, and other non-core content.

For each prepared branch, the exact include/skip decision is recorded in `path_inventory.tsv` and `skipped_paths.tsv`.
""",
        encoding="utf-8",
    )
    print(json.dumps({"branches": len(rows), "prepared": prepared_count, "status_counts": status_counts}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", choices=sorted(REPO_CONFIGS), default=ACTIVE_REPO_ID)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("prepare", "launch", "finalize", "verify"):
        p = sub.add_parser(name)
        p.add_argument("branch")
    p = sub.add_parser("refresh-launchers")
    p.add_argument("branch", nargs="?")
    sub.add_parser("refresh-index")
    args = parser.parse_args()
    set_active_repo(args.repo)
    if args.cmd == "prepare":
        prepare(args.branch)
    elif args.cmd == "launch":
        launch(args.branch)
    elif args.cmd == "finalize":
        finalize(args.branch)
    elif args.cmd == "verify":
        result = verify(args.branch)
        print(json.dumps({k: v for k, v in result.items() if k != "problem_details"}, indent=2))
        if result["problems"]:
            print(json.dumps(result["problem_details"], indent=2))
            raise SystemExit(1)
    elif args.cmd == "refresh-launchers":
        refresh_launchers(args.branch)
    elif args.cmd == "refresh-index":
        refresh_index()


if __name__ == "__main__":
    main()
