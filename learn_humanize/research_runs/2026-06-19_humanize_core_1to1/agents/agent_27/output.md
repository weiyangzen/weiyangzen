# agent_27 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`

## Item Evidence

### HZ-027 `file` `agents/bitlesson-selector.md`
- cursor: `[_]`
- core_role: Agent prompt contract for selecting applicable BitLesson knowledge before a task/sub-task; frontmatter identifies `bitlesson-selector`, model `haiku`, and tools `Read, Grep` at `agents/bitlesson-selector.md:1-5`.
- algorithmic_behavior: Defines a precision-first classifier: consume task, related paths, and `.humanize/bitlesson.md`, return only directly relevant lesson IDs, or `NONE` when no lesson applies (`agents/bitlesson-selector.md:10-17`, `:26-31`).
- inputs_outputs_state: Inputs are sub-task description, path list, and BitLesson content; output must be exactly `LESSON_IDS:` plus `RATIONALE:` with no extra sections (`agents/bitlesson-selector.md:32-41`). No persistent state is written by this prompt file.
- gates_or_invariants: Stable two-line output is the main invariant; weakly related lessons must be excluded (`agents/bitlesson-selector.md:28-39`). Runtime parser enforces nonempty `LESSON_IDS` and `RATIONALE` in `scripts/bitlesson-select.sh:242-267`.
- dependencies_and_callers: The prompt names `scripts/bitlesson-select.sh` as runtime executor and describes provider routing by `bitlesson_model` (`agents/bitlesson-selector.md:19-24`). The script sources `scripts/lib/model-router.sh` and dynamically builds a matching prompt (`scripts/bitlesson-select.sh:11`, `:148-179`).
- edge_cases_or_failure_modes: Empty or lesson-free BitLesson files bypass model selection with `NONE` in runtime (`scripts/bitlesson-select.sh:99-108`); direct agent prompt and runtime prompt diverge slightly because runtime forbids tools/repository inspection (`scripts/bitlesson-select.sh:168-175`) while frontmatter permits `Read, Grep`.
- validation_or_tests: `tests/test-bitlesson-select-routing.sh` covers provider routing, fallback behavior, placeholder knowledge bases, and stable selector output; `tests/test-codex-hook-install.sh` verifies the installed `bitlesson-selector` shim dispatches into this runtime path.
- skip_candidate: `no`

### HZ-057 `file` `scripts/rlcr-stop-gate.sh`
- cursor: `[_]`
- core_role: Non-hook wrapper around `hooks/loop-codex-stop-hook.sh`, allowing skills or scripts to reuse Stop-hook loop enforcement and phase transitions (`scripts/rlcr-stop-gate.sh:3-15`, `:27`).
- algorithmic_behavior: Resolves project root, validates hook and `jq`, builds canonical Stop-hook JSON, invokes the real hook with `CLAUDE_PROJECT_DIR`, then maps hook output into wrapper exits: allow, block, or runtime error (`scripts/rlcr-stop-gate.sh:17-34`, `:81-97`, `:108-178`).
- inputs_outputs_state: Inputs include `--session-id`, `--transcript-path`, `--project-root`, `--json`, and env defaults `CLAUDE_SESSION_ID`, `CLAUDE_TRANSCRIPT_PATH`, `CODEX_MODEL`, `CODEX_PERMISSION_MODE` (`scripts/rlcr-stop-gate.sh:29-34`, `:48-79`). Outputs are stdout/stderr messages and exit codes 0, 10, or 20 (`:8-11`).
- gates_or_invariants: No resolved project root is benign allow (`scripts/rlcr-stop-gate.sh:81-87`); missing hook or `jq` is wrapper error (`:89-97`); empty hook output is allow (`:136-140`); `decision: block` is exit 10 (`:152-160`); unknown decisions fail closed as wrapper errors (`:176-178`).
- dependencies_and_callers: Sources `hooks/lib/project-root.sh` for deterministic root resolution (`scripts/rlcr-stop-gate.sh:25-27`; resolver priority at `hooks/lib/project-root.sh:5-12`, `:41-53`). Delegates all loop-state semantics to `hooks/loop-codex-stop-hook.sh`.
- edge_cases_or_failure_modes: Explicit null handling prevents an empty `session_id` from collapsing the entire JSON object and dropping `transcript_path` (`scripts/rlcr-stop-gate.sh:103-123`). Non-JSON hook output and nonzero hook exits are converted to exit 20 (`:130-146`).
- validation_or_tests: `tests/test-stop-gate.sh:64-204` covers active-loop blocking, `--project-root`, tracked Humanize state, unrelated `.humanize-*` paths, and no-active-loop allow; `tests/test-stop-gate.sh:206-287` covers the empty-session transcript forwarding regression.
- skip_candidate: `no`

