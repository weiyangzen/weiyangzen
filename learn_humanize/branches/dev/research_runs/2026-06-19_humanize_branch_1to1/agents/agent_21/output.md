# agent_21 dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `eec73c4dfcc4f9791933e3cbaa616d4f261ed9e2`

## Item Evidence

### DEV-HZ-021 `directory` `skills/ask-codex`
- cursor: `[_]`
- core_role: Claude skill wrapper for one-shot Codex consultation. The directory contains one file, [skills/ask-codex/SKILL.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/skills/ask-codex/SKILL.md:1), and acts as the command-facing contract for `scripts/ask-codex.sh`.
- algorithmic_behavior: Defines the skill metadata and allowed tool boundary at lines 1-5, then prescribes safe invocation patterns. The key algorithmic rule is argument boundary preservation: free-form question text must be passed as one quoted argument, while flags such as `--codex-model` and `--codex-timeout` must remain separate shell arguments, lines 14-28.
- inputs_outputs_state: Input is `$ARGUMENTS` from the skill call; output is delegated to `ask-codex.sh`, whose stdout is the Codex response and stderr is status, lines 38-42. The skill documents persistent output under `.humanize/skill/<timestamp>/output.md`, line 55.
- gates_or_invariants: The wrapper forbids bare `$ARGUMENTS` expansion, lines 30-36, preventing shell re-parsing of metacharacters before the runtime script can validate input. It also limits tool access to `${CLAUDE_PLUGIN_ROOT}/scripts/ask-codex.sh:*`, line 5.
- dependencies_and_callers: Referenced by command docs and prompt templates for analyze-task routing, including `commands/gen-plan.md`, `commands/start-rlcr-loop.md`, and `prompt-template/explore/worker-prompt.md`. Runtime dependency is [scripts/ask-codex.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/scripts/ask-codex.sh:1).
- edge_cases_or_failure_modes: If callers reconstruct flags incorrectly or use unquoted expansion, shell syntax errors or command injection-like argument splitting can occur before `ask-codex.sh` starts. Non-zero script exits must be reported, lines 40-51.
- validation_or_tests: [tests/test-ask-codex.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/tests/test-ask-codex.sh:553) checks that the skill warns against bare `$ARGUMENTS`, documents the quoted simple invocation, and requires a quoted final argument for free-form text.
- skip_candidate: `no`

### DEV-HZ-051 `file` `scripts/ask-codex.sh`
- cursor: `[_]`
- core_role: Active one-shot workflow runner that turns a `/humanize:ask-codex` skill request into a scoped `codex exec` invocation, while creating project-local evidence and cache artifacts.
- algorithmic_behavior: Parses options until the first positional token or `--`, then joins remaining tokens into the question, lines 86-147. It validates Codex availability, non-empty question, model characters, and effort characters, lines 153-185. It resolves project root via `resolve_project_root`, lines 192-196; creates `.humanize/skill/<unique-id>` and cache directories, lines 202-218; writes `input.md`, lines 224-238; probes supported Codex hook-disable feature names, lines 244-270; builds `codex exec` args with model, effort, sandbox mode, and project root, lines 272-285; then runs Codex through `run_with_timeout`, lines 323-327.
- inputs_outputs_state: Inputs are CLI flags, question text, config-backed `DEFAULT_CODEX_MODEL` and `DEFAULT_CODEX_EFFORT` from `hooks/lib/loop-common.sh`, environment variables such as `CLAUDE_PROJECT_DIR`, `XDG_CACHE_HOME`, and `HUMANIZE_CODEX_BYPASS_SANDBOX`. Outputs are clean Codex stdout, stderr status lines, `.humanize/skill/<id>/input.md`, `output.md`, `metadata.md`, and cache files `codex-run.cmd`, `codex-run.out`, `codex-run.log`, lines 15-17 and 291-305.
- gates_or_invariants: Fails closed when Codex is missing, the question is empty, timeout is malformed, or model/effort contains unsafe characters, lines 120-185. Default sandbox mode is `--full-auto`; bypass requires explicit `HUMANIZE_CODEX_BYPASS_SANDBOX=true` or `1`, lines 279-283. Empty Codex stdout is not success; it writes `status: empty_response` and exits 1, lines 390-414.
- dependencies_and_callers: Sources [scripts/portable-timeout.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/scripts/portable-timeout.sh:1) and [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/hooks/lib/loop-common.sh:31). The model defaults come from [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/hooks/lib/loop-common.sh:208), where config values fall back to `gpt-5.5` and `high`. Called by the `ask-codex` skill and analyze-task workflows.
- edge_cases_or_failure_modes: Timeout exit 124 gets a dedicated metadata status and retry suggestion, lines 338-360. Non-zero Codex exits propagate the original exit code after writing error metadata and tailing stderr, lines 363-388. Home cache creation failure falls back to project-local `cache`, lines 214-218. Concurrent calls avoid collisions by including timestamp, PID, and random bytes in `UNIQUE_ID`, lines 202-203. Older Codex builds are handled by probing which hook-disable names are accepted before adding them, lines 257-266.
- validation_or_tests: [tests/test-ask-codex.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/tests/test-ask-codex.sh:152) covers empty input, help, bad flags, invalid model/effort, success artifacts, non-zero exits, empty output, timeout metadata, concurrent directory uniqueness, argument parsing, cache fallback, and nested hook-disable probing.
- skip_candidate: `no`

