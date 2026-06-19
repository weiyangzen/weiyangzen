# agent_12 add-commit-plan-file-cli 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `20b3ebae90ba6b39c335a1dbdec89affc90c386e`

## Item Evidence

### ADD_COMMIT_PLAN_FILE_CLI-HZ-012 `file` `commands/cancel-rlcr-loop.md`
- cursor: `[_]`
- core_role:
  - Slash-command workflow definition for explicitly cancelling the active RLCR loop. It is part of the loop state machine because active/inactive status is represented by the presence or absence of `.humanize-loop.local/<timestamp>/state.md`.
  - The command frontmatter declares only narrow tools: list loop dirs, move `state.md` to `cancel-state.md`, read `state.md`, and `Read` ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:1)).
- algorithmic_behavior:
  - Selects the current loop directory as the lexicographically newest timestamp directory under `.humanize-loop.local/` using `ls -1d ... | sort -r | head -1` ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:11)).
  - Treats no directory as no active loop and reports that directly ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:18)).
  - Checks activeness by testing for `${LOOP_DIR}state.md`; a newest directory without `state.md` is considered inactive even if it contains preserved exit-state files ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:20)).
  - On active state, it reads the state file for current round and max iterations, then renames `state.md` to `cancel-state.md` ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:28)).
  - This mirrors the shared loop invariant in `find_active_loop`, which also only considers the newest directory active if `state.md` exists ([hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/lib/loop-common.sh:23)).
- inputs_outputs_state:
  - Inputs: `.humanize-loop.local/*/` directory names; the selected newest loop’s `state.md`; state frontmatter fields such as `current_round` and `max_iterations`, which are created by setup ([scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/scripts/setup-rlcr-loop.sh:406)).
  - Output on no loop dir: user-facing message `No active RLCR loop found.` ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:18)).
  - Output on newest dir without active state: user-facing message noting the loop directory exists but has no `state.md` ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:26)).
  - State transition on success: `.humanize-loop.local/<newest>/state.md` -> `.humanize-loop.local/<newest>/cancel-state.md` ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:30)).
  - Preserves all loop artifacts: summaries, reviews, goal tracker, plan backup, and renamed state remain in the loop directory ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:35)).
- gates_or_invariants:
  - Current loop is always newest timestamp, not any older directory with a `state.md` ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:33)).
  - A loop is active only if `state.md` exists in that current loop directory ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:33)).
  - Cancellation is non-destructive: it renames state rather than removing the directory or artifacts.
  - The command is intentionally hidden from slash-command tooling, but still callable by name when instructed ([commands/cancel-rlcr-loop.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/commands/cancel-rlcr-loop.md:4)).
  - The loop’s initial prompt tells the worker not to execute `cancel-rlcr-loop` to escape review, so this command is meant as a user/operator escape hatch rather than normal worker control flow ([scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/scripts/setup-rlcr-loop.sh:565)).
- dependencies_and_callers:
  - Paired with `/humanize:start-rlcr-loop`, whose setup script creates `.humanize-loop.local/<timestamp>/state.md` and prints the cancellation command as the operator stop path ([scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/scripts/setup-rlcr-loop.sh:603)).
  - Uses the same active-loop definition documented in README: loop state is controlled solely by `state.md` in the newest timestamp directory; cancel renames it to `cancel-state.md` ([README.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/README.md:116)).
  - Consumed indirectly by hooks because the stop hook exits early when `find_active_loop` returns empty; after cancellation, no active `state.md` remains, so the stop hook allows exit ([hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/loop-codex-stop-hook.sh:52)).
  - Related shared helper `end_loop` has a formal `cancel` reason, but this command implements cancellation directly with `mv` rather than calling that helper ([hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/lib/loop-common.sh:199)).
- edge_cases_or_failure_modes:
  - If multiple timestamp directories exist, older active-looking loops are ignored by design; only the newest directory is considered current.
  - If the newest directory lacks `state.md`, the command reports no active loop even if an older directory has `state.md`. This matches `find_active_loop` and prevents old loops from being revived.
  - If `cancel-state.md` already exists in the newest directory, the documented `mv` may overwrite or fail depending shell `mv` behavior and permissions; the command does not define a collision policy.
  - The report requires round `N` of `M`, but the markdown does not specify robust parsing for malformed or missing `current_round`/`max_iterations`.
  - Directory selection depends on sortable timestamp names. Setup uses `YYYY-MM-DD_HH-MM-SS`, which supports the lexicographic newest rule ([scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/scripts/setup-rlcr-loop.sh:391)).
- validation_or_tests:
  - `tests/test-state-exit-naming.sh` validates that `cancel-state.md` is not detected as active after `state.md` is absent ([tests/test-state-exit-naming.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/tests/test-state-exit-naming.sh:93)).
  - The same test suite validates that only `state.md` indicates activity and that the newest directory with `state.md` takes precedence ([tests/test-state-exit-naming.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/tests/test-state-exit-naming.sh:38)).
  - README documents the exact manual equivalent command, providing an operator-level contract for cancellation behavior ([README.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/README.md:120)).
  - I did not run tests; this branch export is read-only and this task is research-only.
