# agent_14 add-shell-syntax-check-cicd 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `6e0eebdb803522cd4be735589be4d1d76e8e536e`

## Item Evidence

### ADD_SHELL_SYNTAX_CHECK_CICD-HZ-014 `file` `hooks/loop-read-validator.sh`
- cursor: `[_]`
- core_role:
  - `hooks/loop-read-validator.sh` is the Claude Code `PreToolUse` Read validator for RLCR loop artifacts. It protects the loop’s current-round prompt and summary read path so Claude reads only the active loop session’s current `round-N-prompt.md` or `round-N-summary.md`, and it blocks `round-N-todos.md` access entirely in favor of native todo tooling.
  - It is registered under the `Read` matcher in `hooks/hooks.json:24-29`, so its intended caller is the Claude hook runtime, not a direct user command.
  - It is part of the hook/validator layer described in `README.md:223-232`, where it sits alongside write, edit, bash, and stop hooks.

- algorithmic_behavior:
  - The script runs with `set -euo pipefail` at `hooks/loop-read-validator.sh:12`, then sources shared RLCR helper functions from `hooks/lib/loop-common.sh` at `hooks/loop-read-validator.sh:14-16`.
  - It reads the hook JSON payload from stdin, extracts `.tool_name` with `jq`, and immediately allows anything other than `Read` by exiting `0` at `hooks/loop-read-validator.sh:22-27`.
  - For `Read`, it extracts `.tool_input.file_path`, lowercases it, and evaluates filename predicates at `hooks/loop-read-validator.sh:29-31`.
  - It first applies the hard todos gate: any path ending like `round-[digits]-todos.md` is blocked with `todos_blocked_message "Read"` and exit code `2` at `hooks/loop-read-validator.sh:32-39`. The shared predicate is `is_round_file_type`, implemented as a suffix regex at `hooks/lib/loop-common.sh:54-61`.
  - It then classifies only `summary` and `prompt` round files as guarded files. If the target is not a `round-N-summary.md` or `round-N-prompt.md` suffix, the script allows the read at `hooks/loop-read-validator.sh:45-55`.
  - For guarded prompt/summary files, it checks whether the requested path contains `.humanize-loop.local/` at `hooks/loop-read-validator.sh:57-61`; the helper is a substring regex at `hooks/lib/loop-common.sh:172-176`.
  - It locates loop state from `PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"` and `$PROJECT_ROOT/.humanize-loop.local`, then calls `find_active_loop` at `hooks/loop-read-validator.sh:67-69`.
  - If no active loop exists, it allows the read at `hooks/loop-read-validator.sh:71-73`. This makes the hook inert outside an active RLCR session.
  - It reads the active current round from `$ACTIVE_LOOP_DIR/state.md` via `get_current_round` at `hooks/loop-read-validator.sh:75`; the helper parses YAML frontmatter for `current_round:` and defaults to `0` at `hooks/lib/loop-common.sh:35-47`.
  - It extracts the round number from the requested basename at `hooks/loop-read-validator.sh:81-84`; malformed names that passed earlier classification but do not yield a round number are allowed.
  - It derives the guarded file type as `summary` or `prompt` at `hooks/loop-read-validator.sh:86-92`.
  - It applies three ordered validation gates:
    - Location gate: if the path is not under `.humanize-loop.local/`, it blocks with “Wrong File Location” and prints the current prompt/summary paths at `hooks/loop-read-validator.sh:98-112`.
    - Round gate: if requested `CLAUDE_ROUND` differs from `CURRENT_ROUND`, it blocks with “Wrong Round File” at `hooks/loop-read-validator.sh:118-131`.
    - Exact active-directory gate: it constructs `$ACTIVE_LOOP_DIR/$CLAUDE_FILENAME` and blocks any path that is under `.humanize-loop.local/` but not in the active session directory at `hooks/loop-read-validator.sh:137-149`.
  - If all gates pass, the read is allowed with exit `0` at `hooks/loop-read-validator.sh:151`.

