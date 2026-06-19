# agent_21 improve-monitor-script 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `5af20b79e6fec323a2d5cb9344a6a584db1c635a`

## Item Evidence

### IMPROVE_MONITOR_SCRIPT-HZ-021 `file` `hooks/loop-write-validator.sh`
- cursor: `[_]`
- core_role: PreToolUse `Write` guard for the RLCR loop. It prevents writes that would corrupt loop-owned control surfaces: todos files, prompt files, wrong-round summaries, summaries outside the active loop directory, `state.md`, loop backup `plan.md`, and post-round-0 `goal-tracker.md`. It is registered as the `Write` validator in `hooks/hooks.json:14-21`.

- algorithmic_behavior: The script reads the hook JSON from stdin, extracts `.tool_name` and `.tool_input.file_path` with `jq`, and exits immediately unless the tool is `Write` (`hooks/loop-write-validator.sh:23-30`). It lowercases the target path for pattern detection (`:31`). It first blocks `round-N-todos.md` writes unless the path is allowlisted for the active loop (`:37-44`) and blocks all `round-N-prompt.md` writes (`:47-50`). It then classifies whether the target is a summary file or inside `.humanize/rlcr/` (`:56-61`). Normal project files are allowed. Non-summary files inside the loop directory are allowed unless they are `state.md`, `goal-tracker.md`, or `plan.md` (`:64-72`). For protected loop files, it finds the newest active loop, parses `state.md`, and applies state-specific gates (`:78-89`).

- inputs_outputs_state: Inputs are Claude hook stdin JSON, `CLAUDE_PROJECT_DIR` or `pwd`, the active loop tree under `.humanize/rlcr`, `state.md`, and block templates loaded through `hooks/lib/loop-common.sh`. Outputs are process status only: exit `0` allows the write, exit `2` blocks it with a rendered message on stderr. It does not mutate state. Its state-machine role is to keep writes aligned with the active loop and current round: current round comes from `STATE_CURRENT_ROUND` after `parse_state_file` (`hooks/loop-write-validator.sh:87-90`; parser in `hooks/lib/loop-common.sh:110-136`).

- gates_or_invariants: `state.md` is never writable through `Write` (`hooks/loop-write-validator.sh:95-98`). Loop backup `plan.md` is immutable when the path contains `/.humanize/rlcr/` (`:104-110`). `goal-tracker.md` is blocked once `current_round > 0`, with users redirected to the current summary (`:117-120`). Summary writes outside `.humanize/rlcr` are blocked and redirected to `round-${CURRENT_ROUND}-summary.md` in the active loop (`:127-134`). Summary round numbers must match `current_round` unless allowlisted (`:153-170`). Any protected loop write must target the newest active loop directory exactly, by comparing `FILE_PATH` to `ACTIVE_LOOP_DIR/$CLAUDE_FILENAME` (`:177-188`). The shared allowlist currently permits `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` only in the active loop (`hooks/lib/loop-common.sh:168-186`).

- dependencies_and_callers: Called by Claude hook registration in `hooks/hooks.json:14-21`. Depends on `jq`, Bash, `sed`, `basename`, and shared functions from `hooks/lib/loop-common.sh`, including `find_active_loop`, `is_round_file_type`, `is_allowlisted_file`, `parse_state_file`, `is_state_file_path`, `is_goal_tracker_path`, `is_in_humanize_loop_dir`, `extract_round_number`, and template-backed block message helpers. Template loading is via `hooks/lib/template-loader.sh`, especially `load_and_render_safe` fallback behavior (`hooks/lib/template-loader.sh:167-203`). The active loop directory and backup plan are created by `scripts/setup-rlcr-loop.sh`, which copies the original plan to `LOOP_DIR/plan.md` and writes the loop state (`scripts/setup-rlcr-loop.sh:470-498`).

- edge_cases_or_failure_modes: Non-`Write` inputs are allowed even if malformed for this script’s purposes (`hooks/loop-write-validator.sh:26-28`). Missing or empty `file_path` falls through as a normal file and is allowed. A `round-N-todos.md` path is blocked even outside an active loop unless it is explicitly allowlisted in the active loop (`:37-44`). If no active loop exists, protected summary and loop-directory checks usually allow because the script exits after active-loop lookup (`:83-85`), but prompt-file writes are still blocked earlier. Path validation is string-based, not canonicalized, so relative paths, symlinks, `..`, or duplicate separators may be rejected as wrong directory even if they resolve to the same file. The newest timestamp-named loop with `state.md` is authoritative, so older loop directories are intentionally treated as inactive by `find_active_loop` (`hooks/lib/loop-common.sh:58-79`). The `current_round` comparison assumes numeric state; unlike the stop hook, this validator does not perform an explicit numeric corruption guard before `-gt`.

