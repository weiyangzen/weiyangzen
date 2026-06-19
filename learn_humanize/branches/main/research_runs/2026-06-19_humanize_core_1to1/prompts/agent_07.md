You are worker agent_07 in an execution-cron style research run.

Repository root: /Users/wangweiyang/GitHub/humanize
Work only inside this read-only source checkout: /Users/wangweiyang/GitHub/humanize
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Source commit: 0ec921a36b4365df503511c5567bbd3e02db0df5
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| HZ-007 | directory | `prompt-template` | 60894 | directory contains included core algorithm descendant(s) |
| HZ-037 | file | `config/default_config.json` | 179 | runtime configuration or hook schema participating in gates/routing |
| HZ-067 | file | `tests/test-agent-teams.sh` | 24577 | executable specification for core algorithm behavior |
| HZ-097 | file | `tests/test-stop-gate.sh` | 10477 | executable specification for core algorithm behavior |
| HZ-127 | file | `prompt-template/block/git-tracked-humanize.md` | 530 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| HZ-157 | file | `prompt-template/claude/drift-replan-prompt.md` | 2756 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| HZ-187 | file | `tests/robustness/test-cancel-security-robustness.sh` | 14746 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep the final evidence organized by the assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_07 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`

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
