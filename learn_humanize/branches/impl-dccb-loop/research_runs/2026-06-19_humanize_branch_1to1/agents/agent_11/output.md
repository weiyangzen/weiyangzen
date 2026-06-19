# agent_11 impl-dccb-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `0fabd14f224c998e6dedd7cddaf57c479524700c`

## Item Evidence

### IMPL_DCCB_LOOP-HZ-011 `file` `hooks/check-todos-from-transcript.py`
- cursor: `[_]`
- core_role:
  - `hooks/check-todos-from-transcript.py` is a Stop-hook helper used by both loop stop gates to prevent a loop iteration from ending while the agent still has unfinished TodoWrite items.
  - It is part of the RLCR/DCCB lifecycle hook surface rather than the main blueprint compiler or scheduler. Its core algorithmic role is a pre-review completion gate: cheaply inspect the current Claude transcript, find the newest TodoWrite payload, and report whether any todo status is not `completed`.
  - The helper is invoked by `hooks/loop-dccb-stop-hook.sh:66-73` and `hooks/loop-codex-stop-hook.sh:65-75` before the expensive Codex review sections of those hooks. If it exits with code `1`, the shell hook emits a blocking JSON decision and tells the agent to finish all todos before stopping.
- algorithmic_behavior:
  - Main entrypoint reads a JSON object from stdin as hook input in `main()` at `hooks/check-todos-from-transcript.py:87-93`.
  - It extracts `transcript_path` from the hook input at `hooks/check-todos-from-transcript.py:95-100`; missing or invalid hook input is treated as no todo evidence and exits successfully.
  - `find_latest_todos(transcript_path)` performs a linear scan over the transcript JSONL file at `hooks/check-todos-from-transcript.py:17-84`.
  - For each non-empty line, it attempts `json.loads`; malformed JSONL records are skipped, not fatal, at `hooks/check-todos-from-transcript.py:33-36`.
  - It recognizes three TodoWrite encodings:
    - Claude assistant message blocks: `type == "assistant"` with `message.content[]` tool blocks named `TodoWrite`, at `hooks/check-todos-from-transcript.py:48-60`.
    - Alternative message blocks: `type == "message"` with `content[]` tool blocks named `TodoWrite`, at `hooks/check-todos-from-transcript.py:62-73`.
    - Direct tool-use records: `type == "tool_use"` with `name` or `tool_name` equal to `TodoWrite`, at `hooks/check-todos-from-transcript.py:75-82`.
  - When multiple TodoWrite calls exist, `latest_todos` is overwritten as the scan progresses, so the final non-empty TodoWrite todo list wins. This is the central state transition in the helper: `latest_todos = todos` at `hooks/check-todos-from-transcript.py:59-60`, `72-73`, and `81-82`.
  - After parsing, `main()` treats an empty result as pass-through at `hooks/check-todos-from-transcript.py:105-107`.
  - It then scans the latest todo list, collecting every todo whose `status` field is not exactly `completed`, at `hooks/check-todos-from-transcript.py:109-115`.
  - If any incomplete todo exists, it prints a sentinel line `INCOMPLETE_TODOS`, prints one formatted line per incomplete todo, and exits `1` at `hooks/check-todos-from-transcript.py:117-122`.
  - If all todos in the latest list are completed, it exits `0` at `hooks/check-todos-from-transcript.py:124-125`.
- inputs_outputs_state:
  - Input: stdin JSON hook payload with `transcript_path`, documented in the usage example at `hooks/check-todos-from-transcript.py:9-10` and consumed at `hooks/check-todos-from-transcript.py:89-100`.
  - Input: transcript JSONL file. The helper expects one JSON object per line and tolerates unrelated lines and malformed JSON lines.
  - Input shape for todo state: TodoWrite tool input must contain a `todos` list. Each todo is expected to be a dict with at least `status` and optionally `content`, read at `hooks/check-todos-from-transcript.py:111-114`.
  - Output on pass: no stdout/stderr contract from this script, exit code `0`.
  - Output on block: stdout begins with `INCOMPLETE_TODOS`, followed by incomplete todo lines like `  - [status] content`, and exit code `1`, at `hooks/check-todos-from-transcript.py:117-122`.
  - Output consumed by callers: DCCB stop hook captures stdout/stderr into `TODO_RESULT`, checks exit code `1`, strips the sentinel with `tail -n +2`, then embeds the list into a block decision at `hooks/loop-dccb-stop-hook.sh:68-96`. RLCR does the same at `hooks/loop-codex-stop-hook.sh:67-98`.
  - Internal state is purely local and ephemeral: `latest_todos` in `find_latest_todos()` and `incomplete` in `main()`. No files are written, no repository state is mutated, and no persistent loop state is changed directly.
