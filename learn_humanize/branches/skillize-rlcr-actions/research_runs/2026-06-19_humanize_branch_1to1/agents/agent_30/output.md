# agent_30 skillize-rlcr-actions 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `0a9187b8478dd3ed9c0cf58a4615c61e188fd444`

## Item Evidence

### SKILLIZE_RLCR_ACTIONS-HZ-030 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role:
  - This is an executable specification for the RLCR loop validator allowlist exception. It verifies that the system’s normal restrictions on `round-*-todos.md` and non-current `round-*-summary.md` files have a narrow compatibility escape hatch for exactly four active-loop files.
  - The file directly tests the shared allowlist helper from `hooks/lib/loop-common.sh` and the hook entrypoints `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-read-validator.sh`, and `hooks/loop-bash-validator.sh`.
  - It is included in the full test suite via `tests/run-all-tests.sh:44`, so it is part of the repository’s regression gate surface rather than an isolated manual check.

- algorithmic_behavior:
  - The script initializes counters and simple `pass`/`fail` functions, then exits with `TESTS_FAILED`, making the number of failed assertions the process status (`tests/test-allowlist-validators.sh:19-27`, `tests/test-allowlist-validators.sh:383-391`).
  - `setup_test_loop` creates a temporary git repository, configures a user, makes an initial commit, and creates `.humanize/rlcr/2024-01-01_12-00-00/state.md` with `current_round: 5`; this forces all low-numbered summaries and todos to be non-current unless allowlisted (`tests/test-allowlist-validators.sh:29-62`).
  - The direct helper section specifies the allowlist: `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` must return success only when the full path is inside the active loop directory (`tests/test-allowlist-validators.sh:64-124`).
  - The Write validator section feeds JSON hook input through stdin and expects:
    - exit `0` for allowlisted `round-1-todos.md` and historical `round-0-summary.md`;
    - exit `2` for non-allowlisted `round-3-todos.md` and `round-2-summary.md`;
    - stderr content containing either “todos” or “round” depending on which gate fires (`tests/test-allowlist-validators.sh:126-183`).
  - The Edit validator section mirrors the Write behavior for `round-2-todos.md`, historical `round-1-summary.md`, and blocked `round-4-todos.md` (`tests/test-allowlist-validators.sh:185-226`).
  - The Read validator section ensures allowlisted todos and historical summaries can be read even though normal round-file access rejects stale or wrong files (`tests/test-allowlist-validators.sh:228-282`).
  - The Bash validator section is stricter than direct Read/Write/Edit tool path validation: it allows only full-path shell modifications to active-loop `round-1-todos.md` or `round-2-todos.md`, while rejecting relative names, wrong roots, old loop directories, and same-basename directories outside the project root (`tests/test-allowlist-validators.sh:284-381`).

- inputs_outputs_state:
  - Inputs:
    - Local temporary repo under `mktemp -d` (`tests/test-allowlist-validators.sh:29-31`).
    - Synthetic active RLCR state file with `current_round: 5`, `max_iterations: 42`, `plan_file`, `plan_tracked`, and `start_branch` (`tests/test-allowlist-validators.sh:52-61`).
    - JSON hook payloads shaped as `{"tool_name": "...", "tool_input": {"file_path": "..."}}` for Read/Write/Edit, and `{"tool_name": "Bash", "tool_input": {"command": "..."}}` for Bash (`tests/test-allowlist-validators.sh:135`, `tests/test-allowlist-validators.sh:191`, `tests/test-allowlist-validators.sh:234`, `tests/test-allowlist-validators.sh:290`).
    - `CLAUDE_PROJECT_DIR="$TEST_DIR"` so validators resolve the synthetic `.humanize/rlcr` tree instead of the repository root (`tests/test-allowlist-validators.sh:130-131`).
  - Outputs:
    - Human-readable PASS/FAIL lines.
    - Final summary counts.
    - Process exit code equal to failed assertion count (`tests/test-allowlist-validators.sh:383-391`).
  - State transitions:
    - `setup_test_loop` may initialize a git repo only once and then reuses the same temp directory for later sections (`tests/test-allowlist-validators.sh:33-43`).
    - Each hook invocation temporarily disables `set -e`, captures `RESULT` and `EXIT_CODE`, then restores strict exit behavior with `set -e` (`tests/test-allowlist-validators.sh:136-139`, repeated throughout).
    - The trap removes the temporary test directory on process exit (`tests/test-allowlist-validators.sh:30-31`).

