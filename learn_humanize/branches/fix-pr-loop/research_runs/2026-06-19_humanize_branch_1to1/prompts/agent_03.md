You are worker agent_03 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/fix-pr-loop
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/fix-pr-loop
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: fix-pr-loop
- Source commit: 81f6f49d816a90a0e719db41ce15c4636ab9858a
- Source tree: 0c8a734c36349aa391c24a02d024950f8a027e78
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| FIX_PR_LOOP-HZ-003 | directory | `commands` | 21603 | directory contains included core algorithm descendant(s) |
| FIX_PR_LOOP-HZ-033 | file | `scripts/cancel-rlcr-loop.sh` | 4248 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| FIX_PR_LOOP-HZ-063 | file | `tests/test-pr-loop-scripts.sh` | 12471 | executable specification for core algorithm behavior |
| FIX_PR_LOOP-HZ-093 | file | `prompt-template/block/pr-loop-prompt-write.md` | 360 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| FIX_PR_LOOP-HZ-123 | file | `prompt-template/pr-loop/goal-tracker-initial.md` | 725 | prompt/block template defining algorithmic transitions, gates, or review contracts |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_03 fix-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `81f6f49d816a90a0e719db41ce15c4636ab9858a`

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
