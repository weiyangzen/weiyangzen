# agent_23 add-careful-mode-v1.6.5 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `a12de5d9f36bb10cd62955881f4e76d67d3f50ce`
- notes: Read-only evidence pass. I inspected each assigned file directly and followed only targeted references needed to understand hook/template/test integration.

## Item Evidence

### ADD_CAREFUL_MODE_V1_6_5-HZ-023 `file` `hooks/check-todos-from-transcript.py`
- cursor: `[_]`
- core_role: Stop-hook preflight validator for unfinished Claude work. It prevents RLCR/finalize exit before all todo/task state is complete, and is invoked by `hooks/loop-codex-stop-hook.sh` before git checks or Codex review at lines 340-395.
- algorithmic_behavior: Reads hook JSON from stdin, aggregates incomplete work from two sources, prints `INCOMPLETE_TODOS` plus formatted items, and exits nonzero when unfinished work remains. Legacy `TodoWrite` state is reconstructed from the latest TodoWrite call in transcript JSONL, via `extract_tool_calls_from_entry()` and `find_incomplete_todos_from_transcript()` at lines 23-106. New Task state is not reconstructed from transcript; `find_incomplete_tasks_from_directory()` treats `~/.claude/tasks/<session_id>/*.json` as authoritative at lines 109-145.
- inputs_outputs_state: Inputs are stdin hook JSON with optional `session_id` and `transcript_path` at lines 148-172. Outputs are exit `0` for no work, exit `1` for incomplete work, exit `2` for malformed hook JSON, as documented at lines 9-13 and implemented at lines 174-193. It reads transcript/task files but does not write persistent state.
- gates_or_invariants: Todo status must equal exactly `completed` to pass; any other status, including missing/empty status, is incomplete at lines 96-104. Task status must be `completed` or `deleted` to pass; all other task statuses are incomplete at lines 128-140. Malformed JSONL transcript lines and malformed task files are skipped rather than fatal at lines 81-84 and 141-143.
- dependencies_and_callers: Depends only on Python stdlib `json`, `sys`, `pathlib`, and typing imports at lines 17-20. Main caller is `loop-codex-stop-hook.sh`, which blocks exit and renders `block/incomplete-todos.md` when this script exits `1` at lines 347-384. `tests/test-finalize-phase.sh` exercises the integration with legacy TodoWrite transcript at lines 715-740.
- edge_cases_or_failure_modes: Empty stdin allows exit at lines 151-154. Missing transcript path or nonexistent transcript file allows exit at lines 69-70 and 169-172. Because current code only recognizes `TodoWrite` transcript calls at line 89, historical tests in `tests/test-todo-checker.sh` that expect transcript-level `TaskCreate`/`TaskUpdate` support at lines 297-438 appear stale relative to this implementation. If `session_id` is absent, authoritative task-directory state is not checked.
- validation_or_tests: `tests/test-todo-checker.sh` covers invalid stdin, empty input, nonexistent transcript, legacy todo states, multiple TodoWrite calls, alternate transcript shapes, missing status, and empty content at lines 52-294. However, its TaskCreate/TaskUpdate transcript tests at lines 297-438 no longer match the implementation’s task-directory design. `tests/test-finalize-phase.sh` verifies incomplete todos block finalize completion and Codex is not invoked at lines 699-740.
- skip_candidate: `no`

