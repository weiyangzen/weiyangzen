**Topic and conclusion**

Topic: `Humanize` 的测试套件如何作为 RLCR 核心算法的可执行规格，重点覆盖总测试调度、Finalize 阶段、Stop Hook 后台任务短路、状态转移健壮性。

Conclusion: 这组测试把 RLCR 抽象成一个“文件状态机 + hook 门禁”的算法。核心状态由 `.humanize/rlcr/<timestamp>/` 下的状态文件驱动：`state.md` 表示活动轮次，`finalize-state.md` 表示 Finalize 阶段，`complete-state.md` / `maxiter-state.md` / `stop-state.md` / `cancel-state.md` 表示终止态。Stop hook 是主路由器：先处理无活动 loop、后台任务、跨 session parking，再进入轮次总结、todo、git clean、Codex review、Finalize/complete/maxiter/drift 等门禁。测试明确要求后台任务短路不能修改状态，Finalize 阶段不能调用 Codex，普通轮次必须经 Codex review，并且 drift 状态机有二次 replan、三次 circuit breaker 的行为。

Pinned source commit 已通过只读读取 `.git/refs/heads/main` 确认为 `0ec921a36b4365df503511c5567bbd3e02db0df5`。

**Algorithm subset covered**

覆盖的可执行规格子集：

- 总测试调度器：`tests/run-all-tests.sh`
  - 并行运行所有测试套件，默认并发为 CPU 数但上限 8，可用 `HUMANIZE_TEST_JOBS` 覆盖。
  - 四个关注脚本被纳入总测试数组：`test-stop-hook-bg-allow.sh`、`test-finalize-phase.sh`、`robustness/test-state-transition-robustness.sh`。
  - 每个 suite 独立输出、记录 exit code、提取 Passed/Failed 汇总，任一 suite 失败则总退出 1。

- Finalize Phase：`tests/test-finalize-phase.sh`
  - `state.md -> finalize-state.md -> complete-state.md` 的阶段迁移。
  - Finalize 阶段跳过 Codex review，但仍要求 `finalize-summary.md`、git clean、todos complete。
  - 写/改/读/Bash validators 对 `finalize-state.md`、round contract、`finalize-summary.md` 的特殊规则。
  - 普通 round 不受 Finalize 规则污染。
  - Codex review failure/empty output 不允许进入 Finalize。
  - mainline drift 状态机：`ADVANCED/STALLED/REGRESSED` verdict 更新 stall count 和 drift status。

- Stop Hook 后台任务 short-circuit：`tests/test-stop-hook-bg-allow.sh`
  - transcript 中存在未完成 background Agent/Bash 时，hook `exit 0` 并返回 `systemMessage`，不运行 Codex、不修改 state。
  - 支持 legacy `queue-operation` XML completion 和当前 `system/task_notification` completion。
  - 支持 `~/...` transcript path 展开。
  - 支持 loop start timestamp 过滤，排除 loop 启动前的 background launch。
  - 用 `bg-pending.marker` 做 parking/recovery 信号，跨 session 默认隔离，stop hook 可 opt-in 处理 parked loop。
  - lsof liveness probe 可剪枝 orphaned task。

- State transition robustness：`tests/robustness/test-state-transition-robustness.sh`
  - strict parser 的必需字段、数值字段行为。
  - active loop discovery 的目录选择、finalize/cancel/terminal state 可见性。
  - nested/wrong-location state 不被发现。

**Pseudocode or transition table**

```text
run_all_tests():
  MAX_JOBS = HUMANIZE_TEST_JOBS or min(max(cpu_count, 1), 8)
  if MAX_JOBS invalid: exit 1

  for suite in TEST_SUITES:
    if missing: SKIP
    else run suite in background, using zsh only for ZSH_TESTS
    throttle until active_jobs < MAX_JOBS

  for suite:
    wait PID
    read suite exit/status/output
    strip ANSI
    extract Passed/Failed counters
    if exit != 0 or failed > 0:
      mark failed and preserve detail log
    else:
      mark passed

  if any failed: exit 1
  else: exit 0
```

