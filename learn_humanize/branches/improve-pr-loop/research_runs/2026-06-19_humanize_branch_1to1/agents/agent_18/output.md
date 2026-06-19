# agent_18 improve-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `61f03daecb8ff9c20e535a636b90aa92a3d7c9b2`

## Item Evidence

### IMPROVE_PR_LOOP-HZ-018 `file` `commands/cancel-pr-loop.md`
- cursor: `[_]`
- core_role: Slash-command workflow definition for cancelling an active PR loop. It is a thin command contract around `scripts/cancel-pr-loop.sh`, not an implementation file.
- algorithmic_behavior: The command allows only two Bash invocations, `scripts/cancel-pr-loop.sh` and `scripts/cancel-pr-loop.sh --force`, via frontmatter at `commands/cancel-pr-loop.md:1-4`. The human-facing workflow instructs the agent to run the script, inspect only the first output line, and map `NO_LOOP` / `NO_ACTIVE_LOOP` to “No active PR loop found” or `CANCELLED` to the script’s cancellation message at `commands/cancel-pr-loop.md:11-20`.
- inputs_outputs_state: Input is the active PR-loop state under `.humanize/pr-loop/`, resolved by the script using `CLAUDE_PROJECT_DIR` or `pwd` in `scripts/cancel-pr-loop.sh:72-76`. Output is a status token on stdout. The state transition is implemented by the script: create `.cancel-requested`, then rename `state.md` to `cancel-state.md` at `scripts/cancel-pr-loop.sh:118-122`.
- gates_or_invariants: The command defines the key invariant that a PR loop is active only if `state.md` exists in the newest `.humanize/pr-loop/` directory at `commands/cancel-pr-loop.md:21`. It explicitly excludes RLCR loops and points to `/humanize:cancel-rlcr-loop` instead at `commands/cancel-pr-loop.md:25`.
- dependencies_and_callers: Depends directly on `scripts/cancel-pr-loop.sh`. Related active-loop guard in `scripts/setup-pr-loop.sh:222-240` blocks starting another loop and tells users to cancel the PR loop first. Shared PR-loop detection `find_active_pr_loop` in `hooks/lib/loop-common.sh:795-814` has the same newest-directory plus `state.md` concept, though the cancel script performs its own inline `ls | sort -r | head -1` lookup.
- edge_cases_or_failure_modes: No loop directory yields `NO_LOOP` and exit `1` from `scripts/cancel-pr-loop.sh:76-81`. Newest loop directory without `state.md` yields `NO_ACTIVE_LOOP` and exit `1` at `scripts/cancel-pr-loop.sh:88-98`. Unknown flags exit `3` at `scripts/cancel-pr-loop.sh:60-64`; `--force` is parsed but currently has no behavioral effect at `scripts/cancel-pr-loop.sh:24-31`.
- validation_or_tests: `tests/test-pr-loop-scripts.sh:192-207` validates no-loop behavior returns exit `1` and `NO_LOOP`. `tests/test-pr-loop-scripts.sh:211-244` creates `.humanize/pr-loop/<timestamp>/state.md`, runs the script, expects `CANCELLED`, and verifies `state.md` was renamed to `cancel-state.md`.
- skip_candidate: `no`

### IMPROVE_PR_LOOP-HZ-048 `file` `tests/test-ansi-parsing.sh`
- cursor: `[_]`
- core_role: Executable specification for portable ANSI-stripping and pass/fail counter extraction used by the aggregate test runner.
- algorithmic_behavior: The test encodes the parser used in `tests/run-all-tests.sh`: set `esc=$'\033'`, remove SGR escape sequences with `sed "s/${esc}\\[[0-9;]*m//g"`, then extract numeric counts using `grep -oE 'Passed:[[:space:]]*[0-9]+'` / `Failed:[[:space:]]*[0-9]+` followed by a final numeric grep. The same implementation appears in `tests/run-all-tests.sh:121-125`.
- inputs_outputs_state: Inputs are simulated test-output strings containing ANSI SGR sequences, plain text summaries, bold/color combinations, and multi-line summaries. Outputs are parsed `passed` / `failed` numeric strings and the script’s own colored summary at `tests/test-ansi-parsing.sh:163-178`. Local state consists of `TESTS_PASSED` and `TESTS_FAILED` counters initialized at `tests/test-ansi-parsing.sh:18-19` and mutated by `pass()` / `fail()` at `tests/test-ansi-parsing.sh:21-31`.
- gates_or_invariants: The invariant is cross-platform `sed` portability: comments at `tests/test-ansi-parsing.sh:38-40` state the test uses ANSI-C quoting rather than non-portable hex escapes. The parser only strips SGR codes matching `ESC[` plus digits/semicolons ending in `m`; it does not attempt broader CSI parsing.
- dependencies_and_callers: This test has no sourced helper dependency; it defines local pass/fail functions. It is included in the aggregate suite list at `tests/run-all-tests.sh:31-68`, specifically `test-ansi-parsing.sh` at `tests/run-all-tests.sh:42`.
- edge_cases_or_failure_modes: Covered cases include basic color stripping at `tests/test-ansi-parsing.sh:44-53`, multiple color spans at `tests/test-ansi-parsing.sh:59-67`, passed-count extraction at `tests/test-ansi-parsing.sh:73-81`, failed-count and zero extraction at `tests/test-ansi-parsing.sh:87-109`, multi-line summaries with `tail -1` semantics at `tests/test-ansi-parsing.sh:115-130`, plain text without ANSI codes at `tests/test-ansi-parsing.sh:136-144`, and combined bold/color at `tests/test-ansi-parsing.sh:150-158`.
- validation_or_tests: The file is itself the validation. It exits `0` only when `TESTS_FAILED` is zero at `tests/test-ansi-parsing.sh:170-178`; otherwise it exits `1`. It validates the exact aggregate-runner parser in `tests/run-all-tests.sh:121-125`, so regressions in ANSI stripping would corrupt suite totals.
- skip_candidate: `no`

