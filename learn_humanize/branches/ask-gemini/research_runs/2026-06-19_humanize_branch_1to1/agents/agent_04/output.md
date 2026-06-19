# agent_04 ask-gemini 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 8
- source_commit: `883e3f5bb8106cea4153d9f5e469b2fa7a8d6849`

## Item Evidence

### ASK_GEMINI-HZ-004 `directory` `config`
- cursor: `[_]`
- core_role: Runtime configuration surface for default Humanize behavior and Codex hook installation. Recursive inspection found two files only: `config/default_config.json` and `config/codex-hooks.json`.
- algorithmic_behavior: `config/default_config.json:1-8` seeds defaults for Codex model/effort, BitLesson model, agent teams, alternative plan language, and gen-plan/refine-plan mode. `config/codex-hooks.json:1-23` defines native Codex `Stop` hook groups that invoke RLCR and PR-loop stop hooks through a `{{HUMANIZE_RUNTIME_ROOT}}` placeholder.
- inputs_outputs_state: Input is static JSON plus optional runtime substitution. `scripts/lib/config-loader.sh:63-137` consumes `default_config.json` as required layer 1, then merges user and project config with later overrides. `scripts/install-codex-hooks.sh:94-163` reads `codex-hooks.json`, JSON-escapes runtime root, replaces `{{HUMANIZE_RUNTIME_ROOT}}`, removes previously managed stop hooks, and writes the merged Codex `hooks.json`.
- gates_or_invariants: Default config must exist and be a JSON object; malformed required default config is fatal in `scripts/lib/config-loader.sh:40-60`. Optional user/project malformed configs are warnings and ignored. Hook install requires Codex CLI with `codex_hooks` feature in `scripts/install-codex-hooks.sh:75-83`, and existing `hooks`/`Stop` shapes must be JSON object/list in `scripts/install-codex-hooks.sh:116-127`.
- dependencies_and_callers: `hooks/lib/loop-common.sh:210-223` reads merged `codex_effort` and `agent_teams`, validating effort against `xhigh|high|medium|low`. `commands/refine-plan.md:86-153` explicitly reuses `config-loader.sh` semantics for `alternative_plan_language` and `gen_plan_mode`. `scripts/install-skill.sh` also references default config during install flow.
- edge_cases_or_failure_modes: Missing/malformed required default config blocks config loading. Invalid optional config is nonfatal. Runtime root is JSON-escaped before placeholder replacement to avoid quote/backslash corruption. Managed hook replacement filters only commands matching `hooks/(loop-codex-stop-hook.sh|pr-loop-stop-hook.sh)`, preserving unrelated hooks.
- validation_or_tests: `tests/test-unified-codex-config.sh` asserts `default_config.json` keeps `codex_model` and `codex_effort` keys. `tests/test-config-merge.sh` covers default/user/project merge behavior. `tests/test-codex-hook-install.sh` covers Codex hook install behavior.
- skip_candidate: `no`