### HZ-087 `file` `tests/test-monitor-e2e-deletion.sh`
- cursor: `[_]`
- core_role: Thin executable test shard for monitor deletion behavior; it sources the real e2e test library and runs the bash and zsh deletion cases (`tests/test-monitor-e2e-deletion.sh:1-14`).
- algorithmic_behavior: Prints a test header, invokes `monitor_test_bash_deletion` and `monitor_test_zsh_deletion`, prints accumulated pass/fail counters, and exits 0 only when `TESTS_FAILED` is zero (`tests/test-monitor-e2e-deletion.sh:7-21`).
- inputs_outputs_state: Inputs are inherited shell environment plus functions/globals from `tests/test-monitor-e2e-real.sh`; outputs are TAP-like console pass/fail lines and process exit status. State is `TESTS_PASSED` and `TESTS_FAILED` from the sourced file (`tests/test-monitor-e2e-real.sh:25-37`).
- gates_or_invariants: The sourced bash case creates a real loop fixture, starts `_humanize_monitor_codex`, deletes `.humanize/rlcr`, and requires clean exit, deletion reason, no glob errors, scroll-reset source, and `EXIT_CODE:0` (`tests/test-monitor-e2e-real.sh:56-228`).
- dependencies_and_callers: Depends on `tests/test-monitor-e2e-real.sh` (`tests/test-monitor-e2e-deletion.sh:4-5`), which sources `scripts/humanize.sh` and runs the real monitor (`tests/test-monitor-e2e-real.sh:144-149`). Included in aggregate tests at `tests/run-all-tests.sh:81`.
- edge_cases_or_failure_modes: zsh case skips rather than fails when `zsh` is unavailable (`tests/test-monitor-e2e-real.sh:233-240`). Timeout waiting for monitor termination causes failure (`tests/test-monitor-e2e-real.sh:167-182`). Cleanup kills lingering test monitor processes by fixture pattern (`:46-51`).
- validation_or_tests: This file is itself the validation entrypoint; runtime behavior under test is the graceful deletion branch in `scripts/humanize.sh:838-844` and the no-log polling deletion branch at `scripts/humanize.sh:899-908`.
- skip_candidate: `no`

### HZ-117 `file` `prompt-template/block/claude-eyes-timeout.md`
- cursor: `[_]`
- core_role: Static block template for a GitHub Claude-bot acknowledgement timeout; it explains that no `eyes` reaction arrived after templated retry/wait values (`prompt-template/block/claude-eyes-timeout.md:1-4`).
- algorithmic_behavior: Provides human remediation steps: verify app installation, permissions, PR state, then post a new trigger comment after configuration is fixed (`prompt-template/block/claude-eyes-timeout.md:5-18`).
- inputs_outputs_state: Inputs are placeholders `RETRY_COUNT` and `TOTAL_WAIT_SECONDS`; output is rendered Markdown. The template itself reads/writes no state and defines no executable transition.
- gates_or_invariants: Intended invariant is timeout escalation after exhausted retries, but the file contains only message text. No retry counter, reaction polling, or gate transition is implemented here.
- dependencies_and_callers: Narrow searches found no `load_and_render_safe`, script, hook, or test caller for `block/claude-eyes-timeout.md`; only the file itself and generic mock `gh` reaction fixtures mention related reaction concepts.
- edge_cases_or_failure_modes: If rendered without variables, placeholders remain visible. The message assumes GitHub App configuration is the failure domain and does not encode alternate recovery paths.
- validation_or_tests: Covered only indirectly by generic template loading/reference sweeps such as `tests/test-templates-comprehensive.sh`; no direct behavioral test or active runtime caller was found.
- skip_candidate: `yes: likely inactive/orphaned template in this checkout; message-only artifact, not an implemented core transition`

