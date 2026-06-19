# agent_26 add-commit-plan-file-cli 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `20b3ebae90ba6b39c335a1dbdec89affc90c386e`

## Item Evidence

### ADD_COMMIT_PLAN_FILE_CLI-HZ-026 `file` `tests/test-plan-file-hooks.sh`
- cursor: `[_]`
- core_role:
  - This file is an executable specification for RLCR plan-file integrity and loop-hook enforcement. It does not implement the production algorithm, but it defines the required behavior for the core hook algorithm around immutable plan files, loop state schema, branch consistency, backup protection, YAML-ish state parsing, and stop-hook plan integrity checks.
  - The opening comments identify the covered hooks: `hooks/loop-plan-file-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, and `hooks/loop-bash-validator.sh` at `tests/test-plan-file-hooks.sh:3` to `tests/test-plan-file-hooks.sh:9`. Later tests also exercise `hooks/loop-codex-stop-hook.sh`.
  - The test harness creates a temporary git repository and a synthetic active loop under `.humanize-loop.local/2024-01-01_12-00-00`, making it a contract for how the hooks discover and validate active RLCR loop state.

- algorithmic_behavior:
  - The shared setup function initializes a git repo, creates `plans/test-plan.md`, gitignores `plans/`, copies the plan into the loop directory as `plan.md`, and writes loop state frontmatter with `current_round`, `max_iterations`, `plan_file`, `plan_tracked`, and `start_branch` at `tests/test-plan-file-hooks.sh:37` to `tests/test-plan-file-hooks.sh:85`.
  - UserPromptSubmit validation behavior is specified first. A valid active loop must produce exit code `0` and no output from `loop-plan-file-validator.sh` at `tests/test-plan-file-hooks.sh:91` to `tests/test-plan-file-hooks.sh:104`.
  - The validator must parse YAML-quoted `plan_file` values such as `"plans/test-plan.md"` and still locate the original plan file at `tests/test-plan-file-hooks.sh:106` to `tests/test-plan-file-hooks.sh:119`.
  - The state schema gate must block old/incomplete state files that lack `plan_tracked` or `start_branch`, returning a block payload while still exiting `0`, at `tests/test-plan-file-hooks.sh:121` to `tests/test-plan-file-hooks.sh:159`.
  - Branch consistency is required: changing from the branch recorded in `start_branch` to `feature-branch` must block with a branch-related message at `tests/test-plan-file-hooks.sh:164` to `tests/test-plan-file-hooks.sh:185`.
  - Write/Edit protection behavior is specified for the loop backup plan file. `Write` to `$LOOP_DIR/plan.md` must exit `2` with a plan-related error at `tests/test-plan-file-hooks.sh:194` to `tests/test-plan-file-hooks.sh:205`; `Edit` to the same backup must do the same at `tests/test-plan-file-hooks.sh:211` to `tests/test-plan-file-hooks.sh:221`.
  - Bash protection is specified as an anti-bypass layer. Shell redirection and `rm` against `$LOOP_DIR/plan.md` must exit `2` at `tests/test-plan-file-hooks.sh:228` to `tests/test-plan-file-hooks.sh:251`.
  - The bash validator must also catch a direct `.humanize-loop.local/plan.md` path with no timestamp directory, which is explicitly described as a regex-bypass fix at `tests/test-plan-file-hooks.sh:254` to `tests/test-plan-file-hooks.sh:266`.
  - Command-injection and expansion bypass attempts are part of the required algorithmic surface. The validator must block command substitution, glob expansion, brace expansion, piped `tee`, and backtick substitution patterns targeting `.humanize-loop.local/.../plan.md` at `tests/test-plan-file-hooks.sh:272` to `tests/test-plan-file-hooks.sh:335`.
  - Quote parsing is treated as algorithmic behavior, not formatting. The prompt validator must strip quotes from `start_branch`, detect quoted branch mismatches, and accept quoted `plan_file` and paths with hyphens at `tests/test-plan-file-hooks.sh:341` to `tests/test-plan-file-hooks.sh:459`.
  - Stop-hook plan integrity is a second-stage invariant. The stop hook must block when the project plan content differs from the loop backup at `tests/test-plan-file-hooks.sh:469` to `tests/test-plan-file-hooks.sh:506`, when the project plan is deleted at `tests/test-plan-file-hooks.sh:509` to `tests/test-plan-file-hooks.sh:540`, and when the backup itself is missing at `tests/test-plan-file-hooks.sh:543` to `tests/test-plan-file-hooks.sh:559`.
  - For tracked plans, the stop hook must catch both uncommitted changes and committed changes. The race-condition case modifies a tracked plan after loop start and expects a block at `tests/test-plan-file-hooks.sh:562` to `tests/test-plan-file-hooks.sh:630`. The committed-change case verifies that a clean git status is insufficient; content must still match the backup at `tests/test-plan-file-hooks.sh:655` to `tests/test-plan-file-hooks.sh:730`.

- inputs_outputs_state:
  - Inputs:
    - Temporary repository state from `mktemp -d`, git initialization, commits, `.gitignore`, and branch names at `tests/test-plan-file-hooks.sh:30` to `tests/test-plan-file-hooks.sh:50`.
    - `CLAUDE_PROJECT_DIR`, exported to point hooks at the synthetic project root at `tests/test-plan-file-hooks.sh:91` to `tests/test-plan-file-hooks.sh:98` and in tracked-plan subtests at `tests/test-plan-file-hooks.sh:619` to `tests/test-plan-file-hooks.sh:621`.
    - Hook JSON payloads for `Write`, `Edit`, and `Bash`, each sent over stdin, for example `{"tool_name": "Write", "tool_input": {"file_path": ...}}` at `tests/test-plan-file-hooks.sh:196` to `tests/test-plan-file-hooks.sh:198`.
    - Loop state frontmatter in `$LOOP_DIR/state.md`, especially `plan_file`, `plan_tracked`, and `start_branch`.
    - Project plan file content and loop backup content, compared indirectly through the stop hook.
  - Outputs:
    - Test harness output via `pass`, `fail`, and `skip` helpers at `tests/test-plan-file-hooks.sh:26` to `tests/test-plan-file-hooks.sh:28`.
    - Final test counters and process status: the script exits with `$TESTS_FAILED` at `tests/test-plan-file-hooks.sh:733` to `tests/test-plan-file-hooks.sh:742`.
    - Expected hook outputs are either empty allow responses, stderr block messages with exit `2` for PreToolUse validators, or JSON block objects containing `"decision"` for UserPromptSubmit/Stop hook flows.
  - State transitions:
    - The synthetic repo transitions from initial commit to gitignored-plan loop setup, then to modified state files, branch switches, plan deletion/modification, and tracked-plan subrepositories.
    - The logical RLCR state machine being specified is: active loop discovered from `.humanize-loop.local/<timestamp>/state.md`; state schema validated; branch checked; plan tracking mode checked; backup plan protected during tool use; final stop checks compare current project plan to backup before allowing loop exit.
    - The tests repeatedly call `setup_test_loop` to restore the baseline active-loop state before specific mutation scenarios.

- gates_or_invariants:
  - Required state schema invariant: `state.md` must include `plan_tracked` and `start_branch`; missing fields indicate an outdated loop schema and must block, as tested at `tests/test-plan-file-hooks.sh:121` to `tests/test-plan-file-hooks.sh:159` and `tests/test-plan-file-hooks.sh:631` to `tests/test-plan-file-hooks.sh:653`.
  - Branch invariant: the current git branch must match `start_branch`; branch switching during an active loop is forbidden.
  - Backup invariant: `.humanize-loop.local/.../plan.md` is a read-only backup and must be protected from `Write`, `Edit`, shell redirection, removal, `tee`, and other command modification patterns.
  - Plan immutability invariant: the original project plan must remain present and content-identical to the loop backup for the duration of the RLCR loop. This applies to both tracked and gitignored plans.
  - Tracking-mode invariant: if `plan_tracked: true`, the plan must remain tracked and clean; if `plan_tracked: false`, the plan must remain untracked/gitignored. The tests emphasize stop-time content comparison for both modes.
  - YAML compatibility invariant: quoted scalar values for `plan_file` and `start_branch` must be accepted by validators. Paths with hyphens must not be mangled by parsing.
  - Exit-code invariant:
    - Prompt and stop hooks block by printing JSON and exiting `0`.
    - PreToolUse validators block by printing a reason and exiting `2`.
    - Successful allow cases produce exit `0`, usually with no output.

- dependencies_and_callers:
  - Direct production dependencies exercised:
    - `hooks/loop-plan-file-validator.sh`: parses active loop state, validates schema, branch, and plan tracking mode.
    - `hooks/loop-write-validator.sh`: blocks `Write` access to protected loop files and wrong round paths.
    - `hooks/loop-edit-validator.sh`: blocks `Edit` access to protected loop files and wrong round paths.
    - `hooks/loop-bash-validator.sh`: detects shell commands that modify protected files.
    - `hooks/loop-codex-stop-hook.sh`: validates stop-time plan integrity before expensive review logic.
  - Shared helper dependencies:
    - `hooks/lib/loop-common.sh` provides `find_active_loop`, `get_current_round`, path classifiers, and `command_modifies_file`.
    - `hooks/lib/template-loader.sh` provides `load_and_render_safe` for block messages used by the validators.
  - External command dependencies:
    - `git` for repository setup, branch checks, tracking checks, and status checks.
    - `jq` for parsing hook JSON payloads in validators and constructing JSON block responses in the stop hook.
    - `diff` via stop-hook behavior for comparing project plan and backup.
    - Standard shell tools: `mktemp`, `grep`, `sed`, `cp`, `rm`, `mkdir`, `cat`.
  - Caller model:
    - The tests simulate Claude/Codex hook invocations by piping JSON or `{}` into hook scripts. This models how the hooks are called from `hooks/hooks.json`.

- edge_cases_or_failure_modes:
  - Old state schema: missing `plan_tracked` or `start_branch` must block rather than silently allow.
  - YAML-quoted fields: `"plans/test-plan.md"` and quoted branch names must be stripped safely.
  - Branch mismatch with quoted value: `"different-branch"` must still compare against the actual branch after quote stripping.
  - Plan path with hyphens: `my-plans/test-plan.md` must parse and validate normally.
  - Direct backup path bypass: `.humanize-loop.local/plan.md` must be blocked even without a timestamp segment.
  - Shell bypass variants:
    - `$(date +%Y)` command substitution in a path.
    - `*` glob path segment.
    - `{a,b,c}` brace expansion.
    - `cat ... | tee .../plan.md`.
    - Backtick command substitution.
  - Tracked-file race condition: uncommitted tracked plan modifications after loop start must be detected.
  - Clean-git-status bypass: committed changes to the tracked plan must still block because content differs from the backup.
  - Missing backup: if `.humanize-loop.local/.../plan.md` is gone, stop hook must block even if the project plan exists.
  - Deleted original plan: if the project plan file is gone, stop hook must block and point to the backup.

- validation_or_tests:
  - This file is itself the validation entry point for plan-file hook behavior and exits nonzero when any assertion fails.
  - It covers at least fourteen named scenarios, plus subtests 8.1 through 8.9, spanning prompt validation, tool-use validators, bash bypass prevention, YAML quote parsing, and stop-hook integrity checks.
  - Related implementation details align with the tests:
    - `loop-plan-file-validator.sh` parses `plan_tracked`, `plan_file`, and `start_branch` from frontmatter and strips quotes for the latter two.
    - `loop-bash-validator.sh` calls `command_modifies_file` with the plan-backup regex `\.humanize-loop\.local(/[^/]+)?/plan\.md`, which explains the direct-path and one-segment timestamp tests.
    - `loop-codex-stop-hook.sh` first verifies backup existence, then original plan existence, then tracked git status, and finally content equality with `diff -q`.
  - No test execution was run for this research pass because the assignment requested research notes only and the branch export is read-only; evidence is from direct inspection.

- skip_candidate: `no`

### ADD_COMMIT_PLAN_FILE_CLI-HZ-056 `file` `prompt-template/block/wrong-round-number.md`
- cursor: `[_]`
- core_role:
  - This is a block-message template used by RLCR validators when an agent attempts to write or edit a `round-N-summary.md` file for a round number other than the current loop round.
  - It is a small but core-facing review/guard contract: it turns validator state into user-facing corrective guidance and prevents agents from self-advancing round numbers.
  - The full template is seven lines and contains the title, attempted action/path, current round, correct path, and instruction not to increment the round number.

- algorithmic_behavior:
  - The template renders a deterministic block reason with placeholders:
    - `{{ACTION}}`
    - `{{CLAUDE_ROUND}}`
    - `{{FILE_TYPE}}`
    - `{{CURRENT_ROUND}}`
    - `{{CORRECT_PATH}}`
  - The central transition message says the attempted path is `round-{{CLAUDE_ROUND}}-{{FILE_TYPE}}.md`, but the loop’s current round is `{{CURRENT_ROUND}}` at `prompt-template/block/wrong-round-number.md:3`.
  - It then presents the exact valid destination path at `prompt-template/block/wrong-round-number.md:5`.
  - The final invariant is explicit: “Do NOT increment the round number yourself” at `prompt-template/block/wrong-round-number.md:7`.
  - In production, this template is rendered through `load_and_render_safe` when `loop-write-validator.sh` detects a summary file round mismatch. The call passes `ACTION=write to`, `FILE_TYPE=summary`, the extracted attempted round, the current round from state, and the active loop’s correct summary path.
  - The same template is rendered when `loop-edit-validator.sh` detects a summary edit targeting the wrong round, with `ACTION=edit`.

- inputs_outputs_state:
  - Inputs:
    - Attempted action, e.g. `write to` or `edit`.
    - Attempted round extracted from the filename by `extract_round_number`.
    - File type, currently used for `summary`.
    - Current loop round read from `.humanize-loop.local/<timestamp>/state.md`.
    - Correct path, usually `.humanize-loop.local/<timestamp>/round-<current>-summary.md`.
  - Output:
    - Markdown block text beginning with `# Wrong Round Number`.
    - A clear attempted-vs-current round explanation.
    - The correct path for the active round.
    - A rule forbidding manual round-number advancement.
  - State transitions:
    - The template itself has no state mutation. Its algorithmic role is to halt an invalid Write/Edit transition before a wrong-round summary file can be created or modified.
    - It participates in the broader state transition guard where only the loop system, not the agent, advances `current_round`.

