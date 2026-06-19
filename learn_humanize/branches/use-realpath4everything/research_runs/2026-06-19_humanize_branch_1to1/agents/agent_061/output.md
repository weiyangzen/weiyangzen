# agent_061 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-061 `file` `tests/manual-monitor-test.sh`
- cursor: `[_]`
- core_role:
  - `tests/manual-monitor-test.sh` is a manual executable specification for RLCR monitor deletion behavior. It does not implement the monitor algorithm itself; it creates a minimal `.humanize/rlcr/<timestamp>/` fixture, instructs an operator to run `humanize monitor rlcr`, deletes `.humanize`, and defines the observable success criteria for graceful monitor shutdown.
  - The behavior under test maps to `scripts/humanize.sh` monitor entry dispatch: `humanize monitor rlcr` calls `_humanize_monitor_codex` (`scripts/humanize.sh:1195-1202`).
  - It specifically specifies the expected user-visible behavior when the monitored `.humanize/rlcr` directory disappears while the monitor is running: a clean message, terminal restoration, and no shell glob errors (`tests/manual-monitor-test.sh:5-7`, `tests/manual-monitor-test.sh:51-54`).

- algorithmic_behavior:
  - Initialization:
    - The script resolves its own directory and project root with `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`, then `PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"`, and runs from the project root (`tests/manual-monitor-test.sh:19-21`).
    - This makes all fixture writes relative to the branch export root, not the caller’s current directory after startup.
  - Command dispatcher:
    - Uses a single `case "${1:-}"` over `setup`, `delete`, `cleanup`, and default usage/error (`tests/manual-monitor-test.sh:23-72`).
    - `set -euo pipefail` makes unset variables, failed commands, and failed pipeline components fatal (`tests/manual-monitor-test.sh:17`).
  - `setup` behavior:
    - Creates `.humanize/rlcr/2026-01-16_99-99-99/` (`tests/manual-monitor-test.sh:24-26`).
    - Writes a minimal `state.md` containing `current_round`, `max_iterations`, Codex model/effort, timestamp, and `plan_file` (`tests/manual-monitor-test.sh:27-32`).
    - Writes a minimal `goal-tracker.md` with an immutable goal and one acceptance criterion (`tests/manual-monitor-test.sh:33-38`).
    - Prints the next manual step: run `source scripts/humanize.sh && humanize monitor rlcr` in another terminal (`tests/manual-monitor-test.sh:43-45`).
  - `delete` behavior:
    - Removes the whole `.humanize` tree with `rm -rf .humanize` (`tests/manual-monitor-test.sh:47-50`).
    - Prints the expected monitor observations: exact graceful-stop reason, restored terminal state, and absence of `zsh`/`bash` glob errors (`tests/manual-monitor-test.sh:51-54`).
  - `cleanup` behavior:
    - Also removes `.humanize` with `rm -rf .humanize` and prints completion (`tests/manual-monitor-test.sh:58-61`).
  - Usage/error behavior:
    - Any missing or unknown argument prints `Usage: $0 {setup|delete|cleanup}` and exits `1` (`tests/manual-monitor-test.sh:63-70`).

- inputs_outputs_state:
  - Inputs:
    - Positional command: one of `setup`, `delete`, `cleanup`; missing/unknown input is invalid (`tests/manual-monitor-test.sh:23`, `tests/manual-monitor-test.sh:63-70`).
    - Implicit filesystem input: script must be executed from, or able to resolve into, the repository tree containing `tests/` (`tests/manual-monitor-test.sh:19-21`).
    - Manual external input: a second terminal must run `source scripts/humanize.sh && humanize monitor rlcr` after setup (`tests/manual-monitor-test.sh:10-13`, `tests/manual-monitor-test.sh:43-45`).
  - Outputs:
    - `setup` writes two files:
      - `.humanize/rlcr/2026-01-16_99-99-99/state.md`
      - `.humanize/rlcr/2026-01-16_99-99-99/goal-tracker.md`
    - `delete` and `cleanup` remove `.humanize`.
    - All modes write human-readable instructions/status to stdout.
  - State transitions:
    - No fixture -> active synthetic RLCR session:
      - `setup` creates `.humanize/rlcr/2026-01-16_99-99-99/` plus `state.md` and `goal-tracker.md`.
    - Active synthetic session -> missing monitored tree:
      - `delete` removes `.humanize`, which should make the running monitor see `.humanize/rlcr` disappear.
    - Any leftover fixture -> clean:
      - `cleanup` removes `.humanize`.
  - Production monitor transition being specified:
    - `_humanize_monitor_codex` starts by requiring `.humanize/rlcr` to exist (`scripts/humanize.sh:266-277`).
    - During its main monitor loops, it repeatedly checks for missing `loop_dir` and calls `_graceful_stop ".humanize/rlcr directory no longer exists"` then returns `0` (`scripts/humanize.sh:838-844`, `scripts/humanize.sh:899-908`, `scripts/humanize.sh:1022-1030`).
    - `_graceful_stop` delegates to `_cleanup`, then prints `Monitoring stopped: <reason>` (`scripts/humanize.sh:764-777`).
    - `_cleanup` sets `monitor_running=false`, resets traps, kills tail process if present, restores terminal, and prints `Stopped monitoring.` (`scripts/humanize.sh:736-762`).

