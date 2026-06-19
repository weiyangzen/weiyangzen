# agent_127 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-127 `file` `prompt-template/block/goal-tracker-not-initialized.md`
- cursor: `[_]`
- core_role:
  - This is a prompt/block template used as the user-facing stop-hook block when an RLCR loop reaches the Round 0 exit path while `goal-tracker.md` still contains uninitialized placeholders.
  - It is not executable by itself; its algorithmic role is to encode the remediation contract returned by the stop hook: initialize the immutable goal tracker content before attempting to exit Round 0.
  - The template title and trigger context are explicit at `prompt-template/block/goal-tracker-not-initialized.md:1-3`.

- algorithmic_behavior:
  - The template renders a blocking instruction with two dynamic slots:
    - `{{GOAL_TRACKER_FILE}}` at `prompt-template/block/goal-tracker-not-initialized.md:5` and `:9`.
    - `{{MISSING_ITEMS}}` at `prompt-template/block/goal-tracker-not-initialized.md:6`.
  - It instructs the agent to read the tracker, replace placeholder content, define or extract the ultimate goal, define 3-7 testable acceptance criteria, populate active tasks, and write the updated tracker at `prompt-template/block/goal-tracker-not-initialized.md:8-14`.
  - It also encodes the transition invariant that the immutable section can only be initialized in Round 0 and becomes read-only after that at `prompt-template/block/goal-tracker-not-initialized.md:16`.
  - The stop hook supplies this template only after it has detected one or more placeholder-bearing sections in the tracker. In `hooks/loop-codex-stop-hook.sh:849-880`, the hook extracts `Ultimate Goal`, `Acceptance Criteria`, and `Active Tasks` sections, then checks each for the generic placeholder pattern `[To be ...]`.
  - If any placeholder remains, the hook builds section-specific missing-item lines at `hooks/loop-codex-stop-hook.sh:882-895`, renders this template through `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:897-904`, and returns a JSON block decision at `hooks/loop-codex-stop-hook.sh:906-914`.

- inputs_outputs_state:
  - Inputs:
    - `GOAL_TRACKER_FILE`: active loop tracker path, set by the stop hook as `$LOOP_DIR/goal-tracker.md` at `hooks/loop-codex-stop-hook.sh:844`.
    - `MISSING_ITEMS`: newline-prefixed markdown bullets naming the still-placeholder sections, assembled at `hooks/loop-codex-stop-hook.sh:882-895`.
    - Template variables are resolved by the template loader, whose documented syntax is `{{VARIABLE_NAME}}` at `hooks/lib/template-loader.sh:7-13`.
  - Outputs:
    - Rendered markdown becomes the hook's `reason` field in a JSON response with `"decision": "block"` and system message `Loop: Goal Tracker not initialized in Round 0`, constructed at `hooks/loop-codex-stop-hook.sh:906-913`.
    - The rendered block directs the agent to update `goal-tracker.md`, then retry exit at `prompt-template/block/goal-tracker-not-initialized.md:18`.
  - State transitions:
    - Before this block: Round 0 stop evaluation is in progress and tracker initialization is incomplete.
    - After successful remediation: `goal-tracker.md` should no longer contain placeholder text in the checked sections, allowing the stop hook to continue beyond this gate.
    - The intended tracker transition is from generated placeholder scaffold to initialized immutable goal/acceptance criteria plus mutable active tasks. Normal setup can seed the placeholders at `scripts/setup-rlcr-loop.sh:1079-1092`, `:1097-1111`, and `:1128-1133`.

- gates_or_invariants:
  - Round gate: the initialization check applies only when not finalize phase, not review-started, current round is `0`, and the tracker exists. These conditions are enforced at `hooks/loop-codex-stop-hook.sh:846-849`.
  - Section-specific invariant: only placeholders inside the extracted target sections count; comments in the hook say this avoids coupling to exact wording and avoids false positives elsewhere at `hooks/loop-codex-stop-hook.sh:850-853`.
  - Immutable-section invariant: the template states the immutable section can only be set in Round 0 at `prompt-template/block/goal-tracker-not-initialized.md:16`. Later validators enforce preservation of the immutable section by extracting it and comparing proposed updates at `hooks/lib/loop-common.sh:920-963`.
  - Authoring invariant: the template says to write the updated tracker, but companion validators discourage Bash-based tracker modification. `hooks/lib/loop-common.sh:903-912` provides the Round 0 Bash-block message for goal-tracker writes, and post-Round 0 mutable-only rules are handled in the same library.
  - Placeholder syntax invariant: variables use uppercase `{{...}}` placeholders. The loader keeps unresolved variables as-is and uses single-pass substitution to prevent placeholder injection, documented at `hooks/lib/template-loader.sh:48-55` and implemented at `hooks/lib/template-loader.sh:69-128`.

