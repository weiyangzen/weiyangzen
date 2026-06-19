# agent_06 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-006 `directory` `python`
- cursor: `[_]`
- core_role: Python-side automation/runtime packages, mainly `omp-rpc` host/RPC bindings and `robomp` GitHub issue/PR automation.
- algorithmic_behavior: Recursively contains JSON-RPC command framing, host URI/tool adapters, FastAPI/proxy workflows, GitHub queue handling, sandbox/git orchestration, DB state, worker task routing, and dashboard assets.
- inputs_outputs_state: Inputs are JSON-RPC lines, GitHub webhook/API payloads, env config, git repos, sqlite rows; outputs are comments, PRs, branches, task states, logs, and RPC responses.
- gates_or_invariants: Repo allowlists, webhook/HMAC validation, task timeouts, sandbox isolation, DB issue state transitions, and integration-test gating via `ROBOMP_INTEGRATION=1`.
- dependencies_and_callers: Called by Python services/tests and coding-agent RPC integration; depends on `httpx`, FastAPI-style app code, git subprocesses, sqlite, and `omp --mode rpc`.
- edge_cases_or_failure_modes: Missing integration env skips smoke; failed GitHub proxy/auth blocks actions; git push/comment/PR failures leave DB/workspace evidence.
- validation_or_tests: `python/robomp/tests/test_worker_smoke.py` constructs a bare repo, fake GitHub API, and real `omp` worker path to assert comment/PR/branch/sqlite outcomes.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-036 `directory` `packages/tui`
- cursor: `[_]`
- core_role: Terminal UI framework for rendering, input parsing, component layout, scrollback, image/protocol support, and deterministic terminal updates.
- algorithmic_behavior: Recursively coordinates component render trees, diff rendering, terminal capability detection, keybinding parsing, input widgets, select lists, markdown/math/image renderers, and virtual terminal tests.
- inputs_outputs_state: Inputs are component state, key bytes, terminal dimensions/capabilities, image payloads; outputs are ANSI/terminal control sequences and component line arrays.
- gates_or_invariants: Width-aware truncation, stable key aliases, render cache correctness, scrollback bounds, terminal capability fallbacks, and loop-phase breadcrumbs for expensive filters.
- dependencies_and_callers: Used by `packages/coding-agent` interactive mode and renderer tests; depends on native width/capability helpers and shared utils.
- edge_cases_or_failure_modes: Wide glyphs, ANSI sequences, terminal nesting, unknown TTYs, large fuzzy-filter lists, and duplicate keybindings.
- validation_or_tests: `packages/tui/test` covers keybindings, select filtering, rendering, scroll behavior, and terminal capability regressions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-066 `file` `docs/notebook-tool-runtime.md`
- cursor: `[_]`
- core_role: Runtime architecture contract for notebook read/edit/eval behavior.
- algorithmic_behavior: Specifies that `.ipynb` file tools operate by conversion and serialization, while execution is delegated to the eval/Python kernel runtime, with cell markers and artifact/truncation behavior.
- inputs_outputs_state: Inputs are notebook JSON, virtual cell-marked text, eval code, kernel session keys; outputs are preserved notebook JSON, NDJSON/streaming eval chunks, rich display artifacts, and truncated outputs.
- gates_or_invariants: First marker/cell type/source-array validation, metadata preservation, per-call shutdown, cached kernel sessions keyed by session/cwd/interpreter, reset/cancel semantics, and one dead-kernel retry.
- dependencies_and_callers: Documents `read`, `edit`, and Python eval tool interaction; informs eval executor and notebook serializer behavior.
- edge_cases_or_failure_modes: Invalid markers, empty/unknown cells, dead kernels, concurrent resets, oversized output, and non-execution file edits.
- validation_or_tests: Documentation points to serializer/runtime contracts; relevant behavior is covered by eval and notebook-adjacent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-096 `file` `scripts/edit-benchmark.py`
- cursor: `[_]`
- core_role: Thin benchmark runner for edit workflow variants.
- algorithmic_behavior: Extracts `--variant` before common argparse, falls back to `PI_EDIT_VARIANT`, builds a `BenchmarkSpec`, and delegates execution to `run_benchmark_main` (`scripts/edit-benchmark.py:19-73`).
- inputs_outputs_state: Inputs are CLI args/env variant and benchmark fixture `test.rs`; outputs are benchmark execution through the shared runner.
- gates_or_invariants: Requires a non-empty variant and exits with status 2 if absent; keeps retry instructions fixed.
- dependencies_and_callers: Depends on `packages/typescript-edit-benchmark.runner` and its spec/prompt machinery.
- edge_cases_or_failure_modes: Missing variant, unknown downstream variant, and failed benchmark runner.
- validation_or_tests: Validated indirectly by benchmark package usage; no local unit test in file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-126 `directory` `packages/ai/src`
- cursor: `[_]`
- core_role: Multi-provider AI streaming/auth/dialect/schema/usage layer.
- algorithmic_behavior: Routes model requests to provider transports, maps reasoning/tool-choice options, manages auth/OAuth/API-key resolution, normalizes schemas, parses/serializes dialects, collects usage, and guards provider-specific streaming failures.
- inputs_outputs_state: Inputs are `Model`, context messages, tool schemas, auth stores/env, fetch streams; outputs are `AssistantMessageEventStream`, usage/cost, auth states, and provider errors.
- gates_or_invariants: Provider API switch, strict-schema fallback, retry only before replay-unsafe events, Gemini thinking-loop guard, auth refresh/disable, and no-key errors.
- dependencies_and_callers: Consumed by agent runtime and coding-agent; depends on catalog models, provider registries, auth storage, streaming utilities, and schema utilities.
- edge_cases_or_failure_modes: Expired OAuth, missing env keys, provider 429/quota reset parsing, malformed streaming deltas, incompatible tool schemas, and abort signals.
- validation_or_tests: AI tests cover auth broker, usage history, OpenRouter login, DeepSeek replay, Codex reset, Gemini loop guard, and retry hints.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-156 `directory` `packages/tui/test`
- cursor: `[_]`
- core_role: Contract/regression suite for terminal rendering and input algorithms.
- algorithmic_behavior: Recursively exercises keybinding collision rules, select filtering breadcrumbs, virtual terminal rendering, scrollback, widths, images, markdown, resize/stress behavior, and snapshots/oracles.
- inputs_outputs_state: Inputs are synthetic key bytes, virtual terminal dimensions, component states, fixtures; outputs are rendered line arrays and terminal buffer assertions.
- gates_or_invariants: No key eviction across action namespaces, balanced loop-phase stack, deterministic renders, bounded buffers, and width-safe strings.
- dependencies_and_callers: Tests `@oh-my-pi/pi-tui` primitives used by coding-agent TUI components.
- edge_cases_or_failure_modes: ANSI stripping, printable uppercase shift handling, empty filters, large lists, non-TTY terminals, and wrapped content.
- validation_or_tests: The directory is itself validation evidence.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-186 `file` `docs/tools/debug.md`
- cursor: `[_]`
- core_role: Architecture/runtime contract for the debugger tool and interactive debug menu.
- algorithmic_behavior: Defines single-session DAP launch/attach, request/action dispatch, reverse-handler registration, stepping/continue wait behavior, output/log/raw SSE/profiling/report actions, and cleanup (`docs/tools/debug.md:25-280`).
- inputs_outputs_state: Inputs are adapter configs, launch/attach args, DAP action params, timeouts; outputs are debugger state, stopped/terminated/running results, logs, bundles, and reports.
- gates_or_invariants: Single active debug session, per-action required fields/capability checks, timeout clamp 5-300s, 128KiB output ring, raw SSE caps, and idle cleanup.
- dependencies_and_callers: Documents coding-agent debug tool, DAP transport, debug menu, and renderers.
- edge_cases_or_failure_modes: No active session, unsupported DAP capability, request timeout, reverse request failure, missing adapter, and oversized streams.
- validation_or_tests: Serves as runtime spec; relevant behavior should be covered by debug tool tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-216 `file` `scripts/session-stats/analyze_search_relevance.py`
- cursor: `[_]`
- core_role: Offline analytics script for search-result relevance and follow-up behavior.
- algorithmic_behavior: Opens `~/.omp/stats.db` read-only, extracts paths from search/grep outputs, scans subsequent calls until a user message/window limit, classifies engaged reads, paging, refinement, and abandonment, then prints stats and plots a PNG.
- inputs_outputs_state: Inputs are sqlite session/tool-call rows; outputs are printed classification summaries and `scripts/session-stats/out/search-relevance.png`.
- gates_or_invariants: Read-only DB mode, regex-based path extraction for tree/flat formats, 30-call walk-ahead, and stop at next user message.
- dependencies_and_callers: Depends on sqlite, regex parsing, matplotlib/pandas-style reporting helpers if available in script environment.
- edge_cases_or_failure_modes: Missing DB, malformed result text, no following calls, unavailable plotting backend, and false path extraction.
- validation_or_tests: No direct tests; validates by deterministic offline analysis over recorded sessions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-246 `directory` `packages/coding-agent/src/auto-thinking`
- cursor: `[_]`
- core_role: Automatic thinking-level classifier for coding-agent prompts.
- algorithmic_behavior: Uses online small-model or local tiny-model prompt classifiers, trims prompt head/tail to a bounded length, parses earliest classification keyword, maps difficulty to thinking levels, and clamps to active model support.
- inputs_outputs_state: Inputs are user prompt, model/settings/auth availability, active model capability; output is a `ThinkingLevel`/effort decision or thrown fallback error.
- gates_or_invariants: No model/key availability throws, unparseable output throws, abort propagates, local mapping differs from online mapping, and model support clamps requested level.
- dependencies_and_callers: Called by AgentSession/model setup paths; depends on small model utilities, prompts, settings, and catalog thinking support.
- edge_cases_or_failure_modes: Overlong prompts, ambiguous classifier text, unavailable local model, aborted inference, and incompatible model efforts.
- validation_or_tests: Covered indirectly by thinking-level/session tests and classifier-specific behavior in package tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-276 `directory` `packages/coding-agent/src/plan-mode`
- cursor: `[_]`
- core_role: Plan-mode state, protection, approved-plan resolution, and handoff loading.
- algorithmic_behavior: Resolves approved plan files by title slug/state/listed paths, loads plan text for subagent handoff, creates read matchers protecting `local://PLAN.md` and current plan references, and defines plan state types.
- inputs_outputs_state: Inputs are plan mode state, title/user slug, cwd, local plan paths; outputs are plan text, `ToolError`s, protected resource matchers, and handoff content.
- gates_or_invariants: Missing/empty plan returns undefined or `ToolError` depending call path; scheme selectors normalized; protection persists through compaction.
- dependencies_and_callers: Used by plan mode tools, compaction protection, and subagent handoff.
- edge_cases_or_failure_modes: Empty plan file, title mismatch, stale state path, missing local file, and normalized URL mismatch.
- validation_or_tests: `packages/coding-agent/test/plan-mode-thinking-level.test.ts` covers adjacent plan role model/thinking propagation; plan utilities rely on tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-306 `directory` `packages/coding-agent/test/memories`
- cursor: `[_]`
- core_role: Regression tests for memory discovery/isolation behavior.
- algorithmic_behavior: Asserts memory context uses `memory://` URLs without leaking raw roots and that global memory consolidation is scoped per cwd/job key.
- inputs_outputs_state: Inputs are synthetic memory roots/cwd/session state; outputs are assertions about prompt/context surfaces and consolidation jobs.
- gates_or_invariants: Memory roots must not leak into developer instructions; stage-one global memory listing filters by cwd and jobs key by `global:<cwd>`.
- dependencies_and_callers: Tests memory capability/context loading and mnemopi session integration.
- edge_cases_or_failure_modes: Cross-project memory contamination and path disclosure in prompts.
- validation_or_tests: Directory is validation evidence for memory prompt and isolation contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-336 `file` `crates/pi-ast/src/block.rs`
- cursor: `[_]`
- core_role: Tree-sitter block range and visible-boundary resolver.
- algorithmic_behavior: `block_range_at` resolves the outermost named syntax node starting at a 1-indexed line; `enclosing_block_boundaries` finds opener/closer lines for visible windows.
- inputs_outputs_state: Inputs are source text, language, target/visible lines; outputs are optional block ranges or boundary line sets.
- gates_or_invariants: Rejects blank/out-of-range lines, unknown languages, syntax-error root/subtrees, continuations, and uses a one-column point range to avoid Swift separator issues.
- dependencies_and_callers: Used by hashline/block edit features and AST-aware display/edit tooling; depends on tree-sitter grammars.
- edge_cases_or_failure_modes: Syntax errors, zero-width nodes, multiline boundaries, Swift/Elisp/Python/TS quirks, and lexical fallback on root errors.
- validation_or_tests: Inline Rust tests cover TypeScript, Python, zshrc, Swift, Emacs Lisp, syntax errors, and boundaries.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-366 `file` `crates/pi-natives/src/prof.rs`
- cursor: `[_]`
- core_role: Native always-on scoped profiler for work-stack timing.
- algorithmic_behavior: RAII `profile_region` pushes/pops thread-local stack and records duration/timestamp samples into a global capped buffer; `get_work_profile(last_seconds)` aggregates folded stacks and optional SVG.
- inputs_outputs_state: Inputs are scoped region labels and time window; outputs are sample counts, total milliseconds, markdown summary, and inferno flamegraph SVG when possible.
- gates_or_invariants: `MAX_SAMPLES=10000` circular storage, thread-local stack isolation, and time-window filtering.
- dependencies_and_callers: Native crate consumers call profiling scopes around performance-sensitive operations.
- edge_cases_or_failure_modes: Deep stacks, dropped old samples, SVG generation failure, and empty time windows.
- validation_or_tests: Validated by native crate tests/usage; no separate file-specific test noted.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-396 `file` `packages/agent/src/types.ts`
- cursor: `[_]`
- core_role: Public type contract for the agent loop, tools, events, and lifecycle.
- algorithmic_behavior: Defines `AgentLoopConfig`, `AgentTool`, tool approval/concurrency/deferral/render hooks, message/tool lifecycle events, state transforms, dialect options, and auth/tool choice interfaces.
- inputs_outputs_state: Inputs are model/context/tool configs and runtime callbacks; outputs are typed events and tool/message result shapes.
- gates_or_invariants: Approval tiers, `appendOnly`, dynamic reasoning/tool selection, tool matcher digests, and lifecycle event schemas constrain runtime behavior.
- dependencies_and_callers: Imported by coding-agent, AI streams, TUI renderers, tests, and extension contracts.
- edge_cases_or_failure_modes: Type drift can break tool rendering, event replay, or session persistence.
- validation_or_tests: Compile/type checks and broad package tests validate the contract.
- skip_candidate: `yes: type surface rather than executable algorithm, but it defines core runtime contracts`

