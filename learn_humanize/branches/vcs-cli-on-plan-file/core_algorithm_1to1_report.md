# Humanize `vcs-cli-on-plan-file` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `vcs-cli-on-plan-file`
- Repo: `humanize`
- Source remote: `https://github.com/PolyArch/humanize.git`
- Source commit: `4dd1ca2fece39d3c6d7f84965cd71bda02489397`
- Source tree: `2eceab4140baa5aa2a6130625bfe3e91590ceb99`
- Read-only source export: `/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker slots: `30`
- Worker jobs: `70`
- Active worker refill target: `25`
- Refill interval seconds: `120`
- Recursive source files excluding .git: `69`
- Recursive source directories excluding .git: `14`
- Included core algorithm items: `70`
- Skipped non-core paths: `13`
- Status files complete: `70 / 70`
- Output files: `70 / 70`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 261423 |
| `README.md` | 1 | 1 | 0 | 11734 |
| `commands` | 3 | 2 | 1 | 6804 |
| `hooks` | 12 | 10 | 2 | 199016 |
| `prompt-template` | 43 | 39 | 4 | 83625 |
| `scripts` | 4 | 3 | 1 | 87736 |
| `tests` | 6 | 5 | 1 | 168888 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_01` | 1 | 261423 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_01/output.md` |
| `agent_02` | 1 | 3402 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_02/output.md` |
| `agent_03` | 1 | 90100 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_03/output.md` |
| `agent_04` | 1 | 27875 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_04/output.md` |
| `agent_05` | 1 | 43868 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_05/output.md` |
| `agent_06` | 1 | 84444 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_06/output.md` |
| `agent_07` | 1 | 11734 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_07/output.md` |
| `agent_08` | 1 | 18816 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_08/output.md` |
| `agent_09` | 1 | 16015 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_09/output.md` |
| `agent_10` | 1 | 2735 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_10/output.md` |
| `agent_11` | 1 | 9125 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_11/output.md` |
| `agent_12` | 1 | 995 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_12/output.md` |
| `agent_13` | 1 | 2407 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_13/output.md` |
| `agent_14` | 1 | 4425 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_14/output.md` |
| `agent_15` | 1 | 1397 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_15/output.md` |
| `agent_16` | 1 | 7570 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_16/output.md` |
| `agent_17` | 1 | 33963 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_17/output.md` |
| `agent_18` | 1 | 3558 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_18/output.md` |
| `agent_19` | 1 | 11017 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_19/output.md` |
| `agent_20` | 1 | 4005 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_20/output.md` |
| `agent_21` | 1 | 5349 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_21/output.md` |
| `agent_22` | 1 | 22548 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_22/output.md` |
| `agent_23` | 1 | 2116 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_23/output.md` |
| `agent_24` | 1 | 19204 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_24/output.md` |
| `agent_25` | 1 | 3652 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_25/output.md` |
| `agent_26` | 1 | 35581 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_26/output.md` |
| `agent_27` | 1 | 18077 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_27/output.md` |
| `agent_28` | 1 | 7144 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_28/output.md` |
| `agent_29` | 1 | 19990 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_29/output.md` |
| `agent_30` | 1 | 12414 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_30/output.md` |
| `agent_31` | 1 | 6402 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_31/output.md` |
| `agent_32` | 1 | 1101 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_32/output.md` |
| `agent_33` | 1 | 441 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_33/output.md` |
| `agent_34` | 1 | 255 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_34/output.md` |
| `agent_35` | 1 | 451 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_35/output.md` |
| `agent_36` | 1 | 817 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_36/output.md` |
| `agent_37` | 1 | 270 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_37/output.md` |
| `agent_38` | 1 | 289 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_38/output.md` |
| `agent_39` | 1 | 792 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_39/output.md` |
| `agent_40` | 1 | 707 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_40/output.md` |
| `agent_41` | 1 | 442 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_41/output.md` |
| `agent_42` | 1 | 1088 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_42/output.md` |
| `agent_43` | 1 | 599 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_43/output.md` |
| `agent_44` | 1 | 540 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_44/output.md` |
| `agent_45` | 1 | 1242 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_45/output.md` |
| `agent_46` | 1 | 739 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_46/output.md` |
| `agent_47` | 1 | 376 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_47/output.md` |
| `agent_48` | 1 | 514 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_48/output.md` |
| `agent_49` | 1 | 967 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_49/output.md` |
| `agent_50` | 1 | 462 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_50/output.md` |
| `agent_51` | 1 | 887 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_51/output.md` |
| `agent_52` | 1 | 413 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_52/output.md` |
| `agent_53` | 1 | 238 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_53/output.md` |
| `agent_54` | 1 | 302 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_54/output.md` |
| `agent_55` | 1 | 253 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_55/output.md` |
| `agent_56` | 1 | 348 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_56/output.md` |
| `agent_57` | 1 | 335 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_57/output.md` |
| `agent_58` | 1 | 152 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_58/output.md` |
| `agent_59` | 1 | 318 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_59/output.md` |
| `agent_60` | 1 | 343 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_60/output.md` |
| `agent_61` | 1 | 225 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_61/output.md` |
| `agent_62` | 1 | 109 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_62/output.md` |
| `agent_63` | 1 | 573 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_63/output.md` |
| `agent_64` | 1 | 465 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_64/output.md` |
| `agent_65` | 1 | 1206 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_65/output.md` |
| `agent_66` | 1 | 390 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_66/output.md` |
| `agent_67` | 1 | 101 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_67/output.md` |
| `agent_68` | 1 | 4180 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_68/output.md` |
| `agent_69` | 1 | 1047 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_69/output.md` |
| `agent_70` | 1 | 3898 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_70/output.md` |

## Verification

```json
{
  "branch": "vcs-cli-on-plan-file",
  "research_items": 70,
  "required_worker_jobs": 70,
  "status_files": 70,
  "complete_status_files": 70,
  "output_files": 70,
  "problems": 0
}
```
