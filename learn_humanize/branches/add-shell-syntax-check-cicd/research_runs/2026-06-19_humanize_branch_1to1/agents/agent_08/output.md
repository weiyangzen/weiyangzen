# agent_08 add-shell-syntax-check-cicd 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `6e0eebdb803522cd4be735589be4d1d76e8e536e`

## Item Evidence

### ADD_SHELL_SYNTAX_CHECK_CICD-HZ-008 `file` `commands/start-rlcr-loop.md`
- cursor: `[_]`
- core_role:
  - Slash-command workflow definition and user-facing entrypoint for starting the RLCR loop. The file itself is intentionally thin: frontmatter declares the command description, argument shape, and the only allowed tool, then the command executes `${CLAUDE_PLUGIN_ROOT}/scripts/setup-rlcr-loop.sh` with `$ARGUMENTS` (`commands/start-rlcr-loop.md:1-14`).
  - It is part of the command/control surface for the plan/RLCR algorithm rather than the state-machine implementation. The actual initialization algorithm lives in `scripts/setup-rlcr-loop.sh`, and later iterations are enforced by hooks registered in `hooks/hooks.json`.
  - It defines the high-level loop contract: Claude works from a plan, writes a round summary, Codex reviews on attempted exit, feedback causes another round, and a final `COMPLETE` response terminates the loop (`commands/start-rlcr-loop.md:16-23`).

- algorithmic_behavior:
  - Dispatch behavior: the command delegates all setup to:
    - `"${CLAUDE_PLUGIN_ROOT}/scripts/setup-rlcr-loop.sh" $ARGUMENTS` (`commands/start-rlcr-loop.md:12-14`).
  - User-visible algorithm:
    - Implementation starts from the provided plan path (`commands/start-rlcr-loop.md:18`).
    - Work for each round must be summarized to the expected summary file (`commands/start-rlcr-loop.md:19`, `commands/start-rlcr-loop.md:45`).
    - On exit, Codex reviews that summary (`commands/start-rlcr-loop.md:20`).
    - If Codex reports issues, the user continues with feedback; if Codex outputs `COMPLETE`, the loop ends (`commands/start-rlcr-loop.md:21-22`).
  - Goal drift prevention:
    - The command advertises a Goal Tracker with immutable Ultimate Goal and Acceptance Criteria plus mutable Active Tasks, Completed Items, Deferred Items, and Plan Evolution Log (`commands/start-rlcr-loop.md:24-31`).
    - The setup script implements that by creating `goal-tracker.md`, heuristically extracting goal and acceptance criteria from the plan, and seeding mutable tracking tables (`scripts/setup-rlcr-loop.sh:240-328`).
  - Round 0 bootstrap:
    - Setup script parses options and validates inputs (`scripts/setup-rlcr-loop.sh:93-157`, `scripts/setup-rlcr-loop.sh:163-201`).
    - It creates `.humanize-loop.local/<timestamp>/`, writes `state.md`, writes `goal-tracker.md`, and writes `round-0-prompt.md` (`scripts/setup-rlcr-loop.sh:207-214`, `scripts/setup-rlcr-loop.sh:223-234`, `scripts/setup-rlcr-loop.sh:336-387`).
    - It emits activation details and the initial prompt to the current session (`scripts/setup-rlcr-loop.sh:401-452`).
  - Later-round state machine:
    - Hooks registered in `hooks/hooks.json` attach validators to Write/Edit/Read/Bash and a Stop hook to `loop-codex-stop-hook.sh` (`hooks/hooks.json:4-48`).
    - The Stop hook finds the newest active loop via `state.md`; no active loop allows normal exit (`hooks/loop-codex-stop-hook.sh:50-55`).
    - It blocks early if todos are incomplete, files are too large, git is dirty, required summaries are missing, or Round 0 goal tracker placeholders remain (`hooks/loop-codex-stop-hook.sh:67-99`, `hooks/loop-codex-stop-hook.sh:110-197`, `hooks/loop-codex-stop-hook.sh:199-316`, `hooks/loop-codex-stop-hook.sh:360-465`).
    - It parses `state.md`, builds a Codex review prompt, invokes Codex, and then interprets the last non-empty review line strictly as `COMPLETE`, `STOP`, or “continue” (`hooks/loop-codex-stop-hook.sh:326-354`, `hooks/loop-codex-stop-hook.sh:488-520`, `hooks/loop-codex-stop-hook.sh:724-817`).
    - On `COMPLETE` or `STOP`, it removes `state.md` and allows termination; otherwise it increments `current_round`, writes the next prompt, and blocks exit with feedback (`hooks/loop-codex-stop-hook.sh:819-867`, `hooks/loop-codex-stop-hook.sh:869-940`).

