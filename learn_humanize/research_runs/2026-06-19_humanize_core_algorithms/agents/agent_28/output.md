**Topic And Conclusion**

主题：Path validation and injection resistance。检查范围基于 pinned commit `0ec921a36b4365df503511c5567bbd3e02db0df5`，只读读取确认当前 `.git/HEAD` 指向该提交。

结论：核心机制是“两层防线”：

1. 启动期 `setup-rlcr-loop.sh` 对 plan path 做拒绝式校验：必须是项目内相对路径、无空白、无常见 shell/YAML/通配元字符、leaf 和父目录均不得为 symlink、真实路径不得逃出项目、不得位于 submodule，并附带 git tracking/content gates。
2. 运行期 `loop-bash-validator.sh` 对 Bash hook 命令做基于活跃 RLCR loop/session 的拦截：阻止直接执行关键 hook、阻止修改 `.humanize/rlcr` 状态/备份/summary/contract/todos 等文件，并在 methodology analysis 阶段进一步禁止写命令、脚本执行、解释器、构建工具和输出重定向。

整体设计偏 fail-closed，但仍依赖 Bash regex/字符串解析和检查后再使用路径，存在 TOCTOU 与未覆盖字符类别的残余风险。

**Algorithm Subset Covered**

覆盖文件：

- [hooks/lib/project-root.sh:41](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:41)：项目根目录解析与路径规范化 helper。
- [scripts/setup-rlcr-loop.sh:39](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:39)：plan path 输入、校验、tracking/content gates、状态 YAML 写入前安全检查。
- [hooks/loop-bash-validator.sh:22](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:22)：Bash hook 命令面注入/绕过防护。
- [tests/robustness/test-path-validation-robustness.sh:76](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:76)：生产 path validation 的正反向鲁棒性样本。

显式跳过：安装说明、营销/截图、泛用 usage 文案；只保留定义行为的 usage/错误处理片段。

**Pseudocode Or Transition Table**

```text
resolve_project_root():
  root := CLAUDE_PROJECT_DIR
  if root empty:
    root := git rev-parse --show-toplevel
  if root empty:
    return failure
  return canonicalize_path(root)
```

```text
validate_plan_input(PLAN_FILE, PROJECT_ROOT, flags):
  merge positional PLAN_FILE and --plan-file
  if both supplied: reject
  if PLAN_FILE missing:
    if --skip-impl: use internal placeholder and skip plan validation
    else reject

  require git repo and at least one commit

  if not skip-placeholder:
    if PLAN_FILE starts with "/": reject
    if PLAN_FILE contains whitespace: reject
    if PLAN_FILE contains ; & | $ ` < > ( ) { } [ ] ! # ~ * ? \ : reject

    FULL_PLAN_PATH := PROJECT_ROOT + "/" + PLAN_FILE
    if FULL_PLAN_PATH is symlink: reject
    PLAN_DIR := dirname(FULL_PLAN_PATH)
    if PLAN_DIR does not exist: reject

    CHECK_PATH := PROJECT_ROOT
    for each parent segment in dirname(PLAN_FILE):
      CHECK_PATH := CHECK_PATH + "/" + segment
      if CHECK_PATH is symlink: reject

    if FULL_PLAN_PATH is not regular file: reject
    if FULL_PLAN_PATH is not readable: reject

    RESOLVED_PLAN_DIR := cd PLAN_DIR && pwd
    REAL_PLAN_PATH := RESOLVED_PLAN_DIR + "/" + basename(FULL_PLAN_PATH)
    if REAL_PLAN_PATH not under PROJECT_ROOT + "/": reject

    if .gitmodules exists:
      for each git submodule path:
        if PLAN_FILE == submodule or starts with submodule + "/": reject

    PLAN_IS_TRACKED := git ls-files --error-unmatch PLAN_FILE
    if git status/ls-files timeout: reject
    if --track-plan-file:
      require tracked and clean
    else:
      require not tracked

    require wc -l >= 5
    require at least 3 nonblank, non-comment content lines
