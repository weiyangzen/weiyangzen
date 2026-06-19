# agent_065 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-065 `file` `tests/test-pr-loop-system.sh`
- cursor: `[_]`
- core_role:
  - `tests/test-pr-loop-system.sh` is an executable specification for the repository's PR loop behavior. It is not core runtime code itself, but it codifies the expected algorithmic behavior for PR loop setup, PR reviewer state classification, reaction detection, monitor phase detection, goal-tracker parsing/update/repair, setup failure cleanup, and stop-hook tracker updates.
  - The file defines a custom Bash test harness with isolated temp workdirs and a mocked GitHub CLI path. Harness setup is at `tests/test-pr-loop-system.sh:13-104`: strict shell mode, project/test/mock/fixture path discovery, pass/fail counters, temp git repo initialization, cleanup, and `run_test` isolation.
  - Its `main` dispatcher at `tests/test-pr-loop-system.sh:1754-1897` groups tests by optional filter names such as `reviewer_status`, `reactions`, `phase`, `goal_tracker_schema`, `case_4_5`, and `goal_tracker_integration`, then exits nonzero on any failure.

- algorithmic_behavior:
  - Mutual exclusion specification: active `.humanize/rlcr/<timestamp>/state.md` must block `scripts/setup-pr-loop.sh --codex`, and active `.humanize/pr-loop/<timestamp>/state.md` must block `scripts/setup-rlcr-loop.sh` (`tests/test-pr-loop-system.sh:110-146`). The expected outputs include human-readable conflict errors.
  - Reviewer startup-case classifier specification: the tests rewrite `tests/fixtures/issue-comments.json`, `review-comments.json`, and `pr-reviews.json` to model no comments, partial comments, all comments, PR review submissions, and stale reviews after new commits (`tests/test-pr-loop-system.sh:152-193`, `236-250`, `493-507`, `661-675`, `1315-1378`). The implementation under test is `scripts/check-pr-reviewer-status.sh`, whose public contract returns JSON fields `case`, `reviewers_commented`, `reviewers_missing`, `latest_commit_sha`, `latest_commit_at`, `newest_review_at`, and `has_commits_after_reviews` (`scripts/check-pr-reviewer-status.sh:11-20`).
  - Startup-case semantics are validated as:
    - Case 1: no reviewer comments (`tests/test-pr-loop-system.sh:152-170`).
    - Case 2: some configured bots commented, missing bots reported (`tests/test-pr-loop-system.sh:173-192`).
    - Case 3: all configured bots commented and reviews are fresh (`tests/test-pr-loop-system.sh:493-507`).
    - Case 4: all reviewers commented, but at least one review is stale relative to latest commit (`tests/test-pr-loop-system.sh:1315-1341`).
    - Case 5: partial reviewers commented and at least one existing review is stale (`tests/test-pr-loop-system.sh:1347-1378`).
  - The classifier’s related runtime algorithm maps `codex` to `chatgpt-codex-connector[bot]`, other names to `<bot>[bot]`, combines issue comments, review comments, and PR reviews, records commented/missing/stale bots, and chooses cases by commented/missing/stale counts (`scripts/check-pr-reviewer-status.sh:91-100`, `150-166`, `176-242`).
  - Reaction detection specification: Codex `+1` reaction on a PR is approval, respects an `--after` timestamp filter, and Claude `eyes` reaction confirms receipt of a trigger comment (`tests/test-pr-loop-system.sh:199-229`). The tested command is `scripts/check-bot-reactions.sh`, whose documented exit codes distinguish found, not found, and error (`scripts/check-bot-reactions.sh:9-17`). The Codex path fetches PR issue reactions and filters `chatgpt-codex-connector[bot]` with `content == "+1"` (`scripts/check-bot-reactions.sh:149-184`).
  - Monitor phase detection specification: file-state precedence is final states first, then Codex activity, then active session waiting states. Tests cover `approve-state.md` -> `approved`, `cancel-state.md` -> `cancelled`, `maxiter-state.md` -> `maxiter`, round 0 case 1 -> `waiting_initial_review`, other active states -> `waiting_reviewer`, and recent/growing `round-*-pr-check.md` -> `codex_analyzing` (`tests/test-pr-loop-system.sh:256-309`, `459-487`, `616-636`, `849-899`). The implementation’s documented phase set and growth/mtime cache strategy are at `scripts/lib/monitor-common.sh:258-342`.
  - Monitor display specification: `humanize monitor pr --once` must surface readable `Phase:` text for approved, waiting, cancelled, and Codex-analyzing states. The test wraps `scripts/humanize.sh`, stubs `tput` and `clear`, disables color, and checks output text (`tests/test-pr-loop-system.sh:905-1106`). Display mappings in the shared monitor library include "All reviews approved", "Loop cancelled", "Codex analyzing reviews...", and waiting text (`scripts/lib/monitor-common.sh:344-381`).
  - Goal tracker parsing specification: `parse_goal_tracker` must count acceptance criteria, completed ACs, active tasks, completed/deferred/open rows, and extract goal summary from older/general tracker schema (`tests/test-pr-loop-system.sh:315-371`). `humanize_parse_pr_goal_tracker` must parse total/resolved/remaining issues and last reviewer from PR tracker schema (`tests/test-pr-loop-system.sh:377-417`). The implementation contracts are visible at `scripts/lib/monitor-common.sh:387-498`.
  - Goal tracker update specification: `update_pr_goal_tracker` must add new round rows, update totals, be idempotent for duplicate round+reviewer updates, insert rows inside the Issue Summary table, and repair partial updates where either the summary row or issue log entry exists but not both (`tests/test-pr-loop-system.sh:513-538`, `681-764`, `1180-1309`). The implementation checks both round and reviewer, tracks summary/log partial state, updates totals only when adding a summary row, and uses `awk` to insert inside the table (`hooks/lib/loop-common.sh:1168-1295`).
  - Git/history safety specifications: unpushed commit detection is represented by ahead-count patterning and log presence; force-push detection is represented by `git merge-base --is-ancestor` ancestry checks (`tests/test-pr-loop-system.sh:544-610`).
  - Setup failure specification for stale-review startup cases: when startup Case 4/5 needs a trigger comment and `--claude` requires eyes verification, failure to retrieve `trigger_comment_id` must fail setup, emit "Could not find trigger comment ID", and clean the loop directory (`tests/test-pr-loop-system.sh:1384-1447`). The related setup code creates the loop dir, posts trigger comments for Case 4/5, fetches comment ID/timestamp, refuses local-clock fallback, and removes `$LOOP_DIR` on missing ID or missing eyes reaction (`scripts/setup-pr-loop.sh:394-400`, `443-521`).
  - Setup integration specification: `scripts/setup-pr-loop.sh --codex` must create a `.humanize/pr-loop/<timestamp>/goal-tracker.md` containing an Issue Summary and the mocked PR number (`tests/test-pr-loop-system.sh:1453-1539`). Setup writes state fields including round, configured/active bots, codex model settings, startup case, latest commit, trigger timestamp, and trigger comment ID (`scripts/setup-pr-loop.sh:535-555`), then renders `prompt-template/pr-loop/goal-tracker-initial.md` or fallback content (`scripts/setup-pr-loop.sh:561-635`).
  - Stop-hook integration specification: after a mocked bot review analysis returns `ISSUES_REMAINING`, `hooks/pr-loop-stop-hook.sh` must update the loop `goal-tracker.md` with a Round 1 row mentioning codex (`tests/test-pr-loop-system.sh:1541-1748`). The test builds local mock `gh`, `git`, and `codex` executables and runs the hook with `CLAUDE_PROJECT_DIR` pointed at the synthetic project (`tests/test-pr-loop-system.sh:1595-1719`). The hook’s relevant goal-tracker calls are visible at `hooks/pr-loop-stop-hook.sh:1240-1248`, `1513-1518`.