- gates_or_invariants:
  - Gate invariant: the latest non-empty TodoWrite todo list must have every todo status exactly equal to `completed`; any other string, missing status, or empty status blocks the stop path.
  - Empty/missing evidence is permissive: no transcript path, missing transcript file, invalid hook stdin, no TodoWrite calls, or TodoWrite calls with empty todo arrays all exit `0`. This avoids false blocking when the transcript is unavailable, but it means the helper is only a best-effort TodoWrite gate.
  - Latest-state invariant: only the most recent TodoWrite payload with a non-empty `todos` list is authoritative. Older incomplete todos are ignored if later TodoWrite state marks the remaining list complete.
  - Format invariant: the helper only recognizes tool name exactly `TodoWrite`. Other casing or wrapper names are ignored.
  - The caller-side Stop gate is active only when an RLCR/DCCB loop directory is detected. DCCB exits early when no `.humanize-dccb.local/<timestamp>/dccb-state.md` exists at `hooks/loop-dccb-stop-hook.sh:43-60`; RLCR exits early when no active RLCR loop is found at `hooks/loop-codex-stop-hook.sh:50-57`.
  - In `hooks/hooks.json:42-54`, both `loop-codex-stop-hook.sh` and `loop-dccb-stop-hook.sh` are registered under the `Stop` hook with long timeouts. This helper participates indirectly through those Stop hooks, not as a hook registered directly in `hooks.json`.
- dependencies_and_callers:
  - Runtime dependencies: Python 3 standard library only: `json`, `sys`, and `pathlib.Path`, imported at `hooks/check-todos-from-transcript.py:12-14`.
  - Direct callers:
    - `hooks/loop-dccb-stop-hook.sh:66-73` sets `TODO_CHECKER`, runs `python3 "$TODO_CHECKER"`, and uses exit code `1` to build a DCCB blocking response.
    - `hooks/loop-codex-stop-hook.sh:65-75` does the same for the RLCR stop hook.
  - Hook registration path: `hooks/hooks.json:42-54` registers both stop-hook shell scripts. `README.md:389-398` lists this helper as part of the hook lifecycle directory.
  - It depends on Claude Code transcript semantics, specifically assistant/message/direct tool-use JSONL variants. It does not depend on git, Codex, loop state files, or the DCCB/RLCR state machine directly.
  - It coordinates with the larger loop by returning a simple binary signal: pass or block. The shell hooks translate that into Claude hook JSON with `"decision": "block"` when incomplete todos are present.
- edge_cases_or_failure_modes:
  - Missing transcript file returns an empty todo list and passes at `hooks/check-todos-from-transcript.py:22-23`.
  - Invalid stdin JSON passes at `hooks/check-todos-from-transcript.py:89-93`.
  - Missing `transcript_path` passes at `hooks/check-todos-from-transcript.py:95-97`.
  - Malformed transcript lines are silently skipped at `hooks/check-todos-from-transcript.py:33-36`.
  - A transcript containing only empty TodoWrite arrays passes because the helper only updates `latest_todos` when `todos` is truthy at `hooks/check-todos-from-transcript.py:58-60`, `71-73`, and `80-82`.
  - If the newest TodoWrite call is malformed without `todos`, the prior non-empty TodoWrite remains authoritative. This is likely intentional for resilience, but it can preserve stale todo state.
  - If a todo item lacks `status`, `status` defaults to an empty string and blocks at `hooks/check-todos-from-transcript.py:111-115`.
  - If a todo item lacks `content`, the printed block line has empty content due to `content = todo.get("content", "")`.
  - If the transcript file exists but is unreadable, the script does not catch `OSError`; the Python process would fail non-deterministically from the caller’s perspective. The shell callers only special-case exit code `1`, so other failures do not take the incomplete-todo block path.
  - The helper does not validate allowed todo status vocabulary beyond requiring `completed` for pass. Any status such as `pending`, `in_progress`, custom values, or empty values is treated as incomplete.
  - The helper prints incomplete details to stdout rather than stderr at `hooks/check-todos-from-transcript.py:117-121`; the comment explains this avoids mixed buffering order.
- validation_or_tests:
  - No dedicated tests were found for `hooks/check-todos-from-transcript.py` in the inspected references.
  - The implementation is indirectly validated by the Stop-hook contract in `hooks/loop-dccb-stop-hook.sh:68-96` and `hooks/loop-codex-stop-hook.sh:67-98`, which expect exit code `1` and a sentinel-prefixed output when incomplete todos exist.
  - I did not run mutation or fixture-based tests because this branch export is read-only and the task explicitly requested research notes only. The code inspection covered the assigned file directly plus the two shell callers and hook registration.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `IMPL_DCCB_LOOP-HZ-011`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`