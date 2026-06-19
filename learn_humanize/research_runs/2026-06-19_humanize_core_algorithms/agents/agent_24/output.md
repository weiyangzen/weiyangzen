**Topic and Conclusion**

Topic: Monitor runtime status model

结论：`_humanize_monitor_codex` 的运行时状态模型是一个文件系统驱动的轮询状态机。它不维护独立的持久状态，而是把 `.humanize/rlcr/<timestamp>` 会话目录、状态文件命名、缓存日志文件、终端尺寸和信号处理组合成当前监控视图。核心状态由 `current_session_dir`、`current_file`、`current_loop_status`、`monitor_running`、`cleanup_done`、`last_size`、`last_no_log_status` 和 `resize_needed` 组成。状态优先级由文件存在性决定：`methodology-analysis-state.md` > `state.md` > `*-state.md` > `unknown`。删除 `.humanize/rlcr` 是强终止门，会触发 `_graceful_stop`、恢复终端并以退出码 0 结束；删除单个 session 或 log 则优先尝试切换到最新 session。

**Algorithm Subset Covered**

覆盖范围仅限：

- `scripts/humanize.sh`
  - `_humanize_monitor_codex`
  - session/log/state 发现
  - status bar 状态路由
  - graceful stop / cleanup / signal handling
- `scripts/lib/monitor-common.sh`
  - `monitor_find_latest_session`
  - `monitor_find_state_file`
  - terminal restore/setup helper
  - status color helper
- `tests/test-monitor-runtime.sh`
  - graceful stop、cleanup 幂等、目录删除检测、trap/source 断言
- `tests/test-monitor-e2e-real.sh`
  - bash/zsh 下真实 monitor 的目录删除与 SIGINT 行为断言

明确跳过安装、营销、截图和普通使用说明；没有运行测试，没有编辑文件，没有联网。

**Pseudocode**

```text
start _humanize_monitor_codex:
  if zsh: enable ksharrays
  loop_dir = ".humanize/rlcr"
  current_file = ""
  current_session_dir = ""
  status_bar_height = 11

  if loop_dir missing:
    print error
    return 1

  current_session_dir = latest timestamp session under loop_dir
  current_file = latest round log for current_session_dir
  if no current_session_dir:
    print no sessions
    return 1

  current_loop_status = find_state_file(current_session_dir).status

  wait until terminal_height >= status_bar_height + 3
  setup split terminal

  monitor_running = true
  cleanup_done = false
  resize_needed = false
  last_size = 0
  last_no_log_status = ""

  install signal handlers:
    bash INT/TERM -> cleanup
    bash WINCH -> resize_needed=true
    zsh TRAPINT/TRAPTERM -> cleanup + signal return code
    zsh TRAPWINCH -> resize_needed=true

  while monitor_running:
    if loop_dir missing:
      graceful_stop(".humanize/rlcr directory no longer exists")
      return 0

    current_loop_status = find_state_file(current_session_dir).status
    handle resize if needed
    draw_status_bar(current_session_dir, current_file or N/A, current_loop_status)

    if current_file is empty:
      show no-log message based on current_loop_status

      while monitor_running:
        sleep 0.5
        if loop_dir missing:
          graceful_stop(...)
          return 0

        handle resize
        current_loop_status = find_state_file(current_session_dir).status
        draw_status_bar(..., "N/A", current_loop_status)

        latest_session = find_latest_session(loop_dir)

        if current_session_dir deleted:
          if latest_session exists:
            switch current_session_dir to latest_session
            current_file = latest log in latest_session
            reset no-log state
            if current_file exists: break to outer loop
            else continue waiting
          else:
            current_session_dir = ""
            current_file = ""
            display waiting-for-new-sessions
            continue

        if latest_session exists and differs:
          current_session_dir = latest_session
          reset no-log state

        latest_log = find_latest_codex_log(current_session_dir)
        if latest_log exists:
          current_file = latest_log
          last_size = 0
          break

      continue outer loop

    else:
      last_size = file_size(current_file)
      tail recent log content

      while monitor_running:
        sleep 0.5
        if loop_dir missing:
          graceful_stop(...)
          return 0

        handle resize
        current_loop_status = find_state_file(current_session_dir).status
        draw_status_bar(current_session_dir, current_file, current_loop_status)

        file_size = size(current_file)
        if file_size > last_size:
          print bytes from last_size+1
          last_size = file_size
        else if last_size > 0 and file_size < last_size:
          current_file = ""
          last_size = 0
          reset no-log state
          break

        latest_session = find_latest_session(loop_dir)

        if current_session_dir missing or current_file missing:
          if latest_session exists:
            switch to latest_session
            current_file = latest log in latest_session, maybe empty
            last_size = 0
            break
          else:
            current_session_dir = ""
            current_file = ""
            display waiting
            break

        if latest_session exists and differs:
          switch to latest_session
          current_file = latest log or empty
          last_size = 0
          break

        latest_log = find_latest_codex_log(current_session_dir)
        if latest_log exists and latest_log != current_file:
          current_file = latest_log
          last_size = 0
          break

  reset traps
```

