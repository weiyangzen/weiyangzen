# agent_29 add-gen-plan-command 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 3
- source_commit: `ac298f55075b28c65b2e76f8f73831cf6fd5be2f`

## Item Evidence

### ADD_GEN_PLAN_COMMAND-HZ-029 `file` `scripts/humanize.sh`
- cursor: `[_]`
- core_role:
  - Runtime shell utility exposing `humanize monitor rlcr-loop`; it is an operator-facing monitor for the RLCR loop, not the loop scheduler/runner itself.
  - Main exported entrypoint is `humanize()` at `scripts/humanize.sh:806`, dispatching only `monitor rlcr-loop` to `_humanize_monitor_codex` at `scripts/humanize.sh:811`.
  - `_humanize_monitor_codex` starts at `scripts/humanize.sh:9` and renders a live terminal status bar plus incremental Codex log output for the latest `.humanize/rlcr` session.

- algorithmic_behavior:
  - Locates RLCR state under fixed local loop directory `.humanize/rlcr` (`scripts/humanize.sh:14`) and fails early if absent (`scripts/humanize.sh:20`).
  - Selects latest session by scanning direct child directories with timestamp names matching `YYYY-MM-DD_HH-MM-SS`; comparison is lexicographic on normalized timestamp names (`scripts/humanize.sh:27`, `scripts/humanize.sh:41`).
  - Selects latest Codex run log from external cache path `$HOME/.cache/humanize/<sanitized-project-path>/<session>/round-*-codex-run.log`, not from `.humanize/rlcr`, to avoid project context pollution (`scripts/humanize.sh:51`, `scripts/humanize.sh:57`, `scripts/humanize.sh:61`).
  - Resolves loop status through `_find_state_file`: `state.md` means active, otherwise first `*-state.md` yields a stop reason from filename, otherwise `unknown` (`scripts/humanize.sh:111`, `scripts/humanize.sh:123`, `scripts/humanize.sh:129`).
  - Parses `state.md` scalar fields by grepping keys: `current_round`, `max_iterations`, `codex_model`, `codex_effort`, `started_at`, `plan_file` (`scripts/humanize.sh:152`).
  - Parses `goal-tracker.md` into monitor counters: total criteria, completed criteria, active tasks, completed tasks, deferred tasks, open issues, and goal summary (`scripts/humanize.sh:170`). It supports both table/list acceptance criteria and table sections for task counts (`scripts/humanize.sh:188`, `scripts/humanize.sh:203`).
  - Parses repository git status with `git status --porcelain` plus `git diff --shortstat HEAD` for modified/added/deleted/untracked and insertion/deletion counts (`scripts/humanize.sh:254`).
  - Renders a fixed 11-line status bar using terminal cursor save/restore and scroll region separation (`scripts/humanize.sh:316`, `scripts/humanize.sh:455`).
  - Main monitoring loop updates status every 0.5 seconds in inner loops, tails the latest 50 log lines initially, then streams appended bytes with `tail -c +<offset>` (`scripts/humanize.sh:547`, `scripts/humanize.sh:673`, `scripts/humanize.sh:697`).
  - Auto-switches to newer sessions or newer round logs while running (`scripts/humanize.sh:718`, `scripts/humanize.sh:761`, `scripts/humanize.sh:785`).
  - Detects log truncation/rotation by file size shrinking and resets to search mode (`scripts/humanize.sh:704`).
  - Uses `find` instead of shell globs throughout session/log/state discovery to avoid zsh “no matches found” behavior (`scripts/humanize.sh:35`, `scripts/humanize.sh:71`, `scripts/humanize.sh:131`).

