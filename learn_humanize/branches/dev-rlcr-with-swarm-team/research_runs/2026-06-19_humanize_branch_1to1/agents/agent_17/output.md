# agent_17 dev-rlcr-with-swarm-team 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `0d5f0943ae9b1f80c5115aa946ebeb289e2cb83d`

## Item Evidence

### DEV_RLCR_WITH_SWARM_TEAM-HZ-017 `file` `agents/draft-relevance-checker.md`
- cursor: `[_]`
- core_role: Relevance-gate subagent prompt for `/humanize:gen-plan`; frontmatter defines agent identity, model, and allowed tools at `agents/draft-relevance-checker.md:1-6`.
- algorithmic_behavior: Instructs the agent to inspect repo docs/structure, compare draft semantics to repository purpose, then emit exactly `RELEVANT: ...` or `NOT_RELEVANT: ...` at `agents/draft-relevance-checker.md:14-29`.
- inputs_outputs_state: Input is draft content supplied by the caller plus read-only repo exploration via `Read`, `Glob`, and `Grep`; output is a single verdict string; no file or loop state is modified.
- gates_or_invariants: The policy is intentionally lenient: informal drafts and uncertain matches should pass as relevant, making this a false-negative avoidance gate rather than a strict classifier (`agents/draft-relevance-checker.md:31-36`).
- dependencies_and_callers: `commands/gen-plan.md:50-72` invokes this agent after IO validation; `NOT_RELEVANT` stops plan generation, while `RELEVANT` advances to template loading and plan creation.
- edge_cases_or_failure_modes: Drafts in any language, rough ideas, semantic-but-not-syntactic matches, and vague repo references are expected to pass if plausibly connected; unrelated domains should fail.
- validation_or_tests: `tests/test-gen-plan.sh:111-153` checks the agent file exists and validates name/model/tools; `tests/test-gen-plan.sh:241-292` checks naming and required agent frontmatter.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-047 `file` `tests/setup-monitor-test-env.sh`
- cursor: `[_]`
- core_role: Test fixture generator for `humanize monitor pr`; it seeds `.humanize/pr-loop/<timestamp>/state.md` with PR-loop state variants for monitor parsing tests.
- algorithmic_behavior: Dispatches on `TEST_NAME` values `yaml_list`, `configured`, and `empty`, creating fixed timestamped PR-loop directories and YAML frontmatter state files (`tests/setup-monitor-test-env.sh:20-89`).
- inputs_outputs_state: Inputs are `<test_dir>` and optional `<test_name>` (`tests/setup-monitor-test-env.sh:12-18`); output is the test dir path on stdout plus created state files under the provided temp project (`tests/setup-monitor-test-env.sh:91`).
- gates_or_invariants: Requires a test directory, rejects unknown fixture names, and encodes `configured_bots` as stable baseline while `active_bots` represents current pending reviewers (`tests/setup-monitor-test-env.sh:31-39`, `tests/setup-monitor-test-env.sh:53-60`, `tests/setup-monitor-test-env.sh:74-80`).
- dependencies_and_callers: Called by `tests/test-pr-loop-hooks.sh:1553`, `tests/test-pr-loop-hooks.sh:1580`, and `tests/test-pr-loop-hooks.sh:1602`; production monitor parsing reads these YAML lists in `scripts/humanize.sh:1224-1253`.
- edge_cases_or_failure_modes: The `empty` fixture leaves `active_bots:` without list entries, relying on monitor defaults to display `none`; fixed timestamps avoid nondeterministic latest-session ordering.
- validation_or_tests: The caller validates YAML-list active bot display, separate configured-bot display, and empty active-bot display at `tests/test-pr-loop-hooks.sh:1547-1621`.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-077 `file` `hooks/lib/template-loader.sh`
- cursor: `[_]`
- core_role: Shared prompt-template loading and rendering library used by RLCR/PR-loop hooks and setup scripts; it centralizes template path resolution, substitution, fallback, and directory validation.
- algorithmic_behavior: `get_template_dir` resolves `prompt-template` relative to `hooks/lib` (`hooks/lib/template-loader.sh:24-31`); `load_template` cats existing templates or warns and returns empty (`hooks/lib/template-loader.sh:33-48`).
- inputs_outputs_state: Inputs are template dir/name, raw template content, and `VAR=value` substitutions; outputs are rendered text on stdout and warnings/errors on stderr; it does not persist state.
- gates_or_invariants: `render_template` performs single-pass `{{VAR}}` replacement through prefixed environment variables and awk, preserves missing placeholders, and treats unclosed `{{` literally (`hooks/lib/template-loader.sh:50-132`).
- dependencies_and_callers: Sourced by `hooks/lib/loop-common.sh:156-164` and `scripts/setup-pr-loop.sh:39`; broad consumers use `load_and_render_safe`, including read/write/bash/stop validators and PR-loop setup templates.
- edge_cases_or_failure_modes: Missing or empty templates fall back through `load_and_render_safe` (`hooks/lib/template-loader.sh:170-203`); variable values containing `{{OTHER}}` are not re-expanded; comments state uppercase variable syntax, but the implementation does not enforce that regex.
- validation_or_tests: Template behavior is covered by `tests/test-template-loader.sh`, `tests/test-error-scenarios.sh`, `tests/test-templates-comprehensive.sh`, `tests/robustness/test-template-stress-robustness.sh`, and `tests/robustness/test-template-error-robustness.sh`; `tests/test-template-references.sh` verifies referenced templates and safe renderer usage.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-107 `file` `prompt-template/block/wrong-round-file.md`
- cursor: `[_]`
- core_role: User-facing block template for the loop read validator when a session attempts to read a round-specific prompt or summary that does not match the current round.
- algorithmic_behavior: Renders the attempted round/file type, the authoritative current round, the current prompt/summary paths, and an explicit fallback command placeholder (`prompt-template/block/wrong-round-file.md:1-9`).
- inputs_outputs_state: Inputs are `CLAUDE_ROUND`, `FILE_TYPE`, `CURRENT_ROUND`, `ACTIVE_LOOP_DIR`, and `FILE_PATH`; output is markdown guidance emitted by the validator; no state changes.
- gates_or_invariants: Enforces current-round access discipline: wrong-round reads are blocked unless the path is allowlisted by the read validator.
- dependencies_and_callers: `hooks/loop-read-validator.sh:138-150` selects this template via `load_and_render_safe` and exits with code `2` when the requested round differs from `CURRENT_ROUND`.
- edge_cases_or_failure_modes: The template lists correct current-round files but also says `cat {{FILE_PATH}}` if needed; that is a deliberate escape-style instruction only if other validators permit the shell read.
- validation_or_tests: Indirectly validated by template-reference coverage and read-validator tests; the caller includes an inline fallback with the same core placeholders at `hooks/loop-read-validator.sh:139-149`.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-137 `file` `tests/robustness/test-git-operations-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for production git status/state helpers in `scripts/humanize.sh`, especially monitor status-bar correctness around repository state.
- algorithmic_behavior: Sources helpers and production code (`tests/robustness/test-git-operations-robustness.sh:15-20`), creates temporary git repos, splits pipe-delimited status results with `parse_result`, and runs 25 pass/fail checks.
- inputs_outputs_state: Inputs are local git commands and temp repo mutations; outputs are PASS/FAIL lines plus `print_test_summary`, exiting with the summary status (`tests/robustness/test-git-operations-robustness.sh:21-26`, `tests/robustness/test-git-operations-robustness.sh:502-507`).
- gates_or_invariants: Specifies `humanize_parse_git_status` fields as `modified|added|deleted|untracked|insertions|deletions` (`tests/robustness/test-git-operations-robustness.sh:32-47`) and state names such as `normal`, `detached`, `rebase`, `merge`, `shallow`, and `not_a_repo`.
- dependencies_and_callers: Tests production `humanize_detect_git_state` from `scripts/humanize.sh:120-168` and `humanize_parse_git_status` from `scripts/humanize.sh:170-215`; included in the aggregate runner at `tests/run-all-tests.sh:58-64`.
- edge_cases_or_failure_modes: Covers non-git dirs, detached HEAD, empty repos, feature branches, renames, many untracked files, filenames with spaces, binary files, staged plus unstaged same-file changes, simulated rebase/merge/shallow markers, and permission ambiguity (`tests/robustness/test-git-operations-robustness.sh:168-500`).
- validation_or_tests: Positive status tests cover clean/untracked/modified/added/insertions (`tests/robustness/test-git-operations-robustness.sh:71-158`); negative and git-state tests cover edge cases and special states (`tests/robustness/test-git-operations-robustness.sh:160-500`).
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5/5 item evidence headings present; item IDs intentionally not repeated here to preserve the exact-once identifier invariant
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`