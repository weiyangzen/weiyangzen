# agent_15 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- read_only_note: inspected assigned files and recursive directory contents only; no files modified; no build/test commands run because this branch export is read-only.

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-015 `file` `rust-toolchain.toml`
- cursor: `[_]`
- core_role: pins Rust toolchain used by native crates and build tooling.
- algorithmic_behavior: selects `nightly-2026-04-29`, required components, and cross targets in lines 1-4.
- inputs_outputs_state: input is rustup/cargo invocation in workspace; output is deterministic compiler/component resolution.
- gates_or_invariants: Rust build must have `rustfmt`, `clippy`, `rust-analyzer`, Linux GNU and Windows MSVC targets.
- dependencies_and_callers: consumed implicitly by rustup/cargo for `crates/pi-*`.
- edge_cases_or_failure_modes: missing pinned nightly or target prevents native build/check paths.
- validation_or_tests: validated by Cargo/rustup workflows rather than direct tests.
- skip_candidate: `yes: configuration pin, not an executable algorithm itself`

### OH_MY_HUMANIZE_MAIN-HZ-045 `file` `docs/bash-tool-runtime.md`
- cursor: `[_]`
- core_role: authoritative runtime documentation for the coding-agent `bash` tool and user bang-command surface.
- algorithmic_behavior: defines pipeline from schema merge, command fixups, interceptor, cwd validation, artifact allocation, PTY/non-PTY selection, execution, output truncation, async jobs, result mapping, and rendering; see lines 21-88 and 167-231.
- inputs_outputs_state: inputs are `command`, optional `env`, `timeout`, `cwd`, `pty`, `async`; outputs are `AgentToolResult` content/details, errors, artifacts, live updates, or async job IDs.
- gates_or_invariants: env names validate, trailing `head`/`tail` cleanup is conservative, cwd must exist and be a directory, timeout clamps to `[1, 3600]`, PTY requires `pty=true`, UI, and `PI_NO_PTY!="1"` lines 27-31, 60-84.
- dependencies_and_callers: maps to `src/tools/bash.ts`, `bash-pty-selection.ts`, `bash-executor.ts`, `streaming-output.ts`, renderers, and RPC mode lines 279-294.
- edge_cases_or_failure_modes: invalid regex interceptor rules skip; artifact allocation failure is nonfatal; PTY and non-PTY timeout semantics differ; shell session cache is process-scoped; expanded renderer does not automatically load full artifact lines 56-58, 270-277.
- validation_or_tests: doc references runtime files; behavior is covered by bash/tool rendering, async job, and executor test surfaces elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-075 `file` `docs/task-agent-discovery.md`
- cursor: `[_]`
- core_role: documents task subagent discovery, precedence, selection, and availability gates.
- algorithmic_behavior: normalizes agent definitions from frontmatter, merges project/user/plugin/bundled sources, first-wins dedupes by exact `name`, and rediscover agents at task execution time lines 22-39, 57-89, 106-123.
- inputs_outputs_state: inputs are `.omp/agents`, user agent dir, Claude plugin roots, embedded definitions, settings, env guards; outputs are `AgentDefinition[]`, selected agent, or immediate tool error.
- gates_or_invariants: missing `name`/`description` invalidates custom files; bundled parse is fatal; custom parse failures warn and skip; disabled-agent setting, parent `spawns`, `PI_BLOCKED_AGENT`, recursion depth, and plan mode restrict runtime execution lines 90-104, 146-188.
- dependencies_and_callers: references `src/task/discovery.ts`, `agents.ts`, `types.ts`, `index.ts`, `commands.ts`, `executor.ts`, config and prompts lines 7-18.
- edge_cases_or_failure_modes: tool description can be stale because runtime rediscovers; exact name lookup is case-sensitive; bad custom file does not abort discovery; task call cannot provide ad-hoc output schema lines 120-131.
- validation_or_tests: assigned `packages/coding-agent/test/tool-discovery` and task/subagent tests validate adjacent discovery/availability contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-105 `file` `scripts/install.ps1`
- cursor: `[_]`
- core_role: Windows installer workflow for source or binary installation.
- algorithmic_behavior: detects Bun/Git/Git LFS, installs Bun if needed, configures Bash shell path, installs package via Bun or downloads GitHub release binary, then adds install dir to PATH if needed lines 25-306.
- inputs_outputs_state: inputs are `-Source`, `-Binary`, optional `-Ref`, `PI_INSTALL_DIR`, PATH, GitHub releases, repository refs; outputs are global `omp` install, `settings.json` shellPath, PATH mutation, console status.
- gates_or_invariants: source install requires Bun `>=1.3.14`; `-Ref` source install requires git; binary `-Ref` must resolve as a release tag; expected package path must exist lines 59-67, 171-228, 238-264.
- dependencies_and_callers: calls Bun installer, `bun install -g`, `git clone/checkout/lfs`, GitHub API, `Invoke-WebRequest`.
- edge_cases_or_failure_modes: invalid existing settings JSON is overwritten for shell config; missing Bash warns but does not abort; missing release tag suggests `-Source -Ref`; temp clone cleanup runs in `finally`.
- validation_or_tests: install-script behavior is validated operationally by install workflows rather than local unit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-135 `directory` `packages/collab-web/scripts`
- cursor: `[_]`
- core_role: local collaboration web harness scripts for fixture generation, relay server, mock host, and export bundling.
- algorithmic_behavior: `local-relay.ts` multiplexes WebSocket rooms; `mock-host.ts` generates encrypted session state streams and scripted turns; `fixture.ts` builds deterministic transcript/agent fixtures; `build-tool-views.ts` bundles tool-render UI into coding-agent export JS.
- inputs_outputs_state: inputs are CLI port args, room IDs/keys, fixture frames, Bun build entry; outputs are relay URL, mock host frames, generated `tool-views.generated.js`, console link.
- gates_or_invariants: room paths match `/r/<roomId>`; peer IDs and message queues serialize send/receive; build script escapes inline `</script`; relay closes rooms on shutdown.
- dependencies_and_callers: coordinates with `packages/collab-web/src/lib/link.ts`, `@oh-my-pi/pi-wire`, tool renderers, and coding-agent HTML export.
- edge_cases_or_failure_modes: invalid ports fall back/default; fatal close codes and reconnect delays are encoded in fixture; mock host has shutdown handling.
- validation_or_tests: likely exercised by collab UI/manual harness; no assigned direct tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-165 `directory` `python/robomp/scripts`
- cursor: `[_]`
- core_role: operational script folder for robomp.
- algorithmic_behavior: contains `ping.sh`, a minimal shell probe script.
- inputs_outputs_state: shell environment in, ping/probe status out.
- gates_or_invariants: script presence supports simple liveness invocation, not application logic.
- dependencies_and_callers: belongs to robomp package tooling.
- edge_cases_or_failure_modes: shell availability/path permissions can fail.
- validation_or_tests: no assigned direct tests for this script; robomp tests cover application behavior separately.
- skip_candidate: `yes: tiny operational probe directory, not a core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-195 `file` `docs/tools/read.md`
- cursor: `[_]`
- core_role: authoritative contract for the coding-agent `read` tool.
- algorithmic_behavior: defines unified `path` parser for filesystem, URL, internal URL, archive, SQLite, document, image, notebook, and directory reads, including selector grammar and flow lines 20-94.
- inputs_outputs_state: input is `{ path: string }` with suffix selectors; output is `AgentToolResult` text/image blocks plus details such as `resolvedPath`, URL metadata, truncation, display content, summary, and meta source lines 49-64.
- gates_or_invariants: line numbers are 1-indexed, `+` counts >=1, end >= start, unknown colon suffix falls through, archive paths reject `..`, SQLite query params validate, image max is 20 MiB lines 26-47, 121-170, 188-195.
- dependencies_and_callers: references `read.ts`, `path-utils.ts`, `zip.ts`, `sqlite-reader.ts`, `fetch.ts`, `InternalUrlRouter`, notebook conversion, file snapshots, workspace tree lines 5-18.
- edge_cases_or_failure_modes: out-of-bounds line reads return suggestions, binary archive entries return notices, URL HTTP non-ok may return method `failed`, raw SQLite `q=` is not keyword-restricted beyond no bound parameters lines 281-302.
- validation_or_tests: read contracts are defended by read/internal URL, SQLite, archive, and hashline/edit tests across coding-agent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-225 `file` `scripts/session-stats/sync.py`
- cursor: `[_]`
- core_role: ingestion/synchronization pipeline for session stats into SQLite.
- algorithmic_behavior: migrates DB schema, token-counts text, parses hashline edits, extracts warnings/success, discovers session files, ingests assistant/user/tool/edit records, writes normalized records, and decides incremental update actions; key functions include `_migrate`, `parse_hashline_input`, `parse_file`, `_ingest_*`, `write_records`, `discover_sessions`, `decide_action`, `main` lines 184-1076.
- inputs_outputs_state: inputs are session JSONL files, file mtimes/sizes, existing DB state, optional limits; outputs are SQLite rows for sessions/messages/edits/tool results/statistics.
- gates_or_invariants: legacy ranges and anchors parse defensively; duplicate anchors and repeated blocks are detected; existing state prevents unnecessary reingest; token encoding is cached.
- dependencies_and_callers: uses Python `sqlite3`, `tiktoken` when available, pathlib, multiprocessing-style worker parse helpers.
- edge_cases_or_failure_modes: malformed JSON/session entries can skip or partially ingest; missing tokenizer falls back only if code handles it; duplicate/repeated hashline blocks are warning cases.
- validation_or_tests: operational script, no assigned direct tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-255 `directory` `packages/coding-agent/src/dap`
- cursor: `[_]`
- core_role: Debug Adapter Protocol client/session subsystem.
- algorithmic_behavior: `config.ts` normalizes adapter defaults and selects launch/attach adapters; `client.ts` frames DAP messages, spawns adapters, manages pending requests/timeouts, event handlers, reverse requests, sockets; `session.ts` manages lifecycle, breakpoints, status, output ring buffer, cleanup, heartbeat; `types.ts` defines DAP wire/session contracts.
- inputs_outputs_state: inputs are adapter configs, cwd/program/port, DAP JSON frames, breakpoints, abort signals; outputs are session summaries, capabilities, stack/variable/evaluate results, output snapshots.
- gates_or_invariants: adapter command must resolve; pending requests time out; content-length framing must resync on malformed headers; launch slot serializes startup; output caps at 128 KiB; idle cleanup at 10 minutes lines observed in `session.ts` 103-107 and `client.ts` request handling around 373-390.
- dependencies_and_callers: uses Bun spawn/connect, `resolveCommand`, timers, logger, LSP/tool surfaces.
- edge_cases_or_failure_modes: debugpy missing module maps to install hint; adapter exit rejects pending requests; unknown reverse request gets failure response; socket readiness can timeout.
- validation_or_tests: assigned LSP/DAP-adjacent tests cover batching/subagent tool behavior; DAP-specific tests not in assignment.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-285 `directory` `packages/coding-agent/src/tool-discovery`
- cursor: `[_]`
- core_role: deferred tool discovery and BM25 search index.
- algorithmic_behavior: `mode.ts` resolves all vs MCP-only mode with auto threshold 40 excluding the search tool; `tool-index.ts` converts `AiTool`s into weighted documents and searches with BM25+delta scoring lines 51-65, 220-264.
- inputs_outputs_state: inputs are active tool definitions, summaries, sources, query text, settings; outputs are discoverable tool metadata, server summaries, selected names, ranked search results.
- gates_or_invariants: empty query throws; MCP tool names start `mcp__`; schema property keys are extracted through `toolWireSchema`; auto switches to MCP-only when tool count exceeds threshold or legacy MCP discovery setting is enabled.
- dependencies_and_callers: consumed by session/tool registry to expose `search_tool_bm25` and deferred MCP tools; tests in assigned `test/tool-discovery`.
- edge_cases_or_failure_modes: empty index returns no results; schema extraction failures yield empty keys; source filtering can hide tools from search.
- validation_or_tests: `subagent.test.ts`, `tool-index.test.ts`, `initial-tools.test.ts`, `persistence.test.ts` cover mode/index/deferred behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-315 `directory` `packages/coding-agent/test/tool-discovery`
- cursor: `[_]`
- core_role: contract tests for tool discovery.
- algorithmic_behavior: tests cover search index scoring, initial active/deferred tool partitioning, subagent behavior, and persistence/rebuild.
- inputs_outputs_state: inputs are fixture tool definitions/settings/session state; outputs are assertions on search results, active tool names, deferred tool metadata, persistence state.
- gates_or_invariants: validates threshold/mode behavior and that deferred tools can be found without bloating initial tool list.
- dependencies_and_callers: imports `tool-discovery` mode/index and session/tool registry modules.
- edge_cases_or_failure_modes: tests guard against search tool counting itself and stale persistence.
- validation_or_tests: directory itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-345 `file` `crates/pi-iso/src/overlayfs.rs`
- cursor: `[_]`
- core_role: Linux overlayfs isolation backend.
- algorithmic_behavior: probes kernel overlay support, falls back to `fuse-overlayfs`, creates sibling `upper`, `work`, `merged`, records mount flavor, and dispatches correct teardown lines 98-185.
- inputs_outputs_state: inputs are `lower` and `merged` paths; outputs are mounted overlay or `IsoError`, active mount state in `ACTIVE_MOUNTS`.
- gates_or_invariants: Linux-only; `lower` must be existing directory; kernel mount unavailable errors include EPERM/EACCES/ENODEV/ENOENT/EINVAL; paths with NUL rejected lines 111-154, 187-217, 312-345.
- dependencies_and_callers: implements `IsolationBackend`, uses libc mount/umount, `fuse-overlayfs`, `fusermount3/fusermount`.
- edge_cases_or_failure_modes: stop with unknown mount flavor tries kernel then FUSE to avoid leaks; stale dirs removed before start; FUSE mount binary missing surfaces unavailable error.
- validation_or_tests: expected to be covered by crate/backend integration tests or runtime probes.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-375 `file` `crates/pi-natives/src/tokens.rs`
- cursor: `[_]`
- core_role: native NAPI token-counting bridge.
- algorithmic_behavior: exposes `Encoding` enum and `count_tokens`; lazily initializes embedded `o200k_base` and `cl100k_base`; arrays are encoded in parallel with Rayon lines 23-65.
- inputs_outputs_state: input is a string or string array plus optional encoding; output is aggregate `u32` token count.
- gates_or_invariants: default encoding is `O200kBase`; uses ordinary encoding with no special-token handling.
- dependencies_and_callers: consumed by TS token-budget code through pi-natives; depends on `tiktoken-rs`, `napi`, `rayon`.
- edge_cases_or_failure_modes: BPE init panic would fail process; very large aggregate could theoretically overflow `u32`.
- validation_or_tests: token-count behavior likely covered by native/token tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-405 `file` `packages/agent/test/helpers.ts`
- cursor: `[_]`
- core_role: shared test helper for constructing AI messages.
- algorithmic_behavior: `createUserMessage` and `createAssistantMessage` fill timestamps, provider/model metadata, stop reason, and zeroed usage lines 1-32.
- inputs_outputs_state: input text/content and optional stop reason; output typed `UserMessage`/`AssistantMessage`.
- gates_or_invariants: usage cost/tokens default to zero; assistant metadata fixed to mock provider/model.
- dependencies_and_callers: imported by package agent tests.
- edge_cases_or_failure_modes: timestamp uses current wall clock, so tests should not assert exact time.
- validation_or_tests: helper supports validation; not itself a runtime algorithm.
- skip_candidate: `yes: test fixture helper`

### OH_MY_HUMANIZE_MAIN-HZ-435 `file` `packages/ai/test/anthropic-client.test.ts`
- cursor: `[_]`
- core_role: validates Anthropic client request, retry, error, timeout, and abort semantics.
- algorithmic_behavior: uses fetch mocks to assert non-2xx mapping, retry-after handling, `x-should-retry`, retry exhaustion, timeout, caller abort, request assembly, beta URL, and auth header precedence lines 35-200.
- inputs_outputs_state: mocked fetch responses/errors and streaming params; outputs are thrown typed errors or captured HTTP calls.
- gates_or_invariants: fetchOptions cannot override core request fields; defaultHeaders auth is not overwritten; caller abort is not retried.
- dependencies_and_callers: imports AnthropicMessagesClient and error classes from pi-ai provider code.
- edge_cases_or_failure_modes: empty error response body must not invent body; final retry error surfaces.
- validation_or_tests: file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-465 `file` `packages/ai/test/auth-gateway-cross-protocol-caching.test.ts`
- cursor: `[_]`
- core_role: E2E validation for auth gateway prompt-cache continuity across protocol translation.
- algorithmic_behavior: sends OpenAI Responses-shaped request through gateway to Anthropic, then checks cached instructions prefix across responses-to-anthropic translation; helper `callGateway` and `extractAssistantText` lines 78-100.
- inputs_outputs_state: gateway URL/token, model ID, repeated long instructions; output is OpenAI-like response and assistant text.
- gates_or_invariants: requires `checkAuthGatewayE2EAvailable`; cache key must survive cross-protocol mapping.
- dependencies_and_callers: auth gateway server, OpenAI Responses adapter, Anthropic translation path.
- edge_cases_or_failure_modes: unavailable E2E gateway skips/blocks; model defaults from env fallback.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-495 `file` `packages/ai/test/context-overflow.test.ts`
- cursor: `[_]`
- core_role: broad provider E2E/regression test for context overflow detection.
- algorithmic_behavior: generates oversized content, calls providers/models, and asserts `isContextOverflow` for many APIs; includes LM Studio model discovery helpers and OAuth token setup lines 24-204 and test cases from 210 onward.
- inputs_outputs_state: provider credentials, model specs, generated lorem content; outputs overflow result classification and logs.
- gates_or_invariants: context window must be known or discovered; OAuth/env availability gates provider-specific cases.
- dependencies_and_callers: uses `complete`, catalog `buildModel`, bundled models, `$which`, overflow utility.
- edge_cases_or_failure_modes: silent truncation, rate-limit-looking overflow, local LM Studio absence, stale/missing API keys.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-525 `file` `packages/ai/test/handoff.test.ts`
- cursor: `[_]`
- core_role: validates cross-provider context handoff with tools and assistant/tool-result history.
- algorithmic_behavior: defines common weather tool/schema and provider contexts, then exercises `complete` across provider combinations with existing messages/tool states; helper `testProviderHandoff` around line 271 and suites around 369-520.
- inputs_outputs_state: contexts from providers, tool definitions, API keys; output is completed assistant message.
- gates_or_invariants: contexts must serialize/translate between provider dialects without losing tool/result linkage.
- dependencies_and_callers: imports `complete`, catalog models, zod schema, OAuth helpers.
- edge_cases_or_failure_modes: provider credential absence, tool-call dialect mismatch, schema translation incompatibility.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-555 `file` `packages/ai/test/issue-969-repro.test.ts`
- cursor: `[_]`
- core_role: regression test for custom thinking metadata preserving explicit `xhigh`.
- algorithmic_behavior: creates custom OpenAI-compatible model metadata and asserts configured `xhigh` effort is sent, not downgraded lines 39-40.
- inputs_outputs_state: custom model config and request; output captured request reasoning/thinking effort.
- gates_or_invariants: explicit user/config effort overrides generated/default fallback.
- dependencies_and_callers: OpenAI-compatible provider request shaping.
- edge_cases_or_failure_modes: custom models without catalog metadata can accidentally clamp effort.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-585 `file` `packages/ai/test/openai-completions-progress-chunk.test.ts`
- cursor: `[_]`
- core_role: validates OpenAI-compatible stream idle timeout widening and progress-chunk detection.
- algorithmic_behavior: tests model/provider-specific watchdog widening and `isOpenAICompletionsProgressChunk` rejection/acceptance cases for keepalives, usage, finish_reason, content, tool calls, reasoning, refusal lines 81-345.
- inputs_outputs_state: model specs, SSE chunks, mocked fetch; outputs timeout config and progress boolean/result.
- gates_or_invariants: empty keepalives must not reset watchdog; real progress must reset; DeepSeek/GLM/Kimi widening is host/model gated.
- dependencies_and_callers: OpenAI-compatible resolver/stream implementation and catalog model builder.
- edge_cases_or_failure_modes: third-party proxies must not inherit official-host timeouts; role-only or empty deltas are non-progress.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-615 `file` `packages/ai/test/provider-response.test.ts`
- cursor: `[_]`
- core_role: validates normalized provider response metadata propagation.
- algorithmic_behavior: checks status/header/request-id normalization, callback invocation, and `streamSimple` onResponse propagation for OpenAI completions path lines 7-66.
- inputs_outputs_state: Response objects/SSE events and callback spies; output `ProviderResponseMetadata`.
- gates_or_invariants: status, headers, and request IDs must normalize independent of provider path.
- dependencies_and_callers: imports `normalizeProviderResponse`, `notifyProviderResponse`, `streamSimple`.
- edge_cases_or_failure_modes: streaming wrappers can accidentally drop initial HTTP metadata.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-645 `file` `packages/ai/test/umans-login.test.ts`
- cursor: `[_]`
- core_role: validates UMANs login key verification against Anthropic messages endpoint.
- algorithmic_behavior: tests accepted pasted keys and surfaced validation errors lines 5-52.
- inputs_outputs_state: pasted token/API key and mocked endpoint response; output accepted credential or error.
- gates_or_invariants: login must validate through real Anthropic-compatible messages call, not just syntax.
- dependencies_and_callers: UMANs provider login flow.
- edge_cases_or_failure_modes: endpoint error body must be surfaced clearly.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-675 `file` `packages/catalog/test/discovery-null-limits.test.ts`
- cursor: `[_]`
- core_role: regression test for model discovery unknown limits.
- algorithmic_behavior: asserts discovery emits `null` for `contextWindow` and `maxTokens` when unknown lines 4-5.
- inputs_outputs_state: discovered model payload lacking limits; output normalized model with null limits.
- gates_or_invariants: unknown numeric limits must not become zero, undefined, or inherited unsafe values.
- dependencies_and_callers: catalog discovery/build path.
- edge_cases_or_failure_modes: provider payloads omitting limits.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-705 `file` `packages/catalog/test/preferred-dialect.test.ts`
- cursor: `[_]`
- core_role: validates model ID to preferred wire dialect mapping.
- algorithmic_behavior: single suite maps model IDs to dialects correctly lines 4-5.
- inputs_outputs_state: model IDs in, dialect enum/string out.
- gates_or_invariants: dialect selection must be deterministic for provider routing.
- dependencies_and_callers: catalog model identity/dialect helper.
- edge_cases_or_failure_modes: new model ID affixes can be misclassified.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-735 `file` `packages/coding-agent/src/thinking.ts`
- cursor: `[_]`
- core_role: thinking/reasoning level parsing and model-aware effort resolution.
- algorithmic_behavior: parses effort and thinking levels, maps metadata, disables reasoning for off, resolves level against model support, handles `auto`, clamps effort for model capability, and computes provisional auto effort lines 8-167.
- inputs_outputs_state: input strings/settings/model metadata; output `Effort`, `ThinkingLevel`, metadata, disable flag, or configured auto level.
- gates_or_invariants: allowed levels are inherit/off plus `THINKING_EFFORTS`; unsupported model efforts are clamped; `auto` has separate metadata.
- dependencies_and_callers: imports effort/model types and thinking helpers from catalog/ai.
- edge_cases_or_failure_modes: unknown strings return undefined; model absent falls back conservatively.
- validation_or_tests: covered by thinking display/model-thinking and config tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-765 `file` `packages/coding-agent/test/agent-session-force-tool-choice.test.ts`
- cursor: `[_]`
- core_role: validates forced tool-choice lifecycle in `AgentSession`.
- algorithmic_behavior: creates session with mock tools and asserts forced specific tool transitions to none then clears, filtered-out forced choice requeues, and non-active tool forcing throws lines 78-104.
- inputs_outputs_state: session/tool registry and forced choice; output model/tool-choice state transitions or thrown error.
- gates_or_invariants: cannot force inactive tools; filtered tool availability must not lose forced intent.
- dependencies_and_callers: imports `AgentSession`, `SessionManager`, `ModelRegistry`, tool schemas.
- edge_cases_or_failure_modes: active tool filtering mid-dequeue.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-795 `file` `packages/coding-agent/test/async-yield-queue.test.ts`
- cursor: `[_]`
- core_role: validates async job completion yielding into conversation follow-ups.
- algorithmic_behavior: builds async messages, job manager, harness, and tests poll acknowledgement suppression, multi-completion coalescing, and idle flush prompting lines 25-174.
- inputs_outputs_state: async job manager events and streaming state; output staged custom messages/follow-up prompts.
- gates_or_invariants: acknowledged completions should not duplicate; multiple completions in one window coalesce; idle flush fires once.
- dependencies_and_callers: `AsyncJobManager`, `YieldQueue`, `JobTool`.
- edge_cases_or_failure_modes: race between job polling and idle scheduled flush.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-825 `file` `packages/coding-agent/test/codex-auto-reset.test.ts`
- cursor: `[_]`
- core_role: validates Codex auto-reset credit redemption policy.
- algorithmic_behavior: tests timing windows, distance/jitter checks, reserve credits, duplicate block episodes, non-Codex/Spark skip, disabled policy, legacy config migration, stale report and identity matching lines 50-269.
- inputs_outputs_state: usage reports, account identity, settings overrides; output redemption decision and config migration result.
- gates_or_invariants: keep-credit reserve honored; only active matching account and fresh reports qualify; Spark/non-Codex providers excluded.
- dependencies_and_callers: Codex auto-reset policy and settings schema.
- edge_cases_or_failure_modes: reset timestamp jitter, minute-boundary cooldown fallback, undefined credits.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-855 `file` `packages/coding-agent/test/extension-flag-initial-message.test.ts`
- cursor: `[_]`
- core_role: validates extension CLI flags feeding initial message construction.
- algorithmic_behavior: imports arg parsing, extension flag sink, initial message builder, extension runtime/runner, event bus; tests extension-shadowed flags and prompt message boundaries.
- inputs_outputs_state: CLI args and extension flag definitions; output parsed args, extension sink state, initial message.
- gates_or_invariants: extension flags must not consume prompt text incorrectly; initial message includes intended positional content.
- dependencies_and_callers: `parseArgs`, `applyExtensionFlags`, `buildInitialMessage`, extension loader/runner.
- edge_cases_or_failure_modes: unknown or extension-provided string flags near prompt boundaries.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-885 `file` `packages/coding-agent/test/input-controller-compaction-image.test.ts`
- cursor: `[_]`
- core_role: validates image preservation through input controller compaction queue handling.
- algorithmic_behavior: constructs interactive context and image blocks, then asserts compaction queued/restored messages preserve image content and UI helper behavior.
- inputs_outputs_state: queued messages, restored messages, image data; output compaction submission/queue state.
- gates_or_invariants: image content must survive compaction path, not be converted to plain text or dropped.
- dependencies_and_callers: `InputController`, `UiHelpers`, interactive mode types.
- edge_cases_or_failure_modes: restored queued message shape mismatch; image data in mixed content arrays.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-915 `file` `packages/coding-agent/test/issue-2127-repro.test.ts`
- cursor: `[_]`
- core_role: regression test for enhanced paste OSC packet parsing.
- algorithmic_behavior: builds OSC 5522 packets and recorder, feeds `EnhancedPasteController`, and asserts paste/path handling.
- inputs_outputs_state: terminal escape metadata/payload; output paste events/files recorded.
- gates_or_invariants: packet boundaries and metadata must parse without corrupting paste content.
- dependencies_and_callers: `EnhancedPasteController`.
- edge_cases_or_failure_modes: malformed or partial OSC/ST packet sequences.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-945 `file` `packages/coding-agent/test/keybindings-display.test.ts`
- cursor: `[_]`
- core_role: validates display formatting for keybindings.
- algorithmic_behavior: checks rendered keybinding labels/surfaces fit expected conventions.
- inputs_outputs_state: keybinding definitions in, display strings out.
- gates_or_invariants: key display must be stable for UI/help surfaces.
- dependencies_and_callers: keybindings display utilities/components.
- edge_cases_or_failure_modes: modifier ordering and special-key naming.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-975 `file` `packages/coding-agent/test/memories-runtime.test.ts`
- cursor: `[_]`
- core_role: validates runtime memory backend/session integration.
- algorithmic_behavior: creates temp fixtures, models, storage spies, async flush/settle helpers, and tests save/search/runtime behavior across settings and backend availability lines 30-107.
- inputs_outputs_state: session settings, memory operations, model registry; output saved memories, search results, unavailable errors.
- gates_or_invariants: backend-disabled paths return unavailable handlers; async operations settle without leaking dirs.
- dependencies_and_callers: memory runtime, storage, settings, ai model types, `getAgentDbPath`.
- edge_cases_or_failure_modes: async race settlement, temp dir cleanup, backend unavailable.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1005 `file` `packages/coding-agent/test/profile-bootstrap.test.ts`
- cursor: `[_]`
- core_role: validates global profile/alias flag extraction before CLI dispatch.
- algorithmic_behavior: tests `extractProfileFlags` with global flags, extension flags, optional values, `--`, subcommands, explicit launch/acp, unknown flags, missing values lines 6-281.
- inputs_outputs_state: argv token arrays in; stripped args/profile selection/errors out.
- gates_or_invariants: known string flags consume values; subcommand boundary stops global extraction except launch-shaped commands; missing profile/alias value rejects.
- dependencies_and_callers: `parseArgs`, `PROFILE_BOOTSTRAP_BOUNDARY_ARG`, profile bootstrap helper.
- edge_cases_or_failure_modes: unknown extension flags with flag-looking successors, empty resume values, `--` terminator.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1035 `file` `packages/coding-agent/test/sdk-mcp-auto-discovery.test.ts`
- cursor: `[_]`
- core_role: validates SDK session deferred MCP auto-discovery.
- algorithmic_behavior: uses many-tools MCP fixture and asserts auto discovery flips on when tool count crosses threshold; disposal during connect disconnects manager and avoids resurrecting tools lines 28-126.
- inputs_outputs_state: SDK session config, MCP server fixture, settings; output active/deferred tool state and disposal state.
- gates_or_invariants: threshold-triggered discovery must occur only once active count crosses; disposal is final.
- dependencies_and_callers: `createAgentSession`, `SessionManager`, `AuthStorage`, MCP fixture.
- edge_cases_or_failure_modes: async connect/dispose race.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1065 `file` `packages/coding-agent/test/skills.test.ts`
- cursor: `[_]`
- core_role: validates skill discovery, filtering, source toggles, and collision handling.
- algorithmic_behavior: tests direct-directory loading, invalid/missing descriptions, non-recursive scan, sorting, built-in/custom/user/project source toggles, ignored/include glob filters, disabled frontmatter, `disable-model-invocation`, tilde expansion, and first-wins collisions lines 40-443.
- inputs_outputs_state: skill fixture dirs/settings options; output skill list/capability exposure.
- gates_or_invariants: nested skills not recursively loaded; ignored overrides included; `.agents/skills` remains independent of codex/claude toggles.
- dependencies_and_callers: `loadSkills`, `loadSkillsFromDir`, skill capability discovery.
- edge_cases_or_failure_modes: invalid names/long names still load; malformed/missing frontmatter skips.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1095 `file` `packages/coding-agent/test/system-prompt-personality.test.ts`
- cursor: `[_]`
- core_role: validates personality block injection into system prompt.
- algorithmic_behavior: asserts default personality injection, replacement for non-default personality, and omission for `none` lines 17-58.
- inputs_outputs_state: personality setting in; system prompt text out.
- gates_or_invariants: `none` must omit block entirely; custom replaces default rather than appending.
- dependencies_and_callers: system prompt builder.
- edge_cases_or_failure_modes: accidental duplicate personality blocks.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1125 `file` `packages/coding-agent/test/write-acp-fs.test.ts`
- cursor: `[_]`
- core_role: validates write tool routing through ACP filesystem bridge.
- algorithmic_behavior: constructs `ToolSession` with client bridge and tests plain writes route through bridge, plan artifacts write locally, and bracketed `local://...#TAG` headers are local artifacts lines 38-104.
- inputs_outputs_state: requested path/content/session bridge options; output bridge calls or disk writes.
- gates_or_invariants: ACP bridge is used only for plain text workspace writes; local plan/artifact targets bypass bridge.
- dependencies_and_callers: `WriteTool`, local protocol resolver, plan-mode state.
- edge_cases_or_failure_modes: hashline/local URL headers could otherwise be mistaken for bridge targets.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1155 `file` `packages/hashline/src/prefixes.ts`
- cursor: `[_]`
- core_role: strips read/search hashline and diff prefixes before hashline parsing/tokenization.
- algorithmic_behavior: detects hashline headers, line prefixes, diff plus prefixes, truncation notices; opportunistically strips all-content hash prefixes or majority diff pluses; strict mode strips only all hashline-prefixed content lines lines 19-142.
- inputs_outputs_state: string or line array in; cleaned line array out.
- gates_or_invariants: strict stripping requires every content line prefixed; truncation notices are removed when stripping; recursive prefix stripping avoided by `stripOneLeadingHashlinePrefix`.
- dependencies_and_callers: uses `HL_FILE_HASH_LENGTH`; consumed by hashline edit parser.
- edge_cases_or_failure_modes: content beginning with digits/colon can be corrupted if recursive stripping used in wrong context; mixed `+N:` has special handling.
- validation_or_tests: hashline/edit tests cover prefix recovery.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1185 `file` `packages/mnemopi/test/beam-parity.test.ts`
- cursor: `[_]`
- core_role: integration parity tests for Beam memory storage.
- algorithmic_behavior: creates isolated temp DBs and tests construction/parent creation, remember/recall, batch enrichment with per-row source annotations, and veracity threading into storage/scoring lines 26-83.
- inputs_outputs_state: memory records and DB path; output recalled records/scoring metadata.
- gates_or_invariants: `rememberBatch` enriches every row and preserves source/veracity annotations.
- dependencies_and_callers: `BeamMemory` core.
- edge_cases_or_failure_modes: parent dirs absent, isolated file DB cleanup.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1215 `file` `packages/mnemopi/test/mcp-server.test.ts`
- cursor: `[_]`
- core_role: validates mnemopi MCP tool definitions and JSON-RPC server behavior.
- algorithmic_behavior: tests tool definitions, tool call handling, JSON-RPC handlers, and stdio stream processing lines 45-90 plus helpers lines 24-34.
- inputs_outputs_state: JSON-RPC messages/tool args; output tool responses and protocol frames.
- gates_or_invariants: MCP schema/tool names must match server handlers; stdio parser handles streams.
- dependencies_and_callers: `callToolJson`, `handleJsonRpc`, `runStdio`, MCP tools.
- edge_cases_or_failure_modes: malformed JSON-RPC and temp data dir cleanup.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1245 `file` `packages/mnemopi/test/weibull-mmr-intent.test.ts`
- cursor: `[_]`
- core_role: validates memory recall scoring helpers.
- algorithmic_behavior: tests Weibull decay, query intent classification/weight adjustment, and MMR reranking lines 11-121.
- inputs_outputs_state: timestamps/query/results in; decay weights/reranked results out.
- gates_or_invariants: intent changes scoring weights; MMR balances relevance/diversity.
- dependencies_and_callers: `mmrRerank`, `adjustWeights`, `classifyIntent`, Weibull helpers.
- edge_cases_or_failure_modes: extreme age/score inputs and duplicate-like results.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1275 `file` `packages/snapcompact/research/exp03_numhard.py`
- cursor: `[_]`
- core_role: research experiment for numeric-hard snapcompact evaluation.
- algorithmic_behavior: masks numeric text, renders hard text chunks to PNG, parses conditions, runs model chunks, computes numeric F1 stats, loads baseline, saves samples, and drives experiment from `main` lines 59-381.
- inputs_outputs_state: model/condition/chunk ranges/cache/output dirs; output JSON records, metrics, sample images.
- gates_or_invariants: numeric subset detection gates F1; chunk rendering caches PNGs; CLI args drive model/length/condition grid.
- dependencies_and_callers: PIL/image rendering, model runner context, filesystem caches.
- edge_cases_or_failure_modes: non-numeric golds excluded from numeric subset; missing baseline/model can fail experiment.
- validation_or_tests: research script, no automated assigned tests.
- skip_candidate: `yes: research experiment, not production runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1305 `file` `packages/snapcompact/research/snapcompact_activation_probe.py`
- cursor: `[_]`
- core_role: research probe comparing hidden activations between image/text prompt variants.
- algorithmic_behavior: computes centered Gram, linear CKA, paired cosine, builds prompts, extracts hidden features, runs main analysis lines 40-224.
- inputs_outputs_state: model/processor/images/text prompts; output layer similarity metrics.
- gates_or_invariants: tensors are moved to device; features sampled consistently across conditions.
- dependencies_and_callers: numpy, PIL, ML model/processor stack.
- edge_cases_or_failure_modes: GPU/device/model availability and incompatible hidden-state shapes.
- validation_or_tests: research script.
- skip_candidate: `yes: research-only analysis script`

### OH_MY_HUMANIZE_MAIN-HZ-1335 `file` `packages/snapcompact/research/snapcompact_viz_glyph_matrix.py`
- cursor: `[_]`
- core_role: research visualization generator for snapcompact glyph/activation matrices.
- algorithmic_behavior: loads fonts, normalizes quantiles, computes token boxes and answer bounding boxes, draws activation overlays, layer bars, scar strips, top token tables, then renders output images lines 43-396.
- inputs_outputs_state: source metrics file/output dir in; annotated visualization PNGs out.
- gates_or_invariants: heat normalization uses quantile; answer/token overlays rely on grid geometry.
- dependencies_and_callers: PIL, numpy, filesystem.
- edge_cases_or_failure_modes: font fallback, missing source arrays, token index bounds.
- validation_or_tests: research script.
- skip_candidate: `yes: research visualization, not runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1365 `file` `packages/tui/bench/parse-key.ts`
- cursor: `[_]`
- core_role: benchmark comparing JS and native key parser behavior/performance.
- algorithmic_behavior: defines key samples, runs 2000 iterations, compares mismatches, times JS/native parse loops lines 5-98.
- inputs_outputs_state: static terminal key sequences in; console benchmark timings/mismatch count out.
- gates_or_invariants: native parser should match JS parser for samples before performance comparison is meaningful.
- dependencies_and_callers: TUI key parser and native parser.
- edge_cases_or_failure_modes: sample coverage may miss terminal-specific sequences.
- validation_or_tests: benchmark, not test gate.
- skip_candidate: `yes: benchmark harness, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1395 `file` `packages/tui/test/deccara.test.ts`
- cursor: `[_]`
- core_role: validates DECCARA rectangular background fill detection/planning and TUI integration.
- algorithmic_behavior: tests support detection, encoding, line analysis, fill planning, and integration with virtual terminal around lines 121-285.
- inputs_outputs_state: virtual terminal render output and env patches; output escape sequences/fill plans.
- gates_or_invariants: DECCARA only used when supported and beneficial; background rectangles must not corrupt text.
- dependencies_and_callers: TUI DECCARA helpers, `VirtualTerminal`.
- edge_cases_or_failure_modes: environment opt-outs, resize settle, ANSI background parsing.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1425 `file` `packages/tui/test/markdown-incremental-lex.test.ts`
- cursor: `[_]`
- core_role: validates incremental markdown streaming lexer/render cache stability.
- algorithmic_behavior: renders cold text at growing prefixes and asserts final/growth outputs match for prose, fences, lists, headings, mixed documents lines 19-76.
- inputs_outputs_state: markdown text and width in; rendered lines out.
- gates_or_invariants: incremental streaming must converge to same rendering as full cold render.
- dependencies_and_callers: `Markdown`, render cache, default theme.
- edge_cases_or_failure_modes: partial fenced blocks/list structures while streaming.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1455 `file` `packages/tui/test/tab-bar.test.ts`
- cursor: `[_]`
- core_role: validates tab bar rendering and width handling.
- algorithmic_behavior: tests `TabBar` output visible widths with ANSI theme and tab states lines 1-120.
- inputs_outputs_state: tab labels/theme/active state in; rendered terminal lines out.
- gates_or_invariants: visible width must ignore ANSI styling; active/inactive styling stable.
- dependencies_and_callers: `TabBar`, `visibleWidth`.
- edge_cases_or_failure_modes: long labels and ANSI sequence width.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1485 `file` `packages/utils/src/dirs.ts`
- cursor: `[_]`
- core_role: central directory/profile/path resolution utility for the workspace.
- algorithmic_behavior: normalizes profiles, resolves config roots, agent dirs, XDG dirs, project dirs, plugin paths, caches, logs, sessions, MCP/SSH config paths, install ID generation, and test resets lines 20-855.
- inputs_outputs_state: env vars (`OMP_PROFILE`, `PI_PROFILE`, dirs), cwd, home, active profile; output absolute paths and cached install ID.
- gates_or_invariants: profile names match safe regex and avoid Windows reserved names; `pathIsWithin` and relative path helpers enforce containment; profile-derived agent dir logic separates overrides.
- dependencies_and_callers: used by nearly every package for config/cache/log/session path discovery.
- edge_cases_or_failure_modes: macOS path standardization, env snapshot refresh, invalid profile, missing install-id file creates one.
- validation_or_tests: profile isolation/bootstrap tests validate key behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1515 `file` `packages/utils/src/worker-host.ts`
- cursor: `[_]`
- core_role: records worker host entrypoint and manages worker inbox for CLI re-entry workers.
- algorithmic_behavior: `declareWorkerHostEntry` captures `Bun.main`; `workerHostEntry` returns it; `installWorkerInbox` wires a port listener into promise-backed receive queue; `consumeWorkerInbox` returns pending inbox once lines 9-90.
- inputs_outputs_state: worker port messages in; received message promises/outbox sends out.
- gates_or_invariants: only one pending inbox; worker host entry is nullable outside CLI host.
- dependencies_and_callers: CLI worker dispatch and spawn sites described in AGENTS rules.
- edge_cases_or_failure_modes: consuming inbox before install returns null; multiple installs can replace state.
- validation_or_tests: worker-host smoke tests and CLI smoke probe cover contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1545 `file` `python/omp-rpc/tests/test_user_group.py`
- cursor: `[_]`
- core_role: validates Python RPC client process user/group argument threading.
- algorithmic_behavior: patches process start, captures kwargs, and tests default `None`, explicit user/group, and `extra_groups=None` distinct from empty list lines 14-44.
- inputs_outputs_state: `RpcClient` start kwargs in; captured subprocess args out.
- gates_or_invariants: absence of user/group must pass `None`; empty extra groups must not be conflated with unspecified.
- dependencies_and_callers: `omp_rpc.RpcClient`.
- edge_cases_or_failure_modes: platform/subprocess APIs may treat empty group list differently.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1575 `file` `python/robomp/tests/test_autoclose.py`
- cursor: `[_]`
- core_role: validates robomp issue autoclose scheduler.
- algorithmic_behavior: builds fake GitHub/database/settings, seeds close timestamps, and tests scheduler close behavior plus disabled cases for feature off or zero hours lines 16-172.
- inputs_outputs_state: DB issues/reactions/settings in; GitHub close/comment calls and DB state out.
- gates_or_invariants: scheduler disabled when feature off or hours zero; close conditions depend on configured age/reaction state.
- dependencies_and_callers: `AutocloseScheduler`, `Database`, GitHub client errors/reactions.
- edge_cases_or_failure_modes: GitHub errors, stale close timestamps, reaction info mismatch.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1605 `directory` `packages/coding-agent/src/cli/__tests__`
- cursor: `[_]`
- core_role: CLI workflow command tests.
- algorithmic_behavior: contains `workflow-cli.test.ts`, validating workflow CLI parsing/dispatch behavior.
- inputs_outputs_state: CLI args/config in; workflow command outputs/errors out.
- gates_or_invariants: CLI workflow surface must keep expected command options and validation errors.
- dependencies_and_callers: coding-agent CLI workflow modules.
- edge_cases_or_failure_modes: malformed args, missing files, command boundary parsing.
- validation_or_tests: directory itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1635 `directory` `packages/coding-agent/src/modes/setup-wizard`
- cursor: `[_]`
- core_role: interactive setup wizard UI and state flow.
- algorithmic_behavior: selects scenes, marks completion, runs overlay; scenes implement splash/starfield, providers, sign-in tabs, theme selection/preview, glyph selection, web-search settings, and outro; `wizard-overlay.ts` manages phase transitions/dissolve frames.
- inputs_outputs_state: interactive context/settings/user key events in; settings writes and rendered overlay frames out.
- gates_or_invariants: `OMP_SKIP_SETUP`-style env skip handled; scene controllers return done/skipped; outro duration is 1200 ms; splash tick is 33 ms.
- dependencies_and_callers: TUI components, settings schema, provider auth tabs, theme/glyph config.
- edge_cases_or_failure_modes: narrow terminal clamps lines; sign-in prompts require copyable input; transition phase timing.
- validation_or_tests: setup wizard likely covered by UI/component tests; `outro.ts` separately assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1665 `file` `crates/pi-ast/src/language/mod.rs`
- cursor: `[_]`
- core_role: language registry and extension mapping for AST parsing.
- algorithmic_behavior: enumerates supported languages, maps extensions via `extensions(lang)` around line 552, and likely exposes parser/language selection helpers.
- inputs_outputs_state: file extension/language enum in; parser support metadata out.
- gates_or_invariants: extension lists must be stable and non-overlapping where dispatch depends on them.
- dependencies_and_callers: AST grep/summarization/language detection.
- edge_cases_or_failure_modes: extensionless files or ambiguous extensions.
- validation_or_tests: AST/language tests elsewhere validate parser selection.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1695 `file` `packages/ai/src/auth-gateway/http.ts`
- cursor: `[_]`
- core_role: shared HTTP/auth helpers for auth gateway.
- algorithmic_behavior: builds JSON responses, resolves peer address, timing-safe compares bearer tokens, captures passthrough headers, resolves prompt cache key from body/headers, and applies CORS lines 14-185.
- inputs_outputs_state: Request/Headers/body/tokens in; Response/header maps/cache key/auth boolean out.
- gates_or_invariants: token comparison is timing-safe; authorization requires configured token match; cache key reads selected headers and body fields.
- dependencies_and_callers: auth gateway CLI/server and cross-protocol cache tests.
- edge_cases_or_failure_modes: missing/empty auth header, malformed body cache key, CORS wrapping existing response.
- validation_or_tests: assigned auth gateway caching test and CLI tests cover consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1725 `file` `packages/ai/src/providers/anthropic-messages-server.ts`
- cursor: `[_]`
- core_role: Anthropic Messages server-side wire parser/encoder.
- algorithmic_behavior: parses Anthropic request bodies into internal context/tools/options, walks user/assistant content, maps tool choice/cache retention, encodes assistant response and SSE stream frames, and formats errors lines 81-741.
- inputs_outputs_state: Anthropic request JSON/headers and internal assistant messages in; parsed request, JSON response, SSE bytes, or error response out.
- gates_or_invariants: unknown block types warn once; non-base64 image sources warn; cache_control is validated; stream ping interval is 15 seconds.
- dependencies_and_callers: Anthropic-compatible auth gateway/server, pi-ai message types.
- edge_cases_or_failure_modes: unsupported image source, unknown content blocks, missing stop reason/usage defaulting.
- validation_or_tests: Anthropic client/server and cross-protocol handoff tests cover wire behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1755 `file` `packages/ai/src/providers/openai-responses-wire.ts`
- cursor: `[_]`
- core_role: OpenAI Responses API wire type definitions.
- algorithmic_behavior: declares interfaces/unions for response objects, events, input/output items, tools, tool choices, reasoning, usage, and create params lines 17-6375.
- inputs_outputs_state: TypeScript compile-time inputs are wire JSON structures; outputs are typed contracts for request/response code.
- gates_or_invariants: status/tool/event string unions encode provider API contract; `ReasoningEffort` includes `xhigh` and nullable forms near line 6354.
- dependencies_and_callers: OpenAI Responses provider, request transformers, schema normalizers, auth gateway translations.
- edge_cases_or_failure_modes: API drift can make generated/static types stale.
- validation_or_tests: OpenAI Responses/Codex/schema tests validate runtime consumers.
- skip_candidate: `yes: mostly wire contract/types, little executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1785 `file` `packages/ai/src/registry/huggingface.ts`
- cursor: `[_]`
- core_role: Hugging Face provider registry/login definition.
- algorithmic_behavior: opens OAuth/login flow, validates with router API model, and exports provider definition with auth/API URLs lines 5-51.
- inputs_outputs_state: OAuth controller/key in; API key/provider definition out.
- gates_or_invariants: validation model is `openai/gpt-oss-120b`; API base URL fixed to router endpoint.
- dependencies_and_callers: provider registry and login flow.
- edge_cases_or_failure_modes: OAuth failure or validation model unavailable.
- validation_or_tests: provider registry/login tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1815 `file` `packages/ai/src/registry/types.ts`
- cursor: `[_]`
- core_role: provider registry type contract.
- algorithmic_behavior: defines key resolver and provider definition shapes for login/auth/catalog metadata.
- inputs_outputs_state: provider implementations conform to interfaces; registry consumers receive typed definitions.
- gates_or_invariants: provider definitions must supply IDs, auth strategy, API base/model metadata as required by interface.
- dependencies_and_callers: all provider registry modules.
- edge_cases_or_failure_modes: type-only; runtime errors arise in implementors.
- validation_or_tests: registry tests validate concrete providers.
- skip_candidate: `yes: type contract only`

