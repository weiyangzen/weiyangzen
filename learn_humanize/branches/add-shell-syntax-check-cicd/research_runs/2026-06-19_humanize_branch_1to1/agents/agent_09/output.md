# agent_09 add-shell-syntax-check-cicd 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `6e0eebdb803522cd4be735589be4d1d76e8e536e`

## Item Evidence

### ADD_SHELL_SYNTAX_CHECK_CICD-HZ-009 `file` `hooks/check-todos-from-transcript.py`
- cursor: `[_]`
- core_role:
  - [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:1) is a Stop-hook helper for the RLCR loop. Its role is to inspect the current Claude Code transcript and block loop exit when the latest native `TodoWrite` state still contains unfinished todos.
  - It is part of the stop-gate path, not the Codex review itself. [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/loop-codex-stop-hook.sh:59) runs this checker before large-file, git-clean, and Codex-review gates, specifically as a cheap early failure if work is still pending.
  - It supports the repository’s RLCR invariant that todo tracking should happen through native Claude `TodoWrite`, not manually written `round-*-todos.md` files. The sibling shared hook text explicitly blocks file-based todo access and says to use the native tool instead at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/lib/loop-common.sh:75).

- algorithmic_behavior:
  - The main parser is `find_latest_todos(transcript_path: Path) -> list` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:17). It streams a JSONL transcript line by line, skips blank lines, ignores malformed JSON records, and updates `latest_todos` whenever it finds a `TodoWrite` tool call with a non-empty `todos` array.
  - It recognizes three transcript shapes:
  - Claude Code assistant message format: `entry["type"] == "assistant"`, then `message.content[]`, then blocks with `type == "tool_use"` and `name == "TodoWrite"` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:48).
  - Alternative message format: `entry["type"] == "message"`, then top-level `content[]`, then `TodoWrite` tool blocks at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:62).
  - Direct tool entry format: `entry["type"] == "tool_use"` with `name` or `tool_name` equal to `TodoWrite`, using `input` or `tool_input` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:75).
  - The state transition model is “latest non-empty TodoWrite wins”: every matching non-empty `todos` payload replaces the prior `latest_todos`; older TodoWrite state is discarded. The returned list is therefore the most recent observed todo state, not a merge of all todos.
  - `main()` reads hook JSON from stdin, extracts `transcript_path`, expands `~`, parses latest todos, and exits according to completion status at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:87).
  - Completion is strict string equality: each todo must have `status == "completed"` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:111). Any other status, including `pending`, `in_progress`, missing, empty, or unknown, is treated as incomplete.

- inputs_outputs_state:
  - Input: stdin must be a JSON object with `transcript_path`, as documented in the script usage at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:9).
  - Input: `transcript_path` points to a Claude Code JSONL transcript. The script reads it as UTF-8 text at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:27).
  - Output on pass: exit code `0` with no required stdout when stdin is invalid JSON, `transcript_path` is missing, the transcript file does not exist, no TodoWrite payload is found, latest TodoWrite payload is empty, or all latest todos have `status == "completed"`.
  - Output on failure: exit code `1`, stdout begins with `INCOMPLETE_TODOS`, followed by one line per incomplete todo in the form `  - [<status>] <content>` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:117).
  - Persistent state: none. The only in-memory state is `latest_todos`, plus an `incomplete` list built from the final todo snapshot.
  - Caller consumption: [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/loop-codex-stop-hook.sh:67) captures stdout/stderr together, checks for exit code `1`, strips the first marker line with `tail -n +2`, and embeds the remaining todo list in a JSON Stop-hook block response.

