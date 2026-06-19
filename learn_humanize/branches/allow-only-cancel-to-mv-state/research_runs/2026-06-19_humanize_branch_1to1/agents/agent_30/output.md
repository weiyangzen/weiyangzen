# agent_30 allow-only-cancel-to-mv-state 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `3c39192e9b738743cdc5305a83a797a5ca66889b`

## Item Evidence

### ALLOW_ONLY_CANCEL_TO_MV_STATE-HZ-030 `file` `tests/test-error-scenarios.sh`
- cursor: `[_]`
- core_role:
  - Executable negative/edge-case specification for the prompt template-loading subsystem used by RLCR hook validators.
  - The file directly sources [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/template-loader.sh:13) via `source "$PROJECT_ROOT/hooks/lib/template-loader.sh"` and asserts that missing templates, invalid template directories, empty content, malformed placeholders, strict shell mode, and fallback rendering do not crash validator flows.
  - It is included in the aggregate test runner as one suite in [tests/run-all-tests.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/tests/run-all-tests.sh:42), so it is part of the repo’s validation surface.

- algorithmic_behavior:
  - Initializes `SCRIPT_DIR`, `PROJECT_ROOT`, sources the loader, and resolves `TEMPLATE_DIR` through `get_template_dir "$PROJECT_ROOT/hooks/lib"` at lines 11-15.
  - Defines local `pass` and `fail` counters at lines 22-35, then runs 12 independent assertions and exits based on `TESTS_FAILED` at lines 218-225.
  - Tests missing-file behavior:
    - `load_template "$TEMPLATE_DIR" "non-existing-file.md"` must return empty output and exit 0, lines 45-52.
    - `load_template "/non/existing/path" "block/git-push.md"` must also return empty output and exit 0, lines 58-65.
    - `load_and_render "$TEMPLATE_DIR" "non-existing.md"` must return empty output and exit 0, lines 71-78.
  - Tests render behavior:
    - Empty content passed to `render_template` must return empty output without error, lines 84-91.
    - Values containing regex-looking characters such as `[test]`, `(foo)`, and `*bar*` must render literally, lines 97-105.
    - Empty placeholder `{{}}` and unclosed placeholder `{{UNCLOSED` must remain unchanged, lines 186-205.
  - Tests strict-mode resilience:
    - Runs an isolated `bash -c` with `set -euo pipefail`, sources the loader, renders a missing template, and expects `SCRIPT_COMPLETED`, lines 114-131. This guards against validators aborting just because optional template text is missing.
  - Tests safe fallback behavior:
    - `load_and_render_safe` must emit the fallback when a template is missing, lines 137-144.
    - Fallback text may itself contain placeholders and must substitute variables, lines 150-157.
  - Tests template directory validation:
    - `validate_template_dir "$TEMPLATE_DIR"` must accept the real template root, lines 164-168.
    - `validate_template_dir "/non/existing/path"` must reject invalid directories with nonzero status, lines 175-179.

- inputs_outputs_state:
  - Inputs:
    - Filesystem paths derived from the current checkout: `tests/`, project root, `hooks/lib/template-loader.sh`, and `prompt-template/`.
    - Function arguments to template-loader APIs: template directory, template name, fallback message, and `VAR=value` assignments.
    - Synthetic template strings: `Path: {{PATH}}`, `Test: {{}}`, and `Test: {{UNCLOSED`.
  - Outputs:
    - Human-readable PASS/FAIL lines printed to stdout.
    - A final summary with passed/failed counts at lines 211-216.
    - Process exit 0 when no failures remain, or exit 1 when any assertion failed, lines 218-225.
  - State transitions:
    - The script does not mutate repository state. Its only state is in-memory counters `TESTS_PASSED` and `TESTS_FAILED`.
    - Each assertion advances exactly one counter through `pass()` or `fail()`, lines 25-35.
    - The final process state transitions from “running checks” to success/failure via the exit code.
  - Related system state:
    - Template loader itself uses a single-pass `awk` renderer in [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/template-loader.sh:74), so tests 5, 8, 11, and 12 exercise that rendering path.
    - `load_and_render_safe` suppresses missing-template stderr and chooses fallback rendering if content or result is empty in [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/template-loader.sh:170).

- gates_or_invariants:
  - Missing template files are nonfatal: empty string plus exit 0 is expected for `load_template` and `load_and_render`.
  - Invalid template directories are nonfatal for loading but are rejectable by explicit validation.
  - Rendering must be literal with respect to regex metacharacters in variable values.
  - Fallback text must be renderable with the same placeholder substitution semantics as loaded templates.
  - Malformed placeholders are not normalized or erased: `{{}}` and unclosed `{{...` remain as literal text.
  - Under `set -euo pipefail`, missing templates must not abort hook execution.
  - These gates support the broader hook invariant that a validator block should degrade to inline fallback text rather than emit an empty or crashing error message.