- gates_or_invariants:
  - Round number gate: a summary file operation is valid only when the filename round matches `current_round`.
  - Correct-location invariant: the user/agent must use the active loop directory’s summary path, not invent another round file.
  - Round advancement invariant: the agent must not increment round numbers manually; advancement belongs to loop control logic.
  - Template integrity invariant: all placeholders should be supplied by callers. If any are omitted, the rendered text will retain unresolved `{{...}}` placeholders because the template loader preserves unknown placeholders.

- dependencies_and_callers:
  - `hooks/loop-write-validator.sh` uses this template in the wrong-round summary write branch. The relevant logic extracts the target round, compares it to `CURRENT_ROUND`, computes `CORRECT_PATH`, and renders `block/wrong-round-number.md`.
  - `hooks/loop-edit-validator.sh` uses this template in the wrong-round summary edit branch with the same comparison pattern.
  - `hooks/lib/template-loader.sh` supplies `load_and_render_safe` and `render_template`. Rendering is single-pass, so injected placeholder syntax inside a variable value is not re-expanded.
  - `hooks/lib/loop-common.sh` supplies `extract_round_number`, `get_current_round`, and related round-file classification helpers.
  - Tests that render or validate this exact template include `tests/test-template-loader.sh` and `tests/test-templates-comprehensive.sh`, which assert that values such as `round-3-summary.md`, `current round is **5**`, and the correct path appear after rendering.

