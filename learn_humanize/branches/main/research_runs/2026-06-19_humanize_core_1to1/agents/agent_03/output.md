# agent_03 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`

## Item Evidence

### HZ-003 `directory` `commands`
- cursor: `[_]`
- core_role: Slash-command workflow specification layer for the Humanize lifecycle: idea drafting, plan generation, annotated-plan refinement, RLCR loop startup, and loop cancellation. The directory contains `cancel-rlcr-loop.md`, `gen-idea.md`, `gen-plan.md`, `refine-plan.md`, and `start-rlcr-loop.md`.
- algorithmic_behavior: `commands/gen-idea.md:17-31` defines a draft-only directed-swarm exploration algorithm; `commands/gen-plan.md:32-45` defines a sequential draft-to-plan convergence workflow; `commands/refine-plan.md:30-43` defines a plan-comment refinement workflow; `commands/start-rlcr-loop.md:13-58` gates loop start with compliance checks; `commands/cancel-rlcr-loop.md:9-37` delegates cancellation state transitions to the script.
- inputs_outputs_state: Inputs are command arguments, draft/plan files, repository context, merged config, subagent/Codex results, and loop state files. Outputs include idea drafts, plan files, refined plans, QA ledgers, RLCR loop state under `.humanize/rlcr`, BitLesson initialization, and cancellation reports.
- gates_or_invariants: Planning commands forbid implementation writes (`commands/gen-idea.md:17-20`, `commands/gen-plan.md:20-29`, `commands/refine-plan.md:19-28`); command phases are sequential (`commands/gen-plan.md:34`, `commands/refine-plan.md:32`); RLCR startup blocks unrelated plans and branch-switching instructions (`commands/start-rlcr-loop.md:41-56`); cancellation in finalize phase requires user confirmation (`commands/cancel-rlcr-loop.md:24-35`).
- dependencies_and_callers: Command specs call validators and setup/cancel scripts: `scripts/validate-gen-idea-io.sh`, `scripts/validate-gen-plan-io.sh`, `scripts/validate-refine-plan-io.sh`, `scripts/setup-rlcr-loop.sh`, and `scripts/cancel-rlcr-loop.sh`. They also depend on agents such as `draft-relevance-checker`, `plan-compliance-checker`, and `plan-understanding-quiz`.
- edge_cases_or_failure_modes: Degraded exploration with too few proposals stops or warns (`commands/gen-idea.md:98-103`, `commands/gen-idea.md:135-142`); missing Codex triggers retry/Claude-only choice (`commands/gen-plan.md:208-213`); direct mode cannot auto-start RLCR (`commands/gen-plan.md:255-258`); malformed quiz output warns and proceeds (`commands/start-rlcr-loop.md:86-87`).
- validation_or_tests: `tests/test-gen-plan.sh`, `tests/test-refine-plan.sh`, and command-specific validators provide executable coverage for metadata, templates, exit codes, and algorithmic constraints; `tests/run-all-tests.sh` includes both gen-plan and refine-plan suites.
- skip_candidate: `no`

