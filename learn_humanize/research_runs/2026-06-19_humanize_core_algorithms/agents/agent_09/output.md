**Topic and conclusion**

Topic: Background task short-circuit algorithm, centered on `hooks/lib/loop-bg-tasks.sh`.

Conclusion: 该算法在 Stop Hook 正常 gate/Codex review 之前运行，用 Claude transcript 推导“本轮 RLCR loop 是否仍有未完成后台任务”。若存在未完成后台 Agent/Bash 任务，则 `exit 0` 允许本次 stop 自然结束、输出 `systemMessage`、写入 `bg-pending.marker`，并跳过后续 gate/Codex；若是跨 session 访问已 parked loop，则同样 `exit 0` 但保持 loop 状态不变；若能权威确认同 session 已无 pending bg，则清理 stale marker 并回到正常 Stop Hook 流程。核心判定是集合差：`pending = launched - completed`，再经 liveness probe 剪枝。

**Algorithm subset covered**

覆盖的算法子集只包括：

- `hooks/lib/loop-bg-tasks.sh` 中的 transcript 路径解析、loop 起点时间推导、pending bg task 枚举、liveness probe、四段 Stop Hook guard。
- `tests/test-stop-hook-bg-allow.sh` 中直接验证短路、completion 识别、marker、跨 session、since_ts、liveness probe 的用例。
- `tests/test-monitor-e2e-sigint.sh` 仅作为 SIGINT 测试分片入口；它只 source 另一个测试文件并调用 bash/zsh SIGINT 测试函数，没有定义 background short-circuit 行为。

关键状态变量：

- `loop_dir`: 当前 RLCR loop 目录。
- `hook_input`: Stop Hook 输入 JSON。
- `hook_session_id`: 当前 Claude session id。
- `transcript_path`: 从 hook JSON 的 `.transcript_path` 取出，并支持 `~` / `~/...` 展开。
- `loop_start_ts`: 从 loop 目录名 `YYYY-MM-DD_HH-MM-SS` 解析为 UTC ISO-8601，用于过滤 pre-loop transcript events。
- `bg-pending.marker`: loop parked 信号文件。
- `stored_session_id`: active state file frontmatter 中的 `session_id`。
- `launched`: transcript 中已启动的后台任务 id 集合。
- `completed`: transcript 中已终止的后台任务 id 集合。
- `pending`: `launched - completed`，再经过输出文件/lsof liveness probe 剪枝后的集合。

**Pseudocode**

```text
handle_bg_task_short_circuit(loop_dir, hook_input, hook_session_id):
    loop_start_ts = derive_loop_start_iso_ts(loop_dir)
    transcript_path = extract_transcript_path(hook_input)

    if exists(loop_dir/bg-pending.marker) and hook_session_id == "":
        exit 0 silently

    if exists(loop_dir/bg-pending.marker):
        stored_session_id = read session_id from active state file
        if stored_session_id != "" and hook_session_id != "" and stored_session_id != hook_session_id:
            print JSON systemMessage: parked by another session
            exit 0

    pending_bg_ids = list_pending_background_task_ids(transcript_path, loop_start_ts)
    if pending_bg_ids is non-empty:
        count = number of pending_bg_ids
        touch loop_dir/bg-pending.marker
        print JSON systemMessage: count background task(s) still running
        exit 0

    if exists(loop_dir/bg-pending.marker):
        pending_bg_check = list_pending_background_task_ids(transcript_path, loop_start_ts)
        if list succeeded and pending_bg_check is empty:
            rm loop_dir/bg-pending.marker

    return 0 to normal stop-hook gates
```

Pending 集合算法：

```text
list_pending_background_task_ids(transcript_path, since_ts):
    transcript_path = expand leading "~"
    if transcript_path empty or not regular file: return 1
    if jq missing: return 1

    launched =
        all transcript rows where toolUseResult exists
        and (since_ts empty or timestamp empty or timestamp >= since_ts)
        and (
            toolUseResult.isAsync == true and agentId non-empty
            or backgroundTaskId non-empty
        )
        map id = agentId or backgroundTaskId
        sort unique

    completed =
        union of:
            system/task_notification rows: task_id
            legacy queue-operation enqueue rows containing <task-notification><task-id>...</task-id>
        sort unique, remove empty

    pending = launched - completed

    if pending non-empty:
        tasks_dir = /tmp/claude-<uid>/<project-slug>/<session-id>/tasks
        pending = keep only ids where is_bg_task_alive(id, tasks_dir)

    print pending ids, one per line
    return 0
```

