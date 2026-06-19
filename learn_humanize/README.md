# Unified Humanize Research Index

This directory is the unified learning and research workspace for `PolyArch/humanize` plus `PolyArch/oh-my-humanize`.

## Current State

- Source repositories:
- `humanize`: `https://github.com/PolyArch/humanize.git` local `/Users/wangweiyang/GitHub/humanize`
- `oh-my-humanize`: `https://github.com/PolyArch/oh-my-humanize.git` local `/Users/wangweiyang/GitHub/oh-my-humanize`
- Target repository: `https://github.com/weiyangzen/weiyangzen.git`
- Local research root: `/Users/wangweiyang/GitHub/weiyangzen/learn_humanize`
- Remote repo/branch entries discovered on 2026-06-19: `39`
- Branch folders with algorithm research lists: `39`
- Completed 1:1 algorithm learning branches: `39`
- Branches still needing worker completion: `0`

## 2.0 / 3.0 Branch Check

`git ls-remote --heads origin '2.0' '3.0' 'v2*' 'v3*' 'h2-dev' 'h3*'` returned:

```text
2da7defbd5e955dbc329a27f1745fa74a0bee3f7	refs/heads/h2-dev
```

There is no remote branch named `2.0` or `3.0` at this snapshot. `h2-dev` exists and is the only 2-series-looking branch name found.

## What Counts As Research Here

This is algorithm-subset learning research, not full repository documentation. Each branch folder contains:

- `path_inventory.tsv`: full path inventory with included/skipped decisions.
- `research_list.tsv`: locked algorithm/core subset for 1:1 learning.
- `assignment.tsv`: worker-job assignment plan.
- `execution_blueprint.md`: dual-cursor checklist.
- `todos_20260619.md`: current todo snapshot.
- `research_runs/.../agents/agent_*/output.md`: worker learning output when complete.
- `coverage_matrix.tsv` and `core_algorithm_1to1_report.md`: final accepted branch output when complete.

Non-core installation docs, binary/visual assets, CI-only files, fixtures, and mock data are skipped with explicit reasons in each branch's `skipped_paths.tsv`.

## Status Counts

```text
complete: 39
```

## Index Files

- `branches.tsv`: all discovered remote branches and current research status.
- `progress.tsv`: same schema as `branches.tsv`, regenerated for progress polling.
- `research_queue.tsv`: unified cross-repo todo/done queue for worker claiming.
- `cross_branch_summary.md`: human-readable cross-branch status and scope notes.
- `tools/branch_research.py`: preparation, launch, verify, finalize, and index helper.
