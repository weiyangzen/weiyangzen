# agent_023 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-023 `file` `hooks/check-todos-from-transcript.py`
- cursor: `[_]`
- core_role:
  - `hooks/check-todos-from-transcript.py` is a stop-hook helper/validator for the RLCR loop. Its role is to inspect Claude Code’s transcript and determine whether the latest native `TodoWrite` state still contains unfinished work before the heavier Codex review path runs.
  - It is invoked by `hooks/loop-codex-stop-hook.sh` as the “Quick Check: Are All Todos Completed?” gate at `hooks/loop-codex-stop-hook.sh:339`. The stop hook sets `TODO_CHECKER="$SCRIPT_DIR/check-todos-from-transcript.py"` at `hooks/loop-codex-stop-hook.sh:345`, pipes the original hook input JSON into it at `hooks/loop-codex-stop-hook.sh:349`, and treats exit `1` as a blocking incomplete-todo condition at `hooks/loop-codex-stop-hook.sh:371`.
  - In the RLCR state machine, this file does not mutate loop state directly. It is a read-only decision component whose exit code and stdout drive the parent stop hook’s block/allow transition.

- algorithmic_behavior:
  - Entry point `main()` reads all stdin, strips it, and parses it as hook input JSON at `hooks/check-todos-from-transcript.py:93`.
  - Empty stdin is treated as no transcript context and exits success at `hooks/check-todos-from-transcript.py:95`.
  - Invalid hook-input JSON emits `PARSE_ERROR: ...` to stderr and exits `2` at `hooks/check-todos-from-transcript.py:99`.
  - It extracts `transcript_path` from the parsed hook input at `hooks/check-todos-from-transcript.py:104`. Missing path exits success at `hooks/check-todos-from-transcript.py:105`.
  - It expands `~` in the transcript path at `hooks/check-todos-from-transcript.py:109`.
  - `find_latest_todos(transcript_path)` is the parser core at `hooks/check-todos-from-transcript.py:20`.
  - If the transcript file does not exist, `find_latest_todos()` returns an empty list at `hooks/check-todos-from-transcript.py:25`, causing the main path to allow exit at `hooks/check-todos-from-transcript.py:114`.
  - The parser reads transcript JSONL line by line at `hooks/check-todos-from-transcript.py:30`, strips blank lines at `hooks/check-todos-from-transcript.py:31`, skips empty lines at `hooks/check-todos-from-transcript.py:33`, and ignores malformed JSONL records at `hooks/check-todos-from-transcript.py:36`.
  - It supports three transcript shapes:
    - Claude Code assistant-message shape: `entry.type == "assistant"`, `entry.message.content[]`, `block.type == "tool_use"`, `block.name == "TodoWrite"` at `hooks/check-todos-from-transcript.py:51`.
    - Alternative message shape: `entry.type == "message"`, `entry.content[]`, same tool block detection at `hooks/check-todos-from-transcript.py:65`.
    - Direct tool-use shape: `entry.type == "tool_use"`, tool name from `name` or `tool_name`, input from `input` or `tool_input` at `hooks/check-todos-from-transcript.py:78`.
  - For each supported `TodoWrite` block, it reads `input.todos` and, only when the list is truthy, replaces `latest_todos` at `hooks/check-todos-from-transcript.py:61`, `hooks/check-todos-from-transcript.py:74`, and `hooks/check-todos-from-transcript.py:83`.
  - “Latest” therefore means the last non-empty TodoWrite todos list encountered while scanning the JSONL file in file order.
  - After parsing, `main()` treats no found todos as success at `hooks/check-todos-from-transcript.py:114`.
  - For found todos, every todo whose `status` is not exactly `"completed"` is considered incomplete at `hooks/check-todos-from-transcript.py:120`.
  - Incomplete todos are rendered as `  - [<status>] <content>` at `hooks/check-todos-from-transcript.py:124`.
  - If any incomplete todo exists, the script prints the marker `INCOMPLETE_TODOS`, prints the joined list, and exits `1` at `hooks/check-todos-from-transcript.py:126`.
  - If all todos in the latest non-empty list have `status == "completed"`, it exits `0` at `hooks/check-todos-from-transcript.py:133`.

