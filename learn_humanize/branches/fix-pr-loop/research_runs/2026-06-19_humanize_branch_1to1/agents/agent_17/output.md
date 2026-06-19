# agent_17 fix-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `81f6f49d816a90a0e719db41ce15c4636ab9858a`

## Item Evidence

### FIX_PR_LOOP-HZ-017 `file` `agents/draft-relevance-checker.md`
- cursor: `[_]`
- core_role: Repository-relevance gate agent for `gen-plan`; its frontmatter declares `name: draft-relevance-checker`, `model: haiku`, and read/search-only tools `Read, Glob, Grep` at `agents/draft-relevance-checker.md:1-6`.
- algorithmic_behavior: The prompt instructs the subagent to inspect repository docs and structure, infer project technologies/purpose, compare the supplied draft semantically against repo concepts/files/features, and emit exactly one verdict form: `RELEVANT: ...` or `NOT_RELEVANT: ...` at `agents/draft-relevance-checker.md:14-29`.
- inputs_outputs_state: Input is draft document content plus read-only repository context. Output is a single verdict string with a brief explanation. It does not mutate loop state or files; it is a planning gate before downstream plan generation.
- gates_or_invariants: The decision policy is deliberately lenient: informal drafts and any language are acceptable, semantic relevance matters more than exact wording, and doubt should resolve to relevant at `agents/draft-relevance-checker.md:31-36`.
- dependencies_and_callers: `commands/gen-plan.md:50-72` invokes this agent during Phase 2; `NOT_RELEVANT` stops the command, while `RELEVANT` advances to Phase 3.
- edge_cases_or_failure_modes: False positives are preferred over false negatives by design. The output contract is prompt-enforced rather than schema-enforced, so callers depend on the agent preserving the exact verdict prefix.
- validation_or_tests: `tests/test-gen-plan.sh:111-156`, `tests/test-gen-plan.sh:290-295`, and `tests/test-gen-plan.sh:392-421` validate existence, frontmatter fields, haiku model, tool declaration, valid model name, and English/no-emoji content.
- skip_candidate: `no`

### FIX_PR_LOOP-HZ-047 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role: Executable specification for the RLCR loop file-access allowlist that lets a small set of historical todo/summary files bypass normal round-file blocking.
- algorithmic_behavior: The test creates a temp git repo and active loop state with `current_round: 5` at `tests/test-allowlist-validators.sh:29-64`, then verifies `is_allowlisted_file` accepts only `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` inside the active loop dir at `tests/test-allowlist-validators.sh:72-127`. The underlying allowlist is defined in `hooks/lib/loop-common.sh:423-441`.
- inputs_outputs_state: Inputs are synthetic Claude hook JSON payloads for `Write`, `Edit`, `Read`, and `Bash`. Output is PASS/FAIL accounting and process exit equal to failed test count at `tests/test-allowlist-validators.sh:385-393`. State is isolated under `mktemp` and cleaned by trap.
- gates_or_invariants: Write/Edit/Read must allow exact active-dir allowlist paths and block non-allowlisted rounds with exit `2` plus relevant error text at `tests/test-allowlist-validators.sh:132-283`. Bash is stricter: it allows only full active-loop paths to `round-1-todos.md` or `round-2-todos.md`, blocking wrong directories, bare basenames, old loop dirs, and same timestamp under a different root at `tests/test-allowlist-validators.sh:290-383`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at `tests/test-allowlist-validators.sh:17`; exercises `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-read-validator.sh`, and `hooks/loop-bash-validator.sh`. Bash path restriction is implemented around `hooks/loop-bash-validator.sh:385-392`.
- edge_cases_or_failure_modes: The allowlist is fixed, not derived from `current_round`; this intentionally permits historical files while preserving current-round validation elsewhere. The security-sensitive edge is same basename outside the active loop, covered by tests 21, 23, 24, and 25.
- validation_or_tests: This file is itself the validation harness. It covers 25 assertions across helper-level allowlist behavior and hook-level enforcement. I inspected it read-only and did not execute it.
- skip_candidate: `no`

### FIX_PR_LOOP-HZ-077 `file` `prompt-template/block/finalize-state-file-modification.md`
- cursor: `[_]`
- core_role: User-facing block template for the invariant that `finalize-state.md` is loop-system-managed during Finalize Phase.
- algorithmic_behavior: The template denies direct modification of `finalize-state.md` and redirects the agent toward the allowed finalization workflow: run code simplification, commit changes, and write `finalize-summary.md` at `prompt-template/block/finalize-state-file-modification.md:1-8`.
- inputs_outputs_state: Input is a validator block event; the template has no variables. Output is markdown text rendered to stderr by validator helpers. It does not transition state itself.
- gates_or_invariants: Direct writes/edits/bash modifications to `finalize-state.md` must be blocked; the only valid agent-authored completion artifact is the finalize summary, not the state file.
- dependencies_and_callers: Loaded by `finalize_state_file_blocked_message` in `hooks/lib/loop-common.sh` and called by write/edit/bash validators. Relevant call sites include `hooks/loop-write-validator.sh:152-154`, `hooks/loop-edit-validator.sh:117-119`, and `hooks/loop-bash-validator.sh:139-145`.
- edge_cases_or_failure_modes: Because this is a static block message, cancel-specific exceptions are handled in validator logic, not in the template. If the template is missing, callers fall back to an inline message.
- validation_or_tests: `tests/test-finalize-phase.sh` covers write/edit/bash blocking of `finalize-state.md`, including bash source-protection cases for moving or copying it, as shown in the reference hits around `tests/test-finalize-phase.sh:357-414`.
- skip_candidate: `no`

