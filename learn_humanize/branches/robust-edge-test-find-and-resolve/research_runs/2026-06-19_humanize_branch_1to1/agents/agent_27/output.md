# agent_27 robust-edge-test-find-and-resolve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 3
- source_commit: `a3112ca4d149f56ced783e805b6dfcf029368dc4`

## Item Evidence

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-027 `file` `scripts/humanize.sh`
- cursor: `[_]`
- core_role:
  - Runtime shell utility entrypoint for the Humanize RLCR monitor and related parsers. It exposes reusable parsing helpers plus the `humanize monitor rlcr-loop` command router.
  - It does not implement the RLCR loop itself. It observes loop state generated under `.humanize/rlcr/` and Codex run logs emitted under `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/...`.
  - Main sections:
    - public helper functions: `humanize_split_to_array`, `humanize_parse_goal_tracker`, `humanize_detect_git_state`, `humanize_parse_git_status` at `scripts/humanize.sh:10-204`.
    - monitor implementation `_humanize_monitor_codex` at `scripts/humanize.sh:210-868`.
    - public CLI dispatcher `humanize()` at `scripts/humanize.sh:870-903`.

- algorithmic_behavior:
  - `humanize_split_to_array` converts pipe-delimited protocol strings into shell arrays with separate bash and zsh implementations (`scripts/humanize.sh:10-22`). This is used by the monitor to unpack parser outputs and state-file metadata.
  - `humanize_parse_goal_tracker` parses a markdown `goal-tracker.md` and emits a pipe-delimited summary:
    `total_acs|completed_acs|active_tasks|completed_tasks|deferred_tasks|open_issues|goal_summary` (`scripts/humanize.sh:24-106`).
    - Acceptance criteria are counted from the `### Acceptance Criteria` section, supporting table and list formats (`scripts/humanize.sh:42-48`).
    - Active tasks are counted from `#### Active Tasks`, subtracting rows whose status column is `completed` or `deferred` (`scripts/humanize.sh:50-78`).
    - Completed, deferred, and open issue counts are inferred by counting table rows in named sections (`scripts/humanize.sh:80-97`).
    - A short ultimate-goal display string is extracted from the first content line under `### Ultimate Goal` (`scripts/humanize.sh:98-103`).
  - `humanize_detect_git_state` classifies the current repository as `normal`, `not_a_repo`, `permission_error`, `rebase`, `merge`, `shallow`, or `detached` (`scripts/humanize.sh:108-156`). It checks git directory accessibility first, then specific in-progress markers, then whether `HEAD` is symbolic.
  - `humanize_parse_git_status` emits modified/added/deleted/untracked and diffstat insertion/deletion counts (`scripts/humanize.sh:158-204`). It uses `git status --porcelain` for file-state counts and `git diff --shortstat HEAD` with fallback to `git diff --shortstat` for line counts (`scripts/humanize.sh:167-203`).
  - `_humanize_monitor_codex` provides a terminal monitor:
    - validates `.humanize/rlcr` exists before starting (`scripts/humanize.sh:224-229`);
    - finds the latest timestamp-named RLCR session directory using `find`, not shell globs, to avoid zsh no-match failures (`scripts/humanize.sh:231-253`);
    - finds the latest `round-*-codex-run.log` in the per-project cache path, matching the sanitized current working directory and session timestamp (`scripts/humanize.sh:255-314`);
    - detects active or stopped loop state by preferring `state.md` and otherwise reading `*-state.md` stop files (`scripts/humanize.sh:316-355`);
    - parses state fields such as `current_round`, `max_iterations`, `codex_model`, `codex_effort`, `started_at`, and `plan_file` (`scripts/humanize.sh:357-373`);
    - redraws an 11-line status bar showing session, round, model, loop status, goal tracker progress, git status, goal, plan, and log path (`scripts/humanize.sh:381-518`);
    - sets a terminal scroll region below the status bar and restores it on cleanup (`scripts/humanize.sh:520-536`);
    - traps `INT` and `TERM`, kills any tracked background tail process, restores terminal state, and emits a stop message (`scripts/humanize.sh:538-562`);
    - exits gracefully if `.humanize/rlcr` is deleted while monitoring (`scripts/humanize.sh:564-577`, `scripts/humanize.sh:612-618`, `scripts/humanize.sh:747-750`);
    - handles no-log sessions by polling until a cache log appears or a newer session is created (`scripts/humanize.sh:633-733`);
    - handles log growth, truncation/rotation, session deletion, log deletion, newer sessions, and newer round logs (`scripts/humanize.sh:735-863`).
  - `humanize()` dispatches only `monitor rlcr-loop`; all other commands print usage and return failure (`scripts/humanize.sh:870-903`).