- inputs_outputs_state:
  - Primary command input:
    - `<path/to/plan.md>` plus optional `--max N`, `--codex-model MODEL:EFFORT`, `--codex-timeout SECONDS`, and `--push-every-round` as documented in command frontmatter (`commands/start-rlcr-loop.md:3`) and implemented by the setup parser (`scripts/setup-rlcr-loop.sh:93-157`).
  - Input validation:
    - Plan path is required; relative paths are resolved under `${CLAUDE_PROJECT_DIR:-$(pwd)}` (`scripts/setup-rlcr-loop.sh:163-177`).
    - Plan file must exist and have at least five lines (`scripts/setup-rlcr-loop.sh:179-193`).
    - `codex` must be available on PATH (`scripts/setup-rlcr-loop.sh:195-201`).
    - Numeric options are regex-validated as unsigned integers, but zero is accepted by the regex despite error text saying “positive integer” (`scripts/setup-rlcr-loop.sh:98-107`, `scripts/setup-rlcr-loop.sh:125-135`).
  - Generated outputs:
    - `.humanize-loop.local/<timestamp>/state.md` stores `current_round`, `max_iterations`, Codex model/effort/timeout, push policy, plan file, and start time (`scripts/setup-rlcr-loop.sh:223-234`).
    - `.humanize-loop.local/<timestamp>/goal-tracker.md` stores the immutable and mutable goal-tracking sections (`scripts/setup-rlcr-loop.sh:240-328`).
    - `.humanize-loop.local/<timestamp>/round-0-prompt.md` stores the first instruction packet (`scripts/setup-rlcr-loop.sh:334-387`).
    - Later hooks create `round-N-summary.md`, `round-N-review-prompt.md`, `round-N-review-result.md`, and `round-(N+1)-prompt.md` as the loop progresses (`hooks/loop-codex-stop-hook.sh:360-363`, `hooks/loop-codex-stop-hook.sh:491-493`, `hooks/loop-codex-stop-hook.sh:869-876`).
  - State transitions:
    - Start state: no active loop until `setup-rlcr-loop.sh` creates a timestamped directory and `state.md`.
    - Active Round 0: `current_round: 0`; the user must initialize Goal Tracker and produce `round-0-summary.md`.
    - Continue transition: Stop hook increments `current_round` with `sed`, writes the next prompt, and blocks exit (`hooks/loop-codex-stop-hook.sh:864-876`).
    - Complete transition: last non-empty Codex review line exactly `COMPLETE` removes `state.md` (`hooks/loop-codex-stop-hook.sh:813-827`).
    - Stop/circuit-breaker transition: last non-empty Codex review line exactly `STOP` removes `state.md` (`hooks/loop-codex-stop-hook.sh:830-857`).
    - Max-iteration transition: if the next round exceeds `max_iterations`, the hook removes `state.md` and exits (`hooks/loop-codex-stop-hook.sh:471-476`).
    - Manual cancel transition: `/humanize:cancel-rlcr-loop` removes `.humanize-loop.local/*/state.md` while preserving loop artifacts (`commands/cancel-rlcr-loop.md:11-24`).

