You are worker agent_13 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-pr-loop
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-pr-loop
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: improve-pr-loop
- Source commit: 61f03daecb8ff9c20e535a636b90aa92a3d7c9b2
- Source tree: d68379d07648ba44175cc687b6a8074dedd7cf4e
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| IMPROVE_PR_LOOP-HZ-013 | directory | `prompt-template/plan` | 2959 | directory contains included core algorithm descendant(s) |
| IMPROVE_PR_LOOP-HZ-043 | file | `tests/manual-monitor-test.sh` | 2527 | executable specification for core algorithm behavior |
| IMPROVE_PR_LOOP-HZ-073 | file | `hooks/lib/loop-common.sh` | 49692 | hook or validator implementation for the RLCR state machine |
| IMPROVE_PR_LOOP-HZ-103 | file | `prompt-template/block/wrong-file-location.md` | 318 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| IMPROVE_PR_LOOP-HZ-133 | file | `tests/robustness/test-hook-input-robustness.sh` | 22458 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_13 improve-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `61f03daecb8ff9c20e535a636b90aa92a3d7c9b2`

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