### OH_MY_HUMANIZE_MAIN-HZ-426 `file` `packages/ai/src/stream.ts`
- cursor: `[_]`
- core_role: Central provider dispatch and streaming wrapper.
- algorithmic_behavior: Resolves API keys/auth, dispatches by model API/provider, wraps Gemini loop guard, maps reasoning/tool-choice options, handles custom APIs, Vertex/Bedrock/GitLab/auth paths, and retries auth/usage failures before replay-unsafe output.
- inputs_outputs_state: Inputs are `Model`, `Context`, streaming options, auth storage, env keys; outputs are assistant event streams and final messages.
- gates_or_invariants: Missing keys throw, aborts stop retry, retry flushes only before unsafe events, mandatory reasoning floors apply, and static/dynamic key precedence is provider-specific.
- dependencies_and_callers: Called by agent runtime, search providers, tests, and eval/subagent flows; depends on provider modules, auth storage, catalog descriptors, and thinking-loop utilities.
- edge_cases_or_failure_modes: Provider-specific quota/usage-limit errors, stale OAuth, malformed events, suppressed reasoning, and unsupported APIs.
- validation_or_tests: Covered by `thinking-loop.test.ts`, auth tests, login tests, 429/retry tests, and provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-456 `file` `packages/ai/test/auth-broker-refresher.test.ts`
- cursor: `[_]`
- core_role: Validates OAuth credential refresh/disable algorithm.
- algorithmic_behavior: Creates sqlite auth stores, seeds expiring credentials, spies `refreshOAuthToken`, and verifies refresh, non-refresh, definitive disable, and transient failure retention.
- inputs_outputs_state: Inputs are credential expiry times, refresh skew, mocked OAuth results/errors; outputs are persisted fresh credentials or disabled snapshots/events.
- gates_or_invariants: Refresh only inside skew; `invalid_grant` disables; network/timeout keeps credential active.
- dependencies_and_callers: Tests `AuthBrokerRefresher`, `AuthStorage`, `SqliteAuthCredentialStore`, and OAuth utility.
- edge_cases_or_failure_modes: Env key leakage is cleaned; temp DB lifecycle is closed/removed.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-486 `file` `packages/ai/test/auth-storage-usage-history.test.ts`
- cursor: `[_]`
- core_role: Validates usage-history persistence and hourly downsampling.
- algorithmic_behavior: Records usage snapshots into sqlite, verifies one row per hour/series with latest value winning, filters by provider/since, and checks `AuthStorage.fetchUsageReports()` attribution.
- inputs_outputs_state: Inputs are synthetic `UsageHistoryEntry` and mocked usage reports; outputs are history rows ordered oldest-first.
- gates_or_invariants: Series key is provider/account/window, cache cleanup must not prune usage history, and fresh usage appends one row per limit.
- dependencies_and_callers: Tests `SqliteAuthCredentialStore`, `AuthStorage`, and usage provider resolver.
- edge_cases_or_failure_modes: Same-hour overwrite, independent limits/accounts, ancient rows, and host env API keys avoided by resolver restriction.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-516 `file` `packages/ai/test/google-gemini-cli-429.test.ts`
- cursor: `[_]`
- core_role: Validates Gemini CLI 429 fail-fast and retry-delay parsing.
- algorithmic_behavior: Checks quota/exhausted regex classification and parses retry hints from headers and body patterns including seconds, milliseconds, minutes, hours, compound durations, and Codex-friendly text.
- inputs_outputs_state: Inputs are `Headers` and error body strings; outputs are millisecond retry hints or fail-fast booleans.
- gates_or_invariants: `retry-after` wins over reset-after; ambiguous rate-limit text does not fail fast; empty text yields no delay.
- dependencies_and_callers: Tests retry/quota helpers used by provider/gateway scheduling.
- edge_cases_or_failure_modes: Case-insensitive quota text, generic 429s, and body strings without recognized delays.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-546 `file` `packages/ai/test/issue-883-repro.test.ts`
- cursor: `[_]`
- core_role: Regression for DeepSeek V4 `reasoning_content` replay with tool calls.
- algorithmic_behavior: Builds OpenAI-compatible DeepSeek models, converts assistant tool-call turns, and asserts `requiresReasoningContentForToolCalls` plus empty-string placeholders/content normalization.
- inputs_outputs_state: Inputs are assistant messages with text/tool-only tool calls; outputs are OpenAI wire messages.
- gates_or_invariants: DeepSeek V4 requires `reasoning_content`; no-thinking placeholders are `""`, not `"."`; content must be `""`, not null, for pure tool-use.
- dependencies_and_callers: Tests `convertMessages`, catalog/build compat, and provider message conversion.
- edge_cases_or_failure_modes: DeepSeek served by non-DeepSeek hosts such as Deepinfra and pure tool-call turns.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-576 `file` `packages/ai/test/openai-codex-reset.test.ts`
- cursor: `[_]`
- core_role: Wire-contract regression for OpenAI Codex saved rate-limit reset credits.
- algorithmic_behavior: Records mocked fetch calls for list/consume endpoints and validates URL, method, headers, body, fallback counting, business outcome mapping, and HTTP failure code synthesis.
- inputs_outputs_state: Inputs are access token/account ID/credit ID/mock responses; outputs are credit list or consume result.
- gates_or_invariants: GET `/wham/rate-limit-reset-credits`, POST `/consume` with `credit_id` and `redeem_request_id`, Authorization and account headers.
- dependencies_and_callers: Tests `usage/openai-codex-reset` helpers used by auth/usage recovery.
- edge_cases_or_failure_modes: Missing `available_count`, non-2xx list, already redeemed credits, generated request IDs, and 500 failures.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-606 `file` `packages/ai/test/openrouter-login.test.ts`
- cursor: `[_]`
- core_role: Validates OpenRouter API-key login and environment resolution.
- algorithmic_behavior: Confirms provider registration, `OPENROUTER_API_KEY` lookup, `/api/v1/auth/key` validation, credential persistence, and rejection on failed validation.
- inputs_outputs_state: Inputs are mocked prompts/fetch responses/env; outputs are stored `api_key` credentials or thrown validation errors.
- gates_or_invariants: Validation must hit `/auth/key` with Bearer header; invalid keys are not stored.
- dependencies_and_callers: Tests `AuthStorage.login`, OAuth provider registry, and `getEnvApiKey`.
- edge_cases_or_failure_modes: Restores env after each test and handles 401 text responses.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-636 `file` `packages/ai/test/thinking-loop.test.ts`
- cursor: `[_]`
- core_role: Regression suite for Gemini thinking-loop detection and stream guard.
- algorithmic_behavior: Feeds near-duplicate/verbatim/distinct thinking chunks into `ThinkingLoopDetector`, validates model gating, wraps mock streams, and checks retryable empty-content errors before visible output.
- inputs_outputs_state: Inputs are synthetic streamed thinking/text events and mock models; outputs are detector details or final assistant messages/errors.
- gates_or_invariants: Only Gemini/compat-flagged models guarded; no observable content before loop error; once visible text appears the latch prevents retry hijack.
- dependencies_and_callers: Tests `stream`, `streamSimple`, custom mock provider, `withGeminiThinkingLoopGuard`, and retry classifier.
- edge_cases_or_failure_modes: Unterminated duplicate paragraph, numeric repetitive output, short intentional repeats, Vertex transport, and custom API path.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-666 `file` `packages/catalog/src/models.ts`
- cursor: `[_]`
- core_role: Lazy bundled model registry and cost helper.
- algorithmic_behavior: Lazily builds nested provider/model maps from generated `models.json`, exposes bundled provider/model lookups, computes usage costs, and compares model identity (`packages/catalog/src/models.ts:13-64`).
- inputs_outputs_state: Inputs are generated model specs and `Usage`; outputs are enriched `Model` instances, provider lists, cost totals, and equality booleans.
- gates_or_invariants: Enrichment is lazy and cached; direct `models.json` edits are disallowed by repo rules; equality requires both id and provider.
- dependencies_and_callers: Used by AI/coding-agent tests and model registry; depends on `buildModel` and generated JSON.
- edge_cases_or_failure_modes: Unknown provider/model returns undefined at runtime despite typed access; stale generated JSON affects registry.
- validation_or_tests: Catalog and provider tests exercise bundled lookup and model behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-696 `file` `packages/catalog/test/lm-studio-provider.test.ts`
- cursor: `[_]`
- core_role: Validates LM Studio dynamic local model discovery.
- algorithmic_behavior: Mocks native `/api/v0/models` and OpenAI-compatible `/v1/models`, verifies VLM input classification/context length, and fallback when native metadata hangs.
- inputs_outputs_state: Inputs are mocked fetch responses/abort signals; outputs are dynamic model specs with input capabilities.
- gates_or_invariants: Native metadata can enrich models; OpenAI-compatible discovery must start and native request must abort on timeout/fallback.
- dependencies_and_callers: Tests `lmStudioModelManagerOptions` in OpenAI-compatible provider resolver.
- edge_cases_or_failure_modes: Hanging native endpoint, localhost alternate port, plain LLM vs VLM.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-726 `file` `packages/coding-agent/src/cli.ts`
- cursor: `[_]`
- core_role: Main coding-agent CLI entrypoint and worker-host dispatcher.
- algorithmic_behavior: Sanitizes macOS env, checks Bun version, parses profile/smoke/hidden worker args, declares worker host after early dispatch, dynamically loads command registry, and redirects unknown commands to launch flow.
- inputs_outputs_state: Inputs are argv/env/Bun.main/IPC; outputs are command execution, worker subprocess behavior, smoke-test result, or CLI errors.
- gates_or_invariants: Hidden workers dispatch before command loading; worker host declaration only in real CLI main; smoke test probes stats/tiny workers; native transformer workers die on parent disconnect.
- dependencies_and_callers: Spawned by CLI, workers, tests, and compiled binary; depends on `@oh-my-pi/pi-utils/env`, command registry, worker modules.
- edge_cases_or_failure_modes: Old Bun version, compiled binary worker entrypoint drift, missing parent IPC, smoke failure, and unknown command routing.
- validation_or_tests: Worker-host smoke contract is described in AGENTS; CLI smoke and install tests validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-756 `file` `packages/coding-agent/test/agent-session-branching.test.ts`
- cursor: `[_]`
- core_role: End-to-end-like regression for session branching behavior.
- algorithmic_behavior: Creates real `AgentSession`s, prompts, gathers branchable user messages, branches from first/middle messages, and checks retained/truncated messages and session-file behavior.
- inputs_outputs_state: Inputs are user prompts and optional no-session mode; outputs are branch result, session messages, and new session files.
- gates_or_invariants: Branching from first message empties conversation; in-memory mode creates no file; middle branch keeps prior turns.
- dependencies_and_callers: Tests `AgentSession`, `SessionManager`, tool creation, bundled model, and auth setup.
- edge_cases_or_failure_modes: Skipped without `ANTHROPIC_API_KEY`; temp dirs cleaned.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-786 `file` `packages/coding-agent/test/agent-session-todo-reminder-loop.test.ts`
- cursor: `[_]`
- core_role: Regression for todo reminder self-continuation suppression.
- algorithmic_behavior: Emits synthetic agent stops/tool results into `AgentSession`, spies `agent.continue`, and asserts reminders do not escalate through text-only acknowledgements but do after tool-level progress.
- inputs_outputs_state: Inputs are pending todo phases and emitted agent events; outputs are `todo_reminder` events and developer reminder transcript entries.
- gates_or_invariants: One reminder per user pause unless a tool result occurs between reminders; max reminder count respected.
- dependencies_and_callers: Tests `AgentSession` todo reminder loop and event handling.
- edge_cases_or_failure_modes: Text-only stop loops, tool `todo` progress, async continuation chains, and transcript persistence.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-816 `file` `packages/coding-agent/test/checkpoint-rpc-qa.ts`
- cursor: `[_]`
- core_role: Manual/QA script for checkpoint and rewind behavior in RPC mode.
- algorithmic_behavior: Starts an RPC client against `src/cli.ts`, selects available model by env keys, prompts a checkpoint/find/read/rewind workflow with retries, captures streamed events and session entries, and verifies tool sequence/session effects.
- inputs_outputs_state: Inputs are env API keys, RPC commands, session files; outputs are QA assertions, streamed event sequence, and parsed session entries.
- gates_or_invariants: Requires a provider API key; workflow must call checkpoint then rewind and final `DONE`.
- dependencies_and_callers: Depends on `RpcClient`, `parseSessionEntries`, CLI RPC mode, and checkpoint/rewind tools.
- edge_cases_or_failure_modes: Model noncompliance triggers retry prompts; missing keys/no models prevents meaningful run.
- validation_or_tests: Script itself is validation/QA evidence, not normal unit test.
- skip_candidate: `yes: QA harness script rather than production runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-846 `file` `packages/coding-agent/test/edit-per-file-diff-content.test.ts`
- cursor: `[_]`
- core_role: Regression suite for edit tool old/new full-file diff details.
- algorithmic_behavior: Executes create/update/delete/replace edit paths and asserts `EditToolDetails.oldText/newText` represent full file before/after across aggregated operations.
- inputs_outputs_state: Inputs are temp files and edit operations; outputs are edit details and resulting file text.
- gates_or_invariants: Create-shaped details keep `oldText` key undefined; delete-shaped details keep `newText` key undefined; replace reports full before/after content.
- dependencies_and_callers: Tests `EditTool`, `executeReplaceSingle`, patch aggregation, and diagnostics hooks.
- edge_cases_or_failure_modes: Create followed by update, update followed by delete, deleted files, and replace single mode.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-876 `file` `packages/coding-agent/test/history-storage-sqlite-compat.test.ts`
- cursor: `[_]`
- core_role: Regression for legacy history sqlite schema migration.
- algorithmic_behavior: Builds a legacy `history` table using `unixepoch()` default, opens `HistoryStorage`, adds a new prompt, and verifies rows/index/FTS plus schema default replacement.
- inputs_outputs_state: Inputs are temp sqlite DB and prompts; outputs are migrated schema and preserved history rows.
- gates_or_invariants: Existing rows preserved; default changes to `strftime('%s','now')`; `idx_history_created_at` and `history_fts` exist.
- dependencies_and_callers: Tests `HistoryStorage` and sqlite inspection helper.
- edge_cases_or_failure_modes: Legacy schema drift and FTS/index absence.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-906 `file` `packages/coding-agent/test/interactive-mode-todo-clear.test.ts`
- cursor: `[_]`
- core_role: Validates TUI todo auto-clear display policy.
- algorithmic_behavior: Creates `InteractiveMode`, renders todo container, sets todo phases, and uses fake timers to assert instant/delayed/disabled clearing of closed todos.
- inputs_outputs_state: Inputs are todo phases and `tasks.todoClearDelay`; outputs are rendered panel lines while session todo state remains unchanged.
- gates_or_invariants: Auto-clear affects display only, not session history; `0` clears immediately, `-1` disables, positive values delay.
- dependencies_and_callers: Tests `InteractiveMode`, `AgentSession`, settings, theme, and todo renderer.
- edge_cases_or_failure_modes: Fake timer cleanup, completed/abandoned statuses, and mutation safety.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-936 `file` `packages/coding-agent/test/issue-983-multi-file-extension.test.ts`
- cursor: `[_]`
- core_role: Regression for legacy multi-file Pi extension loading.
- algorithmic_behavior: Creates a temporary extension with `package.json`, `index.ts`, and `helper.ts`, then verifies relative sibling imports work and tool registration succeeds.
- inputs_outputs_state: Inputs are temp extension files and project dir; outputs are loaded extension result with registered tool.
- gates_or_invariants: Loader must honor `pi.extensions` entry and Bun/TS relative import graph.
- dependencies_and_callers: Tests `discoverAndLoadExtensions`.
- edge_cases_or_failure_modes: Multi-file TypeScript extension resolution and loader errors.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-966 `file` `packages/coding-agent/test/mcp-render-status.test.ts`
- cursor: `[_]`
- core_role: Regression suite for MCP tool rendering status and truncation notices.
- algorithmic_behavior: Builds fake MCP tools/connections, renders `ToolExecutionComponent`, and asserts completed/error headers replace pending headers; renders spill metadata as artifact link once.
- inputs_outputs_state: Inputs are MCP args/results/meta; outputs are stripped rendered TUI text.
- gates_or_invariants: MCP tools set `mergeCallAndResult`; body spill notice is stripped and surfaced as styled artifact warning.
- dependencies_and_callers: Tests `MCPTool`, `DeferredMCPTool`, `renderMCPResult`, theme, and TUI component.
- edge_cases_or_failure_modes: MCP error result, pending header remnants, truncation notices, and artifact link duplication.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-996 `file` `packages/coding-agent/test/plan-mode-thinking-level.test.ts`
- cursor: `[_]`
- core_role: Regression for thinking suffix propagation in model roles.
- algorithmic_behavior: Creates sessions with `modelRoles`, calls `resolveRoleModelWithThinking`, and asserts model/thinking/explicit flags for plan/default roles while preserving old `resolveRoleModel`.
- inputs_outputs_state: Inputs are role strings such as `anthropic/claude-sonnet-4-5:xhigh`; outputs are resolved model and thinking metadata.
- gates_or_invariants: Thinking suffix must not be dropped; no suffix means `explicitThinkingLevel=false`; absent role returns no model.
- dependencies_and_callers: Tests `AgentSession`, settings, model registry, and plan-mode model application path.
- edge_cases_or_failure_modes: Different thinking levels, default role, backward compatibility.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1026 `file` `packages/coding-agent/test/rpc-skill-command.test.ts`
- cursor: `[_]`
- core_role: Validates RPC `/skill:<name>` command dispatch.
- algorithmic_behavior: Creates a temp `SKILL.md`, calls `tryRunRpcSkillCommand`, and asserts skill prompt custom message content/user suffix/attribution/display; unknown skill returns false.
- inputs_outputs_state: Inputs are active skills settings and prompt text; outputs are custom skill prompt message or false.
- gates_or_invariants: Skill commands require enabled setting and known skill; unknown commands must fall through to normal prompt handling.
- dependencies_and_callers: Tests RPC mode skill command handling and skill prompt message type.
- edge_cases_or_failure_modes: Missing skill, user-supplied suffix, temp skill cleanup.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1056 `file` `packages/coding-agent/test/session-storage.test.ts`
- cursor: `[_]`
- core_role: Regression for deleting sessions plus artifact directories.
- algorithmic_behavior: Creates session JSONL files/artifact dirs, calls `deleteSessionWithArtifacts`, and asserts success when artifact dir absent and clear error when artifact cleanup fails after file deletion.
- inputs_outputs_state: Inputs are filesystem session/artifact paths; outputs are deleted files or thrown error.
- gates_or_invariants: Missing artifact dir is OK; if artifact removal fails, error states session file was deleted but artifacts remain.
- dependencies_and_callers: Tests `FileSessionStorage`.
- edge_cases_or_failure_modes: Permission-like `rm` failure and partial cleanup.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1086 `file` `packages/coding-agent/test/streaming-render-debug.ts`
- cursor: `[_]`
- core_role: Manual repro/debug script for streaming assistant message rendering.
- algorithmic_behavior: Loads a fixture assistant message, streams thinking content into `AssistantMessageComponent` chunk-by-chunk, then appends final text using a live `TUI`.
- inputs_outputs_state: Inputs are fixture JSON and token-sized chunks; outputs are live terminal render updates.
- gates_or_invariants: Expects fixture with thinking content; exits if missing.
- dependencies_and_callers: Depends on TUI process terminal, assistant renderer, theme, and Bun sleep.
- edge_cases_or_failure_modes: Missing fixture/thinking block, live terminal side effects, and manual visual validation.
- validation_or_tests: Not automated; script exists to reproduce rendering bugs.
- skip_candidate: `yes: debug reproduction script, not core runtime path`

### OH_MY_HUMANIZE_MAIN-HZ-1116 `file` `packages/coding-agent/test/unexpected-stop-classifier.test.ts`
- cursor: `[_]`
- core_role: Regression for unexpected text-only stop candidate/classifier parsing.
- algorithmic_behavior: Builds synthetic assistant messages and asserts candidate selection plus YES/NO/unparseable output parsing.
- inputs_outputs_state: Inputs are assistant `stopReason` and content blocks, plus classifier text; outputs are boolean/undefined parse results.
- gates_or_invariants: Only non-empty text-only `stop` messages are candidates; tool calls, length/aborted, whitespace, and empty content are not.
- dependencies_and_callers: Tests `session/unexpected-stop-classifier`.
- edge_cases_or_failure_modes: Ambiguous classifier responses and mixed tool/text messages.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1146 `file` `packages/hashline/src/format.ts`
- cursor: `[_]`
- core_role: Canonical hashline format constants and display helpers.
- algorithmic_behavior: Defines sigils/keywords/regex fragments, computes 4-hex normalized file hashes, formats hunk headers, anchors, hashline file headers, and numbered lines (`packages/hashline/src/format.ts:9-137`).
- inputs_outputs_state: Inputs are file text, line numbers, cursors, file paths; outputs are hashline headers/lines and hash tags.
- gates_or_invariants: Hash normalizes trailing spaces/tabs/CR before newline/end; line IDs are positive integers; hash tags are uppercase 4-hex.
- dependencies_and_callers: Used by hashline parser/tokenizer/prompt/edit grammar and AST block edit features.
- edge_cases_or_failure_modes: CRLF/trailing whitespace normalization, file hash collision risk due 16-bit tag, cursor variants, and block keyword consistency.
- validation_or_tests: Hashline parser/editor tests validate downstream behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1176 `file` `packages/mnemopi/src/mcp-server.ts`
- cursor: `[_]`
- core_role: TypeScript stdio MCP JSON-RPC server for mnemopi tools.
- algorithmic_behavior: Handles JSONL stdin, `initialize`, `tools/list`, `tools/call`, notifications, parse errors, unknown methods, and wraps tool call results/errors as MCP text content (`packages/mnemopi/src/mcp-server.ts:51-155`).
- inputs_outputs_state: Inputs are JSON-RPC requests and tool args; outputs are JSON-RPC responses on stdout with MCP tool payloads.
- gates_or_invariants: Notifications/no-id return null; `tools/call` requires `params.name`; only stdio transport implemented.
- dependencies_and_callers: Depends on `mcp-tools`; launched by mnemopi MCP integrations.
- edge_cases_or_failure_modes: Malformed JSON, missing tool name, tool exception, unsupported transport, and partial input buffers.
- validation_or_tests: MCP behavior validated by mnemopi tests and integration use.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1206 `file` `packages/mnemopi/test/extraction-wiring.test.ts`
- cursor: `[_]`
- core_role: Validates LLM fact extraction wiring from `remember(extract)`.
- algorithmic_behavior: Creates in-memory `Mnemopi` with mocked completion or no LLM, calls `remember`, drains async extractions, and asserts facts are recallable or skipped.
- inputs_outputs_state: Inputs are memory text and `extract` flag; outputs are stored memory IDs and fact recall rows.
- gates_or_invariants: Extraction fires only when requested; no configured LLM must not break memory storage; `flushExtractions()` drains fire-and-forget work.
- dependencies_and_callers: Tests `Mnemopi`, beam fact recall, and runtime LLM completion hook.
- edge_cases_or_failure_modes: Missing LLM, unrequested extraction, async extraction timing.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1236 `file` `packages/mnemopi/test/streaming.test.ts`
- cursor: `[_]`
- core_role: Validates mnemopi event streaming and delta sync.
- algorithmic_behavior: Tests `MemoryEvent` serialization, `MemoryStream` typed/any listeners with exception isolation and bounded filtering, async listeners, and `DeltaSync` compute/apply/checkpoint persistence.
- inputs_outputs_state: Inputs are memory events, sqlite rows, peer IDs, temp checkpoint dir; outputs are serialized events, listener calls, deltas, checkpoints, and inserted rows.
- gates_or_invariants: Listener exceptions isolated; stream buffer bounded; type/since filters work; delta sync operates on allowed tables and persists checkpoints.
- dependencies_and_callers: Tests `core/streaming`, `initBeam`, and sqlite.
- edge_cases_or_failure_modes: Buffer eviction, callback exceptions, async iterator return, and reload of checkpoints.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1266 `file` `packages/snapcompact/research/diag_glm_forensics.py`
- cursor: `[_]`
- core_role: Offline forensic cache inspector for GLM mono-prod QA responses.
- algorithmic_behavior: Rebuilds exact cached request payloads for a shape/questions/seed, hashes payload keys, reads `.cache/qa/*.json`, and prints questions/golds/usage/raw text without API calls.
- inputs_outputs_state: Inputs are cached SQuAD paragraphs, frame PNGs, shape/model/chars/questions/qpb/seed; outputs are stdout forensic batches.
- gates_or_invariants: Requires existing frame/cache files; no network/API calls; shape must exist in `SHAPES`.
- dependencies_and_callers: Depends on sibling research modules `squad`, `mono_prod`, and `run` cache helpers.
- edge_cases_or_failure_modes: Missing cache hit, frame dir absent, mismatched payload hash, unavailable shape.
- validation_or_tests: Research utility; no production test.
- skip_candidate: `yes: research forensic script, not production core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1296 `file` `packages/snapcompact/research/mono.py`
- cursor: `[_]`
- core_role: Research runner for monolithic long-context text/image retrieval experiments.
- algorithmic_behavior: Builds a whole SQuAD flow, renders optional dense image carriers, sends batched QA prompts through cached LLM calls, computes EM/F1/abstention/position quartiles/cost, and writes JSONL/summary.
- inputs_outputs_state: Inputs are model/env keys, conditions, chars, questions, image size, cache; outputs are result records and summary JSON.
- gates_or_invariants: Conditions must parse as text/image; cached calls avoid duplicate API work; image files are written atomically via temp then replace.
- dependencies_and_callers: Depends on research modules `squad`, `bdf`, `final`, `providers`, and `run`.
- edge_cases_or_failure_modes: Missing env keys, unsupported condition, API max-token stops, image cache misses, and malformed numbered answers.
- validation_or_tests: Research harness; validated by produced metrics rather than tests.
- skip_candidate: `yes: experimental research runner, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1326 `file` `packages/snapcompact/research/snapcompact_text_image_3d_viz.py`
- cursor: `[_]`
- core_role: Research visualization generator for text-vs-image hidden-state comparison.
- algorithmic_behavior: Loads summary/NPZ activation arrays, downsamples/normalizes cosine fields, renders a 3D surface with answer-region rails, composites explanatory panels and cropped answer bitmap, then writes PNG.
- inputs_outputs_state: Inputs are `summary.json`, `text_image_compare.npz`, and carrier image; output is `text-vs-image-3d.png`.
- gates_or_invariants: Uses quantile normalization; marks answer bins within bounds; creates output parent directories.
- dependencies_and_callers: Depends on matplotlib/numpy/Pillow and generated snapcompact research artifacts.
- edge_cases_or_failure_modes: Missing arrays/images, degenerate quantiles, font fallback, and invalid answer indices.
- validation_or_tests: Research visualization; no automated tests.
- skip_candidate: `yes: visualization artifact, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1356 `file` `packages/stats/test/client-view-models.test.ts`
- cursor: `[_]`
- core_role: Regression for stats dashboard model performance series.
- algorithmic_behavior: Builds sparse all-time model performance points and asserts `buildModelPerformanceLookup` preserves old sparse buckets and converts TTFT milliseconds to seconds.
- inputs_outputs_state: Inputs are `ModelPerformancePoint[]` and range `"all"`; output is lookup series data.
- gates_or_invariants: All-time sparse points must not be dropped; ordering remains timestamp ascending.
- dependencies_and_callers: Tests stats client view-model transformation.
- edge_cases_or_failure_modes: Sparse timestamps far apart and per-model/provider keying.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1386 `file` `packages/tui/src/ttyid.ts`
- cursor: `[_]`
- core_role: Stable terminal identifier resolver.
- algorithmic_behavior: Resolves TTY path via `/proc/self/fd/0` on Linux or `ttyname(3)` via FFI on Unix, then falls back through multiplexer/emulator env vars.
- inputs_outputs_state: Inputs are stdin TTY status, platform, FFI/libc result, env vars; output is sanitized terminal ID or null.
- gates_or_invariants: Only `/dev/*` paths become TTY IDs; zellij session name separators normalized; multiplexer envs preferred over host emulator envs.
- dependencies_and_callers: Used by TUI/session breadcrumb/state code; depends on Bun FFI, `node:fs`, `node:os`.
- edge_cases_or_failure_modes: Windows returns env fallback/null, FFI failures return null, inherited nested env ordering, and piped stdin.
- validation_or_tests: Covered indirectly by terminal/capability behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1416 `file` `packages/tui/test/keybindings.test.ts`
- cursor: `[_]`
- core_role: Regression suite for keybinding alias/conflict behavior.
- algorithmic_behavior: Creates `KeybindingsManager` with overrides and asserts defaults are not evicted across action namespaces, shift-printable aliases are preserved, conflicts are reported, and default newline keys exist.
- inputs_outputs_state: Inputs are default/user key maps and key bytes; outputs are key lists, conflict arrays, and match booleans.
- gates_or_invariants: Reusing a key in one action must not evict unrelated defaults; direct user conflicts reported; `esc`/`return` aliases normalize.
- dependencies_and_callers: Tests `@oh-my-pi/pi-tui` keybinding parser/manager.
- edge_cases_or_failure_modes: Uppercase printable keys, `?` alias, Ctrl+J/Shift+Enter newline semantics.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1446 `file` `packages/tui/test/select-filter-breadcrumb.test.ts`
- cursor: `[_]`
- core_role: Regression for event-loop watchdog attribution during select-list filtering.
- algorithmic_behavior: Calls `SelectList.setFilter`, then checks the loop-phase stack is balanced and the recent breadcrumb records `ui.select-filter`.
- inputs_outputs_state: Inputs are select items and filter strings; outputs are loop-phase stack/recent slot state.
- gates_or_invariants: Non-empty fuzzy filters push/pop breadcrumb; empty whitespace filter does not.
- dependencies_and_callers: Tests `SelectList` and loop-phase helpers from `pi-utils`.
- edge_cases_or_failure_modes: Expensive synchronous fuzzy filtering otherwise logged as unknown stall.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1476 `file` `packages/typescript-edit-benchmark/src/shared.ts`
- cursor: `[_]`
- core_role: Recursive sorted file lister for edit benchmark fixtures.
- algorithmic_behavior: Reads directory entries recursively, accumulates file paths relative to root, ignores non-files, and returns sorted results.
- inputs_outputs_state: Inputs are root directory and optional subpath; output is sorted relative file path array.
- gates_or_invariants: Only `Dirent.isFile()` entries included; recursive calls preserve relative path.
- dependencies_and_callers: Used by TypeScript edit benchmark runner/scripts.
- edge_cases_or_failure_modes: Symlinks/non-files ignored; directory read errors propagate.
- validation_or_tests: Benchmark tests/usage validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1506 `file` `packages/utils/src/runtime-install.ts`
- cursor: `[_]`
- core_role: On-demand runtime dependency installer and compiled-binary module resolver patch.
- algorithmic_behavior: Resolves bare specifiers against runtime `node_modules` honoring exports/main/extensions, patches `Module._resolveFilename`, writes runtime manifests, acquires install lock dirs, and installs pinned dependencies.
- inputs_outputs_state: Inputs are runtime dir, dependency specs, stubs, parent module filename; outputs are package manifests, installed `node_modules`, patched resolution, and phase callbacks.
- gates_or_invariants: Stock resolution tried first except distrusted runtime-root hits; parent must be inside runtime root for fallback/stubs; lock acquisition bounds concurrent installs.
- dependencies_and_callers: Used by optional native-heavy runtimes such as transformers/fastembed; depends on `node:module`, filesystem APIs, Bun install/spawn behavior.
- edge_cases_or_failure_modes: Bun compiled resolver ignoring exports, nested `node_modules` version correctness, missing manifests, lock timeout, and install stderr.
- validation_or_tests: Utility tests cover resolver/spacing adjacent behavior; runtime consumers smoke optional installs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1536 `file` `packages/utils/test/spacing.test.ts`
- cursor: `[_]`
- core_role: Regression suite for indentation/editorconfig resolution.
- algorithmic_behavior: Creates temp project `.editorconfig` chains, sets project/default tab width, calls `getIndentation`, and asserts root-to-leaf merge/fallback/error handling.
- inputs_outputs_state: Inputs are file paths and editorconfig files; output is indentation width.
- gates_or_invariants: Nested configs merge root-to-leaf; overlong path components short-circuit to default without syscall; ENOTDIR/errors are tolerated.
- dependencies_and_callers: Tests `tab-spacing` utilities used by renderers and edit formatting.
- edge_cases_or_failure_modes: `ENAMETOOLONG`, normalized `..` paths, non-directory path segments, and default tab width restoration.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1566 `file` `python/robomp/src/proxy_hmac.py`
- cursor: `[_]`
- core_role: HMAC request signing/verification for robomp-to-GitHub-proxy communication.
- algorithmic_behavior: Canonicalizes `(method,path,timestamp,sha256(body))`, signs with HMAC-SHA256, and verifies timestamp/signature with constant-time compare (`python/robomp/src/proxy_hmac.py:23-88`).
- inputs_outputs_state: Inputs are method/path/body/key/timestamp/signature; outputs are `(timestamp, signature)` or `VerifyResult(ok, reason)`.
- gates_or_invariants: ±30s default skew, integer timestamp, required headers, body hash included, path must be path-only canonical form.
- dependencies_and_callers: Used by robomp service/proxy clients; depends on Python `hmac`, `hashlib`, `time`.
- edge_cases_or_failure_modes: Missing headers, malformed timestamp, replay outside skew, signature mismatch, and query/path canonical mismatch.
- validation_or_tests: Covered by robomp tests and integration smoke.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1596 `file` `python/robomp/tests/test_worker_smoke.py`
- cursor: `[_]`
- core_role: Gated end-to-end smoke test for robomp issue triage worker.
- algorithmic_behavior: Seeds a failing bare repo, mocks GitHub API with `httpx.MockTransport`, runs `triage_issue` with sandbox/git transport, then checks comment, PR body, pushed branch, and sqlite issue row.
- inputs_outputs_state: Inputs are env settings, fake webhook payload, bare repo, mocked GitHub requests; outputs are PR/comment captures, refs, and DB state.
- gates_or_invariants: Skips unless `ROBOMP_INTEGRATION=1`; repo allowlist and proxy/HMAC env set; PR body must include Repro/Cause/Fix/Verification and `Fixes #1`.
- dependencies_and_callers: Tests robomp config/db/github/sandbox/tasks and `omp` worker command availability.
- edge_cases_or_failure_modes: Missing integration env, unmocked GitHub path, failed branch push, no PR/comment.
- validation_or_tests: This file is direct smoke validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1626 `directory` `packages/coding-agent/src/extensibility/plugins`
- cursor: `[_]`
- core_role: Plugin installation, discovery, manifest parsing, config, and runtime loading subsystem.
- algorithmic_behavior: Discovers enabled plugin packages, parses specs/features, installs/uninstalls/links via Bun package snapshots, validates extension factories, loads tools/hooks/commands/extensions, and manages doctor/config/feature state.
- inputs_outputs_state: Inputs are plugin specs, lockfiles, settings disables/features, package manifests, node_modules; outputs are loaded extensions, config files, install snapshots, validation errors, and doctor reports.
- gates_or_invariants: Rollback on failed validation, disabled plugins/features filtered, package name/spec validation, one-level extension scan fallback, and no duplicate redundant exports.
- dependencies_and_callers: Used by coding-agent startup/discovery and plugin commands; depends on Bun install, extension loader, marketplace registry/cache.
- edge_cases_or_failure_modes: Git dependency package-name mismatch, invalid extension export, stale lockfile, disabled plugin, missing external tool/env key, and rollback cleanup.
- validation_or_tests: Plugin/extension tests include disabled extensions and multi-file extension loading.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1656 `directory` `packages/mnemopi/src/core/migrations`
- cursor: `[_]`
- core_role: Database migration helpers for mnemopi core storage.
- algorithmic_behavior: Exports migration modules; `e6-triplestore-split` detects pending annotation migration, optionally backs up DB, opens transaction, creates annotations/indexes, inserts migrated rows, and commits/rolls back.
- inputs_outputs_state: Inputs are sqlite DB path/options/dryRun; outputs are migrated annotations, counts/logs, backup file, or rollback error.
- gates_or_invariants: DB path required, backup unless dry run/no backup, `BEGIN IMMEDIATE`, `INSERT OR IGNORE`, and pending detection via missing annotations.
- dependencies_and_callers: Used by mnemopi migration command/startup paths; depends on bun sqlite and filesystem.
- edge_cases_or_failure_modes: Missing DB path, duplicate annotations, transaction failure, standalone DB shape, and dry-run rollback.
- validation_or_tests: Migration behavior covered indirectly by mnemopi DB tests; index export is tiny.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1686 `file` `packages/agent/test/utils/get-current-time.ts`
- cursor: `[_]`
- core_role: Test utility tool for time retrieval and tool-call contracts.
- algorithmic_behavior: Formats current date/time in optional timezone, returns UTC timestamp details, throws on invalid timezone, and exposes an `AgentTool` schema.
- inputs_outputs_state: Inputs are optional timezone string; outputs are text content and `{utcTimestamp}`.
- gates_or_invariants: Invalid timezone errors include current UTC ISO; arktype schema marks timezone optional.
- dependencies_and_callers: Used by agent tests as a simple deterministic-shape tool.
- edge_cases_or_failure_modes: Locale/timezone support and invalid IANA names.
- validation_or_tests: Used by agent core test suites.
- skip_candidate: `yes: test helper tool, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1716 `file` `packages/ai/src/dialect/pi.ts`
- cursor: `[_]`
- core_role: Pi in-band dialect scanner/renderer for thinking and tool calls.
- algorithmic_behavior: Streaming state machine parses `<thinking>` and `<call:tool>` tags, buffers partial suffixes, emits text/thinking/tool start/arg delta/end events, coerces XML-ish members by tool schema, and renders dialect tags.
- inputs_outputs_state: Inputs are streamed text and tool schemas; outputs are assistant text/thinking/tool events or rendered prompt/tool-call syntax.
- gates_or_invariants: Handles partial tags across chunks, arrays/repeated keys, inline target string args, minted tool IDs, and flush of incomplete calls.
- dependencies_and_callers: Used by AI providers/dialects and agent tool-call decoding.
- edge_cases_or_failure_modes: Malformed tags, nested members, partial suffixes, ambiguous inline args, and unfinished calls at stream end.
- validation_or_tests: Dialect/provider tests exercise parsing/rendering behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1746 `file` `packages/ai/src/providers/openai-anthropic-shim.ts`
- cursor: `[_]`
- core_role: Shared streaming shim for providers exposing both OpenAI and Anthropic-compatible APIs.
- algorithmic_behavior: Selects Anthropic-style or OpenAI completions path, builds model/options, maps thinking budget/tool choice, merges headers, streams provider output, and converts caught errors to stream events.
- inputs_outputs_state: Inputs are model/context/options/provider headers; outputs are assistant event stream.
- gates_or_invariants: Provider headers merged before user headers; Anthropic mode only when selected; caught errors surfaced as provider error messages.
- dependencies_and_callers: Used by Kimi/Synthetic shims and related provider integrations.
- edge_cases_or_failure_modes: Header override order, unsupported thinking/tool choice, provider throw during stream setup.
- validation_or_tests: Covered by provider stream tests and shim consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1776 `file` `packages/ai/src/registry/firepass.ts`
- cursor: `[_]`
- core_role: Fire Pass API-key login provider.
- algorithmic_behavior: Prompts/stores an API key and validates it with a chat-completions request against the Fireworks router model rather than `/v1/models`.
- inputs_outputs_state: Inputs are pasted key/fetch; outputs are stored credential or validation error.
- gates_or_invariants: Validation endpoint chosen because `/v1/models` is unauthorized for `fpk` keys.
- dependencies_and_callers: Used by auth registry/login flow.
- edge_cases_or_failure_modes: Invalid key, non-2xx validation response, network failure.
- validation_or_tests: Covered indirectly by auth/login provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1806 `file` `packages/ai/src/registry/openrouter.ts`
- cursor: `[_]`
- core_role: OpenRouter API-key login provider.
- algorithmic_behavior: Validates pasted key against `/api/v1/auth/key` and stores it as API-key credential.
- inputs_outputs_state: Inputs are key/fetch; outputs are credential or validation error.
- gates_or_invariants: Must not use public `/models`; Authorization Bearer header required.
- dependencies_and_callers: Used by auth storage login and OpenRouter provider lookup.
- edge_cases_or_failure_modes: 401 validation failure, network failure, env-key override.
- validation_or_tests: `packages/ai/test/openrouter-login.test.ts` directly validates.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1836 `file` `packages/ai/src/usage/minimax-code.ts`
- cursor: `[_]`
- core_role: Placeholder usage provider for Minimax Code credentials.
- algorithmic_behavior: Detects supported provider IDs and returns `null` usage reports because no quota API exists.
- inputs_outputs_state: Inputs are auth credentials/provider id; output is null usage.
- gates_or_invariants: Only `minimax-code`/CN variants eligible; no fabricated usage.
- dependencies_and_callers: Used by `AuthStorage.fetchUsageReports` resolver.
- edge_cases_or_failure_modes: Provider without quota API should not error or mislead.
- validation_or_tests: Usage history tests cover resolver behavior generically.
- skip_candidate: `yes: intentionally no-op provider adapter`

### OH_MY_HUMANIZE_MAIN-HZ-1866 `file` `packages/ai/test/helpers/index.ts`
- cursor: `[_]`
- core_role: Shared AI test utilities for env isolation, abortable delay, Codex model construction, and auth-gateway E2E probing.
- algorithmic_behavior: Temporarily overrides `Bun.env`, waits with abort cleanup, builds `openai-codex-responses` models, caches gateway health/token status.
- inputs_outputs_state: Inputs are env overrides, delay/signal, model ID, gateway env/token file; outputs are restored env, delay completion/errors, model specs, or E2E status.
- gates_or_invariants: Env always restored in `finally`; abort reason is propagated; gateway requires `E2E` and token/healthz.
- dependencies_and_callers: Used by AI test suites.
- edge_cases_or_failure_modes: Missing token file, health timeout, aborted delay, and env leakage.
- validation_or_tests: Helper supports tests rather than being directly tested.
- skip_candidate: `yes: test helper, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1896 `file` `packages/catalog/src/wire/gemini-headers.ts`
- cursor: `[_]`
- core_role: Wire header/profile helpers for Gemini CLI and Antigravity-compatible requests.
- algorithmic_behavior: Builds Gemini CLI and Antigravity user agents, caches Antigravity UA after first call, exposes modelEnum/maxOutputTokens profiles for Antigravity wire IDs.
- inputs_outputs_state: Inputs are model ID, env version overrides, process platform/arch; outputs are header objects/user-agent strings and optional wire profile.
- gates_or_invariants: Platform/arch mapping to expected client formats; profile keyed by routed upstream wire id, not logical collapsed id.
- dependencies_and_callers: Used by provider discovery/usage without importing heavy Gemini provider dependencies.
- edge_cases_or_failure_modes: Missing profile for checkpoint-only IDs, env version drift, platform mapping quirks.
- validation_or_tests: Provider tests/usage validate headers indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1926 `file` `packages/coding-agent/src/capability/skill.ts`
- cursor: `[_]`
- core_role: Capability definition and type contract for skills.
- algorithmic_behavior: Defines skill frontmatter/content/source shape and `skillCapability` with key, extension ID, and validation for name/path.
- inputs_outputs_state: Inputs are discovered skill files/frontmatter; outputs are capability items and extension IDs `skill:<name>`.
- gates_or_invariants: Missing name/path invalid; `hide` and `disableModelInvocation` omit model listing but preserve explicit access.
- dependencies_and_callers: Used by discovery, internal URL router, `/skill` commands, and system prompt capability rendering.
- edge_cases_or_failure_modes: Frontmatter aliases, hidden explicit skills, invalid skill files.
- validation_or_tests: RPC skill command and internal URL autocomplete tests cover skill surfaces.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1956 `file` `packages/coding-agent/src/cli/setup-cli.ts`
- cursor: `[_]`
- core_role: CLI setup command for Python and speech dependencies.
- algorithmic_behavior: Parses component/flags, checks system or managed Python, probes speech recorder/STT/TTS components, supports JSON/check/install modes, interactive picker, progress display, and exits non-zero on failure.
- inputs_outputs_state: Inputs are CLI flags, TTY availability, env/path probes; outputs are install/check reports, JSON, progress lines, and process exit status.
- gates_or_invariants: Component must be recognized; check-only avoids install; interactive requires TTY; failures exit 1.
- dependencies_and_callers: Invoked by CLI setup workflows; depends on speech/Python setup helpers.
- edge_cases_or_failure_modes: Missing Python, non-TTY interactive request, install failure, and component-specific probes.
- validation_or_tests: Setup smoke/CLI tests cover entry behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1986 `file` `packages/coding-agent/src/commands/grievances.ts`
- cursor: `[_]`
- core_role: CLI command dispatcher for auto-QA grievance reports.
- algorithmic_behavior: Parses positional action `list|clean|push` plus flags and delegates to `listGrievances`, `cleanGrievances`, or `pushGrievances`.
- inputs_outputs_state: Inputs are CLI args/flags; outputs are grievance list/clean/push side effects via called helpers.
- gates_or_invariants: Action constrained to three options; `list` is default; clean supports id/tool/all/json.
- dependencies_and_callers: Registered in command registry; depends on `grievances-cli`.
- edge_cases_or_failure_modes: Invalid CLI options handled by parser; helper failures propagate.
- validation_or_tests: CLI command tests or manual usage validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2016 `file` `packages/coding-agent/src/config/config-file.ts`
- cursor: `[_]`
- core_role: Typed config loader/migrator/cache.
- algorithmic_behavior: Migrates JSON to YAML once per process, parses YAML/JSON/JSONC, validates with arktype plus optional auxiliary validation, caches results, supports mtime checks and formatted `ConfigError`s.
- inputs_outputs_state: Inputs are config file paths/content and schemas; outputs are typed config objects, defaults, cache entries, or stage-specific errors.
- gates_or_invariants: Supported extensions only; parse/schema/aux validation stages distinguish errors; cache invalidation/mtime gates reload.
- dependencies_and_callers: Used by settings/config loading across coding-agent.
- edge_cases_or_failure_modes: Invalid syntax, schema mismatch, stale cache, missing file defaults, and migration write failure.
- validation_or_tests: Config/settings tests validate indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2046 `file` `packages/coding-agent/src/discovery/agents.ts`
- cursor: `[_]`
- core_role: Discovery provider for Agent Skills standard files and project/user context.
- algorithmic_behavior: Walks user/project `.agent`/`.agents` and related dirs, discovers skills/rules/prompts/commands/context/system prompts, loads AGENTS/SYSTEM/rules files, and avoids duplicate home/project traversal.
- inputs_outputs_state: Inputs are cwd/repoRoot/home/settings; outputs are capability items with source metadata.
- gates_or_invariants: Project walk stops at repoRoot/home; home skipped to avoid duplicate user entries; source levels tracked.
- dependencies_and_callers: Used by startup/discovery capability loading and prompt assembly.
- edge_cases_or_failure_modes: Nested repos, duplicate home path, disabled extensions, missing files, and mixed `.md/.mdc` rules.
- validation_or_tests: Disabled extension and memory tests cover discovery filtering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2076 `file` `packages/coding-agent/src/eval/agent-bridge.ts`
- cursor: `[_]`
- core_role: Host-side bridge for eval `agent()` helper spawning subagents.
- algorithmic_behavior: Validates args, blocks plan mode/depth/spawn-disabled/disabled-agent/budget-exhausted cases, resolves agent/model/skills/context/artifacts, runs subprocess subagent with timeout pause, emits progress, records usage, and returns text/details.
- inputs_outputs_state: Inputs are eval args, `ToolSession`, abort signal; outputs are `EvalAgentResult`, progress status events, artifacts, or `ToolError`.
- gates_or_invariants: `EVAL_AGENT_MAX_DEPTH=3`, plan mode unavailable, parent spawn allowlist enforced, turn hard budget enforced, LSP disabled, runtime max disabled, parent eval session intentionally not shared.
- dependencies_and_callers: Used by JS/Python eval bridge; depends on task discovery/executor, model resolver, MCP manager, output manager, subagent prompt template.
- edge_cases_or_failure_modes: Unknown/disabled agent, no budget, subagent abort with empty stderr, artifact temp dir fallback, and deadlock prevention by not reusing parent kernel.
- validation_or_tests: Subagent executor tests and eval bridge behavior cover usage/failure paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2106 `file` `packages/coding-agent/src/goals/state.ts`
- cursor: `[_]`
- core_role: Goal-mode state and event type contract.
- algorithmic_behavior: Defines goal statuses, mode state, tool detail shape, runtime events, token usage, and budget/terminal emission enums.
- inputs_outputs_state: Inputs are goal mutations/usage; outputs are typed state/events for goal tooling.
- gates_or_invariants: Status union constrains active/paused/budget-limited/complete/dropped lifecycle.
- dependencies_and_callers: Used by goal tools/session state.
- edge_cases_or_failure_modes: Type drift in goal event consumers.
- validation_or_tests: Compile checks and goal tests validate.
- skip_candidate: `yes: type-only state contract`

### OH_MY_HUMANIZE_MAIN-HZ-2136 `file` `packages/coding-agent/src/lsp/client.ts`
- cursor: `[_]`
- core_role: JSON-RPC/LSP subprocess manager and file-sync client cache.
- algorithmic_behavior: Spawns/initializes LSP servers with locks, frames JSON-RPC messages, routes responses/notifications/server requests, syncs file opens/changes, waits project load, handles progress/diagnostics, and shuts down idle/global clients.
- inputs_outputs_state: Inputs are command/cwd/root/file content/requests/signals; outputs are LSP responses, diagnostics, progress state, and client cache entries.
- gates_or_invariants: Per command+cwd creation lock, init failure negative cache, per-file operation locks/versioning, caller-owned abort timeout with `$ /cancelRequest`, and published/pending shutdown tracking.
- dependencies_and_callers: Used by LSP tools/diagnostics/edit integrations; depends on process tree spawn, Bun.file reads, JSON-RPC helpers.
- edge_cases_or_failure_modes: Header junk resync, server exit during init, rust-analyzer load polling, request timeout/abort, applyEdit/configuration requests, and idle cleanup.
- validation_or_tests: LSP tests and tool tests validate behavior where available.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2166 `file` `packages/coding-agent/src/mcp/tool-bridge.ts`
- cursor: `[_]`
- core_role: Adapter from MCP tool definitions to coding-agent `CustomTool`s.
- algorithmic_behavior: Sanitizes tool names, normalizes schemas, renders MCP call/results, formats MCP content/resource/image blocks, executes `callTool`, and reconnects/retries once for stale/network errors.
- inputs_outputs_state: Inputs are MCP server connections/tool definitions/args; outputs are agent tool results with MCP details and rendered TUI lines.
- gates_or_invariants: Tool names use `mcp__server_tool`; write approval tier; abort errors rethrown; stale/network errors retry once.
- dependencies_and_callers: Used by MCP manager/discovery and tool execution UI.
- edge_cases_or_failure_modes: Redundant server prefix stripping, invalid schema, disconnected transport, retriable stale connection, and MCP content variants.
- validation_or_tests: `mcp-render-status.test.ts` validates render/merge behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2196 `file` `packages/coding-agent/src/modes/setup-version.ts`
- cursor: `[_]`
- core_role: Setup wizard version constant.
- algorithmic_behavior: Exports `CURRENT_SETUP_VERSION=1` used by cold-launch setup gate without importing full wizard dependencies.
- inputs_outputs_state: Input is stored setup version elsewhere; output is current version constant.
- gates_or_invariants: Must equal max `scene.minVersion` across setup scenes.
- dependencies_and_callers: Used by startup gate and setup wizard tests.
- edge_cases_or_failure_modes: Forgetting to bump when adding scenes causes stale setup detection drift.
- validation_or_tests: Setup wizard barrel/test suite guard mentioned in file comments.
- skip_candidate: `yes: constant-only gate value`

### OH_MY_HUMANIZE_MAIN-HZ-2226 `file` `packages/coding-agent/src/session/session-history-format.ts`
- cursor: `[_]`
- core_role: Concise markdown serializer for `history://` transcript URLs.
- algorithmic_behavior: Converts message arrays to markdown, indexes tool results by call ID, collapses tool calls/results to one-line summaries, elides thinking by default, handles execution/custom/branch/compaction/file mention messages, and supports watched-role labels.
- inputs_outputs_state: Inputs are session messages and formatting options; output is compact markdown ending with newline.
- gates_or_invariants: Tool result consumed once; orphan results render separately; excluded executions skipped; primary arg chosen by preference list; images become `[image]`.
- dependencies_and_callers: Used by internal URL/history readers and advisor/watched session embedding.
- edge_cases_or_failure_modes: Truncated histories with orphan tool results, empty messages, repeated watched roles, JSON stringify failures, and redacted thinking.
- validation_or_tests: Session dump/history tests cover related serialization behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2256 `file` `packages/coding-agent/src/stt/endpointer.ts`
- cursor: `[_]`
- core_role: Deterministic energy-based speech endpointer for live transcription.
- algorithmic_behavior: Buffers 16kHz mono float samples into frames, tracks adaptive noise floor, detects voiced segments, emits partial previews on cadence, finalizes on trailing silence or max length, and includes pre-roll/tail trimming.
- inputs_outputs_state: Inputs are `Float32Array` sample chunks/config; outputs are ordered `{partial|segment,audio}` events.
- gates_or_invariants: RMS threshold is `max(minThreshold, noiseFloor*ratio)`, noise updates only on non-speech, min speech duration discards noise, max segment commits pause-free speech.
- dependencies_and_callers: Used by STT live transcription pipeline before sherpa/Whisper non-streaming decoders.
- edge_cases_or_failure_modes: Leftover partial frames, near-silent rooms, long no-pause speech, short noise bursts, flush of pending segment, and clipping first phoneme without pre-roll.
- validation_or_tests: Unit-testable with synthetic signals; STT tests cover behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2286 `file` `packages/coding-agent/src/tool-discovery/tool-index.ts`
- cursor: `[_]`
- core_role: BM25 index for discoverable/deferred tools.
- algorithmic_behavior: Tokenizes normalized tool names/labels/server/schema keys, computes document frequencies/average length, scores BM25 with field weights, sorts ties by name, and returns ranked tool docs.
- inputs_outputs_state: Inputs are tool definitions and query/limit; outputs are ranked tool matches and scores.
- gates_or_invariants: NFKD accent removal, camel/acronym splitting, schema-key extraction fallback, field weights name 6/label 4/MCP 4/server 2/summary 2/schema 1.
- dependencies_and_callers: Used by `search-tool-bm25.ts` to activate deferred tools.
- edge_cases_or_failure_modes: Empty docs/query, duplicate tokens, schema shape unknown, and deterministic tie ordering.
- validation_or_tests: Tool discovery tests validate search/activation behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2316 `file` `packages/coding-agent/src/tools/grouped-file-output.ts`
- cursor: `[_]`
- core_role: Shared formatter/parser for grouped per-file tool output.
- algorithmic_behavior: Builds prefix-folded path tree headers for files, emits model/display lines, classifies grouped output lines back to dir/file/content contexts, resolves header paths, and groups by blank separators.
- inputs_outputs_state: Inputs are file path list/render callback and output lines/header base; outputs are grouped model/display arrays and line contexts.
- gates_or_invariants: Duplicate/skipped files ignored; URL-like headers marked `isUrl`; suffix/hash tags stripped when resolving; stack keyed by header depth preserves nested dirs.
- dependencies_and_callers: Used by grep/ast-grep/ast-edit/LSP diagnostic renderers and TUI hyperlinking.
- edge_cases_or_failure_modes: Single-file scopes without headers, root-level files, blank separator absence, absolute paths, URL headers, and hash-tag suffixes.
- validation_or_tests: Tool rendering/search tests exercise grouped output.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2346 `file` `packages/coding-agent/src/tools/search-tool-bm25.ts`
- cursor: `[_]`
- core_role: Agent tool wrapper for BM25 deferred-tool discovery.
- algorithmic_behavior: Validates query/limit, searches inactive discoverable tools, activates selected names, returns JSON summaries/details, and renders sanitized/truncated match lines.
- inputs_outputs_state: Inputs are search query, positive integer limit, tool discovery session; outputs are activated tools and JSON/text result.
- gates_or_invariants: Disabled when discovery mode off or session lacks activation; empty query and nonpositive limit rejected; unselected tools only.
- dependencies_and_callers: Uses `tool-index.ts`, tool activation session APIs, and TUI sanitizers.
- edge_cases_or_failure_modes: No matches, activation failure, partial args rendering, tab/long-line sanitization.
- validation_or_tests: Tool discovery tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2376 `file` `packages/coding-agent/src/tui/utils.ts`
- cursor: `[_]`
- core_role: Shared TUI renderer utilities and render-cache hash builder.
- algorithmic_behavior: Provides incremental xxHash64 `Hasher` for strings/numbers/booleans/bigints/optional sentinels, tree prefix helpers, width padding, and state-to-background mapping.
- inputs_outputs_state: Inputs are primitive render state, tree ancestry flags, text/width/state; outputs are bigint cache keys and styled/padded strings.
- gates_or_invariants: String hashing prefixes length; null/undefined optional hashes sentinel `0xff`; padding uses visible width.
- dependencies_and_callers: Used by coding-agent TUI tool renderers/components.
- edge_cases_or_failure_modes: Cache key collision, ANSI width mismatch, nonpositive width.
- validation_or_tests: Renderer tests validate downstream.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2406 `file` `packages/coding-agent/src/utils/zip.ts`
- cursor: `[_]`
- core_role: Central archive reader/writer/extractor for zip/tar/tar.gz.
- algorithmic_behavior: Reads ZIP central directory including ZIP64 metadata, lazily lists/reads members, writes deterministic ZIPs with raw DEFLATE, handles tar via Bun.Archive, and extracts while enforcing path containment/size limits.
- inputs_outputs_state: Inputs are archive bytes/files and destination paths; outputs are member lists, extracted files, or archive bytes.
- gates_or_invariants: Rejects traversal/`..`, unsupported compression/encryption/multidisk, unsafe ranges, tar >256MiB/member >64MiB, and ZIP64 writes.
- dependencies_and_callers: Used by archive tools/import/export flows; depends on Bun.Archive and binary parsing.
- edge_cases_or_failure_modes: Malformed central directory, ZIP64 locator, binary directories, symlink/path traversal, unsupported method, and deterministic 1980 timestamp.
- validation_or_tests: Archive utility tests cover core behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2436 `file` `packages/coding-agent/src/workflow/script-runtime-env.ts`
- cursor: `[_]`
- core_role: Environment builder for workflow script runtimes.
- algorithmic_behavior: Serializes workflow context/resource dir into `OMP_WORKFLOW_CONTEXT` and `OMP_WORKFLOW_RESOURCE_DIR`, merges with base env while dropping undefined values, and returns undefined if no additions.
- inputs_outputs_state: Inputs are optional context/resourceDir/baseEnv; output is env map or undefined.
- gates_or_invariants: Additions override base env; undefined base values omitted.
- dependencies_and_callers: Used by workflow node/script runtime adapters.
- edge_cases_or_failure_modes: Non-serializable context would throw during `JSON.stringify`.
- validation_or_tests: Workflow shell/runtime tests cover env-adjacent script execution.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2466 `file` `packages/coding-agent/test/core/python-executor-owner-cleanup.test.ts`
- cursor: `[_]`
- core_role: Regression suite for retained Python kernel owner cleanup.
- algorithmic_behavior: Mocks `PythonKernel.start`, executes retained/per-call kernels with owner IDs, disposes by owner/global, and asserts shutdown/reuse/race/cancel behavior.
- inputs_outputs_state: Inputs are executor options, fake kernel states, shutdown promises; outputs are execute results and shutdown call counts.
- gates_or_invariants: Shared retained kernel stays alive until last owner; owner disposal claims kernel so new owner gets replacement; per-call kernels excluded from owner cleanup.
- dependencies_and_callers: Tests Python eval executor/session cache and kernel availability.
- edge_cases_or_failure_modes: Dead kernel restart shutdown timeout, stuck executions not blocking cleanup, owner fallback to session ID, cross-cwd/session cleanup.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2496 `file` `packages/coding-agent/test/discovery/disabled-extensions.test.ts`
- cursor: `[_]`
- core_role: Regression for disabled extension filtering in discovery.
- algorithmic_behavior: Creates temp project/home, disables `context-file:project:AGENTS.md`, initializes settings/discovery, and asserts runtime load hides it while dashboard-style load can include disabled items.
- inputs_outputs_state: Inputs are settings/cwd/context file; outputs are capability item arrays.
- gates_or_invariants: Runtime loads exclude disabled by default; `includeDisabled=true` returns disabled items for management UI.
- dependencies_and_callers: Tests discovery initialization, settings, and context-file capability.
- edge_cases_or_failure_modes: HOME mocking, project `.omp/AGENTS.md`, reset cleanup.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2526 `file` `packages/coding-agent/test/helpers/agent-session-setup.ts`
- cursor: `[_]`
- core_role: Minimal assistant message factory for AgentSession tests.
- algorithmic_behavior: Returns a mock `AssistantMessage` with text block, zero usage, provider/model metadata, `stopReason:"stop"`, and timestamp.
- inputs_outputs_state: Input is text; output is assistant message.
- gates_or_invariants: Usage cost fields all present to satisfy runtime shape.
- dependencies_and_callers: Shared by AgentSession test suites.
- edge_cases_or_failure_modes: Timestamp nondeterminism only.
- validation_or_tests: Helper used by tests.
- skip_candidate: `yes: test helper only`

### OH_MY_HUMANIZE_MAIN-HZ-2556 `file` `packages/coding-agent/test/modes/internal-url-autocomplete.test.ts`
- cursor: `[_]`
- core_role: Regression suite for internal URL autocomplete.
- algorithmic_behavior: Sets active skills/rules, tests token extraction, router completion, fuzzy ranking, applying completion in-place, prefix detection, and prompt autocomplete integration.
- inputs_outputs_state: Inputs are prompt lines/cursor, active skill/rule sets; outputs are suggestion lists, prefixes, updated lines/cursor.
- gates_or_invariants: Requires `scheme:/` or `scheme://`; ignores http/https/no-handler schemes and prose colons; completion schemes are enumerated.
- dependencies_and_callers: Tests `InternalUrlRouter`, skill/rule registries, prompt autocomplete provider.
- edge_cases_or_failure_modes: Single slash in-progress tokens, nested local paths, no matches, preserving text after cursor.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2586 `file` `packages/coding-agent/test/session/session-dump-format.test.ts`
- cursor: `[_]`
- core_role: Regression suite for `/dump` tool catalog and transcript formatting.
- algorithmic_behavior: Formats arktype/JSON-schema tools into TypeScript signatures, includes native syntax examples, renders legacy markdown role headings/tool call/result sections, and avoids nested thinking envelopes.
- inputs_outputs_state: Inputs are tool definitions, model, messages; output is session dump text.
- gates_or_invariants: No arktype internals/XML parameter leaks; `_i` intent renders as comment; no native transcript envelope; thinking wrappers unwrapped/re-wrapped once.
- dependencies_and_callers: Tests `formatSessionDumpText`.
- edge_cases_or_failure_modes: Sibling thinking blocks split by tool call, already-enveloped thinking, plain JSON schema.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2616 `file` `packages/coding-agent/test/task/executor-subagent-reminders.test.ts`
- cursor: `[_]`
- core_role: Regression suite for subagent yield reminders and review finding injection.
- algorithmic_behavior: Mocks subagent sessions/SDK, runs subprocess/finalization paths, verifies missing-yield warnings/reminders, busy handling, structured output merging, and `report_finding` injection respecting schemas.
- inputs_outputs_state: Inputs are mock assistant stops/yield items/findings/output schema; outputs are subprocess raw output/stderr/exit code and injected findings.
- gates_or_invariants: Subagents expected to use `yield`; warnings must be actionable; findings inject only when schema allows or legacy/free-form path.
- dependencies_and_callers: Tests `task/executor` and SDK session creation hooks.
- edge_cases_or_failure_modes: No-yield fallback, schema with `additionalProperties:false`, busy session, aborted runs, report findings with reviewer schema.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2646 `file` `packages/coding-agent/test/tools/bash-pty-selection.test.ts`
- cursor: `[_]`
- core_role: Regression for bash PTY/session selection.
- algorithmic_behavior: Tests bash executor/tool option selection for PTY vs non-PTY paths based on command/session/options.
- inputs_outputs_state: Inputs are tool/session settings and bash args; outputs are executor selection assertions.
- gates_or_invariants: PTY only selected when interactive/session semantics require it; noninteractive commands stay pipe-based.
- dependencies_and_callers: Tests bash tool/executor integration.
- edge_cases_or_failure_modes: Session reuse, TTY capability, command forms requiring PTY.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2676 `file` `packages/coding-agent/test/tools/github-cache.test.ts`
- cursor: `[_]`
- core_role: Regression suite for GitHub web/cache behavior.
- algorithmic_behavior: Mocks GitHub fetch/cache paths and asserts cache hit/miss, ETag/body handling, API/raw URL routing, and scraper behavior.
- inputs_outputs_state: Inputs are GitHub URLs, mocked responses, cache dir/state; outputs are cached render results and fetch call assertions.
- gates_or_invariants: Cache keys must be stable and not leak invalid data; conditional requests/metadata preserved where implemented.
- dependencies_and_callers: Tests GitHub scraper/cache utilities used by browser/web tools.
- edge_cases_or_failure_modes: Failed fetch, stale cache, raw vs API URLs, and large content.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2706 `file` `packages/coding-agent/test/tools/review.test.ts`
- cursor: `[_]`
- core_role: Regression suite for code-review/report-finding tooling.
- algorithmic_behavior: Tests review tool/finding schemas, priorities, rendered output, and structured result handling.
- inputs_outputs_state: Inputs are review/finding args and mocked sessions; outputs are tool results and rendered finding payloads.
- gates_or_invariants: Findings must carry priority/confidence/path/line data consistently and be suitable for aggregation.
- dependencies_and_callers: Tests review tools used by subagents and collab renderers.
- edge_cases_or_failure_modes: Missing optional location fields, invalid priority, multiple findings.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2736 `file` `packages/coding-agent/test/utils/clipboard.test.ts`
- cursor: `[_]`
- core_role: Regression suite for image clipboard dispatch across Windows/WSL/Linux.
- algorithmic_behavior: Mocks platform/env, Bun.spawn PowerShell, and native bridge; asserts base64 PNG decoding, fallback behavior, and headless short-circuits.
- inputs_outputs_state: Inputs are platform/env, PowerShell stdout/exit, native result; output is image `{mimeType,data}` or null.
- gates_or_invariants: WSL tries PowerShell first; headless Linux/Termux returns null without native/arboard; Windows PowerShell uses `-Sta`.
- dependencies_and_callers: Tests `readImageFromClipboard` and native bridge integration.
- edge_cases_or_failure_modes: Empty PowerShell payload, nonzero exit, no display server, WSL env detection.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2766 `file` `packages/coding-agent/test/workflow/shell-script-runtime.test.ts`
- cursor: `[_]`
- core_role: Regression suite for workflow shell script runtime adapter.
- algorithmic_behavior: Runs shell scripts in workflow cwd, preserves stdout/long JSON lines, maps nonzero exits, enforces one-shot shell sessions, forwards timeout budget, and aborts promptly.
- inputs_outputs_state: Inputs are workflow activation/node script definitions and abort signals; outputs are `{exitCode,output,error,language}`.
- gates_or_invariants: `reuseShellSession:false`, session key includes workflow activation, long structured JSON must not be ellipsized, abort returns quickly.
- dependencies_and_callers: Tests `createShellScriptRunner`, bash executor, settings.
- edge_cases_or_failure_modes: Nonzero exit, long command state patches, aborted sleep, wait for producer file.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2796 `file` `packages/mnemopi/src/core/episodic-graph.ts`
- cursor: `[_]`
- core_role: SQLite-backed episodic memory graph/gist/fact/link engine.
- algorithmic_behavior: Creates gist/fact/edge tables, extracts gists/facts/entities/temporal/location/emotion heuristically, stores nodes/edges, links new memories to existing by lexical Jaccard/entity/temporal scores, and traverses related memories by BFS depth.
- inputs_outputs_state: Inputs are content, memory IDs, DB path/connection, ingest options; outputs are `IngestResult`, gists/facts/edges, related memory lists, and stats.
- gates_or_invariants: Facts capped at 5 and content truncated to 4096 chars for extraction; edge weights clamped 0..1; unique edges upsert; standalone graph tolerates missing Beam tables.
- dependencies_and_callers: Used by mnemopi memory core; depends on bun sqlite/openDatabase and Beam memory tables when present.
- edge_cases_or_failure_modes: Invalid JSON participants, empty features, missing working/episodic tables, duplicate edges, weak regex facts, and zero-depth traversal.
- validation_or_tests: Mnemopi extraction/streaming tests cover adjacent memory behavior; graph-specific tests may exist outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2826 `file` `packages/mnemopi/src/migrations/index.ts`
- cursor: `[_]`
- core_role: Barrel export for mnemopi migrations.
- algorithmic_behavior: Re-exports migration modules.
- inputs_outputs_state: Inputs/outputs are module exports only.
- gates_or_invariants: Must preserve migration export surface.
- dependencies_and_callers: Imported by migration runner/CLI.
- edge_cases_or_failure_modes: Missing export would hide migration.
- validation_or_tests: Compile checks.
- skip_candidate: `yes: barrel only, not executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2856 `file` `packages/tui/src/components/text.ts`
- cursor: `[_]`
- core_role: Basic TUI text component.
- algorithmic_behavior: Renders fixed text with width truncation/padding/alignment behavior used by containers.
- inputs_outputs_state: Inputs are text, width, component dimensions/options; outputs are rendered line arrays.
- gates_or_invariants: Must respect visible width and component height.
- dependencies_and_callers: Used broadly by TUI/coding-agent components.
- edge_cases_or_failure_modes: ANSI width, multiline text, narrow widths.
- validation_or_tests: TUI render tests cover component behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2886 `directory` `packages/coding-agent/src/extensibility/plugins/marketplace`
- cursor: `[_]`
- core_role: Marketplace registry/cache/fetch/install/update layer for plugins.
- algorithmic_behavior: Validates marketplace/plugin names and versions, reads/writes registries atomically, fetches catalog metadata from local/git/github/url sources, resolves source subdirs safely, stages cache entries, installs/uninstalls/checks upgrades, and schedules auto-update.
- inputs_outputs_state: Inputs are marketplace specs, URLs, git refs, plugin names, local paths; outputs are cached plugin dirs, installed registries, update reports, and warnings.
- gates_or_invariants: Path components reject `..`; staging then rename; relative source containment; invalid catalog/plugin entries skipped with warnings; npm source unsupported in resolver.
- dependencies_and_callers: Used by plugin manager/commands; depends on filesystem, git/network fetchers, plugin installer.
- edge_cases_or_failure_modes: Invalid marketplace JSON, clone subdir escape, orphaned cache refs, missing source file, auto-update failure ignored.
- validation_or_tests: Plugin marketplace tests cover registry/cache/source behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2916 `file` `crates/pi-shell/src/minimizer/filters/mod.rs`
- cursor: `[_]`
- core_role: Dispatch table and wrapper classifier for command-output minimizers.
- algorithmic_behavior: `supports` maps programs/subcommands to filters; `filter` dispatches to language/tool filters; wrapper helpers classify `npm/pnpm/yarn/npx/uv/bundle` invocations by actual command word while skipping flags/value-taking options.
- inputs_outputs_state: Inputs are `MinimizerCtx`, raw command output, exit code; output is `MinimizerOutput`.
- gates_or_invariants: Tool names appearing only as arguments must not route filters; `uv pytest`/`uv -m pytest`/`bundle exec` route to inner tools; unknown wrappers pass through.
- dependencies_and_callers: Used by pi-shell minimizer after command execution; depends on per-domain filters.
- edge_cases_or_failure_modes: `--with pytest echo`, `npm run build -- test`, `python -m pytest`, nested bundle paths, legacy filter kill switch, and JSON lint output preservation.
- validation_or_tests: Inline Rust tests extensively cover wrapper routing and pass-through behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2946 `file` `packages/ai/src/utils/schema/adapt.ts`
- cursor: `[_]`
- core_role: Shared strict JSON-schema adapter for OpenAI-style tool schemas.
- algorithmic_behavior: Upgrades schema to draft 2020-12, honors caller strict boolean, and attempts strict enforcement with fallback if unrepresentable.
- inputs_outputs_state: Inputs are JSON schema and strict flag; output is `{schema, strict}`.
- gates_or_invariants: `PI_NO_STRICT` flag exported for global bypass; non-strict returns upgraded schema unchanged.
- dependencies_and_callers: Used by OpenAI/Anthropic provider tool schema emission.
- edge_cases_or_failure_modes: Draft mismatch and schemas impossible to represent in strict mode.
- validation_or_tests: Provider schema tests validate downstream.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2976 `file` `packages/coding-agent/src/cli/gallery-fixtures/interaction.ts`
- cursor: `[_]`
- core_role: Gallery fixture data for interaction tool rendering.
- algorithmic_behavior: Defines sample streaming/final args, result details, and error result for the `todo` tool gallery.
- inputs_outputs_state: Inputs are static fixture objects; outputs feed gallery renderer.
- gates_or_invariants: Fixture result shape mirrors todo tool details with phases/tasks/completedTasks.
- dependencies_and_callers: Used by CLI gallery fixtures.
- edge_cases_or_failure_modes: Fixture drift from actual tool schema.
- validation_or_tests: Gallery rendering tests/manual review.
- skip_candidate: `yes: static fixture data`

### OH_MY_HUMANIZE_MAIN-HZ-3006 `file` `packages/coding-agent/src/edit/apply-patch/index.ts`
- cursor: `[_]`
- core_role: Multi-file Codex `apply_patch` envelope orchestrator.
- algorithmic_behavior: Parses a `*** Begin Patch` envelope, applies hunks sequentially via single-file `applyPatch`, records added/modified/deleted paths, and formats A/M/D summary.
- inputs_outputs_state: Inputs are raw patch text and apply options; outputs are per-file results plus affected path summary.
- gates_or_invariants: Non-atomic by spec; no hunks throws `ApplyPatchError`; renames reported as modified original path.
- dependencies_and_callers: Used by freeform/grammar apply-patch tool path; depends on parser and patch mode.
- edge_cases_or_failure_modes: Hunk N failure leaves prior hunks applied; empty patch; delete/create/update classification.
- validation_or_tests: Apply-patch/edit tests cover patch behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3036 `file` `packages/coding-agent/src/eval/py/index.ts`
- cursor: `[_]`
- core_role: Python executor backend adapter for eval framework.
- algorithmic_behavior: Checks Python kernel availability, namespaces session IDs with `python:`, reads interpreter/kernel settings, resolves eval URL roots, calls `executePython`, and maps result fields to generic backend result.
- inputs_outputs_state: Inputs are code, cwd/session/options/settings; outputs are eval backend output/exit/cancel/truncation/artifacts/display outputs.
- gates_or_invariants: Session IDs idempotently prefixed; interpreter setting trimmed; artifacts/local roots passed through.
- dependencies_and_callers: Used by eval tool backend registry; depends on Python executor/kernel.
- edge_cases_or_failure_modes: Kernel unavailable, reset requested, abort signal, missing artifacts dir, per-call vs session mode.
- validation_or_tests: Python executor owner cleanup tests validate executor lifecycle.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3066 `file` `packages/coding-agent/src/extensibility/hooks/types.ts`
- cursor: `[_]`
- core_role: Public hook API type contract for extensions/hooks.
- algorithmic_behavior: Defines narrow hook UI/context surfaces, command-safe session methods, event payload types, and tool-result discriminated unions for hook handlers.
- inputs_outputs_state: Inputs are session/tool/agent lifecycle events; outputs are hook return/result types and UI requests.
- gates_or_invariants: Hook context deliberately omits dangerous extension/session mutation methods to avoid deadlocks; command context adds only user-initiated safe controls.
- dependencies_and_callers: Used by hook runner, plugin APIs, and extension authors.
- edge_cases_or_failure_modes: API widening could allow agent-loop deadlocks; type drift breaks external hooks.
- validation_or_tests: Hook/extension compile tests and runtime integration validate.
- skip_candidate: `yes: type/API contract, not executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3096 `file` `packages/coding-agent/src/modes/acp/terminal-auth.ts`
- cursor: `[_]`
- core_role: Arg sanitizer for ACP terminal auth launch.
- algorithmic_behavior: Detects `--acp-terminal-auth`, removes it, and strips `--mode`/`--mode=<value>` args when terminal auth is active.
- inputs_outputs_state: Inputs are raw argv; outputs are `{args, terminalAuth}`.
- gates_or_invariants: Without auth flag, only auth flag removal occurs; with auth, mode is forcibly removed.
- dependencies_and_callers: Used by ACP mode startup/auth path.
- edge_cases_or_failure_modes: `--mode` with missing value, repeated flags, `--mode=` form.
- validation_or_tests: ACP mode tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3126 `file` `packages/coding-agent/src/modes/components/keybinding-hints.ts`
- cursor: `[_]`
- core_role: UI formatting helpers for keybinding hints.
- algorithmic_behavior: Looks up editor/app keybindings, joins multiple keys with `/`, and styles key/description using theme.
- inputs_outputs_state: Inputs are action IDs/keybinding manager/description; outputs are styled hint strings.
- gates_or_invariants: Empty key list yields empty key segment; raw hints bypass lookup.
- dependencies_and_callers: Used by interactive TUI components.
- edge_cases_or_failure_modes: Missing binding produces description with empty key; theme initialization required.
- validation_or_tests: TUI/render tests cover display indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3156 `file` `packages/coding-agent/src/modes/components/tree-selector.ts`
- cursor: `[_]`
- core_role: Interactive session tree selector component.
- algorithmic_behavior: Iteratively flattens session tree, prioritizes active branch, tracks active path/tool calls, filters/searches entries, renders ASCII gutters/connectors with width compression, handles navigation/filter/search/label input keys.
- inputs_outputs_state: Inputs are `SessionTreeNode[]`, current leaf, terminal height, key data; outputs are rendered lines and select/cancel/label callbacks.
- gates_or_invariants: Avoids recursion stack overflow; hides tool-only assistant messages unless current/error; preserves selection across empty filters; reserves content width; supports multiple roots virtual branch.
- dependencies_and_callers: Used by `/tree` interactive mode; depends on pi-tui components, key matchers, theme, path shortening.
- edge_cases_or_failure_modes: Deep branching, last-sibling chain gutter anchors (#2298/#2325), empty hidden-default state, narrow terminal, fuzzy search no matches.
- validation_or_tests: `tree-selector-chain-gutter-2298.test.ts` validates gutter invariants.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3186 `file` `packages/coding-agent/src/modes/rpc/rpc-types.ts`
- cursor: `[_]`
- core_role: JSONL RPC protocol type surface for headless coding-agent mode.
- algorithmic_behavior: Defines command union, session state, response union, subagent frames, extension UI requests, host tool call/update/result frames, and host URI read/write frames.
- inputs_outputs_state: Inputs/outputs are typed JSON-line protocol messages over stdin/stdout.
- gates_or_invariants: Command/response discriminants must align; host URI result content required for successful reads; cancellation frames target pending IDs.
- dependencies_and_callers: Used by RPC server/client, collab/web, host tool/URI integrations.
- edge_cases_or_failure_modes: Protocol drift breaks external clients; optional fields must be tolerated.
- validation_or_tests: RPC tests and checkpoint RPC QA validate behavior.
- skip_candidate: `yes: protocol type contract rather than executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3216 `file` `packages/coding-agent/src/tools/browser/readable.ts`
- cursor: `[_]`
- core_role: HTML readability extraction helper for browser/readable tools.
- algorithmic_behavior: Dynamically loads Readability and linkedom, parses HTML, tries article extraction first, then CSS selector fallback, and converts to text or markdown.
- inputs_outputs_state: Inputs are raw HTML, URL, format; output is readable result with metadata/content or null.
- gates_or_invariants: Result must have non-empty selected content; markdown falls back to text if HTML conversion empty.
- dependencies_and_callers: Used by browser/readable web tooling; depends on `@mozilla/readability`, `linkedom`, and HTML-to-markdown scraper.
- edge_cases_or_failure_modes: No article/body content, dynamic import failures, empty markdown, missing title/byline/excerpt.
- validation_or_tests: Browser/web tests validate extraction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3246 `file` `packages/coding-agent/src/web/scrapers/github.ts`
- cursor: `[_]`
- core_role: Special GitHub URL scraper/renderer.
- algorithmic_behavior: Parses GitHub URLs into repo/blob/tree/commit/issue/pull/actions forms, fetches raw/API data with optional token, renders markdown for issues/comments, commits/diffs, repo/tree/README, actions runs/jobs/logs, and strips log timestamps.
- inputs_outputs_state: Inputs are GitHub URL, timeout, abort signal, env token; outputs are `RenderResult` or null with method/fetchedAt/notes.
- gates_or_invariants: Non-GitHub/unsupported URLs return null; comments paginated; repo tree limited to first 100 files; job logs need token/access and timestamps stripped.
- dependencies_and_callers: Used by web fetch/browser tools; depends on loadPage, GitHub API, env `GITHUB_TOKEN`/`GH_TOKEN`.
- edge_cases_or_failure_modes: API failure fallback to normal rendering, binary/too-large commit patch, expired/unavailable logs, README fetch failure, action job/run ambiguity.
- validation_or_tests: GitHub cache/tool tests validate scraper/cache paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3276 `file` `packages/coding-agent/src/web/scrapers/rawg.ts`
- cursor: `[_]`
- core_role: Special RAWG game page scraper.
- algorithmic_behavior: Recognizes `rawg.io/games/<slug>`, fetches RAWG API JSON, rejects API-key-required responses, formats title/release/rating/platforms/genres/link/description to markdown.
- inputs_outputs_state: Inputs are RAWG URL/timeout/signal; output is `RenderResult` or null.
- gates_or_invariants: Host/path must match; API key error text returns null; descriptions prefer raw text else HTML-to-markdown.
- dependencies_and_callers: Used by web scraper registry; depends on `loadPage`, `tryParseJson`, markdown converter.
- edge_cases_or_failure_modes: API key required, invalid JSON, missing slug, duplicate platform/genre names.
- validation_or_tests: Web scraper tests cover special handlers where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3306 `file` `packages/coding-agent/src/workflow/__tests__/runner.test.ts`
- cursor: `[_]`
- core_role: Regression for workflow lifecycle checkpoint/restart.
- algorithmic_behavior: Runs a three-node workflow with a failing middle activation, reconstructs lifecycle family/checkpoint, then restarts from checkpoint and verifies recovered activations/status.
- inputs_outputs_state: Inputs are in-memory host, workflow definition/freeze, runtime host scripts; outputs are lifecycle entries, checkpoints, state patches, activation status.
- gates_or_invariants: Failed attempt records checkpoint with frontier node IDs, prior completed activation IDs, state, and source mapping; restart can suppress duplicate family/freeze records.
- dependencies_and_callers: Tests workflow runner/scheduler/lifecycle reconstruction.
- edge_cases_or_failure_modes: Mid-graph failure, state patch carry-over, completed activation reuse.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3336 `file` `packages/coding-agent/test/modes/components/tree-selector-chain-gutter-2298.test.ts`
- cursor: `[_]`
- core_role: Regression for session tree selector gutter rendering.
- algorithmic_behavior: Builds synthetic branched session trees, renders stripped tree selector output, and asserts inherited vertical anchors appear only in correct columns for last-sibling chains.
- inputs_outputs_state: Inputs are synthetic `SessionTreeNode`s and active leaf; output is rendered tree text.
- gates_or_invariants: Chain descendants under `└─` anchor one level right; branched grandchildren preserve standard tree semantics without floating verticals.
- dependencies_and_callers: Tests `TreeSelectorComponent` and theme.
- edge_cases_or_failure_modes: Nested last-sibling branch chains and active branch ordering.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3366 `file` `packages/coding-agent/test/modes/theme/shimmer.test.ts`
- cursor: `[_]`
- core_role: Regression for shimmer text raw ANSI crest color.
- algorithmic_behavior: Mocks settings/date, calls `shimmerText` with raw ANSI mid/high color, and asserts raw ANSI present while stripped text remains unchanged.
- inputs_outputs_state: Inputs are text/theme/color options/time; output is ANSI-styled string.
- gates_or_invariants: Raw ANSI color objects must be honored and not corrupt visible text.
- dependencies_and_callers: Tests theme shimmer utility.
- edge_cases_or_failure_modes: Settings uninitialized path, fixed-velocity crest positioning, bold wrapping.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3396 `file` `packages/collab-web/src/components/agents/AgentsPanel.tsx`
- cursor: `[_]`
- core_role: Web UI panel for main/subagent status summaries.
- algorithmic_behavior: Ticks current time every second, sorts main/sub agents with running first/recent activity, computes activity line from current tool/intent/lifecycle/status, and toggles selected agent on click.
- inputs_outputs_state: Inputs are agent snapshots, progress/lifecycle maps, selected ID; output is React rows/empty state.
- gates_or_invariants: Tool duration uses `currentToolStartMs` if present else recent tool end; selected click toggles null.
- dependencies_and_callers: Used by collab web app; depends on `@oh-my-pi/pi-wire` progress types and formatting helpers.
- edge_cases_or_failure_modes: Missing progress/lifecycle, omitted `currentToolStartMs` in wire type, no subagents.
- validation_or_tests: UI tests/manual validation; algorithm is display sorting.
- skip_candidate: `yes: web UI presentation, not core coding-agent algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3426 `file` `packages/collab-web/src/tool-render/tools/report-finding.tsx`
- cursor: `[_]`
- core_role: Web renderer for structured `report_finding` tool calls.
- algorithmic_behavior: Maps priority to tone, summarizes priority/title, renders badges for priority/confidence/path lines, body output, and error result text.
- inputs_outputs_state: Inputs are tool args/result; output is React summary/body nodes.
- gates_or_invariants: Title strips leading `[P\d]`; confidence displayed as percent; path line range optional.
- dependencies_and_callers: Used by collab web tool renderer registry.
- edge_cases_or_failure_modes: Missing/invalid numeric fields, unknown priority tone, long title truncation.
- validation_or_tests: Renderer tests/manual UI.
- skip_candidate: `yes: web presentation renderer`

### OH_MY_HUMANIZE_MAIN-HZ-3456 `file` `packages/stats/src/client/components/chart-shared.tsx`
- cursor: `[_]`
- core_role: Shared stats dashboard chart styling and time-series bucketing utilities.
- algorithmic_behavior: Builds Chart.js plugin/scales configs, styles line/bar datasets, aggregates points by day, and builds top-N-by-model series with an `Other` rollup and disambiguated duplicate model labels.
- inputs_outputs_state: Inputs are chart theme/options and timestamped points; outputs are chart config fragments and `ChartSeries`.
- gates_or_invariants: Empty input returns empty series; labels sorted by timestamp; top-N ranking uses caller-provided weight; duplicate model names include provider.
- dependencies_and_callers: Used by stats dashboard cost/behavior/performance charts; depends on `date-fns`.
- edge_cases_or_failure_modes: Sparse days, models beyond top N, zero buckets, duplicate model IDs across providers.
- validation_or_tests: `client-view-models.test.ts` covers sparse bucket preservation for related view model logic.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3486 `file` `packages/utils/src/vendor/mermaid-ascii/multiline-utils.ts`
- cursor: `[_]`
- core_role: Mermaid ASCII label normalization utility.
- algorithmic_behavior: Strips surrounding quotes, converts `<br>` and `\n` escapes to newlines, removes unsupported inline HTML tags, and reduces markdown emphasis/strikethrough to plain text.
- inputs_outputs_state: Input is raw Mermaid label; output is normalized terminal label string.
- gates_or_invariants: ASCII renderer has no styled spans, so markup must not leak into boxes.
- dependencies_and_callers: Shared by vendored Mermaid ASCII parsers/renderers.
- edge_cases_or_failure_modes: Quoted labels, HTML formatting tags, markdown emphasis regex boundaries.
- validation_or_tests: Mermaid ASCII tests validate rendering where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3516 `file` `packages/coding-agent/src/eval/js/shared/indirect-eval.ts`
- cursor: `[_]`
- core_role: Shared indirect-eval executor for JS/browser eval workers.
- algorithmic_behavior: Appends optional `sourceURL`, calls `globalThis.eval` indirectly so source runs in global scope, and awaits thenables via `awaitMaybePromise`.
- inputs_outputs_state: Inputs are source/filename/value; outputs are eval result or awaited value.
- gates_or_invariants: Indirect eval avoids module lexical scope; avoids `node:vm` due Bun worker termination crash.
- dependencies_and_callers: Used by JS eval worker and browser tab worker.
- edge_cases_or_failure_modes: User code exceptions, synchronous loops, malformed sourceURL filenames, thenable detection.
- validation_or_tests: Eval worker tests validate behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3546 `file` `packages/coding-agent/src/modes/components/status-line/context-thresholds.ts`
- cursor: `[_]`
- core_role: Context usage gauge threshold/formatting helpers.
- algorithmic_behavior: Computes usage level by percent and token-window thresholds, formats `<percent>%/<window>`, and maps levels to theme colors.
- inputs_outputs_state: Inputs are context percent/window; outputs are `normal|warning|purple|error`, display string, and theme color.
- gates_or_invariants: Invalid/nonpositive percent is normal; unknown window uses percent thresholds; finite windows use min(percent threshold, token threshold/window).
- dependencies_and_callers: Used by status line, footer, and subagent renderers.
- edge_cases_or_failure_modes: Null percent renders `?`, huge/small context windows shift thresholds.
- validation_or_tests: Status-line tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3576 `file` `packages/coding-agent/src/web/search/providers/perplexity.ts`
- cursor: `[_]`
- core_role: Perplexity web search provider with OAuth/cookie/API-key/anonymous modes.
- algorithmic_behavior: Builds Perplexity API or ask-endpoint requests, selects auth methods, refreshes OAuth through `withOAuthAccess`, merges incremental SSE snapshots, extracts answers/sources/citations/related questions/usage, falls back across auth methods, and limits sources.
- inputs_outputs_state: Inputs are query/search params/auth storage/env keys/fetch/signal; outputs are `SearchResponse` with provider/authMode/model/requestId/sources.
- gates_or_invariants: OAuth JWT skipped if expiring within 5 minutes; ask endpoint sends session token as cookie not bearer; anonymous not auto-selected unless explicit; abort rethrows immediately; API metadata collected from SSE payloads.
- dependencies_and_callers: Used by web search provider registry; depends on pi-ai OpenAI stream helpers, auth storage, SSE reader, timeout/error classifiers.
- edge_cases_or_failure_modes: Expired OAuth, malformed SSE/text JSON, no response body, provider HTTP errors, missing metadata, API/OpenRouter fallback, source dedupe by URL.
- validation_or_tests: Web search/provider tests validate parsing and auth behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3606 `file` `packages/utils/src/vendor/mermaid-ascii/xychart/types.ts`
- cursor: `[_]`
- core_role: Type definitions for vendored Mermaid xychart parsed/positioned models.
- algorithmic_behavior: Defines parsed chart axes/series and positioned SVG/ASCII layout structures including axes, plot area, bars, lines, grid lines, and legend items.
- inputs_outputs_state: Inputs/outputs are compile-time shapes consumed by parser/layout/render algorithms.
- gates_or_invariants: Axis categories and numeric range are mutually exclusive by convention; series type constrained to bar/line.
- dependencies_and_callers: Used by Mermaid ASCII xychart parser/layout/render modules.
- edge_cases_or_failure_modes: Type drift can break renderer assumptions.
- validation_or_tests: Mermaid xychart tests validate consumers.
- skip_candidate: `yes: type-only model surface`

## Worker Self-Test
- assigned_items_seen: 120 item sections produced for every non-`none` row listed in the prompt: OH_MY_HUMANIZE_MAIN-HZ-006, OH_MY_HUMANIZE_MAIN-HZ-036, OH_MY_HUMANIZE_MAIN-HZ-066, OH_MY_HUMANIZE_MAIN-HZ-096, OH_MY_HUMANIZE_MAIN-HZ-126, OH_MY_HUMANIZE_MAIN-HZ-156, OH_MY_HUMANIZE_MAIN-HZ-186, OH_MY_HUMANIZE_MAIN-HZ-216, OH_MY_HUMANIZE_MAIN-HZ-246, OH_MY_HUMANIZE_MAIN-HZ-276, OH_MY_HUMANIZE_MAIN-HZ-306, OH_MY_HUMANIZE_MAIN-HZ-336, OH_MY_HUMANIZE_MAIN-HZ-366, OH_MY_HUMANIZE_MAIN-HZ-396, OH_MY_HUMANIZE_MAIN-HZ-426, OH_MY_HUMANIZE_MAIN-HZ-456, OH_MY_HUMANIZE_MAIN-HZ-486, OH_MY_HUMANIZE_MAIN-HZ-516, OH_MY_HUMANIZE_MAIN-HZ-546, OH_MY_HUMANIZE_MAIN-HZ-576, OH_MY_HUMANIZE_MAIN-HZ-606, OH_MY_HUMANIZE_MAIN-HZ-636, OH_MY_HUMANIZE_MAIN-HZ-666, OH_MY_HUMANIZE_MAIN-HZ-696, OH_MY_HUMANIZE_MAIN-HZ-726, OH_MY_HUMANIZE_MAIN-HZ-756, OH_MY_HUMANIZE_MAIN-HZ-786, OH_MY_HUMANIZE_MAIN-HZ-816, OH_MY_HUMANIZE_MAIN-HZ-846, OH_MY_HUMANIZE_MAIN-HZ-876, OH_MY_HUMANIZE_MAIN-HZ-906, OH_MY_HUMANIZE_MAIN-HZ-936, OH_MY_HUMANIZE_MAIN-HZ-966, OH_MY_HUMANIZE_MAIN-HZ-996, OH_MY_HUMANIZE_MAIN-HZ-1026, OH_MY_HUMANIZE_MAIN-HZ-1056, OH_MY_HUMANIZE_MAIN-HZ-1086, OH_MY_HUMANIZE_MAIN-HZ-1116, OH_MY_HUMANIZE_MAIN-HZ-1146, OH_MY_HUMANIZE_MAIN-HZ-1176, OH_MY_HUMANIZE_MAIN-HZ-1206, OH_MY_HUMANIZE_MAIN-HZ-1236, OH_MY_HUMANIZE_MAIN-HZ-1266, OH_MY_HUMANIZE_MAIN-HZ-1296, OH_MY_HUMANIZE_MAIN-HZ-1326, OH_MY_HUMANIZE_MAIN-HZ-1356, OH_MY_HUMANIZE_MAIN-HZ-1386, OH_MY_HUMANIZE_MAIN-HZ-1416, OH_MY_HUMANIZE_MAIN-HZ-1446, OH_MY_HUMANIZE_MAIN-HZ-1476, OH_MY_HUMANIZE_MAIN-HZ-1506, OH_MY_HUMANIZE_MAIN-HZ-1536, OH_MY_HUMANIZE_MAIN-HZ-1566, OH_MY_HUMANIZE_MAIN-HZ-1596, OH_MY_HUMANIZE_MAIN-HZ-1626, OH_MY_HUMANIZE_MAIN-HZ-1656, OH_MY_HUMANIZE_MAIN-HZ-1686, OH_MY_HUMANIZE_MAIN-HZ-1716, OH_MY_HUMANIZE_MAIN-HZ-1746, OH_MY_HUMANIZE_MAIN-HZ-1776, OH_MY_HUMANIZE_MAIN-HZ-1806, OH_MY_HUMANIZE_MAIN-HZ-1836, OH_MY_HUMANIZE_MAIN-HZ-1866, OH_MY_HUMANIZE_MAIN-HZ-1896, OH_MY_HUMANIZE_MAIN-HZ-1926, OH_MY_HUMANIZE_MAIN-HZ-1956, OH_MY_HUMANIZE_MAIN-HZ-1986, OH_MY_HUMANIZE_MAIN-HZ-2016, OH_MY_HUMANIZE_MAIN-HZ-2046, OH_MY_HUMANIZE_MAIN-HZ-2076, OH_MY_HUMANIZE_MAIN-HZ-2106, OH_MY_HUMANIZE_MAIN-HZ-2136, OH_MY_HUMANIZE_MAIN-HZ-2166, OH_MY_HUMANIZE_MAIN-HZ-2196, OH_MY_HUMANIZE_MAIN-HZ-2226, OH_MY_HUMANIZE_MAIN-HZ-2256, OH_MY_HUMANIZE_MAIN-HZ-2286, OH_MY_HUMANIZE_MAIN-HZ-2316, OH_MY_HUMANIZE_MAIN-HZ-2346, OH_MY_HUMANIZE_MAIN-HZ-2376, OH_MY_HUMANIZE_MAIN-HZ-2406, OH_MY_HUMANIZE_MAIN-HZ-2436, OH_MY_HUMANIZE_MAIN-HZ-2466, OH_MY_HUMANIZE_MAIN-HZ-2496, OH_MY_HUMANIZE_MAIN-HZ-2526, OH_MY_HUMANIZE_MAIN-HZ-2556, OH_MY_HUMANIZE_MAIN-HZ-2586, OH_MY_HUMANIZE_MAIN-HZ-2616, OH_MY_HUMANIZE_MAIN-HZ-2646, OH_MY_HUMANIZE_MAIN-HZ-2676, OH_MY_HUMANIZE_MAIN-HZ-2706, OH_MY_HUMANIZE_MAIN-HZ-2736, OH_MY_HUMANIZE_MAIN-HZ-2766, OH_MY_HUMANIZE_MAIN-HZ-2796, OH_MY_HUMANIZE_MAIN-HZ-2826, OH_MY_HUMANIZE_MAIN-HZ-2856, OH_MY_HUMANIZE_MAIN-HZ-2886, OH_MY_HUMANIZE_MAIN-HZ-2916, OH_MY_HUMANIZE_MAIN-HZ-2946, OH_MY_HUMANIZE_MAIN-HZ-2976, OH_MY_HUMANIZE_MAIN-HZ-3006, OH_MY_HUMANIZE_MAIN-HZ-3036, OH_MY_HUMANIZE_MAIN-HZ-3066, OH_MY_HUMANIZE_MAIN-HZ-3096, OH_MY_HUMANIZE_MAIN-HZ-3126, OH_MY_HUMANIZE_MAIN-HZ-3156, OH_MY_HUMANIZE_MAIN-HZ-3186, OH_MY_HUMANIZE_MAIN-HZ-3216, OH_MY_HUMANIZE_MAIN-HZ-3246, OH_MY_HUMANIZE_MAIN-HZ-3276, OH_MY_HUMANIZE_MAIN-HZ-3306, OH_MY_HUMANIZE_MAIN-HZ-3336, OH_MY_HUMANIZE_MAIN-HZ-3366, OH_MY_HUMANIZE_MAIN-HZ-3396, OH_MY_HUMANIZE_MAIN-HZ-3426, OH_MY_HUMANIZE_MAIN-HZ-3456, OH_MY_HUMANIZE_MAIN-HZ-3486, OH_MY_HUMANIZE_MAIN-HZ-3516, OH_MY_HUMANIZE_MAIN-HZ-3546, OH_MY_HUMANIZE_MAIN-HZ-3576, OH_MY_HUMANIZE_MAIN-HZ-3606.
- missing_items: none among the 120 non-`none` rows shown in the assignment table; the header says `assigned_item_count: 121`, but the provided table contains 120 item IDs.
- duplicate_items: none
- final_worker_status: `complete`