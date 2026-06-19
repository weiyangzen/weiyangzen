# agent_25 reflection-improve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `13a47fb2260667a272b448e8d3c1a521f2382590`

## Item Evidence

### REFLECTION_IMPROVE-HZ-025 `file` `agents/bitlesson-selector.md`
- cursor: `[_]`
- core_role: Agent prompt specification for selecting applicable BitLesson entries before a task or sub-task. It defines a deterministic review/planning micro-policy rather than runtime code.
- algorithmic_behavior: The prompt takes a sub-task, related paths, and `bitlesson.md` content, then filters lessons by direct relevance only. It explicitly prefers precision, permits `NONE`, and requires a two-line stable output: `LESSON_IDS` and `RATIONALE` at `agents/bitlesson-selector.md:26-39`.
- inputs_outputs_state: Inputs are the current sub-task, file paths, and project lesson content at `agents/bitlesson-selector.md:12-18`. Output is stateless text consumed by later workflow stages; there is no persistent state transition in this file.
- gates_or_invariants: The main invariant is deterministic, minimal selection: no weakly related lessons and no extra sections. The stable format is a contract for downstream parser/reviewer tooling at `agents/bitlesson-selector.md:32-41`.
- dependencies_and_callers: The prompt itself documents that runtime execution is via `scripts/bitlesson-select.sh`, routed to Codex or Claude by configured `bitlesson_model` at `agents/bitlesson-selector.md:19-24`. Related instructions require using this selector in `prompt-template/claude/agent-teams-core.md:23`, `prompt-template/claude/next-round-prompt.md:17`, and `prompt-template/claude/review-phase-prompt.md:11`.
- edge_cases_or_failure_modes: If no lesson is directly relevant, the expected output is `LESSON_IDS: NONE`; if the model emits extra sections or omits either required line, the runtime parser can reject it. The prompt does not validate that selected IDs actually exist; that is handled by downstream BitLesson delta validation.
- validation_or_tests: Runtime behavior is indirectly covered by `tests/test-bitlesson-select-routing.sh`, which mocks Codex/Claude outputs and verifies stable `LESSON_IDS` routing output for configured providers at lines `61-279`. I also ran `bash -n scripts/bitlesson-select.sh`, which passed.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-055 `file` `scripts/fetch-pr-comments.sh`
- cursor: `[_]`
- core_role: Runtime workflow script that gathers PR review context from GitHub and converts heterogeneous API responses into a single markdown prompt input for PR-loop review/fix rounds.
- algorithmic_behavior: Parses `<pr_number> <output_file>` plus `--after` and `--bots`; validates numeric PR and prerequisites `gh`/`jq`; resolves the correct base repository for fork PRs; fetches issue comments, inline review comments, and PR reviews; normalizes them into JSON objects; deduplicates, filters, sorts, and renders markdown. Key sections are argument parsing `scripts/fetch-pr-comments.sh:22-106`, repo resolution `126-162`, retry fetches `176-220`, JSON normalization `261-324`, filtering/sorting `326-343`, and markdown rendering `345-450`.
- inputs_outputs_state: Inputs are CLI args, current GitHub repo context, GitHub API responses, optional timestamp cutoff, and optional active bot list. Output is a markdown file headed with PR number, UTC fetch time, repo, human comments, bot comments, and final warning if endpoints failed at `scripts/fetch-pr-comments.sh:245-254` and `440-450`. State is limited to temp files under `mktemp -d`, cleaned by trap at `169-170`.
- gates_or_invariants: Requires nonempty numeric PR number and output path, installed `gh` and `jq`, and a resolvable current or parent repo. Fetch failure is soft after three retries: it writes an empty JSON array, increments `API_FAILURES`, and continues so partial context can still be produced at `190-205`.
- dependencies_and_callers: Called by `scripts/setup-pr-loop.sh:430-431` to create `round-0-pr-comment.md`, grouped by active bots. It depends on GitHub CLI auth/context and `jq` ISO timestamp parsing via `fromdateiso8601`.
- edge_cases_or_failure_modes: Fork PRs are handled by probing current repo then parent repo at `139-148`. Empty approval reviews are preserved as `[Review state: STATE]` at `300-315`. API rate/network failures can produce incomplete but marked output. Deduplication is by raw `.id` only at `322-324`, which could collide across GitHub resource types in rare cases. `--after` compares timestamp strings at `327-330`; ISO UTC strings sort correctly, but mixed offsets would be weaker than parsed timestamp comparison.
- validation_or_tests: Fixture tests verify all comment types, approval-only reviews, and `--after` filtering in `tests/test-pr-loop-hooks.sh:1242-1318`. Robustness tests cover empty arrays, rate limits, network errors, bot parsing, Unicode, and long bodies in `tests/robustness/test-pr-loop-api-robustness.sh:362-555`. I also ran `bash -n scripts/fetch-pr-comments.sh`, which passed.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-085 `file` `tests/test-monitor-e2e-deletion.sh`
- cursor: `[_]`
- core_role: Executable test shard for monitor deletion behavior. It is not implementation logic, but it specifies critical graceful-stop invariants for real monitor functions.
- algorithmic_behavior: Sources `tests/test-monitor-e2e-real.sh`, prints a deletion-test header, runs three delegated tests, then exits success only if `TESTS_FAILED` is zero at `tests/test-monitor-e2e-deletion.sh:4-22`.
- inputs_outputs_state: Inputs are the sourced test library and host shell environment, including availability of bash/zsh and temp filesystem. Outputs are console pass/fail summaries and process exit code. Shared state is `TESTS_PASSED` and `TESTS_FAILED` initialized by the sourced suite at `tests/test-monitor-e2e-real.sh:25-36`.
- gates_or_invariants: The shard’s invariant is that bash RLCR monitor deletion, zsh RLCR monitor deletion, and PR monitor deletion all pass before the shard returns zero. It does not run SIGINT tests; those are split into other shards.
- dependencies_and_callers: Included in the aggregate suite at `tests/run-all-tests.sh:60-80`. Delegated functions are `monitor_test_bash_deletion`, `monitor_test_zsh_deletion`, and `monitor_test_pr_deletion` from `tests/test-monitor-e2e-real.sh:56`, `233`, and `691`.
- edge_cases_or_failure_modes: The shard fails if the real monitor hangs after `.humanize` state deletion, emits zsh/bash glob errors, fails to restore terminal state, or exits nonzero. zsh-specific coverage is skipped inside the delegated function if zsh is unavailable at `tests/test-monitor-e2e-real.sh:238-240`.
- validation_or_tests: Delegated bash deletion test creates a fake RLCR session, deletes `.humanize/rlcr`, waits for monitor exit, and checks user-friendly deletion text, no glob errors, cleanup text, scroll reset source, and `EXIT_CODE:0` at `tests/test-monitor-e2e-real.sh:56-227`. PR deletion does the same for `.humanize/pr-loop` and `humanize monitor pr --once` at `691-829`. I ran `bash -n tests/test-monitor-e2e-deletion.sh`, which passed.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-115 `file` `prompt-template/block/bitlesson-delta-inconsistent.md`
- cursor: `[_]`
- core_role: Stop-hook block template for invalid `## BitLesson Delta` summaries. It is a small policy surface enforcing consistency between declared BitLesson action and lesson IDs.
- algorithmic_behavior: Provides corrective instructions: `Action: none` must pair with `Lesson ID(s): NONE` or omitted IDs, while `Action: add|update` must include concrete IDs that exist in `.humanize/bitlesson.md` at `prompt-template/block/bitlesson-delta-inconsistent.md:3-7`.
- inputs_outputs_state: Inputs are rendered context from callers, though this template itself has no placeholders. Output is a markdown reason shown in a block decision. It does not mutate state.
- gates_or_invariants: Encodes the invariant that action and lesson IDs cannot diverge. This supports loop exit gating by preventing a summary from claiming no lesson update while naming IDs, or claiming add/update without valid persisted lessons.
- dependencies_and_callers: Loaded through `load_and_render_safe` by `scripts/bitlesson-validate-delta.sh` for multiple failure classes: inconsistent `none` IDs at `158-167`, missing IDs for add/update at `184-194`, missing BitLesson file at `197-207`, empty concrete IDs at `240-249`, invalid ID format at `252-264`, and missing IDs in the KB at `267-281`.
- edge_cases_or_failure_modes: Because it is generic, caller-specific fallback messages can carry more precise variables, but the real template does not render `ACTION`, invalid IDs, or missing IDs. This is useful as stable guidance but less diagnostic than some fallbacks.
- validation_or_tests: `scripts/bitlesson-validate-delta.sh` has syntax validation by `bash -n`, which I ran successfully. I found no direct template-rendering test for this exact file; coverage is indirect through validator paths that load this block.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-145 `file` `prompt-template/block/unpushed-commits.md`
- cursor: `[_]`
- core_role: Stop-hook block template for the push-every-round gate. It prevents loop exit while local commits have not been pushed to the remote review branch.
- algorithmic_behavior: Renders the number of unpushed commits and current branch, explains that `--push-every-round` requires pushing before exit, and gives the exact `git push origin {{CURRENT_BRANCH}}` command at `prompt-template/block/unpushed-commits.md:1-12`.
- inputs_outputs_state: Inputs are `AHEAD_COUNT` and `CURRENT_BRANCH`. Output is markdown returned as the hook block reason. It does not change repository state; it instructs the user/agent to push.
- gates_or_invariants: Enforces that review bots can see the latest fixes before the loop exits. The invariant is only active when push-every-round mode is enabled.
- dependencies_and_callers: Used by PR stop hook after ahead-count detection at `hooks/pr-loop-stop-hook.sh:350-360`, and by Codex loop stop hook after parsing `git status -sb` ahead output at `hooks/loop-codex-stop-hook.sh:678-703`. Both wrap it in JSON block decisions.
- edge_cases_or_failure_modes: If branch or remote detection is degraded, callers may conservatively set `AHEAD_COUNT=1`, causing a safe block. The template assumes `CURRENT_BRANCH` is pushable to `origin`; detached or unusual branch setups rely on caller detection and fallback behavior.
- validation_or_tests: Template rendering is directly tested in `tests/test-templates-comprehensive.sh:517-528`, checking title, count, and branch substitution. I also inspected `hooks/lib/template-loader.sh:50-131`, which performs single-pass `{{VAR}}` substitution to avoid placeholder injection.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-175 `file` `prompt-template/pr-loop/round-0-task-has-comments.md`
- cursor: `[_]`
- core_role: Round-zero PR-loop task template used when fetched PR comments already exist. It tells the agent how to transform review feedback into code fixes, commits, pushes, bot re-review request, and resolution summary.
- algorithmic_behavior: The template prioritizes human comments before bot comments, requires reading relevant files, making fixes, adding tests when needed, committing, pushing, commenting on the PR with `{{BOT_MENTION_STRING}}`, and writing a resolution summary to `@{{RESOLVE_PATH}}` at `prompt-template/pr-loop/round-0-task-has-comments.md:4-27`.
- inputs_outputs_state: Inputs are rendered `{{PR_NUMBER}}`, `{{BOT_MENTION_STRING}}`, and `{{RESOLVE_PATH}}`. Outputs are instructions embedded in `round-0-prompt.md`; expected external artifacts are code/test changes, a commit, a push, a PR comment, and a resolution summary file.
- gates_or_invariants: Important rules forbid modifying `.humanize/pr-loop/` state files, require pushing, require correct bot mention format, and require thorough handling of reviewer concerns at `prompt-template/pr-loop/round-0-task-has-comments.md:30-35`. It also documents the stop-hook polling and validation loop at `39-43`.
- dependencies_and_callers: Loaded by `scripts/setup-pr-loop.sh:847` after initial comments are fetched by `scripts/fetch-pr-comments.sh` at `430-431`; the rendered content is appended to `round-0-prompt.md` at `scripts/setup-pr-loop.sh:850-851`.
- edge_cases_or_failure_modes: If `BOT_MENTION_STRING` or `RESOLVE_PATH` are wrong, the agent may fail to trigger review or write the summary to the expected path. The instruction to modify code and push is unsuitable for read-only/research modes, but in normal PR-loop execution it is the intended behavior.
- validation_or_tests: I found call-site coverage through setup script rendering, but no direct test specifically asserting this template’s substituted content. The broader PR-loop tests cover comment fetch and stop-hook behavior around the same workflow.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6 item headings present, one per assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`