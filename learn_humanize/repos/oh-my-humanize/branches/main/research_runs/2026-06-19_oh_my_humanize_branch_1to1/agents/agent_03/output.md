# agent_03 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-003 `directory` `docs`
- cursor: `[_]`
- core_role: Repository-wide architecture and runtime contract documentation. The directory recursively covers tool runtimes, native bindings, config discovery, MCP, memory, session lifecycle, TUI, provider streaming, and workflow behavior.
- algorithmic_behavior: The docs specify expected algorithms rather than executing them: bash tool flow in `docs/bash-tool-runtime.md`, public tool contract in `docs/tools/bash.md`, shell/PTY/key parsing in `docs/natives-shell-pty-process.md`, memory backend behavior in `docs/memory.md` and `docs/mnemosyne-memory-backend.md`, hooks in `docs/hooks.md`, and config/provider resolution in `docs/config-usage.md`.
- inputs_outputs_state: Inputs are implementation behavior and operator/user-facing interfaces; outputs are stable contracts for command arguments, result shapes, lifecycle states, error states, and side effects. State transitions are documented for shell sessions, PTY processes, handoff/session switching, compaction, memory injection, and hooks.
- gates_or_invariants: Docs repeatedly require bounded output, sanitized TUI rendering, explicit config precedence, model/provider compatibility gates, and native subsystem separation. Tool docs define input/output contracts and limits, e.g. `docs/tools/bash.md:21`, `docs/tools/bash.md:32`, `docs/tools/bash.md:123`.
- dependencies_and_callers: Consumed by maintainers, tests, and feature work across `packages/coding-agent`, `packages/agent`, `packages/ai`, `packages/catalog`, `packages/tui`, `packages/natives`, and Rust crates.
- edge_cases_or_failure_modes: Documentation warns about timeout/cancel semantics, artifact spill, non-interactive shell reuse, MCP lifecycle failures, config ambiguity, and terminal rendering corruption.
- validation_or_tests: Not executable; validation is indirect through package tests and implementation conformance. Directory was recursively inventoried with `find docs -type f`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-033 `directory` `packages/snapcompact`
- cursor: `[_]`
- core_role: Visual/text compaction package that serializes conversations into compact image frames and restored archive payloads for long-context reduction.
- algorithmic_behavior: `src/snapcompact.ts` defines shape catalogs, model-family billing selection, provider image budgets, file-operation summaries, transcript serialization, text normalization, line wrapping, page geometry, frame rendering, archive preservation, and `compact()` orchestration (`packages/snapcompact/src/snapcompact.ts:61`, `:192`, `:681`, `:868`, `:1008`, `:1173`).
- inputs_outputs_state: Inputs are `Message[]`, model/provider metadata, shape options, previous preserved archive data, and file-operation/tool-call content. Outputs are `ImageContent[]`, archive metadata, compaction summary/details, and preserved data keyed by `snapcompact`. State is held in `Archive.frames`, `FileOperations` sets, and preserveData.
- gates_or_invariants: Enforces max frames/image budgets (`MAX_FRAMES`, provider budgets), known shape variants, URL-scheme path filtering, tool-result truncation, normalized renderable glyphs, and provider-specific image billing estimates.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-ai` message types, provider/model identity, prompts under `src/prompts`, and image/render utilities. Used by coding-agent session context restoration (`packages/coding-agent/src/session/session-context.ts:3`).
- edge_cases_or_failure_modes: Handles non-renderable/control characters, URL/internal paths, compound read selectors, stopword dimming, oversized tool output, existing OpenAI remote compaction preserve data, provider frame budget exhaustion, and unknown model families.
- validation_or_tests: `packages/snapcompact/test/snapcompact.test.ts` plus research experiments under `research/`; assigned research files cover Gemini, Braille, and hero visualization.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-063 `file` `docs/natives-shell-pty-process.md`
- cursor: `[_]`
- core_role: Architecture document for native shell, PTY, process, and key parsing subsystems.
- algorithmic_behavior: Describes API models, creation/lifecycle transitions, streaming/minimization, cancellation, timeout, failure behavior, and JS-to-Rust export mapping (`docs/natives-shell-pty-process.md:25`, `:108`, `:184`, `:206`, `:243`).
- inputs_outputs_state: Inputs include shell commands, PTY writes, process IDs, abort signals, key byte sequences, and timeout settings. Outputs include stream chunks, exit status, parsed key IDs, process metadata, and structured native errors. State transitions include spawned, attached, running, terminated, abandoned, and finalized sessions.
- gates_or_invariants: Shell and PTY ownership are separated, abandoned sessions require cleanup, key parsing must distinguish Kitty, CSI-u, modifyOtherKeys, and legacy sequences, and cancellation must not leak subprocesses.
- dependencies_and_callers: Documents Rust native implementations under `crates/pi-natives` and shell minimizer behavior used by `packages/coding-agent` bash/eval render paths.
- edge_cases_or_failure_modes: Covers orphaned sessions, spawn failures, timeout races, abort propagation, partial reads, unsupported key sequences, and cleanup finalization.
- validation_or_tests: Cross-validated by native key tests in `crates/pi-natives/src/keys.rs` and coding-agent bash executor tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-093 `file` `scripts/ci-update-brew-formula.test.ts`
- cursor: `[_]`
- core_role: CI workflow regression test for Homebrew formula rendering.
- algorithmic_behavior: Tests `renderFormula()` output for per-platform URL stanza attributes, completions generation with redirected `HOME`, and asset-specific SHA256 values (`scripts/ci-update-brew-formula.test.ts:11`, `:18`, `:33`, `:43`).
- inputs_outputs_state: Inputs are version plus checksum map; output is formula text. No persistent state.
- gates_or_invariants: Every platform URL must include `using: :nounzip`; shell completions must not write into a real user home; each asset URL must be paired with its expected checksum.
- dependencies_and_callers: Imports `renderFormula` from `scripts/ci-update-brew-formula`; used by release/CI update workflow.
- edge_cases_or_failure_modes: Prevents formula install failures from unzip behavior, buildpath/home pollution, and checksum mismatch.
- validation_or_tests: This file is the validation surface; no runtime command executed in this research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-123 `directory` `packages/agent/src`
- cursor: `[_]`
- core_role: Core agent runtime package: streaming loop, tool execution, append-only context, compaction, telemetry, proxy streams, token counting, and shared types.
- algorithmic_behavior: `agent-loop.ts` drives model streaming, tool-call normalization, intent injection, event emission, continuation, abort/harmony-audit behavior, and tool execution (`packages/agent/src/agent-loop.ts:283`, `:558`, `:606`, `:1460`). `agent.ts` wraps higher-level prompt/session flow. `compaction/` implements cut-point selection, summaries, handoffs, remote compaction, pruning, and file-op tracking. `telemetry.ts` emits GenAI spans and usage/cost metadata.
- inputs_outputs_state: Inputs are `AgentLoopConfig`, messages, system prompts, tools, model streams, abort signals, telemetry config, and session entries. Outputs are `AgentEvent` streams, final messages, tool results, compaction entries, telemetry spans, and run summaries. State includes loop step count, active tool calls, append-only context snapshots, compaction cut ranges, collector records, and abort state.
- gates_or_invariants: Tool schemas receive intent fields according to mode, max step/deadline checks apply, tool results are coerced and malformed results surfaced, abort reasons are normalized, compaction cuts avoid unsafe tool-call boundaries, and telemetry short-circuits when disabled.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-ai`, `@oh-my-pi/pi-utils`, catalog model types, OpenTelemetry, and coding-agent session/tool layers.
- edge_cases_or_failure_modes: Handles malformed tool results, empty tool failures, provider stream interruption after content, explicit vs silent aborts, paused-turn continuation limits, harmony leakage, remote compaction failures, cyclic/circular telemetry content, and content capture bounds.
- validation_or_tests: Covered by many coding-agent tests using `Agent`, including auto-compaction queue, skill keywords, streaming edit abort, transcript streaming commit, and session messages.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-153 `directory` `packages/swarm-extension/src`
- cursor: `[_]`
- core_role: Extension implementing YAML-defined multi-agent swarm/pipeline execution.
- algorithmic_behavior: `schema.ts` parses/validates swarm YAML; `dag.ts` builds dependency graphs, detects cycles, and computes execution waves (`packages/swarm-extension/src/swarm/dag.ts:17`, `:63`, `:106`); `pipeline.ts` schedules wave execution; `executor.ts` runs each agent; `state.ts` tracks per-agent/pipeline status; `render.ts` formats progress; `extension.ts` registers slash commands and status/run handlers.
- inputs_outputs_state: Inputs are YAML files, workspace path, mode, agent definitions, dependencies, and extension command context. Outputs are status text, rendered progress, agent execution results, and state files. State transitions: pending/waiting/running/completed/failed and pipeline idle/running/completed/failed/aborted.
- gates_or_invariants: Valid swarm names, known modes (`pipeline`, `parallel`, `sequential`), acyclic dependency graph, workspace resolution, and command validation before execution.
- dependencies_and_callers: Integrates with coding-agent extension API, model registry/auth discovery, settings, and `Agent` runtime.
- edge_cases_or_failure_modes: Missing YAML, invalid dependencies, cycles, failed agent execution, aborted pipeline, unknown status name, and workspace path resolution issues.
- validation_or_tests: `packages/swarm-extension/src/swarm/__tests__/executor.test.ts` tests executor behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-183 `file` `docs/tools/bash.md`
- cursor: `[_]`
- core_role: Public contract for the coding-agent `bash` tool.
- algorithmic_behavior: Defines source implementation, input schema, output schema, execution flow, variants, side effects, caps, and error behavior (`docs/tools/bash.md:5`, `:21`, `:32`, `:56`, `:101`, `:123`, `:132`).
- inputs_outputs_state: Inputs are command, cwd, env, timeout, background/interactive options, and approval context. Outputs are stdout/stderr/status, artifacts for long output, async job handles, and renderer metadata.
- gates_or_invariants: Validates cwd, clamps timeout, switches PTY/non-PTY based on mode, streams output through sinks, truncates/spills large output, and maps blocked commands or runtime failures to tool errors.
- dependencies_and_callers: Documents `packages/coding-agent/src/exec/bash-executor`, tool renderer, shell session reuse, and native shell/PTY backends.
- edge_cases_or_failure_modes: Long output, blocked command interception, background completion races, cancellation, shell minimizer behavior, artifact expansion, and renderer divergence.
- validation_or_tests: `packages/coding-agent/test/bash-executor.test.ts` is the main contract test suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-213 `file` `scripts/install-tests/source.dockerfile`
- cursor: `[_]`
- core_role: Install smoke-test Docker recipe for source-based local repo installation.
- algorithmic_behavior: Builds a Debian image, installs Bun and nightly Rust, copies the repo, installs dependencies, builds native addon, links coding-agent globally, and verifies `omp --version`.
- inputs_outputs_state: Inputs are repository contents and network package installers; output is a Docker image with linked `omp`. No application state except installed toolchains and global Bun link.
- gates_or_invariants: Requires frozen Bun lockfile, native addon build before global link, and final executable version check.
- dependencies_and_callers: Used by install-test CI scripts; depends on Bun, Rust nightly, `packages/natives`, and `packages/coding-agent`.
- edge_cases_or_failure_modes: Network install failure, lockfile mismatch, native build failure, link failure, and missing `omp` executable.
- validation_or_tests: Final Dockerfile `RUN omp --version` is the smoke validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-243 `directory` `packages/catalog/src/wire`
- cursor: `[_]`
- core_role: Provider wire-protocol constants and normalization helpers shared by catalog discovery and AI auth/provider code.
- algorithmic_behavior: `codex.ts` defines ChatGPT/Codex backend URLs/headers and JWT account extraction (`packages/catalog/src/wire/codex.ts:5`, `:32`); `gemini-headers.ts` builds Gemini CLI and Antigravity user-agent/headers and wire profiles (`:6`, `:29`, `:53`); `github-copilot.ts` normalizes enterprise domains/API endpoints and parses Copilot API-key JSON envelopes (`:44`, `:56`, `:68`, `:100`).
- inputs_outputs_state: Inputs are tokens, model IDs, platform/arch/env, enterprise URLs, and raw API-key strings. Outputs are header maps, base URLs, parsed credentials, and per-wire model metadata. `getAntigravityUserAgent` memoizes computed UA.
- gates_or_invariants: Only HTTPS Copilot API endpoints are accepted; public GitHub hosts are filtered from enterprise domain override; Codex JWT must have three parts and expected claim path; Antigravity profiles are keyed by routed wire ID.
- dependencies_and_callers: Used by `packages/catalog/src/provider-models/openai-compat.ts`, `packages/ai` OAuth/usage/provider implementations, and discovery code.
- edge_cases_or_failure_modes: Malformed JSON API key, invalid URLs, public enterprise host, invalid JWT/base64/JSON, absent Antigravity profile, and platform/arch mapping differences.
- validation_or_tests: Indirectly covered by provider discovery, Google Antigravity usage tests, Copilot usage behavior, and registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-273 `directory` `packages/coding-agent/src/memory-backend`
- cursor: `[_]`
- core_role: Runtime abstraction selecting and exposing memory backends to sessions and tools.
- algorithmic_behavior: `resolve.ts` maps `memory.backend` to off/local/hindsight/mnemopi backends (`packages/coding-agent/src/memory-backend/resolve.ts:19`); `local-backend.ts` wraps rollout-summary memory and learned lessons; `off-backend.ts` is no-op; `runtime.ts` exposes status/search/save with graceful unavailable responses (`:10`, `:52`); `types.ts` defines backend IDs, search/save/status contracts.
- inputs_outputs_state: Inputs are `Settings`, agent dir, cwd, session, search query, and save content. Outputs are backend status, search results, save results, developer instructions, clear/enqueue effects. State lives in selected backend storage, not this router.
- gates_or_invariants: `memory.backend` is the sole runtime selector; no active session returns off/unavailable; absent backend methods produce structured unavailable results rather than throwing.
- dependencies_and_callers: Consumed by memory tools/runtime, settings selector, sessions, local `memories`, hindsight, and mnemopi adapters.
- edge_cases_or_failure_modes: Missing session/settings, disabled memory, backend without search/save/status, dynamic backend import failure, and legacy `memories.enabled` migration ambiguity.
- validation_or_tests: `packages/coding-agent/test/memories/isolation.test.ts` and settings-selector memory refresh tests validate related memory behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-303 `directory` `packages/coding-agent/test/helpers`
- cursor: `[_]`
- core_role: Test support utilities for agent sessions, ACP schema assertions, fetch mocking, settings state, SQLite inspection, and temp-home cleanup.
- algorithmic_behavior: Provides deterministic session setup, mock HTTP routing, schema/type helpers, and cleanup helpers to isolate tests from global config/state.
- inputs_outputs_state: Inputs are temp dirs, fake fetch specs, settings overrides, session messages, and SQLite paths. Outputs are configured objects, mock responses, and cleanup handles. State is temporary test-local filesystem/env/database state.
- gates_or_invariants: Helpers centralize cleanup, avoid persistent user home pollution, and normalize repeated setup across full-suite-safe tests.
- dependencies_and_callers: Imported by coding-agent tests such as skill keywords, auto-compaction queue, ACP, settings, and Python executor display.
- edge_cases_or_failure_modes: Leaked temp homes/settings, stale SQLite handles, mock fetch mismatch, and tests that forget cleanup.
- validation_or_tests: Helper directory itself is exercised by dependent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-333 `directory` `python/omp-rpc/src/omp_rpc`
- cursor: `[_]`
- core_role: Python RPC client/protocol package for controlling OMP sessions and hosting tools/URIs.
- algorithmic_behavior: `protocol.py` defines TypedDict payloads and parsers for messages, events, models, tools, todos, session state, and notifications (`python/omp-rpc/src/omp_rpc/protocol.py:267`, `:284`, `:1072`, `:1484`); `client.py` manages subprocess lifecycle, pending requests, bounded history, prompt lifecycle coordination, concurrency, and error classes (`:200`, `:273`, `:316`, `:334`); `host_tools.py` and `host_uris.py` define decorators/context/result normalization for host extensions.
- inputs_outputs_state: Inputs are JSON-RPC frames, subprocess command, prompt text, host tool/URI callbacks, and timeout/cancel options. Outputs are parsed Python objects, prompt events, tool results, URI reads/writes, and raised RPC errors. State includes pending request maps, pending host calls, prompt lifecycle, subprocess PGID, and bounded history.
- gates_or_invariants: Strict JSON shape cloning, literal/type validation, one prompt lifecycle at a time, timeout/cancel handling, process-group termination, host result normalization, and scheme/tool registration contracts.
- dependencies_and_callers: Used by Python SDK/automation clients connecting to coding-agent RPC mode.
- edge_cases_or_failure_modes: Process exit mid-request, timeout, malformed frame, unknown notification, concurrent prompt command, aborted host call, invalid URI scheme, and host-reported error.
- validation_or_tests: Coding-agent RPC host tool/URI tests validate matching TypeScript side; Python package typing is indicated by `py.typed`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-363 `file` `crates/pi-natives/src/keys.rs`
- cursor: `[_]`
- core_role: Native key sequence parser/matcher for Kitty keyboard protocol, CSI-u, modifyOtherKeys, and legacy terminal sequences.
- algorithmic_behavior: Public NAPI exports include `matches_kitty_sequence`, `parse_key`, `matches_legacy_sequence`, `matches_key`, and `parse_kitty_sequence` (`crates/pi-natives/src/keys.rs:300`, `:382`, `:390`, `:400`, `:408`). Internals parse key IDs, match byte sequences, decode Kitty CSI-u/function keys, normalize keypad/navigation behavior, and format key names/modifiers.
- inputs_outputs_state: Inputs are raw terminal byte strings, requested key IDs, expected codepoint/modifier masks, and Kitty-active flag. Outputs are normalized key IDs, booleans, or structured Kitty parse results. State is stateless except static lookup tables.
- gates_or_invariants: Ignores lock-mask bits, rejects release events for matching, treats legacy ambiguous control bytes as named keys, avoids false base-layout matches for ASCII letters/symbols, and validates numeric fields with checked arithmetic.
- dependencies_and_callers: Used by TUI keyboard input and JS native bindings. Depends on `napi_derive` and `phf`.
- edge_cases_or_failure_modes: ESC-prefixed Alt mixed mode, Dvorak/Colemak base-layout fallback, keypad NumLock/operator remapping, Ctrl-symbol ambiguity, modifyOtherKeys without `~`, malformed CSI sequences, unsupported function keys, and Kitty release events.
- validation_or_tests: Inline Rust tests begin around `crates/pi-natives/src/keys.rs` test module and pin mixed-mode Alt arrows/letters and parsing cases.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-393 `file` `packages/agent/src/telemetry.ts`
- cursor: `[_]`
- core_role: OpenTelemetry instrumentation layer for agent loop, chat calls, tool execution, handoff, usage, cost, and run summaries.
- algorithmic_behavior: Resolves opt-in telemetry (`resolveTelemetry`), starts spans with GenAI attributes, emits request/response/tool content summaries, applies usage and cost estimates, detects LLM gateway headers, records failed chat spans, and bounds/circular-protects serialized content (`packages/agent/src/telemetry.ts:1`, `:52`, `:195`, `:448`, `:622` approximate symbol region from inspection).
- inputs_outputs_state: Inputs are `AgentTelemetryConfig`, session ID, model, agent identity, messages, tools, spans, usage, response headers, and cost hooks. Outputs are OTEL spans/events, `AgentRunCollector` records, warnings, usage/cost callbacks, and run summaries. State includes content capture env cache and per-run collector.
- gates_or_invariants: Disabled telemetry performs no tracer lookup; content capture defaults from `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`; summaries cap message count, array count, object depth/key count, and text chars; telemetry hook failures are swallowed and surfaced as warnings.
- dependencies_and_callers: Used by `agent-loop`, compaction/handoff oneshot calls, and hosts that supply cost/usage callbacks. Depends on `@opentelemetry/api`, `@oh-my-pi/pi-ai`, `AgentRunCollector`, and `EventLoopKeepalive`.
- edge_cases_or_failure_modes: Serializer exceptions, cost estimator exceptions, async usage hook rejection, circular objects, gateway response header absence, non-Error failures, missing usage, and malformed finish reasons.
- validation_or_tests: Indirectly validated through agent loop tests and telemetry consumers; no assigned direct telemetry test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-423 `file` `packages/ai/src/index.ts`
- cursor: `[_]`
- core_role: Public barrel export for `@oh-my-pi/pi-ai`.
- algorithmic_behavior: Re-exports arktype/zod, auth, providers, registry, stream, usage, utility modules, and type surfaces (`packages/ai/src/index.ts:1`-`:48`). It does not implement runtime logic itself.
- inputs_outputs_state: Input is module import specifier; output is aggregate API surface. No runtime state.
- gates_or_invariants: Barrel controls what downstream packages can import from `pi-ai`; catalog values should not be re-exported here except allowed pi-ai types per repo convention.
- dependencies_and_callers: Used by most packages for AI provider types/functions.
- edge_cases_or_failure_modes: Incorrect export can create public API gaps or unwanted dependency graph inflation.
- validation_or_tests: API import tests and package type checks validate this surface.
- skip_candidate: `yes: barrel/API surface only, not an algorithm implementation`