- inputs_outputs_state:
  - Primary input: stdin JSON object from Claude Code hook input. The only field this script consumes is `transcript_path`; example usage is documented at `hooks/check-todos-from-transcript.py:12`.
  - Secondary input: the transcript JSONL file named by `transcript_path`, decoded as UTF-8 at `hooks/check-todos-from-transcript.py:30`.
  - Output on success: no stdout/stderr by design, exit `0`.
  - Output on incomplete todos: stdout begins with `INCOMPLETE_TODOS`, followed by one line per incomplete todo, exit `1` at `hooks/check-todos-from-transcript.py:129`.
  - Output on hook-input JSON parse error: stderr `PARSE_ERROR: ...`, exit `2` at `hooks/check-todos-from-transcript.py:101`.
  - State read: transcript file only.
  - State written: none. No filesystem writes, no loop-state mutation, no todo mutation.
  - Parent state transition:
    - Exit `0` lets `hooks/loop-codex-stop-hook.sh` continue into later stop-hook checks and possible Codex review after `hooks/loop-codex-stop-hook.sh:394`.
    - Exit `1` makes the parent return a JSON block decision at `hooks/loop-codex-stop-hook.sh:384`, using the incomplete todo list derived from the helper output at `hooks/loop-codex-stop-hook.sh:374`.
    - Exit `2` makes the parent return a JSON block decision with a parse-error message at `hooks/loop-codex-stop-hook.sh:352`.

- gates_or_invariants:
  - The central invariant is strict completion: only `status == "completed"` passes. `pending`, `in_progress`, missing status, empty status, or any other value blocks at `hooks/check-todos-from-transcript.py:123`.
  - Only the latest non-empty `TodoWrite` list is authoritative. Older incomplete todo lists are ignored if a later non-empty list is all completed.
  - Empty or missing transcript evidence is fail-open, not fail-closed: empty stdin, missing `transcript_path`, nonexistent transcript file, empty transcript file, no supported `TodoWrite` events, and empty todos lists all exit `0`.
  - Malformed transcript JSONL lines are ignored, but malformed hook input JSON is fatal for this helper and becomes a parent stop-hook block.
  - `content` is not required. Missing content becomes an empty string in output at `hooks/check-todos-from-transcript.py:122`.
  - The script intentionally outputs incomplete-todo details on stdout only for the block case to avoid mixed stdout/stderr ordering issues, as noted at `hooks/check-todos-from-transcript.py:127`.
  - It does not validate todo schema beyond treating each todo as a mapping and reading `.get("status")` / `.get("content")`. If a `todos` list contains a non-dict item, that would raise an `AttributeError` because the loop assumes `todo.get(...)` at `hooks/check-todos-from-transcript.py:121`.

- dependencies_and_callers:
  - Python standard library only: `json`, `sys`, and `pathlib.Path` at `hooks/check-todos-from-transcript.py:15`.
  - Main caller: `hooks/loop-codex-stop-hook.sh`, via `python3 "$TODO_CHECKER"` at `hooks/loop-codex-stop-hook.sh:349`.
  - Hook registration path: `hooks/hooks.json` registers `hooks/loop-codex-stop-hook.sh` as a Claude Code `Stop` hook with timeout `7200` at `hooks/hooks.json:52`.
  - Parent block rendering dependency: `prompt-template/block/incomplete-todos.md`, which tells the agent to complete all todos and mark them completed with `TodoWrite` at `prompt-template/block/incomplete-todos.md:7`.
  - Sibling policy relationship: write/read/edit/bash validators block direct `round-*-todos.md` file use and route work through native `TodoWrite`; for example, `hooks/lib/loop-common.sh` has the user-facing “Use the native TodoWrite tool instead” policy referenced by search results around its todos-block message. This helper is the stop-side enforcement counterpart that reads the native tool transcript rather than a file.
  - Dedicated test caller: `tests/test-todo-checker.sh` invokes this file directly through `TODO_CHECKER="$PROJECT_ROOT/hooks/check-todos-from-transcript.py"` at `tests/test-todo-checker.sh:13`.
  - Integration test caller: `tests/test-finalize-phase.sh` creates a transcript with an `in_progress` todo and verifies the stop hook blocks before Codex invocation at `tests/test-finalize-phase.sh:715`.