### ASK_GEMINI-HZ-034 `file` `commands/refine-plan.md`
- cursor: `[_]`
- core_role: Slash-command workflow contract for refining annotated implementation plans into comment-free refined plans plus QA ledgers. It is planning-only and explicitly forbids repository code implementation or RLCR auto-start in `commands/refine-plan.md:19-28`.
- algorithmic_behavior: Defines a strict sequential pipeline: argument setup, config load, IO validation, comment extraction, classification, processing, refined plan generation, QA generation, and atomic write in `commands/refine-plan.md:30-43`. It reuses gen-plan schema, removes `CMT:/ENDCMT` blocks, classifies feedback, applies plan edits/research, and writes refined plan plus QA.
- inputs_outputs_state: Inputs are `$ARGUMENTS`, required `--input`, optional `--output`, `--qa-dir`, `--alt-language`, and mutually exclusive `--discussion|--direct` in `commands/refine-plan.md:46-83`. Outputs are `OUTPUT_FILE`, `QA_FILE`, and optional language variants named by inserting `_<code>` before extension in `commands/refine-plan.md:493-557`.
- gates_or_invariants: Validation gates include exit-code mapping from `validate-refine-plan-io.sh` in `commands/refine-plan.md:157-181`, stateful CMT scanner requirements in `commands/refine-plan.md:184-258`, required schema sections in `commands/refine-plan.md:384-403`, and pre-QA checks for no comment markers, valid AC/task refs, valid routing tags, and convergence consistency in `commands/refine-plan.md:427-438`.
- dependencies_and_callers: Calls `${CLAUDE_PLUGIN_ROOT}/scripts/validate-refine-plan-io.sh` and reads `${CLAUDE_PLUGIN_ROOT}/prompt-template/plan/refine-plan-qa-template.md` in `commands/refine-plan.md:159-163` and `commands/refine-plan.md:442-445`. Config semantics depend on `${CLAUDE_PLUGIN_ROOT}/scripts/lib/config-loader.sh` and `${CLAUDE_PLUGIN_ROOT}/config/default_config.json` in `commands/refine-plan.md:86-99`.
- edge_cases_or_failure_modes: Handles invalid/missing `--alt-language`, unsupported config language, empty-only comments, nested/stray/unclosed comment blocks, markers inside fences or HTML comments, ambiguous classification, unresolved decisions, unwritable dirs, translation failures, and partial finalization risk. Atomic write requires same-directory temp files and main in-place plan replacement last in `commands/refine-plan.md:531-557`.
- validation_or_tests: `tests/test-refine-plan.sh:720-748` asserts scanner/classification requirements, `tests/test-refine-plan.sh:752-817` asserts mode, schema, language, filename, atomic write, and QA template coverage, and `tests/test-refine-plan.sh:1044-1343` exercises `validate-refine-plan-io.sh` exit codes and success modes.
- skip_candidate: `no`

### ASK_GEMINI-HZ-064 `file` `scripts/rlcr-stop-gate.sh`
- cursor: `[_]`
- core_role: Non-hook wrapper for running RLCR stop-hook logic from skill/workflow contexts while reusing `hooks/loop-codex-stop-hook.sh` enforcement and phase transitions.
- algorithmic_behavior: Parses optional `--session-id`, `--transcript-path`, `--project-root`, and `--json`; builds a Claude/Codex-style Stop hook JSON payload; pipes it to `hooks/loop-codex-stop-hook.sh`; maps hook output into wrapper-level allow/block/error statuses in `scripts/rlcr-stop-gate.sh:43-145`.
- inputs_outputs_state: Inputs include CLI flags, `CLAUDE_SESSION_ID`, `CLAUDE_TRANSCRIPT_PATH`, `CLAUDE_PROJECT_DIR`, `CODEX_MODEL`, and `CODEX_PERMISSION_MODE` in `scripts/rlcr-stop-gate.sh:21-29`. Output is human text or raw JSON. Exit states are `0` allow, `10` block, and `20` wrapper/runtime error as documented in `scripts/rlcr-stop-gate.sh:8-14`.
- gates_or_invariants: Requires executable `hooks/loop-codex-stop-hook.sh` and `jq` in `scripts/rlcr-stop-gate.sh:76-84`. The hook input always includes `hook_event_name: "Stop"`, `stop_hook_active: false`, `cwd`, model, permission mode, and optional session/transcript fields in `scripts/rlcr-stop-gate.sh:86-104`.
- dependencies_and_callers: Directly wraps `hooks/loop-codex-stop-hook.sh`, which discovers active loop state via `CLAUDE_PROJECT_DIR`, `.humanize/rlcr`, and `loop-common.sh` in `hooks/loop-codex-stop-hook.sh:42-80`. It depends on hook JSON decisions where empty output means allow and `decision == "block"` means continue loop.
- edge_cases_or_failure_modes: Unknown or value-less flags exit `20`; missing hook or `jq` exits `20`; nonzero hook exit is normalized to `20`; non-JSON hook output exits `20`; any non-`block` nonempty JSON decision is unexpected and exits `20`.
- validation_or_tests: `tests/test-allowlist-validators.sh:537-575` asserts wrapped direct execution attempts such as `VAR=1 ./scripts/rlcr-stop-gate.sh` and `nohup nice -n 5 ./scripts/rlcr-stop-gate.sh` are blocked by Bash validator rules during active loop contexts.
- skip_candidate: `no`