- gates_or_invariants:
  - Exact allowlist invariant: `hooks/lib/loop-common.sh` defines only four allowed filenames: `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, `round-1-summary.md` (`hooks/lib/loop-common.sh:170-179`).
  - Exact path invariant: `is_allowlisted_file` compares `"$file_path" == "$active_loop_dir/$allowed"`; matching basename alone is insufficient (`hooks/lib/loop-common.sh:181-187`).
  - Active-loop invariant: validators resolve the active loop via `find_active_loop`, which selects only the newest timestamp directory and requires `state.md` or `finalize-state.md` (`hooks/lib/loop-common.sh:58-81`).
  - Tool-specific behavior:
    - Write blocks non-allowlisted todos before broader file-type checks (`hooks/loop-write-validator.sh:37-45`), blocks prompt writes (`hooks/loop-write-validator.sh:47-50`), and blocks non-current summaries unless allowlisted (`hooks/loop-write-validator.sh:181-198`).
    - Edit applies the same todos/prompt and summary-round rules (`hooks/loop-edit-validator.sh:36-49`, `hooks/loop-edit-validator.sh:124-149`).
    - Read blocks todos unless allowlisted and blocks stale summary/prompt reads unless allowlisted (`hooks/loop-read-validator.sh:36-44`, `hooks/loop-read-validator.sh:116-129`).
    - Bash allows active-loop `round-[12]-todos.md` only when the command contains the full escaped active loop path; otherwise it emits the todos block (`hooks/loop-bash-validator.sh:344-351`).
  - Security invariant specifically covered by the test: a path under `/tmp/.humanize/rlcr/<same-active-loop-basename>/round-1-todos.md` must not pass just because the loop directory basename matches (`tests/test-allowlist-validators.sh:368-381`).

- dependencies_and_callers:
  - Sources `hooks/lib/loop-common.sh` directly for helper-level tests (`tests/test-allowlist-validators.sh:15-17`).
  - Calls hook scripts by path under `PROJECT_ROOT/hooks/`:
    - `loop-write-validator.sh` (`tests/test-allowlist-validators.sh:137`, `tests/test-allowlist-validators.sh:150`, `tests/test-allowlist-validators.sh:163`, `tests/test-allowlist-validators.sh:176`).
    - `loop-edit-validator.sh` (`tests/test-allowlist-validators.sh:193`, `tests/test-allowlist-validators.sh:206`, `tests/test-allowlist-validators.sh:219`).
    - `loop-read-validator.sh` (`tests/test-allowlist-validators.sh:236`, `tests/test-allowlist-validators.sh:249`, `tests/test-allowlist-validators.sh:262`, `tests/test-allowlist-validators.sh:275`).
    - `loop-bash-validator.sh` (`tests/test-allowlist-validators.sh:292`, `tests/test-allowlist-validators.sh:305`, `tests/test-allowlist-validators.sh:318`, `tests/test-allowlist-validators.sh:331`, `tests/test-allowlist-validators.sh:344`, `tests/test-allowlist-validators.sh:359`, `tests/test-allowlist-validators.sh:374`).
  - Depends on `jq` inside validators for hook JSON parsing (`hooks/loop-write-validator.sh:23-30`, `hooks/loop-edit-validator.sh:22-30`, `hooks/loop-read-validator.sh:22-30`, `hooks/loop-bash-validator.sh:22-30`).
  - Depends on git being available because the synthetic active loop setup initializes and commits a temp repository (`tests/test-allowlist-validators.sh:36-43`).
  - Integrated into the broader suite through `tests/run-all-tests.sh`, where it appears after ANSI parsing and before finalize/cancel/monitor suites (`tests/run-all-tests.sh:32-54`).

- edge_cases_or_failure_modes:
  - If `jq` is missing, the hook validators fail before the allowlist logic can be exercised.
  - If `git init` or the initial commit fails, the test cannot produce the state file’s `start_branch` value and setup fails (`tests/test-allowlist-validators.sh:36-47`).
  - If `find_active_loop` chooses a newer loop directory than the one created by this test, the allowlist path comparison would fail; the temp project isolation and fixed single loop directory prevent that (`hooks/lib/loop-common.sh:71-80`).
  - Case sensitivity is asymmetric: validators lowercase for pattern detection, but `is_allowlisted_file` compares the original `FILE_PATH` to the exact active-loop path (`hooks/lib/loop-common.sh:170-187`). The test does not cover mixed-case paths.
  - Bash validation intentionally uses command-text regexes, not a shell parser. The assigned test covers common redirect and `tee` forms plus wrong roots, but does not exhaustively test quoting or path spaces for todos commands.
  - The test sets `set -uo pipefail`, not global `set -e`; individual hook calls manage expected failures with `set +e` and `set -e`, so an unexpected ordinary command failure outside those blocks may not always stop immediately unless it is used in a failing conditional context.

- validation_or_tests:
  - This file is itself the validation suite for the allowlist behavior, containing 25 numbered tests (`tests/test-allowlist-validators.sh:70-381`).
  - It validates both direct helper behavior and end-to-end hook exit semantics.
  - It is included in the repository’s aggregate test runner (`tests/run-all-tests.sh:44`).
  - Related template reference validation checks that `block/goal-tracker-bash-write.md` and other common block templates exist for message functions (`tests/test-template-references.sh:149-167`), but this allowlist test mainly asserts exit codes and selected stderr substrings, not full message text.
  - I inspected the file and referenced validators directly; I did not execute the test suite in this read-only branch export.

- skip_candidate: `no`

### SKILLIZE_RLCR_ACTIONS-HZ-060 `file` `prompt-template/block/goal-tracker-bash-write.md`
- cursor: `[_]`
- core_role:
  - This is a block-message template used when a Bash command attempts to modify `goal-tracker.md` during Round 0.
  - It is part of the validator gate UX: the Bash validator blocks the command, and this template tells the agent to use the Write or Edit tool at the validated path instead of bypassing hooks with shell redirection or text-processing commands.
  - Although small, it defines an algorithmically important transition: Bash write attempt to `goal-tracker.md` becomes a blocked tool call with a corrective tool/path instruction.

- algorithmic_behavior:
  - The template emits a Markdown heading, a prohibition on Bash modification of `goal-tracker.md`, a corrective path placeholder, and the reason: shell commands bypass validation hooks (`prompt-template/block/goal-tracker-bash-write.md:1-8`).
  - It accepts one variable, `{{CORRECT_PATH}}`, rendered into the “Use the Write or Edit tool instead” line (`prompt-template/block/goal-tracker-bash-write.md:5`).
  - The template is loaded by `goal_tracker_bash_blocked_message`, which supplies `CORRECT_PATH=$correct_path` via `load_and_render_safe` (`hooks/lib/loop-common.sh:239-248`).
  - The Bash validator calls this message function only when `command_modifies_file "$COMMAND_LOWER" "goal-tracker\.md"` detects a modifying command and `CURRENT_ROUND` is `0` (`hooks/loop-bash-validator.sh:303-317`).
  - For `CURRENT_ROUND > 0`, the Bash validator does not use this template; it switches to `goal_tracker_blocked_message`, telling the agent to put update requests in the current round summary instead (`hooks/loop-bash-validator.sh:308-315`, `hooks/lib/loop-common.sh:601-612`).

- inputs_outputs_state:
  - Inputs:
    - Template variable `CORRECT_PATH`, normally set to `$ACTIVE_LOOP_DIR/goal-tracker.md` by `loop-bash-validator.sh` (`hooks/loop-bash-validator.sh:308-312`).
    - The active loop directory and current round, resolved from `.humanize/rlcr` state before the validator reaches the goal-tracker gate (`hooks/loop-bash-validator.sh:32-53`).
    - A Bash hook JSON payload whose `tool_input.command` text matches a modification pattern for `goal-tracker.md` (`hooks/loop-bash-validator.sh:22-30`, `hooks/lib/loop-common.sh:571-599`).
  - Outputs:
    - Rendered Markdown sent to stderr by the Bash validator through `goal_tracker_bash_blocked_message "$GOAL_TRACKER_PATH" >&2` (`hooks/loop-bash-validator.sh:308-312`).
    - Validator exit code `2`, indicating a blocked PreToolUse hook (`hooks/loop-bash-validator.sh:316-317`).
  - State transitions:
    - No repository state is modified by this template.
    - It participates in a control-flow transition where the attempted Bash write is denied before shell execution and the agent is redirected to a tool path that remains subject to Write/Edit validators.

- gates_or_invariants:
  - Bash-to-goal-tracker modifications are always blocked by `loop-bash-validator.sh`; Round 0 receives this template, later rounds receive a different “Goal Tracker Modification Blocked” message (`hooks/loop-bash-validator.sh:303-317`).
  - Detection relies on `command_modifies_file`, which recognizes redirects, append redirects, `tee`, in-place `sed`/`awk`/`perl`, `mv`/`cp`, `rm`, `dd of=`, `truncate`, `printf >`, and `exec >` forms (`hooks/lib/loop-common.sh:571-599`).
  - The invariant enforced by the template text is that `goal-tracker.md` should be modified through Write/Edit, not through Bash, because Bash bypasses path and round validators (`prompt-template/block/goal-tracker-bash-write.md:3-8`).
  - The template itself does not enforce the gate; enforcement comes from `loop-bash-validator.sh`, while the template provides the operator-facing rejection contract.

- dependencies_and_callers:
  - Direct caller: `goal_tracker_bash_blocked_message` in `hooks/lib/loop-common.sh` (`hooks/lib/loop-common.sh:239-248`).
  - Runtime caller of that helper: `hooks/loop-bash-validator.sh` Round 0 goal-tracker branch (`hooks/loop-bash-validator.sh:308-312`).
  - Template resolution depends on `hooks/lib/template-loader.sh` via `load_and_render_safe`; `loop-common.sh` initializes `TEMPLATE_DIR` from the shared loader (`hooks/lib/loop-common.sh:46-55`).
  - Existence is validated in `tests/test-template-references.sh`, where it is listed as a common template expected by loop-common message functions (`tests/test-template-references.sh:152-163`).
  - Related behavioral tests for Bash modification detection live in `tests/test-bash-validator-patterns.sh`, which includes many `goal-tracker.md` modifying and non-modifying command patterns; the repository search shows that test is dedicated to Bash pattern detection for this class of gate.

- edge_cases_or_failure_modes:
  - If the template file is missing or fails to render, `load_and_render_safe` falls back to an inline message defined in `goal_tracker_bash_blocked_message`; the gate still blocks, but the exact wording may differ (`hooks/lib/loop-common.sh:241-248`).
  - If `CORRECT_PATH` is empty or malformed because active-loop detection failed, this template would render an unhelpful path; however, `loop-bash-validator.sh` exits early and allows all commands when no active loop exists (`hooks/loop-bash-validator.sh:36-43`).
  - Detection is regex-based over lowercased command text. Complex shell constructs not matched by `command_modifies_file` could avoid this specific message, though broader Bash validator tests cover many common write patterns.
  - The wording says “Use the Write or Edit tool,” but after Round 0 direct Write/Edit modifications to goal tracker are separately blocked by other validator logic; this template is therefore only correct for the Round 0 branch where it is called (`hooks/loop-bash-validator.sh:308-315`).
  - This template is a skip candidate only if “core algorithm” is interpreted as production code exclusively. Under this branch’s hook-driven design, block templates are part of the validation contract because they direct the agent’s next permitted action.

- validation_or_tests:
  - Existence check: `tests/test-template-references.sh` includes `block/goal-tracker-bash-write.md` in `COMMON_TEMPLATES` and fails if it is absent (`tests/test-template-references.sh:152-166`).
  - Behavioral coverage: `tests/test-bash-validator-patterns.sh` exercises `goal-tracker.md` modifying command detection across redirects, `tee`, in-place edits, file operations, and non-modifying reads, according to the repository references found during inspection.
  - Template rendering infrastructure is covered broadly by `tests/test-template-loader.sh` and `tests/test-templates-comprehensive.sh`; this specific template is referenced rather than deeply rendered in the comprehensive excerpt I inspected.
  - I inspected the template and its caller path directly; I did not execute the tests in this read-only branch export.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 2 item evidence headings present; no merged sections
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`