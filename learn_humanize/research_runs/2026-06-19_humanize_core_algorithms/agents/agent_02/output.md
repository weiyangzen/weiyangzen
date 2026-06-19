**Topic and Conclusion**

Topic: RLCR setup state initialization.

结论：`setup-rlcr-loop.sh` 的核心机制是一个“启动前门禁 + 状态目录初始化 + Round 0 工件生成”的状态机。只有在依赖、git 仓库、plan 文件、工作区洁净、base branch、YAML 安全性、互斥 active loop 等门禁全部通过后，才创建 `.humanize/rlcr/<timestamp>/state.md`。初始状态固定为 `current_round: 0`，正常模式 `review_started: false`，`--skip-impl` 模式 `review_started: true` 并直接写入 `.review-phase-started`。`base_commit` 在启动时快照化，避免后续 base branch ref 前移导致 review diff 失真。

注：用户给定的 `tests/test-setup-scripts-robustness.sh` 在 pinned commit `0ec921a36b4365df503511c5567bbd3e02db0df5` 下不存在；同名测试实际位于 `tests/robustness/test-setup-scripts-robustness.sh`，以下测试证据引用该路径。

**Algorithm Subset Covered**

覆盖范围限于：

- setup 输入解析与默认状态变量。
- 启动门禁：依赖、active loop 互斥、agent teams 环境、plan 路径与内容、git 仓库、工作区洁净、base branch。
- 状态初始化：loop 目录、plan backup/placeholder、BitLesson 初始化、`state.md` frontmatter、pending session id signal、skip-impl review marker。
- Round 0 初始工件：`goal-tracker.md`、`round-0-summary.md`、`round-0-contract.md`、`round-0-prompt.md`。
- `loop-common.sh` 中与 state 字段、active loop 发现、state 解析严格性相关的共享机制。
- 健壮性测试中直接验证 setup 初始化门禁和 skip-impl 初态的用例。

不覆盖实际 Codex review 执行、stop hook 的后续轮次推进、finalize/methodology analysis 的完整算法。

**Pseudocode**

```text
input:
  PLAN_FILE? positional
  --plan-file?
  --max N default 42
  --codex-model MODEL[:EFFORT] default from loop-common
  --codex-timeout SEC default 5400
  --push-every-round default false
  --base-branch BRANCH?
  --full-review-round N default 5
  --skip-impl default false
  --claude-answer-codex / --yolo => ask_codex_question=false
  --agent-teams default config false
  --privacy default false
  bitlesson policy flags

initialize defaults:
  current_round := 0
  review_started := skip_impl
  mainline_stall_count := 0
  last_mainline_verdict := unknown
  drift_status := normal

parse args:
  reject unknown option
  reject duplicate plan sources
  validate numeric args by regex ^[0-9]+$
  validate full_review_round >= 2
  parse codex_model into model and effort

gate sequence:
  project_root := resolve_project_root() else fail
  require codex, jq, git else fail with all missing deps
  if find_active_loop(.humanize/rlcr) != empty: fail
  if agent_teams=true and env CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS != 1: fail

  if no plan:
    if skip_impl:
      PLAN_FILE := .humanize/skip-impl-placeholder.md
      skip_impl_no_plan := true
      force track_plan_file=false
    else fail

  require git repo and at least one commit

  if not skip_impl_no_plan:
    reject absolute path
    reject whitespace path
    reject shell metacharacters
    reject file symlink
    reject symlink parent segments
    require file exists/readable/inside project/not submodule
    compute plan_is_tracked
    if track_plan_file=true:
      require tracked and clean
    else:
      require not tracked
    require line_count >= 5
    require content_lines >= 3 ignoring blanks, # comments, HTML comments

  start_branch := git rev-parse --abbrev-ref HEAD
  reject YAML-unsafe start_branch
  reject invalid codex_model chars
  require codex_effort in {xhigh, high, medium, low}

  require working tree clean except untracked .humanize[-/]* runtime dirs

  base_branch:
    if user supplied:
      require local branch; remote-only is error
    else:
      try remote HEAD if local exists
      else local main
      else local master
      else fail
  reject YAML-unsafe base_branch
  base_commit := git rev-parse base_branch

transition INIT -> ACTIVE:
  loop_dir := .humanize/rlcr/<timestamp>
  mkdir loop_dir
  if skip_impl_no_plan:
    write loop_dir/plan.md placeholder
    PLAN_FILE := .humanize/rlcr/<timestamp>/plan.md
  else:
    copy plan to loop_dir/plan.md

  initialize .humanize/bitlesson.md
  write loop_dir/state.md frontmatter
  write .humanize/.pending-session-id = (state path, setup script path)
  if skip_impl:
    write loop_dir/.review-phase-started with build_finish_round=0

  write goal-tracker:
    if skip_impl and plan anchored:
      extract goal/ac from plan, fallback scoped defaults
    else if skip_impl without plan:
      review-only goal/ac, no "[To be]" placeholders
    else:
      normal goal tracker with immutable/mutable sections

  write round-0-summary scaffold with BitLesson Delta defaults
  write round-0-contract for skip_impl, otherwise prompt requires Claude to create it
  write round-0-prompt:
    normal mode: implementation plan + routing rules + BitLesson + goal tracker rules
    skip_impl: code review only + contract references

output activation message and prompt
```

