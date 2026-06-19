# agent_14 add-careful-mode-v1.6.5 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `a12de5d9f36bb10cd62955881f4e76d67d3f50ce`
- note: read-only research only; no files modified. I did not run the suites, only inspected assigned files and focused dependencies.

## Item Evidence

### ADD_CAREFUL_MODE_V1_6_5-HZ-014 `directory` `prompt-template/pr-loop`
- cursor: `[_]`
- core_role: PR review-loop prompt surface. The directory contains seven Markdown templates and no nested subdirectories: `codex-goal-tracker-update.md`, `critical-requirements-has-comments.md`, `critical-requirements-no-comments.md`, `goal-tracker-initial.md`, `round-0-header.md`, `round-0-task-has-comments.md`, and `round-0-task-no-comments.md`.
- algorithmic_behavior: `round-0-header.md:1-15` starts the PR review loop prompt and inserts PR metadata plus fetched comments. `round-0-task-has-comments.md:4-43` selects the active remediation path: analyze human comments first, then bot comments, fix issues, commit, push, trigger re-review, and write a resolution summary. `round-0-task-no-comments.md:4-30` selects the waiting path for fresh PRs and explicitly avoids manual trigger comments. `critical-requirements-has-comments.md:6-23` and `critical-requirements-no-comments.md:6-20` restate the terminal actions printed after setup output. `goal-tracker-initial.md:1-33` defines the initial tracker schema. `codex-goal-tracker-update.md:1-64` defines how Codex adds per-round review rows, statistics, and issue log entries.
- inputs_outputs_state: Inputs are template variables rendered by `hooks/lib/template-loader.sh`, mainly `PR_NUMBER`, `START_BRANCH`, `ACTIVE_BOTS_DISPLAY`, `RESOLVE_PATH`, `BOT_MENTION_STRING`, `STARTED_AT`, `STARTUP_CASE`, `GOAL_TRACKER_FILE`, and `NEXT_ROUND`. Outputs become `.humanize/pr-loop/.../goal-tracker.md`, `round-0-prompt.md`, setup terminal text, and later `round-N-codex-prompt.md`; see `scripts/setup-pr-loop.sh:712-713`, `758-764`, `800-851`, `914-940`, and `hooks/pr-loop-stop-hook.sh:1252-1261`.
- gates_or_invariants: The branch point is comment presence: `scripts/setup-pr-loop.sh:723-729` treats the exact “No comments found” sentinel as no-comment mode. No-comment mode forbids trigger comments; has-comment mode requires commit/push plus a bot mention. Tracker-update instructions require preserving header sections and adding rows rather than replacing tables (`codex-goal-tracker-update.md:57-64`).
- dependencies_and_callers: Loaded via `load_and_render_safe` from `hooks/lib/template-loader.sh`; setup falls back to inline strings if templates are missing. Coordinates with sibling `prompt-template/block/*` templates for hook block messages and parent `prompt-template` directory validation.
- edge_cases_or_failure_modes: Missing or empty templates degrade to fallback text, so the loop can still start. If fetched comment output changes and no longer uses the sentinel, setup will choose the has-comments path. Goal tracker schema tests only assert key sections/fields in `tests/test-pr-loop-system.sh:642-655`, so finer tracker semantics depend on prompt compliance.
- validation_or_tests: Covered by PR-loop setup/system tests, especially `tests/test-pr-loop-system.sh:642-655`, plus template reference/comprehensive tests discovered through `tests/run-all-tests.sh:53-54`.
- skip_candidate: `no`

