# agent_23 impl-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 4
- source_commit: `96455ba5aff935988d78439ca55427c603b1adcd`

## Item Evidence

### IMPL_PR_LOOP-HZ-023 `file` `hooks/hooks.json`
- cursor: `[_]`
- core_role: Claude hook manifest for the RLCR and PR loop control plane. It binds Claude hook events to repository validators and stop hooks, making this file the dispatch table for pre-action guards and loop review transitions.
- algorithmic_behavior: On `UserPromptSubmit`, it runs `hooks/loop-plan-file-validator.sh` to validate plan-file state before a user prompt proceeds (`hooks/hooks.json:4-13`). On `PreToolUse`, it routes `Write`, `Edit`, `Read`, and `Bash` tools to specialized validators (`hooks/hooks.json:14-51`). On `Stop`, it runs both `loop-codex-stop-hook.sh` and `pr-loop-stop-hook.sh`, each with a 7200 second timeout (`hooks/hooks.json:52-67`).
- inputs_outputs_state: Input is Claude’s hook event plus tool-specific JSON payload passed to the command hook. Output is the delegated hook script exit status and stderr/stdout block message. The manifest itself stores no loop state, but it determines which scripts can read `.humanize/.../state.md`, validate active rounds, block writes, or advance the stop-review workflow.
- gates_or_invariants: The invariant is tool-class separation: write, edit, read, bash, prompt-submit, and stop events must go through different validators. Bash writes are especially guarded by `loop-bash-validator.sh`, which validates JSON input, fails closed on malformed state, allows no active-loop cases, and blocks goal-tracker Bash mutation (`hooks/loop-bash-validator.sh:24-67`, `hooks/loop-bash-validator.sh:349-357`).
- dependencies_and_callers: Depends on `${CLAUDE_PLUGIN_ROOT}` resolving to the plugin root and on all referenced scripts being present/executable. Tests statically scan these hook scripts as template users in `tests/test-template-references.sh:56-64`, and many tests invoke the delegated validators directly, e.g. `tests/test-plan-file-hooks.sh` and `tests/test-pr-loop-hooks.sh`.
- edge_cases_or_failure_modes: Missing `CLAUDE_PLUGIN_ROOT`, missing scripts, or non-executable scripts would disable enforcement at dispatch time. Both stop hooks are registered for `Stop`, so each stop hook must internally no-op or guard by loop type. Exact matcher names mean a new tool class would not be protected until added here.
- validation_or_tests: Static reference coverage exists through `tests/test-template-references.sh:56-69`; direct hook behavior is covered by tests that invoke the validators and stop hooks, including `tests/test-plan-file-hooks.sh` and `tests/test-pr-loop-hooks.sh`.
- skip_candidate: `no`

### IMPL_PR_LOOP-HZ-053 `file` `tests/test-helpers.sh`
- cursor: `[_]`
- core_role: Shared Bash test harness for loop tests. It is not the loop algorithm itself, but it supplies the pass/fail/skip counters, temporary workspace setup, and mock git repository bootstrap used by executable specs.
- algorithmic_behavior: Defines colored result emitters `pass`, `fail`, and `skip` that mutate global counters (`tests/test-helpers.sh:30-52`). `print_test_summary` reports totals and returns success only when `TESTS_FAILED` is zero (`tests/test-helpers.sh:58-77`). `setup_test_dir` creates `TEST_DIR` with exit cleanup (`tests/test-helpers.sh:86-89`). `init_test_git_repo` initializes a git repo, configures test identity, commits `file.txt`, and restores the previous directory (`tests/test-helpers.sh:93-104`).
- inputs_outputs_state: Inputs are test names/messages, optional expected/got values, optional summary title, and a target directory for git setup. Outputs are colored console lines, return status from `print_test_summary`, global counters `TESTS_PASSED`, `TESTS_FAILED`, `TESTS_SKIPPED`, and a `TEST_DIR` environment variable.
- gates_or_invariants: Any failed assertion increments `TESTS_FAILED`; the summary function is the final gate that converts accumulated failures into process status. `init_test_git_repo` ensures git-dependent tests start from a committed baseline with deterministic user config.
- dependencies_and_callers: Sourced by the PR loop main runner at `tests/test-pr-loop.sh:18-20`; `tests/test-pr-loop-lib.sh:18-21` loads it if helpers are not already present; robustness tests source it and call `setup_test_dir`, e.g. `tests/robustness/test-plan-file-robustness.sh:84-86`. `init_test_git_repo` is used in PR hook tests at `tests/test-pr-loop-hooks.sh:30-31`.
- edge_cases_or_failure_modes: `setup_test_dir` installs a single `EXIT` trap, so repeated setup calls can overwrite prior cleanup. The cleanup trap embeds `TEST_DIR` without shell-quoting at execution time, which is fragile for paths containing spaces. `init_test_git_repo` assumes `git` is installed and that `cd`/commit operations succeed.
- validation_or_tests: No dedicated unit test for this helper file was found; it is indirectly validated by the many tests that source it and rely on its summary status.
- skip_candidate: `yes: shared harness support rather than core RLCR/PR loop transition logic, though it is required by executable specs`