- inputs_outputs_state:
  - Inputs:
    - Current working directory, assumed to be a project root with `.humanize/rlcr`.
    - Session directories under `.humanize/rlcr/<timestamp>/`.
    - State files: `state.md` or `<stop_reason>-state.md`.
    - Optional `goal-tracker.md` inside current session.
    - Codex logs in `$HOME/.cache/humanize/<sanitized-project-path>/<timestamp>/round-*-codex-run.log`.
    - Current git repository status for display.
    - Terminal dimensions from `tput cols` and `tput lines`.
  - Outputs:
    - Terminal UI status bar and live log stream.
    - Usage/error messages for missing loop, missing session, or invalid command.
    - Exit code `1` for missing loop/session or bad CLI usage; graceful monitor stop returns through successful path.
  - State transitions:
    - `current_session_dir` moves from latest discovered timestamp to newer timestamp when found.
    - `current_file` moves from empty to latest log, from old log to newer round log, or to empty when deleted/truncated.
    - `last_size` advances with streamed bytes and resets on file/session switch or truncation.
    - `current_loop_status` transitions based on `state.md` vs `<reason>-state.md`.
    - `monitor_running` flips false on cleanup/trap, causing nested loops to break.

- gates_or_invariants:
  - Requires `.humanize/rlcr` to exist before monitoring starts (`scripts/humanize.sh:20`).
  - Requires at least one timestamp-shaped session directory; otherwise returns with instruction to start an RLCR loop (`scripts/humanize.sh:521`).
  - Session names must match strict timestamp regex; nonmatching child directories are ignored (`scripts/humanize.sh:42`, `scripts/humanize.sh:78`).
  - Log file selection is tied to the current project path after sanitization, so logs from other projects do not bleed into the display (`scripts/humanize.sh:59`).
  - Cleanup is idempotent through `cleanup_done` guard (`scripts/humanize.sh:478`).
  - Terminal scroll region is reset by `_restore_terminal` before exit (`scripts/humanize.sh:465`).
  - zsh compatibility invariant: `ksharrays` is enabled locally in monitor scope and `_split_to_array` branches on bash/zsh behavior (`scripts/humanize.sh:10`, `scripts/humanize.sh:302`).

- dependencies_and_callers:
  - Direct CLI caller is shell function `humanize monitor rlcr-loop` (`scripts/humanize.sh:811`).
  - RLCR loop setup script writes the state/session artifacts that this monitor reads: `scripts/setup-rlcr-loop.sh` writes `push_every_round` and initializes session material, with nearby prompt setup around `scripts/setup-rlcr-loop.sh:640`.
  - Codex stop hook writes cached logs under `$HOME/.cache/humanize/...`; the monitor’s cache path mirrors the comment in `hooks/loop-codex-stop-hook.sh:779`.
  - Tests source this script and run the real `_humanize_monitor_codex` in bash and zsh (`tests/test-monitor-e2e-real.sh:141`, `tests/test-monitor-e2e-real.sh:300`).
  - Related validation helpers in `hooks/lib/loop-common.sh` define `.humanize/rlcr` path detection for hook-level behavior, separate from this monitor (`hooks/lib/loop-common.sh:415`).

- edge_cases_or_failure_modes:
  - Missing `.humanize/rlcr` returns an explicit error and hint (`scripts/humanize.sh:20`).
  - Empty `.humanize/rlcr` or no valid timestamp sessions returns a specific “No session directories found” message (`scripts/humanize.sh:521`).
  - Missing `goal-tracker.md` is tolerated and displayed as zero counts plus “No goal tracker” (`scripts/humanize.sh:172`).
  - Missing state file is tolerated as `unknown` status (`scripts/humanize.sh:116`).
  - Missing log file enters polling mode and displays either “Waiting for log file” for active sessions or a no-log status for ended sessions (`scripts/humanize.sh:568`).
  - Deleting `.humanize/rlcr` during monitoring triggers graceful stop with terminal restoration (`scripts/humanize.sh:549`, `scripts/humanize.sh:501`).
  - Deleting the current session or log switches to latest remaining session/log when possible; otherwise waits for future sessions (`scripts/humanize.sh:620`, `scripts/humanize.sh:724`).
  - If a log rotates/truncates, it clears display and searches again (`scripts/humanize.sh:704`).
  - `find` plus explicit directory/file guards reduce zsh glob failures and stale path races (`scripts/humanize.sh:37`, `scripts/humanize.sh:90`, `scripts/humanize.sh:134`).
  - Potential weakness: `_find_state_file` chooses the first `*-state.md` returned by `find`, which is not sorted; multiple terminal state files could produce nondeterministic displayed stop reason (`scripts/humanize.sh:134`).
  - Potential weakness: round number extraction assumes filenames exactly `round-<num>-codex-run.log`; malformed names matching the broad `find` pattern poorly would affect numeric comparison (`scripts/humanize.sh:94`).

