**Topic and conclusion**

Topic: Finalize 与 Methodology Analysis 两个收尾阶段的核心控制算法。

结论: 这部分不是数值评分算法，而是一个以“布尔门禁 + 文件标记 + 状态文件重命名”为核心的收尾状态机。Finalize 阶段要求在不改变功能的前提下做最后清理，并以任务状态、测试、提交、总结文件作为退出门禁；当 review 被跳过时，路由到更保守的 skipped prompt，强制人工验证，简化变为可选。Methodology Analysis 阶段在 RLCR 循环真正退出前插入一个阻塞式分析阶段，依赖 `methodology-analysis-state.md`、`methodology-analysis-done.md`、`methodology-analysis-report.md`、`.methodology-exit-reason` 四类文件状态决定是否允许最终退出。

**Algorithm subset covered**

- Normal Finalize prompt: [prompt-template/claude/finalize-phase-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-prompt.md:1)
- Review-skipped Finalize prompt: [prompt-template/claude/finalize-phase-skipped-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-skipped-prompt.md:1)
- Methodology Analysis phase library: [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:1)
- Pinned commit verified read-only via `.git/refs/heads/main`: `0ec921a36b4365df503511c5567bbd3e02db0df5`.

**Pseudocode or transition table**

```text
Finalize routing:
  if codex_review == passed:
      enter FinalizePhase
      require code-simplifier Task agent
      simplify recent branch changes: BASE_BRANCH -> START_BRANCH
      enforce: functionality unchanged, tests pass, no new bugs, equivalent-only edits
      before exit:
          complete all [mainline] and [blocking] tasks
          allow [queued] only if documented non-blocking
          commit changes
          write FINALIZE_SUMMARY_FILE with simplifications/files/tests/notes

  if codex_review == skipped:
      enter FinalizePhaseReviewSkipped(REVIEW_SKIP_REASON)
      require manual verification: review code, run available tests, check quality
      optionally invoke code-simplifier if time permits
      enforce same equivalent-only constraints
      before exit:
          complete all [mainline] and [blocking] tasks
          allow [queued] only if documented non-blocking
          commit changes
          write FINALIZE_SUMMARY_FILE with work/files/tests-if-possible/manual-verification
```

```text
Methodology analysis:
  enter_methodology_analysis_phase(exit_reason, description):
      if PRIVACY_MODE == true: return 1
      if LOOP_DIR/methodology-analysis-state.md exists: return 1
      if LOOP_DIR/methodology-analysis-done.md exists and non-empty: return 1

      mv STATE_FILE -> LOOP_DIR/methodology-analysis-state.md
      write exit_reason -> LOOP_DIR/.methodology-exit-reason
      touch LOOP_DIR/methodology-analysis-done.md  # empty placeholder
      render methodology-analysis prompt
      output JSON { decision: "block", reason: prompt, systemMessage: ... }
      return 0

  complete_methodology_analysis():
      require non-empty methodology-analysis-done.md
      require non-empty methodology-analysis-report.md
      require .methodology-exit-reason exists
      normalize exit_reason by deleting whitespace
      require exit_reason in {complete, stop, maxiter}

      mv methodology-analysis-state.md -> ${exit_reason}-state.md
      rm .methodology-exit-reason
      return 0

  block_methodology_analysis_incomplete():
      output JSON { decision: "block", reason: incomplete-instructions, systemMessage: ... }
```

| State | Input/gate | Transition | Output |
|---|---|---|---|
| ReviewPassed | Codex review passed | `FinalizePhase` | Required simplifier + strict equivalent refactor |
| ReviewSkipped | `REVIEW_SKIP_REASON` present | `FinalizePhaseSkipped` | Manual verification + optional simplifier |
| ExitCandidate | `PRIVACY_MODE=true` | skip methodology | return `1` |
| ExitCandidate | active/done marker exists | skip methodology | return `1` |
| ExitCandidate | no skip gates | `MethodologyAnalysisActive` | block JSON |
| MethodologyAnalysisActive | done/report/marker valid | terminal `${exit_reason}-state.md` | return `0` |
| MethodologyAnalysisActive | any completion artifact invalid | still blocked | block JSON |

**Source evidence**

