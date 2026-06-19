**Topic and conclusion**

Topic: Implementation-phase prompt and summary contract.

结论: 这组模板定义的是“下一轮实现代理”的执行契约，而不是业务算法。核心机制是一个带门禁的轮次状态机: 先重锚计划和 tracker，生成本轮 contract；再把工作按 `[mainline] / [blocking] / [queued]` 路由；只允许 mainline gaps 和真正 blocking issues 驱动实现；最后通过提交和工作总结完成退出。没有数值评分模型，只有分类路由和硬性门禁。

**Algorithm subset covered**

覆盖文件仅限题目指定 4 个实现阶段契约模板:

- `prompt-template/claude/next-round-prompt.md`
- `prompt-template/claude/next-round-footer.md`
- `prompt-template/claude/goal-tracker-update-request.md`
- `prompt-template/block/work-summary-missing.md`

核心状态变量:

- `PLAN_FILE`: 原始实现计划，定义完整范围和要求。
- `GOAL_TRACKER_FILE`: goal tracker，包含 Ultimate Goal、Acceptance Criteria、Active/Completed/Deferred、blocking/queued side issues、Plan Evolution、side-issue 状态。
- `ROUND_CONTRACT_FILE`: 当前轮契约，必须在实现前写入。
- `REVIEW_CONTENT`: Codex review 输入，作为本轮问题分类来源。
- `BITLESSON_FILE`: 每个 task/sub-task 执行前的 lesson 选择输入。
- task lane tag: `[mainline]`、`[blocking]`、`[queued]`。
- `NEXT_SUMMARY_FILE` / `SUMMARY_FILE`: 退出前必须写入的工作总结目标。

关键不变量:

- 每轮 contract 必须有且仅有一个 mainline objective。
- 每轮只选 1-2 个目标 AC。
- mainline objective 在本轮内保持稳定。
- `[queued]` 事项必须记录，但不得替代本轮 objective。
- 只有 mainline gaps 和真正 blocking side issues 能驱动下一步代码修改。
- goal tracker 的 mutable section 需要更新；Round 0 之后 immutable section 不得修改。
- 未写 summary 不允许退出。

**Pseudocode**

```text
input:
  PLAN_FILE
  GOAL_TRACKER_FILE
  ROUND_CONTRACT_FILE
  BITLESSON_FILE
  REVIEW_CONTENT
  NEXT_SUMMARY_FILE

state:
  plan
  goal_tracker.mutable
  goal_tracker.immutable
  round_contract
  codex_findings
  tasks = []
  summary_written = false

start_next_round:
  assert work_is_not_finished

  read(PLAN_FILE)
  read(GOAL_TRACKER_FILE)
  read(recent_round_summaries_and_reviews)

  round_contract = {
    mainline_objective: exactly_one(),
    target_ACs: one_or_two(),
    blocking_issues: issues_that_block(mainline_objective),
    queued_issues: issues_out_of_scope_for_current_round(),
    success_criteria: concrete()
  }
  write(ROUND_CONTRACT_FILE, round_contract)

  gate:
    if not exists(ROUND_CONTRACT_FILE):
      prohibit_implementation()

classify_review(REVIEW_CONTENT):
  for finding in codex_findings:
    if finding is plan-derived gap directly needed for objective:
      route finding -> mainline gap
    else if finding prevents mainline objective from succeeding safely:
      route finding -> blocking side issue
    else:
      route finding -> queued side issue

create_or_update_task(work_item):
  tag = classify_as_one_of([mainline, blocking, queued])
  assert tag is present

  if tag == queued:
    document(work_item)
    do_not_let_it_replace_round_objective()

  if tag in [mainline, blocking]:
    allow_as_execution_driver()

before_each_task_or_subtask(task):
  read(BITLESSON_FILE)
  selected_lessons = run(bitlesson-selector, task)
  follow(selected_lessons or NONE)

execute_round:
  keep(round_contract.mainline_objective stable)

  for task in tasks:
    before_each_task_or_subtask(task)
    if task.tag == mainline:
      implement(task)
    else if task.tag == blocking and truly_blocks(mainline_objective):
      implement(task)
    else if task.tag == queued:
      document(task)
      continue_mainline()

  update(goal_tracker.mutable)
  assert not modified(goal_tracker.immutable) after Round 0

  if cannot_safely_reconcile_goal_tracker:
    append Goal Tracker Update Request to summary

complete_work:
  if code_simplifier_plugin_installed:
    run(code_simplifier)

  commit_changes_with_descriptive_message()
  write(NEXT_SUMMARY_FILE, work_summary)
  summary_written = true

exit_gate:
  if not summary_written:
    block_exit_with_work_summary_missing()
    require summary containing:
      - implemented work
      - files created/modified
      - tests added/passed
      - remaining items
    retry_exit_only_after_summary()
```

