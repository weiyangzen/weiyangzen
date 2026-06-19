# agent_17 enhance-rlcr-with-review-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `dd6c37c45c4836773497f878b8925057e9f5318c`

## Item Evidence

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-017 `file` `agents/draft-relevance-checker.md`
- cursor: `[_]`
- core_role: Agent prompt/policy for the `gen-plan` relevance gate. It defines a lightweight repository relevance classifier used before draft analysis and plan generation. Frontmatter declares `name: draft-relevance-checker`, `model: haiku`, and tools `Read, Glob, Grep` at `agents/draft-relevance-checker.md:1`.
- algorithmic_behavior: The agent first explores repo context by checking README/CLAUDE/docs, structure, technologies, and purpose at `agents/draft-relevance-checker.md:16`. It then compares the draft against repo concepts, technologies, components, paths, functions, and usage/modification intent at `agents/draft-relevance-checker.md:21`. It emits exactly `RELEVANT: <brief explanation>` or `NOT_RELEVANT: <brief explanation>` at `agents/draft-relevance-checker.md:27`.
- inputs_outputs_state: Input is draft content supplied by the caller plus read-only repo context gathered through `Read`, `Glob`, and `Grep`. Output is a single verdict string consumed by `commands/gen-plan.md`: `NOT_RELEVANT` stops the command, while `RELEVANT` continues to draft analysis at `commands/gen-plan.md:50`. It mutates no repository or loop state.
- gates_or_invariants: The prompt intentionally uses a lenient semantic gate: informal, multilingual, or rough drafts are acceptable, semantic relevance matters over syntactic similarity, and doubt should resolve to relevant at `agents/draft-relevance-checker.md:31`.
- dependencies_and_callers: Called by the `gen-plan` command’s Phase 2 via Task as `humanize:draft-relevance-checker`, with haiku model and prompt instructions to return only the two verdict forms at `commands/gen-plan.md:56`.
- edge_cases_or_failure_modes: False positives are preferred by policy because “if in doubt” becomes relevant. False negatives should be limited to drafts with no plausible repo connection. The restricted tool set prevents writes and shell execution but also limits deeper dynamic inspection.
- validation_or_tests: `tests/test-gen-plan.sh` validates the agent file exists, has the expected name, uses `haiku`, declares tools, has required frontmatter, has a valid model, and contains no emoji/CJK content at `tests/test-gen-plan.sh:111`, `tests/test-gen-plan.sh:123`, `tests/test-gen-plan.sh:137`, `tests/test-gen-plan.sh:151`, `tests/test-gen-plan.sh:290`, `tests/test-gen-plan.sh:391`, and `tests/test-gen-plan.sh:417`.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-047 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role: Executable specification for RLCR hook allowlist behavior. It defines which protected round todo/summary files may bypass normal validator blocking during loop operation.
- algorithmic_behavior: The test creates a temporary git repo and active RLCR loop state with `current_round: 5`, `max_iterations: 42`, `plan_file`, branches, and `review_started: false` at `tests/test-allowlist-validators.sh:29`. It then verifies direct helper behavior and Read/Write/Edit/Bash validator outcomes across allowlisted and blocked paths.
- inputs_outputs_state: Inputs are synthetic hook JSON payloads for `Read`, `Write`, `Edit`, and `Bash`, plus `CLAUDE_PROJECT_DIR` pointing at the temp repo at `tests/test-allowlist-validators.sh:132`. Output is PASS/FAIL counters and process exit equal to `TESTS_FAILED` at `tests/test-allowlist-validators.sh:385`.
- gates_or_invariants: The allowlist is exact and active-loop-relative. `is_allowlisted_file` permits only `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` under the active loop directory at `hooks/lib/loop-common.sh:417`. Tests 1-7 assert those exact filenames and wrong-directory rejection at `tests/test-allowlist-validators.sh:66`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at `tests/test-allowlist-validators.sh:17`. It exercises `loop-write-validator.sh`, `loop-edit-validator.sh`, `loop-read-validator.sh`, and `loop-bash-validator.sh`. Write allows allowlisted todos before blocking at `hooks/loop-write-validator.sh:55`; Edit does the same at `hooks/loop-edit-validator.sh:38`; Read does the same at `hooks/loop-read-validator.sh:55`.
- edge_cases_or_failure_modes: Bash is stricter than direct file validators: it only allows `round-[12]-todos.md` when the command contains the full active loop path, preventing basename-only, old-loop, wrong-root, and same-basename bypasses at `hooks/loop-bash-validator.sh:385`. The test covers wrong directory, generic relative filename, old loop directory, and same basename under `/tmp` at `tests/test-allowlist-validators.sh:316`, `tests/test-allowlist-validators.sh:342`, `tests/test-allowlist-validators.sh:355`, and `tests/test-allowlist-validators.sh:370`. It does not cover symlinks, case variants, or quoted shell paths.
- validation_or_tests: Tests 8-11 assert Write exit `0` for allowlisted files and exit `2` for blocked round files at `tests/test-allowlist-validators.sh:135`. Tests 12-14 cover Edit at `tests/test-allowlist-validators.sh:187`; tests 15-18 cover Read at `tests/test-allowlist-validators.sh:230`; tests 19-25 cover Bash path-restricted allowlisting at `tests/test-allowlist-validators.sh:286`.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-077 `file` `prompt-template/block/finalize-state-file-modification.md`
- cursor: `[_]`
- core_role: Blocking message template for the invariant that `finalize-state.md` is system-managed during Finalize Phase and must not be user/agent-modified.
- algorithmic_behavior: The template states that `finalize-state.md` cannot be modified and redirects the actor to the permitted Finalize Phase activities: run code-simplifier, commit changes, and write `finalize-summary.md` at `prompt-template/block/finalize-state-file-modification.md:1`.
- inputs_outputs_state: No template variables. Input is only the template load request from the hook layer. Output is markdown text rendered by `finalize_state_file_blocked_message`; the template itself changes no state.
- gates_or_invariants: Protects the `state.md -> finalize-state.md` transition after code review completion. The path helper identifies `finalize-state.md` at `hooks/lib/loop-common.sh:509`, and the block message loader uses this template via `load_and_render_safe` at `hooks/lib/loop-common.sh:466`.
- dependencies_and_callers: Called by Write validator before generic state blocking at `hooks/loop-write-validator.sh:152`, Edit validator at `hooks/loop-edit-validator.sh:117`, and Bash validator for redirects/in-place/mv/cp/shell-wrapper modification attempts at `hooks/loop-bash-validator.sh:139`, `hooks/loop-bash-validator.sh:286`, and `hooks/loop-bash-validator.sh:309`.
- edge_cases_or_failure_modes: If the template is missing or empty, `load_and_render_safe` falls back to an inline message at `hooks/lib/loop-common.sh:468`. Bash cancellation has a special authorized path checked before this block, so the template does not describe that exception.
- validation_or_tests: `tests/test-finalize-phase.sh` verifies `is_finalize_state_file_path` matches full paths and that `finalize_state_file_blocked_message` exists at `tests/test-finalize-phase.sh:253` and `tests/test-finalize-phase.sh:275`. Template reference tests scan hook references and require referenced templates to exist at `tests/test-template-references.sh:83`.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-107 `file` `prompt-template/claude/finalize-phase-prompt.md`
- cursor: `[_]`
- core_role: Finalize Phase transition prompt loaded when Codex review passes. It defines the final algorithmic stage before RLCR completion: functionality-equivalent cleanup, validation, commit, and final summary.
- algorithmic_behavior: The prompt declares review success and Finalize Phase entry at `prompt-template/claude/finalize-phase-prompt.md:1`, instructs Claude to invoke `code-simplifier:code-simplifier` with the Task tool at `prompt-template/claude/finalize-phase-prompt.md:7`, constrains work to non-functional refactoring at `prompt-template/claude/finalize-phase-prompt.md:16`, and requires TodoWrite completion, commit, and `{{FINALIZE_SUMMARY_FILE}}` output at `prompt-template/claude/finalize-phase-prompt.md:41`.
- inputs_outputs_state: Inputs are `{{BASE_BRANCH}}`, `{{START_BRANCH}}`, `{{PLAN_FILE}}`, `{{GOAL_TRACKER_FILE}}`, and `{{FINALIZE_SUMMARY_FILE}}`. Output is a rendered prompt returned as the hook block reason. The caller moves loop state from `state.md` to `finalize-state.md` before rendering at `hooks/loop-codex-stop-hook.sh:996`.
- gates_or_invariants: Entry is gated by Codex review finding no issues, then `enter_finalize_phase` renames state and emits a blocking prompt at `hooks/loop-codex-stop-hook.sh:990`. The phase invariants are no functionality change, no broken tests, no new bugs, and only functionality-equivalent cleanup at `prompt-template/claude/finalize-phase-prompt.md:18`.
- dependencies_and_callers: Loaded with `load_and_render_safe "$TEMPLATE_DIR" "claude/finalize-phase-prompt.md"` at `hooks/loop-codex-stop-hook.sh:1063`. Rendering depends on the single-pass template loader; unresolved variables remain literal if missing. The skipped-review path uses a separate template, not this one, at `hooks/loop-codex-stop-hook.sh:1008`.
- edge_cases_or_failure_modes: If this template is absent, the stop hook uses its inline fallback prompt at `hooks/loop-codex-stop-hook.sh:1043`. If any variable is omitted, placeholders persist because the loader keeps missing variables unchanged. The prompt assumes review passed; using it after skipped or failed review would misrepresent validation state.
- validation_or_tests: `tests/test-finalize-phase.sh` verifies COMPLETE triggers Finalize Phase, `state.md` is replaced by `finalize-state.md`, and the returned prompt mentions simplification at `tests/test-finalize-phase.sh:524`. It also verifies validators parse `finalize-state.md` during Finalize Phase at `tests/test-finalize-phase.sh:820`.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-137 `file` `tests/robustness/test-template-stress-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for the RLCR template renderer under large input, many substitutions, and special-character stress.
- algorithmic_behavior: The script sources `hooks/lib/template-loader.sh` and shared test helpers at `tests/robustness/test-template-stress-robustness.sh:14`. It verifies standard substitution, safe fallback rendering, generated template-file rendering, large value substitution, large template rendering, many variables, literal special characters, empty values, placeholder-in-value injection prevention, repeated placeholders, boundary placeholders, and placeholder-only templates.
- inputs_outputs_state: Inputs are inline template strings, generated temp template files under `TEST_DIR`, and `VAR=value` arguments to `render_template`, `load_and_render`, and `load_and_render_safe`. It writes only temporary test files via `setup_test_dir` and exits with the helper summary status at `tests/robustness/test-template-stress-robustness.sh:285`.
- gates_or_invariants: The core invariant is single-pass, literal substitution. The implementation builds `TMPL_VAR_` environment variables and scans each line with awk, replacing `{{VAR}}` without rescanning inserted values at `hooks/lib/template-loader.sh:58`. The test explicitly checks placeholder injection is prevented at `tests/robustness/test-template-stress-robustness.sh:218`.
- dependencies_and_callers: Depends on `render_template`, `load_and_render`, and `load_and_render_safe` from `hooks/lib/template-loader.sh:50`, `hooks/lib/template-loader.sh:134`, and `hooks/lib/template-loader.sh:167`; depends on `setup_test_dir`, `pass`, `fail`, and `print_test_summary` from `tests/test-helpers.sh:30`, `tests/test-helpers.sh:58`, and `tests/test-helpers.sh:86`.
- edge_cases_or_failure_modes: It covers 10KB and 100KB values at `tests/robustness/test-template-stress-robustness.sh:82` and `tests/robustness/test-template-stress-robustness.sh:96`, a roughly 100KB template at `tests/robustness/test-template-stress-robustness.sh:111`, 50 variables at `tests/robustness/test-template-stress-robustness.sh:134`, regex/sed/shell-sensitive characters at `tests/robustness/test-template-stress-robustness.sh:161`, and newlines at `tests/robustness/test-template-stress-robustness.sh:195`. Portability risk: elapsed timing uses `date +%s%N`, which may fail on BSD/macOS date implementations. The “Unicode content” test uses ASCII text, so it does not actually stress non-ASCII rendering.
- validation_or_tests: The test is itself the validation artifact. Related broader template tests also assert shell metacharacters render literally and placeholder injection remains single-pass at `tests/test-template-loader.sh:257` and `tests/test-template-loader.sh:499`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5 unique item sections above, matching the assigned set in order
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`