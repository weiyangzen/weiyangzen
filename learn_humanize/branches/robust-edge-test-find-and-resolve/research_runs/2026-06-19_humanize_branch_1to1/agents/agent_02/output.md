# agent_02 robust-edge-test-find-and-resolve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 4
- source_commit: `a3112ca4d149f56ced783e805b6dfcf029368dc4`

## Item Evidence

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-002 `directory` `agents`
- cursor: `[_]`
- core_role:
  `agents` is a small agent-definition directory with one recursive child: `agents/draft-relevance-checker.md`. Its algorithmic responsibility is not runtime goal-tracker parsing; it defines a Claude/Task subagent used by the `gen-plan` command to classify whether a user draft belongs to the current repository before plan generation proceeds.
- algorithmic_behavior:
  The child agent frontmatter declares `name: draft-relevance-checker`, `description`, `model: haiku`, and tools `Read, Glob, Grep` at `agents/draft-relevance-checker.md:1-6`. The prompt body instructs the agent to quickly inspect repository docs and structure, compare draft content to repository concepts/files/features, and return exactly one verdict form: `RELEVANT: <brief explanation>` or `NOT_RELEVANT: <brief explanation>` at `agents/draft-relevance-checker.md:12-30`.
  The decision rule is deliberately permissive: it should be lenient, accept informal or multilingual drafts, focus on semantic relevance, and lean relevant when uncertain at `agents/draft-relevance-checker.md:31-36`.
- inputs_outputs_state:
  Input is draft document content passed by `commands/gen-plan.md`, plus read-only repository exploration. Output is a single textual relevance verdict consumed by the command workflow. There is no persisted state, no file modification contract, and no checklist cursor transition in this directory.
- gates_or_invariants:
  The directory supports the `gen-plan` relevance gate. `commands/gen-plan.md:48-68` says after IO validation, the draft is read and `humanize:draft-relevance-checker` is invoked; `NOT_RELEVANT` stops the command, while `RELEVANT` advances to deeper draft analysis. Agent metadata invariants are covered by `tests/test-gen-plan.sh`: file existence at `tests/test-gen-plan.sh:107-116`, exact name at `tests/test-gen-plan.sh:121-129`, model at `tests/test-gen-plan.sh:133-143`, tools field at `tests/test-gen-plan.sh:147-156`, naming/frontmatter/model/content validations at `tests/test-gen-plan.sh:195-245`, `tests/test-gen-plan.sh:208-214`, `tests/test-gen-plan.sh:391-421`.
- dependencies_and_callers:
  Primary caller is `commands/gen-plan.md`, which allows `Task` and directs invocation of `humanize:draft-relevance-checker` at `commands/gen-plan.md:4-11` and `commands/gen-plan.md:52-61`. Test dependency is `tests/test-gen-plan.sh`, which sets `AGENTS_DIR="$PROJECT_ROOT/agents"` at `tests/test-gen-plan.sh:11-14` and validates `agents/draft-relevance-checker.md`.
  Recursive inspection found only:
  `agents`
  `agents/draft-relevance-checker.md`
- edge_cases_or_failure_modes:
  Draft relevance is semantic and intentionally broad; the main risk is false positive relevance because uncertainty is biased toward relevant. False negatives stop plan generation early. Metadata failures include missing frontmatter, invalid agent name, invalid model, missing tools declaration, or disallowed content characters as tested in `tests/test-gen-plan.sh:195-421`.
- validation_or_tests:
  `tests/test-gen-plan.sh` is the direct executable validation surface. `tests/run-all-tests.sh` also includes `test-gen-plan.sh` in the aggregate suite at `tests/run-all-tests.sh:50-51`.
