# Humanize Core Algorithm 1:1 Research Report

## Executive Result

The corrected rerun uses execution-cron style 1:1 coverage: every retained core algorithm file or directory is an individual checklist item, assigned to exactly one worker and verified in that worker output. The prior topic-style report was removed from the active artifact set.

## Run Facts

- Source repository: `https://github.com/PolyArch/humanize.git`
- Source checkout: `/Users/wangweiyang/GitHub/humanize`
- Source commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`
- tmux session: `humanize_core_1to1_20260619`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker count: `30`
- Recursive source files excluding .git: `204`
- Recursive source directories excluding .git: `32`
- Included core algorithm items: `201`
- Skipped non-core paths: `35`
- Status files complete: `30 / 30`
- Output files: `30 / 30`

## 1:1 Coverage Contract

- `path_inventory.tsv` lists every file and directory under the source checkout, recursively excluding `.git`.
- `research_list.tsv` is the authoritative included subset; each row has one `HZ-*` item ID and one assigned worker.
- `coverage_matrix.tsv` proves that each included item has a complete status file, an output file, and at least one matching item ID in the assigned output.
- `execution_blueprint.md` and `todos_20260619.md` use the execution-cron dual cursor; after master verification all 201 items are `[x]`.
- Non-core files/directories are not researched, but are retained in `skipped_paths.tsv` with explicit skip reasons.

## Included/Skipped Counts

| Bucket | Count |
|---|---:|
| Included files | 176 |
| Included directories | 25 |
| Included total | 201 |
| Skipped paths | 35 |
| Worker outputs | 30 |

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 1710486 |
| `README.md` | 1 | 1 | 0 | 4110 |
| `agents` | 5 | 4 | 1 | 24522 |
| `commands` | 6 | 5 | 1 | 162260 |
| `config` | 3 | 2 | 1 | 1124 |
| `docs` | 3 | 2 | 1 | 35106 |
| `hooks` | 16 | 14 | 2 | 649655 |
| `prompt-template` | 70 | 64 | 6 | 182682 |
| `scripts` | 20 | 18 | 2 | 563480 |
| `skills` | 13 | 6 | 7 | 77334 |
| `templates` | 2 | 1 | 1 | 1374 |
| `tests` | 61 | 59 | 2 | 2202781 |

## Core Algorithm Synthesis

Humanize is best described as a prompt-and-hook workflow algorithm rather than a numeric or ML algorithm. The core algorithm subset is the RLCR loop and its surrounding gates: command prompts define how plans are generated/refined, setup scripts initialize loop state, hooks enforce stop-time transitions, validators protect state and output surfaces, Codex review gates block unsafe completion, BitLesson selectors/validators preserve memory deltas, and tests encode the executable state-machine contract.

The 1:1 evidence preserves both file-level and directory-level views. Directory items record coordination behavior across descendants; file items record concrete state parsing, gate enforcement, prompt contracts, and validation rules. This avoids the earlier topic-only coverage gap while still skipping non-core CI, packaging, image, installer, fixture, and mock paths.

## Main Algorithm Areas

- `commands/`: user-facing command protocols for generating plans, refining plans, starting/canceling RLCR loops, and ideation.
- `hooks/`: runtime enforcement layer for stop hooks, validators, protected-file policies, background task handling, and template loading.
- `scripts/`: shell algorithms for setup, routing, model selection, monitors, BitLesson selection/delta validation, IO validation, and stop-gate checks.
- `prompt-template/`: gate and transition text consumed by the workflow; these templates are operational policy, not passive docs.
- `agents/` and `skills/`: higher-level research, compliance, and usage algorithms that drive or constrain the loop.
- `tests/`: executable specification for transition, robustness, validator, monitor, and review behavior. Fixture/mock paths are skipped because they are support data rather than algorithm logic.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_01` | 7 | 1760289 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_01/output.md` |
| `agent_02` | 7 | 72525 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_02/output.md` |
| `agent_03` | 7 | 180132 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_03/output.md` |
| `agent_04` | 7 | 71064 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_04/output.md` |
| `agent_05` | 7 | 61247 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_05/output.md` |
| `agent_06` | 7 | 290960 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_06/output.md` |
| `agent_07` | 7 | 114159 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_07/output.md` |
| `agent_08` | 7 | 361701 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_08/output.md` |
| `agent_09` | 7 | 69963 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_09/output.md` |
| `agent_10` | 7 | 49182 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_10/output.md` |
| `agent_11` | 7 | 1029505 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_11/output.md` |
| `agent_12` | 7 | 83609 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_12/output.md` |
| `agent_13` | 7 | 230539 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_13/output.md` |
| `agent_14` | 7 | 107893 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_14/output.md` |
| `agent_15` | 7 | 80219 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_15/output.md` |
| `agent_16` | 7 | 85353 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_16/output.md` |
| `agent_17` | 7 | 60849 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_17/output.md` |
| `agent_18` | 7 | 105552 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_18/output.md` |
| `agent_19` | 7 | 80760 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_19/output.md` |
| `agent_20` | 7 | 37233 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_20/output.md` |
| `agent_21` | 7 | 29223 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_21/output.md` |
| `agent_22` | 6 | 60740 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_22/output.md` |
| `agent_23` | 6 | 44900 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_23/output.md` |
| `agent_24` | 6 | 20394 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_24/output.md` |
| `agent_25` | 6 | 74560 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_25/output.md` |
| `agent_26` | 6 | 278243 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_26/output.md` |
| `agent_27` | 6 | 11462 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_27/output.md` |
| `agent_28` | 6 | 94839 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_28/output.md` |
| `agent_29` | 6 | 40141 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_29/output.md` |
| `agent_30` | 6 | 27678 | `research_runs/2026-06-19_humanize_core_1to1/agents/agent_30/output.md` |

## Skipped Non-Core Categories

- 9: fixture/mock data; not a core algorithm file
- 7: directory only contains skipped non-core files
- 6: CI workflow; not core algorithm runtime or specification
- 4: installer utility; skipped as non-core algorithm content
- 3: installation guide; skipped as non-core algorithm content
- 2: plugin packaging metadata; not core algorithm runtime or specification
- 2: visual asset; no algorithm text/code to research
- 1: local assistant instruction surface; not repository algorithm behavior
- 1: metadata only; not algorithm behavior

## Verification

The master verifier was run after the 30 tmux workers completed. Result:

```json
{
  "research_items": 201,
  "status_files": 30,
  "complete_status_files": 30,
  "output_files": 30,
  "coverage_problems": 0
}
```

Run `python3 research_runs/2026-06-19_humanize_core_1to1/verify_coverage.py` from this directory to reproduce the coverage gate.
