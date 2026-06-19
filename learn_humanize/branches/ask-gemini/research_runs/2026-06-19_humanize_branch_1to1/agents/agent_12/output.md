# agent_12 ask-gemini 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 8
- source_commit: `883e3f5bb8106cea4153d9f5e469b2fa7a8d6849`

## Item Evidence

### ASK_GEMINI-HZ-012 `file` `README.md`
- cursor: `[_]`
- core_role: Top-level behavior documentation for the Humanize plugin and RLCR workflow. It defines RLCR as "Ralph-Loop with Codex Review" and frames the core algorithm as iterative implementation plus independent review, not one-shot generation (`README.md:9-27`).
- algorithmic_behavior: Documents the main workflow: generate a plan, optionally refine annotated plan comments, run `/humanize:start-rlcr-loop`, optionally ask Gemini, and monitor loop/skill/codex/gemini activity (`README.md:41-70`). It describes a two-phase loop where Claude implements and Codex reviews, with issues feeding back until acceptance criteria are met (`README.md:26`).
- inputs_outputs_state: Inputs are user draft plans, annotated plan files, target plan path, and optional Gemini queries (`README.md:43-60`). Outputs are plan files, refined plans, RLCR loop artifacts, review feedback, and monitor surfaces. State is conceptual here; the file points to commands that create `.humanize` state but does not itself implement state changes.
- gates_or_invariants: Core invariant is "One Build + One Review": Claude implements and Codex independently reviews (`README.md:15-17`). Another gate is human architectural understanding before the loop starts, referenced as "Begin with the End in Mind" (`README.md:18`).
- dependencies_and_callers: Requires Codex CLI for review (`README.md:39`). Mentions Gemini CLI for `/humanize:ask-gemini` (`README.md:58-60`). Links deeper behavior/config docs under `docs/usage.md`, installation docs, and the workflow image (`README.md:22-24`, `README.md:78-85`).
- edge_cases_or_failure_modes: README-level only. It hints at prerequisite failure modes: missing Codex CLI prevents review workflow; missing Gemini CLI prevents Gemini research command. It does not document low-level recovery for malformed state or hook failures.
- validation_or_tests: No direct executable validation in this file. It is validated indirectly by command, hook, and integration suites listed in `tests/run-all-tests.sh`, especially RLCR, PR loop, configuration, and monitor suites (`tests/run-all-tests.sh:59-123`).
- skip_candidate: `no`

### ASK_GEMINI-HZ-042 `file` `hooks/hooks.json`
- cursor: `[_]`
- core_role: Claude Code hook routing table for the RLCR and PR loop state machines. It binds hook lifecycle events to validator and stop-hook scripts (`hooks/hooks.json:1-3`).
- algorithmic_behavior: `UserPromptSubmit` runs `loop-plan-file-validator.sh` before accepting prompts (`hooks/hooks.json:4-13`). `PreToolUse` routes `Write`, `Edit`, `Read`, and `Bash` through path/command validators (`hooks/hooks.json:14-51`). `PostToolUse` runs a Bash post-hook for Bash commands (`hooks/hooks.json:52-62`). `Stop` runs both RLCR and PR loop stop hooks with 7200-second timeouts (`hooks/hooks.json:63-78`).
- inputs_outputs_state: Inputs are Claude hook event payloads for user prompts and tool invocations. Outputs are hook command decisions, including allow/block behavior and JSON decisions from stop hooks. State transitions are delegated to scripts; this config decides which script sees each event.
- gates_or_invariants: The invariant is centralized mediation: writes, edits, reads, bash commands, and stop attempts are not trusted directly during active loops. Stop hooks must have enough time for Codex review or PR bot polling, hence the 7200-second timeout (`hooks/hooks.json:68-74`).
- dependencies_and_callers: Depends on `${CLAUDE_PLUGIN_ROOT}` resolving to the plugin runtime root. Called by Claude Code's hook runner. Downstream scripts share `hooks/lib/loop-common.sh`, which provides active-loop discovery, strict state parsing, block message rendering, and file classifiers (`hooks/lib/loop-common.sh:245-365`, `hooks/lib/loop-common.sh:474-535`).
- edge_cases_or_failure_modes: If `${CLAUDE_PLUGIN_ROOT}` is unset or wrong, every configured hook command can fail. Both stop hooks are registered for every stop event, so each must no-op when its loop type is inactive; `pr-loop-stop-hook.sh` exits when no active PR loop exists (`hooks/pr-loop-stop-hook.sh:65-76`).
- validation_or_tests: Hook references are covered by `tests/test-template-references.sh` and multiple hook suites. The aggregate runner includes `test-plan-file-hooks.sh`, `test-pr-loop-2-hooks.sh`, `test-stop-hook-legacy-compat.sh`, `test-hook-system-robustness.sh`, and PR stop-hook tests (`tests/run-all-tests.sh:66-71`, `tests/run-all-tests.sh:89-92`, `tests/run-all-tests.sh:118-120`).
- skip_candidate: `no`