- inputs_outputs_state:
  - Inputs:
    - current working directory, expected to be a project root containing `.humanize/rlcr/` for monitor mode (`scripts/humanize.sh:218-229`);
    - timestamped session directories named like `YYYY-MM-DD_HH-MM-SS` (`scripts/humanize.sh:245-250`);
    - state files `state.md` or `<stop_reason>-state.md` (`scripts/humanize.sh:316-355`);
    - `goal-tracker.md` inside the selected session (`scripts/humanize.sh:388-417`);
    - Codex run logs from `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/<sanitized-project>/<timestamp>/round-*-codex-run.log` (`scripts/humanize.sh:255-314`);
    - git repository state in the current directory for the git status display (`scripts/humanize.sh:158-204`, `scripts/humanize.sh:419-427`);
    - terminal capabilities through `tput`, `clear`, ANSI escape sequences, `stat`, `tail`, and `find`.
  - Outputs:
    - helper functions output pipe-delimited machine-readable summaries to stdout (`scripts/humanize.sh:24-106`, `scripts/humanize.sh:158-204`);
    - monitor outputs a live terminal status bar plus tailed/incremental log content;
    - monitor returns `1` for missing loop directory or missing sessions at startup (`scripts/humanize.sh:224-229`, `scripts/humanize.sh:586-590`);
    - monitor returns `0` on graceful deletion stop paths (`scripts/humanize.sh:615-618`, `scripts/humanize.sh:747-750`);
    - CLI usage errors return `1` (`scripts/humanize.sh:882-891`, `scripts/humanize.sh:895-900`).
  - State transitions:
    - The script does not persistently mutate project state.
    - It maintains in-memory monitor state: `current_session_dir`, `current_file`, `current_loop_status`, `last_size`, and `last_no_log_status`.
    - It transitions internally among waiting-for-log, following-log, switching-session, switching-log, and graceful-stop modes.
    - It treats `state.md` as `active`; any `*-state.md` file becomes the display status derived from the filename (`scripts/humanize.sh:328-354`).

- gates_or_invariants:
  - Monitor startup gate: `.humanize/rlcr` must exist, and at least one timestamped session directory must exist (`scripts/humanize.sh:224-229`, `scripts/humanize.sh:582-590`).
  - Session naming invariant: only directories matching `^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}$` participate in latest-session/log selection (`scripts/humanize.sh:245-250`, `scripts/humanize.sh:282-285`).
  - Cache-path invariant: monitor log lookup must match the same sanitized project path convention used by the stop hook (`scripts/humanize.sh:262-269`). The stop hook writes to the matching path at `hooks/loop-codex-stop-hook.sh:782-797`.
  - Shell compatibility invariant: zsh gets `ksharrays` enabled locally so array indices match bash expectations (`scripts/humanize.sh:213-216`), and `find` is used instead of globs in session/log scans (`scripts/humanize.sh:239-251`, `scripts/humanize.sh:276-311`, `scripts/humanize.sh:334-348`).
  - Terminal cleanup invariant: `_cleanup` is idempotent through `cleanup_done`, resets traps, restores scroll region, and prints a stop message (`scripts/humanize.sh:543-562`).
  - Log truncation invariant: size shrinkage is treated as rotation/truncation only after prior content was observed (`scripts/humanize.sh:769-779`).