- skip_candidate: `yes: assigned directory is part of command planning/relevance gating, but it is not part of the branch's goal-tracker robustness parser path or the bash-write goal-tracker hook path. It is still covered here because it was explicitly assigned as a directory containing an included descendant.`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-032 `file` `tests/run-all-tests.sh`
- cursor: `[_]`
- core_role:
  `tests/run-all-tests.sh` is the aggregate executable specification for the plugin. It defines the ordered test suite list, runs each suite, normalizes ANSI output, aggregates pass/fail counts, and sets the final process status for CI/manual verification.
- algorithmic_behavior:
  The script initializes counters and `FAILED_SUITES` at `tests/run-all-tests.sh:28-30`, then declares an ordered `TEST_SUITES` array at `tests/run-all-tests.sh:32-63`. The ordering includes core template/hook/parser tests first and robustness suites last. The assigned goal-tracker robustness suite is explicitly included at `tests/run-all-tests.sh:55`.
  For each suite, it computes `suite_path`, skips missing files with a yellow `SKIP`, detects whether the suite needs zsh, executes under zsh only for listed zsh suites, otherwise executes the script directly, captures combined stdout/stderr, and records exit code at `tests/run-all-tests.sh:70-109`.
  It strips ANSI escape sequences and extracts the last `Passed:` and `Failed:` numeric counts from suite output at `tests/run-all-tests.sh:111-115`, adds them to aggregate totals at `tests/run-all-tests.sh:117-118`, and classifies a suite as failed if either exit code is nonzero or parsed failed count is greater than zero at `tests/run-all-tests.sh:120-127`.
- inputs_outputs_state:
  Inputs are executable test files under `tests/`, optional `zsh` availability for `test-zsh-monitor-safety.sh`, and each suite's conventional summary lines. Outputs are console status, aggregate totals, failed suite names, and exit status `0` only if no failed suites were recorded. Mutable state is local shell variables only: `TOTAL_PASSED`, `TOTAL_FAILED`, `FAILED_SUITES`, `output`, `exit_code`, `passed`, `failed`.
- gates_or_invariants:
  Missing suites are skipped rather than failing at `tests/run-all-tests.sh:73-76`, so presence of every named suite is not a hard invariant. zsh-only tests are skipped if zsh is unavailable at `tests/run-all-tests.sh:96-104`. Failure classification is stricter than exit code alone because parsed failed counts also fail the suite at `tests/run-all-tests.sh:120-124`. The final gate exits `1` when `FAILED_SUITES` is nonempty and exits `0` otherwise at `tests/run-all-tests.sh:138-149`.
- dependencies_and_callers:
  Depends on each listed test script being executable or invokable by path, shell utilities `sed`, `grep`, `tail`, and optionally `zsh`. It coordinates sibling suites including `tests/robustness/test-goal-tracker-robustness.sh`, making it the umbrella validation entrypoint for the assigned robustness parser tests.
- edge_cases_or_failure_modes:
  A suite that omits conventional `Passed:`/`Failed:` lines is parsed as zero passed/failed due fallback `echo "0"` at `tests/run-all-tests.sh:114-115`; if it exits `0`, it can be reported as passed with `0 tests`. A missing test file is skipped, not failed. If zsh is missing, the zsh-specific suite is skipped. Only the last matching `Passed:` and `Failed:` counts are used because of `tail -1`, so noisy suites with multiple summaries rely on final summary correctness.
- validation_or_tests:
  This file is itself the validation aggregator. The assigned goal-tracker robustness file is included as a suite entry at `tests/run-all-tests.sh:55`; its pass/fail summary is consumed through the parser at `tests/run-all-tests.sh:111-127`.
- skip_candidate: `no`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-062 `file` `prompt-template/block/goal-tracker-bash-write.md`
- cursor: `[_]`
- core_role:
  This template is the canonical user-facing block message for Bash attempts to modify `goal-tracker.md` during Round 0. It does not detect violations itself; it defines the corrective instruction rendered by the hook helper after the Bash validator detects a write-like command.
