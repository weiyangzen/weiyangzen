# agent_16 improve-monitor-script 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `5af20b79e6fec323a2d5cb9344a6a584db1c635a`

## Item Evidence

### IMPROVE_MONITOR_SCRIPT-HZ-016 `file` `hooks/loop-bash-validator.sh`
- cursor: `[_]`
- core_role: PreToolUse Bash gate for the RLCR loop. It prevents shell commands from bypassing the direct Write/Edit/Read validators and protects loop-owned state surfaces while an active `.humanize/rlcr/<timestamp>/state.md` exists. It is registered as the Bash PreToolUse hook in `hooks/hooks.json:42-48`.

- algorithmic_behavior: The script reads hook JSON from stdin, exits immediately unless `.tool_name` is `Bash`, extracts `.tool_input.command`, lowercases it, finds the newest active loop under `${CLAUDE_PROJECT_DIR:-$(pwd)}/.humanize/rlcr`, parses `state.md`, then applies ordered blocking checks. The main decision flow is:
  - Non-Bash tools are ignored at `hooks/loop-bash-validator.sh:22-27`.
  - Active loop detection uses `find_active_loop` at `hooks/loop-bash-validator.sh:36-42`; no active loop means all Bash commands are allowed.
  - State parsing loads `current_round` and `push_every_round` at `hooks/loop-bash-validator.sh:45-58`.
  - `git push` is blocked when `push_every_round` is not true at `hooks/loop-bash-validator.sh:59-68`.
  - Shell modifications to `state.md` are blocked at `hooks/loop-bash-validator.sh:76-79`.
  - Shell modifications to the loop backup `plan.md` are blocked at `hooks/loop-bash-validator.sh:87-92`.
  - Shell modifications to `goal-tracker.md` are blocked at `hooks/loop-bash-validator.sh:100-109`; Round 0 gets a Bash-specific “use Write/Edit” message, while later rounds get the assigned goal-tracker request template.
  - Shell modifications to generated prompt files are blocked at `hooks/loop-bash-validator.sh:116-119`.
  - Shell modifications to summary files are blocked at `hooks/loop-bash-validator.sh:126-130` so summaries go through Write/Edit validators.
  - Shell modifications to todos files are only allowed for full active-loop paths matching `round-1-todos.md` or `round-2-todos.md`; all other `round-*-todos.md` Bash writes are blocked at `hooks/loop-bash-validator.sh:136-144`.

- inputs_outputs_state: Input is Claude hook JSON on stdin with `tool_name` and `tool_input.command`. It also consumes environment state from `CLAUDE_PROJECT_DIR`, the filesystem state under `.humanize/rlcr`, and frontmatter fields parsed from the active loop `state.md`, especially `current_round` and `push_every_round`. Output is either exit `0` to allow the Bash command or exit `2` with a rendered Markdown block on stderr to block it. It does not mutate repository or loop files. Its state transition role is protective: it preserves active RLCR loop state by preventing direct shell mutation of protected files and redirects allowed state changes into the intended loop channels, especially summary-file requests and Codex review.

- gates_or_invariants: The hook enforces these invariants while an active loop exists:
  - `state.md` is system-managed and cannot be modified through Bash.
  - The loop backup `plan.md` is read-only.
  - `goal-tracker.md` can never be modified through Bash; after Round 0, any goal-tracker change must be requested through the current summary file.
  - Generated `round-*-prompt.md` files are read-only.
  - `round-*-summary.md` files must be written through Write/Edit validators, not shell redirection or shell editors.
  - `round-*-todos.md` Bash writes are denied except for the full active-loop path to `round-1-todos.md` or `round-2-todos.md`.
  - `git push` is denied unless loop state explicitly has `push_every_round: true`.

- dependencies_and_callers: Depends on `jq`, Bash, `grep`, `sed`, `tr`, and shared hook library `hooks/lib/loop-common.sh` sourced at `hooks/loop-bash-validator.sh:14-16`. Active-loop selection and state parsing are implemented in `hooks/lib/loop-common.sh:62-79` and `hooks/lib/loop-common.sh:110-137`. File-modification detection is delegated to `command_modifies_file` in `hooks/lib/loop-common.sh:260-285`, which matches redirection, append redirection, `tee`, `sed -i`, `awk -i inplace`, `perl -i`, two-argument `mv`/`cp`, `rm`, `dd of=`, `truncate`, `printf >`, and fd redirection. Rendered block messages come through template-loader helpers via message functions in `hooks/lib/loop-common.sh:188-237` and `hooks/lib/loop-common.sh:287-299`.

- edge_cases_or_failure_modes: The command classifier is regex-based over the literal lowercased command string, so it cannot resolve variables, command substitutions, symlinks, aliases, or runtime path expansion. Existing tests explicitly document that `echo x > $FILE` is not detected and that multi-source `cp file1 file2 goal-tracker.md` is a known limitation in `tests/test-bash-validator-patterns.sh:165-172`. The `git push` block only matches commands beginning with optional whitespace then `git push`, so indirect forms such as `cd repo && git push` are not covered by that specific gate. The `state.md` and `goal-tracker.md` patterns are broad by basename, so they may block Bash writes to similarly named files outside the loop while a loop is active. The todos allowlist requires the literal full active loop path in the command string; relative paths, quoted/escaped path variants, variables, or equivalent paths through symlinks will be blocked even if they resolve to the active loop file. The plan backup pattern targets `.humanize/rlcr/<optional-one-segment>/plan.md`, matching the expected loop-root backup but not arbitrary nested `plan.md` paths.

