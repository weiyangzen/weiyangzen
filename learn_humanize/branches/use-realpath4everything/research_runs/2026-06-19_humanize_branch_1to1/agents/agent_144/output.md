# agent_144 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-144 `file` `prompt-template/block/work-summary-missing.md`
- cursor: `[_]`
- core_role: This is a stop-hook block-message template used when an RLCR loop participant attempts to exit without creating the required work summary file. The file itself is not executable code, but it defines the remediation contract rendered into the hook’s blocking response. Its title and message establish the failure condition, and its only template variable is `{{SUMMARY_FILE}}`, the concrete path the worker must write before attempting exit again; see `prompt-template/block/work-summary-missing.md:1` and `prompt-template/block/work-summary-missing.md:3`-`8`.

- algorithmic_behavior: The executable gate lives in `hooks/loop-codex-stop-hook.sh`. The hook chooses the expected summary path based on phase: finalize phase expects `$LOOP_DIR/finalize-summary.md`, while normal rounds expect `$LOOP_DIR/round-${CURRENT_ROUND}-summary.md`; see `hooks/loop-codex-stop-hook.sh:750`-`756`. If that file does not exist, the hook renders this template through `load_and_render_safe` with `SUMMARY_FILE=$SUMMARY_FILE`; see `hooks/loop-codex-stop-hook.sh:759`-`767`. It then emits a JSON stop-hook response with `"decision": "block"`, the rendered Markdown as `"reason"`, and a phase-specific `"systemMessage"` before exiting; see `hooks/loop-codex-stop-hook.sh:769`-`783`. This means the template participates in the algorithm as the user-facing branch of the missing-summary gate, not as the predicate implementation.

- inputs_outputs_state: Input is the resolved `SUMMARY_FILE` variable supplied by the stop hook. The template renderer uses `{{VARIABLE_NAME}}` placeholders and single-pass substitution, keeping missing variables literal rather than recursively expanding values; see `hooks/lib/template-loader.sh:7`-`13` and `hooks/lib/template-loader.sh:48`-`56`. Output is rendered Markdown headed `# Work Summary Missing`, including the target path and a checklist of expected summary contents: implemented work, created/modified files, tests added/passed, and remaining items; see `prompt-template/block/work-summary-missing.md:10`-`16`. State transition is external: while the expected summary file is absent, loop exit is blocked; after the file exists, execution proceeds to later gates such as round contract validation, BitLesson delta validation, finalize completion, or Codex review; see `hooks/loop-codex-stop-hook.sh:786`-`838` and `hooks/loop-codex-stop-hook.sh:943`-`969`.

- gates_or_invariants: The invariant enforced by the call site is file existence at exactly the current phase’s expected path. The template’s instruction narrows remediation to writing the summary to `{{SUMMARY_FILE}}`, while write validators enforce that summaries are written in the active `.humanize/rlcr` loop directory and for the current round unless specifically allowlisted; see `hooks/loop-write-validator.sh:269`-`288` and `hooks/loop-write-validator.sh:303`-`325`. Finalize phase is special-cased: `finalize-summary.md` is allowed only in the active loop directory; see `hooks/loop-write-validator.sh:207`-`218`. The template does not validate summary content by itself. Its content bullets are advisory contract text for the worker, while separate validators/review logic handle later content and completion checks.

- dependencies_and_callers: Direct caller is `hooks/loop-codex-stop-hook.sh`, which loads `block/work-summary-missing.md` with `load_and_render_safe`; see `hooks/loop-codex-stop-hook.sh:763`-`767`. Rendering depends on `hooks/lib/template-loader.sh`, particularly `load_template`, `render_template`, and `load_and_render_safe`; see `hooks/lib/template-loader.sh:33`-`46`, `hooks/lib/template-loader.sh:56`-`136`, and `hooks/lib/template-loader.sh:185`-`211`. The active template directory is derived by `hooks/lib/loop-common.sh`, which sets `TEMPLATE_DIR` from the plugin root’s `prompt-template` directory; see `hooks/lib/loop-common.sh:243`-`246`. Related remediation-path validators live in `hooks/loop-write-validator.sh` and path helpers in `hooks/lib/loop-common.sh`, including round file detection and allowlisted historical summaries; see `hooks/lib/loop-common.sh:795`-`837`.

- edge_cases_or_failure_modes: If the template file is missing or renders empty, `load_and_render_safe` falls back to the shorter embedded message in the stop hook, so the gate still blocks but loses the richer “summary should include” checklist; see `hooks/loop-codex-stop-hook.sh:763`-`767` and `hooks/lib/template-loader.sh:194`-`210`. If `SUMMARY_FILE` were not supplied, the placeholder would remain literal because the renderer preserves missing placeholders; see `hooks/lib/template-loader.sh:115`-`121`. If the summary file exists but is empty or low quality, this missing-file gate passes because it checks `[[ ! -f "$SUMMARY_FILE" ]]` only; later validators or review stages must catch content defects. In finalize phase, this gate blocks before Codex review or finalize completion, so a missing `finalize-summary.md` prevents premature loop completion; see `hooks/loop-codex-stop-hook.sh:943`-`952`.

- validation_or_tests: The direct behavior is covered by finalize-phase negative tests. `tests/test-finalize-phase.sh` removes `finalize-summary.md`, invokes `hooks/loop-codex-stop-hook.sh`, and expects a blocking JSON response mentioning summary; see `tests/test-finalize-phase.sh:494`-`509`. The same test asserts that Codex is not invoked while this missing-summary gate is active, confirming this block short-circuits before review execution; see `tests/test-finalize-phase.sh:511`-`517`. Related write-path tests cover `finalize-summary.md` write allowance and round summary path restrictions through the validators, though they are not direct tests of this template text.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `USE_REALPATH4EVERYTHING-HZ-144`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`