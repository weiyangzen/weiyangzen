# agent_116 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-116 `file` `prompt-template/block/finalize-contract-access.md`
- cursor: `[_]`
- core_role: This is a block-message template used by RLCR hook validators when a user or agent tries to access a historical `round-N-contract.md` after the loop has entered Finalize Phase. The file is not executable code, but it is part of the algorithmic guard surface because it communicates the enforced state transition: once Finalize Phase is active, the active contract surface is gone and notes must move to `finalize-summary.md` or `goal-tracker.md`. See `prompt-template/block/finalize-contract-access.md:1` for the block title and `prompt-template/block/finalize-contract-access.md:3` for the phase rule.

- algorithmic_behavior: The template provides the human-facing reason emitted by `finalize_contract_blocked_message` in `hooks/lib/loop-common.sh:877-890`. That helper supplies the `ACTION` variable, loads `block/finalize-contract-access.md`, and renders `{{ACTION}}` into the line that says not to perform that action on historical round contract files. The concrete template body has three behavioral instructions: no active `round-N-contract.md` exists during Finalize Phase, do not perform the requested action on historical contracts, use `finalize-summary.md` for finalize notes, and use `goal-tracker.md` for current mainline/backlog state (`prompt-template/block/finalize-contract-access.md:3-7`).

- inputs_outputs_state: Input is a single template variable, `ACTION`, passed by the caller as values matching the blocked tool path: `read`, `write to`, or `edit` (`hooks/loop-read-validator.sh:218-220`, `hooks/loop-write-validator.sh:220-223`, `hooks/loop-edit-validator.sh:171-173`). Rendering uses the shared loader in `hooks/lib/template-loader.sh`, where placeholders use `{{VARIABLE_NAME}}` syntax and missing variables remain literal (`hooks/lib/template-loader.sh:7-14`). Output is Markdown text printed to stderr by the validators before they block with exit code `2`. State is not mutated by this template. The phase state is detected outside the template by resolving the active state file and checking whether it is `finalize-state.md` (`hooks/loop-read-validator.sh:204-209`, `hooks/loop-write-validator.sh:173-178`, `hooks/loop-edit-validator.sh:137-142`).

- gates_or_invariants: The invariant enforced by callers is: if the active loop state resolves to `finalize-state.md`, then any path matching `round-[0-9]+-contract.md` is blocked. The round-contract path predicate is `is_round_file_type`, implemented with a lowercase path regex ending in `round-[0-9]+-${file_type}.md` (`hooks/lib/loop-common.sh:795-802`). The active state resolver prefers `methodology-analysis-state.md`, then `finalize-state.md`, then `state.md` (`hooks/lib/loop-common.sh:264-279`), so this particular finalize-contract gate triggers only when `finalize-state.md` is the selected active state. Validators parse the state strictly before applying the block; malformed state fails closed with exit code `1` rather than showing this template (`hooks/loop-read-validator.sh:211-215`, `hooks/loop-write-validator.sh:180-184`, `hooks/loop-edit-validator.sh:144-148`, and strict parsing rules in `hooks/lib/loop-common.sh:525-600`).

- dependencies_and_callers: Direct dependency is the template renderer: `load_and_render_safe "$TEMPLATE_DIR" "block/finalize-contract-access.md" ... "ACTION=$action"` in `hooks/lib/loop-common.sh:888-889`. The renderer loads from `prompt-template`, performs single-pass awk substitution, and falls back to a hardcoded message if the template is missing or renders empty (`hooks/lib/template-loader.sh:56-136`, `hooks/lib/template-loader.sh:185-211`). Direct callers are the read, write, and edit validators. The read validator blocks Finalize Phase contract reads (`hooks/loop-read-validator.sh:218-220`), the write validator blocks contract writes after allowing the active `finalize-summary.md` path (`hooks/loop-write-validator.sh:207-223`), and the edit validator blocks contract edits (`hooks/loop-edit-validator.sh:171-173`). The only repository-wide direct reference to the file name is that helper call, plus the fallback copy in `loop-common.sh`.

- edge_cases_or_failure_modes: If `ACTION` is not supplied, the placeholder remains as `{{ACTION}}` because missing variables are preserved by the template renderer (`hooks/lib/template-loader.sh:12-13`), but all current callers pass an action. If the template file is absent or empty, `load_and_render_safe` emits the fallback text in `finalize_contract_blocked_message` (`hooks/lib/loop-common.sh:881-886`, `hooks/lib/template-loader.sh:197-207`). If a contract path is uppercase or mixed-case, validators lower-case the path before calling `is_round_file_type`, so matching should still work through the lowercase path variable used at call sites. If the path is not exactly `round-<digits>-contract.md` at the end, this block does not apply because the regex is anchored (`hooks/lib/loop-common.sh:801`). If `methodology-analysis-state.md` is present, `resolve_active_state_file` selects it before `finalize-state.md`, so the finalize-contract message is not selected under that active phase.

- validation_or_tests: Targeted tests cover all three validator paths. `tests/test-finalize-phase.sh:410-419` asserts that the write validator blocks `round-5-contract.md` during Finalize Phase with exit code `2` and a contract-related message. `tests/test-finalize-phase.sh:434-443` does the same for the edit validator. `tests/test-finalize-phase.sh:1078-1088` does the same for the read validator. These tests validate the observable gate and message category, not the exact Markdown wording of `prompt-template/block/finalize-contract-access.md`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 Item Evidence section present for the single assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`