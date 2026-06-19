**Topic and conclusion**

Topic: Core subset synthesis and skip list

结论：该子集的核心机制是一个“计划生成 -> 计划合规/理解预检 -> RLCR 状态初始化 -> Stop Hook 驱动的两阶段反馈循环”的状态机。实现阶段用 `codex exec` 审阅轮次摘要，只有摘要审阅最后一条非空行是 `COMPLETE` 才进入 Review Phase；Review Phase 改用 `codex review --base <captured-base>` 检查 `[P0-9]` 问题，直到无问题后进入 Finalize Phase。跳过逻辑主要用于：跳过预检/测验、跳过实现直接代码审查、direct 模式跳过计划收敛、Review/Finalize 阶段跳过不再适用的 gate。

**Algorithm subset covered**

覆盖的算法子集仅限这些路径中的行为定义：

- `README.md`: RLCR 两阶段概要。
- `docs/usage.md`: 用户可见的两阶段语义、quiz/skip/yolo、命令选项、配置键。
- `commands/gen-plan.md`: 计划生成、Claude/Codex 收敛、manual review gate、auto-start gate、任务路由标签。
- `commands/start-rlcr-loop.md`: plan compliance pre-check、plan quiz、RLCR 流程语义、Goal Tracker、skip-impl 模式。
- `scripts/setup-rlcr-loop.sh`: CLI 参数、输入 gate、状态文件初始化、skip-impl 初始化、Goal Tracker/round contract/prompt 初始化。
- `hooks/loop-codex-stop-hook.sh`: Stop Hook 状态读取、各类 gate、Codex 摘要审阅、Review Phase、Finalize、drift circuit breaker、下一轮 prompt 生成。

显式跳过：安装、营销、截图、monitor UI、非行为性 quick start 文案；只在 README/usage 中取定义 RLCR 行为的行。

**Pseudocode**

```text
gen_plan(draft, output, mode, auto_start):
  parse flags
  load merged config: alternative_plan_language, gen_plan_mode
  validate IO
  if draft_not_relevant: stop
  create output plan from template + original draft
  codex_v1 = ask_codex(first_pass_analysis)
  candidate = claude_synthesize(draft, codex_v1)

  if mode == direct:
    convergence_status = partially_converged
    human_review_required = true
  else:
    repeat up to 3 rounds:
      codex_review = ask_codex(candidate, prior_disagreements)
      candidate = claude_revise(required_changes)
      update convergence_matrix
      if no required changes and no high-impact disagree: converged
      if 2 consecutive no material changes: converged/partial per state

  collect pending user decisions
  if mode == direct: human_review_required = true
  else if auto_start and convergence_status == converged:
    human_review_required = false
  else:
    human_review_required = true

  write final plan with AC, boundaries, task breakdown, deliberation, pending decisions
  if alt language configured: write translated variant
  if auto_start and converged and discussion and no PENDING:
    start_rlcr_loop(--skip-quiz, output)
```

```text
start_rlcr_loop(args):
  if not skip_impl/help:
    extract safe relative plan path
    run plan compliance checker
    fail closed on relevance/branch-switch/malformed result

  if not skip_impl/yolo/skip_quiz/help and plan_content_available:
    run plan quiz
    if wrong:
      ask user proceed or stop
      if stop: stop

  setup_rlcr_loop(args)
```

```text
setup_rlcr_loop(args):
  defaults:
    max_iterations=42
    codex_timeout=5400
    full_review_round=5
    skip_impl=false
    ask_codex_question=true
    bitlesson_allow_empty_none=true

  parse args
  validate deps: codex, jq, git
  reject active loop
  validate agent_teams env if enabled
  if no plan_file and skip_impl:
    use placeholder plan, SKIP_IMPL_NO_PLAN=true
  else if no plan_file:
    error

  validate git repo and HEAD
  if not SKIP_IMPL_NO_PLAN:
    validate relative non-symlink in-project plan
    validate tracking policy:
      if track_plan_file: tracked and clean
      else: must be untracked/gitignored
    validate plan has >=5 lines and >=3 content lines

  determine start_branch, base_branch, base_commit
  require clean working tree excluding untracked .humanize runtime paths

  create .humanize/rlcr/<timestamp>/
  copy plan or create skip-impl placeholder
  initialize bitlesson
  write state.md:
    current_round=0
    review_started=skip_impl
    base_branch/base_commit/start_branch
    codex config, full_review_round
    ask_codex_question, agent_teams, privacy
    bitlesson_required=false if skip_impl else true
    mainline_stall_count=0
    last_mainline_verdict=unknown
    drift_status=normal

  if skip_impl: create .review-phase-started marker
  create goal-tracker:
    normal: immutable goal/AC + mutable tracking
    skip_impl with plan: plan-anchored review objective
    skip_impl no plan: review-only objective
  create round-0-summary and round-0-contract/prompt
```

