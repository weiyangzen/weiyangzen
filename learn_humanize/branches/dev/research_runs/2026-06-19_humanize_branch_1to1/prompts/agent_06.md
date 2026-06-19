You are worker agent_06 in an execution-cron style branch research run.

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
| DEV-HZ-006 | directory | `hooks` | 278807 | directory contains included core algorithm descendant(s) |
| DEV-HZ-036 | file | `commands/refine-plan.md` | 23115 | command workflow definition for plan/RLCR algorithms |
| DEV-HZ-066 | file | `scripts/validate-gen-plan-io.sh` | 5984 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| DEV-HZ-096 | file | `tests/test-gen-plan.sh` | 41552 | executable specification for core algorithm behavior |
| DEV-HZ-126 | file | `tests/test-worker-result-contract.sh` | 6227 | executable specification for core algorithm behavior |
| DEV-HZ-156 | file | `prompt-template/block/methodology-analysis-state-file-modification.md` | 510 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DEV-HZ-186 | file | `prompt-template/claude/post-alignment-action-items.md` | 499 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DEV-HZ-216 | file | `tests/robustness/test-hook-input-robustness.sh` | 22490 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_06 dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 8
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
