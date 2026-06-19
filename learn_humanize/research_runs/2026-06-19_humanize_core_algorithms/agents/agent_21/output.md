**Topic and conclusion**

Topic: Agent Teams parallelization prompt

结论：该机制不是数值评分型调度器，而是“前置语义门禁 + RLCR 团队领导提示 + 文件所有权并行化约束”的规则算法。它先用 draft/plan 检查器过滤明显无关输入和不兼容的分支切换指令，再让 Team Leader 在 RLCR 轮次内只做拆分、委派、协调、审核和总结；并行的核心安全条件是“任务独立且文件所有权不重叠”，否则必须用依赖顺序串行化。

**Algorithm subset covered**

覆盖的算法相关文件：

- [agents/plan-compliance-checker.md](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:1)：计划进入 RLCR 前的相关性与分支切换合规检查。
- [agents/draft-relevance-checker.md](/Users/wangweiyang/GitHub/humanize/agents/draft-relevance-checker.md:1)：草稿生成计划前的仓库相关性检查。
- [prompt-template/claude/agent-teams-core.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:1)：Agent Teams 模式核心角色、并行拆分、文件冲突、质量和提交规则。
- [prompt-template/claude/agent-teams-instructions.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-instructions.md:1)：初始 RLCR 轮次的输入和总结要求。
- [prompt-template/claude/agent-teams-continue.md](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-continue.md:1)：后续轮次的 review 驱动重组队伍规则。

状态变量可抽象为：

- `repo_context`：README、CLAUDE、目录结构、技术栈、仓库目的。
- `draft_content` / `plan_content`：用户草稿或实现计划。
- `round_type`：`initial` 或 `continuation`。
- `goal_tracker`、`prior_summaries`、`codex_review_feedback`。
- `task_graph`：拆分后的任务、验收标准、`blockedBy` 依赖。
- `file_ownership_map`：文件到队员/任务的独占映射。
- `team_roster`：当前轮新建的团队成员集合。
- `task_status`：TaskList 中的进度、阻塞、完成状态。
- `work_notes`：包括 BitLesson 选择结果 `lesson_id | NONE`。
- `branch_state`：RLCR 全轮次保持不变的工作分支约束。
- `summary_file`：团队完成后的工作总结输出位置。

**Pseudocode or transition table**

```text
function validate_draft(draft_content):
    repo_context = quick_explore_repo(README, CLAUDE, docs, directory)
    relevant =
        mentions_repo_concepts(draft_content, repo_context) OR
        modifies_extends_uses_codebase(draft_content) OR
        learns_from_or_understands_codebase(draft_content) OR
        references_existing_paths_functions_features(draft_content)

    if relevant OR uncertain:
        return "RELEVANT: <brief explanation>"
    else:
        return "NOT_RELEVANT: <brief explanation>"
```

```text
function validate_plan(plan_content):
    repo_context = quick_explore_repo(README, CLAUDE, docs, directory)

    relevance_ok =
        has_substantive_content(plan_content) AND
        (
          mentions_repo_concepts(plan_content, repo_context) OR
          modifies_extends_uses_codebase(plan_content) OR
          references_existing_paths_functions_features(plan_content) OR
          uncertain_but_reasonably_connected(plan_content)
        )

    branch_switch =
        contains_required_branch_change(plan_content)
        AND NOT safe_branch_reference(plan_content)

    # Source requires exactly one verdict, but does not define precedence
    # when both failures are true.
    if branch_switch:
        return "FAIL_BRANCH_SWITCH: <quote specific instruction>"
    if NOT relevance_ok:
        return "FAIL_RELEVANCE: <reason>"
    return "PASS: <brief summary>"
```

```text
function run_agent_teams(round_type):
    assert leader_does_not_code_or_edit()

    if round_type == "initial":
        read(plan_file)
        read(goal_tracker)
        work_scope = plan_file.requirements
    else:
        discard_previous_team()
        review = analyze(codex_review_feedback)
        read(goal_tracker, prior_summaries)
        verify_current_file_state()
        work_scope = only_review_issues_and_gaps(review)
        prioritize_high_priority_items_if_too_large(work_scope)

    task_graph = split_into_independent_tasks(work_scope)
    for each task in task_graph:
        define_scope_and_acceptance_criteria(task)
        require_bitlesson_selector_before_subtask(task)

        if task.touches_file_already_owned_in_parallel:
            add_blockedBy_dependency(task)
        else:
            assign_strict_file_ownership(task)

        if task.high_risk_or_architectural:
            require_plan_mode_and_leader_approval(task)

        spawn_task_tool_member(
            team_name,
            cold_start_context = {
                plan_or_goal,
                relevant_paths,
                prior_done_state,
                exact_assignment,
                acceptance_criteria
            }
        )

    while not all_tasks_done:
        monitor_TaskList()
        if member_blocked_or_stuck:
            unblock_or_reassign()
        if member_idle_after_message:
            respond_to_member()

    review_outputs_before_complete()
    verify_no_file_conflicts()
    verify_acceptance_criteria()
    coordinate_member_commits_in_sequence()
    merge_team_work_and_resolve_conflicts()
    write_work_summary(summary_file)
```