- inputs_outputs_state:
  - Inputs:
    - Optional CLI filter passed to `main` as the first argument; blank means run all groups (`tests/test-pr-loop-system.sh:1754-1880`).
    - Environment: `TEST_VERBOSE` is defined but not materially used in this file (`tests/test-pr-loop-system.sh:10-22`); test setup exports `PATH` with `tests/mocks`, `MOCK_GH_FIXTURES_DIR`, `TEST_TEMP_DIR`, and `CLAUDE_PROJECT_DIR` (`tests/test-pr-loop-system.sh:50-59`).
    - Fixture JSON files under `tests/fixtures`, especially `issue-comments.json`, `review-comments.json`, `pr-reviews.json`, and `reactions.json` (`tests/test-pr-loop-system.sh:152-156`, `173-177`, `1457-1461`).
    - Mock control environment variables such as `MOCK_GH_PR_NUMBER`, `MOCK_GH_PR_STATE`, `MOCK_GH_LATEST_COMMIT_AT`, `MOCK_GH_HEAD_SHA`, and `MOCK_GH_COMMENT_ID_LOOKUP_FAIL` (`tests/test-pr-loop-system.sh:119-120`, `1323-1325`, `1395-1400`, `1463-1467`).
    - Synthetic loop state files under `.humanize/pr-loop` and `.humanize/rlcr`, with YAML-ish frontmatter fields such as `current_round`, `startup_case`, `active_bots`, `trigger_comment_id`, `latest_commit_at` (`tests/test-pr-loop-system.sh:110-145`, `271-303`, `1553-1576`).
  - Outputs:
    - Console test progress and colored result summary via `log_test`, `log_pass`, `log_fail`, and final counts (`tests/test-pr-loop-system.sh:35-48`, `1882-1894`).
    - Exit status `1` when any test group fails (`tests/test-pr-loop-system.sh:1891-1894`).
    - For invoked scripts under test, expected JSON output is validated with `jq`, expected monitor output is validated with `grep`, and expected files/directories are checked with `test -f`, `ls`, and `grep`.
  - State transitions:
    - Each `run_test` creates a fresh temp git repo and removes it afterward (`tests/test-pr-loop-system.sh:50-104`).
    - Individual tests mutate fixtures in place and often restore default fixture contents before returning, for example reviewer status tests and Case 5 tests (`tests/test-pr-loop-system.sh:165-170`, `187-192`, `1371-1378`).
    - PR loop state transitions are modeled by presence/absence of `state.md`, `approve-state.md`, `cancel-state.md`, and `maxiter-state.md` (`tests/test-pr-loop-system.sh:423-487`, `616-636`, `947-1106`).
    - Codex-analysis state is modeled by creation, mtime manipulation, and cached size file `/tmp/humanize-phase-<session>-<round>.size` (`tests/test-pr-loop-system.sh:864-898`).
    - Setup failure transition explicitly expects a transient loop dir to be removed after missing trigger comment ID (`tests/test-pr-loop-system.sh:1431-1439`).
    - Goal tracker update transitions change markdown totals, Issue Summary rows, and Issue Log entries while avoiding duplicate rows for the same round/reviewer (`tests/test-pr-loop-system.sh:681-764`, `1180-1309`).

