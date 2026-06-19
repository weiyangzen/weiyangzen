# agent_13 fix-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `81f6f49d816a90a0e719db41ce15c4636ab9858a`

## Item Evidence

### FIX_PR_LOOP-HZ-013 `directory` `prompt-template/plan`
- cursor: `[_]`
- core_role: Plan-generation template surface. The directory recursively contains one child, `prompt-template/plan/gen-plan-template.md`, which defines the canonical structure for generated implementation plans rather than runtime loop code.
- algorithmic_behavior: The child template forces generated plans into deterministic sections: goal description, TDD-style acceptance criteria with positive and negative tests, path boundaries, allowed choices, feasibility hints, dependencies/sequence, and code-style constraints. Key contract lines: TDD criteria at `prompt-template/plan/gen-plan-template.md:6-23`, scope bounds at `:25-44`, non-prescriptive hints at `:46-55`, dependency sequencing at `:57-67`, and implementation-note restrictions at `:69-74`.
- inputs_outputs_state: Its direct caller is `scripts/validate-gen-plan-io.sh`, which validates `--input` and `--output`, resolves the template path, copies `gen-plan-template.md`, then appends the original draft between marker lines (`scripts/validate-gen-plan-io.sh:133-157`). Output is a new plan file; no loop state is mutated by the template itself.
- gates_or_invariants: The validation script rejects missing/empty input, nonexistent output directory, existing output path, no write permission, and missing template (`scripts/validate-gen-plan-io.sh:79-145`). The template itself encodes plan invariants: acceptance criteria should be testable, upper/lower bounds constrain scope, and implementation code must not inherit plan workflow terms.
- dependencies_and_callers: Depends on the gen-plan IO validator and plugin-root/template path resolution (`scripts/validate-gen-plan-io.sh:133-140`). It coordinates with the broader RLCR system by shaping the plan file later referenced by state and plan validators.
- edge_cases_or_failure_modes: Template absence is treated as plugin configuration error exit `7`; existing output path exits `4`; the template can produce a plan with placeholders if not filled by the user or downstream analysis. Directory inspection found no nested descendants beyond the one file.
- validation_or_tests: Covered indirectly by gen-plan validation behavior. I did not execute it because the branch export is read-only and the script writes the output plan.
- skip_candidate: `no`

### FIX_PR_LOOP-HZ-043 `file` `tests/manual-monitor-test.sh`
- cursor: `[_]`
- core_role: Manual executable specification for RLCR monitor shutdown behavior when `.humanize/` disappears during monitoring.
- algorithmic_behavior: Implements three commands. `setup` creates `.humanize/rlcr/2026-01-16_99-99-99/` plus `state.md` and `goal-tracker.md` fixtures (`tests/manual-monitor-test.sh:23-46`). `delete` removes `.humanize` and tells the operator what monitor behavior to verify (`:47-57`). `cleanup` removes leftovers (`:58-62`).
- inputs_outputs_state: Input is a single CLI verb: `setup`, `delete`, or `cleanup`; invalid usage exits `1` (`:63-71`). Outputs are terminal instructions and filesystem changes under the project root. State transition under test is active monitor session present -> `.humanize/` deleted -> monitor exits cleanly.
- gates_or_invariants: Expected observations are explicit: message `Monitoring stopped: .humanize/rlcr directory no longer exists`, terminal restored, cursor/scroll reset, and no shell glob errors (`:51-54`).
- dependencies_and_callers: Depends on an operator running `source scripts/humanize.sh && humanize monitor rlcr` in another terminal (`:10-14`, `:43-45`). It exercises monitor behavior from `scripts/humanize.sh`, not the hook validators directly.
- edge_cases_or_failure_modes: Destructive in the current project because it uses `rm -rf .humanize` (`:49`, `:60`). The fixture `state.md` lacks YAML frontmatter separators, so it is suitable for monitor tolerance testing but not for strict hook parser paths. The timestamp is synthetic and sorts as a session directory name.
- validation_or_tests: Manual-only; it is not listed in `tests/run-all-tests.sh`. I did not run it because it writes and deletes `.humanize/` in a read-only branch export.
- skip_candidate: `no`