关键转移规则：

| 阶段 | 输入 | Gate / Routing | 输出 |
|---|---|---|---|
| Draft gate | 草稿 + 仓库上下文 | 语义相关性；不确定时判相关 | `RELEVANT` 或 `NOT_RELEVANT` |
| Plan gate | 计划 + 仓库上下文 | 相关性 + 分支切换检测；不确定时放行 | `PASS` / `FAIL_RELEVANCE` / `FAIL_BRANCH_SWITCH` |
| Initial team round | 计划、goal tracker | 先读计划和 tracker，再拆分 | 新团队任务图 |
| Continuation round | Codex review、tracker、旧 summary、当前文件状态 | 丢弃旧团队，只处理 review 问题和缺口 | 新团队任务图 |
| Parallel routing | 任务与文件集合 | 文件不重叠才并行；重叠则 `blockedBy` 串行 | 安全并行执行 |
| Completion gate | 队员输出 | Leader 审核正确性、冲突、验收标准 | 可完成、提交、总结 |

**Source evidence**

- Plan checker 是 RLCR 前置验证器，执行两个检查并返回单一 verdict：[agents/plan-compliance-checker.md:10](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:10)、[agents/plan-compliance-checker.md:14](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:14)。
- Plan 相关性检查要求快速理解仓库文档、目录、技术和目的：[agents/plan-compliance-checker.md:18](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:18)-[21](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:21)；随后判断是否提到仓库概念、修改/扩展/使用代码库、引用存在的路径/函数/功能、是否有实质内容：[agents/plan-compliance-checker.md:23](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:23)-[27](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:27)。
- Plan 相关性采用宽松策略，只拒绝明确无关的计划；合理可连接即通过：[agents/plan-compliance-checker.md:29](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:29)。
- 分支切换检测覆盖自然语言和命令模式，包括 `switch/checkout/create/work on/move to branch`、`git checkout -b`、`git switch`、`git branch`、`gh pr checkout`、worktree 创建和任何中途换分支暗示：[agents/plan-compliance-checker.md:31](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:31)-[38](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:38)。
- 安全消歧规则明确排除 `git checkout -- <file>`、否定性指令、描述性分支引用、`--base-branch` 配置：[agents/plan-compliance-checker.md:40](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:40)-[44](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:44)。
- 分支不变是 RLCR 不变量：工作分支必须在所有轮次保持常量，要求换分支的计划与 RLCR 不兼容：[agents/plan-compliance-checker.md:46](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:46)。
- Plan checker 输出必须是三种 verdict 中且仅有一种：[agents/plan-compliance-checker.md:48](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:48)-[55](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:55)；相关性和分支检测不确定时都倾向 `PASS`：[agents/plan-compliance-checker.md:58](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:58)-[62](/Users/wangweiyang/GitHub/humanize/agents/plan-compliance-checker.md:62)。
- Draft checker 同样先探索仓库，再判断草稿是否修改、扩展、使用、学习或理解代码库，或引用现有路径/函数/功能：[agents/draft-relevance-checker.md:16](/Users/wangweiyang/GitHub/humanize/agents/draft-relevance-checker.md:16)-[25](/Users/wangweiyang/GitHub/humanize/agents/draft-relevance-checker.md:25)。
- Draft checker 输出 `RELEVANT` / `NOT_RELEVANT`，并要求宽松、支持任意语言/粗略想法、关注语义、不确定时判相关：[agents/draft-relevance-checker.md:27](/Users/wangweiyang/GitHub/humanize/agents/draft-relevance-checker.md:27)-[36](/Users/wangweiyang/GitHub/humanize/agents/draft-relevance-checker.md:36)。
- Team Leader 的唯一职责是协调和委派，绝不写代码、编辑文件或自行实现：[prompt-template/claude/agent-teams-core.md:3](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:3)；主要职责包括拆分并行任务、用带 `team_name` 的 Task tool 创建团队、避免冲突、监控和等待队员完成：[prompt-template/claude/agent-teams-core.md:5](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:5)-[12](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:12)。
- 并行拆分要求任务相互独立、无文件冲突、有清晰范围和验收标准，并建议每名队友 5-6 个任务：[prompt-template/claude/agent-teams-core.md:16](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:16)。
- 队员冷启动不继承对话历史，但会自动加载项目 CLAUDE.md 和 MCP；派发时必须提供计划/目标、路径、已完成状态和具体任务：[prompt-template/claude/agent-teams-core.md:17](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:17)。
- 文件冲突模型是“同文件并行编辑会静默覆盖而非产生 merge conflict”，因此必须严格文件所有权；同文件任务必须用 `blockedBy` 串行化：[prompt-template/claude/agent-teams-core.md:18](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:18)。
- 进度通过 TaskList 追踪，阻塞时解阻或重派；完成前必须 review 队员输出、验证正确性、无冲突且满足验收标准：[prompt-template/claude/agent-teams-core.md:19](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:19)-[20](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:20)。
- 提交策略是队员各自提交，Leader 协调整体提交顺序；高风险或架构性任务可要求 plan mode 并由 Leader 审批：[prompt-template/claude/agent-teams-core.md:21](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:21)-[22](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:22)。
- 每个子任务前要求运行 `bitlesson-selector`，并在工作记录中记录 lesson IDs 或 `NONE`：[prompt-template/claude/agent-teams-core.md:23](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-core.md:23)。
- 初始轮次要求先读实现计划和 `goal-tracker.md`，所有队员结束后写指定 summary：[prompt-template/claude/agent-teams-instructions.md:3](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-instructions.md:3)-[8](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-instructions.md:8)。
- 继续轮次要求旧团队已不存在，不能再联系或引用旧队员，必须为本轮创建全新团队：[prompt-template/claude/agent-teams-continue.md:7](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-continue.md:7)。
- 继续轮次先分析 Codex review，避免重做已正确完成的工作，只处理 review 发现的问题和缺口；新队员仍是冷启动，需提供历史完成情况、当前文件状态、具体 review findings 和验收标准：[prompt-template/claude/agent-teams-continue.md:8](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-continue.md:8)-[10](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-continue.md:10)。
- 如果剩余工作超出单轮团队能力，应优先处理高优先级 review 项；分派文件前要快速读取或 grep 验证当前状态：[prompt-template/claude/agent-teams-continue.md:11](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-continue.md:11)-[12](/Users/wangweiyang/GitHub/humanize/prompt-template/claude/agent-teams-continue.md:12)。

