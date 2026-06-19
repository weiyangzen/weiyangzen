# agent_05 templify-prompt 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `0c107abc65600bca4e18b04265b48c91da772491`

## Item Evidence

### TEMPLIFY_PROMPT-HZ-005 `directory` `scripts`
- cursor: `[_]`
- core_role:
  - `scripts/` is the user-facing and runtime support layer for the RLCR loop. It initializes loop state, provides a portable timeout abstraction for Codex review execution, and exposes an interactive monitor for live loop state.
  - Recursive contents inspected: `scripts/setup-rlcr-loop.sh`, `scripts/portable-timeout.sh`, and `scripts/humanize.sh`.
  - This directory coordinates with `commands/start-rlcr-loop.md`, lifecycle hooks under `hooks/`, state files under `.humanize-loop.local/<timestamp>/`, cache logs under `$HOME/.cache/humanize/...`, and prompt/block templates under `prompt-template/`.
- algorithmic_behavior:
  - `scripts/setup-rlcr-loop.sh` is the loop bootstrap algorithm. It parses CLI arguments and defaults at `scripts/setup-rlcr-loop.sh:17`, `scripts/setup-rlcr-loop.sh:27`, and `scripts/setup-rlcr-loop.sh:93`. Supported controls include max iterations, Codex model/effort, Codex timeout, and `--push-every-round`.
  - The setup script validates prerequisites before creating state: plan file must be provided, made absolute if relative, exist, contain at least 5 lines, and `codex` must be available (`scripts/setup-rlcr-loop.sh:163`, `scripts/setup-rlcr-loop.sh:173`, `scripts/setup-rlcr-loop.sh:180`, `scripts/setup-rlcr-loop.sh:185`, `scripts/setup-rlcr-loop.sh:195`).
  - It creates `.humanize-loop.local/<timestamp>/`, then writes `state.md` with `current_round: 0`, max iteration, Codex config, timeout, push policy, plan file, and UTC start time (`scripts/setup-rlcr-loop.sh:207`, `scripts/setup-rlcr-loop.sh:210`, `scripts/setup-rlcr-loop.sh:223`).
  - It creates `goal-tracker.md` with immutable and mutable sections. It heuristically extracts the Ultimate Goal from headings matching goal/objective/purpose and acceptance criteria from headings matching acceptance/criteria/requirements; otherwise it writes placeholders for Round 0 initialization (`scripts/setup-rlcr-loop.sh:240`, `scripts/setup-rlcr-loop.sh:263`, `scripts/setup-rlcr-loop.sh:285`, `scripts/setup-rlcr-loop.sh:293`).
  - It creates `round-0-prompt.md` embedding the plan file, required Goal Tracker initialization steps, task/todo requirements, anti-cheating instruction, commit instruction, and required summary path (`scripts/setup-rlcr-loop.sh:334`, `scripts/setup-rlcr-loop.sh:336`, `scripts/setup-rlcr-loop.sh:339`, `scripts/setup-rlcr-loop.sh:353`, `scripts/setup-rlcr-loop.sh:380`, `scripts/setup-rlcr-loop.sh:382`). Push instructions are conditionally appended when `--push-every-round` is enabled (`scripts/setup-rlcr-loop.sh:389`).
  - `scripts/portable-timeout.sh` abstracts cross-platform timeout behavior. It selects `gtimeout`, GNU `timeout`, `python3`, `python`, or `none` in priority order (`scripts/portable-timeout.sh:10`). `run_with_timeout` then dispatches the requested command through that implementation (`scripts/portable-timeout.sh:33`). Python fallback returns exit code `124` on timeout to match GNU timeout semantics (`scripts/portable-timeout.sh:56`).
  - `scripts/humanize.sh` provides the `humanize monitor rlcr-loop` command. Its monitor finds the newest loop session, finds the latest Codex run log in project-specific cache, parses `state.md`, parses `goal-tracker.md`, parses git status, renders a fixed terminal status bar, and tails the active Codex log while switching to newer logs when they appear (`scripts/humanize.sh:9`, `scripts/humanize.sh:23`, `scripts/humanize.sh:43`, `scripts/humanize.sh:98`, `scripts/humanize.sh:116`, `scripts/humanize.sh:200`, `scripts/humanize.sh:262`, `scripts/humanize.sh:456`, `scripts/humanize.sh:493`).
  - The command dispatcher exposes only `humanize monitor rlcr-loop`; other commands or targets print usage and return failure (`scripts/humanize.sh:520`, `scripts/humanize.sh:525`, `scripts/humanize.sh:526`, `scripts/humanize.sh:533`, `scripts/humanize.sh:545`).
