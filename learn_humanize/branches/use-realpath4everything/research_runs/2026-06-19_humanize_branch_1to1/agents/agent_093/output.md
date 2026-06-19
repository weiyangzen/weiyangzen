# agent_093 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-093 `file` `tests/test-state-exit-naming.sh`
- cursor: `[_]`
- core_role:
  - Executable specification for RLCR loop state lifecycle naming. It locks down that an active loop is represented by `state.md` under `.humanize/rlcr/<timestamp>/`, while terminal states are preserved as reason-specific files such as `complete-state.md`, `cancel-state.md`, `maxiter-state.md`, `stop-state.md`, and `unexpected-state.md`.
  - It also verifies the migration boundary from the legacy `.humanize-loop.local` location to the current `.humanize/rlcr` location, especially through `is_in_humanize_loop_dir` and `find_active_loop` usage.
  - The test is not the implementation itself; it is a shell-level contract for functions sourced from `hooks/lib/loop-common.sh` at `tests/test-state-exit-naming.sh:67`.

- algorithmic_behavior:
  - Test setup creates a temporary git repository, configures a synthetic loop base, and writes state files into `$TEST_DIR/.humanize/rlcr/<timestamp>/`; see `tests/test-state-exit-naming.sh:31-49`.
  - Active-loop discovery behavior:
    - A directory containing only `complete-state.md` must not be returned by `find_active_loop`; see `tests/test-state-exit-naming.sh:51-74`.
    - A directory containing `state.md` must be returned; see `tests/test-state-exit-naming.sh:76-95`.
    - Terminal files `cancel-state.md`, `unexpected-state.md`, `maxiter-state.md`, and `stop-state.md` must not be treated as active; see `tests/test-state-exit-naming.sh:97-159`.
    - A newer timestamped directory with `state.md` takes precedence over older directories; see `tests/test-state-exit-naming.sh:161-180`.
  - Exit-state transition behavior:
    - `end_loop` rejects any reason outside `complete`, `cancel`, `maxiter`, `stop`, and `unexpected`; see `tests/test-state-exit-naming.sh:186-204`.
    - For every valid reason, `end_loop` renames `state.md` to `${reason}-state.md`; see `tests/test-state-exit-naming.sh:206-230`.
    - Missing `state.md` is a failure path with a "State file not found" diagnostic; see `tests/test-state-exit-naming.sh:232-243`.
  - Path classification behavior:
    - `.humanize/rlcr/.../state.md` is recognized as a humanize loop path; see `tests/test-state-exit-naming.sh:249-256`.
    - Legacy `.humanize-loop.local/.../state.md` is not recognized; see `tests/test-state-exit-naming.sh:258-265`.
    - Even if a legacy directory contains `state.md`, searching the new `.humanize/rlcr` base must not find it; see `tests/test-state-exit-naming.sh:267-291`.
  - Implementation contract in `hooks/lib/loop-common.sh`:
    - `resolve_active_state_file` treats `methodology-analysis-state.md`, `finalize-state.md`, and `state.md` as active-state candidates, in that order; see `hooks/lib/loop-common.sh:264-280`. This assigned test specifically covers `state.md` and terminal `*-state.md` files, not the finalize or methodology active states.
    - `find_active_loop` without a session filter checks only the single newest loop directory and returns it only when `resolve_active_state_file` finds an active state; see `hooks/lib/loop-common.sh:332-356`.
    - `end_loop` validates the reason and moves the active state file to `${reason}-state.md`; see `hooks/lib/loop-common.sh:1540-1566`.
    - `is_in_humanize_loop_dir` is a direct grep check for `.humanize/rlcr/`; see `hooks/lib/loop-common.sh:1252-1256`.

- inputs_outputs_state:
  - Inputs:
    - Temporary filesystem layout rooted at `TEST_DIR`, created by `mktemp -d`; see `tests/test-state-exit-naming.sh:31-33`.
    - Synthetic YAML-frontmatter state files written into `.humanize/rlcr/<timestamp>/`; representative examples at `tests/test-state-exit-naming.sh:52-62`, `tests/test-state-exit-naming.sh:78-88`, and `tests/test-state-exit-naming.sh:165-173`.
    - `CLAUDE_PROJECT_DIR="$TEST_DIR"` before sourcing shared helpers; see `tests/test-state-exit-naming.sh:64`.
    - Helper functions sourced from the repository copy of `hooks/lib/loop-common.sh`; see `tests/test-state-exit-naming.sh:15-17` and `tests/test-state-exit-naming.sh:67`.
  - Outputs:
    - Test harness emits `PASS`, `FAIL`, and `SKIP` counters and exits with `TESTS_FAILED`; see `tests/test-state-exit-naming.sh:27-29` and `tests/test-state-exit-naming.sh:293-302`.
    - `find_active_loop` returns either an active loop directory path or an empty string, as asserted throughout `tests/test-state-exit-naming.sh:69-74`, `tests/test-state-exit-naming.sh:90-95`, and `tests/test-state-exit-naming.sh:175-180`.
    - `end_loop` returns nonzero on invalid reason or missing state file, and returns zero after moving `state.md` to the expected terminal filename; see `tests/test-state-exit-naming.sh:196-204`, `tests/test-state-exit-naming.sh:216-229`, and `tests/test-state-exit-naming.sh:235-243`.
  - State transitions:
    - Active: `<loop>/state.md`.
    - Terminal: `<loop>/<reason>-state.md`, where reason is one of `complete`, `cancel`, `maxiter`, `stop`, or `unexpected`.
    - The active-loop cursor is effectively the presence of an active-state filename, not the YAML contents in the terminal-state tests.
  - Related project-root state:
    - `loop-common.sh` sources `hooks/lib/project-root.sh` before helpers are used; see `hooks/lib/loop-common.sh:176-179`.
    - The branch’s realpath theme is represented in `project-root.sh`, which resolves `CLAUDE_PROJECT_DIR` or git top-level through `realpath`; see `hooks/lib/project-root.sh:5-20` and `hooks/lib/project-root.sh:41-52`.
    - `canonicalize_path` and `canonicalize_path_prefix` are available for validators that compare user-provided paths to expected loop paths; see `hooks/lib/project-root.sh:55-96` and `hooks/lib/project-root.sh:98-144`. This assigned test does not directly exercise symlink/canonicalization cases.

