# agent_07 templify-prompt 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `0c107abc65600bca4e18b04265b48c91da772491`

## Item Evidence

### TEMPLIFY_PROMPT-HZ-007 `file` `README.md`
- cursor: `[_]`
- core_role:
  - `README.md` is behavior-defining documentation for the Humanize RLCR state machine. It describes the intended loop: Claude implements and summarizes, Codex reviews, feedback returns to Claude, and the loop ends on Codex completion or iteration limit (`README.md:29-39`).
  - It defines the product-level contract: iterative development, independent Codex review, goal tracking, early issue detection, and a preserved audit trail (`README.md:15-27`).
  - It is not executable code, but it is a high-level requirements source for `commands/start-rlcr-loop.md`, `scripts/setup-rlcr-loop.sh`, `hooks/loop-codex-stop-hook.sh`, and the prompt templates under `prompt-template/`.

- algorithmic_behavior:
  - The loop algorithm starts from a user-authored plan file, requires that plan to include enough detail and acceptance criteria guidance, then runs `/humanize:start-rlcr-loop <plan.md>` with optional iteration, Codex model, timeout, and push policy parameters (`README.md:41-70`, `README.md:187-200`).
  - The documented transition graph is: `plan.md` to Claude implementation and summary, then Codex review, then either feedback back to Claude or terminal completion/max-iteration exit (`README.md:33-39`).
  - The state machine is interruptible and resumable. Active loop state is defined by the presence of `.humanize-loop.local/*/state.md`; removing that state file cancels the active loop while preserving historical artifacts (`README.md:112-128`).
  - The README establishes the Goal Tracker algorithm: Round 0 creates immutable goal and acceptance-criteria anchors; later rounds mutate only task status, completed/deferred items, and plan evolution logs (`README.md:130-143`).
  - It also defines a circuit-breaker behavior for full alignment checks: Codex can detect repeated issues, lack of meaningful acceptance-criteria progress, or circular discussion and output `STOP` to terminate the loop (`README.md:144-151`).
  - Implementation details match the code path: setup writes `state.md` with `current_round`, `max_iterations`, Codex config, push policy, plan file, and timestamp (`scripts/setup-rlcr-loop.sh:223-234`); the stop hook parses those fields before reviewing (`hooks/loop-codex-stop-hook.sh:285-313`).
  - Non-terminal review feedback advances `current_round`, writes the next round prompt, appends goal-tracker update instructions, and blocks exit so Claude continues (`hooks/loop-codex-stop-hook.sh:760-829`).

- inputs_outputs_state:
  - Primary input: a markdown plan file passed to `/humanize:start-rlcr-loop`; documentation says it should include a clear implementation description, acceptance criteria, optional technical approach, and at least five lines (`README.md:41-55`).
  - Command inputs: `--max`, `--codex-model MODEL:EFFORT`, `--codex-timeout SECONDS`, and `--push-every-round` (`README.md:187-200`). The setup script validates option forms and rejects unknown or duplicate plan-file arguments (`scripts/setup-rlcr-loop.sh:93-157`).
  - Runtime prerequisite input: `codex` must be available (`README.md:202-210`), enforced by setup before creating the loop (`scripts/setup-rlcr-loop.sh:195-201`) and again by the stop hook before review (`hooks/loop-codex-stop-hook.sh:512-532`).
  - Persistent project-local outputs: `.humanize-loop.local/<timestamp>/state.md`, `goal-tracker.md`, round prompts, round summaries, review prompts, and review results (`README.md:241-251`).
  - Cache outputs outside the project: `$HOME/.cache/humanize/<sanitized-project-path>/<timestamp>/round-N-codex-run.{cmd,out,log}` for Codex invocation auditing (`README.md:253-257`; implemented at `hooks/loop-codex-stop-hook.sh:536-590`).
  - State transitions:
    - Setup initializes `current_round: 0` and creates Round 0 prompt/state/tracker (`scripts/setup-rlcr-loop.sh:223-243`, `scripts/setup-rlcr-loop.sh:336-387`).
    - Stop hook blocks if the current round summary is absent (`hooks/loop-codex-stop-hook.sh:315-340`).
    - Stop hook blocks Round 0 exit if goal-tracker placeholders remain (`hooks/loop-codex-stop-hook.sh:343-402`).
    - Stop hook removes state and exits on max iteration, Codex completion, or circuit breaker (`hooks/loop-codex-stop-hook.sh:405-414`, `hooks/loop-codex-stop-hook.sh:718-756`).
    - Otherwise, it increments `current_round`, writes the next prompt, and blocks exit with feedback (`hooks/loop-codex-stop-hook.sh:760-829`).