### HZ-033 `file` `commands/gen-plan.md`
- cursor: `[_]`
- core_role: Defines the draft-to-implementation-plan algorithm and the handoff gate into RLCR. It is central because generated plans supply acceptance criteria, task routing tags, dependencies, decisions, and optional auto-start conditions.
- algorithmic_behavior: The file enforces a strict phase machine: mode parse (`commands/gen-plan.md:49-58`), merged config load (`commands/gen-plan.md:62-129`), IO validation (`commands/gen-plan.md:132-150`), relevance check (`commands/gen-plan.md:154-180`), first Codex analysis (`commands/gen-plan.md:184-213`), Claude candidate synthesis (`commands/gen-plan.md:216-253`), iterative Claude/Codex convergence (`commands/gen-plan.md:255-299`), decision resolution (`commands/gen-plan.md:301-370`), final plan generation (`commands/gen-plan.md:372-531`), and write/optional start (`commands/gen-plan.md:533-632`).
- inputs_outputs_state: Inputs are `$ARGUMENTS`, a draft file, config layers, repository context, Codex findings, user decisions, and `prompt-template/plan/gen-plan-template.md`. Outputs are the main plan, optional translated variant, convergence status, pending decision ledger, and optionally `/humanize:start-rlcr-loop --skip-quiz <output-plan-path>` when all auto-start predicates pass (`commands/gen-plan.md:596-605`).
- gates_or_invariants: No coding during plan generation (`commands/gen-plan.md:20-29`); `--discussion` and `--direct` are mutually exclusive (`commands/gen-plan.md:54-57`); validator exit codes stop on missing input, empty input, bad output path, permissions, invalid args, or missing template (`commands/gen-plan.md:140-149`); direct mode sets `partially_converged` and requires review (`commands/gen-plan.md:255-258`); pending decisions block auto-start (`commands/gen-plan.md:596-600`).
- dependencies_and_callers: Calls `scripts/validate-gen-plan-io.sh` (`commands/gen-plan.md:136-138`), `scripts/ask-codex.sh` (`commands/gen-plan.md:190-193`, `commands/gen-plan.md:263-267`), `scripts/setup-rlcr-loop.sh` fallback (`commands/gen-plan.md:610-614`), config-loader semantics (`commands/gen-plan.md:64-74`), and the draft relevance Task agent (`commands/gen-plan.md:160-169`).
- edge_cases_or_failure_modes: Unsupported `alternative_plan_language` disables variant with warning (`commands/gen-plan.md:115-118`); deprecated `chinese_plan` is only a fallback (`commands/gen-plan.md:91-99`); `NOT_RELEVANT` stops (`commands/gen-plan.md:171-175`); max convergence rounds can leave unresolved decisions (`commands/gen-plan.md:286-293`); auto-start failure reports manual command (`commands/gen-plan.md:616-620`).
- validation_or_tests: `scripts/validate-gen-plan-io.sh:1-12` defines exit codes; `scripts/validate-gen-plan-io.sh:162-178` locates and emits the template path; `tests/test-gen-plan.sh` checks command structure, convergence/direct-mode rules, task tags, template parity, and validator behavior.
- skip_candidate: `no`

### HZ-063 `file` `templates/bitlesson.md`
- cursor: `[_]`
- core_role: Seed template for project-local BitLesson memory, consumed by RLCR setup to create `.humanize/bitlesson.md` when missing. It supports the loop’s reusable lesson-selection and lesson-delta algorithm.
- algorithmic_behavior: The template declares a strict entry schema (`templates/bitlesson.md:5-19`) with stable fields: lesson ID, scope, problem, root cause, solution, constraints, validation evidence, and source rounds. New entries are appended under `## Entries` (`templates/bitlesson.md:21-23`).
- inputs_outputs_state: The template itself has no runtime inputs. `scripts/setup-rlcr-loop.sh:860-866` passes it to `scripts/bitlesson-init.sh`, which creates `<project-root>/.humanize/bitlesson.md` if missing and leaves existing files intact (`scripts/bitlesson-init.sh:10-14`, `scripts/bitlesson-init.sh:83-86`).
- gates_or_invariants: Entry field order is strict (`templates/bitlesson.md:5-8`); initialization requires an existing project root and template (`scripts/bitlesson-init.sh:60-67`); the BitLesson relative path must not be absolute or contain `..` (`scripts/bitlesson-init.sh:70-72`); existing non-file path is rejected (`scripts/bitlesson-init.sh:78-80`).
- dependencies_and_callers: Called by `start-rlcr-loop` setup (`scripts/setup-rlcr-loop.sh:857-866`); the command docs require reading `.humanize/bitlesson.md`, running `bitlesson-selector`, and adding/updating lessons after multi-round fixes (`commands/start-rlcr-loop.md:168-180`).
- edge_cases_or_failure_modes: Empty `.humanize/bitlesson.md` does not block `Action: none` by default, but `--require-bitlesson-entry-for-none` can make empty memory blocking (`commands/start-rlcr-loop.md:179-180`). A missing template is a setup failure through `bitlesson-init.sh`.
- validation_or_tests: BitLesson behavior is covered by `tests/test-bitlesson-select-routing.sh`, `tests/test-bitlesson-validate-delta.sh`, and setup/hook tests referenced by search results; `docs/bitlesson.md:27-31` documents initialization from this template.
- skip_candidate: `no`

