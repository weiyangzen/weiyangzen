# learn_humanize

This directory contains the corrected 1:1 core-algorithm research artifact for `PolyArch/humanize`.

The previous topic-style research report was removed and replaced with an execution-cron style checklist. Every retained core algorithm file or directory has exactly one checklist item, one assignment, and one worker evidence path. Non-core files/directories remain visible in the full inventory with skip reasons.

## Source

- Repository: `https://github.com/PolyArch/humanize.git`
- Local checkout: `/Users/wangweiyang/GitHub/humanize`
- Source commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`
- Research run: `research_runs/2026-06-19_humanize_core_1to1`

## Coverage Counts

- Source files, recursive excluding `.git`: 204
- Source directories, recursive excluding `.git`: 32
- Included core algorithm files: 176
- Included core algorithm directories: 25
- Included 1:1 research items: 201
- Skipped non-core files: 28
- Skipped non-core directories: 7

## Method

- Protocol: execution-cron style dual cursor (`[ ]` -> `[_]` -> `[x]`)
- Research list: `research_list.tsv`
- Full inventory with skip reasons: `path_inventory.tsv`
- Blueprint: `execution_blueprint.md`
- Todo snapshot: `todos_20260619.md`
- Workers: 30 tmux windows running `codex exec`
- Model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Depth rule: no artificial traversal-depth limit for assigned directories; workers follow descendants and referenced templates/tests as needed.

## Deliverables

- `core_algorithm_1to1_report.md`: final master synthesis after the 30-worker run.
- `research_list.tsv`: included core algorithm files/directories, one row per research item.
- `path_inventory.tsv`: all files/directories plus included/skipped decision and reason.
- `research_runs/2026-06-19_humanize_core_1to1/agents/agent_*/output.md`: raw worker evidence.
- `coverage_matrix.tsv`: verified one-to-one output coverage for every included item.
- `research_runs/2026-06-19_humanize_core_1to1/claim_ledger.tsv`: final worker/master status per item.

## Final Status

All 30 workers completed. Master coverage verification accepted all 201 included 1:1 research items.
