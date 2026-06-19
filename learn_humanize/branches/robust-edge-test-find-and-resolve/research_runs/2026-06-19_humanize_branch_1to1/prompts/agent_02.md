You are worker agent_02 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/robust-edge-test-find-and-resolve
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/robust-edge-test-find-and-resolve
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: robust-edge-test-find-and-resolve
- Source commit: a3112ca4d149f56ced783e805b6dfcf029368dc4
- Source tree: a5790de8b3fc8edc56d0b302e556cb4f2cf234ae
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-002 | directory | `agents` | 1788 | directory contains included core algorithm descendant(s) |
| ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-032 | file | `tests/run-all-tests.sh` | 4216 | executable specification for core algorithm behavior |
| ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-062 | file | `prompt-template/block/goal-tracker-bash-write.md` | 289 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-092 | file | `tests/robustness/test-goal-tracker-robustness.sh` | 14022 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_02 robust-edge-test-find-and-resolve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 4
- source_commit: `a3112ca4d149f56ced783e805b6dfcf029368dc4`

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
