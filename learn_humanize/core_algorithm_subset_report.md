# Humanize 核心算法 Subset 研究报告

研究日期: 2026-06-19

研究对象: `PolyArch/humanize`

研究 commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`

研究方法: 30 路并行 `tmux` + `codex exec -m gpt-5.5 -c model_reasoning_effort=xhigh`，对源码做只读研究；主会话再综合源码行号和 30 份 agent 输出。

## 结论

Humanize 的核心不是传统意义上的数值算法、排序模型或机器学习训练算法。它的核心算法是一个面向 AI 编程流程的多阶段状态机，核心目标是把“实现、审查、修复、再审查、收尾”变成可审计、可阻断、可恢复的闭环。

可以把它抽象为:

```text
Plan / Draft
  -> gen-plan convergence
  -> setup RLCR state
  -> implementation rounds
  -> Codex summary review
  -> code review phase
  -> finalize phase
  -> terminal state
```

这个状态机围绕 `.humanize/rlcr/<timestamp>/` 下的文件运转，主要状态由 `state.md`、`finalize-state.md`、`methodology-analysis-state.md`、`complete-state.md`、`stop-state.md`、`maxiter-state.md`、`cancel-state.md` 等文件表示。Claude/Codex 不是自由运行，而是被 Stop hook、validators、git gates、BitLesson gates、round contract、Goal Tracker、background-task guards 和 Codex review markers 共同约束。

## 30 路研究执行证据

运行目录: `research_runs/2026-06-19_humanize_core_algorithms`

关键证据文件:

- `run_manifest.env`: 记录 source commit、模型、reasoning effort、tmux session、超时。
- `topics.tsv`: 30 个研究 topic 和 focus paths。
- `status/*.status`: 30 个 agent 均为 `complete`。
- `agents/agent_*/metadata.env`: 每个 agent 的启动/完成时间、topic、codex 路径、exit code。
- `agents/agent_*/output.md`: 每个 topic 的原始研究结论。

本次 run 的 manifest:

```text
source_commit=0ec921a36b4365df503511c5567bbd3e02db0df5
tmux_session=humanize_core_20260619
model=gpt-5.5
reasoning_effort=xhigh
timeout_seconds=7200
```

30 个 topic 覆盖:

1. Core workflow taxonomy
2. RLCR setup state initialization
3. Stop-hook state machine
4. Implementation-phase prompt and summary contract
5. Full-alignment review cadence and drift detection
6. Code-review phase and severity gate
7. Finalize and methodology-analysis phases
8. Loop-common parsing and active-loop selection
9. Background task short-circuit algorithm
10. Bash validator command safety rules
11. Edit/write/read validator protected surfaces
12. Plan-file validator and plan integrity hooks
13. Todo transcript checker
14. Config merge algorithm
15. Model router and task-tag routing
16. ask-codex execution wrapper
17. ask-gemini execution wrapper
18. Gen-plan convergence algorithm
19. Refine-plan comment extraction and validation
20. Gen-idea multi-candidate ideation
21. Agent Teams parallelization prompt
22. BitLesson selector routing
23. BitLesson delta validation algorithm
24. Monitor runtime status model
25. Skill monitor and telemetry parsing
26. Cancel and cleanup semantics
27. Git branch, cleanliness, and push gates
28. Path validation and injection resistance
29. Test suite as executable algorithm spec
30. Core subset synthesis and skip list

## 核心算法 Subset

### 1. Plan 生成与收敛算法

相关文件:

- `commands/gen-plan.md`
- `prompt-template/plan/gen-plan-template.md`
- `scripts/validate-gen-plan-io.sh`
- `commands/start-rlcr-loop.md`

核心机制:

- 输入可以是 loose draft 或已有 markdown draft。
- `gen-plan` 先验证输入输出路径和 draft relevance。
- 在 discussion mode 下，Claude 先根据 draft 和 Codex first-pass critique 生成 candidate plan。
- 然后最多运行 3 轮 Claude/Codex convergence:
  - Codex critique assumptions、missing requirements、alternative directions。
  - Claude 修订 plan。
  - 维护 disagreement / issue matrix。
  - 无 required changes、高影响 disagreement 消失，或连续两轮无实质变化后收敛。
- direct mode 跳过 convergence，强制标记为 `partially_converged`，并要求 human review。
- auto-start RLCR 只有在 discussion mode、converged、无 pending user decisions 时允许。

伪代码:

```text
gen_plan(draft):
  load config
  validate IO
  reject irrelevant draft

  codex_first_pass = ask_codex(draft)
  candidate = claude_generate_plan(draft, codex_first_pass)

  if mode == direct:
    convergence_status = partially_converged
    human_review_required = true
  else:
    for round in 1..3:
      codex_review = ask_codex(candidate)
      candidate = claude_revise(candidate, codex_review)
      update convergence matrix
      if no required changes and no high-impact disagreements:
        convergence_status = converged
        break

  collect pending decisions
  write final plan

  if auto_start and converged and no pending:
    start_rlcr_loop(plan, --skip-quiz)
