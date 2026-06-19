# agent_18 todo2task-careful-mode 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `7d9dd4fbb5c376ae0a72b7caf81c50909ff14c37`

## Item Evidence

### TODO2TASK_CAREFUL_MODE-HZ-018 `file` `commands/cancel-pr-loop.md`
- cursor: `[_]`
- core_role: Slash-command workflow definition for cancelling an active PR review loop. It delegates all mutation to `scripts/cancel-pr-loop.sh`; the command file itself is a thin operator contract. See `commands/cancel-pr-loop.md:1-25`.
- algorithmic_behavior: Presents a two-step flow: run `"${CLAUDE_PLUGIN_ROOT}/scripts/cancel-pr-loop.sh"` and interpret only the first output token. `NO_LOOP` or `NO_ACTIVE_LOOP` maps to “No active PR loop found”; `CANCELLED` maps to reporting the script’s cancellation message. The key active-loop predicate is explicitly defined as `state.md` existing in the newest `.humanize/pr-loop/` directory at `commands/cancel-pr-loop.md:17-23`.
- inputs_outputs_state: Inputs are `CLAUDE_PLUGIN_ROOT`, the script output token, and the PR loop directory state. Outputs are user-facing status text only. State transitions occur in the script dependency: it finds newest `.humanize/pr-loop/*/`, creates `.cancel-requested`, and renames `state.md` to `cancel-state.md`; related implementation lines are `scripts/cancel-pr-loop.sh:72-81`, `scripts/cancel-pr-loop.sh:88-98`, and `scripts/cancel-pr-loop.sh:118-130`.
- gates_or_invariants: Allowed tools restrict execution to `cancel-pr-loop.sh` with or without `--force` (`commands/cancel-pr-loop.md:3`). It must not reimplement cancellation logic in the prompt layer (`commands/cancel-pr-loop.md:21`). It only targets PR loops and explicitly excludes RLCR loops (`commands/cancel-pr-loop.md:25`).
- dependencies_and_callers: Depends on `scripts/cancel-pr-loop.sh`. The broader system references the command as the PR-loop cancellation escape hatch in `scripts/setup-pr-loop.sh`, `hooks/pr-loop-stop-hook.sh`, and `README.md` search hits. `scripts/cancel-pr-loop.sh` itself uses `CLAUDE_PROJECT_DIR` or `pwd` as project root and shell tools `ls`, `sort`, `grep`, `sed`, `touch`, `mv`.
- edge_cases_or_failure_modes: No loop directory yields `NO_LOOP` and exit 1; newest loop dir without `state.md` yields `NO_ACTIVE_LOOP` and exit 1. If state fields are missing, script defaults PR number/current round/max iterations to `?` before reporting (`scripts/cancel-pr-loop.sh:104-112`). `--force` is parsed but has no additional effect (`scripts/cancel-pr-loop.sh:24-40`). Older loop directories are ignored because newest directory wins.
- validation_or_tests: Related executable coverage exists in `tests/test-pr-loop-scripts.sh` for `cancel-pr-loop.sh` and in robustness/state tests that exercise active PR loop detection. The command file itself is declarative and validated indirectly by template/reference tests.
- skip_candidate: `no`

### TODO2TASK_CAREFUL_MODE-HZ-048 `file` `tests/test-ansi-parsing.sh`
- cursor: `[_]`
- core_role: Executable specification for the test aggregation parser’s ANSI-stripping behavior. It protects `tests/run-all-tests.sh` pass/fail count extraction from colored output portability bugs.
- algorithmic_behavior: Defines local `pass`/`fail` counters, then runs eight cases over the exact stripping expression `sed "s/${esc}\\[[0-9;]*m//g"` with `esc=$'\033'`. It verifies basic color removal, multiple colors, `Passed:` extraction, `Failed:` extraction, zero counts, multiline suite summaries, plain text, and combined bold/color codes (`tests/test-ansi-parsing.sh:41-158`).
- inputs_outputs_state: Inputs are synthetic strings containing ANSI SGR escape sequences and plain summary lines. Outputs are colored `PASS`/`FAIL` lines plus final `Passed:` and `Failed:` counts (`tests/test-ansi-parsing.sh:163-178`). State is limited to shell counters `TESTS_PASSED` and `TESTS_FAILED`.
- gates_or_invariants: The invariant is that stripping ANSI SGR sequences must leave parseable plain text for regexes `Passed:[[:space:]]*[0-9]+` and `Failed:[[:space:]]*[0-9]+`. Exit code is 0 only when `TESTS_FAILED` is zero (`tests/test-ansi-parsing.sh:170-178`). The test specifically requires ANSI-C quoting `$'\033'` for GNU/BSD sed portability (`tests/test-ansi-parsing.sh:38-40`).
- dependencies_and_callers: Included in the aggregate suite list at `tests/run-all-tests.sh:32-44`. It directly mirrors the aggregate parser at `tests/run-all-tests.sh:121-125`, where output is stripped and the last pass/fail counts are added into totals.
- edge_cases_or_failure_modes: Covers zero values, multiple escape sequences on one line, no escape sequences, multiline summaries with trailing failure text, and compound SGR codes such as `1;32m`. It only strips SGR color/style codes ending in `m`; non-SGR ANSI sequences are out of scope.
- validation_or_tests: The file is itself the validation. It is also a regression test for `run-all-tests.sh` counting logic, which depends on final suite summaries retaining exact `Passed:` and `Failed:` labels.
- skip_candidate: `no`