- gates_or_invariants:
  - The script only accepts the three explicit subcommands; any other invocation exits nonzero (`tests/manual-monitor-test.sh:63-70`).
  - The fixture session name uses the monitor’s timestamp-shaped session directory convention: `YYYY-MM-DD_HH-MM-SS`, here `2026-01-16_99-99-99` (`tests/manual-monitor-test.sh:26`). The monitor helper selects timestamp-shaped directories and ignores nonmatching children (`scripts/lib/monitor-common.sh:37-63`).
  - The fixture includes `state.md`, which monitor state detection treats as an active state file (`scripts/lib/monitor-common.sh:147-170`).
  - The fixture includes `goal-tracker.md`, required by monitor status rendering and mirrored by automated e2e tests (`tests/manual-monitor-test.sh:33-38`; automated equivalent in `tests/test-monitor-e2e-real.sh:80-93`).
  - The expected graceful stop reason is pinned as `.humanize/rlcr directory no longer exists` (`tests/manual-monitor-test.sh:52`; production checks at `scripts/humanize.sh:841-843`, `scripts/humanize.sh:905-907`, `scripts/humanize.sh:1027-1030`).
  - Terminal restoration invariant:
    - `_restore_terminal` resets the scroll region with `printf "\033[r"` and moves the cursor to the bottom (`scripts/humanize.sh:706-712`).
    - `_cleanup` must call `_restore_terminal` before printing the stopped message (`scripts/humanize.sh:759-761`).
  - Shell safety invariant:
    - The manual expected output says no `zsh`/`bash` `no matches found` errors should appear (`tests/manual-monitor-test.sh:54`).
    - The helper implementation uses `find` instead of unmatched globs for session enumeration to avoid zsh glob failures (`scripts/lib/monitor-common.sh:49-60`).

- dependencies_and_callers:
  - Direct runtime dependencies:
    - `bash`, `mkdir`, `rm`, `cd`, `dirname`, `pwd`, `echo`.
    - The script is executable Bourne-Again shell text, 2535 bytes.
  - Manual caller:
    - Operator runs `./tests/manual-monitor-test.sh setup`, then in another terminal runs `source scripts/humanize.sh && humanize monitor rlcr`, then runs `./tests/manual-monitor-test.sh delete`, then optionally `cleanup` (`tests/manual-monitor-test.sh:9-15`).
  - Production behavior referenced:
    - `scripts/humanize.sh` provides `humanize()` dispatch and `_humanize_monitor_codex` (`scripts/humanize.sh:261-277`, `scripts/humanize.sh:1195-1202`).
    - `scripts/lib/monitor-common.sh` provides session and state helper behavior used by the monitor, including `monitor_find_latest_session` and `monitor_find_state_file` (`scripts/lib/monitor-common.sh:37-63`, `scripts/lib/monitor-common.sh:147-192`).
  - Automated test siblings covering the same specification:
    - `tests/test-monitor-e2e-deletion.sh` runs deletion tests by sourcing `tests/test-monitor-e2e-real.sh` and invoking bash/zsh deletion cases (`tests/test-monitor-e2e-deletion.sh:1-13`).
    - `tests/test-monitor-e2e-real.sh` constructs a real project fixture, runs the real `_humanize_monitor_codex`, deletes `.humanize/rlcr`, and asserts graceful message, deletion reason, no glob errors, cleanup message, scroll reset, and exit code `0` (`tests/test-monitor-e2e-real.sh:54-228`).
    - `tests/test-monitor-runtime.sh` directly verifies graceful stop calls cleanup/restore and prints the stop message (`tests/test-monitor-runtime.sh:56-125`) and verifies terminal restore source structure (`tests/test-monitor-runtime.sh:254-313`).
    - `tests/test-zsh-monitor-safety.sh` verifies `find`-based session lookup avoids zsh unmatched-glob failures for empty/dotfile-only `.humanize/rlcr` directories (`tests/test-zsh-monitor-safety.sh:80-150`).
  - Test runner status:
    - The manual script itself is not listed in `tests/run-all-tests.sh`; automated equivalents are listed: `test-zsh-monitor-safety.sh`, `test-monitor-runtime.sh`, and `test-monitor-e2e-deletion.sh` (`tests/run-all-tests.sh:79-82`).

