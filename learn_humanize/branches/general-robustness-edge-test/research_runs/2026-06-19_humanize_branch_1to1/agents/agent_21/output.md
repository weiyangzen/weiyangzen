# agent_21 general-robustness-edge-test 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `4a4e59ce0cc5613c54d15754a29c7d2a2e9be058`

## Item Evidence

### GENERAL_ROBUSTNESS_EDGE_TEST-HZ-021 `file` `commands/start-pr-loop.md`
- cursor: `[_]`
- core_role: Slash-command workflow definition for starting a PR review loop. The file is intentionally thin: frontmatter defines description, accepted argument shape, tool allowlist, and hidden slash-command behavior at `commands/start-pr-loop.md:1-5`, then delegates execution to `scripts/setup-pr-loop.sh` at `commands/start-pr-loop.md:10-14`.
- algorithmic_behavior: Defines the human-facing sequence: detect current-branch PR, fetch bot review comments, fix issues, push changes, trigger bot re-review, let the Stop Hook poll, and use local Codex validation before either continuing or ending the loop at `commands/start-pr-loop.md:16-24`.
- inputs_outputs_state: Inputs are `$ARGUMENTS`, especially `--claude`, `--codex`, `--max N`, `--codex-model MODEL:EFFORT`, and `--codex-timeout SECONDS` from `commands/start-pr-loop.md:3` and `commands/start-pr-loop.md:25-30`. Runtime output is produced by the setup script: active loop state, prompt files, goal tracker, and user instructions under `.humanize/pr-loop/`; `scripts/setup-pr-loop.sh:535-555` creates `state.md`, and `scripts/setup-pr-loop.sh:641-771` creates the initial prompt.
- gates_or_invariants: Requires at least one bot flag per `commands/start-pr-loop.md:25-30`, mirrored by script validation at `scripts/setup-pr-loop.sh:179-190`. Important workflow gates are: write summaries, push changes, tag correct bots, do not edit loop state, and rely on the Stop Hook at `commands/start-pr-loop.md:50-57`. Termination gates are max iterations, all monitored bots approved, or cancellation at `commands/start-pr-loop.md:58-62`.
- dependencies_and_callers: Direct dependency is `${CLAUDE_PLUGIN_ROOT}/scripts/setup-pr-loop.sh`, enforced by `allowed-tools` at `commands/start-pr-loop.md:4`. The script depends on shared loop helpers at `scripts/setup-pr-loop.sh:210-214`, blocks concurrent RLCR/PR loops at `scripts/setup-pr-loop.sh:220-241`, and requires git, GitHub CLI auth, and Codex availability at `scripts/setup-pr-loop.sh:243-277`.
- edge_cases_or_failure_modes: Failure cases include no bot flag, unknown option, nonnumeric `--max` or timeout, active existing loop, missing git repo/history, missing or unauthenticated `gh`, missing `codex`, or inability to resolve a PR. Fork PR handling is explicitly part of setup script context resolution at `scripts/setup-pr-loop.sh:290-310`.
- validation_or_tests: Covered by PR loop script/system tests found in `tests/test-pr-loop-scripts.sh`, `tests/test-pr-loop-system.sh`, and robustness setup tests; this assigned file itself is a command contract rather than executable logic.
- skip_candidate: `no`