- algorithmic_behavior:
  The template title is `Bash Write Blocked: Use Write or Edit Tool` at `prompt-template/block/goal-tracker-bash-write.md:1`. It tells the actor not to use Bash to modify `goal-tracker.md` at line 3, points them to `{{CORRECT_PATH}}` with Write/Edit at line 5, and explains that `cat`, `echo`, `sed`, `awk`, and similar commands bypass validation hooks at lines 7-8.
  Rendering is performed by `goal_tracker_bash_blocked_message()` in `hooks/lib/loop-common.sh:396-405`, which supplies `CORRECT_PATH` and falls back to a short inline message if the template cannot be loaded.
- inputs_outputs_state:
  Input is `CORRECT_PATH`, rendered from the active loop's `goal-tracker.md` path by the Bash validator. Output is markdown denial text printed to stderr. The template holds no state and has no side effects.
- gates_or_invariants:
  The actual gate is in `hooks/loop-bash-validator.sh`: when `command_modifies_file "$COMMAND_LOWER" "goal-tracker\.md"` matches, Round 0 calls `goal_tracker_bash_blocked_message "$ACTIVE_LOOP_DIR/goal-tracker.md"` and exits `2` at `hooks/loop-bash-validator.sh:321-335`. For later rounds, it uses the separate goal-tracker modification template and asks for a summary-file update request at `hooks/loop-bash-validator.sh:331-334`.
  The detection helper recognizes redirection, append redirection, `tee`, in-place `sed`/`awk`/`perl`, `mv`/`cp`, `rm`, `dd of=`, `truncate`, `printf >`, and fd `exec >` patterns at `hooks/lib/loop-common.sh:772-800`.
- dependencies_and_callers:
  Direct caller is `goal_tracker_bash_blocked_message()` in `hooks/lib/loop-common.sh:396-405`. That helper is called by `hooks/loop-bash-validator.sh:327-335`. Template existence is cross-reference checked in `tests/test-template-references.sh:152-159`.
- edge_cases_or_failure_modes:
  The template only covers Round 0 Bash writes; direct Write/Edit attempts after Round 0 are blocked by `hooks/loop-write-validator.sh:160-168`, and Bash attempts after Round 0 use a different message. Pattern tests document that normal reads like `cat goal-tracker.md`, `grep`, `head`, `tail`, `wc`, `less`, `ls`, `file`, `stat`, and `diff` should not be blocked at `tests/test-bash-validator-patterns.sh:136-152`. A known limitation is called out for multi-source `cp file1.md file2.md goal-tracker.md`, which is not detected by the two-argument `cp src dest` pattern at `tests/test-bash-validator-patterns.sh:165-168`.
- validation_or_tests:
  Template reference validation includes this file at `tests/test-template-references.sh:152-159`. Bash detection behavior is covered by `tests/test-bash-validator-patterns.sh:36-62` and goal-tracker cases at `tests/test-bash-validator-patterns.sh:70-173`.
- skip_candidate: `no`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-092 `file` `tests/robustness/test-goal-tracker-robustness.sh`
- cursor: `[_]`
- core_role:
  This is the AC-3 executable robustness specification for production `humanize_parse_goal_tracker` in `scripts/humanize.sh`. It asserts that goal-tracker parsing remains stable across normal formats, malformed files, large counts, special characters, binary content, empty input, section-only input, and long goal text.
- algorithmic_behavior:
  The script sources test helpers, then sources production `scripts/humanize.sh` at `tests/robustness/test-goal-tracker-robustness.sh:18-24`. It defines `parse_result()` to split the parser's pipe-delimited return format into named fields at `tests/robustness/test-goal-tracker-robustness.sh:38-51`.
  The production contract under test is documented at `tests/robustness/test-goal-tracker-robustness.sh:35-36`: `total_acs|completed_acs|active_tasks|completed_tasks|deferred_tasks|open_issues|goal_summary`.
  The production implementation returns defaults for missing files at `scripts/humanize.sh:26-31`, counts AC rows in the Acceptance Criteria section using list/table regex at `scripts/humanize.sh:42-48`, counts active table rows excluding completed/deferred statuses at `scripts/humanize.sh:50-78`, counts completed/deferred/issues sections through table row subtraction at `scripts/humanize.sh:33-40` and `scripts/humanize.sh:80-97`, extracts unique completed ACs at `scripts/humanize.sh:84-88`, and truncates the first Ultimate Goal content line to 60 chars at `scripts/humanize.sh:98-105`.
