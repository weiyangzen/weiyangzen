# agent_14 impl-dccb-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `0fabd14f224c998e6dedd7cddaf57c479524700c`

## Item Evidence

### IMPL_DCCB_LOOP-HZ-014 `file` `hooks/loop-codex-stop-hook.sh`
- cursor: `[_]`
- core_role:  
  `hooks/loop-codex-stop-hook.sh` is the RLCR Stop hook implementation. It intercepts Claude Code Stop events, decides whether an RLCR loop is active, enforces pre-review gates, launches Codex as an independent reviewer, then either allows exit by removing loop state or blocks exit with the next-round prompt. It is wired as a Stop hook in `hooks/hooks.json:42-49`, before the separate DCCB stop hook at `hooks/hooks.json:50-53`. Although this branch is named `impl-dccb-loop`, this assigned file is RLCR-specific and uses `.humanize-rlcr.local`, not `.humanize-dccb.local`.

- algorithmic_behavior:  
  The hook reads the full Stop-hook JSON input from stdin into `HOOK_INPUT` at `hooks/loop-codex-stop-hook.sh:29`. It intentionally does not skip when `stop_hook_active` is already true, because blocked Stop events are the loop’s iteration mechanism; the controlling signals are active state presence, Codex `COMPLETE`, and max-iteration exhaustion at `hooks/loop-codex-stop-hook.sh:31-37`.

  Active-loop discovery starts from `CLAUDE_PROJECT_DIR` or `pwd`, then `.humanize-rlcr.local`, and delegates to `find_active_loop` from `hooks/lib/loop-common.sh` at `hooks/loop-codex-stop-hook.sh:43-50`. That helper only considers the newest timestamped loop directory and only returns it if it contains `rlcr-state.md`, explicitly avoiding revival of older “zombie” loops in `hooks/lib/loop-common.sh:11-33`. If no active loop exists, the hook exits `0` with no JSON block at `hooks/loop-codex-stop-hook.sh:52-55`.

  Before expensive Codex review, the hook applies several fast gates. It invokes `hooks/check-todos-from-transcript.py` with the hook input and blocks if the latest `TodoWrite` state has non-`completed` todos at `hooks/loop-codex-stop-hook.sh:65-99`; the helper parses Claude transcript JSONL formats and exits `1` when incomplete todos exist in `hooks/check-todos-from-transcript.py:17-84` and `hooks/check-todos-from-transcript.py:87-125`. It scans changed git files and blocks code/docs files over `MAX_LINES=2000` at `hooks/loop-codex-stop-hook.sh:108-197`. It then blocks dirty git worktrees at `hooks/loop-codex-stop-hook.sh:205-277`, including special `.humanize-rlcr.local` and other untracked-artifact guidance at `hooks/loop-codex-stop-hook.sh:215-245`. If `push_every_round: true` is present in state, it also blocks local commits ahead of upstream at `hooks/loop-codex-stop-hook.sh:279-315`.

  The state parser extracts YAML frontmatter from `rlcr-state.md` and reads `current_round`, `max_iterations`, `codex_model`, `codex_effort`, `codex_timeout`, and `plan_file` at `hooks/loop-codex-stop-hook.sh:322-342`. It rejects a nonnumeric `current_round` by deleting the state file and allowing exit at `hooks/loop-codex-stop-hook.sh:344-349`, while a nonnumeric `max_iterations` is normalized to `42` at `hooks/loop-codex-stop-hook.sh:351-354`. The setup script that creates these fields is `scripts/setup-rlcr-loop.sh:223-234`.

  The hook requires the current round summary file before review. Missing `round-N-summary.md` returns a JSON Stop block asking Claude to write the summary at `hooks/loop-codex-stop-hook.sh:356-392`. On round `0`, it also requires `rlcr-tracker.md` to have non-placeholder Ultimate Goal, Acceptance Criteria, and Active Tasks content; placeholder detection and blocking are at `hooks/loop-codex-stop-hook.sh:394-465`.

  Max-iteration logic computes `NEXT_ROUND=current_round+1`; if `NEXT_ROUND > max_iterations`, it deletes `rlcr-state.md` and allows exit without Codex completion at `hooks/loop-codex-stop-hook.sh:467-477`.

  Review prompt generation writes `round-N-review-prompt.md` and expects `round-N-review-result.md` at `hooks/loop-codex-stop-hook.sh:491-495`. The prompt always embeds Claude’s summary and the original `plan_file`, and it instructs Codex to update `rlcr-tracker.md` itself when approving “Goal Tracker Update Request” changes at `hooks/loop-codex-stop-hook.sh:497-514`. Every fifth round by zero-based count, where `current_round % 5 == 4`, becomes a full alignment check at `hooks/loop-codex-stop-hook.sh:516-523`. Full alignment prompts require Acceptance Criteria audit, forgotten-item detection, deferral audit, stagnation review over recent rounds, and `STOP` on the final line if progress is stagnant at `hooks/loop-codex-stop-hook.sh:525-619`. Regular review prompts still require plan/summary review, goal alignment, and strict final-line `COMPLETE` only when all planned work and ACs are fully complete with no deferrals at `hooks/loop-codex-stop-hook.sh:621-681`.

  Codex execution writes debug command/stdout/stderr files under `$HOME/.cache/humanize/<sanitized-project>/<loop-timestamp>` at `hooks/loop-codex-stop-hook.sh:688-702`. It sources `scripts/portable-timeout.sh` if present, otherwise defines a smaller inline timeout wrapper at `hooks/loop-codex-stop-hook.sh:704-722`; the portable helper selects `gtimeout`, GNU `timeout`, Python, or no timeout in `scripts/portable-timeout.sh:9-71`. Codex args are `-m <model>`, optional `-c model_reasoning_effort=<effort>`, `--full-auto`, and `-C <project-root>` at `hooks/loop-codex-stop-hook.sh:724-731`. The hook runs `codex exec` with the review prompt content, writing stdout/stderr to cache files at `hooks/loop-codex-stop-hook.sh:749-755`.

  Result handling is strict. If Codex did not create the expected review result but stdout is nonempty, stdout is copied into the review result at `hooks/loop-codex-stop-hook.sh:757-765`. If no result exists after that, the hook blocks Stop with debug paths and the last 50 stderr lines at `hooks/loop-codex-stop-hook.sh:771-807`. The final nonempty review line is trimmed and compared exactly to `COMPLETE` or `STOP` at `hooks/loop-codex-stop-hook.sh:810-817`. Final `COMPLETE` removes `rlcr-state.md` and allows exit at `hooks/loop-codex-stop-hook.sh:819-828`. Final `STOP` also removes state and allows exit, with different stderr messaging for expected full-alignment versus unexpected non-alignment rounds at `hooks/loop-codex-stop-hook.sh:830-858`.

  If Codex finds issues, any other final line means continue the loop. The hook updates `current_round` in `rlcr-state.md` via a temp file and `mv` at `hooks/loop-codex-stop-hook.sh:864-867`, creates `round-NEXT-prompt.md`, embeds Codex review feedback, points Claude back to the plan and tracker, optionally adds post-alignment instructions, then returns JSON `"decision": "block"` with that next prompt as the reason at `hooks/loop-codex-stop-hook.sh:869-975`.

