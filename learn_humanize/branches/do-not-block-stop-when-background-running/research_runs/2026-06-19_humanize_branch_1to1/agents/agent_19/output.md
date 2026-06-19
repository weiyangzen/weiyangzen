# agent_19 do-not-block-stop-when-background-running 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `3711e5fd9059584c7bf98cf1d19ee02dcf5bef48`

## Item Evidence

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-019 `directory` `skills/ask-codex`
- cursor: `[_]`
- core_role: Defines the `/humanize:ask-codex` skill wrapper for one-shot Codex consultation. Recursive inspection found one child, `skills/ask-codex/SKILL.md`, so the directory’s responsibility is entirely the skill contract and routing metadata.
- algorithmic_behavior: The skill tells the agent to call `${CLAUDE_PLUGIN_ROOT}/scripts/ask-codex.sh` and to preserve user free-form text as one quoted shell argument. It explicitly forbids bare `$ARGUMENTS` expansion because shell metacharacters can be re-parsed before the script starts (`skills/ask-codex/SKILL.md:14-36`).
- inputs_outputs_state: Inputs are optional `--codex-model MODEL:EFFORT`, optional `--codex-timeout SECONDS`, and a question/task. Output is Codex stdout for the caller, status on stderr, and a persisted response under `.humanize/skill/<timestamp>/output.md` (`skills/ask-codex/SKILL.md:38-56`). The underlying script stores project-local skill artifacts and cache logs (`scripts/ask-codex.sh:15-17`, `scripts/ask-codex.sh:391-408`).
- gates_or_invariants: Flags must remain separate shell arguments; the remaining prompt must be quoted as one final argument. Exit-code semantics are part of the skill contract: `0` success, `1` validation error, `124` timeout, other codes as Codex process errors (`skills/ask-codex/SKILL.md:44-51`).
- dependencies_and_callers: Depends on `scripts/ask-codex.sh`, which sources `loop-common.sh` for config-backed Codex defaults (`scripts/ask-codex.sh:31-43`), validates CLI availability and arguments (`scripts/ask-codex.sh:153-180`), and runs `codex exec` through a timeout wrapper (`scripts/ask-codex.sh:296-298`). It is referenced by plan generation and task routing: `gen-plan` permits `scripts/ask-codex.sh`, and RLCR task tags route `analyze` work through `/humanize:ask-codex` (`scripts/setup-rlcr-loop.sh:1331-1337`).
- edge_cases_or_failure_modes: Shell metacharacters in questions are the main documented failure mode. Other failures are delegated to the script: missing Codex CLI, empty prompt, invalid model/effort characters, timeout, and nonzero Codex exit.
- validation_or_tests: `tests/test-ask-codex.sh` uses a mock `codex` binary (`tests/test-ask-codex.sh:39-52`) and specifically asserts that the skill warns against unsafe bare argument expansion and documents the safe quoted invocation (`tests/test-ask-codex.sh:415-424`).
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-049 `file` `scripts/bitlesson-init.sh`
- cursor: `[_]`
- core_role: Bootstraps the BitLesson knowledge-base file for an RLCR project. It is a state-initialization script used before loop state creation.
- algorithmic_behavior: Parses `--project-root`, `--template`, and optional `--bitlesson-relpath`; defaults the relative path to `.humanize/bitlesson.md`; creates the target from the template only when missing; never overwrites an existing regular file (`scripts/bitlesson-init.sh:5-20`, `scripts/bitlesson-init.sh:83-88`).
- inputs_outputs_state: Inputs are an existing project root directory, an existing template file, and a safe relative BitLesson path. Output is the resolved absolute BitLesson file path on stdout (`scripts/bitlesson-init.sh:14`, `scripts/bitlesson-init.sh:75-88`). State transition is “absent BitLesson file” to “template-copied BitLesson file”; existing regular-file state is preserved unchanged.
- gates_or_invariants: Requires `--project-root` and `--template` (`scripts/bitlesson-init.sh:48-58`), rejects non-directory roots and missing templates (`scripts/bitlesson-init.sh:60-68`), rejects absolute or parent-traversal BitLesson paths (`scripts/bitlesson-init.sh:70-73`), and rejects an existing non-regular target path (`scripts/bitlesson-init.sh:78-81`).
- dependencies_and_callers: Called by `scripts/setup-rlcr-loop.sh` during “Initialize BitLesson File” before the RLCR state file is created (`scripts/setup-rlcr-loop.sh:852-862`). Downstream, `hooks/loop-codex-stop-hook.sh` validates non-finalize summaries against this BitLesson file via `scripts/bitlesson-validate-delta.sh` (`hooks/loop-codex-stop-hook.sh:819-837`).
- edge_cases_or_failure_modes: Fails closed on unknown arguments, missing flag values, unsafe relpaths, missing template, absent root, or target path occupied by a directory/device. Because it uses `cp` under `set -euo pipefail`, copy or mkdir failures abort the script.
- validation_or_tests: No narrow test file for this script was in the assigned set. It is indirectly covered by setup-loop flows that call it before state creation and by BitLesson delta validation that assumes the initialized file exists.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-079 `file` `tests/test-finalize-phase.sh`
- cursor: `[_]`
- core_role: Executable specification for RLCR Finalize Phase, review-phase failure handling, protected loop-state files, todo gating, and mainline drift transitions.
- algorithmic_behavior: Builds an isolated temp git repo, sources `hooks/lib/loop-common.sh`, creates mock Codex executables, creates `.humanize/rlcr/<timestamp>` loop state, then drives validators and `hooks/loop-codex-stop-hook.sh` with JSON hook inputs (`tests/test-finalize-phase.sh:40-80`, `tests/test-finalize-phase.sh:172-268`).
- inputs_outputs_state: Inputs include mock Codex outputs, hook JSON, transcript JSONL with TodoWrite state, temporary state files, and git cleanliness. Outputs are PASS/FAIL lines and process exit equal to failed-test count (`tests/test-finalize-phase.sh:36-38`, `tests/test-finalize-phase.sh:1104-1113`). State transitions asserted include `state.md` to `finalize-state.md` on COMPLETE plus clean review, `finalize-state.md` to `complete-state.md` after finalize gates pass, and `state.md` to `maxiter-state.md` when COMPLETE occurs at max iterations (`tests/test-finalize-phase.sh:541-607`, `tests/test-finalize-phase.sh:609-627`).
- gates_or_invariants: Finalize state is active but terminal complete state is not (`tests/test-finalize-phase.sh:324-361`). Finalize exit requires `finalize-summary.md`, clean git state, and completed todos, and it must not invoke Codex again (`tests/test-finalize-phase.sh:494-569`, `tests/test-finalize-phase.sh:770-812`). Write/Edit/Bash validators must block `finalize-state.md` mutation and round-contract access during Finalize while allowing `finalize-summary.md` (`tests/test-finalize-phase.sh:386-480`, `tests/test-finalize-phase.sh:1041-1102`).
- dependencies_and_callers: Depends on `hooks/lib/loop-common.sh`, `loop-write-validator.sh`, `loop-edit-validator.sh`, `loop-bash-validator.sh`, `loop-read-validator.sh`, `loop-plan-file-validator.sh`, `loop-codex-stop-hook.sh`, `check-todos-from-transcript.py`, `git`, `jq`, and Python. The broader test runner includes this file in `tests/run-all-tests.sh:75`.
- edge_cases_or_failure_modes: Asserts Codex review failure and empty review output are hard blocks that preserve `state.md` and set `review_started: true` (`tests/test-finalize-phase.sh:630-767`). Asserts normal non-COMPLETE rounds still block with feedback and increment round state (`tests/test-finalize-phase.sh:814-887`). Asserts missing `Mainline Progress Verdict` blocks without generating the next prompt, while repeated stalled/regressed verdicts escalate to drift recovery and then stop state (`tests/test-finalize-phase.sh:890-1039`).
- validation_or_tests: The file is itself the validation artifact. It also reflects implementation contracts in `loop-codex-stop-hook.sh`: finalize phase skips Codex review and completes after gates (`hooks/loop-codex-stop-hook.sh:937-952`), COMPLETE enters review/finalize flow (`hooks/loop-codex-stop-hook.sh:1826-1872`), and review failure blocks instead of skipping (`hooks/loop-codex-stop-hook.sh:1240-1278`, `hooks/loop-codex-stop-hook.sh:1548-1588`).
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-109 `file` `prompt-template/block/bitlesson-delta-inconsistent.md`
- cursor: `[_]`
- core_role: User-facing block template for inconsistent BitLesson Delta declarations in RLCR summaries.
- algorithmic_behavior: Presents the invariant that `Action: none` must pair with `Lesson ID(s): NONE` or omitted IDs, while `Action: add|update` must provide concrete IDs that exist in `.humanize/bitlesson.md` (`prompt-template/block/bitlesson-delta-inconsistent.md:1-7`).
- inputs_outputs_state: Input is a validation failure selected by `scripts/bitlesson-validate-delta.sh`; output is block-message markdown used as the JSON `reason` for the stop hook. It does not mutate state directly; it supports the stop-hook transition “summary accepted” versus “exit blocked for BitLesson repair.”
- gates_or_invariants: Encodes the action-to-ID consistency gate. The underlying validator also checks the delta block exists, has exactly one action, contains notes for add/update, uses `BL-YYYYMMDD-short-name` format, and references IDs present in the BitLesson file (`scripts/bitlesson-validate-delta.sh:181-217`, `scripts/bitlesson-validate-delta.sh:242-385`).
- dependencies_and_callers: Loaded through `load_and_render_safe` by `scripts/bitlesson-validate-delta.sh` for multiple inconsistency classes, including action `none` with concrete IDs, add/update missing IDs, missing BitLesson file, no concrete IDs, invalid ID format, and missing IDs in the knowledge base (`scripts/bitlesson-validate-delta.sh:250`, `scripts/bitlesson-validate-delta.sh:276`, `scripts/bitlesson-validate-delta.sh:306`, `scripts/bitlesson-validate-delta.sh:349`, `scripts/bitlesson-validate-delta.sh:364`, `scripts/bitlesson-validate-delta.sh:379`).
- edge_cases_or_failure_modes: The template is intentionally generic and has no placeholders, so more specific fallback messages passed by callers are replaced by this stable generic message when the template exists. That favors consistent user guidance over detailed per-failure text.
- validation_or_tests: Indirectly validated by stop-hook BitLesson enforcement paths. The validator returns a JSON block decision with this rendered reason through `block_exit` (`scripts/bitlesson-validate-delta.sh:78-90`).
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-139 `file` `prompt-template/block/stop-hook-direct-execution.md`
- cursor: `[_]`
- core_role: Block template used when a user tries to manually execute managed hook scripts during an active RLCR loop.
- algorithmic_behavior: Tells the agent that hook scripts are managed by the hooks system and should not be run manually; the intended action is to finish the response and let the hook system run automatically (`prompt-template/block/stop-hook-direct-execution.md:1-7`).
- inputs_outputs_state: Input is a Bash command classified as a direct hook-script launch. Output is markdown written to stderr by the Bash validator via `stop_hook_direct_execution_blocked_message`; no loop state is advanced.
- gates_or_invariants: Enforces separation between user/tool commands and hook lifecycle. The Bash validator detects blocked hook-script launch patterns and exits `2` after rendering this template (`hooks/loop-bash-validator.sh:180-183`).
- dependencies_and_callers: `hooks/lib/loop-common.sh` defines `stop_hook_direct_execution_blocked_message` and loads this template with an inline fallback (`hooks/lib/loop-common.sh:1418-1429`). `hooks/loop-bash-validator.sh` is the concrete caller.
- edge_cases_or_failure_modes: Scope is direct Bash execution detection; it does not cover hook invocation by the official hooks runtime. Detection depends on the validator’s command regex, including wrappers and path variants.
- validation_or_tests: No dedicated direct-execution test was in the assigned item set. The behavior is structurally covered by the Bash validator path that renders the template and returns a blocking exit.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-169 `file` `prompt-template/plan/gen-plan-template.md`
- cursor: `[_]`
- core_role: Canonical output schema for generated implementation plans. It shapes downstream RLCR execution by requiring acceptance criteria, path boundaries, task routing tags, deliberation status, pending user decisions, and implementation notes.
- algorithmic_behavior: Requires every acceptance criterion to include positive and negative tests (`prompt-template/plan/gen-plan-template.md:6-23`), separates upper/lower implementation bounds and allowed choices (`prompt-template/plan/gen-plan-template.md:25-44`), and requires each task to carry exactly one `coding` or `analyze` routing tag (`prompt-template/plan/gen-plan-template.md:69-79`).
- inputs_outputs_state: Input is a draft plan plus gen-plan command context. Output is the main plan file, and optionally a translated variant when `alternative_plan_language` resolves to a supported language through merged config (`prompt-template/plan/gen-plan-template.md:106-120`). The generated plan becomes a requirement source for `start-rlcr-loop`.
- gates_or_invariants: Plan code must not leak plan workflow markers into implementation code/comments (`prompt-template/plan/gen-plan-template.md:99-104`). Alternative language generation must preserve identifiers and file paths, use `_code` filename insertion, skip unsupported/English/empty values, and avoid auto-creating `.humanize/config.json` (`prompt-template/plan/gen-plan-template.md:110-120`).
- dependencies_and_callers: `scripts/validate-gen-plan-io.sh` locates this template through `CLAUDE_PLUGIN_ROOT` or script-relative fallback and fails with plugin configuration error if missing (`scripts/validate-gen-plan-io.sh:162-178`). `commands/gen-plan.md` embeds this exact structure, and tests assert the embedded block matches this file byte-for-byte (`tests/test-gen-plan.sh:708-716`). RLCR setup later consumes the `coding`/`analyze` task tags for execution routing (`scripts/setup-rlcr-loop.sh:1331-1337`).
- edge_cases_or_failure_modes: Deterministic designs may collapse upper/lower bounds to the same implementation path (`prompt-template/plan/gen-plan-template.md:44`). Outputs without file extensions still get language suffixes, while unsupported language values disable translation rather than failing (`prompt-template/plan/gen-plan-template.md:114-120`).
- validation_or_tests: `tests/test-gen-plan.sh` checks ask-codex availability in gen-plan, deliberation and pending decision sections, no obsolete convergence/team sections, mandatory task tags, and exact template embedding (`tests/test-gen-plan.sh:120-236`, `tests/test-gen-plan.sh:708-716`).
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6 evidence headings present, matching the assigned table order
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`