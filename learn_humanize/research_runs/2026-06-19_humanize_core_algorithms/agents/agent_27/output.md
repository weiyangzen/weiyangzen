**Topic And Conclusion**

主题：Git 分支、工作区 cleanliness、未推送提交的 RLCR stop-hook 门禁。

结论：该子算法是一个“停止前 fail-closed Git 安全门”。它在 Codex review 等昂贵流程前依次验证：当前分支必须等于 loop 启动分支；仓库状态必须可读取；除未跟踪 `.humanize/` / `.humanize-*` 本地状态外，工作区必须干净；如果 `push_every_round=true`，本地分支不能 ahead 远端。任一门禁失败都会输出 `{"decision":"block", ...}` 并阻止退出；通过后才进入后续 summary/review 流程。当前取证 commit 已确认是 `0ec921a36b4365df503511c5567bbd3e02db0df5`，分支状态为 `main...origin/main`。

**Algorithm Subset Covered**

覆盖范围仅限以下路径中与 Git 分支、干净状态、push gate 直接相关的逻辑：

- `hooks/loop-codex-stop-hook.sh`
- `prompt-template/block/git-not-clean.md`
- `prompt-template/block/unpushed-commits.md`
- `tests/robustness/test-git-operations-robustness.sh`

核心状态变量：

- `PROJECT_ROOT`：Git 操作目标仓库根目录。
- `GIT_TIMEOUT=30`：所有关键 Git 操作超时时间。
- `START_BRANCH`：RLCR loop 启动时记录的分支。
- `CURRENT_BRANCH`：当前 `HEAD` 所在分支。
- `PUSH_EVERY_ROUND`：是否启用每轮必须 push。
- `GIT_IS_REPO`：当前项目是否可被 Git 识别为 repo。
- `GIT_STATUS_CACHED`：一次性缓存的 `git status --porcelain` 输出。
- `GIT_STATUS_FOR_BLOCK`：剔除未跟踪 `.humanize/` / `.humanize-*` 后用于判断 dirty 的状态。
- `GIT_ISSUES`：阻塞原因摘要，例如 `uncommitted changes`。
- `SPECIAL_NOTES`：模板补充说明，例如 untracked 文件提醒。
- `GIT_AHEAD` / `AHEAD_COUNT`：`git status -sb` 中解析出的 ahead 提交数量。

输入：

- RLCR state frontmatter：提供 `start_branch`、`push_every_round` 等 loop 配置。
- Git 命令输出：`rev-parse --abbrev-ref HEAD`、`rev-parse --git-dir`、`status --porcelain`、`status -sb`。
- 模板文件：dirty block 和 unpushed block 的用户可读指令。

输出 / 路由：

- 通过：继续执行后续 summary/review 流程。
- 阻塞：输出 JSON，`decision=block`，并附带 `reason` 与 `systemMessage`。
- 非 Git 仓库：该 hook 的 clean/push gate 不执行，因为 gate 被包在 `GIT_IS_REPO=true` 条件内；但独立 robustness 测试覆盖非 Git 检测。

**Pseudocode**

```bash
# 0. state 已解析出 START_BRANCH, PUSH_EVERY_ROUND 等变量

CURRENT_BRANCH = timeout(30s, git -C PROJECT_ROOT rev-parse --abbrev-ref HEAD)
if git_failed_or_timeout(CURRENT_BRANCH):
    block("Loop: Blocked - git operation failed")

if START_BRANCH != "" and CURRENT_BRANCH != START_BRANCH:
    block("Loop: Blocked - branch changed")

GIT_IS_REPO = command_exists(git) &&
              timeout(30s, git -C PROJECT_ROOT rev-parse --git-dir) succeeds

if GIT_IS_REPO:
    GIT_STATUS_CACHED = timeout(30s, git -C PROJECT_ROOT status --porcelain)
    if status_failed_or_timeout:
        cleanup_stale_index_lock()
        block("Loop: Blocked - git status failed")

# methodology-analysis phase has its own clean check before terminal exit
if IS_METHODOLOGY_ANALYSIS_PHASE:
    if complete_methodology_analysis():
        GIT_STATUS_FOR_BLOCK = remove_untracked_humanize_paths(GIT_STATUS_CACHED)
        if GIT_STATUS_FOR_BLOCK not empty:
            cleanup_stale_index_lock()
            block("uncommitted changes after methodology analysis")
        allow_exit()
    else:
        block_methodology_analysis_incomplete()

if GIT_IS_REPO:
    if git_has_tracked_humanize_state(PROJECT_ROOT):
        cleanup_stale_index_lock()
        block("tracked Humanize state detected")

    GIT_STATUS_FOR_BLOCK = remove lines matching '^?? \.humanize[-/]'
    if GIT_STATUS_FOR_BLOCK not empty:
        GIT_ISSUES = "uncommitted changes"
        SPECIAL_NOTES = notes_for_humanize_local_and_other_untracked_files()
        cleanup_stale_index_lock()
        block("Loop: Blocked - uncommitted changes detected, please commit first")

    if PUSH_EVERY_ROUND == "true":
        GIT_AHEAD = timeout(30s, git -C PROJECT_ROOT status -sb) | grep 'ahead [0-9]*'
        if GIT_AHEAD not empty:
            AHEAD_COUNT = digits(GIT_AHEAD)
            CURRENT_BRANCH = timeout(30s, git rev-parse --abbrev-ref HEAD) || "unknown"
            block("Loop: Blocked - N unpushed commit(s) detected, please push first")

# clean + pushed enough for this gate
continue_to_summary_file_check()
```