### ADD_CAREFUL_MODE_V1_6_5-HZ-044 `file` `tests/run-all-tests.sh`
- cursor: `[_]`
- core_role: Top-level executable specification aggregator for Humanize plugin behavior, including RLCR hooks, PR-loop behavior, template behavior, monitor behavior, and robustness suites.
- algorithmic_behavior: Defines ordered `TEST_SUITES` at `tests/run-all-tests.sh:33-73`, special zsh-only execution at `76-78`, then loops over suites at `80-139`. Missing files are skipped (`83-86`). zsh suites are run with `zsh` only if available (`97-114`); all other suites are executed directly (`115-118`).
- inputs_outputs_state: Input is the repository `tests/` tree and executable suite output. It captures each suite’s stdout/stderr into `output`, strips ANSI codes (`121-123`), extracts final `Passed:` and `Failed:` counts (`124-125`), accumulates totals (`127-128`), records failed suite names in `FAILED_SUITES`, prints a summary, and exits `1` if any suite failed (`148-159`).
- gates_or_invariants: A suite fails the aggregate gate if its process exit code is nonzero or its parsed failed count is greater than zero (`130-134`). Missing suites and unavailable zsh are skips, not failures. The parser assumes test summaries use the shared `Passed:` / `Failed:` labels.
- dependencies_and_callers: Depends on every named script being executable or intentionally absent. It includes the assigned robustness file at `tests/run-all-tests.sh:61`. The pass/fail format aligns with `tests/test-helpers.sh:58-77`.
- edge_cases_or_failure_modes: Suites that omit pass/fail lines contribute `0` counts unless their exit code fails. Only `test-zsh-monitor-safety.sh` is forced through zsh. After each captured run the script enables `set -e` at `119`, so later commands outside guarded capture paths need to remain non-failing.
- validation_or_tests: This file is itself the validation entry point. It does not validate implementation directly; it delegates to ordered suites and enforces aggregate exit status.
- skip_candidate: `no`

### ADD_CAREFUL_MODE_V1_6_5-HZ-074 `file` `hooks/lib/template-loader.sh`
- cursor: `[_]`
- core_role: Shared template loading/rendering library for RLCR and PR-loop hooks. It turns Markdown templates into hook block messages, Codex prompts, Claude prompts, and setup prompts while preserving fallback behavior.
- algorithmic_behavior: `get_template_dir` derives `prompt-template` from the caller’s `hooks/lib` path (`26-31`). `load_template` cats an existing template or warns and returns empty output (`36-48`). `render_template` builds `TMPL_VAR_*` environment entries (`62-69`) and uses one awk pass to scan for `{{...}}` placeholders (`74-129`). `load_and_render` combines load plus render (`136-147`), `append_template` concatenates template content (`151-161`), `load_and_render_safe` uses fallback text when loading or rendering is empty (`170-203`), and `validate_template_dir` checks parent template structure (`208-222`).
- inputs_outputs_state: Inputs are a template directory, relative template name, fallback string for safe calls, and `VAR=value` pairs. Output is rendered text to stdout; warnings/errors go to stderr. The library stores no persistent state.
- gates_or_invariants: Rendering is intentionally single-pass (`54-57`, `71-73`): if a variable value contains another placeholder, it is emitted literally rather than recursively expanded. Unknown placeholders stay unchanged (`119-122`). This is the main prompt-injection/corruption guard for template values containing review content, paths, or shell-like characters.
- dependencies_and_callers: Depends on `awk`, `env`, `cat`, and the `prompt-template` tree. Called by hook validators, `loop-common.sh`, RLCR stop hooks, PR-loop setup/stop hooks, and template tests. The assigned `wrong-round-file.md` is rendered through this library from `hooks/loop-read-validator.sh:144-149`.
- edge_cases_or_failure_modes: Empty template files are treated as missing by `load_and_render_safe`. `load_and_render` silently produces no rendered output when content is empty. Placeholder syntax is conventionally uppercase, but the renderer mechanically uses whatever appears between `{{` and `}}`. Unclosed `{{` is emitted literally by the awk scanner.
- validation_or_tests: Directly exercised by `tests/test-template-loader.sh` and broader template stress/error suites listed in `tests/run-all-tests.sh:35`, `40`, `62`, and `70`.
- skip_candidate: `no`

