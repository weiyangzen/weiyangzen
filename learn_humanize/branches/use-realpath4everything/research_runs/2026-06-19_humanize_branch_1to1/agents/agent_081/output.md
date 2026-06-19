# agent_081 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-081 `file` `tests/test-helpers.sh`
- cursor: `[_]`
- core_role:
  - `tests/test-helpers.sh` is the shared Bash test harness for many top-level and robustness test scripts. It is not product runtime code, but it is executable specification support: it standardizes pass/fail/skip accounting, final exit status behavior through summary return codes, temporary test workspace setup, and mock git repository setup.
  - The file is explicitly intended to be sourced from both `tests/` and `tests/robustness/`, documented at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:5) and [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:6).
  - Direct consumers include path-validation robustness tests at `tests/robustness/test-path-validation-robustness.sh:14`, model-router tests at `tests/test-model-router.sh:7`, agent-teams tests at `tests/test-agent-teams.sh:18`, and many other shell tests found by reference scan.

- algorithmic_behavior:
  - Defines immutable ANSI color constants for harness output at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:13), [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:14), [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:15), and [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:16).
  - Initializes global counters `TESTS_PASSED`, `TESTS_FAILED`, and `TESTS_SKIPPED` to zero at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:22).
  - `pass()` emits a colored `PASS` line and increments `TESTS_PASSED` by one at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:30).
  - `fail()` emits a colored `FAIL` line, conditionally prints expected and actual values based on argument count, and increments `TESTS_FAILED` at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:35).
  - `skip()` emits a colored `SKIP` line, conditionally prints a reason, and increments `TESTS_SKIPPED` at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:46).
  - `print_test_summary()` prints a title, the three counters, suppresses the skipped line when skipped count is zero, and returns `0` only when `TESTS_FAILED == 0`; otherwise it returns `1` at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:58).
  - `setup_test_dir()` creates a fresh temp directory with `mktemp -d`, stores it in global `TEST_DIR`, and installs an `EXIT` trap to remove it at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:86).
  - `init_test_git_repo()` creates a directory, changes into it, initializes a quiet git repo, configures local test identity and disables commit signing, commits `file.txt`, then returns to the previous directory at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:93).

- inputs_outputs_state:
  - Inputs:
    - `pass`, `fail`, and `skip` consume human-readable assertion descriptions; `fail` optionally consumes expected and actual strings, and `skip` optionally consumes a reason.
    - `print_test_summary` consumes an optional title, defaulting to `Test Summary` at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:59).
    - `setup_test_dir` consumes no arguments but depends on `mktemp`.
    - `init_test_git_repo` consumes one directory path at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:94).
  - Outputs:
    - Assertion functions write colored status lines to stdout via `echo -e`.
    - `print_test_summary` writes aggregate counts and returns shell success/failure as the test suite’s final gate.
    - `setup_test_dir` creates filesystem state outside the repository and exports the mutable shell variable `TEST_DIR`.
    - `init_test_git_repo` creates a git repository with one committed file.
  - State transitions:
    - `TESTS_PASSED`, `TESTS_FAILED`, and `TESTS_SKIPPED` transition monotonically upward by one per helper call.
    - `TEST_DIR` is overwritten on every `setup_test_dir` call. Several consumers call it repeatedly in one script, such as `tests/test-agent-teams.sh:35`, `tests/test-agent-teams.sh:85`, and later sections; because each call replaces the global variable and resets the `EXIT` trap, only the latest temp directory is guaranteed to be removed by this helper’s active trap.
    - `init_test_git_repo` temporarily mutates the process working directory through `cd "$dir"` and restores it via `cd - > /dev/null` at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:104).

- gates_or_invariants:
  - Summary success is gated solely on `TESTS_FAILED == 0`; skipped tests do not fail the suite, as implemented at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:71).
  - Skipped count is displayed only when greater than zero at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:66).
  - `fail()` only prints `Expected:` when at least two arguments are supplied and `Got:` when at least three are supplied at [tests/test-helpers.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-helpers.sh:37).
  - The helper assumes it is sourced, not executed as a standalone test runner; there is no main section or automatic summary.
  - The git fixture invariant is a clean repo with user identity configured, GPG signing disabled, one tracked `file.txt`, and an initial commit.

- dependencies_and_callers:
  - Shell/runtime dependencies: Bash, `echo`, `mktemp`, `rm`, `mkdir`, `cd`, and `git`.
  - `init_test_git_repo` depends on `git init`, `git config`, `git add`, and `git commit`; this makes it a setup primitive for tests that need production code to see a real git repository.
  - Representative callers:
    - `tests/robustness/test-path-validation-robustness.sh` sources the helper at line 14 and uses `setup_test_dir` at line 16 before constructing temp plans and invoking `scripts/setup-rlcr-loop.sh`; this ties the helper to the branch’s realpath/path validation executable specifications.
    - `tests/test-agent-teams.sh` sources it at line 18 and uses both `setup_test_dir` and `init_test_git_repo` at lines 35-36 to build isolated projects for setup-script behavior.
    - `tests/test-ask-codex.sh` sources it at line 15, uses `setup_test_dir` at line 29, and `init_test_git_repo` at line 33.
    - `tests/test-model-router.sh` sources it at line 7 and uses `pass`/`fail` for routing assertions, with `setup_test_dir` later for PATH-isolated binary checks.
  - Several test scripts define their own local harness instead of sourcing this file, so this helper is shared but not universal.

- edge_cases_or_failure_modes:
  - Trap quoting risk: `trap "rm -rf $TEST_DIR" EXIT` expands `TEST_DIR` at trap-registration time and does not quote the path inside the trap command. `mktemp -d` normally produces safe paths, but spaces or shell metacharacters in the temp base path could be problematic.
  - Repeated `setup_test_dir` calls overwrite the previous `EXIT` trap, so earlier temp directories are not cleaned by this helper after a later call.
  - `setup_test_dir` does not check `mktemp -d` failure explicitly. Under `set -e`, callers usually abort; without `set -e`, `TEST_DIR` could be empty or stale.
  - `init_test_git_repo` changes the caller’s working directory and relies on `cd -`; with `set -e`, failures abort before restoration, so callers can be left in an unexpected directory on partial failure.
  - `init_test_git_repo` accepts any path string and does not validate emptiness, symlink status, or containment. It is a test fixture helper, so path safety is delegated to callers.
  - The output uses `echo -e`, whose behavior can vary across shells, but the shebang and consumers use Bash.
  - No assertion helper returns non-zero immediately on `fail`; the harness accumulates failures and relies on `print_test_summary` as the exit gate.

- validation_or_tests:
  - Direct inspection covered the full 105-line, 2602-byte file.
  - `bash -n tests/test-helpers.sh` completed successfully, giving syntax validation without executing mutating fixture setup.
  - Reference scan confirmed broad use across top-level and robustness tests, including `test-path-validation-robustness.sh`, `test-agent-teams.sh`, `test-session-id.sh`, `test-stop-hook-bg-allow.sh`, `test-setup-scripts-robustness.sh`, and others.
  - I did not execute the test suite because the assigned task is research-only and the branch export is read-only; executing consumers would create temp repos/files and, in this sandbox, git metadata probing already hit read-only temp/cache restrictions.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 item section present above
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`