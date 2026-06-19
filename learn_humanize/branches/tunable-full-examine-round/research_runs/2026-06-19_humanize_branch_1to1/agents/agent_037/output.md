# agent_037 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-037 `file` `scripts/humanize.sh`
- cursor: `[_]`
- core_role:
  - `scripts/humanize.sh` is the shell entrypoint for the Humanize runtime monitor UI. It does not execute implementation work, claim scheduler items, mutate checklist state, or enforce execution-cron validation gates; its core role is to interpret local loop artifacts and stream them into operator-facing RLCR and PR monitor views.
  - The file defines reusable parsers for goal-tracker summaries and git status, then exposes `humanize monitor rlcr` and `humanize monitor pr` through the public `humanize()` dispatcher at `scripts/humanize.sh:883-924`.
  - It optionally sources shared monitor primitives from `scripts/lib/monitor-common.sh` at `scripts/humanize.sh:7-9`; monitor modes depend on that library for latest-session detection, state-file detection, file-size reads, and PR goal-tracker parsing.

- algorithmic_behavior:
  - Shared parsing:
    - `humanize_split_to_array` converts pipe-delimited output into shell arrays with bash/zsh-specific logic (`scripts/humanize.sh:18-28`). It uses `eval`, so callers must pass trusted variable names.
    - `humanize_parse_goal_tracker` reads a `goal-tracker.md` file and emits `total_acs|completed_acs|active_tasks|completed_tasks|deferred_tasks|open_issues|goal_summary` (`scripts/humanize.sh:32-111`). It counts AC rows/list items under `### Acceptance Criteria`, derives active tasks by subtracting completed/deferred rows in `#### Active Tasks`, counts completed/deferred/open-issue table rows, and truncates the goal summary to 60 chars.
    - `humanize_detect_git_state` classifies repository state as normal, detached, rebase, merge, shallow, permission error, or not-a-repo by inspecting `git rev-parse --git-dir`, rebase directories, `MERGE_HEAD`, `shallow`, and symbolic HEAD (`scripts/humanize.sh:116-162`).
    - `humanize_parse_git_status` reads `git status --porcelain` plus `git diff --shortstat` and emits file-state and line-change counters (`scripts/humanize.sh:166-209`).
  - RLCR monitor:
    - `_humanize_monitor_codex` watches `.humanize/rlcr` sessions and project-scoped cache logs under `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/<sanitized-pwd>/<session>` (`scripts/humanize.sh:219-342`).
    - Latest session selection is timestamp-name based through `monitor_find_latest_session`; latest log selection scans `round-*-codex-run.log` and `round-*-codex-review.log`, choosing newest session then greatest round (`scripts/humanize.sh:237-341`).
    - It draws an 11-line fixed status bar with session, start time, round, model, loop status, AC/task progress, git dirty summary, goal, plan, and current log (`scripts/humanize.sh:374-510`).
    - It tails the current log incrementally by byte offset, handles no-log waiting, detects growth, detects truncation/rotation by file-size shrink, and switches to newer sessions/logs (`scripts/humanize.sh:621-872`).
  - PR monitor:
    - `_humanize_monitor_pr` watches `.humanize/pr-loop`, supports `--once`, and picks the newest PR activity file by mtime across `round-*-pr-check.md`, `round-*-pr-feedback.md`, and `round-*-pr-comment.md` (`scripts/humanize.sh:931-1009`).
    - It maps generic stop-state names into PR-friendly display names such as `approve` to `approved` and `maxiter` to `max-iterations` (`scripts/humanize.sh:1011-1028`).
    - It parses YAML frontmatter from PR loop state files for round, max iterations, PR number, branch, bot lists, Codex model/effort, and start time (`scripts/humanize.sh:1030-1059`).
    - Interactive PR mode uses `tail -n +1 -f` as a background process and swaps the tailed file when newer activity appears (`scripts/humanize.sh:1295-1355`). One-shot mode prints a static report plus recent files and the latest file tail (`scripts/humanize.sh:1215-1292`).