### ASK_GEMINI-HZ-072 `file` `tests/run-all-tests.sh`
- cursor: `[_]`
- core_role: Top-level executable specification and CI-style test orchestrator for Humanize's core algorithms, hooks, templates, PR loop, monitor, config, and robustness behavior.
- algorithmic_behavior: Computes default parallelism from CPU count, caps it at 8, and allows override via `HUMANIZE_TEST_JOBS` (`tests/run-all-tests.sh:19-37`). It detects `wait -n` support for Bash 4.3 plus, otherwise falls back to waiting on the oldest PID (`tests/run-all-tests.sh:39-44`, `tests/run-all-tests.sh:205-221`). It launches each suite in a background isolated output file, throttles active PIDs, waits for completion, parses pass/fail counts, sorts result lines by elapsed time, and exits nonzero if any suite fails (`tests/run-all-tests.sh:166-307`).
- inputs_outputs_state: Inputs are `HUMANIZE_TEST_JOBS`, discovered suite files under `tests/`, shell availability, `zsh` availability for zsh-only suites, and optional installed `codex`. Outputs are colored per-suite status lines, full failure logs for failed suites, aggregate pass/fail counts, and process exit code 0 or 1 (`tests/run-all-tests.sh:272-307`).
- gates_or_invariants: Invalid `HUMANIZE_TEST_JOBS` blocks immediately (`tests/run-all-tests.sh:33-37`). Missing test files are marked skipped rather than failed (`tests/run-all-tests.sh:178-181`). A suite fails if either its exit code is nonzero or its parsed `Failed:` count is above zero (`tests/run-all-tests.sh:250-263`).
- dependencies_and_callers: Depends on all named suites in `TEST_SUITES`, including the assigned `test-pr-loop-3-stophook.sh` and `robustness/test-state-transition-robustness.sh` (`tests/run-all-tests.sh:59-123`). It creates a temporary mock `codex` binary only when `codex` is not installed, satisfying tests that check command presence (`tests/run-all-tests.sh:130-145`).
- edge_cases_or_failure_modes: Output parsing depends on suites printing `Passed:` and `Failed:` lines (`tests/run-all-tests.sh:250-256`). If an exit file is missing, the suite is treated as failed by default (`tests/run-all-tests.sh:245`). zsh-specific tests are skipped if zsh is absent (`tests/run-all-tests.sh:183-187`).
- validation_or_tests: This file is itself the umbrella validation command. It was inspected only; no test execution was performed for this research task.
- skip_candidate: `no`

