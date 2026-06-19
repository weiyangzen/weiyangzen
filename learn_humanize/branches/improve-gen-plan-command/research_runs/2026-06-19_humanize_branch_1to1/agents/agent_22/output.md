# agent_22 improve-gen-plan-command 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 4
- source_commit: `934cf543d66046b72071d121b15583d5e3d6799e`

## Item Evidence

### IMPROVE_GEN_PLAN_COMMAND-HZ-022 `file` `hooks/check-todos-from-transcript.py`
- cursor: `[_]`
- core_role: Stop-hook preflight validator for RLCR/Codex loop exits. It reads the Claude Code transcript and blocks exit when the latest `TodoWrite` state still contains unfinished items, before the more expensive Codex review path runs.
- algorithmic_behavior: `find_latest_todos()` scans a JSONL transcript line by line, ignoring blank lines and malformed JSONL records, and keeps only the most recent non-empty `TodoWrite.input.todos` list across three transcript encodings: assistant message content blocks, alternative `type: message` content blocks, and direct `type: tool_use` records. See [check-todos-from-transcript.py](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/hooks/check-todos-from-transcript.py:20>) and format branches at lines 51, 65, and 78.
- inputs_outputs_state: Input is hook JSON on stdin with optional `transcript_path`; output is process exit code plus optional stdout/stderr. Exit `0` means no actionable todos or all latest todos have `status == "completed"`; exit `1` prints `INCOMPLETE_TODOS` and one line per unfinished todo; exit `2` prints `PARSE_ERROR` to stderr for invalid hook input JSON. Main flow is at [check-todos-from-transcript.py](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/hooks/check-todos-from-transcript.py:90>).
- gates_or_invariants: The only completion invariant is strict string equality to `completed`; missing, empty, `pending`, `in_progress`, or any other status is incomplete. Missing `transcript_path`, missing transcript file, empty transcript, or no `TodoWrite` entries are fail-open exit `0`. Malformed JSONL transcript lines are ignored rather than fatal.
- dependencies_and_callers: Called by [hooks/loop-codex-stop-hook.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/hooks/loop-codex-stop-hook.sh:261>). The caller turns exit `2` into a hook block with parse-error messaging and exit `1` into an incomplete-todos block rendered via `prompt-template/block/incomplete-todos.md`; see stop-hook lines 263-309.
- edge_cases_or_failure_modes: If the newest `TodoWrite` call has an empty `todos` array, the previous non-empty list remains authoritative because replacement only occurs when `todos` is truthy. Non-list `content` blocks are skipped. Transcript file read errors other than missing file are not caught. The checker does not validate todo schema beyond `status` and `content`.
- validation_or_tests: Covered by [tests/test-todo-checker.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/tests/test-todo-checker.sh:51>): invalid stdin, missing path, nonexistent transcript, all-complete, incomplete, in-progress, empty transcript, invalid JSONL lines, latest-call precedence, all three transcript formats, missing status, empty content, and Unicode content.
- skip_candidate: `no`

### IMPROVE_GEN_PLAN_COMMAND-HZ-052 `file` `tests/test-gen-plan.sh`
- cursor: `[_]`
- core_role: Executable specification for the `gen-plan` command surface, its supporting relevance agent, version metadata consistency, content restrictions, and IO validation script exit-code contract.
- algorithmic_behavior: The script initializes project paths from its own location, counts pass/fail totals, then runs positive structural tests PT-1 through PT-9 before negative/fixture tests and IO validator tests. See [tests/test-gen-plan.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/tests/test-gen-plan.sh:11>) for root resolution and lines 54-180 for positive command, agent, and version assertions.
- inputs_outputs_state: Input is the repository checkout plus temporary invalid fixtures under `mktemp -d`; output is colored PASS/FAIL lines and final exit `0` only when `TESTS_FAILED == 0`. The script mutates only temp fixture directories, with cleanup traps at lines 191-193 and 435-436.
- gates_or_invariants: Requires `commands/gen-plan.md` to exist; have non-empty `description`, `allowed-tools`, and `argument-hint`; requires `agents/draft-relevance-checker.md` with exact name `draft-relevance-checker`, exact model `haiku`, and `tools`; requires plugin, marketplace, and README versions to match. It also enforces lowercase hyphenated names, required frontmatter, simple YAML syntax, accepted model aliases or prefixes, and no CJK or emoji in the command and agent files.
- dependencies_and_callers: Directly exercises [commands/gen-plan.md](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/commands/gen-plan.md:1>), [agents/draft-relevance-checker.md](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/agents/draft-relevance-checker.md:1>), and [scripts/validate-gen-plan-io.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/scripts/validate-gen-plan-io.sh:1>). Included in the aggregate suite via [tests/run-all-tests.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/tests/run-all-tests.sh:51>).
- edge_cases_or_failure_modes: YAML syntax validation is heuristic, not a full YAML parser. It labels negative tests NT-1, NT-2, NT-3, and NT-6, with no NT-4/NT-5 section. The script expects GNU-compatible `grep -P`; if unavailable, the emoji/CJK checks can silently skip due to stderr redirection and branch behavior.
- validation_or_tests: IO validator assertions cover exit `6` for missing flag values, flag-as-value, unknown option, and help; exit `1` for missing input; exit `2` for empty input; exit `3` for missing output directory; exit `4` for existing output or output directory; and exit `0` for valid new output path. See [tests/test-gen-plan.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/tests/test-gen-plan.sh:431>) through line 539.
- skip_candidate: `no`