### OH_MY_HUMANIZE_MAIN-HZ-1845 `file` `packages/ai/src/utils/foundry.ts`
- cursor: `[_]`
- core_role: feature flag helper for Foundry behavior.
- algorithmic_behavior: `isFoundryEnabled` returns true based on environment/config toggle lines 3-8.
- inputs_outputs_state: env/config state in; boolean out.
- gates_or_invariants: centralizes flag interpretation.
- dependencies_and_callers: provider/model paths that gate Foundry-specific behavior.
- edge_cases_or_failure_modes: unset or malformed flag defaults false.
- validation_or_tests: feature consumers tested elsewhere.
- skip_candidate: `yes: tiny flag helper`

### OH_MY_HUMANIZE_MAIN-HZ-1875 `file` `packages/catalog/src/discovery/openai-compatible.ts`
- cursor: `[_]`
- core_role: generic OpenAI-compatible `/models` discovery implementation.
- algorithmic_behavior: normalizes base URL, fetches `/models`, validates payload as array or envelope, extracts nested model records, maps each through provider-specific mapper, and filters nulls lines 101-215.
- inputs_outputs_state: base URL, fetch impl, headers, mapper context in; discovered model records/specs out.
- gates_or_invariants: schema validates `id` and optional metadata; URL path normalization appends `/models`; unsupported payload returns empty/null behavior.
- dependencies_and_callers: catalog provider descriptors/resolvers for OpenAI-compatible providers.
- edge_cases_or_failure_modes: providers wrap arrays in nested `data`; null limits handled by assigned catalog test.
- validation_or_tests: `discovery-null-limits.test.ts` and provider discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1905 `file` `packages/coding-agent/src/autolearn/controller.ts`
- cursor: `[_]`
- core_role: decides when to nudge the model toward learning/skill management.
- algorithmic_behavior: builds autolearn instructions depending on available tools and tracks tool-call count threshold through `AutoLearnController`.
- inputs_outputs_state: available manageSkill/learn booleans and tool-call events in; optional instruction/nudge state out.
- gates_or_invariants: default minimum tool calls is 5; no nudge if required capability unavailable.
- dependencies_and_callers: prompt/system instruction assembly and tool-call lifecycle.
- edge_cases_or_failure_modes: repeated nudges avoided by controller state.
- validation_or_tests: memory/skills/autolearn tests likely cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1935 `file` `packages/coding-agent/src/cli/auth-gateway-cli.ts`
- cursor: `[_]`
- core_role: CLI command implementation for auth gateway serve/token/status/check.
- algorithmic_behavior: manages token file, generates secure token, starts server, prints token/status, checks broker snapshot credentials, probes strict completion candidates with retries/timeouts, formats credential completion status lines 34-608.
- inputs_outputs_state: CLI action/flags, broker config, token file, provider credentials in; server process/token/status/check output out.
- gates_or_invariants: actions limited to serve/token/status/check; strict probe max candidates 4, per-attempt timeout 15s, skips certain APIs, retries model errors lines 358-391.
- dependencies_and_callers: auth broker client, AI completion probe, auth gateway HTTP/server helpers.
- edge_cases_or_failure_modes: token creation race uses exclusive create; broker snapshot fetch failure; retryable model errors can move to next candidate.
- validation_or_tests: auth gateway and usage/CLI tests cover portions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1965 `file` `packages/coding-agent/src/cli/usage-cli.ts`
- cursor: `[_]`
- core_role: renders usage limits/history with privacy redaction.
- algorithmic_behavior: builds redaction map, finds distinguishing infixes, aggregates limit statuses, formats bars/amounts/accounts, computes provider window stats, renders breakdown/history sparklines, collects stored accounts, and runs command lines 56-681.
- inputs_outputs_state: usage reports/history/auth storage/flags in; human or JSON usage output out.
- gates_or_invariants: identities are masked consistently; status aggregation preserves most severe; history uses fixed spark width.
- dependencies_and_callers: usage provider reports, auth storage, terminal color formatting.
- edge_cases_or_failure_modes: multiple accounts with overlapping identifiers require distinguishing infixes; unreported accounts listed separately.
- validation_or_tests: usage CLI tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1995 `file` `packages/coding-agent/src/commands/shell.ts`
- cursor: `[_]`
- core_role: shell command registration wrapper.
- algorithmic_behavior: exports a CLI `Command` subclass for shell-related invocation.
- inputs_outputs_state: CLI command context in; command handler execution out.
- gates_or_invariants: integrates with command registry conventions.
- dependencies_and_callers: CLI command registry.
- edge_cases_or_failure_modes: minimal wrapper; behavior mainly in delegated handler.
- validation_or_tests: CLI tests cover command registration.
- skip_candidate: `yes: thin command wrapper`