### DEV-HZ-081 `file` `tests/test-cancel-session.sh`
- cursor: `[_]`
- core_role: Executable specification for session-scoped RLCR cancellation behavior in [scripts/cancel-rlcr-session.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/scripts/cancel-rlcr-session.sh:1).
- algorithmic_behavior: Builds a temporary project with multiple RLCR session directories, lines 35-50, then checks that cancellation targets only the requested session and transforms its active state by creating `.cancel-requested` and renaming the active state file to `cancel-state.md`, lines 75-103.
- inputs_outputs_state: Inputs are helper flags `--project`, `--session-id`, optional `--force`, and a legacy positional session id. Expected outputs include specific exit codes, `CANCELLED <session>` stdout, renamed state files, and untouched sibling session state.
- gates_or_invariants: Missing session id must exit 3, lines 51-61. Non-existent session must exit 1, lines 63-73. Finalize-phase cancellation requires `--force` and exits 2 otherwise, lines 105-124. Unsafe session ids with path separators, leading dots, parent tokens, or traversal shapes must be rejected with exit 3, lines 126-149.
- dependencies_and_callers: Directly exercises [scripts/cancel-rlcr-session.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/scripts/cancel-rlcr-session.sh:28), whose implementation parses flags, validates session ids, detects `state.md`, `methodology-analysis-state.md`, or `finalize-state.md`, and performs `touch` plus `mv`, lines 28-124.
- edge_cases_or_failure_modes: The test explicitly guards against cross-session mutation and path traversal. It also preserves backward compatibility through the legacy positional form, lines 152-162.
- validation_or_tests: This file is itself validation. It uses a per-test `mktemp` tree and reports aggregate pass/fail counts, lines 29-36 and 164-173. I did not execute it because this run is research-only and the branch export is read-only by instruction.
- skip_candidate: `no`

### DEV-HZ-111 `file` `tests/test-stop-gate.sh`
- cursor: `[_]`
- core_role: Executable specification for the non-hook RLCR stop gate wrapper [scripts/rlcr-stop-gate.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/scripts/rlcr-stop-gate.sh:1), mainly project-root selection, tracked-state blocking, and hook input forwarding.
- algorithmic_behavior: Creates active-loop fixtures with `.humanize/rlcr/<session>/state.md` and a copied plan, lines 18-59. It then invokes the gate from different cwd and env combinations, asserting block or allow decisions and wrapper exit-code mapping.
- inputs_outputs_state: Inputs include cwd, `CLAUDE_PROJECT_DIR`, `--project-root`, `--transcript-path`, `--json`, and mock hook output. Outputs are wrapper exit codes 0 or 10, text prefixes `ALLOW:` or `BLOCK:`, and JSON forwarded to the hook when using the mock in test 6.
- gates_or_invariants: Default root resolution must use the target project context and block active loops, lines 64-89. `--project-root` must override cwd and inherited env, lines 91-116 and 298-318. Tracked `.humanize/rlcr` state must block before ordinary loop validation, lines 118-145, while `.humanize-backup` and `.humanizeconfig` must not be confused with loop state, lines 147-178. No active loop must allow stop, lines 180-204.
- dependencies_and_callers: Exercises [scripts/rlcr-stop-gate.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/scripts/rlcr-stop-gate.sh:22), which sources [hooks/lib/project-root.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/hooks/lib/project-root.sh:51), wraps `hooks/loop-codex-stop-hook.sh`, builds Stop-hook JSON with `jq`, and maps hook decisions to wrapper exits, lines 22-178.
- edge_cases_or_failure_modes: Test 6 covers a prior `jq` object-collapse regression: empty `session_id` must become null without dropping a real `transcript_path`, lines 206-287. The implementation uses explicit `if length > 0 then ... else null end`, [scripts/rlcr-stop-gate.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/scripts/rlcr-stop-gate.sh:108).
- validation_or_tests: This file is itself validation. It depends on `tests/test-helpers.sh`, `jq`, git fixture setup, and a mock hook. I did not execute it due to the research-only instruction.
- skip_candidate: `no`

