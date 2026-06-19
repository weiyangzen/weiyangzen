# agent_10 do-not-wish-coding 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `ac6cd9c180bcb9b84f6083fba1e458b4aab9ae14`

## Item Evidence

### DO_NOT_WISH_CODING-HZ-010 `directory` `templates`
- cursor: `[_]`
- core_role: Provides seed templates for RLCR runtime knowledge artifacts. The directory currently contains only `templates/bitlesson.md`, a strict Markdown schema for `.humanize/bitlesson.md`.
- algorithmic_behavior: `templates/bitlesson.md:5-19` defines the required BitLesson entry field order: lesson id, scope, problem, root cause, solution, constraints, validation evidence, and source rounds. `templates/bitlesson.md:21-23` reserves the append-only entries section. The setup path wires this template into runtime by setting `PLUGIN_BITLESSON_TEMPLATE="$SCRIPT_DIR/../templates/bitlesson.md"` and invoking `bitlesson-init.sh` in `scripts/setup-rlcr-loop.sh:822-828`.
- inputs_outputs_state: Input is the static template file. Output is a project-local `.humanize/bitlesson.md` copied from that template when missing; `scripts/bitlesson-init.sh:8-14` documents the behavior and `scripts/bitlesson-init.sh:84-85` creates the parent directory and copies the template. State created from this template is later referenced by loop state fields `bitlesson_file` and `bitlesson_required` in `scripts/setup-rlcr-loop.sh:858-862`.
- gates_or_invariants: The strict field order in `templates/bitlesson.md:7-19` is the invariant. Runtime initialization rejects missing template paths via `scripts/bitlesson-init.sh:55-66`, rejects unsafe relative paths via `scripts/bitlesson-init.sh:71`, and refuses non-regular existing BitLesson paths via `scripts/bitlesson-init.sh:79`.
- dependencies_and_callers: Called by `scripts/setup-rlcr-loop.sh`; validated during stop-hook rounds by `hooks/loop-codex-stop-hook.sh:720-734`, which delegates BitLesson delta enforcement to `scripts/bitlesson-validate-delta.sh`.
- edge_cases_or_failure_modes: Missing template or non-file BitLesson destination blocks initialization. Existing `.humanize/bitlesson.md` causes setup to infer `BITLESSON_REQUIRED=true` when state does not explicitly say otherwise, at `hooks/loop-codex-stop-hook.sh:137-140`.
- validation_or_tests: No direct test file for `templates/bitlesson.md` in the assigned set, but the stop hook’s BitLesson delta gate is executable behavior at `hooks/loop-codex-stop-hook.sh:716-735`, and the setup script proves the template is part of loop bootstrapping.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-040 `file` `hooks/loop-codex-stop-hook.sh`
- cursor: `[_]`
- core_role: Main RLCR stop-hook state machine. It intercepts Claude stop attempts, validates loop invariants, blocks unsafe exits with JSON hook decisions, asks Codex to review implementation progress, moves the loop into review/finalize phases, or terminates on completion, STOP, max-iteration, or corrupted state.
- algorithmic_behavior: The hook reads JSON stdin at `hooks/loop-codex-stop-hook.sh:28`, extracts `session_id`, finds the active loop via `find_active_loop`, and exits early if no matching loop exists at `hooks/loop-codex-stop-hook.sh:58-65`. It resolves either `state.md` or `finalize-state.md` at `hooks/loop-codex-stop-hook.sh:74-81`. It parses frontmatter, preserving raw-field checks so missing `current_round` and `max_iterations` cannot be silently defaulted, at `hooks/loop-codex-stop-hook.sh:87-103` and `hooks/loop-codex-stop-hook.sh:165-178`.
- inputs_outputs_state: Inputs are hook JSON, `.humanize/rlcr/<timestamp>/state.md` or `finalize-state.md`, round summaries, git state, plan backup, goal tracker, BitLesson file, Codex CLI, templates, and cached review artifacts. Outputs are hook JSON with `decision: block` for incomplete/unsafe states, new prompt/summary/review files under the loop directory, debug logs under `$XDG_CACHE_HOME/humanize/...`, state-file renames, and final exit 0 for hook compatibility.
- gates_or_invariants: Enforces valid Codex model/effort at `hooks/loop-codex-stop-hook.sh:151-163`; required schema fields at `hooks/loop-codex-stop-hook.sh:197-242`; branch consistency at `hooks/loop-codex-stop-hook.sh:257-288`; plan integrity unless already in review phase at `hooks/loop-codex-stop-hook.sh:290-371`; no incomplete Task/Todo work before review at `hooks/loop-codex-stop-hook.sh:373-429`; fail-closed git status at `hooks/loop-codex-stop-hook.sh:464-488`; large changed-file line limit at `hooks/loop-codex-stop-hook.sh:490-576`; clean worktree and optional push-every-round at `hooks/loop-codex-stop-hook.sh:578-676`; summary-file existence at `hooks/loop-codex-stop-hook.sh:678-714`; BitLesson delta at `hooks/loop-codex-stop-hook.sh:716-735`; initialized goal tracker in round 0 at `hooks/loop-codex-stop-hook.sh:737-813`; max-iteration limit at `hooks/loop-codex-stop-hook.sh:815-828`.
- dependencies_and_callers: Depends on `hooks/lib/loop-common.sh` for markers, state parsing, active-loop discovery, issue detection, templates, and loop ending; `scripts/portable-timeout.sh` for bounded git/Codex commands; `check-todos-from-transcript.py`; `scripts/bitlesson-validate-delta.sh`; `jq`, `git`, `codex`, `python3`, `awk`, `sed`; and prompt templates under `prompt-template`. It is invoked as a Claude stop hook.
- edge_cases_or_failure_modes: Corrupt or truncated state ends loop or blocks. Git timeout blocks and calls `cleanup_stale_index_lock` at `hooks/loop-codex-stop-hook.sh:440-455`. Missing Codex blocks at `hooks/loop-codex-stop-hook.sh:947-967`. Codex nonzero, missing review file, or empty review file all block with debug paths at `hooks/loop-codex-stop-hook.sh:1428-1528`. Review phase manual-toggle attacks are blocked by requiring `.review-phase-started` at `hooks/loop-codex-stop-hook.sh:1592-1608`. `STOP` terminates differently for full-alignment versus unexpected non-alignment rounds at `hooks/loop-codex-stop-hook.sh:1617-1644`.
- validation_or_tests: `tests/test-session-id.sh` covers session-aware active-loop filtering used at `hooks/loop-codex-stop-hook.sh:58-65`. `tests/robustness/test-plan-file-robustness.sh` covers setup-side plan validation that this hook later protects by backup diff and git status. The hook itself also writes audit prompts and command logs for Codex review at `hooks/loop-codex-stop-hook.sh:1023-1072` and `hooks/loop-codex-stop-hook.sh:1395-1422`.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-070 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role: Executable specification for RLCR validator allowlists around loop-owned round todos and summaries. It verifies that the hook validators block direct file access except a tiny compatibility allowlist.
- algorithmic_behavior: Builds a temporary git repo and active loop state in `setup_test_loop` at `tests/test-allowlist-validators.sh:33-64`. It first tests `is_allowlisted_file` directly, then feeds synthetic Claude hook JSON into `loop-write-validator.sh`, `loop-edit-validator.sh`, `loop-read-validator.sh`, and `loop-bash-validator.sh`.
- inputs_outputs_state: Inputs are generated hook JSON containing `tool_name`, `file_path`, or shell `command`; an active loop directory; and `CLAUDE_PROJECT_DIR`. Outputs are pass/fail counters and process exit code equal to `$TESTS_FAILED` at `tests/test-allowlist-validators.sh:385-393`. Validator success is expected as exit 0; blocked access is expected as exit 2.
- gates_or_invariants: The direct allowlist is exactly `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` in the active loop directory, proven at `tests/test-allowlist-validators.sh:72-126` and implemented in `hooks/lib/loop-common.sh:585-606`. Wrong round, wrong directory, generic relative todos paths, old loop directories, and same-basename different-root paths must be blocked.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at `tests/test-allowlist-validators.sh:17` and executes the read/write/edit/bash validators at `tests/test-allowlist-validators.sh:139`, `tests/test-allowlist-validators.sh:195`, `tests/test-allowlist-validators.sh:238`, and `tests/test-allowlist-validators.sh:294`.
- edge_cases_or_failure_modes: Security-focused cases include wrong directory at `tests/test-allowlist-validators.sh:120-126`, generic `round-1-todos.md` without full path at `tests/test-allowlist-validators.sh:342-353`, old loop directory at `tests/test-allowlist-validators.sh:355-368`, and same basename under `/tmp` at `tests/test-allowlist-validators.sh:370-383`. These prevent bypassing validators by path shape alone.
- validation_or_tests: This file is itself validation. It covers 25 scenarios across helper, Write, Edit, Read, and Bash validators.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-100 `file` `tests/test-session-id.sh`
- cursor: `[_]`
- core_role: Executable specification for session-scoped RLCR loops. It prevents hooks for one Claude session from hijacking another session’s loop, and prevents stale loop revival.
- algorithmic_behavior: The test bootstraps loop state via `scripts/setup-rlcr-loop.sh`, verifies `session_id:` is created empty in `state.md`, then verifies `hooks/loop-post-bash-hook.sh` records the real Claude `session_id` from PostToolUse JSON only after a valid setup command. It also exercises `find_active_loop` for active, finalize, terminal, empty-session, and multi-session directory sets.
- inputs_outputs_state: Inputs are temporary git repos, generated state files, `.humanize/.pending-session-id` signal files, synthetic hook JSON containing `session_id`, and mock setup command paths. Outputs are state mutations from empty `session_id:` to concrete values, removal or preservation of the pending signal, and pass/fail summary via `print_test_summary`.
- gates_or_invariants: Setup must include `session_id:` at `tests/test-session-id.sh:54-66`, initially empty at `tests/test-session-id.sh:68-81`, and a `.pending-session-id` signal at `tests/test-session-id.sh:83-107`. PostToolUse must only consume the signal for boundary-valid setup invocations, covered at `tests/test-session-id.sh:464-528` and `tests/test-session-id.sh:825-1008`. Active-loop lookup must return the newest matching active loop but return empty if that session’s newest loop is terminal, covered at `tests/test-session-id.sh:633-784`.
- dependencies_and_callers: Sources `tests/test-helpers.sh` and `hooks/lib/loop-common.sh` at `tests/test-session-id.sh:15-20`; calls `scripts/setup-rlcr-loop.sh`, `hooks/loop-post-bash-hook.sh`, and `scripts/cancel-rlcr-loop.sh`. The production behavior is implemented by `extract_session_id` and `find_active_loop` in `hooks/lib/loop-common.sh:204-327`, and by command-boundary matching in `hooks/loop-post-bash-hook.sh:56-91`.
- edge_cases_or_failure_modes: Covers non-matching sessions, empty stored session IDs for backward compatibility, finalize-state matching, cancel-state and complete-state terminal blocking, special characters in recorded session IDs, false positives such as `echo /path/setup-rlcr-loop.sh`, quoted-prefix concatenation, and tab-delimited commands. Session IDs with spaces are not represented; the production finder strips spaces from stored IDs at `hooks/lib/loop-common.sh:309`.
- validation_or_tests: This file is the validation suite, ending with `print_test_summary "Session ID Feature Tests"` at `tests/test-session-id.sh:1055-1059`.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-130 `file` `prompt-template/block/incomplete-todos.md`
- cursor: `[_]`
- core_role: Stop-hook blocking prompt template for unfinished Task/Todo work. It is a gate message, not executable logic.
- algorithmic_behavior: Contains the rendered placeholder `{{INCOMPLETE_LIST}}` at `prompt-template/block/incomplete-todos.md:5`, followed by required actions at `prompt-template/block/incomplete-todos.md:7-10`: complete remaining tasks, mark each completed via `TaskUpdate`, and only then summarize/stop.
- inputs_outputs_state: Input is the incomplete task list produced by `hooks/check-todos-from-transcript.py`; output is a Markdown reason string embedded in hook JSON. The stop hook loads it with `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:411-417` when the task checker exits 1.
- gates_or_invariants: The invariant is that Codex review must not start while any task remains incomplete. The last line explicitly blocks proceeding to Codex review until all tasks are finished at `prompt-template/block/incomplete-todos.md:12`.
- dependencies_and_callers: Called only by the stop hook’s incomplete-task gate at `hooks/loop-codex-stop-hook.sh:373-429`.
- edge_cases_or_failure_modes: If the template is missing or render fails, the hook has a fallback message at `hooks/loop-codex-stop-hook.sh:411-415`. If the task checker itself has a parse error, the hook uses a separate parse-error block at `hooks/loop-codex-stop-hook.sh:387-404`.
- validation_or_tests: No direct test in assigned files for this exact template. Its behavior is indirectly tied to the stop hook’s task-checker branch.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-160 `file` `prompt-template/claude/push-every-round-note.md`
- cursor: `[_]`
- core_role: Small prompt fragment that reinforces the push-every-round state invariant after the stop hook creates the next-round prompt.
- algorithmic_behavior: The template text at `prompt-template/claude/push-every-round-note.md:2` says that when `--push-every-round` is enabled, commits must be pushed after each round. The stop hook appends it only when `PUSH_EVERY_ROUND == true` at `hooks/loop-codex-stop-hook.sh:1777-1784`.
- inputs_outputs_state: Input is the parsed `push_every_round` state field from `state.md`, mapped at `hooks/loop-codex-stop-hook.sh:113`. Output is an appended Markdown note in `round-N-prompt.md`.
- gates_or_invariants: Complements the hard git gate that blocks exit for unpushed commits when `PUSH_EVERY_ROUND` is true at `hooks/loop-codex-stop-hook.sh:645-675`. The template is advisory prompt text; the actual gate is git status ahead detection.
- dependencies_and_callers: Loaded through `load_template "$TEMPLATE_DIR" "claude/push-every-round-note.md"` in the stop hook. If missing, fallback text is used at `hooks/loop-codex-stop-hook.sh:1780-1782`.
- edge_cases_or_failure_modes: Missing template degrades to fallback, so loop behavior remains intact. If no upstream/ahead marker is available from `git status -sb`, the hard gate may not detect unpushed commits even though the prompt note is appended.
- validation_or_tests: No direct test in assigned files for this template; the push gate logic is visible in the stop hook.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-190 `file` `tests/robustness/test-plan-file-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for setup-time plan-file validation, which is an upstream invariant for RLCR loop correctness and later stop-hook plan integrity checks.
- algorithmic_behavior: Runs `scripts/setup-rlcr-loop.sh` against generated plan files through `test_plan_validation` at `tests/robustness/test-plan-file-robustness.sh:46-106`. It uses a mock `codex` at `tests/robustness/test-plan-file-robustness.sh:26-40` so the test isolates plan validation from real Codex availability.
- inputs_outputs_state: Inputs are synthetic plan files in a temporary git repo, with `.gitignore` configured to keep plan artifacts untracked and ignored at `tests/robustness/test-plan-file-robustness.sh:112-123`. Outputs are pass/fail messages and final exit from `print_test_summary` at `tests/robustness/test-plan-file-robustness.sh:553-558`.
- gates_or_invariants: Production validation must reject unsafe paths, symlinks, missing files, unreadable files, files outside the project, submodule paths, tracking-status violations, too few total lines, and fewer than 3 meaningful content lines. The production checks are in `scripts/setup-rlcr-loop.sh:421-573` and `scripts/setup-rlcr-loop.sh:581-637`. The test’s helper mirrors content-line counting rules: blank lines, `#` comment lines, and HTML comments do not count, at `tests/robustness/test-plan-file-robustness.sh:129-169`.
- dependencies_and_callers: Depends on `scripts/setup-rlcr-loop.sh`, `tests/test-helpers.sh`, `git`, `wc`, and shell file-generation primitives. The stop hook later relies on the resulting backed-up plan and state metadata for integrity enforcement at `hooks/loop-codex-stop-hook.sh:290-371`.
- edge_cases_or_failure_modes: Covers empty and comments-only files at `tests/robustness/test-plan-file-robustness.sh:300-323`, 1MB+ files and prior SIGPIPE exposure at `tests/robustness/test-plan-file-robustness.sh:325-353`, mixed CRLF/LF at `tests/robustness/test-plan-file-robustness.sh:355-366`, binary/null bytes at `tests/robustness/test-plan-file-robustness.sh:368-388` and `tests/robustness/test-plan-file-robustness.sh:514-525`, very long lines at `tests/robustness/test-plan-file-robustness.sh:390-407`, whitespace-only files at `tests/robustness/test-plan-file-robustness.sh:432-442`, symlinks/directories/unreadable files at `tests/robustness/test-plan-file-robustness.sh:477-512`, and deleted files at `tests/robustness/test-plan-file-robustness.sh:527-551`.
- validation_or_tests: This file is itself validation. Some edge cases only test local shell handling rather than invoking production validation, such as binary content line counting and symlink detection; production-invoked cases are explicit where `test_plan_validation` is called.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 7 item evidence sections present, matching the 7 assigned rows
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`