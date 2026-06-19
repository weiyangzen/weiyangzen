You are worker agent_04 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/todo2task-careful-mode
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/todo2task-careful-mode
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: todo2task-careful-mode
- Source commit: 7d9dd4fbb5c376ae0a72b7caf81c50909ff14c37
- Source tree: 52de937eb6bb6f1eeb841422e1c5fd05e319540d
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| TODO2TASK_CAREFUL_MODE-HZ-004 | directory | `hooks` | 242927 | directory contains included core algorithm descendant(s) |
| TODO2TASK_CAREFUL_MODE-HZ-034 | file | `scripts/check-bot-reactions.sh` | 11447 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| TODO2TASK_CAREFUL_MODE-HZ-064 | file | `tests/test-pr-loop-stophook.sh` | 55327 | executable specification for core algorithm behavior |
| TODO2TASK_CAREFUL_MODE-HZ-094 | file | `prompt-template/block/pr-loop-state-modification.md` | 329 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| TODO2TASK_CAREFUL_MODE-HZ-124 | file | `prompt-template/pr-loop/goal-tracker-initial.md` | 725 | prompt/block template defining algorithmic transitions, gates, or review contracts |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_04 todo2task-careful-mode 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `7d9dd4fbb5c376ae0a72b7caf81c50909ff14c37`

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
