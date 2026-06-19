# agent_20 ask-codex-skill 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `caf375a20530c8bb81e8e8e103a8598c25c11bb0`
- research_scope: read-only inspection; no files modified

## Item Evidence

### ASK_CODEX_SKILL-HZ-020 `file` `commands/cancel-pr-loop.md`
- cursor: `[_]`
- core_role: Slash-command workflow contract for canceling a PR review loop. The command front matter restricts execution to `scripts/cancel-pr-loop.sh` with optional `--force` only, via `allowed-tools` at `commands/cancel-pr-loop.md:1-5`.
- algorithmic_behavior: The command delegates all cancellation logic to the script and requires the agent to inspect the first output line: `NO_LOOP` / `NO_ACTIVE_LOOP` maps to “No active PR loop found,” while `CANCELLED` means report the cancellation output (`commands/cancel-pr-loop.md:11-20`). The active-loop invariant is explicitly “`state.md` exists in the newest PR loop directory” (`commands/cancel-pr-loop.md:21`).
- inputs_outputs_state: Inputs are implicit plugin/project context plus the newest `.humanize/pr-loop/<timestamp>/state.md`. The called script resolves `PROJECT_ROOT` from `CLAUDE_PROJECT_DIR` or `pwd`, finds the newest loop directory, checks `state.md`, creates `.cancel-requested`, then moves `state.md` to `cancel-state.md` (`scripts/cancel-pr-loop.sh:72-123`). Output is a status token plus human-readable detail (`scripts/cancel-pr-loop.sh:128-130`).
- gates_or_invariants: The command is intentionally PR-only and states RLCR loops are unaffected (`commands/cancel-pr-loop.md:25`). Loop artifacts are preserved for reference (`commands/cancel-pr-loop.md:23`). Direct state edits are avoided by command design; cancellation is script-mediated.
- dependencies_and_callers: Depends on `scripts/cancel-pr-loop.sh`. `commands/start-pr-loop.md:58-62` lists `/humanize:cancel-pr-loop` as one of the loop stopping paths. Setup messaging also points users to this cancel command when an active PR loop blocks another setup.
- edge_cases_or_failure_modes: No loop directory produces `NO_LOOP` and exit code 1; a newest loop directory without `state.md` produces `NO_ACTIVE_LOOP` and exit code 1 (`scripts/cancel-pr-loop.sh:78-98`). `--force` is parsed but currently has no additional effect (`scripts/cancel-pr-loop.sh:24-31`, `scripts/cancel-pr-loop.sh:39-41`). If the newest directory is stale but an older one has `state.md`, the script still reports no active loop because it only checks the newest directory.
- validation_or_tests: `tests/test-pr-loop-scripts.sh:181-252` validates help output, no-loop behavior, and active-loop cancellation including the `state.md` to `cancel-state.md` transition.
- skip_candidate: `no`

