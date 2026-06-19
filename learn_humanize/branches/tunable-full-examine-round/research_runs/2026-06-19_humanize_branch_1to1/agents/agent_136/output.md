# agent_136 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-136 `file` `tests/robustness/test-plan-file-robustness.sh`
- cursor: `[_]`
- core_role:
  - Executable robustness specification for RLCR plan-file validation. It drives the production entrypoint [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:320) through temporary plan files and classifies whether production accepted or rejected each file.
  - It is part of the full test runner’s robustness suite: [tests/run-all-tests.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/run-all-tests.sh:63) includes `robustness/test-plan-file-robustness.sh`.
  - It focuses on plan-content resilience rather than normal happy-path setup only: empty files, comment-only files, large files, mixed line endings, binary/null bytes, long lines, special characters, permissions, symlinks, directories, and disappearance during validation are all covered in [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:274).

- algorithmic_behavior:
  - The main production-facing oracle is `test_plan_validation(plan_path)` at [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:24). It:
    - Creates a temporary result file with `mktemp`.
    - Removes `$TEST_DIR/.humanize/rlcr` before each invocation to avoid an existing loop contaminating the result.
    - Runs `CLAUDE_PROJECT_DIR="$TEST_DIR" bash "$PROJECT_ROOT/scripts/setup-rlcr-loop.sh" "$plan_path"` with stdout/stderr redirected to the result file.
    - Treats specific validation messages as rejection: `Plan is too simple`, `Plan file has insufficient content`, `Plan file not found`, `Plan file not readable`, and `symbolic link`.
    - Treats later-stage failures as validation success when output contains `requires codex`, `must be gitignored`, or `start-rlcr-loop activated`, because those messages mean plan validation passed and execution reached a later gate.
    - Also treats creation of `.humanize/rlcr/*/state.md` as an alternate success signal.
  - The test includes a local mirror of the content-line counting algorithm in `count_content_lines()` at [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:104). It ignores blank lines, full-line HTML comments, multi-line HTML comments, and lines beginning with `#`, then counts all remaining lines as content.
  - That mirror aligns with the production content gate in [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:493), where headings beginning with `#` are explicitly treated as comments, not content.
  - Positive production-backed cases:
    - Valid structured markdown plan is accepted: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:152).
    - Minimal plan with exactly three content lines is accepted: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:180).
    - Standard 5KB-ish plan is accepted: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:208).
    - Rich markdown with code fences, tables, lists, links, bold, and italic is accepted: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:227).
    - A generated 1MB+ plan is accepted and timed, protecting against historical large-output/SIGPIPE issues: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:299).
    - Mixed CRLF/LF line endings are accepted: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:329).
  - Negative production-backed cases:
    - Empty plan file is rejected: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:274).
    - Comment-only plan file is rejected: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:283).
    - Deleted/missing plan file is rejected through production validation: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:501).
  - Some later cases are direct shell/file-system robustness checks rather than calls into production: binary content, long lines, special characters, whitespace-only content counting, complex comments, missing-file existence, unreadable mode, symlink detection, directory detection, and null-byte line counting are checked locally in [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:342).

- inputs_outputs_state:
  - Inputs:
    - A single plan path argument passed to `test_plan_validation`, typically relative to `$TEST_DIR`; examples include `valid-plan.md`, `empty-plan.md`, `large-plan.md`, `mixed-endings.md`, and `disappear-plan.md`.
    - The test repository root derived from `SCRIPT_DIR/../..` at [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:15).
    - A temporary mock git repository created inside `$TEST_DIR`, initialized and committed at [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:86).
    - Production receives `CLAUDE_PROJECT_DIR="$TEST_DIR"` so setup runs against the temporary repo rather than the checked-out repository: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:37).
  - Outputs:
    - Test status messages via `pass` and `fail` sourced from [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/test-helpers.sh:30).
    - A final summary and process exit code from `print_test_summary`, where zero failures returns `0` and failures return `1`: [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/test-helpers.sh:58), invoked at [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:531).
    - Temporary production output files are deleted by `test_plan_validation` on all known paths: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:40).
  - State transitions:
    - Test setup creates a temporary directory with cleanup trap through `setup_test_dir`: [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/test-helpers.sh:86).
    - Each production invocation resets `.humanize/rlcr` state before running setup: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:33).
    - Production may create `.humanize/rlcr/<timestamp>/state.md`, which the test treats as validation success: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:64).
    - Production itself copies the validated plan to the loop directory and records `plan_file`/`plan_tracked` in state after passing validation: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:675) and [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:709).

