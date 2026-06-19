**Topic and conclusion**

Topic: `refine-plan` 的评论块提取、分类处理与 IO/结构验证机制。

结论: 该机制是一个顺序流水线，前置由 `validate-refine-plan-io.sh` 做文件、评论块、必需 `gen-plan` section、输出目录、QA 目录门禁；通过后，命令规范要求用有状态扫描器抽取非空评论块，生成无评论工作计划，按启发式分类为 `question`、`change_request`、`research_request`，再把处理结果写入 refined plan 和 QA ledger。核心不是正则替换，而是“可忽略区域 + 评论块状态 + schema 保持 + 交叉引用一致性”的验证/转换算法。

**Algorithm subset covered**

覆盖范围只包含这些算法相关文件和行为：

- `commands/refine-plan.md`: refine-plan 的阶段顺序、输入变量、验证门禁、评论提取、分类、处理、refined plan 生成、QA ledger、写入事务。
- `scripts/validate-refine-plan-io.sh`: 实际 IO 验证器、评论块计数扫描器、section 扫描器、退出码。
- `prompt-template/plan/refine-plan-qa-template.md`: QA 输出结构、ledger 字段、处理结果记录要求。
- `tests/test-refine-plan.sh`: 对提取、分类、路径、验证器退出码和边界行为的断言。

Pinned commit 已核对为 `0ec921a36b4365df503511c5567bbd3e02db0df5`。

**Pseudocode**

```text
input:
  args = --input required, --output optional, --qa-dir optional,
         --alt-language optional, --discussion | --direct optional
  annotated_plan

derive:
  INPUT_FILE = args.input
  OUTPUT_FILE = args.output or INPUT_FILE
  QA_DIR = args.qa_dir or ".humanize/plan_qa"
  QA_FILE = QA_DIR + "/" + basename(INPUT_FILE without extension) + "-qa.md"
  IN_PLACE_MODE = OUTPUT_FILE == INPUT_FILE
  REFINE_PLAN_MODE = CLI mode > config gen_plan_mode > discussion
  ALT_PLAN_LANGUAGE = CLI alt-language > config alternative_plan_language > none

gate Phase 1:
  validator(args without --alt-language)
  if exit != 0: map exit code to blocking user-facing failure and stop

extract Phase 2:
  state = {
    IN_FENCE: false, fence_marker: "",
    IN_HTML_COMMENT: false,
    IN_CMT_BLOCK: false,
    cmt_format: none,
    NEAREST_HEADING: "Preamble",
    current_comment_buffer,
    cmt_has_text,
    extracted_comments: [],
    plan_without_comments
  }

  for each line in document order:
    if outside fence/html/comment and markdown heading:
      NEAREST_HEADING = heading

    if entering/exiting ``` or ~~~ fence:
      ignore all comment markers until matching fence close

    scan line left to right:
      if IN_HTML_COMMENT:
        ignore markers until "-->"
      else if IN_CMT_BLOCK:
        append non-marker segment to comment buffer
        if nested start marker: fatal parse error
        if wrong/stray end marker: fatal parse error
        if expected end marker:
          if trimmed buffer non-empty:
            emit CMT-N with metadata
          remove block from working plan
          leave cmt state
      else:
        if "<!--": enter html ignore region
        if start marker in {CMT:, <cmt>, <comment>}:
          enter comment block with corresponding expected end marker
          preserve non-comment text before inline marker
        if stray end marker:
          fatal parse error
        otherwise preserve visible text

  if EOF while IN_CMT_BLOCK:
    fatal parse error
  if extracted_comments empty:
    stop as no non-empty CMT blocks

classify Phase 3:
  for each raw CMT-N:
    detect intents:
      question if asks why/how/what/explain/clarify or says unclear
      change_request if add/remove/delete/rewrite/restore/rename/split/merge/modify
      research_request if investigate/compare/confirm/current behavior/gather evidence/before deciding

    if multiple intents:
      split deterministic sub-items CMT-N.1, CMT-N.2...
      raw ledger ID remains CMT-N
      dominant_classification priority:
        research_request > change_request > question

    if ambiguous:
      discussion mode -> ask user
      direct mode -> choose most action-driving interpretation and record assumption

process Phase 4:
  question:
    answer in QA; optionally make minimal plan clarification only
  change_request:
    apply requested plan edits; propagate AC/task/dependency/milestone/routing references
  research_request:
    use Read/Glob/Grep only; summarize evidence; integrate clear conclusion or add DEC-N