- inputs_outputs_state:
  Inputs are temporary `goal-tracker*.md` fixtures created under `$TEST_DIR`. Outputs are pass/fail records via helper functions and final summary from `print_test_summary` at `tests/robustness/test-goal-tracker-robustness.sh:526-531`. State transitions are fixture creation, parser invocation, field extraction, assertion, and final exit with the helper summary status.
- gates_or_invariants:
  The parser must:
  count list-format AC entries at `tests/robustness/test-goal-tracker-robustness.sh:60-87`;
  count table-format AC entries at `tests/robustness/test-goal-tracker-robustness.sh:89-116`;
  count active tasks by excluding rows whose status is completed or deferred at `tests/robustness/test-goal-tracker-robustness.sh:118-153`;
  count completed task rows and unique completed AC IDs at `tests/robustness/test-goal-tracker-robustness.sh:155-202`;
  extract Ultimate Goal text at `tests/robustness/test-goal-tracker-robustness.sh:204-227`;
  return exact missing-file defaults at `tests/robustness/test-goal-tracker-robustness.sh:237-244`;
  return zero ACs for empty and malformed/no-header files at `tests/robustness/test-goal-tracker-robustness.sh:246-256` and `tests/robustness/test-goal-tracker-robustness.sh:304-326`;
  handle 60 ACs at `tests/robustness/test-goal-tracker-robustness.sh:258-279`;
  tolerate special characters and binary bytes at `tests/robustness/test-goal-tracker-robustness.sh:281-302` and `tests/robustness/test-goal-tracker-robustness.sh:349-371`;
  count open issues and deferred tasks at `tests/robustness/test-goal-tracker-robustness.sh:373-439`;
  keep header-only files at zero counts at `tests/robustness/test-goal-tracker-robustness.sh:441-475`;
  tolerate bold AC syntax and ignore decimal subnumbering expectations at `tests/robustness/test-goal-tracker-robustness.sh:477-499`;
  enforce goal summary length no more than 60 chars at `tests/robustness/test-goal-tracker-robustness.sh:501-524`.
- dependencies_and_callers:
  Depends on `tests/test-helpers.sh` for `setup_test_dir`, `pass`, `fail`, and `print_test_summary`, and on `scripts/humanize.sh` for the production parser. It is called by the aggregate test runner through `tests/run-all-tests.sh:52-63`, specifically the suite entry at `tests/run-all-tests.sh:55`. Production monitor usage wraps the same parser with `_parse_goal_tracker()` at `scripts/humanize.sh:375-378` and feeds its fields into the monitor status bar at `scripts/humanize.sh:408-417`, displaying AC/task/issue progress at `scripts/humanize.sh:483-492`.
- edge_cases_or_failure_modes:
  The suite intentionally covers non-existent files, empty files, malformed missing-section headers, truncated markdown, binary content, large AC counts, special shell/markdown characters, header-only content, bold AC IDs, decimal subcriteria, and long goal summaries. It also exposes parser assumptions: section boundaries are header-sensitive; table row counts subtract two header/separator rows; active-task parsing requires a pipe table with status in the third column; goal summary uses the first nonblank non-placeholder line after `### Ultimate Goal`; the parser returns a pipe-delimited string, so embedded pipe characters in goal text would be structurally risky though not directly tested here.
- validation_or_tests:
  The file is a test suite and is included in the global runner. I did not run it because the assignment requested research notes only and the environment is read-only/restricted; all inspection was direct source reading.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `4/4 assigned item sections present; each assigned section heading occurs once`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`