**Transition Table**

| 当前条件 | 输入/事件 | Guard | 转移 | 输出/副作用 |
|---|---|---|---|---|
| 初始 | `.humanize/rlcr` 不存在 | `[[ ! -d "$loop_dir" ]]` | 终止 | 打印错误，`return 1` |
| 初始 | 无 timestamp session | `current_session_dir == ""` | 终止 | 打印 “No session directories found”，`return 1` |
| 任意主循环 | `.humanize/rlcr` 被删除 | `[[ ! -d "$loop_dir" ]]` | graceful stop | `_cleanup`，恢复终端，打印原因，`return 0` |
| no-log | 当前 session 被删除，有其他 session | `! -d current_session_dir && latest_session != ""` | switch session | 更新 `current_session_dir/current_file`，清屏提示 |
| no-log | 当前 session 被删除，无其他 session | `! -d current_session_dir && latest_session == ""` | waiting | `current_session_dir=""`，`current_file=""`，显示等待 |
| no-log | 新 log 出现 | `latest_log != ""` | follow-log | `current_file=latest_log`，`last_size=0` |
| follow-log | log 增长 | `file_size > last_size` | stay | 输出新增 bytes，更新 `last_size` |
| follow-log | log 截断/轮转 | `last_size > 0 && file_size < last_size` | no-log/search | `current_file=""`，`last_size=0` |
| follow-log | session/log 被删，有其他 session | `! -d session || ! -f file` 且 `latest_session != ""` | switch session | 更新 session/log，重置 `last_size` |
| follow-log | 更新 session 出现 | `latest_session != current_session_dir` | switch session | 优先切到最新 session，即使还没有 log |
| follow-log | 同 session 新 round log 出现 | `latest_log != current_file` | switch log | `current_file=latest_log`，`last_size=0` |
| 任意 | `SIGINT`/`SIGTERM` | trap | cleanup stop | `monitor_running=false`，恢复终端 |
| 任意 | `SIGWINCH` 或尺寸变化 | resize flag/dimension diff | redraw/reflow | 过小则等待；否则更新 scroll region 并重放 tail |

**State Variables**

