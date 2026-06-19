**Topic and conclusion**

Topic: Code-review phase and severity gate。

结论: 该机制把 `codex review --base <base>` 作为实现完成后的强制质量门。进入 review phase 后，循环不再依赖 `COMPLETE`，也不受 `max_iterations` 限制；唯一通过条件是 `codex review` 的合并日志末尾窗口中没有检测到 `[P0-9]` severity marker。任何 `[P0]` 到 `[P9]` 都等价阻塞，没有按严重度分级放行或加权评分。若 review 命令失败、日志缺失或日志为空，则 fail-closed，阻塞退出并要求重试。

**Algorithm subset covered**

覆盖的算法子集:

- Review phase 入口: implementation review 输出最后非空行 `COMPLETE` 后，设置 `review_started=true`，创建 `.review-phase-started` marker，并立即运行 `codex review`。
- Review execution: 使用 `BASE_COMMIT` 优先，否则 `BASE_BRANCH`，执行 `codex review --base`，stdout/stderr 合并写入 `round-N-codex-review.log`。
- Severity gate: `detect_review_issues(round)` 扫描 review log 的最后 50 行，查找每行前 10 个字符内的 `[P0-9]`。
- Routing:
  - 找到 marker: 抽取从首个 marker 行到文件末尾，写 `round-N-review-result.md`，阻塞退出，把 findings 反馈给 Claude 修复。
  - 未找到 marker: 进入 Finalize Phase。
  - 命令失败或日志无效: 阻塞退出，要求重试。
- Review phase safety gates: schema、branch consistency、summary、incomplete task、marker 文件一致性。
- 明确跳过: review phase 跳过 plan file integrity gate 和 max iteration gate。

**Pseudocode**

```text
on stop hook:
  find active loop by session
  if no loop: allow exit

  parse state.md / finalize-state.md
  validate current_round, max_iterations, review_started, base_branch, branch consistency
  if incomplete tasks: block
  if summary file missing: block

  if finalize-state.md:
    mark complete-state.md
    allow exit

  if implementation_phase:
    run codex exec summary review
    read round-N-review-result.md
    if last_nonempty_line == COMPLETE:
      if current_round >= max_iterations:
        end MAXITER
      else:
        set review_started=true
        reset drift counters
        create .review-phase-started
        run_and_handle_code_review(current_round + 1)

  if review_started == true:
    if .review-phase-started missing:
      block invalid review state
    run_and_handle_code_review(current_round + 1)

run_and_handle_code_review(round):
  exit_code = run_codex_code_review(round)
  if exit_code != 0:
    block_review_failure(round)

  detect_exit, content = detect_review_issues(round)

  if detect_exit == 2:
    block_review_failure(round, "no valid output")
  else if detect_exit == 0 and content not empty:
    set current_round = round
    write review-fix prompt
    block with findings
  else:
    mv state.md -> finalize-state.md
    block with finalize prompt

detect_review_issues(round):
  log = CACHE_DIR/round-{round}-codex-review.log
  result = LOOP_DIR/round-{round}-review-result.md

  if log missing or empty:
    return 2

  tail = last 50 lines of log
  first = first line in tail where substr(line, 1, 10) matches /\[P[0-9]\]/

  if first exists:
    extracted = log[first_absolute_line .. EOF]
    write extracted to result
    output "## Codex Review Issues" + extracted
    return 0

  return 1
```

**Transition table**

| State / condition | Gate result | Transition |
|---|---:|---|
| No active loop | allow | exit 0 |
| `review_started` invalid / `base_branch` missing / branch changed | block | stay in loop |
| Implementation review last line is `COMPLETE` | pass implementation | set `review_started=true`, create marker, run code review |
| Review phase with missing `.review-phase-started` | block | invalid state, require cancel/restart |
| `codex review` non-zero exit | block | retry required |
| review log missing or empty | block | retry required |
| `[P0-9]` found in last 50 lines, first 10 chars | block | increment review round, feed findings to Claude |
| no `[P0-9]` found | pass | enter Finalize Phase |
| Finalize Phase summary complete | allow | rename to `complete-state.md` |

**Source evidence**