- gates_or_invariants:
  - Plan gate: plan file must be supplied, exist, and contain at least five lines (`scripts/setup-rlcr-loop.sh:163-193`), matching README guidance (`README.md:51-55`).
  - Tool gate: Codex CLI must exist before setup and review (`README.md:202-210`, `scripts/setup-rlcr-loop.sh:195-201`, `hooks/loop-codex-stop-hook.sh:512-532`).
  - State invariant: the active loop is controlled by newest loop directory with `state.md`, not by arbitrary older directories; this prevents old loop sessions from reviving unexpectedly (`README.md:116-128`, `hooks/lib/loop-common.sh:23-44`).
  - Summary invariant: each exit attempt requires the current `round-N-summary.md`; wrong round or wrong location is blocked by validators (`hooks/loop-codex-stop-hook.sh:315-340`, `hooks/loop-write-validator.sh:100-165`, `hooks/loop-edit-validator.sh:87-117`).
  - Goal Tracker invariant: immutable section is initialized in Round 0 and treated as read-only after that (`README.md:134-143`, `scripts/setup-rlcr-loop.sh:339-349`).
  - Direct state edits are blocked (`hooks/loop-write-validator.sh:81-88`, `hooks/loop-edit-validator.sh:68-75`, `hooks/loop-bash-validator.sh:67-75`).
  - Direct Goal Tracker edits are allowed through Write/Edit only in Round 0; after Round 0 they are blocked and must go through a Goal Tracker Update Request reviewed by Codex (`hooks/loop-write-validator.sh:90-98`, `hooks/loop-edit-validator.sh:77-85`, `hooks/loop-bash-validator.sh:77-92`, `prompt-template/codex/goal-tracker-update-section.md` referenced at `hooks/loop-codex-stop-hook.sh:434-438`).
  - Git/save gates are stronger than README’s high-level description: before Codex review the hook blocks incomplete todos, oversized changed code/docs files, uncommitted changes, and, when enabled, unpushed commits (`hooks/loop-codex-stop-hook.sh:61-177`, `hooks/loop-codex-stop-hook.sh:179-275`).
  - Terminal review words are strict last-line tokens. The hook checks the last non-empty line exactly to avoid false positives such as explanatory text containing completion wording (`hooks/loop-codex-stop-hook.sh:712-716`).

- dependencies_and_callers:
  - Slash command caller: `/humanize:start-rlcr-loop` invokes `${CLAUDE_PLUGIN_ROOT}/scripts/setup-rlcr-loop.sh` with user arguments (`commands/start-rlcr-loop.md:1-14`).
  - Setup dependency: `scripts/setup-rlcr-loop.sh` creates the loop directory, `state.md`, `goal-tracker.md`, and Round 0 prompt (`scripts/setup-rlcr-loop.sh:203-243`, `scripts/setup-rlcr-loop.sh:330-423`).
  - Stop hook dependency: `hooks/loop-codex-stop-hook.sh` implements the review transition algorithm described by the README (`hooks/loop-codex-stop-hook.sh:3-13`, `hooks/loop-codex-stop-hook.sh:52-57`).
  - Shared hook dependencies: `hooks/lib/loop-common.sh` provides active-loop discovery, round parsing, path classifiers, and blocking message helpers (`hooks/lib/loop-common.sh:23-58`, `hooks/lib/loop-common.sh:65-191`).
  - Template dependency: `hooks/lib/template-loader.sh` loads and renders templates from `prompt-template/`, preserving placeholders not supplied and using safe fallbacks when called through `load_and_render_safe` (`hooks/lib/template-loader.sh:18-33`, `hooks/lib/template-loader.sh:35-117`, `hooks/lib/template-loader.sh:152-188`).
  - Monitor dependency: README’s monitoring dashboard maps to `scripts/humanize.sh`, which parses `state.md`, `goal-tracker.md`, git status, and Codex logs for display (`README.md:88-110`; references in `scripts/humanize.sh:98-144`, `scripts/humanize.sh:269-344`, `scripts/humanize.sh:431-494` from search results).
  - Cancel command dependency: README cancellation maps to `/humanize:cancel-rlcr-loop`, which removes `.humanize-loop.local/*/state.md` (`README.md:120-126`, `commands/cancel-rlcr-loop.md:3-21`).