### OH_MY_HUMANIZE_MAIN-HZ-2025 `file` `packages/coding-agent/src/config/prompt-templates.ts`
- cursor: `[_]`
- core_role: loads and expands prompt templates from configured directories.
- algorithmic_behavior: detects inline arg placeholders, appends fallback args when absent, loads templates from dirs, validates/sorts them, and expands template names into prompt text lines 17-185.
- inputs_outputs_state: template source files and arguments in; `PromptTemplate[]` or expanded prompt text out.
- gates_or_invariants: shell/template placeholder regexes decide fallback; directory load failures handled; duplicate/invalid templates filtered.
- dependencies_and_callers: prompt command/config subsystem.
- edge_cases_or_failure_modes: unknown template reference, templates without placeholders needing fallback args.
- validation_or_tests: prompt/template tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2055 `file` `packages/coding-agent/src/discovery/gemini.ts`
- cursor: `[_]`
- core_role: imports Gemini CLI configuration into coding-agent discovery model.
- algorithmic_behavior: loads MCP servers, settings, context files, extensions, extension modules, and system prompt for provider id `gemini`; source priority/display metadata lines 39-319.
- inputs_outputs_state: Gemini config dirs/settings files/extensions in; discovered MCP/context/settings/system prompt records out.
- gates_or_invariants: project/user levels are tracked; extension dirs read only valid extension metadata; load results carry errors.
- dependencies_and_callers: discovery framework/provider adapters.
- edge_cases_or_failure_modes: missing config files, invalid JSON, extension module load errors.
- validation_or_tests: discovery/profile isolation tests cover adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2085 `file` `packages/coding-agent/src/eval/types.ts`
- cursor: `[_]`
- core_role: shared eval tool type definitions.
- algorithmic_behavior: defines eval language/status/output/result/detail shapes.
- inputs_outputs_state: eval runtimes produce objects conforming to these types.
- gates_or_invariants: language limited to Python or JS.
- dependencies_and_callers: eval tools and renderers.
- edge_cases_or_failure_modes: type-only; runtime validation in eval implementation.
- validation_or_tests: eval tests elsewhere.
- skip_candidate: `yes: type contract only`