```text
stop_hook(hook_input):
  find active loop matching session_id; if none: allow exit
  run background-task guards; may short-circuit
  resolve state file:
    state.md -> normal/review
    finalize-state.md -> finalize
    methodology-analysis-state.md -> methodology

  parse state and validate schema:
    require current_round, max_iterations, plan_tracked, start_branch,
    review_started, base_branch
    validate codex_model/effort and numeric fields

  if branch changed from start_branch: block
  if review_started != true:
    verify plan backup and original plan integrity
  else:
    skip plan integrity check

  if incomplete tasks in transcript: block
  if git status fails: block
  if large changed code/doc file >2000 lines: block
  if methodology phase:
    complete or block methodology analysis

  require clean git tree excluding untracked .humanize runtime paths
  if push_every_round: require no unpushed commits
  require summary file
  if anti-drift active and not finalize: require round contract
  if bitlesson_required and not finalize: validate BitLesson Delta
  if round 0 and implementation phase: require goal tracker initialized
  if not finalize/review and next_round > max_iterations: stop maxiter
  if finalize: rename to complete-state and allow exit

  build Codex summary review prompt:
    regular or full alignment if current_round % full_review_round == full_review_round - 1
    include summary, commit history, recent round files, goal tracker update section

  if review_started == false:
    run codex exec(prompt)
    require non-zero-free output and review result file
    read review result
    require Mainline Progress Verdict unless last line is STOP
    update drift counters:
      ADVANCED -> stall=0, drift=normal
      STALLED/REGRESSED -> stall += 1
      stall >= 2 -> next prompt is drift replan
      stall >= 3 -> stop loop
    if last non-empty line == COMPLETE:
      if current_round >= max_iterations: maxiter
      else set review_started=true, create marker, run codex review round+1
    if last non-empty line == STOP: stop loop
    else update current_round=next_round, create next prompt, block exit

  if review_started == true:
    require .review-phase-started marker
    run codex review --base base_commit_or_base_branch
    if command fails or stdout missing: block retry
    if [P0-9] issues found: current_round=review_round, create review-fix prompt, block
    if no [P0-9] issues: enter finalize phase and block with finalize prompt
```

**Transition table**

| State | Trigger / Gate | Action | Next state |
|---|---|---|---|
| `No active loop` | Stop hook cannot find active loop or session mismatch | exit 0 | outside RLCR |
| `Planning` | draft relevant and IO valid | write plan template + draft | `Codex first-pass` |
| `Planning` | `GEN_PLAN_MODE=direct` | skip convergence rounds, mark partial, require human review | `Final plan generation` |
| `Planning` | discussion mode convergence | run up to 3 Claude/Codex rounds | `converged` or `partially_converged` |
| `Planning` | `auto_start && converged && discussion && no PENDING` | start RLCR with `--skip-quiz` | `RLCR round 0` |
| `Preflight` | compliance check FAIL | stop command | no loop |
| `Preflight` | quiz wrong + user stops | stop command | no loop |
| `Setup normal` | all setup gates pass | state `review_started=false`; create tracker/prompt | `Implementation Phase` |
| `Setup skip-impl` | `--skip-impl` | state `review_started=true`; create review marker | `Review Phase` |
| `Implementation Phase` | incomplete tasks/git dirty/missing summary/contract/BitLesson/goal tracker | JSON block | same round |
| `Implementation Phase` | `codex exec` failure/no result/empty result | JSON block retry | same round |
| `Implementation Phase` | review missing mainline verdict and not STOP | JSON block retry | same round |
| `Implementation Phase` | last line neither `COMPLETE` nor `STOP` | update round/drift, create next prompt | next implementation round |
| `Implementation Phase` | `COMPLETE` | set `review_started=true`; run initial `codex review` | `Review Phase` or finalize/fix |
| `Implementation Phase` | `STOP` | end loop as stop | terminal stop |
| `Implementation Phase` | max iteration exceeded before review | end loop as maxiter | terminal maxiter |
| `Review Phase` | missing `.review-phase-started` | JSON block invalid state | same phase |
| `Review Phase` | `codex review` failure/no stdout | JSON block retry; cannot skip review | same phase |
| `Review Phase` | `[P0-9]` found | update round, create fix prompt | next review-fix round |
| `Review Phase` | no `[P0-9]` found | rename state to `finalize-state.md`, send finalize prompt | `Finalize Phase` |
| `Finalize Phase` | checks pass and summary exists | rename to `complete-state.md` | terminal complete |

