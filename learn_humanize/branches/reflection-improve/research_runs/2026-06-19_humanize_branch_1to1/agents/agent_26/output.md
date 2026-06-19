# agent_26 reflection-improve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `13a47fb2260667a272b448e8d3c1a521f2382590`

## Item Evidence

### REFLECTION_IMPROVE-HZ-026 `file` `agents/draft-relevance-checker.md`
- cursor: `[_]`
- core_role: Lightweight repository-relevance gate for the `gen-plan` command. The agent frontmatter defines name/model/tools at `agents/draft-relevance-checker.md:1`, and its purpose is to decide whether an input draft is semantically related enough to the current repo before a plan file is generated.
- algorithmic_behavior: The prompt requires three phases: quickly inspect repo docs/structure/technologies, analyze the draft for matching concepts/files/features/use-cases, then emit exactly one verdict prefix, `RELEVANT:` or `NOT_RELEVANT:`. See `agents/draft-relevance-checker.md:14`, `agents/draft-relevance-checker.md:21`, and `agents/draft-relevance-checker.md:27`.
- inputs_outputs_state: Input is the user draft content plus repository context read via `Read`, `Glob`, and `Grep` tools. Output is a single textual verdict with a short explanation. It has no persisted local state and performs no repository mutation.
- gates_or_invariants: The policy is intentionally lenient: informal drafts, any language, rough ideas, and doubtful cases should pass as relevant. This lowers false negatives for plan generation. See `agents/draft-relevance-checker.md:31`.
- dependencies_and_callers: Called by `commands/gen-plan.md` Phase 2 after IO validation; the command explicitly instructs use of `humanize:draft-relevance-checker` with haiku and stops if the verdict is not relevant (`commands/gen-plan.md:142`, `commands/gen-plan.md:149`, `commands/gen-plan.md:159`).
- edge_cases_or_failure_modes: A draft with only weak conceptual overlap should still pass; only completely unrelated content should block. Ambiguous multilingual or rough notes are expected and should not fail solely due to style.
- validation_or_tests: `tests/test-gen-plan.sh` verifies the agent file exists, has the expected name, uses the haiku model, declares tools, and passes naming/frontmatter/model checks (`tests/test-gen-plan.sh:111`, `tests/test-gen-plan.sh:256`, `tests/test-gen-plan.sh:271`, `tests/test-gen-plan.sh:423`). Not executed in this read-only research pass.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-056 `file` `scripts/humanize.sh`
- cursor: `[_]`
- core_role: Primary shell entrypoint for humanize monitoring commands. It implements monitor routing for RLCR, PR loop, and skill monitoring, plus helper parsers for loop progress and git state. Entry routing is at `scripts/humanize.sh:1105`; RLCR monitor starts at `scripts/humanize.sh:227`; PR monitor starts at `scripts/humanize.sh:1158`.
- algorithmic_behavior: The RLCR monitor selects the latest `.humanize/rlcr/<timestamp>` session, maps that session to cached logs under `${XDG_CACHE_HOME:-$HOME/.cache}/humanize/<sanitized-project>/<session>`, renders a fixed terminal status bar, tails run/review logs incrementally, and switches to newer sessions or logs as they appear (`scripts/humanize.sh:232`, `scripts/humanize.sh:261`, `scripts/humanize.sh:300`, `scripts/humanize.sh:777`). The PR monitor selects the latest `.humanize/pr-loop` session, chooses the most recent `round-*-pr-check.md`, `round-*-pr-feedback.md`, or `round-*-pr-comment.md`, renders PR/bot/phase status, and either prints once or continuously tails activity (`scripts/humanize.sh:1162`, `scripts/humanize.sh:1194`, `scripts/humanize.sh:1438`, `scripts/humanize.sh:1526`).
- inputs_outputs_state: Inputs include loop directories, `state.md` or stop-state files, `goal-tracker.md`, cached Codex log files, terminal dimensions, git status, and signals. Outputs are terminal UI/status text, live tail output, graceful stop messages, and command return codes. Internal transient state includes `current_session_dir`, `current_file`, `last_size`, `monitor_running`, `cleanup_done`, `resize_needed`, and PR `TAIL_PID`.
- gates_or_invariants: Requires the relevant loop directory at startup (`scripts/humanize.sh:238`, `scripts/humanize.sh:1182`). RLCR enforces log-order consistency: review rounds must come after run rounds, otherwise it reports an inconsistent log state (`scripts/humanize.sh:330`). Terminal height must be large enough for the fixed status area or the monitor waits/resizes safely (`scripts/humanize.sh:600`). Cleanup must restore scroll region via `printf "\033[r"` and stop background tails (`scripts/humanize.sh:645`, `scripts/humanize.sh:675`).
- dependencies_and_callers: Sources `scripts/lib/monitor-common.sh` and `hooks/lib/loop-common.sh` when present (`scripts/humanize.sh:6`, `scripts/humanize.sh:12`), and later sources `scripts/lib/monitor-skill.sh` (`scripts/humanize.sh:1589`). Depends on `find`, `stat`, `tail`, `tput`, `sed`, `grep`, `date`, `git`, and shell-specific trap semantics. Shared helper `monitor_find_latest_session` avoids glob expansion failures (`scripts/lib/monitor-common.sh:40`).
- edge_cases_or_failure_modes: Handles `.humanize/rlcr` deletion with a clean return and user-facing message (`scripts/humanize.sh:779`, `scripts/humanize.sh:703`), current session deletion by switching or waiting (`scripts/humanize.sh:886`, `scripts/humanize.sh:1014`), no log files with centered waiting messages (`scripts/humanize.sh:822`), log truncation/rotation by resetting file state (`scripts/humanize.sh:996`), zsh array indexing via `setopt localoptions ksharrays` (`scripts/humanize.sh:228`), and SIGINT/SIGTERM cleanup with bash and zsh-specific traps (`scripts/humanize.sh:723`, `scripts/humanize.sh:1425`). PR monitor has a less explicit deletion path than RLCR; continuous mode mainly waits for sessions and relies on signal cleanup.
- validation_or_tests: Covered directly by `tests/test-monitor-e2e-real.sh`, which sources the real function bodies and verifies deletion, SIGINT, zsh compatibility, no glob errors, and terminal cleanup. Not executed in this read-only research pass.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-086 `file` `tests/test-monitor-e2e-real.sh`
- cursor: `[_]`
- core_role: Executable end-to-end specification for the real monitor implementations in `scripts/humanize.sh`, specifically graceful deletion handling, shell compatibility, terminal restoration, and signal cleanup.
- algorithmic_behavior: Creates isolated temp projects under `/tmp/test-monitor-e2e-real-$$`, builds fake `.humanize/rlcr` or `.humanize/pr-loop` sessions with state and goal tracker files, creates fake HOME/cache log locations, generates small runner scripts that source `scripts/humanize.sh`, then drives real monitor functions in background processes (`tests/test-monitor-e2e-real.sh:43`, `tests/test-monitor-e2e-real.sh:56`, `tests/test-monitor-e2e-real.sh:107`, `tests/test-monitor-e2e-real.sh:144`).
- inputs_outputs_state: Inputs are synthetic loop/session directories, synthetic YAML-ish state files, goal trackers, fake cache logs, and shimmed `tput`/`clear` functions. Outputs are PASS/FAIL counters, captured monitor output files, process exit status markers, and final process exit code. Test state is cleaned by trap via `cleanup_test` (`tests/test-monitor-e2e-real.sh:46`).
- gates_or_invariants: Each test bounds waiting loops to 20 half-second intervals, force-kills hung monitors, and checks for expected clean-exit signals rather than relying on indefinite process behavior (`tests/test-monitor-e2e-real.sh:167`, `tests/test-monitor-e2e-real.sh:498`, `tests/test-monitor-e2e-real.sh:951`). It asserts no zsh/bash glob errors like “no matches found” or “bad pattern” in output (`tests/test-monitor-e2e-real.sh:200`, `tests/test-monitor-e2e-real.sh:360`, `tests/test-monitor-e2e-real.sh:991`).
- dependencies_and_callers: Depends on bash, optional zsh, `pkill`, `kill`, `sleep`, `mkdir`, `rm`, `grep`, generated runner scripts, and the repository’s `scripts/humanize.sh`. It is self-contained and runs all tests when invoked directly (`tests/test-monitor-e2e-real.sh:1002`).
- edge_cases_or_failure_modes: zsh tests skip when zsh is unavailable (`tests/test-monitor-e2e-real.sh:238`, `tests/test-monitor-e2e-real.sh:560`). SIGINT delivery is treated pragmatically; bash/PR tests can still pass after SIGTERM fallback if the monitor ran and process-group interrupt semantics are unreliable (`tests/test-monitor-e2e-real.sh:505`, `tests/test-monitor-e2e-real.sh:957`). The PR deletion test uses `--once`, so it mainly verifies clean one-shot behavior and no glob errors rather than a long-running deletion loop (`tests/test-monitor-e2e-real.sh:788`).
- validation_or_tests: The file defines six scenarios: RLCR deletion in bash, RLCR deletion in zsh, RLCR SIGINT in bash, RLCR SIGINT in zsh, PR monitor deletion/one-shot, and PR monitor continuous SIGINT (`tests/test-monitor-e2e-real.sh:1008`). Not executed here because the assignment requested research notes only.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-116 `file` `prompt-template/block/bitlesson-delta-invalid.md`
- cursor: `[_]`
- core_role: Blocking prompt template for the BitLesson summary gate when a round summary has a `## BitLesson Delta` section but its action declaration is invalid.
- algorithmic_behavior: The template tells the agent that exactly one action must be present and enumerates the accepted actions: `none`, `add`, or `update` (`prompt-template/block/bitlesson-delta-invalid.md:1`, `prompt-template/block/bitlesson-delta-invalid.md:3`). It is rendered as the stop-hook block reason.
- inputs_outputs_state: Inputs are implicit; this template has no placeholders. Output is Markdown inserted into a JSON block response by the validator. It has no state.
- gates_or_invariants: The backing validator extracts the BitLesson Delta block, parses `Action:` candidates case-insensitively, requires exactly one candidate, and requires membership in the three allowed action values (`scripts/bitlesson-validate-delta.sh:111`, `scripts/bitlesson-validate-delta.sh:118`, `scripts/bitlesson-validate-delta.sh:122`).
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh` invokes `scripts/bitlesson-validate-delta.sh` for non-finalize rounds when BitLesson validation is required (`hooks/loop-codex-stop-hook.sh:746`, `hooks/loop-codex-stop-hook.sh:749`). The validator loads this template through `load_and_render_safe` when the action count/value check fails (`scripts/bitlesson-validate-delta.sh:132`).
- edge_cases_or_failure_modes: Missing `## BitLesson Delta` uses a different template, so this block only covers present-but-invalid sections. Multiple `Action:` lines, missing action, unknown action text, or action values outside alpha-only parsing all fail this gate. Action names are normalized to lowercase before comparison.
- validation_or_tests: The behavior is covered by `scripts/bitlesson-validate-delta.sh`; repository search shows related task-tag/BitLesson tests, but no direct run was performed in this research pass.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-146 `file` `prompt-template/block/work-summary-missing.md`
- cursor: `[_]`
- core_role: Stop-hook blocking prompt template that prevents an RLCR/finalize agent from exiting without writing the expected work summary file.
- algorithmic_behavior: The template tells the agent it attempted to exit without a summary, renders the required `{{SUMMARY_FILE}}`, and lists minimum summary contents: implementation, changed files, tests, and remaining items (`prompt-template/block/work-summary-missing.md:1`, `prompt-template/block/work-summary-missing.md:5`, `prompt-template/block/work-summary-missing.md:10`).
- inputs_outputs_state: Input is the stop hook’s computed summary path. Output is Markdown block feedback embedded in a JSON decision. State comes from the loop phase: finalize expects `finalize-summary.md`; normal rounds expect `round-${CURRENT_ROUND}-summary.md` (`hooks/loop-codex-stop-hook.sh:711`).
- gates_or_invariants: The invariant is file existence before exit. If the file is absent, the hook emits decision `block` and exits successfully as a hook-level block response, not as a shell error (`hooks/loop-codex-stop-hook.sh:718`, `hooks/loop-codex-stop-hook.sh:734`).
- dependencies_and_callers: Loaded by `hooks/loop-codex-stop-hook.sh` via `load_and_render_safe`, with a fallback message if the template cannot be loaded (`hooks/loop-codex-stop-hook.sh:722`, `hooks/loop-codex-stop-hook.sh:725`). It depends on template variable substitution for `SUMMARY_FILE`.
- edge_cases_or_failure_modes: A present but malformed/empty summary is not handled by this specific template; later gates validate BitLesson Delta and goal-tracker behavior. If template rendering fails, the hook’s fallback still blocks with a minimal summary path reminder.
- validation_or_tests: Stop-hook line coverage is inspectable in `hooks/loop-codex-stop-hook.sh`; no executable test was run here.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-176 `file` `prompt-template/pr-loop/round-0-task-no-comments.md`
- cursor: `[_]`
- core_role: Round-0 PR loop task template for startup when no existing PR comments are present. It defines the initial “wait for automatic bot reviews” behavior and prevents redundant trigger comments.
- algorithmic_behavior: Instructs the agent that monitored bots will review automatically, tells it to write an initial summary to `@{{RESOLVE_PATH}}`, and explains that the Stop Hook will poll for bot reviews and then either continue with feedback or finish on approvals (`prompt-template/pr-loop/round-0-task-no-comments.md:4`, `prompt-template/pr-loop/round-0-task-no-comments.md:8`, `prompt-template/pr-loop/round-0-task-no-comments.md:26`).
- inputs_outputs_state: Inputs are `{{ACTIVE_BOTS_DISPLAY}}` and `{{RESOLVE_PATH}}`. Output is part of `.humanize/pr-loop/<session>/round-0-prompt.md`, after the round-0 header and fetched comments. State transition is from PR loop initialization to “waiting for initial bot reviews” with a required round-0 resolve summary.
- gates_or_invariants: Explicitly forbids commenting to trigger first review and forbids modifying `.humanize/pr-loop/` state files (`prompt-template/pr-loop/round-0-task-no-comments.md:18`). The expected exit path is summary write followed by stop-hook polling, not manual bot nudging.
- dependencies_and_callers: `scripts/setup-pr-loop.sh` selects this template when fetched comments contain the exact `*No comments found.*` sentinel (`scripts/setup-pr-loop.sh:723`, `scripts/setup-pr-loop.sh:767`, `scripts/setup-pr-loop.sh:800`). The PR stop hook later polls configured bots and blocks on review timeout if no bot responses arrive (`hooks/pr-loop-stop-hook.sh:802`, `hooks/pr-loop-stop-hook.sh:1177`).
- edge_cases_or_failure_modes: If comments already exist, setup uses a different round-0 task template. If automatic reviews do not arrive, the stop hook returns a blocking timeout message with options. If active bot display or resolve path rendering is wrong, the generated prompt can send the agent to the wrong summary target.
- validation_or_tests: `tests/test-monitor-e2e-real.sh` covers PR monitor behavior around initialized PR-loop state, but not this setup template directly. `scripts/setup-pr-loop.sh` includes fallback content matching this template, reducing template-load failure impact.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6 Item Evidence headings; item IDs intentionally appear only in those headings to preserve exact-once evidence.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`