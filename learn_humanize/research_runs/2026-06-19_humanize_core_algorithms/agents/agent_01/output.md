**Topic and conclusion**

Topic: Core workflow taxonomy for Humanize RLCR.

Conclusion: Humanize 的核心机制是一个由 `Stop` hook 驱动的两阶段反馈状态机。第一阶段让实现代理按计划工作并写 summary，Codex 对 summary 做完整性/正确性审查；只有严格输出 `COMPLETE` 才进入第二阶段。第二阶段执行 `codex review --base <branch>`，以 `[P0-9]` 严重度标记作为缺陷门禁；无问题后进入 finalize/complete。整个循环由 `.humanize/rlcr/<timestamp>/` 下的状态、prompt、summary、review-result、goal-tracker 文件承载，并通过 hook 强制校验状态、分支、计划完整性、summary、git cleanliness、迭代上限、alignment round、review 输出等条件。

**Algorithm subset covered**

覆盖范围仅限以下行为定义：

- RLCR 两阶段主循环：Implementation Phase 与 Code Review Phase。
- Codex native `Stop` hook 的轮次门禁与状态转移。
- Plan Understanding Quiz 的前置理解检查。
- Goal Tracker 的防漂移约束。
- 路由/门禁规则：`COMPLETE`、`STOP`、`[P0-9]`、Open Questions、base branch 选择、full alignment round。
- 失败模式：setup 失败、summary 缺失、空 review、Codex review failure、未完成 Todo、git 不干净、未 push、超迭代、状态/分支/计划完整性失败。

未覆盖安装、截图、营销描述、普通命令示例、监控 UI、Gemini/one-shot ask-codex 细节。

**Pseudocode**

```text
input:
  plan_file?                 # required unless skip_impl
  max_iterations = 42
  codex_model = CLI/config/default/fallback
  codex_timeout = 5400
  base_branch = user_input > remote_default > main > master
  full_review_round = 5
  flags:
    skip_impl
    track_plan_file
    push_every_round
    claude_answer_codex
    agent_teams
    skip_quiz
    yolo = skip_quiz + claude_answer_codex

state:
  session_dir = .humanize/rlcr/<timestamp>/
  phase ∈ {preflight, implementation, review, finalize, complete, cancelled}
  current_round
  max_iterations
  review_started
  base_branch
  goal_tracker:
    immutable: Ultimate Goal, Acceptance Criteria
    mutable: Active Tasks, Completed Items, Deferred Items, Plan Evolution Log

preflight:
  if not skip_quiz and not auto_started_from_converged_gen_plan:
    independent_agent generates 2 multiple-choice plan questions
    if both correct:
      continue
    else:
      explain actual plan
      user chooses proceed_anyway or stop_and_review
      if stop_and_review: halt

setup:
  run setup-rlcr-loop.sh(arguments)
  if exit_code != 0:
    stop and report error

if skip_impl:
  phase = review
else:
  phase = implementation

while phase not in {complete, cancelled}:
  if current_round > max_iterations:
    auto-stop / max-iteration handling

  read prompt:
    if phase == finalize:
      read finalize prompt
    else:
      read .humanize/rlcr/<timestamp>/round-<N>-prompt.md

  implement required changes
  commit changes
  update goal-tracker.md
  write summary:
    implementation/review normal round -> round-<N>-summary.md
    finalize -> finalize-summary.md

  stop normally
  Stop hook runs

  Stop hook validates:
    state schema: current_round, max_iterations, review_started, base_branch, ...
    branch consistency
    plan-file integrity if track_plan_file
    no incomplete Task/Todo
    git clean before exit
    pushed commits if push_every_round
    summary exists
    max iteration policy
    full alignment check on configured rounds
    strict COMPLETE/STOP markers
    review transition marker
    code-review result markers
    Codex output non-empty and successful
    open questions routing

  if hook blocks:
    follow returned instructions
    current_round += 1
    continue

  if phase == implementation:
    Codex reviews summary
    if Codex output == COMPLETE:
      phase = review
      create/observe .review-phase-started transition guard
    else:
      prompt next round with Codex feedback
      current_round += 1
      continue

  if phase == review:
    run codex review --base <base_branch>
    if output contains [P0-9]:
      prompt fixes
      current_round += 1
      continue
    else:
      phase = finalize

  if phase == finalize:
    write finalize-summary.md
    hook validates finalize state
    phase = complete
```

**Transition table**

