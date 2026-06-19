# agent_09 claude/add-dependency-check-tA0P8 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `df26142e5fbed5e2ac3e48f001786cfa77296dda`

## Item Evidence

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-009 `file` `README.md`
- cursor: `[_]`
- core_role:
  Behavior-defining user documentation for the Humanize RLCR and PR-loop workflows. It specifies the top-level state-machine intent: Claude implements, Codex reviews, feedback loops until completion, then a final code review gate decides whether work is done or returned to Claude.
- algorithmic_behavior:
  The RLCR flow is documented as a two-phase loop: Implementation Phase and Review Phase at `README.md:111-114`. The diagram at `README.md:101-109` defines transitions from `plan.md` to Claude implementation, Codex summary review, feedback loop, `COMPLETE`, final `codex review --base <branch>`, issue remediation, and final done state. The PR loop behavior at `README.md:232-240` defines a remote-review loop: detect PR, fetch bot comments, have Claude fix, push, trigger re-review, stop hook polls, local Codex validates remote concerns, repeat until approval or max iterations.
- inputs_outputs_state:
  Inputs include a plan file or generated plan draft (`README.md:117-123`), command options for max iterations, model, timeout, plan tracking, push cadence, base branch, full-review interval, skip implementation, Claude answers, and agent teams (`README.md:147-171`). The PR loop input requires `--claude` and/or `--codex` bot selection (`README.md:197-202`). Outputs/state surfaces include `.humanize/rlcr/<timestamp>/` for progress (`README.md:125`), `.humanize/pr-loop/` for PR monitoring implied by `humanize monitor pr` (`README.md:247-250`), and `.humanize/skill/<timestamp>/` for one-shot Codex consultation artifacts (`README.md:229-230`).
- gates_or_invariants:
  RLCR requires Codex CLI (`README.md:54-57`). The Review Phase uses severity markers `[P0-9]` as review results (`README.md:111-114`). Base branch selection is deterministic by priority: explicit user input, remote default, `main`, then `master` (`README.md:159-160`). Full Alignment Check cadence is bounded by `--full-review-round` with default 5 and minimum 2 (`README.md:161-163`). The PR loop requires GitHub CLI authentication, Codex CLI, and an open associated PR (`README.md:242-245`).
- dependencies_and_callers:
  The README is not executable but defines the public command contract for `/humanize:start-rlcr-loop`, `/humanize:cancel-rlcr-loop`, `/humanize:gen-plan`, `/humanize:start-pr-loop`, `/humanize:cancel-pr-loop`, and `/humanize:ask-codex` (`README.md:132-142`). It references the monitor shell entrypoint from `scripts/humanize.sh` via `humanize monitor [rlcr|pr]` (`README.md:125-129`). It references Codex sandbox behavior through `HUMANIZE_CODEX_BYPASS_SANDBOX` (`README.md:62-95`).
- edge_cases_or_failure_modes:
  The documentation explicitly warns that bypassing the Codex sandbox gives unrestricted filesystem and command access (`README.md:62-87`). PR-loop failure prerequisites include missing `gh`, missing Codex, or no associated PR (`README.md:242-245`). The `--skip-impl` option bypasses the implementation phase and makes the plan optional (`README.md:164-165`), which changes the normal state path.
- validation_or_tests:
  README behavior is covered indirectly by command/script tests found in assigned items and related files: `tests/test-pr-loop-scripts.sh` validates PR setup/cancel behavior, `tests/test-monitor-e2e-sigint.sh` validates monitor interruption, and `tests/robustness/test-goal-tracker-robustness.sh` validates monitor goal parsing. No README-specific test runner was executed because the branch export is read-only.
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-039 `file` `scripts/cancel-pr-loop.sh`
- cursor: `[_]`
- core_role:
  Runtime cancellation script for the PR-loop state machine. It converts the newest active PR loop from active state to cancelled state by creating a cancel signal and renaming `state.md`.
