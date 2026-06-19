# agent_141 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-141 `file` `prompt-template/block/summary-bash-write.md`
- cursor: `[_]`
- core_role:
  - `prompt-template/block/summary-bash-write.md` is a blocking-message template used by the RLCR Bash pre-tool validator when a shell command attempts to modify a round summary file.
  - The template is not executable algorithm code itself; it is the user-facing contract emitted by the algorithmic gate. Its role is to redirect summary-file mutations from Bash redirection or shell editing into the `Write` or `Edit` tool path so the write/edit validators can enforce round-scoped summary invariants.
  - The file’s own content is compact: title at `prompt-template/block/summary-bash-write.md:1`, prohibition at `prompt-template/block/summary-bash-write.md:3`, corrected destination placeholder at `prompt-template/block/summary-bash-write.md:5`, and rationale about validation-hook bypass at `prompt-template/block/summary-bash-write.md:7-8`.

- algorithmic_behavior:
  - Trigger path:
    - `hooks/loop-bash-validator.sh` accepts only Bash tool input after JSON validation and exits early for non-Bash tools at `hooks/loop-bash-validator.sh:24-38`.
    - It resolves the project root via `resolve_project_root`, derives `.humanize/rlcr`, and finds the active loop directory at `hooks/loop-bash-validator.sh:52-60`.
    - It reads the active state file and assigns `CURRENT_ROUND` before the summary-file gate; the relevant flow is indicated by `hooks/loop-bash-validator.sh:191-200`.
    - The summary gate runs at `hooks/loop-bash-validator.sh:511-520`: if `command_modifies_file "$COMMAND_LOWER" "round-[0-9]+-summary\.md"` matches, the validator sets `CORRECT_PATH="$ACTIVE_LOOP_DIR/round-${CURRENT_ROUND}-summary.md"`, renders this template through `summary_bash_blocked_message`, writes it to stderr, and exits `2`.
  - Rendering path:
    - `summary_bash_blocked_message` is defined in `hooks/lib/loop-common.sh:892-901`; it calls `load_and_render_safe "$TEMPLATE_DIR" "block/summary-bash-write.md"` with `CORRECT_PATH=<active loop current summary path>`.
    - `load_and_render_safe` loads the template, renders variables, and falls back to an inline message if the template is missing or empty at `hooks/lib/template-loader.sh:185-211`.
    - Placeholder rendering uses single-pass `{{VAR}}` substitution through `render_template`, preserving unknown placeholders and preventing recursive placeholder expansion at `hooks/lib/template-loader.sh:48-136`.
  - Command matching:
    - `command_modifies_file` detects common Bash write/edit forms: `>`, `>>`, `tee`, `sed -i`, `awk -i inplace`, `perl -i`, `mv`/`cp` to destination, `rm`, `dd of=`, `truncate`, `printf ... >`, and `exec fd>` at `hooks/lib/loop-common.sh:1482-1510`.
    - This means the template is emitted only after command-pattern detection, not during normal summary reads such as `cat round-5-summary.md`.

- inputs_outputs_state:
  - Inputs:
    - Template variable `{{CORRECT_PATH}}`, supplied by `summary_bash_blocked_message` from the active loop directory and current round at `hooks/loop-bash-validator.sh:516-518`.
    - Bash command text from hook input, lowercased before matching at `hooks/loop-bash-validator.sh:45-46`.
    - Active loop state, located by `find_active_loop`; it returns a session-matched active RLCR directory or empty at `hooks/lib/loop-common.sh:332-357` and following session-filter logic.
    - Project-root resolution goes through `resolve_project_root`, which prefers `CLAUDE_PROJECT_DIR`, then `git rev-parse --show-toplevel`, and canonicalizes with `realpath` at `hooks/lib/project-root.sh:41-53`.
  - Outputs:
    - Rendered Markdown block to stderr. The user-visible message includes:
      - “Do not use Bash commands to modify summary files” from `prompt-template/block/summary-bash-write.md:3`.
      - “Use the Write or Edit tool instead” plus the rendered corrected path from `prompt-template/block/summary-bash-write.md:5`.
      - A reason that Bash commands bypass validation hooks and therefore skip round-number validation from `prompt-template/block/summary-bash-write.md:7-8`.
    - Bash validator process exits with status `2` when this gate fires at `hooks/loop-bash-validator.sh:518-519`, which is the blocking signal.
  - State transitions:
    - This template does not mutate repository or loop state.
    - The associated gate transitions the attempted Bash operation from “would execute” to “blocked before execution,” preserving the invariant that summary mutations must pass through write/edit validation hooks.
    - Because the rendered `CORRECT_PATH` is computed from `ACTIVE_LOOP_DIR` plus `CURRENT_ROUND`, the user is redirected to the current round summary rather than the arbitrary summary path referenced in the blocked command.