### GENERAL_ROBUSTNESS_EDGE_TEST-HZ-051 `file` `tests/test-codex-review-merge.sh`
- cursor: `[_]`
- core_role: Executable specification for `detect_review_issues`, the Codex review-log classifier used to decide whether the RLCR loop continues with another implementation round or can proceed toward finalization.
- algorithmic_behavior: The test states the intended algorithm at `tests/test-codex-review-merge.sh:11-15`: scan the entire log from line 1, find the first `[P<digit>]` marker appearing in the first 10 characters of a line, extract from that matching line to EOF, return no-issues when absent. Implementation matches this in `hooks/lib/loop-common.sh:343-386`, using `awk` to find the first line and `sed` to extract the tail.
- inputs_outputs_state: Inputs are synthetic review logs at `$CACHE_DIR/round-N-codex-review.log`, with `LOOP_DIR` and `CACHE_DIR` exported by `setup_test_env` at `tests/test-codex-review-merge.sh:47-54`. Outputs are function stdout prefixed with `## Codex Review Issues`, exit codes, and an audit result file at `$LOOP_DIR/round-N-review-result.md` created by `hooks/lib/loop-common.sh:345-347` and `hooks/lib/loop-common.sh:375-380`.
- gates_or_invariants: Exit code `0` means issues found and loop should continue, `1` means no issues, and `2` is a hard error for missing or empty logs, as documented in `hooks/lib/loop-common.sh:326-331`. Marker detection is position-gated to the first 10 characters only at `hooks/lib/loop-common.sh:358-366`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at `tests/test-codex-review-merge.sh:41-42`. Runtime caller is `hooks/loop-codex-stop-hook.sh`, which invokes `detect_review_issues` during Codex review processing at `hooks/loop-codex-stop-hook.sh:978-981`.
- edge_cases_or_failure_modes: Tests cover valid markers with dash prefixes, markers at char 0, ignored markers later in a line, absent markers, missing logs, empty logs, markers late in files over 50 lines, markers early in long files, multiple markers where the first begins extraction, result-file creation, and exactly 50-line logs at `tests/test-codex-review-merge.sh:57-354`.
- validation_or_tests: This file is the validation artifact. It uses manual pass/fail counters and exits nonzero when `TESTS_FAILED` is positive at `tests/test-codex-review-merge.sh:356-368`.
- skip_candidate: `no`

### GENERAL_ROBUSTNESS_EDGE_TEST-HZ-081 `file` `prompt-template/block/git-not-clean-untracked.md`
- cursor: `[_]`
- core_role: Prompt/block template injected into the RLCR Stop Hook’s git-cleanliness blocker when untracked files other than `.humanize*` are present.
- algorithmic_behavior: Provides advisory classification for untracked files: build outputs, dependency directories, IDE/editor files, logs, caches, and temporary files should usually be ignored rather than committed at `prompt-template/block/git-not-clean-untracked.md:2-10`.
- inputs_outputs_state: Has no template variables. Input is the Stop Hook’s computed `OTHER_UNTRACKED` set; output is markdown appended into `SPECIAL_NOTES`, then rendered into the blocking JSON reason returned to Claude.
- gates_or_invariants: Participates in the “do not exit with dirty git state” invariant. The actual gate is in `hooks/loop-codex-stop-hook.sh:493-545`: any cached git status creates `GIT_ISSUES`, other untracked files load this template at `hooks/loop-codex-stop-hook.sh:513-520`, and the hook returns a `decision: block` response at `hooks/loop-codex-stop-hook.sh:537-544`.
- dependencies_and_callers: Loaded through `load_template "$TEMPLATE_DIR" "block/git-not-clean-untracked.md"` at `hooks/loop-codex-stop-hook.sh:516`. The surrounding git-not-clean message is rendered with `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:527-535`.
- edge_cases_or_failure_modes: `.humanize*` untracked entries are separated into a different note at `hooks/loop-codex-stop-hook.sh:501-511`. If this template is missing or empty, the hook falls back to “Review untracked files - add to .gitignore or commit them.” at `hooks/loop-codex-stop-hook.sh:516-519`.
- validation_or_tests: Template loading is exercised indirectly by Stop Hook and template-loader tests; this file’s behavior is mainly verified by the git-cleanliness blocker path rather than by standalone execution.
- skip_candidate: `no`