### IMPL_PR_LOOP-HZ-083 `file` `prompt-template/block/goal-tracker-bash-write.md`
- cursor: `[_]`
- core_role: Block-message template for the Round 0 gate that prevents Bash-based mutation of `goal-tracker.md` and directs the agent through Write/Edit tool paths where validators can enforce file-location rules.
- algorithmic_behavior: Renders a denial headed “Bash Write Blocked,” states not to use Bash to modify `goal-tracker.md`, inserts `{{CORRECT_PATH}}`, and explains that commands such as `cat`, `echo`, `sed`, and `awk` bypass validation hooks (`prompt-template/block/goal-tracker-bash-write.md:1-8`).
- inputs_outputs_state: Input is the `CORRECT_PATH` template variable. Output is a rendered stderr message from `goal_tracker_bash_blocked_message`, which calls `load_and_render_safe` with this template (`hooks/lib/loop-common.sh:396-405`). It does not mutate state itself.
- gates_or_invariants: Used when `loop-bash-validator.sh` detects a Bash command modifying `goal-tracker.md` during round 0; after rendering, the validator exits with block status (`hooks/loop-bash-validator.sh:343-357`). The invariant is that goal-tracker initialization must happen through Write/Edit rather than shell redirection or in-place shell edits.
- dependencies_and_callers: Depends on the shared template loader and single-pass rendering (`hooks/lib/template-loader.sh:50-132`). The Bash validator reaches it through `goal_tracker_bash_blocked_message` in `hooks/lib/loop-common.sh:396-405`.
- edge_cases_or_failure_modes: If the template is missing or empty, `load_and_render_safe` falls back to an inline message (`hooks/lib/template-loader.sh:170-203`). If `CORRECT_PATH` is not supplied, the placeholder remains literal by loader design (`hooks/lib/template-loader.sh:12-13`, `hooks/lib/template-loader.sh:119-122`). Bash mutation pattern coverage has a known limitation for multi-source `cp` forms, documented in `tests/test-bash-validator-patterns.sh:165-168`.
- validation_or_tests: Template existence is checked as a common template in `tests/test-template-references.sh:152-159`. Bash mutation detection around `goal-tracker.md` is covered by pattern tests for redirection, `tee`, in-place editors, file operations, and false positives in `tests/test-bash-validator-patterns.sh:70-168`.
- skip_candidate: `no`

### IMPL_PR_LOOP-HZ-113 `file` `prompt-template/codex/regular-review.md`
- cursor: `[_]`
- core_role: Regular Codex review prompt contract for non-full-alignment RLCR rounds. It defines the review gate that decides whether Claude’s claimed implementation is incomplete or can emit the terminal `COMPLETE` marker.
- algorithmic_behavior: Requires Codex to read the original plan first (`prompt-template/codex/regular-review.md:3-11`), inspect Claude’s summary (`prompt-template/codex/regular-review.md:14-18`), perform implementation review (`prompt-template/codex/regular-review.md:20-31`), perform mandatory goal alignment (`prompt-template/codex/regular-review.md:33-45`), include the injected goal-tracker update section (`prompt-template/codex/regular-review.md:47`), and write findings to the review result file unless everything is complete (`prompt-template/codex/regular-review.md:49-57`).
- inputs_outputs_state: Inputs are template variables including current round, plan file, prompt file, summary content, docs path, goal-tracker file, goal-tracker update section, and review-result file. Output is `round-N-review-prompt.md`, created by `loop-codex-stop-hook.sh` during regular rounds (`hooks/loop-codex-stop-hook.sh:674-751`).
- gates_or_invariants: Deferrals and unfinished items are explicitly treated as incomplete, and `COMPLETE` may only be the last line when all original plan tasks and acceptance criteria are fully satisfied (`prompt-template/codex/regular-review.md:52-57`). The stop hook then strictly inspects the last non-empty review-result line, avoiding false positives like embedded mentions (`hooks/loop-codex-stop-hook.sh:957-967`).
- dependencies_and_callers: Called by `hooks/loop-codex-stop-hook.sh` when the round is not a full-alignment check; every fifth-round-style alignment path uses a different template (`hooks/loop-codex-stop-hook.sh:686-690`, `hooks/loop-codex-stop-hook.sh:721-751`). Rendering depends on the template loader’s single-pass substitution semantics (`hooks/lib/template-loader.sh:50-132`).
- edge_cases_or_failure_modes: If Codex writes output to stdout instead of the requested file, the stop hook copies stdout into the review-result file (`hooks/loop-codex-stop-hook.sh:902-918`). Missing or empty review-result files are hard failures (`hooks/loop-codex-stop-hook.sh:920-955`). Missing placeholders remain unexpanded by design, so a caller that omits a variable can leak a literal placeholder into the prompt.
- validation_or_tests: Template reference scanning includes `loop-codex-stop-hook.sh` among scripts checked for template references (`tests/test-template-references.sh:56-64`). Template rendering behavior, including single-pass placeholder-injection prevention, is covered in `tests/test-template-loader.sh:525-540`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 4/4 required item headings present exactly once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`