- validation_or_tests:
  - `tests/test-monitor-e2e-real.sh` runs the real monitor in bash, creates a fake `.humanize/rlcr` session plus fake cache log, deletes `.humanize/rlcr`, and verifies graceful exit, no glob errors, cleanup message, source scroll reset, and exit code zero (`tests/test-monitor-e2e-real.sh:59`, `tests/test-monitor-e2e-real.sh:161`, `tests/test-monitor-e2e-real.sh:184`).
  - Same test covers zsh execution path and no zsh glob errors (`tests/test-monitor-e2e-real.sh:230`, `tests/test-monitor-e2e-real.sh:341`).
  - `tests/test-humanize-escape.sh` includes direct validation of the `find`-based iteration patterns used by `humanize.sh` for empty dirs, dotfiles-only dirs, missing `*-state.md`, state-file detection, and latest session detection (`tests/test-humanize-escape.sh:194`, `tests/test-humanize-escape.sh:248`, `tests/test-humanize-escape.sh:296`).
  - I did not run tests in this research pass because the instruction was read-only notes only.

- skip_candidate: `no`

### ADD_GEN_PLAN_COMMAND-HZ-059 `file` `prompt-template/block/git-add-humanize.md`
- cursor: `[_]`
- core_role:
  - User-facing block template shown when a Bash validation hook detects a `git add` command that could add `.humanize/` loop state to version control.
  - It defines the review/repair contract for this gate: use specific paths or patch mode; avoid direct or broad adds involving `.humanize`.

- algorithmic_behavior:
  - The template itself is declarative text, but participates in enforcement through `git_add_humanize_blocked_message` in `hooks/lib/loop-common.sh`.
  - The hook-side algorithm lowercases the command, splits shell segments on operators, finds `git ... add`, extracts add arguments, strips quotes, then blocks direct `.humanize` references, force+broad scope, all-scope adds when `.humanize` exists, and broad-scope adds when `.humanize` is not ignored (`hooks/lib/loop-common.sh:443`, `hooks/lib/loop-common.sh:467`, `hooks/lib/loop-common.sh:480`, `hooks/lib/loop-common.sh:511`, `hooks/lib/loop-common.sh:523`, `hooks/lib/loop-common.sh:529`).
  - If blocked, `git_add_humanize_blocked_message` loads this template via `load_and_render_safe "$TEMPLATE_DIR" "block/git-add-humanize.md"` with a built-in fallback (`hooks/lib/loop-common.sh:541`, `hooks/lib/loop-common.sh:568`).
  - `hooks/loop-bash-validator.sh` calls `git_adds_humanize "$COMMAND_LOWER"` and exits with code `2` after printing the template when the gate fires (`hooks/loop-bash-validator.sh:75`, `hooks/loop-bash-validator.sh:81`).

- inputs_outputs_state:
  - Inputs:
    - Current Bash command string from hook context, lowercased before validation.
    - Current working directory presence of `.humanize`.
    - Git ignore result for `.humanize` via `git check-ignore`.
    - Template directory path used by `load_and_render_safe`.
  - Outputs:
    - Markdown block beginning “Git Add Blocked: .humanize Protection” (`prompt-template/block/git-add-humanize.md:1`).
    - Allowed command examples: specific file, `src/`, patch mode (`prompt-template/block/git-add-humanize.md:8`).
    - Blocked command examples: direct `.humanize`, `git add -A`, `git add --all`, `git add .`, forced broad add (`prompt-template/block/git-add-humanize.md:16`).
    - Hook exit code `2` through caller on blocked command (`hooks/loop-bash-validator.sh:81`).
  - State:
    - Does not mutate repository or loop state; it preserves `.humanize/` by preventing staging.