- gates_or_invariants:
  - Command permission boundary:
    - The slash command only allows `Bash(${CLAUDE_PLUGIN_ROOT}/scripts/setup-rlcr-loop.sh:*)`, so command execution is restricted to the setup script path (`commands/start-rlcr-loop.md:4`).
  - Goal Tracker invariants:
    - Immutable section is Ultimate Goal and Acceptance Criteria; mutable section tracks Active Tasks, Completed Items, Deferred Items, and Plan Evolution Log (`commands/start-rlcr-loop.md:28-31`).
    - Round 0 must initialize Goal Tracker; every round should update task status, plan changes, and discovered issues (`commands/start-rlcr-loop.md:38-42`).
    - Stop hook blocks Round 0 exit if goal, acceptance criteria, or active-task placeholders remain (`hooks/loop-codex-stop-hook.sh:400-465`).
  - Summary invariant:
    - User must write a summary before exit (`commands/start-rlcr-loop.md:45`).
    - Stop hook blocks if the current round summary file is missing (`hooks/loop-codex-stop-hook.sh:360-392`).
    - Write/Edit validators enforce current-round summary paths and block wrong round numbers (`hooks/loop-write-validator.sh:139-154`, `hooks/loop-edit-validator.sh:91-113`).
  - State-file invariant:
    - The command text explicitly forbids editing state files or using cancel commands to cheat (`commands/start-rlcr-loop.md:48`).
    - Write/Edit/Bash validators block `state.md` modifications (`hooks/loop-write-validator.sh:92-95`, `hooks/loop-edit-validator.sh:72-75`, `hooks/loop-bash-validator.sh:74-77`).
  - Prompt/todos invariants:
    - Prompt files are generated instructions and cannot be modified through Write/Edit/Bash validators (`hooks/loop-write-validator.sh:42-45`, `hooks/loop-edit-validator.sh:41-44`, `hooks/loop-bash-validator.sh:101-104`).
    - `round-*-todos.md` access is blocked in favor of native TodoWrite (`hooks/loop-write-validator.sh:37-40`, `hooks/loop-edit-validator.sh:36-39`, `hooks/loop-read-validator.sh:36-39`, `hooks/loop-bash-validator.sh:121-124`).
  - Exit/review gates:
    - Incomplete todos block before Codex review (`hooks/loop-codex-stop-hook.sh:67-99`).
    - Modified code/docs files over 2000 lines block exit (`hooks/loop-codex-stop-hook.sh:108-197`).
    - Dirty git status blocks exit until committed, with a special note that `.humanize-loop.local/` should be ignored rather than committed (`hooks/loop-codex-stop-hook.sh:210-277`).
    - If `--push-every-round` is true, unpushed commits block exit (`hooks/loop-codex-stop-hook.sh:279-315`).
    - Codex completion recognition is intentionally strict: only a final standalone `COMPLETE` or `STOP` is accepted, preventing accidental matches like “CANNOT COMPLETE” (`hooks/loop-codex-stop-hook.sh:813-817`).

- dependencies_and_callers:
  - Direct dependency:
    - `${CLAUDE_PLUGIN_ROOT}/scripts/setup-rlcr-loop.sh`, invoked by the command block (`commands/start-rlcr-loop.md:12-14`).
  - Runtime dependencies:
    - `codex` CLI is required during setup and used later for review (`scripts/setup-rlcr-loop.sh:195-201`, `hooks/loop-codex-stop-hook.sh:724-751`).
    - Common shell utilities: `bash`, `date`, `wc`, `grep`, `sed`, `cat`, `mkdir`, `tr`; hook paths also use `jq`, `python3`, and `git`.
    - `hooks/check-todos-from-transcript.py` is used by the Stop hook when present to prevent exit while todos remain incomplete (`hooks/loop-codex-stop-hook.sh:65-70`).
    - `scripts/portable-timeout.sh` is sourced if present for bounded Codex execution (`hooks/loop-codex-stop-hook.sh:704-721`).
  - Hook dependencies:
    - `hooks/hooks.json` wires the command-created loop state into Claude Code lifecycle hooks (`hooks/hooks.json:4-48`).
    - Validators share helper functions from `hooks/lib/loop-common.sh`, including active loop detection, current round extraction, round-file classification, and blocked-message rendering (`hooks/lib/loop-common.sh:15-47`, `hooks/lib/loop-common.sh:54-90`, `hooks/lib/loop-common.sh:110-236`).
  - Caller/user surface:
    - User invokes `/humanize:start-rlcr-loop <plan.md> ...` as documented by the setup help and README references.
    - `/humanize:cancel-rlcr-loop` is the sibling command for manual termination; it removes active state files but leaves summaries and review results (`commands/cancel-rlcr-loop.md:19-24`).

