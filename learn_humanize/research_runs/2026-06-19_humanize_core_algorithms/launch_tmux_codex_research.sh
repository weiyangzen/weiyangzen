#!/usr/bin/env bash
set -euo pipefail

RUN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="${SOURCE_ROOT:-/Users/wangweiyang/GitHub/humanize}"
TOPICS_FILE="$RUN_ROOT/topics.tsv"
SESSION="${SESSION:-humanize_core_20260619}"
MODEL="${MODEL:-gpt-5.5}"
EFFORT="${EFFORT:-xhigh}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-7200}"

mkdir -p "$RUN_ROOT/prompts" "$RUN_ROOT/agents" "$RUN_ROOT/logs" "$RUN_ROOT/status"

if [[ ! -d "$SOURCE_ROOT/.git" ]]; then
  echo "missing SOURCE_ROOT git repository: $SOURCE_ROOT" >&2
  exit 1
fi
if [[ ! -f "$TOPICS_FILE" ]]; then
  echo "missing topics file: $TOPICS_FILE" >&2
  exit 1
fi
if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is required" >&2
  exit 1
fi
if ! command -v codex >/dev/null 2>&1; then
  echo "codex is required" >&2
  exit 1
fi
CODEX_BIN="$(command -v codex)"
PYTHON_BIN="$(command -v python3 || true)"
if [[ -z "$PYTHON_BIN" ]]; then
  echo "python3 is required for portable timeout handling" >&2
  exit 1
fi

git -C "$SOURCE_ROOT" rev-parse HEAD > "$RUN_ROOT/source_commit.txt"
{
  echo "run_started_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "source_root=$SOURCE_ROOT"
  echo "source_commit=$(cat "$RUN_ROOT/source_commit.txt")"
  echo "tmux_session=$SESSION"
  echo "model=$MODEL"
  echo "reasoning_effort=$EFFORT"
  echo "timeout_seconds=$TIMEOUT_SECONDS"
} > "$RUN_ROOT/run_manifest.env"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already exists: $SESSION" >&2
  echo "attach with: tmux attach -t $SESSION" >&2
  exit 1
fi

