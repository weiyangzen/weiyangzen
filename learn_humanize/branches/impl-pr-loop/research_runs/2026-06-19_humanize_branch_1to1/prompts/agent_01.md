You are worker agent_01 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/impl-pr-loop
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/impl-pr-loop
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: impl-pr-loop
- Source commit: 96455ba5aff935988d78439ca55427c603b1adcd
- Source tree: 87ae2694d112d8130912971c6a6c494694ca9697
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| IMPL_PR_LOOP-HZ-001 | directory | `.` | 1105495 | directory contains included core algorithm descendant(s) |
| IMPL_PR_LOOP-HZ-031 | file | `scripts/cancel-pr-loop.sh` | 3498 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| IMPL_PR_LOOP-HZ-061 | file | `tests/test-pr-loop-scripts.sh` | 12471 | executable specification for core algorithm behavior |
| IMPL_PR_LOOP-HZ-091 | file | `prompt-template/block/pr-loop-prompt-write.md` | 360 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| IMPL_PR_LOOP-HZ-121 | file | `scripts/lib/monitor-common.sh` | 17436 | runtime script implementing workflow, routing, monitor, validation, or state behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_01 impl-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `96455ba5aff935988d78439ca55427c603b1adcd`

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