- dependencies_and_callers:
  - Direct dependency: [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/template-loader.sh:1), specifically `get_template_dir`, `load_template`, `render_template`, `load_and_render`, `load_and_render_safe`, and `validate_template_dir`.
  - Aggregate caller: [tests/run-all-tests.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/tests/run-all-tests.sh:32) lists `test-error-scenarios.sh` in the suite order.
  - Behavioral peers:
    - [tests/test-template-references.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/tests/test-template-references.sh:5) validates that referenced templates exist and that critical validators use `load_and_render_safe`.
    - [tests/test-templates-comprehensive.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/tests/test-templates-comprehensive.sh:5) validates all templates can load and that placeholder syntax is valid.
  - Runtime consumers of the tested loader behavior include [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/loop-read-validator.sh:135) and [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/loop-write-validator.sh:183), which rely on `load_and_render_safe` for block messages.

- edge_cases_or_failure_modes:
  - Missing template file: must not propagate as hook failure, lines 45-52 and 71-78.
  - Missing template directory: `load_template` returns empty, but `validate_template_dir` returns failure, lines 58-65 and 175-179.
  - Empty template content: `render_template ""` returns empty without failure, lines 84-90.
  - Special characters in values: tested specifically to prevent `sed`/regex replacement bugs, lines 97-105.
  - Strict mode: missing templates under `set -euo pipefail` must not interrupt the surrounding script, lines 114-131.
  - Fallback substitution: missing-template fallback with `{{FILE}}` must still render, lines 150-157.
  - Malformed placeholder preservation: empty and unclosed placeholders should stay unchanged, lines 186-205.
  - Environment-dependent failure observed in this read-only branch export: running `bash tests/test-error-scenarios.sh` failed 4 assertions because [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/template-loader.sh:129) uses a here-string into `awk`, and this sandbox cannot create the shell temp file required for that construct. The failing assertions were render-related; the file-system/missing-template gates still passed. This is a validation-environment artifact, not a repository edit.

- validation_or_tests:
  - Direct command executed read-only: `bash tests/test-error-scenarios.sh`.
  - Observed result in this sandbox: exit 1, summary `Passed: 8`, `Failed: 4`.
  - Failure reason shown by shell: `cannot create temp file for here document: Operation not permitted` at `hooks/lib/template-loader.sh:129`.
  - Passing areas during this run: missing template file, missing directory, missing `load_and_render`, empty render non-crash, strict-mode continuation, missing-template fallback without variables, valid template dir, invalid template dir.
  - Failing areas during this run: special-character render, fallback variable substitution, empty placeholder preservation, unclosed placeholder preservation. All failures depend on `render_template`’s here-string path, not on the assigned test file mutating state.
  - Related validation coverage exists in `tests/test-template-references.sh` for template existence and safe fallback usage, and `tests/test-templates-comprehensive.sh` for all-template loading and placeholder syntax.

- skip_candidate: `no`

### ALLOW_ONLY_CANCEL_TO_MV_STATE-HZ-060 `file` `prompt-template/block/wrong-directory-path.md`
- cursor: `[_]`
- core_role:
  - Prompt/block template used when RLCR validators detect an otherwise valid round file name in the wrong active loop directory path.
  - It defines the user-facing block contract for “wrong directory” transitions: the attempted path is blocked, the canonical active-loop path is emitted, and the user receives a suggested read command.
  - The template is small, but it is part of the guardrail behavior because validators use it at deny points that exit with status 2.

- algorithmic_behavior:
  - Template content:
    - Header at line 1: `# Wrong Directory Path`.
    - Attempt description with `{{ACTION}}` and `{{FILE_PATH}}` at line 3.
    - Canonical target path with `{{CORRECT_PATH}}` at line 4.
    - Suggested command using `{{FILE_PATH}}` at line 6.
  - The template itself has no executable code. Its algorithmic behavior is realized through `load_and_render_safe`, which substitutes placeholders in [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/template-loader.sh:170).
  - Read validator caller:
    - [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/loop-read-validator.sh:129) computes `CORRECT_PATH="$ACTIVE_LOOP_DIR/$CLAUDE_FILENAME"`.
    - If `FILE_PATH != CORRECT_PATH`, it renders this template with `ACTION=read`, `FILE_PATH`, and `CORRECT_PATH`, then exits 2 at lines 131-139.
  - Write validator caller:
    - [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/loop-write-validator.sh:177) computes the same canonical path for writes.
    - If `FILE_PATH != CORRECT_PATH`, it renders this template with `ACTION=write to`, then exits 2 at lines 179-187.
  - This creates a deterministic reject transition: attempted tool action -> path canonicalization check -> block message -> exit 2.

