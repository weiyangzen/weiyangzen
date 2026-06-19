# agent_23 claude/add-dependency-check-tA0P8 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `df26142e5fbed5e2ac3e48f001786cfa77296dda`

## Item Evidence

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-023 `file` `commands/cancel-pr-loop.md`
- cursor: `[_]`
- core_role: Slash-command workflow definition for canceling an active PR loop. It is a thin command contract that delegates all behavior to `scripts/cancel-pr-loop.sh`, not an implementation file.
- algorithmic_behavior: The command instructs the agent to run `"${CLAUDE_PLUGIN_ROOT}/scripts/cancel-pr-loop.sh"` and classify the first output line as `NO_LOOP`, `NO_ACTIVE_LOOP`, or `CANCELLED` (`commands/cancel-pr-loop.md:11-20`). It explicitly defines the active-loop predicate: `state.md` must exist in the newest `.humanize/pr-loop/` directory (`commands/cancel-pr-loop.md:21`).
- inputs_outputs_state: Input is ambient plugin/project state plus optional `--force` through the allowed tool list (`commands/cancel-pr-loop.md:3`). Output is user-facing prose derived from the script's first-line status. State transition is implemented by the script: newest PR-loop `state.md` is moved to `cancel-state.md` and `.cancel-requested` is created (`scripts/cancel-pr-loop.sh:118-123`).
- gates_or_invariants: The command must not implement cancellation itself; the script is authoritative (`commands/cancel-pr-loop.md:21`). It preserves the loop directory for comments, summaries, and state (`commands/cancel-pr-loop.md:23`). It is scoped only to PR loops and must not affect `.humanize/rlcr/` (`commands/cancel-pr-loop.md:25`).
- dependencies_and_callers: Depends on `CLAUDE_PLUGIN_ROOT` resolving to the plugin root and on `scripts/cancel-pr-loop.sh`. The script uses `CLAUDE_PROJECT_DIR` or `pwd` for the project root, locates `.humanize/pr-loop`, selects newest directory by reverse sort, and parses `current_round`, `max_iterations`, and `pr_number` from state (`scripts/cancel-pr-loop.sh:72-107`).
- edge_cases_or_failure_modes: No loop directory yields `NO_LOOP` and exit 1 (`scripts/cancel-pr-loop.sh:76-82`). Existing loop directory without `state.md` yields `NO_ACTIVE_LOOP` and exit 1 (`scripts/cancel-pr-loop.sh:88-98`). Unknown script options exit 3 (`scripts/cancel-pr-loop.sh:60-64`). Missing state fields degrade to `?` in the cancellation message (`scripts/cancel-pr-loop.sh:104-112`).
- validation_or_tests: Not directly tested by this assigned file, but the implementation exposes deterministic status tags and exit codes documented in the script (`scripts/cancel-pr-loop.sh:11-15`), which match the command's output dispatch contract.
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-053 `file` `tests/setup-fixture-mock-gh.sh`
- cursor: `[_]`
- core_role: Test fixture generator for PR-loop GitHub API algorithms. It creates a fixture-backed `gh` executable so PR comment fetch/poll scripts can be tested without network calls.
- algorithmic_behavior: Takes `<mock_bin_dir> <fixtures_dir>`, validates both, creates `mock_bin_dir`, writes an executable `gh` script, and prints the mock bin directory (`tests/setup-fixture-mock-gh.sh:16-24`, `tests/setup-fixture-mock-gh.sh:99-101`). The mock dispatches on the first CLI word: `auth`, `repo`, `pr`, or `api` (`tests/setup-fixture-mock-gh.sh:33-93`).
- inputs_outputs_state: Inputs are output bin directory and fixture directory (`tests/setup-fixture-mock-gh.sh:6`, `tests/setup-fixture-mock-gh.sh:16-17`). Output is `$MOCK_BIN_DIR/gh`, made executable, plus stdout containing the directory path. The generated mock returns JSON for `gh api user`, repository metadata, PR number/state, and three PR comment endpoint families.
- gates_or_invariants: Missing arguments fail with usage and exit 1 (`tests/setup-fixture-mock-gh.sh:19-22`). Endpoint routing must map `/issues/*/comments` to `issue_comments.json`, `/pulls/*/comments` to `review_comments.json`, and `/pulls/*/reviews` to `pr_reviews.json` (`tests/setup-fixture-mock-gh.sh:71-86`). Unrecognized commands fail closed with exit 1 (`tests/setup-fixture-mock-gh.sh:95-96`).
- dependencies_and_callers: Called by `setup_fixture_mock_gh` in `tests/test-pr-loop-hooks.sh`, which prepends the generated bin dir to `PATH` before invoking `scripts/fetch-pr-comments.sh` and `scripts/poll-pr-reviews.sh` (`tests/test-pr-loop-hooks.sh:1231-1251`, `tests/test-pr-loop-hooks.sh:1329-1334`). It depends on fixture files under `tests/fixtures/`, including approval-only PR reviews with empty/null bodies (`tests/fixtures/pr_reviews.json:1-21`).
- edge_cases_or_failure_modes: The generated `repo view` mock has simplified matching against the complete argument string and may emit different JSON depending on whether args include `owner,name`, `parent`, `owner`, or `name` (`tests/setup-fixture-mock-gh.sh:40-52`). Default unknown API endpoint returns an empty array instead of failure (`tests/setup-fixture-mock-gh.sh:89-91`), so callers can exercise empty-comment behavior.
- validation_or_tests: Fixture-backed tests assert all comment types are captured, including human issue comments, inline review comments, and approval-only PR reviews rendered as `[Review state: APPROVED]` (`tests/test-pr-loop-hooks.sh:1242-1283`). Additional tests verify `--after` filtering and poll JSON structure with bot response detection (`tests/test-pr-loop-hooks.sh:1287-1419`).
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-083 `file` `tests/test-skill-monitor.sh`
- cursor: `[_]`
- core_role: Executable specification for the `.humanize/skill` monitor algorithm, especially `humanize monitor skill --once`. It verifies aggregation, focus selection, metadata parsing, output selection, and directory filtering.
- algorithmic_behavior: Creates isolated git repos, sources `scripts/humanize.sh`, and constructs synthetic skill invocation directories under `.humanize/skill/<timestamp-id>` (`tests/test-skill-monitor.sh:35-54`, `tests/test-skill-monitor.sh:56-104`). Invocations contain `input.md`, optional `metadata.md`, and optional `output.md`; status controls whether the monitor treats an invocation as completed or running.
- inputs_outputs_state: Inputs are filesystem state under `.humanize/skill`, metadata fields `model`, `effort`, `timeout`, `exit_code`, `duration`, `status`, and question text under `## Question` (`tests/test-skill-monitor.sh:69-97`). Output is the `--once` report printed by `_humanize_monitor_skill`, which includes total counts, status buckets, focused invocation, model, duration, question, watched output, and recent invocations.
- gates_or_invariants: Missing `.humanize/skill` must return nonzero and mention directory absence (`tests/test-skill-monitor.sh:112-118`). Empty skill directory must return nonzero and mention no invocations (`tests/test-skill-monitor.sh:126-133`). Only timestamp-shaped directories are counted (`tests/test-skill-monitor.sh:375-389`). Multi-line questions expose only the first nonblank question line (`tests/test-skill-monitor.sh:301-346`).
- dependencies_and_callers: Tests `_humanize_monitor_skill`, which is dispatched by `humanize monitor skill` (`scripts/humanize.sh:1108-1121`) and sourced from `scripts/lib/monitor-skill.sh` (`scripts/humanize.sh:1587-1590`). The implementation lists timestamp directories newest-first (`scripts/lib/monitor-skill.sh:42-53`), counts statuses from metadata (`scripts/lib/monitor-skill.sh:82-105`), extracts question text (`scripts/lib/monitor-skill.sh:107-114`), and chooses the best monitored file (`scripts/lib/monitor-skill.sh:127-167`).
- edge_cases_or_failure_modes: Running invocation is represented by missing `metadata.md` and should count as `Running: 1` (`tests/test-skill-monitor.sh:249-267`). `empty_response` status increments `Empty` and shows no output (`tests/test-skill-monitor.sh:352-369`). Multiple invocations should focus the newest watchable invocation and count mixed `success`, `error`, and `timeout` states (`tests/test-skill-monitor.sh:198-243`).
- validation_or_tests: This file is itself the validator and is included in the top-level test runner (`tests/run-all-tests.sh:61-65`). It exits 1 if any local assertion fails (`tests/test-skill-monitor.sh:395-404`).
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-113 `file` `prompt-template/block/prompt-file-write.md`
- cursor: `[_]`
- core_role: Prompt/block template that enforces a write-protection gate on generated round prompt files.
- algorithmic_behavior: Tells the agent it cannot write to `round-*-prompt.md` files because those files contain instructions from Codex to Claude (`prompt-template/block/prompt-file-write.md:1-7`). It redirects permitted work to reading the current prompt, executing tasks, and writing results to the summary file (`prompt-template/block/prompt-file-write.md:7-10`).
- inputs_outputs_state: Input is an attempted or relevant operation against `round-*-prompt.md`. Output is a refusal/redirect instruction in the generated prompt. The only allowed state transition is summary-file output; prompt-file mutation is disallowed.
- gates_or_invariants: Instruction immutability is the invariant: "You cannot modify your own instructions" (`prompt-template/block/prompt-file-write.md:7`). If the prompt is wrong, the agent must document that in the summary file rather than patching the prompt (`prompt-template/block/prompt-file-write.md:12`).
- dependencies_and_callers: Depends on the surrounding prompt assembly system injecting this block when prompt-file writes are detected or forbidden. It coordinates with round prompt/summary workflow conventions, but the assigned file itself has no shell dependencies.
- edge_cases_or_failure_modes: If a prompt contains an error, the template prevents direct repair and routes the issue to the summary file (`prompt-template/block/prompt-file-write.md:12`). A failure mode would be omission from a prompt generation path, since the block is declarative and not self-enforcing.
- validation_or_tests: No direct test discovered in the assigned subset. Its behavior is a prompt-level gate, not executable logic.
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-143 `file` `prompt-template/pr-loop/critical-requirements-has-comments.md`
- cursor: `[_]`
- core_role: PR-loop prompt block defining completion gates after review comments exist. It turns comment resolution into a commit/push/re-review workflow contract.
- algorithmic_behavior: On work completion, the agent must commit and push changes, comment on the PR with `{{BOT_MENTION_STRING}} please review`, and write a resolution summary to `{{RESOLVE_PATH}}` (`prompt-template/pr-loop/critical-requirements-has-comments.md:6-17`). The stop hook then polls for bot reviews (`prompt-template/pr-loop/critical-requirements-has-comments.md:23`).
- inputs_outputs_state: Template inputs are `{{PR_NUMBER}}`, `{{BOT_MENTION_STRING}}`, and `{{RESOLVE_PATH}}`. Outputs are a git commit/push, a `gh pr comment` trigger, and a resolution summary containing issues addressed, modified files, and tests added if any (`prompt-template/pr-loop/critical-requirements-has-comments.md:18-22`).
- gates_or_invariants: Work is not considered complete until all three required surfaces are produced: remote branch updated, PR review retriggered, and resolution summary written (`prompt-template/pr-loop/critical-requirements-has-comments.md:6-17`). The stop hook's polling phase depends on this trigger being posted.
- dependencies_and_callers: Depends on git, remote push permissions, GitHub CLI, PR number interpolation, bot mention interpolation, and a valid resolve-summary path. It coordinates with PR-loop stop-hook polling and review comment fetch/poll scripts.
- edge_cases_or_failure_modes: Missing push, missing PR trigger comment, or missing summary leaves the PR loop without a proper re-review transition. Bad template interpolation would produce an invalid `gh pr comment` command or write to the wrong summary path.
- validation_or_tests: Indirectly covered by PR-loop hook/system tests that exercise re-review polling and comment detection. No direct unit test of this template block was found in the assigned files.
- skip_candidate: `no`