### OH_MY_HUMANIZE_MAIN-HZ-453 `file` `packages/ai/test/api-registry.test.ts`
- cursor: `[_]`
- core_role: Contract test for custom API registry registration/cleanup and stream lookup.
- algorithmic_behavior: Imports API registry helpers and validates that custom API stream implementations can be registered, used, and unregistered (`packages/ai/test/api-registry.test.ts:15`).
- inputs_outputs_state: Inputs are custom API IDs and mock stream functions; outputs are resolved stream behavior or registry absence. State is global registry, reset in `afterEach`.
- gates_or_invariants: Custom API state must be removable between tests; registered implementation must match expected stream type.
- dependencies_and_callers: Tests `@oh-my-pi/pi-ai/api-registry` and event stream types.
- edge_cases_or_failure_modes: Registry leakage across tests and missing/unregistered custom API behavior.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-483 `file` `packages/ai/test/auth-storage-refresh-skew.test.ts`
- cursor: `[_]`
- core_role: OAuth credential refresh-skew regression test.
- algorithmic_behavior: Exercises `AuthStorage`, `SqliteAuthCredentialStore`, and OAuth provider registration to ensure token refresh decisions honor skew windows and persisted credential state (`packages/ai/test/auth-storage-refresh-skew.test.ts:8`).
- inputs_outputs_state: Inputs are temp credential DBs, provider metadata, access/refresh token expiry timestamps, and clock/test setup. Outputs are refreshed or reused credentials. State is SQLite auth storage and OAuth provider registry.
- gates_or_invariants: Refresh should occur before hard expiry by configured skew, persist updated credentials, and clean provider registry after tests.
- dependencies_and_callers: Tests `@oh-my-pi/pi-ai/auth-storage` and `registry/oauth`.
- edge_cases_or_failure_modes: Stale tokens, expired refresh token, skew boundary, persistent store cleanup, and provider registry leakage.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-513 `file` `packages/ai/test/google-antigravity-usage.test.ts`
- cursor: `[_]`
- core_role: Usage-provider and ranking-strategy tests for Google Antigravity/Cloud Code Assist.
- algorithmic_behavior: Builds fake credentials/fetch contexts/API models, tests `antigravityUsageProvider`, parses usage limits, and ranks Antigravity models (`packages/ai/test/google-antigravity-usage.test.ts:72`, `:241`).
- inputs_outputs_state: Inputs are fixture access token, fake usage JSON, model metadata, and fetch context. Outputs are normalized usage limits and ranked model decisions. State is contained in fake fetch calls.
- gates_or_invariants: Usage parsing must tolerate provider payload variants, preserve window/amount/status semantics, and ranking must prefer suitable Antigravity model profiles.
- dependencies_and_callers: Tests `@oh-my-pi/pi-ai/usage/google-antigravity` and catalog wire headers/profiles.
- edge_cases_or_failure_modes: Invalid/missing usage payload fields, unlimited limits, absent token, HTTP errors, and model ranking ties.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-543 `file` `packages/ai/test/issue-814-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for z.ai Anthropic tool-result ID workaround.
- algorithmic_behavior: Builds Anthropic-compatible models and messages, converts them with `convertAnthropicMessages`, and verifies tool_result ID handling differs for z.ai vs standard Anthropic (`packages/ai/test/issue-814-repro.test.ts:83`, `:94`).
- inputs_outputs_state: Inputs are user/assistant/tool result messages and model compat metadata. Output is converted Anthropic payload block. No persistent state.
- gates_or_invariants: z.ai compatibility must not emit unsupported/incorrect tool_result IDs while Anthropic behavior remains intact.
- dependencies_and_callers: Tests `providers/anthropic` conversion and catalog model compat.
- edge_cases_or_failure_modes: Provider-specific protocol divergence around tool result IDs.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-573 `file` `packages/ai/test/ollama-thinking-disable.test.ts`
- cursor: `[_]`
- core_role: Ollama chat request thinking-control regression test.
- algorithmic_behavior: Creates a reasoning-capable Ollama model, intercepts outgoing payload, and verifies disabled thinking is encoded correctly (`packages/ai/test/ollama-thinking-disable.test.ts:29`).
- inputs_outputs_state: Inputs are `Context`, model metadata, and fake fetch. Output is Ollama request payload. No persistent state.
- gates_or_invariants: Reasoning models must support explicit disable without sending unsupported fields or omitting needed options.
- dependencies_and_callers: Tests `streamOllama` and catalog `buildModel`.
- edge_cases_or_failure_modes: Thinking enabled by default when user disables it; malformed chat payload.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-603 `file` `packages/ai/test/openai-responses-transport-error-context.test.ts`
- cursor: `[_]`
- core_role: Transport error context test for OpenAI Responses provider.
- algorithmic_behavior: Builds a Responses model, simulates provider/transport failure, and checks `finalizeErrorMessage` includes useful context (`packages/ai/test/openai-responses-transport-error-context.test.ts:28`).
- inputs_outputs_state: Inputs are model/baseUrl, fake fetch/error response, and minimal context. Output is rejected error message. No state.
- gates_or_invariants: Error text should preserve provider/model/endpoint context without losing original failure detail.
- dependencies_and_callers: Tests `streamOpenAIResponses` and HTTP inspector utilities.
- edge_cases_or_failure_modes: Opaque transport errors and missing diagnostic context.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-633 `file` `packages/ai/test/stream-timeout-defaults.test.ts`
- cursor: `[_]`
- core_role: Timeout default and async iterator timeout behavior tests.
- algorithmic_behavior: Validates idle/first-event timeout env parsing and `iterateWithIdleTimeout` / `iterateWithTerminalGrace` behavior (`packages/ai/test/stream-timeout-defaults.test.ts:47`, `:80`, `:147`, `:262`).
- inputs_outputs_state: Inputs are env var values, fallback durations, async generators, and timing behavior. Outputs are resolved timeout values or thrown timeout errors. State is temporary env overrides restored per test.
- gates_or_invariants: Invalid env values fall back; first-event timeout relates to idle timeout; idle timeout rejects stalled streams; terminal grace handles late final events.
- dependencies_and_callers: Tests stream timeout utilities used by provider streaming.
- edge_cases_or_failure_modes: Env leakage, hanging streams, late terminal chunks, zero/negative/invalid timeout values.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-663 `file` `packages/catalog/src/model-manager.ts`
- cursor: `[_]`
- core_role: Model-source resolver/merger/cache manager for bundled, models.dev, dynamic provider discovery, fallback, and cache strategies.
- algorithmic_behavior: `createModelManager` exposes `resolve`; `resolveProviderModels` loads bundled/cache/remote sources, fetches optional models.dev and dynamic provider models, merges/dedupes, writes cache, and normalizes model records (`packages/catalog/src/model-manager.ts:73`, `:108`, `:198`, `:213`, `:251`, `:327`, `:381`).
- inputs_outputs_state: Inputs are provider ID, static models, refresh strategy, cache TTL, fetch implementations, fallback mappers, dynamic fetcher, and optional retained IDs. Outputs are `ModelResolutionResult` with models and source metadata. State includes model cache and a static fingerprint symbol.
- gates_or_invariants: Offline avoids remote; online-if-uncached uses cache when valid; non-authoritative remote failures observe retry timing; dynamic models are merged with bundled compat; invalid model-like records are rejected/normalized.
- dependencies_and_callers: Used by coding-agent `ModelRegistry`, provider descriptor options, and catalog generation/discovery code.
- edge_cases_or_failure_modes: Stale/invalid cache, remote fetch failure, malformed models.dev payload, duplicate IDs, dynamic records with weaker cost/name/limits, and non-authoritative retry windows.
- validation_or_tests: `packages/catalog/test/issue-847-repro.test.ts` validates Ollama dynamic metadata cache/fallback through this manager path.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-693 `file` `packages/catalog/test/issue-847-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Ollama dynamic context-window discovery.
- algorithmic_behavior: Tests `/api/show` context length use, metadata caching across repeated `fetchDynamicModels`, and 128k fallback when `/api/show` is unavailable (`packages/catalog/test/issue-847-repro.test.ts:10`, `:63`, `:93`).
- inputs_outputs_state: Inputs are fake Ollama `/v1/models`, `/api/tags`, and `/api/show` responses. Outputs are resolved model specs. State is in-memory metadata resolver cache.
- gates_or_invariants: Unbundled cloud models must not lose native context length; successful `/api/show` results cache; failed lookups remain recoverable via fallback.
- dependencies_and_callers: Tests `ollamaModelManagerOptions` and catalog fetch interfaces.
- edge_cases_or_failure_modes: Missing show endpoint, unbundled cloud IDs, repeated refreshes causing excess metadata calls.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-723 `file` `packages/coding-agent/scripts/generate-share-viewer.ts`
- cursor: `[_]`
- core_role: Build script generating a standalone HTML share viewer.
- algorithmic_behavior: Reads output path argument, loads `share-loader.js`, generates dark theme vars, plugs loader/theme into export HTML template, and writes final HTML (`packages/coding-agent/scripts/generate-share-viewer.ts:15`, `:21`, `:23`, `:25`).
- inputs_outputs_state: Input is target output path plus static template/loader assets. Output is generated HTML file. No long-lived state.
- gates_or_invariants: Requires an output path; generated template must embed loader and theme variables.
- dependencies_and_callers: Depends on `../src/export/html` and Bun file/write APIs; called by build/package scripts.
- edge_cases_or_failure_modes: Missing argument, missing loader/template, theme generation failure, and write failure.
- validation_or_tests: No assigned direct test; package build would validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-753 `file` `packages/coding-agent/test/agent-session-auto-compaction-queue.test.ts`
- cursor: `[_]`
- core_role: Regression test for queued runtime signals during auto-compaction resume.
- algorithmic_behavior: Builds an `AgentSession` with extension/runtime signal scaffolding and asserts queued signals survive compaction/resume flow (`packages/coding-agent/test/agent-session-auto-compaction-queue.test.ts:31`).
- inputs_outputs_state: Inputs are temp project, fake agent/model/session manager, extension runtime signals, and compaction triggers. Outputs are persisted/observed runtime signals and session behavior. State includes temp `.omp`/session files and extension runner state.
- gates_or_invariants: Auto-compaction must not drop queued work or resume signals; runtime signal store key is isolated.
- dependencies_and_callers: Tests `AgentSession`, `Agent`, extensions loader/runner, settings, auth, and session manager.
- edge_cases_or_failure_modes: Signal loss during compaction, queue resume ordering, temp project cleanup, and extension state leakage.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-783 `file` `packages/coding-agent/test/agent-session-skill-keywords.test.ts`
- cursor: `[_]`
- core_role: Tests keyword-triggered skill prompt steering in `AgentSession`.
- algorithmic_behavior: Uses fake agent stream/session setup and bundled model to ensure skill references inject workflow notice/developer context when user text matches skill keywords (`packages/coding-agent/test/agent-session-skill-keywords.test.ts:25`).
- inputs_outputs_state: Inputs are user prompts, skill files/metadata, model/session settings, and assistant stream. Outputs are generated messages/context sent to agent. State is temp agent dir/session manager.
- gates_or_invariants: Skill steering should trigger on declared keywords, not unrelated text; workflow notice behavior must remain stable.
- dependencies_and_callers: Tests coding-agent skill discovery/injection through `AgentSession`.
- edge_cases_or_failure_modes: Keyword false positives/negatives, stale skill cache, and context omission.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-813 `file` `packages/coding-agent/test/bash-executor.test.ts`
- cursor: `[_]`
- core_role: Contract suite for non-interactive bash execution, shell reuse, cancellation, minimizer settings, output artifacts, and background process cleanup.
- algorithmic_behavior: Exercises `executeBash` and `buildMinimizerOptions`, uses guarded marker writes and polling to prove process cancellation/cleanup behavior (`packages/coding-agent/test/bash-executor.test.ts:25`, `:34`, `:45`, `:62`).
- inputs_outputs_state: Inputs are shell commands, temp dirs, timeout/cancellation signals, settings, shell snapshot mocks, and minimizer settings. Outputs are command result objects, artifact spill metadata, markers, and process status. State includes temp files and reusable shell sessions.
- gates_or_invariants: Background jobs must be killed, output caps enforced, minimizer options built from settings, shell snapshot behavior honored, and cancellation must prevent survivor writes.
- dependencies_and_callers: Tests `exec/bash-executor`, `session/streaming-output`, native shell API, settings, and shell snapshot utilities.
- edge_cases_or_failure_modes: Background completion races, kill settle timing, process survivors, shell quoting, large output, and platform shell differences.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-843 `file` `packages/coding-agent/test/edit-auto-generated-regressions.test.ts`
- cursor: `[_]`
- core_role: Regression tests for auto-generated-file edit guard behavior and agent-loop error propagation.
- algorithmic_behavior: Builds mock edit tools/sessions and streams tool calls to ensure auto-generated edit aborts fire, multi-entry errors surface as `isError`, and explicit tool errors propagate to model wire messages (`packages/coding-agent/test/edit-auto-generated-regressions.test.ts:193`, `:235`, `:314`).
- inputs_outputs_state: Inputs are fake tool calls, temp files, auto-generated guard stubs, and assistant streams. Outputs are tool results, assistant messages, and surfaced errors. State is temp filesystem and session message history.
- gates_or_invariants: Guard errors must not be faked as success; disabling edit streaming abort must not disable auto-generated protection; tool `isError` must survive agent-loop conversion.
- dependencies_and_callers: Tests `AgentSession`, `Agent`, `EditTool`, auto-generated guard, and tool error handling.
- edge_cases_or_failure_modes: Multi-entry edit partial failure, guard rejection, explicit `ToolError`, and streaming tool-call timing.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-873 `file` `packages/coding-agent/test/hindsight-mental-models.test.ts`
- cursor: `[_]`
- core_role: Tests Hindsight mental-model seed resolution, ensure/load/render/diff behavior.
- algorithmic_behavior: Covers `resolveSeedsForScope`, fake API calls for `ensureMentalModels`, block rendering/loading, and content diffing (`packages/coding-agent/test/hindsight-mental-models.test.ts:29`, `:97`, `:202`, `:263`, `:303`).
- inputs_outputs_state: Inputs are bank scope, existing summaries, fake Hindsight API, and rendered markdown blocks. Outputs are seed lists, ensured models, rendered blocks, parsed blocks, and diffs. State is fake API call log.
- gates_or_invariants: Seeds must match scope, existing models should not duplicate, rendering/loading round-trips semantic content, and diffs identify changed/added/removed mental models.
- dependencies_and_callers: Tests coding-agent hindsight memory integration.
- edge_cases_or_failure_modes: Empty scope, existing remote summaries, malformed blocks, and diff normalization.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-903 `file` `packages/coding-agent/test/interactive-mode-plan-review.test.ts`
- cursor: `[_]`
- core_role: High-level interactive-mode tests for plan review rendering, approval calls, abort handling, and token display.
- algorithmic_behavior: Creates `InteractiveMode`, `AgentSession`, fake messages/usages, plan review overlay hooks, and verifies UI/control flow around plan review (`packages/coding-agent/test/interactive-mode-plan-review.test.ts:63`).
- inputs_outputs_state: Inputs are temp session, keybindings, fake agent/model, plan review state, usage values, and user actions. Outputs are rendered components, approved calls, session messages, and state changes. State includes TUI mode state and session manager data.
- gates_or_invariants: Plan review must render token counts compactly, approved calls are recognized, abort labels preserved, and overlay interactions must not corrupt session flow.
- dependencies_and_callers: Tests `InteractiveMode`, `AgentSession`, `AssistantMessageComponent`, plan review overlay, keybindings, theme, and internal URLs.
- edge_cases_or_failure_modes: Agent busy state, user interrupt/silent abort, local URL path resolution, usage formatting, and theme/keybinding initialization.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-933 `file` `packages/coding-agent/test/issue-970-custom-provider-discovery.test.ts`
- cursor: `[_]`
- core_role: Regression tests for custom provider discovery display in model selector.
- algorithmic_behavior: Builds selector with fake `ProviderDiscoveryState`, temp cache/auth/settings, and asserts rendered model discovery state after normalization (`packages/coding-agent/test/issue-970-custom-provider-discovery.test.ts:30`, `:59`).
- inputs_outputs_state: Inputs are provider discovery state, cached models, settings, auth storage, and theme. Output is rendered selector text. State includes temp config/cache and model registry.
- gates_or_invariants: Custom provider discovery must appear with correct state, provider IDs, and model data; VT control chars are stripped for assertions.
- dependencies_and_callers: Tests `ModelSelectorComponent`, `ModelRegistry`, catalog cache, settings, auth storage, and theme.
- edge_cases_or_failure_modes: Discovery state missing/collapsed, custom provider cache mismatch, rendering ANSI noise, and temp home cleanup.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-963 `file` `packages/coding-agent/test/mcp-profile-auth-binding.test.ts`
- cursor: `[_]`
- core_role: Tests per-profile MCP OAuth credential binding and cleanup.
- algorithmic_behavior: Uses SQLite auth store and MCP manager/flow helpers to ensure server auth headers bind to active profile and can be removed (`packages/coding-agent/test/mcp-profile-auth-binding.test.ts:29`).
- inputs_outputs_state: Inputs are MCP server config, active profile, stored OAuth credential, and mocked OAuth flow. Outputs are server authorization headers and credential removal effects. State is SQLite credential DB and profile setting.
- gates_or_invariants: Credentials should be scoped by profile, URL credential IDs should be stable, and managed credential removal must not affect unrelated profiles.
- dependencies_and_callers: Tests `MCPManager`, `mcpOAuthCredentialId`, `removeManagedMcpOAuthCredential`, and profile dirs.
- edge_cases_or_failure_modes: Profile leakage, stale bearer token, credential missing, and cleanup after test.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-993 `file` `packages/coding-agent/test/oauth-manual-input.test.ts`
- cursor: `[_]`
- core_role: Unit tests for OAuth manual input manager.
- algorithmic_behavior: Exercises `OAuthManualInputManager` prompt/input state transitions (`packages/coding-agent/test/oauth-manual-input.test.ts:4`).
- inputs_outputs_state: Inputs are manual auth values/user responses. Outputs are resolved/rejected input promises or state changes. State is manager-held pending input.
- gates_or_invariants: Manual input should resolve exactly once, preserve prompt state, and handle cancellation/error.
- dependencies_and_callers: Tests coding-agent OAuth manual input mode.
- edge_cases_or_failure_modes: Duplicate input, cancel before input, and stale pending state.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1023 `file` `packages/coding-agent/test/rpc-host-tools.test.ts`
- cursor: `[_]`
- core_role: Tests RPC host custom tool bridge and client-side custom tool serving.
- algorithmic_behavior: Verifies host tool updates/results are forwarded, abort emits cancel frames, and RPC client registers host tools and serves tool calls over transport (`packages/coding-agent/test/rpc-host-tools.test.ts:26`, `:83`, `:117`).
- inputs_outputs_state: Inputs are fake RPC frames, host tool descriptors, tool calls, and abort signals. Outputs are tool results, updates, cancel frames, and agent events. State includes pending host tool calls and transport buffer.
- gates_or_invariants: Each tool call must correlate by ID, cancellation must notify host, result normalization must match `AgentToolResult`, and custom tools must register with schema/name metadata.
- dependencies_and_callers: Tests `RpcClient`, `defineRpcClientTool`, `RpcHostToolBridge`, and RPC protocol types.
- edge_cases_or_failure_modes: Aborted execution, missing pending call, malformed frame, and host result/error propagation.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1053 `file` `packages/coding-agent/test/session-messages.test.ts`
- cursor: `[_]`
- core_role: Tests session message conversion and steering wrapping for model/provider protocols.
- algorithmic_behavior: Validates compaction summary conversion, custom message mapping, Copilot initiator attribution, and `wrapSteeringForModel` behavior (`packages/coding-agent/test/session-messages.test.ts:16`, `:57`, `:175`).
- inputs_outputs_state: Inputs are `AgentMessage` variants, image/text/tool content, and model/provider metadata. Outputs are LLM `Message[]` and wrapped steering content. No persistent state.
- gates_or_invariants: Compaction summaries map to appropriate model roles/content, custom messages are preserved or transformed, and steering must fit provider attribution expectations.
- dependencies_and_callers: Tests `session/messages`, `inferCopilotInitiator`, and pi-ai message types.
- edge_cases_or_failure_modes: Orphan/custom messages, mixed text/image content, Copilot attribution, and provider-specific steering wrapping.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1083 `file` `packages/coding-agent/test/streaming-edit-abort.test.ts`
- cursor: `[_]`
- core_role: Tests streaming edit abort behavior for auto-generated guard and internal URL path resolution.
- algorithmic_behavior: Builds random chunked assistant streams with edit tool calls, checks abort timing, non-ToolError ENOENT tolerance, ToolError abort, local URL resolution, and path-available early abort (`packages/coding-agent/test/streaming-edit-abort.test.ts:231`, `:261`, `:291`, `:321`, `:351`, `:400`).
- inputs_outputs_state: Inputs are streamed tool-call argument deltas, temp files, auto-generated guard mocks, and session setup. Outputs are assistant/tool result messages and abort state. State includes streamed content buffers and temp filesystem.
- gates_or_invariants: Auto-generated checks should abort as soon as path is knowable, ignore benign peek ENOENT, propagate guard `ToolError`, and resolve `local://` safely.
- dependencies_and_callers: Tests `AgentSession`, `Agent`, tool schemas, auto-generated guard, and internal URL handling.
- edge_cases_or_failure_modes: Random chunk boundaries, partial JSON tool args, path discovered before full args, internal-scheme panic, and guard race.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1113 `file` `packages/coding-agent/test/transcript-streaming-commit-repro.test.ts`
- cursor: `[_]`
- core_role: Minimal UI regression for transcript assistant streaming commit.
- algorithmic_behavior: Uses `TranscriptContainer` with fake components to assert assistant text commits after streaming (`packages/coding-agent/test/transcript-streaming-commit-repro.test.ts:21`).
- inputs_outputs_state: Inputs are component updates/assistant text chunks. Outputs are rendered transcript state. State is component tree state in memory.
- gates_or_invariants: Streaming assistant text must not disappear or duplicate on commit.
- dependencies_and_callers: Tests transcript container rendering path in coding-agent TUI.
- edge_cases_or_failure_modes: Final commit after deltas and component lifecycle ordering.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1143 `file` `packages/hashline/src/apply.ts`
- cursor: `[_]`
- core_role: Hashline edit applier and repair engine for line-anchored insert/delete/replacement edits.
- algorithmic_behavior: Validates line bounds, drops phantom trailing-line deletes, groups same-anchor edits, detects JSX/structural delimiters, computes delimiter balance, repairs duplicate prefix/suffix/boundary echo, resolves shifted/inward insert landings, and applies edits (`packages/hashline/src/apply.ts:25`, `:57`, `:99`, `:243`, `:595`, `:764`, `:838`, `:897`).
- inputs_outputs_state: Inputs are original text and parsed `Edit[]`. Outputs are `ApplyResult` with changed text, warnings/diagnostics, and applied edits. State is local arrays of file lines, line origins, replacement groups, and warnings.
- gates_or_invariants: Line refs must be in range; replacements are paired delete+insert groups; delimiter-balance repairs must preserve structure; phantom deletes only apply to trailing empty line; warnings mark shifted landings.
- dependencies_and_callers: Used by hashline patcher/edit tooling. Depends on messages, tokenizer cursor clone, and hashline types.
- edge_cases_or_failure_modes: JSX fragments/named closers, duplicated boundary lines, dropped suffix closers, one-sided echo, indentation landing shifts, replacement of EOF phantom line, and overlapping edits.
- validation_or_tests: Hashline parser/apply test suite outside assigned list likely covers; coding-agent edit regression tests exercise downstream behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1173 `file` `packages/mnemopi/src/db.ts`
- cursor: `[_]`
- core_role: SQLite database open/pragma/extension/transaction utilities for Mnemopi.
- algorithmic_behavior: Opens database with directory creation, enables WAL/foreign key/busy timeout pragmas, loads SQLite extensions, provides nested sync/async transaction helpers with rollback/commit state, and closes quietly (`packages/mnemopi/src/db.ts:25`, `:37`, `:43`, `:53`, `:88`, `:121`).
- inputs_outputs_state: Inputs are DB path or `:memory:`, pragma options, extension paths, and transaction callbacks. Outputs are `Database`, callback result, or rollback/close effects. State is a symbol-tagged transaction depth/rollback flag on the DB object.
- gates_or_invariants: Directory creation skipped for `:memory:`, nested transactions share state, rollback propagates when inner transaction fails, and async transaction finalization awaits callback.
- dependencies_and_callers: Used by Mnemopi core storage/recovery/cost logging.
- edge_cases_or_failure_modes: Extension load failure, callback throw, nested rollback, async rejection, close errors swallowed, and in-memory database path.
- validation_or_tests: `packages/mnemopi/test/recovery.test.ts` and Mnemopi integration tests use DB behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1203 `file` `packages/mnemopi/test/embeddings-multilingual.test.ts`
- cursor: `[_]`
- core_role: Tests multilingual embedding metadata and ordering.
- algorithmic_behavior: Temporarily sets env values, tests embedding metadata/language handling and ordering behavior (`packages/mnemopi/test/embeddings-multilingual.test.ts:55`, `:124`).
- inputs_outputs_state: Inputs are env overrides, multilingual text/query fixtures, and embedding functions. Outputs are metadata and ranked results. State is temporary env restored by helper.
- gates_or_invariants: Multilingual metadata must preserve language/script semantics and ranking should not collapse non-English inputs incorrectly.
- dependencies_and_callers: Tests Mnemopi embeddings setup and search ordering.
- edge_cases_or_failure_modes: Env leakage, mixed-language strings, missing embedding provider, and ordering ties.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1233 `file` `packages/mnemopi/test/recovery.test.ts`
- cursor: `[_]`
- core_role: SQLite disaster-recovery helper tests.
- algorithmic_behavior: Creates valid/corrupt SQLite backups, freezes time, and tests `createBackup`, `restoreBackup`, `emergencyRestore`, and `verifyIntegrity` (`packages/mnemopi/test/recovery.test.ts:75`).
- inputs_outputs_state: Inputs are temp SQLite DBs, gzip/corrupt backup files, and frozen timestamps. Outputs are backup files, restored DBs, integrity reports. State is temp dirs and SQLite files.
- gates_or_invariants: Backups must be gzip-compatible, restored DB must pass SQLite header/integrity checks, corrupt backups must fail safely, and timestamps are deterministic.
- dependencies_and_callers: Tests `@oh-my-pi/pi-mnemopi/dr/recovery`.
- edge_cases_or_failure_modes: Corrupt gzip/SQLite file, missing paths, emergency restore path choice, and cleanup after tests.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1263 `file` `packages/snapcompact/research/bench_gemini.py`
- cursor: `[_]`
- core_role: Research benchmark runner for Gemini image/text QA against Snapcompact renderings.
- algorithmic_behavior: `_post` sends JSON with retries; `gemini_complete` builds Gemini request blocks/resolution/max tokens; `main` orchestrates benchmark execution (`packages/snapcompact/research/bench_gemini.py:39`, `:67`, `:106`).
- inputs_outputs_state: Inputs are API key, prompt/image blocks, resolution, max tokens, and benchmark data. Outputs are Gemini JSON responses and benchmark records. State is local run data/cache if main writes outputs.
- gates_or_invariants: Retries are bounded; HTTP errors should be surfaced; request body must match Gemini API content format.
- dependencies_and_callers: Depends on Python HTTP/json utilities and Snapcompact research prompt/image generation.
- edge_cases_or_failure_modes: Rate limits, transient HTTP errors, malformed response JSON, missing API key, and oversized image/prompt.
- validation_or_tests: Research script, not product test; validation is manual/benchmark output.
- skip_candidate: `yes: research benchmark script, not production runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1293 `file` `packages/snapcompact/research/exp21_braille.py`
- cursor: `[_]`
- core_role: Snapcompact research experiment encoding text into Braille-cell image carriers and evaluating QA recovery.
- algorithmic_behavior: Converts text to Braille cells, renders images, atomically saves PNGs, caches model calls, runs QA units, aggregates results, and orchestrates experiment (`packages/snapcompact/research/exp21_braille.py:71`, `:91`, `:114`, `:120`, `:135`, `:161`, `:187`).
- inputs_outputs_state: Inputs are source text/questions, prompt, PNG paths, cache payload, freshness flag, and context. Outputs are Braille images, cached responses, per-question records, aggregate scores. State is filesystem cache/images.
- gates_or_invariants: Atomic save avoids partial PNGs; cache keyed by payload; aggregation preserves per-condition metrics.
- dependencies_and_callers: Uses PIL/image tooling and research provider helpers/prompts under `packages/snapcompact/research`.
- edge_cases_or_failure_modes: Unsupported characters, image rendering font/cell mismatch, stale cache, API failure, and aggregation over empty records.
- validation_or_tests: Research experiment output, not automated product test.
- skip_candidate: `yes: experimental research artifact`

### OH_MY_HUMANIZE_MAIN-HZ-1323 `file` `packages/snapcompact/research/snapcompact_r2_hero.py`
- cursor: `[_]`
- core_role: Research visualization generator for Snapcompact R2 hero graphic.
- algorithmic_behavior: Loads experiment data, resolves fonts, draws tracked text, Bezier curves, additive base, head bars, left/right panels, title/core/stat strip, rounded panels, and saves final visualization (`packages/snapcompact/research/snapcompact_r2_hero.py:53`, `:133`, `:192`, `:279`, `:335`, `:401`, `:466`).
- inputs_outputs_state: Inputs are data files, fonts, rendered carrier image, counts/heads/stats. Output is a composed PIL image. State is local image arrays and draw overlays.
- gates_or_invariants: Font fallback required, coordinate scaling via `u()`, panel layout dimensions fixed, and data load must provide expected answer/context/count/head structures.
- dependencies_and_callers: Depends on PIL, numpy, local research artifacts.
- edge_cases_or_failure_modes: Missing fonts/data/carrier, dimension overflow, unreadable image, and invalid stats shape.
- validation_or_tests: Manual visual inspection/research artifact.
- skip_candidate: `yes: visualization research script`

### OH_MY_HUMANIZE_MAIN-HZ-1353 `file` `packages/stats/src/types.ts`
- cursor: `[_]`
- core_role: Shared stats dashboard/session data type contract.
- algorithmic_behavior: Defines `MessageStats`, `RequestDetails`, session header/entry types, user message stats, and links (`packages/stats/src/types.ts:8`, `:40`, `:50`, `:59`, `:80`, `:120`).
- inputs_outputs_state: Inputs/outputs are TypeScript data shapes exchanged by stats collectors/client. No runtime state.
- gates_or_invariants: Consumers rely on stable field names for usage, service tier, stop reason, and session/message metadata.
- dependencies_and_callers: Imports pi-ai message/usage types and re-exports shared types for stats client/server.
- edge_cases_or_failure_modes: Type drift can break dashboard rendering or request drawer assumptions.
- validation_or_tests: Type checking and stats UI tests validate indirectly.
- skip_candidate: `yes: type contract only, no algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-1383 `file` `packages/tui/src/symbols.ts`
- cursor: `[_]`
- core_role: TUI symbol theme type definitions.
- algorithmic_behavior: Declares `BoxSymbols` and `SymbolTheme` interfaces for border/icons/glyph sets (`packages/tui/src/symbols.ts:1`, `:15`).
- inputs_outputs_state: Inputs/outputs are compile-time shape contracts. No runtime state.
- gates_or_invariants: Theme implementations must satisfy required symbol fields.
- dependencies_and_callers: Re-exported by TUI index and consumed by theme/render components.
- edge_cases_or_failure_modes: Missing symbol fields cause type errors or fallback gaps.
- validation_or_tests: Type checking validates.
- skip_candidate: `yes: type definitions only`

