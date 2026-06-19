# agent_118 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-118 `file` `prompt-template/codex/regular-review.md`
- cursor: `[_]`
- core_role:
  - `prompt-template/codex/regular-review.md` is the regular Codex review prompt for the RLCR loop. It is not executable code, but it defines the review gate contract that determines whether Claude continues another implementation round or is allowed to advance toward code review/finalization.
  - The template’s core role is to force Codex to compare Claude’s claimed completion against the original plan, current round prompt, docs, and goal tracker, and to emit either concrete review findings or the terminal `COMPLETE` marker only when no original-plan work, acceptance criteria, deferrals, or pending tasks remain.
  - The template is selected for non-full-alignment rounds by `hooks/loop-codex-stop-hook.sh`. The hook branches to `codex/full-alignment-review.md` only when the modulo full-review interval matches; otherwise it renders this regular-review template at `hooks/loop-codex-stop-hook.sh:816` through `hooks/loop-codex-stop-hook.sh:846`.

- algorithmic_behavior:
  - The prompt begins by requiring Codex to read the original implementation plan first: `@{{PLAN_FILE}}` is named at `prompt-template/codex/regular-review.md:5` through `prompt-template/codex/regular-review.md:8`. This makes plan conformance the first review input, not Claude’s summary.
  - It then provides the current round prompt as another input, stating that Claude claims completion based on the original plan and `@{{PROMPT_FILE}}` at `prompt-template/codex/regular-review.md:11`.
  - Claude’s work summary is injected between explicit start/end comments at `prompt-template/codex/regular-review.md:14` through `prompt-template/codex/regular-review.md:17`.
  - Part 1 directs Codex to perform a skeptical implementation review focused on discrepancies between plan design and actual implementation at `prompt-template/codex/regular-review.md:20` through `prompt-template/codex/regular-review.md:31`.
  - A key algorithmic rule is that deferrals are not accepted as progress: if Claude deferred planned tasks, Codex must flag them and draft a singular, directive implementation plan for Claude to execute now, not later. This behavior is encoded at `prompt-template/codex/regular-review.md:24` through `prompt-template/codex/regular-review.md:31`.
  - Part 2 requires goal alignment checking against `@{{GOAL_TRACKER_FILE}}`, including acceptance-criteria progress, forgotten original-plan items, deferrals, and plan evolution validity at `prompt-template/codex/regular-review.md:33` through `prompt-template/codex/regular-review.md:45`.
  - Part 3 is a rendered insertion point: `## Part 3: {{GOAL_TRACKER_UPDATE_SECTION}}` at `prompt-template/codex/regular-review.md:47`. The inserted section comes from `prompt-template/codex/goal-tracker-update-section.md`, which makes Codex responsible for evaluating and applying Claude’s requested goal-tracker updates while never modifying the immutable goal/acceptance-criteria section.
  - Part 4 defines the output contract: findings go to `@{{REVIEW_RESULT_FILE}}` when there are mismatches or pending work, and `COMPLETE` may be the last line only when all original-plan tasks and acceptance criteria are fully done with no deferrals or pending work. This contract is at `prompt-template/codex/regular-review.md:49` through `prompt-template/codex/regular-review.md:57`.

- inputs_outputs_state:
  - Template inputs are supplied by `hooks/loop-codex-stop-hook.sh` during rendering:
    - `CURRENT_ROUND`, used in the title at `prompt-template/codex/regular-review.md:1`.
    - `PLAN_FILE`, used at `prompt-template/codex/regular-review.md:6`.
    - `PROMPT_FILE`, used at `prompt-template/codex/regular-review.md:11`.
    - `SUMMARY_CONTENT`, injected at `prompt-template/codex/regular-review.md:16`.
    - `GOAL_TRACKER_FILE`, used at `prompt-template/codex/regular-review.md:35`.
    - `DOCS_PATH`, used at `prompt-template/codex/regular-review.md:23`.
    - `GOAL_TRACKER_UPDATE_SECTION`, inserted at `prompt-template/codex/regular-review.md:47`.
    - `REVIEW_RESULT_FILE`, used at `prompt-template/codex/regular-review.md:52`.
  - The caller creates the concrete loop paths before rendering: `PROMPT_FILE`, `REVIEW_PROMPT_FILE`, and `REVIEW_RESULT_FILE` are assigned at `hooks/loop-codex-stop-hook.sh:761` through `hooks/loop-codex-stop-hook.sh:763`; `SUMMARY_CONTENT` is read at `hooks/loop-codex-stop-hook.sh:765`.
  - The rendered output of this template becomes `$REVIEW_PROMPT_FILE` via `load_and_render_safe ... > "$REVIEW_PROMPT_FILE"` at `hooks/loop-codex-stop-hook.sh:834` through `hooks/loop-codex-stop-hook.sh:846`.
  - The review agent’s expected output is `$REVIEW_RESULT_FILE`. If Codex writes review content to stdout instead, the hook copies stdout into the review result file as a fallback at `hooks/loop-codex-stop-hook.sh:1330` through `hooks/loop-codex-stop-hook.sh:1346`.
  - State transition on `COMPLETE`: the hook reads `$REVIEW_RESULT_FILE`, trims the last non-empty line, and checks it exactly against the completion marker at `hooks/loop-codex-stop-hook.sh:1385` through `hooks/loop-codex-stop-hook.sh:1395`. If complete and not already in review phase, it either stops at max iterations or sets `review_started: true`, creates `.review-phase-started`, and runs the follow-up `codex review` gate at `hooks/loop-codex-stop-hook.sh:1401` through `hooks/loop-codex-stop-hook.sh:1433`.
  - State transition on non-complete regular review: the hook increments `current_round`, creates the next round prompt, embeds the review feedback, and returns a block decision at `hooks/loop-codex-stop-hook.sh:1505` through `hooks/loop-codex-stop-hook.sh:1569`.
  - State transition after follow-up code review: `run_and_handle_code_review` treats Codex review command failure or no output as blocking, review findings as another review-loop round, and no issues as entry to finalize phase at `hooks/loop-codex-stop-hook.sh:999` through `hooks/loop-codex-stop-hook.sh:1027`.