- gates_or_invariants:
  - Shell safety gate: the test uses `set -euo pipefail`, so unhandled command failures, unset variables, and pipeline failures abort execution: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:13).
  - Production path invariants exercised indirectly:
    - Plan paths must be relative: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:320).
    - Plan paths must not contain spaces: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:326).
    - Shell metacharacters are rejected: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:334).
    - The plan file itself cannot be a symlink: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:346).
    - Parent directory path segments cannot be symlinks: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:359).
    - File must exist and be readable: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:382) and [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:388).
    - Resolved path must stay inside the project root: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:394).
  - Production content invariants:
    - At least five physical lines are required: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:483).
    - At least three content lines are required after excluding blank/comment lines: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:531).
    - Lines starting with `#` are non-content for this validator, even though they may be markdown headings: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:493).
  - Test oracle invariant:
    - Later setup failures caused by missing Codex CLI or plan tracking policy are considered success for this file’s concern because they occur after plan validation: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:46) and [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:52).
    - Production checks Codex availability after plan content validation, so `requires codex` is a valid validation-passed sentinel: [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:543).
  - Potential mismatch invariant:
    - The file header says it tests “File disappearance” at [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:9), but the implemented case deletes the file before validation starts, not mid-read: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:519).

- dependencies_and_callers:
  - Direct dependencies:
    - `scripts/setup-rlcr-loop.sh`, the production setup and validation implementation invoked at [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:37).
    - `tests/test-helpers.sh`, sourced for `setup_test_dir`, `pass`, `fail`, and `print_test_summary`: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:84).
    - Standard Unix/Git tooling: `mktemp`, `rm`, `grep`, `ls`, `head`, `wc`, `seq`, `printf`, `chmod`, `ln`, `git`, and `date`.
  - Callers:
    - Standalone execution by invoking the shell script directly.
    - Aggregate suite execution through [tests/run-all-tests.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/run-all-tests.sh:80), with this test registered at line 63.
  - Related sibling coverage:
    - [tests/robustness/test-path-validation-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-path-validation-robustness.sh:55) uses a similar production-output classification helper for plan path/content validation and covers broader path-shape rejection.
    - That sibling also asserts empty, comments-only, short, missing, and directory cases around [tests/robustness/test-path-validation-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-path-validation-robustness.sh:404), while this assigned file adds larger plan-content stress cases.

- edge_cases_or_failure_modes:
  - Empty file: rejected through production because line count is under five.
  - Comments-only file: rejected through production because content count is under three.
  - Large file: accepted if generated size exceeds 1,000,000 bytes and production validation succeeds; failure modes include file generation too small or production rejection.
  - Mixed line endings: accepted through production when `wc -l` and shell reads handle CRLF/LF without reducing line/content counts below thresholds.
  - Binary content and null bytes: the assigned file only verifies `wc -l` can read/count them; it does not call production validation for these cases.
  - Very long line: validates local line-count robustness for a 10,000-character line; it does not call production validation.
  - Special shell characters inside plan content: validates local content-line counting; path metacharacter rejection is covered elsewhere and in production.
  - Whitespace-only file: local content counter must return zero.
  - Complex/nested HTML comments: local counter uses a simple state machine, so invalid nested comment patterns can be counted in unintuitive ways; the test only requires at least two content lines.
  - Nonexistent/deleted file: production should reject with `Plan file not found`.
  - Unreadable file: the test accounts for privileged users by passing either when unreadable is detected or when the process can still read it.
  - Symlink and directory cases near the end are local detection checks, not production invocations, even though production has symlink/file gates.
  - `test_plan_validation` has a subtle state-locality issue: `exit_code` is declared local but not initialized before the production command, then assigned with `exit_code=${exit_code:-0}`. In Bash, an unset local is handled by that expansion, so this is currently safe under `set -u`.
  - Result classification is message-string dependent. If production error text changes without preserving these substrings, the test oracle can misclassify validation outcomes.

- validation_or_tests:
  - The assigned file is itself the validation asset. It defines 19 numbered cases and exits with the shared helper’s failure-sensitive summary: [tests/robustness/test-plan-file-robustness.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/tests/robustness/test-plan-file-robustness.sh:531).
  - It validates production behavior by running `setup-rlcr-loop.sh`, not by importing an isolated validator function. This is stronger as an integration check but makes the oracle depend on later setup gates such as Codex availability and gitignore/tracking status.
  - The production validation gates it exercises are concentrated in [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:310) through [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round/scripts/setup-rlcr-loop.sh:548).
  - I did not execute the test suite because the assignment asked for research notes only and the branch export is read-only; the script itself creates temporary files outside the repo, but its production invocation can create `.humanize/rlcr` under the temp repo, so inspection was sufficient for this research pass.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1/1 item section present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`