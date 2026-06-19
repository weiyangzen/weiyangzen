# agent_16 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`

## Item Evidence

### HZ-016 `directory` `prompt-template/codex`
- cursor: `[_]`
- core_role: Codex-side review contract templates for the RLCR loop. The directory is flat and was inspected recursively: `code-review-phase.md`, `commit-history-section.md`, `full-alignment-review.md`, `goal-tracker-update-section.md`, and `regular-review.md`.
- algorithmic_behavior: `hooks/loop-codex-stop-hook.sh` builds review prompts by loading the goal-tracker update section, deciding whether the current round is a full-alignment checkpoint, rendering commit history, then choosing `codex/full-alignment-review.md` or `codex/regular-review.md` (`hooks/loop-codex-stop-hook.sh:1009`, `:1015`, `:1035`, `:1062`, `:1093`, `:1111`). The code-review audit template documents the later `codex review --base` phase and its severity-marker transition (`prompt-template/codex/code-review-phase.md:14`).
- inputs_outputs_state: Inputs are rendered placeholders such as `PLAN_FILE`, `SUMMARY_CONTENT`, `GOAL_TRACKER_FILE`, `COMMIT_HISTORY_SECTION`, `REVIEW_RESULT_FILE`, and round metadata. Outputs are `round-N-review-prompt.md`, audit prompts, and review instructions that direct Codex to write `round-N-review-result.md` (`hooks/loop-codex-stop-hook.sh:1003`). State is read from loop files and git history, then turned into review directives.
- gates_or_invariants: Regular review requires plan reading, goal alignment, finding classification, and a mandatory `Mainline Progress Verdict` line (`prompt-template/codex/regular-review.md:35`, `:49`, `:56`). Full alignment adds AC audit, deferred-item audit, drift audit, historical stagnation check, and a hard rule that completion is only valid when all original plan tasks and ACs are fully met (`prompt-template/codex/full-alignment-review.md:21`, `:52`, `:77`, `:102`, `:112`). Goal-tracker updates must never modify the immutable section (`prompt-template/codex/goal-tracker-update-section.md:10`).
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh` single-pass rendering (`hooks/lib/template-loader.sh:48`) and the stop hook prompt assembly. It coordinates with `.humanize/rlcr/<timestamp>/goal-tracker.md`, round summaries, review results, git log output, and docs path references.
- edge_cases_or_failure_modes: Missing templates fall back to inline fallback prompts (`hooks/loop-codex-stop-hook.sh:1055`, `:1067`, `:1080`). Invalid or corrupted `full_review_round` defaults to 5 (`hooks/loop-codex-stop-hook.sh:1018`). Missing or non-ancestor base commit causes commit history to fall back to recent branch commits with an annotation (`hooks/loop-codex-stop-hook.sh:1035`).
- validation_or_tests: Template loading and commit-history behavior are covered by `tests/test-commit-history-section.sh` and `tests/test-templates-comprehensive.sh` references; stop-hook tests exercise prompt/review flow. This item was inspected, not executed.
- skip_candidate: `no`

### HZ-046 `file` `hooks/loop-post-bash-hook.sh`
- cursor: `[_]`
- core_role: One-shot PostToolUse Bash hook that binds the just-created RLCR loop to the leader Claude session by recording `session_id` into `state.md`.
- algorithmic_behavior: Reads hook JSON from stdin (`hooks/loop-post-bash-hook.sh:26`), resolves project root without using `pwd` fallback (`:29`), checks `.humanize/.pending-session-id` (`:37`), reads target state path plus setup command signature (`:45`), verifies the Bash command is a real setup invocation (`:61`), extracts `session_id` (`:109`), patches only an empty `session_id:` line with awk (`:120`), then removes the signal file (`:137`).
- inputs_outputs_state: Inputs are PostToolUse JSON fields `.tool_input.command` and `.session_id`, the pending signal file, and the target state file. Output is an updated `state.md` line such as `session_id: <id>` plus deletion of `.humanize/.pending-session-id`. Setup creates the empty `session_id:` state field and signal file at `scripts/setup-rlcr-loop.sh:896` and `:909`.
- gates_or_invariants: No signal means no-op (`hooks/loop-post-bash-hook.sh:40`). Empty or stale state target removes the signal and exits (`:55`). Non-setup Bash commands do not consume the signal (`:103`). Missing command or missing session id leaves the signal for a later valid event (`:71`, `:115`). Existing `session_id` is not overwritten (`:124`).
- dependencies_and_callers: Registered as a PostToolUse Bash hook in `hooks/hooks.json:52`. Depends on `jq` for JSON extraction, `hooks/lib/project-root.sh` for deterministic root resolution, and the setup script signal format. The hook is part of the session isolation chain used by validators and stop hook session filtering.
- edge_cases_or_failure_modes: Normalizes doubled slashes before signature comparison to handle templated paths (`hooks/loop-post-bash-hook.sh:75`). Accepts quoted/unquoted invocations and whitespace boundaries, including tabs (`:85`). Rejects echo-with-path, basename-only, and quoted-prefix concatenation false positives (`:94`). If `jq` is unavailable while a command signature is present, command extraction stays empty and the hook exits without consuming the signal.
- validation_or_tests: `tests/test-session-id.sh` verifies recording and signal deletion (`tests/test-session-id.sh:139`), preservation on non-setup command (`:488`), false-positive rejection (`:849`), quoted-prefix rejection (`:906`), and tab-delimited acceptance (`:989`, `:1035`).
- skip_candidate: `no`

### HZ-076 `file` `tests/test-codex-review-merge.sh`
- cursor: `[_]`
- core_role: Executable specification for the Codex code-review log scanner, `detect_review_issues`, which decides whether review phase continues, blocks, or can enter finalize.
- algorithmic_behavior: The test states the algorithm directly: scan only the last 50 log lines, find the first `[P0-9]` marker within the first 10 characters, extract from that line to EOF, return no-issue when absent, and hard-error on missing/empty log (`tests/test-codex-review-merge.sh:11`). Implementation matches this in `hooks/lib/loop-common.sh:719`, `:755`, `:761`, `:773`, `:786`.
- inputs_outputs_state: Inputs are `CACHE_DIR/round-N-codex-review.log`, `LOOP_DIR`, and a round number. Outputs are stdout content headed by Codex review issues, return code 0 for issues, 1 for no issues, 2 for missing/empty log, and `LOOP_DIR/round-N-review-result.md` when issues are found (`hooks/lib/loop-common.sh:740`, `:777`, `:782`).
- gates_or_invariants: Severity markers not in the first 10 characters are ignored (`tests/test-codex-review-merge.sh:86`). Markers outside the last-50-line window are ignored (`:202`). Exactly 50 lines includes line 1 (`:335`). Multiple findings extract from the first finding through the end (`:232`).
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` (`tests/test-codex-review-merge.sh:41`). The stop hook calls the scanner after `codex review` and treats return code 2 as blocking retry, code 0 as continue review, and code 1 as finalize (`hooks/loop-codex-stop-hook.sh:1300`, `:1306`, `:1309`, `:1313`).
- edge_cases_or_failure_modes: Missing log and empty log both hard-fail (`tests/test-codex-review-merge.sh:136`, `:155`). Debug text containing `[P1]` after column 10 is intentionally ignored to avoid false positives (`:89`). Large logs are bounded by tail scanning to avoid old debug matches and large-argument issues (`hooks/lib/loop-common.sh:729`).
- validation_or_tests: The file is itself the validation artifact with 12 cases covering marker position, no marker, missing/empty logs, long logs, multiple findings, dash-prefix format, result-file creation, and exact 50-line behavior. It was inspected, not executed.
- skip_candidate: `no`

