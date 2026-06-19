# agent_09 add-a-final-code-simplifier-after-codex-complete 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 3
- source_commit: `71ed63c83360c154ed316e8e38853af41ffc3b7e`

## Item Evidence

### ADD_A_FINAL_CODE_SIMPLIFIER_AFTER_CODEX_COMPLETE-HZ-009 `directory` `prompt-template/block`
- cursor: `[_]`
- core_role:
  `prompt-template/block` is the repository’s blocking-message template set for RLCR hook gates. The directory does not enforce transitions by itself; it defines the human-facing contract emitted when validators or stop hooks block reads, writes, bash commands, loop exits, stale schema, dirty git state, missing summaries, incomplete todos, or invalid round/path access. These templates are algorithmically core because hook decisions use them as the reason payload for blocked tool use or stop-hook responses.

- algorithmic_behavior:
  The directory is consumed through `hooks/lib/template-loader.sh`, where `load_template` reads a relative template path, `render_template` performs single-pass `{{VAR}}` substitution, and `load_and_render_safe` falls back if a template is missing or renders empty (`hooks/lib/template-loader.sh:36`, `hooks/lib/template-loader.sh:58`, `hooks/lib/template-loader.sh:170`). The single-pass renderer intentionally does not recursively expand injected placeholders (`hooks/lib/template-loader.sh:54`), so review text or file paths containing `{{...}}` cannot corrupt subsequent prompt rendering.
  
  Contained child roles:
  - Path and round routing templates: `wrong-file-location.md`, `wrong-directory-path.md`, `wrong-round-number.md`, `wrong-round-file.md`, and `wrong-summary-location.md` explain the active loop directory/current-round invariant and provide the correct path (`prompt-template/block/wrong-file-location.md:3`, `prompt-template/block/wrong-round-number.md:3`, `prompt-template/block/wrong-summary-location.md:3`).
  - Managed-file immutability templates: `prompt-file-write.md`, `state-file-modification.md`, `finalized-state-file-modification.md`, `plan-file-modified.md`, `plan-backup-protected.md`, `goal-tracker-modification.md`, `goal-tracker-bash-write.md`, and `summary-bash-write.md` tell the worker which files are system-owned and which write path is allowed (`prompt-template/block/prompt-file-write.md:3`, `prompt-template/block/state-file-modification.md:3`, `prompt-template/block/finalized-state-file-modification.md:3`, `prompt-template/block/goal-tracker-modification.md:3`).
  - Exit and repository hygiene templates: `incomplete-todos.md`, `work-summary-missing.md`, `git-status-failed.md`, `git-not-clean.md`, `git-not-clean-humanize-local.md`, `git-not-clean-untracked.md`, `unpushed-commits.md`, `git-push.md`, `large-files.md`, `codex-review-failed.md`, `schema-outdated.md`, and `goal-tracker-not-initialized.md` support the stop-hook’s pre-review and post-review gates (`prompt-template/block/incomplete-todos.md:3`, `prompt-template/block/git-not-clean.md:3`, `prompt-template/block/unpushed-commits.md:3`, `prompt-template/block/work-summary-missing.md:3`).
  - Final code simplifier messaging is present in several block templates: dirty-git exit guidance includes a step to invoke `code-simplifier` before committing (`prompt-template/block/git-not-clean.md:6`), large-file remediation suggests using it after splitting (`prompt-template/block/large-files.md:16`), and finalized-state protection tells the agent to focus on running the code-simplifier, committing, and writing `finalize-summary.md` (`prompt-template/block/finalized-state-file-modification.md:5`).

- inputs_outputs_state:
  Inputs are template variables passed by hook code, such as `FILE_PATH`, `ACTIVE_LOOP_DIR`, `CURRENT_ROUND`, `CLAUDE_ROUND`, `FILE_TYPE`, `CORRECT_PATH`, `PLAN_FILE`, `BACKUP_PATH`, `INCOMPLETE_LIST`, `GIT_STATUS_EXIT`, `GIT_ISSUES`, `SPECIAL_NOTES`, `AHEAD_COUNT`, `CURRENT_BRANCH`, `SUMMARY_FILE`, `GOAL_TRACKER_FILE`, and `MISSING_ITEMS`. Output is rendered Markdown, normally placed on stderr for PreToolUse hook blocks or inside JSON `reason` fields for stop-hook blocks.
  
  State is not mutated by these files. They describe state transitions enforced elsewhere: retry current tool call with a correct path, finish todos, commit changes, push if configured, initialize the goal tracker, cancel/restart an outdated loop, or continue the RLCR loop. The templates coordinate with `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-bash-validator.sh`, `hooks/loop-plan-file-validator.sh`, and `hooks/loop-codex-stop-hook.sh`.

