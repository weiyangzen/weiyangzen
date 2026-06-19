# agent_24 do-not-block-stop-when-background-running 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `3711e5fd9059584c7bf98cf1d19ee02dcf5bef48`

## Item Evidence

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-024 `directory` `skills/humanize-rlcr`
- cursor: `[_]`
- core_role: Codex-facing RLCR flow entrypoint. The directory recursively contains only `skills/humanize-rlcr/SKILL.md`, which defines how Codex starts and continues Ralph-Loop with Codex Review using native Stop hooks.
- algorithmic_behavior: The skill requires setup through `{{HUMANIZE_RUNTIME_ROOT}}/scripts/setup-rlcr-loop.sh` with forwarded `$ARGUMENTS` (`skills/humanize-rlcr/SKILL.md:24-34`). Each round is driven by generated prompt files, implementation, commit, summary write, normal exit, then automatic Stop-hook evaluation (`skills/humanize-rlcr/SKILL.md:36-48`).
- inputs_outputs_state: Inputs are the plan file/options passed to setup, including `--skip-impl`, `--max`, `--codex-model`, `--codex-timeout`, `--base-branch`, `--full-review-round`, `--push-every-round`, and agent-team/yolo flags (`skills/humanize-rlcr/SKILL.md:76-98`). Outputs/state live under `.humanize/rlcr/<timestamp>/`, especially `round-<N>-prompt.md`, `round-<N>-summary.md`, finalize summaries, review results, and hook-managed state files (`skills/humanize-rlcr/SKILL.md:40-45`).
- gates_or_invariants: It explicitly delegates enforcement to native Stop hooks: schema validation, branch consistency, plan-file integrity, incomplete todo blocking, clean-git exit, push-every-round, summary presence, max-iteration handling, full-alignment rounds, strict `COMPLETE`/`STOP` markers, review-phase marker, `[P0-9]` code-review gating, Codex review failure blocking, and open-question handling (`skills/humanize-rlcr/SKILL.md:50-68`).
- dependencies_and_callers: Installation treats `humanize-rlcr` as one of the synced skill directories (`scripts/install-skill.sh:39-44`) and validates its `SKILL.md` exists (`scripts/install-skill.sh:85-87`). Runtime depends on `scripts/setup-rlcr-loop.sh`, `scripts/cancel-rlcr-loop.sh`, and Stop-hook machinery reached from generated loop state.
- edge_cases_or_failure_modes: Setup nonzero exit is terminal for the flow (`skills/humanize-rlcr/SKILL.md:34`). The critical rules forbid manual edits to `state.md`/`finalize-state.md`, skipping blocked hook output, ad-hoc `codex exec` or `codex review`, and using non-generated files as source of truth (`skills/humanize-rlcr/SKILL.md:69-75`).
- validation_or_tests: `tests/test-codex-hook-install.sh` checks Codex install keeps the entrypoint skill, while setup, session, plan-validation, stop-hook, and unified config tests exercise the scripts this skill invokes.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-054 `file` `scripts/portable-timeout.sh`
- cursor: `[_]`
- core_role: Cross-platform timeout abstraction used by RLCR hooks and skill scripts so monitor/review/git/model calls can be bounded consistently on macOS and Linux.
- algorithmic_behavior: `detect_timeout_impl` selects `gtimeout`, GNU `timeout`, `python3`, `python`, then `none` in priority order (`scripts/portable-timeout.sh:9-27`). `run_with_timeout <seconds> <command> [args...]` dispatches to the selected implementation and returns the wrapped command’s exit code, or `124` for timeout in GNU/Python paths (`scripts/portable-timeout.sh:31-71`).
- inputs_outputs_state: Input is a timeout seconds value followed by a command argv array (`scripts/portable-timeout.sh:33-36`). Output is stdout/stderr from the wrapped command plus the command/timeout exit status. It sets global `TIMEOUT_IMPL` when sourced and exports that variable for callers (`scripts/portable-timeout.sh:29`, `scripts/portable-timeout.sh:73-76`).
- gates_or_invariants: The GNU `timeout` candidate is accepted only if `timeout --version` succeeds, avoiding non-GNU/BSD incompatibility (`scripts/portable-timeout.sh:13-19`). Python fallback uses `subprocess.run(..., timeout=...)` and maps `TimeoutExpired` to `124` (`scripts/portable-timeout.sh:47-61`).
- dependencies_and_callers: Sourced by `hooks/loop-codex-stop-hook.sh` before git/review work (`hooks/loop-codex-stop-hook.sh:49-51`), by `hooks/loop-plan-file-validator.sh`, and by producer scripts such as `scripts/ask-codex.sh:28-29`, `scripts/ask-gemini.sh:29-30`, and `scripts/bitlesson-select.sh`.
- edge_cases_or_failure_modes: If no timeout implementation exists, it warns and runs unbounded (`scripts/portable-timeout.sh:64-68`). The function itself does not validate that timeout seconds are numeric; several callers validate their own CLI timeout values before calling. Python fallback kills the direct subprocess on timeout but does not provide GNU `timeout` process-group semantics for grandchildren.
- validation_or_tests: `tests/robustness/test-timeout-robustness.sh` checks implementation detection, valid implementation names, quick completion, exit `124`, argument preservation, command exit-code preservation, pipelines, zero timeout, large output, rapid cycles, nonexistent commands, special characters, and signal handling (`tests/robustness/test-timeout-robustness.sh:31-247`).
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-084 `file` `tests/test-monitor-e2e-deletion.sh`
- cursor: `[_]`
- core_role: Thin executable split for monitor deletion E2E coverage; it runs the bash and zsh deletion scenarios from the shared real monitor test file.
- algorithmic_behavior: The wrapper sources `tests/test-monitor-e2e-real.sh`, prints a suite header, calls `monitor_test_bash_deletion` and `monitor_test_zsh_deletion`, then exits based on accumulated `TESTS_FAILED` (`tests/test-monitor-e2e-deletion.sh:4-21`).
- inputs_outputs_state: Inputs are the sourced functions and globals from `test-monitor-e2e-real.sh`. Outputs are PASS/FAIL logs and process exit `0` only when `TESTS_FAILED == 0` (`tests/test-monitor-e2e-deletion.sh:19-21`).
- gates_or_invariants: Bash deletion test creates a real `.humanize/rlcr/<timestamp>` session, starts `_humanize_monitor_codex`, deletes `.humanize/rlcr`, waits with a bounded loop, and requires graceful exit (`tests/test-monitor-e2e-real.sh:60-181`). It gates on friendly stop text, deletion reason, absence of zsh/bash glob errors, cleanup message, source scroll-reset escape, and `EXIT_CODE:0` (`tests/test-monitor-e2e-real.sh:187-227`).
- dependencies_and_callers: Depends on `scripts/humanize.sh` exposing the real monitor (`tests/test-monitor-e2e-real.sh:144-149`, `tests/test-monitor-e2e-real.sh:312-319`), fake `HOME`/`XDG_CACHE_HOME` cache layout, terminal command shims, and optional `zsh`.
- edge_cases_or_failure_modes: The zsh path skips when `zsh` is unavailable (`tests/test-monitor-e2e-real.sh:238-240`). Both tests force-kill if the monitor fails to exit within the wait budget, which converts a hang into a failed assertion (`tests/test-monitor-e2e-real.sh:168-178`, `tests/test-monitor-e2e-real.sh:335-345`).
- validation_or_tests: This file is itself validation. It specifically protects deletion-triggered stop behavior, terminal restoration, and shell-glob safety for the RLCR monitor, not the skill monitor.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-114 `file` `prompt-template/block/codex-review-failed.md`
- cursor: `[_]`
- core_role: Blocking prompt template shown when Codex review fails to produce output, keeping the RLCR Stop hook from allowing completion without review evidence.
- algorithmic_behavior: The template renders a short failure report with exit code, missing review result path, debug command/stdout/stderr paths, and last stderr lines, ending with retry guidance (`prompt-template/block/codex-review-failed.md:1-18`).
- inputs_outputs_state: Intended inputs are `CODEX_EXIT_CODE`, `REVIEW_RESULT_FILE`, `CODEX_CMD_FILE`, `CODEX_STDOUT_FILE`, `CODEX_STDERR_FILE`, and `STDERR_CONTENT` placeholders (`prompt-template/block/codex-review-failed.md:5-15`). Output is text embedded as the hook JSON `reason`.
- gates_or_invariants: The Stop hook wraps this rendered text in a JSON decision of `"block"` with system message `Loop: Blocked - Codex review failed, retry required` (`hooks/loop-codex-stop-hook.sh:1612-1619`), so failed review remains a hard loop gate rather than a warning.
- dependencies_and_callers: Loaded through `load_and_render_safe` in `hooks/loop-codex-stop-hook.sh` (`hooks/loop-codex-stop-hook.sh:1601-1610`). Template loading preserves missing placeholders as literal text by design (`hooks/lib/template-loader.sh:7-14`, `hooks/lib/template-loader.sh:115-120`).
- edge_cases_or_failure_modes: Caller/template variable names are partially inconsistent: the hook passes `EXIT_CODE` and `CODEX_LOG_FILE`, but the template expects `CODEX_EXIT_CODE`, `CODEX_STDOUT_FILE`, and `CODEX_STDERR_FILE` (`hooks/loop-codex-stop-hook.sh:1602-1610`; `prompt-template/block/codex-review-failed.md:5-15`). Because missing placeholders are preserved, the user may see raw placeholder text in this block.
- validation_or_tests: `tests/test-template-references.sh` checks that referenced templates exist and that critical validators use safe rendering (`tests/test-template-references.sh:51-111`, `tests/test-template-references.sh:170-201`), but it does not validate placeholder/caller compatibility.
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-144 `file` `prompt-template/block/wrong-contract-location.md`
- cursor: `[_]`
- core_role: Validator block template for the invariant that round contract files must be written inside the active RLCR loop directory.
- algorithmic_behavior: The template emits a title, states the contract-location rule, and renders the correct path through `{{CORRECT_PATH}}` (`prompt-template/block/wrong-contract-location.md:1-5`).
- inputs_outputs_state: Input is one placeholder, `CORRECT_PATH`. Output is stderr text returned by the write validator before it exits nonzero.
- gates_or_invariants: `hooks/loop-write-validator.sh` triggers this template when a summary or contract file write is detected outside `.humanize/rlcr`; for contracts it computes `$ACTIVE_LOOP_DIR/round-${CURRENT_ROUND}-contract.md`, renders this template, and exits `2` (`hooks/loop-write-validator.sh:266-287`).
- dependencies_and_callers: Depends on active-loop detection, `IS_CONTRACT_FILE`, `IN_HUMANIZE_LOOP_DIR`, current round, and `load_and_render_safe`. The fallback message mirrors the same correct-path contract if the template is missing (`hooks/loop-write-validator.sh:270-277`).
- edge_cases_or_failure_modes: The template is intentionally minimal; diagnostic quality depends entirely on the validator supplying the active loop/current round correctly. It does not explain how the wrong path was classified or what attempted path was rejected.
- validation_or_tests: Covered indirectly by template reference validation, which scans hook scripts for referenced template files and fails on missing templates (`tests/test-template-references.sh:83-111`).
- skip_candidate: `no`