### OH_MY_HUMANIZE_MAIN-HZ-1413 `file` `packages/tui/test/issue-848-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for `truncateToWidth` native wrapper nullish input handling.
- algorithmic_behavior: Exercises `truncateToWidth` and `Ellipsis` behavior around nullish/invalid NAPI inputs (`packages/tui/test/issue-848-repro.test.ts:22`).
- inputs_outputs_state: Inputs are strings/width/ellipsis options. Outputs are truncated strings or safe behavior. No state.
- gates_or_invariants: Wrapper must not pass nullish values into native code in a way that crashes.
- dependencies_and_callers: Tests TUI string-width/truncation utilities used by renderers.
- edge_cases_or_failure_modes: Null/undefined wrapper arguments, zero width, and ellipsis fitting.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1443 `file` `packages/tui/test/render-stress.test.ts`
- cursor: `[_]`
- core_role: Subprocess stress test harness for TUI rendering scenarios.
- algorithmic_behavior: Computes worker concurrency/timeouts, spawns render-stress subprocesses, tracks live subprocesses, parses IPC scenario results, and surfaces failure errors (`packages/tui/test/render-stress.test.ts:61`, `:70`, `:105`, `:140`, `:187`).
- inputs_outputs_state: Inputs are scenario lists and env-configured worker counts/timeouts. Outputs are pass/failure results. State includes live subprocess set and IPC counter.
- gates_or_invariants: CI skip flag, bounded subprocess timeouts, cleanup on exit, scenario result validation, and subprocess overhead allowance.
- dependencies_and_callers: Depends on Bun subprocess/IPC and `render-stress-subprocess.ts`.
- edge_cases_or_failure_modes: Hung subprocess, malformed IPC payload, worker timeout, cleanup race, and CI resource constraints.
- validation_or_tests: This file is the stress validation harness.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1473 `file` `packages/typescript-edit-benchmark/src/mutations.ts`
- cursor: `[_]`
- core_role: Mutation engine for TypeScript edit benchmark generation.
- algorithmic_behavior: Parses TS/JS with Babel plugins, discovers AST candidates, applies source edits, and defines mutation classes for operator swaps, literal flips, optional-chain removal, arg swaps, regex quantifier changes, Unicode hyphen, identifier multi-edit, duplicate-line edits, if/else swaps, early return removal, import swaps, statement deletion, and off-by-one changes (`packages/typescript-edit-benchmark/src/mutations.ts:41`, `:80`, `:195`, `:281`, `:588`, `:690`, `:1389`).
- inputs_outputs_state: Inputs are source code, RNG, parser plugins, and mutation selection. Outputs are mutated content plus `MutationInfo`. State is candidate lists and source edit arrays per mutation.
- gates_or_invariants: Parser failures return null; source edits must be sorted/applied without overlap; mutations must preserve syntactic plausibility enough for benchmark; random selection is deterministic given RNG.
- dependencies_and_callers: Depends on Babel parser/traverse/generator/types and regexp-tree AST types.
- edge_cases_or_failure_modes: Unsupported syntax, missing node ranges, overlapping edits, generated invalid code, duplicate identifiers, and regex AST mismatch.
- validation_or_tests: Benchmark suite/type checks; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1503 `file` `packages/utils/src/prompt.ts`
- cursor: `[_]`
- core_role: Prompt formatting and Handlebars rendering utility.
- algorithmic_behavior: Formats prompt markdown/XML-ish text, normalizes RFC2119 emphasis, compacts tables, replaces ASCII symbols outside HTML comments, registers helpers/partials, disambiguates closing braces, compiles cached templates, and renders contexts (`packages/utils/src/prompt.ts:79`, `:89`, `:100`, `:147`, `:191`, `:520`, `:546`, `:558`).
- inputs_outputs_state: Inputs are prompt strings, format options, Handlebars templates, helpers/partials, and template context. Outputs are formatted or rendered strings. State includes Handlebars instance and compiled template cache.
- gates_or_invariants: Avoid formatting inside HTML comments, protect Handlebars closing braces, cache compiled templates by source, and preserve prompt semantics while applying typographic normalization.
- dependencies_and_callers: Used by agent/coding-agent prompt rendering, compaction prompts, guided goals, and docs-generated prompts.
- edge_cases_or_failure_modes: HTML comment spans across lines, Markdown tables, RFC2119 words already bolded, ambiguous `}}`, helper exceptions, and undefined render values.
- validation_or_tests: Prompt behavior covered indirectly by prompt-consuming tests; runtime-install tests cover separate utils area.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1533 `file` `packages/utils/test/runtime-install.test.ts`
- cursor: `[_]`
- core_role: Tests runtime module resolver and install manifest behavior.
- algorithmic_behavior: Builds temp `node_modules`, validates bare specifier splitting, conditional export resolution, runtime module resolver patching, and manifest writing (`packages/utils/test/runtime-install.test.ts:44`, `:59`, `:149`, `:177`).
- inputs_outputs_state: Inputs are fake package manifests/files, runtime node_modules path, stubs, and module specifiers. Outputs are resolved paths, installed resolver behavior, and manifest files. State is temp dirs and patched module resolver registry.
- gates_or_invariants: Resolver must respect exports/main/file extensions, package subpaths, runtime path containment, stubs, and cleanup after tests.
- dependencies_and_callers: Tests `packages/utils/src/runtime-install.ts`.
- edge_cases_or_failure_modes: Conditional exports, missing files, scoped packages, path traversal, resolver leakage, and manifest write errors.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1563 `file` `python/robomp/src/persona.py`
- cursor: `[_]`
- core_role: Prompt/persona rendering layer for RoboMP GitHub issue/PR automation.
- algorithmic_behavior: Implements template lookup/rendering, TOML config loading/validation, phase seeding, host tool description lookup, next-step classification, system/kickoff/resume/completion/dirty-state prompts, thread rendering, followup directives/comments/reviews, and canned final replies (`python/robomp/src/persona.py:25`, `:69`, `:120`, `:131`, `:233`, `:277`, `:302`, `:329`).
- inputs_outputs_state: Inputs are repo/issue/PR/workspace dataclasses, bot login, templates, task kind, thread messages, and inbound comments/reviews. Outputs are rendered prompt/comment strings and seed phase lists. State is template/config files loaded from package resources.
- gates_or_invariants: Template variables must resolve through `_lookup`; required mappings/strings are validated; task kind controls seed phases; directive rendering preserves origin/inbound scope.
- dependencies_and_callers: Used by Python automation around GitHub issue/PR tasks; depends on local templates/TOML and `RepoInfo`, `IssueInfo`, `PullRequestInfo`, `Workspace`.
- edge_cases_or_failure_modes: Missing template key, bad TOML shape, unknown host tool/parameter, empty required strings, thread messages with unsupported shape, and ambiguous next-step classification.
- validation_or_tests: `python/robomp/tests/test_tasks_directive.py` covers task directive rendering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1593 `file` `python/robomp/tests/test_tasks_directive.py`
- cursor: `[_]`
- core_role: Tests RoboMP task directive/persona output.
- algorithmic_behavior: Builds fixture repo/issue/workspace/task inputs and asserts generated directive text includes required task instructions and context.
- inputs_outputs_state: Inputs are fixture dataclasses and task directive inputs. Outputs are rendered strings. No persistent state.
- gates_or_invariants: Directive must include task content, source metadata, and expected instruction framing.
- dependencies_and_callers: Tests `python/robomp/src/persona.py`.
- edge_cases_or_failure_modes: Missing task context, wrong PR/issue scope, and template regression.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1623 `directory` `packages/coding-agent/src/extensibility/custom-tools`
- cursor: `[_]`
- core_role: Custom tool discovery/loading/adaptation API for extensions and user-provided tool modules.
- algorithmic_behavior: `loader.ts` loads tool factories, discovers configured/project paths, reports load errors, and returns loaded tools (`packages/coding-agent/src/extensibility/custom-tools/loader.ts:27`, `:87`, `:170`, `:205`, `:255`); `wrapper.ts` adapts custom tool API to `AgentTool`; `types.ts` defines context, UI, pending actions, result, factory, and error contracts.
- inputs_outputs_state: Inputs are configured paths, cwd, module exports, custom tool context, args, session events, and approval/UI APIs. Outputs are loaded tool descriptors, adapted `AgentTool`s, tool results, render components, and load errors. State is loader path registry and per-tool context.
- gates_or_invariants: Tool path source is tracked, tool factories must return valid shape, load errors are captured rather than crashing discovery, and wrapper normalizes custom result/render behavior.
- dependencies_and_callers: Used by extension loading and agent tool registration. Depends on hook UI context, exec types, and agent-core tool types.
- edge_cases_or_failure_modes: Missing module, invalid export, duplicate tool names, path resolution ambiguity, factory throw, and render/result mismatch.
- validation_or_tests: Custom tool behavior is covered through RPC host custom tool tests and extension/plugin tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1653 `directory` `packages/collab-web/src/tool-render/tools`
- cursor: `[_]`
- core_role: Web collaboration tool-call/result renderer registry, one renderer per tool family.
- algorithmic_behavior: Each `.tsx` file exposes `Summary`/`Body` logic and a renderer constant for tools including bash, read, edit, eval, github, todo, job, memory, search, browser, resolve, report-tool-issue, and more. Renderers parse args/details, compute concise status/meta, and display result-specific panels (`bash.tsx:33`, `edit.tsx:94`, `eval.tsx:242`, `github.tsx:86`, `todo.tsx:33`, `job.tsx:157`).
- inputs_outputs_state: Inputs are tool name, call args, result content/details/error state, and render props. Outputs are React nodes. State is local component computation only.
- gates_or_invariants: Renderers tolerate unknown/missing detail fields, avoid throwing on malformed tool payloads, summarize large/structured results, and map statuses to visual tones/icons.
- dependencies_and_callers: Used by collab web session viewer/live sharing UI. Depends on shared tool-render types and React components.
- edge_cases_or_failure_modes: Malformed JSON-ish details, absent result, truncation artifact notices, terminal IDs, diff stats, mixed eval cells, GitHub run/job failure states, and memory result parsing.
- validation_or_tests: Web renderer tests exist for search render on coding-agent side; collab-web renderers likely covered by UI/build tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1683 `file` `packages/agent/src/compaction/utils.ts`
- cursor: `[_]`
- core_role: Shared compaction/branch summarization utilities for file-operation tracking and conversation serialization.
- algorithmic_behavior: Creates file-op sets, splits/strips read selectors, filters URL-scheme paths, extracts read/write/edit tool calls from assistant messages, computes grouped file lists, formats/upserts `<files>` summaries, and serializes messages for summarization (`packages/agent/src/compaction/utils.ts:22`, `:44`, `:83`, `:112`, `:149`, `:171`).
- inputs_outputs_state: Inputs are agent messages, tool-call args, summaries, file lists, and dialect. Outputs are file operation sets, formatted prompt sections, and serialized conversation text. State is caller-owned `FileOperations`.
- gates_or_invariants: Selector grammar mirrors read tool; internal URLs are excluded from file summaries; modified files override read-only status; summary file list is capped; legacy tags are stripped.
- dependencies_and_callers: Used by compaction and branch summarization. Depends on pi-ai dialect rendering and `file-operations.md` prompt.
- edge_cases_or_failure_modes: Compound selectors (`path:1-50:raw`), `scheme://` paths, legacy `<read-files>` tags, too many files, non-assistant/custom messages, and missing tool args.
- validation_or_tests: Compaction/session tests indirectly validate; no assigned direct unit test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1713 `file` `packages/ai/src/dialect/kimi.ts`
- cursor: `[_]`
- core_role: Kimi in-band tool-call dialect scanner and transcript renderer.
- algorithmic_behavior: `KimiInbandScanner` parses Kimi tool-call section tokens and `<think>` blocks using states `outside`, `section`, `header`, `args`, `thinking`; renderers format tool calls/results/thinking/transcripts with Kimi turn markers (`packages/ai/src/dialect/kimi.ts:15`, `:33`, `:35`, `:261`, `:275`, `:292`, `:329`).
- inputs_outputs_state: Inputs are streamed text chunks, messages, tool calls/results, and dialect render options. Outputs are parsed tool calls/thinking/text deltas and rendered transcript strings. Scanner state tracks current section/header/args/thinking buffers.
- gates_or_invariants: Tool-call tokens must be recognized exactly; JSON arguments use repair parsing; function names normalized; partial suffix overlap avoids premature token emission.
- dependencies_and_callers: Used by Kimi provider/shim and generic dialect infrastructure. Depends on `kimi.md`, coercion/rendering helpers, and pi-ai message types.
- edge_cases_or_failure_modes: Partial token boundaries, malformed JSON arguments, nested/unterminated think blocks, duplicate call IDs, and mixed plain text with in-band calls.
- validation_or_tests: Kimi/provider dialect tests likely cover; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1743 `file` `packages/ai/src/providers/kimi.ts`
- cursor: `[_]`
- core_role: Provider adapter for Kimi coding endpoints.
- algorithmic_behavior: `streamKimi` selects Anthropic-compatible base URL defaults and delegates to OpenAI/Anthropic shim; `isKimiModel` detects Kimi model/provider identity (`packages/ai/src/providers/kimi.ts:35`, `:50`).
- inputs_outputs_state: Inputs are Kimi model, context, options/API key/base URL. Output is `AssistantMessageEventStream`. No persistent state.
- gates_or_invariants: Kimi common headers are applied; Kimi Anthropic base URL is used for shim; model detection prevents incorrect adapter use.
- dependencies_and_callers: Depends on `registry/oauth/kimi` headers and OpenAI-Anthropic shim provider.
- edge_cases_or_failure_modes: Wrong base URL, missing Kimi headers, non-Kimi model routed here.
- validation_or_tests: Provider integration/dialect tests; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1773 `file` `packages/ai/src/registry/cursor.ts`
- cursor: `[_]`
- core_role: Cursor provider registry definition.
- algorithmic_behavior: Exports `cursorProvider` with provider metadata/login callbacks type wiring (`packages/ai/src/registry/cursor.ts:4`).
- inputs_outputs_state: Inputs are OAuth credentials/login callbacks via registry. Outputs are provider definition. No state in file.
- gates_or_invariants: Provider definition shape must match registry contract.
- dependencies_and_callers: Used by OAuth/provider registry.
- edge_cases_or_failure_modes: Incorrect provider ID or missing login metadata breaks Cursor auth discovery.
- validation_or_tests: Registry tests validate provider registration surfaces.
- skip_candidate: `yes: provider metadata surface only`