**Transition table**

| Phase | Input | Gate / rule | Output |
|---|---|---|---|
| Round re-anchor | plan, tracker, recent summaries/reviews | 必须先读并写 round contract；contract 不存在不得实现 | `ROUND_CONTRACT_FILE` |
| Contract construction | current round context | exactly one mainline objective；1-2 target ACs；blocking/queued 分离 | 本轮稳定执行边界 |
| Review triage | `REVIEW_CONTENT` | findings 分为 mainline gaps、blocking side issues、queued side issues | 可执行问题队列 |
| Task routing | work item | 每个 task 必须带 `[mainline]`、`[blocking]` 或 `[queued]` | tagged task |
| Execution eligibility | tagged task | 只有 `[mainline]` 和真正 `[blocking]` 能驱动代码修改 | implementation work |
| Queued handling | non-blocking bug/cleanup/follow-up | 必须记录；不得替代 round objective | deferred/queued state |
| Lesson gate | each task/sub-task | 执行前读 bitlesson 并运行 selector | selected lesson IDs 或 `NONE` |
| Tracker maintenance | round progress | mutable section 更新；Round 0 后 immutable section 不变 | reconciled tracker 或 update request |
| Completion | implemented changes | 可选 code-simplifier；必须 commit；必须写 summary | committed work + summary |
| Exit | summary state | 未写 summary 则阻断退出 | retry allowed only after summary |

**Source evidence**

- Round 必须先重锚: 模板要求实现前重读 plan、goal tracker、最近 summaries/reviews，并写入当前 round contract。见 `prompt-template/claude/next-round-prompt.md:12-18`。
- Contract schema: contract 必须包含 exactly one mainline objective、1-2 target ACs、blocking issues、queued out-of-scope issues、concrete success criteria。见 `prompt-template/claude/next-round-prompt.md:20-25`。
- 实现前置门禁: “Do not start implementation until the round contract exists.” 见 `prompt-template/claude/next-round-prompt.md:27`。
- Task lane 三分类: `[mainline]` 是 plan-derived 且直接推进 objective；`[blocking]` 是阻止 objective 安全成功的问题；`[queued]` 是非阻塞 bug、cleanup 或 follow-up。见 `prompt-template/claude/next-round-prompt.md:31-34`。
- Lane 执行规则: `[mainline]` 是本轮主要成功条件；`[blocking]` 只有真正阻塞时允许；`[queued]` 必须记录但不得替代目标；新 bug 不阻塞则 queued 并继续 mainline。见 `prompt-template/claude/next-round-prompt.md:36-40`。
- 每个 task/sub-task 的 lesson gate: 执行前读 `BITLESSON_FILE`，运行 `bitlesson-selector`，遵循 selected lesson IDs 或 `NONE`。见 `prompt-template/claude/next-round-prompt.md:42-45`。
- Codex review 是下一轮输入块: `REVIEW_CONTENT` 被嵌入为 Codex review result。见 `prompt-template/claude/next-round-prompt.md:48-51`。
- Goal tracker 读取语义: 开工前需理解 Ultimate Goal、AC、Active/Completed/Deferred、blocking vs queued、Plan Evolution、side-issue state。见 `prompt-template/claude/next-round-prompt.md:54-61`。
- Goal tracker 更新规则: mutable section 必须保持更新；Round 0 后不得改 immutable section；无法安全 reconcile 时在 summary 中加入 Goal Tracker Update Request。见 `prompt-template/claude/next-round-prompt.md:63-65`。
- Mainline guardrails: mainline objective 必须稳定；queued issues 不得接管本轮；Codex findings 要分类为 mainline gaps、blocking side issues、queued side issues；只有前两类驱动代码修改。见 `prompt-template/claude/next-round-prompt.md:67-75`。
- Exit integrity guard: 不得通过说谎、编辑 loop state files、执行 `cancel-rlcr-loop` 退出。见 `prompt-template/claude/next-round-footer.md:4`。
- Completion contract: 完成后若安装 code-simplifier 则使用；然后提交 descriptive commit；最后写 summary 到 `NEXT_SUMMARY_FILE`。见 `prompt-template/claude/next-round-footer.md:6-9`。
- Goal Tracker Update Request fallback 的格式: summary 中可包含 Requested Changes 和 Justification；Codex 会 review 并 reconcile。见 `prompt-template/claude/goal-tracker-update-request.md:2-17`。
- Summary missing block: 未写 work summary 即退出会被拦截，必须写到 `SUMMARY_FILE`。见 `prompt-template/block/work-summary-missing.md:1-8`。
- Summary 最小字段: what implemented、files created/modified、tests added/passed、remaining items；写完后才可再次尝试退出。见 `prompt-template/block/work-summary-missing.md:10-16`。