- inputs_outputs_state:
  - Inputs:
    - Hook JSON on stdin, expected to contain `tool_name` and `tool_input.file_path` (`hooks/loop-read-validator.sh:22-30`).
    - `jq` for JSON field extraction (`hooks/loop-read-validator.sh:23`, `hooks/loop-read-validator.sh:29`).
    - Environment variable `CLAUDE_PROJECT_DIR`; if absent, current working directory is used as the project root (`hooks/loop-read-validator.sh:67`).
    - Filesystem state under `.humanize-loop.local/<timestamp>/`, especially `state.md` (`hooks/loop-read-validator.sh:68-75`).
    - Shared helpers from `hooks/lib/loop-common.sh`, including filename classification, active-loop discovery, current-round parsing, and block messages.
  - Outputs:
    - Exit `0` allows the Read tool to proceed.
    - Exit `2` blocks the Read tool and writes human-readable guidance to stderr (`hooks/loop-read-validator.sh:36-39`, `hooks/loop-read-validator.sh:98-112`, `hooks/loop-read-validator.sh:118-131`, `hooks/loop-read-validator.sh:139-149`).
    - The script does not write or mutate repository state.
  - State model:
    - It observes RLCR state rather than advancing it. The current round is authoritative in `state.md`.
    - Initial state is created by `scripts/setup-rlcr-loop.sh`, which writes `state.md` with `current_round: 0` at `scripts/setup-rlcr-loop.sh:223-234` and creates initial round files around `scripts/setup-rlcr-loop.sh:334-336`.
    - Later round advancement is handled by the stop hook, not this read validator; references show `hooks/loop-codex-stop-hook.sh` updates `current_round` and creates next prompt/summary files around `hooks/loop-codex-stop-hook.sh:866-871`.
    - Active session selection is “newest timestamped subdirectory with `state.md`”, implemented in `find_active_loop` at `hooks/lib/loop-common.sh:11-33`.

- gates_or_invariants:
  - Non-Read tools are outside this validator’s scope and pass through unchanged (`hooks/loop-read-validator.sh:25-27`).
  - `round-N-todos.md` is always blocked for Read, independent of active loop state, because todos should use native TodoWrite (`hooks/loop-read-validator.sh:32-39`; message text at `hooks/lib/loop-common.sh:75-90`).
  - Only prompt and summary round files are governed by this script after the todos gate (`hooks/loop-read-validator.sh:48-55`).
  - A guarded read is valid only when all of these are true:
    - An active loop directory exists under the project root.
    - The file path contains `.humanize-loop.local/`.
    - The file’s round number equals `current_round`.
    - The exact path equals `$ACTIVE_LOOP_DIR/<basename>`.
  - The exact-path comparison at `hooks/loop-read-validator.sh:137-149` prevents reading a same-round prompt/summary from an older session directory.
  - The helper’s active-loop invariant ignores older sessions even if they contain `state.md`; only the newest directory is considered active (`hooks/lib/loop-common.sh:11-15`, `hooks/lib/loop-common.sh:23-31`).
  - Case handling is asymmetric: filename pattern checks use a lowercased path, but exact path comparison uses the original `FILE_PATH`. This is appropriate on case-sensitive paths and stricter on case-insensitive paths.

- dependencies_and_callers:
  - Direct registration/caller:
    - `hooks/hooks.json:24-29` maps Claude `PreToolUse` Read events to `${CLAUDE_PLUGIN_ROOT}/hooks/loop-read-validator.sh`.
  - Shared helper dependency:
    - `hooks/lib/loop-common.sh:15-33` provides `find_active_loop`.
    - `hooks/lib/loop-common.sh:37-47` provides `get_current_round`.
    - `hooks/lib/loop-common.sh:49-52` provides `to_lower`.
    - `hooks/lib/loop-common.sh:56-61` provides `is_round_file_type`.
    - `hooks/lib/loop-common.sh:66-73` provides `extract_round_number`.
    - `hooks/lib/loop-common.sh:77-90` provides `todos_blocked_message`.
    - `hooks/lib/loop-common.sh:173-176` provides `is_in_humanize_loop_dir`.
  - Producer/coordinator scripts:
    - `scripts/setup-rlcr-loop.sh` creates the `.humanize-loop.local/<timestamp>/state.md` frontmatter consumed by this hook (`scripts/setup-rlcr-loop.sh:207-234`).
    - `scripts/setup-rlcr-loop.sh` creates initial prompt/summary artifacts using the same `round-N-*` naming convention (`scripts/setup-rlcr-loop.sh:334-336`).
    - `hooks/loop-codex-stop-hook.sh` is the round-advancing coordinator; repository search shows it reads `current_round`, validates summary presence, updates state, and creates next-round prompt/summary files.
  - Sibling validator coordination:
    - `hooks/loop-write-validator.sh` applies complementary write-side gates for todos, prompts, summaries, state, and goal tracker (`hooks/loop-write-validator.sh:34-45`, `hooks/loop-write-validator.sh:88-120`, `hooks/loop-write-validator.sh:139-171`).
    - `hooks/loop-edit-validator.sh` applies complementary edit-side gates for todos, prompts, state, goal tracker, and summary round numbers (`hooks/loop-edit-validator.sh:32-44`, `hooks/loop-edit-validator.sh:68-115`).
  - External tools:
    - Requires `bash`, `jq`, `sed`, `grep`, `sort`, `head`, `basename`, `tr`, and filesystem access to the project loop directory.
    - The branch’s new CI workflow `.github/workflows/shell-syntax-check.yml` discovers all `*.sh` files and runs `bash -n` and `zsh -n` over them (`.github/workflows/shell-syntax-check.yml:19-60`), so this file is in that validation surface.

