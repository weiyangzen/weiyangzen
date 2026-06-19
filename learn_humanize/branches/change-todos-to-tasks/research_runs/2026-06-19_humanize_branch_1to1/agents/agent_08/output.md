# agent_08 change-todos-to-tasks 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `0790d28514ab48bec2668f4ec069592872fed586`

## Item Evidence

### CHANGE_TODOS_TO_TASKS-HZ-008 `file` `README.md`
- cursor: `[_]`
- core_role: Top-level behavior documentation for Humanize/RLCR and PR-loop workflows. It defines the user-facing state machine: plan or draft input, Claude implementation, Codex summary review, final code review, and PR bot review loop. Key refs: `README.md:58-72`, `README.md:145-172`.
- algorithmic_behavior: Documents two main algorithms. RLCR loops from Claude implementation to Codex feedback until a complete signal, then runs `codex review --base <branch>` for severity-gated review. PR loop detects the current branch PR, fetches bot comments, lets Claude fix issues, pushes, triggers bot re-review, polls, runs local Codex validation, and repeats until approval or max iterations.
- inputs_outputs_state: Inputs include a plan file or generated plan draft, command options such as `--max`, `--codex-model`, `--codex-timeout`, `--base-branch`, and PR-loop bot flags. Outputs include `.humanize/rlcr/<timestamp>/` progress artifacts, monitor output, Codex review results, PR-loop state, pushed fixes, and eventual done/approved status. State advances through implementation phase, review phase, issue-remediation cycles, and cancellation paths.
- gates_or_invariants: Requires Codex CLI for review (`README.md:52-55`) and GitHub CLI plus open PR for PR loop (`README.md:173-176`). RLCR has max-iteration and base-branch options (`README.md:108-123`). PR loop requires at least one bot flag (`README.md:150-153`) and all configured bots to approve or be resolved (`README.md:169-171`).
- dependencies_and_callers: Command docs map to `commands/start-rlcr-loop.md`, `commands/start-pr-loop.md`, `commands/gen-plan.md`, and their scripts (`scripts/setup-rlcr-loop.sh`, `scripts/setup-pr-loop.sh`, `scripts/validate-gen-plan-io.sh`). Monitor documentation maps to `scripts/humanize.sh`.
- edge_cases_or_failure_modes: Documentation flags cancellation, max-iteration stopping, missing PR, missing GitHub/Codex CLI, and base-branch auto-detection fallback. The command table omits the `/humanize:` namespace while examples include it, so docs consumers must reconcile plugin shorthand with full command names.
- validation_or_tests: README behavior is covered indirectly by setup, hook, monitor, PR-loop, and robustness tests, including `tests/run-all-tests.sh:32-73`, which lists PR-loop, setup-script, base-branch, template, and state-transition suites.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-038 `file` `scripts/poll-pr-reviews.sh`
- cursor: `[_]`
- core_role: Runtime polling worker for the PR loop. It converts GitHub API comments/reviews into normalized JSON used by the PR stop hook to decide whether remote bots responded.
- algorithmic_behavior: Parses `<pr_number> --after <timestamp> --bots <bot1,bot2>` (`scripts/poll-pr-reviews.sh:23-81`), validates required args and numeric PR (`scripts/poll-pr-reviews.sh:83-102`), checks `gh` and `jq` (`scripts/poll-pr-reviews.sh:104-116`), resolves current or parent repository for fork PR support (`scripts/poll-pr-reviews.sh:122-150`), maps bot aliases to GitHub authors with a Codex special case (`scripts/poll-pr-reviews.sh:164-173`), fetches issue comments, review comments, and PR reviews, then filters by timestamp and bot author (`scripts/poll-pr-reviews.sh:240-305`).
- inputs_outputs_state: Inputs are CLI args, current GitHub repository context, `gh api` responses, and `jq`. Output is a JSON object with `comments`, `bots_responded`, `has_new_comments`, and `comment_count` (`scripts/poll-pr-reviews.sh:317-326`). It writes only temporary files under `mktemp -d` and cleans them with `trap` (`scripts/poll-pr-reviews.sh:193-198`).
- gates_or_invariants: Fails fast for missing/invalid args, missing tools, or inability to locate the PR base repo. API fetches are deliberately soft-fail: `fetch_with_retry` retries three times, emits warnings, returns an empty array, and keeps the polling loop alive (`scripts/poll-pr-reviews.sh:200-235`).
- dependencies_and_callers: Called by `hooks/pr-loop-stop-hook.sh` as `POLL_SCRIPT` (`hooks/pr-loop-stop-hook.sh:811`) during the per-bot polling loop (`hooks/pr-loop-stop-hook.sh:907-965`). The stop hook consumes `.bots_responded[]` (`hooks/pr-loop-stop-hook.sh:967-981`) and `.comments` (`hooks/pr-loop-stop-hook.sh:1042-1045`).
- edge_cases_or_failure_modes: Handles fork PRs by trying the parent repo. Approval-only PR reviews are preserved with a state placeholder rather than dropped (`scripts/poll-pr-reviews.sh:276-294`). Timestamp comparison is string-based, so ISO 8601 input format is an invariant rather than deeply validated. Bot names are trimmed but not fully regex-escaped beyond bracket escaping, so unusual bot input could alter the regex pattern.
- validation_or_tests: Covered by PR-loop robustness tests for help, required args, valid JSON shape, slow API behavior, and API failure returning boolean false for new comments (`tests/robustness/test-pr-loop-api-robustness.sh:619-843`). Fixture tests assert approval-only reviews are included and `--after` filters early comments (`tests/test-pr-loop-hooks.sh:1322-1411`).
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-068 `file` `tests/test-template-loader.sh`
- cursor: `[_]`
- core_role: Executable specification for `hooks/lib/template-loader.sh`, especially safe template loading/rendering and prompt-block substitution behavior used by validators and stop hooks.
- algorithmic_behavior: Sources the loader (`tests/test-template-loader.sh:10-13`), maintains pass/fail counters (`tests/test-template-loader.sh:20-34`), then tests path resolution, file loading, direct rendering, safe fallback rendering, directory validation, literal metacharacter handling, placeholder-injection prevention, and edge variable cases.
- inputs_outputs_state: Inputs are the project `prompt-template` tree, synthetic templates, real templates such as `block/git-push.md` and `block/wrong-round-number.md`, and `VAR=value` substitution pairs. Outputs are colored PASS/FAIL lines and exit code zero only when `TESTS_FAILED` is zero (`tests/test-template-loader.sh:641-659`). State is limited to counters.
- gates_or_invariants: Requires `get_template_dir` to resolve `prompt-template` from `hooks/lib` (`tests/test-template-loader.sh:41-52`), missing templates to return empty or fallback (`tests/test-template-loader.sh:67-78`, `196-222`), unreplaced variables to stay literal (`tests/test-template-loader.sh:181-194`), and `validate_template_dir` to require expected subdirectories (`tests/test-template-loader.sh:224-244`).
- dependencies_and_callers: Directly validates `hooks/lib/template-loader.sh`, whose `render_template` uses environment-prefixed variables and a single-pass `awk` scanner (`hooks/lib/template-loader.sh:58-132`). The loader is used by `hooks/lib/loop-common.sh` message builders, including summary Bash-block messages (`hooks/lib/loop-common.sh:481-490`).
- edge_cases_or_failure_modes: Regression tests cover shell metacharacters including ampersand, backslash, dollar sign, backticks, pipes, semicolons, globs, redirects, quotes, JSON-like strings, regex-like strings, Windows paths, and multiline values (`tests/test-template-loader.sh:247-486`). Placeholder-injection tests ensure injected `{{VAR}}` patterns are not re-expanded (`tests/test-template-loader.sh:488-544`). Unicode cases use explicit byte escapes (`tests/test-template-loader.sh:567-615`).
- validation_or_tests: This file is itself a test suite and is first in `tests/run-all-tests.sh` (`tests/run-all-tests.sh:32-35`). It validates both exact string outputs and grep-based integration with real templates.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-098 `file` `prompt-template/block/summary-bash-write.md`
- cursor: `[_]`
- core_role: Prompt/block template for a write-path gate: it tells Claude that Bash-based modification of RLCR summary files is blocked and that the Write or Edit tool must be used instead.
- algorithmic_behavior: The template renders a fixed Markdown block with one substitution, `{{CORRECT_PATH}}`, pointing to the permitted summary file (`prompt-template/block/summary-bash-write.md:1-8`). It is not an algorithm by itself, but it is part of the validation contract surfaced when a Bash command targets a summary file.
- inputs_outputs_state: Input is `CORRECT_PATH` supplied by the caller. Output is the rendered block headed “Bash Write Blocked” with the correct path and a short explanation that shell commands bypass validation hooks. It has no persistent state.
- gates_or_invariants: Invariant is that summary files must be modified through Write/Edit so round-number and path validation hooks can run. The block is emitted when a Bash command matches `round-[0-9]+-summary.md` and the validator exits with a blocking status (`hooks/loop-bash-validator.sh:370-378`).
- dependencies_and_callers: `summary_bash_blocked_message` in `hooks/lib/loop-common.sh` loads this template through `load_and_render_safe`, with a fallback if the file is missing (`hooks/lib/loop-common.sh:481-490`). `hooks/loop-bash-validator.sh` is the direct behavioral caller for Bash command blocking.
- edge_cases_or_failure_modes: If the template is missing or empty, the fallback message still blocks the action. If `CORRECT_PATH` is not supplied, the placeholder would remain literal because the renderer preserves missing variables; this avoids corrupt substitution but weakens guidance.
- validation_or_tests: `tests/test-template-references.sh` lists `block/summary-bash-write.md` among common templates that must exist (`tests/test-template-references.sh:149-167`). Template rendering and fallback behavior are covered by `tests/test-template-loader.sh`, especially safe loading/rendering and missing-template fallback tests.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-128 `file` `tests/robustness/test-base-branch-detection.sh`
- cursor: `[_]`
- core_role: Robustness test for RLCR base-branch auto-detection used before final Codex review. It isolates the branch-selection logic from `scripts/setup-rlcr-loop.sh`.
- algorithmic_behavior: Defines a local `detect_base_branch` helper (`tests/robustness/test-base-branch-detection.sh:37-64`) that tries remote default branch via `git remote show origin`, falls back to local `main`, then local `master`, and fails when none exist. Test cases create disposable Git repos for no-origin/main, no-origin/master, no-main-or-master failure, and a simulated origin (`tests/robustness/test-base-branch-detection.sh:70-191`).
- inputs_outputs_state: Inputs are temporary Git repositories, branch refs, optional origin remote, and `run_with_timeout`. Outputs are pass/fail assertions and a summary from `print_test_summary` (`tests/robustness/test-base-branch-detection.sh:193-198`). State is temporary repository structure under the test directory.
- gates_or_invariants: Invariant under test is priority order: remote default if known, then local `main`, then local `master`, otherwise nonzero return. The helper guards the remote-default pipeline with `|| true` so a missing origin does not trip `pipefail` (`tests/robustness/test-base-branch-detection.sh:41-48`).
- dependencies_and_callers: Sources `tests/test-helpers.sh` and `scripts/portable-timeout.sh` (`tests/robustness/test-base-branch-detection.sh:16-20`). Mirrors production setup logic around `scripts/setup-rlcr-loop.sh:590-642`, where explicit base-branch validation, remote default detection, local fallback, and failure messaging are implemented.
- edge_cases_or_failure_modes: The header mentions user-specified `--base-branch`, but this file only tests auto-detection. It also diverges from current production by not checking that the remote default branch exists locally before returning it; production does that at `scripts/setup-rlcr-loop.sh:617-622`. This makes it a partial executable spec and a drift-risk test.
- validation_or_tests: Included in the all-tests runner at `tests/run-all-tests.sh:55-67`. It validates missing-origin fallback, master fallback, no-base failure, and origin-present behavior, but does not cover remote-default-without-local-ref or explicit user branch validation.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5 unique item headings present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`