```

关键结论: Plan 阶段的算法价值在于“收敛 gate”，而不是生成文本本身。它试图把后续 RLCR 的输入从一个模糊想法提高到可执行 checklist、AC、边界、routing tag。

### 2. RLCR 初始化状态机

相关文件:

- `scripts/setup-rlcr-loop.sh`
- `hooks/lib/loop-common.sh`
- `tests/robustness/test-setup-scripts-robustness.sh`

核心机制:

- 参数默认值:
  - `max_iterations=42`
  - `codex_timeout=5400`
  - `full_review_round=5`
  - Codex default 从 config 或 fallback 读取。
- 启动前 gate:
  - 依赖必须存在: `codex`、`jq`、`git`。
  - 不能已有 active loop。
  - plan 路径必须安全: 相对路径、无空格、无 shell metacharacters、非 symlink、在项目内。
  - plan 内容必须至少 5 行，且至少 3 条非空非注释内容。
  - git repo 必须存在且有 commit。
  - working tree 必须 clean，排除未跟踪 `.humanize/` runtime。
  - base branch 必须可解析，并在启动时捕获 `base_commit`。
- 初始化输出:
  - `.humanize/rlcr/<timestamp>/state.md`
  - `goal-tracker.md`
  - `round-0-summary.md`
  - `round-0-contract.md` 或 contract 要求
  - `round-0-prompt.md`
  - `.review-phase-started` 仅在 `--skip-impl` 时提前创建。

状态初始化伪代码:

```text
setup_rlcr(args):
  parse args
  require codex, jq, git
  reject active loop
  resolve plan or skip-impl placeholder
  validate git repository
  validate plan path/content/tracking
  validate branch/model/effort
  require clean worktree
  resolve base_branch
  base_commit = rev_parse(base_branch)

  loop_dir = .humanize/rlcr/<timestamp>
  write state.md:
    current_round = 0
    review_started = skip_impl
    base_branch = resolved
    base_commit = captured SHA
    mainline_stall_count = 0
    last_mainline_verdict = unknown
    drift_status = normal

  write initial tracker, summary scaffold, prompt
```

关键结论: `base_commit` 快照是重要设计点。它避免在 `main` 上工作时 base branch ref 随提交前移，导致 `codex review --base main` 自比较为空。

### 3. Stop Hook 主状态机

相关文件:

- `hooks/loop-codex-stop-hook.sh`
- `scripts/rlcr-stop-gate.sh`
- `hooks/lib/loop-common.sh`
- `tests/test-stop-gate.sh`

Stop hook 是 Humanize 的核心调度器。它在 Claude 尝试退出时运行，决定:

- 允许退出。
- 阻断退出并返回下一步 prompt。
- 更新 round。
- 进入 review phase。
- 进入 finalize。
- 进入 terminal state。

主要输入:

- hook JSON: `session_id`、`transcript_path`、`cwd` 等。
- active loop dir。
- state frontmatter。
- round summary。
- goal tracker。
- git status。
- Codex review result。

主流程伪代码:

```text
stop_hook(input):
  loop = find_active_loop(session_id, allow_bg_marker_fallback=true)
  if loop is empty:
    allow_exit()

  handle_background_task_short_circuit()

  state_file = resolve_active_state_file(loop)
  parse and validate state

  validate branch consistency
  validate plan integrity if implementation phase
  validate todos/tasks complete
  validate git status and large file gates
  validate clean worktree and push policy
  require summary file
  require round contract if anti-drift active
  validate BitLesson Delta if required
  validate goal tracker initialization in round 0

  if finalize phase:
    rename finalize-state.md -> complete-state.md
    allow_exit()

  if implementation phase:
    run codex exec against summary review prompt
    require non-empty review result
    parse last non-empty line
    require Mainline Progress Verdict unless STOP
    update drift counters

    if last_line == COMPLETE:
      set review_started=true
      create .review-phase-started
      run codex review
    elif last_line == STOP:
      end stop state
    else:
      current_round += 1
      write next prompt from Codex feedback
      block_exit()

  if review phase:
    require .review-phase-started
    run codex review --base base_commit_or_branch
    if [P0-9] issues:
      write review-fix prompt
      block_exit()
    else:
      rename state.md -> finalize-state.md
      block_exit_with_finalize_prompt()
