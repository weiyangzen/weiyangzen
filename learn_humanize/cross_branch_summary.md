# Unified Humanize Cross-Repo Research Summary

Snapshot date: 2026-06-19

## Direct Answers

- Source remotes:
- `humanize`: `https://github.com/PolyArch/humanize.git` local `/Users/wangweiyang/GitHub/humanize`
- `oh-my-humanize`: `https://github.com/PolyArch/oh-my-humanize.git` local `/Users/wangweiyang/GitHub/oh-my-humanize`
- Remote repo/branch entries discovered: `39`.
- Branch folders with algorithm lists: `39`.
- Completed branch research count: `24`.
- Completed branches: `humanize/add-a-final-code-simplifier-after-codex-complete`, `humanize/add-careful-mode-v1.6.5`, `humanize/add-commit-plan-file-cli`, `humanize/add-gen-plan-command`, `humanize/add-shell-syntax-check-cicd`, `humanize/allow-only-cancel-to-mv-state`, `humanize/ask-codex-skill`, `humanize/ask-gemini`, `humanize/cancel-when-finalize`, `humanize/change-todos-to-tasks`, `humanize/claude/add-dependency-check-tA0P8`, `humanize/dev`, `humanize/dev-rlcr-with-swarm-team`, `humanize/do-not-block-stop-when-background-running`, `humanize/do-not-wish-coding`, `humanize/enhance-rlcr-with-review-loop`, `humanize/feature/codex-bypass-sandbox-env`, `humanize/fix-humanize-escape`, `humanize/fix-pr-loop`, `humanize/fix-too-strict-rule-and-enhance-plan-gen`, `humanize/general-refactor-and-review`, `humanize/h2-dev`, `humanize/main`, `oh-my-humanize/main`.
- Research scope: algorithm-related subset only.
- `2.0` branch researched: no. `origin/2.0` does not exist in the fetched remote branch list.
- `3.0` branch researched: no. `origin/3.0` does not exist in the fetched remote branch list.
- `h2-dev`: complete with 251 algorithm items.

## Status Counts

```text
complete: 24
prepared_not_complete: 15
```

## Current Next Branches Needing Worker Completion

`humanize/general-robustness-edge-test`, `humanize/impl-dccb-loop`, `humanize/impl-pr-loop`, `humanize/improve-gen-plan-command`, `humanize/improve-monitor-script`, `humanize/improve-pr-loop`, `humanize/make-working-folder-to-humanize-only`, `humanize/reflection-improve`, `humanize/robust-edge-test-find-and-resolve`, `humanize/skillize-rlcr-actions`, ... (15 total incomplete)

## Scope Rule

The current research scope is the fuzzy `algorithm subset`, resolved per branch into:

- Included: behavior-defining docs, commands, agents, config, hooks, prompt templates, runtime scripts, skills, templates, and tests.
- Skipped: CI-only files, installation-only docs, local assistant/plugin metadata, binary/visual assets, fixtures, mocks, and other non-core content.

For each prepared branch, the exact include/skip decision is recorded in `path_inventory.tsv` and `skipped_paths.tsv`.
