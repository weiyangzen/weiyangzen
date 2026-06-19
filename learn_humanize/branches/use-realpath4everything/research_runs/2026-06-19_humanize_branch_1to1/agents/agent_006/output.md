# agent_006 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-006 `directory` `hooks`
- cursor: `[_]`
- core_role:
  - `hooks/` is a core RLCR hook system. It wires Claude/Codex hook events to validators and the stop-loop orchestration in [hooks/hooks.json](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/hooks.json:4).
  - The directory owns pre-tool authorization for `Read`, `Write`, `Edit`, and `Bash`; post-Bash session capture; user-prompt plan-file integrity checks; and the `Stop` state machine that runs Codex review, review-phase loops, finalize phase, and methodology-analysis termination.
  - The branch’s `use-realpath4everything` concern is concentrated in [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/project-root.sh:41), [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-read-validator.sh:311), [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-write-validator.sh:341), and cancel authorization in [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:1082). The key invariant is: canonicalize project/root/prefixes for stable comparison across symlinked path prefixes, but do not dereference the leaf when authorizing a user-supplied target path that a write/move/read will operate on.

- algorithmic_behavior:
  - Hook routing:
    - `hooks/hooks.json` maps `UserPromptSubmit` to `loop-plan-file-validator.sh`, `PreToolUse` to read/write/edit/bash validators, `PostToolUse` Bash to `loop-post-bash-hook.sh`, and `Stop` to `loop-codex-stop-hook.sh` with a 7200-second timeout at [hooks/hooks.json](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/hooks.json:4).
  - Project root and path canonicalization:
    - `resolve_project_root` chooses `CLAUDE_PROJECT_DIR`, then `git rev-parse --show-toplevel`, and intentionally never falls back to `pwd`, then passes the result through `canonicalize_path` at [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/project-root.sh:41).
    - `canonicalize_path` uses `realpath` for existing paths, falls back to canonicalizing the parent and reattaching the basename for not-yet-created paths, then Python `os.path.realpath`, then raw input at [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/project-root.sh:113).
    - `canonicalize_path_prefix` resolves only the parent directory and reattaches the original basename at [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/project-root.sh:72). Its comments explicitly explain the security distinction: leaf symlinks must not authorize operations on the symlink target.
  - Shared state and gate helpers:
    - `loop-common.sh` validates hook JSON, rejects null bytes and invalid UTF-8 when `iconv` exists, requires `tool_name`, and detects deeply nested JSON via `jq` path depth at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:91).
    - Active loop discovery is session-aware. Without a session filter it checks only the newest loop directory; with a session filter it scans newest-to-oldest for the caller’s session and treats the newest terminal state as a zombie-prevention stop at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:332).
    - `resolve_active_state_file` prioritizes `methodology-analysis-state.md`, then `finalize-state.md`, then `state.md` at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:268).
    - Strict state parsing requires YAML frontmatter, `current_round`, `max_iterations`, `review_started`, and `base_branch`, and validates numeric/boolean fields at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:533).
    - `upsert_state_fields` rewrites or appends YAML frontmatter fields before the closing separator and is used by stop-hook transitions and drift tracking at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:667).
  - Read validator:
    - `loop-read-validator.sh` blocks direct `round-*-todos.md` access except allowlisted active-loop files at [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-read-validator.sh:56).
    - During methodology analysis, it canonicalizes file and loop paths, blocks reads from project files, and only allows methodology artifacts inside the loop directory at [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-read-validator.sh:86).
    - It blocks stale round prompt/summary/contract reads, old-session `goal-tracker.md`, and wrong-directory round files. Final directory comparison uses `canonicalize_path_prefix` on both the requested path and active-loop expected path at [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-read-validator.sh:305).
  - Write validator:
    - `loop-write-validator.sh` blocks todos writes, prompt writes, all state-file writes, plan backup writes, and summary/contract writes outside `.humanize/rlcr` at [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-write-validator.sh:57).
    - In methodology analysis, only `methodology-analysis-report.md` and `methodology-analysis-done.md` are writable at [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-write-validator.sh:88).
    - It allows `finalize-summary.md` only in the active finalize loop at [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-write-validator.sh:213).
    - It enforces goal-tracker path equality and, after round 0, validates that the immutable section is unchanged by comparing extracted immutable sections at [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-write-validator.sh:243) and [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:951).
    - Final path authorization again uses parent-only canonicalization to handle symlinked prefixes without approving leaf symlink escapes at [hooks/loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-write-validator.sh:334).
  - Edit validator:
    - `loop-edit-validator.sh` mirrors write restrictions for `Edit`, including todos/prompt/state/plan backup restrictions and methodology-analysis limits at [hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-edit-validator.sh:40).
    - For goal-tracker edits after round 0, it requires `old_string` and `new_string`, previews the literal edit using Perl, then applies the immutable-section guard at [hooks/loop-edit-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-edit-validator.sh:204) and [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:968).
    - Unlike read/write, the final edit-validator round-file path check is lighter: it validates in-loop status and round number, but does not perform the same canonicalized full expected-path comparison for all non-goal-tracker summary/contract edits.
  - Bash validator:
    - `loop-bash-validator.sh` validates Bash command JSON, finds the active loop by session, then blocks methodology-analysis file mutation commands, git write commands, interpreters, script execution, build tools, sourcing, and output redirection at [hooks/loop-bash-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-bash-validator.sh:81).
    - It blocks direct execution of hook scripts such as `loop-codex-stop-hook.sh` and `rlcr-stop-gate.sh`, even through common wrappers like `env`, `command`, `timeout`, `nice`, `nohup`, `strace`, shell invocation, or source/dot forms at [hooks/loop-bash-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-bash-validator.sh:166).
    - It blocks `git push` unless `push_every_round` is true at [hooks/loop-bash-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-bash-validator.sh:210).
    - It blocks `git add` operations that target `.humanize` directly, force-add broad scopes, or add broad scopes when `.humanize` is not gitignored via `git_adds_humanize` at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:1280).
    - It blocks Bash modifications to state files, plan backups, goal tracker, prompt, summary, contract, and most todos files using `command_modifies_file` plus extra source-side `mv`/`cp` parsing at [hooks/loop-bash-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-bash-validator.sh:253).
    - The cancel exception is deliberately narrow: `is_cancel_authorized` requires a `.cancel-requested` signal, rejects command substitution/newlines/chaining/extra args, canonicalizes the loop dir, uses `canonicalize_path_prefix` for source and destination, requires source to be active state/finalize/methodology state and destination to be active-loop `cancel-state.md`, and rejects symlinked source files at [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-common.sh:1051).
  - Plan-file prompt validator:
    - `loop-plan-file-validator.sh` runs on `UserPromptSubmit`; it blocks prompt submission when state schema is outdated, the branch changed, a tracked plan is untracked/dirty, or an untracked loop plan becomes tracked at [hooks/loop-plan-file-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-plan-file-validator.sh:18).
    - Git operations use `run_with_timeout` with fail-closed JSON block responses for timeout or unexpected git errors at [hooks/loop-plan-file-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-plan-file-validator.sh:96).
  - Post-Bash session capture:
    - `loop-post-bash-hook.sh` patches `session_id` into state after setup. It reads `.humanize/.pending-session-id`, verifies the Bash command starts with the resolved setup script path, normalizes duplicate slashes, replaces only empty `session_id:`, and removes the signal file at [hooks/loop-post-bash-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-post-bash-hook.sh:37).
  - Todo/task checker:
    - `check-todos-from-transcript.py` reads hook input from stdin, checks authoritative Claude task JSON files under `~/.claude/tasks/<session_id>/` or a test override, and also parses legacy transcript `TodoWrite` calls at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/check-todos-from-transcript.py:123).
    - It treats lanes tagged `[queued]` as non-blocking, defaults untagged tasks to `blocking`, reports `INCOMPLETE_TODOS`, and exits 1 when blocking/mainline tasks remain at [hooks/check-todos-from-transcript.py](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/check-todos-from-transcript.py:24).
  - Background-task helpers:
    - `loop-bg-tasks.sh` derives a loop-start UTC timestamp from the loop directory name, extracts transcript paths, computes pending async task IDs from transcript launch/completion events, prunes dead tasks via `.output` file liveness and `lsof`, and drives stop-hook short-circuit/parked-loop behavior at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-bg-tasks.sh:65).
    - `handle_bg_task_short_circuit` handles ambiguous callers without `session_id`, foreign-session parked loops, pending same-session background work by writing `bg-pending.marker`, and same-session stale-marker cleanup only after a successful no-pending transcript parse at [hooks/lib/loop-bg-tasks.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/loop-bg-tasks.sh:311).
  - Stop hook:
    - `loop-codex-stop-hook.sh` is the main loop state machine. It resolves the active loop, applies background-task guards before other gates, detects normal/finalize/methodology phase, parses state, validates schema, validates branch consistency, validates plan-file integrity outside review phase, blocks incomplete tasks, caches `git status`, blocks tracked `.humanize`, blocks dirty git status, and optionally blocks unpushed commits at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-codex-stop-hook.sh:64).
    - It enforces summary presence, round contract presence when anti-drift state exists, optional BitLesson delta validation, round-0 goal-tracker initialization, and max-iteration termination at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-codex-stop-hook.sh:747).
    - Implementation review builds a Codex prompt, writes review prompt files, runs `codex exec` with nested hooks disabled when supported, captures command/stdout/stderr under cache, copies stdout to the expected review file if needed, requires non-empty review output, and reads the last non-empty line for `COMPLETE` or `STOP` at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-codex-stop-hook.sh:1028).
    - Anti-drift logic requires a `Mainline Progress Verdict`; `ADVANCED` resets stall counters, `STALLED`/`REGRESSED` increments them, two stalls set `replan_required`, and three stalls trigger `stop_for_mainline_drift` at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-codex-stop-hook.sh:1785).
    - On `COMPLETE`, implementation phase sets `review_started=true`, writes `.review-phase-started`, clears drift counters, and runs `codex review --base` using fixed `base_commit` when available at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-codex-stop-hook.sh:1848).
    - Review phase ignores summary-review `COMPLETE`; finalization depends on `codex review` producing no `[P0-9]` issue markers. Issues create next review prompt and increment round at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-codex-stop-hook.sh:1250).
    - Finalize phase skips Codex review, requires `finalize-summary.md`, then either enters methodology analysis or renames state to `complete-state.md` at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-codex-stop-hook.sh:943).
  - Methodology analysis:
    - `methodology-analysis.sh` inserts a final optional methodology phase before terminal state rename. It skips when privacy mode is true, renames active state to `methodology-analysis-state.md`, records `.methodology-exit-reason`, creates a placeholder done file, and blocks with a rendered prompt at [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/methodology-analysis.sh:38).
    - Completion requires non-empty `methodology-analysis-done.md`, non-empty `methodology-analysis-report.md`, a valid stored exit reason of `complete`, `stop`, or `maxiter`, then renames to the terminal state and removes the marker at [hooks/lib/methodology-analysis.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/methodology-analysis.sh:114).
  - Template loader:
    - `template-loader.sh` provides single-pass `{{VAR}}` rendering via environment-prefixed variables and awk, preventing substituted content from being rescanned as placeholders at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/template-loader.sh:56).
    - `load_and_render_safe` falls back to inline messages when template files are missing or render empty at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/template-loader.sh:188).