### HZ-093 `file` `tests/test-refine-plan.sh`
- cursor: `[_]`
- core_role: Executable specification for the refine-plan command, its IO validator, QA template, language/path rules, and install wiring. It is test code, but it defines expected algorithm behavior with concrete assertions.
- algorithmic_behavior: The test builds fixtures (`tests/test-refine-plan.sh:159-421`), implements reference scanners/classifiers/path helpers (`tests/test-refine-plan.sh:427-622`), then verifies command metadata and phase ordering (`tests/test-refine-plan.sh:660-701`), validator docs (`tests/test-refine-plan.sh:703-713`), extraction/classification requirements (`tests/test-refine-plan.sh:716-748`), structure and modes (`tests/test-refine-plan.sh:751-788`), atomic writes (`tests/test-refine-plan.sh:790-801`), QA template coverage (`tests/test-refine-plan.sh:803-817`), install wiring/version consistency (`tests/test-refine-plan.sh:820-880`), reference behavior (`tests/test-refine-plan.sh:891-1040`), and validator exit behavior (`tests/test-refine-plan.sh:1052-1343`).
- inputs_outputs_state: Inputs are repository files (`commands/refine-plan.md`, `prompt-template/plan/refine-plan-qa-template.md`, `scripts/validate-refine-plan-io.sh`, skill/install/docs/metadata) and generated temp fixture plans. Outputs are terminal PASS/FAIL records, counters, temp QA/output directories, and exit code `0` only when no assertion fails (`tests/test-refine-plan.sh:1345-1363`).
- gates_or_invariants: Requires `refine-plan.md` to be planning-only, hidden from slash tool, sequential, and phase-complete (`tests/test-refine-plan.sh:669-701`); comment extraction must ignore fenced code and HTML comments, reject nested/stray/missing end markers, and preserve surrounding inline text (`tests/test-refine-plan.sh:716-730`, `tests/test-refine-plan.sh:891-954`); task tags must remain `coding` or `analyze` (`tests/test-refine-plan.sh:733-764`).
- dependencies_and_callers: Depends on POSIX shell utilities plus `grep`, `sed`, `mktemp`, `chmod`, `realpath`, and the validator script. It directly exercises `scripts/validate-refine-plan-io.sh`, whose parser supports `CMT:/ENDCMT`, `<cmt></cmt>`, and `<comment></comment>` (`scripts/validate-refine-plan-io.sh:62-113`, `scripts/validate-refine-plan-io.sh:258-292`).
- edge_cases_or_failure_modes: Tests missing values and unknown args as exit `7` (`tests/test-refine-plan.sh:1052-1099`), missing/empty/no-comment/malformed comment input as exits `1-3` (`tests/test-refine-plan.sh:1101-1189`), missing required sections as exit `4` (`tests/test-refine-plan.sh:1191-1216`), unwritable output/input dirs as exit `5` (`tests/test-refine-plan.sh:1218-1264`), bad QA path as exit `6` (`tests/test-refine-plan.sh:1276-1283`), and mixed valid/ignored/empty comment markers as valid when one non-empty block remains (`tests/test-refine-plan.sh:1307-1321`).
- validation_or_tests: This file is itself validation; the targeted validator reports success with line and comment counts plus mode (`scripts/validate-refine-plan-io.sh:680-691`). I inspected rather than executed it because the requested task is read-only research.
- skip_candidate: `no`

### HZ-123 `file` `prompt-template/block/git-not-clean-untracked.md`
- cursor: `[_]`
- core_role: Prompt block used by the RLCR stop hook when untracked files are present, adding policy guidance to the “git not clean” gate.
- algorithmic_behavior: The block warns that untracked files may be generated artifacts and lists likely ignore candidates such as build outputs, dependencies, editor files, logs, caches, and temp files (`prompt-template/block/git-not-clean-untracked.md:2-8`). It ends by directing review and `.gitignore` updates (`prompt-template/block/git-not-clean-untracked.md:10`).
- inputs_outputs_state: It has no placeholders and is rendered as static text. The stop hook loads it when `OTHER_UNTRACKED` is non-empty (`hooks/loop-codex-stop-hook.sh:714-721`) and appends it to `SPECIAL_NOTES` for the block message.
- gates_or_invariants: The invariant is policy-level: untracked generated artifacts normally should not be committed blindly; the gate remains a dirty-worktree block, while this template narrows the remediation path toward ignore patterns.
- dependencies_and_callers: Loaded through `load_template` from `hooks/lib/template-loader.sh:36-45`. If missing, the hook falls back to “Review untracked files - add to .gitignore or commit them.” (`hooks/loop-codex-stop-hook.sh:717-720`).
- edge_cases_or_failure_modes: Because it is generic and variable-free, it cannot distinguish intentionally new source files from artifacts. It supplements but does not replace the hook’s status parsing.
- validation_or_tests: Template loading behavior is covered by template-loader and stop-hook tests; the direct call site is `hooks/loop-codex-stop-hook.sh:714-721`.
- skip_candidate: `no`

