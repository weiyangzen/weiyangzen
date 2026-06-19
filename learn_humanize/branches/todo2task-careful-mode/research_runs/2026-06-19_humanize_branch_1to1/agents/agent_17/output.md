# agent_17 todo2task-careful-mode 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `7d9dd4fbb5c376ae0a72b7caf81c50909ff14c37`

## Item Evidence

### TODO2TASK_CAREFUL_MODE-HZ-017 `file` `agents/draft-relevance-checker.md`
- cursor: `[_]`
- core_role: Repository-relevance policy agent used by `gen-plan` before converting a draft into an implementation plan. Its frontmatter defines the agent name, purpose, model, and allowed read-only discovery tools at `agents/draft-relevance-checker.md:1-6`.
- algorithmic_behavior: The prompt instructs the agent to quickly inspect repo documentation and structure, compare the draft semantically against repository concepts/files/features, then emit one of two machine-readable verdict prefixes: `RELEVANT:` or `NOT_RELEVANT:` at `agents/draft-relevance-checker.md:14-29`.
- inputs_outputs_state: Input is draft document content supplied by the caller; repository context is gathered through `Read`, `Glob`, and `Grep`. Output is a single verdict line with a short explanation. It does not mutate state or files.
- gates_or_invariants: The policy is intentionally lenient: informal drafts and multilingual/rough ideas are acceptable, semantic relevance matters more than syntax, and uncertainty should resolve toward relevant at `agents/draft-relevance-checker.md:31-36`. The output prefix is the downstream gate.
- dependencies_and_callers: `commands/gen-plan.md` invokes `humanize:draft-relevance-checker` during Phase 2 after IO validation and before deeper plan generation, and stops the command if the verdict is `NOT_RELEVANT` at `commands/gen-plan.md:50-72`.
- edge_cases_or_failure_modes: False negatives are mitigated by the leniency rule. The prompt may still misclassify drafts that are abstract, use unfamiliar terminology, or reference future files not yet present. Since tools are read-only, it cannot verify behavior by executing code.
- validation_or_tests: `tests/test-gen-plan.sh` validates the agent file exists, has name `draft-relevance-checker`, uses model `haiku`, declares tools, follows naming/frontmatter conventions, uses a valid model, and avoids emoji/CJK content at `tests/test-gen-plan.sh:110-156`, `tests/test-gen-plan.sh:241-244`, `tests/test-gen-plan.sh:289-296`, and `tests/test-gen-plan.sh:391-422`.
- skip_candidate: `no`

### TODO2TASK_CAREFUL_MODE-HZ-047 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role: Executable specification for a narrow RLCR hook exception: certain generated todos/summary files may bypass the normal “wrong round/todos blocked” protections only when they are exact allowlisted filenames in the active loop directory.
- algorithmic_behavior: Builds a temporary git repo and active loop state, sources `hooks/lib/loop-common.sh`, then tests `is_allowlisted_file` directly and through Read/Write/Edit/Bash hook validators. Setup creates `state.md` with `current_round: 5`, plan metadata, and active loop path at `tests/test-allowlist-validators.sh:29-64`.
- inputs_outputs_state: Inputs are synthetic hook JSON payloads for `Read`, `Write`, `Edit`, and `Bash`, plus `CLAUDE_PROJECT_DIR` pointing at the temp repo. Outputs are PASS/FAIL lines and process exit status equal to `TESTS_FAILED` at `tests/test-allowlist-validators.sh:385-393`. State is limited to temp git/loop files cleaned by trap.
- gates_or_invariants: The allowlist is exact path and exact basename only: `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` under the active loop directory. Production implementation returns success only on exact `$active_loop_dir/$allowed` matches at `hooks/lib/loop-common.sh:426-447`.
- dependencies_and_callers: Depends on `hooks/lib/loop-common.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-read-validator.sh`, and `hooks/loop-bash-validator.sh`. The Read/Write/Edit validators call `is_allowlisted_file` when handling round todos or non-current summaries at `hooks/loop-read-validator.sh:55-62` and `hooks/loop-read-validator.sh:138-150`, `hooks/loop-write-validator.sh:55-62` and `hooks/loop-write-validator.sh:228-245`, and `hooks/loop-edit-validator.sh:38-45` and `hooks/loop-edit-validator.sh:155-179`.
- edge_cases_or_failure_modes: Tests explicitly reject same filenames in wrong directories, non-allowlisted future rounds, old loop directories, generic relative filenames, and same loop basename under a different root. Bash path restriction requires the full active loop path for `round-[12]-todos.md` at `hooks/loop-bash-validator.sh:381-393`.
- validation_or_tests: Direct tests cover allowlisted files and wrong-directory rejection at `tests/test-allowlist-validators.sh:66-127`; Write tests cover allowed `round-1-todos.md` and historical `round-0-summary.md`, plus blocked future todos/summary at `tests/test-allowlist-validators.sh:128-185`; Edit and Read mirrors are at `tests/test-allowlist-validators.sh:187-284`; Bash bypass tests are at `tests/test-allowlist-validators.sh:286-383`.
- skip_candidate: `no`