```

关键结论: Humanize 的“循环”不是 agent 自觉遵守，而是 Stop hook 把退出变成一次 state transition。没有合格 summary、git clean、plan/tracker/contract 等证据，就不能进入下一阶段。

### 4. Implementation Phase Summary Review

相关文件:

- `prompt-template/codex/regular-review.md`
- `prompt-template/codex/full-alignment-review.md`
- `hooks/loop-codex-stop-hook.sh`
- `prompt-template/claude/next-round-prompt.md`

核心机制:

- 每轮 Claude 必须写 `round-N-summary.md`。
- Stop hook 构造 Codex review prompt。
- 普通轮使用 regular review。
- 每 `full_review_round` 的 `N-1, 2N-1, 3N-1...` 轮使用 full alignment review。
- Codex 输出的最后一条非空行必须严格为 `COMPLETE` 或 `STOP` 才触发终止/切换。
- 若未 `COMPLETE`，review 内容会被放入下一轮 prompt。

Full alignment 的算法意义:

- 它不是代码审查，而是目标对齐审查。
- 它读取近期 round summaries 和 review results。
- 它要求判断主线是否 advance / stall / regress。
- 它是 drift detection 的输入。

### 5. Review Phase Severity Gate

相关文件:

- `prompt-template/codex/code-review-phase.md`
- `hooks/lib/loop-common.sh`
- `hooks/loop-codex-stop-hook.sh`
- `tests/test-codex-review-merge.sh`

核心机制:

- Implementation Phase 只有 Codex summary review 输出 `COMPLETE` 后才进入 Review Phase。
- Review Phase 改用 `codex review --base <base_commit_or_branch>`。
- `detect_review_issues()` 只扫描 codex review log 最后 50 行。
- 只有前 10 个字符内出现 `[P0-9]` 的行被判为真实 issue 起点。
- 找到 issue 后，从该行抽取到 log 末尾，写入 `round-N-review-result.md`。
- 未找到 `[P0-9]` 则进入 finalize。

伪代码:

```text
run_code_review(round):
  base = base_commit if present else base_branch
  run codex review --base base
  if command failed:
    block retry

  issues = detect_review_issues(log)
  if issues missing due to empty log:
    block retry
  if issues found:
    write review-fix prompt
    block exit
  else:
    enter finalize phase
```

关键结论: Review Phase 的 gate 是 marker-based，不解析完整语义评分。Humanize 把 Codex review 的输出协议约束为 `[P0-9]` severity marker。

### 6. Mainline Drift Detection

相关文件:

- `hooks/loop-codex-stop-hook.sh`
- `prompt-template/codex/full-alignment-review.md`
- `prompt-template/block/mainline-verdict-missing.md`
- `prompt-template/claude/drift-replan-prompt.md`

核心机制:

- Implementation Phase 的 Codex review 必须包含:

```text
Mainline Progress Verdict: ADVANCED / STALLED / REGRESSED
```

- `ADVANCED` 重置 stall count。
- `STALLED` 或 `REGRESSED` 递增 stall count。
- 连续 2 次触发 `drift_status=replan_required`，下一轮 prompt 切换为 drift recovery。
- 连续 3 次触发 circuit breaker，loop 进入 stop state。
- `COMPLETE` 会重置 drift state。

伪代码:

```text
verdict = extract_mainline_progress_verdict(review)
if verdict == unknown and last_line != STOP:
  block retry

if verdict == ADVANCED:
  stall_count = 0
  drift_status = normal
elif verdict in {STALLED, REGRESSED}:
  stall_count += 1
  if stall_count >= 2:
    drift_status = replan_required
  if stall_count >= 3:
    stop_loop()
