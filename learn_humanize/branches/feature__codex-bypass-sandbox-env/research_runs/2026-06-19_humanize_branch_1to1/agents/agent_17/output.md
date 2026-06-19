# agent_17 feature/codex-bypass-sandbox-env 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `f0f1ad947157c3d1e9d0bdd58bf36aae92075cc6`

## Item Evidence

### FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-017 `file` `agents/draft-relevance-checker.md`
- cursor: `[_]`
- core_role: Specialized subagent prompt for deciding whether a user draft is semantically relevant to the current repository before `gen-plan` proceeds; metadata defines `name`, `description`, `model: haiku`, and read-only discovery tools `Read, Glob, Grep` at `agents/draft-relevance-checker.md:1`.
- algorithmic_behavior: The agent first explores repository docs/structure/technology, then compares draft content against repo concepts, components, use, learning goals, paths, functions, and features; it returns one of two machine-readable verdict prefixes, `RELEVANT:` or `NOT_RELEVANT:` at `agents/draft-relevance-checker.md:14`.
- inputs_outputs_state: Input is invoked draft content plus current repo files available through read/search tools; output is a single verdict line with brief explanation; no persistent state is written by this prompt.
- gates_or_invariants: Bias is intentionally permissive: informal, multilingual, rough, or ambiguous drafts should be accepted when reasonably connected, and doubt resolves to relevant at `agents/draft-relevance-checker.md:31`.
- dependencies_and_callers: Depends on repository documentation and file topology, especially `README.md`, `CLAUDE.md`, and other docs listed at `agents/draft-relevance-checker.md:16`; likely called by the `gen-plan` command path per description.
- edge_cases_or_failure_modes: False positives are preferred over false negatives by policy; weak semantic relation, rough wording, or non-English content should not block. A risk remains that missing repository docs could force reliance on directory structure.
- validation_or_tests: No direct executable test in the assigned file; validation is by prompt contract: exact verdict prefixes and lenient relevance criteria.
- skip_candidate: `yes: prompt/policy asset, not executable algorithm code, but it defines a planning gate contract and should remain in coverage`

### FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-047 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role: Executable specification for the RLCR validator exception path that allows a small fixed set of historical/current todo and summary files while preserving normal protections against direct todo manipulation.
- algorithmic_behavior: Creates a temp git repo and active loop state with `current_round: 5`, then validates `is_allowlisted_file()` and the Read/Write/Edit/Bash hooks against expected allow/block exits at `tests/test-allowlist-validators.sh:29`, `tests/test-allowlist-validators.sh:53`, and `tests/test-allowlist-validators.sh:66`.
- inputs_outputs_state: Inputs are synthetic Claude hook JSON payloads for `Read`, `Write`, `Edit`, and `Bash`; outputs are hook exit codes and stderr substrings. The test tracks `TESTS_PASSED` and `TESTS_FAILED`, then exits with the failure count at `tests/test-allowlist-validators.sh:23` and `tests/test-allowlist-validators.sh:385`.
- gates_or_invariants: Only exact active-loop paths for `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` are allowlisted; `round-3-todos.md`, `round-2-summary.md`, wrong directories, old loop dirs, basename-only paths, and same-basename different-root paths must be blocked at `tests/test-allowlist-validators.sh:72`, `tests/test-allowlist-validators.sh:104`, `tests/test-allowlist-validators.sh:120`, and `tests/test-allowlist-validators.sh:370`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at `tests/test-allowlist-validators.sh:17`. The implemented allowlist is the fixed array in `hooks/lib/loop-common.sh:423`. Hook dependencies include `hooks/loop-write-validator.sh:55`, `hooks/loop-read-validator.sh:55`, `hooks/loop-edit-validator.sh:38`, and Bash command modification checks in `hooks/loop-bash-validator.sh:375`.
- edge_cases_or_failure_modes: The security-critical case is path spoofing: an allowed basename is insufficient unless it equals `$ACTIVE_LOOP_DIR/$allowed`. Bash checks also reject writing allowed basenames through relative paths or another root, tested at `tests/test-allowlist-validators.sh:342` and `tests/test-allowlist-validators.sh:370`.
- validation_or_tests: Contains 25 focused assertions: 7 direct allowlist checks, 4 write-hook cases, 3 edit-hook cases, 4 read-hook cases, and 7 Bash path-restriction cases. Success requires zero failures and `exit $TESTS_FAILED`.
- skip_candidate: `no`

### FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-077 `file` `prompt-template/block/finalize-state-file-modification.md`
- cursor: `[_]`
- core_role: Block-message template for attempts to modify `finalize-state.md`, the system-managed state file during Finalize Phase.
- algorithmic_behavior: Tells the agent that `finalize-state.md` cannot be modified and redirects work toward the allowed finalize actions: run code simplification, commit changes, and write `finalize-summary.md` at `prompt-template/block/finalize-state-file-modification.md:1`.
- inputs_outputs_state: Input is a hook/template-render request from a validator; output is markdown shown as the blocking reason. It does not mutate state.
- gates_or_invariants: The invariant is ownership separation: loop system owns `finalize-state.md`; agent writes only `finalize-summary.md` during Finalize Phase at `prompt-template/block/finalize-state-file-modification.md:3`.
- dependencies_and_callers: Loaded through `finalize_state_file_blocked_message()` in `hooks/lib/loop-common.sh:472`. It is used by write/edit/Bash protections when `finalize-state.md` is targeted, for example `hooks/loop-write-validator.sh:152`, `hooks/loop-edit-validator.sh:117`, and `hooks/loop-bash-validator.sh:139`.
- edge_cases_or_failure_modes: The related implementation must check `finalize-state.md` before generic `state.md` because `state.md` suffix matching can also catch `finalize-state.md`; this ordering is documented in validators at `hooks/loop-write-validator.sh:150` and `hooks/loop-bash-validator.sh:132`.
- validation_or_tests: Covered by finalize-phase tests that expect write/edit/Bash blocks for `finalize-state.md`, plus Bash source-protection for `mv`/`cp` from that file in `tests/test-finalize-phase.sh` references found around tests `T-NEG-5` through `T-NEG-5e`.
- skip_candidate: `yes: template-only asset, but it is part of the validator gate surface and user-facing failure contract`

### FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-107 `file` `prompt-template/claude/finalize-phase-prompt.md`
- cursor: `[_]`
- core_role: Finalize Phase prompt template that transitions the agent from accepted implementation into functionality-preserving simplification and final reporting.
- algorithmic_behavior: Declares that Codex review passed, instructs Claude to invoke `code-simplifier:code-simplifier` via Task, constrain changes to behavior-preserving cleanup, complete todos, commit, and write `{{FINALIZE_SUMMARY_FILE}}` at `prompt-template/claude/finalize-phase-prompt.md:1`, `prompt-template/claude/finalize-phase-prompt.md:7`, and `prompt-template/claude/finalize-phase-prompt.md:41`.
- inputs_outputs_state: Inputs are template variables `{{BASE_BRANCH}}`, `{{START_BRANCH}}`, `{{PLAN_FILE}}`, `{{GOAL_TRACKER_FILE}}`, and `{{FINALIZE_SUMMARY_FILE}}`; outputs are agent actions: simplifier review, optional refactor commit, TodoWrite completion, and finalize summary.
- gates_or_invariants: Non-negotiable constraints require no functionality changes, no test failures, no introduced bugs, and only functionality-equivalent cleanup at `prompt-template/claude/finalize-phase-prompt.md:16`.
- dependencies_and_callers: Depends on Task subagent availability, plan and goal tracker references at `prompt-template/claude/finalize-phase-prompt.md:36`, and the finalize lifecycle in `hooks/loop-codex-stop-hook.sh`, where successful completion renames `state.md` to `finalize-state.md` and creates the finalize prompt.
- edge_cases_or_failure_modes: Risk is over-refactoring after acceptance; the prompt counters this by narrowing scope to recently changed code and branch diff `{{BASE_BRANCH}}` to `{{START_BRANCH}}` at `prompt-template/claude/finalize-phase-prompt.md:27`. Failure to write `finalize-summary.md` blocks final completion in the surrounding loop.
- validation_or_tests: Finalize-phase tests exercise finalize-state detection, finalize-summary allowance, finalize-state protection, and completion transition to `complete-state.md`; relevant discovered references are in `tests/test-finalize-phase.sh` around `T-POS-3`, `T-POS-4`, `T-NEG-5`, and finalize completion cases.
- skip_candidate: `yes: prompt template rather than executable code, but it defines an algorithmic phase transition and acceptance/finalization contract`

### FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-137 `file` `tests/robustness/test-pr-loop-api-robustness.sh`
- cursor: `[_]`
- core_role: End-to-end robustness specification for PR-loop API behavior under mocked GitHub CLI responses, covering state discovery, comment fetching, bot parsing, JSON edge cases, stop-hook tolerance, and polling failure semantics.
- algorithmic_behavior: Builds temporary repos and a generated `gh` mock with behavior modes such as `empty_array`, `rate_limit`, `network_error`, `claude_approval`, `codex_issues`, `mixed_bots`, `unicode_comment`, and `long_comment` at `tests/robustness/test-pr-loop-api-robustness.sh:32`. It then invokes real scripts/hooks rather than testing helpers only.
- inputs_outputs_state: Inputs are synthetic `.humanize/pr-loop/<timestamp>/state.md` files, mocked `gh` API output, command-line args to `fetch-pr-comments.sh` and `poll-pr-reviews.sh`, and stop-hook stdin `{}`. Outputs are generated markdown comment files, JSON poller output, hook exit codes, and pass/fail counters from `tests/test-helpers.sh:30`.
- gates_or_invariants: `find_active_pr_loop` must detect the newest PR loop with `state.md` even when `pr_number` is missing at `tests/robustness/test-pr-loop-api-robustness.sh:285` and `tests/robustness/test-pr-loop-api-robustness.sh:324`; production detection is in `hooks/lib/loop-common.sh:798`. API failure in `poll-pr-reviews.sh` must exit 0, emit valid JSON, and set boolean `has_new_comments:false` at `tests/robustness/test-pr-loop-api-robustness.sh:811`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` and `tests/test-helpers.sh` at `tests/robustness/test-pr-loop-api-robustness.sh:18`. Calls `scripts/fetch-pr-comments.sh`, which retries three times, writes empty arrays on failed endpoints, formats markdown, and warns on incomplete results at `scripts/fetch-pr-comments.sh:176`, `scripts/fetch-pr-comments.sh:183`, and `scripts/fetch-pr-comments.sh:445`. Calls `scripts/poll-pr-reviews.sh`, whose retry wrapper returns `[]` on API failure and final JSON fields at `scripts/poll-pr-reviews.sh:207` and `scripts/poll-pr-reviews.sh:317`. Calls `hooks/pr-loop-stop-hook.sh`, which parses YAML-list `configured_bots` and `active_bots` at `hooks/pr-loop-stop-hook.sh:87`.
- edge_cases_or_failure_modes: Covers rate limiting, network failure, auth failure mock behavior, empty arrays, Unicode bodies, very long comment bodies, corrupted PR-loop state, absent active loop, slow API responses, bot author mapping for `codex` to `chatgpt-codex-connector[bot]`, and warning-before-JSON poller output extraction at `tests/robustness/test-pr-loop-api-robustness.sh:379`, `tests/robustness/test-pr-loop-api-robustness.sh:408`, `tests/robustness/test-pr-loop-api-robustness.sh:511`, `tests/robustness/test-pr-loop-api-robustness.sh:528`, and `tests/robustness/test-pr-loop-api-robustness.sh:819`.
- validation_or_tests: Nineteen robustness tests run through summary at `tests/robustness/test-pr-loop-api-robustness.sh:845`. Key assertions include markdown output for no comments, warning/nonzero tolerance for fetch failures, bot comment visibility for Claude/Codex/mixed bots, JSON parseability, `approve-state.md` path writability, poller usage/missing-arg validation, and strict API-failure JSON contract.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5 headings above; each assigned item is represented once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`