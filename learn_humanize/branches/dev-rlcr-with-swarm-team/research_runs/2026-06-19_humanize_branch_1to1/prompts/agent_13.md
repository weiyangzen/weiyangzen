You are worker agent_13 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/dev-rlcr-with-swarm-team
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/dev-rlcr-with-swarm-team
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: dev-rlcr-with-swarm-team
- Source commit: 0d5f0943ae9b1f80c5115aa946ebeb289e2cb83d
- Source tree: b115d62575538a825f4d0193433e663db4e7696c
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| DEV_RLCR_WITH_SWARM_TEAM-HZ-013 | directory | `prompt-template/plan` | 2959 | directory contains included core algorithm descendant(s) |
| DEV_RLCR_WITH_SWARM_TEAM-HZ-043 | file | `scripts/validate-gen-plan-io.sh` | 4822 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| DEV_RLCR_WITH_SWARM_TEAM-HZ-073 | file | `tests/test-templates-comprehensive.sh` | 19978 | executable specification for core algorithm behavior |
| DEV_RLCR_WITH_SWARM_TEAM-HZ-103 | file | `prompt-template/block/unpushed-commits.md` | 348 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DEV_RLCR_WITH_SWARM_TEAM-HZ-133 | file | `scripts/lib/monitor-common.sh` | 17436 | runtime script implementing workflow, routing, monitor, validation, or state behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_13 dev-rlcr-with-swarm-team 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `0d5f0943ae9b1f80c5115aa946ebeb289e2cb83d`

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
