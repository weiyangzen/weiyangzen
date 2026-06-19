# agent_087 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-087 `file` `tests/test-monitor-runtime.sh`
- cursor: `[_]`
- core_role:
  - Executable specification for RLCR monitor runtime shutdown behavior. It verifies that monitor cleanup is idempotent, terminal state is restored, `.humanize/rlcr` deletion causes a graceful stop instead of a crash, and bash/zsh signal handlers route termination through cleanup.
  - The file is not itself production algorithm code, but it encodes required behavior for `scripts/humanize.sh` monitor internals. It is part of the core behavioral contract because the monitor’s long-running loop must safely handle disappearing runtime state and user interrupts.
  - It is registered in the aggregate test suite at `tests/run-all-tests.sh:60-81`, where `test-monitor-runtime.sh` runs alongside monitor e2e deletion and SIGINT tests.

- algorithmic_behavior:
  - Test harness setup:
    - Computes `SCRIPT_DIR` and `PROJECT_ROOT` from the test file location at `tests/test-monitor-runtime.sh:14-15`.
    - Creates an isolated temp work directory `/tmp/test-monitor-runtime-$$`, enters it, and removes it on `EXIT` via `cleanup()` at `tests/test-monitor-runtime.sh:45-53`.
    - Tracks pass/fail counters with `pass()` and `fail()` helpers at `tests/test-monitor-runtime.sh:22-34`.
  - Test 1, graceful stop message and cleanup ordering:
    - Creates a fake `.humanize/rlcr/<timestamp>/state.md` at `tests/test-monitor-runtime.sh:61-62`.
    - Generates `test_graceful_stop.sh`, sources `scripts/humanize.sh`, then defines a minimal monitor environment plus stubbed `_restore_terminal`, `_cleanup`, and `_graceful_stop` at `tests/test-monitor-runtime.sh:65-106`.
    - Requires `_graceful_stop` to call `_cleanup`, `_cleanup` to call `_restore_terminal`, and output both `Monitoring stopped:` plus a user-facing directory deletion explanation at `tests/test-monitor-runtime.sh:111-134`.
    - Production counterpart: `_graceful_stop()` in `scripts/humanize.sh:766-777` calls `_cleanup` before printing the stop reason and cancellation/deletion hint.
  - Test 2, cleanup idempotence:
    - Generates a minimal `_cleanup` guarded by `cleanup_done` and invokes `_graceful_stop` twice plus `_cleanup` twice at `tests/test-monitor-runtime.sh:143-168`.
    - Pass condition is `FINAL_COUNT: 1` at `tests/test-monitor-runtime.sh:173-177`.
    - Production counterpart: `_cleanup()` returns immediately if `cleanup_done` is already true at `scripts/humanize.sh:738-742`; `_graceful_stop()` also checks the same guard at `scripts/humanize.sh:767-772`.
  - Test 3, main loop deletion detection:
    - Generates `check_loop_dir()` mirroring the production directory check: if `loop_dir` is missing, call `_graceful_stop ".humanize/rlcr directory no longer exists"` and return success at `tests/test-monitor-runtime.sh:186-230`.
    - Validates the loop continues while the directory exists, then stops after `rm -rf .humanize/rlcr` at `tests/test-monitor-runtime.sh:235-251`.
    - Production counterpart: `_humanize_monitor_codex()` sets `loop_dir=".humanize/rlcr"` at `scripts/humanize.sh:266`; it rejects startup with a friendly error when the directory is initially absent at `scripts/humanize.sh:272-277`; it checks deletion during the main loop at `scripts/humanize.sh:838-844`, during no-log polling at `scripts/humanize.sh:899-908`, and during incremental log following at `scripts/humanize.sh:1022-1031`.
  - Test 4, terminal restoration:
    - Sources `scripts/humanize.sh` and uses source inspection to assert `_restore_terminal()` exists, resets the scroll region with `printf "\033[r"`, and is called from `_cleanup` at `tests/test-monitor-runtime.sh:263-311`.
    - Production counterpart: `_restore_terminal()` resets the terminal scroll region and moves to the bottom at `scripts/humanize.sh:707-712`; `_cleanup()` invokes it at `scripts/humanize.sh:759`.
    - The setup path also matters: `_setup_terminal()` sets a constrained scroll region for split-view monitoring at `scripts/humanize.sh:651-659`; `_restore_terminal()` reverses that state.
  - Test 5, R1.2 compliance:
    - Source-inspects `_graceful_stop()` to ensure `_cleanup` appears within the function body at `tests/test-monitor-runtime.sh:313-324`.
    - This directly guards the behavior documented in production comments at `scripts/humanize.sh:764-772`.
  - Test 6, bash SIGINT:
    - Creates a standalone bash script that installs `trap '_cleanup' INT TERM`, self-sends `SIGINT`, waits up to ~1 second, and expects `CLEANUP_BY_SIGINT` at `tests/test-monitor-runtime.sh:326-381`.
    - Production counterpart: bash installs `trap '_cleanup' INT TERM` and `trap 'resize_needed=true' WINCH` at `scripts/humanize.sh:792-795`.
  - Test 7, signal handler source verification:
    - Greps `scripts/humanize.sh` for the bash trap and zsh `TRAPINT()`/`TRAPTERM()` definitions at `tests/test-monitor-runtime.sh:383-409`.
    - Production counterpart: zsh handlers call `_cleanup` and return signal-like statuses at `scripts/humanize.sh:787-791`.
  - Test 8, trap reset:
    - Greps near `_cleanup()` for `trap - INT TERM` at `tests/test-monitor-runtime.sh:411-423`.
    - Production counterpart: `_cleanup()` resets `INT`, `TERM`, and `WINCH` traps at `scripts/humanize.sh:744-747`.
  - Test 9, real zsh SIGINT:
    - If `zsh` is available, generates and runs a zsh script using `TRAPINT()`, self-sends `SIGINT`, and expects either `CLEANUP_BY_SIGINT_ZSH` or `ZSH_SIGINT_HANDLED` at `tests/test-monitor-runtime.sh:425-490`.
    - If `zsh` is unavailable, this subtest prints a skip line and does not increment failure count.
  - Summary and exit:
    - Prints pass/fail totals at `tests/test-monitor-runtime.sh:492-500`.
    - Exits `0` only when `TESTS_FAILED == 0`; otherwise exits `1` at `tests/test-monitor-runtime.sh:502-512`.