**Edge cases and risks**

- 双重失败优先级未定义：计划既明显无关又包含换分支指令时，规范只要求输出一个 verdict，但没有规定 `FAIL_RELEVANCE` 与 `FAIL_BRANCH_SWITCH` 的 tie-breaker。
- 相关性判断是语义宽松门禁，不是精确分类器；风险是无关内容被放行，但设计上优先避免误拒。
- 分支检测同样倾向放行；隐晦的“在另一个分支上完成”可能漏检，但可减少安全上下文如 `git checkout -- <file>` 的误报。
- 同文件并行编辑的失败模式很严重：提示明确说会静默覆盖而不是冲突，因此 `file_ownership_map` 是并行化安全的核心。
- 冷启动队员没有 Leader 的对话历史；派发 prompt 缺少当前文件状态、review finding 或验收标准时，会导致实现偏离。
- Continuation 中旧团队不可用；如果 Leader 试图继续联系旧队员，会违反状态模型并阻塞本轮。
- Leader 自行写代码会破坏职责不变量，也会绕开文件所有权、BitLesson、审查和提交顺序约束。
- “每人 5-6 个任务”是启发式，不是容量证明；过度拆分可能增加协调成本，拆分不足会降低并行度。
- `bitlesson-selector` 被要求运行，但这些文件没有定义其算法、失败处理或 lesson 选择质量标准。

**What is explicitly out of scope**

- 安装流程、营销文案、截图、泛用使用说明未纳入。
- 实际 Task tool、MCP、TaskList、`blockedBy`、commit sequencing 的底层实现不在这组文件内。
- `bitlesson-selector` 的内部选择算法、lesson 数据来源和失败恢复不在范围内。
- 没有数值评分、置信度阈值、优先级分数或自动调度器实现；这里只有二元/三元 verdict 与规则化 routing。
- 没有定义 merge 冲突解决算法，只规定 Leader 需要合并团队工作并解决冲突。
- 没有定义 Codex review feedback 的格式，只要求 continuation 轮次先分析并按关键性分配工作。
- 没有覆盖非 Claude 模板、其他 agent 文件、命令实现脚本或 RLCR 外层控制器逻辑。