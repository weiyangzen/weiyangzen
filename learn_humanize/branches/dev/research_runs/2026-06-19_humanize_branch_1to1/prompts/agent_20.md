You are worker agent_20 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/dev
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/dev
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: dev
- Source commit: eec73c4dfcc4f9791933e3cbaa616d4f261ed9e2
- Source tree: 96c7a42d89407320e7901ee2e149ba90da43b267
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| DEV-HZ-020 | directory | `scripts/lib` | 42181 | directory contains included core algorithm descendant(s) |
| DEV-HZ-050 | file | `hooks/loop-write-validator.sh` | 14466 | hook or validator implementation for the RLCR state machine |
| DEV-HZ-080 | file | `tests/test-bitlesson-validate-delta.sh` | 4403 | executable specification for core algorithm behavior |
| DEV-HZ-110 | file | `tests/test-state-exit-naming.sh` | 9047 | executable specification for core algorithm behavior |
| DEV-HZ-140 | file | `prompt-template/block/finalize-contract-access.md` | 283 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DEV-HZ-170 | file | `prompt-template/block/wrong-directory-path.md` | 152 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DEV-HZ-200 | file | `scripts/lib/config-loader.sh` | 4969 | runtime script implementing workflow, routing, monitor, validation, or state behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_20 dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `eec73c4dfcc4f9791933e3cbaa616d4f261ed9e2`

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
