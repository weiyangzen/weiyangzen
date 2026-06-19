**主题与结论**

Topic: Cancel and cleanup semantics。结论：RLCR 取消机制是一个两层算法：`cancel-rlcr-loop.sh` 负责定位“最新活动 loop”并把唯一活动状态文件重命名为 `cancel-state.md`；Bash hook 的 `is_cancel_authorized` 则只在 `.cancel-requested` 信号存在时，放行这一次精确的 `mv <active-state> <cancel-state>`，其余对状态文件的 Bash 修改全部 fail-closed。取消后目录、摘要、review 结果和状态内容被保留，清理范围只包括 pending session 信号和 methodology marker。

**Algorithm subset covered**

覆盖范围：

- 取消入口与用户路由：`commands/cancel-rlcr-loop.md`
- 取消执行算法：`scripts/cancel-rlcr-loop.sh`
- 信号文件与 Bash validator 行为测试：`tests/test-cancel-signal-file.sh`
- 安全鲁棒性测试：`tests/robustness/test-cancel-security-robustness.sh`
- 为解释测试中直接调用的核心授权函数，补充读取了算法相关共享实现：`hooks/lib/loop-common.sh`、`hooks/loop-bash-validator.sh`

核心状态变量：

- `PROJECT_ROOT`：由 `resolve_project_root` 解析；失败则退出 3。
- `LOOP_BASE_DIR=$PROJECT_ROOT/.humanize/rlcr`
- `LOOP_DIR`：`find_active_loop` 返回的最新活动 loop 目录。
- `STATE_FILE=$LOOP_DIR/state.md`
- `METHODOLOGY_ANALYSIS_STATE_FILE=$LOOP_DIR/methodology-analysis-state.md`
- `FINALIZE_STATE_FILE=$LOOP_DIR/finalize-state.md`
- `CANCEL_SIGNAL=$LOOP_DIR/.cancel-requested`
- `ACTIVE_STATE_FILE`：实际被重命名的活动状态文件。
- `LOOP_STATE ∈ {NORMAL_LOOP, METHODOLOGY_ANALYSIS_PHASE, FINALIZE_PHASE}`
- `FORCE ∈ {false,true}`：仅影响 Finalize Phase 是否需要确认。
- `CURRENT_ROUND/MAX_ITERATIONS`：只用于输出诊断，不参与取消判定。

输入：

- CLI 参数：无参数或 `--force`。
- 文件系统状态：最新 loop 目录中是否存在活动 state 文件。
- slash command 路由：脚本首行输出决定用户可见动作。
- Bash hook 命令字符串：用于验证“取消脚本触发的 mv 是否可被放行”。

**Pseudocode or transition table**

```text
cancel_rlcr_loop(force):
  project_root = resolve_project_root() or exit 3
  loop_dir = find_active_loop(project_root/.humanize/rlcr, no_session_filter)

  if loop_dir == "":
    print NO_LOOP
    exit 1

  if exists(loop_dir/state.md):
    state = NORMAL_LOOP
    active_state = loop_dir/state.md
  else if exists(loop_dir/methodology-analysis-state.md):
    state = METHODOLOGY_ANALYSIS_PHASE
    active_state = loop_dir/methodology-analysis-state.md
  else if exists(loop_dir/finalize-state.md):
    state = FINALIZE_PHASE
    active_state = loop_dir/finalize-state.md
  else:
    print NO_ACTIVE_LOOP
    exit 1

  read current_round, max_iterations from active_state; default "?"

  if state == FINALIZE_PHASE and force != true:
    print FINALIZE_NEEDS_CONFIRM
    exit 2

  touch loop_dir/.cancel-requested
  rm -f project_root/.humanize/.pending-session-id
  rm -f loop_dir/.methodology-exit-reason
  mv active_state loop_dir/cancel-state.md

  print one of:
    CANCELLED
    CANCELLED_METHODOLOGY_ANALYSIS
    CANCELLED_FINALIZE
  exit 0
```

授权门禁伪代码：