- inputs_outputs_state:
  - Inputs to `setup-rlcr-loop.sh`: one plan markdown path, optional `--max`, optional `--codex-model MODEL:EFFORT`, optional `--codex-timeout`, optional `--push-every-round`, environment `CLAUDE_PROJECT_DIR`, current working directory, and availability of `codex`.
  - Outputs from `setup-rlcr-loop.sh`: `.humanize-loop.local/<timestamp>/state.md`, `.humanize-loop.local/<timestamp>/goal-tracker.md`, `.humanize-loop.local/<timestamp>/round-0-prompt.md`, expected future summary path `.humanize-loop.local/<timestamp>/round-0-summary.md`, plus activation/completion instructions printed to stdout (`scripts/setup-rlcr-loop.sh:223`, `scripts/setup-rlcr-loop.sh:243`, `scripts/setup-rlcr-loop.sh:336`, `scripts/setup-rlcr-loop.sh:401`, `scripts/setup-rlcr-loop.sh:422`).
  - State transition initialized by setup: no active loop to active loop; `current_round` starts at `0`; immutable Goal Tracker sections are intended to be finalized in Round 0; mutable task tracking begins with placeholder rows (`scripts/setup-rlcr-loop.sh:225`, `scripts/setup-rlcr-loop.sh:257`, `scripts/setup-rlcr-loop.sh:297`, `scripts/setup-rlcr-loop.sh:308`).
  - Inputs to `portable-timeout.sh`: timeout seconds plus command/args. Output is the wrapped command’s exit code, or `124` for Python timeout expiry, or unbounded execution with a warning if no timeout backend exists (`scripts/portable-timeout.sh:33`, `scripts/portable-timeout.sh:47`, `scripts/portable-timeout.sh:64`).
  - Inputs to `humanize.sh`: current working directory containing `.humanize-loop.local`, terminal capabilities through `tput`, project-specific Codex logs under `$HOME/.cache/humanize/<sanitized-project-path>/<timestamp>/`, and git repository status. Output is terminal UI, not persistent state (`scripts/humanize.sh:17`, `scripts/humanize.sh:49`, `scripts/humanize.sh:271`, `scripts/humanize.sh:326`, `scripts/humanize.sh:430`).
- gates_or_invariants:
  - Setup enforces exactly one plan file; multiple positional plan files are rejected (`scripts/setup-rlcr-loop.sh:147`, `scripts/setup-rlcr-loop.sh:150`).
  - `--max` and `--codex-timeout` must be numeric positive-integer strings by regex, though `0` technically matches the current regex (`scripts/setup-rlcr-loop.sh:103`, `scripts/setup-rlcr-loop.sh:130`).
  - The plan must have at least 5 lines, preventing trivial prompt strings from becoming loop state (`scripts/setup-rlcr-loop.sh:185`).
  - `codex` must be on `PATH` before loop state is created (`scripts/setup-rlcr-loop.sh:195`).
  - Stop-hook coordination reads and advances the state created by setup. It parses `current_round`, `max_iterations`, model, effort, timeout, and push policy from `state.md` (`hooks/loop-codex-stop-hook.sh:288`). It blocks missing summaries (`hooks/loop-codex-stop-hook.sh:319`), blocks uninitialized Round 0 Goal Tracker placeholders (`hooks/loop-codex-stop-hook.sh:348`), allows termination on max iterations (`hooks/loop-codex-stop-hook.sh:410`), treats last non-empty Codex result line `COMPLETE` or `STOP` as terminal states (`hooks/loop-codex-stop-hook.sh:712`, `hooks/loop-codex-stop-hook.sh:719`, `hooks/loop-codex-stop-hook.sh:730`), and otherwise increments `current_round` in `state.md` (`hooks/loop-codex-stop-hook.sh:763`).
  - The timeout helper is sourced by the Codex stop hook if present, then used to wrap `codex exec` with the state/env/default timeout (`hooks/loop-codex-stop-hook.sh:550`, `hooks/loop-codex-stop-hook.sh:596`).
  - The monitor assumes timestamp-formatted session directory names and ignores non-matching directories (`scripts/humanize.sh:33`, `scripts/humanize.sh:64`).
