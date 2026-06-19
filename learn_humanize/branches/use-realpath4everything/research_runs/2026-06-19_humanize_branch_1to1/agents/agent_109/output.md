# agent_109 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-109 `file` `prompt-template/block/bitlesson-delta-empty-kb.md`
- cursor: `[_]`
- core_role:
  - Blocking prompt template for the BitLesson stop-gate path when a round summary reports `Action: none` while the BitLesson knowledge base has no concrete lesson entries.
  - The file itself is static Markdown, not executable shell logic. Its algorithmic role is to supply the human-facing block reason rendered by `scripts/bitlesson-validate-delta.sh`.
  - Direct file content:
    - `prompt-template/block/bitlesson-delta-empty-kb.md:1` names the block: `BitLesson Recording Required`.
    - `prompt-template/block/bitlesson-delta-empty-kb.md:3` states that `Action: none` is disallowed because `.humanize/bitlesson.md` has no concrete lesson entries.
    - `prompt-template/block/bitlesson-delta-empty-kb.md:5` instructs the worker to add or update at least one reusable lesson and report `Action: add` or `Action: update`.

- algorithmic_behavior:
  - The template participates in the BitLesson delta validation branch implemented in `scripts/bitlesson-validate-delta.sh`.
  - The validator parses the submitted round summary’s `## BitLesson Delta` block, extracts `Action:` and `Lesson ID(s):`, then counts concrete lesson entries in the configured BitLesson file.
  - When `BITLESSON_ACTION == "none"`, the validator first rejects non-empty/non-`NONE` lesson IDs as inconsistent at `scripts/bitlesson-validate-delta.sh:242-251`.
  - It then checks the empty-knowledge-base strict gate at `scripts/bitlesson-validate-delta.sh:254`: if `CONCRETE_BITLESSON_COUNT == 0` and `BITLESSON_ALLOW_EMPTY_NONE != "true"`, it renders this assigned template through `load_and_render_safe` at `scripts/bitlesson-validate-delta.sh:263-265`.
  - The resulting rendered Markdown becomes the JSON block reason returned by `block_exit` at `scripts/bitlesson-validate-delta.sh:266`.
  - `block_exit` emits a structured JSON object with `decision: "block"`, `reason`, and `systemMessage`, then exits successfully at `scripts/bitlesson-validate-delta.sh:78-90`. That means this is a validation block signal rather than a process error.

- inputs_outputs_state:
  - Inputs to the template itself:
    - No active placeholders are present in the assigned file. It hard-codes `.humanize/bitlesson.md` and “this round”.
    - The invoking validator still passes `CURRENT_ROUND=$CURRENT_ROUND` and `BITLESSON_FILE=$BITLESSON_FILE_REL` at `scripts/bitlesson-validate-delta.sh:263-265`, but those variables are unused by this template.
  - Inputs to the gate that selects the template:
    - `--summary-file`, `--bitlesson-file`, `--bitlesson-relpath`, `--allow-empty-none`, `--template-dir`, and `--current-round` are required CLI arguments at `scripts/bitlesson-validate-delta.sh:6-13`.
    - Required argument validation happens at `scripts/bitlesson-validate-delta.sh:62-67`.
    - The summary file must exist, checked at `scripts/bitlesson-validate-delta.sh:69-72`.
    - The BitLesson knowledge base count is derived by scanning `Lesson ID:` lines and ignoring placeholders such as `<BL-YYYYMMDD-short-name>` at `scripts/bitlesson-validate-delta.sh:227-239`.
  - Outputs:
    - Rendered Markdown block reason text.
    - Structured JSON from `block_exit`, with `decision` set to `block`.
    - System message: `Loop: BitLesson entry required for non-zero round (round $CURRENT_ROUND)` from `scripts/bitlesson-validate-delta.sh:266`.
  - State transitions:
    - No repository state is modified by the template or validator.
    - Workflow state transition is external: the stop gate blocks completion until the worker changes the round summary from `Action: none` to `Action: add` or `Action: update` and adds/updates a matching concrete entry in `.humanize/bitlesson.md`.
    - This aligns with the documented BitLesson workflow: `.humanize/bitlesson.md` is the project knowledge base at `docs/bitlesson.md:27`, and the stop gate validates the required delta section at `docs/bitlesson.md:34`.