### TODO2TASK_CAREFUL_MODE-HZ-078 `file` `prompt-template/block/force-push-detected.md`
- cursor: `[_]`
- core_role: Blocking prompt template for PR-loop force-push detection. It defines the operator-facing transition when the PR HEAD changes non-fast-forward and existing review state must be invalidated.
- algorithmic_behavior: Renders a “Force Push Detected” block with `{{OLD_COMMIT}}`, `{{NEW_COMMIT}}`, and `{{BOT_MENTION_STRING}}`, then instructs the user to post a fresh trigger comment before continuing (`prompt-template/block/force-push-detected.md:1-17`).
- inputs_outputs_state: Inputs are template variables for old commit, new commit, bot mention string, and an optional PR number supplied by the hook. Output is markdown used as the `reason` in a JSON block decision. The concrete state transition happens in `hooks/pr-loop-stop-hook.sh`: it updates `latest_commit_sha`, updates `latest_commit_at`, clears `last_trigger_at`, clears `trigger_comment_id`, and updates in-memory values before rendering the template (`hooks/pr-loop-stop-hook.sh:395-416`).
- gates_or_invariants: Force push is a hard block: after rendering, the hook emits `{"decision":"block"}` and exits without continuing the round (`hooks/pr-loop-stop-hook.sh:418-420`). The template’s invariant is that rewritten history invalidates previous trigger/review state; a new trigger comment after the new commit is required.
- dependencies_and_callers: Called through `load_and_render_safe "$TEMPLATE_DIR" "block/force-push-detected.md"` in `hooks/pr-loop-stop-hook.sh:411-416`. Depends on the template loader and PR-loop state fields parsed earlier in the hook. Related GitHub data comes from `gh pr view --json commits` to get the new head commit timestamp (`hooks/pr-loop-stop-hook.sh:384-393`).
- edge_cases_or_failure_modes: If the new head timestamp cannot be fetched, the hook falls back to current UTC time (`hooks/pr-loop-stop-hook.sh:390-393`). If the template is missing or invalid, `load_and_render_safe` has an inline fallback (`hooks/pr-loop-stop-hook.sh:411-414`). Stale trigger state is explicitly cleared to avoid accepting pre-force-push comments.
- validation_or_tests: Template reference and comprehensive template tests likely cover placeholder resolution. PR-loop stop-hook tests cover force-push and trigger handling paths in the broader suite.
- skip_candidate: `no`