### DO_NOT_BLOCK_STOP_WHEN_BACKGROUND_RUNNING-HZ-174 `file` `scripts/lib/monitor-skill.sh`
- cursor: `[_]`
- core_role: Implements `_humanize_monitor_skill`, the live and one-shot monitor for `.humanize/skill` invocations produced by `ask-codex` and `ask-gemini`.
- algorithmic_behavior: Parses `--once` and `--tool-filter <codex|gemini>`, requires `.humanize/skill`, detects invocation tool from `metadata.md` or `input.md`, filters timestamp-named invocation directories, selects newest/best invocation with watchable content, computes status counts, extracts first question line, finds cache files, and either prints a one-shot report or runs an interactive status-bar plus `tail -f` monitor (`scripts/lib/monitor-skill.sh:18-42`, `scripts/lib/monitor-skill.sh:43-143`, `scripts/lib/monitor-skill.sh:145-217`, `scripts/lib/monitor-skill.sh:339-527`).
- inputs_outputs_state: Inputs are invocation directories named `YYYY-MM-DD_HH-MM-SS...`, `input.md`, optional `metadata.md`, optional `output.md`, global cache under `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/<sanitized-project>/skill-<id>`, and optional local `cache/` (`scripts/lib/monitor-skill.sh:154-163`, `scripts/lib/monitor-skill.sh:165-217`). Outputs are terminal UI/report text; the script keeps only transient monitor state such as current directory/file and `TAIL_PID`.
- gates_or_invariants: Missing `.humanize/skill` returns error with setup guidance (`scripts/lib/monitor-skill.sh:43-48`). Valid invocation directories must match the timestamp prefix regex (`scripts/lib/monitor-skill.sh:77-90`). Unknown legacy invocations pass the Codex filter (`scripts/lib/monitor-skill.sh:66-74`). Status buckets are `success`, `error`, `timeout`, `empty_response`, and implicit `running` when `metadata.md` is absent (`scripts/lib/monitor-skill.sh:119-143`).
- dependencies_and_callers: Sourced by `scripts/humanize.sh` (`scripts/humanize.sh:1243-1246`) and dispatched through `humanize monitor skill|codex|gemini` (`scripts/humanize.sh:1195-1211`). Depends on `monitor_get_yaml_value`, `monitor_format_timestamp`, and `humanize_split_to_array` (`scripts/lib/monitor-skill.sh:8-10`, `scripts/lib/monitor-skill.sh:240-255`).
- edge_cases_or_failure_modes: Interactive cleanup disowns/kills/waits the active tail and restores scroll region/alternate screen (`scripts/lib/monitor-skill.sh:438-461`). If `.humanize/skill` is deleted while running, it cleans up and returns success after printing `Skill directory deleted.` (`scripts/lib/monitor-skill.sh:472-479`). Very narrow terminals may stress substring/truncation math because widths are computed as `term_width - 14` (`scripts/lib/monitor-skill.sh:273-299`).
- validation_or_tests: `tests/test-skill-monitor.sh` covers missing directory, empty directory, single/multiple invocations, running invocations, recent list, question extraction, empty response, and non-timestamp directory filtering (`tests/test-skill-monitor.sh:107-390`). Producer contracts are created by `scripts/ask-codex.sh` and `scripts/ask-gemini.sh`, which write `.humanize/skill/<unique-id>/input.md`, cache files, `output.md`, and metadata statuses (`scripts/ask-codex.sh:202-238`, `scripts/ask-codex.sh:309-405`; `scripts/ask-gemini.sh:181-215`, `scripts/ask-gemini.sh:291-377`).
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `6/6 item sections present; each assigned heading occurs once`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`