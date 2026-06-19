You are worker agent_11 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/general-robustness-edge-test
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/general-robustness-edge-test
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: general-robustness-edge-test
- Source commit: 4a4e59ce0cc5613c54d15754a29c7d2a2e9be058
- Source tree: e5a1cc8e7baf55b12efeae3fb5564c88e5173747
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| GENERAL_ROBUSTNESS_EDGE_TEST-HZ-011 | directory | `prompt-template/claude` | 6966 | directory contains included core algorithm descendant(s) |
| GENERAL_ROBUSTNESS_EDGE_TEST-HZ-041 | file | `scripts/setup-rlcr-loop.sh` | 32055 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| GENERAL_ROBUSTNESS_EDGE_TEST-HZ-071 | file | `tests/test-todo-checker.sh` | 10313 | executable specification for core algorithm behavior |
| GENERAL_ROBUSTNESS_EDGE_TEST-HZ-101 | file | `prompt-template/block/work-summary-missing.md` | 335 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| GENERAL_ROBUSTNESS_EDGE_TEST-HZ-131 | file | `tests/robustness/test-git-operations-robustness.sh` | 14267 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_11 general-robustness-edge-test 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `4a4e59ce0cc5613c54d15754a29c7d2a2e9be058`

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