```

```text
validate_yaml_sensitive_state_values():
  START_BRANCH := git rev-parse --abbrev-ref HEAD
  reject START_BRANCH containing : # " ' ` newline
  reject BASE_BRANCH containing : # " ' ` newline
  reject CODEX_MODEL unless /^[a-zA-Z0-9._-]+$/
  write unquoted YAML keys: plan_file, start_branch, base_branch, etc.
```

```text
validate_bash_hook(HOOK_INPUT):
  require valid JSON, not deeply nested
  if tool_name != Bash: allow
  require tool_input.command
  COMMAND_LOWER := lowercase(command)

  PROJECT_ROOT := resolve_project_root()
  if no project root: allow
  ACTIVE_LOOP_DIR := find_active_loop(PROJECT_ROOT/.humanize/rlcr, session_id)

  if active loop has methodology-analysis-state.md:
    allow leading cancel-rlcr-loop.sh only when no shell metachar/injection operator
    reject git write commands
    reject file manipulation commands
    reject in-place editors
    reject interpreters
    reject shell script execution/source/direct scripts
    reject build tools
    reject file output redirection except selected /dev/fd cases

  if no active loop: allow

  reject direct manual execution of loop-codex-stop-hook.sh or rlcr-stop-gate.sh,
  including common wrappers: env, command, timeout, nice, nohup, strace/ltrace

  parse active state strictly; if malformed: reject
  if push_every_round != true and command is git push: reject
  reject git add targeting .humanize

  reject writes to methodology-analysis-state.md, finalize-state.md, state.md
  also reject mv/cp FROM those state files:
    split command on shell operators
    preserve/strip leading redirections carefully
    match mv/cp source patterns
    also inspect sh/bash -c payloads

  reject Bash modification of plan backup, goal-tracker, prompt, summary,
  round contract, and scoped todos files.