- gates_or_invariants:
  - Test harness invariant: every test runs inside a fresh temporary repository, in a subshell, then cleans `TEST_TEMP_DIR` (`tests/test-pr-loop-system.sh:50-104`).
  - Mutual exclusion invariant: PR loop and RLCR loop must not both be active (`tests/test-pr-loop-system.sh:110-146`).
  - Reviewer-status invariant: all three GitHub feedback sources must be cleared/combined to determine comment state: issue comments, inline review comments, and PR review submissions (`tests/test-pr-loop-system.sh:152-156`, `173-177`, `236-240`; implementation combination at `scripts/check-pr-reviewer-status.sh:150-166`).
  - Startup trigger invariant: round 0 cases 1/2/3 do not require a trigger, but cases 4/5 and all later rounds do (`tests/test-pr-loop-system.sh:1112-1174`).
  - Stale review invariant: new commits after a bot’s own latest review force Case 4 or 5 and set `has_commits_after_reviews=true` (`tests/test-pr-loop-system.sh:1315-1370`; implementation stale-count branch at `scripts/check-pr-reviewer-status.sh:217-242`).
  - Reaction timestamp invariant: a Codex `+1` older than `--after` must not count (`tests/test-pr-loop-system.sh:207-217`; implementation at `scripts/check-bot-reactions.sh:172-180`).
  - Phase detection precedence invariant: final state marker files override active/waiting logic, while recent/growing Codex check files override waiting states (`tests/test-pr-loop-system.sh:256-309`, `459-487`, `849-899`; implementation at `scripts/lib/monitor-common.sh:272-338`).
  - Goal tracker idempotency invariant: if both Issue Summary and Issue Log already have the same round+reviewer, update must skip; if only one exists, update must repair the missing side (`tests/test-pr-loop-system.sh:722-764`, `1242-1309`; implementation at `hooks/lib/loop-common.sh:1184-1218`).
  - Goal tracker table invariant: new summary rows must be inserted inside the Issue Summary table, before `## Total Statistics` (`tests/test-pr-loop-system.sh:1180-1236`).
  - Case 4/5 setup invariant: for Claude, trigger comment ID is mandatory because eyes verification depends on it; missing ID is a hard failure with cleanup (`tests/test-pr-loop-system.sh:1384-1447`; implementation at `scripts/setup-pr-loop.sh:484-503`).
  - Stop-hook tracker invariant: review analysis that leaves issues must still create a tracker row for the next round and preserve bot attribution (`tests/test-pr-loop-system.sh:1685-1748`).