### IMPROVE_PR_LOOP-HZ-078 `file` `prompt-template/block/force-push-detected.md`
- cursor: `[_]`
- core_role: Prompt block template for the PR-loop force-push gate. It defines the user-facing transition when review tracking must be reset after a non-fast-forward commit change.
- algorithmic_behavior: The template renders old and new commit SHAs via `{{OLD_COMMIT}}` and `{{NEW_COMMIT}}` at `prompt-template/block/force-push-detected.md:3`, explains that force pushes reset review state at line `5`, and gives required restart actions at lines `7-10`. It instructs the user to post a new bot trigger comment using `{{BOT_MENTION_STRING}}`.
- inputs_outputs_state: Inputs are template variables supplied by `hooks/pr-loop-stop-hook.sh:414-416`: `OLD_COMMIT`, `NEW_COMMIT`, `BOT_MENTION_STRING`, and `PR_NUMBER`. Output is a rendered block reason embedded in a JSON hook response with `decision: "block"` at `hooks/pr-loop-stop-hook.sh:418-420`.
- gates_or_invariants: The gate fires when a stored `PR_LATEST_COMMIT_SHA` exists, current `HEAD` differs, and `git merge-base --is-ancestor "$PR_LATEST_COMMIT_SHA" "$CURRENT_HEAD"` reports `no`, which indicates the tracked commit is no longer reachable from the new head. This detection is implemented at `hooks/pr-loop-stop-hook.sh:367-379`.
- dependencies_and_callers: Called through `load_and_render_safe` in `hooks/pr-loop-stop-hook.sh:414-416`, with a short inline fallback at `hooks/pr-loop-stop-hook.sh:411-413`. It depends on state values parsed earlier in the PR loop and on git/gh operations for current head and commit timestamp lookup.
- edge_cases_or_failure_modes: If the new commit timestamp cannot be fetched through `gh pr view`, the hook falls back to the current UTC timestamp at `hooks/pr-loop-stop-hook.sh:387-393`. The hook updates state before blocking: `latest_commit_sha`, `latest_commit_at`, `last_trigger_at`, and `trigger_comment_id` are rewritten/cleared at `hooks/pr-loop-stop-hook.sh:395-403`, preventing stale trigger comments from passing later validation.
- validation_or_tests: No direct test file was assigned for this template, but it is reachable through the PR-loop stop hook’s force-push path. Template reference coverage is implied by the repository’s template-reference/comprehensive tests listed in `tests/run-all-tests.sh:31-68`.
- skip_candidate: `no`