- edge_cases_or_failure_modes:
  - Thin wrapper risk:
    - `commands/start-rlcr-loop.md` has no local fallback if `${CLAUDE_PLUGIN_ROOT}` is unset or points to the wrong plugin root; setup depends entirely on that environment path (`commands/start-rlcr-loop.md:4`, `commands/start-rlcr-loop.md:12-14`).
  - Argument validation mismatch:
    - `--max 0` and `--codex-timeout 0` pass the `^[0-9]+$` regex even though error text says positive integer. `--max 0` causes the first Stop hook attempt to exceed max iterations immediately after setup (`scripts/setup-rlcr-loop.sh:98-107`, `scripts/setup-rlcr-loop.sh:125-135`, `hooks/loop-codex-stop-hook.sh:471-476`).
  - Multiple active directories:
    - Active loop selection only considers the newest timestamped directory and ignores older directories even if they still contain `state.md`, preventing zombie resurrection but making older active states unreachable through normal hooks (`hooks/lib/loop-common.sh:11-33`).
  - State corruption:
    - Non-numeric `current_round` causes the Stop hook to warn, delete `state.md`, and stop the loop (`hooks/loop-codex-stop-hook.sh:344-349`).
    - Non-numeric `max_iterations` silently defaults to 42 (`hooks/loop-codex-stop-hook.sh:351-354`).
  - Plan heuristic limitations:
    - Goal extraction looks for specific second-level headings and otherwise inserts placeholders for Round 0 to resolve (`scripts/setup-rlcr-loop.sh:263-291`).
    - Acceptance-criteria extraction is similarly heading-based and may capture too little or too much if the plan format differs (`scripts/setup-rlcr-loop.sh:285-291`).
  - Git gate interaction:
    - The setup script creates `.humanize-loop.local/`; if that directory is untracked and not ignored, the Stop hook sees dirty git status and blocks exit, telling the user to add an ignore rule (`hooks/loop-codex-stop-hook.sh:218-227`, `hooks/loop-codex-stop-hook.sh:248-277`).
  - Codex failure:
    - If Codex does not create a review result and has no stdout fallback, the Stop hook blocks and reports debug file paths plus stderr tail (`hooks/loop-codex-stop-hook.sh:757-807`).
  - Cancellation bypass:
    - The command text forbids cheating by canceling, but the sibling cancel command intentionally supports state-file removal for user-controlled stop. This is a policy tension rather than an implementation bug (`commands/start-rlcr-loop.md:48`, `commands/cancel-rlcr-loop.md:19-24`).
  - Read validator escape hatch:
    - The Read validator blocks reading wrong round files through Read, but its message says to use `cat` if needed, so Bash reads remain available for historical inspection (`hooks/loop-read-validator.sh:98-130`).

- validation_or_tests:
  - No dedicated automated tests were found for `commands/start-rlcr-loop.md` in this branch export.
  - Validation is implemented as runtime gates:
    - Setup-time gates validate argument shape, plan existence, minimum plan length, and Codex CLI availability (`scripts/setup-rlcr-loop.sh:93-201`).
    - Hook-time gates validate todo completion, large-file policy, git clean/push state, state integrity, summary existence, Round 0 Goal Tracker initialization, and Codex review output (`hooks/loop-codex-stop-hook.sh:67-99`, `hooks/loop-codex-stop-hook.sh:110-197`, `hooks/loop-codex-stop-hook.sh:199-316`, `hooks/loop-codex-stop-hook.sh:322-392`, `hooks/loop-codex-stop-hook.sh:400-465`, `hooks/loop-codex-stop-hook.sh:771-817`).
    - PreToolUse validators enforce safe file access and prevent direct tampering with loop state, generated prompts, wrong-round summaries, and post-Round-0 Goal Tracker state (`hooks/loop-write-validator.sh:37-173`, `hooks/loop-edit-validator.sh:36-117`, `hooks/loop-read-validator.sh:36-151`, `hooks/loop-bash-validator.sh:53-126`).
  - Research verification performed:
    - Inspected the assigned file directly with line numbers.
    - Followed direct references to `scripts/setup-rlcr-loop.sh`, `hooks/hooks.json`, `commands/cancel-rlcr-loop.md`, `hooks/lib/loop-common.sh`, and key validator/Stop-hook paths.
    - No files were modified.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1/1; single assigned item section present above`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`