- dependencies_and_callers:
  - Direct runtime dependencies from the test file:
    - `scripts/setup-pr-loop.sh` for PR loop startup, state file creation, trigger comment behavior, and goal tracker creation (`tests/test-pr-loop-system.sh:122-123`, `1402-1404`, `1471-1474`).
    - `scripts/setup-rlcr-loop.sh` for mutual-exclusion coverage from the other loop direction (`tests/test-pr-loop-system.sh:141-145`).
    - `scripts/check-pr-reviewer-status.sh` for cases 1-5 and PR review submission inclusion (`tests/test-pr-loop-system.sh:158-185`, `242-249`, `499-505`, `670-674`, `1326-1337`, `1358-1369`).
    - `scripts/check-bot-reactions.sh` for Codex thumbs-up and Claude eyes (`tests/test-pr-loop-system.sh:199-229`).
    - `scripts/lib/monitor-common.sh` for `get_pr_loop_phase`, `parse_goal_tracker`, `humanize_parse_pr_goal_tracker`, `monitor_find_latest_session`, `monitor_find_state_file`, and `monitor_get_file_size` (`tests/test-pr-loop-system.sh:256-371`, `377-417`, `770-899`).
    - `hooks/lib/loop-common.sh` for `update_pr_goal_tracker` (`tests/test-pr-loop-system.sh:513-538`, `681-764`, `1180-1309`).
    - `scripts/humanize.sh` for monitor command integration (`tests/test-pr-loop-system.sh:905-944`).
    - `hooks/pr-loop-stop-hook.sh` for stop-hook update behavior (`tests/test-pr-loop-system.sh:1710-1717`).
    - `prompt-template/pr-loop/goal-tracker-initial.md` for required schema sections (`tests/test-pr-loop-system.sh:642-655`).
  - Test infrastructure dependencies:
    - `tests/mocks/gh` is inserted at the front of `PATH` for most tests (`tests/test-pr-loop-system.sh:50-54`).
    - JSON fixtures under `tests/fixtures` provide mocked GitHub API data. The file frequently overwrites these fixtures and restores them to baseline.
    - External command dependencies include `bash`, `git`, `jq`, `grep`, `sed`, `awk`, `stat`, `find`, `timeout`, `date`, `mktemp`, and `chmod`.
  - Callers:
    - The file is self-executing via `main "$@"` (`tests/test-pr-loop-system.sh:1897`).
    - It can be run as all tests or by named group filter. The header says `./tests/run-tests.sh [test-name]`, but this file’s actual dispatcher supports direct first-argument filters like `case_4_5`, `goal_tracker_integration`, and `monitor_output` (`tests/test-pr-loop-system.sh:7-11`, `1754-1880`).
    - It appears alongside broader test runners such as `tests/run-all-tests.sh` and related PR-loop test files, but no separate caller was required to understand the assigned file.

