**Topic and Conclusion**

Topic: Edit/Write/Read validators 对 RLCR loop 受保护文件面的访问控制算法。

结论：这组三个 validator 是一个确定性的 first-match gate 链，没有数值评分；路由规则由 `tool_name`、`file_path`、active loop/session、当前 round、loop phase、文件类型和 allowlist 共同决定。核心保护目标是：防止 Claude 读/写/改错误 round、旧 loop、state 文件、prompt 文件、非活动 goal tracker、Finalize 阶段 contract，以及 methodology analysis 阶段的项目内容泄露。allowlist 是极窄的精确路径例外：只允许 active loop 下的 `round-1-todos.md`、`round-2-todos.md`、`round-0-summary.md`、`round-1-summary.md`，不包含 contract。

**Algorithm Subset Covered**

- 覆盖文件：`hooks/loop-read-validator.sh`、`hooks/loop-write-validator.sh`、`hooks/loop-edit-validator.sh`、`tests/test-allowlist-validators.sh`。
- 为解释焦点文件中直接调用的共享算法，额外读取了 `hooks/lib/loop-common.sh` 和 `hooks/lib/project-root.sh` 的相关 helper：输入校验、active loop 查找、round/allowlist 识别、state strict parse、goal tracker immutable-section 检查、路径 canonicalization。
- 未覆盖安装、营销、截图、通用用法文本；未运行测试，未编辑文件，未联网。

**Core State And Inputs**

- 输入：hook JSON 的 `tool_name`、`tool_input.file_path`，Write 额外可能有 `tool_input.content`，Edit 额外使用 `old_string`、`new_string`、`replace_all`，以及顶层 `session_id`。
- 派生状态：`PROJECT_ROOT`、`LOOP_BASE_DIR`、`ACTIVE_LOOP_DIR`、`STATE_FILE_TO_PARSE`、`CURRENT_ROUND`、`IS_FINALIZE_PHASE`、`FILE_PATH_LOWER`、`IS_SUMMARY_FILE`、`IS_CONTRACT_FILE`、`IS_GOAL_TRACKER`、`IN_HUMANIZE_LOOP_DIR`。
- 输出路由：`exit 0` 允许或 pass-through；`exit 1` 输入/状态结构错误；`exit 2` policy block 并输出阻断原因。
- 评分规则：无 scoring。全部是顺序 gate，先命中先返回。

**Pseudocode / Transition Table**

```text
on hook(input):
  if validator is Read/Write:
    require valid UTF-8 JSON, tool_name, depth <= 30, tool_input.file_path
  if tool_name != validator_tool:
    allow

  file_path = tool_input.file_path
  session_id = input.session_id
  active_loop = find_active_loop(project_root/.humanize/rlcr, session_id)

  if file is round-*-todos.md:
    allow only if file_path == active_loop/{round-1-todos.md|round-2-todos.md}
    otherwise block exit 2

  if Edit/Write and file is round-*-prompt.md:
    block exit 2

  if active loop is methodology-analysis phase:
    canonicalize path or fail closed on unresolved traversal/symlink
    Read:
      allow only methodology-analysis-report.md, methodology-analysis-done.md,
      methodology-analysis-state.md inside loop
      block project-root files; allow non-project external files
    Edit/Write:
      allow only methodology-analysis-report.md or methodology-analysis-done.md
      block everything else

  if file is outside this validator's protected surface:
    allow

  state_file = resolve_active_state_file(active_loop)
  strict-parse state; current_round = STATE_CURRENT_ROUND
  if malformed state:
    fail exit 1

  block direct state/finalize/methodology-state edits or writes
  if finalize phase and target is round-*-contract.md:
    block

  if goal-tracker.md:
    require exact active_loop/goal-tracker.md
    Read: allow
    Write/Edit after round > 0:
      preview proposed content
      allow only if IMMUTABLE SECTION remains identical

  if summary/contract/prompt protected round file:
    require .humanize/rlcr location where applicable
    extract round N
    allow if N == current_round or file_path is exact allowlist path
    Read/Write additionally require canonicalized path == active_loop/basename
```