- gates_or_invariants:
  - Only active-state filenames may keep a loop discoverable. Terminal reason files must preserve history while making the loop inactive.
  - `end_loop` accepts only the enumerated reason vocabulary; invalid reasons must fail before filesystem mutation.
  - `find_active_loop "$TEST_DIR/.humanize/rlcr"` must not search or infer legacy `.humanize-loop.local` state.
  - The new loop storage path is `.humanize/rlcr`, and the legacy path is deliberately outside loop-path protection in this test.
  - Newest-loop precedence is lexicographic/timestamp-directory based through `ls -1d ... | sort -r | head -1` in `hooks/lib/loop-common.sh:342-346`; the test validates the expected newest active directory behavior at `tests/test-state-exit-naming.sh:161-180`.
  - The terminal-state names are part of the contract because other hooks and monitors use `find_active_loop` to decide whether a loop is still active.

- dependencies_and_callers:
  - Direct dependencies:
    - Bash, `mktemp`, `git`, `mkdir`, `rm`, `grep`, `sed`, `ls`, `sort`, `head`, `mv`, and POSIX-like filesystem behavior.
    - `hooks/lib/loop-common.sh`, sourced at `tests/test-state-exit-naming.sh:67`.
    - `hooks/lib/project-root.sh`, sourced by `loop-common.sh` at `hooks/lib/loop-common.sh:176-179`.
  - Key implementation functions:
    - `find_active_loop`: `hooks/lib/loop-common.sh:332-425`.
    - `resolve_active_state_file`: `hooks/lib/loop-common.sh:268-280`.
    - `resolve_any_state_file`, relevant for session-filtered lookup but not directly exercised here: `hooks/lib/loop-common.sh:287-306`.
    - `is_in_humanize_loop_dir`: `hooks/lib/loop-common.sh:1253-1256`.
    - `end_loop`: `hooks/lib/loop-common.sh:1540-1566`.
  - Runtime callers using these contracts include:
    - `hooks/loop-codex-stop-hook.sh`, which finds the active loop, resolves active state, and calls `end_loop` for unexpected, max-iteration, stop, and other terminal paths.
    - `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-bash-validator.sh`, and `hooks/loop-plan-file-validator.sh`, which use active-loop/path detection to gate access to loop-managed files.
    - `scripts/statusline.sh`, which mirrors active-loop status behavior for display.
  - Sibling tests cover adjacent behavior:
    - `tests/test-finalize-phase.sh` covers `finalize-state.md` as an active state and transition to `complete-state.md`.
    - `tests/robustness/test-session-robustness.sh` covers session-filtered active-loop behavior and terminal-state ignoring.
    - `tests/test-cancel-signal-file.sh` covers protected cancellation transitions and symlink/prefix canonicalization edge cases.

- edge_cases_or_failure_modes:
  - The test does not cover `finalize-state.md` or `methodology-analysis-state.md`, even though `resolve_active_state_file` treats both as active before `state.md`; see `hooks/lib/loop-common.sh:271-276`.
  - The no-session `find_active_loop` path checks only the single newest directory. This intentionally prevents stale older loops from being revived, but it also means an older active `state.md` is ignored if the newest directory is terminal; the assigned test does not exercise that negative case.
  - `is_in_humanize_loop_dir` is substring-based, not canonicalized. It recognizes any path containing `.humanize/rlcr/`, so stronger project-root and active-loop checks must be enforced by callers when authorization matters.
  - `end_loop` uses `mv "$state_file" "$loop_dir/$target_name"` without explicit checks for an existing terminal target, cross-device errors, permissions, or concurrent writers; the test covers success, invalid reason, and missing source only.
  - Test 9 reuses one loop directory and deletes each expected terminal file after checking it; it validates target creation but not absence of `state.md` after each successful move.
  - YAML contents in terminal files are minimal and mostly irrelevant to these assertions. The active/terminal distinction is filename-driven here, not schema-driven.
  - The script starts with `set -uo pipefail`; after the invalid-reason probe it enables `set -e` at `tests/test-state-exit-naming.sh:199`, so unexpected command failures later in the script can abort the run instead of only incrementing the failure counter.

- validation_or_tests:
  - Read the assigned file directly with line numbers: `tests/test-state-exit-naming.sh:1-302`.
  - Read the relevant implementation in `hooks/lib/loop-common.sh`, especially active-state resolution, active-loop discovery, path classification, and loop termination.
  - Read `hooks/lib/project-root.sh` to understand the related realpath project-root dependency used by sourced loop helpers.
  - Performed read-only syntax validation: `bash -n tests/test-state-exit-naming.sh` exited successfully.
  - Did not run the full integration test because this assignment requests research notes only and the test creates temporary git/state directories as part of execution.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1/1 in Item Evidence`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`