- dependencies_and_callers:
  - `commands/start-rlcr-loop.md` is the slash-command entry point. Its allowed tool is the setup script and it invokes `"${CLAUDE_PLUGIN_ROOT}/scripts/setup-rlcr-loop.sh" $ARGUMENTS` (`commands/start-rlcr-loop.md:4`, `commands/start-rlcr-loop.md:12`).
  - `hooks/hooks.json` registers the Stop hook that later consumes setup-created state and invokes Codex review with timeout (`hooks/hooks.json:42`, `hooks/hooks.json:47`).
  - `hooks/loop-codex-stop-hook.sh` depends on `scripts/portable-timeout.sh` and falls back to an inline timeout wrapper if the script is missing (`hooks/loop-codex-stop-hook.sh:550`).
  - `README.md` instructs users to source `scripts/humanize.sh` and run `humanize monitor rlcr-loop` (`README.md:90`, `README.md:103`). It also documents the `scripts/` directory as setup scripts plus shell utilities (`README.md:233`).
  - `scripts/humanize.sh` relies on the cache path convention produced by the stop hook: `$HOME/.cache/humanize/<sanitized-project-path>/<timestamp>/round-*-codex-run.log` (`scripts/humanize.sh:43`, `hooks/loop-codex-stop-hook.sh:536`, `hooks/loop-codex-stop-hook.sh:543`, `hooks/loop-codex-stop-hook.sh:548`).
- edge_cases_or_failure_modes:
  - `setup-rlcr-loop.sh` uses heading extraction heuristics. If the plan headings are absent, nested, or unconventional, placeholders remain and Round 0 must fill them before the stop hook will allow progress (`scripts/setup-rlcr-loop.sh:263`, `scripts/setup-rlcr-loop.sh:285`, `hooks/loop-codex-stop-hook.sh:356`, `hooks/loop-codex-stop-hook.sh:383`).
  - `--max 0` and `--codex-timeout 0` pass the numeric regex even though help text says positive; this can create immediate max-iteration behavior or timeout behavior dependent on the backend (`scripts/setup-rlcr-loop.sh:103`, `scripts/setup-rlcr-loop.sh:130`, `hooks/loop-codex-stop-hook.sh:410`).
  - The setup script writes files directly with shell redirection. That is expected because it is the bootstrapper, but it means read-only exports cannot execute it successfully.
  - The portable timeout fallback to `none` runs reviews without enforcement and only prints a warning (`scripts/portable-timeout.sh:64`). The inline stop-hook fallback is weaker than the script because it lacks the Python fallback and checks `timeout` before `gtimeout` (`hooks/loop-codex-stop-hook.sh:555`).
  - The monitor requires a terminal with usable `tput`; in non-interactive or narrow terminals, cursor positioning/truncation can behave poorly (`scripts/humanize.sh:271`, `scripts/humanize.sh:326`, `scripts/humanize.sh:388`).
  - `humanize.sh` parses markdown tables and YAML-ish frontmatter with grep/sed. Goal tracker formats outside the expected headings/tables can produce inaccurate counts without failing the monitor (`scripts/humanize.sh:106`, `scripts/humanize.sh:138`, `scripts/humanize.sh:150`, `scripts/humanize.sh:174`).
  - If `.humanize-loop.local` exists but no Codex log exists yet, the monitor waits until a log appears (`scripts/humanize.sh:434`).
