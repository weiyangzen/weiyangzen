# Humanize Cross-Branch Research Summary

Snapshot date: 2026-06-19

## Direct Answers

- `humanize` source remote checked locally: `https://github.com/PolyArch/humanize.git`.
- Remote branches discovered: `38`.
- Completed branch research count: `1`.
- Completed branch: `main`.
- Completed research is algorithm-subset research: yes. The included rows are command workflows, hook/state-machine scripts, prompt templates, runtime scripts, skills, config, and tests that define or validate algorithmic behavior.
- `2.0` branch researched: no. `origin/2.0` does not exist in the fetched remote branch list.
- `3.0` branch researched: no. `origin/3.0` does not exist in the fetched remote branch list.
- `h2-dev`: exists and is the only 2-series-looking branch name found by `ls-remote`; it is not complete in this checkpoint.

## Completed Branch: main

The `main` branch research is stored at `learn_humanize/branches/main`.

Verification result:

```json
{
  "branch": "main",
  "research_items": 201,
  "status_files": 30,
  "complete_status_files": 30,
  "output_files": 30,
  "problems": 0
}
```

Research item breakdown:

```text
directory 25
file 176
```

Skipped non-core paths: `35`.

## Prepared Branch: ask-gemini

The `ask-gemini` branch folder is stored at `learn_humanize/branches/ask-gemini`.

This branch has a locked algorithm list and 30-worker scaffolding, but worker research has not completed:

```json
{
  "branch": "ask-gemini",
  "research_items": 225,
  "status_files": 0,
  "complete_status_files": 0,
  "output_files": 0,
  "problems": 450
}
```

Research item breakdown:

```text
directory 25
file 200
```

Skipped non-core paths: `35`.

## Branch Coverage Status

`branches.tsv` is the authoritative cross-branch status table for this checkpoint. It lists all 38 remote branches, source commits, tree hashes, status, and report paths.

Current statuses:

```text
complete: 1
prepared_not_complete: 1
not_started: 36
```

## Scope Rule

The current research scope is the fuzzy `algorithm subset`, resolved per branch into:

- Included: behavior-defining docs, commands, agents, config, hooks, prompt templates, runtime scripts, skills, templates, and tests.
- Skipped: CI-only files, installation-only docs, local assistant/plugin metadata, binary/visual assets, fixtures, mocks, and other non-core content.

For each prepared branch, the exact include/skip decision is recorded in `path_inventory.tsv` and `skipped_paths.tsv`.