```

**Source Evidence**

- 项目根目录解析优先级是 `CLAUDE_PROJECT_DIR`、`git rev-parse --show-toplevel`、失败返回；注释明确不以 `pwd` 作为 fallback，避免 `cd` 漂移：[hooks/lib/project-root.sh:5](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:5)、[hooks/lib/project-root.sh:10](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:10)。
- `resolve_project_root` 读取 `CLAUDE_PROJECT_DIR`，为空时调用 git，失败返回 1，并经 `canonicalize_path` 输出规范路径：[hooks/lib/project-root.sh:41](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:41)、[hooks/lib/project-root.sh:44](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:44)、[hooks/lib/project-root.sh:51](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:51)。
- `canonicalize_path_prefix` 只解析父目录 symlink 并原样拼回 basename，适用于“用户路径 vs 期望文件名”的比较：[hooks/lib/project-root.sh:55](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:55)、[hooks/lib/project-root.sh:82](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:82)。
- `canonicalize_path` 明确提示 leaf 存在时会解引用 symlink，不应用于授权用户给定路径到期望文件名：[hooks/lib/project-root.sh:106](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:106)。
- setup 参数状态变量包括 `PLAN_FILE`、`PLAN_FILE_EXPLICIT`、`TRACK_PLAN_FILE`：[scripts/setup-rlcr-loop.sh:39](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:39)。
- `--plan-file` 写入 `PLAN_FILE_EXPLICIT`，普通 positional arg 写入 `PLAN_FILE`，多 plan 文件会拒绝：[scripts/setup-rlcr-loop.sh:236](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:236)、[scripts/setup-rlcr-loop.sh:309](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:309)。
- 显式 plan 与 positional plan 不能同时存在；显式 plan 会合并为统一 `PLAN_FILE`：[scripts/setup-rlcr-loop.sh:399](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:399)、[scripts/setup-rlcr-loop.sh:404](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:404)。
- 无 plan 时，只有 `--skip-impl` 可走内部 placeholder，否则拒绝：[scripts/setup-rlcr-loop.sh:409](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:409)、[scripts/setup-rlcr-loop.sh:420](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:420)。
- plan path 拒绝绝对路径、空白字符、shell metacharacters；实际拒绝集合为 `; & | $ ` < > ( ) { } [ ] ! # ~ * ? \`：[scripts/setup-rlcr-loop.sh:455](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:455)、[scripts/setup-rlcr-loop.sh:461](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:461)、[scripts/setup-rlcr-loop.sh:469](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:469)。
- full path 用 `PROJECT_ROOT/PLAN_FILE` 构造，随后拒绝 leaf symlink：[scripts/setup-rlcr-loop.sh:478](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:478)、[scripts/setup-rlcr-loop.sh:481](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:481)。
- 父目录必须存在，并逐段检查父目录 symlink，注释说明是为了阻止 symlink path traversal：[scripts/setup-rlcr-loop.sh:487](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:487)、[scripts/setup-rlcr-loop.sh:494](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:494)、[scripts/setup-rlcr-loop.sh:508](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:508)。
- 文件必须存在、是普通文件且可读：[scripts/setup-rlcr-loop.sh:517](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:517)、[scripts/setup-rlcr-loop.sh:523](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:523)。
- containment gate 通过 `cd PLAN_DIR && pwd` 得到 `REAL_PLAN_PATH`，要求其前缀为 `PROJECT_ROOT/`：[scripts/setup-rlcr-loop.sh:529](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:529)、[scripts/setup-rlcr-loop.sh:532](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:532)、[scripts/setup-rlcr-loop.sh:538](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:538)。
- `.gitmodules` 存在时才检查 submodule，plan path 等于或位于 submodule path 下会拒绝：[scripts/setup-rlcr-loop.sh:543](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:543)、[scripts/setup-rlcr-loop.sh:550](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:550)。
- git status / ls-files 超时 fail-closed；`--track-plan-file` 要求 tracked 且 clean，默认要求不 tracked：[scripts/setup-rlcr-loop.sh:562](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:562)、[scripts/setup-rlcr-loop.sh:574](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:574)、[scripts/setup-rlcr-loop.sh:582](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:582)、[scripts/setup-rlcr-loop.sh:598](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:598)。
- content gate 要求至少 5 行，并至少 3 行非空、非 `#`、非 HTML comment 内容：[scripts/setup-rlcr-loop.sh:618](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:618)、[scripts/setup-rlcr-loop.sh:628](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:628)、[scripts/setup-rlcr-loop.sh:666](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:666)。
- 分支名写入 YAML 前拒绝 `: # " ' ` newline`；base branch 同样校验：[scripts/setup-rlcr-loop.sh:692](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:692)、[scripts/setup-rlcr-loop.sh:799](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:799)。
- state YAML 以未加引号的 plain scalar 写入 `plan_file`、`start_branch`、`base_branch` 等字段，因此前置校验是注入防线的一部分：[scripts/setup-rlcr-loop.sh:880](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:880)、[scripts/setup-rlcr-loop.sh:889](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:889)。
- Bash validator 只处理 Bash tool：读取 JSON、校验结构、拒绝深嵌套，非 Bash 直接允许：[hooks/loop-bash-validator.sh:22](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:22)、[hooks/loop-bash-validator.sh:25](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:25)、[hooks/loop-bash-validator.sh:36](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:36)。
- Bash command 被转小写后参与规则匹配；project root 解析失败时 hook `exit 0`：[hooks/loop-bash-validator.sh:45](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:45)、[hooks/loop-bash-validator.sh:52](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:52)。
- active loop 按 session id 过滤，注释明确不得 fallback 到未过滤 search，避免限制同 repo 其他 session：[hooks/loop-bash-validator.sh:55](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:55)、[hooks/loop-bash-validator.sh:77](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:77)。
- methodology analysis 阶段的 cancel allowlist 会先拒绝 `; | & backtick > < $(...) newline` 等 shell meta，再允许 leading `cancel-rlcr-loop.sh`：[hooks/loop-bash-validator.sh:89](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:89)、[hooks/loop-bash-validator.sh:96](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:96)、[hooks/loop-bash-validator.sh:102](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:102)。
- methodology analysis 阶段阻止 git write、文件修改命令、in-place edit、解释器、shell script、build tool、source/direct script、文件重定向：[hooks/loop-bash-validator.sh:107](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:107)、[hooks/loop-bash-validator.sh:113](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:113)、[hooks/loop-bash-validator.sh:120](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:120)、[hooks/loop-bash-validator.sh:127](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:127)、[hooks/loop-bash-validator.sh:134](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:134)、[hooks/loop-bash-validator.sh:141](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:141)、[hooks/loop-bash-validator.sh:148](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:148)、[hooks/loop-bash-validator.sh:155](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:155)、[hooks/loop-bash-validator.sh:162](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:162)。
- 无 active loop 时 Bash 全放行：[hooks/loop-bash-validator.sh:173](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:173)。
- 直接执行 `loop-codex-stop-hook.sh` 或 `rlcr-stop-gate.sh` 会被拦截，且 pattern 覆盖 env/command/timeout/nice/nohup/trace 等 wrapper：[hooks/loop-bash-validator.sh:184](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:184)、[hooks/loop-bash-validator.sh:197](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:197)、[hooks/loop-bash-validator.sh:199](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:199)。
- active loop 下 state 文件 strict parse 失败会阻断：[hooks/loop-bash-validator.sh:213](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:213)。
- `push_every_round != true` 时阻断 `git push`：[hooks/loop-bash-validator.sh:228](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:228)。
- `.humanize` git add 被单独阻断，防止 `git add -f` 绕过 ignore：[hooks/loop-bash-validator.sh:241](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:241)、[hooks/loop-bash-validator.sh:247](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:247)。
- state/finalize/methodology state 修改通过 `command_modifies_file` gate 阻断；授权 cancel 是例外：[hooks/loop-bash-validator.sh:271](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:271)、[hooks/loop-bash-validator.sh:280](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:280)、[hooks/loop-bash-validator.sh:290](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:290)。
- 为捕获 `mv/cp state.md /tmp/foo` 这类 source-side 绕过，命令会按 shell operators 分段，并剥离 leading redirections 后匹配 source pattern：[hooks/loop-bash-validator.sh:299](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:299)、[hooks/loop-bash-validator.sh:310](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:310)、[hooks/loop-bash-validator.sh:321](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:321)、[hooks/loop-bash-validator.sh:350](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:350)、[hooks/loop-bash-validator.sh:428](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:428)。
- `sh -c` / `bash -c` payload 中含 `mv|cp ... state.md` 也会被二次检测：[hooks/loop-bash-validator.sh:458](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:458)、[hooks/loop-bash-validator.sh:461](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:461)。
- plan backup、goal tracker、prompt、summary、round contract、todos 的 Bash 修改分别阻断：[hooks/loop-bash-validator.sh:496](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:496)、[hooks/loop-bash-validator.sh:509](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:509)、[hooks/loop-bash-validator.sh:524](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:524)、[hooks/loop-bash-validator.sh:534](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:534)、[hooks/loop-bash-validator.sh:546](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:546)、[hooks/loop-bash-validator.sh:561](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:561)。
- robustness test 通过 `CLAUDE_PROJECT_DIR="$TEST_DIR" bash setup-rlcr-loop.sh "$plan_path"` 调生产脚本，并用错误输出判断 path/content validation 是否失败：[tests/robustness/test-path-validation-robustness.sh:76](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:76)、[tests/robustness/test-path-validation-robustness.sh:88](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:88)、[tests/robustness/test-path-validation-robustness.sh:93](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:93)。
- 正向 path 样本覆盖普通相对路径、根目录文件、dash/underscore、嵌套目录、文件名 dots：[tests/robustness/test-path-validation-robustness.sh:122](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:122)、[tests/robustness/test-path-validation-robustness.sh:131](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:131)、[tests/robustness/test-path-validation-robustness.sh:141](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:141)、[tests/robustness/test-path-validation-robustness.sh:151](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:151)、[tests/robustness/test-path-validation-robustness.sh:161](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:161)。
- 反向 path 样本覆盖绝对路径、空格、`; | $ backtick < > & * ? \ ~ ( ) { } [ ] # !`：[tests/robustness/test-path-validation-robustness.sh:179](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:179)、[tests/robustness/test-path-validation-robustness.sh:188](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:188)、[tests/robustness/test-path-validation-robustness.sh:199](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:199)、[tests/robustness/test-path-validation-robustness.sh:217](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:217)、[tests/robustness/test-path-validation-robustness.sh:325](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:325)。
- symlink 样本覆盖 leaf symlink、父目录 symlink、symlink chain：[tests/robustness/test-path-validation-robustness.sh:342](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:342)、[tests/robustness/test-path-validation-robustness.sh:352](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:352)、[tests/robustness/test-path-validation-robustness.sh:367](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:367)。
- 长文件名、10 层深路径被视为应接受；注释说明 Unicode/CJK/Emoji path 当前允许：[tests/robustness/test-path-validation-robustness.sh:387](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:387)、[tests/robustness/test-path-validation-robustness.sh:402](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:402)、[tests/robustness/test-path-validation-robustness.sh:414](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:414)。
- 内容/存在性反向样本覆盖空文件、comments-only、少于 5 行、不存在、目录冒充文件：[tests/robustness/test-path-validation-robustness.sh:425](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:425)、[tests/robustness/test-path-validation-robustness.sh:434](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:434)、[tests/robustness/test-path-validation-robustness.sh:450](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:450)、[tests/robustness/test-path-validation-robustness.sh:463](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:463)、[tests/robustness/test-path-validation-robustness.sh:472](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:472)。

