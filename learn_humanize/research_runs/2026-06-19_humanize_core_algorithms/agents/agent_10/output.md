**Topic and conclusion**

Topic: Bash validator command safety rules（提交 `0ec921a36b4365df503511c5567bbd3e02db0df5`）

结论：`loop-bash-validator.sh` 是一个按阶段递进的 Bash 命令门禁器。它先做 Hook JSON 与工具类型预检，再按 session 找活动 RLCR loop；无活动 loop 时放行。活动 loop 内，它以正则匹配为核心，拦截 Bash 对 `.humanize` 状态、loop 控制文件、round 产物、hook 脚本和受策略约束的 git 命令的修改。`methodology-analysis-state.md` 存在时进入更严格阶段，基本只允许只读 Bash 和安全形态的 `cancel-rlcr-loop.sh`。失败策略总体是：输入/状态损坏 `exit 1`，策略阻断 `exit 2`，不相关或安全命令 `exit 0`。

**Algorithm subset covered**

覆盖范围：

- Hook 输入解析与 Bash 工具筛选：`hooks/loop-bash-validator.sh:22-46`
- 活动 loop/session 定位：`hooks/loop-bash-validator.sh:52-60`，`hooks/lib/loop-common.sh:308-425`
- methodology analysis 阶段 Bash 禁写规则：`hooks/loop-bash-validator.sh:81-171`
- 活动 RLCR loop 内 git push、git add、hook 直跑、状态/计划/round 文件保护：`hooks/loop-bash-validator.sh:173-573`
- 核心命令修改判定器：`hooks/lib/loop-common.sh:1482-1510`
- `.humanize` git-add 判定器：`hooks/lib/loop-common.sh:1258-1376`
- 用户可见阻断模板：`prompt-template/block/git-add-humanize.md:1-34`，`prompt-template/block/git-push.md:1-9`
- 正则行为测试：`tests/test-bash-validator-patterns.sh:36-194`

未覆盖安装、营销、截图、通用用法。

**Pseudocode**

