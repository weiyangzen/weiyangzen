You are worker agent_23 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/add-careful-mode-v1.6.5
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/add-careful-mode-v1.6.5
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: add-careful-mode-v1.6.5
- Source commit: a12de5d9f36bb10cd62955881f4e76d67d3f50ce
- Source tree: 7d847853090e01da8d15947bc1f468d3e7943daf
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| ADD_CAREFUL_MODE_V1_6_5-HZ-023 | file | `hooks/check-todos-from-transcript.py` | 6717 | hook or validator implementation for the RLCR state machine |
| ADD_CAREFUL_MODE_V1_6_5-HZ-053 | file | `tests/test-finalize-phase.sh` | 31038 | executable specification for core algorithm behavior |
| ADD_CAREFUL_MODE_V1_6_5-HZ-083 | file | `prompt-template/block/git-push.md` | 270 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ADD_CAREFUL_MODE_V1_6_5-HZ-113 | file | `prompt-template/claude/post-alignment-action-items.md` | 390 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ADD_CAREFUL_MODE_V1_6_5-HZ-143 | file | `tests/robustness/test-template-error-robustness.sh` | 10937 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_23 add-careful-mode-v1.6.5 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `a12de5d9f36bb10cd62955881f4e76d67d3f50ce`

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