Transition table:

| Condition | Action | Output | Mutation | Next |
|---|---|---|---|---|
| `bg-pending.marker` exists and `hook_session_id` empty | ambiguous caller guard | none | none | `exit 0` |
| marker exists, stored session id and hook session id both non-empty and differ | cross-session parked guard | parked `systemMessage` | none | `exit 0` |
| pending bg ids non-empty | short-circuit active loop | count-based `systemMessage` | create/keep `bg-pending.marker` | `exit 0` |
| marker exists, pending helper succeeds and returns empty | stale marker cleanup | none | remove marker | continue normal gates |
| helper fails or no pending without marker | no short-circuit | none | none | continue normal gates |

**Source evidence**

- `loop-bg-tasks.sh` declares this file owns transcript inspection and the four guard blocks: ambiguous caller, cross-session parked loop, pending bg early exit, same-session stale-marker cleanup at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:5) and [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:10).
- `transcript_path` extraction uses jq and leading-tilde expansion at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:23) and [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:38).
- Loop start boundary converts local wall-clock loop dir names into UTC ISO timestamps for lexical transcript comparison at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:48), with parse/format implementation at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:65).
- Task output dir derivation follows `/tmp/claude-<uid>/<project-slug>/<session-id>/tasks` at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:97), implemented at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:107).
- Liveness probe treats absent output file or missing `lsof` as alive/fail-open, then delegates to `lsof` for open-file detection at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:120) and [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:131).
- Transcript launch/completion semantics are documented as async Agent `agentId`, background Bash `backgroundTaskId`, SDK `system/task_notification`, and legacy XML queue-operation at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:156).
- Launch extraction filters by `since_ts`, `timestamp`, `isAsync`, `agentId`, and `backgroundTaskId` at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:209).
- Completion union is built from SDK `task_notification` plus legacy XML `<task-id>` extraction at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:224).
- `pending = launched - completed` uses `comm -23`, then liveness pruning at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:248).
- Helper failure contract is explicit: missing/invalid transcript or missing jq returns `1`, meaning unknown and “do not short-circuit” at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:187).
- Stop Hook entry point computes `loop_start_ts` and `transcript_path` before guards at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:311).
- Ambiguous caller guard exits silently on marker plus empty session id at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:322).
- Cross-session guard reads stored session id and emits parked message without mutation at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:338).
- Pending bg short-circuit must run before phase/state/git/summary/max-iter/Codex gates, writes marker, emits count message, exits 0 at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:369).
- Same-session stale marker cleanup only removes marker after a successful helper call returns empty at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:407).

Test evidence:

- Test file states expected behavior: pending Agent/Bash causes exit 0 + user-facing `systemMessage`, skips gates/Codex, and leaves loop state unchanged until next natural stop at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:3).
- Fixture builders encode async Agent launch, background Bash launch, legacy completion, and SDK completion formats at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:190).
- `assert_systemmessage_only` verifies exit 0, no Codex marker, JSON `systemMessage`, and unchanged state file at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:291).
- AC-1 through AC-6 cover no bg, pending subagent, pending shell, completed subagent, multiple pending count, and missing transcript fail-closed behavior at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:354).
- Cross-session marker behavior preserves marker/state and emits parked message in AC-11 at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:613).
- Short-circuit writes `bg-pending.marker` in AC-11c at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:718).
- Same-session resume removes stale marker when transcript is readable and no pending bg exists in AC-13 at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:793).
- Cross-session stop must preserve marker and stored `session_id` in AC-14 at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:845).
- SDK `system/task_notification` completion removes matching launch from pending in AC-15 at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:901).
- Mixed legacy XML and SDK completions resolve to empty pending set in AC-16 at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:926).
- Missing transcript and nonexistent transcript preserve marker/session id rather than cleaning up on uncertainty in AC-17/AC-17c at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:955).
- Ambiguous no-session caller with existing marker exits silently and preserves state in AC-19 at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:1096).
- Malformed transcript preserves marker in AC-20 at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:1155).
- `since_ts` filters pre-loop launches; derived UTC behavior is tested under UTC/JST/PST in AC-21 variants at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:1205).
- Liveness probe keeps an open output-file task pending and prunes a no-holder output-file task in AC-23/AC-24 at [tests/test-stop-hook-bg-allow.sh](/Users/wangweiyang/GitHub/humanize/tests/test-stop-hook-bg-allow.sh:1410).
- `tests/test-monitor-e2e-sigint.sh` only sources `test-monitor-e2e-real.sh` and calls `monitor_test_bash_sigint` / `monitor_test_zsh_sigint`; no bg short-circuit state machine is defined there at [tests/test-monitor-e2e-sigint.sh](/Users/wangweiyang/GitHub/humanize/tests/test-monitor-e2e-sigint.sh:4) and [tests/test-monitor-e2e-sigint.sh](/Users/wangweiyang/GitHub/humanize/tests/test-monitor-e2e-sigint.sh:12).