- gates_or_invariants:
  - Summary files must not be modified via Bash because shell redirection and in-place CLI edits bypass `Write`/`Edit` validators. The template states that invariant directly at `prompt-template/block/summary-bash-write.md:3-8`.
  - The correct write destination is the active loop’s current round summary path, not necessarily the round number appearing in the blocked command; this is enforced by `CORRECT_PATH="$ACTIVE_LOOP_DIR/round-${CURRENT_ROUND}-summary.md"` at `hooks/loop-bash-validator.sh:517`.
  - The Bash gate is specific to `round-[0-9]+-summary.md` at `hooks/loop-bash-validator.sh:516`; finalize summaries are governed elsewhere by finalize-phase write/stop-hook logic rather than this template.
  - The gate depends on an active loop. If no active loop is found, the Bash validator exits permissively before these loop-file gates; active-loop discovery is performed at `hooks/loop-bash-validator.sh:52-60`, with no-active-loop handling indicated later at `hooks/loop-bash-validator.sh:156`.
  - The branch’s realpath theme is relevant in the dependency path: `resolve_project_root` canonicalizes root paths using `realpath` to avoid symlink-prefix divergence at `hooks/lib/project-root.sh:14-20` and `hooks/lib/project-root.sh:41-53`.

- dependencies_and_callers:
  - Direct caller:
    - `hooks/lib/loop-common.sh:894-900` defines `summary_bash_blocked_message` and references `block/summary-bash-write.md`.
  - Primary runtime caller:
    - `hooks/loop-bash-validator.sh:516-519` calls `summary_bash_blocked_message` when `command_modifies_file` detects Bash modification of `round-N-summary.md`.
  - Template system:
    - `hooks/lib/template-loader.sh:36-46` loads template files.
    - `hooks/lib/template-loader.sh:56-136` performs single-pass rendering.
    - `hooks/lib/template-loader.sh:188-211` provides safe fallback behavior.
  - Root and loop-state dependencies:
    - `hooks/lib/project-root.sh:41-53` canonicalizes the project root.
    - `hooks/lib/loop-common.sh:332-357` finds the active loop directory.
    - `hooks/lib/loop-common.sh:427-454` and nearby state parsing populate current-round state used by the validator.
  - Related sibling templates:
    - `prompt-template/block/goal-tracker-bash-write.md` is structurally similar for round-0 goal-tracker Bash blocks, called from `hooks/lib/loop-common.sh:903-912`.
    - `prompt-template/block/round-contract-bash-write.md` serves the same “use Write/Edit” pattern for round contract files and is loaded inline at `hooks/loop-bash-validator.sh:528-535`.

- edge_cases_or_failure_modes:
  - Missing or empty template:
    - `load_and_render_safe` falls back to an inline message at `hooks/lib/template-loader.sh:197-207`, so the gate still blocks even if this file is unavailable. The fallback is less detailed than the template because it omits the explicit “cat, echo, sed, awk” examples.
  - Missing `CORRECT_PATH` variable:
    - The template loader preserves unknown placeholders by design at `hooks/lib/template-loader.sh:115-121`; if the caller failed to provide `CORRECT_PATH`, the rendered message would contain the literal `{{CORRECT_PATH}}`. The current caller does provide it at `hooks/lib/loop-common.sh:900`.
  - Pattern coverage limits:
    - `command_modifies_file` is regex-based and covers common write forms at `hooks/lib/loop-common.sh:1489-1502`, but it is not a full shell parser. Complex quoting, variable-expanded filenames, generated paths, or interpreter-driven writes may evade this specific summary gate unless caught by another broader restriction.
    - The tests explicitly acknowledge variable indirection does not match literal file patterns: `assert_not_modifies 'echo x > $FILE'` appears at `tests/test-bash-validator-patterns.sh:170-171`.
  - Non-write reads:
    - `cat round-5-summary.md` should not trigger this template because reading a summary is not a Bash mutation; this expectation is covered at `tests/test-bash-validator-patterns.sh:194`.
  - Wrong-round attempted path:
    - If a command attempts to write `round-5-summary.md` while `CURRENT_ROUND=3`, this template points the user to `round-3-summary.md`, because the output path is state-derived rather than command-derived. That is intentional but can surprise users who were trying to patch historical summaries.
  - Active-loop absence or stale state:
    - Without an active loop, the validator cannot compute `ACTIVE_LOOP_DIR` or `CURRENT_ROUND`, so this gate is not reached. `find_active_loop` also has zombie-loop protections and session filtering, so a mismatched session may not receive this block even if a different loop exists in the same repository.

- validation_or_tests:
  - Direct template existence/reference coverage:
    - `tests/test-template-references.sh:152-157` includes `block/summary-bash-write.md` in the common template list and verifies the file exists.
    - `tests/test-template-references.sh:134-140` also checks whether templates are referenced from hooks.
  - Command-pattern coverage:
    - `tests/test-bash-validator-patterns.sh:186-194` verifies summary write patterns: `echo x > round-5-summary.md` and `cat data >> round-10-summary.md` are modifications, while `cat round-5-summary.md` is not.
  - Template-loader coverage:
    - `tests/test-template-loader.sh:147-164` exercises real-template rendering with substitutions.
    - `tests/test-templates-comprehensive.sh:493-510` exercises integration rendering against real templates and checks substituted output.
  - I did not execute the test suite in this read-only branch export. Evidence above is from direct file inspection only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 Item Evidence heading present for the single assigned row`
- missing_items: `0`
- duplicate_items: `0`
- final_worker_status: `complete`