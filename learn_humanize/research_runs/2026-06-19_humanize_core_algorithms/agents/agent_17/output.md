**Topic and conclusion**

`ask-gemini` 是一个一次性 Gemini CLI 执行包装器：它解析少量 CLI 参数，构造带“必须使用 Google Search”前缀的增强 prompt，以超时保护调用 `gemini -p`，把 Gemini stdout 作为主结果返回，同时把输入、调试命令、stdout/stderr 和元数据落到 `.humanize/skill/...` 与 cache 目录。核心路由不是评分算法，而是基于参数校验、环境变量、缓存可写性、Gemini 退出码和 stdout 是否为空的状态机。

已确认仓库 HEAD 为 pinned commit `0ec921a36b4365df503511c5567bbd3e02db0df5`。

**Algorithm subset covered**

覆盖文件：

- `scripts/ask-gemini.sh`：实际执行状态机、参数解析、校验、prompt 增强、Gemini 调用、结果分类。
- `skills/ask-gemini/SKILL.md`：Claude/skill 层如何安全调用脚本、如何解释 stdout/stderr 和退出码。
- `docs/usage.md`：未发现 `ask-gemini`/Gemini 专属行为定义；其中相关环境变量章节是 Codex sandbox，不参与本 wrapper。

核心输入：

- CLI：`--gemini-model MODEL`、`--gemini-timeout SECONDS`、`--`、free-form question/task。
- 环境：`HUMANIZE_GEMINI_YOLO`、`XDG_CACHE_HOME`、`HOME`、间接使用 `CLAUDE_PROJECT_DIR`/git root resolver。
- 外部命令：`gemini` 必须在 `PATH` 中。
- 共享函数：`run_with_timeout`、`resolve_project_root`，本次按 wrapper 调用点分析，不展开其内部实现。

核心状态变量：

- 配置：`GEMINI_MODEL`、`GEMINI_TIMEOUT`
- 参数解析：`QUESTION_PARTS`、`OPTIONS_DONE`、`QUESTION`
- 路径：`PROJECT_ROOT`、`TIMESTAMP`、`UNIQUE_ID`、`SKILL_DIR`、`CACHE_DIR`
- Gemini 调用：`GEMINI_ARGS`、`AUGMENTED_PROMPT`
- 日志文件：`GEMINI_CMD_FILE`、`GEMINI_STDOUT_FILE`、`GEMINI_STDERR_FILE`
- 执行结果：`START_TIME`、`END_TIME`、`DURATION`、`GEMINI_EXIT_CODE`

**Pseudocode**

```text
init:
  source portable-timeout.sh
  source project-root.sh
  GEMINI_MODEL = "gemini-3.1-pro-preview"
  GEMINI_TIMEOUT = 3600
  QUESTION_PARTS = []
  OPTIONS_DONE = false

parse argv:
  for each arg:
    if OPTIONS_DONE:
      append arg to QUESTION_PARTS
    else if arg == -h or --help:
      print help; exit 0
    else if arg == --:
      OPTIONS_DONE = true
    else if arg == --gemini-model:
      require next value
      GEMINI_MODEL = next
    else if arg == --gemini-timeout:
      require next value
      require next matches ^[0-9]+$
      GEMINI_TIMEOUT = next
    else if arg starts with "-":
      error unknown option; exit 1
    else:
      append arg to QUESTION_PARTS
      OPTIONS_DONE = true

QUESTION = join QUESTION_PARTS with spaces

validation gates:
  if gemini not in PATH: exit 1
  if QUESTION empty: exit 1
  if GEMINI_MODEL not matches ^[a-zA-Z0-9._-]+$: exit 1
  PROJECT_ROOT = resolve_project_root() else exit 1

storage:
  UNIQUE_ID = timestamp + pid + random hex
  SKILL_DIR = PROJECT_ROOT/.humanize/skill/UNIQUE_ID
  mkdir SKILL_DIR
  CACHE_DIR = XDG_CACHE_HOME or HOME/.cache path
  if mkdir CACHE_DIR fails:
    CACHE_DIR = SKILL_DIR/cache
    mkdir CACHE_DIR
  write input.md

command construction:
  GEMINI_ARGS = ["-m", GEMINI_MODEL]
  if HUMANIZE_GEMINI_YOLO in {"true","1"}:
    append "--yolo"
  else:
    append "--sandbox"
  append "-o", "text"

  AUGMENTED_PROMPT =
    "You MUST use Google Search ..." + delimiter + QUESTION

  write gemini-run.cmd debug file

execute:
  START_TIME = now
  GEMINI_EXIT_CODE = 0
  run_with_timeout GEMINI_TIMEOUT gemini GEMINI_ARGS -p AUGMENTED_PROMPT
    stdout -> gemini-run.out
    stderr -> gemini-run.log
    on failure: GEMINI_EXIT_CODE = process exit code
  DURATION = now - START_TIME

classify:
  if GEMINI_EXIT_CODE == 124:
    write metadata status=timeout
    print timeout guidance to stderr
    exit 124

  if GEMINI_EXIT_CODE != 0:
    write metadata status=error
    print last 20 stderr log lines if present
    exit GEMINI_EXIT_CODE

  if stdout file is empty:
    write metadata status=empty_response
    print last 20 stderr log lines if present
    exit 1

  copy stdout to SKILL_DIR/output.md
  write metadata status=success
  print saved path to stderr
  cat stdout file to stdout
  exit 0
```