- `loop_dir=".humanize/rlcr"`：监控根目录，缺失时启动失败或运行中 graceful stop。证据：`scripts/humanize.sh:266-276`、`scripts/humanize.sh:840-843`、`scripts/humanize.sh:1027-1030`
- `current_session_dir`：当前选中的 session，由最新 timestamp 目录决定。证据：`scripts/humanize.sh:798-806`
- `current_file`：当前跟随的 log 文件；为空时进入 no-log waiting 分支。证据：`scripts/humanize.sh:799-800`、`scripts/humanize.sh:883-900`
- `current_loop_status`：由 state 文件检测得到，用于 status bar 和 no-log 文案。证据：`scripts/humanize.sh:809-813`、`scripts/humanize.sh:846-849`
- `monitor_running`：所有循环的运行门。证据：`scripts/humanize.sh:731-734`、`scripts/humanize.sh:838-839`
- `cleanup_done`：cleanup/graceful stop 幂等门。证据：`scripts/humanize.sh:738-742`、`scripts/humanize.sh:766-772`
- `resize_needed`：SIGWINCH 只置位，主循环安全点处理。证据：`scripts/humanize.sh:779-795`
- `last_size/file_size`：增量读取和截断检测。证据：`scripts/humanize.sh:833-836`、`scripts/humanize.sh:1074-1091`
- `last_no_log_status`：避免重复渲染 no-log 文案，状态变化时刷新。证据：`scripts/humanize.sh:836`、`scripts/humanize.sh:889-897`

**Inputs**

- Session 目录：`.humanize/rlcr/YYYY-MM-DD_HH-MM-SS`，只接受 timestamp regex，按字典序取最大。证据：`scripts/lib/monitor-common.sh:37-63`
- State 文件：
  - `methodology-analysis-state.md`
  - `state.md`
  - `<STOP_REASON>-state.md`
  - 缺失/非法 session -> `unknown`
  证据：`scripts/lib/monitor-common.sh:147-192`
- Log 文件：`${XDG_CACHE_HOME:-$HOME/.cache}/humanize/<sanitized-project>/<session>/round-*-codex-run.log` 或 `round-*-codex-review.log`。证据：`scripts/humanize.sh:284-332`、`scripts/humanize.sh:338-375`
- YAML-ish state keys：`current_round`、`max_iterations`、`full_review_round`、`codex_model`、`codex_effort`、`started_at`、`plan_file`、`ask_codex_question`、`review_started`、`agent_teams`、`push_every_round`、`mainline_stall_count`、`last_mainline_verdict`、`drift_status`。证据：`scripts/humanize.sh:382-405`
- Goal tracker：用于 progress display，不驱动 monitor 状态转移。证据：`scripts/humanize.sh:449-463`
- Git status：只用于 status bar。证据：`scripts/humanize.sh:464-472`
- Terminal size 和 signals：`tput lines/cols`，`INT`、`TERM`、`WINCH`。证据：`scripts/humanize.sh:661-698`、`scripts/humanize.sh:784-796`

**Gates and Routing Rules**

- Session selection gate：只考虑一层子目录，并且 basename 必须匹配 `YYYY-MM-DD_HH-MM-SS`；使用 `find` 而不是 glob，避免 zsh “no matches found”。证据：`scripts/lib/monitor-common.sh:49-60`
- State status priority：
  - `methodology-analysis-state.md` -> `methodology-analysis`
  - `state.md` -> `active`
  - 第一个 `*-state.md` -> basename 去掉 `-state.md`
  - 无 -> `unknown`
  证据：`scripts/lib/monitor-common.sh:162-190`
- Log consistency gate：如果同时存在 run 和 review log，则 `max_run_round < min_review_round`；否则报 inconsistent log state 并返回空。证据：`scripts/humanize.sh:334-371`
- Latest log routing：按 round number 最大选 log；round 从文件名 `round-N-codex-run.log` 或 `round-N-codex-review.log` 提取。证据：`scripts/humanize.sh:311-320`、`scripts/humanize.sh:344-361`
- Terminal size gate：最低高度为 `status_bar_height + 3`，不足时显示过小提示并等待 resize。证据：`scripts/humanize.sh:661-688`、`scripts/humanize.sh:815-823`
- Status display routing：
  - `active` 根据 `review_started` 和 `.review-phase-started` 显示 build/review phase。
  - `complete|completed` -> Complete。
  - `finalize` -> Finalize。
  - `stop|cancel|cancelled|maxiter|unexpected|failed|error|timeout` -> red stop state。
  - 其他 -> orange capitalized unknown/other。
  证据：`scripts/humanize.sh:531-576`
