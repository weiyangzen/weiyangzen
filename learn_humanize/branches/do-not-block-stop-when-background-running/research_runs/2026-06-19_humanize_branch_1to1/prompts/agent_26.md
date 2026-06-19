You are worker agent_26 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/do-not-block-stop-when-background-running
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/do-not-block-stop-when-background-running
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: do-not-block-stop-when-background-running
- Source commit: 3711e5fd9059584c7bf98cf1d19ee02dcf5bef48
- Source tree: 85688308d3ac5878c8b92c28f6882eb11eab2640
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-026 | file | `agents/bitlesson-selector.md` | 1444 | agent prompt/policy file defining review or planning behavior |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-056 | file | `scripts/setup-rlcr-loop.sh` | 57023 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-086 | file | `tests/test-monitor-e2e-sigint.sh` | 637 | executable specification for core algorithm behavior |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-116 | file | `prompt-template/block/finalize-state-file-modification.md` | 344 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-146 | file | `prompt-template/block/wrong-file-location.md` | 318 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-176 | file | `skills/ask-gemini/SKILL.md` | 2410 | skill instruction defining algorithmic workflow behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_26 do-not-block-stop-when-background-running 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `3711e5fd9059584c7bf98cf1d19ee02dcf5bef48`

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
