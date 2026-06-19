You are worker agent_18 in an execution-cron style research run.

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
| HZ-018 | directory | `prompt-template/plan` | 8266 | directory contains included core algorithm descendant(s) |
| HZ-048 | file | `hooks/loop-write-validator.sh` | 14281 | hook or validator implementation for the RLCR state machine |
| HZ-078 | file | `tests/test-config-error-handling.sh` | 6134 | executable specification for core algorithm behavior |
| HZ-108 | file | `hooks/lib/loop-common.sh` | 62888 | hook or validator implementation for the RLCR state machine |
| HZ-138 | file | `prompt-template/block/prompt-file-write.md` | 413 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| HZ-168 | file | `prompt-template/codex/code-review-phase.md` | 1273 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| HZ-198 | file | `tests/robustness/test-state-transition-robustness.sh` | 12297 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep the final evidence organized by the assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_18 1:1 Core Algorithm Research

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