**Transition Table**

| 阶段 | 条件 | 转移 / 输出 |
|---|---|---|
| Branch check | `git rev-parse --abbrev-ref HEAD` 失败、超时或空 | `block`: 无法验证分支一致性 |
| Branch check | `CURRENT_BRANCH != START_BRANCH` | `block`: 禁止 loop 中切换分支 |
| Repo detection | `git` 不存在或 `rev-parse --git-dir` 失败 | 跳过 clean/push gate |
| Status cache | `git status --porcelain` 失败或超时 | 清理 `index.lock`，`block`: fail-closed |
| Methodology phase | analysis complete 且剔除 `.humanize` 后仍 dirty | 清理 `index.lock`，`block`: 必须 commit |
| Main clean gate | tracked `.humanize` state 被 Git 跟踪 | 清理 `index.lock`，`block`: 先从 Git 移除 |
| Main clean gate | 剔除未跟踪 `.humanize` 后仍有 status 行 | 清理 `index.lock`，`block`: 必须 commit |
| Push gate | `PUSH_EVERY_ROUND=true` 且 `status -sb` 含 `ahead N` | `block`: 必须 push |
| Push gate | 未启用或没有 ahead | 继续后续 summary/review |

**Source Evidence**

- Hook 初始化 Git 超时与上下文：`PROJECT_ROOT` 来自 `resolve_project_root`，`GIT_TIMEOUT=30`，并加载 portable timeout wrapper。见 `hooks/loop-codex-stop-hook.sh:46-57`。
- State 解析将 `STATE_START_BRANCH` 映射到 `START_BRANCH`，将 `STATE_PUSH_EVERY_ROUND` 映射到 `PUSH_EVERY_ROUND`。见 `hooks/loop-codex-stop-hook.sh:125-134`。
- 分支一致性 gate：通过 `git rev-parse --abbrev-ref HEAD` 获取 `CURRENT_BRANCH`；Git 操作失败或空值直接 block；若当前分支不同于 `START_BRANCH`，输出 “branch changed” block。见 `hooks/loop-codex-stop-hook.sh:286-316`。
- Git status 缓存与 fail-closed：只有 `git` 存在且 `rev-parse --git-dir` 成功才设置 `GIT_IS_REPO=true`；随后缓存 `git status --porcelain`，失败或超时会清理 stale lock 并 block，而不是把空 status 当成 clean。见 `hooks/loop-codex-stop-hook.sh:485-516`。
- stale `index.lock` 清理：源码说明 Git 命令超时可能留下 `.git/index.lock`，helper 解析正确 repo 的 git dir 并 `rm -f index.lock`。见 `hooks/loop-codex-stop-hook.sh:459-483`。
- Methodology analysis phase 的 clean 特例：该阶段在主 clean gate 前运行，因为 `.humanize/rlcr/...` 可能使工作区看起来 dirty；完成 analysis 后仍会重新检查工作区，且同样排除未跟踪 `.humanize`。见 `hooks/loop-codex-stop-hook.sh:606-658`。
- 主 clean gate 先拒绝 tracked Humanize state：如果 `.humanize` 状态被 Git 跟踪，直接 block 并要求先从 Git 移除。见 `hooks/loop-codex-stop-hook.sh:672-690`。
- dirty 判断规则：剔除正则 `^\?\? \.humanize[-/]` 匹配的未跟踪 `.humanize/` 或 `.humanize-*`，其余任何 `git status --porcelain` 行都会设置 `GIT_ISSUES="uncommitted changes"`。见 `hooks/loop-codex-stop-hook.sh:692-700`。
- dirty 时补充 notes：原始 untracked status 中若包含 `.humanize` 本地状态，加入本地状态说明；若还有其他 untracked 文件，加入 “add to .gitignore or commit” 类提醒。见 `hooks/loop-codex-stop-hook.sh:702-722`。
- dirty block 输出：存在 `GIT_ISSUES` 时清理 `index.lock`，渲染 `block/git-not-clean.md`，输出 `decision=block` 和 “please commit first”。见 `hooks/loop-codex-stop-hook.sh:725-749`。
- push gate：仅 `PUSH_EVERY_ROUND=true` 时执行；从 `git status -sb` 中 grep `ahead [0-9]*`，提取 `AHEAD_COUNT`，再渲染 `block/unpushed-commits.md` 并 block。见 `hooks/loop-codex-stop-hook.sh:751-780`。
- push gate 通过后的边界：未触发 block 后离开 Git gate，继续进入 summary 文件检查。见 `hooks/loop-codex-stop-hook.sh:780-797`。
- dirty 模板规定操作：要求 review untracked、用具体路径 `git add <files>`、commit，并禁止 `git add -A` / `git add --all` / `git add .`，禁止 stage `.humanize/` 与 AI authorship。见 `prompt-template/block/git-not-clean.md:1-18`。
- unpushed 模板规定操作：当 `--push-every-round` 启用时，要求 `git push origin {{CURRENT_BRANCH}}` 后才能再次退出。见 `prompt-template/block/unpushed-commits.md:1-12`。
- robustness 测试覆盖 clean repo、分支名、untracked、modified、staged added、insertions。见 `tests/robustness/test-git-operations-robustness.sh:71-158`。
- robustness 测试覆盖非 Git、detached HEAD、多状态、deleted、empty repo、feature branch、rename、大量 untracked、空格文件名、binary、同一文件 staged+unstaged、deletions。见 `tests/robustness/test-git-operations-robustness.sh:168-367`。
- robustness 测试覆盖 Git 状态分类：normal、detached、rebase、merge、shallow、not_a_repo、permission_error 或 graceful fallback。见 `tests/robustness/test-git-operations-robustness.sh:377-500`。