- gates_or_invariants:
  - `.humanize/` is local loop state and must not be committed (`prompt-template/block/git-add-humanize.md:3`).
  - Direct `.humanize` path references are blocked regardless of ignore state (`hooks/lib/loop-common.sh:480`).
  - Force plus broad scope is blocked because it bypasses ignore protection (`hooks/lib/loop-common.sh:511`).
  - `git add -A` and `git add --all` are blocked when `.humanize` exists (`hooks/lib/loop-common.sh:518`, `hooks/lib/loop-common.sh:523`).
  - Broad `git add .` or `git add *` is blocked only when `.humanize` exists and is not ignored, while the template still recommends specific paths (`hooks/lib/loop-common.sh:529`).
  - The template assumes `.humanize` is already in `.gitignore` (`prompt-template/block/git-add-humanize.md:4`), while the underlying gate still defends force-add and unsafe all-add cases.

- dependencies_and_callers:
  - Loaded by `git_add_humanize_blocked_message` in `hooks/lib/loop-common.sh:541`.
  - Invoked by `hooks/loop-bash-validator.sh:81` during Bash command validation.
  - Shares conceptual responsibility with `prompt-template/block/git-not-clean-humanize-local.md`, which explains untracked `.humanize` during git cleanliness checks; this assigned template is specifically for staging prevention.
  - Covered by `tests/test-humanize-escape.sh`, which sources `hooks/lib/loop-common.sh` and exercises `git_adds_humanize`.

- edge_cases_or_failure_modes:
  - Template text is static; if hook logic changes, examples may drift. Current examples are a subset of actual blocked cases, not an exhaustive list.
  - The line “already listed in `.gitignore`” may be inaccurate in a project where `.humanize` exists but is not ignored; however, hook logic detects that case and blocks broad adds (`prompt-template/block/git-add-humanize.md:4`, `hooks/lib/loop-common.sh:529`).
  - The validator lowercases input, so uppercase path variants become lowercase for matching. That is consistent for `.humanize`, but could blur case-sensitive path distinctions in exotic repos.
  - Shell parsing is regex-based, not a full shell parser; complex quoting/escaping could escape or over-trigger, though common chained commands and quoted paths are tested.

- validation_or_tests:
  - `tests/test-humanize-escape.sh` validates direct path variants, quoted variants, force variants, all-add variants, chained commands, `git -C`, allowed specific paths, patch mode, and similarly named non-loop files (`tests/test-humanize-escape.sh:77`, `tests/test-humanize-escape.sh:89`, `tests/test-humanize-escape.sh:102`, `tests/test-humanize-escape.sh:121`, `tests/test-humanize-escape.sh:146`, `tests/test-humanize-escape.sh:157`, `tests/test-humanize-escape.sh:168`).
  - The test specifically asserts `.humanizeconfig`, `.humanize-backup`, and `src/.humanizerc` are allowed to avoid overblocking (`tests/test-humanize-escape.sh:189`).
  - I did not run tests in this research pass because the instruction was read-only notes only.

- skip_candidate: `no`

### ADD_GEN_PLAN_COMMAND-HZ-089 `file` `prompt-template/claude/push-every-round-note.md`
- cursor: `[_]`
- core_role:
  - Small Claude prompt footer used when an RLCR loop is configured with `--push-every-round`.
  - It changes the round contract from local commits only to commit plus remote push after every round.

