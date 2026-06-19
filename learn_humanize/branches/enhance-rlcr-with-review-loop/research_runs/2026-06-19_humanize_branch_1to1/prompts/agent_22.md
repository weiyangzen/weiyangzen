You are worker agent_22 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/enhance-rlcr-with-review-loop
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/enhance-rlcr-with-review-loop
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: enhance-rlcr-with-review-loop
- Source commit: dd6c37c45c4836773497f878b8925057e9f5318c
- Source tree: 0fa8cd9a00b5b352ba560724bae33887982fd314
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-022 | file | `commands/start-rlcr-loop.md` | 3157 | command workflow definition for plan/RLCR algorithms |
| ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-052 | file | `tests/test-error-scenarios.sh` | 7691 | executable specification for core algorithm behavior |
| ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-082 | file | `prompt-template/block/git-not-clean.md` | 817 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-112 | file | `prompt-template/claude/post-alignment-action-items.md` | 390 | prompt/block template defining algorithmic transitions, gates, or review contracts |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_22 enhance-rlcr-with-review-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 4
- source_commit: `dd6c37c45c4836773497f878b8925057e9f5318c`

## Item Evidence

### <ITEM_ID> `<type>` `<path>`
- cursor: `[_]`
- core_role:
- algorithmic_behavior:
- inputs_outputs_state:
- gates_or_invariants:
- dependencies_and_callers:
- edge_cases_or_failure_modes:
- validation_or_tests:
- skip_candidate: `no` or `yes: reason`

## Worker Self-Test
- assigned_items_seen:
- missing_items:
- duplicate_items:
- final_worker_status: `complete`
