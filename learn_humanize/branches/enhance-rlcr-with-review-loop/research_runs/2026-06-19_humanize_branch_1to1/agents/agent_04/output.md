# agent_04 enhance-rlcr-with-review-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `dd6c37c45c4836773497f878b8925057e9f5318c`

## Item Evidence

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-004 `directory` `hooks`
- cursor: `[_]`
- core_role: `hooks/` is the runtime guard and stop-hook layer for both RLCR and PR review loops. `hooks/hooks.json:1-69` wires Claude Code events: `UserPromptSubmit` to plan validation, `PreToolUse` to Write/Edit/Read/Bash validators, and `Stop` to both `loop-codex-stop-hook.sh` and `pr-loop-stop-hook.sh`.
- algorithmic_behavior: The directory enforces loop state integrity before tools run, then controls exit attempts. `hooks/pr-loop-stop-hook.sh:87-174` parses PR-loop YAML state, `:244-256` terminates on merged/closed PRs, `:262-277` requires the current round resolve file, `:283-361` blocks dirty or unpushed work, `:368-424` detects force-push rewrites and clears stale triggers, `:684-708` decides when trigger comments are required, `:757-789` verifies Claude `eyes`, `:897-1049` polls bot responses with per-bot timeout, and `:1354-1623` branches on Codex `APPROVE`, `WAITING_FOR_BOTS`, `USAGE_LIMIT_HIT`, or issue continuation. The RLCR stop hook separately drives implementation review, code-review phase, finalize phase, and next-round prompting in `hooks/loop-codex-stop-hook.sh:716-721`, `:965-994`, `:998-1127`, `:1209-1435`, and `:1437-1537`.
- inputs_outputs_state: Inputs are Claude hook JSON, `.humanize/rlcr/<timestamp>/state.md`, `.humanize/pr-loop/<timestamp>/state.md`, Git state, GitHub PR/comment/reaction APIs, Codex CLI output, and prompt templates. Outputs are hook JSON decisions, generated prompt/comment/check/feedback files, and state-file renames such as `approve-state.md`, `merged-state.md`, `closed-state.md`, `maxiter-state.md`, `usage-limit-state.md`, `finalize-state.md`, and `complete-state.md`.
- gates_or_invariants: Shared validation rejects malformed JSON, null bytes, invalid UTF-8, and deep nesting in `hooks/lib/loop-common.sh:58-132`. Strict state parsing requires frontmatter, numeric round fields, `review_started`, and `base_branch` for RLCR in `:251-324`. PR-loop state files and generated PR artifacts are protected by Write/Edit/Bash validators in `hooks/loop-write-validator.sh:74-94`, `hooks/loop-edit-validator.sh:57-77`, and `hooks/loop-bash-validator.sh:403-442`. `.humanize` is protected from broad or forced `git add` in `hooks/lib/loop-common.sh:924-1020`.
- dependencies_and_callers: `hooks/lib/template-loader.sh:26-222` provides single-pass template loading/rendering. `hooks/lib/loop-common.sh:792-880` provides PR active-loop discovery, read-only PR file detection, and `round-N-pr-resolve.md` round validation. `pr-loop-stop-hook.sh` calls `scripts/check-bot-reactions.sh` at `:459`, `:766`, and `:985`, `scripts/poll-pr-reviews.sh` at `:801` and `:951`, and `scripts/check-pr-reviewer-status.sh` at `:1534`. `loop-codex-stop-hook.sh` uses `hooks/check-todos-from-transcript.py:20-129` to block exit on incomplete TodoWrite state.
- edge_cases_or_failure_modes: Covered edge behavior includes fork PR base-repo resolution (`pr-loop-stop-hook.sh:204-237`), stale trigger rejection after new commits (`:605-629`) or force push (`:396-421`), startup cases where round 0 may or may not require triggers (`:677-708`), Claude bot non-response (`:757-779`), per-bot timeout removal (`:1057-1130`), mixed bot approval with re-add logic (`:1418-1481`), and review-phase tamper detection via `.review-phase-started` marker (`loop-codex-stop-hook.sh:1412-1428`).
- validation_or_tests: `tests/test-pr-loop-stophook.sh` directly exercises PR stop-hook behavior. Additional references show broader PR-loop tests in `tests/test-pr-loop-hooks.sh` and `tests/test-pr-loop-system.sh`. I inspected recursively with `rg --files hooks` and line-numbered reads; no files were modified.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-034 `file` `scripts/check-bot-reactions.sh`
- cursor: `[_]`
- core_role: This script is the reaction signal detector used by PR-loop setup and stop-hook gates. It turns GitHub reactions into deterministic approval/acknowledgement signals for Codex and Claude.
- algorithmic_behavior: It supports two commands: `codex-thumbsup` and `claude-eyes` (`scripts/check-bot-reactions.sh:86-303`). `codex-thumbsup` resolves the PR base repo for fork support (`:123-147`), fetches all issue reactions with pagination (`:149-159`), selects the first `chatgpt-codex-connector[bot]` `+1` reaction (`:161-165`), optionally rejects reactions older than `--after` (`:174-180`), and prints the reaction JSON (`:182-184`). `claude-eyes` parses comment ID, optional PR number, retry count, and delay (`:187-222`), resolves base repo (`:233-257`), sleeps and retries (`:259-263`), fetches paginated comment reactions (`:264-273`), and returns the first `claude[bot]` `eyes` reaction (`:275-284`).
- inputs_outputs_state: Inputs are CLI args, `gh repo view`, `gh pr view`, `gh api` reactions endpoints, `jq`, and `scripts/portable-timeout.sh` sourced at `:31-33`. Outputs are JSON reaction objects on success, stderr diagnostics on timeout/API/argument failures, and exit codes: `0` found, `1` not found, `2` error (`:13-16`, `:57-60`).
- gates_or_invariants: Requires exactly one PR number or comment ID depending on command (`:103-117`, `:213-227`); unknown options and duplicate positional args are hard errors. API operations are timeout-wrapped via `GH_TIMEOUT=30` (`:24-25`). Pagination is mandatory and merged with `jq -s 'add // []'` to avoid missing reactions beyond default page size (`:153-156`, `:267-270`).
- dependencies_and_callers: Called by `scripts/setup-pr-loop.sh:507` for initial Claude eyes confirmation, and by `hooks/pr-loop-stop-hook.sh:459`, `:766`, and `:985` for Codex thumbs-up approval and Claude eyes verification. Tests call it in `tests/test-pr-loop-system.sh:200-225`.
- edge_cases_or_failure_modes: Fork PRs are handled by trying current repo, then parent repo, then current fallback (`:119-147`, `:229-257`). API failure in `codex-thumbsup` exits `2` (`:154-159`); API failure during `claude-eyes` retry continues to the next attempt (`:268-273`). Timestamp comparison is lexical ISO-8601 comparison (`:175-179`), so it assumes normalized UTC timestamps. `claude-eyes` sleeps before every attempt, including the first (`:260-263`), so `--retry 3 --delay 5` waits up to 15 seconds.
- validation_or_tests: Stop-hook tests indirectly validate this script via mocked `gh` for Codex `+1` and Claude `eyes` paths in `tests/test-pr-loop-stophook.sh:176-205`, `:931-966`, and `:1046-1100`. System-level direct tests cover `codex-thumbsup`, `--after`, and `claude-eyes` in `tests/test-pr-loop-system.sh:200-225`.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-064 `file` `tests/test-pr-loop-stophook.sh`
- cursor: `[_]`
- core_role: This is an executable specification for PR stop-hook state-machine behavior, especially the review-loop additions around force pushes, trigger freshness, per-bot polling, bot reactions, startup cases, fork PRs, and mixed approval.
- algorithmic_behavior: `run_stophook_tests` defines isolated shell tests under temporary `.humanize/pr-loop/<timestamp>/` fixtures (`tests/test-pr-loop-stophook.sh:15-1786`). Each test creates a synthetic `state.md`, required `round-N-pr-resolve.md`, mock `gh` and `git` executables, sets `CLAUDE_PROJECT_DIR`, invokes `hooks/pr-loop-stop-hook.sh`, and asserts file/state/output effects.
- inputs_outputs_state: Inputs are fixture state fields such as `current_round`, `configured_bots`, `active_bots`, `startup_case`, `latest_commit_sha`, `latest_commit_at`, `last_trigger_at`, and `trigger_comment_id`. Outputs are pass/fail calls, hook output assertions, and concrete state files like `approve-state.md`, updated `state.md`, `round-1-pr-check.md`, and active bot YAML sections.
- gates_or_invariants: The tests assert stale triggers after force push/new commits are rejected (`:20-138`), case 1 round 0 does not require a trigger (`:140-244`), empty active bots approve (`:246-325`), unpushed commits block exit (`:452-536`), force-push ancestry failure blocks and clears stale trigger requirements (`:538-640`), case 4 missing trigger blocks (`:642-752`), Claude eyes timeout blocks (`:1011-1143`), and fork PR lookup resolves through parent/base repo (`:1395-1522`).
- dependencies_and_callers: The file depends on the wider test harness providing `TEST_DIR`, `PROJECT_ROOT`, `pass`, and `fail`. It invokes `hooks/pr-loop-stop-hook.sh` repeatedly and supplies mocks for the hook’s dependencies: `gh`, `git`, and, in mixed approval, `codex` (`:1682-1706`).
- edge_cases_or_failure_modes: It includes time-sensitive cases using short `poll_timeout` and GNU/BSD-compatible date fallbacks (`:1150-1158`, `:1529-1539`), fake fork behavior where current repo lacks the PR but parent repo has it (`:1429-1479`), missing/old trigger comments (`:57-84`, `:677-710`), and mixed bot outcomes where one bot approves while another reports issues (`:1682-1767`).
- validation_or_tests: The test list executed by the function is explicit at `:1772-1784`. One defined test, `test_stophook_dynamic_startup_case` at `:327-450`, is not included in the final run list, while `test_stophook_dynamic_startup_case_update` at `:1145-1393` is included; that is a coverage detail worth preserving.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-094 `file` `prompt-template/block/pr-loop-state-modification.md`
- cursor: `[_]`
- core_role: This is the user-facing block template for PR-loop state immutability. It is part of the algorithm’s guard contract because it explains why `state.md` may not be modified manually.
- algorithmic_behavior: The template states that `.humanize/pr-loop/state.md` is managed by the PR-loop system and lists the state domains that would be corrupted by manual edits: current round, PR and branch, active bots, Codex config, and polling settings (`prompt-template/block/pr-loop-state-modification.md:1-12`).
- inputs_outputs_state: Input is template loading through `pr_loop_state_blocked_message` in `hooks/lib/loop-common.sh:883-890`; output is stderr block text from Write/Edit/Bash validators when they detect PR-loop `state.md` modification attempts.
- gates_or_invariants: Reinforces the invariant that PR-loop state transitions are hook-owned. It supports blocking in `hooks/loop-write-validator.sh:76-80`, `hooks/loop-edit-validator.sh:59-63`, and `hooks/loop-bash-validator.sh:407-415`.
- dependencies_and_callers: Loaded by `load_and_render_safe "$TEMPLATE_DIR" "block/pr-loop-state-modification.md"` in `hooks/lib/loop-common.sh:889`. It depends only on the template loader fallback path and has no placeholders.
- edge_cases_or_failure_modes: If missing, callers fall back to inline text in `hooks/lib/loop-common.sh:885-887`; behavior still blocks, but the user-facing explanation becomes less complete.
- validation_or_tests: Validator tests are not in this assigned file, but call-site coverage is implied by stop-hook and PR-hook suites that exercise blocked state handling. Direct inspection confirms the template is short and static.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-124 `file` `prompt-template/pr-loop/round-0-header.md`
- cursor: `[_]`
- core_role: This template starts the initial PR-loop prompt shown to the agent in round 0. It frames the loop as monitoring remote review bot feedback and injects PR metadata before fetched comments.
- algorithmic_behavior: It directs “Read and execute below with ultrathink,” declares “PR Review Loop (Round 0),” shows `{{PR_NUMBER}}`, `{{START_BRANCH}}`, and `{{ACTIVE_BOTS_DISPLAY}}`, then introduces the fetched PR comments section (`prompt-template/pr-loop/round-0-header.md:1-15`).
- inputs_outputs_state: Inputs are render variables built in `scripts/setup-pr-loop.sh:651-658`. Output is written to `.humanize/pr-loop/<timestamp>/round-0-prompt.md` before appending `round-0-pr-comment.md` (`scripts/setup-pr-loop.sh:677-684`).
- gates_or_invariants: The header establishes that round 0 uses fetched PR comments as the work basis. It does not itself enforce transitions, but it is the first prompt surface created after `state.md` and `goal-tracker.md` are initialized in `scripts/setup-pr-loop.sh:535-555` and `:561-633`.
- dependencies_and_callers: Called via `load_and_render_safe "$TEMPLATE_DIR" "pr-loop/round-0-header.md"` at `scripts/setup-pr-loop.sh:678`. It depends on `hooks/lib/template-loader.sh:58-132`, whose single-pass rendering prevents variable-value placeholder reinjection.
- edge_cases_or_failure_modes: If missing, `setup-pr-loop.sh` uses the fallback header at `:660-675`. If render variables are absent, unresolved placeholders remain because the template loader deliberately preserves missing placeholders (`hooks/lib/template-loader.sh:115-122`).
- validation_or_tests: Round-0 prompt generation is exercised indirectly through PR-loop setup/system tests; direct call-site inspection confirms this template is part of the initial prompt assembly path.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: all 5 assigned item evidence headers are present exactly once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`