- gates_or_invariants:
  - `Action: none` is allowed only when `Lesson ID(s)` is `NONE` or empty, per `docs/bitlesson.md:49` and the validator branch at `scripts/bitlesson-validate-delta.sh:242-251`.
  - `Action: add` and `Action: update` must reference concrete `BL-YYYYMMDD-short-name` IDs that exist in `.humanize/bitlesson.md`, documented at `docs/bitlesson.md:50` and enforced downstream at `scripts/bitlesson-validate-delta.sh:269-383`.
  - The strict empty-KB gate is controlled by `--require-bitlesson-entry-for-none` / `--allow-empty-none`; docs state this mode blocks empty knowledge bases from repeatedly reporting `none` at `docs/bitlesson.md:51`.
  - The concrete lesson count ignores placeholder IDs, so a template-only `.humanize/bitlesson.md` does not satisfy the gate.
  - The assigned template encodes the remediation invariant: resolving previously discovered issues should produce reusable knowledge, not another `none` delta.

- dependencies_and_callers:
  - Direct caller:
    - `scripts/bitlesson-validate-delta.sh:263` calls `load_and_render_safe "$TEMPLATE_DIR" "block/bitlesson-delta-empty-kb.md"`.
  - Template loading dependency:
    - `scripts/bitlesson-validate-delta.sh:76` sources `hooks/lib/template-loader.sh`.
    - `hooks/lib/template-loader.sh:188-210` defines `load_and_render_safe`, which loads the template, renders placeholders if present, and falls back if the file is missing or empty.
    - `hooks/lib/template-loader.sh:56-135` defines single-pass `{{VAR}}` rendering, preserving missing placeholders.
  - Stop-hook caller path:
    - `hooks/loop-codex-stop-hook.sh:824-831` invokes `scripts/bitlesson-validate-delta.sh` and treats failure of the validator script itself as an error. The validator’s normal block response is JSON, not a nonzero shell failure.
  - Workflow documentation:
    - `docs/bitlesson.md:36-45` defines the required summary block shape.
    - `commands/start-rlcr-loop.md:177-180` instructs users to include `## BitLesson Delta` and notes that strict empty-KB blocking is opt-in through `--require-bitlesson-entry-for-none`.
  - Sibling templates:
    - The file sits beside other BitLesson block templates in `prompt-template/block/`, including `bitlesson-delta-missing.md`, `bitlesson-delta-invalid.md`, `bitlesson-delta-inconsistent.md`, and `bitlesson-delta-missing-notes.md`. Those handle adjacent validation branches.

- edge_cases_or_failure_modes:
  - Static path wording:
    - The assigned template hard-codes `.humanize/bitlesson.md`; if the validator is called with a different `--bitlesson-relpath`, the rendered block reason will not reflect that. The fallback message in `scripts/bitlesson-validate-delta.sh:255-261` does use `{{BITLESSON_FILE}}`, but the actual template does not.
  - Static round wording:
    - The template says “this round” and does not use `{{CURRENT_ROUND}}`; the fallback includes the round number placeholder. The JSON `systemMessage` still includes the concrete round at `scripts/bitlesson-validate-delta.sh:266`.
  - Missing or empty template:
    - `load_and_render_safe` falls back to the embedded validator fallback if the file is absent or renders empty, per `hooks/lib/template-loader.sh:194-210`.
  - Placeholder-only knowledge base:
    - A `.humanize/bitlesson.md` with only sample placeholder IDs remains empty for this gate because placeholder IDs are excluded at `scripts/bitlesson-validate-delta.sh:234`.
  - Missing BitLesson file:
    - If `--bitlesson-file` does not exist, `CONCRETE_BITLESSON_COUNT` stays `0` at `scripts/bitlesson-validate-delta.sh:227-240`, so strict mode blocks `Action: none`.
  - Potential branch relevance:
    - For a branch named `use-realpath4everything`, this template is a mild skip candidate for path-normalization algorithm work because it does not compute or resolve paths. However, it is still part of the core stop-gate contract and can surface path text to users, so it remains relevant to review.

- validation_or_tests:
  - Direct validation coverage exists for the validator script:
    - `tests/test-bitlesson-validate-delta.sh` is dedicated to `bitlesson-validate-delta.sh`.
  - Template reference safety is covered:
    - `tests/test-template-references.sh` scans `load_template`, `load_and_render`, and `load_and_render_safe` references and checks critical validators use safe rendering.
  - Template loader behavior is covered:
    - `tests/test-template-loader.sh` covers `render_template` and `load_and_render_safe`, including missing-template fallback.
    - Robustness coverage exists in `tests/robustness/test-template-stress-robustness.sh` and `tests/robustness/test-template-error-robustness.sh`.
  - I did not run test scripts because this assignment requested read-only research notes only, and the workspace is read-only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 Item Evidence section present`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`