**Source evidence**

- RLCR 本质是两阶段循环：README 说 Implementation 阶段由 Claude 工作、Codex 审阅摘要，Code Review 阶段用 severity markers 检查代码质量，问题反馈直到解决：`README.md:20-27`。usage 也定义 Implementation Phase 与 Review Phase，并说明循环直到 AC 满足或无问题：`docs/usage.md:5-12`。
- `start-rlcr-loop` 参数定义含 `--skip-impl`、`--claude-answer-codex`、`--agent-teams`、`--yolo`、`--skip-quiz`、`--full-review-round` 等核心开关：`commands/start-rlcr-loop.md:1-8`，`docs/usage.md:70-99`。
- Plan compliance pre-check 的 skip list：`--skip-impl`、`-h/--help` 跳过；路径必须相对、无 `..`、安全字符；checker 返回 `PASS` 才继续，`FAIL_RELEVANCE` / `FAIL_BRANCH_SWITCH` / malformed 都停止：`commands/start-rlcr-loop.md:13-57`。
- Plan quiz 是 advisory，不是硬 gate；skip 条件包括 `--skip-impl`、`--yolo`、`--skip-quiz`、help、无 plan 内容；答错后用户可继续或停止：`commands/start-rlcr-loop.md:60-106`。usage 进一步说明 `--skip-quiz` 只跳 quiz，`--yolo` 同时让 Claude 直接回答 Codex Open Questions，auto-start 计划会自动跳 quiz：`docs/usage.md:37-41`。
- RLCR 命令层流程：coding 任务由 Claude 执行，analyze 任务经 `/humanize:ask-codex`；Codex summary review 输出 `COMPLETE` 后进入 Review Phase；Review Phase 用 `codex review --base`，发现 `[P0-9]` 则修复，无 issue 才 Finalize：`commands/start-rlcr-loop.md:117-128`。
- Round 语义不是任务/阶段/里程碑，而是“agent 认为整个 plan 完成后写 summary 并尝试退出”的边界：`commands/start-rlcr-loop.md:130-138`。
- Goal Tracker 的不可变/可变分区、AC 映射、task tag routing、plan evolution、deferral、full alignment check：`commands/start-rlcr-loop.md:139-159`。
- Skip implementation 模式定义：`--skip-impl` 跳过实现阶段，plan 可选，不需要 goal tracker 初始化，退出时直接代码审查：`commands/start-rlcr-loop.md:197-209`。
- `gen-plan` 的 hard constraint：计划生成阶段不得实现代码、不得改源代码或提交；auto-start 只有在 discussion 模式、converged、无 pending decision 时才可启动 RLCR，编码发生在后续 loop 中：`commands/gen-plan.md:20-30`。
- `gen-plan` 阶段顺序和核心 pipeline：mode setup、config、IO validation、relevance、Codex first-pass、Claude v1、Claude/Codex convergence、issue resolution、final plan、write/auto-start：`commands/gen-plan.md:32-45`。
- `GEN_PLAN_MODE=direct` 跳过整个 convergence phase，设置 `PLAN_CONVERGENCE_STATUS=partially_converged` 且 `HUMAN_REVIEW_REQUIRED=true`，因此不能满足 auto-start：`commands/gen-plan.md:255-258`。
- Convergence round 的 Codex 输出 schema、Claude 修订、matrix 字段和 termination rules：无 required changes/高影响 disagree、连续两轮无实质变化、最多 3 轮：`commands/gen-plan.md:261-298`。
- Manual review gate：direct 总是需要人工 review；否则只有 `AUTO_START_RLCR_IF_CONVERGED=true && PLAN_CONVERGENCE_STATUS=converged` 才可设 `HUMAN_REVIEW_REQUIRED=false`；pending decisions 无论是否人工 review 都要写入计划，并在 auto-start 阶段阻塞：`commands/gen-plan.md:305-329`。
- Final plan 必含 AC、Path Boundaries、Task Breakdown，且每个 task exactly one routing tag `coding` 或 `analyze`：`commands/gen-plan.md:447-457`，生成规则禁止未标记任务或其他 tag 值：`commands/gen-plan.md:523-529`。
- Auto-start gate 的四个条件：`AUTO_START_RLCR_IF_CONVERGED=true`、`PLAN_CONVERGENCE_STATUS=converged`、`GEN_PLAN_MODE=discussion`、无 `PENDING`；启动时调用 `/humanize:start-rlcr-loop --skip-quiz <output-plan-path>` 或 fallback 到 setup script：`commands/gen-plan.md:594-614`。
- setup 默认状态：Codex timeout 5400，max iterations 42，full review round 5：`scripts/setup-rlcr-loop.sh:17-23`。状态变量初值包括 `PLAN_FILE`、`TRACK_PLAN_FILE`、`SKIP_IMPL`、`ASK_CODEX_QUESTION`、`AGENT_TEAMS`、`PRIVACY_MODE`：`scripts/setup-rlcr-loop.sh:39-56`。
- setup 参数解析：`--skip-impl` 设置 `SKIP_IMPL=true`；`--claude-answer-codex` 与 `--yolo` 都让 `ASK_CODEX_QUESTION=false`；`--skip-quiz` 在 setup script 中是 no-op，因为 quiz 在 command markdown：`scripts/setup-rlcr-loop.sh:272-290`。
- setup 依赖和互斥 gate：必须有 `codex`、`jq`、`git`；已有 active loop 则拒绝；agent teams 需要环境变量：`scripts/setup-rlcr-loop.sh:334-397`。
- skip-impl 无 plan 时设置内部 placeholder，`--track-plan-file` 被忽略；非 skip-impl 且无 plan 则报错：`scripts/setup-rlcr-loop.sh:408-427`。
- setup plan validation skip list：`SKIP_IMPL_NO_PLAN=true` 时跳过 plan file validation 和 content validation；否则拒绝绝对路径、空格、shell 元字符、symlink、项目外路径、submodule 内路径，并验证 git tracking 策略：`scripts/setup-rlcr-loop.sh:445-609`。
- plan 内容 gate：至少 5 行、至少 3 条非空非注释 content lines；skip-impl no-plan 时跳过并设 `LINE_COUNT=0`：`scripts/setup-rlcr-loop.sh:611-676`。
- setup 固定基线：记录 `START_BRANCH`，验证 branch/model/effort YAML 安全；工作树必须 clean，排除未跟踪 `.humanize/` runtime；base branch 优先级为用户输入、remote default、本地 main、本地 master，并捕获 `BASE_COMMIT` 防止 base branch 自身前进导致 diff 为空：`scripts/setup-rlcr-loop.sh:682-816`。
- state 初始化字段：`current_round`、`max_iterations`、Codex 配置、plan、branches、`base_commit`、`review_started`、`ask_codex_question`、`agent_teams`、`privacy_mode`、BitLesson、`mainline_stall_count`、`last_mainline_verdict`、`drift_status`：`scripts/setup-rlcr-loop.sh:868-907`。
- skip-impl 初始化：`INITIAL_REVIEW_STARTED="$SKIP_IMPL"`；skip-impl 禁用 BitLesson enforcement；skip-impl 创建 `.review-phase-started` marker：`scripts/setup-rlcr-loop.sh:872-923`。
- skip-impl 有 plan 时 Goal Tracker 保留原 plan scope anchor；无 plan 时目标是让当前 branch 通过 code review，不回归现有行为：`scripts/setup-rlcr-loop.sh:931-1057`。
- normal mode prompt 要求先初始化 Goal Tracker、创建 round contract、任务用 `[mainline]`/`[blocking]`/`[queued]`，并按 plan task routing：`coding -> Claude`、`analyze -> /humanize:ask-codex`、无 tag 默认 `coding`：`scripts/setup-rlcr-loop.sh:1290-1344`。
- Stop Hook 作用：拦截退出并用 Codex 审阅；无 active loop/session mismatch 时允许退出；loop 终止由无 state、Codex `COMPLETE`、max iterations 控制：`hooks/loop-codex-stop-hook.sh:1-12`，`hooks/loop-codex-stop-hook.sh:30-37`，`hooks/loop-codex-stop-hook.sh:61-69`。
- Stop Hook 解析 state，映射 `PLAN_TRACKED`、`START_BRANCH`、`BASE_BRANCH`、`BASE_COMMIT`、`CURRENT_ROUND`、`MAX_ITERATIONS`、`REVIEW_STARTED`、Codex config、BitLesson、drift fields，并重新验证模型/effort、required fields 和 numeric fields：`hooks/loop-codex-stop-hook.sh:103-218`。
- schema gate：缺少 `plan_tracked/start_branch`、`review_started`、`base_branch` 会 block；缺少 `full_review_round` 只是警告并默认 5：`hooks/loop-codex-stop-hook.sh:220-283`。
- branch consistency gate：当前 branch 必须等于 start branch，否则 block；Review Phase 跳过 plan integrity，因为 review 不再需要 plan，且 skip-impl 可能无真实 plan：`hooks/loop-codex-stop-hook.sh:285-327`。
- plan integrity gate：实现阶段要求 loop 目录中的 plan backup 存在、原 plan 未删除、tracked plan 无 uncommitted 修改、原 plan 与 backup 无 diff：`hooks/loop-codex-stop-hook.sh:329-399`。
- cheap pre-Codex gates：有未完成 task 则 block；git status 失败 fail-closed；changed code/doc 文件超过 2000 行则 block：`hooks/loop-codex-stop-hook.sh:401-457`，`hooks/loop-codex-stop-hook.sh:485-604`。
- exit 前要求 git clean，排除未跟踪 `.humanize/` runtime；`push_every_round=true` 时要求无 ahead commits：`hooks/loop-codex-stop-hook.sh:666-782`。
- summary/round contract/BitLesson/Goal Tracker gates：缺 summary block；anti-drift state 存在时 require round contract；非 finalize 且 BitLesson required 时校验 delta；round 0 implementation phase require Goal Tracker 初始化：`hooks/loop-codex-stop-hook.sh:784-955`。
- max iteration 与 finalize：Review/Finalize 跳过 max iteration check；Finalize Phase 通过所有检查后 rename 为 `complete-state.md` 并退出，不再做 Codex review：`hooks/loop-codex-stop-hook.sh:956-991`。
- Codex summary review prompt：每 `FULL_REVIEW_ROUND` 的 `N-1, 2N-1...` 轮做 Full Alignment Check；prompt 包含 summary、commit history、recent round files、goal tracker update section：`hooks/loop-codex-stop-hook.sh:999-1125`。
- Codex CLI gate 与参数：缺 Codex CLI block；summary review 用 `codex exec`，review phase 用 `codex review`；嵌套 Codex 调用会尝试 `--disable codex_hooks` 防止 hook recursion：`hooks/loop-codex-stop-hook.sh:1127-1199`。
- Review Phase code review 以 captured `BASE_COMMIT` 优先作为 review base，否则用 `BASE_BRANCH`；这避免在 main 上提交后 branch ref 前进导致自比较：`hooks/loop-codex-stop-hook.sh:1210-1267`。
- `codex review` result routing：命令失败 block；stdout 缺失是 hard error；检测到 `[P0-9]` 则进入 review-fix prompt；无问题进入 Finalize：`hooks/loop-codex-stop-hook.sh:1277-1317`。
- Finalize Phase prompt 只允许功能等价简化/重构，不得改功能、破坏测试或引入 bug；进入 finalize 会 rename state 为 `finalize-state.md` 并 block 让 Claude 完成 finalize summary：`hooks/loop-codex-stop-hook.sh:1319-1403`。
- implementation summary review 执行 `codex exec`；非零 exit、无 result file、empty result 都 block retry；若 Codex 输出到 stdout 则复制到 result file：`hooks/loop-codex-stop-hook.sh:1661-1809`。
- summary review 的 terminal marker：最后一条非空行必须精确是 `COMPLETE` 或 `STOP` 才触发对应路径；避免误判 `CANNOT COMPLETE`：`hooks/loop-codex-stop-hook.sh:1811-1816`。
- mainline drift 规则：implementation phase 必须抽取 Mainline Progress Verdict；`ADVANCED` 重置 stall；`STALLED/REGRESSED` 增加 stall，`>=2` 触发 replan prompt，`>=3` 停止 loop；`COMPLETE` 重置 drift：`hooks/loop-codex-stop-hook.sh:1823-1862`。
- `COMPLETE` 处理：Review Phase 中忽略 summary `COMPLETE`，由 `codex review` 决定退出；Implementation Phase 的 `COMPLETE` 设置 `review_started=true`、清 drift、创建 `.review-phase-started`，并立即运行 initial code review：`hooks/loop-codex-stop-hook.sh:1864-1912`。
- Review Phase 每次退出都运行 `codex review`，且必须存在 marker 防止手动改 state；循环直到无 `[P0-9]`：`hooks/loop-codex-stop-hook.sh:1916-1945`。
- `STOP` 处理：Full Alignment 中 STOP 作为 stagnation circuit breaker；非 alignment 轮出现 STOP 也会尊重并终止：`hooks/loop-codex-stop-hook.sh:1952-1984`。
- 普通问题反馈路径：更新 `current_round` 和 drift 字段，创建下一轮 summary/prompt；drift required 时使用 recovery prompt；Open Question 检测开启时注入 AskUserQuestion notice；追加 routing reminder、push note、goal tracker update request、agent-teams continuation：`hooks/loop-codex-stop-hook.sh:1986-2221`。

