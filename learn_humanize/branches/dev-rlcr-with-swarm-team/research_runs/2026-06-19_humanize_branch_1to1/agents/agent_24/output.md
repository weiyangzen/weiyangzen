# agent_24 dev-rlcr-with-swarm-team 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `0d5f0943ae9b1f80c5115aa946ebeb289e2cb83d`

## Item Evidence

### DEV_RLCR_WITH_SWARM_TEAM-HZ-024 `file` `hooks/hooks.json`
- cursor: `[_]`
- core_role: Static Claude hook registry for the RLCR and PR-loop control plane. It wires user prompts, tool calls, Bash post-processing, and stop events into validator/state-machine scripts (`hooks/hooks.json:2-79`).
- algorithmic_behavior: `UserPromptSubmit` runs `loop-plan-file-validator.sh` for plan/schema/branch tracking gates (`hooks/hooks.json:4-12`). `PreToolUse` dispatches by tool matcher: `Write`, `Edit`, `Read`, and `Bash` each call a dedicated validator (`hooks/hooks.json:14-50`). `PostToolUse` for `Bash` runs `loop-post-bash-hook.sh` to capture session id after setup (`hooks/hooks.json:52-60`). `Stop` runs both RLCR and PR-loop stop hooks with 7200 second timeouts (`hooks/hooks.json:63-76`).
- inputs_outputs_state: Input is Claude hook event JSON passed to the configured command through stdin. Outputs are produced by the scripts, typically allow-by-exit, block-by-exit/stderr for PreToolUse, or JSON `decision: block` for stop hooks. Persistent state is external: `.humanize/rlcr/*/state.md`, `finalize-state.md`, summaries, prompts, review results, and PR-loop state files.
- gates_or_invariants: The registry enforces a layered gate sequence: prompt-time plan validity, pre-tool file/action protection, post-Bash session binding, then stop-time completion review. Tool matchers prevent validators from running on unrelated tool types. Stop hooks must self-filter inactive loops because both RLCR and PR stop hooks are always configured.
- dependencies_and_callers: Depends on Claude Code hook semantics, `CLAUDE_PLUGIN_ROOT`, and the listed scripts. Those scripts share `hooks/lib/loop-common.sh`, including JSON validation (`loop-common.sh:76-113`), active-loop discovery (`loop-common.sh:215-291`), strict state parsing (`loop-common.sh:386-449`), and template fallback rendering through `template-loader.sh`.
- edge_cases_or_failure_modes: If `CLAUDE_PLUGIN_ROOT` is unset or wrong, every command path is invalid. Because Stop has no matcher, unrelated stop events rely on each stop hook detecting “no active loop” and exiting. Hook ordering matters: session id binding in PostToolUse must happen before team/secondary sessions are affected by RLCR filters.
- validation_or_tests: Related coverage includes plan-file validation tests, hook-input robustness, hook-system robustness, finalize-phase validator tests, PR-loop stop-hook tests, and the assigned session/template tests. The registry itself is declarative, so behavior is validated through the referenced scripts rather than this JSON file alone.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-054 `file` `tests/test-error-scenarios.sh`
- cursor: `[_]`
- core_role: Executable error-path specification for `hooks/lib/template-loader.sh`, which is used by RLCR validators and stop hooks to render block prompts without crashing when templates are missing or malformed (`tests/test-error-scenarios.sh:1-15`).
- algorithmic_behavior: Initializes template path through `get_template_dir`, tracks pass/fail counters, then asserts loader functions return safe results across failure cases (`tests/test-error-scenarios.sh:15-35`). It checks missing file, missing directory, missing `load_and_render`, empty render input, special characters, strict-mode survivability, safe fallback behavior, directory validation, empty placeholders, and unclosed placeholders (`tests/test-error-scenarios.sh:42-206`).
- inputs_outputs_state: Inputs are the real `prompt-template` tree, deliberately invalid template paths, synthetic template strings, and variable assignments. Outputs are colored PASS/FAIL lines, `TESTS_PASSED`/`TESTS_FAILED`, and process exit 0 only when all assertions pass (`tests/test-error-scenarios.sh:208-226`). It does not persist repository state.
- gates_or_invariants: Missing templates must produce empty output and exit 0 for `load_template`/`load_and_render` (`tests/test-error-scenarios.sh:42-78`). `load_and_render_safe` must use fallback content and render variables inside fallback (`tests/test-error-scenarios.sh:133-158`). Invalid template directories must be rejected by `validate_template_dir` (`tests/test-error-scenarios.sh:160-180`). Malformed placeholders must remain literal (`tests/test-error-scenarios.sh:182-206`).
- dependencies_and_callers: Directly sources `hooks/lib/template-loader.sh`. The tested functions are implemented at `template-loader.sh:24-31`, `template-loader.sh:36-48`, `template-loader.sh:58-132`, `template-loader.sh:136-147`, `template-loader.sh:170-203`, and `template-loader.sh:208-222`. Runtime dependencies include Bash, `awk`, and standard shell utilities.
- edge_cases_or_failure_modes: The script intentionally avoids top-level `set -e` (`tests/test-error-scenarios.sh:9`) so failed assertions can accumulate. Test 6 embeds a strict `set -euo pipefail` subshell to ensure missing templates do not abort strict-mode callers (`tests/test-error-scenarios.sh:108-131`). It covers regex-sensitive variable values but not very large templates or concurrent rendering; those appear in separate robustness/stress tests.
- validation_or_tests: This file is itself the validation artifact. It verifies the template loader’s graceful degradation contract, which is important because validators call `load_and_render_safe` for blocking messages throughout `loop-common.sh`, `loop-bash-validator.sh`, and `loop-codex-stop-hook.sh`.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-084 `file` `prompt-template/block/git-not-clean-untracked.md`
- cursor: `[_]`
- core_role: Static markdown note appended to the stop-hook “git not clean” block when non-`.humanize` untracked files exist. It guides the agent to classify untracked artifacts into `.gitignore` rather than blindly committing them (`prompt-template/block/git-not-clean-untracked.md:2-10`).
- algorithmic_behavior: The template has no variables. `loop-codex-stop-hook.sh` computes untracked files from cached `git status --porcelain`, separates `.humanize*` from other untracked entries, loads this template for the latter, and appends it to `SPECIAL_NOTES` (`loop-codex-stop-hook.sh:549-568`). That note is then rendered into the broader `block/git-not-clean.md` response (`loop-codex-stop-hook.sh:572-595`).
- inputs_outputs_state: Input is the presence of untracked non-`.humanize` paths in git status. Output is markdown text inside the stop hook’s JSON block reason. It does not change files or loop state directly.
- gates_or_invariants: The actual gate is the stop hook’s clean-repository invariant: any staged, unstaged, or untracked status sets `GIT_ISSUES="uncommitted changes"` and blocks exit before Codex review or completion (`loop-codex-stop-hook.sh:545-596`). This template only refines the explanation for untracked-file cases.
- dependencies_and_callers: Called with `load_template "$TEMPLATE_DIR" "block/git-not-clean-untracked.md"` from `loop-codex-stop-hook.sh:564`. It depends on `template-loader.sh` path resolution and the stop hook’s git status cache.
- edge_cases_or_failure_modes: If the template is missing, the stop hook falls back to a generic “Review untracked files” note (`loop-codex-stop-hook.sh:565-567`). The template lists categories of likely artifacts but does not enumerate actual filenames; actual dirty status comes from the outer git-clean block.
- validation_or_tests: Covered indirectly by template existence/reference tests and by the stop hook’s git-clean behavior. The assigned `tests/test-error-scenarios.sh` confirms missing templates do not crash the loader path used here.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-114 `file` `prompt-template/claude/goal-tracker-update-request.md`
- cursor: `[_]`
- core_role: Static prompt fragment that defines the sanctioned channel for Claude to request goal-tracker changes after Round 0, where direct goal-tracker edits are blocked (`prompt-template/claude/goal-tracker-update-request.md:2-16`).
- algorithmic_behavior: The fragment instructs Claude to include a “Goal Tracker Update Request” section in its summary when tracker changes are needed, with requested changes and justification (`prompt-template/claude/goal-tracker-update-request.md:2-14`). The RLCR stop hook appends this fragment to next-round prompts after Codex finds implementation-phase issues (`loop-codex-stop-hook.sh:1623-1628`).
- inputs_outputs_state: No template variables. Output is markdown appended to `round-N-prompt.md`. It indirectly affects later state because Claude’s summary can carry requested tracker updates, and Codex review prompts include a separate goal-tracker update section instructing Codex to apply justified requests (`loop-codex-stop-hook.sh:793-797`).
- gates_or_invariants: Direct goal-tracker writes/edits after Round 0 are blocked by validators (`loop-write-validator.sh:190-198`, `loop-edit-validator.sh:141-148`), and Bash modifications are blocked through shared messaging (`loop-common.sh:1217-1229`). This template preserves the invariant by routing changes through summary evidence and Codex review rather than direct mutation.
- dependencies_and_callers: Loaded by `load_template` from `loop-codex-stop-hook.sh:1624`; if absent, the stop hook appends a generic fallback instruction (`loop-codex-stop-hook.sh:1625-1627`). It coordinates with `prompt-template/codex/goal-tracker-update-section.md`, the summary file, and `goal-tracker.md`.
- edge_cases_or_failure_modes: Because it is loaded, not rendered, placeholder-like example text remains literal. It is appended in the normal next-round prompt path, not in `continue_review_loop_with_issues`, so review-phase fix prompts do not necessarily receive this exact fragment.
- validation_or_tests: Related coverage should come from goal-tracker robustness and template-reference tests. The assigned template error tests validate that missing prompt fragments have safe fallbacks in the loader path.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-144 `file` `tests/robustness/test-session-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for `find_active_loop`, the active RLCR session resolver used by validators and stop hooks to decide whether a loop is active and which `.humanize/rlcr/<session>` directory owns current state (`tests/robustness/test-session-robustness.sh:1-18`).
- algorithmic_behavior: Creates temporary RLCR directory layouts, calls `find_active_loop "$TEST_DIR/rlcr"`, and asserts returned path or empty output. Positive cases cover newest active session, `finalize-state.md`, many directories, zombie-loop protection, and both `state.md` plus `finalize-state.md` (`tests/robustness/test-session-robustness.sh:33-118`). Negative/edge cases cover empty/nonexistent bases, no subdirectories, missing state files, odd names, symlinks, spaces, deep paths, rapid creation, terminal states, and mixed active/finished sessions (`tests/robustness/test-session-robustness.sh:128-317`).
- inputs_outputs_state: Inputs are filesystem marker files: `state.md`, `finalize-state.md`, `complete-state.md`, and `cancel-state.md`. Output is pass/fail reporting through `tests/test-helpers.sh`, with final exit from `print_test_summary` (`tests/robustness/test-session-robustness.sh:321-323`). State is isolated under `mktemp` and removed by trap (`tests/test-helpers.sh:84-89`).
- gates_or_invariants: No-filter active-loop discovery must check only the single newest immediate child directory and return it only if `state.md` or `finalize-state.md` exists (`loop-common.sh:215-257`). Older stale active files must not revive a loop when the newest directory lacks active state or is terminal (`tests/robustness/test-session-robustness.sh:89-103`, `287-302`). Deep descendants are ignored (`tests/robustness/test-session-robustness.sh:224-238`). Performance for 15 sessions must stay under 1000 ms (`tests/robustness/test-session-robustness.sh:63-87`).
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` and `tests/test-helpers.sh` (`tests/robustness/test-session-robustness.sh:14-19`). The resolver depends on `resolve_active_state_file` preferring `finalize-state.md` over `state.md` (`loop-common.sh:176-190`) and on reverse lexicographic sorting of immediate directories (`loop-common.sh:242-256`).
- edge_cases_or_failure_modes: Symlink test only requires a nonempty result rather than a precise target (`tests/robustness/test-session-robustness.sh:194-208`). Test 18 is labeled Unicode but creates `session-test`, so it does not actually exercise Unicode path bytes (`tests/robustness/test-session-robustness.sh:304-316`). The nanosecond timing check uses `date +%s%N`, which may be platform-sensitive outside GNU date environments (`tests/robustness/test-session-robustness.sh:74-83`).
- validation_or_tests: This file is the direct validation. Related tests extend coverage for session-id filtering, terminal newest-session stale-revival blocking, and finalize-state transitions in other robustness/finalize test scripts.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `5/5 item evidence sections present; each assigned header appears once`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`