**Transition Table**

| State | Gate / Input | Transition | Initialized Variables / Files | Failure Mode |
|---|---|---|---|---|
| `START` | defaults loaded | `ARGS_PARSED` | `MAX_ITERATIONS=42`, `FULL_REVIEW_ROUND=5`, `CODEX_TIMEOUT=5400`, booleans false/true defaults | invalid option/argument exits |
| `ARGS_PARSED` | project root + deps + active loop check | `PRECHECK_OK` | none | missing `codex/jq/git`, active loop, missing project root |
| `PRECHECK_OK` | plan resolution | `PLAN_RESOLVED` | real `PLAN_FILE`, or skip placeholder | no plan without `--skip-impl`, duplicate plan source |
| `PLAN_RESOLVED` | git + plan + content + tracking validation | `PLAN_VALID` | `FULL_PLAN_PATH`, `PLAN_IS_TRACKED`, `LINE_COUNT` | bad path, symlink, tracked/untracked policy mismatch, too-simple plan |
| `PLAN_VALID` | branch/model/worktree/base branch checks | `GIT_CONTEXT_VALID` | `START_BRANCH`, `BASE_BRANCH`, `BASE_COMMIT` | YAML-unsafe branch, dirty tree, no local base branch |
| `GIT_CONTEXT_VALID` | mkdir/copy/init | `LOOP_ACTIVE` | `state.md`, `plan.md`, pending session signal | filesystem write failure in real execution |
| `LOOP_ACTIVE` normal | `SKIP_IMPL=false` | implementation phase starts | `review_started=false`, BitLesson required true, prompt includes plan and task routing | later stop hook governs progression |
| `LOOP_ACTIVE` skip | `SKIP_IMPL=true` | review phase starts immediately | `review_started=true`, `.review-phase-started`, `build_finish_round=0`, BitLesson required false | review-only workflow depends on existing branch diff |

**Source Evidence**

- 默认参数与输入状态：`PLAN_FILE`、`TRACK_PLAN_FILE`、`MAX_ITERATIONS`、Codex model/effort/timeout、`PUSH_EVERY_ROUND`、`FULL_REVIEW_ROUND`、`SKIP_IMPL`、`ASK_CODEX_QUESTION`、`AGENT_TEAMS`、`PRIVACY_MODE` 在 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:39) 初始化；默认常量如 `DEFAULT_CODEX_TIMEOUT=5400`、`DEFAULT_MAX_ITERATIONS=42`、`DEFAULT_FULL_REVIEW_ROUND=5` 在 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:18)。

- 参数解析门禁：`--max` 要求参数且匹配 `^[0-9]+$`，否则退出，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:193)；`--codex-timeout` 同样只校验数字字符串，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:220)；`--full-review-round` 要求数字且至少 2，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:256)；`--skip-impl` 将 `SKIP_IMPL=true`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:272)。

