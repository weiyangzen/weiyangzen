# agent_062 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-062 `file` `tests/test-pr-loop-lib.sh`
- cursor: `[_]`
- core_role:
  - `tests/test-pr-loop-lib.sh` is the shared executable fixture library for the PR-loop test suite. It is not production PR-loop logic, but it is core test infrastructure because it normalizes external dependencies (`gh`, `codex`), initializes isolated test state, and provides the summary gate used by the main PR-loop test runner.
  - The library is sourced by `tests/test-pr-loop.sh:18-20`; that runner then calls `init_pr_loop_test_env` at `tests/test-pr-loop.sh:26`, sources the script/hook/stophook modules at `tests/test-pr-loop.sh:32-34`, runs them at `tests/test-pr-loop.sh:41-47`, and exits through this library’s `print_test_summary` at `tests/test-pr-loop.sh:53`.

- algorithmic_behavior:
  - Single-load guard: `TEST_PR_LOOP_LIB_LOADED` prevents duplicate function definitions on repeated sourcing (`tests/test-pr-loop-lib.sh:11-13`).
  - Path derivation: defaults `SCRIPT_DIR` from `${BASH_SOURCE[0]}` and `PROJECT_ROOT` from the parent directory when not already provided (`tests/test-pr-loop-lib.sh:15-16`).
  - Helper import gate: sources `tests/test-helpers.sh` only if `setup_test_dir` is not already declared (`tests/test-pr-loop-lib.sh:19-21`), avoiding redundant helper loading when the main runner has already sourced it.
  - Mock GitHub CLI generator: `create_mock_gh` writes an executable `gh` script into a caller-provided mock directory (`tests/test-pr-loop-lib.sh:28-91`). Its behavior is command-dispatch based:
    - `gh auth status` always succeeds with “Logged in to github.com” (`tests/test-pr-loop-lib.sh:36-41`).
    - `gh repo view --json owner` and `--json name` return fixed JSON fragments for `testowner` and `testrepo` (`tests/test-pr-loop-lib.sh:43-51`).
    - `gh pr view` returns a fixed base repository, fixed commit timestamp, fixed PR number JSON, or fixed `OPEN` state depending on argument substrings/positions (`tests/test-pr-loop-lib.sh:53-73`).
    - `gh api user` returns `testuser`; other API calls return `[]` (`tests/test-pr-loop-lib.sh:75-83`).
    - Unknown `gh` commands fail closed with stderr and exit `1` (`tests/test-pr-loop-lib.sh:87-88`).
  - Mock Codex generator: `create_mock_codex` writes an executable `codex` script that prints “Mock codex output” and exits `0` (`tests/test-pr-loop-lib.sh:94-103`).
  - Test environment initialization: `init_pr_loop_test_env` creates a temp test directory, creates `$TEST_DIR/mock_bin`, prepends it to `PATH`, installs mock `gh`/`codex`, and exports `MOCK_BIN_DIR` (`tests/test-pr-loop-lib.sh:111-124`).
  - Result gate: `print_test_summary` prints PR-loop pass/fail counts and returns nonzero if `TESTS_FAILED > 0` (`tests/test-pr-loop-lib.sh:131-147`).

- inputs_outputs_state:
  - Inputs:
    - Shell environment variables: optional `TEST_PR_LOOP_LIB_LOADED`, `SCRIPT_DIR`, `PROJECT_ROOT`, and inherited `PATH`.
    - Test counters from `tests/test-helpers.sh`: `TESTS_PASSED`, `TESTS_FAILED`; the helper initializes them at `tests/test-helpers.sh:22-24`.
    - Function availability: `setup_test_dir` controls whether helper sourcing is needed (`tests/test-pr-loop-lib.sh:19`).
    - Function arguments: `create_mock_gh "$mock_dir"` and `create_mock_codex "$mock_dir"` require a target directory path.
  - Outputs:
    - Defines shell functions for the PR-loop test modules: `create_mock_gh`, `create_mock_codex`, `init_pr_loop_test_env`, `print_test_summary`.
    - Creates temp filesystem state under `$TEST_DIR`, specifically `$TEST_DIR/mock_bin/gh` and `$TEST_DIR/mock_bin/codex` (`tests/test-pr-loop-lib.sh:115-121`).
    - Mutates process environment by prepending mock binaries to `PATH` and exporting `MOCK_BIN_DIR` (`tests/test-pr-loop-lib.sh:117-123`).
    - Emits stdout/stderr through mocks and summary printing.
  - State transitions:
    - Library state: unloaded -> loaded via `TEST_PR_LOOP_LIB_LOADED=1`.
    - Test runtime state: no isolated test dir -> temp `TEST_DIR` with cleanup trap via `setup_test_dir` in `tests/test-helpers.sh:86-89`.
    - Dependency state: real `gh`/`codex` resolution -> mock-first resolution through `PATH="$MOCK_BIN_DIR:$PATH"` (`tests/test-pr-loop-lib.sh:117`).
    - Test outcome state: accumulating `TESTS_PASSED`/`TESTS_FAILED` through helper `pass`/`fail` functions (`tests/test-helpers.sh:30-44`) -> suite-level return status in `print_test_summary`.

