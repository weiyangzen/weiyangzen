**Topic and Conclusion**

Topic: Full-alignment review cadence and drift detection。

结论：该子系统不是数值打分器，而是一个“强制全量对齐审查 + 文本判定 + 持久化漂移状态机 + 退出前门禁”的组合机制。全量对齐审查在“可配置间隔”触发，要求 Codex 重新读取原始计划、核对 goal tracker、输出强制的 `Mainline Progress Verdict`。漂移检测依赖三类主线判定：`ADVANCED / STALLED / REGRESSED`；连续停滞/回退会先进入 drift recovery replan，再触发 stop circuit breaker。`COMPLETE` 不是直接终止：它会先进入 Finalize Phase；真正退出前还会经过 methodology analysis phase，除非 privacy mode 跳过。

**Algorithm Subset Covered**

本次只覆盖这三个路径中的算法相关内容：

- [prompt-template/codex/full-alignment-review.md](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:1)：全量目标对齐审查模板、漂移判定输出契约、停止/完成条件。
- [tests/test-finalize-phase.sh](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:208)：Finalize、review failure、drift state machine 的被测行为。
- [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:17)：退出前 methodology analysis phase 的状态迁移和 fail-closed 门禁。

显式状态变量：

- `current_round`, `max_iterations`, `review_started`, `mainline_stall_count`, `last_mainline_verdict`, `drift_status`，由测试状态文件初始化约束，见 [tests/test-finalize-phase.sh:218](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:218) 到 235。
- 终态/中间态文件：`state.md`, `finalize-state.md`, `complete-state.md`, `stop-state.md`, `maxiter-state.md`, `methodology-analysis-state.md`。
- methodology phase 标记：`.methodology-exit-reason`, `methodology-analysis-done.md`, `methodology-analysis-report.md`，见 [hooks/lib/methodology-analysis.sh:64](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:64) 到 72、[hooks/lib/methodology-analysis.sh:114](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:114) 到 171。

**Pseudocode or Transition Table**

```text
on_full_alignment_review(round):
    # Cadence: invoked at configurable intervals; actual interval calculation is outside this subset.
    require read(PLAN_FILE)
    tracker = read(GOAL_TRACKER_FILE)

    for each AC in IMMUTABLE SECTION:
        classify AC as MET | PARTIAL | NOT MET | DEFERRED
        attach evidence/blocker/deferral justification

    forgotten = plan.tasks - tracker.active/completed/deferred
    audit deferred items against Ultimate Goal
    summarize AC counts, active tasks, blockers

    verdict = parse_required_line("Mainline Progress Verdict")
    if verdict missing:
        block round; require review rerun; preserve drift state

    classify findings into:
        Mainline Gaps
        Blocking Side Issues
        Queued Side Issues

    if historical stagnation signs detected:
        write STOP as final line
    else if all original plan tasks done
            and all ACs fully MET
            and no deferred items:
        write COMPLETE as final line
    else:
        write findings; do not write COMPLETE
```

Drift state transitions inferred from tested behavior:

| Input verdict | Prior state | Transition | Evidence |
|---|---:|---|---|
| missing `Mainline Progress Verdict` | any | block, no next prompt, preserve `current_round`, `mainline_stall_count`, `last_mainline_verdict`, `drift_status` | [tests/test-finalize-phase.sh:948](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:948) to 994 |
| `STALLED` with prior stall count `1` | `mainline_stall_count=1` | advance to next round, set stall count `2`, `last_mainline_verdict=stalled`, `drift_status=replan_required`, create Drift Recovery prompt | [tests/test-finalize-phase.sh:893](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:893) to 946 |
| `REGRESSED` with prior stall count `2` and `replan_required` | `mainline_stall_count=2` | create `stop-state.md`, preserve stall count `3`, `last_mainline_verdict=regressed`, `drift_status=replan_required` | [tests/test-finalize-phase.sh:996](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:996) to 1039 |
| `ADVANCED` with non-`COMPLETE` findings | normal round | block with feedback, keep `state.md`, increment `current_round`, write review result | [tests/test-finalize-phase.sh:818](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:818) to 878 |