```

关键结论: Drift detection 是 Humanize 防止“看起来在忙但主线没推进”的核心算法之一。

### 7. Round Contract 与 Goal Tracker

相关文件:

- `prompt-template/claude/next-round-prompt.md`
- `prompt-template/block/round-contract-missing.md`
- `scripts/setup-rlcr-loop.sh`
- `hooks/loop-edit-validator.sh`

Round contract 的不变量:

- 每轮 exactly one mainline objective。
- 每轮只选 1-2 个 target AC。
- 必须区分:
  - `mainline`
  - `blocking`
  - `queued`
- queued side issues 要记录，但不得替代本轮 mainline objective。
- contract 不存在时禁止开始实现。

Goal Tracker 的不变量:

- immutable section: Ultimate Goal、Acceptance Criteria。
- mutable section: Active Tasks、Completed Items、Deferred Items、Plan Evolution。
- Round 0 后 immutable section 不应被修改。
- tracker drift 会由 validators 和 Codex review 共同抑制。

关键结论: Round contract + Goal Tracker 是 Humanize 的 scope-control algorithm。它们让 Codex feedback 不会无限扩大当前轮工作范围。

### 8. Background Task Short-Circuit / Parking

相关文件:

- `hooks/lib/loop-bg-tasks.sh`
- `hooks/loop-codex-stop-hook.sh`
- `tests/test-stop-hook-bg-allow.sh`

核心机制:

- Stop hook 会读取 Claude transcript。
- 如果存在未完成 background Task 或 Bash，hook 不进入 Codex review。
- 它返回 allow/short-circuit message，并写 `bg-pending.marker`。
- 同 session 背景任务完成后，下次 stop 可清理 stale marker。
- 跨 session 看到 marker 时，不接管别人的 parked loop。
- transcript 缺失、不可读、malformed 时 fail-closed，保留 marker 和 session id。
- 支持旧版 queue-operation XML 和新版 task notification completion events。

伪代码:

```text
pending = list_pending_background_task_ids(transcript, since_loop_start)
pending -= completed_task_ids
pending = liveness_filter(pending)

if pending not empty:
  write bg-pending.marker
  allow stop without Codex review

if marker exists and same session and transcript parse succeeds and no pending:
  remove marker

if marker exists and foreign session:
  allow stop, preserve marker/state
```

关键结论: 这是并发安全 gate。它避免主 agent 在子任务仍运行时提前触发 Codex review 或推进状态。

### 9. Validators 和保护面

相关文件:

- `hooks/loop-bash-validator.sh`
- `hooks/loop-edit-validator.sh`
- `hooks/loop-write-validator.sh`
- `hooks/loop-read-validator.sh`
- `hooks/loop-plan-file-validator.sh`
- `hooks/check-todos-from-transcript.py`

核心机制:

- Bash validator 阻断危险命令、Git state 操作、直接写受保护 loop 文件、绕过 summary/write flow。
- Edit/write validators 阻断对 `state.md`、`finalize-state.md`、prompt files、round contract、protected goal tracker immutable section 的错误修改。
- Plan-file validator 确保 plan 在 implementation phase 不被漂移修改。
- Todo checker 从 transcript 判断任务是否未完成，未完成则 block。

关键结论: Validators 是 Stop hook 之外的“前置防线”。Stop hook 是阶段转移 gate，validators 是操作面 gate。

### 10. Git Gate

相关文件:

- `hooks/loop-codex-stop-hook.sh`
- `prompt-template/block/git-not-clean.md`
- `prompt-template/block/unpushed-commits.md`
- `tests/robustness/test-git-operations-robustness.sh`

核心机制:

- 当前分支必须等于 loop 启动分支。
- `git status --porcelain` 失败或超时 fail-closed。
- 工作区必须 clean。
- 未跟踪 `.humanize/` runtime 可以被排除。
- tracked `.humanize` state 不允许。
- `--push-every-round` 时，如果 branch ahead，必须 push 后才能退出。
- dirty block 模板禁止 `git add -A`、`git add --all`、`git add .`，避免把 runtime artifacts 一起提交。

关键结论: Git gate 确保每轮输出有真实 commit 边界，避免未提交代码被 Codex summary review 当作完成。

### 11. BitLesson 记忆选择与 Delta Gate

相关文件:

- `scripts/bitlesson-select.sh`
- `scripts/bitlesson-validate-delta.sh`
- `agents/bitlesson-selector.md`
- `docs/bitlesson.md`

BitLesson selector:

- 根据 config 选择 provider。
- `gpt-*` / `o*` 走 Codex。
- `claude-*` / `haiku|sonnet|opus` 走 Claude。
- `xhigh` 对 Claude 映射为 `high`。
- provider binary 缺失时可 fallback 到 Codex。

BitLesson delta validator:

- 在 summary 中定位 `## BitLesson Delta`。
- 解析时忽略 fenced code block 和 HTML comments。
- `Action` 必须是 `none|add|update` 且唯一。
- `Action: none` 要求 Lesson IDs 为 `NONE` 或空。
- `Action: add|update` 要求具体 Lesson ID 和非 placeholder notes。
- 具体 Lesson ID 必须存在于 `.humanize/bitlesson.md`。