### HZ-106 `file` `tests/test-zsh-monitor-safety.sh`
- cursor: `[_]`
- core_role: Executable zsh safety spec ensuring Humanize monitor logic does not trigger zsh `nomatch` failures when loop/cache directories are empty or contain no matching files.
- algorithmic_behavior: Runs under zsh (`tests/test-zsh-monitor-safety.sh:1`), sources `scripts/humanize.sh`, and simulates monitor helper behavior using `find`-based iteration over `.humanize/rlcr` sessions, state files, and cache logs (`:71`, `:99`, `:172`, `:221`). It also demonstrates that the old glob pattern could fail under zsh while the new `find` pattern does not (`:295`, `:314`).
- inputs_outputs_state: Inputs are a temporary project root, `.humanize/rlcr` session directories/files, `XDG_CACHE_HOME`, and the zsh shell environment. Outputs are pass/fail counters and process exit 0 or 1. No persistent repository state is modified.
- gates_or_invariants: The monitor must source without “no matches found” (`tests/test-zsh-monitor-safety.sh:72`). Empty loop dirs, dotfile-only dirs, no `*-state.md`, empty cache dirs, and full timestamp-session iteration must complete without glob errors (`:80`, `:127`, `:160`, `:208`, `:240`). Test 7 verifies it is actually running under zsh (`:276`).
- dependencies_and_callers: The real monitor sources `scripts/lib/monitor-common.sh` (`scripts/humanize.sh:6`) and wraps `monitor_find_latest_session`, `_find_latest_codex_log`, and `monitor_find_state_file` (`scripts/humanize.sh:279`, `:291`, `:377`). Shared helpers use `find` explicitly to avoid zsh glob errors (`scripts/lib/monitor-common.sh:49`, `:176`).
- edge_cases_or_failure_modes: Empty cache/session paths return empty strings or `|unknown` instead of failing (`scripts/lib/monitor-common.sh:44`, `:157`, `:187`). `scripts/humanize.sh` enables zsh `ksharrays` locally for bash-compatible array indexing inside monitor code (`scripts/humanize.sh:262`).
- validation_or_tests: The script contains eight zsh-focused tests and was inspected, not executed.
- skip_candidate: `no`