**Transition table**

| State | Gate / event | Next state | Output / side effect |
|---|---|---|---|
| init | defaults assigned | parse args | model=`gemini-3.1-pro-preview`, timeout=`3600` |
| parse args | `--gemini-model` with value | parse args | update `GEMINI_MODEL` |
| parse args | `--gemini-timeout` numeric | parse args | update `GEMINI_TIMEOUT` |
| parse args | first non-option | question mode | remaining args become question parts |
| parse args | unknown `-*` | terminal error | exit `1` |
| validate | missing `gemini` | terminal error | exit `1` |
| validate | empty question | terminal error | exit `1` |
| validate | invalid model chars | terminal error | exit `1` |
| validate | no project root | terminal error | exit `1` |
| storage | home cache mkdir fails | cache fallback | use `$SKILL_DIR/cache` |
| build command | `HUMANIZE_GEMINI_YOLO=true/1` | yolo route | add `--yolo` |
| build command | otherwise | sandbox route | add `--sandbox` |
| execute | exit code `124` | timeout failure | metadata `status: timeout`, exit `124` |
| execute | exit code nonzero | process failure | metadata `status: error`, exit same code |
| execute | exit `0` + empty stdout | semantic failure | metadata `status: empty_response`, exit `1` |
| execute | exit `0` + nonempty stdout | success | copy output, metadata `success`, stdout response |

**Source evidence**

- 脚本定义用途：一次性非交互 Gemini 咨询，stdout 返回 Gemini 响应，stderr 返回状态信息，存储位置包括 `.humanize/skill/...` 与 cache：`scripts/ask-gemini.sh:3`、`scripts/ask-gemini.sh:5`、`scripts/ask-gemini.sh:13`、`scripts/ask-gemini.sh:16`。
- 默认模型和超时：`DEFAULT_GEMINI_MODEL="gemini-3.1-pro-preview"`、`DEFAULT_ASK_GEMINI_TIMEOUT=3600`，并赋给运行状态变量：`scripts/ask-gemini.sh:39`、`scripts/ask-gemini.sh:40`、`scripts/ask-gemini.sh:42`、`scripts/ask-gemini.sh:43`。
- 参数解析规则：`--gemini-model` 必须带值，`--gemini-timeout` 必须匹配数字，未知 option 退出，首个非 option 之后切入 question mode：`scripts/ask-gemini.sh:91`、`scripts/ask-gemini.sh:105`、`scripts/ask-gemini.sh:113`、`scripts/ask-gemini.sh:118`、`scripts/ask-gemini.sh:125`、`scripts/ask-gemini.sh:130`。
- question 合并方式是 shell 数组按空格 join：`scripts/ask-gemini.sh:138`、`scripts/ask-gemini.sh:139`。
- 前置校验：要求 `gemini` 在 `PATH`，question 非空，model 只允许 alnum/`._-`，项目根必须可解析：`scripts/ask-gemini.sh:145`、`scripts/ask-gemini.sh:153`、`scripts/ask-gemini.sh:162`、`scripts/ask-gemini.sh:174`。
- 存储目录：`UNIQUE_ID` 由时间戳、PID、随机 hex 组成；project-local 目录为 `.humanize/skill/$UNIQUE_ID`；cache 目录按 project path sanitize，home cache 不可写则回退到 `$SKILL_DIR/cache`：`scripts/ask-gemini.sh:184`、`scripts/ask-gemini.sh:185`、`scripts/ask-gemini.sh:188`、`scripts/ask-gemini.sh:192`、`scripts/ask-gemini.sh:195`。
- input 记录 question、model、timeout、timestamp、tool：`scripts/ask-gemini.sh:205`、`scripts/ask-gemini.sh:208`、`scripts/ask-gemini.sh:214`。
- Gemini 参数构造：始终 `-m MODEL`；`HUMANIZE_GEMINI_YOLO=true/1` 走 `--yolo`，否则默认 `--sandbox`；输出格式强制 `-o text`：`scripts/ask-gemini.sh:224`、`scripts/ask-gemini.sh:226`、`scripts/ask-gemini.sh:227`、`scripts/ask-gemini.sh:230`、`scripts/ask-gemini.sh:233`。
- 增强 prompt 始终前置 Google Search 指令，再拼接原 question：`scripts/ask-gemini.sh:236`、`scripts/ask-gemini.sh:237`、`scripts/ask-gemini.sh:241`。
- 调试命令文件记录时间、工作目录、timeout、命令模板和 prompt：`scripts/ask-gemini.sh:247`、`scripts/ask-gemini.sh:251`、`scripts/ask-gemini.sh:257`、`scripts/ask-gemini.sh:260`。
- 实际调用通过 `run_with_timeout "$GEMINI_TIMEOUT" gemini "${GEMINI_ARGS[@]}" -p "$AUGMENTED_PROMPT"`，stdout/stderr 分流到 cache 文件，失败时捕获退出码：`scripts/ask-gemini.sh:279`、`scripts/ask-gemini.sh:281`、`scripts/ask-gemini.sh:282`、`scripts/ask-gemini.sh:283`、`scripts/ask-gemini.sh:288`。
- 结果分类：`124` timeout，非零 error，零退出但 stdout 为空为 `empty_response`，成功时复制 stdout 到 `output.md` 并 cat 到 stdout：`scripts/ask-gemini.sh:294`、`scripts/ask-gemini.sh:316`、`scripts/ask-gemini.sh:340`、`scripts/ask-gemini.sh:368`、`scripts/ask-gemini.sh:370`、`scripts/ask-gemini.sh:388`。
- Skill 层限制 allowed tool 到脚本路径，并要求 free-form 用户文本必须 quoted，flags 单独作为 shell 参数，question 作为最后一个 quoted 参数；明确禁止 unquoted `$ARGUMENTS`：`skills/ask-gemini/SKILL.md:5`、`skills/ask-gemini/SKILL.md:17`、`skills/ask-gemini/SKILL.md:25`、`skills/ask-gemini/SKILL.md:33`、`skills/ask-gemini/SKILL.md:36`。
- Skill 层输出/退出码契约：stdout 是 Gemini response，stderr 是状态信息；`0` success，`1` validation error，`124` timeout，其他为 Gemini process error：`skills/ask-gemini/SKILL.md:41`、`skills/ask-gemini/SKILL.md:43`、`skills/ask-gemini/SKILL.md:50`、`skills/ask-gemini/SKILL.md:52`。
- Skill 层重复确认默认模型、默认超时和 Google Search 指令：`skills/ask-gemini/SKILL.md:59`、`skills/ask-gemini/SKILL.md:60`、`skills/ask-gemini/SKILL.md:61`。
- `docs/usage.md` 中相关可见环境变量章节是 Codex sandbox，变量名为 `HUMANIZE_CODEX_BYPASS_SANDBOX`，不是 Gemini wrapper 的输入：`docs/usage.md:329`、`docs/usage.md:331`、`docs/usage.md:335`、`docs/usage.md:338`。

