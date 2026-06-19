# agent_16 impl-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 4
- source_commit: `96455ba5aff935988d78439ca55427c603b1adcd`

## Item Evidence

### IMPL_PR_LOOP-HZ-016 `file` `agents/draft-relevance-checker.md`
- cursor: `[_]`
- core_role: Specialized Claude agent prompt used by `commands/gen-plan.md` to decide whether a user draft belongs to the current repository before plan generation proceeds. Frontmatter defines `name: draft-relevance-checker`, `model: haiku`, and read-only discovery tools `Read, Glob, Grep` at `agents/draft-relevance-checker.md:1-6`.
- algorithmic_behavior: The agent performs a three-step relevance classification: inspect repo docs/structure/technology, compare draft content against repo concepts/files/features, then emit exactly `RELEVANT: <brief explanation>` or `NOT_RELEVANT: <brief explanation>` at `agents/draft-relevance-checker.md:12-30`. The policy is intentionally lenient and semantic, with “if in doubt” bias toward relevance at `agents/draft-relevance-checker.md:31-36`.
- inputs_outputs_state: Input is draft document content supplied by the parent `gen-plan` command. Output is a single verdict string consumed by the command gate. It maintains no persistent state; repository state is observed through read/glob/grep only.
- gates_or_invariants: The downstream gate in `commands/gen-plan.md` stops Phase 2 if the verdict is `NOT_RELEVANT` and continues only for `RELEVANT` at `commands/gen-plan.md:49-72`. The invariant is conservative admission: only drafts with no reasonable repository connection should be rejected.
- dependencies_and_callers: Called through the Task tool by `commands/gen-plan.md:55-64`. Structural tests assert the file exists, has the expected name/model/tools, valid frontmatter, valid model, naming convention, and English-only content in `tests/test-gen-plan.sh:111-155`, `tests/test-gen-plan.sh:241-292`, and `tests/test-gen-plan.sh:391-421`.
- edge_cases_or_failure_modes: Informal or multilingual drafts are allowed by policy, so false positives are preferred over false negatives. A malformed output that does not start with the required verdict token would make the parent command’s string gate ambiguous. Because the model is `haiku`, the prompt explicitly asks for quick exploration, which trades depth for low-latency triage.
- validation_or_tests: `tests/test-gen-plan.sh` validates agent metadata and content constraints; it does not execute semantic relevance scenarios. Parent workflow behavior is specified in `commands/gen-plan.md`.
- skip_candidate: `no`

### IMPL_PR_LOOP-HZ-046 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role: Executable specification for the RLCR hook allowlist that permits only a tiny set of generated loop files through otherwise strict Read/Write/Edit/Bash protections. The test declares scope at `tests/test-allowlist-validators.sh:3-10` and sources production helpers from `hooks/lib/loop-common.sh` at `tests/test-allowlist-validators.sh:15-17`.
- algorithmic_behavior: The test creates an isolated git repo and active loop directory with `state.md`, then verifies `is_allowlisted_file()` and four validators. The allowlist itself is exact path equality for `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` under the active loop dir in `hooks/lib/loop-common.sh:324-345`.
- inputs_outputs_state: Inputs are synthetic hook JSON payloads for `Write`, `Edit`, `Read`, and `Bash`, plus `CLAUDE_PROJECT_DIR` pointing at the temp repo. Outputs are process exit codes and stderr text: allow returns exit `0`; policy block returns exit `2`. Test state lives in a temp dir removed by trap at `tests/test-allowlist-validators.sh:29-31`.
- gates_or_invariants: Critical invariant is active-loop path binding, not basename matching. Unit cases allow only the four exact active-loop files at `tests/test-allowlist-validators.sh:70-124`; validator cases block non-allowlisted rounds at `tests/test-allowlist-validators.sh:159-183`, `215-226`, and `258-281`. Bash tests additionally require full active-loop path and reject wrong dir, generic relative filename, old loop dir, and same timestamp under another root at `tests/test-allowlist-validators.sh:314-381`.
- dependencies_and_callers: Exercises `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-read-validator.sh`, and `hooks/loop-bash-validator.sh`. These validators detect active loops with `find_active_loop()` from `hooks/lib/loop-common.sh:147-170`; Read/Write also validate JSON and nested depth before policy checks in `hooks/lib/loop-common.sh:55-129`.
- edge_cases_or_failure_modes: Path comparison is literal for direct tool validators, so path normalization/symlink variants are outside this test. Bash allowlist uses lowercased command text and escaped active-loop path matching, which protects against same-basename and different-root bypasses but still depends on command pattern detection via `command_modifies_file`. The test uses `set -uo pipefail`, not global `set -e`, so each assertion captures failures without aborting early.
- validation_or_tests: Included in the aggregate suite list at `tests/run-all-tests.sh:32-45`. The script exits with `TESTS_FAILED`, making it a direct CI-style contract at `tests/test-allowlist-validators.sh:383-391`.
- skip_candidate: `no`

