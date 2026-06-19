**Topic and conclusion**

Topic: Todo transcript checker

结论: 该机制是一个“停止前任务闸门”。它从两个来源合并未完成项: 新 Task 系统的会话任务目录，以及旧 TodoWrite transcript 的最后一次 todo 快照。只要存在非 `completed` 且非 `queued` lane 的未完成项，就输出 `INCOMPLETE_TODOS` 并以 exit `1` 阻断；无未完成项或无可读任务源时 exit `0` 放行；hook 输入 JSON 本身不可解析时 exit `2`。

**Algorithm subset covered**

覆盖范围仅限以下算法相关文件:

- [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:1): 核心解析、lane 分类、Task 目录扫描、TodoWrite transcript 扫描、退出码与输出格式。
- [tests/test-todo-checker.sh](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:1): 行为断言，包括输入异常、TodoWrite 状态、Task 文件状态、queued/blocking lane、混合来源。
- [prompt-template/block/incomplete-todos.md](/Users/wangweiyang/GitHub/humanize/prompt-template/block/incomplete-todos.md:1): 阻断时展示给模型的恢复动作要求。

未覆盖安装、营销、截图、一般用法说明；只引用定义行为的部分。

**Pseudocode**

```text
state:
  incomplete_items = []
  latest_todos = []
  lane_prefix_pattern = r"^\s*\[(mainline|blocking|queued)\](?:\s|$)"

input:
  stdin JSON hook_input:
    session_id?
    tasks_base_dir?
    transcript_path?

main:
  stdin_content = read_stdin().strip()
  if stdin_content == "":
      exit 0

  try:
      hook_input = json.loads(stdin_content)
  except JSONDecodeError:
      stderr "PARSE_ERROR: ..."
      exit 2

  if hook_input.session_id:
      incomplete_items += scan_task_directory(session_id, tasks_base_dir)

  if hook_input.transcript_path:
      incomplete_items += scan_transcript_latest_todowrite(transcript_path)

  if incomplete_items is empty:
      exit 0

  print "INCOMPLETE_TODOS"
  for item in incomplete_items:
      print formatted item with status, lane, source, and task id if source == task
  exit 1
```

```text
classify_lane(parts...):
  for part in parts:
    if part starts with [mainline], [blocking], or [queued], ignoring leading spaces and case:
      return matched lane lowercased
  return "blocking"
```

```text
scan_task_directory(session_id, tasks_base_dir):
  tasks_dir = tasks_base_dir/session_id if override exists else ~/.claude/tasks/session_id
  if tasks_dir does not exist or is not directory:
      return []

  for each *.json file:
    try parse task JSON
    except JSONDecodeError or OSError:
      skip file

    status = task.status or "pending"
    if status in ("completed", "deleted"):
      continue

    subject = task.subject or ""
    description = task.description or ""
    content = subject or description or "Task <task_id>"
    lane = classify_lane(subject, description)
    if lane == "queued":
      continue

    append incomplete task with status, content, source="task", task_id, lane

  return incomplete
```

```text
scan_transcript_latest_todowrite(transcript_path):
  if transcript file does not exist:
      return []

  for each non-empty line:
    try parse JSON
    except JSONDecodeError:
      continue

    extract tool_use calls from:
      type == "assistant": entry.message.content[]
      type == "message": entry.content[]
      type == "tool_use": entry.name/input or tool_name/tool_input

    for each tool call:
      if tool_name == "TodoWrite" and input.todos is truthy:
          latest_todos = input.todos

  for todo in latest_todos:
    status = todo.status or ""
    if status == "completed":
      continue

    content = todo.content or ""
    lane = classify_lane(content)
    if lane == "queued":
      continue

    append incomplete todo with status, content, source="todo", lane

  return incomplete
```

**Transition table**

