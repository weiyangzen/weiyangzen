# agent_30 robust-edge-test-find-and-resolve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 3
- source_commit: `a3112ca4d149f56ced783e805b6dfcf029368dc4`

## Item Evidence

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-030 `file` `scripts/validate-gen-plan-io.sh`
- cursor: `[_]`
- core_role: IO preflight gate for `/humanize:gen-plan`; it is called as Phase 1 before relevance checking, draft analysis, or plan generation in `commands/gen-plan.md:29-44`.
- algorithmic_behavior: Parses only `--input <path>` and `--output <path>`, rejects missing values, unknown flags, and help via `usage()` with exit `6` (`scripts/validate-gen-plan-io.sh:15-23`, `28-66`). It canonicalizes paths with `realpath -m` fallback, derives `OUTPUT_DIR`, prints the resolved paths, then runs ordered validations (`68-77`).
- inputs_outputs_state: Inputs are CLI args plus filesystem state for input file, output file, output directory, and output directory permissions. Outputs are stdout/stderr-style diagnostic strings, machine-readable `VALIDATION_ERROR:*` markers, `VALIDATION_SUCCESS`, and exit codes `0-6` (`4-11`, `78-130`). It mutates no repository or loop state.
- gates_or_invariants: Requires input exists and is a regular non-empty file (`78-92`); output directory exists (`94-100`); output target is not an existing directory or file (`102-115`); output directory is writable (`117-123`). Output must be a new file path, preventing accidental overwrite.
- dependencies_and_callers: Direct caller is `commands/gen-plan.md`, which whitelists the script in allowed tools (`commands/gen-plan.md:4-6`) and maps each exit code to user-facing stop/continue behavior (`37-44`). User-facing command docs describe the same `--input/--output` contract in `README.md:103-116`.
- edge_cases_or_failure_modes: `--input --output foo` is treated as invalid args; `--help` also exits `6`, which tests encode as expected behavior. `realpath -m` failure falls back to the raw path, so validation still proceeds on systems without compatible `realpath`. Output directory nonexistence is checked before output existence, and output-as-directory shares exit `4` with output-already-exists.
- validation_or_tests: `tests/test-gen-plan.sh:426-541` exercises missing option values, flag-as-value, unknown flag, missing input, empty input, nonexistent output dir, existing output file, output path as directory, valid paths, and help exit code. I did static inspection only; no tests were executed.
- skip_candidate: `no`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-060 `file` `prompt-template/block/git-push.md`
- cursor: `[_]`
- core_role: User-facing block template for the bash command validator’s git-push gate; it defines the policy message shown when an RLCR loop should keep commits local.
- algorithmic_behavior: The template itself is declarative content: title, reason, and remediation command. The active algorithm is in `hooks/loop-bash-validator.sh:74-91`: when `STATE_PUSH_EVERY_ROUND` is not `true` and `COMMAND_LOWER` matches `git push`, the validator renders `block/git-push.md` and exits `2`.
- inputs_outputs_state: Inputs are the current loop state field `push_every_round`, the lowercased bash command, and template availability. Output is the rendered block text: “Git Push Blocked”, local-commit policy, and the `--push-every-round` startup hint (`prompt-template/block/git-push.md:1-9`). It changes no state; it blocks the attempted command by validator exit.
- gates_or_invariants: Default invariant is “commits stay local” unless the loop was started with push-every-round enabled. The block provides the exact opt-in path: `/humanize:start-rlcr-loop plan.md --push-every-round` (`6-9`). If the template is missing, the validator uses a fallback with the same policy (`hooks/loop-bash-validator.sh:85-89`).
- dependencies_and_callers: Loaded through `load_and_render_safe`, whose fallback semantics are defined in `hooks/lib/template-loader.sh:167-203`. `get_template_dir` resolves `prompt-template` relative to `hooks/lib` (`template-loader.sh:24-31`), and `hooks/lib/loop-common.sh:140` initializes `TEMPLATE_DIR`.
- edge_cases_or_failure_modes: The regex only catches commands beginning with optional whitespace then `git push`; wrapper forms or aliases are outside this specific gate. Template failure is non-fatal because `load_and_render_safe` emits fallback content. The template has no variables, so render injection is irrelevant here.
- validation_or_tests: `tests/test-template-loader.sh:55-65` confirms `block/git-push.md` loads and contains “Git Push Blocked”; `tests/test-template-loader.sh:210-222` and `tests/test-templates-comprehensive.sh:456-463` confirm the safe loader prefers the real template over fallback. I did static inspection only; no tests were executed.
- skip_candidate: `no`

### ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-090 `file` `tests/robustness/test-cancel-security-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for AC-10 cancel authorization security. It validates that only the real cancel flow can rename `state.md` or `finalize-state.md` to `cancel-state.md`.
- algorithmic_behavior: The test sources `hooks/lib/loop-common.sh` and `tests/test-helpers.sh`, creates a temp loop dir with `state.md`, then calls `is_cancel_authorized "$LOOP_DIR" "$COMMAND_LOWER"` across positive and negative cases (`tests/robustness/test-cancel-security-robustness.sh:13-31`). It records pass/fail counters and exits with the summary status (`407-412`).
- inputs_outputs_state: Inputs are synthetic loop dirs, `.cancel-requested` signal files, state/finalize files, symlinks, and crafted command strings. Outputs are PASS/FAIL lines via `pass`/`fail`, then aggregate status from `print_test_summary` (`tests/test-helpers.sh:30-78`). State is temporary filesystem state under `TEST_DIR`, cleaned by trap (`test-helpers.sh:84-89`).
- gates_or_invariants: Positive gate requires signal file plus exact `mv` of `state.md` or `finalize-state.md` to `cancel-state.md`, accepting double quotes, single quotes, unquoted paths, and `/./` normalization (`39-89`, `265-276`). Negative gates reject missing signal, command substitution, backticks, shell chaining, pipes, wrong source/destination, extra args, newline injection, remaining variables, non-`mv`, mixed quotes, IFS manipulation, trailing spaces, nonstandard source filename, and symlink sources (`99-367`).
- dependencies_and_callers: It directly specifies `is_cancel_authorized` in `hooks/lib/loop-common.sh:437-614`. That function is used by `hooks/loop-bash-validator.sh` as the sole exception allowing protected state-file moves during cancellation (`117-130`, `264-301`). The user command path is `commands/cancel-rlcr-loop.md:9-36`, backed by `scripts/cancel-rlcr-loop.sh` per repository references.
- edge_cases_or_failure_modes: Regression coverage prevents a loop directory containing the substring `finalize` from bypassing symlink rejection; tests 25-26 assert exact path matching rather than substring classification (`369-405`). The spec intentionally rejects multiple trailing spaces (`304-315`) and mixed quote delimiters (`278-289`), which are stricter than shell permissiveness. It also covers filesystem symlinks, not only lexical path tricks (`332-367`).
- validation_or_tests: Included in the aggregate suite as `robustness/test-cancel-security-robustness.sh` in `tests/run-all-tests.sh:52-62`. Its target implementation documents return codes for missing signal, security violation, mixed quotes, trailing spaces, invalid structure, and symlink source (`hooks/lib/loop-common.sh:437-455`). I did static inspection only; no tests were executed.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-030, ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-060, ROBUST_EDGE_TEST_FIND_AND_RESOLVE-HZ-090
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`