### HZ-153 `file` `prompt-template/block/wrong-summary-location.md`
- cursor: `[_]`
- core_role: Prompt block enforcing the RLCR invariant that round summary files must be written inside the active loop directory.
- algorithmic_behavior: The template declares “Summary files MUST be in the loop directory” and renders the required destination with `{{CORRECT_PATH}}` (`prompt-template/block/wrong-summary-location.md:1-5`).
- inputs_outputs_state: Input is the `CORRECT_PATH` value computed by the write validator from active loop directory and current round. Output is a rendered blocking message sent to stderr before the write validator exits `2` (`hooks/loop-write-validator.sh:282-298`).
- gates_or_invariants: The gate fires when a summary or contract file write targets outside `.humanize/rlcr`; for summaries, the correct path is `$ACTIVE_LOOP_DIR/round-${CURRENT_ROUND}-summary.md` (`hooks/loop-write-validator.sh:291-296`).
- dependencies_and_callers: Rendered by `load_and_render_safe`, which keeps missing placeholders unchanged and falls back if the template is missing or empty (`hooks/lib/template-loader.sh:188-210`).
- edge_cases_or_failure_modes: If template loading fails, the fallback still blocks with a correct-path message (`hooks/loop-write-validator.sh:292-295`). If `CORRECT_PATH` is not supplied, the placeholder would remain literal under single-pass rendering rules (`hooks/lib/template-loader.sh:7-13`).
- validation_or_tests: Covered by write-validator/template tests; the core enforcement is in `hooks/loop-write-validator.sh:278-299`.
- skip_candidate: `no`

### HZ-183 `file` `skills/humanize-refine-plan/SKILL.md`
- cursor: `[_]`
- core_role: Flow-skill packaging for annotated-plan refinement. It mirrors the `refine-plan` command algorithm for skill runtimes and preserves the gen-plan schema while producing a QA ledger.
- algorithmic_behavior: The Mermaid flow lays out parse/config/validate/extract/classify/process/refine/validate/QA/variant/atomic-write/report transitions (`skills/humanize-refine-plan/SKILL.md:18-48`). The prose requires stateful extraction of `CMT:` / `ENDCMT` comments, classification into `question`, `change_request`, or `research_request`, and atomic output writing (`skills/humanize-refine-plan/SKILL.md:67-107`).
- inputs_outputs_state: Required input is `--input <path/to/annotated-plan.md>`; optional inputs are `--output`, `--qa-dir`, `--alt-language`, `--discussion`, and `--direct` (`skills/humanize-refine-plan/SKILL.md:50-65`). Outputs are a refined comment-free plan, QA ledger, optional translated variants, counts, paths, mode, and convergence status (`skills/humanize-refine-plan/SKILL.md:96-107`, `skills/humanize-refine-plan/SKILL.md:157-160`).
- gates_or_invariants: `--discussion` and `--direct` are mutually exclusive; `--alt-language` must not be passed to the validator (`skills/humanize-refine-plan/SKILL.md:62-65`); required gen-plan sections must remain intact (`skills/humanize-refine-plan/SKILL.md:71-83`); routing tags stay `coding` or `analyze` (`skills/humanize-refine-plan/SKILL.md:84`); final plan must have no comment markers and references must be consistent (`skills/humanize-refine-plan/SKILL.md:35-39`).
- dependencies_and_callers: Uses the hydrated `{{HUMANIZE_RUNTIME_ROOT}}`, calls `scripts/validate-refine-plan-io.sh`, and reads `prompt-template/plan/refine-plan-qa-template.md` (`skills/humanize-refine-plan/SKILL.md:12-16`, `skills/humanize-refine-plan/SKILL.md:22`, `skills/humanize-refine-plan/SKILL.md:41`).
- edge_cases_or_failure_modes: Validator failures stop with exit-code-specific meanings (`skills/humanize-refine-plan/SKILL.md:131-142`); parse errors report line, column, heading, and context (`skills/humanize-refine-plan/SKILL.md:26-29`); ambiguous comments ask the user in discussion mode but use smallest safe assumptions in direct mode (`skills/humanize-refine-plan/SKILL.md:30-34`, `skills/humanize-refine-plan/SKILL.md:59-60`); matching main/alternate language skips variants (`skills/humanize-refine-plan/SKILL.md:124-130`).
- validation_or_tests: `tests/test-refine-plan.sh:820-826` asserts the skill exists and is `user-invocable: false`; `tests/test-refine-plan.sh:828-855` checks installer and docs wiring.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `7 item evidence sections present; item IDs are used only as section headings`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`