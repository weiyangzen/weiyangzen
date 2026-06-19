## Topic and conclusion

**Topic:** Gen-plan convergence algorithm
**结论:** `gen-plan` 的核心不是数值评分算法，而是一个顺序执行的多门控收敛状态机：先做参数/配置/IO/相关性门控，再由 Codex 做首轮风险分析，Claude 生成候选计划，随后在 `discussion` 模式下用第二个 Codex 进行最多 3 轮“挑战-修订-矩阵评估”。收敛判定基于定性条件：无 `REQUIRED_CHANGES`、无高影响 `DISAGREE`，或连续两轮无实质变化；否则在 3 轮上限后降级为 `partially_converged` 并把 unresolved 项显式带入用户决策区。`direct` 模式明确跳过收敛轮，永远不能满足 auto-start 条件。

## Algorithm subset covered

覆盖文件仅限任务指定的算法相关子集，按 pinned commit `0ec921a36b4365df503511c5567bbd3e02db0df5` 读取：

- [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:18): 命令状态机、执行模式、收敛循环、人工审查门、最终写入/auto-start 条件。
- [prompt-template/plan/gen-plan-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/gen-plan-template.md:1): 输出计划必须包含的结构、收敛状态、待用户决策、任务路由标签。
- [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:1): 参数解析、IO 前置校验、失败码。
- [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:120): 算法不变量的测试约束，包括 direct 不收敛、auto-start 必须 discussion、3 轮上限、模板一致性、脚本失败码。

## Pseudocode / transition table

```text
input:
  ARGUMENTS = --input draft --output plan [--auto-start-rlcr-if-converged] [--discussion|--direct]
  merged_config = default_config + user_config + project_config
  draft_content
  template_file

state:
  AUTO_START_RLCR_IF_CONVERGED: bool
  GEN_PLAN_MODE: discussion | direct
  ALT_PLAN_LANGUAGE, ALT_PLAN_LANG_CODE
  PLAN_CONVERGENCE_STATUS: converged | partially_converged
  HUMAN_REVIEW_REQUIRED: bool
  convergence_round: 0..3
  convergence_matrix[] = {topic, claude_position, codex_position, resolution_status, delta}
  pending_decisions[] = DEC-N items
  codex_analysis_v1
  candidate_plan

algorithm:
  parse ARGUMENTS
  if --discussion and --direct both present:
    stop invalid arguments

  load merged config
  resolve GEN_PLAN_MODE:
    CLI flag > valid config gen_plan_mode > discussion
  resolve alternative language:
    alternative_plan_language > legacy chinese_plan > disabled

  run validate-gen-plan-io.sh
  if exit != 0:
    map exit code to user-facing failure and stop

  run relevance check
  if NOT_RELEVANT:
    stop
  else:
    initialize output file from template + append original draft

  codex_analysis_v1 = ask-codex(first_pass_prompt)
  if ask-codex fails:
    ask user: retry or continue Claude-only with reduced confidence

  candidate_plan = Claude(draft + codex_analysis_v1 + repo exploration)

  if GEN_PLAN_MODE == direct:
    PLAN_CONVERGENCE_STATUS = partially_converged
    HUMAN_REVIEW_REQUIRED = true
    goto issue_resolution
  else:
    previous_material_change = true
    for round in 1..3:
      codex_review = ask-codex(candidate_plan + prior_disagreements + unresolved_items)
      candidate_plan = Claude.revise(candidate_plan, codex_review.REQUIRED_CHANGES)
      convergence_matrix[round] = assess(
        AGREE, DISAGREE, REQUIRED_CHANGES, OPTIONAL_IMPROVEMENTS, UNRESOLVED
      )

      if no REQUIRED_CHANGES and no high-impact DISAGREE:
        PLAN_CONVERGENCE_STATUS = converged
        break

      if round >= 2 and no material plan changes for two consecutive rounds:
        PLAN_CONVERGENCE_STATUS = converged or partially_converged based on remaining blockers
        break

    if no convergence condition met after round 3:
      PLAN_CONVERGENCE_STATUS = partially_converged
      carry unresolved opposite opinions to user decision phase

issue_resolution:
  if GEN_PLAN_MODE == direct:
    HUMAN_REVIEW_REQUIRED = true
  else if AUTO_START_RLCR_IF_CONVERGED and PLAN_CONVERGENCE_STATUS == converged:
    HUMAN_REVIEW_REQUIRED = false
  else:
    HUMAN_REVIEW_REQUIRED = true

  pending_decisions =
    QUESTIONS_FOR_USER from Codex v1
    + needs_user_decision from final convergence matrix
  dedupe by topic
  remove only items clearly resolved in later refinement
  write remaining items as DEC-N with Decision Status = PENDING

  if HUMAN_REVIEW_REQUIRED:
    ask user about analysis issues, quantitative metrics, and needs_user_decision items

  generate final plan:
    include ACs, path boundaries, task breakdown, deliberation, convergence status, pending decisions
    every task tag must be exactly coding or analyze

  read/review full plan; fix inconsistencies

  if ALT_PLAN_LANGUAGE enabled:
    optionally write translated variant with _<code> suffix

  if AUTO_START_RLCR_IF_CONVERGED
     and PLAN_CONVERGENCE_STATUS == converged
     and GEN_PLAN_MODE == discussion
     and no PENDING decisions:
       start RLCR loop with --skip-quiz
  else:
       report why auto-start skipped
```

