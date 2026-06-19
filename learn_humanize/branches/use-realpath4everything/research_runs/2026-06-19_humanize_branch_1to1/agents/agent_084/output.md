# agent_084 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-084 `file` `tests/test-monitor-e2e-deletion.sh`
- cursor: `[_]`
- core_role: This file is an executable shell-test split for the monitor deletion behavior. It is not the monitor implementation itself; it is a focused end-to-end specification that sources the shared real monitor harness and runs only the Bash and Zsh deletion cases. The assigned file resolves its own directory with `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`, then sources `tests/test-monitor-e2e-real.sh`, so the split runner can be invoked from any working directory while still finding the harness. See `tests/test-monitor-e2e-deletion.sh:1-5`, `tests/test-monitor-e2e-deletion.sh:12-13`.

- algorithmic_behavior: The script enables strict Bash mode with `set -euo pipefail`, prints a deletion-test banner, calls `monitor_test_bash_deletion`, calls `monitor_test_zsh_deletion`, prints a summary using the harness counters, and exits with status 0 only when `TESTS_FAILED` is zero. Its algorithm is deliberately linear: initialize harness, execute the two deletion scenarios, summarize, gate process exit. See `tests/test-monitor-e2e-deletion.sh:3-21`.

  The sourced harness performs the actual behavior specification. For the Bash case, it creates a temporary project under `/tmp/test-monitor-e2e-real-$$`, creates `.humanize/rlcr/<timestamp>/state.md`, creates `goal-tracker.md`, creates a fake cache tree under fake `HOME`/`XDG_CACHE_HOME`, writes a round log, writes a runner script that sources the real `scripts/humanize.sh`, then starts `_humanize_monitor_codex` in the background. After a short startup delay, it deletes `.humanize/rlcr`, waits up to 20 half-second intervals, and validates that the monitor exits cleanly. See `tests/test-monitor-e2e-real.sh:43-51`, `tests/test-monitor-e2e-real.sh:56-181`.

  The Zsh case mirrors the same state setup and deletion transition under `zsh`, guarded by `command -v zsh`; if Zsh is absent it reports a skip rather than failing. It creates its own timestamped session, fake cache path, Zsh runner, background process, deletion trigger, bounded wait, and post-run output assertions. See `tests/test-monitor-e2e-real.sh:233-371`.

- inputs_outputs_state: Inputs are the repository-local harness file, the production monitor script at `scripts/humanize.sh`, shell availability (`bash` always, `zsh` conditionally), a writable `/tmp`, basic Unix tools (`mkdir`, `rm`, `sed`, `grep`, `kill`, `sleep`, `pkill`, `chmod`, `cat`), and fake project/cache fixtures created during the test. The direct runner has no CLI arguments.

  The state transition under test is: valid temporary RLCR session exists, monitor starts and discovers it, `.humanize/rlcr` is removed while the monitor loop is running, production monitor detects deletion, cleanup executes, monitor returns success, harness records pass/fail counters. The production loop being specified checks `[[ ! -d "$loop_dir" ]]`, calls `_graceful_stop ".humanize/rlcr directory no longer exists"`, and returns 0. See `scripts/humanize.sh:838-844`.

  Outputs are human-readable PASS/FAIL lines, summary lines for `TESTS_PASSED` and `TESTS_FAILED`, captured monitor output files under the temp base, and the process exit code. The assigned split exits with 0 when no harness failures were recorded and 1 otherwise. See `tests/test-monitor-e2e-deletion.sh:15-21`.

- gates_or_invariants: The key invariant is that deletion of `.humanize/rlcr` during monitoring is not treated as a shell glob failure, terminal corruption, or test failure. The monitor must print a graceful stop message containing `Monitoring stopped:` and a deletion reason containing `directory no longer exists`; it must not emit `no matches found` or `bad pattern`; it must show cleanup via `Stopped monitoring`; and it must report `EXIT_CODE:0`. See `tests/test-monitor-e2e-real.sh:187-227`.

  Cross-shell compatibility is a gate. The test specifically asserts that the real monitor works under Bash and, when available, under Zsh without glob expansion errors. The production monitor enables Zsh `ksharrays` inside `_humanize_monitor_codex`, while the shared helper uses `find` rather than unmatched globs to locate timestamped session directories. See `scripts/humanize.sh:261-265`, `scripts/lib/monitor-common.sh:40-63`.

  Terminal restoration is a gate. The Bash deletion case verifies the cleanup message and also checks the source contains the scroll-region reset escape sequence via `grep -q 'printf "\\033\[r"' "$PROJECT_ROOT/scripts/humanize.sh"`. The production cleanup path calls `_restore_terminal`, and `_restore_terminal` resets the scroll region with `printf "\033[r"`. See `tests/test-monitor-e2e-real.sh:207-220`, `scripts/humanize.sh:736-762`, `scripts/humanize.sh:706-712`.

  Startup preconditions are also explicit: `_humanize_monitor_codex` requires `.humanize/rlcr` to exist at startup, requires at least one timestamp-named session directory, and checks terminal height before setup. The harness satisfies these by creating timestamp-like session directories and shimmed `tput` functions that return 80 columns and 24 lines. See `scripts/humanize.sh:272-277`, `scripts/humanize.sh:798-826`, `tests/test-monitor-e2e-real.sh:60-154`, `tests/test-monitor-e2e-real.sh:241-322`.