- edge_cases_or_failure_modes:
  - Missing or inactive loop directory: if `.humanize-loop.local` is absent, has no timestamp children, or the newest child lacks `state.md`, `find_active_loop` returns empty and this validator allows prompt/summary reads (`hooks/lib/loop-common.sh:18-33`, `hooks/loop-read-validator.sh:71-73`). This avoids false blocks outside a running loop but means stale files are not protected when no active loop is detected.
  - Newest-directory-only policy: an older directory with valid state is ignored even if it appears active; this intentionally prevents “zombie” loop revival (`hooks/lib/loop-common.sh:11-15`).
  - Corrupt or missing `current_round:` defaults to `0` rather than blocking (`hooks/lib/loop-common.sh:40-47`). A bad state file can therefore cause round-0 files to be treated as current.
  - `jq` failure or invalid JSON will terminate the script because of `set -e`; that is likely a hard hook failure rather than a graceful allow/block.
  - Paths containing `.humanize-loop.local/` outside the actual project root can pass the location substring gate but will still fail the exact active-directory comparison unless they equal `$ACTIVE_LOOP_DIR/<basename>` (`hooks/loop-read-validator.sh:57-61`, `hooks/loop-read-validator.sh:137-149`).
  - The filename is derived with `basename`, so nested files under an active loop directory with a basename matching current prompt/summary are blocked unless the whole path exactly equals the active loop root file (`hooks/loop-read-validator.sh:50`, `hooks/loop-read-validator.sh:137-149`).
  - The regex classifies only suffixes matching `round-[0-9]+-{summary,prompt,todos}.md`; files like `round-01-summary.md` are valid and compare numerically as strings against `CURRENT_ROUND`, so `01` differs from `1`.
  - The block messages suggest using `cat $FILE_PATH` for blocked reads (`hooks/loop-read-validator.sh:109`, `hooks/loop-read-validator.sh:128`, `hooks/loop-read-validator.sh:146`). That is an intentional escape hatch for exceptional access, but it also means Bash read access is not blocked by this Read hook.

- validation_or_tests:
  - Direct read-only validation performed:
    - `bash -n hooks/loop-read-validator.sh && bash -n hooks/lib/loop-common.sh` exited `0`.
    - `zsh -n hooks/loop-read-validator.sh && zsh -n hooks/lib/loop-common.sh` exited `0`.
  - CI coverage:
    - `.github/workflows/shell-syntax-check.yml` checks all `*.sh` files with Bash syntax validation at `.github/workflows/shell-syntax-check.yml:29-44`.
    - The same workflow checks all `*.sh` files with Zsh syntax validation at `.github/workflows/shell-syntax-check.yml:46-60`.
  - I did not find a dedicated tests/spec directory in the branch export; `rg --files hooks .github scripts tests test spec` reported missing `tests`, `test`, and `spec` paths while listing the shell hooks and workflows.
  - No behavioral unit tests for hook JSON scenarios were observed during this item review; validation evidence is syntax-oriented plus manual algorithm inspection.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `ADD_SHELL_SYNTAX_CHECK_CICD-HZ-014`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`