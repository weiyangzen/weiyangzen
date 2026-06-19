# agent_154 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-154 `file` `prompt-template/claude/drift-replan-prompt.md`
- cursor: `[_]`
- core_role:
  `prompt-template/claude/drift-replan-prompt.md` is a Claude next-round prompt template for the RLCR loop’s mainline drift recovery path. It is not implementation logic itself, but it defines the recovery contract that the implementation agent must follow after Codex review judges consecutive rounds as stalled or regressed. Its core algorithmic role is to redirect the next implementation round away from normal issue-clearing and toward a single recovered mainline objective, with explicit blocking-vs-queued issue classification.

- algorithmic_behavior:
  The template starts by declaring "Drift Recovery Mode" and states that Codex judged recent implementation rounds as failing to advance the mainline (`prompt-template/claude/drift-replan-prompt.md:3-10`). It renders the consecutive stalled/regressed count and last mainline verdict via `{{STALL_COUNT}}` and `{{LAST_MAINLINE_VERDICT}}` (`:7-8`).
  
  The prompt then forces re-anchoring on the original plan by embedding `@{{PLAN_FILE}}` (`:12-16`). Before code changes, it requires the worker to re-read the plan, goal tracker, recent summaries/reviews, and rewrite the next round contract at `@{{ROUND_CONTRACT_FILE}}` (`:17-24`). The recovery contract must include exactly one recovered mainline objective, 1-2 target acceptance criteria, drift/stagnation root cause, blocking issues, queued out-of-scope issues, and criteria that would move the verdict back to `ADVANCED` (`:25-32`). Line `:33` is the hard procedural transition: implementation must not start until the recovery contract exists.
  
  The template defines a task-lane classification algorithm for the next round: every Task system task must carry one of `[mainline]`, `[blocking]`, or `[queued]` (`:35-40`). It constrains state transitions by making `[mainline]` plan-derived work the primary lane, allowing `[blocking]` only when it directly unblocks the recovered objective, and requiring non-blocking work to stay queued instead of replacing mainline work (`:42-47`).
  
  The Codex review result is injected between explicit HTML comments using `{{REVIEW_CONTENT}}` (`:48-52`), which gives the implementation agent the concrete failure evidence that triggered recovery. The final sections require reading/updating `@{{GOAL_TRACKER_FILE}}`, preserving immutable tracker content, recording drift cause if it changes planning, keeping blocking vs queued classification accurate, and making tracker and contract agree on the recovered objective (`:55-61`). Recovery guardrails prevent queued cleanup, scope expansion, silent direction changes, and require concrete blockers if a credible objective cannot be produced (`:63-68`).

- inputs_outputs_state:
  Inputs are template variables supplied by `hooks/loop-codex-stop-hook.sh` when drift recovery is required: `PLAN_FILE`, `REVIEW_CONTENT`, `GOAL_TRACKER_FILE`, `ROUND_CONTRACT_FILE`, `CURRENT_ROUND`, `STALL_COUNT`, and `LAST_MAINLINE_VERDICT` (`hooks/loop-codex-stop-hook.sh:2017-2026`). `CURRENT_ROUND` is passed but not consumed by this template, making it an unused render input for this specific file.
  
  Output is a rendered next-round prompt written to `$NEXT_PROMPT_FILE`, e.g. `.humanize/round-N-prompt.md`, by `load_and_render_safe` (`hooks/loop-codex-stop-hook.sh:2017-2026`). The rendered prompt is then further post-processed with optional BitLesson instructions, Agent Teams enforcement, open-question notice, footer, task routing reminder, push note, goal tracker update request, and optional Agent Teams continuation (`hooks/loop-codex-stop-hook.sh:2039-2149`).
  
  The surrounding state machine initializes `NEXT_MAINLINE_STALL_COUNT`, `NEXT_LAST_MAINLINE_VERDICT`, and `NEXT_DRIFT_STATUS` from current state (`hooks/loop-codex-stop-hook.sh:1779-1782`). During implementation-phase review, an `ADVANCED` verdict resets stall count to `0`, last verdict to `advanced`, and drift status to `normal` (`:1793-1798`). A `STALLED` or `REGRESSED` verdict increments the stall count and records the extracted verdict (`:1799-1801`). At `>=2` consecutive stalled/regressed rounds, `DRIFT_REPLAN_REQUIRED=true` and `NEXT_DRIFT_STATUS=replan_required`, causing this template to be rendered for the next round (`:1802-1807`). At `>=3`, the loop switches from recovery prompt generation to circuit breaker stop (`:1808-1810`, `:1910-1911`).

- gates_or_invariants:
  The prompt itself establishes several behavioral gates:
  - Normal issue-clearing behavior is explicitly disallowed for the recovery round (`prompt-template/claude/drift-replan-prompt.md:10`).
  - A recovery contract must exist before implementation starts (`:17-33`).
  - The recovery contract must contain exactly one recovered mainline objective (`:25-27`).
  - Only 1-2 target ACs should be selected to prove mainline progress (`:27`).
  - Blocking issues must directly block the recovered mainline objective; otherwise they must be queued (`:28-31`, `:42-47`).
  - The goal tracker and round contract must describe the same recovered objective (`:57-61`).
  - The round must not broaden scope, spend mostly on queued cleanup, or silently change the original approach (`:63-68`).
  
  The upstream state gate is based on a required review verdict. If implementation review output lacks a valid `Mainline Progress Verdict` and the last marker is not `STOP`, the hook blocks rather than updating drift state (`hooks/loop-codex-stop-hook.sh:1785-1791`). Verdict extraction accepts only unambiguous `ADVANCED`, `STALLED`, or `REGRESSED` values and returns `unknown` for ambiguous multi-verdict lines (`hooks/lib/loop-common.sh:634-662`). Drift status is normalized to either `replan_required` or `normal` (`hooks/lib/loop-common.sh:618-631`).

