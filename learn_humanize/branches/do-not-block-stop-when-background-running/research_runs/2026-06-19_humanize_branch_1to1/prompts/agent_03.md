You are worker agent_03 in an execution-cron style branch research run.

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
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-003 | directory | `commands` | 69944 | directory contains included core algorithm descendant(s) |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-033 | file | `commands/start-rlcr-loop.md` | 11701 | command workflow definition for plan/RLCR algorithms |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-063 | file | `tests/setup-monitor-test-env.sh` | 575 | executable specification for core algorithm behavior |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-093 | file | `tests/test-state-exit-naming.sh` | 9047 | executable specification for core algorithm behavior |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-123 | file | `prompt-template/block/git-tracked-humanize.md` | 530 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-153 | file | `prompt-template/claude/drift-replan-prompt.md` | 2756 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-183 | file | `tests/robustness/test-concurrent-state-robustness.sh` | 14582 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_03 do-not-block-stop-when-background-running 1:1 Core Algorithm Research

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