- skip_candidate: `no`

### ADD_COMMIT_PLAN_FILE_CLI-HZ-042 `file` `prompt-template/block/incomplete-todos.md`
- cursor: `[_]`
- core_role:
  - Stop-hook block template used when Claude attempts to stop an active RLCR loop while the latest TodoWrite state still contains unfinished tasks.
  - It is a control-gate prompt, not executable code, but it defines a required algorithmic transition: block exit before Codex review until all todos are complete ([prompt-template/block/incomplete-todos.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/prompt-template/block/incomplete-todos.md:1)).
- algorithmic_behavior:
  - Presents the incomplete todo list through `{{INCOMPLETE_LIST}}` ([prompt-template/block/incomplete-todos.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/prompt-template/block/incomplete-todos.md:5)).
  - Instructs the agent to complete all remaining todos, mark each with TodoWrite, and only then write a summary and stop ([prompt-template/block/incomplete-todos.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/prompt-template/block/incomplete-todos.md:7)).
  - Explicitly prevents entering Codex review while the work queue is incomplete ([prompt-template/block/incomplete-todos.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/prompt-template/block/incomplete-todos.md:12)).
  - The stop hook invokes this template after plan/branch integrity checks and before large-file checks or Codex review, making it an early cheap gate ([hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/loop-codex-stop-hook.sh:218)).
- inputs_outputs_state:
  - Input placeholder: `INCOMPLETE_LIST`, populated from the todo checker output after stripping the first marker line (`tail -n +2`) ([hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/loop-codex-stop-hook.sh:234)).
  - Upstream data source: Claude hook JSON containing `transcript_path`; the checker reads the transcript and finds the most recent `TodoWrite` call ([hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/check-todos-from-transcript.py:87)).
  - Output: a rendered markdown block assigned to `reason` in a Claude hook JSON response with `"decision": "block"` ([hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/loop-codex-stop-hook.sh:244)).
  - State transition: no file state changes directly; it prevents loop progression from “attempting stop” to “Codex review” until TodoWrite state has no incomplete entries.
- gates_or_invariants:
  - Gate condition: if `check-todos-from-transcript.py` exits `1`, incomplete todos exist and the stop hook blocks immediately ([hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/loop-codex-stop-hook.sh:231)).
  - Todo completeness invariant: every latest todo must have `status == "completed"`; any other status is treated as incomplete ([hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/check-todos-from-transcript.py:109)).
  - Native TodoWrite is the authoritative todo surface; file-based `round-*-todos.md` access is discouraged elsewhere in loop helpers ([hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/lib/loop-common.sh:86)).
  - Template rendering is single-pass, so placeholder-like text inside `INCOMPLETE_LIST` is emitted literally rather than recursively expanded ([hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/lib/template-loader.sh:39)).
- dependencies_and_callers:
  - Direct caller: `hooks/loop-codex-stop-hook.sh`, via `load_and_render_safe "$TEMPLATE_DIR" "block/incomplete-todos.md"` ([hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/loop-codex-stop-hook.sh:241)).
  - Data dependency: `hooks/check-todos-from-transcript.py`, which supports Claude assistant transcript format, alternate message format, and direct `tool_use` entries ([hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/check-todos-from-transcript.py:48)).
  - Rendering dependency: `hooks/lib/template-loader.sh`, especially `load_and_render_safe`, which falls back if the template is missing or renders empty ([hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/lib/template-loader.sh:152)).
  - Operational dependency: start-loop prompt requires creating todos for all discovered issues, so this stop template enforces that earlier instruction at exit time ([scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/scripts/setup-rlcr-loop.sh:540)).
- edge_cases_or_failure_modes:
  - If `transcript_path` is missing, invalid JSON is supplied, the transcript file does not exist, or no TodoWrite call exists, the checker exits `0`, so the template is not shown and the stop may proceed ([hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/check-todos-from-transcript.py:91)).
  - Only the most recent TodoWrite call matters; earlier incomplete todos are ignored if a later TodoWrite list omits or completes them.
  - Any non-`completed` status is incomplete, including `pending`, `in_progress`, misspellings, or unknown statuses.
  - If the checker script is absent, the stop hook skips this gate entirely because it only runs the checker when the file exists ([hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/loop-codex-stop-hook.sh:226)).
  - The template instructs “Do NOT proceed to Codex review,” but enforcement comes from the hook’s JSON block decision, not from the markdown text alone.
- validation_or_tests:
  - No focused test for this exact template file was found in the inspected search results.
  - Behavior is partially covered by the checker implementation contract: incomplete todos produce `INCOMPLETE_TODOS` plus formatted `- [status] content` lines and exit `1` ([hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/check-todos-from-transcript.py:117)).
  - The hook has an inline fallback message if this template is missing or empty, so runtime blocking can continue with degraded wording ([hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/add-commit-plan-file-cli/hooks/loop-codex-stop-hook.sh:236)).
  - I did not run tests; this branch export is read-only and this task is research-only.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `2/2 item sections present; each assigned item id appears once as a section heading`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`