- gates_or_invariants:
  The templates encode the visible explanation for these invariants:
  - Do not create/read/write `round-*-todos.md`; use native TodoWrite, except narrow allowlisted cases enforced in `loop-common.sh` (`prompt-template/block/todos-file-access.md:3`).
  - Prompt files are read-only instructions from Codex to Claude (`prompt-template/block/prompt-file-write.md:3`).
  - `state.md` and `finalized-state.md` are system-managed (`prompt-template/block/state-file-modification.md:3`, `prompt-template/block/finalized-state-file-modification.md:3`).
  - Plan backups and tracked plan content must not change during an active loop (`prompt-template/block/plan-file-modified.md:3`, `prompt-template/block/plan-backup-protected.md:3`).
  - After Round 0, goal-tracker changes must be requested in the summary rather than written directly (`prompt-template/block/goal-tracker-modification.md:3`).
  - A stop attempt requires todos complete, a summary file present, no oversized changed code/doc files, clean git state, and optionally pushed commits (`prompt-template/block/incomplete-todos.md:7`, `prompt-template/block/work-summary-missing.md:5`, `prompt-template/block/large-files.md:3`, `prompt-template/block/git-not-clean.md:5`, `prompt-template/block/unpushed-commits.md:5`).

- dependencies_and_callers:
  `hooks/lib/loop-common.sh` wraps several templates as reusable message functions: todos, prompt writes, state writes, finalized-state writes, summary bash writes, goal-tracker bash writes, and post-Round-0 goal-tracker writes (`hooks/lib/loop-common.sh:190`, `hooks/lib/loop-common.sh:201`, `hooks/lib/loop-common.sh:210`, `hooks/lib/loop-common.sh:219`, `hooks/lib/loop-common.sh:228`, `hooks/lib/loop-common.sh:239`, `hooks/lib/loop-common.sh:450`).
  
  Direct callers include:
  - Read validator path/round blocks (`hooks/loop-read-validator.sh:105`, `hooks/loop-read-validator.sh:122`, `hooks/loop-read-validator.sh:141`).
  - Write validator state, plan, summary, and path blocks (`hooks/loop-write-validator.sh:105`, `hooks/loop-write-validator.sh:132`, `hooks/loop-write-validator.sh:155`, `hooks/loop-write-validator.sh:181`, `hooks/loop-write-validator.sh:207`).
  - Edit validator equivalent blocks (`hooks/loop-edit-validator.sh:86`, `hooks/loop-edit-validator.sh:101`, `hooks/loop-edit-validator.sh:124`).
  - Bash validator git push, state/finalized-state, plan, goal-tracker, prompt, summary, and todos command blocks (`hooks/loop-bash-validator.sh:63`, `hooks/loop-bash-validator.sh:87`, `hooks/loop-bash-validator.sh:272`, `hooks/loop-bash-validator.sh:285`, `hooks/loop-bash-validator.sh:301`, `hooks/loop-bash-validator.sh:311`, `hooks/loop-bash-validator.sh:321`).
  - Stop hook plan modification, incomplete todos, git status, large files, dirty git, unpushed commits, missing summary, and goal tracker initialization blocks (`hooks/loop-codex-stop-hook.sh:230`, `hooks/loop-codex-stop-hook.sh:284`, `hooks/loop-codex-stop-hook.sh:325`, `hooks/loop-codex-stop-hook.sh:399`, `hooks/loop-codex-stop-hook.sh:461`, `hooks/loop-codex-stop-hook.sh:489`, `hooks/loop-codex-stop-hook.sh:529`, `hooks/loop-codex-stop-hook.sh:611`).

