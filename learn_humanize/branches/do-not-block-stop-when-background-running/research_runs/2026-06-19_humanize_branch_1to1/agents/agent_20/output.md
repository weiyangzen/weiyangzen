# agent_20 do-not-block-stop-when-background-running 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `3711e5fd9059584c7bf98cf1d19ee02dcf5bef48`

## Item Evidence

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-020 `directory` `skills/ask-gemini`
- cursor: `[_]`
- core_role: Skill wrapper for invoking Gemini as an external research consultant; directory contains only `skills/ask-gemini/SKILL.md`, which binds the slash-skill contract to `${CLAUDE_PLUGIN_ROOT}/scripts/ask-gemini.sh` via allowed tools at `skills/ask-gemini/SKILL.md:1-6`.
- algorithmic_behavior: The skill instructs callers to pass the user question as a single quoted shell argument, keep supported flags separate, read stdout as Gemini’s answer, and surface non-zero failures to the user; the safety rule explicitly rejects unquoted `$ARGUMENTS` expansion at `skills/ask-gemini/SKILL.md:15-39`.
- inputs_outputs_state: Inputs are optional `--gemini-model`, optional `--gemini-timeout`, and one free-form question/task; outputs are Gemini response on stdout plus status on stderr, with persisted `.humanize/skill/<timestamp>/output.md` noted at `skills/ask-gemini/SKILL.md:41-60`. Supporting runtime script writes input, output, metadata, and cache artifacts under `.humanize/skill/...` and `~/.cache/humanize/...` (`scripts/ask-gemini.sh:16-18`, `181-196`, `365-385`).
- gates_or_invariants: Invocation invariant is “quote free-form text”; runtime gates include installed `gemini`, non-empty question, model-name character whitelist, and timeout handling (`scripts/ask-gemini.sh:142-165`, `291-310`).
- dependencies_and_callers: Depends on Gemini CLI and `scripts/portable-timeout.sh`; user-facing references appear in `README.md` and monitor plumbing filters Gemini skill invocations via `scripts/lib/monitor-skill.sh`. The script always augments prompts with a Google Search instruction (`scripts/ask-gemini.sh:233-238`).
- edge_cases_or_failure_modes: Missing Gemini, empty question, invalid flag, invalid model characters, timeout exit `124`, non-zero Gemini exit, and empty stdout are all explicit failure paths (`scripts/ask-gemini.sh:102-126`, `150-165`, `291-359`).
- validation_or_tests: No dedicated `test-ask-gemini.sh` found; coverage is indirect through skill metadata and monitor references. This is a core integration wrapper, but not directly tied to the background-stop branch behavior.
- skip_candidate: `yes: directory is a tool-skill facade for Gemini research, not a scheduler/background-running algorithm path; still relevant as command routing/state persistence infrastructure`.

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-050 `file` `scripts/bitlesson-select.sh`
- cursor: `[_]`
- core_role: Runtime selector for choosing applicable BitLesson IDs for a sub-task; it turns task/path/BitLesson content into a strict two-line `LESSON_IDS` plus `RATIONALE` contract (`scripts/bitlesson-select.sh:30-39`, `143-175`, `237-262`).
- algorithmic_behavior: Parses `--task`, `--paths`, and `--bitlesson-file`; validates required values and file content; short-circuits to `NONE` when no `## Lesson:` sections exist; otherwise detects provider from configured model, applies codex-only override, validates provider binary, builds an isolated prompt, runs Codex or Claude with a 120s timeout, and normalizes only the first matching output lines (`scripts/bitlesson-select.sh:45-104`, `110-126`, `181-230`, `237-262`).
- inputs_outputs_state: Inputs are CLI args, merged Humanize config (`bitlesson_model`, `codex_model`, `provider_mode`), the BitLesson markdown, and provider CLIs; output is exactly `LESSON_IDS: ...` and `RATIONALE: ...` to stdout or an error to stderr. Internal state includes `PROJECT_ROOT`, `BITLESSON_PROVIDER`, `CODEX_PROJECT_ROOT`, `PROMPT`, `RAW_OUTPUT`, and parsed values.
- gates_or_invariants: Requires non-empty task/paths, existing non-whitespace BitLesson file, known model/provider, available provider binary or fallback, non-timeout provider execution, and stable selector output format; Codex is forced read-only with low effort, optional `--disable codex_hooks`, `--skip-git-repo-check`, and `--ephemeral` when supported (`scripts/bitlesson-select.sh:71-98`, `187-207`, `222-258`).
- dependencies_and_callers: Sources `scripts/lib/config-loader.sh`, `scripts/lib/model-router.sh`, `scripts/portable-timeout.sh`, and `hooks/lib/loop-common.sh` (`scripts/bitlesson-select.sh:9-28`). The `agents/bitlesson-selector.md` spec declares this script as runtime execution and the stable output contract (`agents/bitlesson-selector.md:19-39`).
- edge_cases_or_failure_modes: Unknown arg, empty task/paths, missing/empty BitLesson file, no lessons, unknown model, missing provider binary, Claude unavailable fallback to Codex, Codex unavailable failure, timeout exit `124`, unsupported provider, malformed model output, and selector raw-output leakage on error are handled explicitly.
- validation_or_tests: `tests/test-bitlesson-select-routing.sh` covers Codex routing, stdin prompt via trailing `-`, Claude model routing including case-insensitive opus, unknown model failure, missing Codex failure, Claude-to-Codex fallback, codex-only override, no-lesson short-circuit, and direct-helper Codex args (`tests/test-bitlesson-select-routing.sh:137-496`). Routing helpers are defined in `scripts/lib/model-router.sh:10-60`.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-080 `file` `tests/test-gen-plan.sh`
- cursor: `[_]`
- core_role: Executable specification for the `gen-plan` command, its command/agent metadata, IO validator behavior, plan template parity, and command workflow invariants (`tests/test-gen-plan.sh:1-15`).
- algorithmic_behavior: Uses shell assertions with pass/fail counters; performs positive structure tests against `commands/gen-plan.md`, `agents/draft-relevance-checker.md`, `prompt-template/plan/gen-plan-template.md`, version files, and then negative fixture tests for invalid names, frontmatter, YAML shape, model names, non-English/emoji content, and IO validator exit codes (`tests/test-gen-plan.sh:22-40`, `54-311`, `313-736`).
- inputs_outputs_state: Inputs are repository files plus temporary invalid fixtures from `mktemp -d`; outputs are colored PASS/FAIL lines and process exit `0` only when `TESTS_FAILED=0`. State is accumulated in `TESTS_PASSED` and `TESTS_FAILED`, with cleanup traps for temp dirs (`tests/test-gen-plan.sh:22-24`, `322-324`, `718-736`).
- gates_or_invariants: Enforces `gen-plan.md` frontmatter fields, allowed tools, argument hint, `ask-codex.sh` availability, `--auto-start-rlcr-if-converged`, direct mode not converged, auto-start discussion-only, ultrathink instruction, Codex-before-Claude phase order, mandatory Pending User Decisions, task tags, and template equality (`tests/test-gen-plan.sh:59-247`, `708-715`).
- dependencies_and_callers: Depends on `commands/gen-plan.md`, `agents/draft-relevance-checker.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md`, `scripts/validate-gen-plan-io.sh`, and `prompt-template/plan/gen-plan-template.md`. `commands/gen-plan.md` confirms the side-effect-free IO validation phase and exit-code handling (`commands/gen-plan.md:132-150`).
- edge_cases_or_failure_modes: Fixture tests check uppercase/spaced names, missing description, absent frontmatter, malformed YAML, invalid/empty/partial model aliases, emoji/CJK content, missing validator executable, validator arg errors, missing/empty input, nonexistent output dir, output exists/is directory, mutual exclusion of `--discussion` and `--direct`, and template drift (`tests/test-gen-plan.sh:326-715`).
- validation_or_tests: This file is itself validation; it also invokes `scripts/validate-gen-plan-io.sh`, whose exit-code map is declared at `scripts/validate-gen-plan-io.sh:1-13` and implemented through path/permission/template checks at `scripts/validate-gen-plan-io.sh:35-178`.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-110 `file` `prompt-template/block/bitlesson-delta-invalid.md`
- cursor: `[_]`
- core_role: Block-message template for the BitLesson Delta validator when a round summary has a `## BitLesson Delta` section but no exactly valid action (`prompt-template/block/bitlesson-delta-invalid.md:1-7`).
- algorithmic_behavior: Provides the user-facing remediation contract listing the only accepted actions: `none`, `add`, and `update`. The actual parser extracts action candidates, requires exactly one, lowercases it, and rejects anything outside that set (`scripts/bitlesson-validate-delta.sh:200-218`).
- inputs_outputs_state: Input is a detected summary delta block; output is rendered block text passed to `block_exit`. No persistent state is stored by the template itself.
- gates_or_invariants: The invariant is exactly one `Action:` line with one of `none|add|update`; missing, duplicate, or unknown actions block the stop hook before the round can proceed (`scripts/bitlesson-validate-delta.sh:202-218`).
- dependencies_and_callers: Loaded by `load_and_render_safe "$TEMPLATE_DIR" "block/bitlesson-delta-invalid.md"` in `scripts/bitlesson-validate-delta.sh:216`; fallback text exists inline at `scripts/bitlesson-validate-delta.sh:207-214`.
- edge_cases_or_failure_modes: The surrounding validator ignores fenced code and HTML comments when detecting `## BitLesson Delta`, preventing fake sections from satisfying the gate (`scripts/bitlesson-validate-delta.sh:153-178`). Missing template falls back to inline text.
- validation_or_tests: `tests/test-bitlesson-validate-delta.sh` exercises BitLesson Delta validation, including fenced-code/comment bypass cases and normal-text success; template reference scanning also checks referenced block templates exist.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-140 `file` `prompt-template/block/summary-bash-write.md`
- cursor: `[_]`
- core_role: Block-message template used when Bash attempts to modify a round summary file; it directs the agent to use the Write/Edit tool at a rendered `{{CORRECT_PATH}}` instead of shell writes (`prompt-template/block/summary-bash-write.md:1-8`).
- algorithmic_behavior: The template itself is static remediation text; enforcement happens in the Bash validator by detecting commands that modify `round-[0-9]+-summary.md`, computing the active loop summary path, rendering this template, and exiting with code `2` (`hooks/loop-bash-validator.sh:511-520`).
- inputs_outputs_state: Input is the correct active summary path injected as `CORRECT_PATH`; output is a stderr block message. No state transition happens in the template, but the validator blocks the attempted tool action.
- gates_or_invariants: Summary files must be changed through Write/Edit so validation hooks can enforce round number and summary contract checks; shell commands like `cat`, `echo`, `sed`, and `awk` are disallowed for summary writes (`prompt-template/block/summary-bash-write.md:3-8`).
- dependencies_and_callers: Rendered by `summary_bash_blocked_message()` in `hooks/lib/loop-common.sh:879-888`, then called from `hooks/loop-bash-validator.sh:516-519`. Template existence is included in `tests/test-template-references.sh:149-167`.
- edge_cases_or_failure_modes: If the template is missing, `summary_bash_blocked_message()` has an inline fallback (`hooks/lib/loop-common.sh:883-887`). Detection is filename-pattern based, so protection depends on `command_modifies_file` recognizing the shell command target.
- validation_or_tests: `tests/test-template-references.sh` scans shell template references and explicitly lists `block/summary-bash-write.md` as a required common template (`tests/test-template-references.sh:51-110`, `152-167`).
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-170 `file` `prompt-template/plan/refine-plan-qa-template.md`
- cursor: `[_]`
- core_role: Required QA document schema for `refine-plan`; it records comment dispositions, answers, research findings, plan changes, remaining decisions, and refinement metadata (`prompt-template/plan/refine-plan-qa-template.md:1-119`).
- algorithmic_behavior: It is a fillable template, not executable code. `commands/refine-plan.md` requires reading and completely populating it in Phase 6, with sections for one ledger row per raw `CMT-N`, question answers, research requests, change requests, unresolved decisions, and metadata (`commands/refine-plan.md:457-505`).
- inputs_outputs_state: Inputs are extracted comments, classifications, original plan/output/QA paths, modified plan sections, convergence state, and refinement date. Output is a QA markdown artifact, optionally with a translated variant during the atomic write transaction (`commands/refine-plan.md:508-560`).
- gates_or_invariants: QA generation is not optional; before it, refine-plan must verify required plan sections remain, no comment markers remain, AC/task references are valid, task tags are valid, and unresolved-state sections agree with actual state (`commands/refine-plan.md:442-453`, `459-471`).
- dependencies_and_callers: Called directly from `commands/refine-plan.md`; the command is planning-only, limited to refined plan, QA document, and optional variants (`commands/refine-plan.md:19-28`). It reuses `gen-plan` schema and config-loader semantics (`commands/refine-plan.md:30-43`, `86-90`).
- edge_cases_or_failure_modes: Template has placeholders that must be fully replaced; unresolved items must appear under Remaining Decisions, original comments must be preserved verbatim in fenced blocks, identifiers must stay unchanged, and final status must be `converged` or `partially_converged` (`prompt-template/plan/refine-plan-qa-template.md:86-119`, `commands/refine-plan.md:487-505`).
- validation_or_tests: `tests/test-refine-plan.sh` verifies QA template coverage for title, required sections, ledger columns, input/output/QA metadata paths, and convergence status (`tests/test-refine-plan.sh:803-817`).
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6 unique item evidence sections above; item IDs are intentionally not repeated in this checklist to preserve one section per assigned ID.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`