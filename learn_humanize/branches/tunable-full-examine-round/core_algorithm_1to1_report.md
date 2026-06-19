# Humanize `tunable-full-examine-round` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `tunable-full-examine-round`
- Repo: `humanize`
- Source remote: `https://github.com/PolyArch/humanize.git`
- Source commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`
- Source tree: `963d7c2de33adb281d457398c9498e54b9c36e7b`
- Read-only source export: `/Users/wangweiyang/GitHub/humanize_branch_worktrees/tunable-full-examine-round`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker slots: `30`
- Worker jobs: `144`
- Active worker refill target: `25`
- Refill interval seconds: `120`
- Recursive source files excluding .git: `148`
- Recursive source directories excluding .git: `21`
- Included core algorithm items: `144`
- Skipped non-core paths: `25`
- Status files complete: `144 / 144`
- Output files: `144 / 144`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 1312351 |
| `README.md` | 1 | 1 | 0 | 6564 |
| `agents` | 2 | 1 | 1 | 3576 |
| `commands` | 6 | 5 | 1 | 43206 |
| `hooks` | 13 | 11 | 2 | 531322 |
| `prompt-template` | 58 | 52 | 6 | 122982 |
| `scripts` | 14 | 12 | 2 | 419490 |
| `tests` | 49 | 47 | 2 | 1873545 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_001` | 1 | 1312351 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_001/output.md` |
| `agent_002` | 1 | 1788 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_002/output.md` |
| `agent_003` | 1 | 21603 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_003/output.md` |
| `agent_004` | 1 | 237258 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_004/output.md` |
| `agent_005` | 1 | 40994 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_005/output.md` |
| `agent_006` | 1 | 201027 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_006/output.md` |
| `agent_007` | 1 | 803117 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_007/output.md` |
| `agent_008` | 1 | 6564 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_008/output.md` |
| `agent_009` | 1 | 56806 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_009/output.md` |
| `agent_010` | 1 | 13996 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_010/output.md` |
| `agent_011` | 1 | 6893 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_011/output.md` |
| `agent_012` | 1 | 10385 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_012/output.md` |
| `agent_013` | 1 | 2959 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_013/output.md` |
| `agent_014` | 1 | 6761 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_014/output.md` |
| `agent_015` | 1 | 17436 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_015/output.md` |
| `agent_016` | 1 | 267311 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_016/output.md` |
| `agent_017` | 1 | 1788 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_017/output.md` |
| `agent_018` | 1 | 953 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_018/output.md` |
| `agent_019` | 1 | 1914 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_019/output.md` |
| `agent_020` | 1 | 12548 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_020/output.md` |
| `agent_021` | 1 | 2349 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_021/output.md` |
| `agent_022` | 1 | 3839 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_022/output.md` |
| `agent_023` | 1 | 4754 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_023/output.md` |
| `agent_024` | 1 | 1580 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_024/output.md` |
| `agent_025` | 1 | 16755 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_025/output.md` |
| `agent_026` | 1 | 60345 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_026/output.md` |
| `agent_027` | 1 | 5982 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_027/output.md` |
| `agent_028` | 1 | 7983 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_028/output.md` |
| `agent_029` | 1 | 5210 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_029/output.md` |
| `agent_030` | 1 | 9044 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_030/output.md` |
| `agent_031` | 1 | 68799 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_031/output.md` |
| `agent_032` | 1 | 3498 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_032/output.md` |
| `agent_033` | 1 | 4248 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_033/output.md` |
| `agent_034` | 1 | 11495 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_034/output.md` |
| `agent_035` | 1 | 9834 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_035/output.md` |
| `agent_036` | 1 | 14503 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_036/output.md` |
| `agent_037` | 1 | 55359 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_037/output.md` |
| `agent_038` | 1 | 9682 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_038/output.md` |
| `agent_039` | 1 | 2116 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_039/output.md` |
| `agent_040` | 1 | 29557 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_040/output.md` |
| `agent_041` | 1 | 38477 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_041/output.md` |
| `agent_042` | 1 | 4822 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_042/output.md` |
| `agent_043` | 1 | 2527 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_043/output.md` |
| `agent_044` | 1 | 4629 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_044/output.md` |
| `agent_045` | 1 | 2860 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_045/output.md` |
| `agent_046` | 1 | 2066 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_046/output.md` |
| `agent_047` | 1 | 14613 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_047/output.md` |
| `agent_048` | 1 | 5801 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_048/output.md` |
| `agent_049` | 1 | 6658 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_049/output.md` |
| `agent_050` | 1 | 41264 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_050/output.md` |
| `agent_051` | 1 | 10985 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_051/output.md` |
| `agent_052` | 1 | 7691 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_052/output.md` |
| `agent_053` | 1 | 31038 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_053/output.md` |
| `agent_054` | 1 | 18858 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_054/output.md` |
| `agent_055` | 1 | 2594 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_055/output.md` |
| `agent_056` | 1 | 12037 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_056/output.md` |
| `agent_057` | 1 | 30012 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_057/output.md` |
| `agent_058` | 1 | 13242 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_058/output.md` |
| `agent_059` | 1 | 35614 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_059/output.md` |
| `agent_060` | 1 | 22893 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_060/output.md` |
| `agent_061` | 1 | 51873 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_061/output.md` |
| `agent_062` | 1 | 4240 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_062/output.md` |
| `agent_063` | 1 | 12471 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_063/output.md` |
| `agent_064` | 1 | 55475 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_064/output.md` |
| `agent_065` | 1 | 66645 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_065/output.md` |
| `agent_066` | 1 | 1302 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_066/output.md` |
| `agent_067` | 1 | 9039 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_067/output.md` |
| `agent_068` | 1 | 21290 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_068/output.md` |
| `agent_069` | 1 | 7095 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_069/output.md` |
| `agent_070` | 1 | 19978 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_070/output.md` |
| `agent_071` | 1 | 10351 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_071/output.md` |
| `agent_072` | 1 | 10665 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_072/output.md` |
| `agent_073` | 1 | 49692 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_073/output.md` |
| `agent_074` | 1 | 7114 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_074/output.md` |
| `agent_075` | 1 | 776 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_075/output.md` |
| `agent_076` | 1 | 441 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_076/output.md` |
| `agent_077` | 1 | 344 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_077/output.md` |
| `agent_078` | 1 | 630 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_078/output.md` |
| `agent_079` | 1 | 1125 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_079/output.md` |
| `agent_080` | 1 | 237 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_080/output.md` |
| `agent_081` | 1 | 451 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_081/output.md` |
| `agent_082` | 1 | 817 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_082/output.md` |
| `agent_083` | 1 | 270 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_083/output.md` |
| `agent_084` | 1 | 326 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_084/output.md` |
| `agent_085` | 1 | 289 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_085/output.md` |
| `agent_086` | 1 | 792 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_086/output.md` |
| `agent_087` | 1 | 707 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_087/output.md` |
| `agent_088` | 1 | 442 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_088/output.md` |
| `agent_089` | 1 | 1088 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_089/output.md` |
| `agent_090` | 1 | 515 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_090/output.md` |
| `agent_091` | 1 | 257 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_091/output.md` |
| `agent_092` | 1 | 385 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_092/output.md` |
| `agent_093` | 1 | 360 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_093/output.md` |
| `agent_094` | 1 | 329 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_094/output.md` |
| `agent_095` | 1 | 413 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_095/output.md` |
| `agent_096` | 1 | 379 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_096/output.md` |
| `agent_097` | 1 | 238 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_097/output.md` |
| `agent_098` | 1 | 302 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_098/output.md` |
| `agent_099` | 1 | 253 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_099/output.md` |
| `agent_100` | 1 | 348 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_100/output.md` |
| `agent_101` | 1 | 335 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_101/output.md` |
| `agent_102` | 1 | 152 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_102/output.md` |
| `agent_103` | 1 | 318 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_103/output.md` |
| `agent_104` | 1 | 343 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_104/output.md` |
| `agent_105` | 1 | 225 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_105/output.md` |
| `agent_106` | 1 | 109 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_106/output.md` |
| `agent_107` | 1 | 1695 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_107/output.md` |
| `agent_108` | 1 | 1605 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_108/output.md` |
| `agent_109` | 1 | 573 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_109/output.md` |
| `agent_110` | 1 | 448 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_110/output.md` |
| `agent_111` | 1 | 1206 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_111/output.md` |
| `agent_112` | 1 | 390 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_112/output.md` |
| `agent_113` | 1 | 101 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_113/output.md` |
| `agent_114` | 1 | 875 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_114/output.md` |
| `agent_115` | 1 | 1273 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_115/output.md` |
| `agent_116` | 1 | 4167 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_116/output.md` |
| `agent_117` | 1 | 1047 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_117/output.md` |
| `agent_118` | 1 | 3898 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_118/output.md` |
| `agent_119` | 1 | 2959 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_119/output.md` |
| `agent_120` | 1 | 2008 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_120/output.md` |
| `agent_121` | 1 | 654 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_121/output.md` |
| `agent_122` | 1 | 585 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_122/output.md` |
| `agent_123` | 1 | 725 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_123/output.md` |
| `agent_124` | 1 | 333 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_124/output.md` |
| `agent_125` | 1 | 1390 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_125/output.md` |
| `agent_126` | 1 | 1066 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_126/output.md` |
| `agent_127` | 1 | 17436 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_127/output.md` |
| `agent_128` | 1 | 6042 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_128/output.md` |
| `agent_129` | 1 | 14738 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_129/output.md` |
| `agent_130` | 1 | 16016 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_130/output.md` |
| `agent_131` | 1 | 14267 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_131/output.md` |
| `agent_132` | 1 | 13967 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_132/output.md` |
| `agent_133` | 1 | 22458 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_133/output.md` |
| `agent_134` | 1 | 23690 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_134/output.md` |
| `agent_135` | 1 | 12849 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_135/output.md` |
| `agent_136` | 1 | 14625 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_136/output.md` |
| `agent_137` | 1 | 26629 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_137/output.md` |
| `agent_138` | 1 | 10008 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_138/output.md` |
| `agent_139` | 1 | 38326 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_139/output.md` |
| `agent_140` | 1 | 13794 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_140/output.md` |
| `agent_141` | 1 | 12289 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_141/output.md` |
| `agent_142` | 1 | 10937 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_142/output.md` |
| `agent_143` | 1 | 8882 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_143/output.md` |
| `agent_144` | 1 | 7794 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_144/output.md` |

## Verification

```json
{
  "branch": "tunable-full-examine-round",
  "research_items": 144,
  "required_worker_jobs": 144,
  "status_files": 144,
  "complete_status_files": 144,
  "output_files": 144,
  "problems": 0
}
```
