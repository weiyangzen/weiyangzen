# agent_13 add-shell-syntax-check-cicd 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `6e0eebdb803522cd4be735589be4d1d76e8e536e`

## Item Evidence

### ADD_SHELL_SYNTAX_CHECK_CICD-HZ-013 `file` `hooks/loop-edit-validator.sh`
- cursor: `[_]`
- core_role:
  - `hooks/loop-edit-validator.sh` is a Claude Code `PreToolUse` guard for the RLCR loop’s `Edit` tool path validation.
  - It protects loop-owned control artifacts from direct Claude edits and enforces that round summary edits target the currently active round.
  - It is registered in `hooks/hooks.json:14-21` under `PreToolUse` matcher `Edit`, with command `${CLAUDE_PLUGIN_ROOT}/hooks/loop-edit-validator.sh`.
  - The README lists it as part of the lifecycle hook set at `README.md:223-232`.

- algorithmic_behavior:
  - Bootstraps as strict Bash with `set -euo pipefail` at `hooks/loop-edit-validator.sh:12`, then resolves its own directory and sources `hooks/lib/loop-common.sh` at `hooks/loop-edit-validator.sh:15-16`.
  - Reads the entire hook JSON payload from stdin into `HOOK_INPUT` at `hooks/loop-edit-validator.sh:22`.
  - Extracts `.tool_name` with `jq`; if the tool is not exactly `Edit`, it exits success immediately at `hooks/loop-edit-validator.sh:23-27`.
  - Extracts `.tool_input.file_path`, lowercases it, then performs global filename gates before checking loop-local state at `hooks/loop-edit-validator.sh:29-44`.
  - Blocks any path whose lowercase filename matches `round-[0-9]+-todos.md` by calling `todos_blocked_message "Edit"` and exiting `2` at `hooks/loop-edit-validator.sh:36-39`.
  - Blocks any path whose lowercase filename matches `round-[0-9]+-prompt.md` by calling `prompt_write_blocked_message` and exiting `2` at `hooks/loop-edit-validator.sh:41-44`.
  - If the file is not inside `.humanize-loop.local/`, the validator allows the edit at `hooks/loop-edit-validator.sh:50-52`.
  - For loop-local paths, it resolves `PROJECT_ROOT` from `CLAUDE_PROJECT_DIR` or `pwd`, sets `LOOP_BASE_DIR`, and finds the active loop with `find_active_loop` at `hooks/loop-edit-validator.sh:58-60`.
  - If no active loop exists, it allows the edit at `hooks/loop-edit-validator.sh:62-64`; this avoids blocking stale or absent loop directories.
  - Reads current round from active `state.md` via `get_current_round` at `hooks/loop-edit-validator.sh:66`.
  - Blocks direct edits to any `state.md` path under loop scope at `hooks/loop-edit-validator.sh:72-75`.
  - Blocks `goal-tracker.md` edits after round `0`, routing the user to the current round summary via `goal_tracker_blocked_message`, at `hooks/loop-edit-validator.sh:81-85`.
  - For summary files, extracts the filename beneath `.humanize-loop.local/.../` using two sed patterns and compares the embedded round number against `CURRENT_ROUND` at `hooks/loop-edit-validator.sh:91-115`.
  - If the summary round number is wrong, emits a “Wrong Round Number” message including the correct active summary path and exits `2` at `hooks/loop-edit-validator.sh:101-112`.
  - Success path is `exit 0` at `hooks/loop-edit-validator.sh:117`.

- inputs_outputs_state:
  - Input is Claude hook JSON on stdin, expected to contain `.tool_name` and `.tool_input.file_path`; parsing is done with `jq` at `hooks/loop-edit-validator.sh:22-30`.
  - Output on success is no stdout/stderr and exit code `0`.
  - Output on rejection is a Markdown diagnostic on stderr and exit code `2`.
  - State read:
    - `CLAUDE_PROJECT_DIR`, if set, defines the project root; otherwise the script uses `pwd` at `hooks/loop-edit-validator.sh:58`.
    - `.humanize-loop.local` under the project root is scanned for active loop state at `hooks/loop-edit-validator.sh:59-60`.
    - Active loop selection is delegated to `find_active_loop`, which checks only the newest timestamp-like subdirectory and requires `state.md` to exist, per `hooks/lib/loop-common.sh:15-33`.
    - Current round is parsed from YAML-ish frontmatter key `current_round:` and defaults to `0` if missing, per `hooks/lib/loop-common.sh:37-47`.
  - State written:
    - None. This validator is read-only by design; it gates the proposed edit before the edit tool runs.
  - State transition model:
    - Non-`Edit` hook payload: unchecked passthrough.
    - `Edit` to todos or prompt file: hard blocked independent of active loop state.
    - `Edit` outside `.humanize-loop.local/`: allowed after todos/prompt filename checks.
    - `Edit` inside `.humanize-loop.local/` with no active loop: allowed.
    - `Edit` inside active loop targeting `state.md`: blocked.
    - `Edit` inside active loop targeting `goal-tracker.md` during round `0`: allowed.
    - `Edit` inside active loop targeting `goal-tracker.md` during round `>0`: blocked.
    - `Edit` to `round-N-summary.md` when `N == current_round`: allowed.
    - `Edit` to `round-N-summary.md` when `N != current_round`: blocked with correction path.