### OH_MY_HUMANIZE_MAIN-HZ-1803 `file` `packages/ai/src/registry/openai.ts`
- cursor: `[_]`
- core_role: OpenAI provider registry definition.
- algorithmic_behavior: Exports `openaiProvider` with provider metadata (`packages/ai/src/registry/openai.ts:3`).
- inputs_outputs_state: Input is registry import; output is provider definition. No runtime state.
- gates_or_invariants: Provider ID/definition must match registry expectations.
- dependencies_and_callers: Used by pi-ai registry.
- edge_cases_or_failure_modes: Metadata drift could break OpenAI provider discovery/auth display.
- validation_or_tests: API/registry tests.
- skip_candidate: `yes: provider metadata surface only`

### OH_MY_HUMANIZE_MAIN-HZ-1833 `file` `packages/ai/src/usage/github-copilot.ts`
- cursor: `[_]`
- core_role: GitHub Copilot quota/usage provider.
- algorithmic_behavior: Resolves GitHub API base URL, builds usage windows/amounts/status, parses quota detail, fetches internal and billing usage JSON, normalizes quota snapshots and billing items into `UsageLimit[]`, and exports `githubCopilotUsageProvider` (`packages/ai/src/usage/github-copilot.ts:60`, `:74`, `:103`, `:111`, `:141`, `:172`, `:245`, `:267`, `:318`).
- inputs_outputs_state: Inputs are credential/access token, enterprise API endpoint/domain, fetch context, and GitHub responses. Outputs are normalized usage limits. No persistent state except remote API calls.
- gates_or_invariants: Uses Copilot/OpenCode headers, public vs enterprise URL handling, numeric/boolean coercion, and status derivation from amount/unlimited flags.
- dependencies_and_callers: Depends on catalog Copilot wire helpers and usage framework types.
- edge_cases_or_failure_modes: Enterprise domain/API mismatch, missing username, malformed quota details, unlimited quota, HTTP errors, missing reset date, and billing endpoint differences.
- validation_or_tests: Usage provider tests likely in ai package; no assigned direct Copilot test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1863 `file` `packages/ai/src/utils/tool-choice.ts`
- cursor: `[_]`
- core_role: Provider-specific tool-choice mapper.
- algorithmic_behavior: Extracts forced function names and maps generic `ToolChoice` to OpenAI Completions, OpenAI Responses, and Anthropic formats; detects forced choices (`packages/ai/src/utils/tool-choice.ts:29`, `:46`, `:64`, `:74`, `:90`).
- inputs_outputs_state: Input is generic `ToolChoice` (`auto`, `none`, required/specific shapes). Output is provider-specific choice object/string/undefined. No state.
- gates_or_invariants: Specific tool names must be preserved; unsupported/undefined choices map to provider-safe defaults.
- dependencies_and_callers: Used by provider request builders in pi-ai and coding-agent tool-choice wrappers.
- edge_cases_or_failure_modes: Unknown object shape, forced choice without name, provider mismatch, and `none` vs `auto` semantics.
- validation_or_tests: Tool-choice queue/session tests and provider tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1893 `file` `packages/catalog/src/provider-models/openai-compat.ts`
- cursor: `[_]`
- core_role: Provider-specific model-manager option factory and dynamic catalog mapper for OpenAI-compatible, Anthropic-compatible, Ollama, OpenRouter, ZenMux, Kimi, Wafer, and other providers.
- algorithmic_behavior: Fetches models.dev, maps Anthropic models, builds bundled references, normalizes provider base URLs, fetches Ollama native `/api/tags` and `/api/show` metadata, filters OpenAI/NanoGPT IDs, and exports many `*ModelManagerOptions` factories (`packages/catalog/src/provider-models/openai-compat.ts:36`, `:89`, `:257`, `:448`, `:530`, `:1080+` provider sections).
- inputs_outputs_state: Inputs are API keys, base URLs, fetch impls, provider IDs, discovery records, bundled references, and provider-specific payload fields. Outputs are `ModelManagerOptions` and `ModelSpec[]`. State includes Ollama metadata resolver cache and provider fallback tables.
- gates_or_invariants: Tool-capable model filtering, provider-specific headers, bundled metadata remains canonical where discovery lacks limits/pricing, unknown IDs get safe defaults, and unsupported non-text/image/realtime IDs are filtered.
- dependencies_and_callers: Used by catalog descriptors/generator and coding-agent `ModelRegistry`. Depends on discovery, identity, bundled references, GitHub Copilot wire, and catalog utils.
- edge_cases_or_failure_modes: Malformed discovery records, unavailable remote endpoints, missing API key, incorrect base URL suffix, provider-specific pricing units, unknown upstream thinking format, Ollama fallback, and model ID classification errors.
- validation_or_tests: `issue-847-repro.test.ts`, custom provider discovery tests, and provider catalog generation/regression tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1923 `file` `packages/coding-agent/src/capability/rule-buckets.ts`
- cursor: `[_]`
- core_role: Buckets discovered rules into built-in/default/project/global/other groups.
- algorithmic_behavior: `bucketRules` classifies `Rule` objects into `RuleBuckets` using provider/source metadata and optional TTSR manager context (`packages/coding-agent/src/capability/rule-buckets.ts:33`).
- inputs_outputs_state: Inputs are rule list and bucketing options. Outputs are grouped rule arrays. No persistent state.
- gates_or_invariants: Built-in defaults provider ID is treated specially; bucket assignment must preserve rule identity and avoid dropping unknown rules.
- dependencies_and_callers: Used by capability/rule discovery and UI/config display.
- edge_cases_or_failure_modes: Missing provider ID, duplicate rules, unknown source, and disabled TTSR context.
- validation_or_tests: Capability/rulebook tests likely cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1953 `file` `packages/coding-agent/src/cli/profile-bootstrap.ts`
- cursor: `[_]`
- core_role: Early CLI argv parser for profile flags before command registry initialization.
- algorithmic_behavior: Detects profile bootstrap subcommands, strips/collects global profile/config flags, decides when a boundary is required after global strip, and returns `ProfileBootstrapResult` (`packages/coding-agent/src/cli/profile-bootstrap.ts:46`, `:60`, `:91`).
- inputs_outputs_state: Input is raw argv; output is stripped argv, profile/config info, and flags. No persistent state.
- gates_or_invariants: Unknown long value candidates and subcommand boundaries prevent accidental consumption of command args.
- dependencies_and_callers: Used by CLI startup before loading commands/settings.
- edge_cases_or_failure_modes: `--profile` missing value, unknown long flags, subcommand ambiguity, and global/command flag collision.
- validation_or_tests: CLI/profile tests likely cover; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1983 `file` `packages/coding-agent/src/commands/dry-balance.ts`
- cursor: `[_]`
- core_role: CLI command wrapper for dry-balance workflow.
- algorithmic_behavior: Defines command args/flags and delegates to `runDryBalanceCommand` (`packages/coding-agent/src/commands/dry-balance.ts:4`).
- inputs_outputs_state: Inputs are CLI args/flags. Outputs are command execution side effects from delegated runner. No state in wrapper.
- gates_or_invariants: Command schema must match CLI framework expectations.
- dependencies_and_callers: Used by coding-agent command registry.
- edge_cases_or_failure_modes: Bad arg parsing or mismatch with runner parameters.
- validation_or_tests: CLI command tests/`bun check`.
- skip_candidate: `yes: thin CLI wrapper, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2013 `file` `packages/coding-agent/src/commit/utils.ts`
- cursor: `[_]`
- core_role: Commit-assistant parsing/normalization helpers.
- algorithmic_behavior: Extracts named tool calls from assistant message, concatenates text content, parses JSON payload from text, and normalizes conventional commit analysis/details (`packages/coding-agent/src/commit/utils.ts:4`, `:8`, `:16`, `:28`, `:46`).
- inputs_outputs_state: Inputs are `AssistantMessage`, tool name, JSON-ish text, and parsed analysis/detail objects. Outputs are `ToolCall`, text, parsed unknown value, normalized analysis/detail arrays. No state.
- gates_or_invariants: Only text blocks are included; tool name must match exactly; normalization constrains changelog/category/user-visible fields.
- dependencies_and_callers: Used by commit/guided-goal/agentic commit workflows.
- edge_cases_or_failure_modes: Missing text/tool call, malformed JSON, unexpected category/detail shape.
- validation_or_tests: Commit/guided-goal tests likely cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2043 `file` `packages/coding-agent/src/debug/system-info.ts`
- cursor: `[_]`
- core_role: System/environment information collector and sanitizer for debug reports.
- algorithmic_behavior: Computes macOS marketing name, collects OMP version, OS, arch, CPU, memory, project dir, Bun/process info, formats a debug string, and sanitizes env values (`packages/coding-agent/src/debug/system-info.ts:27`, `:42`, `:80`, `:101`).
- inputs_outputs_state: Inputs are process/os/env/project data. Outputs are `SystemInfo`, formatted text, sanitized env map. No persistent state.
- gates_or_invariants: Sensitive env values must be redacted; output should be stable and human-readable.
- dependencies_and_callers: Used by debug/reporting tooling and support issue generation.
- edge_cases_or_failure_modes: Unknown macOS release, missing project dir, secret-like env keys, and platform differences.
- validation_or_tests: Debug/report-tool issue flows indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2073 `file` `packages/coding-agent/src/edit/read-file.ts`
- cursor: `[_]`
- core_role: Read/serialize abstraction for editable files, including notebooks.
- algorithmic_behavior: `readEditFileText` reads notebook paths via notebook conversion and other paths via `Bun.file`; `serializeEditFileText` serializes edited notebook text or returns plain content (`packages/coding-agent/src/edit/read-file.ts:10`, `:22`).
- inputs_outputs_state: Inputs are absolute path, display path, and edited content. Outputs are editable text or serialized file content. No state.
- gates_or_invariants: Notebook detection controls conversion path; ENOENT handling comes through `isEnoent` imports/use in surrounding code.
- dependencies_and_callers: Used by edit tools and notebook editing flow.
- edge_cases_or_failure_modes: Missing file, invalid notebook JSON, path extension mismatch, and serialization failure.
- validation_or_tests: Notebook/edit tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2103 `file` `packages/coding-agent/src/goals/guided-setup.ts`
- cursor: `[_]`
- core_role: LLM-guided goal setup turn runner.
- algorithmic_behavior: Defines a `respond` tool, parses tool JSON arguments, renders guided-goal prompts, calls `instrumentedCompleteSimple`, extracts tool call/text, and returns either question/summary/update result (`packages/coding-agent/src/goals/guided-setup.ts:12`, `:42`, `:64`).
- inputs_outputs_state: Inputs are agent session, previous guided messages, user reply, model/thinking settings, and telemetry. Outputs are `GuidedGoalTurnResult`. State is conversation messages passed in options.
- gates_or_invariants: Response must parse into expected payload; reasoning settings are mapped/disabled as needed; prompt content is external `.md`.
- dependencies_and_callers: Used by goals mode/setup UI. Depends on agent telemetry, pi-ai tools, prompt renderer, commit utils, and thinking helpers.
- edge_cases_or_failure_modes: Model omits tool call, malformed JSON, unsupported payload kind, provider reasoning constraints, and completion failure.
- validation_or_tests: Goal tool/runtime tests validate adjacent goal behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2133 `file` `packages/coding-agent/src/internal-urls/vault-protocol.ts`
- cursor: `[_]`
- core_role: Internal URL protocol handler for Obsidian vault resources.
- algorithmic_behavior: Parses `vault://` URLs/ops/params, validates relative paths, resolves vault paths, spawns Obsidian CLI with timeout/abort, caches binary/vault directory/active vault info, counts entries, formats links, reads/writes resources, and exposes handler functions (`packages/coding-agent/src/internal-urls/vault-protocol.ts:206`, `:245`, `:288`, `:314`, `:422`, `:467`).
- inputs_outputs_state: Inputs are internal URL, resolve/write context, settings, Obsidian CLI output, file paths, and abort signal. Outputs are `InternalResource`, resolved filesystem paths, CLI spawn results, or errors. State includes cached binary, vault directories, active vault path, and vault info map.
- gates_or_invariants: Vault feature must be enabled; paths must stay within vault root; ops must be known file/vault ops; Obsidian binary must exist; CLI success is asserted.
- dependencies_and_callers: Used by internal URL router/read/write/edit paths. Depends on settings, `parseInternalUrl`, `validateRelativePath`, filesystem, and `$which`.
- edge_cases_or_failure_modes: Disabled vault, missing Obsidian, CLI timeout/abort, malformed URL/op, path traversal, missing active vault, stale cache, and unsupported content type.
- validation_or_tests: Internal URL/edit streaming tests include local URL path handling; vault-specific tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2163 `file` `packages/coding-agent/src/mcp/smithery-registry.ts`
- cursor: `[_]`
- core_role: Smithery MCP registry search/detail/config generator.
- algorithmic_behavior: Clamps search limits, matches identity queries, resolves detail paths, normalizes qualified names, extracts tool/input metadata, chooses connection, creates MCP config, fetches details, maps entries to `SmitherySearchResult`, searches registry, and generates config names (`packages/coding-agent/src/mcp/smithery-registry.ts:121`, `:128`, `:214`, `:243`, `:268`, `:292`, `:391`, `:475`).
- inputs_outputs_state: Inputs are search query/options/API key, Smithery search/detail JSON, and selected connection. Outputs are search results, required input descriptors, display metadata, and `MCPServerConfig`. No persistent state.
- gates_or_invariants: Limit is clamped, sensitive inputs are marked by key/format, connection type must be supported, details must be fetched for entries, and errors use `SmitheryRegistryError`.
- dependencies_and_callers: Used by MCP marketplace/search/install flows. Depends on logger and MCP server config types.
- edge_cases_or_failure_modes: Registry HTTP failure, missing detail path, malformed schema/tools, duplicate identity, unsupported connection, sensitive config values, and bad date metadata.
- validation_or_tests: MCP registry/install tests likely cover; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2193 `file` `packages/coding-agent/src/modes/prompt-action-autocomplete.ts`
- cursor: `[_]`
- core_role: Autocomplete provider for prompt action commands and emoji inline replacement.
- algorithmic_behavior: Extracts action prefix, fuzzy matches/scores definitions, builds autocomplete items with key hints/settings, handles prompt-action item application, and creates provider instances (`packages/coding-agent/src/modes/prompt-action-autocomplete.ts:43`, `:57`, `:84`, `:96`, `:203`).
- inputs_outputs_state: Inputs are text before cursor, autocomplete context, keybindings, settings, and emoji/action definitions. Outputs are autocomplete items or applied text edits. State is provider-held options.
- gates_or_invariants: Prefix detection must avoid normal text; fuzzy score determines ordering; emoji completions are separate path; key hints reflect active keybindings/settings.
- dependencies_and_callers: Used by interactive prompt input. Depends on TUI autocomplete types, keybindings, settings, emoji autocomplete, and prompt actions.
- edge_cases_or_failure_modes: Empty prefix, overlapping emoji/action syntax, stale settings initialization, and bad keybinding hints.
- validation_or_tests: Interactive mode/autocomplete tests likely cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2223 `file` `packages/coding-agent/src/session/session-context.ts`
- cursor: `[_]`
- core_role: Session restoration context builder, including compaction and Snapcompact archive rehydration.
- algorithmic_behavior: Finds restorable session models, latest compaction entry, and builds `SessionContext` from entries by translating messages, compaction summaries, branch summaries, and preserved Snapcompact images (`packages/coding-agent/src/session/session-context.ts:26`, `:45`, `:70`).
- inputs_outputs_state: Inputs are session entries, provider payload, service tier, cwd/session metadata, and conversion options. Outputs are context messages and restorable model/service-tier data. State is reconstructed from append-only session entries.
- gates_or_invariants: Latest compaction dominates restored context; ephemeral model changes are handled separately; Snapcompact archive images are restored from preserve data; custom messages are converted.
- dependencies_and_callers: Used by `AgentSession` resume/fork/open flows. Depends on `@oh-my-pi/snapcompact` and session message factories.
- edge_cases_or_failure_modes: Missing compaction entry, unknown custom entry, stale preserved image archive, branch summary ordering, and model/service-tier changes.
- validation_or_tests: Session message/peek/auto-compaction tests validate related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2253 `file` `packages/coding-agent/src/stt/asr-protocol.ts`
- cursor: `[_]`
- core_role: Worker message protocol types for speech-to-text ASR runtime.
- algorithmic_behavior: Defines progress statuses, file progress state, inbound worker commands, outbound worker events, and transport interface (`packages/coding-agent/src/stt/asr-protocol.ts:3`, `:23`, `:37`, `:62`).
- inputs_outputs_state: Inputs/outputs are typed messages: ping, transcribe/download commands, progress/error/log/result events. State is external to protocol.
- gates_or_invariants: Message discriminants must stay stable between parent and worker.
- dependencies_and_callers: Used by STT client/worker implementation.
- edge_cases_or_failure_modes: Unknown message type, progress file map drift, and parent/worker version mismatch.
- validation_or_tests: Type checking and STT runtime tests.
- skip_candidate: `yes: protocol type contract only`

