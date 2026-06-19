# agent_067 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-067 `file` `tests/test-state-exit-naming.sh`
- cursor: `[_]`
- core_role:
  - Executable specification for RLCR loop terminal-state naming and active-loop discovery.
  - It verifies that an active RLCR loop is represented only by `state.md` under `.humanize/rlcr/<timestamp>/`, while terminal state snapshots are renamed to reason-prefixed files such as `complete-state.md`, `cancel-state.md`, `maxiter-state.md`, `stop-state.md`, and `unexpected-state.md`.
  - It also specifies that the new loop storage root is `.humanize/rlcr`, not legacy `.humanize-loop.local`.

- algorithmic_behavior:
  - Initializes an isolated temporary git project, commits an initial file, and creates a synthetic loop directory at `.humanize/rlcr/2024-01-01_12-00-00` for test fixtures, at `tests/test-state-exit-naming.sh:31-49`.
  - Sources `hooks/lib/loop-common.sh` to test shared algorithm functions directly, especially `find_active_loop`, `end_loop`, and `is_in_humanize_loop_dir`, at `tests/test-state-exit-naming.sh:64-69`.
  - Active-loop detection behavior:
    - A directory containing only `complete-state.md` must not be active, at `tests/test-state-exit-naming.sh:51-74`.
    - A directory containing `state.md` must be active, at `tests/test-state-exit-naming.sh:76-95`.
    - Directories containing only terminal files `cancel-state.md`, `unexpected-state.md`, `maxiter-state.md`, or `stop-state.md` must not be active, at `tests/test-state-exit-naming.sh:97-159`.
    - A newer timestamp directory containing `state.md` takes precedence over an older directory, at `tests/test-state-exit-naming.sh:161-180`.
  - Loop-ending behavior:
    - `end_loop` must reject an invalid reason and emit an invalid-reason error, at `tests/test-state-exit-naming.sh:186-204`.
    - For each valid reason `complete`, `cancel`, `maxiter`, `stop`, and `unexpected`, `end_loop` must rename `state.md` to `<reason>-state.md`, at `tests/test-state-exit-naming.sh:206-230`.
    - Missing `state.md` must be a graceful failure with a not-found warning and nonzero status, at `tests/test-state-exit-naming.sh:232-243`.
  - Path-root behavior:
    - `is_in_humanize_loop_dir` must return true for `.humanize/rlcr/.../state.md`, at `tests/test-state-exit-naming.sh:249-256`.
    - It must return false for legacy `.humanize-loop.local/.../state.md`, at `tests/test-state-exit-naming.sh:258-265`.
    - `find_active_loop` is deliberately invoked only with the new base path `.humanize/rlcr`, so a legacy loop with `state.md` is ignored, at `tests/test-state-exit-naming.sh:267-291`.

- inputs_outputs_state:
  - Inputs:
    - Synthetic loop directories under `$TEST_DIR/.humanize/rlcr`.
    - Synthetic state frontmatter files created inline with here-documents.
    - `CLAUDE_PROJECT_DIR="$TEST_DIR"` exported before sourcing loop helpers, at `tests/test-state-exit-naming.sh:64`.
    - Reason strings passed to `end_loop`: valid reasons and `invalid_reason`.
    - Path strings passed to `is_in_humanize_loop_dir`.
  - Outputs:
    - Test accounting through `TESTS_PASSED`, `TESTS_FAILED`, and `TESTS_SKIPPED`, initialized at `tests/test-state-exit-naming.sh:23-25` and reported at `tests/test-state-exit-naming.sh:293-302`.
    - Human-readable PASS/FAIL/SKIP lines via helper functions at `tests/test-state-exit-naming.sh:27-29`.
    - Process exit status equals `TESTS_FAILED`, at `tests/test-state-exit-naming.sh:302`.
  - State transitions:
    - `state.md` means active loop.
    - Terminal files are snapshots of ended loops and must not revive loop activity.
    - `end_loop "$dir" "$dir/state.md" "$reason"` transforms active state by moving `state.md` to `$dir/<reason>-state.md`; this implementation is in `hooks/lib/loop-common.sh:1119-1145`.
    - The test explicitly removes `state.md` before terminal-file checks, at `tests/test-state-exit-naming.sh:99`.

- gates_or_invariants:
  - Only `state.md` is accepted by this test as an active normal RLCR state; terminal reason files are inactive.
  - The implementation helper currently also treats `finalize-state.md` as active, according to `hooks/lib/loop-common.sh:151-170`; this assigned test does not exercise finalize-state activity.
  - `find_active_loop` only checks the newest timestamp-named child directory by reverse sort, then returns it only if an active state file exists, at `hooks/lib/loop-common.sh:164-173`.
  - This creates a zombie-loop invariant: older directories are ignored even if they contain `state.md`; the test’s newer-directory case asserts newest active directory wins, at `tests/test-state-exit-naming.sh:161-180`.
  - `end_loop` reason vocabulary is closed: `complete|cancel|maxiter|stop|unexpected`, enforced in `hooks/lib/loop-common.sh:1124-1132` and specified by `tests/test-state-exit-naming.sh:186-230`.
  - A missing state file must not create a terminal file; it returns failure after warning, enforced in `hooks/lib/loop-common.sh:1136-1144` and tested at `tests/test-state-exit-naming.sh:232-243`.
  - New path-root invariant: `.humanize/rlcr/` is the only RLCR loop path pattern for this detection helper; `.humanize-loop.local` is intentionally excluded, at `hooks/lib/loop-common.sh:712-716` and `tests/test-state-exit-naming.sh:249-291`.

