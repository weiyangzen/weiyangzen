You are worker agent_09 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/do-not-block-stop-when-background-running
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/do-not-block-stop-when-background-running
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: do-not-block-stop-when-background-running
- Source commit: 3711e5fd9059584c7bf98cf1d19ee02dcf5bef48
- Source tree: 85688308d3ac5878c8b92c28f6882eb11eab2640
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-009 | directory | `skills` | 25778 | directory contains included core algorithm descendant(s) |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-039 | file | `hooks/hooks.json` | 1633 | hook or validator implementation for the RLCR state machine |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-069 | file | `tests/test-bitlesson-select-routing.sh` | 17115 | executable specification for core algorithm behavior |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-099 | file | `tests/test-template-references.sh` | 7103 | executable specification for core algorithm behavior |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-129 | file | `prompt-template/block/mainline-drift-stop.md` | 496 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-159 | file | `prompt-template/claude/next-round-prompt.md` | 2874 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-189 | file | `tests/robustness/test-plan-file-robustness.sh` | 15380 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_09 do-not-block-stop-when-background-running 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `3711e5fd9059584c7bf98cf1d19ee02dcf5bef48`

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
