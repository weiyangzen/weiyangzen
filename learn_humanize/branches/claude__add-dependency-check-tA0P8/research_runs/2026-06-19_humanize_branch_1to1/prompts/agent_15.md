You are worker agent_15 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/claude__add-dependency-check-tA0P8
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/claude__add-dependency-check-tA0P8
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: claude/add-dependency-check-tA0P8
- Source commit: df26142e5fbed5e2ac3e48f001786cfa77296dda
- Source tree: a3c84a8892915ef54a69f05daed4839c1c581af3
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-015 | directory | `prompt-template/pr-loop` | 6761 | directory contains included core algorithm descendant(s) |
| CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-045 | file | `scripts/poll-pr-reviews.sh` | 9532 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-075 | file | `tests/test-pr-loop-3-stophook.sh` | 604 | executable specification for core algorithm behavior |
| CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-105 | file | `prompt-template/block/goal-tracker-not-initialized.md` | 707 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-135 | file | `prompt-template/claude/push-every-round-note.md` | 101 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-165 | file | `tests/robustness/test-pr-loop-api-poll.sh` | 450 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_15 claude/add-dependency-check-tA0P8 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `df26142e5fbed5e2ac3e48f001786cfa77296dda`

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
