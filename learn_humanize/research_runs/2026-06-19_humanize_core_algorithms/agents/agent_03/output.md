**Topic and Conclusion**

Topic: Stop-hook state machine, pinned source commit `0ec921a36b4365df503511c5567bbd3e02db0df5`.

结论：该 Stop hook 是一个 fail-closed 的多阶段 RLCR 状态机。无活动 loop 或无状态文件时放行；一旦发现匹配 session 的活动 loop，就必须依次通过 schema、分支、计划文件、todo、git clean、summary、round contract、BitLesson、goal tracker 等本地 gate。实现阶段用 `codex exec` 审查 summary；`COMPLETE` 不直接结束，而是进入 Review Phase；Review Phase 用 `codex review`，只有无 `[P0-9]` 问题才进入 Finalize Phase；Finalize Phase 通过最终 summary 和 clean-tree gate 后才将状态归档为 complete 或进入 methodology analysis。hook 内部阻断以 JSON `decision:"block"` 输出并 `exit 0`；包装器把它映射成 CLI `exit 10`。

**Algorithm Subset Covered**

覆盖文件：

- `hooks/loop-codex-stop-hook.sh`: Stop hook 主状态机、phase 判定、gate、Codex 路由、状态转移。
- `scripts/rlcr-stop-gate.sh`: 非 hook 环境复用同一状态机的包装器，负责构造 Stop hook 输入并映射退出码。
- `tests/test-stop-gate.sh`: wrapper/root resolution、tracked state、无活动 loop、空 session/transcript 转发等回归行为。

核心状态变量：

- loop 定位：`PROJECT_ROOT`、`LOOP_BASE_DIR`、`LOOP_DIR`、`HOOK_SESSION_ID`。
- phase：`STATE_FILE`，派生 `IS_FINALIZE_PHASE`、`IS_METHODOLOGY_ANALYSIS_PHASE`、`REVIEW_STARTED`。
- 轮次：`CURRENT_ROUND`、`MAX_ITERATIONS`、`NEXT_ROUND`、`FULL_REVIEW_ROUND`。
- repo/计划约束：`PLAN_TRACKED`、`START_BRANCH`、`BASE_BRANCH`、`BASE_COMMIT`、`PLAN_FILE`、`PUSH_EVERY_ROUND`。
- 审查/漂移：`LAST_MAINLINE_VERDICT`、`MAINLINE_STALL_COUNT`、`DRIFT_STATUS`、`DRIFT_REPLAN_REQUIRED`、`MAINLINE_DRIFT_STOP`。
- 文件工件：`round-N-summary.md`、`round-N-contract.md`、`round-N-review-prompt.md`、`round-N-review-result.md`、`finalize-summary.md`、`.review-phase-started`。
- 外部输入：hook stdin JSON、session id、transcript path、git 状态、Codex CLI 输出、summary/contract/goal tracker/BitLesson 文件。

**Transition Table**

| 当前状态 | 输入 / gate 结果 | 动作 | 输出 |
|---|---|---|---|
| No Active Loop | 无 project root、无 `LOOP_DIR`、无 active state | 不进入 RLCR | allow |
| Implementation | schema/branch/plan/todo/git/summary/contract 等任一 gate 失败 | 生成 block reason | block |
| Implementation | `codex exec` 失败、无结果文件、空结果 | 要求重试 | block |
| Implementation | review 最后一条非空行为 `COMPLETE` 且未达 max | `review_started=true`，写 `.review-phase-started`，立即跑 `codex review` | 进入 Review Phase 分支 |
| Implementation | `COMPLETE` 但 `CURRENT_ROUND >= MAX_ITERATIONS` | methodology analysis 或 `end_loop MAXITER` | allow |
| Implementation | 最后一条非空行为 `STOP` | methodology analysis 或 `end_loop STOP` | allow |
| Implementation | 无 `COMPLETE/STOP` | 更新 `current_round` 和 drift 状态，写下一轮 prompt/summary | block |
| Review Phase | `.review-phase-started` 缺失 | 视为手工篡改/状态不一致 | block |
| Review Phase | `codex review` 失败或无 stdout | 硬错误，不能跳过 review | block |
| Review Phase | 检测到 `[P0-9]` issues | current round 前进，写 review-fix prompt | block |
| Review Phase | 无 `[P0-9]` issues | `state.md -> finalize-state.md`，发 finalize prompt | block |
| Finalize Phase | `finalize-summary.md` 缺失或 git 不 clean | 要求补齐/提交 | block |
| Finalize Phase | 所有 gate 通过 | methodology analysis 或 `finalize-state.md -> complete-state.md` | allow |
| Methodology Phase | analysis 未完成 | 要求完成 analysis | block |
| Methodology Phase | analysis 完成且 tree clean | 终态可退出 | allow |

