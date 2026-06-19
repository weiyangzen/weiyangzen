# agent_18 robust-edge-test-find-and-resolve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 3
- source_commit: `a3112ca4d149f56ced783e805b6dfcf029368dc4`

## Item Evidence

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-018 `file` `hooks/check-todos-from-transcript.py`
- cursor: `[_]`
- core_role:
  - Stop-hook helper that enforces the RLCR “finish active todo list before leaving the round” gate.
  - It reads Claude Code hook input from stdin, extracts `transcript_path`, scans the transcript JSONL, finds the most recent `TodoWrite` call, and reports whether every todo in that latest call has `status == "completed"`.
  - It is called by `hooks/loop-codex-stop-hook.sh:261-309` before expensive Codex review work. A failure blocks Stop with an “incomplete todos” reason rendered from `prompt-template/block/incomplete-todos.md`.

- algorithmic_behavior:
  - `find_latest_todos(transcript_path)` at `hooks/check-todos-from-transcript.py:20-87` is the main scan function.
  - It returns `[]` if the transcript path does not exist (`:25-26`), making missing/no transcript a permissive no-op.
  - It reads the transcript line by line as JSONL (`:30-39`), skips blank lines, and ignores malformed JSONL entries instead of failing the whole scan.
  - It recognizes three transcript shapes:
    - Claude Code assistant message blocks: `type == "assistant"` with `message.content[]` tool-use blocks (`:51-64`).
    - Alternative message blocks: `type == "message"` with top-level `content[]` (`:65-76`).
    - Direct tool-use entries: `type == "tool_use"` with `name` or `tool_name` (`:78-85`).
  - Each matching non-empty `TodoWrite.input.todos` replaces `latest_todos`; this deliberately implements “last TodoWrite wins” (`:62-63`, `:75-76`, `:84-85`).
  - `main()` at `:90-129` parses hook input, expands `~` in `transcript_path`, calls the scanner, and treats any todo whose status is not exactly `completed` as incomplete (`:113-119`).

- inputs_outputs_state:
  - Input: stdin JSON object, expected to include `transcript_path`; usage is documented at `hooks/check-todos-from-transcript.py:12-13`.
  - Secondary input: transcript JSONL file containing Claude/tool call entries.
  - Output/state transition:
    - Exit `0`: all todos complete, no todos found, no transcript path, or nonexistent transcript (`:7-8`, `:99-111`, `:128-129`).
    - Exit `1`: latest todo list contains any non-`completed` status; stdout begins with `INCOMPLETE_TODOS`, followed by formatted lines such as `- [pending] Task` (`:121-126`).
    - Exit `2`: hook input itself is invalid JSON; stderr prints `PARSE_ERROR: ...` (`:92-97`).
  - It does not mutate repository state. Its only “state” is the latest todo list found during transcript scan.

- gates_or_invariants:
  - The latest `TodoWrite` call is authoritative, not an aggregate over all historical todos. This prevents an old incomplete todo snapshot from blocking after a newer completed snapshot appears.
  - Only the exact string `completed` passes (`hooks/check-todos-from-transcript.py:116-119`); `pending`, `in_progress`, missing status, empty status, or any unknown status are incomplete.
  - Empty or missing todo data is permissive: `find_latest_todos()` only updates `latest_todos` when `todos` is truthy (`:62`, `:75`, `:84`), and `main()` exits `0` for no todos (`:109-111`).
  - Hook input JSON parse errors are fail-closed for the Stop hook: the checker exits `2`, and `loop-codex-stop-hook.sh` converts that into a blocking JSON decision (`hooks/loop-codex-stop-hook.sh:268-284`).
  - Transcript JSONL line parse errors are fail-open per line (`hooks/check-todos-from-transcript.py:36-39`), preserving robustness against noisy transcripts.

- dependencies_and_callers:
  - Runtime dependencies: Python standard library only, specifically `json`, `sys`, and `pathlib.Path` (`hooks/check-todos-from-transcript.py:15-17`).
  - Direct caller: `hooks/loop-codex-stop-hook.sh`, which sets `TODO_CHECKER="$SCRIPT_DIR/check-todos-from-transcript.py"` (`hooks/loop-codex-stop-hook.sh:261`) and feeds it the full hook input (`:263-266`).
  - Hook entrypoint context: `hooks/hooks.json:52-59` wires `loop-codex-stop-hook.sh` as the Stop hook with a 7200-second timeout.
  - Related prompt/template surface: incomplete todo block is rendered by `load_and_render_safe "$TEMPLATE_DIR" "block/incomplete-todos.md"` in `hooks/loop-codex-stop-hook.sh:292-298`.
  - Related policy surface: validators block file-based round todos and direct users toward native `TodoWrite`, e.g. `hooks/loop-read-validator.sh:48-59` and `hooks/lib/loop-common.sh:353`.