- gates_or_invariants:
  - The file assumes it is sourced, not executed directly; its definitions are inside the load guard block (`tests/test-pr-loop-lib.sh:11-147`).
  - Mock installation invariant: `init_pr_loop_test_env` must run before tests that expect `gh` and `codex` to be present in `PATH`.
  - External-dependency invariant: tests relying on this fixture see an authenticated GitHub CLI, an available Codex CLI, PR state `OPEN`, base repo `testowner/testrepo`, commit timestamp `2026-01-18T12:00:00Z`, and empty API comment/review arrays unless a module overrides the mock.
  - Failure invariant: unknown `gh` invocations fail with exit `1`, making unsupported API shapes visible rather than silently succeeding (`tests/test-pr-loop-lib.sh:87-88`).
  - Summary invariant: any positive `TESTS_FAILED` count makes the PR-loop suite fail (`tests/test-pr-loop-lib.sh:140-146`).
  - The summary implementation intentionally overrides the generic helper summary sourced from `tests/test-helpers.sh:58-78`; this PR-loop-specific version prints a fixed “PR Loop Tests” heading and does not include skipped counts.

- dependencies_and_callers:
  - Direct dependency: `tests/test-helpers.sh`, specifically `setup_test_dir`, `pass`, `fail`, and shared counters (`tests/test-pr-loop-lib.sh:19-21`; `tests/test-helpers.sh:22-44`, `tests/test-helpers.sh:86-89`).
  - Main caller: `tests/test-pr-loop.sh`, which sources the library, initializes the environment, runs script/hook/stophook modules, and calls the summary (`tests/test-pr-loop.sh:18-53`).
  - Downstream test modules:
    - `tests/test-pr-loop-scripts.sh` validates `setup-pr-loop.sh`, `cancel-pr-loop.sh`, `fetch-pr-comments.sh`, and `poll-pr-reviews.sh`; its `run_script_tests` dispatches all script groups at `tests/test-pr-loop-scripts.sh:405-410`.
    - `tests/test-pr-loop-hooks.sh` and `tests/test-pr-loop-stophook.sh` contain broader hook and stop-hook tests; some define more specialized mocks, which means this shared mock is the baseline rather than the only fixture.
  - Production surfaces represented by the mocks:
    - `scripts/setup-pr-loop.sh` requires `gh auth status` and `codex` availability (`scripts/setup-pr-loop.sh:263-277`), resolves PR/repo metadata through `gh repo view` and `gh pr view` (`scripts/setup-pr-loop.sh:295-354`).
    - `scripts/fetch-pr-comments.sh` resolves the base repo and fetches issue comments, PR review comments, and PR reviews through `gh api` (`scripts/fetch-pr-comments.sh:130-219`).
    - `scripts/poll-pr-reviews.sh` resolves the base repo, maps bot names, then polls/fetches comments via `gh api` (`scripts/poll-pr-reviews.sh:126-245`).

- edge_cases_or_failure_modes:
  - The mock `gh` is deliberately minimal and does not fully emulate `gh -q`/`--jq` behavior. For example, `gh pr view --json number -q .number` would return `{"number": 123}` instead of scalar `123` (`tests/test-pr-loop-lib.sh:65-67`), while production code often expects scalar output.
  - Argument-order sensitivity: production calls such as `gh pr view --repo "$CURRENT_REPO" --json number -q .number` (`scripts/setup-pr-loop.sh:310`) do not match the mock’s positional `$3 == "--json" && $4 == "number"` check, so the shared mock may exit `0` with empty output for that shape.
  - `gh repo view --json owner,name -q ...` in production (`scripts/setup-pr-loop.sh:296-301`, `scripts/fetch-pr-comments.sh:131`) is broader than the mock’s separate `owner`/`name` cases (`tests/test-pr-loop-lib.sh:45-49`), so this fixture is better suited for argument/guard tests than full GitHub metadata integration.
  - `gh repo view --json parent` is not implemented; fork-parent behavior requires specialized mocks elsewhere.
  - API calls other than `gh api user` always return `[]`, so comment/review algorithms see an empty GitHub surface unless tests install richer mocks.
  - Repeated `init_pr_loop_test_env` calls would prepend additional mock dirs to `PATH` and replace temp cleanup behavior through `setup_test_dir`; the main runner calls it once.
  - If `TEST_PR_LOOP_LIB_LOADED` is already set in the environment before sourcing, none of the functions are defined. That is correct for re-source idempotence but brittle if the variable leaks from an outer shell.

- validation_or_tests:
  - The assigned file is itself part of the executable PR-loop specification: it supplies fixtures consumed by the main suite in `tests/test-pr-loop.sh`.
  - Direct syntax validation performed during research: `bash -n tests/test-pr-loop-lib.sh` returned exit `0`.
  - A follow-up metadata probe using `git ls-files -s tests/test-pr-loop-lib.sh` was blocked by the read-only/macOS toolchain environment because `git` attempted to create an `xcrun` cache file under `/tmp`; this did not affect the shell syntax result or file inspection.
  - The broader suite’s validation behavior flows through `TESTS_FAILED`: helper `fail` increments the counter (`tests/test-helpers.sh:35-44`), and this library’s `print_test_summary` returns `1` when failures exist (`tests/test-pr-loop-lib.sh:140-146`).

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 Item Evidence heading
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`