- edge_cases_or_failure_modes:
  - Fixture mutation can leak across tests if a test returns early before restoring fixture content. Several tests manually restore fixtures on both success and failure paths, but this is local discipline rather than a generic harness guarantee (`tests/test-pr-loop-system.sh:165-170`, `1413-1444`, `1485-1536`).
  - The file is not safe to run in a read-only branch export because it writes temp files, rewrites fixture files, creates/removes `.humanize/pr-loop`, and creates local wrapper/mock scripts (`tests/test-pr-loop-system.sh:50-70`, `152-156`, `1468-1530`, `1595-1708`). I therefore inspected rather than executed it.
  - `test_unpushed_commits_detected` computes `ahead_count` but does not assert on it; it only checks that the latest log entry exists (`tests/test-pr-loop-system.sh:566-571`). As an executable spec, that is weaker than the test name suggests.
  - `test_startup_case_4_5_detection` only checks that returned JSON has a `.case` field, not that it is specifically 4 or 5; stronger Case 4/5 assertions appear later in `test_case4_all_commented_new_commits` and `test_case5_partial_commented_new_commits` (`tests/test-pr-loop-system.sh:661-675`, `1315-1378`).
  - Timestamp comparisons in the underlying reviewer-status and reaction logic are lexicographic string comparisons, so they depend on normalized ISO-8601 UTC timestamps. The tests use `2026-01-18T...Z` consistently (`scripts/check-pr-reviewer-status.sh:191`, `scripts/check-bot-reactions.sh:176`).
  - Phase detection writes cache files in `/tmp`; the test cleans the specific cache file in the Codex analyzing test, but cache collisions are possible if sessions share names (`tests/test-pr-loop-system.sh:886-898`; implementation cache path at `scripts/lib/monitor-common.sh:297-307`).
  - GNU/BSD portability is partially accounted for with dual `date` and `stat` invocations (`tests/test-pr-loop-system.sh:880-885`, `1548-1551`; implementation stat fallback at `scripts/lib/monitor-common.sh:293-313`).
  - The monitor wrapper creates a temporary executable inside the test project and uses `timeout 10`; if monitor startup hangs or `timeout` is unavailable, the test behavior depends on the host shell utilities (`tests/test-pr-loop-system.sh:910-943`).
  - Case 4/5 setup failure test validates cleanup by checking for any `.humanize/pr-loop/*/state.md`; if setup created other files without `state.md`, that specific check would not catch them (`tests/test-pr-loop-system.sh:1431-1439`).
  - Stop-hook integration test mocks only selected `gh`, `git`, and `codex` subcommands. It validates the tracker side effect, not full hook behavior across all real GitHub/API branches (`tests/test-pr-loop-system.sh:1595-1717`).

- validation_or_tests:
  - This file is itself the validation harness. It includes 38 `run_test` invocations across the dispatcher (`tests/test-pr-loop-system.sh:1767-1880`) covering:
    - Mutual exclusion: 2 tests.
    - Reviewer status and PR review inclusion: cases 1, 2, 3, 4, 5 plus PR reviews.
    - Bot reactions: Codex `+1`, timestamp filtering, Claude `eyes`.
    - Phase and state-file detection: approved, waiting initial, waiting reviewer, cancelled, maxiter, Codex analyzing, state-file discovery.
    - Goal tracker parsing and update behavior: parser, schema, totals, table insertion, idempotency, partial repair.
    - Git ancestry/unpushed behavior: unpushed placeholder and merge-base ancestry.
    - Monitor output labels: approved, waiting, cancelled, Codex analyzing.
    - Setup and stop-hook integration: goal-tracker creation, missing trigger-comment failure cleanup, stop-hook round update.
  - Assertions are mostly `jq -e`, `grep`, file existence checks, explicit shell conditionals, and command exit-code checks. Failures return nonzero from each test function and are aggregated by `run_test`.
  - I did not execute this test file in the branch export because the instructions prohibit modification and the test script intentionally writes to fixtures and creates/removes test state under the working tree. Direct file inspection was used for this research item.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `TUNABLE_FULL_EXAMINE_ROUND-HZ-065`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`