- edge_cases_or_failure_modes:
  Missing templates should not produce empty block reasons because most critical callers use `load_and_render_safe` with inline fallbacks (`hooks/lib/template-loader.sh:167`). Two special-note templates are loaded with `load_template`, but the stop hook provides inline fallback strings if they are absent (`hooks/loop-codex-stop-hook.sh:443`, `hooks/loop-codex-stop-hook.sh:453`).
  
  Missing variables remain visible as unresolved placeholders rather than failing rendering (`hooks/lib/template-loader.sh:13`). That is fail-soft but can leave confusing block text if a caller forgets a variable. The directory also contains some advisory text that is not itself enforcement. For example, `git-not-clean.md` and `large-files.md` recommend code-simplifier invocation, but the hard gate is the stop hook’s git/large-file check, not plugin detection.

- validation_or_tests:
  `tests/test-template-references.sh` scans hook scripts for `load_template`, `load_and_render`, and `load_and_render_safe` references and fails if referenced templates are missing (`tests/test-template-references.sh:56`, `tests/test-template-references.sh:93`, `tests/test-template-references.sh:102`). It also checks common `loop-common.sh` templates exist (`tests/test-template-references.sh:149`). `tests/test-templates-comprehensive.sh` includes real-template rendering checks for `wrong-round-number.md` and `unpushed-commits.md` (`tests/test-templates-comprehensive.sh:498`, `tests/test-templates-comprehensive.sh:517`). I did not execute tests in this read-only research pass.

- skip_candidate: `no`

### ADD_A_FINAL_CODE_SIMPLIFIER_AFTER_CODEX_COMPLETE-HZ-039 `file` `hooks/lib/loop-common.sh`
- cursor: `[_]`
- core_role:
  `hooks/lib/loop-common.sh` is the shared RLCR hook library. It centralizes state field names, terminal-state markers, active-loop discovery, state frontmatter parsing, round-file recognition, protected-path detection, cancel authorization, bash write-pattern detection, reusable block-message rendering, and state-file termination. Hook scripts source it before applying read/write/edit/bash/stop/plan gates (`hooks/loop-read-validator.sh:16`, `hooks/loop-write-validator.sh:17`, `hooks/loop-edit-validator.sh:16`, `hooks/loop-bash-validator.sh:16`, `hooks/loop-codex-stop-hook.sh:48`, `hooks/loop-plan-file-validator.sh:17`).

