# Humanize `h2-dev` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `h2-dev`
- Source commit: `2da7defbd5e955dbc329a27f1745fa74a0bee3f7`
- Source tree: `bef2487769543ff367da2da425136b0cfefae129`
- Read-only source export: `/Users/wangweiyang/GitHub/humanize_branch_worktrees/h2-dev`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker count: `30`
- Recursive source files excluding .git: `324`
- Recursive source directories excluding .git: `53`
- Included core algorithm items: `251`
- Skipped non-core paths: `126`
- Status files complete: `30 / 30`
- Output files: `30 / 30`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 2298469 |
| `README.md` | 1 | 1 | 0 | 8232 |
| `agents` | 5 | 4 | 1 | 24522 |
| `commands` | 7 | 6 | 1 | 205472 |
| `config` | 3 | 2 | 1 | 1124 |
| `docs` | 3 | 2 | 1 | 46536 |
| `hooks` | 16 | 14 | 2 | 659524 |
| `prompt-template` | 74 | 67 | 7 | 219189 |
| `scripts` | 25 | 23 | 2 | 653357 |
| `skills` | 14 | 7 | 7 | 90315 |
| `templates` | 2 | 1 | 1 | 1374 |
| `tests` | 100 | 98 | 2 | 3185156 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_01` | 9 | 2367945 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_01/output.md` |
| `agent_02` | 9 | 73154 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_02/output.md` |
| `agent_03` | 9 | 231369 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_03/output.md` |
| `agent_04` | 9 | 214227 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_04/output.md` |
| `agent_05` | 9 | 106168 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_05/output.md` |
| `agent_06` | 9 | 404941 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_06/output.md` |
| `agent_07` | 9 | 130524 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_07/output.md` |
| `agent_08` | 9 | 342869 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_08/output.md` |
| `agent_09` | 9 | 93083 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_09/output.md` |
| `agent_10` | 9 | 35949 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_10/output.md` |
| `agent_11` | 9 | 1542138 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_11/output.md` |
| `agent_12` | 8 | 51335 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_12/output.md` |
| `agent_13` | 8 | 154601 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_13/output.md` |
| `agent_14` | 8 | 73506 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_14/output.md` |
| `agent_15` | 8 | 163834 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_15/output.md` |
| `agent_16` | 8 | 51877 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_16/output.md` |
| `agent_17` | 8 | 92977 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_17/output.md` |
| `agent_18` | 8 | 66546 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_18/output.md` |
| `agent_19` | 8 | 47649 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_19/output.md` |
| `agent_20` | 8 | 92761 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_20/output.md` |
| `agent_21` | 8 | 49772 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_21/output.md` |
| `agent_22` | 8 | 43982 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_22/output.md` |
| `agent_23` | 8 | 64396 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_23/output.md` |
| `agent_24` | 8 | 78331 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_24/output.md` |
| `agent_25` | 8 | 70802 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_25/output.md` |
| `agent_26` | 8 | 70616 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_26/output.md` |
| `agent_27` | 8 | 331706 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_27/output.md` |
| `agent_28` | 8 | 210201 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_28/output.md` |
| `agent_29` | 8 | 63247 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_29/output.md` |
| `agent_30` | 8 | 72764 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_30/output.md` |

## Verification

```json
{
  "branch": "h2-dev",
  "research_items": 251,
  "status_files": 30,
  "complete_status_files": 30,
  "output_files": 30,
  "problems": 0
}
```
