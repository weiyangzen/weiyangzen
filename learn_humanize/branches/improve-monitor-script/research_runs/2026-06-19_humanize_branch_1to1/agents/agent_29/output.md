# agent_29 improve-monitor-script 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `5af20b79e6fec323a2d5cb9344a6a584db1c635a`

## Item Evidence

### IMPROVE_MONITOR_SCRIPT-HZ-029 `file` `tests/test-error-scenarios.sh`
- cursor: `[_]`
- core_role:
  - Executable error-path specification for `hooks/lib/template-loader.sh`. It defines how the prompt-template loading/rendering layer must behave when templates, directories, placeholder syntax, or strict shell modes encounter bad or missing inputs.
  - It is included by the aggregate test runner at [tests/run-all-tests.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/run-all-tests.sh:32), where `test-error-scenarios.sh` is part of the ordered suite list at line 42.
- algorithmic_behavior:
  - Initializes its local test harness with `set -uo pipefail`, derives `SCRIPT_DIR`, `PROJECT_ROOT`, sources [template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:13), and resolves `TEMPLATE_DIR` via `get_template_dir` at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:11).
  - Maintains pass/fail state in `TESTS_PASSED` and `TESTS_FAILED`, with `pass()` and `fail()` mutating those counters and printing diagnostics at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:22).
  - Exercises missing template behavior: `load_template "$TEMPLATE_DIR" "non-existing-file.md"` must produce empty output and exit `0` at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:45).
  - Exercises missing directory behavior: `load_template "/non/existing/path" "block/git-push.md"` must also produce empty output and exit `0` at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:58).
  - Exercises `load_and_render` missing-template behavior: missing templates must collapse to empty output without failing the caller at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:71).
  - Exercises empty-content rendering: `render_template "" "VAR=value"` must return empty output and exit `0` at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:84).
  - Exercises literal value safety: values containing regex-like characters such as brackets, parentheses, and asterisks must render literally at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:97).
  - Exercises strict-mode survivability by launching an isolated `bash -c` with `set -euo pipefail`, calling `load_and_render` on a missing template, and requiring `SCRIPT_COMPLETED` to appear at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:112).
  - Exercises `load_and_render_safe` fallback mode, both raw fallback and fallback rendered with variables, at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:137) and [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:150).
  - Exercises template directory validation: valid template roots must pass and invalid roots must fail at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:164) and [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:175).
  - Exercises malformed placeholder invariants: empty `{{}}` placeholders and unclosed `{{UNCLOSED` placeholders must remain unchanged at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:186) and [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:199).
- inputs_outputs_state:
  - Inputs: repository-local `hooks/lib/template-loader.sh`, the resolved `prompt-template` directory, nonexistent template names, invalid absolute paths, literal template strings, fallback strings, and `VAR=value` substitution pairs.
  - Outputs: colored PASS/FAIL lines, expected/got diagnostics for failures, final pass/fail summary, and process exit `0` only when `TESTS_FAILED` is zero at [tests/test-error-scenarios.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-error-scenarios.sh:218).
  - State transitions: each assertion advances `TESTS_PASSED` or `TESTS_FAILED`; final status is derived solely from `TESTS_FAILED`, so this file behaves like a deterministic gate over the template-loader contract.
  - The script intentionally captures command substitutions and `$?` after loader calls, making empty output plus successful exit an explicit state distinct from shell failure.
- gates_or_invariants:
  - Missing template files and missing template directories are non-fatal: empty stdout and exit `0` are required for `load_template` and `load_and_render` missing-template paths.
  - `render_template` must be a literal single-pass renderer: special regex characters in replacement values are not interpreted as regex or shell syntax.
  - `load_and_render_safe` must prevent blank user-facing validator messages by falling back when a template is missing and by rendering placeholders inside the fallback.
  - `validate_template_dir` must distinguish a valid template tree from a missing root.
  - Malformed placeholders must not be destructively rewritten: empty placeholder and unclosed placeholder cases are expected to remain literal.
  - Strict shell mode must not convert missing template lookup into premature script termination.