- Normal Finalize 的进入条件是 review 已通过、实现完成、验收满足，随后进入 Finalize Phase: [prompt-template/claude/finalize-phase-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-prompt.md:3) lines 3-5。
- Normal Finalize 强制调用 `code-simplifier:code-simplifier` Task agent: [prompt-template/claude/finalize-phase-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-prompt.md:9) lines 9-14。
- Finalize 的不可协商约束是功能不变、测试不失败、不引入 bug、仅做功能等价清理: [prompt-template/claude/finalize-phase-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-prompt.md:16) lines 16-23；skipped prompt 同样约束见 [prompt-template/claude/finalize-phase-skipped-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-skipped-prompt.md:26) lines 26-33。
- Normal Finalize 的优化目标是近期变更、`BASE_BRANCH` 到 `START_BRANCH` 差异、去复杂度、读性、重复代码、控制流、死代码/未用变量: [prompt-template/claude/finalize-phase-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-prompt.md:25) lines 25-34。
- Finalize 退出门禁包括完成 `[mainline]`/`[blocking]`、只允许已记录的非阻塞 `[queued]`、提交、写 summary: [prompt-template/claude/finalize-phase-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-prompt.md:41) lines 41-52；skipped 版本见 [prompt-template/claude/finalize-phase-skipped-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-skipped-prompt.md:40) lines 40-51。
- Review skipped 路径显式带 `REVIEW_SKIP_REASON`，要求人工检查、运行可用测试、检查常见质量问题: [prompt-template/claude/finalize-phase-skipped-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-skipped-prompt.md:3) lines 3-13。
- Review skipped 路径下简化是 optional，且仍聚焦 `BASE_BRANCH` 到 `START_BRANCH`: [prompt-template/claude/finalize-phase-skipped-prompt.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/finalize-phase-skipped-prompt.md:15) lines 15-24。
- Methodology Analysis 的职责是在 RLCR 真正退出前，由独立 Opus agent 从方法论角度分析开发记录，并可帮助提交 GitHub issue: [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:5) lines 5-10。
- Methodology enter 函数的参数、全局变量、返回语义定义在 [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:22) lines 22-36。
- Methodology enter 的 skip gates: privacy mode、re-entry marker、非空 done marker，见 [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:42) lines 42-61。
- Methodology enter 的状态转移: rename state、写 exit reason、创建空 done placeholder、渲染 prompt、输出 `decision:block` JSON，见 [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:64) lines 64-99。
- Methodology complete 的完成门禁: 非空 done、非空 report、存在 exit reason marker、exit reason 属于 `complete|stop|maxiter`，见 [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:119) lines 119-163。
- Methodology complete 的终态命名规则是 `${exit_reason}-state.md`，然后删除 `.methodology-exit-reason`: [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:165) lines 165-173。
- Incomplete blocker 会再次输出 `decision:block`，并要求生成分析、review report、可选 issue、写非空 completion note: [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/methodology-analysis.sh:183) lines 183-206。

**Edge cases and risks**

- 无数值评分或排序规则；所有 routing/scoring 都是布尔门禁、文件存在性、非空内容和枚举校验。
- `enter_methodology_analysis_phase` 不校验 `exit_reason`，无效值会先写入 `.methodology-exit-reason`，到 completion 时才 fail closed: lines 68-69 与 155-161。
- `methodology-analysis-done.md` 在 enter 时会被创建为空 placeholder；只有写入实际内容后 completion 才通过，避免空文件误判完成: lines 71-72 与 123-128。
- Completion 只校验 done/report 非空，不校验报告结构、质量或是否真的由 Opus agent 完成: lines 123-143。
- `mv "$LOOP_DIR/methodology-analysis-state.md" "$LOOP_DIR/$target_name"` 前没有显式检查 source state 是否存在；从该文件本身看，`mv` 失败后的错误处理依赖外层 shell 行为，不在本函数内闭环: lines 165-173。
- Enter 阶段的 `mv`、写 marker、`touch`、prompt 渲染和 `jq` 输出也没有逐步状态回滚；函数末尾显式 `return 0`，因此部分 I/O 失败可能导致不一致状态，除非调用环境启用了额外错误策略: lines 64-99。
- Review skipped 路径下 code simplification 是 optional，核心风险由人工验证承担；这比 review passed 路径少一个已通过审查的前置保证: skipped prompt lines 3-17。

**What is explicitly out of scope**

- 未检查安装、营销、截图、普通使用说明。
- 未分析 `code-simplifier:code-simplifier` agent 的内部算法；这里只覆盖 prompt 对它的调用要求。
- 未分析 `Task` tool、`TaskUpdate`、`load_and_render_safe`、`jq` 的实现。
- 未分析 `loop-codex-stop-hook.sh` 的调用编排；本结论只基于 `methodology-analysis.sh` 中公开的函数契约和状态转移。
- 未分析 `claude/methodology-analysis-prompt.md` 模板内容，因为它不在本次 focus paths 中。