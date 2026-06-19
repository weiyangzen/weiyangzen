**Topic and Conclusion**

Topic: `ask-codex` execution wrapper.

结论：`ask-codex.sh` 是一个一次性 Codex 调用包装器，不做迭代、不做答案评分。核心算法是：解析受控参数，将自由文本问题合并为单个 prompt，经过可执行文件、空输入、模型/effort 字符集、项目根目录等 gate 后，创建唯一运行目录和缓存目录，使用 `run_with_timeout` 执行 `codex exec`，再按 `exit_code` 与 stdout 是否为空路由到 `success`、`timeout`、`error`、`empty_response` 四类终态。`SKILL.md` 的关键机制是调用侧 shell-quoting 约束，防止 free-form 用户文本被 shell 二次解析。

Pinned source commit 已确认当前 HEAD 为 `0ec921a36b4365df503511c5567bbd3e02db0df5`。读取 git 元数据时 macOS 工具链因只读沙箱尝试写 `/tmp/xcrun_db-*` 失败并输出警告，但 `git rev-parse HEAD` 返回了该提交。

**Algorithm Subset Covered**

覆盖范围只包括：

- 包装器入口、参数解析、默认状态与校验 gate：[`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:39)
- 项目/缓存/skill 目录与运行产物生成：[`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:202)
- `codex exec` 命令构造、timeout 包装、stdout/stderr 分流：[`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:244)
- 结果路由、metadata 状态写入、最终 stdout 输出：[`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:309)
- skill 调用约束，尤其是 quoted final argument 规则：[`skills/ask-codex/SKILL.md`](/Users/wangweiyang/GitHub/humanize/skills/ask-codex/SKILL.md:14)
- mock 测试确认的行为契约：[`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:39)

状态变量：

- `QUESTION_PARTS`, `OPTIONS_DONE`, `QUESTION`：参数解析状态与最终 prompt。
- `CODEX_MODEL`, `CODEX_EFFORT`, `CODEX_TIMEOUT`：执行配置，默认来自 shared loop config 与本脚本 timeout 默认值。
- `PROJECT_ROOT`, `TIMESTAMP`, `UNIQUE_ID`, `SKILL_DIR`, `CACHE_DIR`：运行上下文与持久化路径。
- `CODEX_EXEC_ARGS`, `CODEX_AUTO_FLAG`：实际 `codex exec` 参数。
- `CODEX_STDOUT_FILE`, `CODEX_STDERR_FILE`, `CODEX_CMD_FILE`：缓存运行产物。
- `START_TIME`, `END_TIME`, `DURATION`, `CODEX_EXIT_CODE`：执行结果状态。
- metadata `status`：`success | timeout | error | empty_response`。

输入：

- CLI 参数：`--codex-model [MODEL[:EFFORT]]`、`--codex-timeout SECONDS`、`--`、question text。
- 环境：`HUMANIZE_CODEX_BYPASS_SANDBOX`、`XDG_CACHE_HOME`、`HOME`，以及 sourced libs 提供的默认模型/effort 和项目根目录解析函数。
- 外部命令：`codex`、`run_with_timeout`、`resolve_project_root`。

输出：

- stdout：仅在成功路径输出 Codex response。
- stderr：状态、错误、debug 路径、stderr 尾部。
- project-local 文件：`.humanize/skill/<unique-id>/input.md`、`output.md`、`metadata.md`。
- cache 文件：`codex-run.cmd`、`codex-run.out`、`codex-run.log`。

**Pseudocode**

```text
init:
  CODEX_MODEL  = DEFAULT_CODEX_MODEL
  CODEX_EFFORT = DEFAULT_CODEX_EFFORT
  CODEX_TIMEOUT = 3600
  QUESTION_PARTS = []
  OPTIONS_DONE = false

parse argv:
  for token in argv:
    if OPTIONS_DONE:
      append token to QUESTION_PARTS
    else if token is -h/--help:
      print help; exit 0
    else if token is --:
      OPTIONS_DONE = true
    else if token is --codex-model:
      require next arg
      if next contains ":":
        CODEX_MODEL = prefix before first colon
        CODEX_EFFORT = suffix after first colon
      else:
        CODEX_MODEL = next
        CODEX_EFFORT = DEFAULT_CODEX_EFFORT
    else if token is --codex-timeout:
      require next arg matching ^[0-9]+$
      CODEX_TIMEOUT = next
    else if token starts with "-":
      error unknown option; exit 1
    else:
      append token to QUESTION_PARTS
      OPTIONS_DONE = true

QUESTION = join QUESTION_PARTS with spaces

gates:
  require codex in PATH, else exit 1
  require QUESTION non-empty, else exit 1
  require CODEX_MODEL matches ^[a-zA-Z0-9._-]+$, else exit 1
  require CODEX_EFFORT matches ^[a-zA-Z0-9_-]+$, else exit 1
  require PROJECT_ROOT = resolve_project_root(), else exit 1

storage:
  UNIQUE_ID = timestamp + pid + 4 random bytes hex
  SKILL_DIR = PROJECT_ROOT/.humanize/skill/UNIQUE_ID
  mkdir SKILL_DIR
  CACHE_DIR = ${XDG_CACHE_HOME or ~/.cache}/humanize/<sanitized-project-path>/skill-UNIQUE_ID
  if mkdir CACHE_DIR fails:
    CACHE_DIR = SKILL_DIR/cache
    mkdir CACHE_DIR
  write input.md
  write codex-run.cmd debug file

command:
  CODEX_EXEC_ARGS = ["-m", CODEX_MODEL]
  if CODEX_EFFORT non-empty:
    append ["-c", "model_reasoning_effort=CODEX_EFFORT"]
  if HUMANIZE_CODEX_BYPASS_SANDBOX in {"true", "1"}:
    CODEX_AUTO_FLAG = "--dangerously-bypass-approvals-and-sandbox"
  else:
    CODEX_AUTO_FLAG = "--full-auto"
  append [CODEX_AUTO_FLAG, "-C", PROJECT_ROOT]

execute:
  START_TIME = now
  printf QUESTION | run_with_timeout CODEX_TIMEOUT codex exec CODEX_EXEC_ARGS -
    > codex-run.out
    2> codex-run.log
  CODEX_EXIT_CODE = shell exit code or 0
  DURATION = now - START_TIME

route:
  if CODEX_EXIT_CODE == 124:
    write metadata status=timeout, exit_code=124
    print timeout guidance to stderr
    exit 124

  if CODEX_EXIT_CODE != 0:
    write metadata status=error, exit_code=CODEX_EXIT_CODE
    print last 20 stderr lines if present
    exit CODEX_EXIT_CODE

  if codex-run.out is empty:
    write metadata status=empty_response, exit_code=0
    print last 20 stderr lines if present
    exit 1

  copy codex-run.out to SKILL_DIR/output.md
  write metadata status=success, exit_code=0
  print output.md path to stderr
  cat codex-run.out to stdout
  exit 0
```

**Transition Table**

| Phase | Gate / Condition | Action | Terminal Status |
|---|---|---|---|
| Help | `-h` or `--help` | print usage | exit `0`, no Codex run |
| Arg parse | missing option value, bad timeout, unknown option | stderr error | exit `1` |
| Prereq | `codex` absent | stderr install/retry hint | exit `1` |
| Prereq | empty `QUESTION` | stderr usage hint | exit `1` |
| Safety | invalid model chars | stderr error | exit `1` |
| Safety | invalid effort chars | stderr error | exit `1` |
| Context | cannot resolve project root | stderr error | exit `1` |
| Execute | wrapped Codex exits `124` | metadata `status: timeout` | exit `124` |
| Execute | wrapped Codex exits non-zero except `124` | metadata `status: error` | propagate exit code |
| Execute | exit `0`, stdout file empty | metadata `status: empty_response` | exit `1` |
| Execute | exit `0`, stdout non-empty | copy output, metadata `status: success`, cat stdout | exit `0` |

评分/路由规则：没有内容评分、置信度评分或多模型仲裁。唯一 routing 依据是 `CODEX_EXIT_CODE` 和 `codex-run.out` 是否非空。

**Source Evidence**

- 默认配置：`DEFAULT_ASK_CODEX_TIMEOUT=3600`，`CODEX_MODEL`/`CODEX_EFFORT` 取 shared defaults，`CODEX_TIMEOUT` 取本地默认值，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:39)。
- 参数解析使用 `OPTIONS_DONE`，第一段 positional 或 `--` 后全部进入 question text，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:86) 和 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:100)。
- `--codex-model` 支持 `MODEL:EFFORT`，否则使用默认 effort，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:105)。
- `--codex-timeout` 必须匹配 `^[0-9]+$`，错误文案称 positive integer，但正则允许 `0`，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:120)。
- question 通过 `${QUESTION_PARTS[*]}` 用空格合并，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:146)。
- prereq gates：检查 `codex`、空 question、模型字符集、effort 字符集，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:153)、[`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:162)、[`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:172)、[`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:180)。
- 项目根目录依赖 `resolve_project_root`，失败则 exit `1`，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:192)。
- `UNIQUE_ID` 由 timestamp、PID、4 字节随机 hex 构成，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:202)。
- project-local 和 cache 目录布局、home cache 不可写时 fallback 到 `SKILL_DIR/cache`，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:205) 和 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:209)。
- `input.md` 记录 question、model、effort、timeout、timestamp、tool，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:224)。
- `CODEX_EXEC_ARGS` 使用 `-m MODEL`，effort 通过 `-c model_reasoning_effort=...` 传入，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:244)。
- 自动化 flag 默认 `--full-auto`；环境变量为 `true` 或 `1` 时改为危险 bypass，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:250)。
- 命令固定加 `-C "$PROJECT_ROOT"`，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:256)。
- debug 命令文件记录 invocation 与 prompt，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:262)。
- 实际执行是 `printf '%s' "$QUESTION" | run_with_timeout "$CODEX_TIMEOUT" codex exec "${CODEX_EXEC_ARGS[@]}" -`，stdout/stderr 分别写缓存文件，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:296)。
- timeout 路径写 `status: timeout` 并 exit `124`，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:309)。
- 非零错误路径写 `status: error`，打印 stderr 尾部并传播 exit code，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:334)。
- 空 stdout 路径写 `status: empty_response`，exit `1`，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:361)。
- 成功路径 copy stdout 到 `output.md`，写 `status: success`，最后 `cat` 原 stdout 文件，见 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:391) 和 [`scripts/ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/scripts/ask-codex.sh:414)。
- `SKILL.md` 要求 free-form 用户文本不能裸 `$ARGUMENTS`，简单调用必须 `"$ARGUMENTS"`，带 flags 时 flags 分离、剩余问题作为一个 quoted final argument，见 [`skills/ask-codex/SKILL.md`](/Users/wangweiyang/GitHub/humanize/skills/ask-codex/SKILL.md:14)、[`skills/ask-codex/SKILL.md`](/Users/wangweiyang/GitHub/humanize/skills/ask-codex/SKILL.md:22)、[`skills/ask-codex/SKILL.md`](/Users/wangweiyang/GitHub/humanize/skills/ask-codex/SKILL.md:30)。
- `SKILL.md` 定义调用方解释 exit code：`0` success、`1` validation、`124` timeout、other Codex process error，见 [`skills/ask-codex/SKILL.md`](/Users/wangweiyang/GitHub/humanize/skills/ask-codex/SKILL.md:44)。
- 测试 mock Codex 消费 stdin、按环境变量输出 stdout/stderr/exit code，确认测试不触发真实 Codex，见 [`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:39)。
- 测试覆盖 validation、success output、metadata、error propagation、timeout、并发唯一目录、参数解析、cache 文件、skill quoting 指南，见 [`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:84)、[`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:164)、[`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:220)、[`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:286)、[`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:330)、[`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:382)、[`tests/test-ask-codex.sh`](/Users/wangweiyang/GitHub/humanize/tests/test-ask-codex.sh:415)。