### OH_MY_HUMANIZE_MAIN-HZ-2283 `file` `packages/coding-agent/src/tiny/title-protocol.ts`
- cursor: `[_]`
- core_role: Worker message protocol for local tiny title/completion model subprocess.
- algorithmic_behavior: Defines progress events, inbound commands (`ping`, `generate`, `complete`, `download`), outbound responses (`pong`, `title`, `completion`, `downloaded`, `error`, `progress`, `log`), and transport interface (`packages/coding-agent/src/tiny/title-protocol.ts:3`, `:23`, `:32`, `:51`).
- inputs_outputs_state: Inputs are model key, message/prompt, max tokens, download request. Outputs are title/completion/progress/error/log messages. State is maintained by tiny-model client/worker.
- gates_or_invariants: Parent owns lifecycle; no close handshake by design to avoid NAPI finalizer issues.
- dependencies_and_callers: Used by tiny title client and worker host dispatch.
- edge_cases_or_failure_modes: Worker crash, download progress partials, null title/completion, and model key mismatch.
- validation_or_tests: Tiny dtype/smoke tests validate adjacent tiny-model worker behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2313 `file` `packages/coding-agent/src/tools/gh-renderer.ts`
- cursor: `[_]`
- core_role: TUI renderer for GitHub tool calls/results, especially run/watch status.
- algorithmic_behavior: Formats operation titles/meta, issue/PR identifiers, run/job labels, status visuals, failed logs, watch sections, fallback components, and exposes `githubToolRenderer` (`packages/coding-agent/src/tools/gh-renderer.ts:52`, `:80`, `:119`, `:160`, `:232`, `:394`, `:418`).
- inputs_outputs_state: Inputs are GitHub tool args, result details/content, render options, width, and theme. Outputs are TUI components/lines. State is local rendering computation.
- gates_or_invariants: Status/conclusion sets map to stable icons/colors; width fallback applies; fallback text extracted when structured details absent.
- dependencies_and_callers: Used by GitHub tool render path in coding-agent TUI.
- edge_cases_or_failure_modes: Missing PR/issue/run fields, failed log truncation, pending/running statuses, malformed result content, and narrow terminal width.
- validation_or_tests: GitHub tool rendering covered indirectly; collab-web has separate renderer.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2343 `file` `packages/coding-agent/src/tools/report-tool-issue.ts`
- cursor: `[_]`
- core_role: Tool for reporting tool issues and optional Auto-QA grievance persistence/flush.
- algorithmic_behavior: Builds tool params, resolves Auto-QA enablement/consent, persists consent, opens Auto-QA SQLite DB, resolves push config, flushes queued grievances with cooldown/batch/timeout, and creates the report tool (`packages/coding-agent/src/tools/report-tool-issue.ts:30`, `:43`, `:153`, `:200`, `:338`, `:421`, `:460`).
- inputs_outputs_state: Inputs are settings, active tool names, user report args, consent handler, env overrides, DB rows, and flush options. Outputs are tool result, persisted grievance rows, remote flush result, and settings updates. State includes consent handler, failure cooldown state, and SQLite queue.
- gates_or_invariants: Auto-QA requires enablement and consent unless bypassed; flush batch capped; failures observe cooldown; env overrides can configure endpoint/token.
- dependencies_and_callers: Used by agent tools and tests. Depends on settings, SQLite, tool/session types, and logger/network fetch.
- edge_cases_or_failure_modes: Consent denial, DB unavailable, network failure, flush timeout, repeated failure cooldown, sensitive config missing, and invalid active tool name.
- validation_or_tests: `packages/coding-agent/test/tools/report-tool-issue-consent.test.ts` validates consent resolution.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2373 `file` `packages/coding-agent/src/tui/status-line.ts`
- cursor: `[_]`
- core_role: Standardized TUI status header line formatter for tool output.
- algorithmic_behavior: Flattens CR/LF in title/description/meta/badge fields and renders icon/title/description/badge/meta with theme colors (`packages/coding-agent/src/tui/status-line.ts:20`, `:24`).
- inputs_outputs_state: Inputs are `StatusLineOptions`, theme, spinner frame. Output is one status line string. No state.
- gates_or_invariants: Newlines in caller-provided fragments are replaced with spaces so status cannot expand into multiple rows.
- dependencies_and_callers: Used by tool renderers; depends on theme and `formatStatusIcon`.
- edge_cases_or_failure_modes: Empty meta, icon override precedence, newline injection, and badge formatting.
- validation_or_tests: Tool renderer tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2403 `file` `packages/coding-agent/src/utils/tool-choice.ts`
- cursor: `[_]`
- core_role: Coding-agent helper for local tool-choice queue/validation mapping.
- algorithmic_behavior: Wraps/gates generic tool choice behavior for coding-agent session/tool control. It is adjacent to pi-ai `utils/tool-choice` and used by session force-tool-choice flows.
- inputs_outputs_state: Inputs are tool choice directives or active tool names. Outputs are normalized/validated choices. State is external queue/session state.
- gates_or_invariants: Forced tool names must correspond to active tools; unsupported choices should fail or fall back predictably.
- dependencies_and_callers: Used by `AgentSession` tool-choice queue and tests such as force-tool-choice/yield.
- edge_cases_or_failure_modes: Tool filtered out before dequeue, forced non-active tool, and stale choice after abort.
- validation_or_tests: Tool-choice queue/session tests cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2433 `file` `packages/coding-agent/src/workflow/runtime-binding.ts`
- cursor: `[_]`
- core_role: Workflow runtime binding availability checker.
- algorithmic_behavior: Filters unavailable runtime capabilities, computes capabilities required by selected start nodes, and returns blocking error text if required tool/agent/plugin/extension/skill capabilities are unavailable (`packages/coding-agent/src/workflow/runtime-binding.ts:5`, `:9`, `:18`, `:31`).
- inputs_outputs_state: Inputs are `RuntimeBindingSnapshot`, workflow definition, and start node IDs. Output is optional error string/unavailable list. No state.
- gates_or_invariants: Only capability prefixes `tool:`, `agent:`, `plugin:`, `extension:`, `skill:` block; script nodes map to `bash` or `eval`, human to `ask`, agent/review to `task` plus optional agent ID.
- dependencies_and_callers: Used by workflow slash command/start lifecycle before running nodes.
- edge_cases_or_failure_modes: Missing start node ignored, unknown node type has no capabilities, and broad unavailable entries only block if they match required capability prefix.
- validation_or_tests: `packages/coding-agent/test/workflow/runner.test.ts` covers workflow runtime behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2463 `file` `packages/coding-agent/test/core/python-executor-display.test.ts`
- cursor: `[_]`
- core_role: Test for Python kernel display output propagation.
- algorithmic_behavior: Uses `FakeKernel` and `executePythonWithKernel` to assert display outputs are captured/preserved (`packages/coding-agent/test/core/python-executor-display.test.ts:6`).
- inputs_outputs_state: Inputs are fake kernel display messages and code execution request. Outputs are `KernelDisplayOutput` entries in execution result. State is fake kernel message queue.
- gates_or_invariants: Display outputs must not be dropped or flattened into plain text incorrectly.
- dependencies_and_callers: Tests Python eval executor/kernel integration.
- edge_cases_or_failure_modes: Multiple display outputs, mime payload shape, and execution completion ordering.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2493 `file` `packages/coding-agent/test/discovery/claude-commands.test.ts`
- cursor: `[_]`
- core_role: Tests Claude Code slash command discovery.
- algorithmic_behavior: Writes command files into temp dirs, clears fs cache/settings, loads slash-command capability, and asserts discovered commands (`packages/coding-agent/test/discovery/claude-commands.test.ts:15`).
- inputs_outputs_state: Inputs are temp command files and config roots. Outputs are discovered `SlashCommand[]`. State is fs cache/settings reset.
- gates_or_invariants: Discovery must respect Claude command layout/scope and not leak cache between tests.
- dependencies_and_callers: Tests capability discovery and slash command capability.
- edge_cases_or_failure_modes: Bad command file, cache stale after filesystem changes, and project/global precedence.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2523 `file` `packages/coding-agent/test/goals/goal-tool.test.ts`
- cursor: `[_]`
- core_role: Tests goal tool runtime behavior and budget reporting.
- algorithmic_behavior: Builds goal/usage/session harness and verifies `GoalTool` operations and `completionBudgetReport` semantics (`packages/coding-agent/test/goals/goal-tool.test.ts:58`).
- inputs_outputs_state: Inputs are goal state, token usage, tool args, and session override. Outputs are updated goal state and tool result content. State is cloned goal mode state in harness.
- gates_or_invariants: Goal mutations must preserve mode state, budget reporting must reflect token usage, and tool ops must validate inputs.
- dependencies_and_callers: Tests goals runtime/state/tool implementation.
- edge_cases_or_failure_modes: Missing goal, completed/abandoned status, usage overflow, and bad operation args.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2553 `file` `packages/coding-agent/test/memories/isolation.test.ts`
- cursor: `[_]`
- core_role: Tests project isolation for memory keys/scopes.
- algorithmic_behavior: Uses two cwd constants and memory helpers to ensure records for one project do not appear in another (`packages/coding-agent/test/memories/isolation.test.ts:19`).
- inputs_outputs_state: Inputs are project CWDs and memory records. Outputs are filtered memory results. State is in-memory/test memory store.
- gates_or_invariants: Memory backend scope must include project/cwd isolation.
- dependencies_and_callers: Tests coding-agent memory backend/session integration.
- edge_cases_or_failure_modes: Cross-project leakage and path normalization collisions.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2583 `file` `packages/coding-agent/test/session/peek-session-init.test.ts`
- cursor: `[_]`
- core_role: Tests `SessionManager.peekSessionInit` lightweight session metadata read.
- algorithmic_behavior: Writes session entries and asserts latest `session_init` contract/header cwd are returned, legacy sessions return init null, unreadable files return null (`packages/coding-agent/test/session/peek-session-init.test.ts:41`, `:68`, `:80`).
- inputs_outputs_state: Inputs are temp session JSONL files and session entries. Outputs are peeked init/header metadata or null. State is temp session storage.
- gates_or_invariants: Peek must avoid full session open while preserving tools/spawns/readSummarize contract.
- dependencies_and_callers: Tests `SessionManager`.
- edge_cases_or_failure_modes: Missing `session_init`, unreadable file, multiple init entries, and header cwd recovery.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2613 `file` `packages/coding-agent/test/task/create-memo.test.ts`
- cursor: `[_]`
- core_role: Tests task tool discovery memo creation.
- algorithmic_behavior: Mocks task discovery, creates `TaskTool` session, and asserts memo content for discovered agents (`packages/coding-agent/test/task/create-memo.test.ts:26`).
- inputs_outputs_state: Inputs are cwd/session and discovered agent list. Outputs are task memo/tool result. State is spy/mocked discovery.
- gates_or_invariants: Memo must include relevant discovered agents and avoid stale discovery.
- dependencies_and_callers: Tests `TaskTool.create` and `task/discovery`.
- edge_cases_or_failure_modes: No agents, duplicate agents, discovery failure, and session cwd mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2643 `file` `packages/coding-agent/test/tools/auto-generated-guard.test.ts`
- cursor: `[_]`
- core_role: Tests auto-generated file edit guard.
- algorithmic_behavior: Creates temp files/content and checks `assertEditableFileContent` / `assertEditableFile` allow safe files and throw `ToolError` for generated content (`packages/coding-agent/test/tools/auto-generated-guard.test.ts:17`, `:50`).
- inputs_outputs_state: Inputs are file path/content/settings. Outputs are success or `ToolError`. State is temp filesystem/settings.
- gates_or_invariants: Generated files must be protected before edit/write; settings reset before tests.
- dependencies_and_callers: Tests tools auto-generated guard used by edit/write.
- edge_cases_or_failure_modes: Generated marker detection, missing file, extension-specific generated content, and settings influence.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2673 `file` `packages/coding-agent/test/tools/find-validate-paths.test.ts`
- cursor: `[_]`
- core_role: Tests find tool path expansion/validation and renderer behavior.
- algorithmic_behavior: Validates delimited path expansion and `findToolRenderer` output with theme/component rendering (`packages/coding-agent/test/tools/find-validate-paths.test.ts:33`, `:136`).
- inputs_outputs_state: Inputs are delimited paths/globs, temp files, renderer args/results, and theme. Outputs are validated path lists and rendered text. State is temp filesystem and initialized theme.
- gates_or_invariants: Delimited paths must expand safely, invalid paths rejected, renderer should sanitize/format summaries.
- dependencies_and_callers: Tests find path utilities and renderer.
- edge_cases_or_failure_modes: Delimiter ambiguity, path traversal, missing files, glob rendering, and theme geometry.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2703 `file` `packages/coding-agent/test/tools/report-tool-issue-consent.test.ts`
- cursor: `[_]`
- core_role: Tests Auto-QA consent resolution for report-tool-issue.
- algorithmic_behavior: Resets consent state and asserts `resolveAutoQaConsent` behavior across settings/persisted/handler outcomes (`packages/coding-agent/test/tools/report-tool-issue-consent.test.ts:24`).
- inputs_outputs_state: Inputs are settings and consent handler return values. Outputs are boolean consent decisions and persisted state. State is test reset consent handler/settings.
- gates_or_invariants: Denied/null consent should not enable Auto-QA; persisted consent should be honored.
- dependencies_and_callers: Tests `report-tool-issue.ts`.
- edge_cases_or_failure_modes: Handler unavailable, handler null, settings undefined, and persisted local setting mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2733 `file` `packages/coding-agent/test/tools/yield.test.ts`
- cursor: `[_]`
- core_role: Tests Yield tool schema and execution behavior.
- algorithmic_behavior: Creates tool sessions, validates strict schema using pi-ai validation, and exercises `YieldTool` operations (`packages/coding-agent/test/tools/yield.test.ts:37`).
- inputs_outputs_state: Inputs are yield tool args and session state. Outputs are schema validation results and tool results. State is mock session.
- gates_or_invariants: Success data schema must be strict and arguments validated before execution.
- dependencies_and_callers: Tests `YieldTool`, pi-ai schema/validation, and settings/session types.
- edge_cases_or_failure_modes: Invalid args, missing success data, strict schema enforcement, and session overrides.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2763 `file` `packages/coding-agent/test/workflow/runner.test.ts`
- cursor: `[_]`
- core_role: Tests workflow runner execution, run-store reconstruction, state patch events, and model/script node runtime integration.
- algorithmic_behavior: Parses workflow source, creates fake host/freeze/runtime bindings, runs workflows, and asserts event/state behavior (`packages/coding-agent/test/workflow/runner.test.ts:146`).
- inputs_outputs_state: Inputs are workflow definitions, fake model, runtime host, freeze snapshot, bindings, and script node inputs. Outputs are run entries/events/state patches and reconstructed runs. State is captured run-store entries.
- gates_or_invariants: Node execution order, state patch emission, freeze/resource handling, and model resolution must remain stable.
- dependencies_and_callers: Tests workflow definition/freeze/node-runtime/run-store/runner modules.
- edge_cases_or_failure_modes: Agent decision branch, script node failure, missing binding, persisted run reconstruction, and state patch detection.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2793 `file` `packages/mnemopi/src/core/cost-log.ts`
- cursor: `[_]`
- core_role: SQLite cost logging and aggregation for Mnemopi.
- algorithmic_behavior: Opens/initializes cost log DB, creates table, inserts cost rows, aggregates stats optionally by session, and formats local ISO timestamps (`packages/mnemopi/src/core/cost-log.ts:23`, `:29`, `:47`, `:68`, `:100`).
- inputs_outputs_state: Inputs are db path, timestamp/model/provider/tokens/cost/session data. Outputs are DB rows and `CostStats`. State is SQLite database at default or provided path.
- gates_or_invariants: Default directory exists, aggregate nulls become zeros, and session filter constrains stats.
- dependencies_and_callers: Used by Mnemopi cost tracking.
- edge_cases_or_failure_modes: DB open/create failure, missing session ID, null aggregate row, and timestamp timezone formatting.
- validation_or_tests: Mnemopi tests likely cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2823 `file` `packages/mnemopi/src/dr/index.ts`
- cursor: `[_]`
- core_role: Barrel export for Mnemopi disaster recovery helpers.
- algorithmic_behavior: Re-exports `./recovery` (`packages/mnemopi/src/dr/index.ts:1`).
- inputs_outputs_state: Import surface only; no runtime state.
- gates_or_invariants: Recovery API must remain exported from package subpath.
- dependencies_and_callers: Used by `packages/mnemopi/test/recovery.test.ts`.
- edge_cases_or_failure_modes: Missing export breaks consumers.
- validation_or_tests: Recovery test imports through this barrel.
- skip_candidate: `yes: barrel export only`