| Current state | Event / gate | Next state | Rule |
|---|---:|---|---|
| `preflight` | quiz skipped by `--skip-quiz` or `--yolo` | `setup` | Skip only quiz, or skip quiz plus Claude answers Codex questions. |
| `preflight` | quiz both correct | `setup` | Loop proceeds immediately. |
| `preflight` | quiz missed, user proceeds | `setup` | Quiz is advisory, not hard gate. |
| `preflight` | quiz missed, user stops | halted | User reviews plan instead of starting. |
| `setup` | setup script non-zero | halted/error | Stop and report error. |
| `setup` | `--skip-impl` | `review` | Plan optional in review-only mode. |
| `setup` | normal plan file | `implementation` | Plan-driven implementation loop. |
| `implementation` | summary missing / invalid state / dirty git / etc. | blocked same phase | Stop hook blocks exit and returns instructions. |
| `implementation` | Codex review not `COMPLETE` | next implementation round | Feedback becomes next prompt. |
| `implementation` | strict `COMPLETE` marker | `review` | Enters code review phase. |
| `review` | `codex review` output contains `[P0-9]` | next fix round | Severity markers gate completion. |
| `review` | no issues | `finalize` | Loop completes with finalize phase. |
| `finalize` | finalize summary and state accepted | `complete` | Writes complete state. |
| any active phase | cancel command | cancelled | Cancel loop; force exists for finalize phase. |

**Source evidence**

- RLCR 的定义是 “Ralph-Loop with Codex Review”，核心是 AI 生成代码通过外部 review feedback 迭代细化：`README.md:9-12`。
- README 将核心概念压缩为 “One Build + One Review”：Claude 实现，Codex 独立 review；并说明 loop 持续到 acceptance criteria 满足，Agent Teams 可选并行：`README.md:13-18`。
- README 明确两阶段：Implementation 与 Code Review；issues feed back into implementation until resolved：`README.md:20-27`。
- Usage guide 的算法摘要：Implementation Phase 中 Claude 执行 plan，Codex review summaries until `COMPLETE`；Review Phase 中 `codex review --base <branch>` 用 `[P0-9]` severity markers 做质量检查；循环直到 acceptance criteria met 或 no issues remain：`docs/usage.md:5-12`。
- Plan Understanding Quiz 在 RLCR 开始前运行，用两个多选问题检查对技术实现细节的理解：组件如何变化、架构如何连接；答错时解释计划并让用户选择继续或停止，但它是 advisory，不是硬 gate：`docs/usage.md:16-35`。
- Quiz 跳过规则：`--skip-quiz` 只跳 quiz；`--yolo` 同时跳 quiz 并启用 `--claude-answer-codex`；由 converged `gen-plan` 自动启动的 RLCR 自动跳 quiz：`docs/usage.md:37-41`。
- `start-rlcr-loop` 关键输入和默认值：`--max` 默认 42，Codex review timeout 默认 5400 秒，base branch priority 是 user input > remote default > main > master，full alignment 默认 5 且发生在 N-1、2N-1、3N-1 等轮次：`docs/usage.md:70-100`。
- Humanize skill 进一步规定 Implementation Phase 的内部步骤：AI work plan、写 summary、Codex review summary、发现问题继续、Codex 输出 `COMPLETE` 进入 Review Phase：`skills/humanize/SKILL.md:34-42`。
- Review Phase 规则：`codex review --base <branch>` 检查 code quality，问题用 `[P0-9]` 标记；有问题则 AI 修复并继续，无问题则进入 Finalize Phase；Codex CLI 0.114.0+ 且 hooks enabled 时安装 native `Stop` hook 自动执行 exit gating：`skills/humanize/SKILL.md:43-48`。
- 工作轮次的强制顺序：setup 脚本启动；若 setup 非零则停止并报告；每轮读取 `round-<N>-prompt.md` 或 finalize prompt，实现、commit、写 summary、正常 stop/exit，让 native Stop hook 自动运行；若 hook blocks exit，则按返回指令继续下一轮：`skills/humanize-rlcr/SKILL.md:24-49`。
- Stop-hook enforcement 列出了实际门禁：state/schema validation，包括 `current_round`、`max_iterations`、`review_started`、`base_branch`；branch consistency；plan-file integrity；incomplete Task/Todo blocking；git-clean；push-every-round；summary presence；max iteration；full alignment；strict `COMPLETE`/`STOP`；review-phase transition guard；`[P0-9]` code-review gating；Codex review failure/empty output hard block；open-question handling：`skills/humanize-rlcr/SKILL.md:50-68`。
- Critical rules 禁止手动编辑 `state.md` 或 `finalize-state.md`，禁止绕过 blocked hook 手动宣布完成，禁止用 ad-hoc `codex exec` / `codex review` 替代 hook-managed transitions，并要求以 loop 生成的 prompt/review-result 文件为 source of truth：`skills/humanize-rlcr/SKILL.md:69-75`。
- Goal Tracker 防止 goal drift：immutable section 是 Ultimate Goal 和 Acceptance Criteria，Round 0 设置后不再改变；mutable section 包括 Active Tasks、Completed Items、Deferred Items、Plan Evolution Log：`skills/humanize/SKILL.md:152-158`。
- Goal Tracker 原则：每个 task 映射到具体 AC，plan changes 要记录 justification，deferred tasks 需要 strong justification，每 N 轮执行 full alignment audit：`skills/humanize/SKILL.md:159-165`。
- Summary/goal tracker 是硬性操作规则：退出前必须写 work summary，保持 `goal-tracker.md` 更新，包含 implementation、changed files、tests；禁止通过编辑 state files 或 cancel commands 作弊；写 summary 后正常退出以触发 Stop hook：`skills/humanize/SKILL.md:166-173`。
- 存储状态空间：`.humanize/rlcr/<timestamp>/` 下包含 `state.md`、`goal-tracker.md`、`round-N-summary.md`、`round-N-review-result.md`、`finalize-state.md`、`finalize-summary.md`、`methodology-analysis-*`、`complete-state.md`：`skills/humanize/SKILL.md:180-203`。
- Review-only mode 的输入约束：`path/to/plan.md` unless `--skip-impl`；`--skip-impl` start directly in review path；review phase 固定 `codex review` runs with `gpt-5.5:high`：`skills/humanize-rlcr/SKILL.md:76-98`。