### TODO2TASK_CAREFUL_MODE-HZ-077 `file` `prompt-template/block/finalize-state-file-modification.md`
- cursor: `[_]`
- core_role: Block-message template used when an agent attempts to modify `finalize-state.md`, the loop-owned state marker for the Finalize Phase.
- algorithmic_behavior: Presents a deterministic refusal: `finalize-state.md` is managed by the loop system, and the agent should instead run the code-simplifier agent, commit changes, and write `finalize-summary.md` at `prompt-template/block/finalize-state-file-modification.md:1-8`.
- inputs_outputs_state: Input comes indirectly from hook rendering through the template loader; output is a human-facing block reason. No state transition is performed by the template itself.
- gates_or_invariants: The invariant is that `finalize-state.md` is not user/agent-editable. Production helpers expose this through `finalize_state_file_blocked_message`, with an inline fallback if the template cannot load at `hooks/lib/loop-common.sh:478-485`.
- dependencies_and_callers: Called by Write/Edit validators when a path matches `finalize-state.md` and by Bash validator when command patterns modify or move/copy from `finalize-state.md`: `hooks/loop-write-validator.sh:148-155`, `hooks/loop-edit-validator.sh:113-120`, and `hooks/loop-bash-validator.sh:139-146`, `hooks/loop-bash-validator.sh:286-327`.
- edge_cases_or_failure_modes: `finalize-state.md` must be checked before generic `state.md` because the generic `state.md` regex also matches `finalize-state.md`; both Write and Edit validators call this out at `hooks/loop-write-validator.sh:148-152` and `hooks/loop-edit-validator.sh:113-117`.
- validation_or_tests: Finalize-phase tests verify Write/Edit/Bash blocking, including Bash redirection and mv/cp source protection, at `tests/test-finalize-phase.sh:357-414`.
- skip_candidate: `no`