### DEV-HZ-141 `file` `prompt-template/block/finalize-state-file-modification.md`
- cursor: `[_]`
- core_role: Blocking prompt template for attempts to modify `finalize-state.md` during the Finalize Phase.
- algorithmic_behavior: Provides the exact denial message: `finalize-state.md` is loop-managed, and the user/agent should instead run the code-simplifier agent, commit changes, and write `finalize-summary.md`, lines 1-8.
- inputs_outputs_state: Has no dynamic placeholders. Input is selection by validator code; output is a rendered block message on stderr through `load_and_render_safe`.
- gates_or_invariants: The invariant is that `finalize-state.md` remains system-owned during Finalize Phase. The related renderer is `finalize_state_file_blocked_message` in [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/hooks/lib/loop-common.sh:873), which uses this template and falls back to a shorter hard-coded message if loading fails.
- dependencies_and_callers: Called indirectly by write/bash validators through the common message helper. It coordinates with other state-file block templates such as `state-file-modification.md` and Finalize-specific contract access blocking.
- edge_cases_or_failure_modes: If the template is missing or malformed, `load_and_render_safe` fallback still blocks, so enforcement does not depend solely on this file. If wording becomes stale, the gate still blocks but may send agents to the wrong Finalize artifact.
- validation_or_tests: Covered indirectly by validator tests that exercise loop state and file-modification guards; the direct implementation reference is [hooks/lib/loop-common.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/hooks/lib/loop-common.sh:873).
- skip_candidate: `no`

### DEV-HZ-171 `file` `prompt-template/block/wrong-file-location.md`
- cursor: `[_]`
- core_role: Blocking prompt template for reads of loop files from the wrong location, steering agents back to the active loop directory.
- algorithmic_behavior: Renders `{{FILE_PATH}}`, `{{ACTIVE_LOOP_DIR}}`, and `{{CURRENT_ROUND}}` into a diagnostic that lists the current round prompt and summary paths and suggests a direct `cat {{FILE_PATH}}` only if that exact file is needed, lines 1-9.
- inputs_outputs_state: Inputs are placeholder values supplied by validators; output is a block message. The template does not mutate state, but it controls read-path correction at enforcement time.
- gates_or_invariants: The invariant is that current loop prompt/summary/goal tracker access must be rooted in `{{ACTIVE_LOOP_DIR}}`, not stale or copied files elsewhere. [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/hooks/loop-read-validator.sh:227) renders this template for wrong `goal-tracker.md` paths and for round files outside the active loop directory, lines 227-241 and 270-279.
- dependencies_and_callers: Depends on `loop-read-validator.sh` state detection, strict state parsing, round extraction, and `load_and_render_safe`. Coordinates with sibling templates for wrong round file and finalize contract access.
- edge_cases_or_failure_modes: If `ACTIVE_LOOP_DIR` is not found, the validator exits allow before this template is reached, [hooks/loop-read-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/hooks/loop-read-validator.sh:200). If the active state file is malformed, the validator blocks before rendering this specific location guidance, lines 211-215.
- validation_or_tests: Covered indirectly by loop read-validator tests and by references in `rg` to the render sites. I did not execute tests.
- skip_candidate: `no`

### DEV-HZ-201 `file` `scripts/lib/model-router.sh`
- cursor: `[_]`
- core_role: Shared routing helper that maps model names to execution providers, verifies provider CLI dependencies, and normalizes reasoning effort across Codex and Claude.
- algorithmic_behavior: Uses a source guard, lines 6-8. `detect_provider` rejects empty model names, routes `gpt-*` and `o<number>*` to `codex`, routes `claude-*`, `haiku`, `sonnet`, or `opus` case-insensitively to `claude`, and rejects unknown names, lines 10-30. `check_provider_dependency` maps provider to `codex` or `claude` binary and checks `PATH`, lines 32-60. `map_effort` accepts `xhigh`, `high`, `medium`, `low`, maps `xhigh` to `high` only for Claude, and passes other valid efforts through, lines 62-91.
- inputs_outputs_state: Inputs are model name, provider name, and effort string. Outputs are provider strings, mapped effort strings, or stderr diagnostics with non-zero returns. It does not write persistent state.
- gates_or_invariants: Unknown providers, unknown model patterns, empty models, and invalid efforts are hard failures. Dependency checks fail if the required binary is absent, with Codex install guidance for `codex`, lines 49-59.
- dependencies_and_callers: Sourced by [scripts/bitlesson-select.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/scripts/bitlesson-select.sh:11) and [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/tests/test-model-router.sh:8). The router itself only depends on shell builtins, `grep`, and `command -v`.
- edge_cases_or_failure_modes: Model routing is prefix/pattern based, so new providers or model families fail closed until added. Claude cannot receive `xhigh`; the helper logs an info line and downgrades it to `high`, lines 84-87. It does not validate that a routed Codex model is actually available to the installed CLI.
- validation_or_tests: [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/dev/tests/test-model-router.sh:30) covers Codex model patterns, Claude aliases and full names, unknown and empty models, mocked binary dependency success/failure, and effort mapping/error cases through line 426.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 7 Item Evidence headings, one per assigned research row; item IDs are not repeated in this self-test to preserve exact-once heading evidence.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`