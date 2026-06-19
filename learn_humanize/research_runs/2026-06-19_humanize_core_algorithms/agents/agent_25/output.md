**Topic and conclusion**
Topic: Skill monitor and telemetry parsing（`Agent 25`，pinned commit `0ec921a36b4365df503511c5567bbd3e02db0df5`）。结论：核心算法是一个基于 `.humanize/skill/<timestamp...>/` 目录的轮询监控器，使用目录名时间戳排序、`metadata.md`/`input.md` 状态推断、工具过滤和文件优先级路由来选择“当前聚焦 invocation”。遥测解析侧主要有两条：`statusline.sh` 从 Claude status JSON 与 `.humanize/rlcr` 状态文件解析 RLCR 状态；ANSI 测试验证通过可移植 sed 规则先剥离 SGR 颜色码，再抽取 `Passed`/`Failed` 数字。

**Algorithm subset covered**
- Skill invocation 监控入口、参数、状态变量：`_humanize_monitor_skill`、`--once`、`--tool-filter`、`current_skill_dir/current_file/check_interval/status_bar_height`（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:18) lines 18-41）。
- Invocation 目录发现、工具识别、过滤、排序、计数、问题抽取、缓存路径和 watched file 选择（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:50) lines 50-217）。
- `--once` 汇总输出和 interactive tail 循环（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:339) lines 339-527）。
- Statusline 中与 Humanize/RLCR 相关的状态文件解析、session-aware 过滤、颜色映射；泛用 cost/model/session 展示只在影响解析宽度时纳入（[scripts/statusline.sh](/Users/wangweiyang/GitHub/humanize/scripts/statusline.sh:36) lines 36-167, [scripts/statusline.sh](/Users/wangweiyang/GitHub/humanize/scripts/statusline.sh:346) lines 346-403）。
- ANSI 解析测试中的 SGR stripping 和 `Passed`/`Failed` 数字抽取（[tests/test-ansi-parsing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-ansi-parsing.sh:38) lines 38-130）。

**Pseudocode / transition table**
```text
monitor_skill(args):
  state:
    skill_dir=".humanize/skill"
    current_skill_dir="", current_file=""
    check_interval=2, status_bar_height=9
    once_mode=false, tool_filter=""

  parse args:
    --once => once_mode
    --tool-filter <codex|gemini> => tool_filter

  gate:
    if skill_dir missing: return 1

  list_dirs():
    find direct child dirs
    keep basename matching YYYY-MM-DD_HH-MM-SS*
    keep if passes_tool_filter(dir)
    return reverse lexical sort  # newest first because name starts with sortable timestamp

  get_tool(dir):
    if metadata.md has YAML tool: return it
    else if input.md has "- Tool:": return it
    else return unknown

  passes_tool_filter(dir):
    if no filter: pass
    if get_tool(dir) == filter: pass
    if tool unknown and filter == codex: pass  # legacy codex compatibility
    else skip

  count_stats():
    for filtered valid dirs:
      total++
      if metadata.md missing: running++
      else status in {success,error,timeout,empty_response} increments bucket

  find_monitored_file(dir):
    is_running = metadata.md missing
    prefix = gemini-run if tool==gemini else codex-run
    gcache = ~/.cache/humanize/<sanitized-project>/skill-<unique_id>
    lcache = dir/cache

    if running:
      prefer gcache/prefix.log non-empty
      then gcache/prefix.out non-empty
      then gcache/prefix.log even empty
      then legacy non-empty codex/gemini logs
      repeat for lcache
      then input.md
    else:
      prefer dir/output.md non-empty
      then cache prefix.out non-empty
      then cache prefix.log non-empty
      then legacy non-empty codex/gemini out
      repeat for lcache
      then output.md even empty
    else none

  find_best_invocation():
    for dirs newest-first:
      f = find_monitored_file(dir)
      if f exists and non-empty: return dir|f
    fallback: return newest_dir|find_monitored_file(newest_dir)

  once_mode:
    latest = newest filtered dir; if none return 1
    focus = newest invocation with non-empty watchable file, else latest
    print stats, metadata/defaults, question, cache, watched output, recent top 10
    if watched file non-empty: cat it
    else if status running: "(Still running...)"
    else: "(No output available)"

  interactive:
    enter alternate screen, hide cursor, set scroll region
    loop every 2s:
      if skill_dir deleted: cleanup and exit
      focus,file = find_best_invocation()
      if no focus: show waiting
      if focus changed: stop old tail, reset current_file
      draw status bar
      if file changed and non-empty path: clear output area; tail -n +1 -f file
      if no current_file: show "Waiting for skill output..."
```

