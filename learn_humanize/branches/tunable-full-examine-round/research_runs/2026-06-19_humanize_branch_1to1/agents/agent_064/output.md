# agent_064 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-064 `file` `tests/test-pr-loop-stophook.sh`
- cursor: `[_]`
- core_role: This file is an executable shell specification for the PR-loop stop hook. It defines `run_stophook_tests()` and, inside that function, a suite of integration-style tests that synthesize `.humanize/pr-loop/<timestamp>/state.md`, resolution files, and mocked `gh`, `git`, and sometimes `codex` executables before invoking `hooks/pr-loop-stop-hook.sh` through `CLAUDE_PROJECT_DIR`. The file is directly sourced by the aggregate PR-loop test runner at `tests/test-pr-loop.sh:32-47`.

- algorithmic_behavior: The suite validates the stop hook’s exit-control algorithm for PR review loops. It models the hook as a state machine whose active state is `state.md` and whose terminal states are renamed state files such as `approve-state.md`, `merged-state.md`, `closed-state.md`, `maxiter-state.md`, and related stop outputs in the hook implementation. The tests cover:
  - stale trigger rejection after a newer commit timestamp: the fixture sets `latest_commit_at: 2026-01-18T14:00:00Z`, while mocked issue comments include an older `@claude` trigger at `2026-01-18T12:00:00Z`; the expected behavior is to block and require a new trigger (`tests/test-pr-loop-stophook.sh:25-47`, `tests/test-pr-loop-stophook.sh:57-83`, `tests/test-pr-loop-stophook.sh:125-134`).
  - startup case 1 exception: round 0 with `startup_case: 1` may proceed without a trigger if initial auto-review approval is detected, especially Codex `+1` (`tests/test-pr-loop-stophook.sh:140-167`, `tests/test-pr-loop-stophook.sh:176-191`, `tests/test-pr-loop-stophook.sh:228-239`).
  - empty `active_bots` completion: if no active bots remain, the hook should complete by creating or moving to `approve-state.md` (`tests/test-pr-loop-stophook.sh:246-321`).
  - dynamic startup-case recomputation: one older test is defined but not invoked (`test_stophook_dynamic_startup_case`, `tests/test-pr-loop-stophook.sh:327-450`); the invoked dynamic test uses current timestamps and expects `startup_case` to persist and change away from `1` when comments arrive (`tests/test-pr-loop-stophook.sh:1145-1393`, invoked at `tests/test-pr-loop-stophook.sh:1782`).
  - unpushed commit blocking: mocked `git status -sb` returns `ahead 2`; the stop hook should block before exit (`tests/test-pr-loop-stophook.sh:452-533`).
  - force-push/history rewrite detection: mocked `git rev-parse HEAD` returns a new SHA and `git merge-base --is-ancestor` exits 1, forcing a re-trigger block (`tests/test-pr-loop-stophook.sh:538-637`).
  - missing trigger blocking for trigger-required cases: `startup_case: 4` with no comments should block with trigger guidance (`tests/test-pr-loop-stophook.sh:642-749`).
  - per-bot timeout auto-removal: with short `poll_timeout: 2` and no bot comments, the hook should time out, remove the bot from `active_bots`, and complete if no active bots remain (`tests/test-pr-loop-stophook.sh:754-891`).
  - Codex `+1` approval path: round 0, case 1, active `codex`, mocked `+1` reaction should remove Codex and approve if it was the only active bot (`tests/test-pr-loop-stophook.sh:896-1005`).
  - Claude eyes verification: when Claude is configured and trigger-required, absence of an eyes reaction on the trigger should block with an eyes/configuration timeout (`tests/test-pr-loop-stophook.sh:1011-1140`).
  - fork PR base-repo resolution: mocked current fork lookup fails, parent/upstream lookup succeeds, and the hook should not fail on PR lookup (`tests/test-pr-loop-stophook.sh:1395-1519`).
  - mixed bot approval and issue tracking: Claude approves while Codex reports issues; the loop must continue, Codex must remain active, Claude must be removed, and `approve-state.md` must not be created (`tests/test-pr-loop-stophook.sh:1524-1767`).