- edge_cases_or_failure_modes:
  - Multiple historical loop directories: only the newest timestamped directory with `state.md` is active; older state files are ignored (`hooks/lib/loop-common.sh:23-44`).
  - Corrupt `current_round`: stop hook warns, removes the state file, and exits instead of continuing from invalid state (`hooks/loop-codex-stop-hook.sh:303-308`).
  - Invalid `max_iterations`: stop hook defaults to 42 when parsing fails (`hooks/loop-codex-stop-hook.sh:310-313`).
  - Missing summary: blocks exit before Codex review and instructs writing the current round summary (`hooks/loop-codex-stop-hook.sh:315-340`).
  - Missing or uninitialized Goal Tracker placeholders in Round 0: blocks exit with the assigned template `prompt-template/block/goal-tracker-not-initialized.md` (`hooks/loop-codex-stop-hook.sh:343-402`).
  - Codex failures: nonzero exit, missing review file, failed stdout copy, or empty review file all produce a blocking failure with debug file paths (`hooks/loop-codex-stop-hook.sh:607-707`).
  - Max iteration reached without completion removes state and exits, preserving artifacts for inspection (`hooks/loop-codex-stop-hook.sh:405-414`; README artifact preservation at `README.md:128`).
  - README states full alignment checks occur at rounds 4, 9, 14, etc. after every four rounds of work (`README.md:142`); hook implementation uses `CURRENT_ROUND % 5 == 4`, so the effective alignment schedule is every fifth round with zero-based numbering (`hooks/loop-codex-stop-hook.sh:440-444`).

- validation_or_tests:
  - Template reference tests scan hook scripts and verify referenced templates exist so blocking messages are not empty (`tests/test-template-references.sh:51-116`).
  - The same test has explicit common-template coverage for goal tracker and state modification blockers (`tests/test-template-references.sh:149-167`) and checks critical validators use safe template rendering (`tests/test-template-references.sh:169-201`).
  - Comprehensive template tests validate directory structure, load every markdown template, and check placeholder syntax rules (`tests/test-templates-comprehensive.sh:61-130`).
  - Comprehensive tests also cover malformed placeholder detection and rendering edge cases (`tests/test-templates-comprehensive.sh:200-290`).
  - Error-scenario tests document missing-template behavior: missing files/directories return empty strings with no crash, but this can produce empty feedback unless safe fallback rendering is used (`tests/test-error-scenarios.sh:21-120`).
  - I did not execute test scripts because this assignment is research-only in a read-only branch export; validation here is based on direct inspection of test definitions.

- skip_candidate: `no`

### TEMPLIFY_PROMPT-HZ-037 `file` `prompt-template/block/goal-tracker-not-initialized.md`
- cursor: `[_]`
- core_role:
  - This file is a blocking prompt template used when a Round 0 exit attempt occurs before the Goal Tracker has been properly initialized.
  - It is algorithmically core because it defines the remediation contract for a specific state-machine gate: Round 0 cannot progress to Codex review while required goal-tracker placeholders remain (`prompt-template/block/goal-tracker-not-initialized.md:1-18`).
  - The template is invoked by `hooks/loop-codex-stop-hook.sh` when placeholder detection finds missing Ultimate Goal, Acceptance Criteria, or Active Tasks (`hooks/loop-codex-stop-hook.sh:343-402`).