### ASK_GEMINI-HZ-102 `file` `tests/test-pr-loop-3-stophook.sh`
- cursor: `[_]`
- core_role: Split test runner for the slowest PR loop stop-hook integration tests. It is a focused executable specification for `hooks/pr-loop-stop-hook.sh` behavior.
- algorithmic_behavior: Sources shared test helpers and PR-loop test library, skips in GitHub Actions, initializes mock PR-loop environment, sources `tests/test-pr-loop-stophook.sh`, runs `run_stophook_tests`, prints summary, and exits with the accumulated test status (`tests/test-pr-loop-3-stophook.sh:10-30`).
- inputs_outputs_state: Inputs are `GITHUB_ACTIONS`, `tests/test-helpers.sh`, `tests/test-pr-loop-lib.sh`, and `tests/test-pr-loop-stophook.sh` (`tests/test-pr-loop-3-stophook.sh:15-26`). Outputs are the PR Loop Stop Hook Tests summary and process exit status. Temporary `.humanize/pr-loop/<timestamp>/state.md` fixtures are created by the sourced suite, not by this wrapper.
- gates_or_invariants: The CI skip is explicit because the suite contains timeout-based bot polling tests (`tests/test-pr-loop-3-stophook.sh:18-22`). Otherwise, all sourced stop-hook tests must pass before the runner exits successfully.
- dependencies_and_callers: Delegates behavior to `tests/test-pr-loop-stophook.sh`, whose test list covers force-push trigger rejection, startup case 1 trigger exemption, approval terminal state creation, unpushed commit blocking, force-push detection, missing trigger blocking, bot timeout removal, Codex +1 approval, Claude eyes timeout, dynamic `startup_case` updates, fork PR base repo resolution, and mixed bot approval (`tests/test-pr-loop-stophook.sh:1769-1780`).
- edge_cases_or_failure_modes: If `GITHUB_ACTIONS=true`, the suite reports skipped rather than exercising stop-hook behavior. If the sourced library or suite is unavailable, `set -euo pipefail` causes immediate failure. Runtime edge cases covered by the delegated suite map to `pr-loop-stop-hook.sh` gates: resolution summary required (`hooks/pr-loop-stop-hook.sh:262-277`), clean git required (`hooks/pr-loop-stop-hook.sh:283-311`), push required (`hooks/pr-loop-stop-hook.sh:313-360`), force-push clears stale trigger state (`hooks/pr-loop-stop-hook.sh:368-421`), and trigger/eyes gates precede polling (`hooks/pr-loop-stop-hook.sh:620-800`).
- validation_or_tests: This runner is invoked by the aggregate suite at `tests/run-all-tests.sh:89-92`. Its sourced test suite validates concrete PR loop state transitions such as `state.md` to `approve-state.md` when active bots are empty (`tests/test-pr-loop-stophook.sh:246-322`) and continued looping when only one of multiple bots approves (`tests/test-pr-loop-stophook.sh:1520-1763`).
- skip_candidate: `no`

### ASK_GEMINI-HZ-132 `file` `prompt-template/block/finalize-contract-access.md`
- cursor: `[_]`
- core_role: Block-message template for Finalize Phase access to historical round contract files. It defines the user-facing gate once there is no active `round-N-contract.md` (`prompt-template/block/finalize-contract-access.md:1-7`).
- algorithmic_behavior: Renders a denial message with `{{ACTION}}`, telling the agent not to read, edit, or write historical round contracts and to use `finalize-summary.md` or `goal-tracker.md` instead (`prompt-template/block/finalize-contract-access.md:3-7`).
- inputs_outputs_state: Input is template variable `ACTION`, supplied by `finalize_contract_blocked_message` (`hooks/lib/loop-common.sh:808-820`). Output is a block reason emitted to stderr by read/write/edit validators. It does not modify state; it guards state-sensitive file access.
- gates_or_invariants: In Finalize Phase, round contracts are no longer active authoritative working files. Write validator blocks contract writes in finalize (`hooks/loop-write-validator.sh:238-241`), edit validator blocks contract edits (`hooks/loop-edit-validator.sh:178-180`), and read validator blocks contract reads (`hooks/loop-read-validator.sh:203-205`).
- dependencies_and_callers: Depends on the shared template loader through `load_and_render_safe` and the active phase detection based on `finalize-state.md` from `resolve_active_state_file` (`hooks/lib/loop-common.sh:245-261`). Called only through validators that have found an active RLCR loop and parsed state strictly.
- edge_cases_or_failure_modes: If the template is missing or rendering fails, `finalize_contract_blocked_message` has an inline fallback (`hooks/lib/loop-common.sh:812-820`). If no active loop is found, validators allow normal access rather than applying this finalize gate.
- validation_or_tests: Finalize phase tests exercise contract and finalize-state protections, including read/write/edit/bash behavior around `finalize-state.md` and finalize completion (`tests/test-finalize-phase.sh` references in search results around contract and finalize-state checks).
- skip_candidate: `no`