- inputs_outputs_state: Inputs are synthetic PR-loop state frontmatter files, resolution summaries, hook stdin `{}`, environment variables, and mocked command outputs.
  - Required test inputs include `CLAUDE_PROJECT_DIR`, inherited `PROJECT_ROOT`, inherited `TEST_DIR`, mocked `PATH`, state files under `.humanize/pr-loop/2026-01-18_12-00-00/state.md`, and `round-N-pr-resolve.md` files. The suite relies on `pass`/`fail` helpers from `tests/test-helpers.sh:30-44` and the aggregate setup from `tests/test-pr-loop.sh:18-27`.
  - State fields exercised across tests include `current_round`, `max_iterations`, `pr_number`, `start_branch`, `configured_bots`, `active_bots`, `codex_model`, `codex_effort`, `codex_timeout`, `poll_interval`, `poll_timeout`, `started_at`, `last_trigger_at`, `trigger_comment_id`, `startup_case`, `latest_commit_sha`, and `latest_commit_at`.
  - Outputs asserted by the tests are mostly hook stderr/stdout messages and filesystem state transitions: creation or movement to `approve-state.md`, mutation of `state.md`, persistence/change of `startup_case`, removal or retention of bot names under `active_bots`, existence/content of `round-N-pr-check.md`, and absence of premature approval for mixed results.
  - The implementation dependency being specified parses state at `hooks/pr-loop-stop-hook.sh:87-174`, resolves active PR-loop directories via `find_active_pr_loop` from `hooks/lib/loop-common.sh:798`, checks PR base repository before state polling at `hooks/pr-loop-stop-hook.sh:196-237`, validates PR open/closed/merged state at `hooks/pr-loop-stop-hook.sh:239-256`, and requires a round resolution file at `hooks/pr-loop-stop-hook.sh:258-277`.

- gates_or_invariants: The tests encode several invariants that the stop hook must preserve:
  - a resolution summary for the current round must exist before stop approval or polling (`hooks/pr-loop-stop-hook.sh:262-277`; tested by each fixture creating `round-N-pr-resolve.md`, for example `tests/test-pr-loop-stophook.sh:51-52`);
  - non-`.humanize` uncommitted changes and unpushed commits block exit before review completion (`hooks/pr-loop-stop-hook.sh:283-361`; unpushed case tested at `tests/test-pr-loop-stophook.sh:493-530`);
  - force-pushed or newly pushed commits invalidate stale `last_trigger_at` and `trigger_comment_id`, update commit metadata, and require a new `@bot` trigger (`hooks/pr-loop-stop-hook.sh:364-424`, `hooks/pr-loop-stop-hook.sh:598-629`);
  - trigger comments must come from the current GitHub user, mention configured bots, be paginated, and, when `latest_commit_at` exists, be newer than that commit timestamp (`hooks/pr-loop-stop-hook.sh:518-590`);
  - trigger requirement depends on `current_round`, `startup_case`, and whether new commits were detected: round 0 cases 1/2/3 do not require a trigger unless new commits are detected, while cases 4/5 and later rounds do (`hooks/pr-loop-stop-hook.sh:673-736`);
  - Claude eyes verification is ordered after trigger validation, not before, to avoid checking stale trigger IDs (`hooks/pr-loop-stop-hook.sh:738-789`);
  - polling must track all configured bots, not just currently active bots, so previously approved bots can be re-added if they post new issues (`hooks/pr-loop-stop-hook.sh:791-873`, `hooks/pr-loop-stop-hook.sh:1418-1481`);
  - per-bot timeout removes only timed-out bots and completes only when no active bots remain (`hooks/pr-loop-stop-hook.sh:1051-1166`);
  - Codex local validation controls loop continuation via final markers: `APPROVE`, `WAITING_FOR_BOTS`, `USAGE_LIMIT_HIT`, or issue-bearing output that updates `active_bots` and feedback files (`hooks/pr-loop-stop-hook.sh:1219-1400`);
  - mixed approval must not inflate resolved issue count and must not complete the loop unless all bots approve; the hook explicitly keeps `ISSUES_RESOLVED_COUNT=0` on non-final mixed results (`hooks/pr-loop-stop-hook.sh:1492-1519`; tested at `tests/test-pr-loop-stophook.sh:1715-1767`).

