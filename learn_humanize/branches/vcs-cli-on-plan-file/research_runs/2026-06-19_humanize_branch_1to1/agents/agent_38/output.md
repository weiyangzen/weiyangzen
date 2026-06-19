# agent_38 vcs-cli-on-plan-file 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `4dd1ca2fece39d3c6d7f84965cd71bda02489397`

## Item Evidence

### VCS_CLI_ON_PLAN_FILE-HZ-038 `file` `prompt-template/block/goal-tracker-bash-write.md`
- cursor: `[_]`
- core_role: This is a prompt/block template used by the RLCR loop Bash validator to explain a blocked write path for `goal-tracker.md`. Its specific role is user-facing remediation for Round 0 Bash-based goal tracker writes: it tells the agent that shell writes are not allowed and points to the correct file path for Write/Edit-based modification. The template content is only 8 lines and centers on the `{{CORRECT_PATH}}` placeholder at `prompt-template/block/goal-tracker-bash-write.md:5`.

- algorithmic_behavior: The file is not executable logic by itself; it participates in a validation transition through `goal_tracker_bash_blocked_message` in `hooks/lib/loop-common.sh:295`. That helper renders this template via `load_and_render_safe "$TEMPLATE_DIR" "block/goal-tracker-bash-write.md" ... "CORRECT_PATH=$correct_path"` at `hooks/lib/loop-common.sh:303`. The actual gate is in `hooks/loop-bash-validator.sh`: Bash hook input is parsed, non-Bash tools are ignored, the active loop and current round are resolved, and then `command_modifies_file "$COMMAND_LOWER" "goal-tracker\.md"` triggers the goal-tracker branch at `hooks/loop-bash-validator.sh:166`. In Round 0, the validator emits this template and exits with status `2` at `hooks/loop-bash-validator.sh:167-174`.

- inputs_outputs_state: Input to this template is one render variable: `CORRECT_PATH`, normally set to `$ACTIVE_LOOP_DIR/goal-tracker.md` by `hooks/loop-bash-validator.sh:168-169`. The rendered output is a Markdown block headed `Bash Write Blocked: Use Write or Edit Tool` from `prompt-template/block/goal-tracker-bash-write.md:1`, followed by the prohibition and corrected path. State transition is external: the Bash command is rejected before mutation, preserving `goal-tracker.md` so subsequent Write/Edit validators can enforce their own checks. No repository or loop state is mutated by the template itself.

- gates_or_invariants: The invariant enforced around this template is that Bash commands such as redirection, `tee`, in-place `sed`, in-place `awk`, `perl -i`, `mv`/`cp`, and `dd of=` must not bypass validation for `goal-tracker.md`; those command patterns are defined in `command_modifies_file` at `hooks/lib/loop-common.sh:324-347`. The template states the reason explicitly: Bash commands bypass validation hooks at `prompt-template/block/goal-tracker-bash-write.md:7`. The Round 0 gate differs from later rounds: Round 0 Bash writes get this Write/Edit remediation, while Round > 0 goal tracker modifications are routed to `goal_tracker_blocked_message` and the summary-request path at `hooks/loop-bash-validator.sh:170-172`.

- dependencies_and_callers: Direct caller is `goal_tracker_bash_blocked_message` in `hooks/lib/loop-common.sh:297-303`. The only discovered runtime path to that helper is the Bash pre-tool validator in `hooks/loop-bash-validator.sh:166-174`. Template resolution depends on `hooks/lib/template-loader.sh`: `get_template_dir` points to `prompt-template` at `hooks/lib/template-loader.sh:11-16`, `load_template` reads the file if present at `hooks/lib/template-loader.sh:21-33`, and `render_template` performs single-pass `{{VAR}}` substitution at `hooks/lib/template-loader.sh:43-117`. The safe wrapper falls back to inline text if the template is missing or renders empty at `hooks/lib/template-loader.sh:155-188`. The template is also included in the common-template existence list in `tests/test-template-references.sh:153-160`.

- edge_cases_or_failure_modes: If no active loop is found, the Bash validator exits without reaching this gate at `hooks/loop-bash-validator.sh:36-42`. If the command is not reported as tool `Bash`, the hook exits at `hooks/loop-bash-validator.sh:22-27`. If the template file is missing or empty, `load_and_render_safe` uses the fallback string in `goal_tracker_bash_blocked_message`, still substituting `CORRECT_PATH`, so the block degrades gracefully rather than allowing the write. Detection is regex-based over a lowercased shell command, so unusual shell constructs not represented in `command_modifies_file` could evade this specific gate; conversely, commands matching the write patterns are blocked without deeper shell parsing. If `CURRENT_ROUND` is not `0`, this file is intentionally not used; the stricter post-Round 0 template is `prompt-template/block/goal-tracker-modification.md`.

- validation_or_tests: Direct validation coverage is template/reference focused rather than a dedicated behavioral test for this exact block. `tests/test-template-references.sh:153-160` asserts that `block/goal-tracker-bash-write.md` exists among common templates. The same test script checks template references under hooks and includes `hooks/loop-bash-validator.sh` in its reference scan at `tests/test-template-references.sh:63`. The template loader behavior is validated by `tests/test-template-loader.sh:197-222`, which confirms `load_and_render_safe` uses a fallback for missing templates and uses an existing template when available. No specific test was found that invokes `loop-bash-validator.sh` with a Round 0 Bash command targeting `goal-tracker.md`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 item section present for the assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`