- gates_or_invariants:
  - `COMPLETE` is a strict last-line marker. The hook uses the last non-empty line only, trims whitespace, and compares it exactly to the completion marker at `hooks/loop-codex-stop-hook.sh:1388` through `hooks/loop-codex-stop-hook.sh:1395`. This prevents text like “cannot complete” from accidentally passing.
  - The template itself forbids `COMPLETE` when any original-plan task is deferred, unfinished, or not fully implemented at `prompt-template/codex/regular-review.md:53` through `prompt-template/codex/regular-review.md:56`.
  - The template requires goal alignment summary counts in the form `ACs: X/Y addressed | Forgotten items: N | Unjustified deferrals: N` at `prompt-template/codex/regular-review.md:42` through `prompt-template/codex/regular-review.md:45`. This gives a compact acceptance-criteria and deferral gate in the review output.
  - The inserted goal-tracker update section adds an invariant that the immutable Ultimate Goal and Acceptance Criteria must not be modified; see `prompt-template/codex/goal-tracker-update-section.md:6` through `prompt-template/codex/goal-tracker-update-section.md:10`.
  - The hook validates state before this prompt is rendered. It blocks missing `current_round` and `max_iterations`, invalid numeric round values, invalid Codex model/effort strings, and outdated schema fields at `hooks/loop-codex-stop-hook.sh:118` through `hooks/loop-codex-stop-hook.sh:208`.
  - Regular review is skipped in favor of full alignment review on configured alignment rounds. `FULL_REVIEW_ROUND` is validated/defaulted at `hooks/loop-codex-stop-hook.sh:773` through `hooks/loop-codex-stop-hook.sh:783`, then the regular template is used only in the `else` branch at `hooks/loop-codex-stop-hook.sh:831` through `hooks/loop-codex-stop-hook.sh:846`.
  - Template rendering is single-pass: placeholder values containing `{{...}}` are not recursively expanded. This avoids prompt corruption or placeholder injection from summary/review content; see `hooks/lib/template-loader.sh:50` through `hooks/lib/template-loader.sh:132`.

- dependencies_and_callers:
  - Direct caller: `hooks/loop-codex-stop-hook.sh`, which renders `codex/regular-review.md` with `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:834` through `hooks/loop-codex-stop-hook.sh:846`.
  - Rendering dependency: `hooks/lib/template-loader.sh`. `load_and_render_safe` loads the template, falls back when missing/empty, renders variables, and returns rendered content at `hooks/lib/template-loader.sh:167` through `hooks/lib/template-loader.sh:203`.
  - Loader initialization dependency: `hooks/lib/loop-common.sh` sources `template-loader.sh`, sets `TEMPLATE_DIR`, and validates the template directory at `hooks/lib/loop-common.sh:139` through `hooks/lib/loop-common.sh:149`.
  - Marker dependency: `hooks/lib/loop-common.sh` defines the completion and stop markers at `hooks/lib/loop-common.sh:30` through `hooks/lib/loop-common.sh:32`.
  - Runtime dependency: Codex CLI. The hook checks for `codex` and blocks with install guidance if missing at `hooks/loop-codex-stop-hook.sh:855` through `hooks/loop-codex-stop-hook.sh:875`.
  - Runtime invocation: the rendered prompt is sent to `codex exec` with model, reasoning effort, full-auto mode, and project root at `hooks/loop-codex-stop-hook.sh:891` through `hooks/loop-codex-stop-hook.sh:897` and `hooks/loop-codex-stop-hook.sh:1248` through `hooks/loop-codex-stop-hook.sh:1273`.
  - Related template dependency: `prompt-template/codex/goal-tracker-update-section.md` is rendered into Part 3 via `GOAL_TRACKER_UPDATE_SECTION`, built at `hooks/loop-codex-stop-hook.sh:767` through `hooks/loop-codex-stop-hook.sh:771`.
  - Sibling templates coordinate the larger loop: `prompt-template/codex/full-alignment-review.md` handles scheduled full alignment rounds; `prompt-template/claude/next-round-prompt.md` receives review feedback when regular review does not pass; `prompt-template/claude/finalize-phase-prompt.md` is used after review gates pass.