- dependencies_and_callers:
  - The user-facing command is documented by tests/manual usage as `source scripts/humanize.sh && humanize monitor rlcr-loop`, and the script’s dispatcher exposes that same route (`scripts/humanize.sh:876-891`).
  - `scripts/setup-rlcr-loop.sh` creates the RLCR session/state model that the monitor reads; its help describes `.humanize/rlcr/*/state.md` and round files (`scripts/setup-rlcr-loop.sh:91-99`).
  - `hooks/loop-codex-stop-hook.sh` writes Codex debug artifacts into the cache path consumed by `_find_latest_codex_log` (`hooks/loop-codex-stop-hook.sh:782-797`).
  - The monitor depends on shell tools: `git`, `sed`, `grep`, `sort`, `wc`, `cut`, `find`, `basename`, `pwd`, `tput`, `clear`, `stat`, `tail`, `kill`, and `seq`.
  - Direct test callers source `scripts/humanize.sh`:
    - `tests/test-monitor-e2e-real.sh` runs the real `_humanize_monitor_codex` in bash and zsh (`tests/test-monitor-e2e-real.sh:103-149`, `tests/test-monitor-e2e-real.sh:276-310`);
    - `tests/robustness/test-goal-tracker-robustness.sh` tests `humanize_parse_goal_tracker` (`tests/robustness/test-goal-tracker-robustness.sh:1-36`);
    - `tests/robustness/test-git-operations-robustness.sh` tests `humanize_parse_git_status` and git state handling (`tests/robustness/test-git-operations-robustness.sh:1-33`);
    - `tests/robustness/test-hook-input-robustness.sh` also invokes parser and monitor paths according to search evidence.

- edge_cases_or_failure_modes:
  - Missing tracker file returns a valid fallback tuple with `No goal tracker` (`scripts/humanize.sh:28-30`), so the monitor can still render.
  - Missing `.humanize/rlcr` before startup is a hard monitor error, while deletion during runtime is a graceful stop (`scripts/humanize.sh:224-229`, `scripts/humanize.sh:615-618`).
  - Empty/no-log sessions do not fail immediately; the monitor displays a waiting or no-log message based on loop status and keeps polling (`scripts/humanize.sh:633-731`).
  - If a current session or log disappears, the monitor switches to the latest available session/log or waits for new sessions (`scripts/humanize.sh:685-713`, `scripts/humanize.sh:789-823`).
  - If multiple `*-state.md` files exist, `_find_state_file` takes the first `find` result, so display status may be filesystem-order dependent (`scripts/humanize.sh:334-351`).
  - Pipe-delimited protocols can be confused if `goal_summary` or other returned fields contain literal `|`; `humanize_split_to_array` has no escaping layer (`scripts/humanize.sh:10-22`, `scripts/humanize.sh:98-105`).
  - `eval` is used with the destination array name in `humanize_split_to_array` (`scripts/humanize.sh:15-21`); this is acceptable for internal fixed names but unsafe for untrusted `arr_name`.
  - `humanize_parse_git_status` returns a seventh explanatory field for non-git directories despite its comment documenting six fields (`scripts/humanize.sh:158-164`). Current monitor consumers read only the first six.
  - Git status parsing covers common modified/added/deleted/untracked/renamed states but only approximates complex porcelain states such as conflicts or copies (`scripts/humanize.sh:173-188`).
  - Very narrow terminals can make `max_display_len` and suffix/prefix lengths small or negative in truncation math (`scripts/humanize.sh:436-447`); robustness tests mention narrow terminal scenarios, but the script itself has no explicit minimum-width guard.
  - `tail_pid` cleanup support exists, but the monitor uses polling rather than a background `tail -f`, so `tail_pid` is normally empty (`scripts/humanize.sh:538-557`, `scripts/humanize.sh:735-768`).

