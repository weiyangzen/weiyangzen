You are worker agent_12 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/ask-gemini
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/ask-gemini
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: ask-gemini
- Source commit: 883e3f5bb8106cea4153d9f5e469b2fa7a8d6849
- Source tree: b9476bfda3f064efcefd5b341d9ddae04a6be9a3
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| ASK_GEMINI-HZ-012 | file | `README.md` | 3600 | behavior-defining documentation for workflow/state-machine algorithms |
| ASK_GEMINI-HZ-042 | file | `hooks/hooks.json` | 1811 | hook or validator implementation for the RLCR state machine |
| ASK_GEMINI-HZ-072 | file | `tests/run-all-tests.sh` | 9732 | executable specification for core algorithm behavior |
| ASK_GEMINI-HZ-102 | file | `tests/test-pr-loop-3-stophook.sh` | 786 | executable specification for core algorithm behavior |
| ASK_GEMINI-HZ-132 | file | `prompt-template/block/finalize-contract-access.md` | 283 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ASK_GEMINI-HZ-162 | file | `prompt-template/block/unpushed-commits.md` | 348 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ASK_GEMINI-HZ-192 | file | `prompt-template/pr-loop/critical-requirements-no-comments.md` | 585 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ASK_GEMINI-HZ-222 | file | `tests/robustness/test-state-transition-robustness.sh` | 12297 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_12 ask-gemini 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 8
- source_commit: `883e3f5bb8106cea4153d9f5e469b2fa7a8d6849`

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