| 阶段 | 输入状态 | 转移 / gate | 输出状态 |
|---|---|---|---|
| Phase 0 | CLI args | `--discussion` 与 `--direct` 互斥；`--auto-start...` 只设置意图 | `AUTO_START_RLCR_IF_CONVERGED`, raw mode flags |
| Phase 0.5 | merged config + CLI flags | CLI mode 优先于 config；默认 `discussion` | `GEN_PLAN_MODE` |
| Phase 1 | draft/output/template paths | IO script exit code 0 才继续 | validated paths + `TEMPLATE_FILE` |
| Phase 2 | draft + repo | relevance checker 返回 `RELEVANT` 才继续 | initialized output plan with original draft |
| Phase 3 | draft + repo context | Codex 首轮输出结构化风险/问题/标准 | `Codex Analysis v1` |
| Phase 4 | draft + Codex v1 | Claude 生成 candidate plan + issue map | `candidate_plan_v1` |
| Phase 5 | candidate plan | `direct` 跳过；`discussion` 最多 3 轮 Codex review + Claude revision | `converged` 或 `partially_converged` |
| Phase 6 | status + matrix + questions | 决定是否人工审查；无条件汇总 pending decisions | `HUMAN_REVIEW_REQUIRED`, `DEC-N` |
| Phase 7/8 | final plan state | 写入计划，复查一致性，条件式翻译与 auto-start | final plan + optional RLCR start |

## Source evidence