**Edge cases and risks**

- Scope hijack: 若把非阻塞 cleanup 或 follow-up 错标为 `[blocking]`，queued issue 会接管本轮，违反 mainline guardrails。
- Contract ambiguity: contract 只允许 exactly one mainline objective；如果写入多个 objective，会破坏后续 blocking 判断，因为“是否阻塞”依赖单一 objective。
- AC 过载: contract 规定 1-2 target ACs；选择过多 AC 会让 round scope 膨胀，并削弱 queued/out-of-scope 边界。
- Tracker drift: 若实现过程中没有更新 mutable goal tracker，下一轮会读取过期的 Active/Completed/Deferred 和 side-issue 状态。
- Immutable mutation: Round 0 后修改 immutable section 是显式违规，可能污染 Ultimate Goal 或原始 AC。
- Unsafe tracker reconciliation: 模板给了 fallback，但如果既不能安全更新 tracker、又没有在 summary 写 Goal Tracker Update Request，Codex 没有结构化输入来修正 tracker。
- Lesson gate omission: 每个 task/sub-task 都要求运行 `bitlesson-selector`；批量 task 容易漏掉 sub-task 级别选择。
- Summary/exit failure: summary 是退出硬门禁；即使实现完成，缺失 summary 也会触发 `Work Summary Missing`，要求补写后重试。
- Commit-before-summary ordering risk: footer要求先 commit 再写 summary；若 summary 本身也需要纳入 commit，模板没有说明。这是契约层的潜在歧义。
- 无数值评分: 该模板没有定义 priority score、severity score 或 tie-breaker；多个 blocking/mainline 项同时存在时，只提供分类规则，不提供排序算法。

**What is explicitly out of scope**

- 安装流程、营销文案、截图、泛用说明: 本次未检查，且不参与该实现阶段契约。
- 业务功能实现细节: 模板只规定 round execution contract，不定义具体产品算法。
- Codex review 的生成算法: 这里只消费 `REVIEW_CONTENT`，不定义 Codex 如何产生 review。
- `bitlesson-selector` 内部选择逻辑: 模板只要求运行并遵循结果，不定义 selector 的评分或匹配算法。
- `goal-tracker.md` 的完整 schema: 本组文件只描述需要读取/更新的语义和 fallback section，不给出完整 tracker 文件格式。
- loop runner 的底层状态机实现: 模板禁止编辑 loop state 或执行 `cancel-rlcr-loop`，但不定义 loop runner 源码行为。
- code-simplifier 插件实现: 这里只定义“若安装则使用”的条件动作，不定义插件逻辑。
- 网络、依赖安装、测试框架策略: 指定文件没有定义这些行为。