- algorithmic_behavior:
  Key sections:
  - Constants define state frontmatter keys, Codex review markers, and terminal exit reasons (`hooks/lib/loop-common.sh:15`, `hooks/lib/loop-common.sh:26`, `hooks/lib/loop-common.sh:30`).
  - Template setup sources `template-loader.sh`, resolves `TEMPLATE_DIR`, and warns rather than aborting if template validation fails (`hooks/lib/loop-common.sh:46`, `hooks/lib/loop-common.sh:51`, `hooks/lib/loop-common.sh:53`).
  - `find_active_loop` inspects only the newest `.humanize/rlcr/*/` directory and returns it only if it contains `state.md` or `finalized-state.md` (`hooks/lib/loop-common.sh:58`, `hooks/lib/loop-common.sh:71`, `hooks/lib/loop-common.sh:75`). This prevents older “zombie” loop folders from becoming active again.
  - `get_current_round` and `parse_state_file` extract YAML-like frontmatter between `---` delimiters, set global `STATE_*` variables, strip legacy quotes for branch/plan fields, and default missing `current_round`, `max_iterations`, and `push_every_round` values (`hooks/lib/loop-common.sh:83`, `hooks/lib/loop-common.sh:98`, `hooks/lib/loop-common.sh:119`, `hooks/lib/loop-common.sh:133`).
  - Round-file helpers identify `round-N-summary.md`, `round-N-prompt.md`, and `round-N-todos.md`, and extract `N` (`hooks/lib/loop-common.sh:146`, `hooks/lib/loop-common.sh:155`).
  - `is_allowlisted_file` allows a small exact-path exception set for early todo/summary files inside the active loop directory (`hooks/lib/loop-common.sh:167`, `hooks/lib/loop-common.sh:174`).
  - Block-message functions render templates with fallbacks for todos, prompt writes, state writes, finalized-state writes, summary bash writes, goal-tracker bash writes, and post-Round-0 goal-tracker modifications (`hooks/lib/loop-common.sh:190`, `hooks/lib/loop-common.sh:201`, `hooks/lib/loop-common.sh:210`, `hooks/lib/loop-common.sh:219`, `hooks/lib/loop-common.sh:228`, `hooks/lib/loop-common.sh:239`, `hooks/lib/loop-common.sh:450`).
  - Path classifiers identify `goal-tracker.md`, `state.md`, `finalized-state.md`, and `finalize-summary.md` (`hooks/lib/loop-common.sh:250`, `hooks/lib/loop-common.sh:256`, `hooks/lib/loop-common.sh:262`, `hooks/lib/loop-common.sh:268`).
  - `is_cancel_authorized` is a security gate for the only allowed state-file move during cancel: it requires `.cancel-requested`, rejects command substitution, backticks, newlines, shell chaining operators, hidden variables, non-`mv` commands, wrong source/destination paths, and extra args (`hooks/lib/loop-common.sh:274`, `hooks/lib/loop-common.sh:290`, `hooks/lib/loop-common.sh:295`, `hooks/lib/loop-common.sh:305`, `hooks/lib/loop-common.sh:323`, `hooks/lib/loop-common.sh:328`, `hooks/lib/loop-common.sh:378`, `hooks/lib/loop-common.sh:396`, `hooks/lib/loop-common.sh:404`).
  - `command_modifies_file` detects common bash-side write bypasses such as redirection, `tee`, in-place editors, `mv`/`cp` to target, `rm`, `dd of=`, `truncate`, `printf >`, and `exec fd>` (`hooks/lib/loop-common.sh:420`, `hooks/lib/loop-common.sh:427`).
  - `end_loop` validates the terminal reason and renames the active state file to `complete-state.md`, `cancel-state.md`, `maxiter-state.md`, `stop-state.md`, or `unexpected-state.md` (`hooks/lib/loop-common.sh:464`, `hooks/lib/loop-common.sh:476`, `hooks/lib/loop-common.sh:486`, `hooks/lib/loop-common.sh:488`).

- inputs_outputs_state:
  Inputs:
  - Filesystem paths: loop base dir, state file, active loop dir, file paths from hook payloads.
  - Parsed command strings: lowercased bash commands for cancel and write-bypass detection.
  - State frontmatter fields: `plan_tracked`, `start_branch`, `plan_file`, `current_round`, `max_iterations`, `push_every_round`, `codex_model`, `codex_effort`, and `codex_timeout`.
  - Template variables for rendered block messages.
  
  Outputs:
  - Shell return codes from predicate functions.
  - Echoed active-loop path, current round, or rendered Markdown.
  - Global `STATE_*` variables from `parse_state_file`.
  - Filesystem state transition from `end_loop` via `mv`.
  
  State transitions:
  - Normal active loop: `state.md` exists.
  - Finalize active loop: `finalized-state.md` exists and is considered active by `find_active_loop` (`hooks/lib/loop-common.sh:61`, `hooks/lib/loop-common.sh:75`).
  - Terminal loop: `end_loop` renames active state to a reason-specific `*-state.md`; those terminal files are not recognized by `find_active_loop`.
  - Authorized cancel path permits moving `state.md` to `cancel-state.md` only when the signal file and exact command shape match. It does not authorize `finalized-state.md` moves.

- gates_or_invariants:
  - Only the newest loop directory can be active; older folders are ignored even if they still contain state (`hooks/lib/loop-common.sh:58`).
  - `finalized-state.md` is a first-class active state for Finalize Phase detection (`hooks/lib/loop-common.sh:61`, `hooks/lib/loop-common.sh:76`).
  - `state.md` matching is broad enough that `finalized-state.md` also matches `state\.md$`; validators therefore check finalized-state first, as seen in write/edit/bash callers (`hooks/loop-write-validator.sh:103`, `hooks/loop-edit-validator.sh:84`, `hooks/loop-bash-validator.sh:80`).
  - Cancel is fail-closed: no signal file, command substitution, extra args, chained commands, remaining `$`, wrong source, or wrong destination means unauthorized (`hooks/lib/loop-common.sh:290`, `hooks/lib/loop-common.sh:295`, `hooks/lib/loop-common.sh:300`, `hooks/lib/loop-common.sh:305`, `hooks/lib/loop-common.sh:323`, `hooks/lib/loop-common.sh:383`, `hooks/lib/loop-common.sh:396`).
  - Bash write detection is pattern-based and intentionally catches multiple write mechanisms rather than only `>` redirection (`hooks/lib/loop-common.sh:427`).
  - Terminal exit reasons are whitelisted before state rename (`hooks/lib/loop-common.sh:476`).