- algorithmic_behavior:
  The script parses only `--force`, `-h`, and `--help`; unknown options exit with code 3 (`scripts/cancel-pr-loop.sh:24-66`). It resolves `PROJECT_ROOT` from `CLAUDE_PROJECT_DIR` or `pwd`, then uses `.humanize/pr-loop` as its only loop base (`scripts/cancel-pr-loop.sh:72-76`). It selects the newest loop directory with `ls -1d ... | sort -r | head -1` (`scripts/cancel-pr-loop.sh:75-76`). A loop is considered active only if the newest loop directory contains `state.md` (`scripts/cancel-pr-loop.sh:88-98`). Cancellation touches `.cancel-requested` and moves `state.md` to `cancel-state.md` (`scripts/cancel-pr-loop.sh:118-122`).
- inputs_outputs_state:
  Inputs are command-line flags, current working directory or `CLAUDE_PROJECT_DIR`, and `.humanize/pr-loop/<timestamp>/state.md`. It reads `current_round`, `max_iterations`, and `pr_number` from the active state file (`scripts/cancel-pr-loop.sh:104-112`). Outputs are status tokens on stdout: `NO_LOOP`, `NO_ACTIVE_LOOP`, or `CANCELLED` (`scripts/cancel-pr-loop.sh:78-81`, `95-97`, `128-130`). State transition is `state.md` present -> `.cancel-requested` present plus `cancel-state.md` present and `state.md` absent.
- gates_or_invariants:
  The script is PR-loop-only and does not touch `.humanize/rlcr/` (`scripts/cancel-pr-loop.sh:54-56`). It exits 1 if no newest loop directory exists or if the newest directory has no active `state.md` (`scripts/cancel-pr-loop.sh:78-82`, `91-98`). It uses `set -euo pipefail` (`scripts/cancel-pr-loop.sh:18`), so unexpected command failures abort.
- dependencies_and_callers:
  The slash command wrapper delegates all logic to this script and treats first-line status as authoritative (`commands/cancel-pr-loop.md:1-25`). `commands/start-pr-loop.md:58-62` documents user cancellation as a PR loop stopping condition. Setup scripts block starting RLCR/PR loops when a PR loop is active and instruct users to run `/humanize:cancel-pr-loop` (`scripts/setup-pr-loop.sh:220-240`, `scripts/setup-rlcr-loop.sh:306-312`). The PR stop hook presents cancel as an operator escape path for timeout, missing Codex, and bot-wait states (`hooks/pr-loop-stop-hook.sh:1169-1175`, `1309-1316`, `1399-1407`). The Codex skill docs expose the runtime path at `skills/humanize/SKILL.md:125-129`.
- edge_cases_or_failure_modes:
  `--force` is parsed but currently has no additional effect (`scripts/cancel-pr-loop.sh:39-41`). If the newest directory is already non-active but older directories contain active state, this script returns `NO_ACTIVE_LOOP` because it checks only the newest directory. If state keys are absent, display values default to `?` (`scripts/cancel-pr-loop.sh:109-112`). Existing `cancel-state.md` would be overwritten by `mv` behavior depending on platform and permissions; no explicit collision guard is present.
- validation_or_tests:
  Related tests in `tests/test-pr-loop-scripts.sh` validate help output, no-loop exit code/status, and active cancellation renaming from `state.md` to `cancel-state.md` (`tests/test-pr-loop-scripts.sh:181-239`). I did not run tests because the task requested research notes only in a read-only branch export.
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-069 `file` `tests/test-monitor-e2e-sigint.sh`
- cursor: `[_]`
- core_role:
  Executable specification wrapper for monitor SIGINT behavior. It selects a subset of the real monitor e2e suite focused on Ctrl+C/SIGINT handling for RLCR bash, RLCR zsh, and PR monitor modes.
- algorithmic_behavior:
  The file sources `tests/test-monitor-e2e-real.sh` and invokes exactly three test functions: `monitor_test_bash_sigint`, `monitor_test_zsh_sigint`, and `monitor_test_pr_sigint` (`tests/test-monitor-e2e-sigint.sh:4-14`). It prints a summary and exits 0 only when `TESTS_FAILED` is zero (`tests/test-monitor-e2e-sigint.sh:16-22`).