```text
find_active_loop(base_dir, caller_session_id = "", allow_marker_adoption = false):
  scan direct children of base_dir in reverse lexicographic order
  active state candidates are state.md and finalize-state.md
  terminal-only dirs such as complete-state.md/cancel-state.md are not active

  if caller_session_id matches state session_id:
    return exact-match loop even if older than a foreign marked loop

  if no exact match:
    return newest compatible active loop
    if session mismatch:
      return only when allow_marker_adoption == true and bg-pending.marker exists
      otherwise return empty

  ignore nested state files under subdirectories
```

```text
stop_hook(input):
  session_id = input.session_id or ""
  transcript_path = input.transcript_path or ""

  loop = find_active_loop(.humanize/rlcr, session_id, allow_marker_adoption=true)
  if loop is empty:
    exit 0 with no systemMessage and no Codex

  if loop has bg-pending.marker:
    if session_id is empty:
      exit 0 silently, preserve marker/state
    if stored session_id != session_id:
      exit 0 with "parked" systemMessage, preserve marker/state

  since_ts = derive_loop_start_iso_ts(loop basename)
  pending = list_pending_background_task_ids(transcript_path, since_ts)
  pending -= completed task ids from legacy queue-operation XML
  pending -= completed task ids from system task_notification
  pending = liveness_filter(pending)

  if pending count > 0:
    write bg-pending.marker
    exit 0 with systemMessage mentioning count
    do not mutate state
    do not run Codex

  if previous marker exists and transcript is readable/parseable and same session:
    remove stale bg-pending.marker
  if transcript missing/unreadable/malformed:
    preserve marker and stored session_id

  continue normal RLCR gates
```

```text
normal_round_stop_hook(state.md):
  require round-N-summary.md
  require todos complete
  require git clean where relevant
  run Codex review

  if Codex review fails or stdout is empty:
    block exit
    preserve state.md
    set/retain review_started: true
    do not create finalize-state.md or complete-state.md

  require "Mainline Progress Verdict: ADVANCED|STALLED|REGRESSED"
  if missing:
    block exit
    preserve current_round and drift state

  update drift fields:
    ADVANCED  -> reset or keep normal progress
    STALLED/REGRESSED -> increment mainline_stall_count
    if stall_count == 2:
      current_round += 1
      drift_status = replan_required
      create next round prompt with Drift Recovery Mode
      block exit
    if stall_count >= 3:
      rename state.md -> stop-state.md
      preserve final drift fields
      stop loop

  if Codex output contains COMPLETE:
    if current_round >= max_iterations:
      rename state.md -> maxiter-state.md
      do not enter Finalize
    else:
      run/require successful review path
      rename state.md -> finalize-state.md
      block with Finalize prompt
  else:
    current_round += 1
    keep state.md
    create review result / next prompt
    block with feedback
```

```text
finalize_stop_hook(finalize-state.md):
  do not invoke Codex

  if finalize-summary.md missing:
    block with summary error
  else if git dirty:
    block with git/clean error
  else if todos incomplete:
    block with todo/task error
  else:
    rename finalize-state.md -> complete-state.md
    exit 0 with no block decision
```

| State file | Meaning | Active? | Main transitions |
|---|---:|---:|---|
| `state.md` | Normal RLCR round | Yes | non-COMPLETE feedback keeps `state.md` and increments round; COMPLETE enters `finalize-state.md`; max iteration enters `maxiter-state.md`; drift breaker enters `stop-state.md` |
| `finalize-state.md` | Finalize Phase | Yes | all finalize gates pass -> `complete-state.md`; missing summary/git dirty/todos incomplete -> block and remain |
| `complete-state.md` | Completed terminal state | No | no active loop discovery |
| `maxiter-state.md` | Max-iteration terminal state | No | created instead of Finalize when `current_round == max_iterations` |
| `stop-state.md` | Drift/circuit-break terminal state | No | created after third stalled/regressed round |
| `cancel-state.md` | Cancelled terminal state | No | ignored by active loop discovery |

**Source evidence**