- `prompt-template/codex/code-review-phase.md:3-4`: 该文件只是 audit 文档，并说明 `codex review` 不接收 prompt input，而是基于 git diff 自动 review。
- `prompt-template/codex/code-review-phase.md:14-17`: 定义 code review phase 行为: 运行 `codex review --base`，扫描 `[P0-9]`，有问题则返回修复 prompt，无问题进入 Finalize Phase。
- `prompt-template/codex/code-review-phase.md:21-28`: 预期 issue 格式为 bullet 行上的 `[P0]`、`[P1]` 等 severity marker。
- `hooks/loop-codex-stop-hook.sh:134-140`: 从 state 读取 `full_review_round`、`review_started`，并把 code review effort 固定为 `high`。
- `hooks/loop-codex-stop-hook.sh:244-269`: `review_started` 必须是 `true/false`，`base_branch` 不能为空，否则阻塞为 schema outdated。
- `hooks/loop-codex-stop-hook.sh:321-327`: review phase 中跳过 plan file integrity check，因为此阶段只关心 code review。
- `hooks/loop-codex-stop-hook.sh:962-965`: review phase 跳过 max iteration check，直到 `[P?]` issues 清零。
- `hooks/loop-codex-stop-hook.sh:981-990`: Finalize Phase 不再执行 Codex review，检查通过后把状态转为 `complete-state.md`。
- `hooks/loop-codex-stop-hook.sh:1214-1220`: review base 优先使用 loop start 捕获的 `BASE_COMMIT`，否则使用 `BASE_BRANCH`，避免分支自比较。
- `hooks/loop-codex-stop-hook.sh:1223-1246`: 生成 `round-N-codex-review.cmd`、`round-N-codex-review.log` 和 audit prompt。
- `hooks/loop-codex-stop-hook.sh:1265-1267`: 实际执行 `codex review ... --base "$review_base"`，并把 stdout/stderr 合并写入 log。
- `hooks/loop-codex-stop-hook.sh:1288-1316`: `run_and_handle_code_review` 的三分支: command failure 阻塞、detect exit 0 阻塞修复、无 issues 进入 finalize。
- `hooks/loop-codex-stop-hook.sh:1494-1584`: 发现 issues 后更新 `current_round`，生成 review-fix prompt，并以 JSON `decision=block` 反馈给 Claude。
- `hooks/loop-codex-stop-hook.sh:1586-1658`: `codex review` 失败或无有效输出是 hard error，阻塞退出并要求重试。
- `hooks/loop-codex-stop-hook.sh:1864-1870`: 在 review phase 中 `COMPLETE` signal 被忽略，退出由 code review gate 决定。
- `hooks/loop-codex-stop-hook.sh:1894-1909`: implementation `COMPLETE` 后设置 `review_started=true`、创建 `.review-phase-started`，并立即运行初始 code review。
- `hooks/loop-codex-stop-hook.sh:1919-1944`: review phase 每次退出都会运行 code review；缺少 marker 文件则阻塞，防止手工篡改 state。
- `hooks/lib/loop-common.sh:720-724`: `detect_review_issues` 返回码定义: `0=issues found`，`1=no issues`，`2=log missing/empty hard error`。
- `hooks/lib/loop-common.sh:728-739`: severity gate 算法说明: 只扫最后 50 行，每行前 10 字符内寻找 `[P?]`，找到则从该行抽取到末尾。
- `hooks/lib/loop-common.sh:745-748`: log 文件缺失或为空返回 `2`。
- `hooks/lib/loop-common.sh:755-766`: 实现上 `tail -n 50` 后用 `awk substr($0, 1, 10) ~ /\[P[0-9]\]/`。
- `hooks/lib/loop-common.sh:768-783`: 找到 marker 后写 `round-N-review-result.md`，输出 `## Codex Review Issues`，返回 `0`。
- `hooks/lib/loop-common.sh:786-787`: 未找到 marker 返回 `1`，表示无 issues。
- `tests/test-codex-review-merge.sh:5-15`: 测试文件直接声明被测算法: 最后 50 行、前 10 字符、从首个匹配行抽取到末尾、无匹配返回 1。
- `tests/test-codex-review-merge.sh:62-80`: `[P1]`、`[P2]` 在常见 bullet 位置时必须检测到。
- `tests/test-codex-review-merge.sh:89-107`: `[P?]` 不在前 10 字符内时必须忽略。
- `tests/test-codex-review-merge.sh:139-168`: 缺失或空 log 返回 hard error `2`。
- `tests/test-codex-review-merge.sh:177-197`: 长 log 中末尾窗口内的 `[P1]` 能被检测到。
- `tests/test-codex-review-merge.sh:200-226`: 超出最后 50 行窗口的早期 `[P1]` 被忽略。
- `tests/test-codex-review-merge.sh:230-254`: 多个 marker 时从第一个 marker 行抽取到末尾。
- `tests/test-codex-review-merge.sh:263-303`: marker 在行首或 `- [P1]` bullet 前缀下均可检测。
- `tests/test-codex-review-merge.sh:306-330`: issues found 时必须创建 `round-N-review-result.md`。
- `prompt-template/block/codex-review-failed.md:3-18`: review 失败模板要求展示 exit code、result file、debug files、stderr 最后 50 行，并提示下次退出会再次尝试 review。