### FIX_PR_LOOP-HZ-107 `file` `prompt-template/claude/finalize-phase-prompt.md`
- cursor: `[_]`
- core_role: Finalize Phase instruction contract shown after Codex review passes and before the RLCR loop can complete.
- algorithmic_behavior: The prompt declares implementation complete, instructs Claude to invoke `code-simplifier:code-simplifier` through the Task tool, and limits work to functionality-equivalent simplification/refactoring at `prompt-template/claude/finalize-phase-prompt.md:1-24`.
- inputs_outputs_state: Inputs are template variables `{{BASE_BRANCH}}`, `{{START_BRANCH}}`, `{{PLAN_FILE}}`, `{{GOAL_TRACKER_FILE}}`, and `{{FINALIZE_SUMMARY_FILE}}` at `prompt-template/claude/finalize-phase-prompt.md:29-45`. Expected outputs are completed todos, a descriptive commit, and a finalize summary listing simplifications, modified files, passing tests, and refactoring notes at `prompt-template/claude/finalize-phase-prompt.md:41-51`.
- gates_or_invariants: The prompt forbids functionality changes, test regressions, new bugs, and non-equivalent cleanup at `prompt-template/claude/finalize-phase-prompt.md:16-24`. It scopes review to recent changes and the branch delta from base to start at `prompt-template/claude/finalize-phase-prompt.md:25-34`.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh` loads this template when entering Finalize Phase after review success; search references show `state.md` is renamed to `finalize-state.md` and the template is rendered via `claude/finalize-phase-prompt.md` around `hooks/loop-codex-stop-hook.sh:1036-1097`.
- edge_cases_or_failure_modes: This template assumes review has passed; skipped or uncertain review uses a separate skipped-finalize prompt. Operationally, the “use code-simplifier” instruction can block clean completion if the subagent is unavailable unless caller fallback policy handles it.
- validation_or_tests: `tests/test-finalize-phase.sh` validates Finalize Phase entry, prompt mention of code-simplifier, finalize-summary allowance, finalize-state protection, todo completion requirements, and final state completion behavior.
- skip_candidate: `no`

### FIX_PR_LOOP-HZ-137 `file` `tests/robustness/test-pr-loop-api-robustness.sh`
- cursor: `[_]`
- core_role: Robustness specification for PR-loop API, bot-comment parsing, state detection, and polling behavior under GitHub CLI failures.
- algorithmic_behavior: The script sources shared loop/test helpers at `tests/robustness/test-pr-loop-api-robustness.sh:16-21`, builds a behavior-switching mock `gh` command at `tests/robustness/test-pr-loop-api-robustness.sh:32-239`, creates PR-loop state fixtures at `tests/robustness/test-pr-loop-api-robustness.sh:241-261`, and initializes isolated git repos at `tests/robustness/test-pr-loop-api-robustness.sh:264-276`.
- inputs_outputs_state: Inputs are mocked `gh` behaviors, temp repos, PR number `123`, timestamps, and bot lists. Outputs are PASS/FAIL lines plus `print_test_summary` exit status at `tests/robustness/test-pr-loop-api-robustness.sh:845-850`. State is isolated under `mktemp` and `.humanize/pr-loop/<timestamp>/`.
- gates_or_invariants: `find_active_pr_loop` must detect a newest dir with `state.md` even with missing `pr_number` at `tests/robustness/test-pr-loop-api-robustness.sh:285-345`; `fetch-pr-comments.sh` must handle empty arrays, rate limits, network errors, Claude/Codex/mixed bot comments, unicode, and long bodies at `tests/robustness/test-pr-loop-api-robustness.sh:355-550`; stop-hook handling must not crash on no active loop or corrupted state at `tests/robustness/test-pr-loop-api-robustness.sh:560-609`; `poll-pr-reviews.sh` must validate args and output parseable JSON with boolean `has_new_comments`, including strict API-failure behavior at `tests/robustness/test-pr-loop-api-robustness.sh:620-843`.
- dependencies_and_callers: Exercises `hooks/lib/loop-common.sh:798-814`, `hooks/pr-loop-stop-hook.sh`, `scripts/fetch-pr-comments.sh`, and `scripts/poll-pr-reviews.sh`. Production retry behavior returns empty arrays on API failure in `scripts/fetch-pr-comments.sh:183-208` and `scripts/poll-pr-reviews.sh:210-235`; polling maps `codex` to `chatgpt-codex-connector[bot]` at `scripts/poll-pr-reviews.sh:164-187`.
- edge_cases_or_failure_modes: Covered edges include rate limits, connection errors, slow API, empty JSON, unicode, very long comments, mixed bot outputs, missing args, corrupted state text, and warnings before JSON. The `auth_failure` mock behavior exists but is not asserted in this script.
- validation_or_tests: This file is the validation harness. It verifies output file creation for comment fetches, JSON shape for polling, graceful stop-hook behavior, and strict boolean `false` on polling API failure. I inspected it read-only and did not execute it.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `5/5 item evidence sections present; each assigned heading appears once`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`