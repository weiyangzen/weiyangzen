# agent_02 change-todos-to-tasks 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `0790d28514ab48bec2668f4ec069592872fed586`

## Item Evidence

### CHANGE_TODOS_TO_TASKS-HZ-002 `directory` `agents`
- cursor: `[_]`
- core_role: Holds repository-local Claude subagent definitions. Recursively, this directory contains one child: `agents/draft-relevance-checker.md`, a gen-plan relevance gate agent.
- algorithmic_behavior: `draft-relevance-checker.md` defines frontmatter name/model/tools at `agents/draft-relevance-checker.md:1-6`, then instructs the agent to inspect repo docs/structure and classify a draft as relevant or not at `agents/draft-relevance-checker.md:14-29`. The expected outputs are exact verdict prefixes: `RELEVANT:` or `NOT_RELEVANT:`.
- inputs_outputs_state: Input is draft content passed by the gen-plan command plus read-only repository exploration via `Read`, `Glob`, and `Grep`. Output is a short verdict string. It has no persistent filesystem state of its own.
- gates_or_invariants: The gate is intentionally lenient: informal or non-English drafts are allowed, semantic relevance is preferred over syntactic matching, and uncertainty should resolve to relevant at `agents/draft-relevance-checker.md:31-36`.
- dependencies_and_callers: `commands/gen-plan.md:50-72` invokes `humanize:draft-relevance-checker` after IO validation and stops plan generation if the verdict is `NOT_RELEVANT`. Tests validate the agent file, name, model, and tools in `tests/test-gen-plan.sh:107-156`.
- edge_cases_or_failure_modes: Main risk is false-negative gating of a usable draft; the prompt mitigates this by biasing toward relevance. A missing/renamed agent or wrong model breaks command-contract validation in the gen-plan tests.
- validation_or_tests: `tests/test-gen-plan.sh:111-156` checks existence, `name: draft-relevance-checker`, `model: haiku`, and a `tools:` field; later tests also validate naming/model/content conventions.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-032 `file` `scripts/cancel-pr-loop.sh`
- cursor: `[_]`
- core_role: Implements the PR-loop cancellation state transition for `/humanize:cancel-pr-loop`.
- algorithmic_behavior: Parses `--force` and help at `scripts/cancel-pr-loop.sh:24-66`; resolves project root from `CLAUDE_PROJECT_DIR` or `pwd` at `scripts/cancel-pr-loop.sh:72`; selects the newest `.humanize/pr-loop/*/` directory by reverse lexical sort at `scripts/cancel-pr-loop.sh:75-76`; requires `state.md` in that newest loop at `scripts/cancel-pr-loop.sh:88-98`; extracts round/max/pr metadata at `scripts/cancel-pr-loop.sh:104-112`; creates `.cancel-requested` and renames `state.md` to `cancel-state.md` at `scripts/cancel-pr-loop.sh:118-122`; prints `CANCELLED` plus a summary at `scripts/cancel-pr-loop.sh:128-130`.
- inputs_outputs_state: Inputs are CLI flags, `CLAUDE_PROJECT_DIR`, the `.humanize/pr-loop` directory tree, and YAML-like fields in `state.md`. Outputs are status tokens on stdout, a `.cancel-requested` signal file, and preserved `cancel-state.md`. State transition is active loop state file to cancelled state file.
- gates_or_invariants: Only PR loops are targeted, not RLCR loops, as documented in help at `scripts/cancel-pr-loop.sh:54-56`. A loop is active only if the newest PR-loop directory contains `state.md`; otherwise it emits `NO_LOOP` or `NO_ACTIVE_LOOP` and exits with code 1.
- dependencies_and_callers: `commands/cancel-pr-loop.md:1-25` exposes the slash-command wrapper and maps output tokens to user-facing responses. `hooks/pr-loop-stop-hook.sh:951-954` exits polling when `.cancel-requested` appears. `scripts/lib/monitor-common.sh:272-275` reports `cancel-state.md` as `cancelled`. Hook protection allows this rename only when authorized by a cancel signal via `hooks/loop-bash-validator.sh:133-142` and `hooks/lib/loop-common.sh:551-710`.
- edge_cases_or_failure_modes: If the newest loop directory is already inactive but an older one has `state.md`, the script still returns `NO_ACTIVE_LOOP` because it only considers the newest directory. Missing metadata falls back to `?` at `scripts/cancel-pr-loop.sh:109-112`. `--force` currently has no behavioral effect. Because `set -euo pipefail` is used, `touch` or `mv` filesystem failures abort with the underlying command status rather than the documented generic code 3.
- validation_or_tests: `tests/test-pr-loop-scripts.sh:181-252` verifies help output, no-loop behavior, and active-loop cancellation including `state.md` removal and `cancel-state.md` creation. Cancel-signal security is covered more deeply by `tests/test-cancel-signal-file.sh` and robustness tests referenced by the repository search.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-062 `file` `tests/test-pr-loop-lib.sh`
- cursor: `[_]`
- core_role: Shared PR-loop test harness library that supplies mocks, environment setup, and summary behavior for executable PR-loop specifications.
- algorithmic_behavior: Uses `TEST_PR_LOOP_LIB_LOADED` as a source-once guard at `tests/test-pr-loop-lib.sh:10-13`; resolves `SCRIPT_DIR` and `PROJECT_ROOT` at `tests/test-pr-loop-lib.sh:15-16`; sources `tests/test-helpers.sh` when needed at `tests/test-pr-loop-lib.sh:18-21`; creates mock `gh` behavior at `tests/test-pr-loop-lib.sh:27-88`; creates mock `codex` behavior at `tests/test-pr-loop-lib.sh:90-101`; initializes a temp test environment and prepends mock binaries to `PATH` at `tests/test-pr-loop-lib.sh:107-121`; prints pass/fail summary and returns failure on any failed test at `tests/test-pr-loop-lib.sh:127-144`.
- inputs_outputs_state: Inputs are the requested mock directory and existing global test counters/helper functions. Outputs are executable mock binaries under `$TEST_DIR/mock_bin`, exported `MOCK_BIN_DIR`, a modified `PATH`, and a summary exit status. State is held in shell globals such as `TEST_DIR`, `TESTS_PASSED`, and `TESTS_FAILED`.
- gates_or_invariants: Idempotent loading prevents duplicate function setup. The mock `gh` only allows the command shapes used by PR-loop tests and exits 1 for unhandled commands at `tests/test-pr-loop-lib.sh:84-85`. Summary returns nonzero if any test failed at `tests/test-pr-loop-lib.sh:137-143`.
- dependencies_and_callers: Depends on `tests/test-helpers.sh` for `setup_test_dir`, `pass`, and `fail`; those helpers create temp dirs and test counters at `tests/test-helpers.sh:22-89`. `tests/test-pr-loop.sh:18-27` sources this library, initializes the environment, and then sources the PR-loop script/hook/stop-hook test modules.
- edge_cases_or_failure_modes: The mock `gh` is intentionally narrow and will fail new command shapes unless extended. `create_mock_codex` assumes the mock directory already exists, unlike `create_mock_gh`; the normal initializer satisfies that. Because the library prepends `PATH`, tests deliberately shadow real `gh` and `codex`.
- validation_or_tests: This file is not a standalone test case; it is the support layer used by the PR-loop suite. Its behavior is exercised indirectly by `tests/test-pr-loop.sh:26-47` and all sourced PR-loop modules.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-092 `file` `prompt-template/block/plan-file-modified.md`
- cursor: `[_]`
- core_role: User-facing block template for the active-session plan-file immutability gate.
- algorithmic_behavior: Renders a concise block reason naming `{{PLAN_FILE}}`, stating that plan modifications are forbidden during an active session, prescribing cancel/update/restart steps, and showing `{{BACKUP_PATH}}` at `prompt-template/block/plan-file-modified.md:1-12`.
- inputs_outputs_state: Inputs are `PLAN_FILE` and `BACKUP_PATH` template variables. Output is a rendered markdown reason used in a hook block response. It does not mutate state.
- gates_or_invariants: Enforces the invariant that a tracked plan file must match its startup backup during the loop. The associated stop hook compares the current plan to backup and blocks when they differ at `hooks/loop-codex-stop-hook.sh:315-334`.
- dependencies_and_callers: Called by `hooks/loop-codex-stop-hook.sh:329-331` through `load_and_render_safe`. The template loader keeps missing placeholders literal and has fallback handling for missing or empty templates at `hooks/lib/template-loader.sh:167-203`.
- edge_cases_or_failure_modes: The hook has an earlier uncommitted-change path with an inline message at `hooks/loop-codex-stop-hook.sh:300-311`; this template covers content drift detected by backup diff. If `PLAN_FILE` or `BACKUP_PATH` is not supplied, the placeholder remains visible by design.
- validation_or_tests: Template reference existence is checked by `tests/test-template-references.sh:56-110`, and all templates are load/syntax checked by `tests/test-templates-comprehensive.sh:82-194`.
- skip_candidate: `no`