- validation_or_tests:
  - `tests/test-monitor-e2e-real.sh` validates real monitor behavior for graceful deletion, no zsh/bash glob errors, terminal cleanup, and bash/zsh operation (`tests/test-monitor-e2e-real.sh:1-13`, `tests/test-monitor-e2e-real.sh:185-224`, `tests/test-monitor-e2e-real.sh:343-360`).
  - `tests/test-monitor-runtime.sh` validates cleanup and graceful-stop patterns; search evidence shows direct checks for `_restore_terminal`, scroll reset, and `_graceful_stop`.
  - `tests/test-zsh-monitor-safety.sh` validates sourcing and monitor-scan behavior under zsh with empty/dotfile-only directories, based on search evidence.
  - `tests/robustness/test-goal-tracker-robustness.sh` validates standard tables, mixed AC formats, large counts, special characters, empty/malformed files, and related parser behavior (`tests/robustness/test-goal-tracker-robustness.sh:1-36`).
  - `tests/robustness/test-git-operations-robustness.sh` validates clean, modified, added, deleted, untracked, detached, rebase/merge, and non-git behavior (`tests/robustness/test-git-operations-robustness.sh:1-33`).
  - I did not run tests because this task requested research notes only and the branch export is read-only.

- skip_candidate: `no`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-057 `file` `prompt-template/block/git-not-clean-humanize-local.md`
- cursor: `[_]`
- core_role:
  - Small prompt/block template used by the RLCR stop hook when git is dirty specifically because `.humanize*` local loop artifacts are untracked.
  - It adds a special remediation note to the broader Git-not-clean block, telling the user that `.humanize/` is generated by `humanize:start-rlcr-loop` and should not be committed (`prompt-template/block/git-not-clean-humanize-local.md:2-4`).

- algorithmic_behavior:
  - The template has no placeholders. Rendering is a direct file read.
  - It instructs the operator to append `.humanize*` to `.gitignore` and stage the ignore-file change (`prompt-template/block/git-not-clean-humanize-local.md:5-8`).
  - In the stop hook, git status is cached, untracked lines are extracted, and paths matching `.humanize` trigger loading this template (`hooks/loop-codex-stop-hook.sh:437-450`).
  - The rendered note is appended to `SPECIAL_NOTES`, which is then interpolated into the broader `block/git-not-clean.md` message before the hook returns a JSON block decision (`hooks/loop-codex-stop-hook.sh:464-485`).

- inputs_outputs_state:
  - Inputs:
    - The template itself;
    - the stop hook’s cached `git status --porcelain` output;
    - an untracked-file grep path containing `.humanize` (`hooks/loop-codex-stop-hook.sh:441-446`).
  - Outputs:
    - Markdown text inserted into a stop-hook block reason.
    - Suggested shell commands:
      - `echo '.humanize*' >> .gitignore`
      - `git add .gitignore`
  - State transitions:
    - The template does not mutate state by itself.
    - If followed by the user/agent, it transitions `.humanize*` artifacts from untracked git noise to ignored local artifacts, and stages `.gitignore` for commit.
    - The hook remains blocked until the repo becomes clean; this template only explains how to satisfy that gate.

- gates_or_invariants:
  - Git clean gate: any cached non-empty porcelain status becomes `GIT_ISSUES="uncommitted changes"` and blocks exit (`hooks/loop-codex-stop-hook.sh:437-485`).
  - Special-case invariant: `.humanize*` artifacts are local loop state and should not be committed (`prompt-template/block/git-not-clean-humanize-local.md:2-4`).
  - Fallback invariant: if this template is missing or empty, the hook substitutes a shorter note: `Note: .humanize* directories are intentionally untracked.` (`hooks/loop-codex-stop-hook.sh:446-449`).