- validation_or_tests:
  - Static syntax check run for all scripts: `bash -n scripts/humanize.sh scripts/setup-rlcr-loop.sh scripts/portable-timeout.sh`, result `scripts_syntax_ok`.
  - Repository tests mostly cover hook/template behavior rather than direct execution of these scripts. Search did not show a dedicated unit test for `setup-rlcr-loop.sh`, `portable-timeout.sh`, or the monitor command.
  - Existing hook behavior that consumes script outputs is covered indirectly through hook/test files, including template reference validation and template-loader error-scenario tests (`tests/test-template-references.sh:149`, `tests/test-error-scenarios.sh:21`).
- skip_candidate: `no`

### TEMPLIFY_PROMPT-HZ-035 `file` `prompt-template/block/goal-tracker-bash-write.md`
- cursor: `[_]`
- core_role:
  - This file is a block-message template for the Bash PreToolUse validation path. It tells the agent that Bash-based writes to `goal-tracker.md` are forbidden and that the Write/Edit tools must be used instead.
  - Its role is algorithmic despite being markdown: it defines the user-facing failure contract for a validation gate, including the corrective path placeholder.
- algorithmic_behavior:
  - Template content is a short markdown diagnostic: title, prohibition, corrective action using `{{CORRECT_PATH}}`, and rationale that shell commands bypass validation hooks (`prompt-template/block/goal-tracker-bash-write.md:1`, `prompt-template/block/goal-tracker-bash-write.md:3`, `prompt-template/block/goal-tracker-bash-write.md:5`, `prompt-template/block/goal-tracker-bash-write.md:7`).
  - It is rendered by `goal_tracker_bash_blocked_message`, which passes `CORRECT_PATH` into `load_and_render_safe` (`hooks/lib/loop-common.sh:126`, `hooks/lib/loop-common.sh:134`).
  - The gate fires from `hooks/loop-bash-validator.sh` when a Bash tool call appears to modify `goal-tracker.md` and the active loop is in Round 0 (`hooks/loop-bash-validator.sh:83`, `hooks/loop-bash-validator.sh:84`, `hooks/loop-bash-validator.sh:85`). The hook writes this rendered template to stderr and exits `2`, which blocks the tool call (`hooks/loop-bash-validator.sh:86`, `hooks/loop-bash-validator.sh:91`).
  - After Round 0, the same Bash attempt uses a different contract: write a Goal Tracker update request into the current summary, not direct modification (`hooks/loop-bash-validator.sh:87`, `hooks/loop-bash-validator.sh:88`, `hooks/lib/loop-common.sh:180`).
- inputs_outputs_state:
  - Input variable: `CORRECT_PATH`, normally `$ACTIVE_LOOP_DIR/goal-tracker.md` from the newest active loop (`hooks/loop-bash-validator.sh:38`, `hooks/loop-bash-validator.sh:45`, `hooks/loop-bash-validator.sh:85`).
  - Input trigger: JSON hook input where `.tool_name == "Bash"` and `.tool_input.command` contains a modeled file-modification operation targeting `goal-tracker.md` (`hooks/loop-bash-validator.sh:22`, `hooks/loop-bash-validator.sh:25`, `hooks/loop-bash-validator.sh:29`).
  - Output: rendered markdown feedback on stderr and hook exit code `2`; no repository state is mutated by this template path (`hooks/loop-bash-validator.sh:86`, `hooks/loop-bash-validator.sh:91`).
  - State transition: the attempted Bash command is prevented before execution. The loop state remains unchanged; the expected next transition is for the agent to use Write/Edit in Round 0 or, after Round 0, a summary-based update request.