- dependencies_and_callers: The assigned file depends directly on `tests/test-monitor-e2e-real.sh` for function definitions and pass/fail counters. That harness depends on the production monitor in `scripts/humanize.sh`, which sources shared monitor utilities from `scripts/lib/monitor-common.sh` when available. See `tests/test-monitor-e2e-deletion.sh:4-5`, `tests/test-monitor-e2e-real.sh:144-149`, `scripts/humanize.sh:6-9`.

  The monitor implementation under test uses `monitor_find_latest_session`, `monitor_find_state_file`, and `monitor_get_file_size` from the shared monitor library through local wrapper functions. The deletion test most directly exercises latest-session discovery, state-file lookup, terminal setup/restoration, loop deletion detection, and cleanup. See `scripts/humanize.sh:279-380`, `scripts/humanize.sh:828-831`, `scripts/lib/monitor-common.sh:29-63`, `scripts/lib/monitor-common.sh:84-92`.

  The runner is included in the repository’s aggregate test list immediately before the SIGINT split. The sibling `tests/test-monitor-e2e-sigint.sh` sources the same harness but runs `monitor_test_bash_sigint` and `monitor_test_zsh_sigint`, confirming that this assigned file is the deletion-focused half of a split e2e monitor suite. See `tests/run-all-tests.sh:79-82`, `tests/test-monitor-e2e-sigint.sh:1-21`.

  There is also a manual companion script documenting the same deletion scenario for interactive verification: set up `.humanize/rlcr`, run `humanize monitor rlcr`, delete `.humanize`, and confirm clean stop, terminal restoration, and no glob errors. See `tests/manual-monitor-test.sh:5-14`, `tests/manual-monitor-test.sh:47-56`.

- edge_cases_or_failure_modes: Failure modes covered by this assigned split include monitor not exiting within the bounded wait after deletion, missing graceful-stop text, missing deletion reason, Bash/Zsh glob errors, missing cleanup message, missing terminal scroll reset in source, and nonzero monitor exit after graceful stop. See `tests/test-monitor-e2e-real.sh:167-227`, `tests/test-monitor-e2e-real.sh:335-370`.

  The Zsh deletion path is conditional. If `zsh` is not installed, the test prints `SKIP: zsh not available` and does not increment the failure counter. This means the split can pass without exercising Zsh on systems that lack it. See `tests/test-monitor-e2e-real.sh:238-240`.

  Timing sensitivity exists: both deletion scenarios sleep 2 seconds before removing `.humanize/rlcr`, then wait up to 10 seconds total for monitor exit. A very slow startup or a hung monitor can fail the test. The cleanup trap also kills lingering monitor processes matching the test temp identifier and removes the temp base at exit, which protects later runs but means diagnostics live only in captured output before cleanup. See `tests/test-monitor-e2e-real.sh:46-51`, `tests/test-monitor-e2e-real.sh:161-181`, `tests/test-monitor-e2e-real.sh:329-349`.

  The Bash runner accepts an `OUTPUT_FILE` argument but only uses shell redirection from the parent to capture output; this is harmless but redundant. See `tests/test-monitor-e2e-real.sh:111-115`, `tests/test-monitor-e2e-real.sh:156-159`.

- validation_or_tests: This file is itself the validation asset. It validates real production monitor behavior rather than a stub: the generated runner scripts source `scripts/humanize.sh` and call `_humanize_monitor_codex` directly. See `tests/test-monitor-e2e-real.sh:105-149`, `tests/test-monitor-e2e-real.sh:286-319`.

  The direct validation command for this item is `tests/test-monitor-e2e-deletion.sh`; as part of the full suite it is listed in `tests/run-all-tests.sh`. I inspected the file and its direct dependencies only; I did not execute the test because the assignment requested research notes only and the branch export is read-only. See `tests/test-monitor-e2e-deletion.sh:1-21`, `tests/run-all-tests.sh:79-82`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: one assigned item section present above
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`