### IMPL_PR_LOOP-HZ-076 `file` `prompt-template/block/force-push-detected.md`
- cursor: `[_]`
- core_role: Blocking prompt template for PR-loop force-push recovery. It explains that commit history changed non-fast-forward and that review state must be restarted with a fresh trigger comment.
- algorithmic_behavior: The template renders `{{OLD_COMMIT}}`, `{{NEW_COMMIT}}`, and `{{BOT_MENTION_STRING}}` into a human-facing block at `prompt-template/block/force-push-detected.md:1-17`. It is selected when `hooks/pr-loop-stop-hook.sh` detects that the stored `latest_commit_sha` is no longer an ancestor of current `HEAD`.
- inputs_outputs_state: Inputs are template variables from `pr-loop-stop-hook`: old SHA, new SHA, bot mention string, and PR number at `hooks/pr-loop-stop-hook.sh:412-417`. Output is a rendered Markdown reason embedded in a JSON block decision with system message “PR Loop: Force push detected - please re-trigger bots” at `hooks/pr-loop-stop-hook.sh:419-421`. State is also updated before rendering: `latest_commit_sha`, `latest_commit_at`, `last_trigger_at`, and `trigger_comment_id` are rewritten/cleared at `hooks/pr-loop-stop-hook.sh:396-410`.
- gates_or_invariants: The gate triggers only when current `HEAD` differs from stored SHA and `git merge-base --is-ancestor` reports the stored SHA is not reachable from current `HEAD` at `hooks/pr-loop-stop-hook.sh:370-380`. Clearing trigger fields prevents old comments from satisfying the next review cycle.
- dependencies_and_callers: Rendered through `load_and_render_safe`, whose template loader performs single-pass `{{VAR}}` substitution and falls back if the template is absent at `hooks/lib/template-loader.sh:50-57` and `hooks/lib/template-loader.sh:167-203`. Force-push detection also depends on `git rev-parse`, `git merge-base`, and `gh pr view --json commits` timestamp lookup at `hooks/pr-loop-stop-hook.sh:371-389`.
- edge_cases_or_failure_modes: If GitHub timestamp lookup fails, the hook falls back to current UTC time at `hooks/pr-loop-stop-hook.sh:391-394`, which preserves safety but may reject some nearby comments. If the old commit is still ancestor, this template is not used; normal fast-forward progress continues. If the template is missing, the fallback still blocks and asks for a new bot trigger.
- validation_or_tests: `tests/test-pr-loop-stophook.sh` simulates a history rewrite by mocking `git merge-base` to fail and asserts force-push/re-trigger text appears at `tests/test-pr-loop-stophook.sh:538-640`.
- skip_candidate: `no`

### IMPL_PR_LOOP-HZ-106 `file` `prompt-template/claude/goal-tracker-update-request.md`
- cursor: `[_]`
- core_role: Claude prompt fragment appended to later RLCR rounds to route goal-tracker changes through a structured request section rather than direct mutation.
- algorithmic_behavior: The template tells Claude to include a `## Goal Tracker Update Request` section only when needed, with requested changes and justification at `prompt-template/claude/goal-tracker-update-request.md:2-14`. It changes the state transition from direct goal-tracker editing to reviewable change request.
- inputs_outputs_state: Input is the current round prompt context built by `hooks/loop-codex-stop-hook.sh`; output is additional Markdown appended to `NEXT_PROMPT_FILE` at `hooks/loop-codex-stop-hook.sh:1108-1113`. The produced request can mention completion evidence, open issues, plan evolution, or deferrals, but it does not update the tracker by itself.
- gates_or_invariants: The invariant is that post-round goal tracker changes are mediated. Bash validator blocks shell modifications to `goal-tracker.md`; in round `0` it points to direct tool usage, while later rounds it instructs changes to be requested in the summary at `hooks/loop-bash-validator.sh:343-358`. The template supplies the expected request format for that later-round path.
- dependencies_and_callers: Loaded via `load_template`; if missing, the stop hook appends a fallback sentence at `hooks/loop-codex-stop-hook.sh:1108-1112`. Goal tracker update mechanics live separately in `update_pr_goal_tracker()`, which idempotently updates summary rows, totals, and issue log entries for PR-loop analysis at `hooks/lib/loop-common.sh:1055-1219`.
- edge_cases_or_failure_modes: Because the section is conditional, Claude may omit it when changes are actually needed. The template relies on Codex review to accept/reject the request, so stale tracker state can persist until the next Codex/hook reconciliation. It is a prompt contract, not a parser-enforced schema.
- validation_or_tests: No test directly asserts this template text. Related coverage verifies goal-tracker parsing/update behavior and that mixed approvals do not incorrectly count issues as resolved in `tests/test-pr-loop-stophook.sh:1682-1735`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `4 item sections above; one heading per assigned row`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`