### ASK_CODEX_SKILL-HZ-050 `file` `tests/setup-monitor-test-env.sh`
- cursor: `[_]`
- core_role: Executable fixture generator for PR monitor state parsing tests. It creates controlled `.humanize/pr-loop/<timestamp>/state.md` files so monitor tests can exercise YAML-list bot state without going through validators (`tests/setup-monitor-test-env.sh:1-8`).
- algorithmic_behavior: Takes `<test_dir> <test_name>`, validates `test_dir`, dispatches on `test_name`, creates a loop session directory, and writes front matter for three monitor scenarios: full YAML list active bots, configured-vs-active subset, and empty `active_bots` (`tests/setup-monitor-test-env.sh:12-89`).
- inputs_outputs_state: Inputs are positional `TEST_DIR` and optional `TEST_NAME` defaulting to `default`, although `default` is not a supported case (`tests/setup-monitor-test-env.sh:12-20`). Outputs are a synthetic state file under `.humanize/pr-loop/` and a final echo of the test directory (`tests/setup-monitor-test-env.sh:91`). State fields include `current_round`, `max_iterations`, `pr_number`, `start_branch`, `configured_bots`, `active_bots`, `codex_model`, `codex_effort`, and `started_at`.
- gates_or_invariants: Missing `TEST_DIR` fails with usage and exit code 1 (`tests/setup-monitor-test-env.sh:15-18`). Unknown scenario names fail with an allowed-case list (`tests/setup-monitor-test-env.sh:84-87`). The fixture format preserves YAML-list indentation expected by the monitor parser.
- dependencies_and_callers: Called by `tests/test-pr-loop-hooks.sh:1552-1602`. Production behavior under test is `_humanize_monitor_pr`, whose parser extracts YAML-list `configured_bots` and `active_bots` with `sed`, defaults empty lists to `none`, and serializes display fields (`scripts/humanize.sh:1250-1279`).
- edge_cases_or_failure_modes: The empty fixture writes `active_bots:` with no list entries (`tests/setup-monitor-test-env.sh:77-80`), which parser defaults to `none` (`scripts/humanize.sh:1273-1274`). Current display code renders that as “all approved” rather than literal `none` (`scripts/humanize.sh:1347-1353`), while the test expects `Active Bots:.*none` (`tests/test-pr-loop-hooks.sh:1610-1614`), so this fixture exposes a likely assertion/display mismatch.
- validation_or_tests: The three generated states feed monitor tests for YAML-list parsing, configured bot display, and empty active bot handling (`tests/test-pr-loop-hooks.sh:1547-1621`).
- skip_candidate: `no`