- edge_cases_or_failure_modes:
  - Missing template file: `load_and_render_safe` falls back to `REGULAR_REVIEW_FALLBACK`, defined at `hooks/loop-codex-stop-hook.sh:805` through `hooks/loop-codex-stop-hook.sh:814`, rather than producing an empty prompt.
  - Empty rendered template: `load_and_render_safe` also uses fallback if rendering returns empty content at `hooks/lib/template-loader.sh:189` through `hooks/lib/template-loader.sh:199`.
  - Missing substitution values: the template loader keeps unresolved placeholders literally, per `hooks/lib/template-loader.sh:12` through `hooks/lib/template-loader.sh:14` and implementation at `hooks/lib/template-loader.sh:115` through `hooks/lib/template-loader.sh:122`. That means a caller omission does not crash rendering, but may weaken review instructions by leaving raw placeholders in the prompt.
  - Codex execution failure: nonzero `codex exec` exit blocks the loop and reports debug files at `hooks/loop-codex-stop-hook.sh:1283` through `hooks/loop-codex-stop-hook.sh:1328`.
  - Review result missing: if neither `$REVIEW_RESULT_FILE` nor stdout content exists, the hook blocks with an explicit “review result file not created” failure at `hooks/loop-codex-stop-hook.sh:1348` through `hooks/loop-codex-stop-hook.sh:1374`.
  - Empty review result: a created-but-empty result file blocks at `hooks/loop-codex-stop-hook.sh:1376` through `hooks/loop-codex-stop-hook.sh:1383`.
  - `COMPLETE` before max iteration but follow-up `codex review` fails: the hook blocks and preserves review phase state rather than finalizing; the behavior is implemented at `hooks/loop-codex-stop-hook.sh:1005` through `hooks/loop-codex-stop-hook.sh:1023`.
  - `STOP` during a non-alignment regular round is treated as unusual but honored as a circuit-breaker termination at `hooks/loop-codex-stop-hook.sh:1471` through `hooks/loop-codex-stop-hook.sh:1498`, even though this regular-review template only instructs `COMPLETE`, not `STOP`.
  - Review phase tampering: if `review_started: true` is set without `.review-phase-started`, the hook blocks as inconsistent state at `hooks/loop-codex-stop-hook.sh:1446` through `hooks/loop-codex-stop-hook.sh:1462`.

- validation_or_tests:
  - Template existence/reference validation: `tests/test-template-references.sh` scans shell calls to `load_template`, `load_and_render`, and `load_and_render_safe`, extracts referenced template paths, and fails missing files at `tests/test-template-references.sh:83` through `tests/test-template-references.sh:110`. This covers the hook reference to `codex/regular-review.md`.
  - Comprehensive template loading/syntax validation: `tests/test-templates-comprehensive.sh` loads every Markdown template under `prompt-template/` at `tests/test-templates-comprehensive.sh:83` through `tests/test-templates-comprehensive.sh:107`, then checks placeholder syntax for malformed braces, spaces, and lowercase names at `tests/test-templates-comprehensive.sh:113` through `tests/test-templates-comprehensive.sh:194`.
  - Template loader unit tests: `tests/test-template-loader.sh` verifies `get_template_dir`, loading existing/missing files, variable replacement, multiline rendering, unreplaced variable preservation, and safe fallback behavior at `tests/test-template-loader.sh:41` through `tests/test-template-loader.sh:222`.
  - Review-loop transition tests: `tests/test-finalize-phase.sh` verifies that a mock `COMPLETE` response triggers transition toward finalize/review behavior at `tests/test-finalize-phase.sh:510` through `tests/test-finalize-phase.sh:540`; it also verifies code-review failure after `COMPLETE` blocks finalization at `tests/test-finalize-phase.sh:566` through `tests/test-finalize-phase.sh:619`, and empty follow-up review output blocks at `tests/test-finalize-phase.sh:625` through `tests/test-finalize-phase.sh:670`.
  - Non-complete behavior is tested in `tests/test-finalize-phase.sh`: mock review feedback ending with `CONTINUE` keeps `state.md`, increments `current_round`, creates the review result file, and includes review feedback in the block output at `tests/test-finalize-phase.sh:747` through `tests/test-finalize-phase.sh:815`.
  - I did not run tests in this read-only branch export; I inspected test coverage and code paths only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: TUNABLE_FULL_EXAMINE_ROUND-HZ-118
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`