- 依赖门禁：启动前收集缺失的 `codex`、`jq`、`git`，一次性报错退出，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:340) 和 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:354)。测试覆盖缺失 `codex`、缺失 `jq`、多个依赖一起报错、依赖齐全继续，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:1059)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:1088)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:1118)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:1160)。

- active loop 互斥：setup 调用 `find_active_loop "$PROJECT_ROOT/.humanize/rlcr"`，非空即拒绝启动，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:369)。测试用 fake `.humanize/rlcr/.../state.md` 验证 “already active” 阻断，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:502)。

- active loop 发现规则：无 session filter 时只检查最新目录，若有 active state 文件才返回，以避免旧 zombie loop 被复活，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:308) 和 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:342)。active state 优先级是 `methodology-analysis-state.md`、`finalize-state.md`、`state.md`，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:264)。

- skip-impl plan 可选：无 plan 且 `--skip-impl` 时使用内部 placeholder、标记 `SKIP_IMPL_NO_PLAN=true`，并忽略 `--track-plan-file`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:408)。测试验证 `--skip-impl` 无 plan 不因 “No plan file provided” 失败，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:869)。

- plan 路径安全门禁：拒绝绝对路径、空白路径、shell metacharacters，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:455)、[scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:461)、[scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:469)。对应测试见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:286)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:309)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:329)。

- symlink 与路径穿越防护：拒绝 plan 文件本身 symlink、父目录 symlink、非项目内 resolved path，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:481)、[scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:494)、[scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:529)。测试覆盖文件 symlink 和父目录 symlink，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:540)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:567)。

- plan tracking 策略：`--track-plan-file` 要求 plan 已 tracked 且 clean；否则 plan 必须不 tracked，即 gitignored runtime input，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:562) 到 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:607)。测试覆盖 tracked plan 未加 flag 被拒绝，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:473)。

- plan 内容门禁：至少 5 行，且忽略空白、`#` 注释和 HTML 注释后至少 3 条 content lines，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:618) 和 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:628)。测试覆盖短 plan 和纯注释 plan，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:230)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:260)。

- branch/model/worktree 门禁：`START_BRANCH` 从 git 读取且拒绝 YAML-unsafe 字符，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:686)；Codex model 只允许 `[a-zA-Z0-9._-]+`，effort 限定 `xhigh|high|medium|low`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:702)；工作区必须 clean，但过滤 `.humanize[-/]` runtime untracked 目录，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:723)。测试覆盖 YAML-unsafe branch、非法 model、`.humanizeconfig` 仍视为 dirty，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:357)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:388)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:431)。

- base branch 选择与快照：显式 `--base-branch` 必须是本地分支；自动选择优先级是 remote default 本地存在、`main`、`master`；之后捕获 `BASE_COMMIT=git rev-parse "$BASE_BRANCH"`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:743) 和 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:807)。

- state schema 字段：共享库定义 `plan_tracked`、`start_branch`、`base_branch`、`base_commit`、`plan_file`、`current_round`、`max_iterations`、`push_every_round`、Codex 配置、`review_started`、`full_review_round`、`ask_codex_question`、`session_id`、`agent_teams`、`privacy_mode`、mainline stall/drift 字段，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:24)。

- `state.md` 初始化：写入 `current_round: 0`、`max_iterations`、Codex 参数、push/full-review、plan/start/base/base_commit、`review_started`、question policy、session、agent/privacy、BitLesson、stall/drift、`started_at`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:880)。`INITIAL_REVIEW_STARTED="$SKIP_IMPL"`，BitLesson enforcement 在 skip-impl 下关闭，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:872)。

- session id 后绑定：setup 写 `.humanize/.pending-session-id`，内容为 state 文件路径和 setup 脚本签名，PostToolUse hook 后续消费并 patch `session_id`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:909)。