简化伪代码：

```text
read hook_input
root = resolve_project_root() or allow
loop = find_active_loop(root/.humanize/rlcr, session_id) or allow
handle_bg_task_short_circuit(loop, hook_input, session_id)

state = resolve_active_state_file(loop) or allow
phase = filename(state)
parse frontmatter into state variables
validate schema, branch, plan, todo, git, summary, contract, bitlesson, goal tracker

if methodology_phase:
    allow only when complete_methodology_analysis() and git-clean pass

if finalize_phase:
    require finalize-summary and all gates; then complete-state or methodology

if review_started:
    require .review-phase-started
    run codex review
    if review failure or [P0-9] issues: block with review-fix prompt
    else rename state to finalize-state and block with finalize prompt

run codex exec summary review
if failure/missing/empty: block
marker = last_non_empty_line(review_result)
verdict = Mainline Progress Verdict unless marker == STOP
update drift counters:
    ADVANCED => stall=0
    STALLED/REGRESSED => stall += 1
    stall >= 2 => replan prompt
    stall >= 3 => drift circuit breaker
if marker == COMPLETE: enter review phase
if marker == STOP or drift breaker: stop loop
else current_round += 1 and block with next-round prompt
```

**Source Evidence**

- Stop hook 从 stdin 读取 hook JSON，并明确“不检查 `stop_hook_active`”，因为被阻断后继续停止时仍要运行审查；终止由无 active loop、`MARKER_COMPLETE`、max iterations 控制：`hooks/loop-codex-stop-hook.sh:28-36`。
- project root 解析失败直接 `exit 0`；按 session-aware active loop 查找，找不到或 session 不匹配则放行：`hooks/loop-codex-stop-hook.sh:46-69`。
- 背景任务 guard 顺序固定：无 session 且 marker、跨 session parked loop、pending background、同 session stale marker cleanup；guard 命中时直接输出 JSON 并退出：`hooks/loop-codex-stop-hook.sh:71-83`。
- phase 由 active state 文件名判定：`finalize-state.md` 表示 Finalize Phase，`methodology-analysis-state.md` 表示 Methodology Phase：`hooks/loop-codex-stop-hook.sh:91-101`。
- 状态 frontmatter 被解析成计划、分支、轮次、review、Codex、BitLesson、drift 等变量；`current_round`、`max_iterations` 等关键字段先检查 raw frontmatter，避免默认值掩盖截断状态：`hooks/loop-codex-stop-hook.sh:107-171`、`hooks/loop-codex-stop-hook.sh:186-218`。
- Codex model/effort 被正则校验，非法时 `end_loop EXIT_UNEXPECTED` 后退出：`hooks/loop-codex-stop-hook.sh:172-184`。
- schema gate 缺 `plan_tracked/start_branch`、无效 `review_started`、缺 `base_branch` 均 block：`hooks/loop-codex-stop-hook.sh:225-270`。
- 分支 gate 要求当前分支等于 `START_BRANCH`，git 检查失败也 fail-closed block：`hooks/loop-codex-stop-hook.sh:289-316`。
- Review Phase 会跳过 plan integrity；实现阶段要求 plan backup、原始 plan 存在、tracked plan 无未提交修改、backup diff 通过：`hooks/loop-codex-stop-hook.sh:321-399`。
- todo checker parse error 或未完成任务会在 Codex 审查前 block：`hooks/loop-codex-stop-hook.sh:408-456`。
- git status 被缓存，失败/超时 fail-closed；tracked Humanize state 直接 block；dirty tree block，但 untracked `.humanize/` 与 `.humanize-*` 被排除；`push_every_round=true` 时检查 ahead commits：`hooks/loop-codex-stop-hook.sh:492-516`、`hooks/loop-codex-stop-hook.sh:667-780`。
- Methodology Phase 在主 git-clean gate 前处理；analysis 完成后仍重新检查非 `.humanize/` dirty tree：`hooks/loop-codex-stop-hook.sh:617-663`。
- summary gate 根据 phase 选择 `finalize-summary.md` 或 `round-N-summary.md`；缺失即 block：`hooks/loop-codex-stop-hook.sh:788-821`。
- anti-drift 状态存在时要求 `round-N-contract.md`；BitLesson required 时调用 delta validator；Round 0 goal tracker 仍含 placeholder 时 block：`hooks/loop-codex-stop-hook.sh:827-855`、`hooks/loop-codex-stop-hook.sh:861-875`、`hooks/loop-codex-stop-hook.sh:882-954`。
- max iteration gate 在非 Finalize、非 Review Phase 下按 `NEXT_ROUND > MAX_ITERATIONS` 触发 methodology 或 `EXIT_MAXITER`：`hooks/loop-codex-stop-hook.sh:960-973`。
- Finalize Phase 通过所有 gate 后尝试 methodology analysis，否则 `finalize-state.md -> complete-state.md` 并 allow：`hooks/loop-codex-stop-hook.sh:981-990`。
- Full Alignment Check 路由规则是 `CURRENT_ROUND % FULL_REVIEW_ROUND == FULL_REVIEW_ROUND - 1`，默认/非法值回退到 5：`hooks/loop-codex-stop-hook.sh:1015-1025`。
- 缺 Codex CLI 会 block；嵌套 Codex 调用会探测并使用 `--disable codex_hooks` 防止 hook 递归：`hooks/loop-codex-stop-hook.sh:1133-1153`、`hooks/loop-codex-stop-hook.sh:1169-1181`。
- Review Phase 的 `codex review` 路由：命令失败 block；`detect_review_issues` 返回 `0=有问题`、`1=无问题`、`2=stdout 缺失硬错误`；无问题进入 finalize：`hooks/loop-codex-stop-hook.sh:1288-1317`。
- `enter_finalize_phase` 将 state 改名为 `finalize-state.md`，但仍输出 `decision:"block"`，要求 Claude 做 finalize summary/commit 后再次 stop：`hooks/loop-codex-stop-hook.sh:1321-1402`。
- Mainline drift 规则：实现期 review 必须给 `Mainline Progress Verdict`，除非 `STOP`；`ADVANCED` 清零，`STALLED/REGRESSED` 累加，`>=2` 触发 replan，`>=3` 触发 drift circuit breaker：`hooks/loop-codex-stop-hook.sh:1817-1862`、`hooks/loop-codex-stop-hook.sh:1421-1457`。
- marker 只看最后一条非空行且必须严格等于 `COMPLETE` 或 `STOP`，避免误判 `CANNOT COMPLETE`：`hooks/loop-codex-stop-hook.sh:1808-1815`。
- `COMPLETE` 在实现期进入 Review Phase，写 `review_started=true`、重置 drift、创建 `.review-phase-started`，然后立即跑 initial code review；在 Review Phase 中 `COMPLETE` 被忽略，是否 finalize 只看 review issue 检测：`hooks/loop-codex-stop-hook.sh:1864-1910`。
- Review Phase 每次 stop 都重新跑 code review，且要求 `.review-phase-started` marker，防止手动把 state 改成 `review_started=true`：`hooks/loop-codex-stop-hook.sh:1916-1945`。
- 非完成、非停止的实现期结果会更新 `current_round`、drift 字段，创建下一轮 prompt/summary，并以 block 形式把下一轮指令返回：`hooks/loop-codex-stop-hook.sh:1990-2221`。
- wrapper 定义退出码：`0=allow`、`10=block`、`20=wrapper/runtime error`：`scripts/rlcr-stop-gate.sh:8-14`。
- wrapper 构造标准 Stop hook JSON；空 `session_id/transcript_path` 显式变成 `null`，避免 jq `select` 导致整个对象坍缩：`scripts/rlcr-stop-gate.sh:99-123`。
- wrapper 执行 hook 后：hook 非零 -> `20`；空输出 -> allow `0`；JSON `decision:"block"` -> `10`；无 `decision` 字段按 Stop hook spec 放行；未知 decision -> `20`：`scripts/rlcr-stop-gate.sh:125-178`。
- 测试确认默认 project root 使用调用方 cwd 并能 block 活动 loop；`--project-root` 可从仓库外指定目标 repo：`tests/test-stop-gate.sh:64-116`。
- 测试确认 tracked `.humanize/rlcr/.../goal-tracker.md` 会走 dedicated “Tracked Humanize State Blocked”，但 `.humanize-backup`、`.humanizeconfig` 不被误判为 loop state：`tests/test-stop-gate.sh:118-178`。
- 测试确认无 active loop 时 wrapper `exit 0` 且输出 `ALLOW:`；空 session id 时仍转发 transcript path，并到达 block decision 分支而非 wrapper error/错误 allow：`tests/test-stop-gate.sh:180-286`。

