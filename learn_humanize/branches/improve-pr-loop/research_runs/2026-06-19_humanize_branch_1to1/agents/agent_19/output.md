# agent_19 improve-pr-loop 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 5
- source_commit: `61f03daecb8ff9c20e535a636b90aa92a3d7c9b2`

## Item Evidence

### IMPROVE_PR_LOOP-HZ-019 `file` `commands/cancel-rlcr-loop.md`
- cursor: `[_]`
- core_role: Slash-command workflow contract for cancelling an active RLCR loop. It is a command-facing state transition wrapper around `scripts/cancel-rlcr-loop.sh`, with explicit handling for normal loop state versus Finalize Phase.
- algorithmic_behavior: Runs `"${CLAUDE_PLUGIN_ROOT}/scripts/cancel-rlcr-loop.sh"` first, then branches on the first output token: `NO_LOOP` / `NO_ACTIVE_LOOP`, `CANCELLED`, `CANCELLED_FINALIZE`, or `FINALIZE_NEEDS_CONFIRM` at `commands/cancel-rlcr-loop.md:11-22`. On `FINALIZE_NEEDS_CONFIRM`, it asks the user whether to force cancellation, then optionally runs the same script with `--force` at `commands/cancel-rlcr-loop.md:23-34`.
- inputs_outputs_state: Input is the current `.humanize/rlcr` loop state plus optional user confirmation. Output is a user-facing cancellation report. The underlying script finds the newest loop directory, accepts `state.md` or `finalize-state.md` as active state, touches `.cancel-requested`, and renames the active state to `cancel-state.md` at `scripts/cancel-rlcr-loop.sh:69-99` and `scripts/cancel-rlcr-loop.sh:134-151`.
- gates_or_invariants: The command allows only two Bash invocations and `AskUserQuestion` in frontmatter at `commands/cancel-rlcr-loop.md:1-4`. Finalize cancellation is confirmation-gated unless `--force` is selected, matching the script’s exit code `2` behavior at `scripts/cancel-rlcr-loop.sh:11-15` and `scripts/cancel-rlcr-loop.sh:117-128`.
- dependencies_and_callers: Depends on `CLAUDE_PLUGIN_ROOT` and `scripts/cancel-rlcr-loop.sh`. The setup help and loop prompts point users here as the supported stop path, for example `scripts/setup-rlcr-loop.sh:102-104`. Bash hook protections also special-case authorized state-file moves after the cancel signal exists, so this command coordinates with `hooks/loop-bash-validator.sh:139-155`.
- edge_cases_or_failure_modes: If no newest loop directory exists, output starts `NO_LOOP`; if a directory exists but neither `state.md` nor `finalize-state.md` exists, output starts `NO_ACTIVE_LOOP`, per `scripts/cancel-rlcr-loop.sh:72-99`. During Finalize Phase, refusing confirmation leaves `finalize-state.md` untouched and reports that the phase will continue. The command relies on the script’s first output line being stable.
- validation_or_tests: Related cancellation behavior is covered by `tests/test-cancel-signal-file.sh` references found in the tree, and the command’s own allowed-tool list restricts execution to the intended script paths. Direct script exit codes and output tokens are documented in `scripts/cancel-rlcr-loop.sh:11-15`.
- skip_candidate: `no`

### IMPROVE_PR_LOOP-HZ-049 `file` `tests/test-bash-validator-patterns.sh`
- cursor: `[_]`
- core_role: Executable specification for `command_modifies_file` detection patterns used by loop Bash validators to prevent shell-based mutation of protected loop files.
- algorithmic_behavior: Sources `hooks/lib/loop-common.sh`, lowercases each test command through `to_lower`, and asserts whether `command_modifies_file "$command_lower" "$pattern"` returns success at `tests/test-bash-validator-patterns.sh:11-14` and `tests/test-bash-validator-patterns.sh:36-62`. It checks write redirections, `tee`, in-place editors, `mv` / `cp` / `rm`, `dd`, `truncate`, and `exec` redirection at `tests/test-bash-validator-patterns.sh:69-134`.
- inputs_outputs_state: Inputs are command strings and target regexes such as `goal-tracker\.md`, `state\.md`, and `round-[0-9]+-summary\.md`. Output is a pass/fail count and process exit status: zero only when `TESTS_FAILED` is zero at `tests/test-bash-validator-patterns.sh:196-214`. It mutates only in-memory counters.
- gates_or_invariants: The matcher must catch modification intent without over-blocking read-only commands. False-positive guard cases include `cat`, `grep`, `head`, `tail`, `wc`, `less`, `echo`, `ls`, `file`, `stat`, and `diff` at `tests/test-bash-validator-patterns.sh:136-153`.
- dependencies_and_callers: Depends on `to_lower` at `hooks/lib/loop-common.sh:394-397` and `command_modifies_file` at `hooks/lib/loop-common.sh:1068-1096`. The production caller is `hooks/loop-bash-validator.sh`, which applies the matcher to RLCR state files, plan backups, goal tracker, round prompt/summary/todos files, and PR loop state/read-only files at `hooks/loop-bash-validator.sh:139-155` and `hooks/loop-bash-validator.sh:336-438`.
- edge_cases_or_failure_modes: Known limitation is documented in the test: `cp file1.md file2.md goal-tracker.md` is not detected because the pattern expects a two-operand `cp src dest` shape at `tests/test-bash-validator-patterns.sh:165-168`. Variable-based destinations such as `echo x > $FILE` are intentionally not matched at `tests/test-bash-validator-patterns.sh:170-172`.
- validation_or_tests: This file is itself the validation harness. It exercises target-specific patterns for state files and summary files at `tests/test-bash-validator-patterns.sh:175-194`, then fails the shell process on any regression.
- skip_candidate: `no`