**Source Evidence**

- Read/Write 做统一 JSON 防御：拒绝 null byte、非法 UTF-8、非法 JSON、缺 `tool_name`，并检查 nesting depth；Edit 没走同一 helper，只直接用 `jq` 取字段。见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:91):91-165、[hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:23):23-50、[hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:24):24-51、[hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:23):23-34。
- Active loop 是 session-aware：无 session 时只看最新 active dir；有 session 时按新到旧找该 session 的最新 state，若该 session 最新 loop 已 terminal，则返回空，避免 zombie loop 复活。见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:308):308-425。`session_id` 从 hook JSON 顶层提取，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:253):253-256。
- Active state 优先级是 `methodology-analysis-state.md`、`finalize-state.md`、`state.md`；strict parse 要求 YAML frontmatter、`current_round`、`max_iterations`、`review_started`、`base_branch`，并校验数值/布尔字段。见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:268):268-280、[hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:533):533-600。
- Round 文件识别是小写路径的 anchored regex：`round-[0-9]+-${file_type}.md$`；round number 从 `summary|prompt|todos|contract` 文件名提取。见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:797):797-814。
- Allowlist 是精确路径匹配，不是 basename 匹配：只包含 `round-1-todos.md`、`round-2-todos.md`、`round-0-summary.md`、`round-1-summary.md`，并要求 `file_path == active_loop_dir/allowed`。见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:819):819-837。测试覆盖允许项、拒绝 `round-3-todos.md`、`round-2-summary.md`、`round-0-contract.md`、错误目录同名文件，见 [tests/test-allowlist-validators.sh](/Users/wangweiyang/GitHub/humanize/tests/test-allowlist-validators.sh:72):72-132。
- Todos gate：Read/Write/Edit 对 `round-*-todos.md` 先查 active loop 和 allowlist；非 allowlist 直接 `exit 2`。见 [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:56):56-64、[hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:57):57-65、[hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:40):40-48。
- Prompt gate：Write/Edit 直接阻断 prompt 文件；Read 把 prompt 作为受限 round file，走 active loop、round、directory 校验。见 [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:67):67-70、[hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:50):50-52、[hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:175):175-186。
- Methodology Analysis gate：Edit/Write 只允许 loop 内 `methodology-analysis-report.md` 和 `methodology-analysis-done.md`；Read 允许这两个加 `methodology-analysis-state.md`，并阻断 project root 内其他文件读取。三者都做 realpath/parent fallback，并在无法 canonicalize 时对 `..` 和 symlink fail closed。见 [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:76):76-167、[hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:79):79-142、[hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:62):62-123。
- Write protected surface：非 summary/contract/finalize-summary 且不在 `.humanize/rlcr` 直接允许；loop 内非 state/goal/plan/summary/contract/finalize-summary 的普通文件也允许。见 [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:149):149-166。
- State 文件保护：Write/Edit 阻断 `methodology-analysis-state.md`、`finalize-state.md`、任何 `state.md`；匹配 helper 见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:995):995-1025，调用见 [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:202):202-215、[hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:166):166-179。
- Finalize phase：Write 允许 active loop 下精确 `finalize-summary.md`；Read/Write/Edit 在 finalize phase 阻断 contract。见 [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:223):223-233、[hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:218):218-220、[hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:181):181-183。
- Goal tracker：路径必须归一化后等于 `ACTIVE_LOOP_DIR/goal-tracker.md`；round > 0 时 Write 要求完整 `content`，Edit 先用 literal edit 预览新内容，再比较 immutable section。见 [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:227):227-245、[hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:253):253-275、[hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:204):204-239、[hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:923):923-963、[hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:968):968-991。
- Read/Write directory hardening：对用户路径和期望路径使用 `canonicalize_path_prefix`，只解析 parent、不解引用 leaf，避免 leaf symlink 把访问扩大到 loop 外；Read/Write 比较 canonicalized `FILE_PATH` 与 `ACTIVE_LOOP_DIR/basename`。见 [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:55):55-96、[hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:305):305-324、[hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:342):342-364。
- Allowlist 行为测试 fixture 把 current round 设为 5，因此 `round-5-contract.md` 是当前 round 正常允许，而不是 allowlist 例外；stale contract 被阻断。见 [tests/test-allowlist-validators.sh](/Users/wangweiyang/GitHub/humanize/tests/test-allowlist-validators.sh:53):53-62、[tests/test-allowlist-validators.sh](/Users/wangweiyang/GitHub/humanize/tests/test-allowlist-validators.sh:143):143-219、[tests/test-allowlist-validators.sh](/Users/wangweiyang/GitHub/humanize/tests/test-allowlist-validators.sh:225):225-288、[tests/test-allowlist-validators.sh](/Users/wangweiyang/GitHub/humanize/tests/test-allowlist-validators.sh:294):294-369。