- validation_or_tests: Direct test coverage is present but not executed in this read-only research pass. `tests/test-plan-file-hooks.sh:194-205` verifies `Write` blocks loop backup `plan.md`; `tests/test-plan-file-hooks.sh:1030-1040` verifies legacy `.humanize-loop.local` paths are allowed. `tests/test-allowlist-validators.sh:133-183` checks allowlisted todos/summary behavior and blocking for non-allowlisted round files. `tests/test-template-references.sh:56-64` includes this validator in template-reference scanning, and `:174-195` checks critical validators use safe template rendering.

- skip_candidate: `no`

### IMPROVE_MONITOR_SCRIPT-HZ-051 `file` `prompt-template/block/plan-file-modified.md`
- cursor: `[_]`
- core_role: Block-message template for the RLCR plan immutability gate. It is not executable code, but it defines the user-facing contract emitted when the original plan file diverges from the loop backup during an active RLCR loop.

- algorithmic_behavior: The template contains two placeholders, `{{PLAN_FILE}}` and `{{BACKUP_PATH}}` (`prompt-template/block/plan-file-modified.md:3-12`). It tells the user the plan changed since loop start, states that modifying plan files is forbidden during an active loop, and gives the required transition path: cancel the current loop, update the plan, then start a new loop with the same plan path (`:5-10`). The backup path is surfaced for recovery (`:12`).

- inputs_outputs_state: Inputs are values supplied by the stop hook: `PLAN_FILE` from parsed loop state and `BACKUP_PLAN="$LOOP_DIR/plan.md"` (`hooks/loop-codex-stop-hook.sh:77-88`, `:170`). Output is rendered Markdown text assigned to `REASON`; the stop hook wraps it in JSON with `"decision": "block"` and `"systemMessage": "Loop: Blocked - plan file modified"` (`hooks/loop-codex-stop-hook.sh:232-236`). The template itself has no state mutation. Its state-machine effect is to stop loop completion/review progression when plan integrity fails.

- gates_or_invariants: This template is reached only after the stop hook confirms the backup exists, the original plan still exists, and the content comparison fails (`hooks/loop-codex-stop-hook.sh:174-219`). Setup establishes the invariant by copying the plan into the loop directory as `plan.md` and recording `plan_file` plus `plan_tracked` in `state.md` (`scripts/setup-rlcr-loop.sh:475-498`). The enforced invariant is: the active loop’s original plan content must remain byte-equivalent to the backup captured at loop start.

- dependencies_and_callers: Primary caller is `hooks/loop-codex-stop-hook.sh:219-236`, through `load_and_render_safe "$TEMPLATE_DIR" "block/plan-file-modified.md"`. Rendering semantics come from `hooks/lib/template-loader.sh`: placeholders use `{{VAR}}`, missing variables remain literal, and substitution is single-pass to prevent placeholder injection (`hooks/lib/template-loader.sh:7-13`, `:50-132`). The hook sources `hooks/lib/loop-common.sh`, which initializes `TEMPLATE_DIR` via `get_template_dir` (`hooks/lib/loop-common.sh:46-55`; `hooks/lib/template-loader.sh:24-31`).

- edge_cases_or_failure_modes: The tracked-plan uncommitted-change path does not use this template; it emits an inline JSON reason first when `git status --porcelain "$PLAN_FILE"` is non-empty (`hooks/loop-codex-stop-hook.sh:202-214`). Deleted original plans and missing backups also use separate inline reasons (`:174-196`). If the template is missing or renders empty, `load_and_render_safe` falls back to an inline message with the same placeholders supplied by the hook (`hooks/loop-codex-stop-hook.sh:220-234`; `hooks/lib/template-loader.sh:167-203`). If caller variables are omitted, placeholders remain visible rather than failing closed, by template-loader design.

- validation_or_tests: `tests/test-plan-file-hooks.sh:469-507` modifies the project plan, invokes `hooks/loop-codex-stop-hook.sh`, and expects a JSON block mentioning plan modification. `tests/test-template-references.sh:56-64` scans hook scripts that reference templates, including the stop hook and validators, and validates template existence through the discovered references. No tests were run during this research pass.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `2 unique Item Evidence sections, matching assigned_item_count`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`