- edge_cases_or_failure_modes:
  - Missing template file: callers use `load_and_render_safe`, so production validators fall back to inline block text if this template is absent or empty.
  - Missing variables: unknown placeholders remain visible, which makes caller/template mismatch apparent but could produce less polished block text.
  - Incorrect `CORRECT_PATH`: the template trusts the caller. If the active-loop path calculation is wrong, the block message will faithfully display the wrong destination.
  - Non-summary future use: `FILE_TYPE` is parameterized, so the template can render other round file types, but current observed callers use it for `summary`.
  - Attempted manual round advancement: the final line explicitly covers the case where an agent thinks it should create the next round’s summary file before loop control has advanced state.

- validation_or_tests:
  - `tests/test-template-loader.sh` renders `block/wrong-round-number.md` with `ACTION=edit`, `CLAUDE_ROUND=3`, `FILE_TYPE=summary`, `CURRENT_ROUND=5`, and `CORRECT_PATH=/tmp/round-5-summary.md`, then checks that the title, attempted file, and current-round text appear.
  - `tests/test-templates-comprehensive.sh` performs a similar real-template integration check and additionally verifies the rendered correct path.
  - The Write/Edit validators’ own wrong-round branches depend on this template for their blocking output, although the assigned `tests/test-plan-file-hooks.sh` focuses on plan-file protection rather than directly asserting wrong-round summary behavior.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `2/2 item sections present`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`