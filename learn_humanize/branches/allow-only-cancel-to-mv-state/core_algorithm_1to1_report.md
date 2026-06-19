# Humanize `allow-only-cancel-to-mv-state` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `allow-only-cancel-to-mv-state`
- Source commit: `3c39192e9b738743cdc5305a83a797a5ca66889b`
- Source tree: `2f62748ab4b74130f357b879d61ec081e2f5d394`
- Read-only source export: `/Users/wangweiyang/GitHub/humanize_branch_worktrees/allow-only-cancel-to-mv-state`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker count: `30`
- Recursive source files excluding .git: `72`
- Recursive source directories excluding .git: `14`
- Included core algorithm items: `72`
- Skipped non-core paths: `14`
- Status files complete: `30 / 30`
- Output files: `30 / 30`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 397421 |
| `README.md` | 1 | 1 | 0 | 9596 |
| `commands` | 3 | 2 | 1 | 7882 |
| `hooks` | 12 | 10 | 2 | 228320 |
| `prompt-template` | 37 | 33 | 4 | 65304 |
| `scripts` | 4 | 3 | 1 | 112798 |
| `tests` | 14 | 13 | 1 | 407668 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_01` | 3 | 432517 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_01/output.md` |
| `agent_02` | 3 | 27015 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_02/output.md` |
| `agent_03` | 3 | 111067 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_03/output.md` |
| `agent_04` | 3 | 43167 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_04/output.md` |
| `agent_05` | 3 | 64067 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_05/output.md` |
| `agent_06` | 3 | 224277 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_06/output.md` |
| `agent_07` | 3 | 21115 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_07/output.md` |
| `agent_08` | 3 | 42384 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_08/output.md` |
| `agent_09` | 3 | 17147 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_09/output.md` |
| `agent_10` | 3 | 7332 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_10/output.md` |
| `agent_11` | 3 | 10385 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_11/output.md` |
| `agent_12` | 3 | 5880 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_12/output.md` |
| `agent_13` | 2 | 3227 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_13/output.md` |
| `agent_14` | 2 | 4766 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_14/output.md` |
| `agent_15` | 2 | 1728 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_15/output.md` |
| `agent_16` | 2 | 11749 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_16/output.md` |
| `agent_17` | 2 | 37900 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_17/output.md` |
| `agent_18` | 2 | 5124 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_18/output.md` |
| `agent_19` | 2 | 8113 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_19/output.md` |
| `agent_20` | 2 | 5495 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_20/output.md` |
| `agent_21` | 2 | 6627 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_21/output.md` |
| `agent_22` | 2 | 30027 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_22/output.md` |
| `agent_23` | 2 | 2529 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_23/output.md` |
| `agent_24` | 2 | 25033 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_24/output.md` |
| `agent_25` | 2 | 2981 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_25/output.md` |
| `agent_26` | 2 | 14875 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_26/output.md` |
| `agent_27` | 2 | 6054 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_27/output.md` |
| `agent_28` | 2 | 7006 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_28/output.md` |
| `agent_29` | 2 | 41559 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_29/output.md` |
| `agent_30` | 2 | 7843 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_30/output.md` |

## Verification

```json
{
  "branch": "allow-only-cancel-to-mv-state",
  "research_items": 72,
  "status_files": 30,
  "complete_status_files": 30,
  "output_files": 30,
  "problems": 0
}
```