### GENERAL_ROBUSTNESS_EDGE_TEST-HZ-111 `file` `prompt-template/claude/next-round-prompt.md`
- cursor: `[_]`
- core_role: Claude continuation prompt template for the RLCR “next round” transition after Codex review found issues.
- algorithmic_behavior: Tells Claude the work is unfinished, forces rereading the original plan, injects Codex review content, requires Todos for all discovered issues, and prevents narrow handling of only the highest-priority issue at `prompt-template/claude/next-round-prompt.md:1-19`.
- inputs_outputs_state: Inputs are `PLAN_FILE`, `REVIEW_CONTENT`, and `GOAL_TRACKER_FILE` at `prompt-template/claude/next-round-prompt.md:6`, `prompt-template/claude/next-round-prompt.md:18`, and `prompt-template/claude/next-round-prompt.md:24`. Output is `round-N-prompt.md`, written after the Stop Hook increments `current_round` at `hooks/loop-codex-stop-hook.sh:1471-1492`.
- gates_or_invariants: Enforces plan alignment and complete issue tracking at `prompt-template/claude/next-round-prompt.md:3-14`. It also defines a goal-tracker write gate: after Round 0 Claude may read the tracker but cannot directly modify it; requested changes must be summarized as a “Goal Tracker Update Request” at `prompt-template/claude/next-round-prompt.md:22-31`.
- dependencies_and_callers: Rendered by `hooks/loop-codex-stop-hook.sh` using `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:1480-1492`. It depends on Codex review content produced earlier in the hook, including `REVIEW_CONTENT=$(cat "$REVIEW_RESULT_FILE")` at `hooks/loop-codex-stop-hook.sh:1351-1358`.
- edge_cases_or_failure_modes: If review content includes template-like braces, safe rendering matters because `REVIEW_CONTENT` is untrusted generated text. If this template cannot be loaded, the hook falls back to a shorter inline next-round prompt at `hooks/loop-codex-stop-hook.sh:1480-1489`.
- validation_or_tests: Covered by template rendering tests such as `tests/test-template-loader.sh` and comprehensive template tests; the runtime transition is additionally covered by Stop Hook/finalize phase tests.
- skip_candidate: `no`

### GENERAL_ROBUSTNESS_EDGE_TEST-HZ-141 `file` `tests/robustness/test-state-transition-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable spec for RLCR state-file parsing, active-loop discovery, finalize/cancel state handling, and state transition edge cases.
- algorithmic_behavior: Creates synthetic `.humanize/rlcr/<timestamp>/` loop directories and state variants, then exercises `parse_state_file_strict`, `get_current_round`, and `find_active_loop`. Helper state writers are defined at `tests/robustness/test-state-transition-robustness.sh:30-89`.
- inputs_outputs_state: Inputs are generated `state.md`, `finalize-state.md`, and `cancel-state.md` files with YAML frontmatter. Outputs are pass/fail assertions and a final test summary via `print_test_summary` at `tests/robustness/test-state-transition-robustness.sh:419-424`.
- gates_or_invariants: Strict parser requires YAML separators plus `current_round`, `max_iterations`, `review_started`, and `base_branch`, and validates numeric rounds plus boolean `review_started` in `hooks/lib/loop-common.sh:251-323`. Active-loop discovery checks only the newest lexicographic child directory and only treats `state.md` or `finalize-state.md` as active at `hooks/lib/loop-common.sh:150-173`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` and `tests/test-helpers.sh` at `tests/robustness/test-state-transition-robustness.sh:14-18`. The same helpers are used by read/write/edit/bash/plan validators and the Stop Hook, as shown by callers of `find_active_loop` and `parse_state_file_strict` in `hooks/loop-*-validator.sh`.
- edge_cases_or_failure_modes: Covers round 0, arbitrary round progression, max round equality, finalize-state detection, finalize coexisting with regular state, cancel-state being inactive, new state after cancel, negative rounds being parsed, over-max rounds being parsed with enforcement elsewhere, nonnumeric rounds rejected, required fields missing, newest directory selection, lexicographic ordering, and nested state files ignored at `tests/robustness/test-state-transition-robustness.sh:98-417`.
- validation_or_tests: This file is itself the validation suite. It defines 16 named tests and exits with the aggregated summary result at `tests/robustness/test-state-transition-robustness.sh:423-424`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `5/5 item sections present above; item IDs are intentionally not repeated here to preserve exactly-once occurrence`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`