| 条件 | 状态转移 / 输出 | gate |
|---|---|---|
| stdin 为空 | 不解析任务源，直接 exit `0` | 放行 |
| stdin 不是合法 JSON | stderr 输出 `PARSE_ERROR`，exit `2` | hook 输入错误 |
| 无 `session_id` 且无 `transcript_path` | `incomplete_items=[]`，exit `0` | 放行 |
| Task 目录不存在 | Task 来源返回空列表 | 放行或继续检查 transcript |
| Task status 为 `completed` 或 `deleted` | 忽略 | 不阻断 |
| Task status 缺失 | 默认 `pending` | 可能阻断 |
| TodoWrite status 为 `completed` | 忽略 | 不阻断 |
| TodoWrite status 缺失或非 `completed` | 作为未完成候选 | 可能阻断 |
| lane 前缀是 `[queued]` | 从未完成列表中过滤 | 不阻断 |
| lane 无前缀或前缀不在白名单 | 默认 `blocking` | 阻断 |
| 最终未完成列表非空 | stdout 输出 `INCOMPLETE_TODOS` 和明细，exit `1` | 阻断 |

**Source evidence**

- lane 只识别行首标签 `[mainline]`、`[blocking]`、`[queued]`，忽略大小写；无匹配时默认 `blocking`: [hooks/check-todos-from-transcript.py:24](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:24), [hooks/check-todos-from-transcript.py:27](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:27), [hooks/check-todos-from-transcript.py:35](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:35)。
- transcript 工具调用来源有三类: `assistant.message.content[]`、`message.content[]`、直接 `tool_use` entry: [hooks/check-todos-from-transcript.py:46](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:46), [hooks/check-todos-from-transcript.py:47](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:47), [hooks/check-todos-from-transcript.py:49](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:49), [hooks/check-todos-from-transcript.py:63](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:63)。
- legacy TodoWrite 只保留“最后一次有 todos 的 TodoWrite 输入”作为状态快照: [hooks/check-todos-from-transcript.py:82](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:82), [hooks/check-todos-from-transcript.py:99](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:99), [hooks/check-todos-from-transcript.py:101](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:101), [hooks/check-todos-from-transcript.py:102](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:102)。
- TodoWrite 中 `status != "completed"` 即未完成；`queued` lane 被过滤；输出项带 `source="todo"` 和 lane: [hooks/check-todos-from-transcript.py:106](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:106), [hooks/check-todos-from-transcript.py:109](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:109), [hooks/check-todos-from-transcript.py:110](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:110), [hooks/check-todos-from-transcript.py:111](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:111)。
- Task 系统读取 `~/.claude/tasks/<session_id>/`，测试可通过 `tasks_base_dir` 覆盖；目录不存在返回空: [hooks/check-todos-from-transcript.py:123](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:123), [hooks/check-todos-from-transcript.py:136](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:136), [hooks/check-todos-from-transcript.py:139](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:139), [hooks/check-todos-from-transcript.py:140](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:140)。
- Task status 缺省为 `pending`；只有 `completed` 和 `deleted` 不算未完成；content 优先级为 `subject`、`description`、`Task <id>`: [hooks/check-todos-from-transcript.py:149](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:149), [hooks/check-todos-from-transcript.py:150](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:150), [hooks/check-todos-from-transcript.py:152](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:152), [hooks/check-todos-from-transcript.py:155](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:155)。
- Task lane 从 `subject` 和 `description` 推断；`queued` 被过滤；坏 JSON 或不可读任务文件被跳过: [hooks/check-todos-from-transcript.py:156](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:156), [hooks/check-todos-from-transcript.py:157](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:157), [hooks/check-todos-from-transcript.py:166](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:166)。
- main 先检查 Task 目录，再检查 legacy transcript，并把两个来源累加: [hooks/check-todos-from-transcript.py:186](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:186), [hooks/check-todos-from-transcript.py:191](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:191), [hooks/check-todos-from-transcript.py:192](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:192), [hooks/check-todos-from-transcript.py:196](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:196), [hooks/check-todos-from-transcript.py:198](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:198)。
- exit 语义: 空 stdin exit `0`，输入 JSON 解析错误 exit `2`，无未完成项 exit `0`，有未完成项输出 marker 后 exit `1`: [hooks/check-todos-from-transcript.py:176](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:176), [hooks/check-todos-from-transcript.py:179](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:179), [hooks/check-todos-from-transcript.py:181](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:181), [hooks/check-todos-from-transcript.py:184](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:184), [hooks/check-todos-from-transcript.py:200](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:200), [hooks/check-todos-from-transcript.py:219](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:219), [hooks/check-todos-from-transcript.py:221](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:221)。
- 输出格式区分 Task 和 TodoWrite: Task 项包含 `Task #<id>`，TodoWrite 项不含 task id: [hooks/check-todos-from-transcript.py:212](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:212), [hooks/check-todos-from-transcript.py:214](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:214), [hooks/check-todos-from-transcript.py:216](/Users/wangweiyang/GitHub/humanize/hooks/check-todos-from-transcript.py:216)。
- 测试确认关键行为: 非法 stdin JSON exit `2`: [tests/test-todo-checker.sh:52](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:52)；空 stdin exit `0`: [tests/test-todo-checker.sh:64](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:64)；多次 TodoWrite 使用最新快照: [tests/test-todo-checker.sh:227](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:227)；`in_progress` 阻断: [tests/test-todo-checker.sh:145](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:145), [tests/test-todo-checker.sh:373](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:373)；`queued` 不阻断: [tests/test-todo-checker.sh:160](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:160), [tests/test-todo-checker.sh:390](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:390)；行内 `[queued]` 不降级: [tests/test-todo-checker.sh:175](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:175), [tests/test-todo-checker.sh:424](/Users/wangweiyang/GitHub/humanize/tests/test-todo-checker.sh:424)。
- prompt 模板要求停止前完成所有任务、用 `TaskUpdate` 标成 `completed`，完成前不得进入 Codex review: [prompt-template/block/incomplete-todos.md:3](/Users/wangweiyang/GitHub/humanize/prompt-template/block/incomplete-todos.md:3), [prompt-template/block/incomplete-todos.md:7](/Users/wangweiyang/GitHub/humanize/prompt-template/block/incomplete-todos.md:7), [prompt-template/block/incomplete-todos.md:9](/Users/wangweiyang/GitHub/humanize/prompt-template/block/incomplete-todos.md:9), [prompt-template/block/incomplete-todos.md:12](/Users/wangweiyang/GitHub/humanize/prompt-template/block/incomplete-todos.md:12)。