- dependencies_and_callers:
  - Direct caller: `hooks/loop-codex-stop-hook.sh` loads `block/goal-tracker-not-initialized.md` through `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:902-904`.
  - Template engine dependency: `hooks/lib/template-loader.sh` provides `load_template`, `render_template`, and safe loading behavior. `load_template` reads from `$TEMPLATE_DIR/$template_name` at `hooks/lib/template-loader.sh:33-46`; `render_template` performs variable replacement at `hooks/lib/template-loader.sh:56-136`.
  - Upstream state producer: `scripts/setup-rlcr-loop.sh` creates `goal-tracker.md`. In normal mode it may populate placeholders when plan extraction fails or active tasks still need model initialization, shown at `scripts/setup-rlcr-loop.sh:1060-1156`.
  - Related skip path: skip-implementation trackers are generated with concrete review-only goals and no placeholder text at `scripts/setup-rlcr-loop.sh:931-1057`, which explains why the stop hook skips this check when review has already started.
  - Sibling templates in the same block family cover adjacent tracker gates, including `prompt-template/block/goal-tracker-bash-write.md` and `prompt-template/block/goal-tracker-modification.md`; these are referenced by `hooks/lib/loop-common.sh:903-912` and the later mutable-section block path around `hooks/lib/loop-common.sh:1512-1528`.

- edge_cases_or_failure_modes:
  - Missing template file: the caller supplies a short fallback block at `hooks/loop-codex-stop-hook.sh:897-901`, so a missing template does not crash the stop hook.
  - Missing variables: the renderer preserves unresolved `{{VAR}}` tokens rather than failing, documented at `hooks/lib/template-loader.sh:12-13` and implemented at `hooks/lib/template-loader.sh:114-121`.
  - Placeholder value injection: rendered values are not rescanned, so if `MISSING_ITEMS` contains `{{...}}`, it will not trigger a second substitution pass; this is intentional at `hooks/lib/template-loader.sh:52-55`.
  - Nonstandard headings: the hook looks for exact markdown headings beginning `### Ultimate Goal`, `### Acceptance Criteria`, and `#### Active Tasks` using `awk` ranges at `hooks/loop-codex-stop-hook.sh:859-879`. A malformed tracker with renamed headings may bypass this specific placeholder gate or produce incomplete missing-item diagnostics.
  - Placeholder pattern specificity: detection searches for `[To be ` followed by a lowercase letter at `hooks/loop-codex-stop-hook.sh:861-879`. Different placeholder wording or capitalization may not be caught by this gate.
  - File absence: if `goal-tracker.md` does not exist, this template is not used because the check requires `-f "$GOAL_TRACKER_FILE"` at `hooks/loop-codex-stop-hook.sh:849`.
  - Review/finalize bypass: finalize phase and review-started mode skip this gate by design at `hooks/loop-codex-stop-hook.sh:846-849`.

- validation_or_tests:
  - Direct static validation exists through comprehensive template tests. `tests/test-templates-comprehensive.sh:83-107` loads every markdown template, `tests/test-templates-comprehensive.sh:114-130` validates placeholder syntax, and `tests/test-templates-comprehensive.sh:575-605` renders every template with dummy values and checks for unreplaced placeholders.
  - Stop-hook behavior for this template’s missing-item payload is covered by section-specific tests:
    - Ultimate Goal only: `tests/test-plan-file-hooks.sh:841-914`.
    - Acceptance Criteria only: `tests/test-plan-file-hooks.sh:916-986`.
    - Active Tasks only: `tests/test-plan-file-hooks.sh:988-1056`.
    - All three placeholders: `tests/test-plan-file-hooks.sh:1058-1126`.
  - Setup robustness includes a skip-implementation regression that verifies skip mode creates tracker content without `[To be ...]` placeholders, referenced in search output at `tests/robustness/test-setup-scripts-robustness.sh:929-937`.
  - I inspected the assigned file directly with line numbers and confirmed its recorded size is 707 bytes via `wc -c`. I did not run the full test suite because this branch export is read-only and the task requested research notes only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 item section present; the single assigned item id is used only as that section heading`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`