- 总调度器：
  - `run-all-tests.sh` 说明每个 suite 独立 temp dir，因此并行安全：`tests/run-all-tests.sh:7-8`。
  - 默认并发由 `default_jobs` 计算，CPU 数无效回退 4，上限 8，下限 1：`tests/run-all-tests.sh:21-30`。
  - `HUMANIZE_TEST_JOBS` 覆盖并校验必须为 `>=1` 整数：`tests/run-all-tests.sh:33-37`。
  - 关注的三个 suite 被列入总数组：`test-stop-hook-bg-allow.sh` 在 `tests/run-all-tests.sh:71`，`test-finalize-phase.sh` 在 `tests/run-all-tests.sh:75`，`robustness/test-state-transition-robustness.sh` 在 `tests/run-all-tests.sh:118`。
  - 后台启动 suite 并写出 output/exit/time 文件：`tests/run-all-tests.sh:184-196`。
  - 通过 `wait -n` 或 oldest PID fallback 节流：`tests/run-all-tests.sh:201-217`。
  - 汇总时用 suite exit code 和 Failed 计数共同判失败：`tests/run-all-tests.sh:241-255`。
  - 有失败 suite 则打印 detail 并 `exit 1`，否则 `exit 0`：`tests/run-all-tests.sh:286-303`。

- 状态字段和 fixture 规格：
  - Finalize 测试的 `state.md` fixture 包含 `current_round`、`max_iterations`、`codex_model`、`codex_timeout`、`plan_file`、`start_branch`、`base_branch`、`review_started`、`mainline_stall_count`、`last_mainline_verdict`、`drift_status`、`started_at` 等字段：`tests/test-finalize-phase.sh:218-235`。
  - Robustness 测试的普通 state 必备字段包括 `current_round`、`max_iterations`、`plan_file`、`start_branch`、`base_branch`、Codex 配置、`review_started`：`tests/robustness/test-state-transition-robustness.sh:30-51`。
  - Finalize state fixture 使用 `finalize-state.md`，并设置 `finalize_mode: true`、`review_started: true`：`tests/robustness/test-state-transition-robustness.sh:54-71`。
  - Cancel state fixture 使用 `cancel-state.md` 和 `cancelled: true`：`tests/robustness/test-state-transition-robustness.sh:74-88`。

- Active loop discovery：
  - `finalize-state.md` 被检测为 active loop：`tests/test-finalize-phase.sh:331-339`。
  - `complete-state.md` 不被检测为 active loop：`tests/test-finalize-phase.sh:346-360`。
  - 普通 `state.md` 仍被检测为 active loop：`tests/test-finalize-phase.sh:367-375`。
  - Robustness 版同样要求 Finalize active、Cancel inactive：`tests/robustness/test-state-transition-robustness.sh:148-158`、`tests/robustness/test-state-transition-robustness.sh:182-191`。
  - cancel 后较新的普通 state 可被发现：`tests/robustness/test-state-transition-robustness.sh:194-206`。
  - 多目录选择按最新/逆字典序，且测试明确说明是 lexicographic sorting 而不是 timestamp validation：`tests/robustness/test-state-transition-robustness.sh:371-382`、`tests/robustness/test-state-transition-robustness.sh:385-401`。
  - nested wrong-location state 被忽略：`tests/robustness/test-state-transition-robustness.sh:404-416`。

- State validation：
  - round 0 strict parse 成功：`tests/robustness/test-state-transition-robustness.sh:98-112`。
  - round 5、round == max_iterations 均可读取为有效值：`tests/robustness/test-state-transition-robustness.sh:114-138`。
  - negative round 被 `get_current_round` 解析，测试注释指出 regex 接受但可能表示错误：`tests/robustness/test-state-transition-robustness.sh:217-235`。
  - over-max round 被解析，测试说明 enforcement elsewhere：`tests/robustness/test-state-transition-robustness.sh:238-256`。
  - non-numeric round 被 strict parser 拒绝：`tests/robustness/test-state-transition-robustness.sh:259-281`。
  - 缺 `current_round`、`max_iterations`、`base_branch` 均被 strict parser 拒绝：`tests/robustness/test-state-transition-robustness.sh:292-313`、`tests/robustness/test-state-transition-robustness.sh:315-337`、`tests/robustness/test-state-transition-robustness.sh:339-360`。