- inputs_outputs_state:  
  Inputs are Stop-hook stdin JSON, especially `transcript_path` consumed indirectly by `check-todos-from-transcript.py`; environment variables `CLAUDE_PROJECT_DIR`, `CODEX_TIMEOUT`, `HOME`, and plugin path context; the active loop directory under `.humanize-rlcr.local`; git repository state; the current `round-N-summary.md`; `rlcr-tracker.md`; and frontmatter in `rlcr-state.md`.

  Primary outputs are either no block with exit `0`, meaning Stop is allowed, or JSON from `jq` with `"decision": "block"`, `"reason"`, and `"systemMessage"` at each block point, for example incomplete todos at `hooks/loop-codex-stop-hook.sh:90-98`, dirty git at `hooks/loop-codex-stop-hook.sh:268-276`, missing summary at `hooks/loop-codex-stop-hook.sh:383-391`, failed Codex review at `hooks/loop-codex-stop-hook.sh:799-807`, and next-round feedback at `hooks/loop-codex-stop-hook.sh:966-974`.

  Persistent state transitions are centered on `.humanize-rlcr.local/<timestamp>/rlcr-state.md`. Active state is the presence of that file. Terminal transitions remove it on corrupted `current_round`, max-iteration exhaustion, Codex `COMPLETE`, or Codex `STOP` at `hooks/loop-codex-stop-hook.sh:345-348`, `hooks/loop-codex-stop-hook.sh:473-476`, `hooks/loop-codex-stop-hook.sh:820-827`, and `hooks/loop-codex-stop-hook.sh:831-857`. Nonterminal review failure increments `current_round`, writes the next prompt, and blocks Stop at `hooks/loop-codex-stop-hook.sh:864-975`.

  Per-round files are `round-N-prompt.md`, `round-N-summary.md`, `round-N-review-prompt.md`, and `round-N-review-result.md`, described by the file header at `hooks/loop-codex-stop-hook.sh:8-12` and produced/consumed throughout `hooks/loop-codex-stop-hook.sh:360`, `hooks/loop-codex-stop-hook.sh:491-493`, and `hooks/loop-codex-stop-hook.sh:870-876`. Debug state is written outside the project tree under `$HOME/.cache/humanize` at `hooks/loop-codex-stop-hook.sh:690-702`.