### ASK_GEMINI-HZ-094 `file` `tests/test-monitor-e2e-deletion.sh`
- cursor: `[_]`
- core_role: Focused executable test shard for monitor deletion behavior. It delegates to real monitor e2e helper functions and runs only deletion-related tests.
- algorithmic_behavior: Sources `tests/test-monitor-e2e-real.sh`, prints a deletion test header, runs `monitor_test_bash_deletion`, `monitor_test_zsh_deletion`, and `monitor_test_pr_deletion`, then exits `0` only if `TESTS_FAILED` is zero in `tests/test-monitor-e2e-deletion.sh:4-22`.
- inputs_outputs_state: Input is the sourced helper library plus ambient shell tools (`bash`, optional `zsh`) and repository scripts. Output is pass/fail console summary using shared `TESTS_PASSED`/`TESTS_FAILED` counters from `tests/test-monitor-e2e-real.sh:20-37`.
- gates_or_invariants: Uses `set -euo pipefail` in `tests/test-monitor-e2e-deletion.sh:3`. The shard invariant is that deletion of `.humanize/rlcr` or `.humanize/pr-loop` during monitoring should terminate gracefully with no glob errors and clean exit behavior.
- dependencies_and_callers: Depends on `tests/test-monitor-e2e-real.sh`. Bash RLCR deletion test creates fake RLCR state and goal tracker, sources real `scripts/humanize.sh`, runs `_humanize_monitor_codex`, deletes `.humanize/rlcr`, and verifies graceful output in `tests/test-monitor-e2e-real.sh:56-228`. Zsh variant is in `tests/test-monitor-e2e-real.sh:233-372`. PR-loop deletion test runs `humanize monitor pr --once` and deletes the PR loop directory in `tests/test-monitor-e2e-real.sh:691-829`.
- edge_cases_or_failure_modes: Monitor not exiting within bounded loop is failure. Missing `zsh` skips zsh deletion case. Output containing `no matches found` or `bad pattern` fails. Missing “Monitoring stopped” or exit-code marker fails. PR monitor accepts clean exit indications including `Stopped`, `gracefully`, or `EXIT_CODE:0`.
- validation_or_tests: This file is itself validation coverage and is listed as a split shard. It verifies deletion behavior across bash RLCR, zsh RLCR, and PR monitor surfaces.
- skip_candidate: `no`