create_agent_files() {
  local id="$1"
  local title="$2"
  local focus_paths="$3"
  local agent_dir="$RUN_ROOT/agents/agent_${id}"
  local prompt_file="$RUN_ROOT/prompts/agent_${id}.md"
  local runner="$agent_dir/run.sh"
  local timeout_runner="$agent_dir/timeout_run.py"

  mkdir -p "$agent_dir"

  {
    echo "# Humanize Core Algorithm Research - Agent $id"
    echo
    echo "You are one of 30 parallel research agents. Work read-only."
    echo
    echo "Repository root: $SOURCE_ROOT"
    echo "Pinned source commit: $(cat "$RUN_ROOT/source_commit.txt")"
    echo "Topic: $title"
    echo "Focus paths: $focus_paths"
    echo
    echo "Task:"
    echo "1. Inspect only the algorithm-relevant subset for this topic. Skip installation, marketing, screenshots, and generic usage text unless it defines behavior."
    echo "2. Extract the core mechanism as an algorithm: state variables, inputs, transitions, gates, scoring/routing rules, failure modes, and invariants."
    echo "3. Cite source evidence with file paths and line numbers. Use rg, sed, nl, or similar read-only commands."
    echo "4. Produce concise Markdown in Chinese. Keep it technical and evidence-backed."
    echo
    echo "Output format:"
    echo "- Topic and conclusion"
    echo "- Algorithm subset covered"
    echo "- Pseudocode or transition table"
    echo "- Source evidence"
    echo "- Edge cases and risks"
    echo "- What is explicitly out of scope"
    echo
    echo "Do not edit files. Do not commit. Do not run network searches."
  } > "$prompt_file"

  {
    echo "#!/usr/bin/env python3"
    echo "import subprocess"
    echo "import sys"
    echo
    echo "timeout_seconds = int(sys.argv[1])"
    echo "stdin_path, stdout_path, stderr_path = sys.argv[2:5]"
    echo "cmd = sys.argv[5:]"
    echo "with open(stdin_path, 'rb') as stdin_f, open(stdout_path, 'wb') as stdout_f, open(stderr_path, 'wb') as stderr_f:"
    echo "    try:"
    echo "        proc = subprocess.run(cmd, stdin=stdin_f, stdout=stdout_f, stderr=stderr_f, timeout=timeout_seconds)"
    echo "        raise SystemExit(proc.returncode)"
    echo "    except subprocess.TimeoutExpired:"
    echo "        stderr_f.write(f'portable timeout expired after {timeout_seconds}s\\n'.encode())"
    echo "        raise SystemExit(124)"
  } > "$timeout_runner"
  chmod +x "$timeout_runner"

  {
    echo "#!/usr/bin/env bash"
    echo "set -euo pipefail"
    echo "AGENT_DIR=\"$agent_dir\""
    echo "PROMPT_FILE=\"$prompt_file\""
    echo "OUT_FILE=\"\$AGENT_DIR/output.md\""
    echo "STDOUT_FILE=\"\$AGENT_DIR/stdout.log\""
    echo "STDERR_FILE=\"\$AGENT_DIR/stderr.log\""
    echo "STATUS_FILE=\"$RUN_ROOT/status/agent_${id}.status\""
    echo "echo running > \"\$STATUS_FILE\""
    echo "echo \"started_utc=\$(date -u +%Y-%m-%dT%H:%M:%SZ)\" > \"\$AGENT_DIR/metadata.env\""
    echo "echo \"topic=$title\" >> \"\$AGENT_DIR/metadata.env\""
    echo "echo \"codex_bin=$CODEX_BIN\" >> \"\$AGENT_DIR/metadata.env\""
    echo "set +e"
    echo "\"$PYTHON_BIN\" \"$timeout_runner\" \"$TIMEOUT_SECONDS\" \"\$PROMPT_FILE\" \"\$STDOUT_FILE\" \"\$STDERR_FILE\" \"$CODEX_BIN\" -a never exec -m \"$MODEL\" -c model_reasoning_effort=\"$EFFORT\" -C \"$SOURCE_ROOT\" -s read-only --ephemeral -o \"\$OUT_FILE\" -"
    echo "code=\$?"
    echo "set -e"
    echo "echo \"finished_utc=\$(date -u +%Y-%m-%dT%H:%M:%SZ)\" >> \"\$AGENT_DIR/metadata.env\""
    echo "echo \"exit_code=\$code\" >> \"\$AGENT_DIR/metadata.env\""
    echo "if [[ \$code -eq 0 && -s \"\$OUT_FILE\" ]]; then echo complete > \"\$STATUS_FILE\"; else echo failed:\$code > \"\$STATUS_FILE\"; fi"
    echo "exit \$code"
  } > "$runner"
  chmod +x "$runner"
}

count=0
while IFS=$'\t' read -r id title focus_paths; do
  [[ "$id" == "id" ]] && continue
  [[ -z "${id:-}" ]] && continue
  create_agent_files "$id" "$title" "$focus_paths"
  count=$((count + 1))
done < "$TOPICS_FILE"

if [[ "$count" -ne 30 ]]; then
  echo "expected 30 topics, found $count" >&2
  exit 1
fi

first_runner="$RUN_ROOT/agents/agent_01/run.sh"
tmux new-session -d -s "$SESSION" -n "agent01" "bash '$first_runner'; printf '\\n[agent01 done] press Ctrl-b d to detach or inspect logs\\n'; exec bash"

for id in $(seq -w 2 30); do
  runner="$RUN_ROOT/agents/agent_${id}/run.sh"
  tmux new-window -t "$SESSION:" -n "agent${id}" "bash '$runner'; printf '\\n[agent${id} done] press Ctrl-b d to detach or inspect logs\\n'; exec bash"
done

echo "launched $count codex research agents in tmux session: $SESSION"
echo "attach: tmux attach -t $SESSION"
echo "status: find '$RUN_ROOT/status' -type f -name '*.status' -maxdepth 1 -print -exec cat {} \\;"