RLCR status parsing:
```text
resolve_rlcr_display(session_dir):
  methodology-analysis-state.md => Analyzing
  finalize-state.md             => Finalizing
  state.md                      => Active
  first *-state.md              => Capitalized basename without "-state.md"
  otherwise                     => Off

get_rlcr_status(rlcr_dir, session_id):
  if rlcr_dir missing: Off
  has_sid_aware = any state md contains "^session_id: .+"

  if session_id empty:
    if no session-aware files:
      use newest rlcr subdir only
    else:
      newest-to-oldest, return first dir whose chosen state file has stored session_id
    if none: Off

  if session_id provided:
    newest-to-oldest:
      choose finalize-state.md, else state.md, else first *-state.md
      parse session_id from YAML frontmatter with awk
      if missing stored_sid and has_sid_aware: skip
      if missing stored_sid and no sid-aware files: return that dir display
      if stored_sid == session_id: return that dir display
    Off
```

ANSI parsing:
```text
esc = $'\033'
stripped = sed "s/${esc}\[[0-9;]*m//g"
passed = grep -oE 'Passed:[[:space:]]*[0-9]+' | grep -oE '[0-9]+$' | tail -1
failed = grep -oE 'Failed:[[:space:]]*[0-9]+' | grep -oE '[0-9]+$' | tail -1
fallback in simple cases: || echo "0"
```

**Source evidence**
- 入口与状态变量：函数设置 zsh 兼容选项，初始化 `skill_dir`、`current_skill_dir`、`current_file`、`check_interval=2`、`status_bar_height=9`、`once_mode=false`、`tool_filter=""`，并解析 `--once`/`--tool-filter`（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:18) lines 18-41）。
- 根门控：`.humanize/skill` 不存在时输出错误并 `return 1`（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:43) lines 43-48）；测试覆盖 missing dir 和 empty dir 分别失败（[tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize/tests/test-skill-monitor.sh:112) lines 112-133）。
- 工具识别：优先读 `metadata.md` YAML `tool`，再从 `input.md` 的 `- Tool:` fallback，否则 `unknown`（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:50) lines 50-64）。
- 工具过滤：空 filter 全通过；精确匹配通过；`unknown + codex` 兼容 legacy；否则 skip（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:66) lines 66-75）。
- 目录有效性与排序：只接受时间戳前缀目录，`find` 后 `sort -r` 最新优先（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:77) lines 77-95）；非时间戳目录被忽略有测试（[tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize/tests/test-skill-monitor.sh:372) lines 372-389）。
- 聚焦选择：优先“最新且 watched file 非空”的 invocation；没有内容时 fallback 到绝对最新（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:97) lines 97-117）。多 invocation 测试要求最新有内容项成为 focused（[tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize/tests/test-skill-monitor.sh:198) lines 198-243）。
- 状态计数：`metadata.md` 存在则按 `success/error/timeout/empty_response` 计数；缺 metadata 视为 `running`（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:119) lines 119-143）。测试覆盖 success/error/timeout/running/empty_response（[tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize/tests/test-skill-monitor.sh:202) lines 202-230, [tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize/tests/test-skill-monitor.sh:251) lines 251-267, [tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize/tests/test-skill-monitor.sh:352) lines 352-369）。
- 问题抽取：只取 `## Question` 到下一个 `##` 区间内首个非空非标题行，并去前导空白（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:145) lines 145-152）；测试确认多行 question 只显示首行（[tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize/tests/test-skill-monitor.sh:296) lines 296-346）。
- 缓存路径：用 git root 或 pwd，经 sed sanitize，拼成 `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/<sanitized>/skill-<unique_id>`，仅存在才返回（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:154) lines 154-163）。
- watched file 路由：running 优先 cache `.log`，completed 优先 `output.md` 非空，再 cache `.out/.log`，支持 codex/gemini prefix 与 legacy fallback（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:165) lines 165-217）。
- `--once` 输出：无 invocation 返回 1；否则打印总数、bucket、focused metadata、watched output、最近 10 条（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:339) lines 339-425）。
- interactive 循环：alternate screen、scroll region、trap cleanup、目录删除退出、focus/file 变化时重启 `tail -n +1 -f`（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:428) lines 428-527）。
- RLCR 状态解析：状态文件优先级为 `methodology-analysis-state.md`、`finalize-state.md`、`state.md`、任意 `*-state.md`，否则 `Off`（[scripts/statusline.sh](/Users/wangweiyang/GitHub/humanize/scripts/statusline.sh:36) lines 36-63）。
- RLCR session gate：预扫描是否存在 `session_id`；有 session id 时 newest-to-oldest 匹配；有 session-aware 文件时跳过 session-unaware entries（[scripts/statusline.sh](/Users/wangweiyang/GitHub/humanize/scripts/statusline.sh:65) lines 65-155）。
- RLCR 颜色路由：`Active|Finalizing` 绿，`Complete` 青，`Cancel|Stop|Pause` 黄，`Maxiter|Failed|Timeout` 红，`Off` dim，其他黄（[scripts/statusline.sh](/Users/wangweiyang/GitHub/humanize/scripts/statusline.sh:157) lines 157-167）。
- ANSI parsing：测试明确使用 `$'\033'` 与 `sed "s/${esc}\\[[0-9;]*m//g"`，目标是 GNU/BSD sed 可移植；随后通过 grep 抽取计数（[tests/test-ansi-parsing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-ansi-parsing.sh:38) lines 38-47, [tests/test-ansi-parsing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-ansi-parsing.sh:74) lines 74-90, [tests/test-ansi-parsing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-ansi-parsing.sh:116) lines 116-125）。

