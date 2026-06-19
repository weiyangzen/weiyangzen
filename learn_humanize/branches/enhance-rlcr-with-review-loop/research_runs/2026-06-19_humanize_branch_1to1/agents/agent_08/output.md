# agent_08 enhance-rlcr-with-review-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `dd6c37c45c4836773497f878b8925057e9f5318c`

## Item Evidence

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-008 `file` `README.md`
- cursor: `[_]`
- core_role: Behavior-defining product/workflow contract for RLCR and PR-loop operation. It defines RLCR as Claude implementation plus independent Codex review, with a documented two-phase loop: implementation review until `COMPLETE`, then `codex review --base <branch>` quality review with severity markers; see `README.md:7-13`, `README.md:60-72`.
- algorithmic_behavior: Documents the primary state machine as plan input -> Claude work and summary -> Codex review -> feedback back to Claude -> completion signal -> code-review phase -> either issue-fix loop or done; the PR loop similarly detects an open PR, fetches bot comments, has Claude fix, pushes, triggers re-review, polls, validates locally with Codex, and repeats until approval or max iterations; see `README.md:155-163`.
- inputs_outputs_state: Inputs are plan/draft paths, command options, bot flags, base-branch option, Codex model/effort, timeouts, and max iterations. Outputs include `.humanize/rlcr/<timestamp>/` monitoring artifacts, generated plans with AC-style criteria, PR-loop state/comment/check files by implication from commands, and terminal completion/cancel states; see `README.md:74-85`, `README.md:101-116`, `README.md:137-153`.
- gates_or_invariants: Requires Codex CLI for RLCR and GitHub CLI for PR loop; enforces max-iteration and timeout concepts; PR-loop requires an associated open PR; base branch auto-detection is specified as remote default, then local `main`, then local `master`; see `README.md:52-55`, `README.md:113-115`, `README.md:165-168`.
- dependencies_and_callers: This documentation is consumed by users through Claude Code plugin commands and maps to `commands/start-rlcr-loop.md`, `commands/start-pr-loop.md`, `scripts/setup-rlcr-loop.sh`, `scripts/setup-pr-loop.sh`, `hooks/loop-codex-stop-hook.sh`, and `hooks/pr-loop-stop-hook.sh`.
- edge_cases_or_failure_modes: Documents cancellation commands, optional pushing per round, explicit tracked plan-file mode, base-branch override, and PR-loop bot selection. A documentation mismatch risk exists: command table omits the `/humanize:` namespace while examples include it (`README.md:80-93`).
- validation_or_tests: The README itself is not executable, but its base-branch and PR-loop claims are covered by scripts/tests such as `tests/robustness/test-base-branch-detection.sh`, `tests/test-pr-loop-hooks.sh`, and `tests/test-pr-loop-scripts.sh`.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-038 `file` `scripts/poll-pr-reviews.sh`
- cursor: `[_]`
- core_role: Runtime PR-loop polling script that normalizes GitHub issue comments, review comments, and PR reviews into one JSON event stream filtered by bot author and timestamp; see `scripts/poll-pr-reviews.sh:1-10`, `scripts/poll-pr-reviews.sh:236-304`.
- algorithmic_behavior: Parses `<pr_number> --after <timestamp> --bots <list>`, validates required arguments and numeric PR number, resolves the PR base repository for fork support, maps bot aliases to GitHub authors, fetches three API endpoints with retries, normalizes fields through `jq`, combines arrays, filters by `created_at >= after` and author regex, then emits `{comments,bots_responded,has_new_comments,comment_count}`; see `scripts/poll-pr-reviews.sh:23-103`, `scripts/poll-pr-reviews.sh:126-157`, `scripts/poll-pr-reviews.sh:166-186`, `scripts/poll-pr-reviews.sh:316-325`.
- inputs_outputs_state: Inputs are GitHub PR number, ISO-like timestamp, comma-separated bot aliases, current repository identity from `gh`, and API responses. Output is JSON on stdout; warnings/errors go to stderr. It does not persist state; caller state is handled by `hooks/pr-loop-stop-hook.sh`.
- gates_or_invariants: Fails closed on missing/invalid CLI args, missing `gh`, missing `jq`, or inability to resolve repository owner/name. API endpoint failures are deliberately degraded to empty arrays after three attempts so polling can continue through partial outages; see `scripts/poll-pr-reviews.sh:108-116`, `scripts/poll-pr-reviews.sh:199-233`.
- dependencies_and_callers: Depends on Bash, `gh`, `jq`, GitHub REST endpoints, `mktemp`, and `trap`. Called by the PR-loop stop hook through `POLL_SCRIPT="$PLUGIN_ROOT/scripts/poll-pr-reviews.sh"` after trigger validation and timestamp selection; see `hooks/pr-loop-stop-hook.sh:791-817`.
- edge_cases_or_failure_modes: Handles fork PRs by trying current repo then parent repo; empty PR review bodies become a state placeholder so approval-only reviews are visible (`scripts/poll-pr-reviews.sh:275-288`). Timestamp comparison is lexical and assumes comparable ISO formats. Bot regex escaping only handles square brackets, so unexpected bot alias characters could affect regex behavior. The `API_FAILURES` counter is diagnostic only and effectively not surfaced.
- validation_or_tests: Fixture-backed tests verify valid JSON, approval-only review placeholders, bot response reporting, and `--after` filtering (`tests/test-pr-loop-hooks.sh:1322-1419`). Script-level tests cover help and missing-argument errors (`tests/test-pr-loop-scripts.sh:329-380`).
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-068 `file` `tests/test-template-loader.sh`
- cursor: `[_]`
- core_role: Executable specification for template loading/rendering behavior used by RLCR and PR-loop hooks; it directly sources `hooks/lib/template-loader.sh` and asserts both normal rendering and security-sensitive edge cases; see `tests/test-template-loader.sh:10-13`.
- algorithmic_behavior: Runs a Bash test harness with pass/fail counters, checking `get_template_dir`, `load_template`, `render_template`, `load_and_render`, `load_and_render_safe`, and `validate_template_dir`; it exits successfully only when no failures were recorded; see `tests/test-template-loader.sh:20-34`, `tests/test-template-loader.sh:641-659`.
- inputs_outputs_state: Inputs are real template files under `prompt-template`, synthetic template strings, `VAR=value` assignments, fallback strings, missing paths, and invalid directories. Outputs are colored PASS/FAIL lines plus a final process exit code.
- gates_or_invariants: Specifies exact single-pass substitution behavior: multiple variables render, unused variables are ignored, missing variables remain as placeholders, fallback is used when safe rendering cannot load a template, and directory validation requires expected subdirectories; see `tests/test-template-loader.sh:81-145`, `tests/test-template-loader.sh:167-244`.
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh`, real templates such as `block/git-push.md` and `block/wrong-round-number.md`, Bash, `grep`, and standard shell utilities. It is included in the aggregate suite list at `tests/run-all-tests.sh:32-40`.
- edge_cases_or_failure_modes: Covers shell metacharacters as literal values, including ampersands, backslashes, dollar signs, backticks, pipes, redirections, quotes, glob syntax, regex-like text, JSON-like text, Windows paths, and multiline values (`tests/test-template-loader.sh:247-487`). It also asserts placeholder injection prevention where a rendered value containing `{{OTHER_VAR}}` must not be re-expanded (`tests/test-template-loader.sh:488-543`).
- validation_or_tests: This file is itself validation. It cross-checks the implementation contract documented in `hooks/lib/template-loader.sh:7-21` and the single-pass AWK renderer in `hooks/lib/template-loader.sh:58-132`.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-098 `file` `prompt-template/block/summary-bash-write.md`
- cursor: `[_]`
- core_role: Prompt/block template for the hook gate that prevents Bash-based summary-file writes from bypassing Write/Edit validation paths.
- algorithmic_behavior: Renders a short denial message with `{{CORRECT_PATH}}`, instructing the actor to use Write or Edit and explaining that shell tools bypass validation hooks; see `prompt-template/block/summary-bash-write.md:1-8`.
- inputs_outputs_state: Input is the `CORRECT_PATH` template variable supplied by `summary_bash_blocked_message`. Output is rendered block text, normally sent to stderr by the Bash validator. It does not mutate repository state directly.
- gates_or_invariants: Enforces the invariant that `round-N-summary.md` changes must go through the tool path that can validate current round number and location. The actual gate is in `hooks/loop-bash-validator.sh:370-379`, which detects summary-file modification by Bash and exits with a block code.
- dependencies_and_callers: Loaded by `hooks/lib/loop-common.sh:475-483` through `load_and_render_safe`; that function is invoked from `hooks/loop-bash-validator.sh:375-378`. It depends on `hooks/lib/template-loader.sh` for safe placeholder replacement and fallback behavior.
- edge_cases_or_failure_modes: If the template is missing or empty, `load_and_render_safe` supplies a fallback message with the same `CORRECT_PATH` variable (`hooks/lib/loop-common.sh:479-483`). If `CORRECT_PATH` is incorrect upstream, this template will faithfully render the wrong path; path correctness is owned by the caller.
- validation_or_tests: Template reference validation explicitly includes `block/summary-bash-write.md` as a required common template (`tests/test-template-references.sh:149-167`). Hook behavior around Bash command detection is covered by the broader Bash validator tests.
- skip_candidate: `no`

### ENHANCE_RLCR_WITH_REVIEW_LOOP-HZ-128 `file` `tests/robustness/test-base-branch-detection.sh`
- cursor: `[_]`
- core_role: Robustness executable spec for RLCR base-branch auto-detection, focused on missing-origin handling and local fallback order.
- algorithmic_behavior: Creates temporary Git repositories, defines a local `detect_base_branch` helper that checks remote default via `git remote show origin`, then falls back to local `main`, then local `master`, and returns failure when none exists; see `tests/robustness/test-base-branch-detection.sh:24-64`.
- inputs_outputs_state: Inputs are temporary repos with controlled branch/remote configurations and a timeout value passed to `run_with_timeout`. Outputs are pass/fail records and a final summary via `print_test_summary`; temporary state is under `TEST_DIR` with trap cleanup from `tests/test-helpers.sh:84-89`.
- gates_or_invariants: Asserts no-origin repositories still fall back to local `main` or `master`, and repositories with no `main`/`master` fail detection; see `tests/robustness/test-base-branch-detection.sh:70-149`. It also exercises an origin scenario that may detect remote default or accept local fallback; see `tests/robustness/test-base-branch-detection.sh:151-191`.
- dependencies_and_callers: Depends on `git`, `tests/test-helpers.sh`, and `scripts/portable-timeout.sh`. It is tied to production logic in `scripts/setup-rlcr-loop.sh:532-604`, where production also validates explicit user base branches, local ref existence for remote default, YAML-safe branch names, and captured base commit.
- edge_cases_or_failure_modes: The test helper is not a perfect copy of current production: production only accepts a remote default if the branch exists locally (`scripts/setup-rlcr-loop.sh:560-565`), while the helper echoes any non-unknown remote default. The test does not cover explicit `--base-branch`, remote-default-without-local-ref, YAML-unsafe names, detached HEAD, or base commit capture. It also is not listed in the aggregate test suite block shown at `tests/run-all-tests.sh:32-66`.
- validation_or_tests: This file is validation for base-branch fallback behavior, but its coverage is partial relative to `scripts/setup-rlcr-loop.sh:537-604`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `5 item evidence sections present; each assigned item_id is used once as a section heading`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`