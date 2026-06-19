You are worker agent_14 in an execution-cron style branch research run.

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
| H2_DEV-HZ-014 | directory | `prompt-template/block` | 16588 | directory contains included core algorithm descendant(s) |
| H2_DEV-HZ-044 | file | `hooks/loop-bash-validator.sh` | 24695 | hook or validator implementation for the RLCR state machine |
| H2_DEV-HZ-074 | file | `tests/config.test.ts` | 5971 | executable specification for core algorithm behavior |
| H2_DEV-HZ-104 | file | `tests/test-explore-manifest.sh` | 5799 | executable specification for core algorithm behavior |
| H2_DEV-HZ-134 | file | `tests/test-validate-explore-idea-io.sh` | 16749 | executable specification for core algorithm behavior |
| H2_DEV-HZ-164 | file | `prompt-template/block/codex-review-failed.md` | 441 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| H2_DEV-HZ-194 | file | `prompt-template/block/wrong-contract-location.md` | 130 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| H2_DEV-HZ-224 | file | `prompt-template/plan/refine-plan-qa-template.md` | 3133 | prompt/block template defining algorithmic transitions, gates, or review contracts |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_14 h2-dev 1:1 Core Algorithm Research

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