- dependencies_and_callers:
  - Called only through the template loader from `hooks/loop-codex-stop-hook.sh` (`hooks/loop-codex-stop-hook.sh:446`).
  - The loader uses direct file reads for templates and returns an empty string if a file is absent (`hooks/lib/template-loader.sh:33-48`).
  - It coordinates with the parent `block/git-not-clean.md` template through `SPECIAL_NOTES` (`hooks/loop-codex-stop-hook.sh:467-475`).
  - It exists because `scripts/setup-rlcr-loop.sh` and the RLCR system create `.humanize/rlcr/...` local state, which the workflow should keep out of commits.

- edge_cases_or_failure_modes:
  - The hook detects `.humanize` with `grep -q '\.humanize'` over untracked lines, so any untracked path containing that substring can trigger this note, not only the root `.humanize/` directory (`hooks/loop-codex-stop-hook.sh:441-446`).
  - The suggested `echo '.humanize*' >> .gitignore` is append-only and can duplicate existing ignore entries.
  - The broad `.humanize*` pattern intentionally also ignores legacy or sibling `.humanize-*` paths, but it could ignore any future tracked-intended path matching that prefix.
  - The template tells the user to stage `.gitignore`, but the parent hook still requires a commit and clean working tree afterward; staging alone will not pass the git-clean gate.
  - If `.gitignore` itself is untracked or has unrelated changes, following this note may still leave the broader dirty-state block active.

- validation_or_tests:
  - Search evidence shows related test setup adding `.humanize*` to `.gitignore` in `tests/test-plan-file-hooks.sh`, but I did not find a direct golden assertion for the exact text of this template.
  - The enclosing git-clean gate is implemented in `hooks/loop-codex-stop-hook.sh:426-485`.
  - Template loading/fallback behavior is covered structurally by `hooks/lib/template-loader.sh:33-48` and `hooks/lib/template-loader.sh:167-180`.
  - I did not run tests because this task requested research notes only and the branch export is read-only.

- skip_candidate: `no`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-087 `file` `prompt-template/codex/full-alignment-review.md`
- cursor: `[_]`
- core_role:
  - Mandatory Codex review prompt template for every fifth RLCR review checkpoint. It defines the high-rigor alignment audit that decides whether the implementation is complete, must continue, or is stagnating enough to stop.
  - The stop hook selects this template when `CURRENT_ROUND % 5 == 4` (`hooks/loop-codex-stop-hook.sh:686-690`) and writes the rendered prompt to `round-N-review-prompt.md` (`hooks/loop-codex-stop-hook.sh:721-734`).

- algorithmic_behavior:
  - The template requires Codex to read the original implementation plan first through `@{{PLAN_FILE}}` (`prompt-template/codex/full-alignment-review.md:5-10`).
  - It embeds Claude’s round summary between explicit markers using `{{SUMMARY_CONTENT}}` (`prompt-template/codex/full-alignment-review.md:13-16`).
  - Part 1 audits the goal tracker:
    - read `@{{GOAL_TRACKER_FILE}}` (`prompt-template/codex/full-alignment-review.md:19-22`);
    - verify every immutable acceptance criterion with `MET / PARTIAL / NOT MET / DEFERRED` statuses and evidence/blocker/justification columns (`prompt-template/codex/full-alignment-review.md:23-29`);
    - compare original plan versus tracker to detect forgotten tasks or unverified completion claims (`prompt-template/codex/full-alignment-review.md:30-35`);
    - re-evaluate each deferred item for validity and contradiction with the ultimate goal (`prompt-template/codex/full-alignment-review.md:36-41`);
    - summarize acceptance criteria, active tasks, remaining rounds, and blockers (`prompt-template/codex/full-alignment-review.md:42-48`).
  - Part 2 requires a critical implementation review, reality-checking Claude’s claims and using `@{{DOCS_PATH}}` for design documents (`prompt-template/codex/full-alignment-review.md:50-55`).
  - Part 3 injects `{{GOAL_TRACKER_UPDATE_SECTION}}`, which is rendered separately by the stop hook and shared with regular reviews (`hooks/loop-codex-stop-hook.sh:680-684`, `prompt-template/codex/full-alignment-review.md:57`).
  - Part 4 is a stagnation/circuit-breaker audit:
    - states completed iterations from round 0 to current round (`prompt-template/codex/full-alignment-review.md:59-62`);
    - points Codex to historical prompts, summaries, review prompts, and review results under `.humanize/rlcr/{{LOOP_TIMESTAMP}}/` (`prompt-template/codex/full-alignment-review.md:63-73`);
    - instructs Codex to review especially the last 5 rounds and lists stagnation signs (`prompt-template/codex/full-alignment-review.md:74-83`);
    - requires `STOP` as the last line when stagnation is detected (`prompt-template/codex/full-alignment-review.md:84`).
  - Part 5 defines terminal marker semantics:
    - write findings/action items to `@{{REVIEW_RESULT_FILE}}` if issues exist or any AC is not met, including deferred ACs (`prompt-template/codex/full-alignment-review.md:86-89`);
    - write `STOP` as last line for stagnation (`prompt-template/codex/full-alignment-review.md:90`);
    - write `COMPLETE` as last line only when all original plan tasks are done, all ACs are fully met, and there are no deferrals (`prompt-template/codex/full-alignment-review.md:91-93`).