- dependencies_and_callers:
  `loop-common.sh` depends on `hooks/lib/template-loader.sh` for template discovery and rendering (`hooks/lib/loop-common.sh:47`). It is sourced by the read/write/edit/bash validators, stop hook, and plan-file validator. The validators combine its helpers with JSON hook payload parsing through `jq`; stop/plan hooks additionally use `scripts/portable-timeout.sh` for git timeouts (`hooks/loop-codex-stop-hook.sh:50`, `hooks/loop-plan-file-validator.sh:19`).
  
  Important caller behaviors:
  - Read validator uses `find_active_loop`, `parse_state_file`, round helpers, `is_allowlisted_file`, and rendered block messages to prevent stale or misplaced round-file reads (`hooks/loop-read-validator.sh:36`, `hooks/loop-read-validator.sh:63`, `hooks/loop-read-validator.sh:75`, `hooks/loop-read-validator.sh:116`).
  - Write and edit validators protect todos, prompts, state/finalized-state, plan backup, goal tracker, and wrong-round summaries (`hooks/loop-write-validator.sh:37`, `hooks/loop-write-validator.sh:47`, `hooks/loop-write-validator.sh:105`, `hooks/loop-write-validator.sh:145`; `hooks/loop-edit-validator.sh:36`, `hooks/loop-edit-validator.sh:86`, `hooks/loop-edit-validator.sh:114`).
  - Bash validator uses `command_modifies_file` and `is_cancel_authorized`, with extra source-side protections for moving/copying `state.md` or `finalized-state.md` (`hooks/loop-bash-validator.sh:87`, `hooks/loop-bash-validator.sh:93`, `hooks/loop-bash-validator.sh:113`, `hooks/loop-bash-validator.sh:230`).
  - Stop hook uses `parse_state_file`, marker constants, exit reasons, and `end_loop` to progress rounds, enter Finalize Phase, terminate as max-iteration/stop/unexpected, or complete Finalize Phase (`hooks/loop-codex-stop-hook.sh:88`, `hooks/loop-codex-stop-hook.sh:102`, `hooks/loop-codex-stop-hook.sh:961`, `hooks/loop-codex-stop-hook.sh:1049`).

- edge_cases_or_failure_modes:
  - `find_active_loop` sorts directory names lexically descending, so timestamp naming must remain sortable; a newer malformed directory suppresses older active loops by design.
  - `parse_state_file` is permissive and does not itself validate required fields or numeric values. Callers handle schema and numeric validation, such as stop hook checks for invalid `codex_model`, `codex_effort`, and `current_round` (`hooks/loop-codex-stop-hook.sh:102`, `hooks/loop-codex-stop-hook.sh:115`).
  - `is_state_file_path` matches `finalized-state.md`; this is explicitly handled by caller ordering, but a new caller could get it wrong.
  - `is_in_humanize_loop_dir` is a substring grep, not canonical path validation (`hooks/lib/loop-common.sh:414`). Callers that need exact active-loop paths compare later.
  - `command_modifies_file` is regex-based and not a full shell parser. The tests document a known limitation: multi-source `cp file1 file2 goal-tracker.md` is not detected by the basic `cp src dest` pattern (`tests/test-bash-validator-patterns.sh:166`). The bash validator adds extra segmentation and source-side state-file checks for the most sensitive state moves (`hooks/loop-bash-validator.sh:113`).
  - `is_cancel_authorized` lowercases the command and active loop path before comparison. That is useful for normalized hook input but assumes lowercased path comparison is acceptable for the intended environment.