- dependencies_and_callers: The test file depends on the shell test harness and the PR-loop implementation surface:
  - Called by `tests/test-pr-loop.sh`, which sources `test-pr-loop-stophook.sh` and then invokes `run_stophook_tests` after script and hook tests (`tests/test-pr-loop.sh:32-47`).
  - Depends on `tests/test-helpers.sh` for `pass`, `fail`, counters, and temporary directory setup (`tests/test-helpers.sh:30-88`).
  - Invokes `hooks/pr-loop-stop-hook.sh` in every test through `echo '{}' | "$PROJECT_ROOT/hooks/pr-loop-stop-hook.sh"` or `timeout ... bash -c ...`.
  - The target hook depends on `hooks/lib/loop-common.sh` for bot mapping, YAML list rendering, mention string building, active loop discovery, and goal tracker updates; relevant helper definitions are indexed at `hooks/lib/loop-common.sh:726-767`, `hooks/lib/loop-common.sh:798`, and `hooks/lib/loop-common.sh:1168`.
  - The hook also calls `scripts/portable-timeout.sh`, `scripts/check-bot-reactions.sh`, `scripts/poll-pr-reviews.sh`, and `scripts/check-pr-reviewer-status.sh`, with call sites visible at `hooks/pr-loop-stop-hook.sh:58`, `hooks/pr-loop-stop-hook.sh:459`, `hooks/pr-loop-stop-hook.sh:766`, `hooks/pr-loop-stop-hook.sh:801`, `hooks/pr-loop-stop-hook.sh:985`, and `hooks/pr-loop-stop-hook.sh:1534`.
  - Tests mock `gh` extensively for GitHub API, PR state, PR commits, base repository, parent repository, comments, reviews, reactions, and current user responses. They mock `git` for HEAD SHA, git-dir, clean/dirty status, branch status, and merge-base ancestry. The mixed-approval test additionally mocks `codex exec` by placing a fake `codex` on `PATH` (`tests/test-pr-loop-stophook.sh:1682-1706`).

- edge_cases_or_failure_modes: The suite is focused on failure-prone stop-hook behavior:
  - stale trigger comments before a force push or newer commit must not be reused (`tests/test-pr-loop-stophook.sh:57-83`, `hooks/pr-loop-stop-hook.sh:564-576`);
  - no trigger is permitted only in startup cases where the workflow is allowed to process initial or existing reviews (`hooks/pr-loop-stop-hook.sh:677-708`);
  - fork PRs require using the base/parent repository for PR view and issue comment/reaction lookups, otherwise `gh pr view` can fail in the fork (`hooks/pr-loop-stop-hook.sh:196-237`, `tests/test-pr-loop-stophook.sh:1429-1479`);
  - GitHub API pagination and `--jq` behavior are simulated because `gh api --paginate --jq` returns transformed objects per page before aggregation (`tests/test-pr-loop-stophook.sh:57-83`, `hooks/pr-loop-stop-hook.sh:535-543`);
  - macOS compatibility is reflected in date fallbacks using `date -u -d ... || date -u -v...` in dynamic timestamp tests (`tests/test-pr-loop-stophook.sh:1152-1158`, `tests/test-pr-loop-stophook.sh:1531-1539`), matching the hook’s own portable date parsing fallback (`hooks/pr-loop-stop-hook.sh:867`);
  - bot timeouts are anchored to trigger time, but for startup cases 2/3 historical-comment processing uses the current time to avoid immediate timeout (`hooks/pr-loop-stop-hook.sh:858-868`);
  - `test_stophook_dynamic_startup_case` is defined at `tests/test-pr-loop-stophook.sh:327-450` but is not invoked in the final call list; the invoked dynamic coverage is `test_stophook_dynamic_startup_case_update` at `tests/test-pr-loop-stophook.sh:1782`;
  - many tests treat output-message matching as an alternate pass path if a state file is missing, which makes them robust to implementation details but less strict for some state transitions; stronger assertions are present for timeout and mixed-approval state mutation (`tests/test-pr-loop-stophook.sh:863-890`, `tests/test-pr-loop-stophook.sh:1750-1767`);
  - the tests intentionally use `|| true` around hook invocations because the hook returns JSON block/allow decisions while the shell test wants to inspect output regardless of exit status.

- validation_or_tests: This assigned file is itself validation coverage. It contains 13 test function definitions, but the runner at the bottom invokes 12 of them: `test_stophook_force_push_rejects_old_trigger`, `test_stophook_case1_no_trigger_required`, `test_stophook_approve_creates_state`, `test_stophook_step6_unpushed_commits`, `test_stophook_step65_force_push_detection`, `test_stophook_step7_missing_trigger`, `test_stophook_bot_timeout_auto_remove`, `test_stophook_codex_thumbsup_approval`, `test_stophook_claude_eyes_timeout`, `test_stophook_dynamic_startup_case_update`, `test_stophook_fork_pr_base_repo_resolution`, and `test_stophook_goal_tracker_mixed_approval` (`tests/test-pr-loop-stophook.sh:1772-1784`). I did not execute the suite because the assignment asked for research notes only and the branch export is read-only; inspection was direct source review. A `git status --short` probe also failed because this export is not a normal writable git checkout in the sandbox, so no repository-state validation was possible.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 unique assigned item section present above`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`