- Progress scoring/routing：
  - `completed_acs < total_acs` 时 AC progress 为 yellow，否则 green。
  - queued issues > 0 -> yellow；blocking issues > 0 -> red。
  证据：`scripts/humanize.sh:607-623`
- Drift routing：
  - `drift_status == replan_required` -> red。
  - `mainline_stall_count > 0` -> yellow。
  - 其他 -> dim。
  证据：`scripts/humanize.sh:595-604`

**Failure Modes**

- 启动时 `.humanize/rlcr` 缺失：非 graceful，打印错误并 `return 1`。证据：`scripts/humanize.sh:272-277`
- 启动时没有 session：打印 “No session directories found” 并 `return 1`。证据：`scripts/humanize.sh:802-807`
- 运行中 `.humanize/rlcr` 被删除：graceful stop，恢复终端，打印用户友好原因，`return 0`。证据：`scripts/humanize.sh:840-843`、`scripts/humanize.sh:904-907`、`scripts/humanize.sh:1027-1030`
- 当前 session 被删除但还有其他 session：切到最新 session。证据：`scripts/humanize.sh:959-984`、`scripts/humanize.sh:1099-1123`
- 当前 log 被删除：如果还有 session，切换；否则清空当前状态并等待新 session。证据：`scripts/humanize.sh:1099-1130`
- log 截断或轮转：进入重新搜索 log 的状态。证据：`scripts/humanize.sh:1081-1091`
- terminal 太小：重置 scroll region、显示居中提示并等待尺寸恢复。证据：`scripts/humanize.sh:672-688`、`scripts/humanize.sh:854-867`
- signal 中断：bash trap 调 `_cleanup`；zsh 用 `TRAPINT/TRAPTERM` 调 `_cleanup` 并返回信号码。证据：`scripts/humanize.sh:784-795`
- inconsistent log phase：`codex-run` round 大于等于 review round 时输出错误并返回空 log。证据：`scripts/humanize.sh:364-371`

**Invariants**

- cleanup 幂等：`cleanup_done=true` 后再次调用 `_cleanup` 或 `_graceful_stop` 直接返回。证据：`scripts/humanize.sh:738-742`、`scripts/humanize.sh:766-772`；测试覆盖：`tests/test-monitor-runtime.sh:137-177`
- graceful stop 必须调用 cleanup，因此会恢复终端。证据：`scripts/humanize.sh:764-777`；测试覆盖：`tests/test-monitor-runtime.sh:313-324`
- cleanup 必须关闭循环、重置 traps、杀后台进程、恢复终端并打印停止消息。证据：`scripts/humanize.sh:738-762`
- 运行中根目录删除必须返回 0，而不是错误退出。E2E 断言 `Monitoring stopped:`、`directory no longer exists`、`EXIT_CODE:0`。证据：`tests/test-monitor-e2e-real.sh:187-227`
- bash/zsh 均不得出现 glob 错误。证据：`tests/test-monitor-e2e-real.sh:200-205`、`tests/test-monitor-e2e-real.sh:360-369`
- terminal scroll region 必须恢复为 full screen：`printf "\033[r"`。证据：`scripts/humanize.sh:706-712`；测试覆盖：`tests/test-monitor-runtime.sh:299-310`
- SIGWINCH handler 不直接输出 escape sequence，只置 `resize_needed`，避免与 status bar draw 竞争。证据：`scripts/humanize.sh:779-795`

**Source Evidence**