- inputs_outputs_state:
  - Inputs:
    - Hook stdin JSON with fields such as `tool_name`, `tool_input.file_path`, `tool_input.command`, `session_id`, and `transcript_path`.
    - Active loop state under `.humanize/rlcr/<timestamp>/`: `state.md`, `finalize-state.md`, or `methodology-analysis-state.md`; summaries; contracts; prompts; goal tracker; pending markers.
    - Git repository state, current branch, plan file status, dirty/unpushed status.
    - Claude task files and transcript JSONL for blocking incomplete task detection and background task liveness.
    - Config loaded via `scripts/lib/config-loader.sh`, timeout wrapper via `scripts/portable-timeout.sh`, BitLesson validator via `scripts/bitlesson-validate-delta.sh`, prompt templates under `prompt-template/`.
    - External tools: `jq`, `git`, `realpath`, `python3` fallback for path canonicalization, `perl` for edit previews, `codex`, optional `lsof`.
  - Outputs:
    - Hook exit codes: normal allow exits `0`; validators use `2` for user-blocked tool operations and `1` for hard malformed input in several pre-tool validators.
    - Claude hook JSON block objects with `decision`, `reason`, and often `systemMessage` for prompt/stop gates.
    - State transitions by rename: `state.md` to `finalize-state.md`, `methodology-analysis-state.md`, `complete-state.md`, `stop-state.md`, `maxiter-state.md`, `unexpected-state.md`, or authorized `cancel-state.md`.
    - Generated or updated loop artifacts: review prompts/results, next-round prompts, placeholder summary files, `.review-phase-started`, `bg-pending.marker`, `.methodology-exit-reason`, methodology report/done files.
    - Debug/audit cache under `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/<sanitized-project>/<loop-ts>/`.
  - State transitions:
    - No active loop -> allow exit/tool use.
    - Normal implementation -> block until clean git, complete tasks, summary/contract, then Codex summary review.
    - Review output issues -> increment `current_round`, update drift fields, write next prompt/summary scaffold, block with instructions.
    - Review output `COMPLETE` -> set `review_started=true`, create marker, run `codex review`; no review issues -> finalize phase.
    - Finalize phase -> require finalize summary, then methodology analysis or terminal complete.
    - Methodology phase -> require non-empty done/report and valid exit reason, then terminal state.
    - Background work pending -> stop hook exits naturally but parks loop with `bg-pending.marker`.

