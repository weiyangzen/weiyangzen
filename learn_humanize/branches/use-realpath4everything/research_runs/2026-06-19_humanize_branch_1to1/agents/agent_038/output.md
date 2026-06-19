# agent_038 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-038 `file` `hooks/check-todos-from-transcript.py`
- cursor: `[_]`
- core_role:
  - Stop-hook preflight validator for RLCR/task completion. It prevents the main stop/review path from continuing while Claude Code still has unfinished native Task-system tasks or legacy `TodoWrite` todos.
  - It is a lightweight gate, not the main RLCR state machine itself: it emits process exit codes and a plain-text incomplete list, and `hooks/loop-codex-stop-hook.sh` converts those results into hook JSON decisions.
  - The script explicitly supports two task state surfaces: transcript-parsed legacy `TodoWrite` calls and file-backed Claude task JSON under `~/.claude/tasks/<session_id>/`, with the file-backed Task directory described as authoritative in comments at `hooks/check-todos-from-transcript.py:123-129`.

- algorithmic_behavior:
  - Lane classification is prefix-only. `LANE_PREFIX_PATTERN` accepts only leading `[mainline]`, `[blocking]`, or `[queued]` markers, case-insensitive, followed by whitespace or end-of-string at `hooks/check-todos-from-transcript.py:24`. `classify_lane()` checks provided text parts in order and defaults to `blocking` if no leading lane tag is found at `hooks/check-todos-from-transcript.py:27-35`.
  - Transcript extraction handles three transcript shapes:
    - `type == "assistant"` with tool blocks in `message.content`;
    - `type == "message"` with tool blocks in `content`;
    - direct `type == "tool_use"` entries using either `name`/`input` or `tool_name`/`tool_input`.
    These are implemented in `extract_tool_calls_from_entry()` at `hooks/check-todos-from-transcript.py:38-70`.
  - Legacy todo scanning reads JSONL line by line, ignores blank and malformed JSONL lines, extracts every `TodoWrite` call, and keeps only the most recent non-empty `todos` array as the current legacy todo state at `hooks/check-todos-from-transcript.py:73-103`.
  - Legacy incomplete detection treats any todo whose `status` is not exactly `"completed"` as incomplete, except leading `[queued]` items, which are ignored at `hooks/check-todos-from-transcript.py:104-120`.
  - File-backed Task scanning builds the task directory from either test override `tasks_base_dir/session_id` or default `Path.home() / ".claude" / "tasks" / session_id` at `hooks/check-todos-from-transcript.py:136-140`. It scans `*.json`, loads each task, defaults missing status to `"pending"`, treats statuses other than `"completed"` and `"deleted"` as incomplete, derives display content from `subject`, then `description`, then `Task <task_id>`, and skips leading `[queued]` tasks at `hooks/check-todos-from-transcript.py:143-170`.
  - `main()` reads JSON hook input from stdin, exits success for empty stdin, exits parse-error for invalid JSON, aggregates incomplete file-backed tasks first and legacy transcript todos second, and exits success only if the aggregate list is empty at `hooks/check-todos-from-transcript.py:173-202`.
  - When incomplete work exists, output starts with marker `INCOMPLETE_TODOS`, followed by one formatted line per blocker. Task-system entries include `(Task #<id>)`; legacy todos do not. This output contract is implemented at `hooks/check-todos-from-transcript.py:204-221`.

- inputs_outputs_state:
  - Inputs:
    - stdin JSON hook input, expected to include optional `session_id`, optional `transcript_path`, and optional test-only `tasks_base_dir` at `hooks/check-todos-from-transcript.py:173-198`.
    - legacy transcript JSONL file referenced by `transcript_path`, read as UTF-8 at `hooks/check-todos-from-transcript.py:85`.
    - Claude task JSON files under `~/.claude/tasks/<session_id>/*.json`, or `tasks_base_dir/<session_id>/*.json` when overridden for tests, at `hooks/check-todos-from-transcript.py:136-147`.
  - Outputs:
    - exit `0`: all detected tasks complete, deleted, queued, absent, or no usable task surfaces exist; documented at `hooks/check-todos-from-transcript.py:9-11` and implemented at `hooks/check-todos-from-transcript.py:177-179`, `200-202`.
    - exit `1`: incomplete non-queued work exists; emits `INCOMPLETE_TODOS` plus formatted blockers on stdout at `hooks/check-todos-from-transcript.py:204-221`.
    - exit `2`: stdin hook input is invalid JSON; emits `PARSE_ERROR: ...` on stderr at `hooks/check-todos-from-transcript.py:181-184`.
  - State transitions:
    - Internal legacy state is `latest_todos`, overwritten by each later non-empty `TodoWrite.todos` list in transcript order at `hooks/check-todos-from-transcript.py:82-103`.
    - There is no persistent mutation. The script is read-only with respect to transcript and task files.
    - Logical gate state transitions are delegated to the caller: `hooks/loop-codex-stop-hook.sh` runs this checker at `hooks/loop-codex-stop-hook.sh:408-413`; exit `2` becomes a `decision: block` parse-error response at `hooks/loop-codex-stop-hook.sh:415-431`; exit `1` becomes a `decision: block` incomplete-task response at `hooks/loop-codex-stop-hook.sh:434-455`.