- inputs_outputs_state:
  Inputs are the sourced e2e helper script and the shell environment. The sourced helper creates temporary `.humanize/rlcr/<timestamp>/` and `.humanize/pr-loop/<timestamp>/` fixtures, fake `$HOME`/`XDG_CACHE_HOME` cache trees, `state.md`, `goal-tracker.md`, and log files. Outputs are pass/fail counters and process exit code. State under test is monitor process lifetime and terminal cleanup after SIGINT.
- gates_or_invariants:
  The wrapper depends on `set -euo pipefail` (`tests/test-monitor-e2e-sigint.sh:3`). The underlying bash SIGINT test sends `kill -INT` to the process group or process, waits with a bounded 20 * 0.5s loop, and then accepts either clean SIGINT exit or forced SIGTERM handling as pass if the monitor ran (`tests/test-monitor-e2e-real.sh:492-519`). It requires cleanup text or a clean `EXIT_CODE:[01]` and no glob errors (`tests/test-monitor-e2e-real.sh:529-549`). The zsh SIGINT test skips when zsh is unavailable, otherwise requires exit after SIGINT and no glob errors (`tests/test-monitor-e2e-real.sh:555-685`). The PR SIGINT test starts `humanize monitor pr` without `--once`, sends SIGINT, and requires clean exit evidence or proof the monitor ran before interruption, with no glob errors (`tests/test-monitor-e2e-real.sh:834-995`).
- dependencies_and_callers:
  It depends on real monitor functions in `scripts/humanize.sh`: `_humanize_monitor_codex` and `_humanize_monitor_pr`. The RLCR monitor installs cleanup traps and resets terminal scroll region (`scripts/humanize.sh:643-699`, `721-733`), checks loop directory deletion in active and no-log loops (`scripts/humanize.sh:775-840`, `948-951`), and dispatches through `humanize monitor rlcr|pr` (`scripts/humanize.sh:1108-1118`). It also depends on terminal command shims in the e2e helper so the real monitor can run non-interactively.
- edge_cases_or_failure_modes:
  SIGINT delivery differs between bash, zsh, and process groups; the tests account for this by allowing SIGTERM fallback in bash and PR monitor cases (`tests/test-monitor-e2e-real.sh:505-519`, `957-970`). zsh is optional and produces a skip when unavailable (`tests/test-monitor-e2e-real.sh:560-562`). Glob expansion failures such as `no matches found` and `bad pattern` are explicitly forbidden because these were known shell-compatibility hazards (`tests/test-monitor-e2e-real.sh:544-549`, `680-683`, `991-995`).
- validation_or_tests:
  The assigned file is itself the validation entrypoint. It delegates all assertions to `tests/test-monitor-e2e-real.sh` and reports aggregate pass/fail counts. I inspected but did not execute it because running it creates temp directories and processes, while the task requested research notes only.
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-099 `file` `prompt-template/block/git-not-clean-untracked.md`
- cursor: `[_]`
- core_role:
  Prompt block that defines the remediation contract when git state includes untracked files. It is a small behavior template for the “working tree not clean” gate rather than executable code.
- algorithmic_behavior:
  The block classifies untracked files as likely build artifacts, test outputs, runtime-generated files, dependencies, editor metadata, logs, caches, or temp files (`prompt-template/block/git-not-clean-untracked.md:2-8`). It instructs the agent/operator to review untracked files and add appropriate patterns to `.gitignore` (`prompt-template/block/git-not-clean-untracked.md:10`).
- inputs_outputs_state:
  Input is an upstream git cleanliness check that has detected untracked files. Output is prompt guidance appended to a larger prompt or gate message. State transition intended by the template is not “commit untracked files”; it is “classify untracked artifacts and update ignore policy if appropriate.”