- skip-impl review phase marker：`--skip-impl` 写 `.review-phase-started`，内容 `build_finish_round=0`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:920)。测试验证 marker 和 `review_started: true`，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:885)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:916)。

- Round 0 工件：skip-impl 有无 plan 分别生成 anchored/review-only `goal-tracker.md`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:929) 和 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1002)；正常模式生成带 IMMUTABLE/MUTABLE section 的 tracker，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1060)。summary scaffold 在模式分支前创建，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1195)。skip-impl contract/prompt 创建并引用 round contract，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1202) 和 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1225)。测试覆盖 skip-impl tracker 无 placeholder、summary scaffold、round contract、prompt 引用、plan anchor，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:929)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:943)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:959)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:972)、[tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:1015)。

- routing/scoring rules seeded into prompt：正常 prompt 要求任务 lane tag 为 `[mainline]`、`[blocking]`、`[queued]`，并要求 routing tag `coding|analyze`，`coding` 由 Claude 执行，`analyze` 走 `/humanize:ask-codex`，无 tag 默认 `coding`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1324) 和 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1335)。输出消息声明后续正常模式以 Codex `COMPLETE` 进入 review phase，review 以 `[P0-9]` issues 判定，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1493)；skip-impl 输出声明直接 run code review 并用 `[P0-9]` findings 作为修复循环，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:1451)。

- state 解析不变量：宽松 parser 为可选字段补默认值，但明确不 default `review_started`，以便后续 schema validation 能发现缺失，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:494)。严格 parser 要求 YAML frontmatter、`current_round`、`max_iterations`、`review_started`、`base_branch`，并验证 numeric/boolean，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:533)。

**Edge Cases and Risks**

- `--codex-timeout 0` 被接受。源码用 `^[0-9]+$`，测试明确记录 0 是当前行为，见 [tests/robustness/test-setup-scripts-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-setup-scripts-robustness.sh:657)。风险是后续 timeout wrapper 对 0 的语义可能是立即超时或无限制，取决于实现，不在本子集确认。

- `--max 0` 理论上也会通过 regex，因为 `--max` 只要求数字字符串，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:198)。这与报错文本 “positive integer” 不完全一致；本测试只覆盖非数字和负数路径。

- `session_id` 初始为空，依赖 PostToolUse hook 之后 patch。setup 本身只写 pending signal，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:909)。若 hook 未运行或信号未消费，active loop 的 session 隔离会退化为 backward-compatible empty-session 匹配，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:381)。

- active loop 无 session filter 时只看最新目录。这个设计防 zombie loop，但如果最新目录损坏且旧目录仍 active，setup 可能不把旧目录当 active；这是源码注释明确的 tradeoff，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:310)。

- base branch 必须本地存在。远端存在但本地不存在会失败并要求 fetch，本地 main/master 不存在也会失败，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:748)。这是为了 `codex review --base` 使用 local ref。

- plan 文件默认必须 gitignored；tracked plan 只有显式 `--track-plan-file` 且 clean 才允许。这能避免 plan 被实现提交混入，但会让已纳入版本管理的计划文件在默认路径失败，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:582)。

- skip-impl 无 plan 会创建 placeholder 并把 `PLAN_FILE` 改为 `.humanize/rlcr/<timestamp>/plan.md`，见 [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:829)。这使 review-only 模式可启动，但 scope anchor 退化为通用 contract；有 plan 的 skip-impl 会保留 plan goal/ac anchor。

**What Is Explicitly Out Of Scope**

- 不分析 `rlcr-stop-gate.sh` 的后续 stop/review/finalize 执行逻辑。
- 不分析 Codex CLI 调用细节、review prompt 模板完整语义、`[P0-9]` issue 提取实现的完整路径。
- 不分析安装、营销、截图、用户文档中不定义行为的文本。
- 不运行测试、不修改文件、不提交。
- 不做网络搜索。
- 不把缺失的 `tests/test-setup-scripts-robustness.sh` 当作存在；只引用 pinned commit 中实际存在的 `tests/robustness/test-setup-scripts-robustness.sh`。