- validation_or_tests:
  - `tests/test-bash-validator-patterns.sh` directly tests `command_modifies_file` against redirection, `tee`, in-place editors, file ops, `dd`, `truncate`, `exec`, false positives, state files, and summary files (`tests/test-bash-validator-patterns.sh:69`, `tests/test-bash-validator-patterns.sh:82`, `tests/test-bash-validator-patterns.sh:96`, `tests/test-bash-validator-patterns.sh:110`, `tests/test-bash-validator-patterns.sh:124`, `tests/test-bash-validator-patterns.sh:136`, `tests/test-bash-validator-patterns.sh:175`, `tests/test-bash-validator-patterns.sh:186`).
  - `tests/test-finalize-phase.sh` covers finalized-state helpers, active-loop detection for `finalized-state.md`, terminal non-detection for `complete-state.md`, validator protection of `finalized-state.md`, Finalize Phase entry/completion, and validator parsing of finalized state (`tests/test-finalize-phase.sh:174`, `tests/test-finalize-phase.sh:219`, `tests/test-finalize-phase.sh:238`, `tests/test-finalize-phase.sh:293`, `tests/test-finalize-phase.sh:460`, `tests/test-finalize-phase.sh:617`).
  - `tests/test-cancel-signal-file.sh` exercises `is_cancel_authorized` directly for signal, missing signal, wrong commands, extra args, quoted paths, and hidden variables (`tests/test-cancel-signal-file.sh:1254`).
  - `tests/test-state-exit-naming.sh` covers `find_active_loop` and `end_loop` terminal file naming (`tests/test-state-exit-naming.sh:64`, `tests/test-state-exit-naming.sh:179`).
  I did not execute tests in this read-only branch research run.

- skip_candidate: `no`

### ADD_A_FINAL_CODE_SIMPLIFIER_AFTER_CODEX_COMPLETE-HZ-069 `file` `prompt-template/claude/next-round-footer.md`
- cursor: `[_]`
- core_role:
  `prompt-template/claude/next-round-footer.md` is the footer appended to the next-round prompt when Codex review does not return `COMPLETE` or `STOP` and the RLCR loop advances to another round. It is part of the prompt-driven transition contract: do not fake exit, do not modify state/cancel, optionally run code-simplifier, commit, and write the next summary.

- algorithmic_behavior:
  The footer begins with a separator, warns that the agent must not exit by “lying,” editing the loop state file, or executing `cancel-rlcr-loop`, then lists required post-work actions (`prompt-template/claude/next-round-footer.md:2`, `prompt-template/claude/next-round-footer.md:4`, `prompt-template/claude/next-round-footer.md:6`). Its only template input is `{{NEXT_SUMMARY_FILE}}`, rendered into the final summary instruction (`prompt-template/claude/next-round-footer.md:9`).
  
  The stop hook uses this template after Codex finds issues: it increments `current_round`, writes `round-N-prompt.md`, optionally appends post-alignment guidance, appends this footer, then optionally appends push and goal-tracker request instructions (`hooks/loop-codex-stop-hook.sh:1057`, `hooks/loop-codex-stop-hook.sh:1062`, `hooks/loop-codex-stop-hook.sh:1075`, `hooks/loop-codex-stop-hook.sh:1080`, `hooks/loop-codex-stop-hook.sh:1088`, `hooks/loop-codex-stop-hook.sh:1094`, `hooks/loop-codex-stop-hook.sh:1103`).

- inputs_outputs_state:
  Input:
  - `NEXT_SUMMARY_FILE`, passed by `loop-codex-stop-hook.sh` as the active loop’s next summary path (`hooks/loop-codex-stop-hook.sh:1064`, `hooks/loop-codex-stop-hook.sh:1091`).
  
  Output:
  - Rendered Markdown appended to `round-${NEXT_ROUND}-prompt.md`.
  
  State transition context:
  - Before this footer is rendered, the stop hook updates `current_round` in the state file with `sed` and moves the temp file over the state file (`hooks/loop-codex-stop-hook.sh:1057`).
  - The footer itself does not mutate state. It supports the blocked-exit transition where the hook returns JSON with `"decision": "block"` and the next prompt as the reason (`hooks/loop-codex-stop-hook.sh:1113`).
  - It is not used for the separate Finalize Phase transition. Finalize Phase uses `prompt-template/claude/finalize-phase-prompt.md` after Codex emits `COMPLETE` and the hook renames `state.md` to `finalized-state.md` (`hooks/loop-codex-stop-hook.sh:961`, `hooks/loop-codex-stop-hook.sh:979`, `prompt-template/claude/finalize-phase-prompt.md:1`).