- edge_cases_or_failure_modes:
  - Nonexistent transcript path exits `0`; this avoids false blocks when the hook does not provide a usable transcript but can also fail open if transcript collection is broken.
  - Malformed hook input exits `2`; caller blocks with parse-error details.
  - Malformed lines inside a transcript are ignored, so a transcript with invalid noise plus a valid latest completed todo passes.
  - If the latest `TodoWrite` has an empty `todos` list, the previous non-empty todo snapshot remains authoritative because updates only happen when `todos` is truthy.
  - Missing `status` becomes `""` and blocks (`hooks/check-todos-from-transcript.py:116-119`).
  - Missing `content` becomes `""`, still blocks if status is incomplete, producing a low-information incomplete line.
  - It does not validate todo schema beyond `status` and `content`; unexpected extra fields such as `activeForm` are ignored.

- validation_or_tests:
  - Dedicated test file: `tests/test-todo-checker.sh`.
  - Tests cover invalid/empty hook JSON returning exit `2` (`tests/test-todo-checker.sh:51-73`), missing `transcript_path` and nonexistent transcript returning exit `0` (`:75-97`), all-completed todo lists passing (`:106-119`), incomplete and in-progress statuses failing (`:121-157`), invalid JSONL lines being ignored (`:179-194`), latest TodoWrite winning (`:196-210`), direct and alternative transcript formats (`:212-240`), missing status and empty content edge cases (`:249-278`), and unicode content (`:280-293`).
  - Finalize-phase tests also exercise TodoWrite transcript shapes around incomplete and completed cases at `tests/test-finalize-phase.sh:523` and `tests/test-finalize-phase.sh:577`.
  - I inspected tests but did not execute them, per “research notes only”.

- skip_candidate: `no`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-048 `file` `tests/test-template-references.sh`
- cursor: `[_]`
- core_role:
  - Executable specification for the RLCR template-reference integrity gate.
  - Its purpose is to prevent hook/validator block messages from going empty because a shell validator references a missing prompt template.
  - It verifies both existence of explicitly referenced templates and safe fallback usage in critical validators.

- algorithmic_behavior:
  - Initializes `SCRIPT_DIR`, `PROJECT_ROOT`, and `TEMPLATE_DIR="$PROJECT_ROOT/prompt-template"` at `tests/test-template-references.sh:14-16`.
  - Maintains counters for pass/fail/warning outcomes (`:25-27`) through helper functions `pass`, `fail`, `warn`, and `section` (`:29-49`).
  - Section 1 scans a fixed set of shell scripts that are expected to load templates (`:54-64`):
    - `hooks/loop-codex-stop-hook.sh`
    - `hooks/loop-read-validator.sh`
    - `hooks/loop-write-validator.sh`
    - `hooks/loop-edit-validator.sh`
    - `hooks/loop-bash-validator.sh`
    - `hooks/lib/loop-common.sh`
  - For each existing script, it reads non-comment lines and matches calls to `load_template`, `load_and_render`, or `load_and_render_safe` where the first argument is exactly `"$TEMPLATE_DIR"` (`:87-96`).
  - It extracts the second quoted argument as the template path using `sed` (`:96`), constructs `$TEMPLATE_DIR/$template_path`, and fails if that file does not exist (`:98-107`).
  - Section 2 enumerates every Markdown template under `prompt-template` (`:121-126`) and checks whether the template path is directly quoted anywhere under `hooks/` (`:134-141`). Unreferenced templates are warnings only, acknowledging dynamic or future use (`:130-140`).
  - Section 3 asserts a hardcoded common-template set exists (`:149-167`), covering shared message helpers in `hooks/lib/loop-common.sh`.
  - Section 4 enforces that critical validators use `load_and_render_safe` rather than unsafe `load_and_render` for template-rendered blocking messages (`:172-200`).
  - The script exits `0` only when `TESTS_FAILED == 0`; warnings do not fail the run (`:221-229`).

- inputs_outputs_state:
  - Inputs:
    - Repository layout rooted one directory above `tests/`.
    - Fixed script list at `tests/test-template-references.sh:57-64`.
    - Template tree under `prompt-template`.
    - Hardcoded common templates at `:152-159`.
    - Critical validator list at `:176-180`.
  - Outputs:
    - Human-readable colored PASS/FAIL/WARN lines.
    - Summary counts for passed, failed, and warnings (`:206-211`).
    - If missing references are found, prints a “CRITICAL: Missing template files” list (`:213-219`).
    - Exit `0` when all hard checks pass; exit `1` otherwise (`:221-229`).
  - It mutates no repo files; it only reads scripts and templates.

