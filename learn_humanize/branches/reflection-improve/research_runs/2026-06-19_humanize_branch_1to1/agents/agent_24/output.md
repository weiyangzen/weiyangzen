# agent_24 reflection-improve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `13a47fb2260667a272b448e8d3c1a521f2382590`

## Item Evidence

### REFLECTION_IMPROVE-HZ-024 `directory` `tests/robustness`
- cursor: `[_]`
- core_role: Recursive robustness specification suite for loop setup, hook safety, state/session parsing, PR review APIs, template rendering, git/base-branch detection, timeout behavior, and monitor helpers. The directory has 19 shell files, no child directories, and 8,852 total lines by direct inventory.
- algorithmic_behavior: Exercises production algorithm surfaces rather than mocks only. Key child roles: `test-setup-scripts-robustness.sh` covers `setup-rlcr-loop.sh`/`setup-pr-loop.sh` argument, dependency, mutual-exclusion, skip-impl, full-review-round, YAML, symlink, and repo gates (`:90`, `:466`, `:528`, `:869`, `:968`, `:1078`); `test-path-validation-robustness.sh` and `test-plan-file-robustness.sh` validate plan path/content admission (`:76`, `:116`, `:172`, `:293`); `test-state-file-robustness.sh`, `test-state-transition-robustness.sh`, `test-concurrent-state-robustness.sh`, and `test-session-robustness.sh` cover state schemas, active/finalize/cancel transitions, newest-session selection, concurrent reads, and zombie-loop prevention (`test-state-transition-robustness.sh:141`, `:175`, `:364`; `test-session-robustness.sh:89`); hook tests validate JSON, depth, UTF-8/null-byte, edit/write/bash/stop-hook behavior (`test-hook-input-robustness.sh:28`, `:177`, `:201`; `test-hook-system-robustness.sh:34`, `:310`, `:454`); PR loop tests split a shared library into fetch and poll suites (`test-pr-loop-api-fetch.sh:15`, `test-pr-loop-api-poll.sh:14`) over `fetch-pr-comments.sh`, `poll-pr-reviews.sh`, and `pr-loop-stop-hook.sh`; template tests stress `render_template`/`load_and_render_safe`; timeout tests cover portable `run_with_timeout`; git/goal/base tests cover monitor-facing parsers.
- inputs_outputs_state: Inputs are generated temp repos, state files under `.humanize/...`, synthetic hook JSON, mock `gh` and `codex` binaries, mock PR comments/reviews, plan files, template files, terminal/log fixtures, and command strings. Outputs are pass/fail assertions via `tests/test-helpers.sh`, generated temp artifacts, and runner exit code aggregation. State transitions under test include `state.md` to `finalize-state.md`, cancel terminal states, PR loop review polling, setup-created markers, and atomic state reads during concurrent writes.
- gates_or_invariants: Suite asserts malformed or unsafe input is rejected without crashes: invalid JSON, null bytes, invalid UTF-8, deep JSON, state edits, goal-tracker modification after round 0, bad plan paths, shell metacharacters, symlink chains, absolute paths, missing dependencies, corrupted state, and API failures. It also codifies current tolerances such as some tolerant state parsing defaults and `--codex-timeout 0` acceptance.
- dependencies_and_callers: `tests/run-all-tests.sh` includes the robustness files as parallel suites at `:101-119`; the PR-loop split wrappers source `test-pr-loop-api-robustness.sh` (`test-pr-loop-api-fetch.sh:15`, `test-pr-loop-api-poll.sh:14`). Production dependencies include `hooks/lib/loop-common.sh`, `hooks/lib/template-loader.sh`, `scripts/humanize.sh`, `scripts/portable-timeout.sh`, setup scripts, hook validators, and PR scripts. `loop-common.sh` itself exposes tested helpers for hook JSON validation and active loop/state discovery (`hooks/lib/loop-common.sh:80`, `:213`, `:257`).
- edge_cases_or_failure_modes: Covers high-risk failure modes: stale active-loop resurrection, malformed YAML, CRLF state files, binary/null content, permission denial, missing repos/remotes, detached/rebase/merge/shallow git states, slow/failing GitHub API, rate limits, long PR comments, Unicode, long templates/variables, and shell injection in cancel commands.
- validation_or_tests: This item is itself validation coverage. I inspected the recursive tree and runner registration; I did not execute the suite in this read-only research pass.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-054 `file` `scripts/check-pr-reviewer-status.sh`
- cursor: `[_]`
- core_role: Runtime PR-loop classifier that maps whole-PR reviewer history into startup/re-review cases for active bot reviewers.
- algorithmic_behavior: Parses `<pr_number> --bots <bot1,bot2>` (`:49-85`), maps bot aliases to GitHub author logins, with special `codex -> chatgpt-codex-connector[bot]` (`:91-100`), resolves the PR base repo by checking current repo then fork parent (`:109-140`), fetches latest PR head commit and committed date (`:142-151`), gathers issue comments, inline review comments, and PR review submissions with pagination (`:153-165`), combines them via `jq -s 'add // []'` (`:167-168`), then computes which bots commented, are missing, and are stale per bot (`:174-205`).
- inputs_outputs_state: Inputs are GitHub CLI context, PR number, comma-separated bot list, `gh`, `jq`, and `scripts/portable-timeout.sh` (`:38-40`). Output is JSON with `case`, `reviewers_commented`, `reviewers_missing`, `latest_commit_sha`, `latest_commit_at`, `newest_review_at`, and `has_commits_after_reviews` (`:259-275`). It does not persist state; it derives state from PR history.
- gates_or_invariants: Requires exactly one PR number and required `--bots`; unknown options and duplicate PR args fail (`:49-85`). All GitHub calls use `run_with_timeout "$GH_TIMEOUT"` with default 60 seconds (`:35-40`). Per-bot staleness compares ISO timestamps lexically (`:192-196`), so freshness is determined per reviewer, not by global newest review.
- dependencies_and_callers: Called by `scripts/setup-pr-loop.sh` to determine initial PR-loop case (`setup-pr-loop.sh:437-438`) and by `hooks/pr-loop-stop-hook.sh` during loop updates (`pr-loop-stop-hook.sh:1557`). Tested by PR-loop system/stophook suites (`tests/test-pr-loop-system.sh:159`, `:662`, `:1327`; `tests/test-pr-loop-stophook.sh:1192-1257`).
- edge_cases_or_failure_modes: If PR base repo cannot be resolved, warns and falls back to current repo (`:137-140`), which may still fail later if empty. Comment fetch failures become empty arrays (`:156-165`), but commit-info fetch failure is fatal (`:143-148`). Case comments at `:22-27` mention 1-5, but implementation gives case 5 for partial reviewers with stale comments (`:223-230`), not only “all reviewers commented, new commits after.”
- validation_or_tests: JSON behavior and case detection are exercised in PR-loop test suites; direct robustness API tests cover related fetch/poll behavior under empty, rate-limited, network-error, slow, and failing API mocks.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-084 `file` `tests/test-model-router.sh`
- cursor: `[_]`
- core_role: Executable specification for provider routing, CLI dependency checks, and effort mapping in `scripts/lib/model-router.sh`.
- algorithmic_behavior: Sources `tests/test-helpers.sh` and `scripts/lib/model-router.sh` (`:5-8`), creates mock binaries in temp `bin` dirs (`:17-27`), then asserts `detect_provider` routes OpenAI-style `gpt-*` and `o[0-9]*` names to `codex` (`:29-111`) and Claude family names/keywords to `claude` (`:113-196`). It verifies unknown and empty model names fail with diagnostics (`:198-230`), provider dependency checks succeed/fail based on PATH (`:232-298`), and effort mapping transforms or rejects values (`:300-420`).
- inputs_outputs_state: Inputs are model strings, provider strings, effort strings, PATH composition, and temporary mock binaries. Outputs are pass/fail lines and final summary from `print_test_summary` (`:422-426`). Temporary state lives under helper-managed test dirs; no repo state is modified.
- gates_or_invariants: Codex model gate is prefix-based: `gpt-*` or `o[0-9]*`; Claude gate is case-insensitive match on `^claude-` or `haiku|sonnet|opus` as implemented in `scripts/lib/model-router.sh:18-29`. Dependency gate requires executable `codex` or `claude` in PATH (`model-router.sh:32-60`). Effort gate allows only `xhigh|high|medium|low`; `xhigh` maps to `high` only for Claude with an info log (`model-router.sh:62-90`).
- dependencies_and_callers: Registered in all-tests runner (`tests/run-all-tests.sh:95-99`). The router is consumed by `scripts/bitlesson-select.sh` for model-to-provider dispatch (`bitlesson-select.sh:11`, `:89`). The test uses `SAFE_BASE_PATH` to isolate PATH lookup (`tests/test-model-router.sh:10`).
- edge_cases_or_failure_modes: Unknown model names must exit non-zero and include error text (`:205-213`); empty model names must be rejected (`:222-230`); missing CLI binaries fail provider checks (`:250-264`, `:284-298`); unsupported effort `ultra` must fail for both Claude and Codex (`:388-420`). Test numbering duplicates “Test 10” around empty model and codex dependency, but behavior remains distinct.
- validation_or_tests: This file is direct validation for `detect_provider`, `check_provider_dependency`, and `map_effort`; I inspected it and the implementation file. I did not execute it.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-114 `file` `prompt-template/block/bitlesson-delta-empty-kb.md`
- cursor: `[_]`
- core_role: Prompt gate block that forbids `Action: none` when BitLesson knowledge base has no concrete lesson entries.
- algorithmic_behavior: Emits a “BitLesson Recording Required” instruction and explicitly says `Action: none` is not allowed while `.humanize/bitlesson.md` lacks concrete lesson entries (`:1-3`). It then requires adding or updating at least one reusable lesson entry and reporting `Action: add` or `Action: update` when resolving prior-round issues (`:5`).
- inputs_outputs_state: Input is the BitLesson delta-validation context deciding that the KB is empty. Output is a rendered prompt/reason block inserted into validation feedback. It changes no state itself; it constrains the model’s next reported action and expected BitLesson file delta.
- gates_or_invariants: Invariant is non-empty learning capture before “none” can pass. It establishes an algorithmic transition from empty KB plus resolved issues to mandatory add/update action.
- dependencies_and_callers: Loaded through `load_and_render_safe` in `scripts/bitlesson-validate-delta.sh` when building the rejection reason (`bitlesson-validate-delta.sh:179`). Rendering uses `hooks/lib/template-loader.sh` safe fallback behavior (`template-loader.sh:170-203`).
- edge_cases_or_failure_modes: If the template is missing or empty, caller fallback text is used by `load_and_render_safe`, so the gate should still produce a blocking reason. The template has no variables, so rendering injection risk is minimal.
- validation_or_tests: Template reference coverage includes prompt-template blocks in `tests/test-template-references.sh`; BitLesson routing is covered separately by `tests/test-bitlesson-select-routing.sh` in the runner. Direct content inspected at `prompt-template/block/bitlesson-delta-empty-kb.md:1-5`.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-144 `file` `prompt-template/block/todos-file-access.md`
- cursor: `[_]`
- core_role: Prompt safety block that forbids direct `round-*-todos.md` file creation/access and routes task state through native Task tools.
- algorithmic_behavior: Tells agents “Do NOT create or access `round-*-todos.md` files” (`:3`) and requires native task tools instead (`:5-8`). This is a prompt-level access-control transition: file-backed todos are blocked in favor of tool-managed task state visible in the UI.
- inputs_outputs_state: Input is a prompt assembly path that needs to warn about todo file access. Output is rendered markdown guidance. It does not modify task state; it defines the permitted state interface.
- gates_or_invariants: Invariant is that task tracking must use `TaskCreate`, `TaskUpdate`, and `TaskList`, not ad hoc round todo files. The block prevents hidden or divergent task state.
- dependencies_and_callers: Exposed by `hooks/lib/loop-common.sh` through a helper that calls `load_and_render_safe "$TEMPLATE_DIR" "block/todos-file-access.md"` (`loop-common.sh:626`). Template reference tests list this block (`tests/test-template-references.sh:153`). Rendering semantics come from `hooks/lib/template-loader.sh:170-203`.
- edge_cases_or_failure_modes: Missing template falls back to inline text from the caller. The block assumes Claude Code native Task tools exist; in non-Claude contexts this may be a skip/alternate-routing concern, but within this repository’s hook prompt assembly it is a deliberate contract.
- validation_or_tests: Direct content inspected at `prompt-template/block/todos-file-access.md:1-8`; included in template-reference validation.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-174 `file` `prompt-template/pr-loop/round-0-header.md`
- cursor: `[_]`
- core_role: PR-loop round-0 prompt header template that initializes the reviewer-monitoring context before fetched comments are appended.
- algorithmic_behavior: Starts with “Read and execute below with ultrathink” (`:1`), declares “PR Review Loop (Round 0)” (`:3`), identifies the agent as monitoring remote review bots (`:5`), renders PR number, start branch, and active bot display from placeholders (`:7-10`), then opens a “Review Comments” section for fetched PR comments (`:12-15`).
- inputs_outputs_state: Inputs are `{{PR_NUMBER}}`, `{{START_BRANCH}}`, and `{{ACTIVE_BOTS_DISPLAY}}` from setup state. Output is markdown prompt header content written into the round-0 PR loop prompt. It does not persist state directly but frames the initial loop state for the reviewing agent.
- gates_or_invariants: Requires round-0 prompt context to include exact PR identity, starting branch, and active reviewers before review comments. Placeholder syntax relies on single-pass rendering, so inserted values containing `{{...}}` are not recursively expanded (`hooks/lib/template-loader.sh:50-58`, `:71-131`).
- dependencies_and_callers: `scripts/setup-pr-loop.sh` loads this template via `load_and_render_safe "$TEMPLATE_DIR" "pr-loop/round-0-header.md"` (`setup-pr-loop.sh:758`) after fetching comments and reviewer status (`setup-pr-loop.sh:430-438`). It depends on `hooks/lib/template-loader.sh` and prompt-template directory validation.
- edge_cases_or_failure_modes: If the template is missing/empty, setup uses fallback header content through `load_and_render_safe`. Missing or malformed variables would leave unresolved placeholders because missing variables are intentionally preserved by the template engine (`template-loader.sh:13`, `:120-121`).
- validation_or_tests: Direct content inspected at `prompt-template/pr-loop/round-0-header.md:1-15`; setup and PR-loop tests cover prompt/template references and round initialization paths.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `REFLECTION_IMPROVE-HZ-024`, `REFLECTION_IMPROVE-HZ-054`, `REFLECTION_IMPROVE-HZ-084`, `REFLECTION_IMPROVE-HZ-114`, `REFLECTION_IMPROVE-HZ-144`, `REFLECTION_IMPROVE-HZ-174`
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`