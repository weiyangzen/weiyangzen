You are worker agent_25 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/h2-dev
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/h2-dev
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: h2-dev
- Source commit: 2da7defbd5e955dbc329a27f1745fa74a0bee3f7
- Source tree: bef2487769543ff367da2da425136b0cfefae129
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| H2_DEV-HZ-025 | directory | `skills/humanize-refine-plan` | 6293 | directory contains included core algorithm descendant(s) |
| H2_DEV-HZ-055 | file | `scripts/bitlesson-validate-delta.sh` | 12319 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| H2_DEV-HZ-085 | file | `tests/test-allowlist-validators.sh` | 22380 | executable specification for core algorithm behavior |
| H2_DEV-HZ-115 | file | `tests/test-monitor-runtime.sh` | 14060 | executable specification for core algorithm behavior |
| H2_DEV-HZ-145 | file | `tests/workflow-graph.test.ts` | 6027 | executable specification for core algorithm behavior |
| H2_DEV-HZ-175 | file | `prompt-template/block/goal-tracker-modification.md` | 486 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| H2_DEV-HZ-205 | file | `prompt-template/claude/finalize-phase-skipped-prompt.md` | 1750 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| H2_DEV-HZ-235 | file | `skills/humanize/SKILL.md` | 7487 | skill instruction defining algorithmic workflow behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_25 h2-dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 8
- source_commit: `2da7defbd5e955dbc329a27f1745fa74a0bee3f7`

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