**Edge cases and risks**

- 失效放行风险: transcript 文件不存在、Task 目录不存在、空 stdin、无 `session_id`/`transcript_path` 都会 exit `0`。这适合避免误阻断，但也意味着上游未传递路径或会话 ID 时无法发现未完成任务。
- 坏行容忍: transcript 中单行 JSON 解析失败会被忽略，Task 目录中坏 JSON 或 OSError 文件也会被跳过；这降低 hook 脆弱性，但可能漏报损坏任务文件。
- TodoWrite 状态模型是“最后快照”而不是事件归并。旧 pending 任务如果后来被最后一次 TodoWrite 快照移除，就不会阻断；测试明确期望该行为。
- Task 与 TodoWrite 来源是累加关系。混合场景中任一来源发现未完成项都会阻断；测试覆盖“legacy completed + new task pending”仍 exit `1`。
- lane 识别只看开头标签。正文中出现 `[queued]` 不会绕过阻断，这是刻意的安全默认；但如果用户把 lane 标签写在非开头位置，也不会生效。
- lane 默认 `blocking`。任何无标签、空 content、缺 status 的非完成项都会阻断；这偏保守。
- Task status 只有 `completed` 和 `deleted` 被视为完成/忽略。任何新状态名，例如 `cancelled`、`skipped`、`done`，都会被当成未完成。
- 输出顺序对 Task 文件依赖 `Path.glob("*.json")` 的迭代顺序，代码没有排序；这不影响 gate 判定，但会影响明细展示稳定性。
- prompt 要求用 `TaskUpdate` 完成任务，但 legacy TodoWrite 项本身没有 task id；恢复动作对 TodoWrite 来源可能需要上游工具/模型根据上下文映射。

**What is explicitly out of scope**

- 不分析 hook 如何被注册、何时触发、由哪个上游系统消费 exit code。
- 不分析 Claude Code TaskCreate/TaskUpdate 的完整协议，只分析本 checker 读取到的 task JSON 字段。
- 不分析 `INCOMPLETE_TODOS` marker 之后的模板注入链路，只覆盖模板本身表达的阻断要求。
- 不运行测试、不安装依赖、不联网、不检查截图、README、营销文案或通用使用说明。
- 不评估安全边界之外的文件系统权限、真实 `~/.claude/tasks` 内容或用户环境中的实时任务状态。