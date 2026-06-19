**Topic and conclusion**

Topic: `loop-common.sh` 的状态文件解析与 active loop 选择，包含 `project-root.sh` 对 `.humanize/rlcr` 定位的前置约束。

结论：该算法不是按时间戳解析目录名，而是按 `ls ... | sort -r` 的路径字典序选择候选。无 `session_id` 时只检查“最新”一个子目录，以防旧 `state.md` 被复活；有 `session_id` 时按新到旧扫描，找到该 session 的最新状态目录后立即判定其是否 active，若该 session 最新目录已终态则返回空，不回退到旧 active 目录。空的 stored `session_id` 被视为兼容旧状态文件，匹配任意请求 session。active 状态文件优先级为 `methodology-analysis-state.md` > `finalize-state.md` > `state.md`。

**Algorithm subset covered**

覆盖文件：

- [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:39): `session_id` 字段常量、hook JSON session 提取、状态文件解析、active/any state 解析、`find_active_loop`。
- [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:41): 项目根解析和 canonicalize 辅助。
- [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:203): session-aware active loop 行为测试。
- [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:33): 多目录、终态、异常目录名、深层目录等鲁棒性测试。

显式不覆盖安装、营销、截图、通用 CLI 用法，也不覆盖未在指定 focus paths 内的 post hook 具体实现。

**Pseudocode**

```text
resolve_project_root():
  root = CLAUDE_PROJECT_DIR
  if root empty:
    root = git rev-parse --show-toplevel
  if root empty:
    fail
  return canonicalize_path(root)

resolve_active_state_file(loop_dir):
  if methodology-analysis-state.md exists: return it
  if finalize-state.md exists: return it
  if state.md exists: return it
  return ""

resolve_any_state_file(loop_dir):
  active = resolve_active_state_file(loop_dir)
  if active not empty: return active
  return first file matching *-state.md, if any

find_active_loop(loop_base_dir, filter_session_id="", allow_bg_marker_fallback="false"):
  if loop_base_dir is not directory:
    return ""

  if filter_session_id empty:
    newest_dir = reverse_lexicographic_first(immediate_child_dirs(loop_base_dir))
    if newest_dir has active state file:
      return newest_dir without trailing slash
    return ""

  marker_candidate = ""
  for dir in reverse_lexicographic_order(immediate_child_dirs(loop_base_dir)):
    any_state = resolve_any_state_file(dir)
    if any_state empty:
      continue

    stored_session_id = parse session_id from YAML frontmatter, delete spaces

    if stored_session_id empty OR stored_session_id == filter_session_id:
      if dir has active state file:
        return dir
      else:
        return ""   # session newest is terminal; do not revive older loop

    if allow_bg_marker_fallback == true
       AND marker_candidate empty
       AND dir/bg-pending.marker exists
       AND dir has active state file:
      marker_candidate = dir

  if allow_bg_marker_fallback == true AND marker_candidate not empty:
    return marker_candidate

  return ""
```

**Transition table**

| Input state | Filter | Gate | Output / transition |
|---|---:|---|---|
| `loop_base_dir` 不存在 | any | `[[ ! -d ]]` | `""` |
| 无 session filter | empty | 只取 reverse-sort 后第一个子目录 | 若有 active state 返回该目录，否则 `""` |
| 有 session filter，扫描到无 state 的目录 | non-empty | `resolve_any_state_file == ""` | 跳过 |
| 有 session filter，stored session 为空 | non-empty | backward compat | 当作匹配当前 session |
| 有 session filter，stored session 相等 | non-empty | exact match | active 则返回；terminal 则立即 `""` |
| 有 session filter，stored session 不等 | non-empty | 默认 strict isolation | 跳过 |
| stored session 不等且允许 bg fallback | non-empty | `bg-pending.marker` + active state | 仅记录候选；无 exact match 后才返回 |
| 最新匹配 session 为 `complete-state.md` / `cancel-state.md` | non-empty | any-state 匹配但 active-state 为空 | 返回 `""`，阻断旧 loop |

**Source evidence**

- `session_id` 是状态字段常量：`FIELD_SESSION_ID="session_id"` 定义在 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:39)。
- hook JSON 的 session 输入只从顶层 `.session_id` 读取，失败为空：见 `extract_session_id()` 的 `jq -r '.session_id // empty'`，位于 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:250)。
- `loop-common.sh` 在初始化时加载 `project-root.sh`，并用 `resolve_project_root` 尝试得到项目根；无项目根时跳过 config 加载，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:176) 和 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:189)。
- 项目根解析优先级明确为 `CLAUDE_PROJECT_DIR`，其次 `git rev-parse --show-toplevel`，不使用 `pwd` 防止 `cd` 漂移导致 `.humanize/rlcr` miss，见 [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:5) 和 [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:10)。
- `resolve_project_root()` 的实际实现：读取 `CLAUDE_PROJECT_DIR`，否则 git toplevel，空则 return 1，并 canonicalize 输出，见 [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/project-root.sh:41)。
- active state 优先级是 `methodology-analysis-state.md`、`finalize-state.md`、`state.md`，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:264) 到 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:280)。
- any state 先走 active state，再 fallback 到任意 `*-state.md`，因此终态文件参与“该 session 最新目录”的判定，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:282) 到 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:305)。
- `find_active_loop` 的注释写明无 filter 只检查最新目录以防 zombie loop，有 filter 则找该 session 最新目录，若最新为终态立即返回空，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:308) 到 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:320)。
- 无 filter 分支使用 `ls -1d "$loop_base_dir"/*/ | sort -r | head -1` 取单个最新子目录，然后只看 active state，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:342) 到 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:356)。
- session filter 分支按新到旧扫描，先 `resolve_any_state_file`，再从 YAML frontmatter 中 `sed` 提取 `session_id` 并 `tr -d ' '` 去空格，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:359) 到 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:383)。
- stored `session_id` 为空或等于 filter 即匹配；匹配后 active 返回目录，非 active 立即返回空，不再扫描旧目录，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:384) 到 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:396)。
- mismatched session 默认隔离；只有 `allow_bg_marker_fallback=true`、存在 `bg-pending.marker` 且仍 active 时记录 marker candidate，且 exact match 优先于 marker fallback，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:399) 到 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:420)。
- tolerant parser `parse_state_file()` 把 frontmatter 读入 `STATE_FRONTMATTER`，经 `_parse_state_fields` 设置 `STATE_SESSION_ID`；`STATE_SESSION_ID` 不做默认值填充，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:446)、[hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:463)、[hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:494)。
- strict parser 校验 frontmatter separator、必需字段、数值字段和 `review_started` boolean；`session_id` 不属于 strict 必需字段，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:533) 到 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:599)。

