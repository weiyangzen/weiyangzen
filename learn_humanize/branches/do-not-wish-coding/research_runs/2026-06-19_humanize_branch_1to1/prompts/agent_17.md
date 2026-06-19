You are worker agent_17 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/do-not-wish-coding
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/do-not-wish-coding
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: do-not-wish-coding
- Source commit: ac6cd9c180bcb9b84f6083fba1e458b4aab9ae14
- Source tree: 3ea02272d1dfedbaeb33258dde5a71a911816d51
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| DO_NOT_WISH_CODING-HZ-017 | directory | `prompt-template/plan` | 4980 | directory contains included core algorithm descendant(s) |
| DO_NOT_WISH_CODING-HZ-047 | file | `scripts/ask-codex.sh` | 11948 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| DO_NOT_WISH_CODING-HZ-077 | file | `tests/test-config-error-handling.sh` | 6126 | executable specification for core algorithm behavior |
| DO_NOT_WISH_CODING-HZ-107 | file | `tests/test-templates-comprehensive.sh` | 19975 | executable specification for core algorithm behavior |
| DO_NOT_WISH_CODING-HZ-137 | file | `prompt-template/block/prompt-file-write.md` | 413 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DO_NOT_WISH_CODING-HZ-167 | file | `prompt-template/pr-loop/codex-goal-tracker-update.md` | 2008 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| DO_NOT_WISH_CODING-HZ-197 | file | `tests/robustness/test-state-transition-robustness.sh` | 12289 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_17 do-not-wish-coding 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `ac6cd9c180bcb9b84f6083fba1e458b4aab9ae14`

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