- algorithmic_behavior:
  - Template content is one note: when `--push-every-round` is enabled, the agent must push commits to remote after each round (`prompt-template/claude/push-every-round-note.md:2`).
  - Initial round prompt generation in `scripts/setup-rlcr-loop.sh` appends equivalent text directly when `PUSH_EVERY_ROUND` is true (`scripts/setup-rlcr-loop.sh:655`).
  - Subsequent prompt generation in `hooks/loop-codex-stop-hook.sh` loads this assigned template and appends it to the next Claude prompt only when `PUSH_EVERY_ROUND` is true (`hooks/loop-codex-stop-hook.sh:1094`, `hooks/loop-codex-stop-hook.sh:1096`, `hooks/loop-codex-stop-hook.sh:1100`).
  - If the template is missing or empty, the stop hook falls back to “Also push your changes after committing” (`hooks/loop-codex-stop-hook.sh:1097`).
  - Enforcement is not only instructional: the stop hook checks for unpushed commits when `PUSH_EVERY_ROUND` is true and blocks stopping if local branch is ahead of remote (`hooks/loop-codex-stop-hook.sh:489`). It renders `prompt-template/block/unpushed-commits.md` for that gate (`hooks/loop-codex-stop-hook.sh:501`).

- inputs_outputs_state:
  - Inputs:
    - Loop setup flag `--push-every-round`, parsed into `PUSH_EVERY_ROUND=true` (`scripts/setup-rlcr-loop.sh:148`).
    - State field `push_every_round` written into loop state (`scripts/setup-rlcr-loop.sh:492`) and later parsed as `STATE_PUSH_EVERY_ROUND`.
    - Current branch and upstream ahead count for enforcement in stop hook.
  - Outputs:
    - Appended note in next Claude prompt requiring push after committing.
    - If ignored, stop hook can output an unpushed-commits block telling the agent to push current branch.
  - State transitions:
    - Setup-time CLI flag becomes persisted state.
    - Persisted state controls whether future round prompts include the push note.
    - If the agent commits without pushing, loop exit/finalization is blocked until remote catches up.

- gates_or_invariants:
  - The note is conditional; it must not appear when `--push-every-round` is false.
  - When enabled, every round’s prompt should carry push instruction and the stop hook should reject unpushed local commits.
  - The push gate is paired with the default opposite gate in `hooks/loop-bash-validator.sh`: when push-every-round is false, `git push` is blocked during the loop (`hooks/loop-bash-validator.sh:63`).
  - This template is an instruction surface, while the stop hook provides the hard invariant.

- dependencies_and_callers:
  - Appended to next-round Claude prompts by `hooks/loop-codex-stop-hook.sh:1096`.
  - Setup round uses hardcoded equivalent text in `scripts/setup-rlcr-loop.sh:655`; that means this template governs later rounds, not necessarily the initial prompt.
  - Related enforcement template is `prompt-template/block/unpushed-commits.md`, which tells the agent to run `git push origin {{CURRENT_BRANCH}}` when ahead (`prompt-template/block/unpushed-commits.md:1`).
  - README documents `--push-every-round` as an option for `/humanize:start-rlcr-loop`.

- edge_cases_or_failure_modes:
  - The template says “push your commits to remote” but does not specify branch/upstream. Enforcement template later gives `git push origin {{CURRENT_BRANCH}}`.
  - Initial round does not load this template; it uses duplicated literal text in setup script. Wording drift is possible between round zero and later rounds.
  - If no upstream exists, the stop-hook ahead-count logic may need separate handling outside this template; the assigned file does not encode fallback instructions for missing upstream.
  - If remote push fails due to auth/network/rejection, the template provides no remediation; enforcement only keeps the loop blocked until commits are pushed.

- validation_or_tests:
  - Search evidence shows `PUSH_EVERY_ROUND` is parsed, persisted, used in setup prompt, used in stop hook prompt generation, and used for unpushed-commit blocking (`scripts/setup-rlcr-loop.sh:41`, `scripts/setup-rlcr-loop.sh:149`, `scripts/setup-rlcr-loop.sh:492`, `hooks/loop-codex-stop-hook.sh:489`, `hooks/loop-codex-stop-hook.sh:1095`).
  - `prompt-template/block/unpushed-commits.md` provides the enforcement-side user instruction when the push was not performed (`prompt-template/block/unpushed-commits.md:3`).
  - I did not run tests in this research pass because the instruction was read-only notes only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 3 unique assigned item sections present; item identifiers are only used in those section headers.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`