# agent_16 dev-rlcr-with-swarm-team 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `0d5f0943ae9b1f80c5115aa946ebeb289e2cb83d`

## Item Evidence

### DEV_RLCR_WITH_SWARM_TEAM-HZ-016 `directory` `tests/robustness`
- cursor: `[_]`
- core_role: Recursive robustness specification suite for the Humanize/RLCR and PR-loop state machines. It is a flat directory of 17 executable Bash specs, all integrated into `tests/run-all-tests.sh` at lines 59-75, and sharing result/accounting helpers from `tests/test-helpers.sh:30-78`.
- algorithmic_behavior: The directory exercises edge cases around loop state parsing, active-session discovery, hook JSON validation, protected-file write/read gates, cancel authorization, PR-loop API polling, setup-script validation, timeout behavior, template rendering, git state parsing, and goal-tracker parsing. Test headings show 361 numbered test cases across the suite.
- inputs_outputs_state: Inputs are generated temp repos/files under `TEST_DIR`, mocked `gh`, mocked state files under `.humanize/rlcr` and `.humanize/pr-loop`, hook JSON payloads, shell commands, plan files, and template fixtures. Outputs are PASS/FAIL/SKIP counters and process exit status via `print_test_summary`; some specs also assert generated state, prompt, review, goal-tracker, or PR-comment output files.
- gates_or_invariants: The suite encodes invariants such as newest-loop-only “zombie-loop protection” (`test-session-robustness.sh:89-100`, `test-concurrent-state-robustness.sh:186-201`), strict parser rejection of missing schema fields (`test-state-file-robustness.sh:146-276`), cancel command whitelisting and symlink rejection (`test-cancel-security-robustness.sh:36-411`), setup mutual exclusion between active RLCR and PR loops (`test-setup-scripts-robustness.sh:532-600`), and prevention of broad or unsafe path/plan-file inputs (`test-path-validation-robustness.sh:176-486`).
- dependencies_and_callers: Children source `hooks/lib/loop-common.sh`, `hooks/lib/template-loader.sh`, `scripts/humanize.sh`, `scripts/portable-timeout.sh`, `scripts/setup-rlcr-loop.sh`, `scripts/setup-pr-loop.sh`, `scripts/fetch-pr-comments.sh`, `scripts/poll-pr-reviews.sh`, and hook validators. `tests/run-all-tests.sh:83-142` runs each suite and aggregates pass/fail counts.
- edge_cases_or_failure_modes: Covers malformed JSON, null/invalid bytes, deep nesting, CRLF, binary content, very long values/files, permission denial, missing files, symlinks, path metacharacters, shell injection, command substitution, stale/terminal states, corrupted state, rate limits, network errors, slow APIs, detached HEAD, rebase/merge state, empty repos, and timeout fallbacks.
- validation_or_tests: This item is itself validation. Key child roles: `test-state-file-robustness.sh` validates tolerant/strict state parsing; `test-session-robustness.sh` validates active loop discovery; `test-cancel-security-robustness.sh` validates `is_cancel_authorized`; `test-concurrent-state-robustness.sh` validates concurrent state reads and atomic writes; `test-hook-system-robustness.sh` validates validators and stop hooks; `test-pr-loop-api-robustness.sh` validates mocked GitHub API behavior.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-046 `file` `tests/setup-fixture-mock-gh.sh`
- cursor: `[_]`
- core_role: Fixture-backed mock `gh` CLI generator for deterministic PR-loop/fetch-poll tests. It turns static `tests/fixtures` JSON into a command executable named `gh`.
- algorithmic_behavior: Requires `<mock_bin_dir> <fixtures_dir>` (`tests/setup-fixture-mock-gh.sh:16-22`), creates `MOCK_BIN_DIR/gh` (`:24-31`), and dispatches by first CLI token: `auth status` succeeds, `repo view` emits owner/name/parent JSON, `pr view` emits number/state JSON, and `api` maps GitHub endpoints to fixture JSON (`:33-92`).
- inputs_outputs_state: Inputs are a destination mock bin directory, fixtures directory, and runtime `gh` arguments. Outputs are an executable mock at `$MOCK_BIN_DIR/gh` plus the printed mock-bin path (`:99-101`). No persistent repo state is changed outside the supplied mock directory.
- gates_or_invariants: Hard fails on missing arguments (`:19-22`). Known API routes must emit fixture files: issue comments from `issue_comments.json` (`:71-75`), review comments from `review_comments.json` (`:77-81`), and PR reviews from `pr_reviews.json` (`:83-87`). Unknown `api` routes intentionally return `[]` (`:89-91`); unknown top-level commands return exit 1 (`:95-96`).
- dependencies_and_callers: Called by `tests/test-pr-loop-hooks.sh:1234-1237` to place a mock `gh` on `PATH` for `fetch-pr-comments.sh` and `poll-pr-reviews.sh`. Mirrors production fetch temp filenames in `scripts/fetch-pr-comments.sh:172-174`.
- edge_cases_or_failure_modes: It does not validate fixture file existence; missing fixture JSON will fail at mock runtime via `cat`. Endpoint matching is substring-based, so it assumes production scripts call the expected `/issues/.../comments`, `/pulls/.../comments`, and `/pulls/.../reviews` shapes.
- validation_or_tests: Supports fixture tests named in `tests/test-pr-loop-hooks.sh:1243`, `:1323`, and `:1372`; those verify comment fetching, review polling, and after-filter behavior under deterministic GitHub API responses.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-076 `file` `hooks/lib/loop-common.sh`
- cursor: `[_]`
- core_role: Shared implementation library for RLCR and PR-loop hooks, setup/cancel scripts, validators, state parsing, active-loop discovery, protected-file gates, cancel security, git-add protection, review issue extraction, and PR goal-tracker updates.
- algorithmic_behavior: Defines state field constants and default Codex config (`hooks/lib/loop-common.sh:24-45`); validates hook JSON/UTF-8/null bytes (`:76-113`); discovers active loop directories with optional session filtering and terminal-state stale-loop prevention (`:180-291`); parses state in tolerant and strict modes (`:296-449`); detects Codex review issues by `[P?]` markers (`:468-511`); emits templated block messages (`:564-619`, `:1009-1025`, `:1149-1185`, `:1219-1229`); enforces cancel-command shape (`:670-829`); protects `.humanize` from accidental `git add` (`:1049-1145`); renames active state to terminal state in `end_loop` (`:1238-1264`); and idempotently updates PR goal tracker tables/logs (`:1287-1434`).
- inputs_outputs_state: Inputs include hook JSON, state files, loop base directories, command strings, file paths, review logs, and goal-tracker JSON. Outputs include exported/global `STATE_*` variables, rendered stderr block messages, active-loop paths, parsed round numbers, terminal `*-state.md` files, review-result files, and updated goal-tracker markdown.
- gates_or_invariants: Strict parser requires two YAML separators and required `current_round`, `max_iterations`, `review_started`, and `base_branch` fields (`:394-423`), numeric rounds/iteration values (`:424-434`), and boolean `review_started` (`:436-440`). `find_active_loop` only checks newest unfiltered dir to avoid reviving stale loops (`:215-227`, `:242-257`). `is_cancel_authorized` requires `.cancel-requested`, rejects substitution/operators/newlines/extra args/mixed quotes/remaining `$`, requires exact source/destination paths, and rejects symlink state files (`:674-829`). `git_adds_humanize` blocks direct `.humanize`, force broad adds, and broad adds when `.humanize` is unignored (`:1086-1141`).
- dependencies_and_callers: Sourced by hook validators and stop hooks: `hooks/loop-read-validator.sh:19`, `hooks/loop-write-validator.sh:19`, `hooks/loop-edit-validator.sh:18`, `hooks/loop-bash-validator.sh:18`, `hooks/loop-plan-file-validator.sh:17`, `hooks/loop-codex-stop-hook.sh:47`, `hooks/pr-loop-stop-hook.sh:54`, plus setup/cancel scripts (`scripts/setup-rlcr-loop.sh:31`, `scripts/setup-pr-loop.sh:40`, `scripts/cancel-rlcr-loop.sh:74`) and `scripts/humanize.sh:14-15`.
- edge_cases_or_failure_modes: Tolerant parsing defaults optional values and may return `0` for unreadable/malformed current round (`:299-305`, `:363-374`). CRLF frontmatter can fail exact `^---$` matching. Session filtering treats empty stored `session_id` as backward-compatible match (`:272-277`). `update_pr_goal_tracker` avoids double-counting by checking both summary row and log entry before adding totals (`:1303-1337`).
- validation_or_tests: Direct robustness coverage is broad: state parsing in `tests/robustness/test-state-file-robustness.sh`, active loops in `test-session-robustness.sh`, transitions in `test-state-transition-robustness.sh`, cancellation in `test-cancel-security-robustness.sh`, concurrent reads in `test-concurrent-state-robustness.sh`, hook behavior in `test-hook-system-robustness.sh`, and PR-loop API/goal-tracker paths in `test-pr-loop-api-robustness.sh`.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-106 `file` `prompt-template/block/wrong-file-location.md`
- cursor: `[_]`
- core_role: Template contract for the read-validator gate when an agent tries to read a loop prompt/summary from the wrong physical loop directory.
- algorithmic_behavior: Renders a short block headed “Wrong File Location” and interpolates `FILE_PATH`, `ACTIVE_LOOP_DIR`, and `CURRENT_ROUND` (`prompt-template/block/wrong-file-location.md:1-9`). It tells the agent the current prompt and summary file names, anchoring reads to `round-{{CURRENT_ROUND}}-prompt.md` and `round-{{CURRENT_ROUND}}-summary.md`.
- inputs_outputs_state: Inputs are template variables supplied by `hooks/loop-read-validator.sh:127-130`. Output is a rendered stderr message; it does not mutate state.
- gates_or_invariants: The invariant is directory locality: round prompt/summary access must use the active loop directory discovered from state, not an arbitrary matching filename elsewhere. The caller enforces this after resolving active state and current round (`hooks/loop-read-validator.sh:85-124`).
- dependencies_and_callers: Loaded through `load_and_render_safe` from `hooks/loop-read-validator.sh:127`; template loading itself is initialized by `loop-common.sh:156-165` through `template-loader.sh`.
- edge_cases_or_failure_modes: If the template is missing or invalid, the read validator has an inline fallback at `hooks/loop-read-validator.sh:124-126`. The final line says “If you need this file, use: `cat {{FILE_PATH}}`” (`prompt-template/block/wrong-file-location.md:9`), which is advisory text but could be confusing because the gate is actively blocking that path; the enforced behavior still comes from the validator.
- validation_or_tests: Template reference integrity is checked by `tests/test-template-references.sh:149-150`; wrong-location behavior is exercised through hook input/system robustness and comprehensive template tests.
- skip_candidate: `no`

