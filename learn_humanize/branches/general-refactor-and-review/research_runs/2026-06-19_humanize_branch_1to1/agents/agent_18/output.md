# agent_18 general-refactor-and-review 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `1fea22e96345f1005992936983b85317a156e3d5`

## Item Evidence

### GENERAL_REFACTOR_AND_REVIEW-HZ-018 `file` `hooks/loop-edit-validator.sh`
- cursor: `[_]`
- core_role: PreToolUse validator for Claude `Edit` calls in the RLCR loop. It protects generated/control files under `.humanize/rlcr` and enforces which actor may edit loop state surfaces. The hook is registered for the `Edit` matcher in `hooks/hooks.json:24-30`.

- algorithmic_behavior: The script reads hook JSON from stdin, extracts `.tool_name`, and exits successfully for any tool other than `Edit` (`hooks/loop-edit-validator.sh:22-27`). For `Edit`, it extracts `.tool_input.file_path`, lowercases it via shared helper, and then applies a path-based gate sequence (`hooks/loop-edit-validator.sh:29-30`):
  - round todo files are generally blocked because native TodoWrite should own todo state; only explicitly allowlisted active-loop files pass (`hooks/loop-edit-validator.sh:36-44`).
  - round prompt files are always blocked because prompts are generated instructions from Codex to Claude (`hooks/loop-edit-validator.sh:46-49`).
  - non-`.humanize/rlcr` paths bypass loop-specific controls (`hooks/loop-edit-validator.sh:55-57`).
  - active loop discovery and state parsing establish the current RLCR round (`hooks/loop-edit-validator.sh:63-73`).
  - `state.md` edits are blocked as hook-managed state (`hooks/loop-edit-validator.sh:79-82`).
  - `plan.md` backups inside `.humanize/rlcr` are blocked with the `block/plan-backup-protected.md` template (`hooks/loop-edit-validator.sh:88-95`).
  - `goal-tracker.md` edits are blocked after round 0 and redirected into the current round summary as an update request (`hooks/loop-edit-validator.sh:102-105`).
  - summary edits are checked against the current round; wrong-round summaries are blocked unless allowlisted (`hooks/loop-edit-validator.sh:112-136`).
  - all accepted paths end at `exit 0` (`hooks/loop-edit-validator.sh:140`).

- inputs_outputs_state: Input is Claude hook JSON on stdin with `tool_name` and `tool_input.file_path`. It uses environment `CLAUDE_PROJECT_DIR` when present, otherwise `pwd`, to locate `.humanize/rlcr` (`hooks/loop-edit-validator.sh:37-39`, `hooks/loop-edit-validator.sh:63-65`). It reads the newest active loop directory through `find_active_loop`, then parses `state.md` to populate `STATE_CURRENT_ROUND` (`hooks/lib/loop-common.sh:62-79`, `hooks/lib/loop-common.sh:110-136`). Outputs are exit status plus stderr block reasons: `0` allows the edit, `2` blocks it. It does not mutate files; its only state transition effect is preventing invalid external edits so the RLCR state machine remains consistent.

- gates_or_invariants: The validator preserves these invariants:
  - only `Edit` requests are evaluated; other tools are ignored (`hooks/loop-edit-validator.sh:25-27`).
  - todo files matching `round-[0-9]+-todos.md` are blocked unless they are active-loop allowlist entries (`round-1-todos.md`, `round-2-todos.md`) from `is_allowlisted_file` (`hooks/lib/loop-common.sh:146-150`, `hooks/lib/loop-common.sh:168-186`).
  - prompt files matching `round-[0-9]+-prompt.md` are read-only from Claude’s perspective (`hooks/loop-edit-validator.sh:46-49`).
  - loop state files matching `state.md` are hook-owned (`hooks/lib/loop-common.sh:245-249`, `hooks/loop-edit-validator.sh:79-82`).
  - only current-round summaries may be edited, except historical allowlisted summaries (`round-0-summary.md`, `round-1-summary.md`) (`hooks/loop-edit-validator.sh:112-136`, `hooks/lib/loop-common.sh:172-177`).
  - after round 0, the goal tracker may not be directly edited by Claude; changes must be requested via the current summary (`hooks/loop-edit-validator.sh:102-105`).