- inputs_outputs_state:
  - Inputs:
    - `CURRENT_ROUND`, `PLAN_FILE`, `SUMMARY_CONTENT`, `GOAL_TRACKER_FILE`, `DOCS_PATH`, `GOAL_TRACKER_UPDATE_SECTION`, `COMPLETED_ITERATIONS`, `LOOP_TIMESTAMP`, `PREV_ROUND`, `PREV_PREV_ROUND`, and `REVIEW_RESULT_FILE` from the stop hook render call (`hooks/loop-codex-stop-hook.sh:721-734`);
    - historical round files under `.humanize/rlcr/<timestamp>/`;
    - design docs at `{{DOCS_PATH}}`;
    - the current goal tracker and original plan.
  - Outputs:
    - Rendered prompt file: `$LOOP_DIR/round-${CURRENT_ROUND}-review-prompt.md` (`hooks/loop-codex-stop-hook.sh:674-676`, `hooks/loop-codex-stop-hook.sh:721-734`);
    - expected review output file: `$LOOP_DIR/round-${CURRENT_ROUND}-review-result.md`;
    - terminal status marker on the last non-empty line: `COMPLETE`, `STOP`, or neither.
  - State transitions:
    - `COMPLETE` last line causes the stop hook to rename `state.md` to `finalize-state.md` and block with a finalize prompt, unless already at max iterations (`hooks/loop-codex-stop-hook.sh:966-1025`).
    - `STOP` last line causes the hook to end the loop with stop state via `end_loop ... "$EXIT_STOP"` (`hooks/loop-codex-stop-hook.sh:1028-1055`).
    - Any other non-empty review content advances `current_round` to the next round and creates the next prompt with the review feedback (`hooks/loop-codex-stop-hook.sh:1058-1083`).
    - If `COMPLETE` occurs when `CURRENT_ROUND >= MAX_ITERATIONS`, finalize is skipped and the loop terminates as max-iteration state (`hooks/loop-codex-stop-hook.sh:968-973`).