- edge_cases_or_failure_modes:
  - Fail-open cases:
    - Empty hook input exits `0`.
    - Valid hook JSON without `transcript_path` exits `0`.
    - Nonexistent transcript path exits `0`.
    - Empty transcript exits `0`.
    - Transcript with no supported TodoWrite entries exits `0`.
    - TodoWrite entries with `todos: []` do not replace `latest_todos`, so they cannot clear a previous non-empty todo list.
  - Malformed transcript JSONL lines are skipped silently. This is resilient to noisy transcript files but can hide corruption if all useful lines are malformed.
  - Hook input parse errors exit `2`; the parent stop hook blocks with a parse-error reason rather than allowing a potentially unsafe stop.
  - Transcript file read errors other than nonexistent file are not caught. Permission errors, decoding errors, directories passed as transcript paths, or mid-read I/O failures would propagate as Python exceptions and likely produce a non-`0/1/2` exit. The parent only special-cases `1` and `2`, so an unexpected Python crash would fall through as if the todo check passed, because `TODO_EXIT` would be neither `1` nor `2`.
  - Non-dict todo list elements would crash on `todo.get(...)`, also falling into the unexpected-exit behavior above in the parent.
  - Status comparison is exact and case-sensitive. `"Completed"` or `"done"` blocks.
  - Because the parser only records truthy `todos`, a later TodoWrite call with an intentionally empty todo list is ignored and the previous non-empty list remains authoritative. Depending on Claude’s transcript semantics, that may be conservative or stale.
  - The helper is named for “Claude Code transcript” and hardcodes `TodoWrite`. It does not understand Codex-native planning state, execution-cron `[_]`/`[x]` checklist states, or scheduler todo snapshot files.

- validation_or_tests:
  - Dedicated unit-style shell tests are in `tests/test-todo-checker.sh`.
  - Covered input handling:
    - Invalid JSON exits `2` at `tests/test-todo-checker.sh:51`.
    - Empty input exits `0` at `tests/test-todo-checker.sh:63`.
    - Missing `transcript_path` exits `0` at `tests/test-todo-checker.sh:75`.
    - Nonexistent transcript exits `0` at `tests/test-todo-checker.sh:87`.
  - Covered todo semantics:
    - All completed exits `0` at `tests/test-todo-checker.sh:106`.
    - Pending exits `1` at `tests/test-todo-checker.sh:121`.
    - Output includes incomplete task details at `tests/test-todo-checker.sh:136`.
    - `in_progress` exits `1` at `tests/test-todo-checker.sh:144`.
    - Missing status is incomplete at `tests/test-todo-checker.sh:249`.
    - Empty content is still incomplete at `tests/test-todo-checker.sh:265`.
  - Covered transcript variants:
    - Empty transcript exits `0` at `tests/test-todo-checker.sh:166`.
    - Invalid JSONL lines are ignored at `tests/test-todo-checker.sh:179`.
    - Multiple TodoWrite calls use the latest at `tests/test-todo-checker.sh:196`.
    - Direct `tool_use` format is handled at `tests/test-todo-checker.sh:212`.
    - `type: message` format is handled at `tests/test-todo-checker.sh:227`.
  - Stop-hook integration coverage:
    - `tests/test-finalize-phase.sh:721` verifies incomplete todos make `loop-codex-stop-hook.sh` block.
    - `tests/test-finalize-phase.sh:735` verifies Codex is not invoked during the incomplete-todos short-circuit.
    - `tests/test-finalize-phase.sh:769` verifies a transcript with all completed todos allows the normal stop-hook review path to proceed.
  - I did not run the tests in this branch export because the environment is read-only/restricted and the test suite creates temporary files. I inspected the test sources directly instead.
  - A read-only provenance check using `git rev-parse` failed because this branch export is not a Git checkout with a `.git` directory visible in the restricted workspace, and the environment also blocked cache creation under `/tmp`. The source commit in this report is therefore taken from the scheduler metadata.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1/1 item evidence section present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`