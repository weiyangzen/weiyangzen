# agent_073 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-073 `file` `tests/test-codex-review-merge.sh`
- cursor: `[_]`
- core_role:
  - `tests/test-codex-review-merge.sh` is an executable shell specification for the Codex review-log merge/detection algorithm implemented by `detect_review_issues()` in `hooks/lib/loop-common.sh`.
  - Its core contract is declared at `tests/test-codex-review-merge.sh:5-15`: detect `[P0-9]` review findings only when the marker appears near the beginning of a line, scan only the last 50 log lines, extract from the first matching issue line through EOF, and return distinct exit codes for issues, no issues, and invalid/missing logs.
  - It is part of the project test suite via `tests/run-all-tests.sh:60-77`, where `test-codex-review-merge.sh` is registered alongside other hook/loop validation suites.

- algorithmic_behavior:
  - The test loads the real shared implementation by sourcing `hooks/lib/loop-common.sh` at `tests/test-codex-review-merge.sh:41-42`; it does not stub `detect_review_issues()`.
  - The setup function creates a synthetic RLCR loop directory and Codex review cache directory, then exports `LOOP_DIR` and `CACHE_DIR` for the implementation under test at `tests/test-codex-review-merge.sh:47-54`.
  - The implementation under test constructs the input log as `$CACHE_DIR/round-${round}-codex-review.log` and the persisted extracted result as `$LOOP_DIR/round-${round}-review-result.md` at `hooks/lib/loop-common.sh:740-743`.
  - The algorithm first rejects a missing or zero-size log with exit `2` at `hooks/lib/loop-common.sh:745-749`.
  - It computes total line count, chooses a 50-line scan window, and calculates the absolute start line of that window at `hooks/lib/loop-common.sh:751-758`.
  - It pipes `tail -n 50` into `awk`, matching only lines where `substr($0, 1, 10)` contains `/\[P[0-9]\]/`, returning the first relative line number only at `hooks/lib/loop-common.sh:759-766`.
  - When a match exists, it converts the relative tail line into an absolute file line, extracts from that line through EOF with `sed -n "${found_line},\$p"`, writes the raw extraction to the review-result file, and prints a markdown-wrapped `## Codex Review Issues` block to stdout at `hooks/lib/loop-common.sh:768-783`.
  - When no match exists in the scan window, it emits an informational stderr message and returns `1` at `hooks/lib/loop-common.sh:786-787`.
  - The stop-hook caller treats these results as loop-control decisions: exit `2` blocks as review failure, exit `0` with content continues the review loop with issues, and exit `1` proceeds to finalize at `hooks/loop-codex-stop-hook.sh:1262-1278`.

- inputs_outputs_state:
  - Inputs:
    - One positional round number passed to `detect_review_issues`, e.g. calls at `tests/test-codex-review-merge.sh:73`, `:98`, `:123`, `:142`, `:161`, `:189`, `:218`, `:246`, `:270`, `:294`, `:321`, `:346`.
    - Environment globals `LOOP_DIR` and `CACHE_DIR`, exported by `setup_test_env` at `tests/test-codex-review-merge.sh:49-53`.
    - Synthetic log files named `round-N-codex-review.log` under `$CACHE_DIR`, written by individual scenarios.
  - Outputs:
    - Exit `0` means issues found; stdout must include extracted issue text, often checked with `grep -q '\[P1\]'`, `'\[P2\]'`, or `'\[P0\]'`.
    - Exit `1` means no valid issue marker found in the allowed scan area.
    - Exit `2` means the log file is missing or empty, treated as a hard review failure.
    - On issue detection, a persistent audit/result file `$LOOP_DIR/round-N-review-result.md` is created; test 11 verifies this at `tests/test-codex-review-merge.sh:306-330`.
  - State transitions:
    - The test harness increments `TESTS_PASSED` or `TESTS_FAILED` through `pass()` and `fail()` helpers at `tests/test-codex-review-merge.sh:23-31`.
    - Each test case calls `setup_test_env`; this reuses deterministic subpaths under one `mktemp` root and ensures both loop and cache directories exist before writing logs.
    - The suite exits `1` if any scenario fails at `tests/test-codex-review-merge.sh:356-368`; otherwise it exits successfully by falling through.
    - In production integration, `run_codex_code_review()` writes the Codex review command file and combined log file at `hooks/loop-codex-stop-hook.sh:1185-1229`, then `run_and_handle_code_review()` feeds that log to `detect_review_issues()` at `hooks/loop-codex-stop-hook.sh:1250-1278`.