### ASK_GEMINI-HZ-162 `file` `prompt-template/block/unpushed-commits.md`
- cursor: `[_]`
- core_role: Block-message template for the "must push before exiting" invariant. It is used when a loop requires remote-visible commits before review or stop completion.
- algorithmic_behavior: Renders the current branch and ahead count, explains that `--push-every-round` requires pushing, and provides the exact `git push origin {{CURRENT_BRANCH}}` action (`prompt-template/block/unpushed-commits.md:1-12`).
- inputs_outputs_state: Inputs are `AHEAD_COUNT` and `CURRENT_BRANCH`. Output is a stop-hook block reason. It does not change loop state; it prevents state advancement until local commits are pushed.
- gates_or_invariants: PR loop always requires push before exit; `pr-loop-stop-hook.sh` computes ahead count from `git status -sb`, upstream comparison, `origin/<branch>`, or PR head SHA, then renders this template and blocks when count is positive (`hooks/pr-loop-stop-hook.sh:313-360`). RLCR uses the same template when `push_every_round` is true (`hooks/loop-codex-stop-hook.sh:685-708`).
- dependencies_and_callers: Depends on Git commands, optional GitHub PR head lookup for missing upstream PR branches, and the shared template renderer. PR loop caller passes `AHEAD_COUNT` and `CURRENT_BRANCH` at `hooks/pr-loop-stop-hook.sh:356-357`.
- edge_cases_or_failure_modes: If PR head cannot be fetched in the no-upstream fallback path, the PR loop fails closed by assuming unpushed commits (`hooks/pr-loop-stop-hook.sh:330-344`). If branch is ahead according to `git status -sb`, the hook blocks even if worktree is otherwise clean.
- validation_or_tests: `tests/test-pr-loop-stophook.sh` has a Step 6 test that mocks `git status -sb` as `[ahead 2]` and expects an unpushed/ahead/push message (`tests/test-pr-loop-stophook.sh:452-532`). Template rendering is also covered by comprehensive template tests (`tests/test-templates-comprehensive.sh:517-527`).
- skip_candidate: `no`