- dependencies_and_callers:
  - Direct dependency: [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:26), especially `get_template_dir`, `load_template`, `render_template`, `load_and_render`, `load_and_render_safe`, and `validate_template_dir`.
  - `load_template` emits empty output plus a warning on stderr when the file is absent at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:36).
  - `render_template` performs single-pass `awk` substitution from `TMPL_VAR_` environment variables at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:58).
  - `load_and_render_safe` catches missing or empty templates and uses the fallback path at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:170).
  - Aggregate caller: [tests/run-all-tests.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/run-all-tests.sh:47) runs this suite, captures its output, parses pass/fail counts, and treats nonzero exit or failed assertions as a failed suite.
  - Related coverage overlaps with `tests/test-template-loader.sh` and `tests/test-templates-comprehensive.sh`, which cover broader rendering and template loading cases, but this assigned file is specifically the negative/error-scenario gate.
- edge_cases_or_failure_modes:
  - A missing template must not produce non-empty user prompt content accidentally; the test requires empty output in raw loader paths.
  - A missing template must not crash under `set -euo pipefail`; the strict-mode subshell at lines 114-126 is the explicit regression test for command substitution and non-fatal loader behavior.
  - Fallback rendering is a critical failure mode: if fallback variables are not substituted, validators can emit generic or blank block messages.
  - `render_template` currently feeds content to `awk` through a here-string in [template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:129). In this read-only sandbox, that here-string attempted to create a temp file and failed with `cannot create temp file for here document: Operation not permitted`, causing render-dependent assertions to fail. This is an environment/sandbox limitation observed during validation, but it also indicates the implementation depends on writable shell temp storage.
  - Malformed placeholder handling is intentionally tolerant; the test expects no hard validation error for `{{}}` or unclosed placeholders.
- validation_or_tests:
  - Ran `bash tests/test-error-scenarios.sh` in the read-only branch export. Result: exit `1`, 8 passed, 4 failed.
  - Failures were all render-dependent and accompanied by shell errors from [template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:129): `cannot create temp file for here document: Operation not permitted`.
  - Passing portions confirmed missing template, missing directory, missing `load_and_render`, strict-mode continuation, raw fallback without substitution, and valid/invalid directory checks under the current sandbox.
  - Ran `bash tests/test-template-references.sh` as adjacent validation of template existence and safe loader usage. Result: exit `0`, 76 passed, 0 failed, 1 warning for an unrelated unreferenced template. It confirmed `block/wrong-directory-path.md` exists and is referenced by both read and write validators.
- skip_candidate: `no`

### IMPROVE_MONITOR_SCRIPT-HZ-059 `file` `prompt-template/block/wrong-directory-path.md`
- cursor: `[_]`
- core_role:
  - User-facing block template for the directory-path invariant in RLCR loop file validators. It is emitted when a read or write targets a valid round file name but from a directory other than the active loop directory.
  - The template defines the transition from “blocked tool operation” to “actionable correction” by surfacing the attempted action, attempted file path, canonical path, and a suggested `cat` command.
- algorithmic_behavior:
  - Template body is short and fully placeholder-driven: title at line 1, attempted action/path at line 3, canonical path at line 4, and a read command hint at line 6 in [wrong-directory-path.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/prompt-template/block/wrong-directory-path.md:1).
  - Placeholder inputs are `ACTION`, `FILE_PATH`, and `CORRECT_PATH`.
  - In the read validator, the directory-path gate computes `CORRECT_PATH="$ACTIVE_LOOP_DIR/$CLAUDE_FILENAME"` and compares it with the requested `FILE_PATH`; mismatch emits this template with `ACTION=read` and exits `2` at [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/loop-read-validator.sh:129).
  - In the write validator, the equivalent gate computes the active-loop path and emits this template with `ACTION=write to` before exiting `2` at [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/loop-write-validator.sh:177).
  - Both callers use `load_and_render_safe`, so if this template is missing or empty the validators use inline fallback text instead of emitting a blank block message.