- inputs_outputs_state:
  - Inputs:
    - CLI/function inputs: `humanize monitor rlcr`, `humanize monitor pr`, optional PR `--once`, parser file paths.
    - Filesystem inputs: `.humanize/rlcr/<timestamp>/state.md` or stop-state files, `.humanize/rlcr/<timestamp>/goal-tracker.md`, cache logs in `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/...`, `.humanize/pr-loop/<timestamp>/state.md` or stop-state files, PR round files, and PR `goal-tracker.md`.
    - Runtime inputs: current working directory, `XDG_CACHE_HOME`, `HOME`, terminal size from `tput`, current git repository state, bash vs zsh environment.
  - Outputs:
    - Parser functions emit pipe-delimited summaries on stdout.
    - Monitor functions print terminal status bars, log tails, waiting messages, usage text, and error messages; they return nonzero for missing required loop roots or missing sessions in one-shot paths.
    - No durable repo files are written by this script.
  - State transitions:
    - RLCR monitor maintains local `current_session_dir`, `current_file`, `current_loop_status`, `last_size`, `last_no_log_status`, `monitor_running`, and `cleanup_done` state (`scripts/humanize.sh:530-618`).
    - RLCR terminal state transitions are: clear screen, reserve top status-bar lines, stream log body, reset scroll region on cleanup or graceful stop (`scripts/humanize.sh:512-560`).
    - PR monitor maintains `current_session_dir`, `current_file`, `TAIL_PID`, `monitor_running`, and `cleanup_done`; it starts/kills the background tail process when session or activity file changes (`scripts/humanize.sh:1169-1200`, `scripts/humanize.sh:1314-1345`).
    - Signal state is managed with zsh `TRAPINT`/`TRAPTERM` or bash `trap` handlers for cleanup (`scripts/humanize.sh:578-588`, `scripts/humanize.sh:1202-1213`).

- gates_or_invariants:
  - RLCR monitor requires `.humanize/rlcr` to exist before startup; otherwise it returns with an operator-facing error (`scripts/humanize.sh:231-235`).
  - PR monitor requires `.humanize/pr-loop` to exist before startup; otherwise it returns with an operator-facing error (`scripts/humanize.sh:955-960`).
  - Session directories must match `YYYY-MM-DD_HH-MM-SS`; nonconforming directories are ignored (`scripts/humanize.sh:286-289`, shared helper `scripts/lib/monitor-common.sh:54-60`).
  - RLCR cache lookup uses sanitized current project path, so the monitor only watches logs associated with the current checkout path (`scripts/humanize.sh:250-256`).
  - RLCR has a defensive log-order invariant: if both run and review logs exist in a session, the maximum run round must be strictly less than the minimum review round, or the function emits an inconsistency error (`scripts/humanize.sh:297-337`).
  - State-file detection prioritizes active `state.md`; otherwise it chooses a `*-state.md` stop file and derives the stop reason from the filename (`scripts/lib/monitor-common.sh:147-180`).
  - The monitor code intentionally uses `find` rather than shell globs to avoid zsh “no matches found” failures in empty directories (`scripts/humanize.sh:280-328`, `scripts/lib/monitor-common.sh:49-60`).
  - Cleanup is idempotent via `cleanup_done` guards and resets traps before killing background work (`scripts/humanize.sh:537-560`, `scripts/humanize.sh:1176-1199`).

- dependencies_and_callers:
  - Direct sourced dependency: `scripts/lib/monitor-common.sh`, especially `monitor_get_file_size`, `monitor_find_latest_session`, `monitor_find_state_file`, and `humanize_parse_pr_goal_tracker` (`scripts/lib/monitor-common.sh:32-35`, `scripts/lib/monitor-common.sh:40-63`, `scripts/lib/monitor-common.sh:154-180`, `scripts/lib/monitor-common.sh:465-498`).
  - External command dependencies: `git`, `sed`, `grep`, `sort`, `wc`, `tr`, `cut`, `head`, `tail`, `find`, `stat`, `basename`, `pwd`, `tput`, `clear`, `seq`, `sleep`, `kill`, and shell process substitution.
  - Upstream producers:
    - RLCR cache log naming aligns with stop-hook log files such as `round-${CURRENT_ROUND}-codex-run.log` and `round-${round}-codex-review.log` referenced by `hooks/loop-codex-stop-hook.sh:930-932` and `hooks/loop-codex-stop-hook.sh:1250-1252`.
    - PR loop setup advertises `humanize monitor pr` as the operator monitor command (`scripts/setup-pr-loop.sh:105`, `README.md:176`).
  - Test callers source this file directly, including parser robustness tests and monitor e2e tests (`tests/robustness/test-goal-tracker-robustness.sh:21-22`, `tests/robustness/test-git-operations-robustness.sh:17-19`, `tests/test-monitor-e2e-real.sh:148-152`, `tests/test-monitor-e2e-real.sh:776-793`).