- dependencies_and_callers: It sources `hooks/lib/loop-common.sh` (`hooks/loop-edit-validator.sh:14-16`). That library sources the template loader and sets `TEMPLATE_DIR` (`hooks/lib/loop-common.sh:46-55`). Direct helper dependencies include `to_lower`, `is_round_file_type`, `find_active_loop`, `is_allowlisted_file`, `is_in_humanize_loop_dir`, `parse_state_file`, `is_state_file_path`, `is_goal_tracker_path`, `goal_tracker_blocked_message`, `todos_blocked_message`, and `prompt_write_blocked_message` (`hooks/lib/loop-common.sh:62-79`, `hooks/lib/loop-common.sh:139-197`, `hooks/lib/loop-common.sh:199-205`, `hooks/lib/loop-common.sh:239-299`). Template dependencies include `block/todos-file-access.md`, `block/prompt-file-write.md`, `block/state-file-modification.md`, `block/plan-backup-protected.md`, `block/goal-tracker-modification.md`, and `block/wrong-round-number.md` through direct or shared `load_and_render_safe` calls (`hooks/loop-edit-validator.sh:91-93`, `hooks/loop-edit-validator.sh:124-135`; shared templates listed in `tests/test-template-references.sh:152-159`). Caller registration is `hooks/hooks.json:24-30`.

- edge_cases_or_failure_modes: If the active loop base does not exist, or the newest loop lacks `state.md`, `find_active_loop` returns empty and most loop-specific controls are skipped after non-allowlisted todo handling (`hooks/lib/loop-common.sh:65-78`, `hooks/loop-edit-validator.sh:67-69`). Because `set -euo pipefail` is active (`hooks/loop-edit-validator.sh:12`), invalid JSON or missing `jq` can hard-fail instead of returning a structured block. `parse_state_file` can return `1` for a missing state file (`hooks/lib/loop-common.sh:110-115`); under `set -e`, that would abort if called after an active loop was found but its state disappeared. Path checks are regex/string based, not canonicalized; symlink, `..`, or case-folding behavior depends on the raw path string and the lowercased copy. `is_in_humanize_loop_dir` only matches the modern `.humanize/rlcr/` path, and tests confirm legacy `.humanize-loop.local` plan backups are intentionally allowed (`tests/test-plan-file-hooks.sh:1043-1054`).

- validation_or_tests: `tests/test-allowlist-validators.sh` exercises edit allowlist behavior: active `round-2-todos.md` allowed, historical `round-1-summary.md` allowed, and `round-4-todos.md` blocked (`tests/test-allowlist-validators.sh:189-226`). `tests/test-plan-file-hooks.sh` verifies edit blocking for `.humanize/rlcr/.../plan.md` backups and allowing legacy `.humanize-loop.local/.../plan.md` (`tests/test-plan-file-hooks.sh:211-221`, `tests/test-plan-file-hooks.sh:1043-1054`). `tests/test-template-references.sh` includes this validator in template scanning and safe-render checks (`tests/test-template-references.sh:57-63`, `tests/test-template-references.sh:176-180`). I did not execute tests because this pass is research-only in a read-only branch export.

- skip_candidate: `no`

### GENERAL_REFACTOR_AND_REVIEW-HZ-048 `file` `prompt-template/block/incomplete-todos.md`
- cursor: `[_]`
- core_role: Stop-hook block template for an RLCR completion gate. It defines the user-facing reason when Claude attempts to stop while the transcript’s latest TodoWrite state still contains incomplete todos.

- algorithmic_behavior: The file is a static Markdown template with one substitution variable, `{{INCOMPLETE_LIST}}` (`prompt-template/block/incomplete-todos.md:1-12`). It is loaded by the stop hook after the todo checker reports incomplete work. The stop hook calls `check-todos-from-transcript.py`, receives exit code `1`, strips the leading marker from checker output, renders this template with `INCOMPLETE_LIST`, and returns a JSON block decision (`hooks/loop-codex-stop-hook.sh:246-288`). The transition it enforces is “Stop requested” to “blocked, continue working” rather than allowing Codex review/final summary.