- gates_or_invariants:
  - Full alignment checkpoint cadence is zero-based: rounds where `CURRENT_ROUND % 5 == 4` use this template (`hooks/loop-codex-stop-hook.sh:686-690`). That means the first checkpoint is round 4 after rounds 0-4 have occurred.
  - Original plan is authoritative for scope; Codex must read it before reviewing (`prompt-template/codex/full-alignment-review.md:5-10`).
  - Deferred items are explicitly incomplete for `COMPLETE` purposes (`prompt-template/codex/full-alignment-review.md:91-93`).
  - `STOP` and `COMPLETE` are strict last-line markers. The hook trims whitespace on the last non-empty line and requires exact equality, preventing false positives such as “CANNOT COMPLETE” (`hooks/loop-codex-stop-hook.sh:960-967`, `hooks/loop-codex-stop-hook.sh:1028-1029`).
  - The template requires historical progress review before triggering stagnation STOP, tying STOP to repeated lack of progress rather than a single bad round (`prompt-template/codex/full-alignment-review.md:74-84`).
  - The template requires action items when issues are found, so the next-round prompt can feed actionable review content back to Claude (`prompt-template/codex/full-alignment-review.md:86-89`, `hooks/loop-codex-stop-hook.sh:1071-1083`).

- dependencies_and_callers:
  - Rendered by `hooks/loop-codex-stop-hook.sh` during full-alignment rounds (`hooks/loop-codex-stop-hook.sh:721-734`).
  - Loaded and rendered through `hooks/lib/template-loader.sh`; placeholder replacement is single-pass and leaves missing variables unchanged (`hooks/lib/template-loader.sh:7-14`, `hooks/lib/template-loader.sh:50-132`).
  - Depends on the shared goal-tracker update section rendered from `prompt-template/codex/goal-tracker-update-section.md` (`hooks/loop-codex-stop-hook.sh:680-684`).
  - Consumed by Codex CLI through `codex exec` with project root set by `-C "$PROJECT_ROOT"` (`hooks/loop-codex-stop-hook.sh:818-845`).
  - Marker constants come from `hooks/lib/loop-common.sh` according to search evidence: `MARKER_COMPLETE="COMPLETE"` and `MARKER_STOP="STOP"`.

- edge_cases_or_failure_modes:
  - If the template is missing or renders empty, the stop hook fallback is much weaker and does not include the full stagnation audit or no-deferral completion rule (`hooks/loop-codex-stop-hook.sh:698-708`, `hooks/loop-codex-stop-hook.sh:721-734`).
  - Because rendering is single-pass, any `{{...}}` inside `SUMMARY_CONTENT` is preserved instead of being accidentally substituted. This prevents prompt corruption but can leave literal placeholders in Codex-visible content if the summary contains them (`hooks/lib/template-loader.sh:54-57`, `hooks/lib/template-loader.sh:116-122`).
  - Historical file references assume the `.humanize/rlcr/<timestamp>/round-*` files exist. Missing history may weaken the stagnation check but does not stop prompt generation.
  - The phrase “every 5 rounds” can be human-confusing because implementation uses zero-based `CURRENT_ROUND % 5 == 4`; operationally that means rounds 4, 9, 14, etc.
  - A Codex review that writes findings but accidentally ends with `COMPLETE` will be accepted by marker parsing; the correctness gate is in prompt compliance, not parser semantic validation beyond the last-line marker.
  - Conversely, a review that states all work is complete but does not put exact `COMPLETE` on its own final non-empty line will continue the loop.
  - `STOP` during a non-alignment round is still honored by the hook, though logged as unusual; this template is the normal source of STOP instructions (`hooks/loop-codex-stop-hook.sh:1028-1055`).

- validation_or_tests:
  - Marker handling is tested in `tests/test-finalize-phase.sh`: a mock Codex output ending in `COMPLETE` triggers finalize-state creation, while max-iteration COMPLETE creates maxiter state instead (`tests/test-finalize-phase.sh:448-501`).
  - Normal non-COMPLETE review feedback is tested to keep `state.md` active and block with feedback for the next round (`tests/test-finalize-phase.sh:548-590`).
  - Hook code validates review result existence and non-emptiness before marker parsing (`hooks/loop-codex-stop-hook.sh:902-955`).
  - I did not find a direct golden test for the exact full-alignment template body, but its render path and terminal marker consequences are represented by the stop-hook and finalize-phase tests.
  - I did not run tests because this task requested research notes only and the branch export is read-only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 3 section headers present, matching `assigned_item_count`
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`