- gates_or_invariants:
  - Todo files must not be edited through `Edit`; users are directed to native TodoWrite by the shared message in `hooks/lib/loop-common.sh:75-90`.
  - Prompt files are read-only instructions from Codex to Claude; writes/edits are blocked by `prompt_write_blocked_message` in `hooks/lib/loop-common.sh:92-108`.
  - Loop `state.md` is owned by the loop system, not Claude edits, enforced by `is_state_file_path` and `state_file_blocked_message` in `hooks/lib/loop-common.sh:110-124` and `hooks/lib/loop-common.sh:166-170`.
  - `goal-tracker.md` becomes Codex-owned after round `0`; the gate depends on numeric `CURRENT_ROUND > 0` at `hooks/loop-edit-validator.sh:81`.
  - Summary edits must not self-increment the round number; the summary filename round must match the active loop state at `hooks/loop-edit-validator.sh:99-112`.
  - File type detection is case-insensitive because `FILE_PATH_LOWER` is used for filename checks at `hooks/loop-edit-validator.sh:30`, with lowercase conversion implemented at `hooks/lib/loop-common.sh:49-52`.
  - Round file matching is anchored to end-of-path with regex `round-[0-9]+-${file_type}\.md$` in `hooks/lib/loop-common.sh:54-61`.
  - The validator does not enforce that an allowed summary path is under the active loop directory; unlike `loop-write-validator.sh`, this edit validator only checks the embedded round number for summaries. The sibling write validator performs stricter directory correction at `hooks/loop-write-validator.sh:157-171`.

- dependencies_and_callers:
  - Runtime dependencies:
    - `bash`.
    - `jq` for JSON extraction at `hooks/loop-edit-validator.sh:23` and `hooks/loop-edit-validator.sh:29`.
    - POSIX-ish utilities: `cat`, `tr`, `grep`, `sed`, `ls`, `sort`, `head`.
    - Shared hook library `hooks/lib/loop-common.sh`.
  - Shared functions used:
    - `to_lower`, `is_round_file_type`, `todos_blocked_message`, `prompt_write_blocked_message`, `is_in_humanize_loop_dir`, `find_active_loop`, `get_current_round`, `is_state_file_path`, `state_file_blocked_message`, `is_goal_tracker_path`, `goal_tracker_blocked_message`, and `extract_round_number`.
  - Caller:
    - Claude plugin hook registration in `hooks/hooks.json:14-21`.
  - Sibling coordination:
    - `loop-write-validator.sh` implements related `Write`-tool gates and has stricter summary-location validation, including blocking summary writes outside `.humanize-loop.local` and checking exact active loop directory path at `hooks/loop-write-validator.sh:107-171`.
    - `loop-read-validator.sh`, `loop-bash-validator.sh`, and `loop-codex-stop-hook.sh` are listed in the hook suite at `hooks/hooks.json:23-50`, but this assigned file specifically handles `Edit`.

- edge_cases_or_failure_modes:
  - Missing or malformed `jq` input can fail under `set -euo pipefail`; the script assumes valid Claude hook JSON and available `jq`.
  - Empty `file_path` becomes an empty string; it is not a todos/prompt path, not inside `.humanize-loop.local/`, and exits allowed at `hooks/loop-edit-validator.sh:29-52`.
  - `find_active_loop` only considers the newest loop directory by reverse lexical sort; older directories with `state.md` are intentionally ignored to avoid reviving stale loops, per `hooks/lib/loop-common.sh:11-33`.
  - If the newest loop directory lacks `state.md`, `find_active_loop` returns empty and loop-local edits are allowed at `hooks/loop-edit-validator.sh:62-64`.
  - If `current_round:` is missing or unparsable, `get_current_round` defaults to `0`; that means goal tracker edits are allowed and only `round-0-summary.md` is considered current.
  - `[[ "$CURRENT_ROUND" -gt 0 ]]` expects an integer. A non-numeric `current_round` value could cause a Bash integer comparison error and abort because of `set -e`.
  - `is_in_humanize_loop_dir` is a substring regex check for `.humanize-loop.local/`, not canonical path normalization, at `hooks/lib/loop-common.sh:172-176`.
  - Summary filename extraction handles one nested loop directory and a fallback direct loop path at `hooks/loop-edit-validator.sh:91-96`; unusual deeper layouts may still produce a filename string that includes slashes.
  - The edit validator checks summary round correctness but does not block summary files outside `.humanize-loop.local/` unless they already match todos/prompt gates; this is an intentional or residual asymmetry versus `loop-write-validator.sh`.
  - Direct Bash modifications are outside this file’s scope and are handled by `loop-bash-validator.sh` through the separate `Bash` hook registration.

- validation_or_tests:
  - Direct syntax validation was run read-only:
    - `bash -n hooks/loop-edit-validator.sh` exited `0`.
    - `bash -n hooks/lib/loop-common.sh` exited `0`.
  - Reference search found hook registration and documentation references, but no direct test fixture for `loop-edit-validator.sh` in the inspected tree:
    - `hooks/hooks.json:19` registers the assigned validator.
    - `README.md:227` lists it in the hook directory.
    - Search for `shellcheck`, `bash -n`, `shfmt`, and `loop-edit-validator` found no CI/test script beyond hook registration and docs.
  - `find` for common shallow test/config markers produced no matching files in the checked scope, so no repository-native test command was identified from this export.
  - No files were modified.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1/1 item evidence section present; exact item id appears only in that section header`
- missing_items: `0`
- duplicate_items: `0`
- final_worker_status: `complete`