- gates_or_invariants:
  - Only applies to the Bash tool; non-Bash hook inputs exit successfully (`hooks/loop-bash-validator.sh:25`).
  - Only applies when an active loop directory exists; outside an active loop, Bash commands are allowed (`hooks/loop-bash-validator.sh:36`, `hooks/loop-bash-validator.sh:40`).
  - State-file write blocking runs before goal-tracker write blocking, so a command that matches `state.md` is stopped by the state-file message first (`hooks/loop-bash-validator.sh:67`, `hooks/loop-bash-validator.sh:72`).
  - The command classifier looks for specific shell mutation patterns: redirection, `tee`, `sed -i`, `awk -i inplace`, `perl -i`, `mv`/`cp`, and `dd of=` (`hooks/lib/loop-common.sh:155`, `hooks/lib/loop-common.sh:162`).
  - Template rendering is single-pass, so values containing `{{...}}` are not recursively expanded (`hooks/lib/template-loader.sh:35`, `hooks/lib/template-loader.sh:39`, `hooks/lib/template-loader.sh:56`).
  - `load_and_render_safe` falls back to an inline message if the template is missing or renders empty (`hooks/lib/template-loader.sh:155`, `hooks/lib/template-loader.sh:164`, `hooks/lib/template-loader.sh:177`).
- dependencies_and_callers:
  - Direct caller: `hooks/lib/loop-common.sh` through `goal_tracker_bash_blocked_message` (`hooks/lib/loop-common.sh:126`).
  - Runtime caller: `hooks/loop-bash-validator.sh` when command modification detection matches `goal-tracker.md` in Round 0 (`hooks/loop-bash-validator.sh:83`).
  - Hook registration: Bash PreToolUse matcher invokes `hooks/loop-bash-validator.sh` (`hooks/hooks.json:32`, `hooks/hooks.json:37`).
  - Rendering dependency: `hooks/lib/template-loader.sh`, especially `load_and_render_safe` and `render_template` (`hooks/lib/template-loader.sh:43`, `hooks/lib/template-loader.sh:155`).
  - Related sibling contract: `prompt-template/block/summary-bash-write.md` uses the same block style for summary files; `prompt-template/block/goal-tracker-modification.md` is the post-Round-0 direct-modification block.
- edge_cases_or_failure_modes:
  - Detection is pattern-based on the raw lowercased Bash command. Complex indirect writes, shell variables that resolve to `goal-tracker.md`, commands hidden inside scripts, or unusual quoting/path whitespace may evade the classifier (`hooks/lib/loop-common.sh:162`).
  - The path-matching fragments use `[^[:space:]]*`, so paths with spaces before `goal-tracker.md` are a likely weak spot (`hooks/lib/loop-common.sh:163`).
  - The message says “Use Write or Edit Tool,” but the Write/Edit validators only allow direct Goal Tracker modification in Round 0. After Round 0 the correct path is a summary update request, and the Bash validator switches templates accordingly (`hooks/loop-write-validator.sh:94`, `hooks/loop-edit-validator.sh:81`, `hooks/loop-bash-validator.sh:87`).
  - If the template is missing, users still receive the fallback from `loop-common.sh`, but the more detailed rationale from this file is lost (`hooks/lib/loop-common.sh:130`, `hooks/lib/template-loader.sh:164`).
- validation_or_tests:
  - Static inspection confirms the template exists and contains the expected `{{CORRECT_PATH}}` placeholder (`prompt-template/block/goal-tracker-bash-write.md:5`).
  - `tests/test-template-references.sh` includes `block/goal-tracker-bash-write.md` in the common template existence list (`tests/test-template-references.sh:152`, `tests/test-template-references.sh:157`).
  - Template-loader tests exercise missing-template behavior and single/special-character rendering generally, which supports this template’s fallback/render path (`tests/test-error-scenarios.sh:21`, `tests/test-error-scenarios.sh:74`, `hooks/lib/template-loader.sh:155`).
  - No direct hook execution test for this exact template output was found in the inspected references.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `2/2 section headers present; item identifiers are not repeated in this checklist`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`