### OH_MY_HUMANIZE_MAIN-HZ-2853 `file` `packages/tui/src/components/settings-list.ts`
- cursor: `[_]`
- core_role: TUI component for searchable, grouped settings lists with scrolling and interaction.
- algorithmic_behavior: Sanitizes single-line text, builds filter text, manages `SettingsList` component render, fuzzy filtering, scroll view, keyboard/mouse interaction, item sections, and theme styling (`packages/tui/src/components/settings-list.ts:9`, `:82`, `:93`).
- inputs_outputs_state: Inputs are setting items, theme, query, dimensions, keyboard/mouse events. Outputs are rendered component lines and selection/activation events. State includes query/filter, focused item, scroll position, and section layout.
- gates_or_invariants: Tabs/newlines sanitized, visible width/truncation respected, filter text combines relevant fields, and scroll/selection remain within bounds.
- dependencies_and_callers: Used by settings selector/UI. Depends on fuzzy filter, keybindings, mouse, scroll view, and TUI utils.
- edge_cases_or_failure_modes: Narrow width, long labels/descriptions, no matches, mouse outside bounds, and stale scroll after filter.
- validation_or_tests: `settings-selector-memory-refresh.test.ts` and keybinding selector tests cover usage indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2883 `directory` `packages/coding-agent/src/eval/py/__tests__`
- cursor: `[_]`
- core_role: Python eval package-local tests.
- algorithmic_behavior: Contains `prelude.test.ts`, which validates Python eval prelude/helper behavior for kernel execution setup.
- inputs_outputs_state: Inputs are prelude code/fixtures; outputs are test assertions. State is test-only.
- gates_or_invariants: Python executor prelude must expose expected helper behavior before runtime evaluation.
- dependencies_and_callers: Tests `packages/coding-agent/src/eval/py` internals.
- edge_cases_or_failure_modes: Prelude drift causing notebook/eval helper failures.
- validation_or_tests: Directory is itself validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2913 `file` `crates/pi-shell/src/minimizer/filters/jvm.rs`
- cursor: `[_]`
- core_role: Rust shell-output minimizer for Maven/Gradle/JVM build tools.
- algorithmic_behavior: Dispatches Maven/Gradle commands, detects Maven phases and Gradle tasks, strips ANSI/progress, filters Surefire blocks, compile/package/quiet output, Gradle build/test/connected/lint/dependencies/other/bootRun output, caps noisy sections, and preserves actionable failures (`crates/pi-shell/src/minimizer/filters/jvm.rs:101`, `:116`, `:165`, `:277`, `:678`, `:760`, `:921`, `:1091`, `:1249`, `:1297`, `:1451`, `:1526`, `:1671`).
- inputs_outputs_state: Inputs are minimizer context with program/command, captured output, and exit code. Outputs are `MinimizerOutput` passthrough/transformed text. State is local parser state machines for Surefire blocks, reactor summary, failure caps, context windows, and dependency aggregation.
- gates_or_invariants: Verbose flags bypass filtering; Maven quiet routes differently; phase/task detection skips option values; framework stack frames/noise are removed while user failure signal remains; caps bound failing classes and dependency lists.
- dependencies_and_callers: Used by shell minimizer in bash executor/native shell output. Depends on regex and minimizer primitives/cap classes.
- edge_cases_or_failure_modes: Multi-module reactor summaries, Surefire 2/3 close formats, failed class trails, Gradle no-device connected tests, Android lint context blocks, Spring Boot runtime logs, quoted command limitations, and empty output fallback hints.
- validation_or_tests: Inline Rust tests in module plus shell minimizer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2943 `file` `packages/ai/src/registry/oauth/wafer.ts`
- cursor: `[_]`
- core_role: API-key login definitions for Wafer Pass and Wafer Serverless providers.
- algorithmic_behavior: Uses `createApiKeyLogin` to define dashboard/model URLs and login metadata for two Wafer provider auth flows (`packages/ai/src/registry/oauth/wafer.ts:26`, `:39`).
- inputs_outputs_state: Input is user API key through login flow. Output is OAuth/API-key credential object. No local state.
- gates_or_invariants: Provider-specific auth URLs/model endpoints must match registry/provider IDs.
- dependencies_and_callers: Used by pi-ai OAuth registry and catalog Wafer provider options.
- edge_cases_or_failure_modes: Wrong model URL/provider ID prevents validation/discovery.
- validation_or_tests: Registry/auth tests likely cover indirectly.
- skip_candidate: `yes: declarative auth metadata wrapper`

