# agent_28 do-not-block-stop-when-background-running 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `3711e5fd9059584c7bf98cf1d19ee02dcf5bef48`

## Item Evidence

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-028 `file` `agents/plan-compliance-checker.md`
- cursor: `[_]`
- core_role: Pre-RLCR plan gate agent prompt. It validates that a candidate implementation plan is relevant to the current repository and does not require branch switching before `/start-rlcr-loop` proceeds; see `agents/plan-compliance-checker.md:8-15`.
- algorithmic_behavior: Runs two checks: repository relevance by inspecting docs, directory shape, technologies, paths, and substantive plan content at `agents/plan-compliance-checker.md:16-29`; branch-switch detection by scanning for checkout/switch/branch/worktree instructions at `agents/plan-compliance-checker.md:31-46`.
- inputs_outputs_state: Input is the plan file content plus read-only repository context. Output is exactly one verdict line: `PASS`, `FAIL_RELEVANCE`, or `FAIL_BRANCH_SWITCH`, specified at `agents/plan-compliance-checker.md:48-55`. It has no persistent local state.
- gates_or_invariants: Relevance is intentionally lenient and should only reject clearly unrelated plans; branch-switch detection is also lenient on ambiguity. It must emit exactly one verdict and never multiple results; see `agents/plan-compliance-checker.md:56-62`.
- dependencies_and_callers: Called by `commands/start-rlcr-loop.md:13-56`, which extracts a safe relative plan path, reads it, invokes `humanize:plan-compliance-checker` via Task, and fail-closes on relevance failure, branch-switch failure, or malformed output.
- edge_cases_or_failure_modes: Safe branch-like patterns are excluded: file restore via `git checkout -- <file>`, explicit “do not switch” language, descriptive branch references, and `--base-branch`; see `agents/plan-compliance-checker.md:40-44`. Malformed agent output causes `/start-rlcr-loop` to stop at `commands/start-rlcr-loop.md:52-56`.
- validation_or_tests: No dedicated executable test was found for this specific agent prompt. The prompt contains example verdicts at `agents/plan-compliance-checker.md:64-76`, and caller behavior is specified in `commands/start-rlcr-loop.md:41-56`.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-058 `file` `scripts/validate-gen-plan-io.sh`
- cursor: `[_]`
- core_role: Phase-1 IO validator for `/gen-plan`, enforcing draft input and output target safety before plan generation. It is explicitly invoked by `commands/gen-plan.md:132-150`.
- algorithmic_behavior: Parses `--input`, `--output`, `--auto-start-rlcr-if-converged`, `--discussion`, and `--direct` at `scripts/validate-gen-plan-io.sh:29-74`; rejects mutually exclusive mode flags at `scripts/validate-gen-plan-io.sh:76-80`; resolves absolute paths at `scripts/validate-gen-plan-io.sh:98-101`.
- inputs_outputs_state: Inputs are CLI args, filesystem state, and optional `CLAUDE_PLUGIN_ROOT`. Outputs are validation status lines, resolved paths, `TEMPLATE_FILE`, and exit codes. It does not create the output plan file; `commands/gen-plan.md:150` documents the side-effect-free expectation.
- gates_or_invariants: Required `--input` and `--output` are enforced at `scripts/validate-gen-plan-io.sh:82-91`; input must exist and be non-empty at `scripts/validate-gen-plan-io.sh:108-122`; output directory must exist and be writable at `scripts/validate-gen-plan-io.sh:124-153`; output path must not already exist and must not be a directory at `scripts/validate-gen-plan-io.sh:132-145`.
- dependencies_and_callers: `/gen-plan` allowlists and invokes this script at `commands/gen-plan.md:4-7` and `commands/gen-plan.md:132-138`. Template discovery depends on `prompt-template/plan/gen-plan-template.md`, resolved via `CLAUDE_PLUGIN_ROOT` or script-relative fallback at `scripts/validate-gen-plan-io.sh:162-169`.
- edge_cases_or_failure_modes: Direct mode plus auto-start only prints a note because auto-start convergence applies to discussion mode at `scripts/validate-gen-plan-io.sh:93-96`. Missing template exits 7 at `scripts/validate-gen-plan-io.sh:171-175`. Unknown flags and missing flag values exit 6 through `usage`.
- validation_or_tests: `tests/test-gen-plan.sh:557-705` covers invalid flag values, unknown flags, missing input, empty input, missing output dir, existing output, directory output, success path, auto-start flag acceptance, discussion/direct recognition, mutual exclusion, and help exit.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-088 `file` `tests/test-plan-file-hooks.sh`
- cursor: `[_]`
- core_role: Executable specification for RLCR plan-file hook behavior across prompt, write, edit, bash, and stop hooks. It exercises the core plan immutability, branch invariance, state schema, and stop-gate integrity contracts.
- algorithmic_behavior: Builds isolated git test repos and loop state under temp dirs at `tests/test-plan-file-hooks.sh:30-140`, including mock `codex`, `.humanize/rlcr/<timestamp>`, `state.md`, plan backup, and round contract. It then runs hook scripts with JSON payloads and asserts exit codes/output text.
- inputs_outputs_state: Inputs include hook JSON payloads, `CLAUDE_PROJECT_DIR`, `PATH` with mock codex, `XDG_CACHE_HOME`, git branch/status, `state.md`, `plan.md`, `goal-tracker.md`, and summary files. Outputs are PASS/FAIL/SKIP counters and final process exit equal to failed test count at `tests/test-plan-file-hooks.sh:1172-1181`.
- gates_or_invariants: UserPromptSubmit must pass valid state and block malformed state or branch changes at `tests/test-plan-file-hooks.sh:145-243`. Write/Edit/Bash validators must block loop `plan.md` backup mutation at `tests/test-plan-file-hooks.sh:252-310`. Stop hook must block modified/deleted/missing plan state at `tests/test-plan-file-hooks.sh:563-658`.
- dependencies_and_callers: Depends on `hooks/loop-plan-file-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-bash-validator.sh`, and `hooks/loop-codex-stop-hook.sh`. These are installed as Claude hooks in `hooks/hooks.json:4-69`; the suite is listed by `tests/run-all-tests.sh:69`.
- edge_cases_or_failure_modes: Covers YAML-quoted `plan_file` and `start_branch`, branch name defaults across `main`/`master`, hyphenated plan paths, missing round contract, tracked plan modifications, committed tracked plan content drift, outdated schema JSON blocking, and direct `.humanize/rlcr/plan.md` path handling; see `tests/test-plan-file-hooks.sh:395-835`.
- validation_or_tests: This file is itself the validation harness. It also regression-tests shell bypass patterns: command substitution, glob expansion, brace expansion, piped `tee`, and backticks at `tests/test-plan-file-hooks.sh:326-393`; section-specific placeholder reporting at `tests/test-plan-file-hooks.sh:837-1126`; and legacy `.humanize-loop.local` allow behavior at `tests/test-plan-file-hooks.sh:1128-1170`.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-118 `file` `prompt-template/block/git-not-clean-humanize-local.md`
- cursor: `[_]`
- core_role: Stop-hook message fragment for the special case where local `.humanize/` state is detected in git status. It reinforces that RLCR state should remain uncommitted.
- algorithmic_behavior: Emits a markdown note saying `.humanize/` is created by `humanize:start-rlcr-loop`, should not be committed, and suggests adding `.humanize*` to `.gitignore`; see `prompt-template/block/git-not-clean-humanize-local.md:2-8`.
- inputs_outputs_state: No template variables are used. Input is only template loading by the stop hook. Output is advisory markdown appended to the broader git-not-clean block. It has no direct state transition.
- gates_or_invariants: The invariant is “local Humanize state stays out of commits.” The template itself is advisory; the stop hook performs the actual blocking when non-ignored dirty tracked/untracked state remains.
- dependencies_and_callers: Loaded by `hooks/loop-codex-stop-hook.sh:667-674` when untracked `.humanize`-style paths are present alongside a dirty-worktree block. The surrounding git dirty gate is assembled at `hooks/loop-codex-stop-hook.sh:654-700`.
- edge_cases_or_failure_modes: The suggested command appends `.humanize*` and could duplicate an existing ignore entry if applied blindly. If the template cannot be loaded, the stop hook falls back to an inline note at `hooks/loop-codex-stop-hook.sh:670-672`.
- validation_or_tests: No direct assertion for this exact template was found in the inspected tests. Its reference is covered structurally through stop-hook template usage and template-reference coverage, but behavior is mostly exercised through the stop hook’s git-clean gate.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-148 `file` `prompt-template/block/wrong-round-number.md`
- cursor: `[_]`
- core_role: Write/Edit validator block template for attempts to write or edit a round summary/contract file whose filename round does not match current loop state.
- algorithmic_behavior: Renders `ACTION`, `CLAUDE_ROUND`, `FILE_TYPE`, `CURRENT_ROUND`, and `CORRECT_PATH` into a concrete correction message; see `prompt-template/block/wrong-round-number.md:1-7`.
- inputs_outputs_state: Inputs are render variables supplied by hook validators. Output is markdown sent to stderr before the validator exits with a blocking status. It does not mutate loop state.
- gates_or_invariants: Summary and contract filenames must target the current round only. The message explicitly tells the agent not to increment the round number itself at `prompt-template/block/wrong-round-number.md:7`.
- dependencies_and_callers: `hooks/loop-edit-validator.sh:234-258` renders this template for wrong-round edits. `hooks/loop-write-validator.sh:305-322` renders it for wrong-round writes. Both compute the correct file path under `ACTIVE_LOOP_DIR`.
- edge_cases_or_failure_modes: The validators only trigger when the file is a summary or contract, a round number can be extracted, the extracted round differs from `CURRENT_ROUND`, and the path is not allowlisted; see `hooks/loop-edit-validator.sh:234-259` and `hooks/loop-write-validator.sh:305-323`.
- validation_or_tests: Template rendering is directly checked by `tests/test-template-loader.sh:151-163` and `tests/test-templates-comprehensive.sh:498-510`, verifying variable substitution for wrong round, current round, and correct path.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-178 `file` `skills/humanize-refine-plan/SKILL.md`
- cursor: `[_]`
- core_role: Flow skill contract for refining an annotated `gen-plan` document into a comment-free plan plus QA ledger while preserving planning schema and convergence state.
- algorithmic_behavior: Defines a staged flow from argument parsing, config loading, validator execution, stateful `CMT:`/`ENDCMT` extraction, classification, processing, plan regeneration, QA generation, optional variants, atomic writes, and success reporting; see `skills/humanize-refine-plan/SKILL.md:18-48`.
- inputs_outputs_state: Required input is `--input <annotated-plan.md>`; optional inputs are `--output`, `--qa-dir`, `--alt-language`, `--discussion`, and `--direct` at `skills/humanize-refine-plan/SKILL.md:50-65`. Outputs are refined plan, QA ledger, and optional translated variants at `skills/humanize-refine-plan/SKILL.md:96-107`.
- gates_or_invariants: Preserves required `gen-plan` sections, removes resolved comment blocks, keeps routing tags restricted to `coding` or `analyze`, preserves optional sections, and writes outputs atomically; see `skills/humanize-refine-plan/SKILL.md:67-87`.
- dependencies_and_callers: Depends on `scripts/validate-refine-plan-io.sh` and `prompt-template/plan/refine-plan-qa-template.md` as shown in the flow at `skills/humanize-refine-plan/SKILL.md:22-45`. `commands/refine-plan.md:1-180` expands the executable command contract, validator invocation, mode/config semantics, and write constraints.
- edge_cases_or_failure_modes: `--discussion` and `--direct` are mutually exclusive; `--alt-language` must not be passed to the validator; omitted `--output` means in-place refinement; unsupported alternate languages are constrained by the mapping at `skills/humanize-refine-plan/SKILL.md:108-130`; validator exit codes 1-7 are defined at `skills/humanize-refine-plan/SKILL.md:131-143`.
- validation_or_tests: `tests/test-refine-plan.sh:640-860` checks command metadata, planning-only constraints, phase order, section preservation, alternate-language rules, atomic write requirements, QA template coverage, install wiring, and skill `user-invocable: false`. `tests/test-refine-plan.sh:1040-1343` checks validator argument errors, comment parsing exclusions, missing sections, writable paths, QA directory handling, and mode reporting.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `6/6 item evidence sections present; item IDs appear only as section headers`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`