Completion/finalization routing:

```text
if review output COMPLETE:
    if current_round >= max_iterations:
        state.md -> maxiter-state.md
        skip Finalize
    else if codex review fails or returns empty output:
        block; keep state.md; set/preserve review_started=true
    else:
        state.md -> finalize-state.md
        block with Finalize prompt

while finalize-state.md active:
    require finalize-summary.md
    require clean git state
    require todos complete
    do not invoke Codex
    finalize-state.md -> complete-state.md
```

Methodology analysis routing:

```text
enter_methodology_analysis_phase(exit_reason):
    if PRIVACY_MODE == true:
        skip
    if methodology-analysis-state.md exists:
        skip re-entry
    if methodology-analysis-done.md exists and nonempty:
        skip already completed

    STATE_FILE -> methodology-analysis-state.md
    write exit_reason to .methodology-exit-reason
    touch empty methodology-analysis-done.md
    render prompt
    return block JSON

complete_methodology_analysis():
    require methodology-analysis-done.md exists and non-whitespace
    require methodology-analysis-report.md exists and non-whitespace
    require .methodology-exit-reason exists
    require exit_reason in {complete, stop, maxiter}

    methodology-analysis-state.md -> <exit_reason>-state.md
    remove .methodology-exit-reason
    allow exit
```

**Source Evidence**

- 全量审查是“mandatory checkpoint”，但节奏只声明为“configurable intervals”；具体间隔计算不在这三个文件内：[prompt-template/codex/full-alignment-review.md:3](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:3)。
- 审查必须先读原始计划，保证对齐基准来自 `PLAN_FILE`，见 [prompt-template/codex/full-alignment-review.md:7](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:7) 到 10。
- AC 审计要求逐个核对 immutable section，并输出 `MET / PARTIAL / NOT MET / DEFERRED`，见 [prompt-template/codex/full-alignment-review.md:21](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:21) 到 30。
- Forgotten item detection 通过比较原始计划和当前 goal tracker 的 Active/Completed/Deferred 集合完成，见 [prompt-template/codex/full-alignment-review.md:32](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:32) 到 36。
- Deferred item audit 要重新验证 deferral 是否仍有效、是否应解除、是否违背 Ultimate Goal，见 [prompt-template/codex/full-alignment-review.md:38](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:38) 到 42。
- Drift audit 明确检查当前 round 是否仍服务原计划、主线目标是否清晰单一、是否推进主线 AC，见 [prompt-template/codex/full-alignment-review.md:52](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:52) 到 58。
- 漂移输出契约要求 `Mainline Progress Verdict: ADVANCED / STALLED / REGRESSED`，并统计 blocking/queued side issues，见 [prompt-template/codex/full-alignment-review.md:59](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:59) 到 64。
- `Mainline Progress Verdict` 是硬门禁；遗漏会被 stop hook 阻塞并要求重跑审查，见 [prompt-template/codex/full-alignment-review.md:66](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:66)。
- 全量对齐审查会读取最近历史文件，包括 previous review result、two-rounds-ago review result、previous summary，见 [prompt-template/codex/full-alignment-review.md:81](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:81) 到 92。
- 停滞触发信号包括重复问题、多个 round 无 AC 进展、重复错误、循环讨论、无新代码、Codex 重复反馈未处理，见 [prompt-template/codex/full-alignment-review.md:94](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:94) 到 100。
- 停滞时最终行必须写 `STOP`，见 [prompt-template/codex/full-alignment-review.md:102](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:102)。
- `COMPLETE` 的唯一条件是所有原始任务完成、所有 AC 满足、无 deferral；deferred 明确视为 incomplete，见 [prompt-template/codex/full-alignment-review.md:111](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/full-alignment-review.md:111) 到 114。
- Drift 状态变量由 state frontmatter 持久化：`mainline_stall_count`, `last_mainline_verdict`, `drift_status`，见 [tests/test-finalize-phase.sh:218](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:218) 到 235。
- 连续第二次 `STALLED` 会生成 drift recovery prompt，并把 `drift_status` 置为 `replan_required`，见 [tests/test-finalize-phase.sh:893](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:893) 到 946。
- 缺失 verdict 会 block、不会生成下一轮 prompt、并保留既有 drift state，见 [tests/test-finalize-phase.sh:948](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:948) 到 994。
- 第三次 stalled/regressed 会触发 circuit breaker，产生 `stop-state.md`，并保留最终漂移状态，见 [tests/test-finalize-phase.sh:996](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:996) 到 1039。
- `COMPLETE` 正常不会直接终止，而是进入 Finalize Phase：`state.md -> finalize-state.md` 并 block with prompt，见 [tests/test-finalize-phase.sh:591](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:591) 到 607。
- 到达 max iterations 时跳过 Finalize，直接产生 `maxiter-state.md`，见 [tests/test-finalize-phase.sh:609](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:609) 到 627。
- Codex review failure 或 empty output 会 block，不创建 `finalize-state.md`/`complete-state.md`，并保留 `state.md` 与 `review_started: true`，见 [tests/test-finalize-phase.sh:633](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:633) 到 688、[tests/test-finalize-phase.sh:694](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:694) 到 767。
- Finalize Phase 要求 summary、git clean，完成后 `finalize-state.md -> complete-state.md`，且不调用 Codex，见 [tests/test-finalize-phase.sh:494](/Users/wangweiyang/GitHub/humanize/tests/test-finalize-phase.sh:494) 到 568。
- methodology analysis 进入时会把当前状态重命名为 `methodology-analysis-state.md`、记录 exit reason、创建空 done placeholder，并返回 block JSON，见 [hooks/lib/methodology-analysis.sh:38](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:38) 到 99。
- methodology completion 要求 done/report 都存在且非空，exit reason 必须是 `complete|stop|maxiter`，否则 fail closed，见 [hooks/lib/methodology-analysis.sh:114](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:114) 到 173。