- dependencies_and_callers:
  Primary caller is `hooks/loop-codex-stop-hook.sh`, which chooses this template over `prompt-template/claude/next-round-prompt.md` when `DRIFT_REPLAN_REQUIRED=true` (`hooks/loop-codex-stop-hook.sh:2017-2028`). The hook renders it through `load_and_render_safe`, so a missing or empty template falls back to the inline `DRIFT_REPLAN_FALLBACK` prompt (`hooks/loop-codex-stop-hook.sh:2000-2015`, `:2017-2026`).
  
  Rendering depends on `hooks/lib/template-loader.sh`. Template syntax is `{{VARIABLE_NAME}}`; substitution is single-pass, missing variables remain literal placeholders, and variable values are not rescanned for nested placeholders (`hooks/lib/template-loader.sh:7-14`, `:48-56`, `:69-128`). This matters for `{{REVIEW_CONTENT}}`, because review text containing `{{...}}` cannot accidentally mutate the prompt during rendering.
  
  Drift state fields and enums are defined in `hooks/lib/loop-common.sh`: `mainline_stall_count`, `last_mainline_verdict`, `drift_status`, verdicts `advanced/stalled/regressed/unknown`, and drift statuses `normal/replan_required` (`hooks/lib/loop-common.sh:42-52`). State parsing defaults missing drift fields to `0`, `unknown`, and `normal` for legacy loops (`hooks/lib/loop-common.sh:489-518`, `:589-597`).
  
  A sibling stop template handles the next escalation level. After a third consecutive stalled/regressed round, the loop uses `prompt-template/block/mainline-drift-stop.md` through `stop_for_mainline_drift`, writes final drift state, ends the loop, and returns a block decision with "mainline drift circuit breaker triggered" (`hooks/loop-codex-stop-hook.sh:1383-1418`; `prompt-template/block/mainline-drift-stop.md:1-13`).

- edge_cases_or_failure_modes:
  If the review result omits a valid mainline verdict, the drift state machine refuses to proceed and emits a "Mainline Verdict Missing" block instead of rendering this recovery prompt (`hooks/loop-codex-stop-hook.sh:1421-1453`, `:1785-1791`). This protects against accidentally resetting or incrementing drift counters from malformed review output.
  
  If the template file is absent or renders empty, `load_and_render_safe` emits `DRIFT_REPLAN_FALLBACK`; the fallback preserves the core behavior but is less detailed than this file, lacking the full task-lane rules and goal tracker guardrails (`hooks/loop-codex-stop-hook.sh:2000-2015`; `hooks/lib/template-loader.sh:188-210`).
  
  If drift continues for a third consecutive stalled/regressed implementation round, the system no longer asks for another recovery round; it stops the loop through the mainline drift circuit breaker (`hooks/loop-codex-stop-hook.sh:1808-1810`, `:1910-1911`). That means this template is the second-strike recovery path, not the final-stop path.
  
  If `AGENT_TEAMS=true`, the generated drift prompt is modified after initial rendering: an Agent Teams delegation warning is injected near `## Original Implementation Plan`, and continuation instructions are appended later (`hooks/loop-codex-stop-hook.sh:2054-2076`, `:2145-2155`). Therefore consumers should treat the final prompt file as the rendered template plus post-processing, not a byte-for-byte render of this markdown file.
  
  The template passes through raw review content inside a marked block (`prompt-template/claude/drift-replan-prompt.md:48-52`). The single-pass renderer prevents placeholder injection from review content, but the prompt still relies on the agent following the boundary comments rather than treating embedded review prose as higher-priority instructions.

- validation_or_tests:
  `tests/test-finalize-phase.sh` validates the main state transition: with `mainline_stall_count: 1` and a new `Mainline Progress Verdict: STALLED`, the hook blocks exit, creates `round-4-prompt.md`, and the prompt contains "Drift Recovery Mode" (`tests/test-finalize-phase.sh:893-938`). The same test asserts state becomes `current_round=4`, `mainline_stall_count=2`, `last_mainline_verdict=stalled`, and `drift_status=replan_required` (`:940-946`).
  
  The same test file validates the third-strike escalation: starting from stall count `2` and drift status `replan_required`, a `REGRESSED` verdict creates `stop-state.md` and preserves `stall=3`, `verdict=regressed`, `drift=replan_required` (`tests/test-finalize-phase.sh:996-1039`).
  
  `tests/test-agent-teams.sh` verifies that a drift recovery prompt still preserves Agent Teams continuation when `agent_teams=true`, checking both "Drift Recovery Mode" and "Agent Teams" in the generated round prompt (`tests/test-agent-teams.sh:631-668`).
  
  `tests/robustness/test-state-file-robustness.sh` verifies that drift-tracking fields parse correctly from state frontmatter (`tests/robustness/test-state-file-robustness.sh:476-499`).

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 Item Evidence section for the single assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`