- gates_or_invariants:
  Invariant: generated or dependency-like untracked files should usually be ignored instead of committed (`prompt-template/block/git-not-clean-untracked.md:2-8`). The template does not itself decide whether a file is safe; it requires review.
- dependencies_and_callers:
  Direct callers were not resolved in the assigned-file inspection, but the path and content indicate it is a reusable prompt-template block consumed by whichever command/hook builds git-not-clean remediation prompts. It coordinates with repository-level git status gates such as monitor status parsing in `scripts/humanize.sh`, which counts untracked files for display (`scripts/humanize.sh:170-215`, `563-574`), but this block is not invoked by the monitor display itself.
- edge_cases_or_failure_modes:
  Misclassification risk is high if untracked source files are assumed to be artifacts. The template mitigates this by saying “typically” and “review untracked files” rather than always ignore. It does not mention generated files that should be committed, such as lockfiles or migration files.
- validation_or_tests:
  No direct test was found for this exact prompt block during assigned inspection. Its behavior is validated only indirectly by prompt assembly or git cleanliness workflows elsewhere. Because it defines an algorithmic gate response but is not executable, test coverage appears indirect.
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-129 `file` `prompt-template/claude/finalize-phase-skipped-prompt.md`
- cursor: `[_]`
- core_role:
  Claude prompt template for the Finalize Phase when code review was skipped. It defines fallback validation and completion obligations after the normal review gate cannot run.
- algorithmic_behavior:
  The template injects `{{REVIEW_SKIP_REASON}}` as a warning (`prompt-template/claude/finalize-phase-skipped-prompt.md:1-5`). It instructs manual verification: review code changes, run available tests, and check common quality issues (`prompt-template/claude/finalize-phase-skipped-prompt.md:7-14`). It optionally routes work through a `code-simplifier:code-simplifier` Task subagent, focused on changes from `{{BASE_BRANCH}}` to `{{START_BRANCH}}` (`prompt-template/claude/finalize-phase-skipped-prompt.md:15-24`).
- inputs_outputs_state:
  Template inputs are `{{REVIEW_SKIP_REASON}}`, `{{BASE_BRANCH}}`, `{{START_BRANCH}}`, `{{PLAN_FILE}}`, `{{GOAL_TRACKER_FILE}}`, and `{{FINALIZE_SUMMARY_FILE}}`. Outputs expected from Claude are completed task statuses, a commit, and a finalize summary written to the specified file (`prompt-template/claude/finalize-phase-skipped-prompt.md:35-50`). State transition is from “review skipped / implementation not fully validated” into “finalize with manual verification evidence.”
- gates_or_invariants:
  The constraints are explicit and non-negotiable: must not change existing functionality, must not fail existing tests, must not introduce bugs, and only functionality-equivalent simplification/cleanup is allowed (`prompt-template/claude/finalize-phase-skipped-prompt.md:26-34`). Before exit, all tasks must be marked completed via TaskUpdate, changes must be committed, and a summary must include work done, modified files, test confirmation if possible, and manual verification notes (`prompt-template/claude/finalize-phase-skipped-prompt.md:40-50`).
- dependencies_and_callers:
  The template depends on the broader RLCR prompt engine to substitute placeholders and provide TaskUpdate/Task tools. It references plan and goal tracker files as authoritative context (`prompt-template/claude/finalize-phase-skipped-prompt.md:35-39`). It also depends on a `code-simplifier:code-simplifier` agent being available if the optional simplification path is used (`prompt-template/claude/finalize-phase-skipped-prompt.md:15-24`).
- edge_cases_or_failure_modes:
  If review is skipped for infrastructure reasons, the prompt still requires manual verification but cannot guarantee equivalence. If tests are unavailable or cannot run, the summary may only say “if possible” for tests (`prompt-template/claude/finalize-phase-skipped-prompt.md:46-50`), leaving residual risk. Optional simplification could introduce change despite constraints, so the non-functional-change invariant is central.
