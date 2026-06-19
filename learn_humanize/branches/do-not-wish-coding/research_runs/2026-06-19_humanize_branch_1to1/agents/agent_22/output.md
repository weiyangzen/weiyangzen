# agent_22 do-not-wish-coding 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `ac6cd9c180bcb9b84f6083fba1e458b4aab9ae14`

## Item Evidence

### DO_NOT_WISH_CODING-HZ-022 `directory` `skills/humanize-gen-plan`
- cursor: `[_]`
- core_role: Flow skill for converting a rough draft into a structured implementation `plan.md`; recursive inspection found this directory contains one file, `skills/humanize-gen-plan/SKILL.md`.
- algorithmic_behavior: The flow declares itself as `humanize-gen-plan` and `type: flow` at `skills/humanize-gen-plan/SKILL.md:1-5`; its mermaid flow validates IO, reads the draft, rejects repo-irrelevant drafts, loops with the user on clarity/consistency/completeness/functionality issues, confirms quantitative metrics, generates plan sections, writes the output, reviews inconsistencies, and checks language unification at `skills/humanize-gen-plan/SKILL.md:18-45`.
- inputs_outputs_state: Required inputs are `--input <path/to/draft.md>` and `--output <path/to/plan.md>` at `skills/humanize-gen-plan/SKILL.md:48-53`; output is a new plan with Goal Description, AC-form acceptance criteria, path boundaries, dependencies, milestones, and implementation notes at `skills/humanize-gen-plan/SKILL.md:54-93`.
- gates_or_invariants: IO validation must pass before draft analysis; the referenced validator rejects missing/empty input, nonexistent output directory, existing output path, output directory target, missing write permission, invalid mode flags, and missing plan template at `scripts/validate-gen-plan-io.sh:76-95` and `scripts/validate-gen-plan-io.sh:108-178`.
- dependencies_and_callers: The skill expects installer hydration of `{{HUMANIZE_RUNTIME_ROOT}}` at `skills/humanize-gen-plan/SKILL.md:12-16`, calls `scripts/validate-gen-plan-io.sh` in its flow at `skills/humanize-gen-plan/SKILL.md:20`, and documents `/flow:humanize-gen-plan` plus `/skill:humanize-gen-plan` entry points at `skills/humanize-gen-plan/SKILL.md:108-123`.
- edge_cases_or_failure_modes: Draft irrelevance stops the flow; unresolved issues return to analysis through user questioning; quantitative metrics trigger a user confirmation branch; multiple languages trigger a unification question; validator exit codes map operational failures from 1 through 7 at `skills/humanize-gen-plan/SKILL.md:95-107`.
- validation_or_tests: The concrete IO validator is `scripts/validate-gen-plan-io.sh`, whose usage and options include discussion/direct modes and optional auto-start note at `scripts/validate-gen-plan-io.sh:16-26` and `scripts/validate-gen-plan-io.sh:93-95`; no runtime test was executed in this read-only research pass.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-052 `file` `scripts/cancel-rlcr-loop.sh`
- cursor: `[_]`
- core_role: Runtime cancellation script for an active RLCR loop; it turns an active loop state into terminal cancellation state while preserving loop artifacts.
- algorithmic_behavior: Parses only `--force` and help at `scripts/cancel-rlcr-loop.sh:24-63`, resolves `PROJECT_ROOT` from `CLAUDE_PROJECT_DIR` or `pwd`, sources `hooks/lib/loop-common.sh`, and locates the active loop with `find_active_loop` at `scripts/cancel-rlcr-loop.sh:69-87`.
- inputs_outputs_state: Inputs are optional `--force`, active `.humanize/rlcr/<timestamp>/state.md` or `finalize-state.md`, and optional env root; outputs are machine-readable first-line statuses `NO_LOOP`, `NO_ACTIVE_LOOP`, `FINALIZE_NEEDS_CONFIRM`, `CANCELLED`, or `CANCELLED_FINALIZE` at `scripts/cancel-rlcr-loop.sh:89-112`, `scripts/cancel-rlcr-loop.sh:131-141`, and `scripts/cancel-rlcr-loop.sh:161-169`.
- gates_or_invariants: Finalize phase requires confirmation unless `--force` is provided at `scripts/cancel-rlcr-loop.sh:131-141`; cancellation creates `.cancel-requested`, removes pending session id, and renames the active state file to `cancel-state.md` at `scripts/cancel-rlcr-loop.sh:148-155`.
- dependencies_and_callers: Slash command policy calls this script and interprets its first output line in `commands/cancel-rlcr-loop.md:1-36`; `find_active_loop` is defined in `hooks/lib/loop-common.sh:251-327`; Bash validators permit only the exact authorized state-to-cancel rename after the signal file exists via `is_cancel_authorized` at `hooks/lib/loop-common.sh:698-875`.
- edge_cases_or_failure_modes: Cancellation intentionally ignores session filtering because the slash command has no hook `session_id`, documented at `scripts/cancel-rlcr-loop.sh:76-84`; without a filter, `find_active_loop` checks only the newest loop directory for zombie-loop protection at `hooks/lib/loop-common.sh:251-292`, so an older active directory is not revived if the newest loop is terminal.
- validation_or_tests: `tests/test-session-id.sh:348-383` asserts cancellation works regardless of stored `session_id` and renames state; `tests/test-session-id.sh:385-436` asserts newer terminal loops prevent stale older cancellation; `tests/test-cancel-signal-file.sh:80-135` and `tests/test-cancel-signal-file.sh:240-380` specify the signal-file and injection-blocking behavior around the hook-authorized move.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-082 `file` `tests/test-helpers.sh`
- cursor: `[_]`
- core_role: Shared shell test harness used by algorithm and robustness tests; it is support infrastructure for executable specifications rather than runtime RLCR behavior.
- algorithmic_behavior: Defines color constants and mutable counters at `tests/test-helpers.sh:13-24`, then exposes `pass`, `fail`, and `skip` functions that increment counters and print standardized results at `tests/test-helpers.sh:30-52`.
- inputs_outputs_state: Functions accept message strings and optional expected/got details; global state is `TESTS_PASSED`, `TESTS_FAILED`, `TESTS_SKIPPED`, and `TEST_DIR`; `setup_test_dir` creates a temporary directory and installs cleanup trap at `tests/test-helpers.sh:84-89`.
- gates_or_invariants: `print_test_summary` returns success only when `TESTS_FAILED` is zero and otherwise returns failure at `tests/test-helpers.sh:58-78`; `init_test_git_repo` creates a deterministic git repo with configured identity, one tracked file, and an initial commit at `tests/test-helpers.sh:91-104`.
- dependencies_and_callers: Many test suites source this helper, including PR loop, stop gate, config, model router, session id, agent teams, and robustness tests, as shown by repository references to `source "$SCRIPT_DIR/test-helpers.sh"` and `source "$SCRIPT_DIR/../test-helpers.sh"`.
- edge_cases_or_failure_modes: Repeated `setup_test_dir` calls replace the same `TEST_DIR` variable and trap; `init_test_git_repo` changes directories and relies on `cd -` to restore; git must be available and commit signing is explicitly disabled at `tests/test-helpers.sh:97-103`.
- validation_or_tests: This file is not itself a test case; it provides the pass/fail mechanics used by tests that specify RLCR state, PR loop, template, config, and hook behavior. No tests were executed in this read-only research pass.
- skip_candidate: `yes: helper harness only; it supports core executable specifications but does not implement workflow routing, hooks, templates, or state transitions itself`