### OH_MY_HUMANIZE_MAIN-HZ-2115 `file` `packages/coding-agent/src/hindsight/transcript.ts`
- cursor: `[_]`
- core_role: extracts session transcript messages for hindsight processing.
- algorithmic_behavior: reads session manager context, maps user/assistant messages, extracts text from string or content blocks lines 14-71.
- inputs_outputs_state: session manager/context messages in; `HindsightMessage[]` out.
- gates_or_invariants: only user and assistant text is extracted; non-text blocks ignored.
- dependencies_and_callers: hindsight analysis/reporting feature.
- edge_cases_or_failure_modes: missing content or nonstandard content arrays yield empty text.
- validation_or_tests: session transcript/hindsight tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2145 `file` `packages/coding-agent/src/lsp/types.ts`
- cursor: `[_]`
- core_role: LSP tool and protocol type/schema definitions.
- algorithmic_behavior: declares tool params via `lspSchema`, diagnostics, locations, workspace edits, code actions, symbols, hover, linter client, server/client JSON-RPC contracts lines 8-437.
- inputs_outputs_state: LSP JSON-RPC/tool payloads in; typed TS contracts out.
- gates_or_invariants: diagnostic severity constrained to 1-4; operation names and symbol kinds map to protocol constants.
- dependencies_and_callers: LSP client/tool implementation and tests.
- edge_cases_or_failure_modes: type drift with language-server protocol.
- validation_or_tests: assigned `subagent-lsp.test.ts` and `lsp-batching.test.ts`.
- skip_candidate: `yes: protocol/type contract, not executable logic`