### HZ-147 `file` `prompt-template/block/work-summary-missing.md`
- cursor: `[_]`
- core_role: Stop-hook block template used when an RLCR round/finalize summary file is missing (`prompt-template/block/work-summary-missing.md:1-8`).
- algorithmic_behavior: Instructs the worker to write the required summary file and include implemented work, files changed, tests, and remaining items before retrying exit (`prompt-template/block/work-summary-missing.md:10-16`).
- inputs_outputs_state: Input is `SUMMARY_FILE`; output is rendered Markdown embedded in the Stop-hook JSON block reason. It does not directly mutate state.
- gates_or_invariants: The hook selects `finalize-summary.md` in finalize phase or `round-N-summary.md` otherwise, blocks if the file does not exist, renders this template, and emits `decision: block` with a phase-specific system message (`hooks/loop-codex-stop-hook.sh:788-820`).
- dependencies_and_callers: Runtime caller is `load_and_render_safe "$TEMPLATE_DIR" "block/work-summary-missing.md"` in `hooks/loop-codex-stop-hook.sh:801-805`; fallback text exists if the template cannot be loaded.
- edge_cases_or_failure_modes: Missing template falls back to a shorter built-in message (`hooks/loop-codex-stop-hook.sh:801-805`). Existing but malformed summaries pass this existence gate and are handled by later summary/content gates.
- validation_or_tests: `tests/test-stop-gate.sh:18-89` creates an active loop without a summary and expects `rlcr-stop-gate` to block with a real loop reason; template rendering is also covered by generic template tests.
- skip_candidate: `no`

### HZ-177 `file` `scripts/lib/model-router.sh`
- cursor: `[_]`
- core_role: Shared shell routing library that maps configured model names and effort levels to supported providers for BitLesson/model execution paths (`scripts/lib/model-router.sh:1-10`).
- algorithmic_behavior: `detect_provider` routes `gpt-*` and `oN*` to `codex`, Claude-like names to `claude`, and rejects empty/unknown models (`scripts/lib/model-router.sh:10-30`). `check_provider_dependency` maps provider to required binary and validates `PATH` (`:32-60`). `map_effort` validates effort/provider and maps Claude `xhigh` to `high` (`:62-91`).
- inputs_outputs_state: Inputs are shell arguments: model name, provider, effort. Outputs are provider/effort strings on stdout, diagnostics on stderr, and nonzero return for invalid inputs. No persistent state.
- gates_or_invariants: Only providers `codex` and `claude` are accepted (`scripts/lib/model-router.sh:36-47`, `:66-73`); only `xhigh`, `high`, `medium`, `low` efforts are accepted (`:75-82`); missing binaries are hard failures with install hints (`:49-59`).
- dependencies_and_callers: Sourced by `scripts/bitlesson-select.sh:11`, which calls `detect_provider` for `bitlesson_model` and `check_provider_dependency` before invoking the selector (`scripts/bitlesson-select.sh:115-130`).
- edge_cases_or_failure_modes: Matching is case-sensitive for `gpt-*` but case-insensitive for Claude regex; any model string containing `haiku`, `sonnet`, or `opus` routes to Claude, which may overmatch custom names (`scripts/lib/model-router.sh:18-28`). Unsupported newer provider families are rejected.
- validation_or_tests: `tests/test-model-router.sh:29-230` covers Codex/Claude/unknown/empty model routing; `:232-298` covers missing/present binaries; `:300-420` covers effort mapping and invalid effort failures. `tests/test-bitlesson-select-routing.sh` validates integration with selector routing.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6/6 item sections present, one section per assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`