### IMPROVE_PR_LOOP-HZ-079 `file` `prompt-template/block/git-add-humanize.md`
- cursor: `[_]`
- core_role: User-facing block template for the invariant that `.humanize/` local loop state must not be staged into version control.
- algorithmic_behavior: Provides the denial reason and safe alternatives after `git_adds_humanize` detects a risky `git add`. It tells the actor to stage specific paths, directories, or patch hunks instead of broad additions at `prompt-template/block/git-add-humanize.md:8-15`, and lists blocked command classes at `prompt-template/block/git-add-humanize.md:16-25`.
- inputs_outputs_state: Input is the blocked Bash command context from `hooks/loop-bash-validator.sh`. Output is rendered Markdown to stderr via `git_add_humanize_blocked_message`, which loads this template with a fallback at `hooks/lib/loop-common.sh:1028-1066`. It does not mutate repository state.
- gates_or_invariants: The invariant is that `.humanize/` is local loop state and should remain uncommitted, stated at `prompt-template/block/git-add-humanize.md:1-6`. It also includes a narrow path for adding `.humanize*` to `.gitignore`, requiring `git add .gitignore` and warning that the commit message must not include the literal protected string at `prompt-template/block/git-add-humanize.md:26-34`.
- dependencies_and_callers: Called by `hooks/loop-bash-validator.sh` when `git_adds_humanize "$COMMAND_LOWER"` returns true at `hooks/loop-bash-validator.sh:109-118`. The matcher handles direct `.humanize` paths, forced broad adds, `--all`, broad scope targets, chained commands, and `git -C` forms at `hooks/lib/loop-common.sh:908-1026`.
- edge_cases_or_failure_modes: Non-force `git add .` is blocked only when `.humanize` exists and is not ignored, while `git add -A` is blocked whenever `.humanize` exists because it may include untracked state at `hooks/lib/loop-common.sh:1005-1020`. Because the input is lowercased, the matcher explicitly treats `-A` as `-a` at `hooks/lib/loop-common.sh:912-914`.
- validation_or_tests: Related tests appear in `tests/test-humanize-escape.sh` and hook robustness tests discovered by repository search. The production block path is deterministic: a true matcher result emits this template and exits with status `2` at `hooks/loop-bash-validator.sh:115-117`.
- skip_candidate: `no`

### IMPROVE_PR_LOOP-HZ-109 `file` `prompt-template/claude/goal-tracker-update-request.md`
- cursor: `[_]`
- core_role: Prompt footer contract that routes Goal Tracker mutations through a structured request instead of allowing direct edits by the implementation actor after Codex review feedback.
- algorithmic_behavior: Defines the exact Markdown section an actor should include in a round summary when Goal Tracker updates are needed: requested changes plus justification at `prompt-template/claude/goal-tracker-update-request.md:2-14`. It explicitly delegates review and update authority to Codex at `prompt-template/claude/goal-tracker-update-request.md:16`.
- inputs_outputs_state: Input is the actor’s need to change task status, open issues, plan evolution, or deferrals. Output is a structured summary section that the loop can later review. It does not directly update `goal-tracker.md`.
- gates_or_invariants: Preserves the invariant that Goal Tracker changes must be justified and reviewed rather than silently edited. This pairs with Bash-level blocking of `goal-tracker.md` modifications after Round 0, where the validator tells the actor to write a request into the round summary at `hooks/loop-bash-validator.sh:343-357`.
- dependencies_and_callers: Loaded by `hooks/loop-codex-stop-hook.sh` and appended to the next-round prompt after Codex finds issues at `hooks/loop-codex-stop-hook.sh:1551-1556`. It depends on template loading through `load_template`; if missing, the hook falls back to a one-line instruction at `hooks/loop-codex-stop-hook.sh:1552-1555`.
- edge_cases_or_failure_modes: The template is advisory and structured, so enforcement depends on surrounding hooks and Codex review. If the actor omits the section despite needing a change, the state transition may stall because Goal Tracker updates are not made directly by this template.
- validation_or_tests: Indirectly validated through stop-hook behavior and Goal Tracker protection tests. The Bash validator’s `goal_tracker_blocked_message` path uses a related block template/fallback to steer post-Round-0 updates into summaries at `hooks/lib/loop-common.sh:1098-1110`.
- skip_candidate: `no`