**Edge cases and risks**
- `metadata.md` 缺失即判定 running；如果已完成但 metadata 写入失败，会被统计为 running，并优先展示 log/input（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:173) lines 173-207）。
- `tool` 缺失时被视为 `unknown`；在 `--tool-filter codex` 下 legacy 目录会被包含，在 `gemini` 下会被排除，可能造成历史 Gemini invocation 不可见（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:68) lines 68-75）。
- 排序依赖目录名时间戳的反向字典序；只要命名保持 `YYYY-MM-DD_HH-MM-SS...`，不需要读文件 mtime，但错误命名会被完全忽略（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:77) lines 77-90）。
- `find_best_invocation` 会跳过最新但空输出的 completed invocation，聚焦到较旧但有内容的 invocation；这是设计行为，但会让“Focused”不总是绝对最新（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:97) lines 97-117）。
- 文件路径返回格式用 `dir|file` 管道分隔；若路径本身含 `|`，shell split 会误切。当前生成目录和缓存路径通常不会含此字符，但算法没有转义（[scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/monitor-skill.sh:99) lines 99-116）。
- ANSI stripping 只覆盖 SGR 形态 `ESC[` + `[0-9;]*` + `m`；不会剥离光标移动、OSC、清屏等非颜色 ANSI 序列（[tests/test-ansi-parsing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-ansi-parsing.sh:45) lines 45-47）。
- `statusline.sh` 的 `strip_ansi` 用 `sed 's/\x1b\[[0-9;]*m//g'`，而测试强调 `$'\033'` 方式是 GNU/BSD sed 可移植方案；两者存在可移植性风格不一致风险（[scripts/statusline.sh](/Users/wangweiyang/GitHub/humanize/scripts/statusline.sh:346) lines 346-349, [tests/test-ansi-parsing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-ansi-parsing.sh:38) lines 38-47）。
- RLCR 无 `filter_session_id` 且没有 session-aware 文件时只看 newest dir，意图是 zombie-loop protection；这会忽略较旧但仍有状态文件的目录（[scripts/statusline.sh](/Users/wangweiyang/GitHub/humanize/scripts/statusline.sh:82) lines 82-92）。

**What is explicitly out of scope**
- 未分析安装流程、README/营销文案、截图、命令帮助文本、Claude statusline 的通用 cost/model/branch/session 展示逻辑，除非它影响 RLCR/ANSI 宽度解析。
- 未运行测试、未执行交互式 monitor；本任务按要求只读检查源码和测试断言。
- 未分析 `ask-codex`/`ask-gemini` invocation 的创建算法、metadata 写入方、cache 写入方、`monitor-common.sh` 的 YAML/timestamp helper 实现。
- 未做网络搜索、未编辑文件、未提交。