- gates_or_invariants:
  - Every direct template reference in the scanned shell scripts must resolve to an existing file (`tests/test-template-references.sh:93-107`).
  - Missing scripts in the fixed scan list are warnings, not failures (`:74-78`); this makes the check tolerant of optional scripts but weaker against deleted validators.
  - Not every template must be referenced; unreferenced templates only warn (`:130-140`).
  - The common-template set is mandatory regardless of whether direct scanning finds the references (`:152-167`).
  - Critical validators must use `load_and_render_safe`; any plain `load_and_render "$TEMPLATE_DIR"` in `loop-read-validator.sh`, `loop-write-validator.sh`, or `loop-edit-validator.sh` is a failure (`:176-200`).
  - The parser only recognizes one-line calls containing `"$TEMPLATE_DIR"` and a quoted template path after it. Multiline calls, variable template names, single quotes, or unquoted paths can evade Section 1.
  - Because the script uses `set -uo pipefail` but not `set -e` (`:12`), it can accumulate multiple failures and report a full summary instead of stopping on first failure.

- dependencies_and_callers:
  - Runtime dependencies: Bash, `find`, `grep`, `sed`, standard Unix test operators, and ANSI-capable terminal output.
  - It validates calls to functions defined in `hooks/lib/template-loader.sh`, particularly:
    - `load_template` returns file content or empty string with warning (`hooks/lib/template-loader.sh:36-48`).
    - `load_and_render` returns nothing when a template is missing (`:136-147`).
    - `load_and_render_safe` falls back when a template is missing or renders empty (`:170-203`).
  - Hook/template wiring depends on `hooks/lib/loop-common.sh`, which sets `TEMPLATE_DIR` and validates template directory shape (`hooks/lib/loop-common.sh:140-143`).
  - The hook entrypoints whose block messages this protects are registered in `hooks/hooks.json:14-59`.
  - Related broader test coverage exists in `tests/test-template-loader.sh` and `tests/test-templates-comprehensive.sh`, but this assigned script is the direct cross-reference gate.

- edge_cases_or_failure_modes:
  - Section 1 can miss template references split across lines or hidden behind variables/functions because it uses per-line regex matching.
  - It can also false-count lines in unusual syntax if `"$TEMPLATE_DIR"` and a quoted string appear in a matching line but not as intended function arguments.
  - It does not include `hooks/loop-plan-file-validator.sh` in `SCRIPTS_TO_CHECK` or `CRITICAL_SCRIPTS`, even though `rg` shows it uses `load_and_render_safe "$TEMPLATE_DIR" "block/schema-outdated.md"`; that means this script’s coverage is intentionally or accidentally narrower than the full hook set.
  - It treats missing scanned scripts as warnings, so a removed validator will not fail this test by itself.
  - It does not validate placeholder completeness for templates; it only checks file existence and safe rendering function usage. Placeholder rendering is covered elsewhere, e.g. `tests/test-template-loader.sh:147-164` and `tests/test-templates-comprehensive.sh:493-514`.
  - It uses `grep -rq "\"$template\"" "$PROJECT_ROOT/hooks/"`; template paths containing regex metacharacters could affect matching, though current paths are simple Markdown paths.

- validation_or_tests:
  - This file is itself an executable validation script.
  - It is likely included by the aggregate test runner under `tests/run-all-tests.sh` if that runner enumerates `tests/test-*.sh` files; I did not inspect that runner deeply because the assigned item’s behavior is self-contained.
  - Related validations:
    - `tests/test-template-loader.sh:147-164` checks real rendering of `block/wrong-round-number.md`.
    - `tests/test-templates-comprehensive.sh:493-514` checks real template rendering with all variables.
    - `tests/test-error-scenarios.sh` covers missing-template behavior and `load_and_render_safe` fallback behavior.
  - I inspected the script and related references but did not execute tests.

- skip_candidate: `no`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-078 `file` `prompt-template/block/wrong-round-file.md`
- cursor: `[_]`
- core_role:
  - Blocking-message template for the RLCR Read validator when an agent tries to read a prompt or summary file from a non-current round.
  - It is part of the “current round is authoritative” guard: agents should not consume stale prompt/summary context unless the file is allowlisted.
  - This template specifically serves read attempts. Write/Edit use the sibling `prompt-template/block/wrong-round-number.md`.

- algorithmic_behavior:
  - The template is static Markdown with variable placeholders:
    - `{{CLAUDE_ROUND}}`
    - `{{FILE_TYPE}}`
    - `{{CURRENT_ROUND}}`
    - `{{ACTIVE_LOOP_DIR}}`
    - `{{FILE_PATH}}`
  - Content starts with heading `# Wrong Round File` at `prompt-template/block/wrong-round-file.md:1`.
  - It names the attempted stale round file and current round at `:3`.
  - It lists the active current-round prompt and summary files at `:5-7`.
  - It ends with a direct command hint for the requested file path at `:9`.
  - Rendering is performed through `load_and_render_safe`, so if this template is missing or empty the read validator still has a fallback message.