### HZ-136 `file` `prompt-template/block/plan-backup-protected.md`
- cursor: `[_]`
- core_role: User-facing block template enforcing that the loop-local `plan.md` backup is read-only during RLCR execution.
- algorithmic_behavior: The template explains that `.humanize/rlcr/<session>/plan.md` is a backup of the original plan and “cannot be modified” (`prompt-template/block/plan-backup-protected.md:3`). Validators load it when Write, Edit, or Bash would modify the backup.
- inputs_outputs_state: Input is an attempted operation targeting a loop `plan.md`. Output is the rendered block reason and validator exit code 2. State is deliberately unchanged; the backup remains an immutable plan anchor.
- gates_or_invariants: Write validator blocks `plan.md` in `.humanize/rlcr/` (`hooks/loop-write-validator.sh:240`). Edit validator blocks the same backup (`hooks/loop-edit-validator.sh:190`). Bash validator uses `command_modifies_file` against `.humanize/rlcr/.../plan.md` (`hooks/loop-bash-validator.sh:496`).
- dependencies_and_callers: Loaded via `load_and_render_safe` from `hooks/lib/template-loader.sh`; called by write/edit/bash validators. It coordinates with setup, which copies or creates the loop backup plan at `scripts/setup-rlcr-loop.sh:829`.
- edge_cases_or_failure_modes: The block applies to the loop backup, not necessarily the original plan file. Bash protection depends on command-pattern detection, while Write/Edit rely on resolved file path and basename checks.
- validation_or_tests: Plan-file hook and finalize tests reference this protection path; direct implementation references are in the three validators above. This file is a core gate message, not a standalone executable.
- skip_candidate: `no`