伪代码:

```text
delta = extract_section(summary, "## BitLesson Delta",
                        ignoring fences and html comments)
action = parse_single_action(delta)
ids = parse_lesson_ids(delta)
notes = parse_notes(delta)

if action == none:
  require ids empty or NONE
  if knowledge base empty and policy disallows empty none:
    block
else:
  require concrete ids
  require notes non-empty and not placeholder
  require bitlesson file exists
  require ids are valid and present
```

关键结论: BitLesson 是项目记忆更新 gate。它不只是文档，而是把“本轮学到的 reusable lesson 是否被记录”纳入 loop exit 条件。

### 12. Config Merge 与 Model Router

相关文件:

- `scripts/lib/config-loader.sh`
- `scripts/lib/model-router.sh`
- `config/default_config.json`

Config merge:

- 层级顺序:
  1. empty object
  2. default config
  3. user config
  4. project config
- 每层必须是 JSON object。
- required default config malformed 是 fatal。
- optional user/project malformed 会 warning 并忽略。
- merge 前递归 strip nulls。
- 后层覆盖前层。

Model router:

- `gpt-*` 或 `o[0-9]*` -> Codex provider。
- `claude-*`、`haiku`、`sonnet`、`opus` -> Claude provider。
- effort 只允许 `xhigh|high|medium|low`。
- Claude 不支持 `xhigh` 时映射为 `high`。

关键结论: 配置层决定默认模型、BitLesson provider、agent teams 等行为，是状态机参数化入口。

### 13. ask-codex / ask-gemini Wrappers

相关文件:

- `scripts/ask-codex.sh`
- `skills/ask-codex/SKILL.md`
- `scripts/ask-gemini.sh`
- `skills/ask-gemini/SKILL.md`

ask-codex:

- 一次性 Codex consultation，不进入 RLCR 状态机。
- 参数解析支持 `--codex-model MODEL:EFFORT` 和 timeout。
- 保存 input/output/metadata 到 `.humanize/skill/<unique-id>/`。
- cache 调试命令和 stdout/stderr 到 `~/.cache/humanize/...`。
- 支持 sandbox bypass env，但默认 full-auto。

ask-gemini:

- 用于 deep web / external research。
- 与 RLCR 不同，是外部咨询 wrapper。

关键结论: 它们是辅助算法工具，不是主循环本身。`analyze` task tag 会路由到 ask-codex。

### 14. Agent Teams 并行模式

相关文件:

- `prompt-template/claude/agent-teams-core.md`
- `prompt-template/claude/agent-teams-instructions.md`
- `prompt-template/claude/agent-teams-continue.md`
- `agents/plan-compliance-checker.md`
- `agents/draft-relevance-checker.md`

核心机制:

- Claude 作为 team leader。
- coding tasks 可拆给 agents。
- team leader 不应自己写代码。
- 仍受主 RLCR loop 的 Stop hook、summary、git、review gates 约束。
- Agent Teams 只是 implementation execution 并行化，不替代 Codex review gate。

关键结论: Agent Teams 是并行执行策略，不是 completion 判断策略。

### 15. Finalize 与 Methodology Analysis

相关文件:

- `prompt-template/claude/finalize-phase-prompt.md`
- `prompt-template/claude/finalize-phase-skipped-prompt.md`
- `hooks/lib/methodology-analysis.sh`
- `tests/test-finalize-phase.sh`

Finalize Phase:

- 只有 Review Phase 无 `[P0-9]` issue 后进入。
- `state.md` rename 为 `finalize-state.md`。
- 不再运行 Codex review。
- 要求 `finalize-summary.md`。
- 允许功能等价简化/重构。
- 不得改功能、不得引入 bug、不得破坏测试。
- 所有检查通过后 rename 为 `complete-state.md`。

Methodology Analysis:

- 在 stop/maxiter 等终止路径前可进入分析状态。
- 它用于总结方法论，不是实现主循环。