- inputs_outputs_state:
  - Inputs are supplied by `hooks/loop-read-validator.sh` when a read target is a round prompt/summary with a mismatched round:
    - `CLAUDE_ROUND` extracted from basename via `extract_round_number` (`hooks/loop-read-validator.sh:102`).
    - `FILE_TYPE` computed as `summary` or `prompt` from the path (`:107-113`).
    - `CURRENT_ROUND` parsed from `state.md` or `finalize-state.md` (`:85-96`).
    - `ACTIVE_LOOP_DIR` from active loop discovery (`:77-80`).
    - `FILE_PATH` from hook input (`:45`).
  - Output is rendered Markdown written to stderr by the read validator (`hooks/loop-read-validator.sh:141-146`), followed by exit `2` (`:147`), which blocks the Read tool.
  - It does not modify RLCR files or state; it communicates the state transition “Read request denied because target round != current round.”

- gates_or_invariants:
  - The guard condition is in `hooks/loop-read-validator.sh:135`: `CLAUDE_ROUND != CURRENT_ROUND` and the target is not allowlisted.
  - This branch only runs after:
    - Hook input JSON is valid (`hooks/loop-read-validator.sh:24-31`).
    - Tool is `Read` (`:34-38`).
    - `file_path` exists (`:40-45`).
    - Target is a round `summary` or `prompt` file (`:66-68`).
    - An active loop exists (`:77-83`).
    - State parsing succeeds strictly (`:91-95`).
    - Round number can be extracted (`:102-105`).
  - The template is a message-only gate component; enforcement is in the shell validator, not in the Markdown file.
  - Allowlisted files bypass this block even if their round number differs (`hooks/loop-read-validator.sh:135`), matching the RLCR exception policy for allowed todo/summary paths.

- dependencies_and_callers:
  - Direct caller: `hooks/loop-read-validator.sh:141-146`.
  - Hook registration: `hooks/hooks.json:33-39` wires `loop-read-validator.sh` for `PreToolUse` Read events.
  - Template loader: `hooks/lib/template-loader.sh` implements placeholder rendering and fallback behavior. The single-pass renderer preserves missing placeholders and prevents recursive substitution (`hooks/lib/template-loader.sh:50-132`); `load_and_render_safe` provides fallback behavior (`:170-203`).
  - Existence of this template is validated by `tests/test-template-references.sh` Section 1 because `loop-read-validator.sh` directly references `block/wrong-round-file.md` (`tests/test-template-references.sh:83-107`).
  - Neighboring templates cover related branches:
    - `prompt-template/block/wrong-file-location.md` for round files outside the active loop directory.
    - `prompt-template/block/wrong-directory-path.md` for correct basename in wrong loop directory.
    - `prompt-template/block/wrong-round-number.md` for write/edit wrong-round summary operations.

- edge_cases_or_failure_modes:
  - If the template is deleted or empty, `load_and_render_safe` uses the fallback text embedded in `hooks/loop-read-validator.sh:136-140`; blocking still occurs, but the richer “Current round files” guidance is lost.
  - If any variable is missing from the render call, `render_template` leaves the placeholder intact rather than failing (`hooks/lib/template-loader.sh:120-121`), so the block still prints but may contain raw `{{...}}`.
  - The final instruction says `cat {{FILE_PATH}}`, which points at the attempted file, while the body lists current-round files. That is useful when the block is advisory, but it can be confusing because the attempted stale read is the thing being blocked; the fallback says “Read from: active loop” instead.
  - The template handles both `prompt` and `summary` values through `{{FILE_TYPE}}`; it is not used for todos, because todos are blocked earlier with the native TodoWrite policy (`hooks/loop-read-validator.sh:48-59`).
  - If state parsing fails, this template is not rendered; the validator exits with a generic malformed-state error (`hooks/loop-read-validator.sh:91-95`).

- validation_or_tests:
  - Direct reference existence is covered by `tests/test-template-references.sh:93-107` through the `loop-read-validator.sh` call.
  - Safe renderer usage for the read validator is covered by `tests/test-template-references.sh:176-200`, which fails if critical validators use unsafe `load_and_render`.
  - Template rendering mechanics are covered by loader tests, though they focus on sibling `wrong-round-number.md`: `tests/test-template-loader.sh:147-164` and `tests/test-templates-comprehensive.sh:493-514`.
  - I inspected the template and caller; no tests were run.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `3 unique item evidence headings, one per assigned row`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`