### ASK_CODEX_SKILL-HZ-080 `file` `tests/test-template-loader.sh`
- cursor: `[_]`
- core_role: Executable specification for the shared template loading/rendering algorithm in `hooks/lib/template-loader.sh`. It sources the library directly and treats failures as process exit 1 (`tests/test-template-loader.sh:8-13`, `tests/test-template-loader.sh:641-659`).
- algorithmic_behavior: Tests `get_template_dir`, `load_template`, `render_template`, `load_and_render`, `load_and_render_safe`, and `validate_template_dir`. The production renderer is a single-pass AWK scanner using `{{VAR}}` placeholders populated through `TMPL_VAR_` environment variables (`hooks/lib/template-loader.sh:24-31`, `hooks/lib/template-loader.sh:36-47`, `hooks/lib/template-loader.sh:58-132`, `hooks/lib/template-loader.sh:170-222`).
- inputs_outputs_state: Inputs are template directory paths, template file names, fallback strings, and `VAR=value` substitutions. Outputs are rendered strings, warnings for missing files, pass/fail counters, and final exit status (`tests/test-template-loader.sh:20-34`, `tests/test-template-loader.sh:651-659`). It does not mutate repository state.
- gates_or_invariants: The spec requires existing templates to load, missing templates to return empty or fallback depending on function, unused substitutions to be no-ops, unreplaced placeholders to remain as-is, and valid template directories to contain expected subdirectories (`tests/test-template-loader.sh:41-243`).
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh`. Included in the aggregate test suite as the first test suite in `tests/run-all-tests.sh:31-34`. It indirectly guards all prompt-template consumers that use `load_and_render_safe`, including PR-loop setup and loop validation messages.
- edge_cases_or_failure_modes: Tests literal rendering of shell metacharacters including ampersands, backslashes, dollar signs, backticks, pipes, redirection, quotes, hashes, globs, JSON-like text, regex text, and multiline values (`tests/test-template-loader.sh:247-486`). It also verifies placeholder-injection prevention where injected values containing `{{OTHER_VAR}}` are not rescanned (`tests/test-template-loader.sh:488-543`), plus empty values, non-ASCII content, underscore-prefixed names, and numeric variable names (`tests/test-template-loader.sh:545-639`).
- validation_or_tests: This file is itself the validator. Key integration coverage includes rendering `block/wrong-round-number.md` with multiple variables (`tests/test-template-loader.sh:146-164`) and safe fallback behavior for missing templates (`tests/test-template-loader.sh:196-222`).
- skip_candidate: `no`

### ASK_CODEX_SKILL-HZ-110 `file` `prompt-template/block/summary-bash-write.md`
- cursor: `[_]`
- core_role: Prompt block used as a validator rejection message when an agent attempts to modify summary files through Bash instead of approved Write/Edit tooling.
- algorithmic_behavior: The template emits a short blocking instruction: do not use Bash commands to modify summary files, use the correct path, and avoid shell tools because they bypass validation hooks (`prompt-template/block/summary-bash-write.md:1-8`). `{{CORRECT_PATH}}` is the only substitution variable (`prompt-template/block/summary-bash-write.md:5`).
- inputs_outputs_state: Input is `CORRECT_PATH`, supplied by `summary_bash_blocked_message "$correct_summary_path"` (`hooks/lib/loop-common.sh:609-618`). Output is a rendered block sent to stderr by the Bash validator caller (`hooks/loop-bash-validator.sh:377`). It does not change loop state; it blocks an invalid write path.
- gates_or_invariants: Enforces the invariant that summary file writes must pass through Write/Edit tooling so round-number validation hooks can run. The template explicitly names `cat`, `echo`, `sed`, and `awk` as disallowed for this purpose (`prompt-template/block/summary-bash-write.md:7-8`).
- dependencies_and_callers: Loaded via `load_and_render_safe "$TEMPLATE_DIR" "block/summary-bash-write.md"` in `hooks/lib/loop-common.sh:617`. The template reference is also part of common-template existence checks in `tests/test-template-references.sh:152-167`.
- edge_cases_or_failure_modes: If the template is missing or empty, `loop-common.sh` has a fallback message with the same core instruction and `{{CORRECT_PATH}}` substitution (`hooks/lib/loop-common.sh:613-617`). If `CORRECT_PATH` is absent or malformed, the rendered guidance may be less actionable, but the block still prevents Bash-based summary writes.
- validation_or_tests: `tests/test-template-references.sh:152-167` asserts this common block template exists. `tests/test-template-loader.sh` validates the safe rendering and fallback machinery this block relies on.
- skip_candidate: `no`

### ASK_CODEX_SKILL-HZ-140 `file` `prompt-template/pr-loop/round-0-header.md`
- cursor: `[_]`
- core_role: Header template for the initial PR review loop prompt. It establishes Round 0 context, PR metadata, active bot display, and the handoff point for fetched review comments (`prompt-template/pr-loop/round-0-header.md:1-15`).
- algorithmic_behavior: `scripts/setup-pr-loop.sh` builds `TEMPLATE_VARS` for `PR_NUMBER`, `START_BRANCH`, `ACTIVE_BOTS_DISPLAY`, `RESOLVE_PATH`, and bot mentions, then renders this header with `load_and_render_safe` (`scripts/setup-pr-loop.sh:731-758`). The rendered header is written to `round-0-prompt.md`, and fetched comments are appended immediately after (`scripts/setup-pr-loop.sh:760-764`).
- inputs_outputs_state: Inputs are PR number, start branch, and active bots display. Output is the first section of `.humanize/pr-loop/<timestamp>/round-0-prompt.md`. It is followed by task content selected according to whether fetched comments contain the no-comments sentinel (`scripts/setup-pr-loop.sh:723-728`, `scripts/setup-pr-loop.sh:800-851`).
- gates_or_invariants: The header is Round 0-specific and frames the agent as monitoring feedback from remote review bots (`prompt-template/pr-loop/round-0-header.md:3-15`). It does not itself decide whether comments exist; that gate lives in `setup-pr-loop.sh` and affects the subsequent task template.
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh` through `load_and_render_safe`. Called only from `scripts/setup-pr-loop.sh:758` in the inspected references. Fallback header text in `setup-pr-loop.sh:740-755` mirrors the template if the file cannot be loaded.
- edge_cases_or_failure_modes: Missing template falls back to the embedded header (`scripts/setup-pr-loop.sh:740-758`). Missing substitution values remain visible as placeholders because the renderer preserves unreplaced variables, which is useful for diagnosis but could leak unresolved `{{...}}` into prompts. The header does not include `RESOLVE_PATH`; the later task template carries that operational instruction.
- validation_or_tests: Indirectly validated by template-loader coverage for `load_and_render_safe` and by PR-loop setup flows that render `round-0-prompt.md`. No dedicated assertion for this exact header content was found in the inspected assigned-scope references.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `5/5 item headings present; each assigned heading occurs once`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`