关键结论: Finalize 是“代码已通过 review 后的清理阶段”，不是继续实现新功能的阶段。

## 可明确跳过的非核心内容

以下内容在本次研究中不作为核心算法:

- 安装说明和 marketplace 命令。
- README 截图和 monitor dashboard 图片。
- 普通 CLI usage 示例，除非定义状态机行为。
- 文案、营销性描述、quick start 截图。
- Kimi/Claude/Codex 安装细节。
- Monitor UI 展示层。
- 单纯模板文本，除非它定义 gate、状态转移或输出协议。
- 测试 fixture 中不影响算法行为的 mock plumbing。

## 风险与设计边界

1. Completion 依赖输出协议。

Implementation Phase 依赖 Codex review 的最后非空行严格等于 `COMPLETE` 或 `STOP`。Review Phase 依赖 `[P0-9]` marker。协议简单可审计，但如果 reviewer 没有按协议输出，需要 hard block 或可能漏判。

1. Review issue detection 是启发式。

`detect_review_issues()` 扫描 review log 最后 50 行，并要求 `[P0-9]` 出现在前 10 个字符内。这降低 false positive，但也意味着 marker 位置异常会被忽略。

1. Git clean gate 强但不是 remote sync gate。

当前算法重视 clean、branch consistency、push-every-round ahead 检测，但没有完整处理 behind/diverged/remote push failure 等所有同步状态。

1. Plan quiz 是 advisory。

用户答错仍可选择继续。它降低误解风险，但不是强制 correctness gate。

1. `--yolo` 降低人工阻力，也降低安全边界。

`--yolo` 跳过 quiz，并让 Claude 直接回答 Codex open questions。适合高信任场景，不适合需求模糊或高风险改动。

1. Agent Teams 并发依赖 background guards。

Background-task short-circuit 避免子任务未完成时推进状态，但 transcript 缺失或格式变化会让算法进入 fail-closed/保守路径。

1. BitLesson 是记忆 gate，不保证 lesson 质量。

Delta validator 能保证格式、一致性、ID 存在，但不能证明 lesson 内容本身高质量。

## 最小核心文件清单

如果只研究 Humanize 核心算法，优先读这些文件:

- `README.md`
- `docs/usage.md`
- `commands/gen-plan.md`
- `commands/start-rlcr-loop.md`
- `scripts/setup-rlcr-loop.sh`
- `hooks/loop-codex-stop-hook.sh`
- `hooks/lib/loop-common.sh`
- `hooks/lib/loop-bg-tasks.sh`
- `hooks/loop-bash-validator.sh`
- `hooks/loop-edit-validator.sh`
- `hooks/loop-write-validator.sh`
- `hooks/loop-read-validator.sh`
- `hooks/loop-plan-file-validator.sh`
- `hooks/check-todos-from-transcript.py`
- `scripts/lib/config-loader.sh`
- `scripts/lib/model-router.sh`
- `scripts/bitlesson-select.sh`
- `scripts/bitlesson-validate-delta.sh`
- `prompt-template/codex/full-alignment-review.md`
- `prompt-template/codex/regular-review.md`
- `prompt-template/codex/code-review-phase.md`
- `prompt-template/claude/next-round-prompt.md`
- `prompt-template/claude/review-phase-prompt.md`
- `prompt-template/claude/finalize-phase-prompt.md`
- `tests/test-stop-hook-bg-allow.sh`
- `tests/test-finalize-phase.sh`
- `tests/test-codex-review-merge.sh`
- `tests/robustness/test-state-transition-robustness.sh`
- `tests/robustness/test-setup-scripts-robustness.sh`
- `tests/robustness/test-git-operations-robustness.sh`

## 总结

Humanize 的核心算法是“AI 工作流控制系统”，不是单点算法函数。它把 AI 编程拆成多个有证据的状态转移:

- plan 必须收敛或显式人工确认。
- loop 启动必须通过 setup gates。
- 每轮必须写 summary、commit、保持 git clean。
- Codex summary review 决定 implementation 是否完成。
- Codex code review 用 `[P0-9]` markers 决定是否能 finalize。
- drift detection 防止主线停滞。
- background-task guard 防止并发任务未完成就推进。
- validators 保护 state、prompt、plan、summary、goal tracker 等关键文件。
- BitLesson gate 约束项目记忆更新。

这套机制的核心价值在于把 AI 代理的“自然语言协作”压成可执行的协议、文件状态和阻断规则。
