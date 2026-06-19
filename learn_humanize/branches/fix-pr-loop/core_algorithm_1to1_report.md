# Humanize `fix-pr-loop` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `fix-pr-loop`
- Repo: `humanize`
- Source remote: `https://github.com/PolyArch/humanize.git`
- Source commit: `81f6f49d816a90a0e719db41ce15c4636ab9858a`
- Source tree: `0c8a734c36349aa391c24a02d024950f8a027e78`
- Read-only source export: `/Users/wangweiyang/GitHub/humanize_branch_worktrees/fix-pr-loop`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker count: `30`
- Recursive source files excluding .git: `148`
- Recursive source directories excluding .git: `21`
- Included core algorithm items: `144`
- Skipped non-core paths: `25`
- Status files complete: `30 / 30`
- Output files: `30 / 30`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 1313248 |
| `README.md` | 1 | 1 | 0 | 6564 |
| `agents` | 2 | 1 | 1 | 3576 |
| `commands` | 6 | 5 | 1 | 43206 |
| `hooks` | 13 | 11 | 2 | 532284 |
| `prompt-template` | 58 | 52 | 6 | 122982 |
| `scripts` | 14 | 12 | 2 | 420902 |
| `tests` | 49 | 47 | 2 | 1872883 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_01` | 5 | 1435312 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_01/output.md` |
| `agent_02` | 5 | 10325 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_02/output.md` |
| `agent_03` | 5 | 39407 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_03/output.md` |
| `agent_04` | 5 | 305175 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_04/output.md` |
| `agent_05` | 5 | 119519 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_05/output.md` |
| `agent_06` | 5 | 218842 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_06/output.md` |
| `agent_07` | 5 | 884899 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_07/output.md` |
| `agent_08` | 5 | 43730 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_08/output.md` |
| `agent_09` | 5 | 81008 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_09/output.md` |
| `agent_10` | 5 | 80985 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_10/output.md` |
| `agent_11` | 5 | 70323 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_11/output.md` |
| `agent_12` | 5 | 39991 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_12/output.md` |
| `agent_13` | 5 | 77954 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_13/output.md` |
| `agent_14` | 5 | 42537 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_14/output.md` |
| `agent_15` | 5 | 33969 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_15/output.md` |
| `agent_16` | 5 | 284470 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_16/output.md` |
| `agent_17` | 5 | 44987 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_17/output.md` |
| `agent_18` | 5 | 18997 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_18/output.md` |
| `agent_19` | 5 | 48596 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_19/output.md` |
| `agent_20` | 5 | 68291 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_20/output.md` |
| `agent_21` | 5 | 27280 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_21/output.md` |
| `agent_22` | 5 | 23674 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_22/output.md` |
| `agent_23` | 5 | 45045 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_23/output.md` |
| `agent_24` | 5 | 29433 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_24/output.md` |
| `agent_25` | 4 | 20911 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_25/output.md` |
| `agent_26` | 4 | 77341 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_26/output.md` |
| `agent_27` | 4 | 37748 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_27/output.md` |
| `agent_28` | 4 | 25565 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_28/output.md` |
| `agent_29` | 4 | 44871 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_29/output.md` |
| `agent_30` | 4 | 34460 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_30/output.md` |

## Verification

```json
{
  "branch": "fix-pr-loop",
  "research_items": 144,
  "status_files": 30,
  "complete_status_files": 30,
  "output_files": 30,
  "problems": 0
}
```
