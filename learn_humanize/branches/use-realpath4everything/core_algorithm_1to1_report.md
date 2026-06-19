# Humanize `use-realpath4everything` Core Algorithm 1:1 Research Report

## Executive Result

This branch uses the same execution-cron 1:1 coverage protocol: every retained core algorithm file or directory is an individual checklist item, assigned to one worker and verified in that worker output.

## Run Facts

- Branch: `use-realpath4everything`
- Repo: `humanize`
- Source remote: `https://github.com/PolyArch/humanize.git`
- Source commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`
- Source tree: `e82a446dc9fb060a3c0edf5156d4934bee330e53`
- Read-only source export: `/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything`
- Codex model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Worker slots: `30`
- Worker jobs: `197`
- Active worker refill target: `25`
- Refill interval seconds: `120`
- Recursive source files excluding .git: `201`
- Recursive source directories excluding .git: `31`
- Included core algorithm items: `197`
- Skipped non-core paths: `35`
- Status files complete: `197 / 197`
- Output files: `197 / 197`

## Included Paths By Top-Level Area

| Area | Items | Files | Directories | Bytes represented |
|---|---:|---:|---:|---:|
| `.` | 1 | 0 | 1 | 1688060 |
| `README.md` | 1 | 1 | 0 | 3745 |
| `agents` | 5 | 4 | 1 | 24522 |
| `commands` | 5 | 4 | 1 | 139888 |
| `config` | 3 | 2 | 1 | 1124 |
| `docs` | 3 | 2 | 1 | 35106 |
| `hooks` | 16 | 14 | 2 | 642115 |
| `prompt-template` | 68 | 63 | 5 | 181614 |
| `scripts` | 19 | 17 | 2 | 550814 |
| `skills` | 13 | 6 | 7 | 77334 |
| `templates` | 2 | 1 | 1 | 1374 |
| `tests` | 61 | 59 | 2 | 2201949 |

## Core Algorithm Synthesis

The branch's algorithm subset is the prompt/hook/script/test state-machine surface: commands define plan and RLCR entrypoints, hooks and validators enforce runtime transitions, prompt templates encode gate decisions, scripts implement setup/routing/monitoring/memory validation, and tests act as executable algorithm specifications. Non-core CI, install docs, assets, packaging metadata, fixtures, and mocks are tracked only as skipped paths.

## Worker Assignment Summary

| Worker | Items | Bytes | Evidence |
|---|---:|---:|---|
| `agent_001` | 1 | 1688060 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_001/output.md` |
| `agent_002` | 1 | 12261 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_002/output.md` |
| `agent_003` | 1 | 69944 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_003/output.md` |
| `agent_004` | 1 | 562 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_004/output.md` |
| `agent_005` | 1 | 17553 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_005/output.md` |
| `agent_006` | 1 | 270171 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_006/output.md` |
| `agent_007` | 1 | 60538 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_007/output.md` |
| `agent_008` | 1 | 254324 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_008/output.md` |
| `agent_009` | 1 | 25778 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_009/output.md` |
| `agent_010` | 1 | 687 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_010/output.md` |
| `agent_011` | 1 | 972497 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_011/output.md` |
| `agent_012` | 1 | 3745 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_012/output.md` |
| `agent_013` | 1 | 101773 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_013/output.md` |
| `agent_014` | 1 | 16588 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_014/output.md` |
| `agent_015` | 1 | 22925 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_015/output.md` |
| `agent_016` | 1 | 12759 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_016/output.md` |
| `agent_017` | 1 | 8266 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_017/output.md` |
| `agent_018` | 1 | 42166 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_018/output.md` |
| `agent_019` | 1 | 1983 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_019/output.md` |
| `agent_020` | 1 | 2410 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_020/output.md` |
| `agent_021` | 1 | 7446 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_021/output.md` |
| `agent_022` | 1 | 3958 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_022/output.md` |
| `agent_023` | 1 | 6293 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_023/output.md` |
| `agent_024` | 1 | 3688 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_024/output.md` |
| `agent_025` | 1 | 256955 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_025/output.md` |
| `agent_026` | 1 | 1444 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_026/output.md` |
| `agent_027` | 1 | 1788 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_027/output.md` |
| `agent_028` | 1 | 3619 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_028/output.md` |
| `agent_029` | 1 | 5410 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_029/output.md` |
| `agent_030` | 1 | 2060 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_030/output.md` |
| `agent_031` | 1 | 33068 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_031/output.md` |
| `agent_032` | 1 | 23115 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_032/output.md` |
| `agent_033` | 1 | 11701 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_033/output.md` |
| `agent_034` | 1 | 383 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_034/output.md` |
| `agent_035` | 1 | 179 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_035/output.md` |
| `agent_036` | 1 | 1896 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_036/output.md` |
| `agent_037` | 1 | 15657 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_037/output.md` |
| `agent_038` | 1 | 7509 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_038/output.md` |
| `agent_039` | 1 | 1633 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_039/output.md` |
| `agent_040` | 1 | 23517 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_040/output.md` |
| `agent_041` | 1 | 85635 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_041/output.md` |
| `agent_042` | 1 | 9920 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_042/output.md` |
| `agent_043` | 1 | 8082 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_043/output.md` |
| `agent_044` | 1 | 5807 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_044/output.md` |
| `agent_045` | 1 | 12504 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_045/output.md` |
| `agent_046` | 1 | 13791 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_046/output.md` |
| `agent_047` | 1 | 12042 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_047/output.md` |
| `agent_048` | 1 | 10944 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_048/output.md` |
| `agent_049` | 1 | 2136 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_049/output.md` |
| `agent_050` | 1 | 7777 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_050/output.md` |
| `agent_051` | 1 | 12319 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_051/output.md` |
| `agent_052` | 1 | 5930 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_052/output.md` |
| `agent_053` | 1 | 54644 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_053/output.md` |
| `agent_054` | 1 | 2124 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_054/output.md` |
| `agent_055` | 1 | 6019 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_055/output.md` |
| `agent_056` | 1 | 57169 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_056/output.md` |
| `agent_057` | 1 | 13554 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_057/output.md` |
| `agent_058` | 1 | 5758 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_058/output.md` |
| `agent_059` | 1 | 21742 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_059/output.md` |
| `agent_060` | 1 | 687 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_060/output.md` |
| `agent_061` | 1 | 2535 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_061/output.md` |
| `agent_062` | 1 | 9556 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_062/output.md` |
| `agent_063` | 1 | 575 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_063/output.md` |
| `agent_064` | 1 | 24577 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_064/output.md` |
| `agent_065` | 1 | 22380 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_065/output.md` |
| `agent_066` | 1 | 5809 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_066/output.md` |
| `agent_067` | 1 | 15982 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_067/output.md` |
| `agent_068` | 1 | 6666 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_068/output.md` |
| `agent_069` | 1 | 17115 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_069/output.md` |
| `agent_070` | 1 | 4403 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_070/output.md` |
| `agent_071` | 1 | 44941 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_071/output.md` |
| `agent_072` | 1 | 9966 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_072/output.md` |
| `agent_073` | 1 | 11000 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_073/output.md` |
| `agent_074` | 1 | 10729 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_074/output.md` |
| `agent_075` | 1 | 6134 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_075/output.md` |
| `agent_076` | 1 | 7516 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_076/output.md` |
| `agent_077` | 1 | 4898 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_077/output.md` |
| `agent_078` | 1 | 7699 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_078/output.md` |
| `agent_079` | 1 | 40143 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_079/output.md` |
| `agent_080` | 1 | 27572 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_080/output.md` |
| `agent_081` | 1 | 2602 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_081/output.md` |
| `agent_082` | 1 | 12604 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_082/output.md` |
| `agent_083` | 1 | 13603 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_083/output.md` |
| `agent_084` | 1 | 645 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_084/output.md` |
| `agent_085` | 1 | 22253 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_085/output.md` |
| `agent_086` | 1 | 637 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_086/output.md` |
| `agent_087` | 1 | 13290 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_087/output.md` |
| `agent_088` | 1 | 38107 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_088/output.md` |
| `agent_089` | 1 | 22916 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_089/output.md` |
| `agent_090` | 1 | 58394 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_090/output.md` |
| `agent_091` | 1 | 38452 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_091/output.md` |
| `agent_092` | 1 | 11569 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_092/output.md` |
| `agent_093` | 1 | 9047 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_093/output.md` |
| `agent_094` | 1 | 10477 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_094/output.md` |
| `agent_095` | 1 | 60057 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_095/output.md` |
| `agent_096` | 1 | 6208 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_096/output.md` |
| `agent_097` | 1 | 7335 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_097/output.md` |
| `agent_098` | 1 | 21298 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_098/output.md` |
| `agent_099` | 1 | 7103 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_099/output.md` |
| `agent_100` | 1 | 19983 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_100/output.md` |
| `agent_101` | 1 | 19987 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_101/output.md` |
| `agent_102` | 1 | 28114 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_102/output.md` |
| `agent_103` | 1 | 10665 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_103/output.md` |
| `agent_104` | 1 | 19107 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_104/output.md` |
| `agent_105` | 1 | 62888 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_105/output.md` |
| `agent_106` | 1 | 7465 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_106/output.md` |
| `agent_107` | 1 | 4785 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_107/output.md` |
| `agent_108` | 1 | 7528 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_108/output.md` |
| `agent_109` | 1 | 302 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_109/output.md` |
| `agent_110` | 1 | 301 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_110/output.md` |
| `agent_111` | 1 | 134 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_111/output.md` |
| `agent_112` | 1 | 207 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_112/output.md` |
| `agent_113` | 1 | 244 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_113/output.md` |
| `agent_114` | 1 | 776 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_114/output.md` |
| `agent_115` | 1 | 441 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_115/output.md` |
| `agent_116` | 1 | 283 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_116/output.md` |
| `agent_117` | 1 | 344 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_117/output.md` |
| `agent_118` | 1 | 1125 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_118/output.md` |
| `agent_119` | 1 | 237 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_119/output.md` |
| `agent_120` | 1 | 451 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_120/output.md` |
| `agent_121` | 1 | 945 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_121/output.md` |
| `agent_122` | 1 | 270 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_122/output.md` |
| `agent_123` | 1 | 326 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_123/output.md` |
| `agent_124` | 1 | 530 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_124/output.md` |
| `agent_125` | 1 | 289 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_125/output.md` |
| `agent_126` | 1 | 486 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_126/output.md` |
| `agent_127` | 1 | 707 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_127/output.md` |
| `agent_128` | 1 | 475 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_128/output.md` |
| `agent_129` | 1 | 1088 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_129/output.md` |
| `agent_130` | 1 | 496 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_130/output.md` |
| `agent_131` | 1 | 408 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_131/output.md` |
| `agent_132` | 1 | 510 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_132/output.md` |
| `agent_133` | 1 | 257 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_133/output.md` |
| `agent_134` | 1 | 385 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_134/output.md` |
| `agent_135` | 1 | 413 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_135/output.md` |
| `agent_136` | 1 | 155 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_136/output.md` |
| `agent_137` | 1 | 441 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_137/output.md` |
| `agent_138` | 1 | 379 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_138/output.md` |
| `agent_139` | 1 | 243 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_139/output.md` |
| `agent_140` | 1 | 394 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_140/output.md` |
| `agent_141` | 1 | 302 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_141/output.md` |
| `agent_142` | 1 | 284 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_142/output.md` |
| `agent_143` | 1 | 348 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_143/output.md` |
| `agent_144` | 1 | 335 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_144/output.md` |
| `agent_145` | 1 | 130 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_145/output.md` |
| `agent_146` | 1 | 152 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_146/output.md` |
| `agent_147` | 1 | 318 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_147/output.md` |
| `agent_148` | 1 | 343 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_148/output.md` |
| `agent_149` | 1 | 225 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_149/output.md` |
| `agent_150` | 1 | 109 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_150/output.md` |
| `agent_151` | 1 | 1767 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_151/output.md` |
| `agent_152` | 1 | 3111 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_152/output.md` |
| `agent_153` | 1 | 638 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_153/output.md` |
| `agent_154` | 1 | 2756 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_154/output.md` |
| `agent_155` | 1 | 1840 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_155/output.md` |
| `agent_156` | 1 | 1750 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_156/output.md` |
| `agent_157` | 1 | 708 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_157/output.md` |
| `agent_158` | 1 | 4030 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_158/output.md` |
| `agent_159` | 1 | 448 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_159/output.md` |
| `agent_160` | 1 | 2874 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_160/output.md` |
| `agent_161` | 1 | 181 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_161/output.md` |
| `agent_162` | 1 | 499 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_162/output.md` |
| `agent_163` | 1 | 101 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_163/output.md` |
| `agent_164` | 1 | 2222 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_164/output.md` |
| `agent_165` | 1 | 1273 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_165/output.md` |
| `agent_166` | 1 | 471 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_166/output.md` |
| `agent_167` | 1 | 4917 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_167/output.md` |
| `agent_168` | 1 | 1269 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_168/output.md` |
| `agent_169` | 1 | 4829 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_169/output.md` |
| `agent_170` | 1 | 5133 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_170/output.md` |
| `agent_171` | 1 | 3133 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_171/output.md` |
| `agent_172` | 1 | 4969 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_172/output.md` |
| `agent_173` | 1 | 2243 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_173/output.md` |
| `agent_174` | 1 | 13058 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_174/output.md` |
| `agent_175` | 1 | 21896 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_175/output.md` |
| `agent_176` | 1 | 1983 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_176/output.md` |
| `agent_177` | 1 | 2410 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_177/output.md` |
| `agent_178` | 1 | 3958 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_178/output.md` |
| `agent_179` | 1 | 6293 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_179/output.md` |
| `agent_180` | 1 | 3688 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_180/output.md` |
| `agent_181` | 1 | 7446 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_181/output.md` |
| `agent_182` | 1 | 6050 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_182/output.md` |
| `agent_183` | 1 | 14746 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_183/output.md` |
| `agent_184` | 1 | 14582 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_184/output.md` |
| `agent_185` | 1 | 14275 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_185/output.md` |
| `agent_186` | 1 | 16254 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_186/output.md` |
| `agent_187` | 1 | 22490 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_187/output.md` |
| `agent_188` | 1 | 29227 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_188/output.md` |
| `agent_189` | 1 | 13584 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_189/output.md` |
| `agent_190` | 1 | 15380 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_190/output.md` |
| `agent_191` | 1 | 10123 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_191/output.md` |
| `agent_192` | 1 | 44764 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_192/output.md` |
| `agent_193` | 1 | 15546 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_193/output.md` |
| `agent_194` | 1 | 12297 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_194/output.md` |
| `agent_195` | 1 | 10945 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_195/output.md` |
| `agent_196` | 1 | 8890 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_196/output.md` |
| `agent_197` | 1 | 7802 | `research_runs/2026-06-19_humanize_branch_1to1/agents/agent_197/output.md` |

## Verification

```json
{
  "branch": "use-realpath4everything",
  "research_items": 197,
  "required_worker_jobs": 197,
  "status_files": 197,
  "complete_status_files": 197,
  "output_files": 197,
  "problems": 0
}
```