- Finalize validators：
  - `is_finalize_state_file_path` 只匹配 `finalize-state.md`，不匹配 `state.md`，支持 full path：`tests/test-finalize-phase.sh:279-299`。
  - `is_finalize_summary_path` 匹配 `finalize-summary.md`，不匹配 `round-0-summary.md`：`tests/test-finalize-phase.sh:301-314`。
  - Write validator 允许 `finalize-summary.md`，阻止 `finalize-state.md` 和 Finalize 阶段 round contract：`tests/test-finalize-phase.sh:386-419`。
  - Edit validator 阻止 `finalize-state.md` 和 Finalize 阶段 round contract：`tests/test-finalize-phase.sh:422-443`。
  - Bash validator 阻止修改、`mv FROM`、`cp FROM finalize-state.md`：`tests/test-finalize-phase.sh:446-479`。
  - Read validator 在 Finalize 阶段允许 current round summary，但阻止 round contract：`tests/test-finalize-phase.sh:1064-1087`。
  - Bash/Plan-file validators 必须能 parse `finalize-state.md`：`tests/test-finalize-phase.sh:1051-1061`、`tests/test-finalize-phase.sh:1090-1101`。

- Finalize stop hook：
  - Finalize 缺 `finalize-summary.md` 时 block，且不调用 Codex：`tests/test-finalize-phase.sh:494-517`。
  - Finalize 有 summary 但 git dirty 时 block：`tests/test-finalize-phase.sh:520-535`。
  - Finalize 所有检查通过时 `finalize-state.md` 被 rename 为 `complete-state.md`，exit 0 且无 block：`tests/test-finalize-phase.sh:541-560`。
  - Finalize completion 仍不调用 Codex：`tests/test-finalize-phase.sh:563-568`。
  - Finalize 阶段 todos incomplete 时 block，且不调用 Codex：`tests/test-finalize-phase.sh:770-811`。

- COMPLETE / maxiter / review gate：
  - Codex 输出包含 `COMPLETE` 且未达 max iteration 时，`state.md -> finalize-state.md`，并 block 返回 Finalize/simplification prompt：`tests/test-finalize-phase.sh:575-607`。
  - 达到 `current_round == max_iterations` 时跳过 Finalize，创建 `maxiter-state.md`，删除活动 state：`tests/test-finalize-phase.sh:609-626`。
  - Codex review non-zero failure 时 block，不创建 `finalize-state.md`/`complete-state.md`，保留 `state.md` 且 `review_started: true`：`tests/test-finalize-phase.sh:633-688`。
  - Codex review empty stdout 时 block，不进入 Finalize，并要求 review log 存在且为空，保留 `state.md review_started: true`：`tests/test-finalize-phase.sh:690-767`。
  - 普通 round 的非 COMPLETE review block，保持 `state.md`，不创建 finalize/complete，且 `current_round` 增到 4，并生成 `round-3-review-result.md`：`tests/test-finalize-phase.sh:818-877`。
  - block 输出必须包含 Codex review feedback：`tests/test-finalize-phase.sh:880-887`。

- Mainline drift 状态机：
  - 两次 stalled 触发 drift recovery prompt，创建 `round-4-prompt.md`：`tests/test-finalize-phase.sh:893-932`。
  - recovery prompt 必须包含 `Drift Recovery Mode`：`tests/test-finalize-phase.sh:934-938`。
  - 二次 stalled 后状态为 `current_round=4`、`mainline_stall_count=2`、`last_mainline_verdict=stalled`、`drift_status=replan_required`：`tests/test-finalize-phase.sh:940-946`。
  - 缺 `Mainline Progress Verdict` 时 block，不生成下一轮 prompt，保留原 drift 状态：`tests/test-finalize-phase.sh:948-994`。
  - 第三次 stalled/regressed 触发 circuit breaker，生成 `stop-state.md` 并带 drift message：`tests/test-finalize-phase.sh:996-1030`。
  - stop-state 保留最终 drift 字段 `stall=3`、`verdict=regressed`、`drift=replan_required`：`tests/test-finalize-phase.sh:1033-1039`。