### IMPROVE_PR_LOOP-HZ-139 `file` `tests/robustness/test-setup-scripts-robustness.sh`
- cursor: `[_]`
- core_role: Broad executable robustness specification for the two loop setup entry points, `scripts/setup-rlcr-loop.sh` and `scripts/setup-pr-loop.sh`, covering argument parsing, plan validation, Git preconditions, mutual exclusion, symlink safety, timeout handling, review-round cadence parameters, and skip-implementation mode.
- algorithmic_behavior: Builds isolated temporary Git repositories, creates minimal plans, invokes setup scripts with `CLAUDE_PROJECT_DIR` bound to the test repo, and checks output/exit-code contracts using shared `pass` / `fail` helpers at `tests/robustness/test-setup-scripts-robustness.sh:15-87`. It then runs 45 numbered cases across RLCR arguments at `tests/robustness/test-setup-scripts-robustness.sh:89-215`, plan/Git/YAML validation at `tests/robustness/test-setup-scripts-robustness.sh:216-464`, PR setup at `tests/robustness/test-setup-scripts-robustness.sh:465-526`, and later feature modes at `tests/robustness/test-setup-scripts-robustness.sh:741-1067`.
- inputs_outputs_state: Inputs are temporary repos, synthetic plan files, fake loop directories, and mock binaries such as `codex`, `gh`, `timeout`, and `gtimeout`. Outputs are pass/fail assertions and temporary `.humanize` state in test repos. For skip-implementation mode, expected state includes `.review-phase-started`, `review_started: true`, and a non-placeholder `goal-tracker.md` at `tests/robustness/test-setup-scripts-robustness.sh:991-1039`.
- gates_or_invariants: Setup must reject malformed numeric options, duplicate plan specification, unknown options, non-Git directories, Git repos without commits, unsafe plan paths, tracked plans without `--track-plan-file`, YAML-unsafe branch/model values, active loop collisions, and symlink traversal. These gates map to concrete implementation checks in `scripts/setup-rlcr-loop.sh:120-204`, `scripts/setup-rlcr-loop.sh:246-305`, `scripts/setup-rlcr-loop.sh:322-374`, and `scripts/setup-rlcr-loop.sh:450-583`.
- dependencies_and_callers: Depends on `tests/test-helpers.sh`, `scripts/portable-timeout.sh`, `scripts/setup-rlcr-loop.sh`, `scripts/setup-pr-loop.sh`, `git`, and optional mocked command shims. PR setup checks map to bot flag, Git repo, and GitHub auth gates in `scripts/setup-pr-loop.sh:115-156`, `scripts/setup-pr-loop.sh:226-245`, and `scripts/setup-pr-loop.sh:264-267`.
- edge_cases_or_failure_modes: Documents several intentional/current behaviors: negative `--max` may be parsed as an unknown option depending on syntax at `tests/robustness/test-setup-scripts-robustness.sh:129-153`; `--codex-timeout 0` is accepted because validation is non-negative despite the message saying positive at `tests/robustness/test-setup-scripts-robustness.sh:749-765`; symlink tests may pass as unsupported if symlink creation fails at `tests/robustness/test-setup-scripts-robustness.sh:620-630` and `tests/robustness/test-setup-scripts-robustness.sh:648-658`.
- validation_or_tests: The script is an end-to-end robustness validator and exits through `print_test_summary` at `tests/robustness/test-setup-scripts-robustness.sh:1069-1074`. It validates both failure gates and positive progression, such as valid RLCR args proceeding to Codex checks at `tests/robustness/test-setup-scripts-robustness.sh:668-712` and valid PR args proceeding to `gh auth` checks at `tests/robustness/test-setup-scripts-robustness.sh:714-739`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 5/5 headings present once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`