### ASK_GEMINI-HZ-124 `file` `hooks/lib/template-loader.sh`
- cursor: `[_]`
- core_role: Shared template loading/rendering library for RLCR and PR loop hooks. It turns prompt/block templates into hook messages while preserving safe fallback behavior.
- algorithmic_behavior: `get_template_dir` resolves plugin `prompt-template`; `load_template` reads a named template or warns; `render_template` performs single-pass `{{VAR}}` substitution via environment-prefixed awk variables; `load_and_render` combines load/render; `append_template` appends optional templates; `load_and_render_safe` falls back when missing or empty; `validate_template_dir` checks required subdirs in `hooks/lib/template-loader.sh:24-238`.
- inputs_outputs_state: Inputs are a template directory, relative template name, fallback string, and `VAR=value` assignments. Output is rendered text. Missing variables remain as placeholders per `hooks/lib/template-loader.sh:7-14` and `hooks/lib/template-loader.sh:114-121`.
- gates_or_invariants: Single-pass substitution is the key safety invariant: inserted values are not rescanned, preventing placeholder injection and accidental replacement inside variable content in `hooks/lib/template-loader.sh:48-56` and `hooks/lib/template-loader.sh:69-128`. `validate_template_dir` requires `block`, `codex`, `claude`, `plan`, and `pr-loop` subdirectories in `hooks/lib/template-loader.sh:213-238`.
- dependencies_and_callers: Sourced by `hooks/lib/loop-common.sh:227-235`, which initializes `TEMPLATE_DIR` and degrades to inline fallbacks if validation fails. Used heavily by `hooks/loop-codex-stop-hook.sh` for block prompts and phase prompts, including code-review audit generation at `hooks/loop-codex-stop-hook.sh:1136-1142`. Also used by `scripts/setup-pr-loop.sh` and `scripts/bitlesson-validate-delta.sh`.
- edge_cases_or_failure_modes: Missing template returns empty plus warning; safe loader suppresses missing-template errors and emits fallback. If awk fails, `render_template` returns nonzero and safe loader falls back. Malformed placeholder without closing `}}` treats `{{` literally in `hooks/lib/template-loader.sh:101-108`.
- validation_or_tests: `tests/test-template-loader.sh:41-220` covers directory resolution, existing/missing loads, single/multiple/multiline substitutions, unreplaced variables, and safe fallback. `tests/robustness/test-template-stress-robustness.sh:33-180` covers large values/templates, many substitutions, regex characters, and ampersands.
- skip_candidate: `no`

### ASK_GEMINI-HZ-154 `file` `prompt-template/block/prompt-file-write.md`
- cursor: `[_]`
- core_role: Block template for denying writes to generated RLCR prompt files, enforcing the invariant that agents may read instructions but cannot modify their own prompt artifacts.
- algorithmic_behavior: Provides a concise denial message: prompt files contain instructions from Codex to Claude; the correct flow is read prompt, execute tasks, write results to summary, and report prompt errors in the summary in `prompt-template/block/prompt-file-write.md:1-12`.
- inputs_outputs_state: Has no template variables. Input is the write-validator/common-loop decision that a `round-*-prompt.md` write is attempted. Output is rendered block text returned to the agent.
- gates_or_invariants: The invariant is prompt immutability. `hooks/lib/loop-common.sh:781-788` wraps this template through `prompt_write_blocked_message`, with an inline fallback if the template is unavailable.
- dependencies_and_callers: Loaded through `load_and_render_safe` from `hooks/lib/template-loader.sh`. The common loop library exposes the message to write/Bash validators that detect prompt-file mutation attempts. Related PR-loop prompt block uses a separate template path in `hooks/lib/loop-common.sh:1332-1340`.
- edge_cases_or_failure_modes: If the template file is missing or empty, the fallback still blocks prompt writes, but loses the fuller instruction text. Since no variables are used, rendering cannot fail due to missing values.
- validation_or_tests: Covered indirectly by template-loader tests for existing templates/fallbacks and by validator suites that assert prompt-file write attempts are blocked. `hooks/lib/loop-common.sh:781-788` is the production call point.
- skip_candidate: `no`