- Background short-circuit：
  - 文件头定义核心规则：pending background Agent/Bash 时必须 `exit 0 + systemMessage`，不运行 gate 或 Codex review，磁盘 state 不变：`tests/test-stop-hook-bg-allow.sh:3-10`。
  - AC 列表覆盖 no bg、pending subagent/shell、completion、multi pending、missing transcript、no active loop、Finalize pending bg、wrapper、tilde、cross-session marker、completion formats、malformed transcript 等：`tests/test-stop-hook-bg-allow.sh:12-34`。
  - fixture 中普通 loop state 包含 `session_id` 可选字段相关的上下文，并在 Finalize fixture 下改用 `finalize-state.md` 和 `finalize-summary.md`：`tests/test-stop-hook-bg-allow.sh:101-159`。
  - transcript builder 将 `run_in_background:true` tool use、async Agent result、background shell result、legacy task completion、SDK task notification 编码成 JSONL：`tests/test-stop-hook-bg-allow.sh:190-253`。
  - assertion 明确 short-circuit 必须 exit 0、无 Codex marker、有 `systemMessage`、state hash 不变：`tests/test-stop-hook-bg-allow.sh:291-328`。
  - no bg dispatch 走正常 Codex flow：`tests/test-stop-hook-bg-allow.sh:354-363`。
  - pending subagent/shell 分别触发 `1 background task` systemMessage：`tests/test-stop-hook-bg-allow.sh:365-395`。
  - 已完成 subagent 继续 Codex flow：`tests/test-stop-hook-bg-allow.sh:397-409`。
  - 2 subagents + 1 shell 要显示 `3 background task(s)`：`tests/test-stop-hook-bg-allow.sh:411-432`。
  - missing/empty/no transcript_path 在无 marker 场景走 Codex，即 fail-closed 不误 short-circuit：`tests/test-stop-hook-bg-allow.sh:434-454`。
  - no active loop 时 exit 0，无 systemMessage，无 Codex：`tests/test-stop-hook-bg-allow.sh:456-473`。
  - Finalize phase + pending bg 也 short-circuit，且 `finalize-state.md` 不变：`tests/test-stop-hook-bg-allow.sh:476-489`。
  - wrapper `rlcr-stop-gate.sh` 必须把 pending bg 映射成 `ALLOW:`：`tests/test-stop-hook-bg-allow.sh:491-518`。
  - `~/...` transcript path 必须展开，hook、helper、wrapper 都覆盖：`tests/test-stop-hook-bg-allow.sh:520-604`。

- Session parking / marker invariants：
  - cross-session 且有 `bg-pending.marker` 时返回 `parked` systemMessage，marker 和 state hash 不变，无 Codex：`tests/test-stop-hook-bg-allow.sh:606-667`。
  - cross-session 但无 marker 时保持隔离，不 adoption、不 systemMessage、不 Codex：`tests/test-stop-hook-bg-allow.sh:670-716`。
  - short-circuit 实际写入 `bg-pending.marker`：`tests/test-stop-hook-bg-allow.sh:718-739`。
  - `find_active_loop` 优先 exact session match，即使较新的 foreign loop 有 marker，也返回较旧 exact match；扫描不删除 foreign marker：`tests/test-stop-hook-bg-allow.sh:742-790`。
  - same-session resume 且无 pending bg 时移除 stale marker，session_id 不变：`tests/test-stop-hook-bg-allow.sh:793-843`。
  - cross-session stop 不得删除 marker 或改写 stored `session_id`：`tests/test-stop-hook-bg-allow.sh:845-899`。
  - default `find_active_loop` 不通过 marker 暴露 foreign parked loop；第三参数 opt-in 才返回 marker dir：`tests/test-stop-hook-bg-allow.sh:1052-1094`。
  - empty session caller + marker 是 ambiguous，必须 silent exit 0、preserve marker/state、无 Codex：`tests/test-stop-hook-bg-allow.sh:1096-1152`。
  - missing/nonexistent transcript with marker 必须 preserve marker 和 stored session_id：`tests/test-stop-hook-bg-allow.sh:955-1049`。
  - malformed transcript with marker 必须 preserve marker：`tests/test-stop-hook-bg-allow.sh:1155-1203`。