```text
is_cancel_authorized(active_loop_dir, command_lower):
  require exists(active_loop_dir/.cancel-requested)
  reject "$(", backticks, newline, ;, &&, ||, |
  reject remaining "$" after replacing $loop_dir/${loop_dir}
  reject multiple trailing spaces
  require command starts exactly with "mv "
  parse exactly two args, allowing both unquoted or consistently single/double quoted
  reject mixed quote delimiters
  canonicalize parent prefixes without dereferencing leaf symlinks
  require src in:
    active_loop_dir/state.md
    active_loop_dir/finalize-state.md
    active_loop_dir/methodology-analysis-state.md
  require dest == active_loop_dir/cancel-state.md
  reject if real on-disk source file is a symlink
  authorize
```

状态转移表：

| 当前文件状态 | 参数 | 输出首行 / exit | 状态转移 | 清理动作 |
|---|---:|---|---|---|
| 最新活动 loop 不存在 | 任意 | `NO_LOOP` / 1 | 无 | 无 |
| loop 目录存在但无活动 state | 任意 | `NO_ACTIVE_LOOP` / 1 | 无 | 无 |
| `state.md` | 任意 | `CANCELLED` / 0 | `state.md -> cancel-state.md` | 建立 `.cancel-requested`，删除 `.pending-session-id` 和 `.methodology-exit-reason` |
| `methodology-analysis-state.md` | 任意 | `CANCELLED_METHODOLOGY_ANALYSIS` / 0 | `methodology-analysis-state.md -> cancel-state.md` | 同上 |
| `finalize-state.md` | 无 `--force` | `FINALIZE_NEEDS_CONFIRM` / 2 | 无 | 无 |
| `finalize-state.md` | `--force` | `CANCELLED_FINALIZE` / 0 | `finalize-state.md -> cancel-state.md` | 同上 |

**Source evidence**