### TODO2TASK_CAREFUL_MODE-HZ-108 `file` `prompt-template/claude/finalize-phase-skipped-prompt.md`
- cursor: `[_]`
- core_role: Finalize-phase prompt for the RLCR/loop path when automated code review was skipped. It defines a degraded-validation transition into finalization with extra manual verification obligations.
- algorithmic_behavior: Warns with `{{REVIEW_SKIP_REASON}}`, tells the agent that implementation could not be fully validated, asks for manual review/tests/quality checks, optionally invokes `code-simplifier:code-simplifier`, enforces functionality-equivalent changes only, references plan/tracker files, and requires a final summary at `{{FINALIZE_SUMMARY_FILE}}` (`prompt-template/claude/finalize-phase-skipped-prompt.md:1-50`).
- inputs_outputs_state: Inputs are `REVIEW_SKIP_REASON`, `BASE_BRANCH`, `START_BRANCH`, `PLAN_FILE`, `GOAL_TRACKER_FILE`, and `FINALIZE_SUMMARY_FILE`. Output is the markdown prompt handed to Claude during finalization. State transition is performed by `enter_finalize_phase`: it renames `state.md` to `finalize-state.md`, computes `finalize-summary.md`, and renders this skipped-review template when `skip_reason` is non-empty (`hooks/loop-codex-stop-hook.sh:1041-1086`).
- gates_or_invariants: Non-negotiable invariants are no functionality change, no failing existing tests, no new bugs, and only functionality-equivalent cleanup (`prompt-template/claude/finalize-phase-skipped-prompt.md:26-34`). The before-exit gate requires all tasks marked completed, a commit, and a finalize summary (`prompt-template/claude/finalize-phase-skipped-prompt.md:40-50`).
- dependencies_and_callers: Called by `hooks/loop-codex-stop-hook.sh` through `load_and_render_safe "$TEMPLATE_DIR" "claude/finalize-phase-skipped-prompt.md"` with the listed variables (`hooks/loop-codex-stop-hook.sh:1080-1086`). It depends on loop state variables such as `PLAN_FILE`, `GOAL_TRACKER_FILE`, `BASE_BRANCH`, and `START_BRANCH`.
- edge_cases_or_failure_modes: Review-skip mode is explicitly lower confidence: the prompt compensates by requiring manual verification. If the template cannot render, an inline fallback with the same core constraints is present in the caller (`hooks/loop-codex-stop-hook.sh:1053-1078`). If tests are unavailable, the summary must still state verification limits.
- validation_or_tests: Finalize behavior is covered by `tests/test-finalize-phase.sh` and template reference/comprehensive tests. The caller’s fallback reduces failure impact if the external template is missing.
- skip_candidate: `no`

### TODO2TASK_CAREFUL_MODE-HZ-138 `file` `tests/robustness/test-pr-loop-api-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable specification for PR-loop API/state behavior under GitHub CLI failures, bot comment variants, JSON edge cases, stop-hook resilience, and polling contracts.
- algorithmic_behavior: Builds temporary repos and mocked `gh` binaries with behavior modes including empty arrays, rate limits, network errors, auth failure, Claude approval, Codex issues, mixed bots, Unicode comments, and long comments (`tests/robustness/test-pr-loop-api-robustness.sh:32-239`). It then runs nineteen tests across active-state detection, `fetch-pr-comments.sh`, bot response formatting, JSON edge cases, stop-hook handling, and `poll-pr-reviews.sh` (`tests/robustness/test-pr-loop-api-robustness.sh:278-849`).
- inputs_outputs_state: Inputs are temporary `.humanize/pr-loop/.../state.md` files, generated Git repos, mocked `gh` outputs, PR number `123`, timestamps, and bot filters. Outputs are pass/fail counters via `tests/test-helpers.sh`, generated comment markdown files, hook decisions, and polling JSON. State is created under `TEST_DIR`, including PR loop state (`tests/robustness/test-pr-loop-api-robustness.sh:241-276`).
- gates_or_invariants: `find_active_pr_loop` must detect newest active loops by `state.md`, even when optional fields like `pr_number` are absent (`tests/robustness/test-pr-loop-api-robustness.sh:285-345`; implementation at `hooks/lib/loop-common.sh:801-820`). `fetch-pr-comments.sh` must create structured output for empty comments and tolerate API failures with warnings or nonzero status. `poll-pr-reviews.sh` has a stricter API-failure invariant: exit 0, output valid JSON, and set boolean `has_new_comments:false` (`tests/robustness/test-pr-loop-api-robustness.sh:811-840`).
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` and `tests/test-helpers.sh` (`tests/robustness/test-pr-loop-api-robustness.sh:16-21`). Exercises `scripts/fetch-pr-comments.sh`, `hooks/pr-loop-stop-hook.sh`, and `scripts/poll-pr-reviews.sh`. Those scripts depend on `gh`, `jq`, git, temp files, and repository/PR resolution logic.
- edge_cases_or_failure_modes: Covers missing `pr_number`, YAML-list `active_bots`, empty comment arrays, rate limiting, connection refusal, corrupted state files, writable approve-state paths, Unicode bodies, very long bodies, slow API responses, and total API failure. It also checks bot identity mapping for `claude[bot]` and `chatgpt-codex-connector[bot]`, including severity markers such as `[P1]`.
- validation_or_tests: The file is included in the aggregate suite at `tests/run-all-tests.sh:55-73`. It uses helper summaries from `tests/test-helpers.sh:58-78`, so the suite exit status reflects accumulated failures. Its strongest validation is the jq parse/type check for polling JSON under API failure.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: TODO2TASK_CAREFUL_MODE-HZ-018, TODO2TASK_CAREFUL_MODE-HZ-048, TODO2TASK_CAREFUL_MODE-HZ-078, TODO2TASK_CAREFUL_MODE-HZ-108, TODO2TASK_CAREFUL_MODE-HZ-138
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`