### IMPROVE_GEN_PLAN_COMMAND-HZ-082 `file` `prompt-template/block/git-status-failed.md`
- cursor: `[_]`
- core_role: Block-message template for the RLCR/Codex stop-hook git-status safety gate. It defines the user-facing reason when repository state cannot be verified.
- algorithmic_behavior: This template interpolates `{{GIT_STATUS_EXIT}}` into a concise failure explanation and enumerates possible causes: git lock contention, invalid repository state, or slow large-repo operations. See [git-status-failed.md](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/prompt-template/block/git-status-failed.md:1>).
- inputs_outputs_state: Input variable is `GIT_STATUS_EXIT`; output is rendered markdown used as the hook block reason. It does not perform computation itself, but is part of the transition from git-status failure to stop-hook block decision.
- gates_or_invariants: Supports fail-closed behavior: when `git status --porcelain` fails or times out, the loop cannot verify clean/dirty state and must block rather than continue. The gate is implemented at [hooks/loop-codex-stop-hook.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/hooks/loop-codex-stop-hook.sh:322>).
- dependencies_and_callers: Loaded via `load_and_render_safe "$TEMPLATE_DIR" "block/git-status-failed.md"` in [loop-codex-stop-hook.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/hooks/loop-codex-stop-hook.sh:335>). Fallback text exists in the caller for template-load failure.
- edge_cases_or_failure_modes: If the template is missing or render fails, the fallback message is less detailed than this file because it omits the cause list. The template assumes the caller supplies a numeric or meaningful exit-code string.
- validation_or_tests: No direct named assertion found for this exact template in the inspected test references. Its behavior is indirectly covered by stop-hook tests that exercise git-status failure paths and by template-loading infrastructure.
- skip_candidate: `no`

### IMPROVE_GEN_PLAN_COMMAND-HZ-112 `file` `prompt-template/codex/goal-tracker-update-section.md`
- cursor: `[_]`
- core_role: Codex review prompt section that assigns the reviewer responsibility for goal-tracker updates after Round 0, preserving the rule that Claude may request changes but cannot directly modify `goal-tracker.md`.
- algorithmic_behavior: The template tells Codex to inspect any “Goal Tracker Update Request” in Claude’s summary, evaluate whether it serves the Ultimate Goal, update `@{{GOAL_TRACKER_FILE}}` if approved, reject with explanation if not, and never modify the immutable Ultimate Goal/Acceptance Criteria section. See [goal-tracker-update-section.md](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/prompt-template/codex/goal-tracker-update-section.md:1>).
- inputs_outputs_state: Input variable is `GOAL_TRACKER_FILE`; output is rendered prompt text inserted into both regular review and full-alignment review prompts. State transition is review-mediated: requested changes may become tracker edits only after Codex approval.
- gates_or_invariants: Protects the immutable section, requires justification against the Ultimate Goal, and narrows permitted tracker updates to task moves, Plan Evolution Log entries, Open Issues entries, and strongly justified deferrals. Lines 5-11 define approve/reject behavior and immutable-section protection.
- dependencies_and_callers: Rendered in [hooks/loop-codex-stop-hook.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/hooks/loop-codex-stop-hook.sh:683>) and injected into full-alignment and regular review templates at lines 723-751. It coordinates with goal-tracker modification blockers in `prompt-template/block/goal-tracker-modification.md` and bash/write validators referenced by the hook library.
- edge_cases_or_failure_modes: The template is advisory prompt logic, so enforcement depends on Codex following it and separate write/bash validators blocking disallowed Claude edits. If Claude omits a request section, this prompt creates no update obligation. If the request targets immutable content, the reviewer must reject or avoid that part.
- validation_or_tests: Directly rendered in [tests/test-templates-comprehensive.sh](</Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command/tests/test-templates-comprehensive.sh:531>), which asserts the rendered output contains “Goal Tracker Update Requests” and the provided goal-tracker path.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: IMPROVE_GEN_PLAN_COMMAND-HZ-022, IMPROVE_GEN_PLAN_COMMAND-HZ-052, IMPROVE_GEN_PLAN_COMMAND-HZ-082, IMPROVE_GEN_PLAN_COMMAND-HZ-112
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`