- inputs_outputs_state:
  - Inputs:
    - Repository production file: `scripts/humanize.sh`, sourced or grepped by subtests.
    - Test-created runtime tree: `.humanize/rlcr/2026-01-16_10-00-00/state.md`.
    - Shell availability: bash is required by the test shebang; zsh is optional for Test 9.
    - Process signals: generated scripts send `SIGINT` to themselves.
    - `$PROJECT_ROOT` and `$TEST_BASE` arguments passed into generated helper scripts.
  - Outputs:
    - Human-readable PASS/FAIL lines with ANSI color escapes.
    - Generated temporary helper scripts under `/tmp/test-monitor-runtime-$$`.
    - Process exit status `0` on all non-skipped checks passing, `1` if any failed check increments `TESTS_FAILED`.
    - Expected message fragments include `RESTORE_TERMINAL_CALLED`, `CLEANUP_CALLED`, `Monitoring stopped:`, `directory no longer exists`, `FINAL_COUNT: 1`, `STOPPED_AFTER_DELETE`, `CLEANUP_BY_SIGINT`, and zsh-specific signal markers.
  - State transitions modeled by the test:
    - `cleanup_done=false -> true` on first cleanup.
    - `monitor_running=true -> false` in cleanup.
    - loop directory state `exists -> deleted`, causing monitor state `continuing -> graceful stop`.
    - terminal state `split scroll region -> restored full scroll region`.
    - signal handler state `active traps -> cleanup invoked -> traps reset`.
    - pass/fail counters increment monotonically across subtests.

- gates_or_invariants:
  - Cleanup must be idempotent: repeated `_graceful_stop` or `_cleanup` calls cannot execute cleanup body more than once.
  - Graceful stop must call cleanup before printing final stop messages, preserving terminal restoration guarantees.
  - Deleting `.humanize/rlcr` during monitoring must be treated as a clean stop with exit `0`, not as an unhandled failure.
  - `_restore_terminal()` must reset the terminal scroll region using `printf "\033[r"`.
  - `_cleanup()` must call `_restore_terminal`.
  - Bash monitor mode must install `trap '_cleanup' INT TERM`.
  - Zsh monitor mode must define `TRAPINT()` and `TRAPTERM()`.
  - Cleanup must reset signal traps to avoid repeated or recursive cleanup.
  - Failure gate is centralized: any failed assertion increments `TESTS_FAILED`; final exit is nonzero if the count is nonzero.

