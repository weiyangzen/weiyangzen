You are worker agent_09 in an execution-cron style branch research run.

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
| H2_DEV-HZ-009 | directory | `skills` | 30105 | directory contains included core algorithm descendant(s) |
| H2_DEV-HZ-039 | file | `config/default_config.json` | 179 | runtime configuration or hook schema participating in gates/routing |
| H2_DEV-HZ-069 | file | `scripts/validate-refine-plan-io.sh` | 21742 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| H2_DEV-HZ-099 | file | `tests/test-config-merge.sh` | 7516 | executable specification for core algorithm behavior |
| H2_DEV-HZ-129 | file | `tests/test-template-loader.sh` | 21274 | executable specification for core algorithm behavior |
| H2_DEV-HZ-159 | file | `prompt-template/block/bitlesson-delta-inconsistent.md` | 301 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| H2_DEV-HZ-189 | file | `prompt-template/block/stop-hook-direct-execution.md` | 394 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| H2_DEV-HZ-219 | file | `prompt-template/explore/final-idea-template.md` | 627 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| H2_DEV-HZ-249 | file | `tests/robustness/test-template-error-robustness.sh` | 10945 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_09 h2-dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 9
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