- algorithmic_behavior:
  - The hook first confirms it is Round 0 and that `goal-tracker.md` exists (`hooks/loop-codex-stop-hook.sh:346-348`).
  - It reads the tracker and sets three booleans based on exact placeholder text:
    - Ultimate Goal placeholder: `\[To be extracted from plan`
    - Acceptance Criteria placeholder: `\[To be defined by Claude`
    - Active Tasks placeholder: `\[To be populated by Claude`
    (`hooks/loop-codex-stop-hook.sh:349-366`).
  - It builds a rendered `MISSING_ITEMS` list naming whichever sections still contain placeholders (`hooks/loop-codex-stop-hook.sh:368-381`).
  - If any missing item exists, it renders this template through `load_and_render_safe`, emits a JSON hook response with `"decision": "block"`, and exits without running Codex review (`hooks/loop-codex-stop-hook.sh:383-400`).
  - The template instructs Claude to read `{{GOAL_TRACKER_FILE}}`, replace placeholders with actual content, define three to seven testable acceptance criteria, populate active tasks with AC mapping, then write `goal-tracker.md` (`prompt-template/block/goal-tracker-not-initialized.md:5-15`).
  - It encodes a one-way transition: the immutable section can only be set in Round 0; after this round it becomes read-only (`prompt-template/block/goal-tracker-not-initialized.md:16`).

- inputs_outputs_state:
  - Template inputs:
    - `{{GOAL_TRACKER_FILE}}`: absolute or project-local path to the active loop’s `goal-tracker.md`, supplied by the stop hook (`hooks/loop-codex-stop-hook.sh:388-390`).
    - `{{MISSING_ITEMS}}`: newline list of missing goal, acceptance criteria, and/or active tasks sections, assembled by the stop hook (`hooks/loop-codex-stop-hook.sh:368-381`).
  - Template output: markdown block text used as the hook `reason` field in a JSON response to Claude Code (`hooks/loop-codex-stop-hook.sh:392-399`).
  - State consumed: current round from `state.md`, active loop directory, and current `goal-tracker.md` content (`hooks/loop-codex-stop-hook.sh:285-301`, `hooks/loop-codex-stop-hook.sh:346-350`).
  - State preserved: `state.md` is not advanced when this block fires; `current_round` remains 0 and the loop waits for a corrected tracker before exit can be attempted again.
  - State produced by remediation: the expected user/Claude action is an updated `goal-tracker.md` with non-placeholder Ultimate Goal, three to seven testable acceptance criteria, and Active Tasks mapped to acceptance criteria (`prompt-template/block/goal-tracker-not-initialized.md:8-15`).

- gates_or_invariants:
  - Round gate: this template is only checked in Round 0 (`hooks/loop-codex-stop-hook.sh:348`).
  - Placeholder gate: the gate depends on literal placeholder substrings generated by setup (`scripts/setup-rlcr-loop.sh:271-290`, `scripts/setup-rlcr-loop.sh:308-313`) and later matched by the stop hook (`hooks/loop-codex-stop-hook.sh:356-366`).
  - Immutable-section invariant: Round 0 is the only direct-write window for the Ultimate Goal and Acceptance Criteria (`prompt-template/block/goal-tracker-not-initialized.md:16`; setup prompt reinforces this at `scripts/setup-rlcr-loop.sh:339-349`).
  - Tool-use invariant: Bash modification of `goal-tracker.md` is blocked even in Round 0 and the user is instructed to use Write/Edit instead (`hooks/loop-bash-validator.sh:77-92`, `hooks/lib/loop-common.sh:126-135`).
  - Post-Round-0 invariant: Write/Edit/Bash direct modifications of `goal-tracker.md` are blocked after Round 0; changes must be requested in the summary and reviewed by Codex (`hooks/loop-write-validator.sh:90-98`, `hooks/loop-edit-validator.sh:77-85`, `hooks/loop-bash-validator.sh:83-92`, `hooks/lib/loop-common.sh:180-191`).
  - Safe-render invariant: the hook calls `load_and_render_safe`, so if the template is missing or empty the inline fallback is still rendered with variables (`hooks/loop-codex-stop-hook.sh:383-390`, `hooks/lib/template-loader.sh:152-188`).