### OH_MY_HUMANIZE_MAIN-HZ-2175 `file` `packages/coding-agent/src/memory-backend/runtime.ts`
- cursor: `[_]`
- core_role: adapts memory backend operations into runtime context callable by prompts/tools.
- algorithmic_behavior: creates `MemoryRuntimeContext` with search/save functions, session binding, and unavailable fallback functions lines 10-64.
- inputs_outputs_state: backend operation context/session in; runtime context with search/save out.
- gates_or_invariants: unavailable backend returns structured unavailable search/save behavior.
- dependencies_and_callers: memory backend implementations and session memory integration.
- edge_cases_or_failure_modes: backend ID missing or disabled.
- validation_or_tests: assigned `memories-runtime.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2205 `file` `packages/coding-agent/src/plan-mode/state.ts`
- cursor: `[_]`
- core_role: minimal plan-mode state interface.
- algorithmic_behavior: type-only shape for plan mode state, including mode/activity fields.
- inputs_outputs_state: components consume/produce objects matching interface.
- gates_or_invariants: state fields define plan-mode availability.
- dependencies_and_callers: write ACP test imports it for session fixture.
- edge_cases_or_failure_modes: none in this file.
- validation_or_tests: plan-mode tests elsewhere.
- skip_candidate: `yes: tiny type declaration`

### OH_MY_HUMANIZE_MAIN-HZ-2235 `file` `packages/coding-agent/src/session/snapcompact-inline.ts`
- cursor: `[_]`
- core_role: converts large text context blocks into inline snapcompact image frames to save tokens.
- algorithmic_behavior: estimates candidate savings, budgets provider image frames, skips errors/images, gates minimum tool result tokens, plans swaps, caches rendered frames by hash, replaces tool results/system prompt sections with images, and reports savings lines 51-542.
- inputs_outputs_state: context, model, snapcompact options/system prompt in; transformed context and savings estimates out.
- gates_or_invariants: model must support images; provider image budget must remain; tool result min is 3000 tokens; system prompt max frames 6; savings margin 0.9 lines 51-80, 178-205, 417-525.
- dependencies_and_callers: `snapcompact`, token counting, session context transform pipeline.
- edge_cases_or_failure_modes: existing images exhaust budget; error tool results skipped; stale cache entries removed for non-live tool call IDs.
- validation_or_tests: compaction/image tests and snapcompact research support behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2265 `file` `packages/coding-agent/src/task/discovery.ts`
- cursor: `[_]`
- core_role: runtime implementation of task agent discovery.
- algorithmic_behavior: loads agents from directories, merges nearest project `.omp`, user `.omp`, plugin roots, and bundled agents, dedupes first-wins, and provides exact-name lookup lines 25-122.
- inputs_outputs_state: cwd/home and filesystem/plugin roots in; discovery result and `AgentDefinition[]` out.
- gates_or_invariants: only `.omp` config source is accepted; missing dirs become empty; bad files warn/skip; bundled agents appended after custom/plugin.
- dependencies_and_callers: task tool executor and task docs.
- edge_cases_or_failure_modes: lexicographic file ordering affects first-wins collisions; runtime rediscovery may differ from initial description.
- validation_or_tests: task-agent discovery docs and task/tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2295 `file` `packages/coding-agent/src/tools/bash-pty-selection.ts`
- cursor: `[_]`
- core_role: predicate for local interactive bash PTY eligibility.
- algorithmic_behavior: `canUseInteractiveBashPty` returns true only when input `pty` is true, `PI_NO_PTY` is not `1`, and context has UI plus `ui` object lines 4-14.
- inputs_outputs_state: requested pty flag/context/env in; boolean out.
- gates_or_invariants: no UI or env opt-out forces non-PTY fallback.
- dependencies_and_callers: `BashTool` PTY/non-PTY selection documented in bash runtime.
- edge_cases_or_failure_modes: requested PTY in print/RPC mode falls back with notice.
- validation_or_tests: bash runtime/tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2325 `file` `packages/coding-agent/src/tools/jtd-to-typescript.ts`
- cursor: `[_]`
- core_role: converts JSON Type Definition schemas into TypeScript type strings.
- algorithmic_behavior: maps primitive JTD types, recursively converts enum/elements/properties/optionalProperties/values/discriminator/definitions, and exports `jtdToTypeScript` lines 19-136.
- inputs_outputs_state: JTD schema object in; TS type declaration/string out.
- gates_or_invariants: unknown/empty schema falls back to `unknown`-like representation; optional props marked optional.
- dependencies_and_callers: tool schema/documentation generation.
- edge_cases_or_failure_modes: recursive definitions and discriminator mappings.
- validation_or_tests: tool/schema generation tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2355 `file` `packages/coding-agent/src/tools/write.ts`
- cursor: `[_]`
- core_role: implementation and renderer for the model-facing write tool.
- algorithmic_behavior: validates schema, strips accidental hashline headers, snapshots existing content, routes ACP bridge writes, handles archive/SQLite write targets, normalizes archive subpaths, writes files, may chmod shebang files executable, builds render previews and diagnostics lines 71-1064.
- inputs_outputs_state: `path`, `content`, session cwd/settings/bridge in; file/archive/sqlite side effects and tool result/details out.
- gates_or_invariants: archive subpaths reject traversal; SQLite target parser controls table/key forms; ACP bridge excluded for local plan/artifact URLs; shebang chmod note appended.
- dependencies_and_callers: path utils, archive utilities, SQLite writer, local protocol, session snapshot store, render utils.
- edge_cases_or_failure_modes: loose hashline header stripping, archive path not found, bridge failure, executable chmod failure, streaming preview truncation.
- validation_or_tests: assigned `write-acp-fs.test.ts` and write tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2385 `file` `packages/coding-agent/src/utils/event-bus.ts`
- cursor: `[_]`
- core_role: small pub/sub event bus for extension/runtime communication.
- algorithmic_behavior: stores handlers by event name, emits payloads, unsubscribes via returned cleanup lines 3-33.
- inputs_outputs_state: event names/payloads/handlers in; callback side effects out.
- gates_or_invariants: handler sets are isolated per event; unsubscribe removes exact handler.
- dependencies_and_callers: extension runtime tests and controllers.
- edge_cases_or_failure_modes: handler exceptions if not caught by caller.
- validation_or_tests: extension flag initial message test imports it.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2415 `file` `packages/coding-agent/src/workflow/dsl.ts`
- cursor: `[_]`
- core_role: compiles workflow DSL blocks into normalized graph/contracts.
- algorithmic_behavior: validates block records, compiles nodes/edges, imports/namespaces external modules, rewrites prompt/resource references, merges capabilities/contracts, computes graph boundaries, sorts edges, and throws `WorkflowDslError` on invalid shape lines 1-652.
- inputs_outputs_state: DSL block and external modules/options in; compile result with nodes/edges/entry/exit/contracts out.
- gates_or_invariants: required fields must be arrays/strings/records; external IDs are namespaced; resource paths joined safely; edge conditions are rewritten by node prefix.
- dependencies_and_callers: workflow freeze/package loader and CLI.
- edge_cases_or_failure_modes: cyclic/invalid references, missing external entrypoints/exits, non-record blocks.
- validation_or_tests: assigned `artifact-freeze.test.ts` covers workflow resources/policies; DSL tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2445 `file` `packages/coding-agent/test/cli/ttsr-cli.test.ts`
- cursor: `[_]`
- core_role: validates TTSR CLI command behavior.
- algorithmic_behavior: tests context inference/source matching, JSON output, AST matching, list shape, directory scan, gitignore settings, hidden files, size/binary skip, and exported sources lines 87-490.
- inputs_outputs_state: temp rules/snippets/dirs and CLI args in; stdout/exit behavior out.
- gates_or_invariants: explicit `--source text` prevents tool-scoped rule; project gitignore respected unless disabled; large/binary files skipped.
- dependencies_and_callers: TTSR CLI runner, settings, project dirs.
- edge_cases_or_failure_modes: AST-only whitespace spans, hidden workflow files, binary-looking files.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2475 `file` `packages/coding-agent/test/core/python-kernel-session.test.ts`
- cursor: `[_]`
- core_role: validates Python kernel reuse/disposal modes.
- algorithmic_behavior: tests session-mode reuse, per-call kernel creation/disposal, and reset behavior lines 42-83.
- inputs_outputs_state: executePython mode/reset flags in; kernel lifecycle calls/results out.
- gates_or_invariants: session mode reuses same kernel until reset; per-call mode disposes after call.
- dependencies_and_callers: Python execution kernel session manager.
- edge_cases_or_failure_modes: reset while active, disposal leaks.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2505 `file` `packages/coding-agent/test/discovery/profile-isolation.test.ts`
- cursor: `[_]`
- core_role: validates user-level config discovery follows active profile.
- algorithmic_behavior: tests slash commands and skills resolve from profile-specific agent dir instead of default lines 41-97.
- inputs_outputs_state: temp profile dirs/settings/env in; discovered commands/skills out.
- gates_or_invariants: active profile must isolate native config roots.
- dependencies_and_callers: utils dir/profile resolution, discovery/skills systems.
- edge_cases_or_failure_modes: stale cached dirs/env snapshots.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2535 `file` `packages/coding-agent/test/internal-urls/local-protocol.test.ts`
- cursor: `[_]`
- core_role: validates `local://` internal URL safety and root resolution.
- algorithmic_behavior: tests root listing, file read from session local root, traversal block, session-id fallback, short Windows temp root, symlink escape block, caller override priority, ENOENT surfacing lines 21-172.
- inputs_outputs_state: local protocol options/session/artifacts dirs in; resolved content/errors out.
- gates_or_invariants: all resolved paths must stay within local root; caller context overrides installed defaults.
- dependencies_and_callers: `LocalProtocolHandler`, internal URL router.
- edge_cases_or_failure_modes: symlink escape, long Windows paths, missing artifact dirs.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2565 `file` `packages/coding-agent/test/session-manager/build-context.test.ts`
- cursor: `[_]`
- core_role: validates session history to model context reconstruction.
- algorithmic_behavior: tests empty/simple messages, custom attribution, thinking/model changes, compaction summaries/replacement history, branch paths, orphan handling, dangling tool_use stripping lines 63-429.
- inputs_outputs_state: session entries/leaf ID in; model context messages and metadata out.
- gates_or_invariants: latest compaction wins; branch path selected by leaf; dangling unpaired tool_use removed.
- dependencies_and_callers: `buildSessionContext`.
- edge_cases_or_failure_modes: unknown leaf falls back to last entry; orphaned entries handled gracefully.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2595 `file` `packages/coding-agent/test/slash-commands/debug.test.ts`
- cursor: `[_]`
- core_role: validates debug slash command behavior.
- algorithmic_behavior: tests debug command parsing/output for coding-agent slash command surface.
- inputs_outputs_state: slash command args/session state in; debug output/action out.
- gates_or_invariants: debug command must be available and format expected information.
- dependencies_and_callers: slash command registry/debug handler.
- edge_cases_or_failure_modes: missing args or disabled command.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2625 `file` `packages/coding-agent/test/task/subagent-lsp.test.ts`
- cursor: `[_]`
- core_role: validates LSP tool availability/behavior inside subagents.
- algorithmic_behavior: constructs task/subagent scenarios and verifies LSP use/batching across child sessions.
- inputs_outputs_state: task agent config, LSP fixture/client in; subagent tool results out.
- gates_or_invariants: subagent tool restrictions must still allow LSP when configured; child session isolation maintained.
- dependencies_and_callers: task executor, LSP tool.
- edge_cases_or_failure_modes: parent/child tool list mismatch.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2655 `file` `packages/coding-agent/test/tools/browser-stealth-targets.test.ts`
- cursor: `[_]`
- core_role: validates browser stealth target matching.
- algorithmic_behavior: tests URL/domain/path target selection for stealth/scraper browser handling.
- inputs_outputs_state: target URLs/settings in; stealth decision out.
- gates_or_invariants: only configured or known targets get stealth behavior.
- dependencies_and_callers: browser/web tooling.
- edge_cases_or_failure_modes: subdomains, URL normalization, invalid URLs.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2685 `file` `packages/coding-agent/test/tools/lsp-batching.test.ts`
- cursor: `[_]`
- core_role: validates LSP batching behavior.
- algorithmic_behavior: tests multiple LSP operations coalesce/batch as expected.
- inputs_outputs_state: queued LSP requests in; batched client calls/results out.
- gates_or_invariants: batching should not reorder semantically dependent requests.
- dependencies_and_callers: LSP tool/client layer.
- edge_cases_or_failure_modes: concurrent requests and flush timing.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2715 `file` `packages/coding-agent/test/tools/sqlite.test.ts`
- cursor: `[_]`
- core_role: validates SQLite read/write tool behavior.
- algorithmic_behavior: tests SQLite selector parsing, listing/schema/query/row rendering and write/update paths.
- inputs_outputs_state: temp SQLite DB and selectors in; rendered tables/errors/updates out.
- gates_or_invariants: readonly read path validates selectors and caps; write path validates table/key/operations.
- dependencies_and_callers: SQLite reader/writer tools.
- edge_cases_or_failure_modes: invalid where/order/query params, rowid vs primary key, render width caps.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2745 `file` `packages/coding-agent/test/workflow/artifact-freeze.test.ts`
- cursor: `[_]`
- core_role: validates workflow artifact freeze packaging and production policy gates.
- algorithmic_behavior: tests same-name resource dir freezing, escape rejection, no cwd/legacy fallback, change request files, unsupported operations, checkpoint/change policy requirements, deadline validation, DSL-declared policies, and package load lines 21-699.
- inputs_outputs_state: workflow markdown/resources in; frozen artifact/package/errors out.
- gates_or_invariants: resources cannot escape same-name dir; production freeze requires checkpoint/change policy; unsupported change ops rejected.
- dependencies_and_callers: `freezeWorkflowArtifact`, `loadWorkflowArtifact`, workflow DSL.
- edge_cases_or_failure_modes: path traversal, non-positive deadlines, legacy fallback leakage.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2775 `file` `packages/collab-web/src/lib/link.ts`
- cursor: `[_]`
- core_role: collaboration link and encrypted relay envelope utilities.
- algorithmic_behavior: base64url encode/decode, pack/unpack peer envelopes, rewrite peer ID, generate room ID, normalize relay origins, format and parse collab links lines 24-185.
- inputs_outputs_state: relay URL/room ID/key/write token/envelope bytes in; share link or parsed link/envelope out.
- gates_or_invariants: room path and bare link regexes constrain IDs; local hostnames detected; envelope header length must match protocol.
- dependencies_and_callers: collab scripts/mock host/web client.
- edge_cases_or_failure_modes: invalid base64url, malformed room path, invalid relay URL.
- validation_or_tests: collab link tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2805 `file` `packages/mnemopi/src/core/patterns.ts`
- cursor: `[_]`
- core_role: memory compression and pattern detection.
- algorithmic_behavior: computes compression stats, compresses memory records, tracks detected patterns, counts common keys/sources/content terms/timestamps, and returns ranked patterns lines 1-484.
- inputs_outputs_state: memory records in; compression stats and detected patterns out.
- gates_or_invariants: UTF-8 byte sizing used for compression; stopwords filtered; counters rank most common entries.
- dependencies_and_callers: mnemopi recall/consolidation pipeline.
- edge_cases_or_failure_modes: missing content/source/timestamp fields; non-string record values.
- validation_or_tests: mnemopi pattern/beam tests indirectly cover memory behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2835 `file` `packages/stats/src/client/index.tsx`
- cursor: `[_]`
- core_role: React stats dashboard entrypoint.
- algorithmic_behavior: mounts root app into DOM `#root` lines 1-10.
- inputs_outputs_state: browser DOM in; React app mounted out.
- gates_or_invariants: `#root` element must exist.
- dependencies_and_callers: Vite/stats client bundle.
- edge_cases_or_failure_modes: missing root element throws due non-null assertion.
- validation_or_tests: UI smoke/build validates.
- skip_candidate: `yes: UI bootstrap, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2865 `file` `python/omp-rpc/src/omp_rpc/client.py`
- cursor: `[_]`
- core_role: Python RPC client process/protocol coordinator.
- algorithmic_behavior: starts/stops subprocess groups, terminates process groups, clones JSON, defines error classes, tracks pending requests/host tool calls/URI requests, bounded error history, prompt lifecycle, concurrency and protocol state in `RpcClient` lines 111-334 and onward.
- inputs_outputs_state: client commands/prompts/listeners/process options in; JSON-RPC messages, prompt turns, host-tool callbacks, errors out.
- gates_or_invariants: async commands set is `prompt`/`abort_and_prompt`; todo statuses constrained; bounded history limit 128; concurrency errors prevent overlapping prompts.
- dependencies_and_callers: omp RPC protocol module, subprocess, threading/async primitives.
- edge_cases_or_failure_modes: process exit, timeout, command error, protocol error, host tool call lifecycle.
- validation_or_tests: assigned `test_user_group.py` covers process user/group threading; broader RPC tests cover protocol.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2895 `directory` `packages/utils/src/vendor/mermaid-ascii/class`
- cursor: `[_]`
- core_role: vendored Mermaid class-diagram parser/types.
- algorithmic_behavior: `parser.ts` parses class diagrams, class members, relationships/arrows, namespaces and ensures class nodes; `types.ts` defines positioned/unpositioned class diagram contracts lines 27-271.
- inputs_outputs_state: Mermaid class diagram lines in; class nodes/relationships/namespaces out.
- gates_or_invariants: relationship arrows map to finite relationship types and marker direction; unknown/member parse failures skipped or null.
- dependencies_and_callers: Mermaid ASCII converter/rendering.
- edge_cases_or_failure_modes: malformed class member syntax, unknown arrows, duplicate class declarations.
- validation_or_tests: mermaid-ascii tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2925 `file` `packages/ai/src/providers/openai-codex/request-transformer.ts`
- cursor: `[_]`
- core_role: transforms requests for OpenAI Codex Responses Lite compatibility.
- algorithmic_behavior: derives reasoning config, filters input, converts orphan function outputs to messages, repairs tool call pairs, strips image detail fields, and exports `transformRequestBody` lines 64-257.
- inputs_outputs_state: request body/model/options in; transformed request body out.
- gates_or_invariants: orphan output limit 16 KiB; reasoning context can be `auto`, current turn, all turns; image detail stripped for target compatibility.
- dependencies_and_callers: OpenAI Codex provider transport.
- edge_cases_or_failure_modes: interrupted tool output sentinel, missing paired tool calls, oversized orphan outputs.
- validation_or_tests: OpenAI Codex response-lite/reset tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2955 `file` `packages/ai/src/utils/schema/normalize.ts`
- cursor: `[_]`
- core_role: provider-specific JSON schema normalization and strict-mode enforcement.
- algorithmic_behavior: decontaminates/upgrades/dereferences schemas, renames fields, strips unsupported fields, lifts defaults to descriptions, collapses combiners, handles nullable unions, rejects residual incompatibilities/falls back, normalizes for Google/CCA/MCP/Moonshot/OpenAI Responses, sanitizes regex/patternProperties, and enforces strict schema lines 28-1900.
- inputs_outputs_state: arbitrary schema/options in; provider-compatible schema or fallback out.
- gates_or_invariants: residual incompatibilities can trigger fallback; OpenAI lookarounds unsupported; CCA forbids combiners; strict mode narrows enums/consts and resolves refs.
- dependencies_and_callers: tool schema wire conversion across AI providers.
- edge_cases_or_failure_modes: cycles handled with epoch/WeakMap; invalid JSON schema fallback; unrepresentable strict branches.
- validation_or_tests: schema-wire/schema-compatibility/provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2985 `file` `packages/coding-agent/src/commit/agentic/index.ts`
- cursor: `[_]`
- core_role: agentic commit command executor.
- algorithmic_behavior: analyzes commit args, proposes single/split commits, confirms split plans, runs git commit operations, appends files to last commit, formats warnings/file summaries, and loads changelog entries lines 21-355.
- inputs_outputs_state: commit args/diff/proposals in; git commits or warnings/errors out.
- gates_or_invariants: split plan confirmation required; changelog context loaded for affected paths; files can be appended to last split commit.
- dependencies_and_callers: commit command CLI, git helpers, changelog analysis.
- edge_cases_or_failure_modes: user rejects plan, invalid proposal, git commit failure.
- validation_or_tests: commit command tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3015 `file` `packages/coding-agent/src/edit/modes/apply-patch.ts`
- cursor: `[_]`
- core_role: converts apply-patch params into edit entries/previews.
- algorithmic_behavior: validates `applyPatchSchema`, expands patch operations to `ApplyPatchEntry[]`, and builds preview entries lines 16-53.
- inputs_outputs_state: patch params in; normalized edit entries out.
- gates_or_invariants: schema constrains patch shape; output entries include paths.
- dependencies_and_callers: edit tool apply-patch mode.
- edge_cases_or_failure_modes: unsupported patch operation rejected by schema/expansion.
- validation_or_tests: edit/apply-patch tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3045 `file` `packages/coding-agent/src/export/html/share-loader.js`
- cursor: `[_]`
- core_role: browser-side loader for exported/shared HTML transcripts.
- algorithmic_behavior: loads embedded or remote share payload, decompresses/parses as needed, and hydrates exported view script.
- inputs_outputs_state: URL/hash/embed payload in; rendered export state out.
- gates_or_invariants: payload format/version must match expected loader contract.
- dependencies_and_callers: HTML export bundle and generated tool views.
- edge_cases_or_failure_modes: malformed payload, fetch failure, missing browser APIs.
- validation_or_tests: export/share tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3075 `file` `packages/coding-agent/src/extensibility/plugins/parser.ts`
- cursor: `[_]`
- core_role: parses and formats plugin spec strings.
- algorithmic_behavior: parses marketplace/package/version/path spec into `ParsedPluginSpec`, formats it back, and extracts npm package names lines 12-105.
- inputs_outputs_state: plugin spec string in; parsed marketplace/name/version/path out.
- gates_or_invariants: package name extraction handles scoped packages; invalid specs rejected/normalized.
- dependencies_and_callers: plugin install/marketplace CLI.
- edge_cases_or_failure_modes: scoped packages with subpaths, version separators, local path specs.
- validation_or_tests: plugin parser tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3105 `file` `packages/coding-agent/src/modes/components/btw-panel.ts`
- cursor: `[_]`
- core_role: TUI panel component for `/btw` side-channel answers.
- algorithmic_behavior: tracks running/complete/aborted/error states and renders question/answer/status UI in a container lines 6-112.
- inputs_outputs_state: panel state/options in; rendered TUI rows and branchable state out.
- gates_or_invariants: branchable only when complete with non-empty answer, tested separately.
- dependencies_and_callers: `BtwController`, overlay UI.
- edge_cases_or_failure_modes: empty answer, aborted/error request.
- validation_or_tests: assigned `btw-controller.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3135 `file` `packages/coding-agent/src/modes/components/overlay-box.ts`
- cursor: `[_]`
- core_role: reusable terminal overlay box drawing helpers.
- algorithmic_behavior: fits/clamps text by width, draws top/divider/bottom borders, rows, and split layout borders/rows lines 10-108.
- inputs_outputs_state: text/width/sidebar widths in; ANSI-styled strings out.
- gates_or_invariants: width calculations prevent overflow; split body width derived from sidebar.
- dependencies_and_callers: setup wizard and modal overlay components.
- edge_cases_or_failure_modes: tiny widths and long titles.
- validation_or_tests: UI component tests indirectly.
- skip_candidate: `yes: UI rendering utility, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3165 `file` `packages/coding-agent/src/modes/controllers/btw-controller.ts`
- cursor: `[_]`
- core_role: controller for `/btw` side-channel question flow and branch promotion.
- algorithmic_behavior: wraps question in prompt, aborts previous request on replacement, runs ephemeral turn, updates panel state, sanitizes assistant reply for branch, and prevents duplicate/ineligible branch actions lines 7-173.
- inputs_outputs_state: question/context/model/session leaf in; panel updates and optional branch request out.
- gates_or_invariants: empty question rejected; no model configured errors; branch only after complete non-empty answer from same leaf.
- dependencies_and_callers: `BtwPanelComponent`, ephemeral turn runner, branch context.
- edge_cases_or_failure_modes: active request aborted by next request, session leaf changes before branch, native replay metadata stripped.
- validation_or_tests: assigned `btw-controller.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3195 `file` `packages/coding-agent/src/modes/utils/copy-targets.ts`
- cursor: `[_]`
- core_role: extracts copyable targets from chat messages/tool calls.
- algorithmic_behavior: parses fenced code and quote blocks, extracts eval code and last shell/eval command, summarizes hints, ranks message/code/quote/command targets, and builds copy target list from recent messages lines 59-360.
- inputs_outputs_state: agent messages/tool calls in; `CopyTarget[]` out.
- gates_or_invariants: only last 50 messages considered; open/close fence regex controls block extraction.
- dependencies_and_callers: TUI copy menu/keyboard actions.
- edge_cases_or_failure_modes: unterminated fences, multiline quotes, unknown tool args.
- validation_or_tests: copy target/component tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3225 `file` `packages/coding-agent/src/web/scrapers/aur.ts`
- cursor: `[_]`
- core_role: special web handler for Arch AUR package pages.
- algorithmic_behavior: extracts package name, calls AUR RPC, and returns formatted package metadata as special handler result lines 5-162.
- inputs_outputs_state: AUR URL/fetch in; package summary/version/votes/maintainer metadata out.
- gates_or_invariants: only valid AUR package URLs handled; null returned for non-targets.
- dependencies_and_callers: web fetch/render pipeline.
- edge_cases_or_failure_modes: package not found, RPC failure, malformed response.
- validation_or_tests: web scraper media/special handler tests adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3255 `file` `packages/coding-agent/src/web/scrapers/jetbrains-marketplace.ts`
- cursor: `[_]`
- core_role: special web handler for JetBrains Marketplace plugin pages.
- algorithmic_behavior: validates host, extracts plugin/update data, computes rating/votes and build compatibility, formats plugin metadata lines 55-159.
- inputs_outputs_state: Marketplace URL/fetch JSON in; rendered plugin summary out.
- gates_or_invariants: host must be `plugins.jetbrains.com`; rating shape can be number/object/null.
- dependencies_and_callers: web special handlers.
- edge_cases_or_failure_modes: missing latest update, vendor fields absent, incompatible rating shapes.
- validation_or_tests: web scraper tests adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3285 `file` `packages/coding-agent/src/web/scrapers/snapcraft.ts`
- cursor: `[_]`
- core_role: special web handler for Snapcraft package pages.
- algorithmic_behavior: formats publisher/channel names, picks version from channels, extracts downloads, and returns snap metadata lines 64-187.
- inputs_outputs_state: Snapcraft URL/API response in; package summary/version/publisher/downloads out.
- gates_or_invariants: channel map preferred for version; downloads extracted from multiple possible shapes.
- dependencies_and_callers: web fetch/render pipeline.
- edge_cases_or_failure_modes: missing channel map, publisher absent, malformed downloads.
- validation_or_tests: web scraper tests adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3315 `file` `packages/coding-agent/test/modes/components/chat-block.test.ts`
- cursor: `[_]`
- core_role: validates ChatBlock lifecycle and cleanup semantics.
- algorithmic_behavior: tests onMount idempotence, live/finalized transitions, cleanup once, dispose idempotence, render routing, immediate cleanup after dispose, child disposal, timer cleanup lines 28-127.
- inputs_outputs_state: component lifecycle calls in; cleanup/render/finalized state out.
- gates_or_invariants: cleanup runs exactly once; disposed blocks cannot request host render.
- dependencies_and_callers: chat block component/container.
- edge_cases_or_failure_modes: finish then dispose double cleanup, cleanup registered after dispose.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3345 `file` `packages/coding-agent/test/modes/controllers/btw-controller.test.ts`
- cursor: `[_]`
- core_role: validates `/btw` panel/controller behavior.
- algorithmic_behavior: tests branchability, dispatch to ephemeral turn, abort replacement, escape clearing, empty question rejection, missing model error, branch eligibility, reply sanitization, duplicate branch guard, leaf-change invalidation, cleanup lines 75-390.
- inputs_outputs_state: controller requests/context state in; panel state/branch calls out.
- gates_or_invariants: branch only complete non-empty answer from original leaf; native replay payload metadata stripped.
- dependencies_and_callers: `BtwController`, `BtwPanelComponent`.
- edge_cases_or_failure_modes: active request replaced/aborted, branch in flight, session leaf changes.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3375 `file` `packages/coding-agent/test/tools/web-scrapers/media.test.ts`
- cursor: `[_]`
- core_role: validates media special web scrapers.
- algorithmic_behavior: tests Vimeo, Spotify, and Hugging Face URL recognition and metadata fetch for tracks/albums/playlists/podcasts/models/datasets/spaces lines 9-132.
- inputs_outputs_state: URLs and mocked fetch responses in; scraper result/null out.
- gates_or_invariants: non-target and invalid URLs return null; target URLs map to correct media kind.
- dependencies_and_callers: web scraper handlers.
- edge_cases_or_failure_modes: org/model vs bare model IDs, player Vimeo URLs.
- validation_or_tests: file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3405 `file` `packages/collab-web/src/tool-render/tools/ask.tsx`
- cursor: `[_]`
- core_role: web renderer for ask/request-user-input tool calls.
- algorithmic_behavior: normalizes options/questions/answers, strips `(Recommended)`, derives questions from args/details, and renders summary/body question blocks lines 29-217.
- inputs_outputs_state: tool args/result details in; React nodes out.
- gates_or_invariants: options/questions tolerate malformed raw shapes by filtering/normalizing.
- dependencies_and_callers: collab-web tool render registry.
- edge_cases_or_failure_modes: missing details/answers, recommended suffix in labels.
- validation_or_tests: collab tool renderer tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3435 `file` `packages/collab-web/src/tool-render/tools/write.tsx`
- cursor: `[_]`
- core_role: web renderer for write tool calls/results.
- algorithmic_behavior: extracts diagnostics, renders summary with path/content preview and body with result/errors lines 8-82.
- inputs_outputs_state: write tool args/result in; React nodes out.
- gates_or_invariants: diagnostics shape filtered from details; missing result handled.
- dependencies_and_callers: collab-web tool render registry.
- edge_cases_or_failure_modes: malformed details or huge content previews.
- validation_or_tests: renderer tests likely elsewhere.
- skip_candidate: `yes: UI rendering adapter`