**Edge Cases and Risks**

- `--codex-timeout` 文案说 positive integer，但正则 `^[0-9]+$` 接受 `0`。如果 `run_with_timeout 0` 的语义是立即超时或无超时，行为取决于外部 timeout wrapper；焦点文件内未定义。
- `QUESTION="${QUESTION_PARTS[*]}"` 会把多个 shell 参数用空格重组；调用方若已把 free-form question 作为一个 quoted final argument，则能保留该单参数内部内容，但多参数形式无法保留原始分隔结构。
- `--codex-model a:b:c` 会解析为 model=`a`、effort=`b:c`，随后 effort 字符集校验因冒号失败；这是隐式失败路径。
- `CODEX_MODEL` 允许点、下划线、连字符；`CODEX_EFFORT` 不允许点。若未来 effort 名称含点会被拒绝。
- `UNIQUE_ID` 使用 timestamp + PID + 4 random bytes，测试断言并发会产生不同 skill/cache dirs；碰撞概率很低但不是形式化唯一。
- debug 文件 `codex-run.cmd` 记录完整 prompt。对敏感问题，这是持久化泄露风险；脚本没有 redact 机制。
- timeout 和 error 路径不 copy `codex-run.out` 到 `output.md`，但 stdout/stderr 缓存在 cache 中。调用方若只看 project-local `output.md`，失败路径没有标准输出文件。
- `HUMANIZE_CODEX_BYPASS_SANDBOX=true|1` 会切到 `--dangerously-bypass-approvals-and-sandbox`；这是显式危险模式，仅由环境变量控制。
- 若 home cache 不可写，会 fallback 到 project-local `SKILL_DIR/cache`；这改变了缓存位置，也可能把更多运行日志放进项目目录。
- 脚本依赖 `portable-timeout.sh` 和 `loop-common.sh` 的函数/默认值，但本次按焦点路径未展开这些 shared library 的内部算法。

**What Is Explicitly Out Of Scope**

- Codex CLI 自身的推理、工具调用、sandbox 实现、timeout 实现细节。
- `portable-timeout.sh` 的跨平台 timeout 算法。
- `loop-common.sh` 中 `DEFAULT_CODEX_MODEL`、`DEFAULT_CODEX_EFFORT`、`resolve_project_root` 的内部实现。
- 安装流程、README、营销文案、截图、泛用 usage 教程。
- 真实网络调用或真实 Codex 执行结果质量评估。
- RLCR loop 或其他 Humanize hooks 的迭代机制。
- 非焦点路径中的配置加载、插件安装、shell 集成逻辑。