- gates_or_invariants:
  The file encodes prompt-level invariants:
  - Do not exit by falsifying completion or editing loop state (`prompt-template/claude/next-round-footer.md:4`).
  - Do not self-cancel through `cancel-rlcr-loop` (`prompt-template/claude/next-round-footer.md:4`).
  - If the `code-simplifier` plugin is installed, run it before exiting the next round (`prompt-template/claude/next-round-footer.md:7`).
  - Commit changes and write the work summary to the exact next summary file (`prompt-template/claude/next-round-footer.md:8`, `prompt-template/claude/next-round-footer.md:9`).
  
  These are soft prompt instructions. Hard enforcement is in validators and the stop hook: state/finalized-state writes are blocked by write/edit/bash validators, dirty git blocks exit, missing summary blocks exit, and unauthorized cancel commands are rejected by `is_cancel_authorized`.

- dependencies_and_callers:
  The sole observed direct caller is `hooks/loop-codex-stop-hook.sh`, which renders the footer via `load_and_render_safe "$TEMPLATE_DIR" "claude/next-round-footer.md"` with `NEXT_SUMMARY_FILE=$NEXT_SUMMARY_FILE` (`hooks/loop-codex-stop-hook.sh:1089`, `hooks/loop-codex-stop-hook.sh:1091`). It depends on `hooks/lib/template-loader.sh` for loading/rendering and on `hooks/lib/loop-common.sh` for template directory setup.
  
  Sibling coordination:
  - The footer is appended after `claude/next-round-prompt.md` and optional `claude/post-alignment-action-items.md` (`hooks/loop-codex-stop-hook.sh:1075`, `hooks/loop-codex-stop-hook.sh:1081`).
  - It is followed by optional `claude/push-every-round-note.md` and `claude/goal-tracker-update-request.md` (`hooks/loop-codex-stop-hook.sh:1095`, `hooks/loop-codex-stop-hook.sh:1104`).
  - The final-code-simplifier branch’s stronger post-`COMPLETE` path is handled by `claude/finalize-phase-prompt.md`, which explicitly instructs `code-simplifier:code-simplifier` after Codex review passes (`prompt-template/claude/finalize-phase-prompt.md:5`, `prompt-template/claude/finalize-phase-prompt.md:9`).

- edge_cases_or_failure_modes:
  - If this template is missing, the stop hook fallback still tells the agent to commit and write the summary, but the fallback does not include the code-simplifier instruction or the explicit “do not lie/edit state/cancel” warning (`hooks/loop-codex-stop-hook.sh:1089`).
  - The code-simplifier instruction is conditional on the plugin being installed and is not enforced by this template. The stop hook enforces clean git and summary presence, not successful simplifier invocation.
  - Because this footer is appended on continuing rounds, not only Finalize Phase, it can encourage code-simplifier use before every blocked-exit retry. The dedicated final simplifier gate/prompt is separate and only appears after Codex emits `COMPLETE`.

- validation_or_tests:
  `tests/test-template-references.sh` scans `hooks/loop-codex-stop-hook.sh` and validates referenced templates exist (`tests/test-template-references.sh:56`, `tests/test-template-references.sh:93`, `tests/test-template-references.sh:102`). The hook reference to this exact footer is visible at `hooks/loop-codex-stop-hook.sh:1091`. I did not execute tests in this read-only research pass.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen:
  - `ADD_A_FINAL_CODE_SIMPLIFIER_AFTER_CODEX_COMPLETE-HZ-009`
  - `ADD_A_FINAL_CODE_SIMPLIFIER_AFTER_CODEX_COMPLETE-HZ-039`
  - `ADD_A_FINAL_CODE_SIMPLIFIER_AFTER_CODEX_COMPLETE-HZ-069`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`