- dependencies_and_callers:
  - Direct dependency:
    - `hooks/lib/loop-common.sh`, sourced at `tests/test-state-exit-naming.sh:67`.
  - Functions under test:
    - `find_active_loop` in `hooks/lib/loop-common.sh:156-174`.
    - `is_in_humanize_loop_dir` in `hooks/lib/loop-common.sh:713-716`.
    - `end_loop` in `hooks/lib/loop-common.sh:1119-1145`.
  - Related production callers:
    - `hooks/loop-codex-stop-hook.sh` sets `LOOP_BASE_DIR="$PROJECT_ROOT/.humanize/rlcr"` and calls `find_active_loop` to decide whether the stop hook should act, at `hooks/loop-codex-stop-hook.sh:43-63`.
    - The stop hook uses `end_loop` for schema/model/state errors as `unexpected-state.md`, at `hooks/loop-codex-stop-hook.sh:120-149`.
    - It uses `end_loop` for max-iteration termination, at `hooks/loop-codex-stop-hook.sh:730-733` and `hooks/loop-codex-stop-hook.sh:1403-1406`.
    - It directly renames `finalize-state.md` to `complete-state.md` when finalization succeeds, at `hooks/loop-codex-stop-hook.sh:742-747`.
    - It uses `end_loop` for STOP/circuit-breaker termination, at `hooks/loop-codex-stop-hook.sh:1471-1498`.
    - `scripts/cancel-rlcr-loop.sh` documents and performs cancellation by creating `.cancel-requested` and moving active state to `cancel-state.md`, at `scripts/cancel-rlcr-loop.sh:1-15`, `scripts/cancel-rlcr-loop.sh:49-53`, and `scripts/cancel-rlcr-loop.sh:134-152`.
    - `scripts/setup-rlcr-loop.sh` uses `find_active_loop` to reject starting a second RLCR loop while one is active, at `scripts/setup-rlcr-loop.sh:232-246`, and creates new loop sessions under `.humanize/rlcr/<timestamp>`, at `scripts/setup-rlcr-loop.sh:667-694`.
  - Related tests:
    - `tests/test-finalize-phase.sh` also verifies `complete-state.md` is not active and checks finalize completion renames to `complete-state.md`.
    - `tests/robustness/test-concurrent-state-robustness.sh` and `tests/robustness/test-session-robustness.sh` contain broader robustness coverage for `find_active_loop`, including empty directories, nonexistent bases, old directories, and terminal states.
    - `tests/test-cancel-signal-file.sh` covers guarded shell `mv state.md cancel-state.md` behavior with a cancel signal.

- edge_cases_or_failure_modes:
  - Invalid reason to `end_loop` must fail without renaming, tested at `tests/test-state-exit-naming.sh:186-204`.
  - Missing `state.md` must fail with “State file not found” text and preserve no false terminal file, tested at `tests/test-state-exit-naming.sh:232-243`.
  - Terminal state files are inactive even when they contain plausible frontmatter, tested for all named terminal reasons at `tests/test-state-exit-naming.sh:51-159`.
  - Legacy `.humanize-loop.local` paths are deliberately not recognized, tested at `tests/test-state-exit-naming.sh:258-291`.
  - `find_active_loop` only examines the newest child directory. If newest directory exists but lacks `state.md` or `finalize-state.md`, older active loops are ignored by design; this is documented in `hooks/lib/loop-common.sh:151-154` and partially exercised by newer-directory precedence in this test.
  - `find_active_loop` sorts directory names lexically, so correctness assumes timestamp-like directory names sort chronologically, as used by fixtures such as `2024-01-02_12-00-00`.
  - The test leaves terminal files like `complete-state.md`, `cancel-state.md`, `unexpected-state.md`, `maxiter-state.md`, and `stop-state.md` side by side in the same synthetic directory. The invariant is therefore specifically that only `state.md` or implementation-recognized active files matter, not that terminal files are mutually exclusive.
  - The test uses `set -uo pipefail`, not initial `set -e`, at `tests/test-state-exit-naming.sh:13`. It temporarily toggles `set +e` and `set -e` around expected failures, at `tests/test-state-exit-naming.sh:196-199`, `tests/test-state-exit-naming.sh:216-219`, and `tests/test-state-exit-naming.sh:235-238`; after Test 8, the script continues with `errexit` enabled, so later unexpected command failures abort instead of only incrementing `TESTS_FAILED`.

- validation_or_tests:
  - This file is itself the validation artifact. It contains 13 named test scenarios:
    - Tests 1-7 cover active-loop discovery and state filename semantics, at `tests/test-state-exit-naming.sh:38-180`.
    - Tests 8-10 cover `end_loop` validation and rename behavior, at `tests/test-state-exit-naming.sh:186-243`.
    - Tests 11-13 cover path detection and legacy path exclusion, at `tests/test-state-exit-naming.sh:249-291`.
  - I inspected the test and its referenced helper implementation directly. I did not execute the test in this read-only branch export; an attempted repository metadata check failed because this export is not a git checkout with usable `.git`, and the environment reported restricted temp/cache writes from developer tooling.
  - The test’s expected implementation behavior matches the helper definitions in `hooks/lib/loop-common.sh` for `end_loop` and path detection. For `find_active_loop`, the helper recognizes both `state.md` and `finalize-state.md` as active, while this specific test only asserts the normal `state.md` and terminal-file cases.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 item section present, matching the single assigned row above
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`