# agent_27 dev-rlcr-with-swarm-team 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `0d5f0943ae9b1f80c5115aa946ebeb289e2cb83d`

## Item Evidence

### DEV_RLCR_WITH_SWARM_TEAM-HZ-027 `file` `hooks/loop-edit-validator.sh`
- cursor: `[_]`
- core_role: PreToolUse `Edit` gate for RLCR and PR-loop managed files; it prevents Claude from mutating generated prompts, loop state, protected trackers, and wrong-round artifacts.
- algorithmic_behavior: Reads hook JSON from stdin, exits early unless `.tool_name` is `Edit`, lowercases `tool_input.file_path`, extracts `session_id`, then runs ordered path gates: todos/prompt suffix checks, PR-loop protection, RLCR active-loop discovery, strict state parsing, state/plan/goal/summary validation; see `hooks/loop-edit-validator.sh:24`, `hooks/loop-edit-validator.sh:41`, `hooks/loop-edit-validator.sh:60`, `hooks/loop-edit-validator.sh:86`, `hooks/loop-edit-validator.sh:106`.
- inputs_outputs_state: Input is Claude hook JSON with `tool_name`, `tool_input.file_path`, optional `session_id`; outputs are exit `0` allow, exit `2` user-correctable block with rendered message, or exit `1` on malformed state fail-closed; it reads active `state.md` or `finalize-state.md` but does not mutate state.
- gates_or_invariants: `round-*-prompt.md` edits are always blocked; `round-*-todos.md` edits are blocked unless in the hardcoded active-loop allowlist; PR-loop `state.md` and generated comment/prompt/check/feedback files are read-only; RLCR `state.md`, `finalize-state.md`, and `plan.md` backups are blocked; `goal-tracker.md` is editable only in round `0`; summary file round must match current round unless allowlisted.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` for `find_active_loop`, `resolve_active_state_file`, `parse_state_file_strict`, path classifiers, allowlist checks, PR-round validation, and template-backed block messages; depends on `jq`, `sed`, `basename`, and `CLAUDE_PROJECT_DIR`/`PROJECT_ROOT` environment resolution.
- edge_cases_or_failure_modes: Because suffix checks run before confirming `.humanize/rlcr`, files named like `round-N-prompt.md` outside the loop are still blocked; malformed JSON can terminate under `set -e`; no active loop permits most `.humanize/rlcr` edits after early gates; malformed active state blocks all protected RLCR edits; `finalize-state.md` must be checked before generic `state.md` because the generic matcher also matches it.
- validation_or_tests: Related tests are discoverable in `tests/test-allowlist-validators.sh`, `tests/test-finalize-phase.sh`, `tests/test-session-id.sh`, and robustness tests that exercise the shared functions used here; direct behavior is shaped by `hooks/lib/loop-common.sh:180`, `hooks/lib/loop-common.sh:233`, `hooks/lib/loop-common.sh:386`, `hooks/lib/loop-common.sh:520`, `hooks/lib/loop-common.sh:542`, `hooks/lib/loop-common.sh:962`.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-057 `file` `tests/test-helpers.sh`
- cursor: `[_]`
- core_role: Shared shell test harness for executable specs; it standardizes result accounting, temporary directory setup, and mock Git repository initialization.
- algorithmic_behavior: Defines color constants and counters, then exposes `pass`, `fail`, `skip`, `print_test_summary`, `setup_test_dir`, and `init_test_git_repo`; counters are incremented by assertion helpers and summary returns success only when failures equal zero; see `tests/test-helpers.sh:22`, `tests/test-helpers.sh:30`, `tests/test-helpers.sh:58`.
- inputs_outputs_state: Inputs are assertion labels and optional expected/got text; output is human-readable PASS/FAIL/SKIP plus process return status from `print_test_summary`; state is kept in global `TESTS_PASSED`, `TESTS_FAILED`, `TESTS_SKIPPED`, and `TEST_DIR`.
- gates_or_invariants: Test scripts using this file can gate CI by exiting with `print_test_summary`; `setup_test_dir` installs an EXIT trap to clean the generated directory; `init_test_git_repo` creates a real Git repo with local identity and an initial commit.
- dependencies_and_callers: Used by robustness and integration shell tests via `source`; depends on `mktemp`, `trap`, `git`, `mkdir`, `cd`, and shell globals; no production hook calls this file.
- edge_cases_or_failure_modes: `setup_test_dir` overwrites any existing `TEST_DIR` variable and trap; `init_test_git_repo` changes directories and assumes Git is available; trap command is not strongly quoted, though `mktemp -d` normally returns safe paths.
- validation_or_tests: This file is not itself tested here, but it is the assertion substrate for `tests/robustness/test-state-transition-robustness.sh:17` and other robustness suites.
- skip_candidate: `yes: support harness only; it contains no production RLCR state transition logic, but is required to interpret assigned executable specs`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-087 `file` `prompt-template/block/git-status-failed.md`
- cursor: `[_]`
- core_role: Fail-closed block template used when the stop hook cannot verify repository cleanliness with `git status`.
- algorithmic_behavior: Provides a rendered diagnostic headed “Git Status Failed,” interpolating `{{GIT_STATUS_EXIT}}`, then lists likely causes and tells the user to run git status manually; see `prompt-template/block/git-status-failed.md:1`.
- inputs_outputs_state: Input is template variable `GIT_STATUS_EXIT`; output is Markdown block text returned inside the stop-hook JSON decision; it carries no persistent state.
- gates_or_invariants: Supports the invariant that review/loop continuation is blocked when repository state cannot be verified; the hook treats git status timeout/failure as unsafe rather than proceeding.
- dependencies_and_callers: Loaded by `load_and_render_safe` from `hooks/loop-codex-stop-hook.sh:443` after `run_with_timeout git status --porcelain` fails at `hooks/loop-codex-stop-hook.sh:432`; rendering semantics come from `hooks/lib/template-loader.sh:170`.
- edge_cases_or_failure_modes: If the placeholder is not supplied it remains literal by template-loader design; if the template is missing the caller uses an inline fallback; this template does not include timeout duration or raw stderr, only exit code and generic causes.
- validation_or_tests: Indirectly validated by stop-hook behavior around `GIT_STATUS_EXIT` handling at `hooks/loop-codex-stop-hook.sh:434`; no direct template unit test was found in the inspected references.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-117 `file` `prompt-template/claude/open-question-notice.md`
- cursor: `[_]`
- core_role: Prompt notice that changes the next Claude round contract when Codex review output contains open questions.
- algorithmic_behavior: Static Markdown instructs Claude to use `AskUserQuestion` before resolving other Codex findings; the stop hook injects it only when `ASK_CODEX_QUESTION` is `true` and a short line contains `Open Question`; see `prompt-template/claude/open-question-notice.md:1` and `hooks/loop-codex-stop-hook.sh:1564`.
- inputs_outputs_state: Input is presence of detected open-question text in `REVIEW_RESULT_FILE`; output is inserted prompt text in `NEXT_PROMPT_FILE`; no state file is changed by the template itself.
- gates_or_invariants: Establishes a human-clarification gate: open questions must be asked before normal finding resolution proceeds.
- dependencies_and_callers: Loaded with `load_template "$TEMPLATE_DIR" "claude/open-question-notice.md"` at `hooks/loop-codex-stop-hook.sh:1577`; injection is performed by an `awk` rewrite after the Codex review-result end marker and separator at `hooks/loop-codex-stop-hook.sh:1581`.
- edge_cases_or_failure_modes: Detection is heuristic: line length must be under 40 and contain exact substring `Open Question`, so longer headings or differently cased text may be missed; if template loading returns empty, the hook has an inline fallback.
- validation_or_tests: The relevant behavioral surface is in the stop hook’s detection and insertion block at `hooks/loop-codex-stop-hook.sh:1566`; no direct test for this template was found in inspected references.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-147 `file` `tests/robustness/test-state-transition-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for RLCR state parsing, active-loop selection, finalize/cancel handling, and state-schema rejection.
- algorithmic_behavior: Sources `hooks/lib/loop-common.sh` and test helpers, creates temporary loop directories, writes representative `state.md`, `finalize-state.md`, and `cancel-state.md`, then asserts parser and discovery results across 16 cases; setup and helper writers are at `tests/robustness/test-state-transition-robustness.sh:14`, `tests/robustness/test-state-transition-robustness.sh:30`, `tests/robustness/test-state-transition-robustness.sh:54`, `tests/robustness/test-state-transition-robustness.sh:74`.
- inputs_outputs_state: Inputs are generated frontmatter fixtures under `TEST_DIR`; outputs are PASS/FAIL lines and final exit status from `print_test_summary`; state transitions are simulated by file presence/renaming patterns rather than by production mutation code.
- gates_or_invariants: Specifies that round `0`, arbitrary positive rounds, and `round == max_iterations` parse; `finalize-state.md` makes a loop active; `cancel-state.md` is terminal and not active; newer active loop beats older terminal loop; nonnumeric and missing required fields are rejected by `parse_state_file_strict`; nested state files are ignored.
- dependencies_and_callers: Depends on `find_active_loop`, `get_current_round`, and `parse_state_file_strict` from `hooks/lib/loop-common.sh:233`, `hooks/lib/loop-common.sh:296`, `hooks/lib/loop-common.sh:386`; depends on test counters and temp cleanup from `tests/test-helpers.sh:86`.
- edge_cases_or_failure_modes: Documents intentional laxness: negative rounds are parsed by `get_current_round` and strict parser regex allows signed numbers; rounds above `max_iterations` parse because enforcement is elsewhere; active-loop discovery is lexicographic and only checks expected one-level loop directories; Test 5 only proves finalize file coexistence, not actual `resolve_active_state_file` precedence.
- validation_or_tests: Contains its own validation cases: valid progression at lines `98-138`, finalize at `148-172`, cancel at `182-207`, invalid/schema cases at `217-361`, and directory discovery at `371-417`; exits with the shared summary at `tests/robustness/test-state-transition-robustness.sh:423`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5 unique item sections above; item IDs appear as section headings only
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`