### ASK_GEMINI-HZ-192 `file` `prompt-template/pr-loop/critical-requirements-no-comments.md`
- cursor: `[_]`
- core_role: PR-loop Round 0 prompt block for the startup case where there are no existing bot comments. It defines the initial no-comments handoff contract.
- algorithmic_behavior: Tells Claude that completion requires writing a resolution summary to `{{RESOLVE_PATH}}`, noting that Round 0 is awaiting initial bot reviews and that there are no issues yet, then attempting to exit so the Stop Hook can poll for bot reviews (`prompt-template/pr-loop/critical-requirements-no-comments.md:6-20`).
- inputs_outputs_state: Input is `RESOLVE_PATH`. Output is prompt text embedded by `scripts/setup-pr-loop.sh`; the corresponding file path is set as `round-0-pr-resolve.md` (`scripts/setup-pr-loop.sh:721`) and passed into template variables (`scripts/setup-pr-loop.sh:736`).
- gates_or_invariants: The block forbids commenting on the PR to trigger review in this startup case because the bots should review automatically on a new PR (`prompt-template/pr-loop/critical-requirements-no-comments.md:15-20`). Runtime enforces the summary file requirement before polling (`hooks/pr-loop-stop-hook.sh:262-277`) and treats Round 0 startup cases 1, 2, and 3 as not requiring a trigger unless new commits are detected (`hooks/pr-loop-stop-hook.sh:613-633`).
- dependencies_and_callers: Rendered by `scripts/setup-pr-loop.sh` through `load_and_render_safe` for the no-comments path (`scripts/setup-pr-loop.sh:914`). Coordinates with `prompt-template/pr-loop/round-0-task-no-comments.md`, which carries the same `RESOLVE_PATH` workflow instruction.
- edge_cases_or_failure_modes: If the agent exits without writing the resolve file, the PR stop hook blocks with "Resolution Summary Missing" (`hooks/pr-loop-stop-hook.sh:262-277`). If new commits are detected later, the stop hook overrides the no-trigger assumption and requires a fresh trigger (`hooks/pr-loop-stop-hook.sh:545-565`, `hooks/pr-loop-stop-hook.sh:620-627`).
- validation_or_tests: The PR stop-hook suite validates the Case 1 no-trigger behavior (`tests/test-pr-loop-stophook.sh:140-244`) and missing trigger behavior for Case 4 (`tests/test-pr-loop-stophook.sh:642-748`).
- skip_candidate: `no`

### ASK_GEMINI-HZ-222 `file` `tests/robustness/test-state-transition-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for RLCR state-file transitions, strict state parsing, active loop discovery, finalize/cancel handling, and edge-case round values.
- algorithmic_behavior: Creates temporary RLCR loop directories and synthetic `state.md`, `finalize-state.md`, and `cancel-state.md` files (`tests/robustness/test-state-transition-robustness.sh:30-89`). It then exercises valid round parsing, finalize detection, cancel non-activation, invalid field handling, and loop directory discovery (`tests/robustness/test-state-transition-robustness.sh:95-423`).
- inputs_outputs_state: Inputs are generated state frontmatter fields such as `current_round`, `max_iterations`, `base_branch`, and `review_started` (`tests/robustness/test-state-transition-robustness.sh:35-47`). Outputs are pass/fail records through `test-helpers.sh` and process exit status from `print_test_summary` (`tests/robustness/test-state-transition-robustness.sh:423-424`). State is local to the test temp directory.
- gates_or_invariants: Strict parser accepts valid Round 0 and max-round states (`tests/robustness/test-state-transition-robustness.sh:98-138`). It rejects nonnumeric `current_round` and missing required fields (`tests/robustness/test-state-transition-robustness.sh:259-361`). Implementation requires YAML separators, `current_round`, `max_iterations`, `review_started`, and `base_branch`, and validates numeric/boolean fields (`hooks/lib/loop-common.sh:474-528`).
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` for `parse_state_file_strict`, `get_current_round`, and `find_active_loop` (`tests/robustness/test-state-transition-robustness.sh:14-17`). The tested implementation resolves active state files in priority order `methodology-analysis-state.md`, `finalize-state.md`, then `state.md` (`hooks/lib/loop-common.sh:245-261`).
- edge_cases_or_failure_modes: Negative rounds are parsed by `get_current_round` and accepted by the numeric regex, even though they may indicate bad state (`tests/robustness/test-state-transition-robustness.sh:217-235`, `hooks/lib/loop-common.sh:512-516`). Rounds above `max_iterations` are parsed, with enforcement elsewhere (`tests/robustness/test-state-transition-robustness.sh:238-257`). Active loop discovery uses lexicographic newest-directory ordering and ignores nested misplaced state files (`tests/robustness/test-state-transition-robustness.sh:371-417`, `hooks/lib/loop-common.sh:316-330`).
- validation_or_tests: This file is a validation suite and is included in the aggregate test runner (`tests/run-all-tests.sh:120`). Related robustness coverage also appears in concurrent state, state file, session, and hook-system robustness suites listed by the aggregate runner (`tests/run-all-tests.sh:105-120`).
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `8/8 item headings present, each assigned item represented once`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`