### ADD_CAREFUL_MODE_V1_6_5-HZ-104 `file` `prompt-template/block/wrong-round-file.md`
- cursor: `[_]`
- core_role: Read-block template for stale or future RLCR round files. It is part of the guardrail that keeps agents focused on the active round’s prompt/summary.
- algorithmic_behavior: The template tells the agent it attempted to read `round-{{CLAUDE_ROUND}}-{{FILE_TYPE}}.md` while the active round is `{{CURRENT_ROUND}}` (`prompt-template/block/wrong-round-file.md:3`), lists the current round prompt and summary paths (`5-7`), and gives an explicit manual `cat {{FILE_PATH}}` escape hatch (`9`).
- inputs_outputs_state: Render inputs are `CLAUDE_ROUND`, `FILE_TYPE`, `CURRENT_ROUND`, `ACTIVE_LOOP_DIR`, and `FILE_PATH`, supplied by `hooks/loop-read-validator.sh:144-149`. Output is stderr block text and the read validator exits with block status `2` (`hooks/loop-read-validator.sh:138-150`).
- gates_or_invariants: The invariant is that Read-tool access to round prompt/summary files must match the active round unless the target is allowlisted (`hooks/loop-read-validator.sh:138`). The template itself performs no logic; it encodes the user-facing contract for the gate.
- dependencies_and_callers: Depends on `load_and_render_safe` and the read validator’s current-round parsing from active RLCR state (`hooks/loop-read-validator.sh:88-100`). Sibling templates cover wrong directory and wrong location cases.
- edge_cases_or_failure_modes: If variables are missing, unresolved placeholders remain because template rendering preserves unknown placeholders. If the template is missing, the read validator has an inline fallback at `hooks/loop-read-validator.sh:139-143`.
- validation_or_tests: Referenced in template-loader tests (`tests/test-template-loader.sh:153-155`) and comprehensive template tests. Functional behavior is covered by read-validator and hook-system tests named in `tests/run-all-tests.sh`.
- skip_candidate: `no`

### ADD_CAREFUL_MODE_V1_6_5-HZ-134 `file` `tests/robustness/test-hook-input-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable specification for hook JSON parsing, command-modification detection, and monitor edge cases. It pipes synthetic hook JSON into production validators rather than testing stubs.
- algorithmic_behavior: Sets strict mode and sources `hooks/lib/loop-common.sh` plus test helpers (`tests/robustness/test-hook-input-robustness.sh:12-19`). Hook parsing tests cover valid Read/Write/Bash JSON (`35-69`), invalid JSON (`71-85`), missing `tool_name` (`87-100`), missing `tool_input.file_path` (`102-115`), 10KB commands (`117-133`), special characters (`135-147`), Unicode paths (`149-161`), unknown tool pass-through (`163-175`), deeply nested JSON rejection (`177-199`), non-UTF8 rejection (`201-217`), and null-byte no-crash handling (`219-235`).
- inputs_outputs_state: Inputs are generated JSON strings, temporary files, fake project dirs, fake HOME/XDG cache dirs, and generated monitor runner scripts. Outputs are pass/fail lines plus final summary from `print_test_summary` at `670`. Temporary state includes `.humanize/rlcr/<timestamp>/state.md`, `goal-tracker.md`, and cache logs for monitor tests (`491-511`, `583-603`).
- gates_or_invariants: Production validators must reject malformed JSON, missing required fields, JSON depth over 30, and invalid UTF-8 without signal crashes. Unknown tools must pass through. Long/special/unicode valid input must not be rejected. Monitor must exit gracefully when no session exists (`444-486`) and must not crash under narrow terminals or ANSI logs (`488-665`).
- dependencies_and_callers: Uses `validate_hook_input`, `require_tool_input_field`, `is_deeply_nested`, and `command_modifies_file` from `hooks/lib/loop-common.sh:60-134` and `1077-1102`; calls `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, and `hooks/loop-bash-validator.sh`, whose JSON/depth gates are at their early parse sections. It also sources `scripts/humanize.sh` for `humanize_parse_goal_tracker`, `humanize_parse_git_status`, `humanize_detect_git_state`, and `_humanize_monitor_codex` (`381-433`, `444-665`).
- edge_cases_or_failure_modes: Null bytes are explicitly not asserted as rejected because Bash command substitution strips them before the hook can inspect them (`219-230`). Non-UTF8 behavior depends on `iconv`/`jq` but the expected hook exit is `1` (`201-217`). The monitor tests shim `tput` and `clear`, delete session dirs asynchronously, and assert exit code `<128`, so they mainly detect crashes rather than exact UI rendering. The later monitor trap at `448` replaces the earlier temp-dir cleanup trap from `setup_test_dir`, which can leave the first temp dir uncleaned if run as written.
- validation_or_tests: Included by the aggregate runner at `tests/run-all-tests.sh:61`. It is an executable spec for hook input robustness and monitor no-crash behavior, not a branch implementation test by itself.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5 item sections present; each assigned heading appears once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`