- gates_or_invariants:  
  The hook’s main invariant is that Claude may not leave the RLCR loop until a terminating condition removes `rlcr-state.md` or the loop has no active state. Review cannot run if native TodoWrite todos are incomplete, if changed code/docs files exceed 2000 lines, if git has uncommitted changes, if required pushes are pending, if the summary is missing, or if round-0 tracker setup is incomplete.

  Final-line review markers are exact. `COMPLETE` or `STOP` must be the last nonempty line after trimming whitespace; incidental text such as “cannot COMPLETE” will not terminate the loop because only the last line is compared at `hooks/loop-codex-stop-hook.sh:813-817`.

  Goal tracker mutability is split by round. Round 0 requires initialization by Claude, but after round 0, Codex is responsible for tracker mutations through reviewed update requests. The Stop hook enforces this in prompts at `hooks/loop-codex-stop-hook.sh:497-514` and `hooks/loop-codex-stop-hook.sh:898-907`, while sibling validators block direct writes after round 0 in `hooks/loop-write-validator.sh:97-105` and Bash bypasses in `hooks/loop-bash-validator.sh:79-94`.

  The loop treats deferrals as incomplete. Both full-alignment and regular review prompt text explicitly says `COMPLETE` is allowed only when all original tasks/ACs are done with no deferrals at `hooks/loop-codex-stop-hook.sh:613-618` and `hooks/loop-codex-stop-hook.sh:674-679`.

  The hook preserves local-only loop artifacts by warning against committing `.humanize-rlcr.local` at `hooks/loop-codex-stop-hook.sh:218-228`. It also depends on the broader validator set to keep prompt/state files from being modified by Claude; those are wired in `hooks/hooks.json:4-40`.

- dependencies_and_callers:  
  Direct caller wiring is `hooks/hooks.json`, which registers `hooks/loop-codex-stop-hook.sh` as a Claude Code Stop hook with a 7200-second timeout at `hooks/hooks.json:42-49`.

  Loop creation is handled by `/humanize:start-rlcr-loop`, which calls `scripts/setup-rlcr-loop.sh` via `commands/start-rlcr-loop.md:1-14`. The setup script validates the plan file, checks `codex` availability, creates `.humanize-rlcr.local/<timestamp>`, writes `rlcr-state.md`, initializes `rlcr-tracker.md`, and creates `round-0-prompt.md` in `scripts/setup-rlcr-loop.sh:159-234` and `scripts/setup-rlcr-loop.sh:236-423`.

  Manual cancellation is the removal of `rlcr-state.md`, described in `commands/cancel-rlcr-loop.md:7-24`. This matches the hook’s active-state model.

  Shared shell functions come from `hooks/lib/loop-common.sh`, especially `find_active_loop`, `to_lower`, and shared block-message/path helpers at `hooks/lib/loop-common.sh:15-52` and `hooks/lib/loop-common.sh:75-235`. The Stop hook directly uses `find_active_loop` and `to_lower`.

  The todo preflight depends on `hooks/check-todos-from-transcript.py`, which accepts hook JSON on stdin and reads the latest `TodoWrite` tool call from the transcript at `hooks/check-todos-from-transcript.py:87-125`.

  Runtime command dependencies include `bash`, `jq`, `python3`, `git`, `codex`, `sed`, `grep`, `wc`, `tail`, `mkdir`, `cp`, `mv`, and one of `gtimeout`, GNU `timeout`, Python timeout fallback, or no timeout. The timeout abstraction is `scripts/portable-timeout.sh:1-76`.

  Sibling hooks coordinate the state machine by preventing Claude from bypassing the Stop hook. `hooks/loop-write-validator.sh` blocks prompt writes, wrong summary locations/round numbers, state writes, and post-round-0 tracker writes in `hooks/loop-write-validator.sh:33-173`. `hooks/loop-bash-validator.sh` blocks shell redirection/edit bypasses for state, tracker, prompt, summary, and todos files, and blocks `git push` unless `push_every_round` is true in `hooks/loop-bash-validator.sh:48-126`.