- gates_or_invariants:
  - Project root resolution must be stable across `cd`: `pwd` is deliberately excluded as a fallback in [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/lib/project-root.sh:10).
  - Both sides of path comparisons must be canonicalized. Full realpath is appropriate for project root and trusted existing paths; `canonicalize_path_prefix` is required for user-supplied file targets where a leaf symlink must not authorize operating on the symlink target.
  - Active-loop selection is session-scoped; validators do not adopt foreign `bg-pending.marker` loops, while the stop hook opts into marker fallback to report or resume parked loops.
  - State parsing fails closed in validators and stop-hook schema gates; malformed or missing critical state fields block or terminate unexpectedly rather than silently defaulting.
  - State files, finalize state, methodology state, prompts, plan backups, and `.humanize` runtime state are hook-managed and protected from user tool writes.
  - Goal tracker immutable section can be initialized in round 0, but after round 0 only mutable updates pass.
  - Bash mutation is not trusted as an editing path for protected RLCR files; Write/Edit are required so validators can inspect target and content.
  - Stop-hook progress requires clean git state and committed work before Codex review. `push_every_round=true` adds remote push cleanliness as a gate.
  - Review phase cannot be manually toggled by editing state: `.review-phase-started` must exist when `review_started=true`.
  - Background-task marker cleanup is fail-closed: marker removal requires a readable/parseable transcript and an empty pending-task set.
  - Methodology completion is fail-closed on missing/empty done/report files or invalid exit reason.