**Edge Cases And Risks**

- Fail-open 情况：无法解析 `PROJECT_ROOT` 或找不到 `ACTIVE_LOOP_DIR` 时，多数 validator `exit 0`；这是为了避免无 active loop 时误拦截，但也意味着 active loop 发现失败会扩大允许面。证据见 Read `PROJECT_ROOT`/active loop fallback [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:76):76-83、200-201；Write [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:174):174-180；Edit [hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:138):138-145。
- Edit validator 没有 Read/Write 的 `validate_hook_input`、`is_deeply_nested`、`require_tool_input_field file_path` 统一校验；非法 JSON 或缺字段会由裸 `jq`/空路径路径间接处理，错误码和安全语义不一致。证据见 Edit parse [hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:23):23-34，对比 Read/Write 校验 [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:25):25-43、[hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:26):26-44。
- Edit 对 summary/contract 只校验 round number，不像 Read/Write 进一步 canonicalize 到 `ACTIVE_LOOP_DIR/basename`；因此 `.humanize/rlcr/old-loop/round-${CURRENT_ROUND}-summary.md` 这类“旧 loop 但同 round 文件”可能通过 Edit。证据：Edit 在 summary/contract gate 后直接 `exit 0`，见 [hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:246):246-275；Read/Write 有目录 canonical gate，见 [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:305):305-324、[hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:342):342-364。
- `is_in_humanize_loop_dir` 只是 grep `\.humanize/rlcr/`，不是 canonical project-root membership 判断；Read/Write 后续有 active-dir canonical gate，Edit 的部分路径没有。见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1253):1253-1256。
- Goal tracker immutable guard 对 legacy tracker fail-open：如果当前文件没有 `IMMUTABLE SECTION`，`goal_tracker_mutable_update_allowed` 直接允许。见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:960):960-962。
- Methodology phase 明确承认 spawned agents 不受同一 hook session 限制，依赖 analysis prompt 做 sanitization；这是一条设计边界，不是 validator 内强制机制。见 Read 注释 [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-read-validator.sh:79):79-82，Write/Edit 同类注释见 [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:82):82-85、[hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-edit-validator.sh:65):65-68。

**Explicitly Out Of Scope**

- `loop-bash-validator.sh` 的 Bash command parsing 和 wrapper-blocking 算法；`tests/test-allowlist-validators.sh` 包含 Bash 断言，但本 topic 是 Edit/Write/Read protected surfaces。
- 模板渲染文件内容，只把 `load_and_render_safe` 视为阻断消息输出机制。
- RLCR setup/stop/finalize 全流程、Codex review 逻辑、background task 逻辑、git add `.humanize` 保护逻辑。
- 安装文档、营销文案、截图、通用 CLI 使用说明。
- 运行测试或动态验证；本次只做 pinned commit 上的只读源码抽取。