refine Phase 5:
  REFINED_PLAN_TEXT = PLAN_WITH_COMMENTS_REMOVED + accepted refinements
  validate invariants:
    required sections present
    no comment markers remain
    referenced AC/task IDs exist
    each task has exactly one routing tag: coding or analyze
    pending decisions match convergence status

QA Phase 6:
  populate all template sections
  ledger has exactly one row per raw CMT-N in document order
  preserve original comment text verbatim in fenced blocks

write Phase 7:
  prepare all final text in memory
  write temp files in destination dirs
  if any temp/translation step fails: delete temps, leave existing outputs untouched
  replace auxiliary outputs before in-place main plan
```

**Transition table**

| State / Gate | Trigger | Transition | Output / Failure |
|---|---|---|---|
| Arg parsing | Missing `--input`, missing flag value, unknown flag, both `--discussion` and `--direct` | Stop before validation | Exit `7` from validator or command-level invalid argument |
| Input existence | `INPUT_FILE` is not a file | Stop | Exit `1`, `INPUT_NOT_FOUND` |
| Input content | file exists but size 0 | Stop | Exit `2`, `INPUT_EMPTY` |
| Comment scan | no valid non-empty block after ignoring fences/html/empty blocks | Stop | Exit `3`, `NO_COMMENT_BLOCKS` |
| Comment scan | nested start marker inside active comment | Stop | Exit `3` via parse error |
| Comment scan | stray/wrong end marker | Stop | Exit `3` via parse error |
| Comment scan | EOF while inside comment | Stop | Exit `3` via missing end marker |
| Section scan | required `gen-plan` headings absent outside ignored regions | Stop | Exit `4`, `MISSING_REQUIRED_SECTIONS` |
| Output dir | new output dir absent or not writable | Stop | Exit `5` |
| In-place output | input dir not writable | Stop | Exit `5` |
| QA dir | cannot create or not writable | Stop | Exit `6` |
| Extraction complete | at least one non-empty comment | Continue | `EXTRACTED_COMMENTS`, `PLAN_WITH_COMMENTS_REMOVED` |
| Classification ambiguous | discussion mode | Ask minimum user question | classification confirmed |
| Classification ambiguous | direct mode | Use action-driving assumption | assumption recorded in QA |
| Refinement validation | reconcilable inconsistency | repair before QA | continue |
| Refinement validation | cannot fix without inventing requirements | Stop | blocking inconsistency |
| Final write | temp write/translation failure | cleanup temps | final outputs untouched |
| Final write | partial finalization failure | restore if possible | otherwise report partial-finalization risk |

**Source evidence**

- 顺序阶段与禁止并行: `commands/refine-plan.md` 要求严格按阶段执行，不跨阶段并行；阶段包括 setup、config、IO validation、comment extraction、classification、processing、plan refinement、QA generation、atomic write。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:30), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:32), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:34).
- 计划范围不允许扩展到实现代码，写入范围限 refined plan、QA document、可选翻译变体；并且必须复用 `gen-plan` schema。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:19), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:21), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:23), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:28).
- CLI 状态变量包括 `INPUT_FILE`、`OUTPUT_FILE`、`QA_DIR`、`CLI_ALT_LANGUAGE_RAW`、discussion/direct flags；`--input` 必需，`--output` 缺省为 in-place，`--qa-dir` 缺省为 `.humanize/plan_qa`，discussion/direct 互斥。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:46), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:48), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:57).
- `QA_FILE` 从输入 basename 派生，而不是输出 basename；`--alt-language` 不传给 validator。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:65), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:68), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:72).
- 模式解析优先级是 CLI `--discussion`、CLI `--direct`、有效 config `gen_plan_mode`、默认 `discussion`；非法 config 值告警后回退。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:107), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:109), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:116).
- 语言变体解析优先级是 CLI `--alt-language`、config `alternative_plan_language`、无变体；支持固定语言表，`English/en` 为 no-op，不支持的 CLI 值停止，不支持的 config 值告警并禁用。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:118), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:120), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:126), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:140).
- validator 退出码语义: `0` 继续，`1` 输入不存在，`2` 空文件，`3` 无评论块，`4` 缺必需 sections，`5` 输出目录问题，`6` QA 目录问题，`7` 参数非法。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:157), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:165), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:4).
- validator 参数解析实际只接受 `--input`、`--output`、`--qa-dir`、`--discussion`、`--direct`、help；未知选项走 usage 并退出 `7`。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:480), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:493), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:499), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:544).
- 评论提取必须用有状态 scanner，不是 naive regex；状态包含 `IN_FENCE`、`IN_HTML_COMMENT`、`IN_CMT_BLOCK`、`NEAREST_HEADING`。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:184), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:186), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:188).
- 支持三种评论格式: `CMT:`/`ENDCMT`、`<cmt>`/`</cmt>`、`<comment>`/`</comment>`；支持 inline 和 multiline。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:197), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:199), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:203).
- 忽略 fenced code block 和 HTML comment 内的评论标记；heading 只在非 fence/html/comment 区域更新；inline 移除时保留周围非评论文本。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:223), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:225), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:226).
- 只为 trim 后非空的评论块分配 `CMT-N`，空块从工作计划中移除但不进 ledger、不消费 ID。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:227), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:228).
- 每条非空评论记录的元数据包括 ID、原文、trim 后文本、起止行列、nearest heading、location label、inline/multiline form、context excerpt。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:230), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:232).
- fatal parse errors 包括 nested start、stray/wrong end、EOF inside block；错误必须含 kind、line/column、nearest heading、context excerpt。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:244), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:246), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:252).
- 实际 validator scanner 的状态初始化包括 `count`、`in_fence`、`in_html`、`in_cmt`、`fence_marker`、`nearest_heading`、open line/column/heading/excerpt、`cmt_has_text`、`cmt_format`。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:115).
- validator 的 marker 查找表包含三种 start/end marker 以及 HTML comment markers。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:62), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:64).
- validator 在 fenced code block 中直接跳过，直到匹配 fence close；进入 fence 只在非 html/comment 状态发生。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:139), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:147).
- validator 在 active comment 中遇到 expected end marker 时，只有 `cmt_has_text` 为真才增加 count；遇到 nested start 或 wrong end marker 报错。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:182), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:209), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:227), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:232).
- validator 对 EOF 未闭合评论块输出 missing end marker parse error 并退出 awk code `2`，外层映射为验证失败 exit `3`。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:303), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:589).
- section scanner 也忽略 fenced code、HTML comment、comment block 内内容，只打印可见 heading；必需 sections 基于该可见 heading 集合验证。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:318), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:339), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:472), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:608).
- validator 的 IO gates: 输入存在、非空、至少一个有效非空评论块、必需 sections、输出目录/输入目录可写、QA 目录可创建且可写。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:573), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:581), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:589), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:608), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:639), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:662).
- 分类集合固定为 `question`、`change_request`、`research_request`；每个 raw block 必须恰好一个 primary classification。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:276), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:280).
- 分类启发式: question 对应 why/how/what/explain/clarify/unclear；change request 对应 add/remove/delete/rewrite/restore/rename/split/merge/modify；research request 对应 investigate/compare/confirm/current behavior/gather evidence/before deciding。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:288), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:532), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:537), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:542).
- 多意图 raw block 会拆成 `CMT-N.1` 等子项，但 ledger 保留 raw ID；dominant classification 优先级是 `research_request > change_request > question`。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:296), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:301), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:547).
- ambiguous classification 的路由: `discussion` 模式使用 `AskUserQuestion`；`direct` 模式选择最能驱动动作的解释并在 QA 记录假设。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:306), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:310).
- 处理规则: question 主要写 QA，只做最小澄清；change_request 直接改 refined plan 并传播一致性；research_request 只用 `Read`、`Glob`、`Grep` 做限定研究，必要时生成/更新 `DEC-N`。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:336), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:351), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:368).
- 每个 raw `CMT-N` 最终 disposition 必须是 `answered`、`applied`、`researched`、`deferred`、`resolved` 之一；原始评论文本必须按 Phase 2 捕获结果原样保存在 QA 中。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:378), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:380), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:386), [prompt-template/plan/refine-plan-qa-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/refine-plan-qa-template.md:17).
- convergence invariant: unresolved user decisions 存在时为 `partially_converged`；全部解决且无 pending decisions 时为 `converged`。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:390), [prompt-template/plan/refine-plan-qa-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/refine-plan-qa-template.md:118).
- refined plan 必须保留必需 `gen-plan` sections；可选 section 和 original design appendix 输入存在时保留。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:395), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:399), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:413).
- refined plan 验证: 无评论标记残留、引用的 `AC-*` 存在、task dependency 指向现存 task 或 `-`、每个 task row 恰好一个 `coding` 或 `analyze` routing tag、pending decisions 与 convergence status 一致。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:442), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:446).
- QA 文档必须使用模板且非可选；必须包含 Summary、Comment Ledger、Answers、Research Findings、Plan Changes Applied、Remaining Decisions、Refinement Metadata。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:457), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:461), [prompt-template/plan/refine-plan-qa-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/refine-plan-qa-template.md:1).
- QA ledger 必须按 Phase 2 的 raw `CMT-N` 文档顺序一行一个，列包含 ID、dominant classification、location、原文摘录、final disposition；子项处理写在详情区，不增加 raw ledger 行。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:473), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:475), [prompt-template/plan/refine-plan-qa-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/refine-plan-qa-template.md:7), [prompt-template/plan/refine-plan-qa-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/refine-plan-qa-template.md:11).
- final write 是事务式: 所有内容先在内存准备，temp files 写到目标目录；任一 temp/translation 失败则删 temp、保留现有 final outputs；全部 temp 成功后才替换。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:508), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:546), [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:559).
- 测试覆盖了 inline 评论计数、保留周围文本、multiline 移除、忽略 fence/html 中 marker。证据: [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:891), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:903), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:925), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:931), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:944).
- 测试覆盖了分类优先级: research over change，change over question。证据: [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:955), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:975), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:981).
- 测试覆盖了 validator 参数错误、无评论、HTML/fence marker 不计数、空评论不计数、未闭合、嵌套、缺 sections、输出/QA 目录、in-place/new-file 模式。证据: [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:1051), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:1101), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:1128), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:1155), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:1176), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:1191), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:1285).

**Edge cases and risks**

- `validate-refine-plan-io.sh` 的 `scan_cmt_blocks` 只计数有效非空评论块，不生成完整 `EXTRACTED_COMMENTS` 元数据；完整元数据和 `PLAN_WITH_COMMENTS_REMOVED` 是命令规范要求，由执行方在 Phase 2 另行实现。证据: validator 只 `print count`，见 [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:303)；命令规范要求输出 records 和 cleaned plan，见 [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:265).
- validator 的 section 必需项是 substring 检查，`"## Feasibility Hints"` 可以匹配实际 schema `"## Feasibility Hints and Suggestions"`；这是有意兼容还是宽松匹配未进一步说明。证据: required array 用 `"## Feasibility Hints"`，见 [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:608)；命令 required section 写完整 heading，见 [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:401).
- 测试中的 `scan_reference_comments` 参考提取器只实现 classic `CMT:`/`ENDCMT` 路径，而正式命令和 validator 支持三种格式；因此测试 reference scanner 对 `<cmt>`/`<comment>` 的算法覆盖不足。证据: reference scanner 只查找 `CMT:`/`ENDCMT`，见 [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:463), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:505)；正式要求三格式，见 [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:199).
- validator 将 HTML comment marker 出现在 active CMT 内时计为 `cmt_has_text` 并进入 HTML ignore 状态；这意味着评论内部的 `<!-- ... -->` 会让该评论视为非空，即使可见文本为空。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:202).
- `stray_end` 同时覆盖“外部孤立 end marker”和“active comment 内 wrong end marker”，错误文案统一为 stray comment end marker；对用户来说可定位，但不区分 wrong-format end。证据: [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:232), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:294).
- 分类启发式是关键词优先级，没有数值评分；复杂自然语言可能落入 `ambiguous`，discussion 模式需用户确认，direct 模式会记录假设。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:306), [tests/test-refine-plan.sh](/Users/wangweiyang/GitHub/humanize/tests/test-refine-plan.sh:547).
- refined plan 后置验证里 AC/task 引用、routing tag、convergence status 的一致性是命令规范要求；当前 validator 前置脚本不执行这些深层 plan 语义检查。证据: validator gates 结束在 IO/section/dir validation，见 [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:680)；后置验证规范在 command Phase 5，见 [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:442).
- 命令文档要求所有 writes 发生在 Phase 7，validator 允许提前创建 `QA_DIR` 且命令把它视为 expected setup；这是一个明确例外。证据: [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:176), [scripts/validate-refine-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-refine-plan-io.sh:662).

**What is explicitly out of scope**

- 不覆盖安装、marketplace、plugin metadata、README 版本一致性、Claude/Codex/Kimi 安装文档 wiring；这些在测试文件存在，但不属于评论提取与验证算法。
- 不覆盖截图、营销文案、普通用户使用教程。
- 不覆盖实际实现业务代码修改；`refine-plan` 明确仅处理 plan artifacts，不实现 repository code。
- 不覆盖 RLCR 自动启动；命令明确 v1 不自动启动 RLCR。
- 不覆盖新 plan schema 设计；refined plan 必须复用现有 `gen-plan` schema。
- 不覆盖网络研究；`research_request` 的范围是 repository 内 `Read`、`Glob`、`Grep`，且本次研究也未运行网络搜索。