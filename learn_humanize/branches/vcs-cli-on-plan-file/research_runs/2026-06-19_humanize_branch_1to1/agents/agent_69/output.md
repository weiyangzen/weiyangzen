# agent_69 vcs-cli-on-plan-file 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `4dd1ca2fece39d3c6d7f84965cd71bda02489397`

## Item Evidence

### VCS_CLI_ON_PLAN_FILE-HZ-069 `file` `prompt-template/codex/goal-tracker-update-section.md`
- cursor: `[_]`
- core_role: This file is a Codex review-prompt fragment that defines the handoff contract for goal-tracker mutations after Round 0. Its role is not to execute updates directly, but to instruct Codex to adjudicate Claude’s “Goal Tracker Update Request” summary section and, if justified, update the loop’s `goal-tracker.md` itself. The core contract starts at `prompt-template/codex/goal-tracker-update-section.md:1` and states the ownership boundary at lines `3-6`.

- algorithmic_behavior: The template encodes a three-step transition: evaluate Claude’s requested change, apply approved changes to `@{{GOAL_TRACKER_FILE}}`, or explain rejected requests in the review. The approved mutation classes are enumerated in `prompt-template/codex/goal-tracker-update-section.md:6-10`: move tasks between Active/Completed/Deferred, append Plan Evolution Log entries with round number and justification, add Open Issues, and preserve the immutable goal/acceptance area. Rejection behavior is explicit at line `11`: the review must say why the request was rejected. Common request classes are normalized at lines `13-17`, covering completion, new issues, plan changes, and strongly justified deferrals.

- inputs_outputs_state: Primary input is rendered variable `GOAL_TRACKER_FILE`, substituted into the `@{{GOAL_TRACKER_FILE}}` target at `prompt-template/codex/goal-tracker-update-section.md:6`. Runtime content input is Claude’s round summary, specifically a “Goal Tracker Update Request” section named in lines `3` and `11`. Output is not a separate file from this template; it instructs Codex either to mutate the rendered goal-tracker path or to include rejection rationale in `REVIEW_RESULT_FILE` through the parent review prompt. The rendered section is assigned to `GOAL_TRACKER_UPDATE_SECTION` by `hooks/loop-codex-stop-hook.sh:539-540`, then injected into full-alignment and regular review templates via `hooks/loop-codex-stop-hook.sh:579-590` and `hooks/loop-codex-stop-hook.sh:595-606`.

- gates_or_invariants: The main invariant is that Claude cannot directly modify `goal-tracker.md` after Round 0; this template mirrors the enforcement boundary stated at `prompt-template/codex/goal-tracker-update-section.md:3`. The template also declares an immutable-section gate at line `10`, forbidding changes to Ultimate Goal and Acceptance Criteria. Strong-justification gating for deferrals is called out at line `17`. Separate validators enforce the ownership rule: Write operations against `goal-tracker.md` after Round 0 are blocked in `hooks/loop-write-validator.sh:91-98`, Edit operations are blocked in `hooks/loop-edit-validator.sh:78-85`, and Bash modifications are blocked in `hooks/loop-bash-validator.sh:161-174`. The shared blocking message tells Claude to request changes in the summary instead of editing directly at `prompt-template/block/goal-tracker-modification.md:1-25`.

- dependencies_and_callers: The fragment depends on the template-loader’s `{{VARIABLE_NAME}}` substitution semantics in `hooks/lib/template-loader.sh:35-43`; that loader is single-pass, so values containing template markers are not recursively expanded. It is rendered safely with a fallback by `load_and_render_safe` in `hooks/loop-codex-stop-hook.sh:537-540`; fallback behavior for missing or empty templates is implemented in `hooks/lib/template-loader.sh:155-185`. Its direct callers are the Codex stop hook’s review-prompt builder and the two parent templates: `prompt-template/codex/full-alignment-review.md:57` and `prompt-template/codex/regular-review.md:47`. The complementary Claude-side request format appears in `prompt-template/claude/goal-tracker-update-request.md:1-16`.

- edge_cases_or_failure_modes: If this file is missing or empty, the stop hook falls back to a shorter instruction at `hooks/loop-codex-stop-hook.sh:537-538`, preserving a minimal goal-tracker update path but losing the detailed allowed-change list and immutable-section warning. If `GOAL_TRACKER_FILE` is not supplied or is wrong, the rendered instruction can point Codex at the wrong target; there is no validation inside this template itself. If Claude’s request lacks evidence or justification, the template’s expected behavior is rejection or review commentary, but enforcement is reviewer-driven rather than machine-validated here. A subtle formatting edge exists because parent templates include `## Part 3: {{GOAL_TRACKER_UPDATE_SECTION}}`; since this fragment itself begins with a heading at `prompt-template/codex/goal-tracker-update-section.md:1`, the rendered prompt can contain a composite heading followed by the embedded heading text, but this is stylistic rather than a state-machine failure.

- validation_or_tests: Template substitution coverage exists in `tests/test-templates-comprehensive.sh:531-540`, which renders `codex/goal-tracker-update-section.md` with a sample `.humanize-loop.local/.../goal-tracker.md` path and asserts that both the “Goal Tracker Update Requests” heading and rendered path appear. Broader template-loader tests cover safe rendering and fallback behavior, while `tests/test-template-references.sh` checks critical validators use safe rendering. I did not run the test suite because this branch export is read-only and the task requested research notes only; direct inspection confirmed the expected references.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 Item Evidence section present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`