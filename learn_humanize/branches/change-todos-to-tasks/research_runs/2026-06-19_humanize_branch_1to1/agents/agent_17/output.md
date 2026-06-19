# agent_17 change-todos-to-tasks 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `0790d28514ab48bec2668f4ec069592872fed586`

## Item Evidence

### CHANGE_TODOS_TO_TASKS-HZ-017 `file` `agents/draft-relevance-checker.md`
- cursor: `[_]`
- core_role: Agent prompt for the `gen-plan` relevance gate. It decides whether a user draft belongs to the current repository before the command continues into deeper plan generation. The frontmatter defines `name: draft-relevance-checker`, `model: haiku`, and read-only discovery tools `Read, Glob, Grep` at `agents/draft-relevance-checker.md:1-5`.
- algorithmic_behavior: The agent is given draft content, quickly explores repository docs and structure, identifies technologies/purpose, compares draft concepts/files/features to the repo, then emits one of two exact verdict prefixes: `RELEVANT:` or `NOT_RELEVANT:` at `agents/draft-relevance-checker.md:14-29`.
- inputs_outputs_state: Inputs are the draft document content and repository files reachable through read/glob/grep. Output is a single verdict line with a brief explanation. No persistent state is mutated; this is a pure decision prompt.
- gates_or_invariants: The classifier is intentionally permissive: informal drafts, any language, semantic connection, and “if in doubt, lean toward relevant” are explicit invariants at `agents/draft-relevance-checker.md:31-37`. The only hard negative is content with no reasonable repository connection.
- dependencies_and_callers: `commands/gen-plan.md:50-72` runs this as Phase 2 after IO validation, asks it to inspect README/CLAUDE/main files, and stops the command on `NOT_RELEVANT`. `tests/test-gen-plan.sh:111-153` validates the file exists and has the expected name, model, and tools.
- edge_cases_or_failure_modes: False negatives are mitigated by the lenient policy, but the prompt relies on the model obeying exact prefix output; downstream text matching could fail if the agent adds extra formatting or ambiguous wording. Since tools are read-only, it cannot repair missing context.
- validation_or_tests: Structural coverage exists in `tests/test-gen-plan.sh`, including agent file presence, frontmatter name, `haiku` model, and tools specification. There is no direct behavioral fixture that feeds unrelated/relevant drafts and asserts the verdict.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-047 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role: Executable regression spec for the transition from direct `round-*-todos.md` file access to native task tooling, while preserving a small compatibility allowlist for early loop files. It exercises shared allowlist logic plus Read/Write/Edit/Bash validators.
- algorithmic_behavior: The test creates a temporary git repo and active RLCR loop state at `.humanize/rlcr/2024-01-01_12-00-00`, with `current_round: 5`, then calls `is_allowlisted_file` and each hook using JSON hook payloads at `tests/test-allowlist-validators.sh:29-64`.
- inputs_outputs_state: Inputs are synthetic hook JSON for `Read`, `Write`, `Edit`, and `Bash`, plus generated state files and command strings. Outputs are hook exit codes and stderr text. Test state is isolated in `mktemp -d` and removed by trap at `tests/test-allowlist-validators.sh:29-31`.
- gates_or_invariants: The explicit allowlist is exactly `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md`, implemented in `hooks/lib/loop-common.sh:423-441`. Anything outside the active loop dir, wrong basename, old loop dir, same basename under another root, or generic relative path must be blocked.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at `tests/test-allowlist-validators.sh:15-17`, then invokes `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-read-validator.sh`, and `hooks/loop-bash-validator.sh`. The validators use `find_active_loop`, `is_round_file_type`, `extract_round_number`, `parse_state_file_strict`, and `todos_blocked_message`.
- edge_cases_or_failure_modes: Covers wrong directory at `tests/test-allowlist-validators.sh:120-126`, non-allowlisted current-loop files at `tests/test-allowlist-validators.sh:104-118`, Bash full-path restrictions at `tests/test-allowlist-validators.sh:290-352`, old loop directory at `tests/test-allowlist-validators.sh:355-368`, and same active-loop basename under `/tmp` at `tests/test-allowlist-validators.sh:370-383`.
- validation_or_tests: Tests 1-7 assert `is_allowlisted_file`; tests 8-11 assert Write allow/block behavior; tests 12-14 assert Edit behavior; tests 15-18 assert Read behavior; tests 19-25 assert Bash path-restricted behavior. The script exits with `TESTS_FAILED`, so any regression fails CI-style execution at `tests/test-allowlist-validators.sh:385-393`.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-077 `file` `prompt-template/block/finalize-state-file-modification.md`
- cursor: `[_]`
- core_role: Block-message template used when a model attempts to modify `finalize-state.md`, which is system-owned during RLCR Finalize Phase.
- algorithmic_behavior: The template tells the agent it cannot modify `finalize-state.md`, then redirects the agent to the permitted finalize workflow: run code simplification, commit changes, and write `finalize-summary.md` at `prompt-template/block/finalize-state-file-modification.md:1-8`.
- inputs_outputs_state: Input is indirect: hook validators render this template when state-file protection fires. Output is human/model-facing block text. It does not mutate state; it protects the transition state file from user-agent writes.
- gates_or_invariants: `finalize-state.md` is loop-managed and not agent-managed. The invariant is enforced by helper `finalize_state_file_blocked_message` in `hooks/lib/loop-common.sh:472-478`, with path detection in `hooks/lib/loop-common.sh:515-518`.
- dependencies_and_callers: Used by Write/Edit/Bash validators. Write blocks it at `hooks/loop-write-validator.sh:148-155`; Edit blocks it at `hooks/loop-edit-validator.sh:112-120`; Bash blocks destination/source/shell-wrapper attempts at `hooks/loop-bash-validator.sh:139-145`, `hooks/loop-bash-validator.sh:286-293`, and `hooks/loop-bash-validator.sh:306-318`.
- edge_cases_or_failure_modes: The Bash validator checks `finalize-state.md` before generic `state.md` because substring matching could otherwise misclassify the file. Cancel flow is the intentional exception when `is_cancel_authorized` allows system rename to cancel state.
- validation_or_tests: `tests/test-finalize-phase.sh` covers blocked Write/Edit/Bash modification, `mv`/`cp` source protection, active-loop detection with `finalize-state.md`, and summary requirements. Related robustness tests cover session/state transition detection.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-107 `file` `prompt-template/claude/finalize-phase-prompt.md`
- cursor: `[_]`
- core_role: Claude-facing Finalize Phase prompt rendered after Codex review passes and implementation is complete. It defines the last algorithmic phase before loop completion.
- algorithmic_behavior: The prompt instructs Claude to invoke `code-simplifier:code-simplifier` through the Task tool, perform only functionality-equivalent cleanup, run tests, commit changes, complete TaskUpdate items, and write `{{FINALIZE_SUMMARY_FILE}}` at `prompt-template/claude/finalize-phase-prompt.md:7-51`.
- inputs_outputs_state: Inputs are template vars `{{BASE_BRANCH}}`, `{{START_BRANCH}}`, `{{PLAN_FILE}}`, `{{GOAL_TRACKER_FILE}}`, and `{{FINALIZE_SUMMARY_FILE}}`. Outputs are a commit, task-status updates, and `finalize-summary.md`; the loop system, not the agent, manages `finalize-state.md`.
- gates_or_invariants: Non-negotiable constraints prohibit functionality changes, test failures, new bugs, and non-equivalent refactors at `prompt-template/claude/finalize-phase-prompt.md:16-24`. Focus is restricted to recent changes, especially diff from base to start branch at `prompt-template/claude/finalize-phase-prompt.md:25-35`.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh` renders this template after code review succeeds, passing `FINALIZE_SUMMARY_FILE`, `PLAN_FILE`, `GOAL_TRACKER_FILE`, `BASE_BRANCH`, and `START_BRANCH` at `hooks/loop-codex-stop-hook.sh:1078-1103`. The same hook renames active `state.md` to `finalize-state.md` before blocking with the finalize prompt at `hooks/loop-codex-stop-hook.sh:1037-1043`.
- edge_cases_or_failure_modes: If code-simplifier is unavailable, the prompt still requires equivalent cleanup/testing/summary, but there is no local fallback text in this file. If tests are not run or summary is missing, the stop hook’s Finalize Phase checks block completion; `hooks/loop-codex-stop-hook.sh:610-628` expects `finalize-summary.md` in Finalize Phase.
- validation_or_tests: `tests/test-finalize-phase.sh` exercises entry into Finalize Phase on COMPLETE, prompt content mentioning code-simplifier, parsing of `finalize-state.md`, blocked state modification, finalize-summary allowance, and completion by renaming to `complete-state.md`.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-137 `file` `tests/robustness/test-pr-loop-api-robustness.sh`
- cursor: `[_]`
- core_role: Robustness spec for PR-loop API handling, state detection, comment fetching, bot-response parsing, stop-hook tolerance, and polling failure contracts. It tests actual scripts with mocked `gh`.
- algorithmic_behavior: `create_mock_gh` generates behavior-specific GitHub CLI shims for empty arrays, rate limits, network errors, auth failures, Claude approval comments, Codex issue comments, mixed bots, unicode comments, and long comments at `tests/robustness/test-pr-loop-api-robustness.sh:32-239`. The script then drives state helpers, `fetch-pr-comments.sh`, `pr-loop-stop-hook.sh`, and `poll-pr-reviews.sh`.
- inputs_outputs_state: Inputs are temporary git repos, `.humanize/pr-loop/<timestamp>/state.md`, mocked `gh` commands, PR number `123`, bot lists, and timestamps. Outputs are markdown comment files, hook block/pass exit codes, JSON from polling, and pass/fail counters from `tests/test-helpers.sh`.
- gates_or_invariants: `find_active_pr_loop` must detect newest PR loop dirs with `state.md`, even with missing `pr_number`, as asserted at `tests/robustness/test-pr-loop-api-robustness.sh:285-345` and implemented in `hooks/lib/loop-common.sh:795-814`. `poll-pr-reviews.sh` must reject missing args, output valid JSON on success, and on API failure exit 0 with boolean `has_new_comments:false` at `tests/robustness/test-pr-loop-api-robustness.sh:811-843`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` and `tests/test-helpers.sh` at `tests/robustness/test-pr-loop-api-robustness.sh:16-21`. Calls `scripts/fetch-pr-comments.sh`, whose retry wrapper writes empty arrays and records API failures at `scripts/fetch-pr-comments.sh:176-220`; calls `scripts/poll-pr-reviews.sh`, whose retry wrapper returns `[]` on failure at `scripts/poll-pr-reviews.sh:200-235`; calls `hooks/pr-loop-stop-hook.sh`, which parses YAML-list `active_bots` and `configured_bots` at `hooks/pr-loop-stop-hook.sh:87-170`.
- edge_cases_or_failure_modes: Covers rate-limit stderr and nonzero `gh api`, network refusal, empty API arrays, Unicode JSON payloads, 10KB comment bodies, corrupted PR-loop state that should not crash with signal-like exit, missing active loop, slow API response, and mocked API failure. It does not assert auth-failure behavior directly despite providing an `auth_failure` mock branch.
- validation_or_tests: Tests 1-3 cover state detection; 4-6 cover fetch empty/rate-limit/network behavior; 7-9 cover Claude/Codex/mixed bot formatting; 10-11 cover JSON edge cases; 12-14 cover stop-hook no-loop/corrupted-state/approve path; 15-19 cover poll help, arg validation, JSON shape, slow API, and strict API failure JSON. Summary exits through `print_test_summary` at `tests/robustness/test-pr-loop-api-robustness.sh:845-850`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: CHANGE_TODOS_TO_TASKS-HZ-017, CHANGE_TODOS_TO_TASKS-HZ-047, CHANGE_TODOS_TO_TASKS-HZ-077, CHANGE_TODOS_TO_TASKS-HZ-107, CHANGE_TODOS_TO_TASKS-HZ-137
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`