- 入口脚本声明取消动作是创建 `.cancel-requested` 并重命名状态文件，exit code 0/1/2/3 分别表示成功、无活动 loop、Finalize 需确认、其他错误：[scripts/cancel-rlcr-loop.sh:5](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:5), [scripts/cancel-rlcr-loop.sh:11](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:11), [scripts/cancel-rlcr-loop.sh:49](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:49)。
- 取消是全局项目级操作，不按 `session_id` 过滤；脚本显式说明 standalone slash command 无调用 session，并调用 `find_active_loop "$LOOP_BASE_DIR"` 找最新活动 loop：[scripts/cancel-rlcr-loop.sh:80](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:80), [scripts/cancel-rlcr-loop.sh:90](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:90)。
- `find_active_loop` 在无 session filter 时只检查单个最新目录，避免旧目录 stale `state.md` 被复活；只有该目录有活动 state 才返回：[hooks/lib/loop-common.sh:308](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:308), [hooks/lib/loop-common.sh:342](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:342)。
- 脚本中的活动 state 判定顺序是 `state.md`、`methodology-analysis-state.md`、`finalize-state.md`；没有活动 state 则 `NO_ACTIVE_LOOP`：[scripts/cancel-rlcr-loop.sh:103](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:103), [scripts/cancel-rlcr-loop.sh:108](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:108), [scripts/cancel-rlcr-loop.sh:117](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:117)。
- Finalize Phase 默认不立即取消，而是输出 `FINALIZE_NEEDS_CONFIRM`、round 信息和 `Use --force`，并以 2 退出：[scripts/cancel-rlcr-loop.sh:139](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:139)。
- 真正取消动作顺序是先 `touch "$CANCEL_SIGNAL"`，再删除 pending session 文件和 methodology exit marker，最后 `mv "$ACTIVE_STATE_FILE" "$LOOP_DIR/cancel-state.md"`：[scripts/cancel-rlcr-loop.sh:156](/Users/wangweiyang/GitHub/humanize/scripts/cancel-rlcr-loop.sh:156)。
- slash command 路由只看脚本首行：`NO_LOOP/NO_ACTIVE_LOOP` 报无活动 loop，三个 `CANCELLED*` 报输出消息，`FINALIZE_NEEDS_CONFIRM` 进入用户确认；确认 yes 时执行 `--force`：[commands/cancel-rlcr-loop.md:17](/Users/wangweiyang/GitHub/humanize/commands/cancel-rlcr-loop.md:17), [commands/cancel-rlcr-loop.md:24](/Users/wangweiyang/GitHub/humanize/commands/cancel-rlcr-loop.md:24), [commands/cancel-rlcr-loop.md:31](/Users/wangweiyang/GitHub/humanize/commands/cancel-rlcr-loop.md:31)。
- 文档明确“活动 loop”由最新 loop 目录中的 `state.md`、`methodology-analysis-state.md` 或 `finalize-state.md` 定义，并保留 loop 目录内容供参考：[commands/cancel-rlcr-loop.md:37](/Users/wangweiyang/GitHub/humanize/commands/cancel-rlcr-loop.md:37), [commands/cancel-rlcr-loop.md:39](/Users/wangweiyang/GitHub/humanize/commands/cancel-rlcr-loop.md:39)。
- Bash validator 对 `methodology-analysis-state.md`、`finalize-state.md`、`state.md` 的修改先调用 `is_cancel_authorized`；授权才 `exit 0`，否则 block：[hooks/loop-bash-validator.sh:271](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:271), [hooks/loop-bash-validator.sh:280](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:280), [hooks/loop-bash-validator.sh:289](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:289)。
- validator 还把 shell operator 分段，检测 `mv/cp ... state.md` 作为源路径的绕过，并对 shell wrapper `sh -c`/`bash -c` 做额外拦截：[hooks/loop-bash-validator.sh:299](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:299), [hooks/loop-bash-validator.sh:310](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:310), [hooks/loop-bash-validator.sh:458](/Users/wangweiyang/GitHub/humanize/hooks/loop-bash-validator.sh:458)。
- `is_cancel_authorized` 的契约和失败码包括缺少 signal、注入/替换、混合引号、多余尾空格、结构非法、源文件 symlink：[hooks/lib/loop-common.sh:1033](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1033)。
- 授权函数必须先看到 `.cancel-requested`，否则返回 1：[hooks/lib/loop-common.sh:1055](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1055)。
- 注入防护拒绝 `$()`、反引号、换行、`;`、`&&`、`||`、`|`，并拒绝多个尾随空格：[hooks/lib/loop-common.sh:1062](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1062), [hooks/lib/loop-common.sh:1067](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1067), [hooks/lib/loop-common.sh:1072](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1072), [hooks/lib/loop-common.sh:1077](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1077)。
- `$loop_dir`/`${loop_dir}` 会被归一化成真实路径；归一化后仍存在 `$` 则拒绝，用于阻断 `${IFS}` 等隐藏变量：[hooks/lib/loop-common.sh:1092](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1092), [hooks/lib/loop-common.sh:1101](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1101)。
- 授权命令必须以 `mv` 开头，解析出且仅解析出两个参数；混合单/双引号会拒绝：[hooks/lib/loop-common.sh:1106](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1106), [hooks/lib/loop-common.sh:1115](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1115), [hooks/lib/loop-common.sh:1181](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1181), [hooks/lib/loop-common.sh:1185](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1185)。
- 源路径只能是三个活动 state 文件之一，目标必须是 `cancel-state.md`；路径使用 parent-prefix canonicalization，避免 leaf symlink alias 被误授权：[hooks/lib/loop-common.sh:1191](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1191), [hooks/lib/loop-common.sh:1210](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1210), [hooks/lib/loop-common.sh:1217](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1217)。
- 源文件本体若是 symlink 则拒绝；实现用精确路径比较避免目录名包含 `finalize` 或 `methodology` 时误分类：[hooks/lib/loop-common.sh:1232](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1232)。
- 信号文件测试证明：有 signal 的精确 `mv state.md cancel-state.md` 允许；无 signal、错误目标、错误目录 signal、`rm`、`sed -i`、`echo > state.md` 均阻断：[tests/test-cancel-signal-file.sh:80](/Users/wangweiyang/GitHub/humanize/tests/test-cancel-signal-file.sh:80), [tests/test-cancel-signal-file.sh:121](/Users/wangweiyang/GitHub/humanize/tests/test-cancel-signal-file.sh:121), [tests/test-cancel-signal-file.sh:181](/Users/wangweiyang/GitHub/humanize/tests/test-cancel-signal-file.sh:181), [tests/test-cancel-signal-file.sh:201](/Users/wangweiyang/GitHub/humanize/tests/test-cancel-signal-file.sh:201), [tests/test-cancel-signal-file.sh:223](/Users/wangweiyang/GitHub/humanize/tests/test-cancel-signal-file.sh:223)。
- 鲁棒性测试覆盖 finalize 源、单引号、无引号为正例；缺 signal、命令替换、链式 operator、错误源/目标、多余参数为反例：[tests/robustness/test-cancel-security-robustness.sh:39](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-cancel-security-robustness.sh:39), [tests/robustness/test-cancel-security-robustness.sh:51](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-cancel-security-robustness.sh:51), [tests/robustness/test-cancel-security-robustness.sh:99](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-cancel-security-robustness.sh:99), [tests/robustness/test-cancel-security-robustness.sh:109](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-cancel-security-robustness.sh:109), [tests/robustness/test-cancel-security-robustness.sh:174](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-cancel-security-robustness.sh:174)。
- symlink 相关回归测试要求接受 symlinked prefix，但拒绝 destination/source leaf symlink alias，以及拒绝 `state.md`/`finalize-state.md` 本体为 symlink：[tests/test-cancel-signal-file.sh:1345](/Users/wangweiyang/GitHub/humanize/tests/test-cancel-signal-file.sh:1345), [tests/test-cancel-signal-file.sh:1376](/Users/wangweiyang/GitHub/humanize/tests/test-cancel-signal-file.sh:1376), [tests/test-cancel-signal-file.sh:1400](/Users/wangweiyang/GitHub/humanize/tests/test-cancel-signal-file.sh:1400), [tests/robustness/test-cancel-security-robustness.sh:332](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-cancel-security-robustness.sh:332)。