- 命令必须以 `ultrathink` 执行，且计划生成期间禁止编码；允许写入仅限 plan 输出文件和可选翻译文件，auto-start 只能在后续 RLCR loop 中发生：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:18), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:20), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:24), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:28)。
- 全流程被定义为严格顺序执行，阶段包括执行模式、配置、IO、相关性、Codex 首轮、Claude v1、收敛循环、分歧解决、最终计划、写入完成：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:32), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:34), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:36)。
- 执行模式状态变量来自参数：`AUTO_START_RLCR_IF_CONVERGED`、`GEN_PLAN_MODE_DISCUSSION`、`GEN_PLAN_MODE_DIRECT`；`discussion/direct` 同时出现必须停止：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:49), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:51), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:56)。
- auto-start 的核心门控是 discussion mode + converged + no pending decisions；direct mode 明确不满足：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:58), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:594), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:596)。
- 配置合并顺序为 default、user、project，后层覆盖前层；fatal 配置错误停止，optional malformed JSON 仅 warning 并继续：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:66), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:70), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:74)。
- `GEN_PLAN_MODE` 的优先级是 CLI flag > merged config `gen_plan_mode` > default `discussion`：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:119), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:122)。
- IO validation exit code 映射由命令消费：0 继续并解析 `TEMPLATE_FILE`，1-7 分别停止并报告输入不存在、空输入、输出目录不存在、输出已存在、无写权限、非法参数、模板缺失：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:132), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:140)。
- 验证脚本实现了同一失败码表，并且解析 `--auto-start-rlcr-if-converged`、`--discussion`、`--direct`；direct+auto-start 只提示不会触发：[scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:4), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:35), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:54), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:76), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:93)。
- IO 脚本检查顺序是 input exists、input non-empty、output dir exists、output path not directory/existing、output dir writable，然后定位 template 并输出 `TEMPLATE_FILE`：[scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:108), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:116), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:124), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:132), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:147), [scripts/validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:162)。
- 相关性 gate：draft 完全无关时停止；相关时复制模板并附加原始 draft，之后进入 Codex 首轮：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:154), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:171), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:176)。
- Codex 首轮必须早于 Claude plan synthesis，输出字段包括 `CORE_RISKS`、`MISSING_REQUIREMENTS`、`TECHNICAL_GAPS`、`ALTERNATIVE_DIRECTIONS`、`QUESTIONS_FOR_USER`、`CANDIDATE_CRITERIA`：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:184), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:190), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:198)。
- Codex 不可用时不是静默降级，而是让用户选择 retry 或 Claude-only，并要求在计划里注明 cross-review confidence 降低：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:208)。
- Claude v1 的分析维度是 clarity、consistency、completeness、functionality，并要求 Explore agents 调查相关组件、文件、模式、依赖：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:216), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:224), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:247)。
- `direct` 模式跳过 Phase 5，直接设置 `PLAN_CONVERGENCE_STATUS=partially_converged` 与 `HUMAN_REVIEW_REQUIRED=true`，不能满足 auto-start：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:255), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:257)。
- 收敛轮中第二 Codex review 的输入必须包含当前 candidate plan、prior disagreements、unresolved items；输出必须含 `AGREE`、`DISAGREE`、`REQUIRED_CHANGES`、`OPTIONAL_IMPROVEMENTS`、`UNRESOLVED`：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:261), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:263), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:268)。
- Claude 修订必须处理 `REQUIRED_CHANGES` 并记录接受/拒绝 rationale；每轮更新 convergence matrix，字段是 Topic、Claude position、Second Codex position、Resolution status、Round-to-round delta：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:275), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:278)。
- 循环终止条件：无 `REQUIRED_CHANGES` 且无 high-impact `DISAGREE`；或连续两轮无 material plan changes；或最多 3 轮。达到上限仍有 opposite opinions 时显式带到用户决策阶段：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:286), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:288), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:293)。
- 收敛状态只有两个显式值：满足收敛条件为 `converged`，否则 `partially_converged`：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:295)。
- Phase 6 不得丢弃或覆盖原始 draft；澄清只能作为增量补充：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:301)。
- 人工审查 gate：direct 一律需要；否则 auto-start enabled 且 converged 才可跳过；跳过时直接进最终计划生成：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:305), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:307), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:312)。
- pending decisions 无条件汇总：来自 Phase 3 `QUESTIONS_FOR_USER` 和最终 convergence matrix 中 `needs_user_decision`；去重，只删除有清晰 resolved evidence 的项；剩余写为 `DEC-N` 且 `Decision Status=PENDING`：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:314), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:316), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:318), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:322)。
- 该 pending 汇总同时服务两类路径：人工审查时可见；跳过人工审查时通过 auto-start 的 `PENDING` 检查阻断启动：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:326)。
- 最终计划结构必须包含 `Task Breakdown`、`Claude-Codex Deliberation`、`Convergence Status`、`Pending User Decisions`：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:447), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:458), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:466), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:469)。
- 任务路由规则：每个 task 恰好一个 tag，取值只允许 `coding` 或 `analyze`；`coding` 给 Claude，`analyze` 通过 Codex `/humanize:ask-codex`：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:447), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:449)；模板同样固定该列：[prompt-template/plan/gen-plan-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/gen-plan-template.md:69)。
- 生成规则要求完整保留 draft 信息、记录 debate traceability、记录 convergence status、达到收敛或最大轮次才停止，并保留 carry-over decisions：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:523), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:525), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:527)。
- 写入阶段要求用 Edit 更新计划、保留底部原始 draft、完整复读检查一致性与 contradiction：[commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:537), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:544)。
- 测试约束验证了核心算法属性：允许 `ask-codex.sh`、暴露 auto-start flag、direct 不标记 converged、auto-start 需要 discussion、包含 Phase 3/5、最多 3 轮、Phase 3 在 Phase 4 前：[tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:125), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:131), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:137), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:143), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:161), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:173), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:179)。
- 测试还验证模板必须包含 deliberation、pending decisions、convergence status，且不再包含旧的 `Convergence Log` / `Codex Team Workflow` 区块：[tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:189), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:195), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:201), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:213)。
- 测试验证 pending consolidation 必须存在，且同时引用 `QUESTIONS_FOR_USER` 和 `needs_user_decision` 两类来源：[tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:237), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:243)。
- 测试覆盖验证脚本失败码：缺 value/未知 flag/help 为 6，input not found 为 1，empty input 为 2，output dir missing 为 3，output exists 或 directory 为 4，valid 为 0，auto-start flag accepted，discussion/direct recognized 且 mutually exclusive：[tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:569), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:596), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:605), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:614), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:624), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:634), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:654), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:663), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:672), [tests/test-gen-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-gen-plan.sh:688)。