- edge_cases_or_failure_modes:
  - If `scripts/lib/monitor-common.sh` is absent, the source step is optional, but monitor functions still call its helpers unguarded. Parser helpers remain usable; monitor modes would fail at runtime with missing functions.
  - `humanize_parse_goal_tracker` uses `|` as a field delimiter, so a goal summary containing a literal pipe can shift downstream array fields in the status bar.
  - `humanize_parse_git_status` returns an extra trailing message in the non-git case (`0|0|0|0|0|0|not a git repo`) while the normal contract documents six fields; current display ignores the extra field (`scripts/humanize.sh:168-170`, `scripts/humanize.sh:411-419`).
  - Very narrow terminals can make `max_display_len=$((term_width - 12))` negative, which may produce bad substring behavior in plan/goal truncation (`scripts/humanize.sh:428-439`).
  - RLCR log consistency checking may suppress log selection if review/run round numbering does not follow the script’s strict ordering assumption (`scripts/humanize.sh:330-337`).
  - RLCR handles missing current logs, deleted session dirs, log deletion, and log truncation/rotation by resetting current state and searching again (`scripts/humanize.sh:641-740`, `scripts/humanize.sh:777-830`).
  - PR `--once` registers EXIT/INT/TERM cleanup traps before returning early, so in a sourced interactive shell it can leave cleanup behavior installed until shell exit (`scripts/humanize.sh:1202-1213`, `scripts/humanize.sh:1215-1292`).
  - PR missing-state fallback emits fewer fields than the main parser normally emits, which can leave model/effort/start display fields empty in degraded paths (`scripts/humanize.sh:1031-1033`).
  - The PR one-shot recent-file listing pipes raw `find` output into `xargs ls`, so unusual whitespace in filenames would be fragile (`scripts/humanize.sh:1268-1274`).

- validation_or_tests:
  - Read-only syntax validation run for this research: `bash -n scripts/humanize.sh` returned `OK`.
  - Existing parser coverage:
    - Goal tracker robustness tests source production `scripts/humanize.sh` and cover standard table/list formats, mixed AC formats, large counts, special characters, empty/malformed/truncated/binary files, open issues, deferred tasks, and long-goal truncation (`tests/robustness/test-goal-tracker-robustness.sh:5-11`, `tests/robustness/test-goal-tracker-robustness.sh:237-371`, `tests/robustness/test-goal-tracker-robustness.sh:501-521`).
    - Git robustness tests source production `scripts/humanize.sh` and cover clean/dirty/untracked states plus normal, detached, rebase, merge, shallow, non-git, and permission scenarios (`tests/robustness/test-git-operations-robustness.sh:5-10`, `tests/robustness/test-git-operations-robustness.sh:377-495`).
  - Existing monitor coverage:
    - E2E monitor tests run the real `_humanize_monitor_codex` for directory deletion and SIGINT under bash/zsh, and run the real PR monitor in one-shot and interactive SIGINT paths (`tests/test-monitor-e2e-real.sh:5-9`, `tests/test-monitor-e2e-real.sh:59-63`, `tests/test-monitor-e2e-real.sh:234-237`, `tests/test-monitor-e2e-real.sh:376-379`, `tests/test-monitor-e2e-real.sh:686-793`, `tests/test-monitor-e2e-real.sh:827-922`).
    - Runtime tests inspect graceful stop and terminal restoration behavior (`tests/test-monitor-runtime.sh:6`, `tests/test-monitor-runtime.sh:274-320`, `tests/test-monitor-runtime.sh:391-419`).
    - Zsh safety tests source `humanize.sh` under zsh and exercise empty/dotfile-only directory behavior to protect against glob failures (`tests/test-zsh-monitor-safety.sh:3`, `tests/test-zsh-monitor-safety.sh:63-76`, `tests/test-zsh-monitor-safety.sh:208-235`).

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1/1 evidence section present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`