- dependencies_and_callers:
  - Direct caller: `hooks/loop-codex-stop-hook.sh` references `"block/goal-tracker-not-initialized.md"` in the Round 0 initialization check (`hooks/loop-codex-stop-hook.sh:383-390`).
  - Setup dependency: `scripts/setup-rlcr-loop.sh` creates the initial `goal-tracker.md` placeholders that this template asks Claude to replace (`scripts/setup-rlcr-loop.sh:243-328`).
  - Initial prompt dependency: setup also writes a Round 0 prompt that mirrors this template’s instructions before implementation begins (`scripts/setup-rlcr-loop.sh:336-387`).
  - Loader dependency: `hooks/lib/template-loader.sh` supplies `load_template`, `render_template`, and `load_and_render_safe`; rendering uses single-pass placeholder substitution to prevent injected placeholder values from being rescanned (`hooks/lib/template-loader.sh:18-33`, `hooks/lib/template-loader.sh:35-117`, `hooks/lib/template-loader.sh:152-188`).
  - Validator dependencies: `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, and `hooks/loop-bash-validator.sh` enforce where and how the Goal Tracker can be changed, so this template’s remediation path is constrained by those validators.

- edge_cases_or_failure_modes:
  - If setup heuristically extracts a goal or acceptance criteria from the plan, those sections may not contain placeholders; the block will only report remaining placeholder sections, often Active Tasks (`scripts/setup-rlcr-loop.sh:263-291`, `hooks/loop-codex-stop-hook.sh:356-381`).
  - If a user removes placeholder text but leaves semantically empty or weak content, this gate passes because validation is string-based; deeper quality is left to Codex review and full alignment checks.
  - If `goal-tracker.md` is absent in Round 0, this specific template is not invoked because the condition requires the file to exist (`hooks/loop-codex-stop-hook.sh:348`); downstream review may fail or other file-access behavior may apply.
  - If placeholder text is altered slightly, the grep-based detector may not catch it. The invariant depends on setup’s exact placeholder strings (`scripts/setup-rlcr-loop.sh:271-290`, `scripts/setup-rlcr-loop.sh:312`).
  - If the template file is missing, `load_and_render_safe` uses the shorter fallback message instead of failing the hook (`hooks/loop-codex-stop-hook.sh:383-390`, `hooks/lib/template-loader.sh:152-188`).
  - The template says to “Write the updated goal-tracker.md” (`prompt-template/block/goal-tracker-not-initialized.md:14`), but Bash writes are blocked; successful remediation must use Write/Edit tooling, consistent with validator behavior (`hooks/loop-bash-validator.sh:77-92`).

- validation_or_tests:
  - Template reference validation scans hook scripts for template references and fails if a referenced template file is missing (`tests/test-template-references.sh:51-116`). This covers the stop hook’s reference to `block/goal-tracker-not-initialized.md`.
  - Cross-reference tests ensure common goal-tracker blocking templates exist (`tests/test-template-references.sh:149-167`), while the broader scan catches templates directly referenced in hooks.
  - Comprehensive template tests verify all templates can be loaded and are non-empty or at least not load failures (`tests/test-templates-comprehensive.sh:82-112`).
  - Placeholder syntax tests enforce uppercase `{{VAR_NAME}}` style and detect malformed placeholders such as extra braces, spaces, or lowercase variable names (`tests/test-templates-comprehensive.sh:113-130`, `tests/test-templates-comprehensive.sh:200-256`). This template’s `{{GOAL_TRACKER_FILE}}` and `{{MISSING_ITEMS}}` conform.
  - Error scenario tests document the risk of missing templates producing empty feedback when unsafe loading is used, supporting why this call path uses `load_and_render_safe` (`tests/test-error-scenarios.sh:21-120`).
  - I did not execute test scripts because this assignment is research-only in a read-only branch export; validation here is based on direct inspection of the tests and hook call sites.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: TEMPLIFY_PROMPT-HZ-007, TEMPLIFY_PROMPT-HZ-037
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`