### OH_MY_HUMANIZE_MAIN-HZ-2973 `file` `packages/coding-agent/src/cli/gallery-fixtures/edit.ts`
- cursor: `[_]`
- core_role: Gallery/demo fixture for edit tool rendering or CLI showcase.
- algorithmic_behavior: Provides canned edit-related data/components for gallery rendering. It is not part of live edit execution.
- inputs_outputs_state: Inputs are fixture constants; outputs are demo-rendered UI examples. State is static.
- gates_or_invariants: Fixture shape must match current renderer contracts to keep gallery useful.
- dependencies_and_callers: Used by CLI gallery fixtures.
- edge_cases_or_failure_modes: Fixture drift from actual edit renderer/result details.
- validation_or_tests: Gallery/build tests if present; no assigned direct test.
- skip_candidate: `yes: static demo fixture, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3003 `file` `packages/coding-agent/src/commit/map-reduce/utils.ts`
- cursor: `[_]`
- core_role: Token estimation/truncation helpers for commit map-reduce summarization.
- algorithmic_behavior: Estimates tokens as `ceil(text.length / 4)` and truncates text to `maxTokens * 4` chars with marker (`packages/coding-agent/src/commit/map-reduce/utils.ts:1`, `:5`).
- inputs_outputs_state: Inputs are text and max token budget. Outputs are estimated token count or truncated text. No state.
- gates_or_invariants: Text within budget returns unchanged; over-budget output appends truncation marker.
- dependencies_and_callers: Used by commit map-reduce flows.
- edge_cases_or_failure_modes: Crude token approximation, negative/zero maxTokens, and marker itself exceeding strict token budgets.
- validation_or_tests: Commit map-reduce tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3033 `file` `packages/coding-agent/src/eval/js/worker-protocol.ts`
- cursor: `[_]`
- core_role: Worker protocol for JavaScript eval sandbox/runtime.
- algorithmic_behavior: Defines session snapshot, error payload, tool reply, inbound/outbound worker frames, display output typing, and transport interface (`packages/coding-agent/src/eval/js/worker-protocol.ts:5`, `:14`, `:20`, `:22`, `:30`, `:42`).
- inputs_outputs_state: Inputs are init/run/tool-reply/close frames. Outputs are ready/init-failed/text/display/tool-call/result/log/closed frames. State is maintained by JS eval worker/client, not protocol.
- gates_or_invariants: `localRoots` map enables internal URL substitution; run frames include snapshot; errors carry abort/tool-error flags.
- dependencies_and_callers: Used by JS eval worker and parent executor.
- edge_cases_or_failure_modes: Tool reply mismatch, worker init failure, abort error shape, local URL root missing, and protocol version drift.
- validation_or_tests: JS eval tests likely cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3063 `file` `packages/coding-agent/src/extensibility/hooks/loader.ts`
- cursor: `[_]`
- core_role: Hook discovery and module loader for extensibility hooks.
- algorithmic_behavior: Discovers hook paths, loads modules, validates exported hook shape, orders handlers, and returns loaded hook/error results. It wires hook modules into runtime event surfaces described by docs.
- inputs_outputs_state: Inputs are configured hook paths, cwd/config dirs, and module exports. Outputs are loaded hook descriptors and load errors. State is loader-local caches/results.
- gates_or_invariants: Invalid modules should produce load errors without killing app; path resolution must respect config/project ordering; handler order must remain deterministic.
- dependencies_and_callers: Used by extension/hook runtime and `docs/hooks.md` behavior.
- edge_cases_or_failure_modes: Missing file, bad export, duplicate hook IDs, module throw, and path precedence conflicts.
- validation_or_tests: Hook/extensibility tests likely cover; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3093 `file` `packages/coding-agent/src/modes/acp/acp-event-mapper.ts`
- cursor: `[_]`
- core_role: Maps internal agent/session/tool events to ACP session notifications and content blocks.
- algorithmic_behavior: Maps tool kind, agent session events, assistant message updates/ends, todo results, tool start/update/end content, replayed tool args, command/eval text, locations, diffs, terminal content, embedded resources, and readable text with limits (`packages/coding-agent/src/modes/acp/acp-event-mapper.ts:130`, `:159`, `:402`, `:429`, `:451`, `:545`, `:596`, `:639`, `:923`).
- inputs_outputs_state: Inputs are `AgentSessionEvent`, tool args/results, replay cwd/session ID, and current message progress. Outputs are ACP `SessionNotification` updates. State includes per-message progress tracking.
- gates_or_invariants: Text is capped, locations resolve against cwd, command/eval content preserved across updates, terminal content deduped, malformed replay args preserved raw, and notification discriminators validated.
- dependencies_and_callers: Used by ACP mode/server. Tested by `acp-event-mapper.test.ts`.
- edge_cases_or_failure_modes: Streaming deltas plus final text duplication, malformed JSON string args, move-style paths, terminal-only details, embedded resources, mutated discriminators, and empty readable content.
- validation_or_tests: Extensive ACP event mapper tests listed in scan cover command/eval/diff/location/terminal/replay cases.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3123 `file` `packages/coding-agent/src/modes/components/hook-message.ts`
- cursor: `[_]`
- core_role: TUI component for rendering custom hook messages.
- algorithmic_behavior: Creates a themed box, optionally delegates to custom hook renderer, supports collapsed/expanded body, rebuilds on invalidation, and uses `renderFramedMessage` (`packages/coding-agent/src/modes/components/hook-message.ts:8`, `:19`, `:34`, `:39`).
- inputs_outputs_state: Inputs are `HookMessage` and optional renderer. Output is component tree. State is expanded flag and child component/box.
- gates_or_invariants: Collapsed default is 5 lines; custom renderer replaces default box; rebuild removes stale children.
- dependencies_and_callers: Used by transcript/session message rendering for hook-generated entries.
- edge_cases_or_failure_modes: Custom renderer returning component, repeated invalidation, collapse toggles, and missing renderer.
- validation_or_tests: Hook message UI tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3153 `file` `packages/coding-agent/src/modes/components/todo-reminder.ts`
- cursor: `[_]`
- core_role: TUI reminder component shown when agent stops with incomplete todos.
- algorithmic_behavior: Renders warning box with count, reminder attempt/max, and unchecked todo list (`packages/coding-agent/src/modes/components/todo-reminder.ts:7`, `:23`).
- inputs_outputs_state: Inputs are todo items, attempt, max attempts. Output is component tree. State is box content.
- gates_or_invariants: Singular/plural label and attempt counter must match provided values.
- dependencies_and_callers: Used by todo reminder event/UI flow.
- edge_cases_or_failure_modes: Empty todo list, long todo content, high attempt counts.
- validation_or_tests: Todo reminder tests if present; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3183 `file` `packages/coding-agent/src/modes/rpc/rpc-client.ts`
- cursor: `[_]`
- core_role: TypeScript RPC client for coding-agent sessions, events, custom tools, and host interactions.
- algorithmic_behavior: Defines command/event/tool types, validates response/event frame shapes, normalizes tool results, registers custom tools, handles agent/session/subagent/available-command/host-tool/extension UI frames, and implements `RpcClient` request lifecycle (`packages/coding-agent/src/modes/rpc/rpc-client.ts:42`, `:89`, `:126`, `:193`, `:206`).
- inputs_outputs_state: Inputs are transport frames, commands, prompt text, custom tool definitions, and callbacks. Outputs are RPC responses/events, tool results, and listener callbacks. State includes request IDs, pending responses, listener sets, and registered tools.
- gates_or_invariants: Frame type guards protect malformed payloads; command IDs correlate responses; custom tool results normalize string vs object; host tool calls/cancels must route to registered handler.
- dependencies_and_callers: Used by SDK/RPC mode and tested by `rpc-host-tools.test.ts`.
- edge_cases_or_failure_modes: Unknown frame, response to missing request, tool cancel, extension UI request, listener errors, transport close, and malformed result.
- validation_or_tests: `packages/coding-agent/test/rpc-host-tools.test.ts` and RPC host URI tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3213 `file` `packages/coding-agent/src/slash-commands/helpers/workflow.ts`
- cursor: `[_]`
- core_role: Slash-command controller for workflow lifecycle, dashboard/status/list/graph, start/stop/interrupt/restart, freeze, change requests, runtime binding audit, and formatting.
- algorithmic_behavior: Parses workflow subcommands/args, loads workflow definitions, starts active attempts, manages active attempt maps, stops/interrupts nodes with abort controllers, handles freeze/change request approve/reject/apply, builds runtime binding snapshots, collects plugin/extension/skill/tool/model capabilities, writes draft resources, emits graph/dashboard/status/help views, and formats lifecycle summaries (`packages/coding-agent/src/slash-commands/helpers/workflow.ts:177`, `:381`, `:530`, `:607`, `:743`, `:906`, `:1501`, `:1681`, `:2078`, `:2490`).
- inputs_outputs_state: Inputs are parsed slash command, runtime/session context, workflow files, active attempts, change request IDs, checkpoint IDs, runtime capabilities, and user flags. Outputs are `SlashCommandResult`, emitted graph views/messages, workflow runs, drafts, and abort side effects. State includes `WeakMap` of active workflow attempts per runtime and persisted workflow lifecycle records.
- gates_or_invariants: Start conflicts block duplicate workflows, runtime binding unavailable blocks starts, stop/interrupt target resolution handles ambiguity, change requests require valid IDs/state, and lifecycle flushing happens around restart/stop.
- dependencies_and_callers: Used by `/workflow` slash command and ACP workflow entrypoint. Depends on workflow definition/runner/scheduler/lifecycle/graph/draft modules, marketplace manager, parser helpers, and runtime model registry.
- edge_cases_or_failure_modes: Ambiguous attempt IDs, missing checkpoint, stale active attempt, abort races, unavailable capabilities, malformed args, duplicate change application, persisted session lookup failure, and resource restore path validation.
- validation_or_tests: `packages/coding-agent/test/workflow/runner.test.ts` plus workflow slash command tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3243 `file` `packages/coding-agent/src/web/scrapers/firefox-addons.ts`
- cursor: `[_]`
- core_role: Special web scraper handler for Firefox Add-ons pages/API.
- algorithmic_behavior: Normalizes categories, collects extension permissions from addon file data, fetches addon JSON, and returns structured markdown/content for addons (`packages/coding-agent/src/web/scrapers/firefox-addons.ts:44`, `:65`, `:86`).
- inputs_outputs_state: Inputs are addon URL, timeout, abort signal, and remote JSON. Output is scraper result content. No persistent state.
- gates_or_invariants: Categories can be string array or localized record; permissions must be deduped/normalized; fetch respects timeout/signal.
- dependencies_and_callers: Used by web fetch/search special handler system.
- edge_cases_or_failure_modes: Missing current version/file, localized category shape, addon not found, network timeout, and malformed JSON.
- validation_or_tests: Web scraper tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3273 `file` `packages/coding-agent/src/web/scrapers/pub-dev.ts`
- cursor: `[_]`
- core_role: Special scraper handler for Dart `pub.dev` package pages.
- algorithmic_behavior: Fetches/parses pub.dev package metadata and formats relevant package content (`packages/coding-agent/src/web/scrapers/pub-dev.ts:7`).
- inputs_outputs_state: Inputs are pub.dev URL, timeout, abort signal. Output is scraper result/markdown text. No persistent state.
- gates_or_invariants: Handler should only process supported pub.dev URLs and honor abort/timeout.
- dependencies_and_callers: Used by web fetch/search special handler registry.
- edge_cases_or_failure_modes: Unsupported URL path, package missing, network failure, malformed page/API response.
- validation_or_tests: Web scraper tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3303 `file` `packages/coding-agent/src/web/search/render.ts`
- cursor: `[_]`
- core_role: TUI renderer for web search calls/results.
- algorithmic_behavior: Renders fallback text, error panels, search result answers/items/images, collapsed/expanded previews, call previews, and exposes `webSearchToolRenderer` (`packages/coding-agent/src/web/search/render.ts:29`, `:57`, `:78`, `:248`, `:258`).
- inputs_outputs_state: Inputs are search response/details, expanded flag, provider label, theme, tool args/result. Outputs are TUI components. State is local render computation.
- gates_or_invariants: Collapsed items are capped by preview constants; fallback/error paths render safely; content text is sanitized/truncated by utility components.
- dependencies_and_callers: Used by web search tool render path and tested directly.
- edge_cases_or_failure_modes: Empty answer/results, provider error, malformed details, long snippets, and expanded/collapsed transitions.
- validation_or_tests: `packages/coding-agent/test/web/search/render.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3333 `file` `packages/coding-agent/test/modes/components/settings-selector-memory-refresh.test.ts`
- cursor: `[_]`
- core_role: Tests settings selector memory tab refresh/render behavior.
- algorithmic_behavior: Stubs stdout geometry, initializes theme/settings, focuses memory tab, creates `SettingsSelectorComponent`, and asserts memory tab content refreshes (`packages/coding-agent/test/modes/components/settings-selector-memory-refresh.test.ts:64`).
- inputs_outputs_state: Inputs are settings state, terminal geometry, and component actions. Outputs are rendered component text/state. State is global settings/theme restored in hooks.
- gates_or_invariants: Memory backend changes should be reflected in settings selector without stale display.
- dependencies_and_callers: Tests settings selector and memory backend state.
- edge_cases_or_failure_modes: Geometry-dependent layout, settings reset leakage, memory tab focus, and stale backend status.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3363 `file` `packages/coding-agent/test/modes/controllers/session-selector-delete.test.ts`
- cursor: `[_]`
- core_role: Tests session selector delete confirmation controller/UI behavior.
- algorithmic_behavior: Creates fake sessions/selector, renders text, and asserts delete confirmation flow invokes provided async delete callback correctly (`packages/coding-agent/test/modes/controllers/session-selector-delete.test.ts:43`).
- inputs_outputs_state: Inputs are session list, user key/actions, and delete callback result. Outputs are rendered text and deletion callback calls. State is selector focus/confirmation state.
- gates_or_invariants: Delete must require confirmation and not delete wrong session.
- dependencies_and_callers: Tests `SessionSelectorComponent`.
- edge_cases_or_failure_modes: Delete callback false, focus changes during confirmation, and session title/ID formatting.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3393 `file` `packages/coding-agent/test/web/search/render.test.ts`
- cursor: `[_]`
- core_role: Tests web search result rendering.
- algorithmic_behavior: Builds `SearchResponse` fixtures, renders search result, extracts answer section, and asserts sanitized/structured output (`packages/coding-agent/test/web/search/render.test.ts:48`).
- inputs_outputs_state: Inputs are answer text/result fixtures and theme. Output is rendered text. No persistent state.
- gates_or_invariants: Answer rendering must preserve semantic lines and sanitize unsafe text.
- dependencies_and_callers: Tests `renderSearchResult`.
- edge_cases_or_failure_modes: HTML/control characters, long answer lines, empty answer/results.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3423 `file` `packages/collab-web/src/tool-render/tools/memory-reflect.tsx`
- cursor: `[_]`
- core_role: Collab-web renderer for memory reflect tool.
- algorithmic_behavior: Renders summary from args and body from result for reflection output, exporting `reflectRenderer` (`packages/collab-web/src/tool-render/tools/memory-reflect.tsx:10`, `:15`, `:28`).
- inputs_outputs_state: Inputs are tool args/result. Output is React nodes. No persistent state.
- gates_or_invariants: Missing result should render gracefully.
- dependencies_and_callers: Used by collab-web tool renderer registry.
- edge_cases_or_failure_modes: Empty reflection content, malformed args/result, and result error.
- validation_or_tests: Collab-web render/build tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3453 `file` `packages/stats/src/client/app/ThemeToggle.tsx`
- cursor: `[_]`
- core_role: Stats web UI theme preference toggle.
- algorithmic_behavior: Cycles preference `system -> light -> dark -> system`, chooses matching lucide icon and label, and updates `useThemePreference` on click.
- inputs_outputs_state: Input is current theme preference and button click. Output is next preference. State is external theme preference hook.
- gates_or_invariants: Button has accessible aria-label/title; icon map covers every preference.
- dependencies_and_callers: Used by stats client app UI. Depends on `lucide-react` and `useSystemTheme`.
- edge_cases_or_failure_modes: Unknown preference would miss map entry; hook failure prevents update.
- validation_or_tests: UI/build tests.
- skip_candidate: `yes: small UI component, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3483 `file` `packages/stats/src/client/ui/index.ts`
- cursor: `[_]`
- core_role: Barrel export for stats client UI components.
- algorithmic_behavior: Re-exports AsyncBoundary, DataTable, states, JsonBlock, MetricCluster, Panel, drawer, segmented control, skeleton, and StatusPill.
- inputs_outputs_state: Import/export surface only; no state.
- gates_or_invariants: UI components must remain exported for client imports.
- dependencies_and_callers: Stats client app.
- edge_cases_or_failure_modes: Missing export breaks imports.
- validation_or_tests: Type/build tests.
- skip_candidate: `yes: barrel export only`

### OH_MY_HUMANIZE_MAIN-HZ-3513 `file` `packages/coding-agent/src/commit/agentic/tools/schemas.ts`
- cursor: `[_]`
- core_role: Arktype schemas for agentic commit tool payloads.
- algorithmic_behavior: Defines `commitTypeSchema` and `detailSchema` with allowed conventional commit types and changelog categories.
- inputs_outputs_state: Inputs are unknown tool payload values. Outputs are schema validation results/types. No state.
- gates_or_invariants: Commit type must be one of fixed conventional categories; detail text is required; changelog category/user-visible are optional constrained fields.
- dependencies_and_callers: Used by agentic commit tools.
- edge_cases_or_failure_modes: Unknown commit type/category, missing detail text, and non-boolean user-visible flag.
- validation_or_tests: Agentic commit tests likely cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3543 `file` `packages/coding-agent/src/modes/components/extensions/state-manager.ts`
- cursor: `[_]`
- core_role: Extension dashboard state loader/filter/tree/tab manager.
- algorithmic_behavior: Loads all extensions, builds sidebar tree, flattens tree, filters by query/provider, builds provider tabs, applies disabled-extension state, creates initial dashboard state, toggles providers, and refreshes state (`packages/coding-agent/src/modes/components/extensions/state-manager.ts:47`, `:304`, `:367`, `:390`, `:447`, `:520`, `:555`, `:590`).
- inputs_outputs_state: Inputs are cwd, disabled IDs, extension manifests, query/provider. Outputs are `DashboardState`, tree nodes, flat items, filtered extensions, provider tabs. State includes disabled/shadowed/provider selection data.
- gates_or_invariants: Shadowed/disabled extensions must be represented; provider tabs aggregate counts; filter preserves matching structure.
- dependencies_and_callers: Used by extension settings/dashboard UI.
- edge_cases_or_failure_modes: Duplicate/shadowed extension IDs, disabled IDs unknown, empty extension set, query no matches, provider tab stale after refresh.
- validation_or_tests: Extension UI tests likely cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3573 `file` `packages/coding-agent/src/web/search/providers/kagi.ts`
- cursor: `[_]`
- core_role: Kagi web search provider adapter.
- algorithmic_behavior: `searchKagi` builds request params, enforces default/max result count, calls Kagi API, maps response to search types, and `KagiProvider` wraps provider class integration (`packages/coding-agent/src/web/search/providers/kagi.ts:17`, `:21`, `:65`).
- inputs_outputs_state: Inputs are query, API key/config, result count, fetch implementation. Outputs are normalized search results. No persistent state.
- gates_or_invariants: Result count capped at 40 with default 10; API key required by caller/config; fetch errors surface as provider errors.
- dependencies_and_callers: Used by web search provider registry.
- edge_cases_or_failure_modes: Missing API key, non-OK response, malformed Kagi JSON, zero/too many results.
- validation_or_tests: Web search provider/render tests cover adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3603 `file` `packages/utils/src/vendor/mermaid-ascii/sequence/types.ts`
- cursor: `[_]`
- core_role: Vendored sequence-diagram parsed/positioned type model.
- algorithmic_behavior: Defines logical `SequenceDiagram` actors/messages/blocks/notes and positioned render structures for actors, lifelines, messages, activations, blocks, and notes.
- inputs_outputs_state: Inputs/outputs are TypeScript data shapes passed between parser/layout/renderer. No runtime state.
- gates_or_invariants: Message actors reference actor IDs; block start/end/dividers index messages; positioned variants must include coordinates/dimensions.
- dependencies_and_callers: Used by vendored Mermaid ASCII sequence parser/layout/renderer.
- edge_cases_or_failure_modes: Type drift between parser and renderer, invalid actor references, and bad block indices.
- validation_or_tests: Mermaid ASCII tests/build type checks.
- skip_candidate: `yes: type model only, no executable algorithm`

## Worker Self-Test
- assigned_items_seen: 121 — OH_MY_HUMANIZE_MAIN-HZ-003, OH_MY_HUMANIZE_MAIN-HZ-033, OH_MY_HUMANIZE_MAIN-HZ-063, OH_MY_HUMANIZE_MAIN-HZ-093, OH_MY_HUMANIZE_MAIN-HZ-123, OH_MY_HUMANIZE_MAIN-HZ-153, OH_MY_HUMANIZE_MAIN-HZ-183, OH_MY_HUMANIZE_MAIN-HZ-213, OH_MY_HUMANIZE_MAIN-HZ-243, OH_MY_HUMANIZE_MAIN-HZ-273, OH_MY_HUMANIZE_MAIN-HZ-303, OH_MY_HUMANIZE_MAIN-HZ-333, OH_MY_HUMANIZE_MAIN-HZ-363, OH_MY_HUMANIZE_MAIN-HZ-393, OH_MY_HUMANIZE_MAIN-HZ-423, OH_MY_HUMANIZE_MAIN-HZ-453, OH_MY_HUMANIZE_MAIN-HZ-483, OH_MY_HUMANIZE_MAIN-HZ-513, OH_MY_HUMANIZE_MAIN-HZ-543, OH_MY_HUMANIZE_MAIN-HZ-573, OH_MY_HUMANIZE_MAIN-HZ-603, OH_MY_HUMANIZE_MAIN-HZ-633, OH_MY_HUMANIZE_MAIN-HZ-663, OH_MY_HUMANIZE_MAIN-HZ-693, OH_MY_HUMANIZE_MAIN-HZ-723, OH_MY_HUMANIZE_MAIN-HZ-753, OH_MY_HUMANIZE_MAIN-HZ-783, OH_MY_HUMANIZE_MAIN-HZ-813, OH_MY_HUMANIZE_MAIN-HZ-843, OH_MY_HUMANIZE_MAIN-HZ-873, OH_MY_HUMANIZE_MAIN-HZ-903, OH_MY_HUMANIZE_MAIN-HZ-933, OH_MY_HUMANIZE_MAIN-HZ-963, OH_MY_HUMANIZE_MAIN-HZ-993, OH_MY_HUMANIZE_MAIN-HZ-1023, OH_MY_HUMANIZE_MAIN-HZ-1053, OH_MY_HUMANIZE_MAIN-HZ-1083, OH_MY_HUMANIZE_MAIN-HZ-1113, OH_MY_HUMANIZE_MAIN-HZ-1143, OH_MY_HUMANIZE_MAIN-HZ-1173, OH_MY_HUMANIZE_MAIN-HZ-1203, OH_MY_HUMANIZE_MAIN-HZ-1233, OH_MY_HUMANIZE_MAIN-HZ-1263, OH_MY_HUMANIZE_MAIN-HZ-1293, OH_MY_HUMANIZE_MAIN-HZ-1323, OH_MY_HUMANIZE_MAIN-HZ-1353, OH_MY_HUMANIZE_MAIN-HZ-1383, OH_MY_HUMANIZE_MAIN-HZ-1413, OH_MY_HUMANIZE_MAIN-HZ-1443, OH_MY_HUMANIZE_MAIN-HZ-1473, OH_MY_HUMANIZE_MAIN-HZ-1503, OH_MY_HUMANIZE_MAIN-HZ-1533, OH_MY_HUMANIZE_MAIN-HZ-1563, OH_MY_HUMANIZE_MAIN-HZ-1593, OH_MY_HUMANIZE_MAIN-HZ-1623, OH_MY_HUMANIZE_MAIN-HZ-1653, OH_MY_HUMANIZE_MAIN-HZ-1683, OH_MY_HUMANIZE_MAIN-HZ-1713, OH_MY_HUMANIZE_MAIN-HZ-1743, OH_MY_HUMANIZE_MAIN-HZ-1773, OH_MY_HUMANIZE_MAIN-HZ-1803, OH_MY_HUMANIZE_MAIN-HZ-1833, OH_MY_HUMANIZE_MAIN-HZ-1863, OH_MY_HUMANIZE_MAIN-HZ-1893, OH_MY_HUMANIZE_MAIN-HZ-1923, OH_MY_HUMANIZE_MAIN-HZ-1953, OH_MY_HUMANIZE_MAIN-HZ-1983, OH_MY_HUMANIZE_MAIN-HZ-2013, OH_MY_HUMANIZE_MAIN-HZ-2043, OH_MY_HUMANIZE_MAIN-HZ-2073, OH_MY_HUMANIZE_MAIN-HZ-2103, OH_MY_HUMANIZE_MAIN-HZ-2133, OH_MY_HUMANIZE_MAIN-HZ-2163, OH_MY_HUMANIZE_MAIN-HZ-2193, OH_MY_HUMANIZE_MAIN-HZ-2223, OH_MY_HUMANIZE_MAIN-HZ-2253, OH_MY_HUMANIZE_MAIN-HZ-2283, OH_MY_HUMANIZE_MAIN-HZ-2313, OH_MY_HUMANIZE_MAIN-HZ-2343, OH_MY_HUMANIZE_MAIN-HZ-2373, OH_MY_HUMANIZE_MAIN-HZ-2403, OH_MY_HUMANIZE_MAIN-HZ-2433, OH_MY_HUMANIZE_MAIN-HZ-2463, OH_MY_HUMANIZE_MAIN-HZ-2493, OH_MY_HUMANIZE_MAIN-HZ-2523, OH_MY_HUMANIZE_MAIN-HZ-2553, OH_MY_HUMANIZE_MAIN-HZ-2583, OH_MY_HUMANIZE_MAIN-HZ-2613, OH_MY_HUMANIZE_MAIN-HZ-2643, OH_MY_HUMANIZE_MAIN-HZ-2673, OH_MY_HUMANIZE_MAIN-HZ-2703, OH_MY_HUMANIZE_MAIN-HZ-2733, OH_MY_HUMANIZE_MAIN-HZ-2763, OH_MY_HUMANIZE_MAIN-HZ-2793, OH_MY_HUMANIZE_MAIN-HZ-2823, OH_MY_HUMANIZE_MAIN-HZ-2853, OH_MY_HUMANIZE_MAIN-HZ-2883, OH_MY_HUMANIZE_MAIN-HZ-2913, OH_MY_HUMANIZE_MAIN-HZ-2943, OH_MY_HUMANIZE_MAIN-HZ-2973, OH_MY_HUMANIZE_MAIN-HZ-3003, OH_MY_HUMANIZE_MAIN-HZ-3033, OH_MY_HUMANIZE_MAIN-HZ-3063, OH_MY_HUMANIZE_MAIN-HZ-3093, OH_MY_HUMANIZE_MAIN-HZ-3123, OH_MY_HUMANIZE_MAIN-HZ-3153, OH_MY_HUMANIZE_MAIN-HZ-3183, OH_MY_HUMANIZE_MAIN-HZ-3213, OH_MY_HUMANIZE_MAIN-HZ-3243, OH_MY_HUMANIZE_MAIN-HZ-3273, OH_MY_HUMANIZE_MAIN-HZ-3303, OH_MY_HUMANIZE_MAIN-HZ-3333, OH_MY_HUMANIZE_MAIN-HZ-3363, OH_MY_HUMANIZE_MAIN-HZ-3393, OH_MY_HUMANIZE_MAIN-HZ-3423, OH_MY_HUMANIZE_MAIN-HZ-3453, OH_MY_HUMANIZE_MAIN-HZ-3483, OH_MY_HUMANIZE_MAIN-HZ-3513, OH_MY_HUMANIZE_MAIN-HZ-3543, OH_MY_HUMANIZE_MAIN-HZ-3573, OH_MY_HUMANIZE_MAIN-HZ-3603
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`