- edge_cases_or_failure_modes:  
  If `.humanize-rlcr.local` contains multiple timestamped loop directories, only the newest directory can be active. If the newest directory lacks `rlcr-state.md` but an older one has it, the hook exits as inactive because `find_active_loop` intentionally ignores older directories.

  If `hooks/check-todos-from-transcript.py` is missing, the todo gate is skipped. If the helper receives invalid hook JSON or no `transcript_path`, it exits `0` and the Stop hook proceeds, per `hooks/check-todos-from-transcript.py:87-107`. If the helper fails with an exit code other than `1`, the Stop hook does not explicitly block; it only branches on `TODO_EXIT == 1` at `hooks/loop-codex-stop-hook.sh:72`.

  Large-file detection only inspects files present in `git status --porcelain`, not the whole repository. Oversized existing tracked files that are unchanged will not block. In non-git directories, all git-related gates are skipped because they are guarded by `git rev-parse --git-dir` at `hooks/loop-codex-stop-hook.sh:110` and `hooks/loop-codex-stop-hook.sh:206`.

  A malformed nonnumeric `current_round` stops the loop by deleting state rather than blocking for repair. A malformed `max_iterations` silently falls back to `42`. A configured max of `0` is accepted by the numeric regex and would make `NEXT_ROUND=1` exceed max immediately, allowing exit without review.

  The hook assumes `$HOME/.cache/humanize/...` is writable. Because `set -euo pipefail` is active, failures such as `mkdir -p "$CACHE_DIR"` could abort without emitting the structured JSON block expected by Claude Code.

  Codex availability is verified when the loop is started by `scripts/setup-rlcr-loop.sh:195-201`, but the Stop hook itself does not preflight `codex` before execution. If `codex exec` fails and no review result/stdout is produced, the hook blocks with debug information at `hooks/loop-codex-stop-hook.sh:771-807`.

  The script comment at `hooks/loop-codex-stop-hook.sh:725` says Codex reads from stdin and uses `-w`, but the actual invocation passes prompt content as a positional argument to `codex exec` and redirects stdout/stderr at `hooks/loop-codex-stop-hook.sh:749-751`. If the CLI contract changes, this is a fragile integration point.

  `STOP` is honored even outside full-alignment rounds. The hook labels that path “unexpected” but still removes state and exits at `hooks/loop-codex-stop-hook.sh:845-857`.

- validation_or_tests:  
  Direct read-only validation performed for this research: `bash -n hooks/loop-codex-stop-hook.sh` passed with no syntax errors.

  No dedicated test/spec files were present in the read-only export from a `find` scan for common test/spec names. Validation evidence is therefore source inspection of the hook, caller wiring in `hooks/hooks.json`, lifecycle setup in `scripts/setup-rlcr-loop.sh`, shared helpers in `hooks/lib/loop-common.sh`, and the todo checker in `hooks/check-todos-from-transcript.py`.

  `git status --short` could not be used as repository validation in this export because the branch export did not include a `.git` directory and the sandbox also blocked macOS `/tmp` xcrun cache creation. No files were modified.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `IMPL_DCCB_LOOP-HZ-014`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`