### CLAUDE__ADD_DEPENDENCY_CHECK_TA0P8-HZ-173 `file` `tests/robustness/test-timeout-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for the portable timeout abstraction used by setup scripts, ask-codex, PR loop, RLCR loop, and hook robustness tests.
- algorithmic_behavior: Sources `scripts/portable-timeout.sh` and `tests/test-helpers.sh`, then validates timeout implementation discovery and `run_with_timeout` behavior across success, timeout, command arguments, exit-code propagation, pipelines, edge timeout values, output volume, rapid cycles, missing commands, special characters, signals, subshells, and environment export (`tests/robustness/test-timeout-robustness.sh:14-18`, `tests/robustness/test-timeout-robustness.sh:31-272`).
- inputs_outputs_state: Inputs are timeout seconds plus command/args passed to `run_with_timeout`. Outputs are stdout/stderr from the wrapped command and exit codes, with `124` as the expected timeout code when a timeout implementation exists (`tests/robustness/test-timeout-robustness.sh:62-77`). The sourced script sets and exports `TIMEOUT_IMPL` (`scripts/portable-timeout.sh:29`, `scripts/portable-timeout.sh:73-76`).
- gates_or_invariants: `TIMEOUT_IMPL` must be one of `gtimeout`, `timeout`, `python3`, `python`, or `none` (`tests/robustness/test-timeout-robustness.sh:41-49`). Quick commands must complete normally (`tests/robustness/test-timeout-robustness.sh:51-60`). Successful nonzero exits must be preserved (`tests/robustness/test-timeout-robustness.sh:89-100`). When timeout exists, long sleeps must return `124` quickly (`tests/robustness/test-timeout-robustness.sh:120-137`).
- dependencies_and_callers: Tests `detect_timeout_impl` and `run_with_timeout`. The implementation selects `gtimeout`, GNU `timeout`, Python fallback, or no-timeout mode in priority order (`scripts/portable-timeout.sh:9-27`) and dispatches accordingly (`scripts/portable-timeout.sh:31-71`). `run_with_timeout` is used by setup scripts and ask-codex for git, gh, Codex, and polling timeouts.
- edge_cases_or_failure_modes: Zero timeout may either succeed or immediately timeout and both are accepted (`tests/robustness/test-timeout-robustness.sh:139-155`). Empty command is considered handled regardless of exit code (`tests/robustness/test-timeout-robustness.sh:201-209`). Signal-handling command may return `0` or `124` (`tests/robustness/test-timeout-robustness.sh:221-233`). If no timeout implementation exists, long-running commands are skipped as timeout assertions and the wrapper runs without enforcement (`scripts/portable-timeout.sh:64-68`).
- validation_or_tests: This file is included in `tests/run-all-tests.sh` robustness coverage (`tests/run-all-tests.sh:65-75`) and exits through `print_test_summary`, returning nonzero on failures (`tests/robustness/test-timeout-robustness.sh:274-279`).
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6 unique item headings above, matching the assigned count
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`