# agent_28 do-not-wish-coding 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `ac6cd9c180bcb9b84f6083fba1e458b4aab9ae14`
- note: research-only pass; no files modified and no validation commands executed.

## Item Evidence

### DO_NOT_WISH_CODING-HZ-028 `file` `agents/plan-understanding-quiz.md`
- cursor: `[_]`
- core_role: Defines the advisory pre-RLCR plan-understanding quiz agent. It converts a concrete plan plus repository context into a small technical comprehension check before `/humanize:start-rlcr-loop` proceeds.
- algorithmic_behavior: The agent must analyze plan content, inspect repository docs/structure/referenced files, then generate exactly two multiple-choice questions and one technical summary. `QUESTION_1` targets changed components/mechanism; `QUESTION_2` targets integration constraints or existing patterns (`agents/plan-understanding-quiz.md:14-35`).
- inputs_outputs_state: Input is the plan file content supplied by the caller plus repository context gathered through `Read`, `Glob`, and `Grep` (`agents/plan-understanding-quiz.md:4-5`, `:24-28`). Output is a rigid 13-field text record: two questions, eight options, two answers, and `PLAN_SUMMARY` (`:57-75`). The prompt itself does not persist state.
- gates_or_invariants: Must output all 13 fields, each answer must be exactly one of `A`, `B`, `C`, or `D`, each question has exactly four options and one correct answer, correct answer positions should be randomized, and the output language should match the plan language (`agents/plan-understanding-quiz.md:31`, `:77-85`).
- dependencies_and_callers: Called by `commands/start-rlcr-loop.md`, which instructs the Task tool to invoke `humanize:plan-understanding-quiz`, parse the 13 fields, ask both questions, and let the user proceed or stop after wrong answers (`commands/start-rlcr-loop.md:61-106`). User-facing behavior is documented in `docs/usage.md:26-41`.
- edge_cases_or_failure_modes: If the plan is short or thin, the agent must derive questions from available hints (`agents/plan-understanding-quiz.md:84`). If the agent output is malformed, the command warns that the quiz is unavailable and continues without it (`commands/start-rlcr-loop.md:87`). The quiz is explicitly advisory, not a hard gate (`commands/start-rlcr-loop.md:63`, `docs/usage.md:33-35`).
- validation_or_tests: I did not find a direct shell test for this agent prompt. The caller contract is specified in `commands/start-rlcr-loop.md:76-87`, and the user-facing flow is documented in `docs/usage.md:28-35`.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-058 `file` `scripts/portable-timeout.sh`
- cursor: `[_]`
- core_role: Provides a shared, portable timeout abstraction for Git, GitHub CLI, Codex, setup, hook, and robustness workflows across macOS/Linux.
- algorithmic_behavior: `detect_timeout_impl()` selects the first available implementation in priority order: Homebrew `gtimeout`, GNU `timeout`, `python3`, `python`, or `none` (`scripts/portable-timeout.sh:9-27`). `run_with_timeout <seconds> <command> [args...]` dispatches through that selected implementation while preserving command arguments as an array (`:31-71`).
- inputs_outputs_state: Inputs are timeout seconds and command argv. Outputs are the wrapped command’s stdout/stderr and exit status. `TIMEOUT_IMPL` is computed at source time and exported for sourcing scripts and subprocess visibility (`scripts/portable-timeout.sh:29`, `:73-76`).
- gates_or_invariants: GNU `timeout` is accepted only if `timeout --version` succeeds, avoiding non-GNU/BSD ambiguity (`scripts/portable-timeout.sh:13-19`). Python fallback exits `124` on `subprocess.TimeoutExpired`, matching GNU timeout convention (`:47-61`). If no implementation exists, it warns and runs the command without enforcement (`:64-68`).
- dependencies_and_callers: Sourced by core setup/hooks/scripts including `hooks/loop-codex-stop-hook.sh`, `hooks/pr-loop-stop-hook.sh`, `scripts/setup-rlcr-loop.sh`, `scripts/setup-pr-loop.sh`, `scripts/ask-codex.sh`, and GitHub helper scripts. `rg` showed use of `run_with_timeout` for git, gh, Codex exec/review, and PR-loop checks.
- edge_cases_or_failure_modes: If `TIMEOUT_IMPL=none`, long-running commands are not bounded. Because implementation detection happens when the file is sourced, later `PATH` changes do not update `TIMEOUT_IMPL` unless detection is rerun. Python fallback times out the direct subprocess; it is not an explicit process-group killer, so child process behavior can vary for complex shells.
- validation_or_tests: `tests/robustness/test-timeout-robustness.sh` covers detection, valid implementation names, quick command success, timeout exit `124`, argument preservation, exit-code preservation, pipelines via `sh -c`, zero timeout variance, large output, rapid cycles, nonexistent/empty command behavior, special characters, signal handling, subshells, and `TIMEOUT_IMPL` export (`tests/robustness/test-timeout-robustness.sh:31-279`).
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-088 `file` `tests/test-monitor-runtime.sh`
- cursor: `[_]`
- core_role: Executable specification for RLCR monitor runtime behavior, focused on graceful shutdown, terminal restoration, idempotent cleanup, directory deletion detection, and signal handling.
- algorithmic_behavior: The script creates a temporary test workspace under `/tmp`, synthesizes small runtime test scripts, sources or inspects `scripts/humanize.sh`, tracks pass/fail counters, and exits nonzero if any check fails (`tests/test-monitor-runtime.sh:12-53`, `:492-513`).
- inputs_outputs_state: Inputs are the repository’s `scripts/humanize.sh`, a temporary `.humanize/rlcr` directory, optional `zsh`, and shell signal behavior. Outputs are colorized PASS/FAIL lines and final exit `0` or `1`. Internal test state is `TESTS_PASSED`, `TESTS_FAILED`, temporary files, and stub state variables such as `cleanup_done`, `monitor_running`, and `tail_pid`.
- gates_or_invariants: `_graceful_stop` must call `_cleanup`, `_cleanup` must be idempotent, deletion of `.humanize/rlcr` must stop monitoring gracefully, `_restore_terminal` must reset scroll region, bash `INT`/`TERM` traps and zsh `TRAPINT`/`TRAPTERM` must exist, and cleanup must reset traps (`tests/test-monitor-runtime.sh:56-135`, `:137-178`, `:180-251`, `:253-324`, `:326-490`).
- dependencies_and_callers: The implementation under test is `scripts/humanize.sh`: `_restore_terminal` resets scroll region and moves cursor (`scripts/humanize.sh:645-651`), `_cleanup` flips state, resets traps, kills `tail_pid`, restores terminal, and prints stop text (`:670-701`), `_graceful_stop` calls `_cleanup` and emits the deletion/cancel message (`:703-716`), and the monitor loop checks `.humanize/rlcr` at multiple polling points (`:777-783`, `:839-843`, `:950-954`).
- edge_cases_or_failure_modes: Several tests use simplified redefinitions rather than the real functions, so they specify expected semantics but can drift from implementation details (`tests/test-monitor-runtime.sh:64-106`, `:143-168`, `:186-230`). There is also a dead/brittle grep pipeline at `tests/test-monitor-runtime.sh:282` because `grep -q` emits no output into the next `grep`; a later source check at `:307-311` covers the same `_cleanup -> _restore_terminal` invariant more reliably.
- validation_or_tests: This file is itself validation. It also statically checks implementation source for function definitions, escape-sequence reset, trap setup, and trap reset (`tests/test-monitor-runtime.sh:274-307`, `:390-423`). I did not execute it in this research-only pass.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-118 `file` `prompt-template/block/codex-review-failed.md`
- cursor: `[_]`
- core_role: Markdown block template for communicating a blocking Codex review failure and telling the user that another review attempt will occur on exit.
- algorithmic_behavior: Renders failure metadata: exit code, missing review result file, debug command/stdout/stderr file paths, and the last stderr content (`prompt-template/block/codex-review-failed.md:1-18`). It is a prompt/output contract rather than executable code.
- inputs_outputs_state: Inputs are template variables `CODEX_EXIT_CODE`, `REVIEW_RESULT_FILE`, `CODEX_CMD_FILE`, `CODEX_STDOUT_FILE`, `CODEX_STDERR_FILE`, and `STDERR_CONTENT`. Output is a Markdown reason string used in a hook block response. No persistent state is written by the template itself.
- gates_or_invariants: The template assumes the review result file was not created and frames the failure as retryable. The template loader performs single-pass substitution and preserves unresolved placeholders (`hooks/lib/template-loader.sh:7-13`, `:116-121`), so callers must supply matching variable names.
- dependencies_and_callers: `block_review_failure` in `hooks/loop-codex-stop-hook.sh` invokes `load_and_render_safe "$TEMPLATE_DIR" "block/codex-review-failed.md"` when `codex review` fails or produces no stdout (`hooks/loop-codex-stop-hook.sh:1088-1098`, `:1106-1109`, `:1320-1380`). The rendered reason is returned in JSON with `"decision": "block"` and system message `"Loop: Blocked - Codex review failed, retry required"` (`:1372-1379`).
- edge_cases_or_failure_modes: The current call site passes `EXIT_CODE` and `CODEX_LOG_FILE`, but the template expects `CODEX_EXIT_CODE` and `CODEX_STDERR_FILE`; it also does not pass `CODEX_STDOUT_FILE` (`hooks/loop-codex-stop-hook.sh:1362-1370` vs. `prompt-template/block/codex-review-failed.md:5-11`). Because missing placeholders are preserved, this can leak unresolved `{{...}}` markers in the user-facing block instead of falling back.
- validation_or_tests: I found no direct test that renders `block/codex-review-failed.md`. Template loader tests cover missing-variable preservation and real rendering for other templates, not this one (`hooks/lib/template-loader.sh:116-121`; `tests/test-template-loader.sh:151-164`).
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-148 `file` `prompt-template/block/wrong-round-number.md`
- cursor: `[_]`
- core_role: Validator block template for preventing writes/edits to stale `round-N-summary.md` files when the active RLCR state is on a different round.
- algorithmic_behavior: Renders a concise correction message: attempted action, stale round/file type, current round, correct path, and the invariant “Do NOT increment the round number yourself” (`prompt-template/block/wrong-round-number.md:1-7`).
- inputs_outputs_state: Inputs are `ACTION`, `CLAUDE_ROUND`, `FILE_TYPE`, `CURRENT_ROUND`, and `CORRECT_PATH`. Output is Markdown to stderr from validators; the validators then exit with code `2` to block the operation.
- gates_or_invariants: Write/edit validators extract the round from attempted summary filenames and compare it to `STATE_CURRENT_ROUND`. If mismatched and not allowlisted, they render this template and block (`hooks/loop-write-validator.sh:230-247`, `hooks/loop-edit-validator.sh:162-179`). Missing template variables would be preserved by `render_template`, making caller completeness important (`hooks/lib/template-loader.sh:116-121`).
- dependencies_and_callers: Used by `hooks/loop-write-validator.sh` and `hooks/loop-edit-validator.sh` through `load_and_render_safe`. Related read-path round mismatches use `block/wrong-round-file.md`, not this template (`hooks/loop-read-validator.sh:138-149`).
- edge_cases_or_failure_modes: The template applies to summary write/edit checks, not all round-file reads. If `extract_round_number` returns empty, the write/edit validators do not block on round mismatch. Allowlisted files bypass the guard. Caller-provided `ACTION` wording changes the sentence, for example “write to” vs. “edit”.
- validation_or_tests: `tests/test-template-loader.sh` renders the real template and checks title, stale filename, and current round (`tests/test-template-loader.sh:151-164`). `tests/test-templates-comprehensive.sh` also checks all key replacements, including correct path (`tests/test-templates-comprehensive.sh:498-510`).
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-178 `file` `skills/ask-codex/SKILL.md`
- cursor: `[_]`
- core_role: Skill instruction for one-shot Codex consultation through `scripts/ask-codex.sh`, used when Claude needs an independent expert answer rather than starting an RLCR loop.
- algorithmic_behavior: The skill constrains invocation shape: quote free-form user text, pass simple questions as one final quoted argument, and if flags are present, keep flags as separate shell arguments while keeping the remaining question as one quoted final argument (`skills/ask-codex/SKILL.md:12-36`).
- inputs_outputs_state: Inputs are optional `--codex-model MODEL:EFFORT`, optional `--codex-timeout SECONDS`, and a question/task string (`skills/ask-codex/SKILL.md:4`, `:16-28`). The script outputs Codex response on stdout and status/debug information on stderr (`:38-42`). It saves response state under `.humanize/skill/<timestamp>/output.md` (`:53-56`).
- gates_or_invariants: The central invariant is shell-safety: never run the script with bare `$ARGUMENTS`, because shell reparsing can break or reinterpret metacharacters (`skills/ask-codex/SKILL.md:14`, `:30-36`). Exit handling maps `0` to success, `1` to validation error, `124` to timeout, and other values to Codex process errors (`:44-51`).
- dependencies_and_callers: Allowed tool target is `${CLAUDE_PLUGIN_ROOT}/scripts/ask-codex.sh` (`skills/ask-codex/SKILL.md:5`). The script itself sources `portable-timeout.sh` and `loop-common.sh`, validates model/effort characters, creates `.humanize/skill` and cache directories, runs `codex exec` through `run_with_timeout`, and writes metadata for success/error/timeout/empty response (`scripts/ask-codex.sh:28-43`, `:153-186`, `:202-237`, `:243-410`). RLCR task-tag routing points `analyze` tasks to `/humanize:ask-codex` (`commands/start-rlcr-loop.md:120-123`).
- edge_cases_or_failure_modes: If Codex is missing, the question is empty, flags are unknown/malformed, model or effort contains unsafe characters, Codex times out, returns nonzero, or returns empty stdout, the script reports an error and exits nonzero (`scripts/ask-codex.sh:153-186`, `:308-380`). The skill’s safety depends on the caller preserving quoting; incorrect reconstruction can fail before the script starts.
- validation_or_tests: `tests/test-ask-codex.sh` uses a mock Codex binary to test empty question, help, unknown options, missing flag values, invalid model/effort characters, successful stdout and saved files, nonzero exit propagation, timeout `124`, empty response, uniqueness of skill/cache dirs, `--` separator, timeout recording, and the skill’s unsafe `$ARGUMENTS` warning (`tests/test-ask-codex.sh:84-420`). `tests/test-unified-codex-config.sh` verifies config-backed defaults and CLI override behavior (`tests/test-unified-codex-config.sh:658-681`, `:811-870`).
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6 unique `## Item Evidence` sections, matching the assigned count.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`