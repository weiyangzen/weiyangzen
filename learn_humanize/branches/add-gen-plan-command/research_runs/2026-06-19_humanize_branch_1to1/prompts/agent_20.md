You are worker agent_20 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/add-gen-plan-command
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/add-gen-plan-command
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: add-gen-plan-command
- Source commit: ac298f55075b28c65b2e76f8f73831cf6fd5be2f
- Source tree: 7508ec5e6c8c06c71100f6a7576f90227fb4dbe1
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| ADD_GEN_PLAN_COMMAND-HZ-020 | file | `commands/start-rlcr-loop.md` | 579 | command workflow definition for plan/RLCR algorithms |
| ADD_GEN_PLAN_COMMAND-HZ-050 | file | `tests/test-template-loader.sh` | 21290 | executable specification for core algorithm behavior |
| ADD_GEN_PLAN_COMMAND-HZ-080 | file | `prompt-template/block/wrong-file-location.md` | 318 | prompt/block template defining algorithmic transitions, gates, or review contracts |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_20 add-gen-plan-command 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 3
- source_commit: `ac298f55075b28c65b2e76f8f73831cf6fd5be2f`

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