- gates_or_invariants:
  - Fail-closed for malformed hook input: invalid stdin JSON blocks via exit `2`; the caller turns that into a block response rather than allowing a stop with unknown task state.
  - Fail-open for missing task surfaces: empty stdin, missing `session_id`, missing `transcript_path`, non-existent transcript file, and non-existent task directory all produce no incomplete items and therefore exit `0`.
  - Completion invariant is strict by status string: for legacy todos, only `status == "completed"` is complete; for file-backed tasks, only `status in ("completed", "deleted")` is non-blocking.
  - Lane invariant is prefix-scoped: `[queued]` only bypasses the gate if it appears at the start of `content`, `subject`, or `description` according to `LANE_PREFIX_PATTERN`. Inline text containing `[queued]` remains blocking because the regex anchors at string start.
  - Default-lane invariant is conservative: untagged tasks are `blocking`, preventing accidental bypass when a task lacks lane metadata.
  - Aggregation invariant: task-directory and transcript blockers are additive. A complete legacy todo list does not cancel an incomplete file-backed task, and vice versa.

- dependencies_and_callers:
  - Python standard library only: `json`, `re`, `sys`, `pathlib.Path`, and typing `List`, `Tuple` at `hooks/check-todos-from-transcript.py:17-21`.
  - Direct shell caller is `hooks/loop-codex-stop-hook.sh`, which sets `TODO_CHECKER="$SCRIPT_DIR/check-todos-from-transcript.py"` and runs it with the raw hook input at `hooks/loop-codex-stop-hook.sh:408-413`.
  - Caller output integration:
    - exit `2` renders a parse-error block with `jq` at `hooks/loop-codex-stop-hook.sh:415-431`;
    - exit `1` strips the marker with `tail -n +2`, renders `prompt-template/block/incomplete-todos.md`, and emits `decision: block` at `hooks/loop-codex-stop-hook.sh:434-455`.
  - The incomplete-task message template consumes `{{INCOMPLETE_LIST}}` and instructs completion via `TaskUpdate` status `"completed"` at `prompt-template/block/incomplete-todos.md:1-10`.
  - `tests/run-all-tests.sh` includes `test-todo-checker.sh` in the default test suite list at `tests/run-all-tests.sh:59-64`.

- edge_cases_or_failure_modes:
  - Malformed JSONL transcript lines are silently ignored, so a damaged transcript can hide legacy todo updates if those updates are on malformed lines. This is intentional per implementation at `hooks/check-todos-from-transcript.py:91-94` and covered by tests.
  - Malformed or unreadable task JSON files are silently skipped at `hooks/check-todos-from-transcript.py:166-168`, which favors availability over fail-closed behavior for individual task files.
  - Empty `TodoWrite.todos` arrays do not replace `latest_todos` because the update only happens when `if todos:` is true at `hooks/check-todos-from-transcript.py:100-102`. A later explicit empty todo list in the transcript would therefore not clear earlier pending legacy todos.
  - Non-list `content` blocks in transcript entries are ignored because extraction only iterates when `content` is a list at `hooks/check-todos-from-transcript.py:55-62`.
  - Any non-empty unknown status, and missing legacy todo status, blocks because the status is compared only to `"completed"` at `hooks/check-todos-from-transcript.py:107-110`.
  - Missing file-backed task status defaults to `"pending"` and blocks at `hooks/check-todos-from-transcript.py:149-150`.
  - Task directory ordering is filesystem/glob order, not sorted, so incomplete output order for file-backed tasks is not guaranteed by the script.
  - If both `subject` and `description` exist and only `description` has a leading lane tag, `classify_lane(subject, description)` checks subject first; an untagged subject followed by `[queued]` description will still become queued because `classify_lane` continues until it finds a matching prefix. If subject has any explicit lane tag, it wins.
  - The script itself does not validate RLCR checklist cursor vocabulary (`[ ]`, `[_]`, `[x]`). Its role is native Claude task/todo completion gating, so it is adjacent to, but not itself a checker for, the execution-cron dual-cursor protocol.

- validation_or_tests:
  - Dedicated test script: `tests/test-todo-checker.sh`.
  - Covered input handling includes invalid stdin JSON exit `2`, empty stdin exit `0`, missing `transcript_path`, and non-existent transcript path at `tests/test-todo-checker.sh:52-98`.
  - Covered legacy todo behavior includes all-complete, pending, in-progress, leading `[queued]` bypass, inline `[queued]` still blocking, empty transcript, malformed JSONL lines ignored, latest `TodoWrite` wins, direct `tool_use`, and `type: message` formats at `tests/test-todo-checker.sh:107-271`.
  - Covered legacy edge cases include missing status as incomplete, empty content as incomplete, and Unicode content at `tests/test-todo-checker.sh:280-324`.
  - Covered file-backed Task behavior includes pending default, completed, in-progress, leading `[queued]` bypass, explicit `[blocking]`, inline `[queued]` still blocking, mixed complete/incomplete tasks, all complete, deleted ignored, mixed legacy plus file-backed task surfaces, Task ID output, and non-existent session directory at `tests/test-todo-checker.sh:339-535`.
  - I did not modify files. I also did not run the test suite; repository inspection was read-only. A `git status --short` check could not complete in this branch export because the environment reported it was not a git repository and macOS tooling could not create temp/cache files under the sandbox.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1/1 evidence sections present`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`