### IMPROVE_PR_LOOP-HZ-108 `file` `prompt-template/claude/finalize-phase-skipped-prompt.md`
- cursor: `[_]`
- core_role: Claude prompt template for entering RLCR Finalize Phase when code review was skipped. It defines the manual-verification contract and final output obligations for an unvalidated implementation path.
- algorithmic_behavior: The template warns that review was skipped using `{{REVIEW_SKIP_REASON}}` at `prompt-template/claude/finalize-phase-skipped-prompt.md:1-5`, requires manual verification steps at lines `7-13`, optionally allows simplification through `code-simplifier:code-simplifier` at lines `15-24`, enforces no behavior changes and no test regressions at lines `26-34`, references plan/tracker files at lines `35-39`, and requires a finalize summary at lines `40-50`.
- inputs_outputs_state: Inputs are supplied by `enter_finalize_phase` in `hooks/loop-codex-stop-hook.sh:1069-1075`: `FINALIZE_SUMMARY_FILE`, `PLAN_FILE`, `GOAL_TRACKER_FILE`, `REVIEW_SKIP_REASON`, `BASE_BRANCH`, and `START_BRANCH`. Output is a rendered `reason` in a JSON hook response with `decision: "block"` and a system message at `hooks/loop-codex-stop-hook.sh:1105-1113`.
- gates_or_invariants: The state transition into finalize happens before rendering: `state.md` is renamed to `finalize-state.md` at `hooks/loop-codex-stop-hook.sh:1036-1037`, and the required summary path is set to `$LOOP_DIR/finalize-summary.md` at `hooks/loop-codex-stop-hook.sh:1039`. The skipped template is selected only when `skip_reason` is non-empty at `hooks/loop-codex-stop-hook.sh:1042`.
- dependencies_and_callers: Called by `enter_finalize_phase`, which is also used for the normal successful review path with an empty skip reason at `hooks/loop-codex-stop-hook.sh:1024-1027`. The skipped prompt is loaded through `load_and_render_safe`; if unavailable, the hook has an inline fallback beginning at `hooks/loop-codex-stop-hook.sh:1043`.
- edge_cases_or_failure_modes: Because skipped review means the implementation was not fully validated, the template shifts validation responsibility to manual checks and available tests. It also constrains optional simplification to functionality-equivalent changes only, preventing the finalize phase from becoming a feature/change phase.
- validation_or_tests: The broader finalize behavior is covered by `tests/test-finalize-phase.sh` in the aggregate suite list at `tests/run-all-tests.sh:31-68`. The hook’s normal transition path explicitly treats “no issues found” as proceed-to-finalize at `hooks/loop-codex-stop-hook.sh:1024-1027`; the skipped path is distinguished by non-empty `skip_reason`.
- skip_candidate: `no`

### IMPROVE_PR_LOOP-HZ-138 `file` `tests/robustness/test-session-robustness.sh`
- cursor: `[_]`
- core_role: Robustness specification for active RLCR session detection under concurrent/session-directory edge cases. It directly tests `find_active_loop` from `hooks/lib/loop-common.sh`.
- algorithmic_behavior: The script sources `hooks/lib/loop-common.sh` and shared test helpers at `tests/robustness/test-session-robustness.sh:14-18`, creates temporary loop-directory layouts, calls `find_active_loop "$TEST_DIR/rlcr"`, and checks expected path-or-empty outputs across 18 cases. The target function is defined at `hooks/lib/loop-common.sh:156-174`.
- inputs_outputs_state: Inputs are filesystem states under `$TEST_DIR/rlcr`: timestamped directories, arbitrary names, symlinks, spaces, nested paths, and marker files. Valid active markers are `state.md` and `finalize-state.md`, matching `hooks/lib/loop-common.sh:168-170`. Output is either the newest active loop directory path with trailing slash removed or an empty string.
- gates_or_invariants: The central invariant is newest-only detection. `find_active_loop` lists immediate child directories, sorts descending, chooses one newest directory, and checks only that directory for `state.md` or `finalize-state.md` at `hooks/lib/loop-common.sh:164-173`. Comments at `hooks/lib/loop-common.sh:151-154` state this prevents older “zombie” loops from being revived.
- dependencies_and_callers: Depends on `setup_test_dir`, `pass`, `fail`, and `print_test_summary` from `tests/test-helpers.sh:21-68`. Runtime callers of `find_active_loop` include loop validators and setup scripts, found in `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-bash-validator.sh`, `hooks/loop-plan-file-validator.sh`, `hooks/loop-codex-stop-hook.sh`, `scripts/setup-pr-loop.sh`, and `scripts/setup-rlcr-loop.sh`.
- edge_cases_or_failure_modes: Positive cases cover newest session with `state.md`, finalize phase detection, many sessions under 1000ms, both state files, and rapid creation at `tests/robustness/test-session-robustness.sh:33-118` and `240-257`. Negative/edge cases cover empty or missing base directory, files without subdirectories, newest directory lacking state despite older active state, unexpected names, symlinked directories, spaces in names, one-level-only lookup, finished `complete-state.md`, cancelled `cancel-state.md`, mixed finished/newer versus active/older sessions, and Unicode-graceful naming at `tests/robustness/test-session-robustness.sh:128-317`.
- validation_or_tests: The file is included in the aggregate runner as `robustness/test-session-robustness.sh` at `tests/run-all-tests.sh:54`. It exits with the result of `print_test_summary` at `tests/robustness/test-session-robustness.sh:318-323`, which returns nonzero when any assertion failed.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `5/5 item sections present exactly once in Item Evidence`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`