- dependencies_and_callers:
  - Direct production dependency:
    - `scripts/humanize.sh`, especially `_humanize_monitor_codex()` at `scripts/humanize.sh:261`, terminal helpers at `scripts/humanize.sh:651-712`, cleanup and graceful stop at `scripts/humanize.sh:731-777`, signal setup at `scripts/humanize.sh:784-796`, and loop deletion checks at `scripts/humanize.sh:838-844`, `scripts/humanize.sh:899-908`, and `scripts/humanize.sh:1022-1031`.
  - Indirect production dependency:
    - `scripts/humanize.sh` sources monitor common helpers from `scripts/lib/monitor-common.sh` when present at `scripts/humanize.sh:9`; `_humanize_monitor_codex()` then wraps shared helpers such as `monitor_find_latest_session` and `monitor_get_file_size`.
  - Test-suite caller:
    - `tests/run-all-tests.sh` includes `test-monitor-runtime.sh` at `tests/run-all-tests.sh:80`.
  - External commands used by the test:
    - `mkdir`, `rm`, `chmod`, `grep`, `kill`, `wait`, `sleep`, `bash`, optional `zsh`.
  - Generated helper scripts:
    - `test_graceful_stop.sh`, `test_double_cleanup.sh`, `test_loop_detection.sh`, `test_terminal_restore.sh`, `test_sigint_bash.sh`, and optional `test_sigint_zsh.zsh`.

- edge_cases_or_failure_modes:
  - Source-inspection fragility:
    - Test 4 checks `grep -A30 "^    _cleanup()"` for `_restore_terminal` at `tests/test-monitor-runtime.sh:305-310`; formatting changes, indentation changes, or a longer cleanup body could cause false failures even if behavior remains correct.
    - Test 5 uses `grep -A5 "_graceful_stop()"` at `tests/test-monitor-runtime.sh:320`; if comments or guard logic push `_cleanup` beyond five lines, the test may fail despite correct behavior.
    - Test 8 uses `grep -A10 "_cleanup()"` at `tests/test-monitor-runtime.sh:419`; trap reset must remain near the function header to satisfy this check.
  - Test 4 contains a pipeline `grep -q '_restore_terminal' "$2/scripts/humanize.sh" | grep -q '_cleanup'` at `tests/test-monitor-runtime.sh:282`; because the first `grep -q` emits no output, that nested block is effectively not useful. The later direct check at `tests/test-monitor-runtime.sh:307-311` is the real validation.
  - Several tests reimplement simplified versions of `_cleanup()` and `_graceful_stop()` rather than invoking the nested production functions directly. This validates the intended algorithmic pattern and source shape, but does not fully exercise the real interactive monitor path.
  - Optional zsh coverage is environment-dependent. Missing `zsh` produces `SKIP: zsh not available for runtime test` at `tests/test-monitor-runtime.sh:488-490` without failing the suite.
  - Signal timing is probabilistic but bounded: SIGINT tests sleep in 0.1 second increments and wait up to about 1 second. Slow or unusual process scheduling could produce intermittent failure.
  - The test writes to `/tmp/test-monitor-runtime-$$`; concurrent runs are mostly isolated by PID, but stale temp directories from PID reuse would be removed by the `EXIT` trap only for the current run.
  - Because `set -euo pipefail` is active at `tests/test-monitor-runtime.sh:12`, unexpected nonzero statuses outside guarded conditionals can abort the whole test before the summary.
  - Production monitor terminal functions use `tput` and terminal dimensions; this test mostly avoids true interactive terminal assertions, so terminal-specific failures may require e2e tests for full coverage.

- validation_or_tests:
  - This assigned file is itself a validation script. It verifies monitor runtime behavior through a mix of:
    - Generated miniature runtime scripts for cleanup, graceful stop, deletion detection, and signal handling.
    - Source inspections against `scripts/humanize.sh`.
    - Optional real zsh signal handling.
  - It is part of the full suite through `tests/run-all-tests.sh:80`.
  - I did not execute the test because the worker instruction says “Do not modify files. Produce research notes only,” and this script creates temporary files and directories under `/tmp`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 item section present; the sole assigned item_id appears exactly once as an evidence heading`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`