- gates_or_invariants:
  - Fail-closed for known unfinished todos: if any latest todo status is not exactly `completed`, the checker exits `1` and the Stop hook blocks exit before Codex review.
  - Fail-open for missing or unusable hook context: invalid stdin JSON exits `0` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:89); missing `transcript_path` exits `0` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:95); nonexistent transcript returns no todos at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:22); no todos exits `0` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:105).
  - Malformed JSONL transcript records are ignored, not fatal, at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:33). This makes the checker tolerant of noisy transcript data but can mask corruption.
  - Empty `todos` payloads do not clear prior todo state. Because the code only assigns `latest_todos = todos` when `todos` is truthy, a later `TodoWrite` call with an empty array is ignored rather than treated as “no todos remain” at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:58).
  - The Stop hook treats this as a pre-review guard. When incomplete todos are found, it returns a Claude hook response with `"decision": "block"` and tells the agent to complete and mark all todos before attempting to stop at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/loop-codex-stop-hook.sh:77).
  - Hook registration is via the repository hook manifest: [hooks/hooks.json](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/hooks.json:42) registers `loop-codex-stop-hook.sh` for `Stop`, which is the indirect runtime entry for this Python checker.

- dependencies_and_callers:
  - Runtime dependencies are only Python standard library modules: `json`, `sys`, and `pathlib.Path` at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:12).
  - Direct caller: [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/loop-codex-stop-hook.sh:65) resolves `TODO_CHECKER="$SCRIPT_DIR/check-todos-from-transcript.py"` and executes it with `python3`, feeding the original hook input JSON.
  - Indirect caller: Claude Code Stop-hook infrastructure invokes [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/loop-codex-stop-hook.sh:1), as configured in [hooks/hooks.json](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/hooks.json:42).
  - Coordination with sibling validators: `loop-read-validator.sh`, `loop-write-validator.sh`, `loop-edit-validator.sh`, and `loop-bash-validator.sh` all use shared round-file blocking conventions from [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/lib/loop-common.sh:54). That matters because this Python script depends on transcript-native TodoWrite state, while sibling validators discourage external markdown todo files.
  - Documentation reference: README lists the script as a lifecycle hook component at [README.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/README.md:223).

- edge_cases_or_failure_modes:
  - If stdin is not valid JSON, the checker silently allows stop continuation. This is intentionally permissive but weakens enforcement if the hook input shape changes or is truncated.
  - If the transcript path is missing, unreadable due to permissions, nonexistent, or not present in hook input, the checker allows continuation. The nonexistent-file case is handled; permission/read errors are not caught and would likely surface as a Python exception unless the caller absorbs the non-`1` exit as non-blocking.
  - If a transcript line is malformed JSON, the line is skipped. If the only latest TodoWrite state is in a malformed line, stale earlier state or no state may be used.
  - A later empty `TodoWrite` array does not clear previous todos. If Claude Code legitimately writes `todos: []` to indicate no remaining todos, this script would retain the previous non-empty todo list and could falsely block exit.
  - The checker does not validate todo item schema. Non-dict entries would fail at `todo.get(...)` because the loop assumes each todo is dict-like at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:111).
  - Completion vocabulary is hard-coded to `completed`. If Claude Code changes status names or casing, the gate will treat all changed statuses as incomplete.
  - The script’s module docstring says failure details go to stderr, but implementation prints the marker and todo list to stdout at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/check-todos-from-transcript.py:117). The caller is compatible because it captures `2>&1`, but the docstring is stale.
  - The Stop hook initializes `TODO_EXIT` through `TODO_RESULT=$(...) || TODO_EXIT=$?`, then defaults unset to zero at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-shell-syntax-check-cicd/hooks/loop-codex-stop-hook.sh:69). It only blocks on exit code `1`; unexpected script errors with another exit code do not trigger the incomplete-todos block and fall through to later gates.

- validation_or_tests:
  - I found no dedicated test or spec files for this repository in a shallow test/spec file search, and no direct test reference for `check-todos-from-transcript.py`.
  - Existing validation is integration-style by hook wiring: `hooks/hooks.json` registers the Stop hook; the Stop hook invokes this checker; the checker’s exit code controls whether the Stop hook emits a blocking JSON decision before Codex review.
  - A focused validation set for this file would cover: assistant-format TodoWrite with pending status exits `1`; all `completed` exits `0`; direct `tool_use` format works; malformed JSONL lines are skipped; nonexistent transcript exits `0`; later TodoWrite replaces earlier TodoWrite; and empty later TodoWrite behavior is either confirmed as intended or fixed if undesired.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1/1 evidence section present`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`