**Edge cases and risks**

- Quiz 不是硬 gate：用户即使答错也能 proceed，因此它降低 plan misunderstanding 风险，但不能防止错误计划被放大。证据见 `docs/usage.md:33-35`。
- `--yolo` 同时跳过 quiz 并允许 Claude 直接回答 Codex Open Questions，减少人工停顿，但增加自动化误判和 goal drift 风险。证据见 `docs/usage.md:39-40`、`docs/usage.md:96-98`。
- `--skip-impl` 允许 plan file optional 并直接进入 review path，因此状态机缺少 implementation-phase 的 AC-driven build context；适合 review-only，不应推断其能验证完整 plan execution。证据见 `docs/usage.md:89-90`、`skills/humanize-rlcr/SKILL.md:82-90`。
- `track_plan_file` 只在 applicable/when tracked 时强制 plan-file integrity；未启用或未跟踪时，计划漂移主要依赖 Goal Tracker 和 review，而不是文件完整性 gate。证据见 `skills/humanize-rlcr/SKILL.md:56`、`skills/humanize/SKILL.md:80-82`。
- Code-review gate 依赖 `[P0-9]` markers；若 review 输出为空或失败会 hard block，但若 review 未标出真实问题，状态机会认为 no issues。证据见 `skills/humanize-rlcr/SKILL.md:65-66`。
- Full Alignment Check 是周期性，不是每轮完整 goal audit；默认发生在第 `N-1, 2N-1, 3N-1...` 轮，默认 N=5。证据见 `docs/usage.md:86-88`。
- `current_round`、`max_iterations`、`review_started`、`base_branch` 等是 hook 校验字段，但具体 schema 和 mutation implementation 不在本文件子集中。证据只到 `skills/humanize-rlcr/SKILL.md:54`。
- 取消命令存在，且 finalize phase 可 force cancel；这会终止正常状态机，属于人为中断路径。证据见 `skills/humanize/SKILL.md:89-95`、`docs/usage.md:325-327`。

**What is explicitly out of scope**

- 安装流程、marketplace、CLI prerequisite、Codex/Kimi/Claude 安装细节。
- README 的截图、monitor dashboard、营销性 “build with confidence” 文案。
- `gen-idea`、Gemini deep web research、monitor 命令的实现。
- `ask-codex` one-shot consultation 的完整算法；这里只将其与 RLCR 区分。
- `refine-plan` 的 comment parser/QA ledger 细节，除非作为 RLCR 前置计划质量流程。
- 具体 shell scripts 的实现细节，例如 `setup-rlcr-loop.sh`、Stop hook 脚本、`cancel-rlcr-loop.sh`，因为本任务 focus paths 不包括 scripts。
- Codex review prompt 内容、实际 scoring rubric、severity `[P0-9]` 的语义分级定义；给定文件只说明 marker gate，没有定义每个 P 级含义。
- 方法论分析文件 `methodology-analysis-*` 的算法；目录结构列出它们，但本子集没有行为定义。