### ADD_CAREFUL_MODE_V1_6_5-HZ-053 `file` `tests/test-finalize-phase.sh`
- cursor: `[_]`
- core_role: Executable specification for the RLCR Finalize Phase state machine. It defines the required behavior around entering finalize after Codex COMPLETE, protecting finalize state, completing the loop, and preserving normal round behavior.
- algorithmic_behavior: Builds an isolated git repo and mock `codex`, creates `.humanize/rlcr/<timestamp>` state, then drives real hooks and validators. Setup helpers create state frontmatter with `current_round`, `max_iterations`, Codex config, `push_every_round`, plan fields, and `review_started` at lines 180-205. The test explicitly models transitions among `state.md`, `finalize-state.md`, `complete-state.md`, and `maxiter-state.md`.
- inputs_outputs_state: Inputs are mocked hook JSON payloads, mock Codex outputs, transcript JSONL, git cleanliness, and loop state files. Outputs are pass/fail counters and hook/validator exit behavior. State transitions asserted include `state.md -> finalize-state.md` after COMPLETE at lines 524-539, `finalize-state.md -> complete-state.md` when all finalize gates pass at lines 476-496, and `state.md -> maxiter-state.md` at max iteration at lines 542-560.
- gates_or_invariants: `finalize-state.md` is an active loop but `complete-state.md` is not, tested at lines 282-320. `finalize-state.md` must not be modified through Write/Edit/Bash or copied/moved as a Bash source, tested at lines 345-415. Finalize completion requires `finalize-summary.md`, clean git status, and complete todos before exit, tested at lines 429-483 and 699-740. Finalize phase must not invoke Codex, tested at lines 446-452 and 498-504.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at line 49 and uses `find_active_loop`, `is_finalize_state_file_path`, `is_finalize_summary_path`, `parse_state_file`, and validator hooks. It directly invokes `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-bash-validator.sh`, `hooks/loop-read-validator.sh`, `hooks/loop-plan-file-validator.sh`, and `hooks/loop-codex-stop-hook.sh`.
- edge_cases_or_failure_modes: Review failures and empty review stdout must block instead of entering finalize, preserving `state.md` with `review_started: true`, tested at lines 562-619 and 621-696. Normal non-COMPLETE review feedback must keep `state.md`, increment `current_round`, write `round-N-review-result.md`, and include feedback in the block output at lines 743-814. Validators must parse `finalize-state.md` as the active state file at lines 816-865.
- validation_or_tests: This file is itself the validation suite and ends with `exit $TESTS_FAILED` at lines 867-876. It also documents its positive and negative case matrix at lines 5-19, making it a high-value behavioral spec for the finalize algorithm.
- skip_candidate: `no`

### ADD_CAREFUL_MODE_V1_6_5-HZ-083 `file` `prompt-template/block/git-push.md`
- cursor: `[_]`
- core_role: User-facing block template for the RLCR “local commits by default” push gate.
- algorithmic_behavior: Provides the message emitted when a Bash command attempts `git push` while `push_every_round` is not enabled. The hook loads it through `load_and_render_safe "$TEMPLATE_DIR" "block/git-push.md"` in `hooks/loop-bash-validator.sh` at lines 96-104.
- inputs_outputs_state: Input is implicit loop state parsed by the Bash validator, specifically `STATE_PUSH_EVERY_ROUND` from active `state.md` or `finalize-state.md` at `loop-bash-validator.sh` lines 74-96. Output is stderr block text from this template and validator exit `2`; no repository state is changed.
- gates_or_invariants: The invariant is that remote push is disallowed unless the loop was started with `--push-every-round`. The template states that commits stay local and names `/humanize:start-rlcr-loop plan.md --push-every-round` as the opt-in path at lines 3-9.
- dependencies_and_callers: Depends on the shared template loader behavior in `hooks/lib/template-loader.sh`, especially `load_and_render_safe()` fallback semantics at lines 167-203. `tests/test-template-loader.sh` verifies `block/git-push.md` loads and safe rendering prefers the real template over fallback at lines 55-65 and 210-222.
- edge_cases_or_failure_modes: If the template is missing or empty, `loop-bash-validator.sh` has an inline fallback at lines 99-103, so the gate still blocks. Command matching is limited to commands whose lowercase text starts with `git push` in `loop-bash-validator.sh` line 98; wrapped push commands may depend on other Bash command detection logic outside this specific template.
- validation_or_tests: `tests/test-template-loader.sh` directly validates loading this template at lines 59-64 and fallback bypass at lines 216-221. `tests/test-templates-comprehensive.sh` also references the “Git Push Blocked” content around lines 459-462.
- skip_candidate: `no`