- inputs_outputs_state:
  - Inputs:
    - `ACTION`: usually `read` from the Read hook or `write to` from the Write hook.
    - `FILE_PATH`: the path supplied by the tool invocation.
    - `CORRECT_PATH`: active loop directory plus the expected filename.
  - Outputs:
    - Rendered Markdown block written to stderr by the calling hook.
    - Calling validator exits with code 2 to block the tool action.
  - State transitions:
    - No repository or loop state is modified by the template.
    - The only state transition is validator control flow from allowed candidate to blocked action when path equality fails.
  - State-file branch context:
    - The broader branch invariant for state mutation is implemented elsewhere: [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/loop-common.sh:251) allows cancel only when `.cancel-requested` exists and the command is exactly `mv active-loop/state.md active-loop/cancel-state.md`.
    - [hooks/loop-bash-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/loop-bash-validator.sh:81) and [hooks/loop-bash-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/loop-bash-validator.sh:218) call that authorization gate before permitting any `state.md` move/copy source or destination pattern.
    - This assigned template is adjacent to, but not the direct enforcer of, the “only cancel may mv state” algorithm.

- gates_or_invariants:
  - Path equality is strict: `FILE_PATH` must equal `ACTIVE_LOOP_DIR/$CLAUDE_FILENAME`; otherwise the action is denied.
  - The message must preserve both attempted and correct paths so the agent can recover by using the canonical active-loop path.
  - Placeholder names are uppercase and valid under the template syntax described in [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/template-loader.sh:7).
  - The template must exist because both read and write validators pass it to `load_and_render_safe`; missing-template behavior falls back to inline messages, but the intended guard UX depends on this file.
  - The caller’s invariant is block-on-mismatch, exit 2, with no state mutation.

- dependencies_and_callers:
  - Direct callers:
    - [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/loop-read-validator.sh:135).
    - [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/loop-write-validator.sh:183).
  - Rendering dependency:
    - [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/template-loader.sh:58), especially single-pass `render_template`.
  - Shared setup dependency:
    - [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/hooks/lib/loop-common.sh:46) sources the template loader and initializes `TEMPLATE_DIR`.
  - Test coverage dependency:
    - [tests/test-template-references.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/tests/test-template-references.sh:56) scans validators for template references and verifies referenced files exist.
    - [tests/test-templates-comprehensive.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state/tests/test-templates-comprehensive.sh:90) loads all Markdown templates and validates placeholder syntax.

- edge_cases_or_failure_modes:
  - If `FILE_PATH` has a correct filename but is in an old loop directory or another `.humanize/rlcr` directory, the callers compute the active-loop `CORRECT_PATH` and block.
  - If `FILE_PATH` differs only by path spelling, symlink, relative/absolute form, or extra path segment, the callers’ raw string comparison can block even if the filesystem target might resolve similarly.
  - The suggested command at line 6 says `cat {{FILE_PATH}}`, not `cat {{CORRECT_PATH}}`. That is notable because the block says the attempted path is wrong but then suggests reading the attempted path. The fallback in callers instead points to the correct path conceptually. This may be a UX bug or intentional “show attempted command” text, but it is a skip-risk detail for reviewers.
  - If template rendering fails or the file is missing, `load_and_render_safe` falls back to inline text in both callers, preserving the block decision but changing message content.
  - Special characters or spaces in `FILE_PATH` and `CORRECT_PATH` are interpolated literally; the template wraps paths in backticks, but line 6 does not shell-quote the path.

- validation_or_tests:
  - Direct inspection confirmed placeholders at lines 3-6 are `ACTION`, `FILE_PATH`, and `CORRECT_PATH`.
  - `rg` found exactly the relevant call sites in `loop-read-validator.sh` and `loop-write-validator.sh`.
  - Template existence is covered by `tests/test-template-references.sh`, which scans critical shell scripts for `load_and_render_safe "$TEMPLATE_DIR" "..."` references and fails on missing files.
  - Syntax/loading is covered by `tests/test-templates-comprehensive.sh`, which iterates all `prompt-template/**/*.md` files and validates placeholder syntax.
  - No direct execution was needed for this template because it is data consumed by the hook validators; the assigned test execution above also incidentally confirms template-loader fallback behavior, though render paths were limited by the read-only sandbox’s here-string temp-file restriction.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 2 item sections present; each assigned item heading appears once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`