### CHANGE_TODOS_TO_TASKS-HZ-122 `file` `prompt-template/pr-loop/critical-requirements-no-comments.md`
- cursor: `[_]`
- core_role: Round-0 PR-loop prompt block for the no-existing-comments path, defining what the worker must do before the stop hook polls initial bot reviews.
- algorithmic_behavior: Instructs the user/agent to write a resolution summary to `{{RESOLVE_PATH}}`, note that Round 0 is awaiting initial bot reviews with no issues yet, then exit so the stop hook can poll; it explicitly forbids commenting on the PR to trigger review at `prompt-template/pr-loop/critical-requirements-no-comments.md:6-20`.
- inputs_outputs_state: Input is the `RESOLVE_PATH` template variable. Output is rendered markdown appended to the initial PR-loop prompt. Intended downstream state is a resolution summary file at that path and a stop-hook polling phase, not a PR comment.
- gates_or_invariants: Applies only when `COMMENT_COUNT` is zero. The invariant is that a fresh PR should wait for automatic bot review instead of manually triggering with a comment.
- dependencies_and_callers: `scripts/setup-pr-loop.sh:890-915` chooses this template when no comments exist and uses `load_and_render_safe` with an equivalent fallback. The same script defines PR-loop defaults and stop/cancel semantics at `scripts/setup-pr-loop.sh:17-31` and `scripts/setup-pr-loop.sh:99-105`.
- edge_cases_or_failure_modes: If `RESOLVE_PATH` is missing, the placeholder remains literal. If the template is missing or empty, setup falls back to embedded text at `scripts/setup-pr-loop.sh:893-914`. Using this template in a has-comments flow would suppress required PR comment/re-review behavior, so the `COMMENT_COUNT` branch is the critical selector.
- validation_or_tests: Loaded by the comprehensive template suite at `tests/test-templates-comprehensive.sh:82-194`; direct setup usage is also discoverable by repository reference checks, though `tests/test-template-references.sh` focuses primarily on hook template calls.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5 of 5 assigned rows have one evidence section above; item-id strings are used only as section headings.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`