- dependencies_and_callers:
  - `hooks/hooks.json` is the direct caller configuration for the hook entrypoints.
  - `loop-read-validator.sh`, `loop-write-validator.sh`, `loop-edit-validator.sh`, `loop-bash-validator.sh`, `loop-plan-file-validator.sh`, and `loop-codex-stop-hook.sh` all source `hooks/lib/loop-common.sh`.
  - `loop-common.sh` sources `hooks/lib/project-root.sh`, `scripts/lib/config-loader.sh`, `hooks/lib/template-loader.sh`, and finally `hooks/lib/loop-bg-tasks.sh`.
  - `loop-codex-stop-hook.sh` also sources `scripts/portable-timeout.sh` and `hooks/lib/methodology-analysis.sh`; it shells out to `scripts/bitlesson-validate-delta.sh` and `codex`.
  - `loop-post-bash-hook.sh` sources only `hooks/lib/project-root.sh` to avoid needing full loop-common dependencies for session-id patching.
  - `check-todos-from-transcript.py` is called by the stop hook at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/hooks/loop-codex-stop-hook.sh:408).
  - Scripts outside `hooks` depend on these helpers too: `scripts/ask-codex.sh` and `scripts/bitlesson-select.sh` source `loop-common.sh`; `scripts/bitlesson-select.sh` also sources `project-root.sh`; monitor/status scripts mirror active-loop state logic.
  - Prompt templates under `prompt-template/block`, `prompt-template/claude`, and `prompt-template/codex` are runtime dependencies for all user-facing block prompts and review prompts.
  - Tests referencing this directory include `tests/test-finalize-phase.sh`, `tests/test-stop-hook-bg-allow.sh`, `tests/test-cancel-signal-file.sh`, `tests/test-disable-nested-codex-hooks.sh`, `tests/test-todo-checker.sh`, `tests/test-template-references.sh`, and `tests/robustness/test-hook-system-robustness.sh`.