---

## Incremental Refresh Addendum - oh-my-humanize/main bf4509d4f

# agent_delta_03 oh-my-humanize main incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-2763 `file` `packages/coding-agent/test/workflow/runner.test.ts`
- cursor: `[_]`
- current_core_role: `packages/coding-agent/test/workflow/runner.test.ts` is the package-level contract suite for `runWorkflow`: it exercises activation persistence, state patch validation/materialization, liveness guards, lifecycle attempt/checkpoint recording, restart prompt resolution, and script-file materialization. For OH_MY_HUMANIZE_MAIN-HZ-2763 specifically, the current file now pins the stop/deadline lifecycle behavior around `signal` versus `nodeAbortSignal` and the runner’s ability to persist an aborted activation/checkpoint even when a node runtime does not cooperate with abort.
- algorithmic_delta_since_old_commit: The targeted delta is the new regression test at `runner.test.ts:564`-`624`: `"checkpoints deadline-aborted lifecycle activations even when the runtime ignores abort"`. It starts a workflow whose `runAgentNode` resolves a `started` latch and then awaits a never-resolving promise, aborts both the scheduler stop controller and the node abort controller, and requires `runWorkflow` to settle within a 100ms `Promise.race` instead of hanging. The expected result is scheduler activation `["build", "aborted"]`, lifecycle attempt `["attempt-node-abort-ignored-1", "stopped", undefined]`, lifecycle activation `["build", "aborted"]`, and checkpoint `attempt-node-abort-ignored-1:checkpoint-1` with `completedActivationIds: []`, `abortedActivationIds: ["activation-1"]`, `frontierNodeIds: ["build"]`, empty state, and identity source mapping. This extends the older deadline-abort coverage at `runner.test.ts:507`-`562`, which only covered a runtime that eventually throws after observing abort.
- current_inputs_outputs_state: Inputs under test are parsed workflow definitions from inline YAML or package-local workflow files, a memory `WorkflowRunStoreHost` from `createHost`, `runWorkflow` options including `runId`, `startNodeId`, `runtimeHost`, optional lifecycle metadata, scheduler `signal`, dedicated `nodeAbortSignal`, `maxRuntimeMs`, and `packageRoot`. Outputs/state are reconstructed from appended custom entries using `reconstructWorkflowRuns` and `reconstructWorkflowFamilies`. For cancellation after a completed node, the file expects the attempt to stop with completed activation `activation-1`, checkpoint frontier `["review"]`, and state `{ work: { summary: "built" } }` (`runner.test.ts:408`-`462`). For node-deadline abort, it expects the activation to be persisted as `aborted`, not `failed`, with frontier reset to the aborted node so restart can retry `build` (`runner.test.ts:538`-`560`, `603`-`622`). For max runtime, `maxRuntimeMs: 1` yields an aborted `build` activation with reason `"workflow max runtime elapsed after 1ms"` and the same retry frontier/checkpoint shape (`runner.test.ts:626` onward). For script files, `packageRoot: dir` plus `script.file: ./scripts/score.py` causes the runtime input to contain `script: 'print("scored")\n'`, `scriptLanguage: "py"`, and the original `scriptPath: "./scripts/score.py"` (`runner.test.ts:889`-`931`).
- new_or_changed_gates_or_invariants: The central invariant added since the old commit is that workflow stop/deadline must not depend on runtime cooperation. A node runtime may ignore `input.signal` and leave its promise pending forever; the runner still has to mark the active activation aborted, stop the lifecycle attempt, and create a restartable checkpoint. The adjacent implementation currently enforces this through `executeAndPersistActivation`, which passes `context.nodeAbortSignal ?? context.signal` into `executeWorkflowNode` and wraps it with `awaitWorkflowNodeExecution` (`src/workflow/runner.ts:373`-`385`). That wrapper registers an abort listener and rejects on a zero-delay timer with the abort reason if the underlying operation does not settle (`src/workflow/runner.ts:432`-`460`). The scheduler then classifies caught errors as aborted when `context.nodeAbortSignal` or `context.signal` is aborted (`src/workflow/scheduler.ts:238`-`246`) and records aborted activations into the stopped frontier (`src/workflow/scheduler.ts:145`-`154`). Another invariant is separation of scheduler stop and node abort: `runner.test.ts:464`-`504` verifies the runtime receives the dedicated `nodeAbortController.signal`, while the scheduler `stopController.signal` can stop downstream scheduling and checkpoint `review`. For max runtime, `workflowRuntimeSignal` combines the timeout signal into both scheduler and node abort paths while preserving the timeout reason (`src/workflow/runner.ts:148`-`186`).
- dependencies_and_callers: The test imports `parseWorkflowDefinition`, lifecycle helpers (`startWorkflowFamily`, `proposeWorkflowChangeRequest`, `approveWorkflowChangeRequest`, `reconstructWorkflowFamilies`), `WorkflowNodeRuntimeHost`/`WorkflowScriptNodeInput`, `reconstructWorkflowRuns`, and `runWorkflow`. The runner delegates scheduling to `runWorkflowScheduler`, node execution to `executeWorkflowNode`, prompt loading to `resolveWorkflowPrompt`, model audit to `resolveWorkflowNodeModel`, state validation/materialization to `validateWorkflowActivationOutput` and `materializeSingleWriteData`, and lifecycle persistence to `appendWorkflowAttemptActivation*`, `requestWorkflowAttemptStop`, and `createWorkflowCheckpoint`. For script-file behavior, `runWorkflow` resolves `node.script.file` under `packageRoot`, rejects escapes outside the package root, prefers frozen resource snapshots when present, and reads the file text before execution (`src/workflow/runner.ts:601`-`640`); `executeScriptNode` then forwards the hydrated code plus original `scriptPath`, language, timeout, resource dir, context, and signal to `runScriptNode` (`src/workflow/node-runtime.ts:134`-`162`). Headless JS workflow script cwd handling is not directly asserted in this assigned file; the applicable adjacent path is the session/eval adapter, where eval requests carry code/language/title but no cwd field (`src/workflow/session-runtime.ts:221`-`238`), and the eval runner uses the supplied `ToolSession.cwd` when cloning settings for the eval tool (`src/workflow/eval-tool-runtime.ts:7`-`31`). Thus this item validates package-root file hydration for workflow scripts, while cwd execution semantics for headless JS are covered outside this file by eval/session-runtime tests.
- edge_cases_or_failure_modes: Covered failure modes include: scheduler stop after a successful activation must checkpoint downstream frontier without running the next node; a dedicated node abort signal must not be confused with the scheduler stop signal; a node that throws after deadline abort must be recorded as `aborted` instead of `failed`; a node that ignores abort and never settles must still produce a stopped attempt/checkpoint instead of hanging; max runtime timeout must abort active work and checkpoint the active node for retry; activation-limited attempts must honor approved frontier mappings; script-only liveness loops must fail fast instead of creating fake progress; invalid activation output must be rejected before state patches persist; package-local script files must require `packageRoot`, stay inside that root, and retain declared language/path when sent to the runtime. The new ignored-abort test specifically guards the hang failure where `Promise.race` would return `"timeout"` and throw `"workflow stop did not checkpoint when the node runtime ignored abort"`.
- validation_or_tests: Current validation is the Bun test suite in `packages/coding-agent/test/workflow/runner.test.ts`. The new delta’s direct validation is `checkpoints deadline-aborted lifecycle activations even when the runtime ignores abort` (`runner.test.ts:564`-`624`), with a 100ms timeout guard around `runWorkflow`. Related existing validations in the same file are `passes a dedicated node abort signal separately from the scheduler stop signal` (`runner.test.ts:464`-`504`), `checkpoints deadline-aborted lifecycle activations instead of failing the attempt` (`runner.test.ts:507`-`562`), `checkpoints lifecycle attempts when max runtime elapses` (`runner.test.ts:626` onward), and `loads package-local script files with their declared language` (`runner.test.ts:889`-`931`). I did not run the tests because the task requested read-only research notes only; inspection was limited to the read-only export.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-2763`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
