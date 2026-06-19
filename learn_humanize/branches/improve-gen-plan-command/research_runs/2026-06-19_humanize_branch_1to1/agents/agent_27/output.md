# agent_27 improve-gen-plan-command 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 4
- source_commit: `934cf543d66046b72071d121b15583d5e3d6799e`

## Item Evidence

### IMPROVE_GEN_PLAN_COMMAND-HZ-027 `file` `hooks/loop-plan-file-validator.sh`
- cursor: `[_]`
- core_role: RLCR `UserPromptSubmit` guard that prevents loop progress when the loop state schema, branch, or plan-file tracking invariant is unsafe. It is wired in `hooks/hooks.json:4`-`10`.
- algorithmic_behavior: Reads hook stdin, finds the newest active `.humanize/rlcr/<timestamp>` loop via `find_active_loop`, prefers `finalize-state.md` over `state.md`, strictly parses YAML frontmatter, then gates on required v1.1.2 fields, branch consistency, and git tracking state. No active loop exits allow at `hooks/loop-plan-file-validator.sh:29`-`35`.
- inputs_outputs_state: Inputs are hook JSON stdin, `CLAUDE_PROJECT_DIR`/cwd, active RLCR state file, git branch/status, and `plan_file`/`plan_tracked`/`start_branch` state fields. Outputs are either silence with exit `0` for allow, or Claude hook JSON `{"decision":"block","reason":...}` with exit `0` for policy blocks. Malformed state is a hard shell failure path with stderr and exit `1` at `hooks/loop-plan-file-validator.sh:44`-`48`.
- gates_or_invariants: Requires nonempty `plan_tracked` and `start_branch` after strict parse at `hooks/loop-plan-file-validator.sh:79`-`89`; rejects branch drift from `start_branch` at `hooks/loop-plan-file-validator.sh:95`-`115`; when `plan_tracked=true`, requires the plan still be tracked and clean at `hooks/loop-plan-file-validator.sh:123`-`192`; when false, requires it remain untracked/gitignored at `hooks/loop-plan-file-validator.sh:193`-`228`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` for strict state parsing, field constants, templates, and active-loop discovery; sources `scripts/portable-timeout.sh` for bounded git calls; uses `jq` to JSON-escape rendered schema errors. `parse_state_file_strict` strips quotes from `start_branch` and `plan_file` in `hooks/lib/loop-common.sh:260`-`268`.
- edge_cases_or_failure_modes: Fails closed on git branch lookup timeout/failure, `git ls-files` timeout/unknown error, and `git status` timeout/unknown error. Timeout code `124` gets explicit messages; malformed state exits `1`, while schema-outdated state blocks with rendered `block/schema-outdated.md`.
- validation_or_tests: `tests/test-plan-file-hooks.sh` covers valid pass, quoted `plan_file`, missing `plan_tracked`, missing `start_branch`, branch switching, quoted `start_branch`, branch mismatch with quotes, and hyphenated plan path at lines `91`-`185` and `337`-`460`. Related stop-hook integrity tests verify the same state fields and plan backup/content invariants at `tests/test-plan-file-hooks.sh:469`-`731`.
- skip_candidate: `no`

### IMPROVE_GEN_PLAN_COMMAND-HZ-057 `file` `tests/test-plan-file-hooks.sh`
- cursor: `[_]`
- core_role: Executable specification for RLCR plan-file immutability, state schema compatibility, branch pinning, and hook bypass resistance across `UserPromptSubmit`, `PreToolUse`, and `Stop` hooks.
- algorithmic_behavior: Creates isolated temp git repos, initializes `.humanize/rlcr/<timestamp>` state and plan backup, invokes validators with synthetic Claude hook JSON, then asserts allow/block outcomes by exit code and output text. Setup writes gitignored plan files, loop backup `plan.md`, and YAML frontmatter including `plan_tracked` and `start_branch` at `tests/test-plan-file-hooks.sh:37`-`86`.
- inputs_outputs_state: Inputs are temp repo state files, hook JSON payloads for `Write`, `Edit`, and `Bash`, local git state, and generated goal trackers/summaries. Outputs are pass/fail counters and process exit equal to `TESTS_FAILED` at `tests/test-plan-file-hooks.sh:1056`-`1065`.
- gates_or_invariants: Specifies that `loop-plan-file-validator.sh` allows valid state silently, blocks schema gaps with JSON containing the missing field, and blocks branch drift. Specifies that Write/Edit/Bash validators block `.humanize/rlcr/.../plan.md` backup mutation with exit `2`, while legacy `.humanize-loop.local` paths are allowed at `tests/test-plan-file-hooks.sh:1012`-`1054`.
- dependencies_and_callers: Calls `hooks/loop-plan-file-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-bash-validator.sh`, and `hooks/loop-codex-stop-hook.sh`. It indirectly exercises `hooks/lib/loop-common.sh` path/state parsing, `command_modifies_file`, and stop-hook plan integrity/goal-tracker checks.
- edge_cases_or_failure_modes: Covers command-substitution, glob, brace, pipe, and backtick bypass attempts against Bash plan backup protection at `tests/test-plan-file-hooks.sh:268`-`335`. Covers YAML quote stripping, hyphenated plan paths, deleted original plan, missing backup, uncommitted tracked-plan edits, and committed tracked-plan edits where `git status` is clean but backup diff catches mutation.
- validation_or_tests: Test cases are grouped by hook class: UserPromptSubmit tests `1`-`4`; Write/Edit/Bash tests `5`-`8.5`; YAML/stop-hook parsing tests `8.6`-`8.9`; stop-hook plan integrity tests `9`-`14`; section-specific goal-tracker placeholder tests `14.1`-`14.4`; legacy negative tests `15`-`17`.
- skip_candidate: `no`

### IMPROVE_GEN_PLAN_COMMAND-HZ-087 `file` `prompt-template/block/large-files.md`
- cursor: `[_]`
- core_role: Stop-hook block template used when RLCR exit validation detects changed tracked/new files over the configured line-count threshold.
- algorithmic_behavior: Provides a rendered human-facing block reason with `{{MAX_LINES}}` and `{{LARGE_FILES}}` placeholders, then instructs code files to be split into modular files and documentation files into logical sections while preserving behavior/narrative. Template content is at `prompt-template/block/large-files.md:1`-`25`.
- inputs_outputs_state: Inputs are template variables from `loop-codex-stop-hook.sh`: `MAX_LINES=2000` and a newline list of offending files with line counts and inferred type. Output is the `reason` field of a Stop hook JSON block, rendered by `load_and_render_safe`.
- gates_or_invariants: Enforces a review/maintainability gate before exit: each changed code/doc file must be under `MAX_LINES`; code splitting must keep functionality “strictly unchanged”; docs splitting must preserve cross-references and navigation.
- dependencies_and_callers: Called from `hooks/loop-codex-stop-hook.sh:402`-`422` after git status is cached and modified/new files are scanned. File type is inferred by extension in `hooks/loop-codex-stop-hook.sh:373`-`388`; line count and threshold comparison occur at `hooks/loop-codex-stop-hook.sh:390`-`399`. Rendering is via the single-pass template loader in `hooks/lib/template-loader.sh:50`-`132`.
- edge_cases_or_failure_modes: Only changed paths from `git status --porcelain` are scanned, renamed paths use the post-rename target, deleted files are skipped, unknown extensions are ignored, and nonnumeric `wc -l` output is ignored. If template loading fails, stop hook falls back to an inline shorter large-file message at `hooks/loop-codex-stop-hook.sh:402`-`409`.
- validation_or_tests: Template reference existence is covered by the template reference scanner patterns in `tests/test-template-references.sh:83`-`110`; template rendering/fallback behavior is covered generically by `tests/test-template-loader.sh:196`-`220`. I did not find a dedicated large-file threshold fixture in the assigned test file.
- skip_candidate: `no`

### IMPROVE_GEN_PLAN_COMMAND-HZ-117 `file` `prompt-template/pr-loop/goal-tracker-initial.md`
- cursor: `[_]`
- core_role: Initial PR-loop goal tracker template defining the starting state for review-bot approval tracking.
- algorithmic_behavior: Renders PR metadata, ultimate goal, an initial issue-summary table, zeroed aggregate statistics, and an initial Round 0 issue log. It establishes the PR-loop state as “awaiting initial reviews” with zero found/resolved/remaining issues at `prompt-template/pr-loop/goal-tracker-initial.md:15`-`32`.
- inputs_outputs_state: Inputs are `PR_NUMBER`, `START_BRANCH`, `STARTED_AT`, `ACTIVE_BOTS_DISPLAY`, and `STARTUP_CASE`. Output is `.humanize/pr-loop/<timestamp>/goal-tracker.md`, written by `scripts/setup-pr-loop.sh:561`-`633`.
- gates_or_invariants: The initial tracker records the monitored bot set and makes approval from all monitored bots the ultimate goal at `prompt-template/pr-loop/goal-tracker-initial.md:11`-`14`. The initial counters all start at `0`, creating a deterministic baseline for later PR-loop stop-hook and updater logic.
- dependencies_and_callers: Rendered by `load_and_render_safe "$TEMPLATE_DIR" "pr-loop/goal-tracker-initial.md"` in `scripts/setup-pr-loop.sh:578`-`633`. Template variables are assembled from PR setup state and active bot selection; the fallback goal tracker in the same script contains a richer legacy schema with acceptance criteria/current status/log sections.
- edge_cases_or_failure_modes: Missing template falls back to the inline tracker at `scripts/setup-pr-loop.sh:588`-`630`, whose schema differs from this file by including Acceptance Criteria and Current Status sections. Because render substitution is single-pass, placeholder-like text inside variable values is not recursively expanded.
- validation_or_tests: `tests/test-pr-loop-system.sh:641`-`654` asserts this template contains `Issue Summary`, `Total Statistics`, `Issue Log`, and the three total-stat fields. Template loader behavior is covered by `tests/test-template-loader.sh`, especially missing-template fallback and normal existing-template rendering.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 4 item sections, matching the 4 assigned rows
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`