**Test-backed behavior**

- 匹配 session 返回 active loop；不匹配 session 返回空：见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:203) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:236)。
- stored `session_id:` 为空匹配任意 filter，维持旧状态文件兼容：见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:239) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:260)。
- 无 filter 模式保持 backward compatibility，存在任意 session_id 也能返回最新 active loop：见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:263) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:285)。
- `finalize-state.md` 被视为 active，且 session filter 生效：见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:288) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:317)。
- `parse_state_file` 能读出 `STATE_SESSION_ID`：见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:321) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:345)。
- 有 filter 时会跳过更新但不同 session 的目录，找到较旧的匹配 session；无 filter 时返回最新 active 目录：见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:577) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:630)。
- 匹配 session 的最新目录若为 `complete-state.md`，阻断旧 `state.md` 复活；无 filter 时最新为终态也返回空：见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:634) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:683)。
- 不同 session 相互隔离：session A 最新为终态返回空，不影响 session B 找到自己的 active loop，见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:687) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:744)。
- `cancel-state.md` 也作为终态阻断旧 active loop 复活：见 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:748) 到 [tests/test-session-id.sh](/Users/wangweiyang/GitHub/humanize/tests/test-session-id.sh:783)。
- 鲁棒性测试确认无 filter 时多目录选 reverse-sort 最新 active，`finalize-state.md` 可检测，15 个目录性能小于 1000ms，见 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:33) 到 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:87)。
- zombie 保护：最新目录无 active state 时，即使旧目录有 `state.md` 也返回空，见 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:89) 到 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:102)。
- 空目录、不存在目录、无子目录、所有子目录无 state 都返回空：见 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:128) 到 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:177)。
- 目录名不要求时间格式；空格目录名可用；深层路径不会被递归扫描，只看 base 下一级子目录：见 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:179) 到 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:238)。
- 只有 `complete-state.md` 或 `cancel-state.md` 的目录无 filter 下被忽略；最新 finished、旧 active 时仍返回空，见 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:259) 到 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:299)。

**Edge cases and risks**

- 目录“新旧”由字符串 reverse sort 决定，不解析时间戳；非标准命名被接受，但排序语义可能与真实创建时间不同。测试明确允许非标准目录名，见 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:179)。
- 无 filter 模式只看一个最新目录；这是有意的 zombie-loop protection，但代价是最新目录损坏或终态时，不会自动找旧 active loop。
- session filter 模式会扫描所有 immediate child dirs；规模很大时成本为 `O(n log n)` 排序加 `O(n)` state 读取。测试仅覆盖 15 个目录小于 1000ms，见 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:63)。
- `stored_session_id` 提取时 `tr -d ' '` 删除普通空格，因此 session id 内的空格无法被精确保留；`_parse_state_fields` 对 `STATE_SESSION_ID` 不删除空格，两处语义不完全一致，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:382) 与 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:463)。
- `resolve_any_state_file` 对 terminal fallback 用 `ls "$loop_dir"/*-state.md | head -1`，若同一目录存在多个 terminal state，选择由 shell/ls 排序决定；算法没有冲突检测，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:302)。
- active state 优先级中 `methodology-analysis-state.md` 高于 `finalize-state.md` 高于 `state.md`；如果同一目录同时存在多个 active 文件，不报错，只按优先级选择。
- symlinked session dir 被鲁棒性测试接受为“非空结果”，但没有在 `find_active_loop` 内做 canonicalization 或 symlink 拒绝；路径安全主要依赖其他调用点的 canonicalize 逻辑，见 [tests/robustness/test-session-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-session-robustness.sh:194)。
- marker fallback 是 routing 例外：只在显式第三参为 `"true"` 时允许 mismatched session adoption；若调用方误开该参数，会削弱 strict session isolation。实现注释声明只有 stop hook 应 opt in，见 [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:325)。

**What is explicitly out of scope**

- 不分析安装脚本、README、截图、营销文本或通用使用说明。
- 不分析非 focus paths 中的 hook 调用链，例如具体哪个 validator 如何传入 `session_id`，除非该行为已由指定测试文件体现。
- 不分析 `loop-bg-tasks.sh` 的背景任务状态机；这里只覆盖 `find_active_loop` 中暴露出的 `bg-pending.marker` fallback 路由规则。
- 不运行测试、不修改文件、不提交。当前工作只基于 read-only 源码与测试证据。