- validation_or_tests:
  No direct test was found for this exact template in assigned inspection. It is a behavior contract consumed by the prompt-generation path and should be validated by template rendering tests or e2e skipped-review flows if present.
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-159 `file` `tests/robustness/test-goal-tracker-robustness.sh`
- cursor: `[_]`
- core_role:
  Executable robustness specification for `humanize_parse_goal_tracker` in `scripts/humanize.sh`. It protects monitor progress accounting against malformed, large, partial, and unusual `goal-tracker.md` inputs.
- algorithmic_behavior:
  The test sources `tests/test-helpers.sh`, then the production `scripts/humanize.sh`, and calls `setup_test_dir` (`tests/robustness/test-goal-tracker-robustness.sh:15-24`). It documents the parser return schema as `total_acs|completed_acs|active_tasks|completed_tasks|deferred_tasks|open_issues|goal_summary` (`tests/robustness/test-goal-tracker-robustness.sh:31-37`). `parse_result` splits fields by pipe using `cut` (`tests/robustness/test-goal-tracker-robustness.sh:38-51`). The production function counts ACs in list/table formats, active table rows excluding completed/deferred statuses, completed tasks, unique completed ACs, deferred tasks, open issues, and first Ultimate Goal content line (`scripts/humanize.sh:36-118`).
- inputs_outputs_state:
  Inputs are generated fixture files under `$TEST_DIR`, each representing a goal tracker variant. Output is pass/fail test accounting from helper functions and final test summary (`tests/robustness/test-goal-tracker-robustness.sh:526-531`). The parsed state feeds monitor display fields for AC progress, tasks, deferred work, issues, and goal summary via `_draw_status_bar` (`scripts/humanize.sh:407-417`, `551-580`).
- gates_or_invariants:
  The parser must return defaults for missing files: `0|0|0|0|0|0|No goal tracker` (`tests/robustness/test-goal-tracker-robustness.sh:237-244`, implemented at `scripts/humanize.sh:39-43`). It must count standard list ACs (`tests/robustness/test-goal-tracker-robustness.sh:60-87`), table ACs (`89-116`), active tasks excluding completed/deferred (`118-153`), completed task rows and unique completed ACs (`155-202`), open issues (`373-409`), deferred tasks (`411-439`), mixed bold AC forms (`477-499`), and large AC counts of 60 without overflow (`258-279`). It must degrade gracefully for empty, malformed, truncated, binary-mixed, and headers-only files (`246-257`, `304-371`, `441-475`).
- dependencies_and_callers:
  The test directly depends on `humanize_parse_goal_tracker` from `scripts/humanize.sh` (`tests/robustness/test-goal-tracker-robustness.sh:21-22`). The parser is called by `_humanize_monitor_codex` through `_parse_goal_tracker` (`scripts/humanize.sh:369-372`) and feeds the monitor status bar (`scripts/humanize.sh:407-417`, `557-580`). It also appears in another robustness test path for hook input handling (`rg` found `tests/robustness/test-hook-input-robustness.sh:402`).
- edge_cases_or_failure_modes:
  The parser relies on section headers such as `### Acceptance Criteria`, `#### Active Tasks`, `### Completed and Verified`, `### Explicitly Deferred`, and `### Open Issues`; malformed files without proper headers should return zero ACs (`tests/robustness/test-goal-tracker-robustness.sh:304-326`). AC sub-numbering like `AC-3.1` is not expected to count under the current regex (`tests/robustness/test-goal-tracker-robustness.sh:477-495`). Pipe-delimited output can be fragile if `goal_summary` itself contains `|`; the test suite does not cover that. Binary content is only required to preserve at least one parseable AC, not full recovery (`tests/robustness/test-goal-tracker-robustness.sh:349-371`).
- validation_or_tests:
  The assigned file is the validation suite. It defines 18 tests and exits with the helper summary result (`tests/robustness/test-goal-tracker-robustness.sh:60-531`). I inspected it but did not execute it because the run instruction was research-only and the branch export is read-only.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `6/6; exactly one Item Evidence section was written for each assigned row`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`