# agent_175 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-175 `file` `scripts/lib/monitor-skill.sh`
- cursor: `[_]`
- core_role:
  - Provides `_humanize_monitor_skill`, the CLI monitor implementation behind `humanize monitor skill`, `humanize monitor codex`, and `humanize monitor gemini`.
  - It is sourced by [scripts/humanize.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/humanize.sh:1243) and dispatched from the `monitor` subcommand cases at [scripts/humanize.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/humanize.sh:1196).
  - Its algorithmic responsibility is read-only observation of `.humanize/skill` invocations produced by `ask-codex.sh` and `ask-gemini.sh`: it discovers invocation directories, classifies status, selects the best output/log file, renders aggregate status, and optionally tails live output.

- algorithmic_behavior:
  - Entrypoint starts at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:18). It initializes monitor state, parses `--once`, and parses `--tool-filter <codex|gemini>` without rejecting unknown filters; an unknown filter simply matches no non-unknown tool directories.
  - It requires `.humanize/skill` relative to the current directory, returning an error if absent at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:43). This is a current-working-directory contract, not a script-location contract.
  - `_skill_get_tool` reads `tool` from `metadata.md` first, then falls back to `- Tool:` in `input.md`, otherwise returns `unknown` at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:53).
  - `_skill_passes_filter` allows all directories with no filter, exact matches for codex/gemini filters, and treats legacy `unknown` entries as codex when filtering codex at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:68).
  - `_skill_list_dirs_sorted` scans only immediate children of `.humanize/skill`, keeps names matching `YYYY-MM-DD_HH-MM-SS...`, applies the tool filter, and sorts reverse lexicographically so timestamp-style names become newest-first at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:79).
  - `_skill_find_best_invocation` chooses the newest invocation with a non-empty watchable file; if none has content, it falls back to the newest directory, even with no output yet at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:100).
  - `_skill_count_stats` treats invocations lacking `metadata.md` as running and classifies completed invocations by YAML `status` values `success`, `error`, `timeout`, and `empty_response` at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:121).
  - `_skill_find_monitored_file` prefers live cache logs for running invocations and project `output.md` for completed invocations. It supports tool-specific cache prefixes `codex-run` and `gemini-run`, plus legacy cross-prefix fallback at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:169).
  - `--once` mode prints aggregate counts, focused invocation metadata, watched output content, and up to ten recent invocations, then exits at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:339).
  - Interactive mode switches to the terminal alternate screen, sets a scroll region below a fixed status bar, redraws every two seconds, and restarts `tail -f` whenever the focused invocation or watched file changes at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:428).

- inputs_outputs_state:
  - Inputs are CLI flags, current working directory, `.humanize/skill/<timestamp...>/input.md`, optional `metadata.md`, optional `output.md`, optional local `cache/`, and optional global cache under `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/<sanitized-project-root>/skill-<unique-id>`.
  - Producer contract confirmed in [scripts/ask-codex.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/ask-codex.sh:205): codex writes `.humanize/skill/<unique-id>`, cache files `codex-run.cmd/out/log`, `input.md` with `- Tool: codex`, and `metadata.md` statuses on timeout/error/empty/success.
  - Gemini mirrors the same shape with `gemini-run.cmd/out/log` and `- Tool: gemini` in [scripts/ask-gemini.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/ask-gemini.sh:187).
  - Outputs are terminal text only: an error/summary in `--once`, or an alternate-screen live dashboard plus `tail -f` stream in interactive mode. The assigned file does not write repository state.
  - Runtime state is local shell state: `current_skill_dir`, `current_file`, `TAIL_PID`, `monitor_running`, and `cleanup_done`. State transition is directory/file focus change -> stop old tail -> redraw -> start new tail at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:493).

- gates_or_invariants:
  - Gate: `.humanize/skill` must exist before any monitoring begins; otherwise return nonzero with a setup hint.
  - Gate: valid invocation directories must match the timestamp prefix regex; nonmatching children are ignored.
  - Invariant: missing `metadata.md` means running; completed state is inferred only from `metadata.md`.
  - Invariant: cache path derivation uses `git rev-parse --show-toplevel` or `pwd`, then sanitizes with the same character replacement used by producers at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:156).
  - Invariant: running invocations prefer stderr/log because live progress is likely there; completed invocations prefer final project-local `output.md`.
  - Invariant: cleanup is idempotent through `cleanup_done`, and both bash and zsh signal handling paths restore terminal state and stop the background tail at [scripts/lib/monitor-skill.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-skill.sh:449).

- dependencies_and_callers:
  - Caller surface: README documents `humanize monitor skill`, `humanize monitor codex`, and `humanize monitor gemini` at [README.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/README.md:64).
  - Dispatch/source path: [scripts/humanize.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/humanize.sh:1203) calls `_humanize_monitor_skill`, and [scripts/humanize.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/humanize.sh:1243) sources this file.
  - Shared helper dependencies: `monitor_get_yaml_value` and `monitor_format_timestamp` come from [scripts/lib/monitor-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/scripts/lib/monitor-common.sh:201), and `humanize_split_to_array` is expected from `humanize.sh`.
  - External command dependencies: `find`, `sort`, `head`, `basename`, `sed`, `grep`, `git`, `tput`, `clear`, `tail`, `kill`, `wait`, and shell support for arrays/process substitution. zsh compatibility is partially handled with `ksharrays` and custom trap functions.
  - Data producers: `ask-codex.sh` and `ask-gemini.sh` create the monitored files and metadata; this monitor assumes their storage naming and status vocabulary.

- edge_cases_or_failure_modes:
  - Branch-relevant path concern: `skill_dir` is relative and `_skill_find_cache_dir` uses `git rev-parse` or `pwd`, but it does not canonicalize via `realpath`. If invoked from a symlinked checkout path, cache lookup can diverge from the producer if producer root resolution canonicalizes differently.
  - `--tool-filter` lacks value validation; `--tool-filter` at end consumes an empty string and behaves like no filter because `tool_filter` becomes empty.
  - `_skill_find_best_invocation` can focus an older invocation with content while a newer invocation is still empty/running; this is intentional for watchability but can make the dashboard’s “focused” item differ from absolute newest.
  - Metadata parsing is simple frontmatter grep. Quoted values have quotes stripped, but complex YAML, duplicate keys, colons in key names, or multiline values are not supported.
  - Question extraction keeps only the first nonblank line under `## Question`, so multiline prompts are summarized but not fully shown.
  - Terminal-width arithmetic can become fragile on very narrow terminals because truncation subtracts fixed margins and then slices strings.
  - Interactive mode assumes `tput` works. In a non-TTY context, `--once` is the safer path and is the path covered by tests.
  - Tail cleanup uses `disown`, which may be unavailable or semantically different in some shells, but errors are suppressed.

- validation_or_tests:
  - Static syntax validation run read-only: `bash -n scripts/lib/monitor-skill.sh` returned success.
  - Dedicated tests exist in [tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-skill-monitor.sh:1). They cover missing directory, empty directory, completed invocation, mixed statuses, running invocation, recent list, question extraction, empty response, and ignoring non-timestamp directories.
  - Tests exercise `--once` mode only; the test header explicitly notes interactive mode is not tested because it requires a terminal at [tests/test-skill-monitor.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-skill-monitor.sh:5).
  - Producer-side tests for skill output/metadata/cache exist around [tests/test-ask-codex.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/use-realpath4everything/tests/test-ask-codex.sh:174), validating the contract consumed by this monitor.
  - I did not run the full test suite because this task is research-only and the workspace is read-only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 Item Evidence section present for the single assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`