### DEV_RLCR_WITH_SWARM_TEAM-HZ-136 `file` `tests/robustness/test-concurrent-state-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness spec for concurrent and degraded state access in the RLCR/PR-loop state machine, focused on `loop-common.sh` helpers.
- algorithmic_behavior: Builds synthetic state files with `create_state_file` (`tests/robustness/test-concurrent-state-robustness.sh:30-50`), sources `loop-common.sh` (`:72`), and runs 22 test cases over parsing, active-loop discovery, concurrent reads, atomic write visibility, strict validation, PR-loop detection, stale loop rejection, and numeric/permission edge cases.
- inputs_outputs_state: Inputs are temporary `.humanize`-style directory trees and generated `state.md`, `finalize-state.md`, and `cancel-state.md` files. Outputs are PASS/FAIL counters via `print_test_summary` (`:558-559`); transient state files are confined to `TEST_DIR`.
- gates_or_invariants: `get_current_round` must tolerate whitespace, empty values, comments, CRLF degradation, Unicode content, zero and large values (`:59-160`, `:373-387`, `:494-527`). `find_active_loop` must return the newest active loop, prefer `finalize-state.md`, reject nonexistent/empty bases, and avoid older stale state when the newest dir has no active state (`:170-240`, `:452-484`). Atomic `mv` writes should never expose nonnumeric reads (`:279-322`).
- dependencies_and_callers: Sources `tests/test-helpers.sh` at `:17` and `hooks/lib/loop-common.sh` at `:72`; uses `get_current_round`, `find_active_loop`, `parse_state_file_strict`, and `find_active_pr_loop`. Included in global test execution at `tests/run-all-tests.sh:71`.
- edge_cases_or_failure_modes: Accepts either default `0` or parsed values for some formatting-degradation cases (`:94-98`, `:117-121`, `:134-139`), reflecting tolerant behavior rather than strict YAML parsing. The “malformed YAML” strict test expects nonzero exit (`:332-351`), but strict parsing is field/format based rather than a full YAML parser. Permission handling is skipped when running as root (`:529-552`).
- validation_or_tests: This file is itself validation. It specifically stress-tests simultaneous 10-reader access (`:250-277`) and 20 reads during 50 atomic writer iterations (`:285-321`), proving read paths tolerate concurrent scheduler/hook access when writers use temp-file plus `mv`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5 item evidence sections above; each assigned item section heading is present once and no item sections were merged.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`