### FIX_PR_LOOP-HZ-073 `file` `hooks/lib/loop-common.sh`
- cursor: `[_]`
- core_role: Shared algorithm library for RLCR and PR-loop hooks. It centralizes state-field constants, JSON hook input validation, active-loop discovery, state parsing, template-backed block messages, cancel authorization, PR-loop helpers, command mutation detection, loop termination, and PR goal-tracker reconciliation.
- algorithmic_behavior: `validate_hook_input` rejects null bytes, invalid UTF-8 when `iconv` exists, invalid JSON, and missing `tool_name` (`hooks/lib/loop-common.sh:59-96`). `is_deeply_nested` rejects JSON depth above a caller-provided threshold (`:119-133`). `find_active_loop` and `find_active_pr_loop` select only the newest timestamp directory with active state (`:151-174`, `:795-814`). `parse_state_file` is tolerant with defaults (`:209-244`), while `parse_state_file_strict` fails closed for missing frontmatter, missing required fields, nonnumeric rounds/iterations, invalid `review_started`, or missing `base_branch` (`:255-330`). `detect_review_issues` scans Codex review logs for `[P0-9]` markers in the first 10 characters and writes an extracted result file (`:349-392`).
- inputs_outputs_state: Inputs are function args, hook JSON, state files, log files, and active loop directories. Outputs include exported globals such as `VALIDATED_TOOL_NAME`, `STATE_CURRENT_ROUND`, rendered stderr block messages, return codes, generated review-result files, renamed state files, and updated PR goal trackers. `end_loop` mutates loop state by renaming `state.md` to `{complete,cancel,maxiter,stop,unexpected}-state.md` (`:1119-1145`). `update_pr_goal_tracker` mutates issue summary totals and appends per-round log entries idempotently by round+reviewer (`:1168-1315`).
- gates_or_invariants: Hook inputs must be valid JSON and not too deep before tool-specific policy runs; strict state parsing is used by validators to block malformed loop state. Cancel is allowed only with `.cancel-requested`, no command substitution/newlines/chaining, exact `mv state.md|finalize-state.md cancel-state.md`, no remaining `$`, no extra args, matching quote style, and nonsymlink source (`:551-710`). `.humanize` git-add protection blocks direct, force, broad, and all-scope adds when risky (`:930-1026`). `command_modifies_file` detects redirection, `tee`, in-place edits, `mv/cp`, `rm`, `dd`, `truncate`, `printf >`, and fd redirection (`:1071-1096`).
- dependencies_and_callers: Sources `hooks/lib/template-loader.sh` and initializes `TEMPLATE_DIR` (`:139-149`). Called by `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-bash-validator.sh`, `hooks/loop-plan-file-validator.sh`, `hooks/pr-loop-stop-hook.sh`, and `hooks/loop-codex-stop-hook.sh`. Concrete call sites include JSON/depth gates in read/write/bash validators (`hooks/loop-read-validator.sh:25-45`, `hooks/loop-write-validator.sh:25-45`, `hooks/loop-bash-validator.sh:24-44`), strict state parsing in plan validation (`hooks/loop-plan-file-validator.sh:29-48`), PR-loop discovery in the PR stop hook (`hooks/pr-loop-stop-hook.sh:51-65`), and Codex review handling (`hooks/loop-codex-stop-hook.sh:986-1015`).
- edge_cases_or_failure_modes: If `iconv` is absent, invalid UTF-8 validation is skipped. Bash command substitution can strip null bytes before this library sees them, which the robustness test documents. Strict parser accepts negative numeric values because the regex allows `^-?[0-9]+$`. `_normalize_path` only collapses `/./` and `//`, not `..`. Active-loop discovery intentionally ignores older active directories. Regex-based shell detection is necessarily conservative and can miss unusual shell syntax or overblock matching filenames.
- validation_or_tests: Exercised by `tests/robustness/test-hook-input-robustness.sh`, `tests/test-bash-validator-patterns.sh`, `tests/test-cancel-signal-file.sh`, `tests/robustness/test-cancel-security-robustness.sh`, `tests/robustness/test-state-file-robustness.sh`, and related hook/system tests. The robustness suite is included in `tests/run-all-tests.sh:55-72`.
- skip_candidate: `no`