**Edge cases and risks**

- Severity 没有阈值: `[P0]` 到 `[P9]` 全部等价阻塞；算法只做 marker 存在性检测，不解析数字含义，不做评分或优先级 routing。证据是 scanner 正则仅为 `/\[P[0-9]\]/`，见 `hooks/lib/loop-common.sh:761-763`。
- 可能漏报: 只扫描最后 50 行。若 `codex review` 先输出 findings，后面追加超过 50 行调试/摘要，早期 `[P?]` 会被忽略；测试明确固化了该行为，见 `tests/test-codex-review-merge.sh:200-226`。
- 可能漏报: marker 必须出现在每行前 10 个字符内。带长前缀、深缩进、文件名前缀的 issue 行可能被忽略；测试也固化了“中间位置忽略”，见 `tests/test-codex-review-merge.sh:89-107`。
- 可能误报: 任意 tail 窗口内、前 10 字符出现 `[P0-9]` 都会被视为 issue；算法不校验 bullet 格式、路径、解释文本或是否来自真正 review finding。
- Review phase 可能无限持续: max iteration gate 在 review phase 被跳过，直到 marker 清零或失败/取消；见 `hooks/loop-codex-stop-hook.sh:962-965`。
- `base_branch` 缺失的 skip path 基本不可达或至少存在设计张力: 前置 schema gate 已在 `base_branch` 为空时阻塞，见 `hooks/loop-codex-stop-hook.sh:258-269`，但后面仍有 “No base_branch configured, skipping code review phase” 分支，见 `hooks/loop-codex-stop-hook.sh:1886-1890`。
- 失败模板变量有不一致风险: 模板使用 `{{CODEX_EXIT_CODE}}` 和 `{{CODEX_STDERR_FILE}}`，见 `prompt-template/block/codex-review-failed.md:5-11`；hook 传入的是 `EXIT_CODE` 和 `CODEX_LOG_FILE`，见 `hooks/loop-codex-stop-hook.sh:1640-1648`。如果模板渲染器不兼容别名，失败提示可能残留未替换占位符。
- Audit 文档和实际文件也有轻微不一致: 模板列出 `round-N-codex-review.out` 和 stderr log，见 `prompt-template/codex/code-review-phase.md:34-36`；实际 code review 把 stdout/stderr 合并进单个 `.log`，见 `hooks/loop-codex-stop-hook.sh:1265-1267`，且 `detect_review_issues` 也说明分析 combined log，见 `hooks/lib/loop-common.sh:738-739`。

**What is explicitly out of scope**

- 不覆盖安装、CLI 获取、认证、网络、营销说明、截图或普通使用文档。
- 不覆盖 implementation phase 的完整 RLCR 规划算法、goal tracker 更新算法、BitLesson 选择算法、agent teams delegation、methodology analysis phase。
- 不评估 `codex review` 自身如何生成 `[P0-9]`，只分析 Humanize 如何调用、解析和路由其输出。
- 不运行测试、不修改文件、不提交；本次只基于 pinned HEAD 工作树的只读源码证据。