### DO_NOT_WISH_CODING-HZ-112 `file` `hooks/lib/template-loader.sh`
- cursor: `[_]`
- core_role: Shared template-loading and single-pass rendering library for RLCR and PR loop prompts, validation block messages, and hook feedback.
- algorithmic_behavior: `get_template_dir` derives the plugin `prompt-template` directory from a hooks/lib path at `hooks/lib/template-loader.sh:24-31`; `load_template` emits file contents or an empty string with a warning at `hooks/lib/template-loader.sh:33-48`; `render_template` performs single-pass `{{VAR}}` replacement through `awk` and `TMPL_VAR_` environment variables at `hooks/lib/template-loader.sh:50-132`.
- inputs_outputs_state: Inputs are template content, template directory/name, and `VAR=value` assignments; output is rendered text to stdout; missing variables remain as placeholders by design at `hooks/lib/template-loader.sh:115-122`; values are not rescanned, preventing placeholder injection at `hooks/lib/template-loader.sh:54-57` and `hooks/lib/template-loader.sh:116-119`.
- gates_or_invariants: `load_and_render_safe` falls back when a template is missing or rendering yields empty output at `hooks/lib/template-loader.sh:167-203`; `validate_template_dir` requires `block`, `codex`, and `claude` subdirectories at `hooks/lib/template-loader.sh:205-222`.
- dependencies_and_callers: `hooks/lib/loop-common.sh` sources this library and initializes `TEMPLATE_DIR` with warning-only validation at `hooks/lib/loop-common.sh:194-202`; `setup-pr-loop.sh` renders PR prompt components through `load_and_render_safe` at `scripts/setup-pr-loop.sh:757-800` and `scripts/setup-pr-loop.sh:847-850`; hook validators call block-message wrappers such as `todos_blocked_message` at `hooks/lib/loop-common.sh:608-617`.
- edge_cases_or_failure_modes: Missing templates produce empty output unless safe fallback is used; variable names in assignments are accepted from the `VAR=value` prefix and values may contain shell metacharacters literally; very large rendered values flow through environment variables, so system env-size limits are an implicit boundary.
- validation_or_tests: `tests/test-template-loader.sh:41-233` covers directory resolution, load/render, missing templates, fallback, and validation; `tests/test-template-loader.sh:247-520` covers shell metacharacters and placeholder-injection prevention; `tests/test-error-scenarios.sh:42-180` covers strict-mode and fallback behavior; `tests/test-template-references.sh:51-230` validates referenced hook templates and safe rendering usage.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-142 `file` `prompt-template/block/todos-file-access.md`
- cursor: `[_]`
- core_role: Static block-message template used when the hook system prevents direct access to RLCR `round-*-todos.md` files.
- algorithmic_behavior: The template tells the agent not to create or access `round-*-todos.md` files and to use native task tools instead at `prompt-template/block/todos-file-access.md:1-8`; there are no placeholders or dynamic branches in the template itself.
- inputs_outputs_state: Loaded via `todos_blocked_message`, whose `action` parameter is accepted but not rendered into this template; the wrapper provides fallback text and calls `load_and_render_safe` at `hooks/lib/loop-common.sh:608-617`.
- gates_or_invariants: Read, Write, Edit, and Bash validators block todos access/modification unless explicit active-loop allowlist conditions pass; read gating is at `hooks/loop-read-validator.sh:54-66`, write at `hooks/loop-write-validator.sh:54-66`, edit at `hooks/loop-edit-validator.sh:37-49`, and Bash modification gating at `hooks/loop-bash-validator.sh:393-403`.
- dependencies_and_callers: The allowlist includes `round-1-todos.md` and `round-2-todos.md` plus selected summaries at `hooks/lib/loop-common.sh:592-605`; this means the template is the general rejection surface, while some active-loop paths are intentionally exempted by validators.
- edge_cases_or_failure_modes: If the template is missing, `todos_blocked_message` falls back to inline text at `hooks/lib/loop-common.sh:612-616`; if the agent attempts Bash modification outside the active loop path or outside the round-1/round-2 todos exception, the Bash validator emits this block and exits with a blocking status at `hooks/loop-bash-validator.sh:397-403`.
- validation_or_tests: `tests/test-template-references.sh:152-164` explicitly checks `block/todos-file-access.md` as a common template; template loading and fallback behavior are covered by `tests/test-template-loader.sh:197-221` and `tests/test-error-scenarios.sh:134-158`.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-172 `file` `prompt-template/pr-loop/round-0-task-has-comments.md`
- cursor: `[_]`
- core_role: PR loop Round 0 task template used when fetched PR comments already exist; it tells the coding agent how to resolve review feedback and trigger another review cycle.
- algorithmic_behavior: The template prioritizes human comments over bot comments, asks the agent to read relevant code, make fixes, add tests as needed, commit, push, comment on the PR for re-review, and write a resolution summary at `prompt-template/pr-loop/round-0-task-has-comments.md:4-27`.
- inputs_outputs_state: Render variables include `{{PR_NUMBER}}`, `{{BOT_MENTION_STRING}}`, and `{{RESOLVE_PATH}}`; setup constructs the broader variable set at `scripts/setup-pr-loop.sh:731-738`, renders this template only when `COMMENT_COUNT` is nonzero, and appends it to `round-0-prompt.md` at `scripts/setup-pr-loop.sh:766-850`.
- gates_or_invariants: The prompt’s rules prohibit modifying `.humanize/pr-loop/` state files, require pushes for bot visibility, require the bot mention comment format, and require thorough handling of reviewer concerns at `prompt-template/pr-loop/round-0-task-has-comments.md:30-35`.
- dependencies_and_callers: The template is selected by `scripts/setup-pr-loop.sh` as the has-comments branch at `scripts/setup-pr-loop.sh:801-848`; if missing or empty, setup uses an inline fallback with the same variable contract at `scripts/setup-pr-loop.sh:803-847`.
- edge_cases_or_failure_modes: If template variables are omitted, the renderer preserves unresolved placeholders by design at `hooks/lib/template-loader.sh:115-122`; if the PR comment command is not run or fails, remote bots may not re-review; if the resolution summary is not written to `@{{RESOLVE_PATH}}`, the Stop Hook’s later polling/validation loop lacks the expected human-readable resolution artifact.
- validation_or_tests: General PR loop setup tests reference `scripts/setup-pr-loop.sh`, but the template-reference test scans hook scripts and `loop-common.sh`, not this setup script, at `tests/test-template-references.sh:56-64`; therefore this template has indirect coverage through setup flow and renderer tests, not a focused existence check in that reference scanner.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6/6 unique Item Evidence headings present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`