- Background completion / time boundary / liveness：
  - 当前 `system/task_notification` completion 能清空 pending：`tests/test-stop-hook-bg-allow.sh:901-924`。
  - legacy XML completion 与 SDK notification 的 union 能清空 pending：`tests/test-stop-hook-bg-allow.sh:926-953`。
  - transcript scan 必须用 loop start `since_ts` 过滤，pre-loop launch 不算 pending：`tests/test-stop-hook-bg-allow.sh:1205-1239`。
  - `derive_loop_start_iso_ts` 在 UTC/JST/PST 下做本地 wall-clock 到 UTC 的转换：`tests/test-stop-hook-bg-allow.sh:1242-1287`。
  - end-to-end pre-loop launch 不写 marker，Codex 运行：`tests/test-stop-hook-bg-allow.sh:1289-1309`。
  - wrapper 无 session_id 且无 prior marker 时 pending bg 仍写 marker 并输出 `ALLOW` + systemMessage：`tests/test-stop-hook-bg-allow.sh:1312-1350`。
  - wrapper 无 session_id 且已有 marker 时 silent `ALLOW`，不输出 parked，不改 state：`tests/test-stop-hook-bg-allow.sh:1353-1407`。
  - lsof alive 时 pending task 仍 short-circuit；lsof dead/orphaned 时剪枝并运行 Codex：`tests/test-stop-hook-bg-allow.sh:1410-1459`。

**Edge cases and risks**

- Negative `current_round` 被解析而不是 strict 拒绝；测试注释明确说这可能表示错误，说明范围校验不在 `get_current_round` 层完成：`tests/robustness/test-state-transition-robustness.sh:217-235`。
- `current_round > max_iterations` 也能被解析，测试明确写着 enforcement is elsewhere；如果调用方忘记执行 maxiter gate，会有越界轮次风险：`tests/robustness/test-state-transition-robustness.sh:238-256`。
- loop dir 选择使用 lexicographic ordering 而不是 timestamp validation；格式异常但字典序更大的目录可能被选中，这是测试承认的行为边界：`tests/robustness/test-state-transition-robustness.sh:385-401`。
- `finalize-state.md` 与 `state.md` 可共存，测试只断言 finalize 文件存在，并用注释说明 finalize-state should be preferred；共存状态本身没有在 robustness 测试中强制清理：`tests/robustness/test-state-transition-robustness.sh:160-171`。
- transcript missing/no key 在无 marker 时走 Codex flow，但在已有 marker 时必须 preserve marker；这是 fail-closed 的双重语义，调用方不能把“无 pending 输出”直接解释为“后台任务完成”：`tests/test-stop-hook-bg-allow.sh:434-454`、`tests/test-stop-hook-bg-allow.sh:955-1049`。
- malformed transcript 不能触发 marker cleanup，否则会丢失 parked loop recovery 信号：`tests/test-stop-hook-bg-allow.sh:1155-1203`。
- empty session_id + existing marker 被视为 ambiguous，只能 silent allow；这保护跨 session，但也意味着 wrapper 若不传 session_id，不能推进已有 parked loop：`tests/test-stop-hook-bg-allow.sh:1096-1152`、`tests/test-stop-hook-bg-allow.sh:1353-1407`。
- pre-loop launch 过滤依赖 loop dir basename 转 UTC；时区转换错误会导致旧后台任务误阻塞或新后台任务被忽略：`tests/test-stop-hook-bg-allow.sh:1205-1287`。
- liveness probe 依赖 `/tmp/claude-<uid>/.../*.output` 和 `lsof` 语义；dead/orphaned task 会被剪枝进入 Codex，alive task 会继续 short-circuit：`tests/test-stop-hook-bg-allow.sh:1410-1459`。
- Codex review failure 或 empty stdout 必须 preserve `state.md` with `review_started: true`；否则可能跳过 review 直接 Finalize：`tests/test-finalize-phase.sh:633-688`、`tests/test-finalize-phase.sh:690-767`。
- 缺 `Mainline Progress Verdict` 会 block 并 preserve drift state；这避免无 verdict 时错误推进 drift 状态机，但也使 verdict 格式成为强 gate：`tests/test-finalize-phase.sh:948-994`。

**What is explicitly out of scope**

- 未分析安装流程、营销文案、截图、README 泛用说明。
- 未运行测试套件；本次只读解析脚本作为可执行规格。
- 未修改文件、未提交 commit、未进行网络搜索。
- 未覆盖 `run-all-tests.sh` 中列出的其他 suites 的算法细节，只确认它们如何被总调度器调度。
- 未把 hook 实现源码作为主要对象展开审计；仅在测试通过 `source`/调用 hook 的语境下解释被测算法行为。
- 未评价 Codex 实际模型质量、review 内容质量或 prompt 文案完整性，只提取测试中可断言的状态、门禁和迁移行为。