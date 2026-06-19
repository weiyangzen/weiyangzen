You are worker agent_12 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/ask-codex-skill
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/ask-codex-skill
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: ask-codex-skill
- Source commit: caf375a20530c8bb81e8e8e103a8598c25c11bb0
- Source tree: cb4d25ddf1911f588dce6e4c285c9ed74b58b61a
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| ASK_CODEX_SKILL-HZ-012 | directory | `prompt-template/claude` | 12533 | directory contains included core algorithm descendant(s) |
| ASK_CODEX_SKILL-HZ-042 | file | `scripts/poll-pr-reviews.sh` | 9532 | runtime script implementing workflow, routing, monitor, validation, or state behavior |
| ASK_CODEX_SKILL-HZ-072 | file | `tests/test-pr-loop-hooks.sh` | 51873 | executable specification for core algorithm behavior |
| ASK_CODEX_SKILL-HZ-102 | file | `prompt-template/block/no-trigger-comment.md` | 515 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ASK_CODEX_SKILL-HZ-132 | file | `prompt-template/codex/full-alignment-review.md` | 4167 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| ASK_CODEX_SKILL-HZ-162 | file | `tests/robustness/test-template-stress-robustness.sh` | 8882 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_12 ask-codex-skill 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `caf375a20530c8bb81e8e8e103a8598c25c11bb0`

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