### FIX_PR_LOOP-HZ-103 `file` `prompt-template/block/wrong-file-location.md`
- cursor: `[_]`
- core_role: Template-backed block message for the read validator when an agent tries to read a round prompt/summary file from outside the active `.humanize/rlcr/` loop directory.
- algorithmic_behavior: Renders `{{FILE_PATH}}`, `{{ACTIVE_LOOP_DIR}}`, and `{{CURRENT_ROUND}}`; it points the agent to the current round prompt and summary paths (`prompt-template/block/wrong-file-location.md:1-9`). The runtime gate is in `hooks/loop-read-validator.sh`: if a `round-N-summary.md` or `round-N-prompt.md` read is outside `.humanize/rlcr/`, it renders this template and exits `2` (`hooks/loop-read-validator.sh:118-132`).
- inputs_outputs_state: Inputs are render variables from the active loop discovery and strict state parser. Output is a stderr block message; no filesystem state changes occur.
- gates_or_invariants: The gate preserves round-file locality: round prompt/summary reads must come from the newest active loop directory and the current round unless allowlisted later by round validation. Template rendering is single-pass via `template-loader.sh`, so injected `{{VAR}}` inside values is not recursively expanded (`hooks/lib/template-loader.sh:50-131`).
- dependencies_and_callers: Loaded through `load_and_render_safe` from `hooks/loop-read-validator.sh:127-130`; fallback text exists in the caller if the template is missing. Template discovery and fallback behavior come from `hooks/lib/template-loader.sh:167-203`.
- edge_cases_or_failure_modes: The final line says `cat {{FILE_PATH}}`, which can be confusing because it repeats the originally blocked path rather than a corrected path; because this is a read-hook block, Bash `cat` may also avoid the Read-tool-specific location gate. That may be intentional for non-loop files with round-like names, but it is a UX/security ambiguity worth noting.
- validation_or_tests: Template existence and safe rendering are checked by template-reference and template-loader tests; read-validator behavior is covered by hook robustness tests that pipe JSON into real validators.
- skip_candidate: `no`

### FIX_PR_LOOP-HZ-133 `file` `tests/robustness/test-hook-input-robustness.sh`
- cursor: `[_]`
- core_role: Automated executable specification for hook JSON parsing robustness plus monitor edge-case behavior.
- algorithmic_behavior: Sets up a temporary test dir, sources `loop-common.sh` and test helpers, then pipes JSON into the actual read/write/bash validators (`tests/robustness/test-hook-input-robustness.sh:14-40`). It verifies valid Read/Write/Bash JSON passes (`:35-69`), malformed JSON and missing fields reject without signal crashes (`:71-115`), long/special/Unicode commands are handled (`:117-160`), unknown tool names pass through (`:163-175`), deep JSON rejects (`:177-199`), non-UTF8 rejects with exit `1` (`:201-217`), and null bytes do not crash even if Bash strips them (`:219-235`).
- inputs_outputs_state: No CLI args. Inputs are generated JSON strings, temporary logs, temporary `.humanize/rlcr` sessions, fake HOME/cache dirs, and shimmed terminal functions. Outputs are PASS/FAIL lines and an aggregate exit code from `print_test_summary` (`:666-671`). State is isolated through `setup_test_dir`, which uses `mktemp -d` and traps cleanup (`tests/test-helpers.sh:84-89`).
- gates_or_invariants: Validator gates are expressed as exit-code expectations: valid inputs exit `0`; invalid JSON/missing fields/deep nesting exit nonzero `<128`; non-UTF8 must exit `1`; monitor scenarios must exit `<128` to prove graceful behavior. Command mutation detection must identify `sed -i` and redirection patterns via `command_modifies_file` (`tests/robustness/test-hook-input-robustness.sh:343-370`).
- dependencies_and_callers: Depends on `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-bash-validator.sh`, `hooks/lib/loop-common.sh`, `scripts/humanize.sh`, and `tests/test-helpers.sh`. It is part of the main robustness list in `tests/run-all-tests.sh:55-72`.
- edge_cases_or_failure_modes: Binary and null-byte behavior depends on shell transport and locale; the script explicitly notes Bash strips null bytes before hook code may see them (`:219-230`). Monitor integration creates runner scripts in temp dirs, shims `tput`/`clear`, deletes session directories asynchronously, and only asserts non-signal exit rather than exact rendered monitor content (`:444-664`).
- validation_or_tests: This file is itself the validation asset. I did not run it because the current branch export is read-only and the script creates temp files, fake project trees, runner scripts, and monitor fixtures.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5 item sections, matching the 5 assigned rows
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`