**Edge Cases And Risks**

- `PLAN_FILE` 的错误提示说“only alphanumeric, dash, underscore, dot, and slash”，但实现是 deny-list，不是严格 allow-list；它允许 Unicode，以及未被列入拒绝集的 `:`、引号、逗号、加号、等号、百分号、`@` 等字符。Unicode 允许是测试注释明确行为：[tests/robustness/test-path-validation-robustness.sh:414](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-path-validation-robustness.sh:414)。这不一定直接等于 shell injection，但对 YAML/plain prompt 语义仍是残余面。
- 分支名有 YAML 安全校验，但 `plan_file` 同样以 unquoted YAML 写入；plan path 拒绝了 `# ! & * [ ] { } backtick` 和空白，但没有像 branch 一样拒绝 `:` 或引号。因为空格被拒绝，典型 `key: value` 注入受限；但 YAML parser 兼容性和以 `@` 等特殊字符开头的情况没有被测试覆盖。
- `loop-bash-validator.sh` 在无法解析 project root 时 `exit 0`，即 fail-open；这是 hook 场景的显式设计，但意味着根目录解析失效时运行期 Bash 防护不生效：[hooks/loop-bash-validator.sh:52](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:52)。
- setup 的 path 检查与后续 `cp "$FULL_PLAN_PATH" "$LOOP_DIR/plan.md"` 之间不是原子操作；恶意并发进程可能在校验后替换路径或文件，存在 TOCTOU 风险：[scripts/setup-rlcr-loop.sh:850](/Users/wangweiyang/GitHub/humanize/scripts/setup-rlcr-loop.sh:850)。
- methodology analysis 的 cancel allow pattern 阻断 shell metacharacters，但 pattern 没有锚定到命令结尾；无元字符的额外参数可能仍匹配 allow path。是否危险取决于 `cancel-rlcr-loop.sh` 参数语义，该脚本不在本次范围。
- Bash validator 的 command 防护是 regex/string parser，不是 shell AST。它覆盖了大量 wrapper、redirection、operator 分段与 `sh -c` 情况，但仍应视为防御层而非完整 shell 语义解析器。
- `command_modifies_file`、`git_adds_humanize`、`find_active_loop` 等 helper 来自 `loop-common.sh`，本次按 focus path 未展开读取；因此 destination write detection 的精确匹配语义在本报告中只按调用点描述。
- robustness test 覆盖了常见 shell metacharacters 与 symlink，但没有实际覆盖 colon、quotes、`@`、Unicode 文件名创建、`..` traversal、submodule path、以及并发替换/TOCTOU。

**What Is Explicitly Out Of Scope**

- 未分析安装、README、营销文案、截图、命令帮助中不定义行为的文本。
- 未读取 `hooks/lib/loop-common.sh`、`portable-timeout.sh`、cancel script、message templates；它们只作为本子集调用到的外部 helper 处理。
- 未运行测试；本轮遵守 read-only，仅用 `rg`、`sed`、`nl`、`wc` 读取证据。
- 未评估 Codex/Claude 运行时、hook 注册机制、Git 子模块命令输出的完整语义、YAML parser 具体实现。
- 未审计所有 `.humanize` 文件写入策略，只覆盖与 path validation / injection resistance 直接相关的 plan path、state YAML、Bash command gate。