### ADD_CAREFUL_MODE_V1_6_5-HZ-113 `file` `prompt-template/claude/post-alignment-action-items.md`
- cursor: `[_]`
- core_role: Prompt-injection fragment for rounds immediately following a Full Goal Alignment Check. It nudges the implementation agent toward alignment gaps surfaced by Codex.
- algorithmic_behavior: Static Markdown section with three prioritized categories: forgotten items, unmet acceptance criteria, and unjustified deferrals at lines 2-7. `hooks/loop-codex-stop-hook.sh` appends it to the next-round prompt only when `FULL_ALIGNMENT_CHECK == true` at lines 1566-1572.
- inputs_outputs_state: Input is the derived `FULL_ALIGNMENT_CHECK` boolean in the stop hook. Output is appended text in `round-${NEXT_ROUND}-prompt.md`; it does not alter state files or hook decisions by itself.
- gates_or_invariants: It is not a hard validator. Its algorithmic contract is advisory but state-machine relevant: after a full alignment review, the next round must focus on gaps in goal coverage, AC status, and deferral legitimacy instead of treating review feedback as ordinary code review only.
- dependencies_and_callers: Called only through `load_template "$TEMPLATE_DIR" "claude/post-alignment-action-items.md"` in `loop-codex-stop-hook.sh` at line 1568. Related review templates define the upstream concepts: `prompt-template/codex/full-alignment-review.md` includes “Forgotten Items Detection” and “Deferred Items Audit”; regular review also mentions forgotten/deferred items.
- edge_cases_or_failure_modes: If the template is missing, the hook silently skips appending because it checks `[[ -n "$POST_ALIGNMENT" ]]` before writing at lines 1568-1571. There is no fallback for this fragment, unlike block templates, so missing content degrades alignment guidance without blocking the loop.
- validation_or_tests: Covered indirectly by template reference/comprehensive suites, and `rg` shows its only concrete hook caller is `loop-codex-stop-hook.sh` lines 1566-1572. No assigned test directly asserts its content appears in generated next-round prompts.
- skip_candidate: `no`

### ADD_CAREFUL_MODE_V1_6_5-HZ-143 `file` `tests/robustness/test-template-error-robustness.sh`
- cursor: `[_]`
- core_role: Robustness specification for the shared prompt-template rendering subsystem used by hooks, block messages, and next-round prompt construction.
- algorithmic_behavior: Sources `hooks/lib/template-loader.sh` and `tests/test-helpers.sh` at lines 15-18, creates a temp test directory, and verifies `load_and_render_safe()` and `render_template()` under malformed input, missing files, odd variable names, filesystem anomalies, and concurrency. It is explicitly about template error handling per lines 3-10.
- inputs_outputs_state: Inputs are generated temporary template files and inline template strings. Outputs are pass/fail assertions through shared test helpers and final `print_test_summary` at lines 337-341. It writes only into the test temp directory.
- gates_or_invariants: Missing template files/directories must use fallback at lines 34-51. Malformed placeholders must not crash and should return non-empty output at lines 73-115. Variable values containing `{{OTHER}}` must not recursively expand at lines 165-173, matching `render_template()`’s single-pass invariant in `hooks/lib/template-loader.sh` lines 50-57 and 71-129.
- dependencies_and_callers: Depends directly on `load_template`, `render_template`, and `load_and_render_safe` from `hooks/lib/template-loader.sh`. That loader is sourced globally by `hooks/lib/loop-common.sh` at lines 140-149, so failures here would affect validators, block templates, finalize prompts, and review prompts.
- edge_cases_or_failure_modes: Covers empty templates at lines 53-63, whitespace-only templates at lines 220-226, UTF-8 BOM at lines 208-218, filenames with spaces at lines 228-243, permission-denied behavior at lines 245-260, concurrent reads at lines 270-299, subdirectory templates at lines 309-318, and symlinked templates at lines 320-334. Some cases intentionally accept multiple safe outcomes, e.g. empty template may return empty or fallback, and permission behavior may vary by system.
- validation_or_tests: This file is the validation artifact. It complements `tests/test-template-loader.sh`, which checks normal loader behavior including real `block/git-push.md` loading at lines 55-65 and safe fallback behavior at lines 210-222.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `5/5 item evidence headings present; IDs intentionally not repeated here to preserve the exactly-once output constraint`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`