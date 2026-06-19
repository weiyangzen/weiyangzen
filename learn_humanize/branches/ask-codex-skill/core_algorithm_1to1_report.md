# Humanize `ask-codex-skill` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `ask-codex-skill`
- Source commit: `caf375a20530c8bb81e8e8e103a8598c25c11bb0`
- Source tree: `cb4d25ddf1911f588dce6e4c285c9ed74b58b61a`
- Read-only source export: `/Users/wangweiyang/GitHub/humanize_branch_worktrees/ask-codex-skill`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker count: `30`
- Recursive source files excluding .git: `165`
- Recursive source directories excluding .git: `23`
- Included core algorithm items: `163`
- Skipped non-core paths: `25`
- Status files complete: `30 / 30`
- Output files: `30 / 30`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 1465377 |
| `README.md` | 1 | 1 | 0 | 9066 |
| `agents` | 2 | 1 | 1 | 3576 |
| `commands` | 6 | 5 | 1 | 43286 |
| `hooks` | 14 | 12 | 2 | 569616 |
| `prompt-template` | 62 | 56 | 6 | 140094 |
| `scripts` | 15 | 13 | 2 | 485376 |
| `skills` | 3 | 1 | 2 | 4167 |
| `tests` | 59 | 57 | 2 | 2065254 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_01` | 6 | 1498266 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_01/output.md` |
| `agent_02` | 6 | 34623 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_02/output.md` |
| `agent_03` | 6 | 48923 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_03/output.md` |
| `agent_04` | 6 | 358276 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_04/output.md` |
| `agent_05` | 6 | 60456 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_05/output.md` |
| `agent_06` | 6 | 280861 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_06/output.md` |
| `agent_07` | 6 | 53431 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_07/output.md` |
| `agent_08` | 6 | 970780 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_08/output.md` |
| `agent_09` | 6 | 33993 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_09/output.md` |
| `agent_10` | 6 | 89428 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_10/output.md` |
| `agent_11` | 6 | 94471 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_11/output.md` |
| `agent_12` | 6 | 87502 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_12/output.md` |
| `agent_13` | 6 | 25668 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_13/output.md` |
| `agent_14` | 5 | 54175 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_14/output.md` |
| `agent_15` | 5 | 108343 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_15/output.md` |
| `agent_16` | 5 | 91528 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_16/output.md` |
| `agent_17` | 5 | 6286 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_17/output.md` |
| `agent_18` | 5 | 318830 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_18/output.md` |
| `agent_19` | 5 | 14473 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_19/output.md` |
| `agent_20` | 5 | 24944 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_20/output.md` |
| `agent_21` | 5 | 31629 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_21/output.md` |
| `agent_22` | 5 | 48553 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_22/output.md` |
| `agent_23` | 5 | 42365 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_23/output.md` |
| `agent_24` | 5 | 30760 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_24/output.md` |
| `agent_25` | 5 | 73508 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_25/output.md` |
| `agent_26` | 5 | 65270 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_26/output.md` |
| `agent_27` | 5 | 44821 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_27/output.md` |
| `agent_28` | 5 | 87474 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_28/output.md` |
| `agent_29` | 5 | 53198 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_29/output.md` |
| `agent_30` | 5 | 52977 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_30/output.md` |

## Verification

```json
{
  "branch": "ask-codex-skill",
  "research_items": 163,
  "status_files": 30,
  "complete_status_files": 30,
  "output_files": 30,
  "problems": 0
}
```