**Edge cases and risks**

- 多活动 state 文件并存时存在优先级不一致：取消脚本按 `state.md -> methodology-analysis-state.md -> finalize-state.md` 选择，而共享 `resolve_active_state_file` 按 `methodology-analysis-state.md -> finalize-state.md -> state.md` 选择。这隐含不变量是同一 loop 目录中最多只能有一个活动 state 文件；若不变量被破坏，脚本与 hook 可能对“当前 phase”判断不同。
- `.cancel-requested` 在取消后没有被删除；它用于在 `mv` 前授权 validator。正常情况下活动 state 已被移动为 `cancel-state.md`，最新目录不再 active，因此不会继续参与 loop。但如果外部错误地在同一目录重新创建活动 state，残留 signal 可能重新满足授权前置条件。
- `cancel-state.md` 若已存在，脚本直接 `mv "$ACTIVE_STATE_FILE" "$LOOP_DIR/cancel-state.md"`，没有显式防覆盖检查。算法假设 active loop 目录不会同时已有 terminal cancel state。
- Finalize Phase 的普通取消是两步协议：脚本返回 `FINALIZE_NEEDS_CONFIRM`，slash command 再问用户并用 `--force` 执行。若直接调用脚本且忽略 exit 2，不会取消。
- hook 授权是 Bash command 字符串级门禁，不是通用 shell parser；测试覆盖大量注入、链式、wrapper、重定向和 symlink alias，但本质仍依赖正则与受限解析。
- 无活动 loop 时 Bash validator 允许命令通过；这与测试期望一致，但也意味着保护只在 `find_active_loop` 成功时生效。
- Methodology Analysis Phase 中 Bash 限制允许 `cancel-rlcr-loop.sh` 作为 leading command，并拒绝 metacharacter 后才早退；这是为了允许取消，同时阻断在 methodology phase 中借取消命令拼接额外写操作。

**What is explicitly out of scope**

- 未分析安装流程、市场文案、截图、泛用帮助文本，除非它们定义取消行为。
- 未分析 RLCR 主循环评分、Codex review、计划生成、finalize 内容生成等非取消路径。
- 未分析所有 hook 的完整安全策略，只覆盖与取消授权、状态文件保护、cleanup 直接相关的分支。
- 未执行测试套件、未编辑文件、未提交；本次为只读源码与测试语义提取。
- 未进行网络搜索。