### OH_MY_HUMANIZE_MAIN-HZ-3465 `file` `packages/stats/src/client/routes/CostsRoute.tsx`
- cursor: `[_]`
- core_role: stats dashboard cost route.
- algorithmic_behavior: fetches cost series, renders overview cards, bar labels plugin, and cost trend chart lines 23-234.
- inputs_outputs_state: active/range/refresh trigger and API data in; React panels/charts out.
- gates_or_invariants: route only fetches/renders when active; chart labels use plugin color mapping.
- dependencies_and_callers: stats client API and Chart.js.
- edge_cases_or_failure_modes: empty series, inactive route, fetch failure.
- validation_or_tests: stats UI tests/build.
- skip_candidate: `yes: UI presentation route, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3495 `file` `python/robomp/web/src/components/Issues.tsx`
- cursor: `[_]`
- core_role: React component for robomp issue list.
- algorithmic_behavior: renders issue rows and metadata from props, with row helper component lines 11-117.
- inputs_outputs_state: issues props in; JSX table/list out.
- gates_or_invariants: issue row fields displayed consistently.
- dependencies_and_callers: robomp web app.
- edge_cases_or_failure_modes: empty list or missing optional fields.
- validation_or_tests: web component tests/build.
- skip_candidate: `yes: UI component`

### OH_MY_HUMANIZE_MAIN-HZ-3525 `file` `packages/coding-agent/src/extensibility/plugins/marketplace/cache.ts`
- cursor: `[_]`
- core_role: marketplace plugin cache path and lifecycle manager.
- algorithmic_behavior: validates cache version/components, computes cached plugin paths, copies plugin into cache, checks existence, removes cached plugin, cleans orphaned cache entries lines 23-136.
- inputs_outputs_state: cache dir/marketplace/plugin/version/source path/installed paths in; cached dirs and removal count out.
- gates_or_invariants: version regex allows alnum/dot/underscore/plus/hyphen; path components validated to avoid unsafe cache paths.
- dependencies_and_callers: plugin marketplace installer/loader.
- edge_cases_or_failure_modes: orphan cleanup must not remove installed paths; invalid version rejected.
- validation_or_tests: plugin cache tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3555 `file` `packages/coding-agent/src/modes/setup-wizard/scenes/outro.ts`
- cursor: `[_]`
- core_role: setup wizard outro frame renderer.
- algorithmic_behavior: centers/clamps lines and renders outro frames based on width/height/elapsed with duration constant `SETUP_OUTRO_MS = 1200` lines 6-35.
- inputs_outputs_state: terminal width/height/elapsed ms in; string frame lines out.
- gates_or_invariants: line width clamped to avoid overflow.
- dependencies_and_callers: setup wizard overlay.
- edge_cases_or_failure_modes: very small terminal dimensions.
- validation_or_tests: setup wizard/UI tests.
- skip_candidate: `yes: UI animation renderer`

### OH_MY_HUMANIZE_MAIN-HZ-3585 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/converter.ts`
- cursor: `[_]`
- core_role: converts parsed Mermaid graph into ASCII graph layout input.
- algorithmic_behavior: converts nodes/edges/subgraphs, recursively converts subgraphs, deduplicates subgraph nodes, checks ancestry, and builds subgraph map lines 25-271.
- inputs_outputs_state: `MermaidGraph` plus config in; `AsciiGraph` with subgraphs/nodes/edges out.
- gates_or_invariants: subgraph node dedupe prevents duplicate rendering; ancestry checks preserve hierarchy.
- dependencies_and_callers: mermaid-ascii renderer.
- edge_cases_or_failure_modes: nested subgraphs and nodes belonging to multiple scopes.
- validation_or_tests: mermaid-ascii tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3615 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/rounded.ts`
- cursor: `[_]`
- core_role: rounded box shape renderer for ASCII diagrams.
- algorithmic_behavior: exports `roundedRenderer` with corner/edge glyph behavior lines 18-27.
- inputs_outputs_state: shape render request in; rounded ASCII border glyphs out.
- gates_or_invariants: renderer conforms to `ShapeRenderer`.
- dependencies_and_callers: mermaid-ascii shape registry.
- edge_cases_or_failure_modes: terminal font/glyph support.
- validation_or_tests: ASCII diagram rendering tests elsewhere.
- skip_candidate: `yes: small rendering constant`

## Worker Self-Test
- assigned_items_seen: `121`
- missing_items: `none`
- duplicate_items: `none`
- evidence_shape_check: every assigned row was represented as one `###` item evidence section with cursor `[_]`; no assigned item was marked with any master-acceptance cursor.
- final_worker_status: `complete`

