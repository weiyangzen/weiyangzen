You are worker agent_08 in an execution-cron style branch research run.

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
| ASK_GEMINI-HZ-008 | directory | `scripts` | 353611 | directory contains included core algorithm descendant(s) |
| ASK_GEMINI-HZ-038 | file | `config/default_config.json` | 179 | runtime configuration or hook schema participating in gates/routing |
| ASK_GEMINI-HZ-068 | file | `scripts/validate-gen-plan-io.sh` | 5758 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| ASK_GEMINI-HZ-098 | file | `tests/test-plan-file-hooks.sh` | 38107 | executable specification for core algorithm behavior |
| ASK_GEMINI-HZ-128 | file | `prompt-template/block/bitlesson-delta-missing-notes.md` | 207 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ASK_GEMINI-HZ-158 | file | `prompt-template/block/state-file-modification.md` | 243 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ASK_GEMINI-HZ-188 | file | `prompt-template/plan/gen-plan-template.md` | 5133 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ASK_GEMINI-HZ-218 | file | `tests/robustness/test-pr-loop-api-robustness.sh` | 28609 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_08 ask-gemini 1:1 Core Algorithm Research

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