**Edge Cases and Risks**

- hook 内部 block 按 Claude hook 约定是 `exit 0 + JSON decision:block`；非 hook 调用者必须使用 wrapper 才能得到机器可区分的 `exit 10`。
- corrupt state 的处理不统一：部分 schema 旧版是 JSON block，部分字段非法会 `end_loop EXIT_UNEXPECTED` 后 allow，这更像“终止 loop”而不是“要求修复后继续”。
- `BASE_BRANCH` 缺失既有早期 schema block，也有后续“skip code review”分支；在当前路径下后者基本不可达，属于遗留兼容逻辑风险。
- git gate 对普通 dirty tree fail-closed，但刻意排除 untracked `.humanize/` / `.humanize-*`；同时 tracked Humanize state 会 dedicated block。边界由 helper `git_has_tracked_humanize_state` 决定，其实现不在本次 focus path 内。
- Review Phase 不看 `COMPLETE` marker，而看 `[P0-9]` issue 检测；如果 review 输出格式变化，可能造成误 block 或误 finalize。
- drift counter 是简单阈值状态机：连续 `STALLED/REGRESSED` 两轮进入 replan，三轮停止；它不衡量实际代码 diff，只信任 Codex verdict。
- `stop_hook_active` 被故意忽略，所以同一 Stop 继续链会反复触发 hook；防递归主要靠 nested Codex 的 `--disable codex_hooks` 探测。
- wrapper 的 no-project-root 行为是 benign allow，不是错误；在错误 cwd 下可能静默绕过 gate，但这是脚本显式设计。

**What Is Explicitly Out Of Scope**

- 未分析安装、营销、截图、通用使用说明。
- 未深入读取 helper 实现：`loop-common.sh`、`project-root.sh`、`loop-bg-tasks.sh`、`methodology-analysis.sh`、`check-todos-from-transcript.py`、`bitlesson-validate-delta.sh`；这里只记录 focus scripts 对它们的调用契约。
- 未分析 prompt template 的完整文案，只保留影响状态机行为的 fallback/调用点。
- 未评价 Codex 审查质量、模型选择、网络/auth 可靠性，只分析 CLI exit/output contract。
- 未运行测试或修改文件；证据来自 pinned commit 的只读 `git show | nl` / `rg`。