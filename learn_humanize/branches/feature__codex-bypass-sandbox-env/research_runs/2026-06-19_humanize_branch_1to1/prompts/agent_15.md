You are worker agent_15 in an execution-cron style branch research run.

Repository root: /Users/wangweiyang/GitHub/humanize_branch_worktrees/feature__codex-bypass-sandbox-env
Work only inside this read-only branch export: /Users/wangweiyang/GitHub/humanize_branch_worktrees/feature__codex-bypass-sandbox-env
Do not edit the scheduler's authoritative checkout directly: /Users/wangweiyang/GitHub/weiyangzen
Do not modify files. Produce research notes only.

Run metadata:
- Branch: feature/codex-bypass-sandbox-env
- Source commit: f0f1ad947157c3d1e9d0bdd58bf36aae92075cc6
- Source tree: 18bfb7a089ea90d5a898f1c19ed4a698a1e00afd
- Model requested by scheduler: gpt-5.5
- Reasoning effort requested by scheduler: xhigh
- Protocol: 1:1 file/folder coverage for the branch's core algorithm subset
- Worker success cursor: mark assigned items only as `[_]` in your written evidence. Never mark `[x]`.

Your assigned one-to-one research items:

| item_id | type | path | bytes | inclusion reason |
|---|---|---:|---:|---|
| FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-015 | directory | `scripts/lib` | 17436 | directory contains included core algorithm descendant(s) |
| FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-045 | file | `tests/setup-fixture-mock-gh.sh` | 2683 | executable specification for core algorithm behavior |
| FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-075 | file | `prompt-template/block/claude-eyes-timeout.md` | 776 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-105 | file | `prompt-template/block/wrong-round-number.md` | 225 | prompt/block template defining algorithmic transitions, gates, or review contracts |
| FEATURE__CODEX_BYPASS_SANDBOX_ENV-HZ-135 | file | `tests/robustness/test-path-validation-robustness.sh` | 13424 | executable specification for core algorithm behavior |

Research requirements:
1. Treat each non-`none` row above as a separate checklist item. Do not merge items into a single broad topic.
2. For every file item, inspect the file directly and identify its algorithmic role, inputs, outputs, state transitions, gates, validation behavior, key functions/sections, dependencies, and edge cases.
3. For every directory item, inspect the directory recursively without an artificial depth limit. Summarize the directory's algorithmic responsibility, its contained child roles, and how it coordinates with sibling or parent paths.
4. Follow references to related commands, hooks, templates, scripts, tests, and config when needed to understand behavior, but keep final evidence organized by assigned item IDs.
5. If an assigned item appears misclassified as core algorithm, keep the item section, mark it `[_]`, and explicitly explain why it is a skip candidate. Do not silently drop it.
6. Include concrete path references and line references where useful. Keep quotes short.
7. End with a worker self-test checklist proving that every assigned item_id appears exactly once in your output.

Required output format:

# agent_15 feature/codex-bypass-sandbox-env 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `f0f1ad947157c3d1e9d0bdd58bf36aae92075cc6`

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