**Edge cases and risks**

- **git 在受限环境中可能失败**：算法对 git status/rev-parse 等多处 fail-closed；若 git 命令超时或失败，会 block 或 setup 失败，而不是继续执行。
- **Review Phase 不受 max iteration 限制**：实现阶段受 `max_iterations` 限制，但 Review Phase 明确跳过 max iteration，因为必须持续到 `[P0-9]` 清零。这可避免绕过 code review，但也可能无限卡在 review failure 或长期问题修复中。
- **`BASE_BRANCH` 空的 skip path 理论存在但 setup 通常已防止**：Stop Hook 在 `COMPLETE` 后若 `BASE_BRANCH` 空会设置 `REVIEW_SKIPPED`，但所读片段未看到后续调用 skipped finalize；setup 正常会要求 base branch 存在。因此实际风险是旧/损坏 state 可能走到未完整处理的分支。
- **plan integrity 在 Review Phase 被跳过**：这是为 skip-impl 和 review-only 合理设计，但意味着进入 Review Phase 后 plan 改动不再由 hook 阻止。
- **Open Question 检测是启发式**：仅检测长度 `<40` 且包含 `Open Question` 的行，格式偏差可能漏注入 AskUserQuestion notice。
- **mainline verdict 是硬依赖**：implementation review 若缺少 `Mainline Progress Verdict` 会 block retry；如果 Codex 模板或输出格式不稳定，会造成非代码问题的循环阻塞。
- **large file gate 只检查 git status 中变化文件**：未变化的大文件不在该 gate 的检测范围内；且阈值固定 2000 行。
- **`--yolo` 扩大自动化风险**：它不仅跳过 quiz，还让 Claude 直接回答 Codex Open Questions，减少人工澄清；这在 usage 中被定义为 full automation。
- **direct plan mode 不能 auto-start**：设计上将 direct 视为 partial convergence 并强制 human review；这避免未审阅计划直接进入 RLCR，但降低全自动路径可用性。

**What is explicitly out of scope**

- 安装流程、marketplace 命令、依赖安装链接、截图与 monitor dashboard 展示。
- `gen-idea`、`refine-plan`、`ask-gemini`、`ask-codex` 的完整机制；只保留其被本子集调用或路由的行为。
- BitLesson 内部 selector/lesson 格式；这里只纳入 RLCR gate 和 summary delta 要求。
- `hooks/lib/*`、templates、Python todo checker、config loader 的内部实现；本报告只引用 focus paths 中暴露出的调用语义。
- Codex CLI 自身的 review scoring 算法；仓库只把 `[P0-9]`、`COMPLETE`、`STOP`、Mainline Progress Verdict 作为外部输出协议处理。
- UI、营销表述、项目定位叙事、图片资源、安装文档。