- edge_cases_or_failure_modes:
  - Symlinked project prefixes like `/var` versus `/private/var` are handled by realpath canonicalization; leaf symlinks are deliberately not dereferenced by prefix comparison to avoid approving a read/write/move through a symlink that escapes the loop directory.
  - Nonexistent write targets are handled by canonicalizing parent directories and reattaching the basename.
  - If `realpath` fails in methodology-analysis validators, code falls back to raw absolute paths, blocks traversal segments, and in read mode rejects unresolved symlinks; write/edit methodology fallback does not include the same explicit unresolved-leaf-symlink rejection as read mode, though it only allows two methodology filenames inside the loop.
  - Invalid hook JSON, null bytes, invalid UTF-8, missing required tool fields, and excessive JSON depth block before authorization logic.
  - Git commands may time out or fail; plan-file validator and stop hook generally fail closed with block JSON. Stale `index.lock` cleanup is attempted after git status failure.
  - Codex CLI missing, nonzero Codex exit, absent/empty review result, or failing `codex review` all block the loop and ask for retry rather than silently succeeding.
  - Missing `Mainline Progress Verdict` in implementation review blocks to avoid unsafe drift state updates.
  - `STOP` outside a full-alignment round is unusual but honored and terminal.
  - Max-iteration handling differs by phase: implementation can terminate/maxiter, review phase ignores max iterations until code-review issues clear, finalize phase skips max-iteration checks.
  - Session ID absence with `bg-pending.marker` causes silent stop-hook allow to avoid incorrectly adopting or cleaning a parked loop.
  - `git_adds_humanize` uses current working directory for `.humanize` existence and `git check-ignore`, while stop hook uses `PROJECT_ROOT` for tracked-state checks. If hook cwd diverges, broad non-force `git add .` heuristics may depend on cwd; direct `.humanize` references and forced broad adds are still blocked by pattern alone.
  - `loop-edit-validator.sh` extracts `tool_name` with direct `jq` rather than the shared `validate_hook_input`, so its malformed JSON behavior can be less structured than read/write/bash validators.
  - The export was read-only and did not contain a usable `.git` checkout for source-commit verification; filesystem inspection was used and source metadata was taken from the scheduler prompt.

- validation_or_tests:
  - Direct tests visible in the repo cover many hook paths:
    - `tests/test-todo-checker.sh` targets `check-todos-from-transcript.py`.
    - `tests/test-finalize-phase.sh` exercises write/edit/bash/read validators and stop-hook finalize behavior.
    - `tests/test-stop-hook-bg-allow.sh` covers background-task short-circuit, cross-session parked-loop behavior, marker creation/preservation/cleanup, missing/malformed transcript preservation, and loop-start transcript boundaries.
    - `tests/test-cancel-signal-file.sh` covers cancel authorization, including canonicalization of symlinked loop prefixes as noted around the test comments near path canonicalization.
    - `tests/test-disable-nested-codex-hooks.sh` verifies nested Codex reviewer calls pass `--disable codex_hooks`.
    - `tests/test-template-references.sh` and `tests/test-templates-comprehensive.sh` validate referenced templates and template rendering.
    - `tests/robustness/test-hook-system-robustness.sh` covers edit-validator input behavior, plan-file validator behavior, goal-tracker mutable/immutable rules, old-session read blocking, concurrent hook reads, corrupt/incomplete state, and deep JSON cases.
    - `tests/robustness/test-path-validation-robustness.sh`, `tests/robustness/test-cancel-security-robustness.sh`, `tests/robustness/test-state-file-robustness.sh`, and `tests/robustness/test-session-robustness.sh` are relevant robustness suites for the same algorithmic surfaces.
  - I did not run the test suite because this task requested research notes only and the branch export is read-only. All validation notes above are based on recursive inspection of `hooks/` plus referenced tests/scripts/templates.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 Item Evidence section present for the single assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`