**Edge cases and risks**

- `--gemini-timeout` 的错误文案称必须是 positive integer，但正则 `^[0-9]+$` 接受 `0`；`0` 的真实语义取决于 `run_with_timeout` 实现，本文件未定义。
- Google Search 是 prompt 级约束，不是 wrapper 可验证的不变量；脚本不会检查 Gemini 是否真的搜索、是否给出引用、引用是否有效。
- 首个非 option 参数后，所有后续参数都被当作 question；因此 question 之后的 `--gemini-timeout` 不会再被解析成 option。
- `QUESTION="${QUESTION_PARTS[*]}"` 会用空格合并多个参数；如果调用方没有按 skill 要求把 free-form question 作为一个 quoted 参数传入，原始 shell quoting/newline 语义可能丢失。
- project-local `.humanize/skill/...` 创建失败、input/debug/metadata 写入失败会受 `set -euo pipefail` 影响直接中止；这类写入失败没有专门的 metadata 状态。
- home cache 不可写有 fallback，但 project-local 目录不可写没有 fallback。
- `HUMANIZE_GEMINI_YOLO=true/1` 会把 Gemini 切到 `--yolo` 自动批准模式；默认才是 `--sandbox`。
- `gemini-run.cmd` 是调试记录，不是可安全复制执行的完整 shell-escaped 命令；它用 `"gemini ${GEMINI_ARGS[*]} -p \"<prompt>\""` 记录模板。
- timeout、process error 和 empty stdout 三类失败都会保留 cache logs，但 skill 层要求调用方把非零退出报告给用户，不定义自动重试。
- `epoch_to_iso` 对 GNU/BSD `date` 做兼容；都失败时写 `unknown`，不会阻塞主流程。

**What is explicitly out of scope**

- 不分析 Gemini CLI 内部模型行为、搜索实现、citation 质量或联网策略。
- 不展开 `scripts/portable-timeout.sh` 的 timeout 实现，也不展开 `hooks/lib/project-root.sh` 的 root 解析细节；这里只按 `ask-gemini.sh` 的调用契约建模。
- 不覆盖安装说明、marketing 文案、示例问题本身、截图或通用 Humanize usage。
- 不把 `docs/usage.md` 的 Codex sandbox 环境变量当作 Gemini wrapper 行为；Gemini wrapper 使用的是 `HUMANIZE_GEMINI_YOLO`。
- 不运行 Gemini、不执行网络搜索、不验证外部 Google Search 结果。