## Edge cases and risks

- **无数值 score。** 源码/文档没有定义分数、阈值或排序函数；“收敛评分”实际是 qualitative gate：`REQUIRED_CHANGES`、high-impact `DISAGREE`、material plan changes、max rounds。
- **`high-impact DISAGREE` 未机械定义。** 算法要求无 high-impact `DISAGREE` 才收敛，但没有给出自动分类规则，依赖 Claude/Codex 判断，存在主观性。
- **`two consecutive rounds produce no material plan changes` 可能误判。** “material” 无明确 diff 阈值，可能把停滞误认为收敛，或把小修订误认为未收敛。
- **Codex 不可用会降级。** 失败时可由用户选择 Claude-only，但必须标注 cross-review confidence 降低；这会削弱双代理收敛保证。
- **direct 模式是有意的非收敛路径。** 它跳过 Phase 5 并强制 `partially_converged`/人工审查，不能 auto-start；如果用户以为 direct 表示“直接执行”，会被门控阻断。
- **pending decisions 是 auto-start 的硬阻断。** 即使 `PLAN_CONVERGENCE_STATUS=converged`，只要 `Decision Status=PENDING` 仍存在，就不能启动 RLCR。
- **原始 draft 是不可丢失 invariant。** Phase 6 和 Phase 8 都要求保留原始 draft，澄清只能追加；若最终计划摘要与原始 draft 冲突，必须修复。
- **模板一致性是测试约束。** `gen-plan.md` 内嵌 Plan Structure 必须与 `gen-plan-template.md` 完全一致，修改其中一处会破坏测试。
- **IO validator 标称 side-effect-free，但测试脚本自身会创建临时 fixtures。** 算法层面的实际命令 validator 不创建 output 文件；测试创建临时文件只用于验证失败码，不属于 gen-plan 运行时机制。

## What is explicitly out of scope

- 安装、插件市场元数据、README 营销文案、截图、通用使用说明。
- RLCR loop 内部实现、编码执行策略、PR/commit 流程；`gen-plan` 只可能在满足条件后启动后续命令，不在计划生成阶段编码。
- `ask-codex.sh` 的内部实现、Codex CLI 调用细节、超时策略细节；本研究只覆盖 `gen-plan` 如何路由和消费其输出。
- `draft-relevance-checker` agent 的完整提示词与模型行为；这里只覆盖 `gen-plan` 对 `RELEVANT/NOT_RELEVANT` gate 的使用。
- 配置加载器 `scripts/lib/config-loader.sh` 的内部合并实现；这里只覆盖 `gen-plan.md` 对合并语义的要求。
- 翻译质量、语言检测算法、替代语言 mapping 之外的国际化行为。
- 对当前工作区未提交改动的评估；取证目标是 pinned commit `0ec921a36b4365df503511c5567bbd3e02db0df5`。