### HZ-166 `file` `prompt-template/claude/push-every-round-note.md`
- cursor: `[_]`
- core_role: Prompt fragment that carries the `--push-every-round` policy into Claude’s next-round instructions.
- algorithmic_behavior: The template adds a direct instruction to push commits to remote after each round when the flag is enabled (`prompt-template/claude/push-every-round-note.md:2`). `hooks/loop-codex-stop-hook.sh` appends it to generated next-round prompts only when `PUSH_EVERY_ROUND` is true (`hooks/loop-codex-stop-hook.sh:2167`).
- inputs_outputs_state: Input is the state/config value `push_every_round`, written by setup from the CLI flag (`scripts/setup-rlcr-loop.sh:46`, `:887`). Output is appended prompt text; there is no direct git push execution in this template.
- gates_or_invariants: Conditional append only when enabled. If the template is missing, the stop hook falls back to “Also push your changes after committing” (`hooks/loop-codex-stop-hook.sh:2169`). Initial round prompt uses an inline equivalent note when setup sees `PUSH_EVERY_ROUND=true` (`scripts/setup-rlcr-loop.sh:1433`).
- dependencies_and_callers: Depends on template loading through `load_template` and on state parsing in the stop hook. Coordinates with setup-generated prompts and subsequent round prompt generation.
- edge_cases_or_failure_modes: This is an instruction surface, not an enforcement gate; actual push success must be validated elsewhere. Initial-round behavior does not load this file directly, so drift between the inline setup note and this template could produce inconsistent wording.
- validation_or_tests: Covered indirectly by setup/prompt generation tests and template reference checks. No standalone executable test is assigned to this fragment.
- skip_candidate: `no`

### HZ-196 `file` `tests/robustness/test-setup-scripts-robustness.sh`
- cursor: `[_]`
- core_role: Broad executable robustness spec for `scripts/setup-rlcr-loop.sh`, the setup state machine that initializes RLCR loop state, validates inputs, and creates first-round artifacts.
- algorithmic_behavior: The test constructs isolated git repos and invokes setup through `run_rlcr_setup` with `CLAUDE_PROJECT_DIR` set (`tests/robustness/test-setup-scripts-robustness.sh:82`). It covers argument parsing, plan validation, YAML safety, git repo checks, active-loop exclusion, symlink rejection, skip-impl bootstrap, timeout behavior, full-review cadence validation, and dependency checks.
- inputs_outputs_state: Inputs include CLI args, plan files, git repo state, mocked `codex`, `jq`, and timeout tools. Outputs are exit codes/messages plus loop artifacts such as `state.md`, `.pending-session-id`, `.review-phase-started`, `goal-tracker.md`, `round-0-summary.md`, `round-0-contract.md`, and `round-0-prompt.md` (`tests/robustness/test-setup-scripts-robustness.sh:901`, `:919`, `:943`, `:959`).
- gates_or_invariants: Setup rejects missing/duplicate plan args, invalid numerics, unknown options, short/comment-only plans, spaces/metacharacters/absolute paths, YAML-unsafe branch/model values, non-git repos, repos without commits, tracked plans without `--track-plan-file`, dirty worktrees, active loops, symlinked plan paths, and missing dependencies (`tests/robustness/test-setup-scripts-robustness.sh:102`, `:205`, `:230`, `:286`, `:357`, `:418`, `:473`, `:502`, `:540`, `:1059`).
- dependencies_and_callers: Directly targets `scripts/setup-rlcr-loop.sh`, which validates dependencies (`scripts/setup-rlcr-loop.sh:340`), mutual exclusion (`:369`), optional skip-impl plan behavior (`:408`), git repo state (`:433`), plan path/content safety (`:455`, `:618`), branch/model safety (`:686`, `:702`), clean working tree (`:723`), base branch selection (`:748`), state creation (`:880`), signal creation (`:909`), and prompt/tracker generation (`:929`, `:1195`).
- edge_cases_or_failure_modes: Timeout zero is currently accepted because numeric validation allows `0` (`tests/robustness/test-setup-scripts-robustness.sh:657`). Very large timeouts are accepted (`:675`). Timeout mocks simulate git operation failure (`:695`). `.humanizeconfig` remains dirty and blocks setup, unlike ignored runtime `.humanize/` state (`:431`). Some YAML-unsafe branch behavior depends on git version support for such branch names (`:370`).
- validation_or_tests: The file is itself the validation suite with 49 named tests and a summary emitted by `print_test_summary` (`tests/robustness/test-setup-scripts-robustness.sh:1191`). It was inspected, not executed.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 7 item-evidence section headings present exactly once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`