**Edge Cases and Risks**

- Cadence 风险：模板只说“configurable intervals”，这三个文件不包含触发间隔、取模逻辑或配置解析；因此无法从本子集证明具体 cadence 是否正确。
- Verdict 解析风险：核心状态机依赖文本行 `Mainline Progress Verdict`。测试覆盖了“缺失 verdict”会 fail closed，但未在本子集证明大小写、额外空格、多 verdict、拼写错误如何处理。
- `ADVANCED` 的 drift reset 行为在本子集未被直接断言。测试只证明 normal round 会继续并递增 `current_round`，未证明 `mainline_stall_count` 是否归零。
- 停滞检测本质是审查者根据历史文件作语义判断；模板列出信号，但没有数值阈值、相似度算法或自动重复问题检测。
- `COMPLETE` 路由有多重门禁：即使 review 输出 `COMPLETE`，Codex review failure 或空输出也会阻止进入 Finalize。这降低误完成风险，但也引入外部 review 可用性风险。
- Methodology phase 的 done marker 先创建为空文件；完成判断依赖“非空 done + 非空 report”。若 report 内容无实质质量，仅非空即可通过该文件内的门禁。
- `PRIVACY_MODE=true` 会跳过 methodology analysis；这保护隐私，但也绕过退出后的方法论复盘。
- `exit_reason` 缺失或非法会阻止 methodology completion，这是 fail-closed；但如果 `methodology-analysis-state.md` 丢失，本文件中的 `mv` 路径没有显式前置存在性检查。

**What Is Explicitly Out of Scope**

- 实际 full-alignment cadence scheduler、配置项来源、round 间隔计算：不在所给三文件内。
- stop hook 的完整实现、verdict parser 具体正则、state 写回函数：只通过测试行为间接观察，未读取实现文件。
- Git clean、todo complete、write/read/bash validator 的内部算法：测试覆盖其期望行为，但实现不在本次焦点内。
- 安装、营销、截图、泛用说明：已跳过。
- 数值 scoring、confidence threshold、概率路由：这三个文件没有定义，只有枚举判定与 fail-closed 门禁。
- methodology analysis prompt 的完整内容：本文件只提供 fallback 与渲染入口，具体模板不在本次焦点路径内。