- gates_or_invariants:
  - Marker-position invariant: `[P0-9]` must appear within the first 10 characters of a line. Test 1 validates normal detection at `tests/test-codex-review-merge.sh:56-81`; test 2 validates that later mentions are ignored at `tests/test-codex-review-merge.sh:83-107`; test 9 validates position `0` at `tests/test-codex-review-merge.sh:257-278`; test 10 validates the common `- [P1]` prefix at `tests/test-codex-review-merge.sh:280-303`.
  - Window invariant: only the last 50 lines are scanned. Test 6 places `[P1]` at line 55 of a 60-line log and expects detection at `tests/test-codex-review-merge.sh:171-197`; test 7 places `[P1]` at line 5 of a 70-line log and expects no detection at `tests/test-codex-review-merge.sh:199-227`.
  - Extraction invariant: once the first eligible priority marker is found, all subsequent content through EOF is extracted. Test 8 checks that `[P0]`, later `[P2]`, and trailing non-issue text are all included at `tests/test-codex-review-merge.sh:229-255`.
  - Boundary invariant: exactly 50 lines means the first line is inside the scan window. Test 12 validates a `[P1]` on line 1 of a 50-line log at `tests/test-codex-review-merge.sh:332-354`.
  - Hard-error invariant: absent or empty logs are not interpreted as “no issues”; they return `2`. Missing-log behavior is tested at `tests/test-codex-review-merge.sh:133-150`, and empty-log behavior at `tests/test-codex-review-merge.sh:152-169`.
  - Audit invariant: issue detection must persist an extracted result file for later review-loop evidence. Test 11 checks file creation at `tests/test-codex-review-merge.sh:306-330`; implementation writes it at `hooks/lib/loop-common.sh:777-779`.

- dependencies_and_callers:
  - Direct dependencies:
    - Bash with `set -uo pipefail` at `tests/test-codex-review-merge.sh:18`.
    - Standard shell utilities: `mktemp`, `mkdir`, `rm`, `touch`, `seq`, `grep`, `tail`, `awk`, `sed`, `wc`.
    - `hooks/lib/loop-common.sh`, sourced at `tests/test-codex-review-merge.sh:41-42`.
  - Transitive implementation dependencies:
    - `loop-common.sh` sources `hooks/lib/project-root.sh`, `scripts/lib/config-loader.sh`, and `hooks/lib/template-loader.sh` during load at `hooks/lib/loop-common.sh:171-240`; the tested function itself relies only on `LOOP_DIR`, `CACHE_DIR`, and shell text tools once loaded.
  - Production caller:
    - `hooks/loop-codex-stop-hook.sh` generates the review prompt/command/log files in `run_codex_code_review()` at `hooks/loop-codex-stop-hook.sh:1171-1235`.
    - `run_and_handle_code_review()` calls `detect_review_issues "$round"` and branches on its exit status at `hooks/loop-codex-stop-hook.sh:1262-1278`.
    - If the Codex review command fails or `detect_review_issues()` returns hard error `2`, `block_review_failure()` blocks exit and renders a retry-required failure reason at `hooks/loop-codex-stop-hook.sh:1548-1620`.

- edge_cases_or_failure_modes:
  - False positives from debug text are intentionally reduced by two filters: scan only the last 50 lines and require marker placement within characters 1-10. Tests 2 and 7 are the strongest guards against this behavior.
  - A valid `[P?]` marker outside the last 50 lines is ignored even if it is syntactically correct; this is deliberate per `tests/test-codex-review-merge.sh:200-206` and `hooks/lib/loop-common.sh:728-736`.
  - A `[P?]` mention after character 10 is ignored even in short logs, preventing mid-sentence or explanatory references from triggering issue loops.
  - Missing and empty logs are hard failures because the review phase cannot safely be skipped without Codex output; tests 4 and 5 enforce exit `2`.
  - Multiple valid markers do not cause multiple separate extraction passes; the first eligible marker determines the extraction start, and later lines are included as plain downstream content.
  - Result-file writing assumes `$LOOP_DIR` already exists. The test’s setup creates it at `tests/test-codex-review-merge.sh:51`; production loop setup is expected to do the same before review handling.
  - The test script temporarily disables `errexit` around calls expected to return nonzero with `set +e`, captures `$?`, then restores `set -e`, e.g. `tests/test-codex-review-merge.sh:72-75`; this lets negative cases assert exit codes without aborting the suite.

- validation_or_tests:
  - The file itself is the validation artifact, covering 12 scenarios:
    - Test 1: valid issue markers near line start return `0` and include both `[P1]` and `[P2]` at `tests/test-codex-review-merge.sh:56-81`.
    - Test 2: markers outside the first 10 characters return `1` at `tests/test-codex-review-merge.sh:83-107`.
    - Test 3: no marker returns `1` at `tests/test-codex-review-merge.sh:109-131`.
    - Test 4: missing log returns `2` at `tests/test-codex-review-merge.sh:133-150`.
    - Test 5: empty log returns `2` at `tests/test-codex-review-merge.sh:152-169`.
    - Test 6: marker inside the final 50 lines of a long log returns `0` at `tests/test-codex-review-merge.sh:171-197`.
    - Test 7: marker outside the final 50 lines returns `1` at `tests/test-codex-review-merge.sh:199-227`.
    - Test 8: extraction starts at the first eligible marker and includes trailing content at `tests/test-codex-review-merge.sh:229-255`.
    - Test 9: marker at character position 0 is detected at `tests/test-codex-review-merge.sh:257-278`.
    - Test 10: dash-prefixed review item format is detected at `tests/test-codex-review-merge.sh:280-303`.
    - Test 11: issue detection creates `round-N-review-result.md` at `tests/test-codex-review-merge.sh:306-330`.
    - Test 12: exactly 50 lines includes line 1 in the scan window at `tests/test-codex-review-merge.sh:332-354`.
  - I did not execute the test suite because the assignment explicitly requested research notes only and no file modifications; the script creates temporary files and result artifacts during execution.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 item section present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`