- 入口和初始状态：`scripts/humanize.sh:261-277`
- session 发现算法：`scripts/lib/monitor-common.sh:37-63`
- log 发现、round 提取和 run/review consistency gate：`scripts/humanize.sh:284-375`
- state 文件到 `loop_status` 的映射：`scripts/lib/monitor-common.sh:147-192`
- state.md 字段解析和默认值：`scripts/humanize.sh:382-405`
- status bar 状态路由：`scripts/humanize.sh:531-576`
- progress/issues/drift 显示规则：`scripts/humanize.sh:595-623`
- terminal setup/restore/resize gates：`scripts/humanize.sh:651-712`
- cleanup/graceful stop/signal handling：`scripts/humanize.sh:731-796`
- 主循环根目录删除 gate：`scripts/humanize.sh:838-843`
- no-log waiting 分支：`scripts/humanize.sh:883-1008`
- follow-log 增量读取、截断、session/log 切换：`scripts/humanize.sh:1010-1178`
- runtime stub/source tests：`tests/test-monitor-runtime.sh:55-135`、`tests/test-monitor-runtime.sh:137-177`、`tests/test-monitor-runtime.sh:180-251`、`tests/test-monitor-runtime.sh:313-423`
- real E2E deletion tests：`tests/test-monitor-e2e-real.sh:54-228`、`tests/test-monitor-e2e-real.sh:231-370`
- real SIGINT tests：`tests/test-monitor-e2e-real.sh:375-550`、`tests/test-monitor-e2e-real.sh:553-685`

**Edge Cases and Risks**

- `monitor_find_state_file` 对多个 `*-state.md` 使用 `find` 的第一个结果，没有排序；如果多个 terminal state 文件同时存在，结果可能依赖文件系统遍历顺序。证据：`scripts/lib/monitor-common.sh:172-185`
- `state.md` 优先级高于所有 stop-state 文件；如果 active state 和 terminal state 同时残留，会显示 `active`。证据：`scripts/lib/monitor-common.sh:162-170`
- `_parse_state_md` 用 `grep "^key:"` 扫全文件，不限定 YAML frontmatter；正文中行首同名 key 也可能被解析。证据：`scripts/humanize.sh:390-405`
- `monitor_get_yaml_value` 存在于 common helper，但 `_humanize_monitor_codex` 的 state parser 没用它；实际算法不是 frontmatter parser。证据：`scripts/lib/monitor-common.sh:198-213`、`scripts/humanize.sh:382-405`
- `tail_pid` cleanup 路径存在，但当前片段没有看到赋值；cleanup 逻辑为未来/旧实现保留，实际增量读取是轮询 `tail -c`。证据：`scripts/humanize.sh:731-757`、`scripts/humanize.sh:1074-1080`
- `check_interval=2` 被定义，但实际内层轮询使用 `sleep 0.5`；该变量不是有效控制参数。证据：`scripts/humanize.sh:266-270`、`scripts/humanize.sh:900-902`、`scripts/humanize.sh:1022-1024`
- E2E bash SIGINT 测试对 SIGINT 交付不严格：若进程未退出会先 `SIGTERM`/`SIGKILL`，并可能把 “handled via SIGTERM” 算作 pass；因此 bash SIGINT 的真实保证弱于 zsh。证据：`tests/test-monitor-e2e-real.sh:492-519`
- `date -d` 是 GNU 风格；macOS 下失败会 fallback 原始 `started_at`，显示不会中断但不会本地化。证据：`scripts/humanize.sh:474-482`
- `grep -oP` 用于读取 `.review-phase-started` 的 `build_finish_round`，部分 grep 实现不支持 `-P`；失败时只是省略 round display。证据：`scripts/humanize.sh:539-550`

**What Is Explicitly Out of Scope**

- 不分析 RLCR loop 如何生成 state 文件、goal tracker 或 log。
- 不分析 Codex 调用、hook 执行、review/build 业务算法。
- 不分析安装脚本、README、截图、营销文案或普通 CLI 使用说明。
- 不验证测试是否能在当前机器通过；本次只做只读源码证据提取。
- 不覆盖 monitor UI 的视觉设计细节，除非它直接决定状态路由或 failure handling。
- 不覆盖 git status/goal tracker 的完整解析正确性，只把它们作为 status bar 输入提及。