### TODO2TASK_CAREFUL_MODE-HZ-107 `file` `prompt-template/claude/finalize-phase-prompt.md`
- cursor: `[_]`
- core_role: Finalize Phase instruction template delivered to Claude after Codex review has passed and before the RLCR loop is allowed to complete.
- algorithmic_behavior: Converts a successful review state into a constrained cleanup/refactor task: use `code-simplifier:code-simplifier`, keep functionality equivalent, preserve tests, focus on recent branch changes, complete tasks, commit, and write `finalize-summary.md` at `prompt-template/claude/finalize-phase-prompt.md:1-51`.
- inputs_outputs_state: Inputs are template variables `{{BASE_BRANCH}}`, `{{START_BRANCH}}`, `{{PLAN_FILE}}`, `{{GOAL_TRACKER_FILE}}`, and `{{FINALIZE_SUMMARY_FILE}}`. Output is a rendered block response returned to Claude. The state transition is performed by the stop hook, which renames `state.md` to `finalize-state.md` before rendering at `hooks/loop-codex-stop-hook.sh:1041-1050`.
- gates_or_invariants: Non-negotiable constraints require no functionality change, no existing test failures, no new bugs, and only functionality-equivalent cleanup at `prompt-template/claude/finalize-phase-prompt.md:16-24`. Before exit, the agent must complete tasks, commit, and write the finalize summary at `prompt-template/claude/finalize-phase-prompt.md:41-51`.
- dependencies_and_callers: `enter_finalize_phase` loads this template on the non-skipped-review path with the branch/plan/summary variables at `hooks/loop-codex-stop-hook.sh:1088-1113`, returns it as a JSON block reason at `hooks/loop-codex-stop-hook.sh:1116-1124`, and is reached when code review passes with no issues at `hooks/loop-codex-stop-hook.sh:1028-1038`.
- edge_cases_or_failure_modes: If review is skipped, a sibling skipped prompt is used instead, not this template, at `hooks/loop-codex-stop-hook.sh:1053-1086`. Once already in Finalize Phase, the stop hook skips further Codex review and completes the loop by renaming `finalize-state.md` to `complete-state.md` after checks pass at `hooks/loop-codex-stop-hook.sh:738-750`.
- validation_or_tests: `tests/test-finalize-phase.sh` checks that COMPLETE triggers Finalize Phase, creates `finalize-state.md`, blocks with a finalize prompt mentioning code-simplifier, and later completes by renaming to `complete-state.md` at `tests/test-finalize-phase.sh:524-539` and `tests/test-finalize-phase.sh:489-492`.
- skip_candidate: `no`

### TODO2TASK_CAREFUL_MODE-HZ-137 `file` `tests/robustness/test-plan-file-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable specification for plan-file validation in `scripts/setup-rlcr-loop.sh`, especially content sufficiency, size/path edge cases, line-ending tolerance, and disappearance/missing-file behavior.
- algorithmic_behavior: Creates a temp repo, mocks `codex`, invokes production `setup-rlcr-loop.sh` through `test_plan_validation`, classifies known validation errors as rejection, and treats setup activation, loop state creation, codex-missing, or gitignore-required output as validation success at `tests/robustness/test-plan-file-robustness.sh:18-106`.
- inputs_outputs_state: Inputs are generated plan files under the temp repo. Outputs are PASS/FAIL counters from `tests/test-helpers.sh`, ending with `print_test_summary` and exit status at `tests/robustness/test-plan-file-robustness.sh:551-556`. It writes only temp files and cleans them by trap.
- gates_or_invariants: Production gates include relative path only, no spaces/metacharacters, no symlink file or symlink parent traversal, parent dir exists, file exists/readable, path remains inside project, not inside submodule, correct git tracking/gitignore posture, at least 5 total lines, and at least 3 nonblank/noncomment content lines at `scripts/setup-rlcr-loop.sh:327-548`.
- dependencies_and_callers: Depends on `scripts/setup-rlcr-loop.sh`, `tests/test-helpers.sh`, git, `wc`, shell regexes, and a mock `codex` placed earlier in `PATH` at `tests/robustness/test-plan-file-robustness.sh:26-40`. The production content-line logic mirrors the local helper `count_content_lines` at `tests/robustness/test-plan-file-robustness.sh:127-167` and `scripts/setup-rlcr-loop.sh:500-543`.
- edge_cases_or_failure_modes: Positive production cases include valid plans, exactly 3 content lines, standard 5KB files, rich markdown, 1MB+ files, and mixed CRLF/LF endings at `tests/robustness/test-plan-file-robustness.sh:176-288` and `tests/robustness/test-plan-file-robustness.sh:323-364`. Negative production cases include empty files, comment-only files, and deleted/missing plan files at `tests/robustness/test-plan-file-robustness.sh:298-321` and `tests/robustness/test-plan-file-robustness.sh:525-549`.
- validation_or_tests: Some robustness probes do not invoke production setup and instead validate local read/count behavior: binary content, very long lines, special characters, whitespace-only content count, complex comments, missing-file detection, unreadable-file detection, symlink detection, directory detection, and null-byte line counting at `tests/robustness/test-plan-file-robustness.sh:366-523`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `5 Item Evidence sections; all assigned items represented once as section headings`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`