**Edge Cases And Risks**

- Fail-closed 是显式设计：`git status` 失败或超时不会被解释为 clean，而是阻塞退出，降低绕过 clean gate 的风险。证据见 `hooks/loop-codex-stop-hook.sh:490-515`。
- `.humanize/` 只有“未跟踪”状态被排除；如果 Humanize 状态被 tracked，则会触发专门 block。这保持了本地插件状态可存在，但不能进入版本库。证据见 `hooks/loop-codex-stop-hook.sh:677-690` 与 `hooks/loop-codex-stop-hook.sh:692-698`。
- `HUMANIZE_UNTRACKED_PATTERN='^\?\? \.humanize[-/]'` 只匹配 porcelain 中未跟踪的 `.humanize/` 或 `.humanize-*`；若 `.humanize` 下文件已 staged/modified，不会被该正则排除，会进入 dirty gate。证据见 `hooks/loop-codex-stop-hook.sh:692-700`。
- push gate 只解析 `git status -sb` 中的 `ahead N`；没有显式处理 `behind`、diverged、无 upstream、push 失败、远端不可达等情形。若没有出现 `ahead N`，该 gate 不阻塞。证据见 `hooks/loop-codex-stop-hook.sh:755-780`。
- branch gate 使用 `rev-parse --abbrev-ref HEAD`。detached HEAD 通常返回 `HEAD`，如果 `START_BRANCH` 是普通分支会触发 branch changed；robustness 测试确认 detached 状态可被相关生产函数识别，但 stop hook 本身这里按分支不一致阻塞。证据见 `hooks/loop-codex-stop-hook.sh:290-316` 与 `tests/robustness/test-git-operations-robustness.sh:388-400`。
- 非 Git 仓库时，stop hook 的 Git clean/push gate 因 `GIT_IS_REPO=false` 被跳过；测试层面另有非 Git 状态处理覆盖。证据见 `hooks/loop-codex-stop-hook.sh:492-516`、`hooks/loop-codex-stop-hook.sh:672-780`、`tests/robustness/test-git-operations-robustness.sh:168-177`、`tests/robustness/test-git-operations-robustness.sh:466-475`。
- `cleanup_stale_index_lock` 没有年龄/进程占用判定，只要目标 `.git/index.lock` 存在就删除。源码意图是修复超时 Git 命令留下的 lock，但如果并发 Git 操作确实仍在运行，存在误删活跃 lock 的理论风险。证据见 `hooks/loop-codex-stop-hook.sh:462-483`。
- dirty gate 使用 cached status；缓存发生在 large-file 和 clean gate 之前。好处是避免多次 Git 调用并保持一致视图；风险是 hook 内后续自身生成的文件若发生在缓存之后，clean gate 不会看到，除非对应阶段另有检查。证据见 `hooks/loop-codex-stop-hook.sh:485-499` 与 `hooks/loop-codex-stop-hook.sh:672-698`。
- 模板指令强调不能用宽泛 stage 命令，说明算法不只判断 dirty，还约束 remediation 行为，避免把 loop artifacts 或无关文件一起提交。证据见 `prompt-template/block/git-not-clean.md:7-16`。

**What Is Explicitly Out Of Scope**

- 未分析安装、营销、截图、README 通用使用说明。
- 未分析 Codex review 的评分机制、summary 文件生成、bitlesson、goal tracker、large file detection 的完整算法；只在它们影响 Git gate 顺序时引用。
- 未分析 `scripts/humanize.sh` 中 `humanize_parse_git_status` / `humanize_detect_git_state` 的实现体，因为本任务 focus path 未包含该文件；这里只引用 robustness 测试对这些行为的期望。
- 未验证远端网络 push 行为，也未运行网络搜索或远端 Git 操作。
- 未编辑文件、未提交、未运行破坏性 Git 命令。