---

## Incremental Directory Refresh Addendum - oh-my-humanize/main bf4509d4f - OH_MY_HUMANIZE_MAIN-HZ-1605

# agent_dir_09 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-1605 `directory` `packages/coding-agent/src/cli/__tests__`
- cursor: `[_]`
- current_directory_core_role: This directory is the CLI-level regression test surface for workflow command behavior. It currently contains one core descendant, `workflow-cli.test.ts`, which invokes `runWorkflowCommand()` directly with mocked stdout/stderr and temporary frozen `.omhflow` artifacts. Its responsibility is not low-level scheduler testing; it verifies the user-visible CLI contract around workflow lookup errors, artifact/package validation, headless workflow start output, frozen resources, requested cwd propagation, and signal-triggered stop/checkpoint behavior.
- directory_level_delta_since_old_commit: The directory’s responsibility expanded from mostly artifact resolution/error-output and frozen resource smoke coverage into headless execution lifecycle coverage. The changed test file now pins two important CLI integration contracts: headless JavaScript workflow scripts must run relative to the CLI-requested `cwd`, and an interrupted headless workflow start must stop cleanly with a persisted lifecycle checkpoint rather than leaving a run/attempt alive. This corresponds to the broader source changes in `workflow-cli.ts` and `workflow/runner.ts`, where `cwd` is explicitly passed into eval/shell/agent runtime hosts, start signals are injected/cleaned up, `nodeAbortSignal` is passed to `runWorkflow`, and runtime/deadline aborts are converted into stopped checkpoints.
- affected_descendant_algorithms: `workflow-cli.test.ts` now exercises the headless workflow start path across artifact loading, freeze/resource use, runtime host construction, eval script execution, signal handling, scheduler abort, lifecycle reconstruction, and JSON output shaping. The new cwd test creates a frozen `.omhflow` with a JS script file that reads `marker.txt` via `Bun.file("marker.txt")`; success proves `runHeadlessEvalScript()` changes into the requested workspace cwd before running code and restores process state afterward. The new SIGINT test creates a sleeping shell node, emits SIGINT through a fake `WorkflowStartSignalTarget`, and proves the CLI start signal aborts both scheduling and active node execution so the runner records an aborted activation/checkpoint and reports stopped status.
- current_inputs_outputs_state: Test inputs are synthetic temp artifacts/resources created with `Bun.write()`, command structs passed to `runWorkflowCommand()`, flags such as `cwd`, `json`, `runId`, and `familyId`, optional `OMHFLOW_DIR`, and an injectable fake signal target implementing `once()`/`off()`. Outputs are captured stdout/stderr strings and process exit-code side effects. For successful headless starts, stdout is parsed as JSON and checked for `run.status`, completed/failed counts, frontier node ids, reconstructed run `stateKeys`, family attempts, and checkpoints. For error cases, stderr is checked for user-facing messages without internal stack/source type names.
- new_or_changed_gates_or_invariants: Headless JS script nodes must observe `flags.cwd` for relative filesystem operations, not the artifact resource directory, repository cwd, or original process cwd. Frozen resource script execution must still load script text from the frozen package/resource snapshot while runtime relative IO follows the requested cwd. Headless `start` must only accept frozen `.omhflow` artifacts. On SIGINT/SIGTERM, CLI workflow start must abort the active node, return JSON with `run.status: "stopped"`, keep the interrupted node in the frontier, mark the lifecycle attempt stopped, create a checkpoint with the same frontier, and unregister signal listeners. Runner-level invariants behind this directory now include separate scheduler stop vs node abort signals, deadline/max-runtime abort reasons, and checkpointing stopped/aborted lifecycle attempts instead of failing or hanging.
- dependencies_and_callers: The directory depends on `bun:test`, `node:path`, `TempDir` from `@oh-my-pi/pi-utils`, and `runWorkflowCommand`/`WorkflowStartSignalTarget` from `../workflow-cli`. The tests indirectly cover `workflow-cli.ts` helpers including workflow spec resolution, `.omhflow` package loading/freezing, `createSessionWorkflowRuntimeHost()`, `runHeadlessEvalScript()`, `runHeadlessShellScript()`, `createWorkflowStartSignalController()`, JSON rendering, and error handling for `WorkflowArtifactRegistryError`/`WorkflowPackageError`. Downstream implementation dependencies include `workflow/runner.ts`, `workflow/lifecycle`, `workflow/run-store`, `workflow/package-loader`, and frozen resource materialization. Complementary lower-level caller coverage lives in `packages/coding-agent/test/workflow/runner.test.ts`, especially node abort signal, ignored abort, and max-runtime checkpoint tests.
- edge_cases_or_failure_modes: The cwd regression would fail if JS eval scripts run from the artifact directory or ambient repo cwd, making relative workspace reads such as `marker.txt` fail or read the wrong file. The signal regression would fail if SIGINT only stops scheduling but not active node work, if a sleeping shell process remains alive, if the attempt is marked failed instead of stopped, if no checkpoint is written, if the frontier is lost, or if process signal listeners leak after command completion. Related runner failure modes now guarded outside this directory include deadline-aborted nodes being classified as failures, runtime implementations ignoring abort and causing hangs, and max-runtime expiration not producing stopped lifecycle checkpoints. Existing tests still guard stackless error output for ambiguous flow lookup/package errors and rejection of non-artifact headless starts.
- validation_or_tests: Inspected `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts` recursively; the directory currently has one file. Relevant test cases in this directory are `runs headless js workflow scripts from the requested cwd` and `checkpoints headless workflow starts on SIGINT instead of leaving a run alive`, alongside existing coverage for ambiguous lookup errors, artifact package errors, non-artifact start rejection, and frozen data resources for shell nodes. Related implementation and runner tests inspected include `workflow-cli.ts` signal/cwd/runtime host logic and `runner.test.ts` cases for dedicated node abort signals, deadline-aborted lifecycle activations, ignored abort, and max-runtime checkpointing. Tests were not executed in this read-only research pass.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-1605`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