- edge_cases_or_failure_modes:
  - Running without a valid command exits `1` after usage output (`tests/manual-monitor-test.sh:63-70`).
  - `setup` overwrites the synthetic fixture files if rerun, because it uses `>` redirection for `state.md` and `goal-tracker.md` (`tests/manual-monitor-test.sh:27-38`).
  - `delete` and `cleanup` are destructive to the whole `.humanize` tree, not just the synthetic timestamp directory (`tests/manual-monitor-test.sh:48-60`). This is intentional for the deletion scenario but unsafe around real active `.humanize` state.
  - The manual fixture does not create a Codex log under `$HOME/.cache/humanize/...`; production monitor handles no-log state by displaying a waiting/no-log message and continuing to poll (`scripts/humanize.sh:883-908`). Therefore the manual test primarily exercises deletion while waiting or monitoring, not log-follow correctness.
  - The synthetic timestamp has invalid clock fields `99-99-99`, but the monitor’s session-name gate only checks numeric shape, not clock validity (`scripts/lib/monitor-common.sh:54-60`). This is acceptable for fixture selection.
  - If the monitor is started before `setup`, `_humanize_monitor_codex` returns an error because `.humanize/rlcr` is missing (`scripts/humanize.sh:272-277`).
  - If `delete` is run before the second terminal starts monitoring, it will still remove `.humanize`, but there is no running monitor to observe graceful shutdown.
  - Because `set -euo pipefail` is active, failures in `cd`, `mkdir`, or `rm` abort the script (`tests/manual-monitor-test.sh:17-21`, `tests/manual-monitor-test.sh:26`, `tests/manual-monitor-test.sh:49-60`).
  - No realpath/canonical-path behavior is directly asserted in this manual script beyond resolving the script’s parent root with `cd ... && pwd`; the script is mainly a monitor lifecycle regression harness.

- validation_or_tests:
  - Manual validation defined by the file:
    - `./tests/manual-monitor-test.sh setup`
    - In a second terminal: `source scripts/humanize.sh && humanize monitor rlcr`
    - `./tests/manual-monitor-test.sh delete`
    - Expected observations: `Monitoring stopped: .humanize/rlcr directory no longer exists`, terminal scroll/cursor restored, and no `no matches found` errors (`tests/manual-monitor-test.sh:9-15`, `tests/manual-monitor-test.sh:51-56`).
  - Automated validation equivalents:
    - `tests/test-monitor-e2e-deletion.sh` covers real deletion behavior via bash and zsh test functions (`tests/test-monitor-e2e-deletion.sh:12-13`).
    - `tests/test-monitor-e2e-real.sh` validates monitor exits after deletion, emits graceful stop text, includes deletion reason, avoids glob errors, prints cleanup message, contains scroll-region reset in source, and returns exit code `0` (`tests/test-monitor-e2e-real.sh:164-227`).
    - `tests/test-monitor-runtime.sh` validates `_graceful_stop -> _cleanup -> _restore_terminal` and terminal restore implementation (`tests/test-monitor-runtime.sh:56-125`, `tests/test-monitor-runtime.sh:254-313`).
    - `tests/test-zsh-monitor-safety.sh` validates empty and dotfile-only loop directories do not trigger zsh glob errors (`tests/test-zsh-monitor-safety.sh:80-150`).
  - I did not run the manual scenario because it intentionally mutates `.humanize` and requires a second interactive terminal. I also did not run automated tests because this worker request is research-only and the branch export is read-only.
  - Repository status validation was attempted with `git status --short && git rev-parse HEAD`, but this branch export has no `.git` directory and macOS toolchain cache creation was blocked by the read-only sandbox, so no git status result was available. File inspection was done directly from the provided path.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `USE_REALPATH4EVERYTHING-HZ-061`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`