```text
input = stdin JSON

if !validate_hook_input(input): exit 1
if is_deeply_nested(input, 30): exit 1

tool = input.tool_name
if tool != "Bash": exit 0

if missing input.tool_input.command: exit 1
command = input.tool_input.command
cmd = lower(command)

project_root = resolve_project_root()
if project_root missing: exit 0

session_id = input.session_id
active_loop = find_active_loop(project_root/.humanize/rlcr, session_id)

if active_loop has methodology-analysis-state.md:
    if cmd is leading cancel-rlcr-loop.sh
       and no shell metacharacters (; | & ` > < $( newline):
        exit 0

    if cmd matches git write verbs:
        block("Git write commands"); exit 2
    if cmd matches file manipulation verbs:
        block("File modification commands"); exit 2
    if cmd matches sed -i / awk -i inplace / perl -i:
        block("In-place editing"); exit 2
    if cmd matches interpreter execution:
        block("Running interpreters"); exit 2
    if cmd matches shell script entrypoints:
        block("Running shell scripts"); exit 2
    if cmd matches build tools:
        block("Build tools"); exit 2
    if cmd matches source or dot command:
        block("Sourcing scripts"); exit 2
    if cmd matches direct script execution:
        block("Direct script execution"); exit 2
    stripped = remove safe redirections to /dev/* and fd duplication
    if stripped contains ">":
        block("File redirection"); exit 2

if active_loop is empty:
    exit 0

state_file = resolve_active_state_file(active_loop)
if !parse_state_file_strict(state_file):
    exit 1

current_round = STATE_CURRENT_ROUND
push_every_round = STATE_PUSH_EVERY_ROUND

if push_every_round != true and cmd starts with "git push":
    render block/git-push.md; exit 2

if git_adds_humanize(cmd):
    render block/git-add-humanize.md; exit 2

if cmd directly executes loop-codex-stop-hook.sh or rlcr-stop-gate.sh
   through allowed wrapper prefixes:
    block direct hook execution; exit 2

for protected state files in order:
    methodology-analysis-state.md
    finalize-state.md
    state.md
    if command_modifies_file(cmd, file):
        if is_cancel_authorized(active_loop, cmd): exit 0
        block matching state file; exit 2

split cmd into shell segments, preserving redirection placeholders
strip leading redirections from each segment
if any mv/cp source references methodology-analysis-state.md/finalize-state.md/state.md:
    if is_cancel_authorized(...): exit 0
    block matching state file; exit 2

if cmd contains sh/bash -c payload with mv/cp protected state file:
    if is_cancel_authorized(...): exit 0
    block matching state file; exit 2

if command_modifies_file(cmd, ".humanize/rlcr/.../plan.md"):
    block plan backup write; exit 2

if command_modifies_file(cmd, "goal-tracker.md"):
    if current_round == 0:
        block with bash-specific goal tracker message
    else:
        block with round-aware goal tracker message
    exit 2

if command_modifies_file(cmd, "round-N-prompt.md"):
    block prompt write; exit 2

if command_modifies_file(cmd, "round-N-summary.md"):
    block summary bash write; exit 2

if command_modifies_file(cmd, "round-N-contract.md"):
    block round contract bash write; exit 2

if command_modifies_file(cmd, "round-N-todos.md"):
    only allow when full active loop path matches round-1/2-todos.md
    otherwise block todos access; exit 2

exit 0
```

**Transition table**

| Gate | Condition | State/action |
|---|---|---|
| JSON gate | invalid JSON/null byte/non-UTF8/missing `tool_name` | `exit 1` |
| DoS depth gate | JSON depth `> 30` | `exit 1` |
| Tool route | `tool_name != Bash` | `exit 0` |
| Bash input gate | missing `tool_input.command` | `exit 1` |
| Project root route | cannot resolve project root | `exit 0` |
| Loop route | no active session-matched loop | `exit 0` |
| Methodology-analysis mode | active loop has `methodology-analysis-state.md` | enter stricter Bash allow/deny layer |
| Cancel exception | safe leading `cancel-rlcr-loop.sh`, no shell metacharacters | `exit 0` |
| Methodology write gates | git writes, file ops, in-place edit, interpreters, scripts, build tools, source, direct scripts, unsafe redirection | `exit 2` |
| State parse gate | active state malformed | fail closed, `exit 1` |
| Git push gate | `push_every_round != true` and command starts `git push` | `exit 2` |
| Git add `.humanize` gate | `git_adds_humanize(cmd)` | `exit 2` |
| Hook script gate | direct/wrapped execution of stop hook/gate scripts | `exit 2` |
| Protected file gates | Bash write patterns target state/plan/goal/prompt/summary/contract/todos | `exit 2` unless explicit cancel authorization for state files |
| Default | no gate matches | `exit 0` |

**Source evidence**

- `loop-bash-validator.sh` loads shared functions, reads stdin JSON, validates structure, rejects deep nesting, routes non-Bash tools to allow, and requires `tool_input.command`: `hooks/loop-bash-validator.sh:14-46`。
- It resolves project root, extracts `session_id`, and finds a session-aware active loop under `.humanize/rlcr`: `hooks/loop-bash-validator.sh:52-60`。`find_active_loop` documents newest-dir/zombie-loop protection and session filtering semantics: `hooks/lib/loop-common.sh:308-425`。
- Methodology analysis phase is triggered by `methodology-analysis-state.md` in the active loop: `hooks/loop-bash-validator.sh:81`。Comments explicitly state only read-only operations and `cancel-rlcr-loop.sh` are allowed, with spawned-agent/session limitations: `hooks/loop-bash-validator.sh:64-78`。
- Cancel exception requires the script name as the leading command and rejects shell metacharacters including `; | & \` > < $(` and newline: `hooks/loop-bash-validator.sh:82-105`。
- Methodology-analysis phase blocks git write verbs such as `commit/add/reset/.../push/...`: `hooks/loop-bash-validator.sh:106-112`；file manipulation commands such as `tee/install/touch/mv/cp/rm/dd/truncate/.../patch`: `hooks/loop-bash-validator.sh:113-119`；in-place `sed/awk/perl`: `hooks/loop-bash-validator.sh:120-126`；common interpreters: `hooks/loop-bash-validator.sh:127-133`；shell entrypoints: `hooks/loop-bash-validator.sh:134-140`；build tools: `hooks/loop-bash-validator.sh:141-147`；source/dot commands: `hooks/loop-bash-validator.sh:148-154`；direct script execution: `hooks/loop-bash-validator.sh:155-161`；unsafe output redirection after stripping `/dev/*` and fd duplication: `hooks/loop-bash-validator.sh:162-170`。
- If no active loop remains after methodology checks, Bash commands are allowed: `hooks/loop-bash-validator.sh:173-176`。
- Active loop state is resolved and parsed strictly; malformed state blocks for safety: `hooks/loop-bash-validator.sh:209-217`。Strict parser requires frontmatter and fields such as `current_round`, `max_iterations`, `review_started`, `base_branch`, and validates numeric/boolean fields: `hooks/lib/loop-common.sh:525-600`。
- Git push is blocked when `STATE_PUSH_EVERY_ROUND` is not `true` and command starts with `git push`: `hooks/loop-bash-validator.sh:221-237`。The prompt says commits should remain local and `--push-every-round` is required to push each round: `prompt-template/block/git-push.md:1-9`。
- `.humanize` git-add protection is global after loop detection: `hooks/loop-bash-validator.sh:241-250`。The helper splits chained commands, detects `git ... add`, normalizes quotes, blocks direct `.humanize` paths, force+broad scope, `-A/--all` when `.humanize` exists, and broad `.`/`*` when `.humanize` is not ignored: `hooks/lib/loop-common.sh:1280-1376`。The rendered policy explains `.humanize/` is local loop state, gives allowed specific adds, and lists blocked examples: `prompt-template/block/git-add-humanize.md:1-34`。
- Direct execution of `loop-codex-stop-hook.sh` or `rlcr-stop-gate.sh` is blocked, including wrapper prefixes such as assignment/env/command/timeout/nice/nohup/strace/ltrace: `hooks/loop-bash-validator.sh:178-202`。
- State files are protected in specificity order: `methodology-analysis-state.md`, then `finalize-state.md`, then `state.md`, because `state\.md` would also match `finalize-state.md`: `hooks/loop-bash-validator.sh:259-297`。
- Additional mv/cp source protection handles moving/copying protected state files away from their path, not only writing to them as destinations: `hooks/loop-bash-validator.sh:299-315`。Commands are split on shell operators while preserving redirection constructs, then leading redirections are stripped before segment matching: `hooks/loop-bash-validator.sh:316-456`。
- Shell wrapper bypasses such as `sh -c 'mv state.md /tmp/foo'` are separately detected: `hooks/loop-bash-validator.sh:458-488`。
- Plan backup writes are blocked via `command_modifies_file` against `.humanize/rlcr/.../plan.md`: `hooks/loop-bash-validator.sh:490-501`。
- `goal-tracker.md` Bash writes are blocked, with round-dependent messaging: round 0 prompts Bash-specific Write/Edit path; later rounds use round-aware goal tracker block: `hooks/loop-bash-validator.sh:503-517`。
- Round prompt, summary, contract, and todos files are protected through filename patterns: `hooks/loop-bash-validator.sh:519-569`。Todos has an exception only when command references the full active loop path for `round-1-todos.md` or `round-2-todos.md`: `hooks/loop-bash-validator.sh:561-568`。
- Core file-modification detector is a fixed regex list for redirection, `tee`, in-place `sed/awk/perl`, `mv/cp` destination, `rm`, `dd of=`, `truncate`, `printf >`, and `exec fd>`: `hooks/lib/loop-common.sh:1482-1510`。
- Tests assert redirection, `tee`, in-place editors, `mv/cp/rm`, `dd/truncate/exec`, and state/summary patterns are detected: `tests/test-bash-validator-patterns.sh:69-194`。They also assert read-only commands such as `cat`, `grep`, `head`, `tail`, `wc`, `less`, `ls`, `stat`, `diff` are not detected: `tests/test-bash-validator-patterns.sh:136-153`。

**Edge cases and risks**

- `command_modifies_file` 是正则启发式，不是 shell parser。变量间接目标不会被识别；测试明确 `echo x > $FILE` 不应被判定为修改目标文件：`tests/test-bash-validator-patterns.sh:170-172`。
- 多源 `cp file1 file2 goal-tracker.md` 是已知未覆盖场景；测试注释说明该模式期望 `cp src dest` 格式：`tests/test-bash-validator-patterns.sh:165-168`。
- 普通目标文件匹配主要基于无空白 token，例如 `[^[:space:]]*${file_pattern}`；带空格路径、复杂 quoting、process substitution 等非典型 shell 语法可能存在漏判。状态文件 mv/cp source 保护单独做了更强的 segment/leading-redirection 清理，但这只覆盖状态文件源路径场景：`hooks/loop-bash-validator.sh:316-456`。
- Methodology-analysis 阶段明确接受两个架构限制：只读 Bash 不阻断，否则会破坏基础操作；不同 `session_id` 的 spawned agents 不受 hook 限制，只靠 prompt sanitization：`hooks/loop-bash-validator.sh:68-75`。
- `resolve_project_root` 失败时直接允许 Bash：`hooks/loop-bash-validator.sh:52`。这是可用性优先的路由，但安全性依赖项目根能被正确解析。
- `.humanize` 的 broad-scope git-add 阻断依赖当前工作目录下 `.humanize` 是否存在，以及 `git check-ignore -q .humanize` 结果：`hooks/lib/loop-common.sh:1355-1371`。如果命令通过 `git -C` 操作其他目录，函数语义仍按当前执行环境检查 `.humanize`。
- 所有命令先 lower-case；这有助于大小写命令检测，测试覆盖 `ECHO X > GOAL-TRACKER.MD`：`tests/test-bash-validator-patterns.sh:75-80`。但 lower-case 也会改变大小写敏感路径文本，适用于当前保护文件名固定小写的设计。
- Git push gate 只匹配以空白后 `git push` 开头的命令：`hooks/loop-bash-validator.sh:228-237`。链式命令中后续段的 `git push` 不在该 gate 的正则覆盖范围内；methodology 阶段的 git write gate覆盖链式分隔符，但普通 active-loop push gate没有同等 segment 解析。

**What is explicitly out of scope**

- 不分析安装流程、README 使用说明、营销文案、截图或非 Bash validator 行为。
- 不分析 Read/Write/Edit validator 的完整算法，只引用共享库中 Bash validator 直接调用的函数。
- 不运行测试、不修改文件、不提交；本次为 read-only 源码抽取。
- 不评价 prompt 文案风格，只把 `git-add-humanize.md` 与 `git-push.md` 作为阻断策略输出证据。
- 不把此 validator 视为完整 shell 安全沙箱；源码本身采用正则和阶段门禁，未实现完整 shell AST 解析。