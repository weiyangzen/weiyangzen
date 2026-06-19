# agent_11 reflection-improve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `13a47fb2260667a272b448e8d3c1a521f2382590`

## Item Evidence

### REFLECTION_IMPROVE-HZ-011 `directory` `tests`
- cursor: `[_]`
- core_role: The `tests` directory is the repository’s executable contract suite for Humanize/RLCR/PR-loop behavior. It contains 74 files across 4 directories: top-level shell specs, `tests/robustness` adversarial specs, `tests/fixtures` GitHub API JSON fixtures, and `tests/mocks/gh` for mocked GitHub CLI behavior.
- algorithmic_behavior: `tests/run-all-tests.sh` is the coordinating harness: it enumerates suites at lines 60-120, runs them in parallel with `HUMANIZE_TEST_JOBS` throttling at lines 19-37 and 168-220, supplies a fallback mock `codex` at lines 131-142, strips ANSI before pass/fail aggregation at lines 247-250, then exits nonzero if any suite failed at lines 287-304. This makes the directory a regression oracle rather than production runtime code.
- inputs_outputs_state: Inputs are shell environment variables, temporary git repos, hook JSON payloads, mock `codex`/`gh` binaries, and fixture JSON. Outputs are pass/fail counters and exit status. Shared helpers in `tests/test-helpers.sh` define `pass`, `fail`, `skip`, `print_test_summary`, `setup_test_dir`, and `init_test_git_repo` at lines 30-105.
- gates_or_invariants: The suite gates JSON hook validation, RLCR state parsing, active-loop detection, branch and plan invariants, prompt/template existence, Codex review markers, task completion gates, monitor cleanup, PR-loop API polling, and path/symlink security. It explicitly treats BSD/GNU portability as an invariant, for example `test-ansi-parsing.sh` verifies BSD-compatible ANSI stripping.
- dependencies_and_callers: Most suites source production code directly: `hooks/lib/loop-common.sh`, `hooks/lib/template-loader.sh`, `scripts/humanize.sh`, `scripts/portable-timeout.sh`, setup scripts, stop hooks, and PR-loop scripts. `tests/mocks/gh` simulates `gh pr view`, `gh api`, comments, reactions, reviews, repo metadata, and auth status using fixture/env-driven responses.
- edge_cases_or_failure_modes: Covered edge classes include malformed/deep JSON, null bytes, path traversal, symlinks, missing or corrupted `state.md`, concurrent hook reads, deleted monitor directories, zsh glob failures, git detached/rebase/merge states, timeout fallback behavior, PR closed/merged states, API rate/error responses, missing templates, huge templates, CJK/special characters, and stale/unsafe config.
- validation_or_tests: Key child roles include `test-finalize-phase.sh` for finalize-state transitions; `test-cancel-signal-file.sh` and robustness cancel security for authorized cancel moves; `test-codex-review-merge.sh` for `[P?]` review extraction; `test-todo-checker.sh` for legacy TodoWrite and Task-system incompletion; `test-session-id.sh` for session-filtered active loops; `test-agent-teams.sh` for prompt/state propagation; PR-loop split suites for scripts/hooks/stop-hook; and robustness suites for state, setup, path, git, template, timeout, and hook systems.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-041 `file` `hooks/loop-edit-validator.sh`
- cursor: `[_]`
- core_role: PreToolUse `Edit` gate for RLCR and PR-loop protected files. It prevents the agent from mutating generated/control surfaces that drive the RLCR state machine.
- algorithmic_behavior: Reads hook JSON from stdin, extracts `.tool_name`, and exits immediately unless the tool is `Edit` at lines 24-29. It lowercases the target path, extracts `session_id`, blocks round todos and prompt edits at lines 41-54, applies PR-loop protections at lines 60-80, then enforces RLCR-specific restrictions after locating the session-matched active loop at lines 89-150.
- inputs_outputs_state: Input is Claude hook JSON with `tool_name`, `tool_input.file_path`, and optional `session_id`. Output is exit `0` to allow, exit `2` for user/action blocks with stderr template messages, or exit `1` for malformed state safety failure. It does not mutate state.
- gates_or_invariants: Gates include no editing `round-*-todos.md` unless allowlisted, no editing `round-*-prompt.md`, no editing PR-loop `state.md` or generated PR read-only files, correct PR `round-N-pr-resolve.md`, methodology-analysis-only write surface, no `state.md`/`finalize-state.md`/`methodology-analysis-state.md` edits, no RLCR backup `plan.md` edits, no `goal-tracker.md` edits after round 0, and no wrong-round summaries.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at line 18. Depends on `to_lower`, `extract_session_id`, `is_round_file_type`, `find_active_loop`, `is_allowlisted_file`, `is_in_pr_loop_dir`, `is_pr_loop_readonly_file`, `validate_pr_resolve_round`, `resolve_active_state_file`, `parse_state_file_strict`, `is_*_state_file_path`, `is_goal_tracker_path`, `extract_round_number`, and template-backed blocked-message helpers.
- edge_cases_or_failure_modes: The methodology phase canonicalizes paths with `realpath` and falls back for older BSD/macOS behavior at lines 97-107. The summary filename extraction has two sed paths to handle nested vs direct RLCR paths at lines 201-206. A malformed active state fails closed with exit `1` at lines 146-150. Paths outside `.humanize/rlcr` generally pass through, delegating broader filesystem security to the tool sandbox.
- validation_or_tests: `tests/robustness/test-hook-system-robustness.sh` validates normal Edit JSON, malformed JSON behavior, missing `file_path`, state edit blocking, and traversal-to-state blocking at lines 40-155. `tests/test-allowlist-validators.sh` covers Edit allowlist behavior for historical summaries/todos.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-071 `file` `tests/test-ansi-parsing.sh`
- cursor: `[_]`
- core_role: Focused executable spec for the ANSI-stripping/count-parsing algorithm used by the parallel test harness.
- algorithmic_behavior: Defines pass/fail counters at lines 18-31, then tests the portable expression `sed "s/${esc}\\[[0-9;]*m//g"` with `$'\033'` ANSI-C quoting at lines 38-47. It verifies extracted `Passed:` and `Failed:` integers through `grep -oE` and tail selection.
- inputs_outputs_state: Inputs are synthetic strings containing ANSI SGR escape sequences. Outputs are colored `PASS`/`FAIL` lines, final `Passed:`/`Failed:` counts, and exit `0` only when all assertions pass at lines 160-178.
- gates_or_invariants: The invariant is that test-runner aggregation must work on GNU/Linux and BSD/macOS `sed`; it must handle plain text, multiple color spans, bold+color, zero failures, and multiline suite summaries.
- dependencies_and_callers: It is listed in `tests/run-all-tests.sh` at line 71. It mirrors the production harness stripping/parsing logic at `tests/run-all-tests.sh:230-250`.
- edge_cases_or_failure_modes: Covers multiple ANSI sequences in one line at lines 55-67, complex multiline summary with both passed/failed counts at lines 112-130, no ANSI text at lines 133-144, and combined bold/color at lines 147-158. It only targets SGR `m` sequences, not arbitrary cursor/control sequences.
- validation_or_tests: Self-contained eight-test script. It is itself a validation asset for `run-all-tests.sh` result parsing.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-101 `file` `tests/test-skill-monitor.sh`
- cursor: `[_]`
- core_role: Executable specification for `_humanize_monitor_skill --once`, the monitor view over one-shot ask-codex skill invocation state in `.humanize/skill`.
- algorithmic_behavior: Builds isolated git repos, sources `scripts/humanize.sh`, fabricates skill invocation directories with `input.md`, `metadata.md`, and optional `output.md`, then asserts monitor summary text and focused-output behavior. Test data construction is in `create_skill_invocation` at lines 56-104.
- inputs_outputs_state: Inputs are temporary `.humanize/skill/<timestamp-id>` directories. `input.md` carries question/model/effort/timeout fields, `metadata.md` carries status/duration/exit code, and `output.md` carries model response text. Output is `_humanize_monitor_skill --once` text plus script pass/fail counters.
- gates_or_invariants: Monitor must error when `.humanize/skill` is missing or empty, count `success`, `error`, `timeout`, `empty_response`, and `running`, focus the newest invocation with usable content, include model/duration/question/output, list recent invocations newest-first, extract only the first question line, show “No output available” for empty responses, and ignore non-timestamp directories.
- dependencies_and_callers: Sources `scripts/humanize.sh` at line 53, which sources `scripts/lib/monitor-skill.sh`. Production monitor functions are in `monitor-skill.sh`: directory validation lines 35-40, timestamp directory filter lines 42-53, status counting lines 82-105, question extraction lines 107-114, best monitored file selection lines 127-167, and `--once` output lines 268-345.
- edge_cases_or_failure_modes: Tests running invocation without `metadata.md` at lines 245-267, multiline questions at lines 295-346, empty response at lines 348-369, and non-skill directory filtering at lines 371-389. The interactive terminal mode is explicitly not tested because it requires a terminal at file header lines 5-6.
- validation_or_tests: This is the direct test suite. Related producer behavior is in `scripts/ask-codex.sh`, which writes `.humanize/skill/<unique-id>/input.md`, cache files, `metadata.md`, and `output.md` at lines 202-237 and 261-410.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-131 `file` `prompt-template/block/incomplete-todos.md`
- cursor: `[_]`
- core_role: Stop-hook block template for the pre-Codex-review task-completion gate.
- algorithmic_behavior: Renders an incomplete-task list through `{{INCOMPLETE_LIST}}` at line 5, then instructs the agent to complete every remaining task and mark each task completed via `TaskUpdate` before attempting to stop at lines 7-10.
- inputs_outputs_state: Input is the rendered incomplete task list from `hooks/check-todos-from-transcript.py`. Output is a blocking reason string embedded in JSON by the stop hook. The template itself has no side effects.
- gates_or_invariants: Enforces “no Codex review while tasks remain incomplete” at line 12. This keeps worker/agent task state as a hard precondition before RLCR review/stop transitions.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh` runs the task checker at lines 387-392, handles parse errors at lines 394-410, detects incomplete tasks at lines 413-416, renders this template with `load_and_render_safe` at lines 418-424, and returns JSON `decision: block` at lines 428-432.
- edge_cases_or_failure_modes: If the task checker parse fails, the hook emits a separate parse-error block rather than using this template. If the template is missing, `load_and_render_safe` uses an inline fallback at `loop-codex-stop-hook.sh:418-424`.
- validation_or_tests: `tests/test-todo-checker.sh` covers legacy TodoWrite and TaskCreate/TaskUpdate incomplete/completed states. Stop-hook integration references the same gate in `tests/test-finalize-phase.sh` and robustness stop-hook coverage.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-161 `file` `prompt-template/claude/open-question-notice.md`
- cursor: `[_]`
- core_role: Claude-facing escalation notice inserted when Codex review output contains Open Questions.
- algorithmic_behavior: Single-line instruction requiring `AskUserQuestion` before resolving any other Codex findings. The stop hook detects “Open Question” headings by scanning review content lines shorter than 40 characters, then prepends/injects this notice.
- inputs_outputs_state: Input is Codex review content containing an Open Question marker. Output is a prompt notice sent back to Claude in the next blocked-round response. The template has no direct state mutation.
- gates_or_invariants: Open questions are treated as a user-clarification gate, not as ordinary fix items. This protects the RLCR transition from proceeding on ambiguous requirements.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh` performs detection at lines 1770-1782, loads this template at line 1783, and falls back to an inline equivalent at lines 1784-1785. Setup exposes the policy toggle in `scripts/setup-rlcr-loop.sh` help/config around lines 85-87, where bypassing AskUserQuestion is marked not recommended.
- edge_cases_or_failure_modes: Detection is intentionally narrow: a line must contain `Open Question` and be under 40 characters, so prose mentions or long headings may not trigger. If the template is missing, an inline fallback preserves the gate.
- validation_or_tests: Covered indirectly through stop-hook review prompt/result tests; no standalone test file is assigned specifically to this one-line template.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-191 `file` `tests/robustness/test-hook-system-robustness.sh`
- cursor: `[_]`
- core_role: Broad robustness executable spec for hook-system safety across Edit, plan-file validation, Bash/Write/Read validators, stop hooks, state parsing, concurrency, and JSON edge cases.
- algorithmic_behavior: Creates temporary loop/project fixtures, pipes hook JSON into production hook scripts, asserts exit codes and block decisions, creates state files with different schemas, uses mock `codex` for active-loop stop-hook behavior, and checks that concurrent hook invocations do not corrupt state.
- inputs_outputs_state: Inputs are synthetic hook payloads, temporary `.humanize/rlcr` and `.humanize/pr-loop` dirs, state frontmatter, plan files, git repos, large JSON payloads, and mock binaries. Outputs are pass/fail counters via `tests/test-helpers.sh` and any hook block JSON/stderr captured for assertions.
- gates_or_invariants: Valid Edit JSON passes; `state.md` edits block; malformed/missing JSON does not crash; paths outside `.humanize` pass through; traversal to `state.md` blocks; valid plan edits pass; non-plan edits pass; whitespace/special state fields parse; Bash cannot modify `state.md` or post-round-0 `goal-tracker.md`; unrelated dangerous commands pass to sandbox; concurrent read validators preserve state; stop hooks allow no-state exits; incomplete/corrupt state ends or handles gracefully; valid active RLCR loop blocks exit; large/null/deep JSON stays bounded.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh`, `scripts/portable-timeout.sh`, and `tests/test-helpers.sh` at lines 22-24. Calls production `loop-edit-validator.sh`, `loop-plan-file-validator.sh`, `loop-bash-validator.sh`, `loop-write-validator.sh`, `loop-read-validator.sh`, `loop-codex-stop-hook.sh`, and `pr-loop-stop-hook.sh`.
- edge_cases_or_failure_modes: Explicitly covers malformed JSON at lines 80-92, missing `file_path` at lines 94-107, traversal inside `.humanize` at lines 124-155, missing YAML delimiter at lines 290-307, command injection/security boundary behavior at lines 317-382, concurrent hooks at lines 421-451, corrupt/missing critical state fields at lines 493-557, active-loop block behavior at lines 559-613, 100KB JSON at lines 623-635, escaped null at lines 637-649, and 10-level nested JSON at lines 651-665.
- validation_or_tests: This file is itself the validation artifact and is also included in the full harness at `tests/run-all-tests.sh:115`. It complements `tests/robustness/test-hook-input-robustness.sh` by focusing on hooks not covered there, as declared at lines 5-15.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `7 unique assigned item sections above; item IDs intentionally appear only in their section headings`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`