- inputs_outputs_state: Template input is `INCOMPLETE_LIST`, generated from the latest incomplete TodoWrite entries in the transcript (`hooks/loop-codex-stop-hook.sh:272-283`). The checker reads hook input JSON from stdin, looks for `transcript_path`, parses the JSONL transcript, and tracks the most recent TodoWrite list across supported transcript formats (`hooks/check-todos-from-transcript.py:90-107`, `hooks/check-todos-from-transcript.py:51-87`). Any todo whose `status` is not `completed` becomes an incomplete-list line formatted as `- [status] content` (`hooks/check-todos-from-transcript.py:113-126`). Rendered output is embedded in the stop hook’s `reason` field with `decision: "block"` and system message `"Loop: Blocked - incomplete todos detected, please finish all tasks first"` (`hooks/loop-codex-stop-hook.sh:285-292`).

- gates_or_invariants: The template instructs the agent to complete all remaining todos, mark each with TodoWrite, and only then write a summary and stop (`prompt-template/block/incomplete-todos.md:7-10`). It also explicitly blocks proceeding to Codex review while any todo is unfinished (`prompt-template/block/incomplete-todos.md:12`). The implementation invariant behind this text is status-based: only exact `completed` todos are accepted; `pending`, `in_progress`, missing status, empty-content incomplete todos, and any other non-completed status block stop (`hooks/check-todos-from-transcript.py:113-119`).

- dependencies_and_callers: Direct caller is `hooks/loop-codex-stop-hook.sh` via `load_and_render_safe "$TEMPLATE_DIR" "block/incomplete-todos.md"` (`hooks/loop-codex-stop-hook.sh:277-283`). The caller depends on `hooks/check-todos-from-transcript.py` for transcript parsing and incomplete detection (`hooks/loop-codex-stop-hook.sh:246-250`). Template resolution flows through the shared template loader sourced by `hooks/lib/loop-common.sh` (`hooks/lib/loop-common.sh:46-55`). The stop hook itself is registered as the RLCR `Stop` hook in `hooks/hooks.json:52-59`.

- edge_cases_or_failure_modes: If the checker cannot parse hook input JSON, the stop hook blocks with a parse-error message rather than using this template (`hooks/loop-codex-stop-hook.sh:253-269`). If no `transcript_path` exists, the transcript file does not exist, or no TodoWrite call is found, the checker exits `0` and this template is not used (`hooks/check-todos-from-transcript.py:25-27`, `hooks/check-todos-from-transcript.py:99-111`). Invalid JSONL lines inside the transcript are ignored, so a malformed line will not block by itself (`hooks/check-todos-from-transcript.py:36-39`). Because the hook uses only the latest non-empty TodoWrite list, an earlier incomplete list can be superseded by a later completed list (`hooks/check-todos-from-transcript.py:28-87`). If the template is missing, the hook has an inline fallback, but the message loses the more explicit “Do NOT proceed to Codex review” wording (`hooks/loop-codex-stop-hook.sh:277-283`).

- validation_or_tests: `tests/test-todo-checker.sh` covers the checker states that feed this template: all completed exits `0`, incomplete exits `1`, output includes todo details, `in_progress` blocks, empty transcript allows, invalid JSONL lines are ignored, multiple TodoWrite calls use the latest, direct/alternative transcript formats work, missing status blocks, and empty-content incomplete todos are still incomplete (`tests/test-todo-checker.sh:106-286`). `tests/test-template-references.sh` scans hook scripts for template references and validates template existence/safe rendering patterns for hook templates (`tests/test-template-references.sh:52-72`, `tests/test-template-references.sh:145-186`). I did not execute tests because this pass is research-only in a read-only branch export.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 2/2 item sections present exactly once above
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`