**Edge cases and risks**

- `since_ts` derivation failure widens scope: if loop dir basename does not parse or `date` cannot parse/format, `loop_start_ts` is empty, and transcript launch filtering becomes unbounded. That can allow pre-loop background work to pin the loop.
- Timestamp filtering is lexical string comparison. It works for normalized ISO UTC strings like `2026-03-01T00:00:00.000Z`; non-normalized timestamp formats could route incorrectly.
- Events without `.timestamp` are intentionally included to support older transcripts and fixtures. This preserves compatibility but can allow old un-timestamped launches to count as current-loop pending.
- Completion status is not scored: any SDK `task_notification` status, including failed or stopped, is terminal by design. That prevents completed/failed tasks from pinning the loop but does not distinguish success from failure.
- Helper failures are fail-closed for short-circuit: missing transcript, non-file transcript, missing jq, or parse failure mean “unknown”, so the hook should not short-circuit. With an existing marker, cleanup is also blocked unless a successful empty pending result is observed.
- The liveness probe is fail-open when output file is absent or `lsof` is unavailable, so a lost completion event plus absent output file can keep a task looking alive indefinitely.
- There is a comment/code tension in liveness: comments say fail-open for `lsof` non-zero reasons other than “no holders”, but implementation returns the raw `lsof` status, so any non-zero `lsof` result prunes the task as dead. Evidence: comment at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:124), implementation at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-bg-tasks.sh:140).
- Short-circuit comments say loop state is left untouched, but the algorithm does write `bg-pending.marker`. The stricter invariant is: state file/session metadata are not rewritten; marker may be created or later removed by the parking algorithm.
- Ambiguous caller guard deliberately emits no `systemMessage`. This avoids cross-session mutation when `session_id` is missing, but wrappers/users get less visibility when a marker already exists.
- `comm -23` requires sorted inputs; the implementation sorts both launched and completed sets before diffing, so this invariant currently holds.
- `tests/test-stop-hook-bg-allow.sh` header lists AC-1 through AC-20, but the file also contains AC-21 through AC-24. The executable tests are broader than the header summary.

**What is explicitly out of scope**

- Installation flow, README/marketing text, screenshots, generic usage docs.
- Normal Stop Hook gate logic after this helper returns: branch checks, plan checks, git-clean checks, summary checks, max-iteration checks, and Codex review behavior are only relevant as “skipped” or “continued to”, not analyzed internally.
- `find_active_loop` internals beyond behavior asserted by this test file; its marker opt-in behavior is observed through AC-12/AC-18 but not reverse-engineered here.
- `scripts/rlcr-stop-gate.sh` internals; wrapper behavior is only considered where `tests/test-stop-hook-bg-allow.sh` verifies pass-through/ALLOW semantics.
- `test-monitor-e2e-real.sh` and monitor SIGINT implementation details. The focused `tests/test-monitor-e2e-sigint.sh` file is only a delegation wrapper and does not define the background task short-circuit algorithm.
- Runtime execution of tests. I kept the work read-only and did not run network searches or edit files.