- inputs_outputs_state:
  - Inputs from caller state: active loop directory found via `find_active_loop`, current round parsed from `state.md`, requested `FILE_PATH`, derived `CLAUDE_FILENAME`, and the caller-specific `ACTION`.
  - Render inputs: `ACTION=read` or `ACTION=write to`, `FILE_PATH=<requested path>`, and `CORRECT_PATH=<active loop path>/<filename>`.
  - Output: markdown block message to stderr, followed by validator exit code `2` to block the tool call.
  - State transition: no repository state is modified; the validator transitions the tool request from allowed to blocked when `FILE_PATH != CORRECT_PATH`.
- gates_or_invariants:
  - The canonical directory invariant is exact string equality: the requested path must equal `$ACTIVE_LOOP_DIR/$CLAUDE_FILENAME`.
  - The template is only reached after earlier gates determine the file is a relevant round file and after active loop state exists. For reads, earlier checks cover todos files, non-round files, file location outside `.humanize/rlcr`, and wrong round number before this directory path check at [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/loop-read-validator.sh:36).
  - For writes, earlier gates block todos files, prompt writes, state writes, protected plan backup writes, goal tracker writes after round 0, summaries outside `.humanize/rlcr`, and wrong summary round before this directory path check at [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/loop-write-validator.sh:37).
  - The template syntax itself must remain compatible with `render_template`’s placeholder rules: uppercase variable names inside `{{...}}`.
- dependencies_and_callers:
  - Direct callers:
    - [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/loop-read-validator.sh:135)
    - [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/loop-write-validator.sh:183)
  - Shared dependencies:
    - `loop-common.sh` sources the template loader and initializes `TEMPLATE_DIR` at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/loop-common.sh:46).
    - `find_active_loop` chooses the newest loop directory with `state.md` at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/loop-common.sh:62).
    - `parse_state_file` is used by validators before round-aware path decisions at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/loop-common.sh:110).
    - `load_and_render_safe` supplies fallback behavior at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:170).
  - Reference validation explicitly scans shell callers and confirms this template exists at [tests/test-template-references.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-template-references.sh:54).
- edge_cases_or_failure_modes:
  - If `wrong-directory-path.md` is missing, both validators still block with inline fallback because they use `load_and_render_safe`; however, the polished corrective message from this template is lost.
  - If `ACTION`, `FILE_PATH`, or `CORRECT_PATH` is omitted by a caller, the unresolved placeholder remains literal because `render_template` preserves missing variables by design in [template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/hooks/lib/template-loader.sh:120).
  - The final line always suggests `cat {{FILE_PATH}}`, which is directly appropriate for read blocks but less semantically aligned with write blocks where `ACTION=write to`; the write validator still uses this same template. That is not necessarily a correctness bug, but it is a UX mismatch edge case.
  - Path comparison is exact string comparison, so equivalent paths with different normalization, symlinks, relative segments, or trailing slash differences may still block.
  - If there is no active loop directory, callers exit `0` before this template is reached, so the directory invariant is enforced only when loop state is discoverable.
- validation_or_tests:
  - `bash tests/test-template-references.sh` passed with 76 passes, 0 failures, and 1 unrelated warning. It confirmed this template is referenced by both `loop-read-validator.sh` and `loop-write-validator.sh`.
  - `tests/test-templates-comprehensive.sh` includes broad all-template loading and rendering coverage. Its all-template loop loads each `*.md`, extracts uppercase placeholders, renders dummy values, and warns on unreplaced placeholders at [tests/test-templates-comprehensive.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-monitor-script/tests/test-templates-comprehensive.sh:562).
  - The assigned `tests/test-error-scenarios.sh` validates the fallback and malformed placeholder behavior that protects this block template’s callers when rendering fails or variables are absent.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 2 unique Item Evidence sections present, one per assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`