### ASK_GEMINI-HZ-184 `file` `prompt-template/codex/code-review-phase.md`
- cursor: `[_]`
- core_role: Audit prompt template for RLCR Code Review Phase. It records the `codex review` invocation and expected severity-marker contract rather than feeding a prompt to Codex.
- algorithmic_behavior: Renders review round metadata, base branch, timestamp, explains that `codex review --base {{BASE_BRANCH}}` runs automated review, scans `[P0-9]` severity markers, routes issues back to remediation, and transitions to Finalize when none are found in `prompt-template/codex/code-review-phase.md:1-36`.
- inputs_outputs_state: Template variables are `{{REVIEW_ROUND}}`, `{{BASE_BRANCH}}`, and `{{TIMESTAMP}}`. Output is `round-{{REVIEW_ROUND}}-review-prompt.md` audit file plus related command/output/log files listed in `prompt-template/codex/code-review-phase.md:30-36`.
- gates_or_invariants: The review gate is severity-marker based: issues found block and produce a fix prompt; no issues transition to Finalize in `prompt-template/codex/code-review-phase.md:12-18`. The template also documents that `codex review` does not accept prompt input in `prompt-template/codex/code-review-phase.md:3-4`.
- dependencies_and_callers: Rendered by `run_codex_code_review` in `hooks/loop-codex-stop-hook.sh:1105-1163`, using `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:1136-1142`. The production code also passes `BASE_COMMIT`, `REVIEW_BASE`, and `REVIEW_BASE_TYPE`; this template currently ignores those extra variables, while the fallback includes more fields in `hooks/loop-codex-stop-hook.sh:1123-1135`.
- edge_cases_or_failure_modes: Missing template falls back to a simpler audit prompt. Because this template uses `BASE_BRANCH` rather than the computed fixed `review_base`, the audit file may underrepresent commit-based review context even though the actual command uses `review_base` in `hooks/loop-codex-stop-hook.sh:1110-1163`.
- validation_or_tests: Template-loader tests cover rendering behavior. RLCR stop-hook code-review path writes this audit file and command/debug files, then blocks on failed review via `block_review_failure` in `hooks/loop-codex-stop-hook.sh:1482-1555`.
- skip_candidate: `no`

### ASK_GEMINI-HZ-214 `file` `tests/robustness/test-path-validation-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable specification for RLCR plan path and content validation in `scripts/setup-rlcr-loop.sh`.
- algorithmic_behavior: Creates an isolated temp git repo, mocks `codex`, creates plan fixtures, runs production `setup-rlcr-loop.sh` with `CLAUDE_PROJECT_DIR="$TEST_DIR"`, classifies path/content validation errors by output regex, and asserts acceptance/rejection cases in `tests/robustness/test-path-validation-robustness.sh:12-113`.
- inputs_outputs_state: Inputs are generated plan paths/content and production setup script. State includes temp repo, `.gitignore` to keep plan files untracked/gitignored, mock `codex` on `PATH`, and `.humanize/rlcr` cleanup before each case in `tests/robustness/test-path-validation-robustness.sh:16-48` and `tests/robustness/test-path-validation-robustness.sh:83-89`. Output is pass/fail test summary via `print_test_summary`.
- gates_or_invariants: Positive gates accept normal relative names, root filename, dash/underscore, nested dirs, dotted filenames, long filenames, and deep paths in `tests/robustness/test-path-validation-robustness.sh:122-170` and `tests/robustness/test-path-validation-robustness.sh:387-412`. Negative gates reject absolute paths, whitespace, shell metacharacters, symlink files, parent-directory symlinks, empty/comment-only/short/nonexistent files, and directory-as-file in `tests/robustness/test-path-validation-robustness.sh:179-365` and `tests/robustness/test-path-validation-robustness.sh:425-480`.
- dependencies_and_callers: Tests production validation in `scripts/setup-rlcr-loop.sh:452-616`, which rejects absolute paths, spaces, shell metacharacters, symlink files and parent dirs, missing/unreadable/out-of-project paths, submodule paths, and non-gitignored plan files. Content gates are in `scripts/setup-rlcr-loop.sh:619-650` onward, including minimum line count and non-comment content.
- edge_cases_or_failure_modes: The test notes Unicode/CJK/emoji path characters are allowed in `tests/robustness/test-path-validation-robustness.sh:414-416`. Long filename test is skipped as pass if the filesystem rejects fixture creation. The helper treats “requires codex” and “must be gitignored” as evidence path validation passed, but this branch’s mock codex means most accepted paths should proceed beyond dependency checks.
- validation_or_tests: This file is the validation artifact. It ends with `print_test_summary "Path Validation Robustness Test Summary"` and exits with the test helper status in `tests/robustness/test-path-validation-robustness.sh:482-487`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 8 section headings above, one per assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`