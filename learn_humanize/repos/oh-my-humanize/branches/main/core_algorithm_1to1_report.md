# oh-my-humanize `main` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `main`
- Repo: `oh-my-humanize`
- Source remote: `https://github.com/PolyArch/oh-my-humanize.git`
- Source commit: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- Source tree: `3ffa5b519699a566bb59ebd4eed3f819c29bf7e7`
- Read-only source export: `/Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker count: `30`
- Recursive source files excluding .git: `4541`
- Recursive source directories excluding .git: `501`
- Included core algorithm items: `3619`
- Skipped non-core paths: `1423`
- Status files complete: `30 / 30`
- Output files: `30 / 30`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 35039469 |
| `.fallowrc.jsonc` | 1 | 1 | 0 | 1212 |
| `AGENTS.md` | 1 | 1 | 0 | 17007 |
| `Cargo.toml` | 1 | 1 | 0 | 24798 |
| `README.md` | 1 | 1 | 0 | 35217 |
| `biome.json` | 1 | 1 | 0 | 1442 |
| `bunfig.toml` | 1 | 1 | 0 | 617 |
| `crates` | 97 | 84 | 13 | 9040106 |
| `docs` | 75 | 72 | 3 | 2607980 |
| `infra` | 3 | 2 | 1 | 26762 |
| `packages` | 3279 | 3030 | 249 | 146916273 |
| `python` | 97 | 84 | 13 | 5316610 |
| `rust-analyzer.toml` | 1 | 1 | 0 | 118 |
| `rust-toolchain.toml` | 1 | 1 | 0 | 160 |
| `rustfmt.toml` | 1 | 1 | 0 | 1568 |
| `scripts` | 56 | 53 | 3 | 1743302 |
| `tsconfig.base.json` | 1 | 1 | 0 | 488 |
| `tsconfig.tools.json` | 1 | 1 | 0 | 276 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_01` | 121 | 39521168 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_01/output.md` |
| `agent_02` | 121 | 3286525 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_02/output.md` |
| `agent_03` | 121 | 4189852 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_03/output.md` |
| `agent_04` | 121 | 2516134 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_04/output.md` |
| `agent_05` | 121 | 34216679 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_05/output.md` |
| `agent_06` | 121 | 7686267 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_06/output.md` |
| `agent_07` | 121 | 6167605 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_07/output.md` |
| `agent_08` | 121 | 2162504 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_08/output.md` |
| `agent_09` | 121 | 3754058 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_09/output.md` |
| `agent_10` | 121 | 2884532 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_10/output.md` |
| `agent_11` | 121 | 2850520 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_11/output.md` |
| `agent_12` | 121 | 2652485 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_12/output.md` |
| `agent_13` | 121 | 13941975 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_13/output.md` |
| `agent_14` | 121 | 8821361 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_14/output.md` |
| `agent_15` | 121 | 1545425 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_15/output.md` |
| `agent_16` | 121 | 4428106 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_16/output.md` |
| `agent_17` | 121 | 3728097 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_17/output.md` |
| `agent_18` | 121 | 1998318 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_18/output.md` |
| `agent_19` | 121 | 2252437 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_19/output.md` |
| `agent_20` | 120 | 2921711 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_20/output.md` |
| `agent_21` | 120 | 3374195 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_21/output.md` |
| `agent_22` | 120 | 3231497 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_22/output.md` |
| `agent_23` | 120 | 2456174 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_23/output.md` |
| `agent_24` | 120 | 3473422 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_24/output.md` |
| `agent_25` | 120 | 2460994 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_25/output.md` |
| `agent_26` | 120 | 6285053 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_26/output.md` |
| `agent_27` | 120 | 3916606 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_27/output.md` |
| `agent_28` | 120 | 19193241 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_28/output.md` |
| `agent_29` | 120 | 1963914 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_29/output.md` |
| `agent_30` | 120 | 2892550 | `research_runs/2026-06-19_oh_my_humanize_branch_1to1/agents/agent_30/output.md` |

## Verification

```json
{
  "branch": "main",
  "research_items": 3619,
  "status_files": 30,
  "complete_status_files": 30,
  "output_files": 30,
  "problems": 0
}
```
## Incremental Refresh - oh-my-humanize/main `bf4509d4f`

Remote `oh-my-humanize/main` advanced after the original full run. The source export, manifest, indexes, and affected item evidence were refreshed to source commit `bf4509d4f5a669375b3c88510ba0449e9770884c` / tree `3ffa5b519699a566bb59ebd4eed3f819c29bf7e7`.

Changed core algorithm items refreshed by incremental workers:

- `OH_MY_HUMANIZE_MAIN-HZ-1967` `packages/coding-agent/src/cli/workflow-cli.ts`: headless JS workflow scripts now execute from requested cwd.
- `OH_MY_HUMANIZE_MAIN-HZ-2432` `packages/coding-agent/src/workflow/runner.ts`: node execution is raced against abort so ignored aborts still checkpoint.
- `OH_MY_HUMANIZE_MAIN-HZ-2763` `packages/coding-agent/test/workflow/runner.test.ts`: regression coverage for ignored node abort checkpointing.
- `OH_MY_HUMANIZE_MAIN-HZ-2969` `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts`: regression coverage for JS cwd and headless SIGINT checkpointing.

Incremental evidence lives under `research_runs/2026-06-20_oh_my_humanize_main_incremental/agents/*/output.md` and is appended to the corresponding original worker output.
### Directory Item Refresh Coverage

The same incremental refresh also updated ancestor directory item evidence for the changed workflow CLI/runner/test files: `.`, `packages`, `packages/coding-agent`, `packages/coding-agent/src`, `packages/coding-agent/src/cli`, `packages/coding-agent/src/workflow`, `packages/coding-agent/test`, `packages/coding-agent/test/workflow`, and `packages/coding-agent/src/cli/__tests__`. Directory addenda live in `research_runs/2026-06-20_oh_my_humanize_main_incremental_dirs/agents/*/output.md` and are appended to the original directory worker outputs.
