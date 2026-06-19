# agent_101 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-101 `file` `prompt-template/block/work-summary-missing.md`
- cursor: `[_]`
- core_role: This is a stop-gate prompt block used when the RLCR/Codex loop detects that the required work summary file has not been written. The file itself is not an algorithm implementation, but it defines the user-facing contract for a mandatory lifecycle transition: an attempted exit is blocked until a summary exists at the expected path. Direct content is in `prompt-template/block/work-summary-missing.md:1-16`.

- algorithmic_behavior: The template renders a blocking instruction headed “Work Summary Missing” and tells the agent that it attempted to exit without writing the required work summary. Its only dynamic field is `{{SUMMARY_FILE}}`, shown inside a fenced block at `prompt-template/block/work-summary-missing.md:5-8`. It also defines the minimum summary payload: implemented work, files created or modified, tests added or passed, and remaining items at `prompt-template/block/work-summary-missing.md:10-14`. After the summary is written, the template permits another exit attempt at `prompt-template/block/work-summary-missing.md:16`. The actual decision logic lives in `hooks/loop-codex-stop-hook.sh`: the hook chooses `finalize-summary.md` in finalize phase or `round-${CURRENT_ROUND}-summary.md` otherwise, then blocks if that file is missing at `hooks/loop-codex-stop-hook.sh:609-617`.

- inputs_outputs_state: Input is the rendered variable `SUMMARY_FILE`, passed by the stop hook via `load_and_render_safe "$TEMPLATE_DIR" "block/work-summary-missing.md" ... "SUMMARY_FILE=$SUMMARY_FILE"` at `hooks/loop-codex-stop-hook.sh:620-624`. Template rendering uses the shared loader’s `{{VARIABLE_NAME}}` placeholder model, documented at `hooks/lib/template-loader.sh:7-13`, and performs single-pass environment-backed substitution at `hooks/lib/template-loader.sh:58-129`. Output is markdown text assigned to `REASON`, then embedded into a JSON stop-hook response with `"decision": "block"`, `"reason": $reason`, and a phase-specific `"systemMessage"` at `hooks/loop-codex-stop-hook.sh:626-640`. State transition is external to the template: missing summary keeps the loop in blocked-stop state; creating the expected summary file allows the hook to continue past this gate into later checks.

- gates_or_invariants: The invariant is “no exit without the expected summary file.” The gate is file-existence based only: `[[ ! -f "$SUMMARY_FILE" ]]` at `hooks/loop-codex-stop-hook.sh:616`. The expected path changes by phase: finalize phase requires `$LOOP_DIR/finalize-summary.md`, normal phase requires `$LOOP_DIR/round-${CURRENT_ROUND}-summary.md` at `hooks/loop-codex-stop-hook.sh:609-614`. The template requires the rendered summary destination to be explicit and keeps the action narrowly scoped to writing that summary. The loader preserves unresolved placeholders if a variable is missing, per `hooks/lib/template-loader.sh:115-121`, so the hook must supply `SUMMARY_FILE` for a useful message.

- dependencies_and_callers: The direct caller is `hooks/loop-codex-stop-hook.sh`, which loads this block from `$TEMPLATE_DIR` and falls back to a shorter inline message if the template is missing or renders empty at `hooks/loop-codex-stop-hook.sh:620-624`. Fallback behavior is implemented by `load_and_render_safe` in `hooks/lib/template-loader.sh:167-203`. The template directory is resolved through the hook/common template infrastructure; `get_template_dir` maps a plugin root to `prompt-template` at `hooks/lib/template-loader.sh:24-31`. Related validators coordinate with the same summary contract: the write validator explicitly allows `finalize-summary.md` in the active loop directory before broader summary-location checks at `hooks/loop-write-validator.sh:162-172`.

- edge_cases_or_failure_modes: If the template file is missing or empty, the hook falls back to an inline “Work Summary Missing” message, so the gate still blocks but with reduced guidance (`hooks/loop-codex-stop-hook.sh:620-624`, `hooks/lib/template-loader.sh:176-199`). If `SUMMARY_FILE` is not passed, the template would leave `{{SUMMARY_FILE}}` unresolved because missing variables are retained, not blanked (`hooks/lib/template-loader.sh:115-121`). The gate checks only existence, not whether the summary contains the four requested sections or meaningful content. A wrong phase or stale state file can point the required summary path at `finalize-summary.md` instead of a round summary, or vice versa; the template simply reflects the path chosen by the hook. The hook exits with JSON decision `block` but shell exit code `0` at `hooks/loop-codex-stop-hook.sh:632-640`, so callers must inspect the JSON decision rather than treating process success as permission to exit.

- validation_or_tests: `tests/test-finalize-phase.sh` covers the finalize-phase missing-summary path by removing `finalize-summary.md`, invoking `hooks/loop-codex-stop-hook.sh`, and asserting the JSON contains a block decision and summary-related message at `tests/test-finalize-phase.sh:429-443`. The same test asserts Codex is not called when the summary gate fails, confirming this gate short-circuits before review execution at `tests/test-finalize-phase.sh:446-451`. Broader template infrastructure tests describe coverage for loading all templates, rendering behavior, edge cases, fallback mechanisms, and placeholder syntax at `tests/test-templates-comprehensive.sh:3-10`, but I did not find a targeted test that validates every line or required bullet in this specific `work-summary-missing.md` block.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1/1; the sole assigned item is represented once in the Item Evidence section
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`