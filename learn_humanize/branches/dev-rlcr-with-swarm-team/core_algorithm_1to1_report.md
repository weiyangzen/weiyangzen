# Humanize `dev-rlcr-with-swarm-team` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `dev-rlcr-with-swarm-team`
- Source commit: `0d5f0943ae9b1f80c5115aa946ebeb289e2cb83d`
- Source tree: `b115d62575538a825f4d0193433e663db4e7696c`
- Read-only source export: `/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev-rlcr-with-swarm-team`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker count: `30`
- Recursive source files excluding .git: `154`
- Recursive source directories excluding .git: `21`
- Included core algorithm items: `150`
- Skipped non-core paths: `25`
- Status files complete: `30 / 30`
- Output files: `30 / 30`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 1418466 |
| `README.md` | 1 | 1 | 0 | 8266 |
| `agents` | 2 | 1 | 1 | 3576 |
| `commands` | 6 | 5 | 1 | 43286 |
| `hooks` | 14 | 12 | 2 | 567045 |
| `prompt-template` | 61 | 55 | 6 | 129000 |
| `scripts` | 14 | 12 | 2 | 458420 |
| `tests` | 51 | 49 | 2 | 2009251 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_01` | 5 | 1465721 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_01/output.md` |
| `agent_02` | 5 | 99760 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_02/output.md` |
| `agent_03` | 5 | 78576 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_03/output.md` |
| `agent_04` | 5 | 266677 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_04/output.md` |
| `agent_05` | 5 | 70262 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_05/output.md` |
| `agent_06` | 5 | 287976 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_06/output.md` |
| `agent_07` | 5 | 952225 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_07/output.md` |
| `agent_08` | 5 | 75762 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_08/output.md` |
| `agent_09` | 5 | 109472 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_09/output.md` |
| `agent_10` | 5 | 25786 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_10/output.md` |
| `agent_11` | 5 | 66279 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_11/output.md` |
| `agent_12` | 5 | 61539 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_12/output.md` |
| `agent_13` | 5 | 45543 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_13/output.md` |
| `agent_14` | 5 | 32110 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_14/output.md` |
| `agent_15` | 5 | 47710 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_15/output.md` |
| `agent_16` | 5 | 341637 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_16/output.md` |
| `agent_17` | 5 | 25578 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_17/output.md` |
| `agent_18` | 5 | 35574 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_18/output.md` |
| `agent_19` | 5 | 39535 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_19/output.md` |
| `agent_20` | 5 | 42646 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_20/output.md` |
| `agent_21` | 5 | 24671 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_21/output.md` |
| `agent_22` | 5 | 63352 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_22/output.md` |
| `agent_23` | 5 | 46115 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_23/output.md` |
| `agent_24` | 5 | 20641 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_24/output.md` |
| `agent_25` | 5 | 87896 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_25/output.md` |
| `agent_26` | 5 | 98646 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_26/output.md` |
| `agent_27` | 5 | 21435 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_27/output.md` |
| `agent_28` | 5 | 31722 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_28/output.md` |
| `agent_29` | 5 | 44573 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_29/output.md` |
| `agent_30` | 5 | 27891 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_30/output.md` |

## Verification

```json
{
  "branch": "dev-rlcr-with-swarm-team",
  "research_items": 150,
  "status_files": 30,
  "complete_status_files": 30,
  "output_files": 30,
  "problems": 0
}
```