- validation_or_tests: I did not execute tests because this is a read-only research task. Relevant inspected coverage includes `tests/test-bash-validator-patterns.sh:69-194`, which exercises the shared Bash modification regexes and documents false-positive/false-negative expectations, and `tests/test-allowlist-validators.sh:288-380`, which verifies Bash todos allowlist behavior for active-loop full paths, wrong directories, wrong round numbers, generic relative paths, old loop directories, and same-basename different roots. Hook registration coverage is visible in `hooks/hooks.json:42-48`.

- skip_candidate: `no`

### IMPROVE_MONITOR_SCRIPT-HZ-046 `file` `prompt-template/block/goal-tracker-modification.md`
- cursor: `[_]`
- core_role: Markdown block template for the post-Round-0 goal-tracker ownership gate. It tells Claude that only Codex can modify `goal-tracker.md` after Round 0 and specifies the required summary-file request contract. Although it is not executable code, it is core to the RLCR state machine because it defines the transition from direct goal-tracker mutation to request-mediated Codex updates.

- algorithmic_behavior: The template renders a blocking message headed with the current round at `prompt-template/block/goal-tracker-modification.md:1`. It states that after Round 0 only Codex can modify the Goal Tracker at `prompt-template/block/goal-tracker-modification.md:3`, prohibits direct modification through Write, Edit, or Bash at `prompt-template/block/goal-tracker-modification.md:5`, and instructs the agent to include a `Goal Tracker Update Request` section in the current summary file at `prompt-template/block/goal-tracker-modification.md:7-23`. The requested format separates requested changes from justification, making goal-tracker updates reviewable rather than directly mutating loop state. The message closes by stating that Codex will review and update if justified at `prompt-template/block/goal-tracker-modification.md:25`.

- inputs_outputs_state: Template inputs are `CURRENT_ROUND` and `SUMMARY_FILE`, passed by `goal_tracker_blocked_message` in `hooks/lib/loop-common.sh:289-298`. Output is rendered Markdown used as the validator’s blocking reason. The immediate state transition is “attempted direct goal-tracker write” to “blocked action plus required summary update request.” The downstream state transition occurs when the stop hook reads the summary and includes Codex goal-tracker update instructions in the review prompt; this handoff is assembled in `hooks/loop-codex-stop-hook.sh:636-642` and inserted into regular or full-alignment review prompts at `hooks/loop-codex-stop-hook.sh:679-705`.

- gates_or_invariants: The template expresses these invariants:
  - After Round 0, Claude does not directly modify `goal-tracker.md`.
  - Goal-tracker changes must be expressed as a structured request in the current round summary.
  - Requests require both concrete requested changes and justification tied to the Ultimate Goal.
  - Codex is the reviewer and applying authority for accepted changes.
  - The template pairs with the Codex-side rule in `prompt-template/codex/goal-tracker-update-section.md:3-11`, where Codex evaluates requests, updates the tracker if approved, rejects unjustified requests, and must never modify the immutable Ultimate Goal / Acceptance Criteria section.

- dependencies_and_callers: Called by `goal_tracker_blocked_message` in `hooks/lib/loop-common.sh:296-298`. Direct Write attempts after Round 0 call it through `hooks/loop-write-validator.sh:117-120`; direct Edit attempts call it through `hooks/loop-edit-validator.sh:102-105`; Bash modification attempts after Round 0 call it through `hooks/loop-bash-validator.sh:100-107`. The next-round prompt also includes a separate Claude-side request template from `prompt-template/claude/goal-tracker-update-request.md:2-16`, appended by `hooks/loop-codex-stop-hook.sh:1013-1018`. Template existence is checked in `tests/test-template-references.sh:152-159`.

- edge_cases_or_failure_modes: If this template is missing or cannot be loaded, `goal_tracker_blocked_message` falls back to a shorter inline message in `hooks/lib/loop-common.sh:292-298`, so blocking still occurs but the detailed request format is degraded. The template itself does not validate that the summary file exists, that the agent uses the exact heading, or that Codex actually applies the requested update; those are prompt-contract behaviors enforced indirectly through the stop-hook review flow. If placeholders are not rendered correctly, the user-facing block would expose `{{CURRENT_ROUND}}` or `{{SUMMARY_FILE}}`, but the fallback path reduces the chance of a totally empty block. This template is intentionally inactive for Round 0; Round 0 Bash goal-tracker writes get a different Bash-specific block, while Write/Edit can be used for initial tracker setup according to the surrounding validator behavior.

- validation_or_tests: I did not execute tests because this is a read-only research task. Inspected validation surfaces include `tests/test-template-references.sh:152-159`, which requires `block/goal-tracker-modification.md` to exist among common templates, plus caller references in Write/Edit/Bash validators and the Codex review-prompt handoff. Related behavior is covered by the Codex instruction template at `prompt-template/codex/goal-tracker-update-section.md:1-17` and the Claude request template at `prompt-template/claude/goal-tracker-update-request.md:2-16`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 2/2 evidence sections present, each assigned item heading appears once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`