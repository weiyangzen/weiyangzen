# agent_26 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-026 `directory` `packages/ai`
- cursor: `[_]`
- core_role: Multi-provider LLM client package: provider registry, auth storage/broker/gateway, request/stream adapters, dialect/in-band tool renderers, usage/rate-limit accounting, schema normalization, and provider regression tests.
- algorithmic_behavior: Recursively contains API routing (`src/api-registry.ts`), provider implementations (`src/providers/*`), model/provider registries (`src/registry/*`), dialect scanners/renderers (`src/dialect/*`), usage ranking (`src/usage/*`), request debug/retry/stream helpers (`src/utils/*`), and schema adapters (`src/utils/schema/*`). The central behavior is normalizing a coding-agent `Context` into provider-specific wire payloads, streaming assistant/tool events back into common message shapes, and selecting credentials/providers without leaking local-only config.
- inputs_outputs_state: Inputs are `Model<Api>`, credentials/API keys/OAuth tokens, message history, tools, tool schemas, abort signals, and provider settings. Outputs are streamed `AssistantMessage` events, usage/cost objects, normalized errors, auth updates, and cache/debug artifacts. Persistent or process state includes auth DB storage, auth-broker snapshots, token caches, provider singleton registration, and usage caches.
- gates_or_invariants: Catalog values are imported from `@oh-my-pi/pi-catalog/*`; schema utilities enforce provider constraints; retry classifiers distinguish transient transport failures from quota/account limits; local endpoint leakage is blocked in bundled catalog tests; OAuth refresh/ranking paths must not block first selection indefinitely.
- dependencies_and_callers: Used by `packages/agent` and `packages/coding-agent` for completions and streaming; depends on `@oh-my-pi/pi-catalog`, Bun fetch/crypto APIs, provider SDK wire formats, and auth/usage utility modules.
- edge_cases_or_failure_modes: Provider-specific auth header precedence, SSE parse interruptions, abandoned tool-use replay, forced `tool_choice` with absent tools, local endpoint leakage, JSON-schema dialect incompatibility, cached token expiry skew, and provider retries after first-event/stream errors.
- validation_or_tests: Extensive direct tests under `packages/ai/test`, including assigned tests for Anthropics retry classification, Codex OAuth credential ranking, Copilot Anthropic auth, forced tool-choice guards, models.json endpoint leak guard, OpenRouter Responses parity, and schema normalization.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-056 `file` `docs/mnemosyne-memory-backend.md`
- cursor: `[_]`
- core_role: Architecture/runtime documentation for the coding-agent Mnemopi long-term memory backend.
- algorithmic_behavior: Defines the backend flow: open scoped Mnemopi SQLite banks, recall relevant memories into the first-turn `<memories>` block, retain completed turns after agent turns, add pre-compaction context, and route `/memory` commands through the shared memory backend interface (`docs/mnemosyne-memory-backend.md:21-27`).
- inputs_outputs_state: Inputs are `memory.backend`, `mnemopi.*` settings, cwd-derived project scope, conversation turns, compaction requests, and embedding/LLM settings. Outputs are recalled memory blocks, retained facts/episodes, diagnostics/stats, and scoped bank database files.
- gates_or_invariants: Recalled memory is explicitly background context, not instructions (`docs/mnemosyne-memory-backend.md:29`). Scoping modes constrain read/write visibility: global, per-project, or per-project-tagged (`docs/mnemosyne-memory-backend.md:59-67`).
- dependencies_and_callers: Documents `@oh-my-pi/pi-mnemopi`, coding-agent memory commands, Mnemopi `BankManager`, local/remote embedding providers, pi-ai smol model dynamic LLM completion, and optional memory model override.
- edge_cases_or_failure_modes: Project hash scoping prevents cwd basename collisions; `noEmbeddings` forces FTS-only recall; embedding model variant changes rebuild stored embeddings; subagents alias parent Mnemopi state or remain inert (`docs/mnemosyne-memory-backend.md:156-160`).
- validation_or_tests: Documentation maps to memory backend behavior and Mnemopi tests such as proactive linking and consolidation regression tests assigned below.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-086 `file` `scripts/ci-macos-sign.sh`
- cursor: `[_]`
- core_role: CI release workflow script for signing, hardened-runtime launch testing, and notarizing the macOS `omp` binary.
- algorithmic_behavior: Validates macOS host and binary argument, checks required Apple secrets, creates an isolated temporary keychain, imports Developer ID certificate, signs with entitlements, verifies the signature, runs `--version` and `--smoke-test`, zips the binary, submits it to `notarytool`, and fails if status is not `Accepted` (`scripts/ci-macos-sign.sh:29-145`).
- inputs_outputs_state: Inputs are binary path plus `APPLE_CERTIFICATE_P12`, password, App Store Connect key id/issuer/key, and `scripts/macos-entitlements.plist`. Outputs are an in-place signed binary, notarization submission JSON, and CI stdout/stderr diagnostics. Temporary state is keychain, decoded cert/key, zip, and isolated HOME under `mktemp`.
- gates_or_invariants: `set -euo pipefail`; non-Darwin hosts, missing binary, missing env, missing entitlements, missing Developer ID identity, failed launch smoke, and non-accepted notarization all exit nonzero.
- dependencies_and_callers: Called by GitHub Actions release pipeline after binary build; depends on macOS `security`, `codesign`, `ditto`, `xcrun notarytool`, `openssl`, `base64`, and Python JSON parsing.
- edge_cases_or_failure_modes: Bare Mach-O cannot be stapled, so ticket verification is online; hardened-runtime entitlement omissions can pass signing but fail `--smoke-test`; notary failures fetch logs when submission id is present (`scripts/ci-macos-sign.sh:111-140`).
- validation_or_tests: The script validates itself operationally via `codesign --verify`, `codesign -dvvv`, binary `--version`, and binary `--smoke-test`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-116 `file` `scripts/tool_io.py`
- cursor: `[_]`
- core_role: Offline transcript-analysis helper for extracting tool calls/results from coding-agent session JSONL files.
- algorithmic_behavior: Lists recent `*.jsonl` session files by mtime, iterates message entries, records assistant `toolCall` blocks in a pending map, pairs them with `toolResult` messages by `toolCallId`, yields unresolved calls optionally, and exposes filtering helpers for success/failure/diff/path plus reservoir sampling (`scripts/tool_io.py:138-270`).
- inputs_outputs_state: Inputs are `ToolIOConfig`, tool names/groups, session JSONL files, and max item/file/day limits. Outputs are `ToolInvocation` objects with call args, result text, details, diff, timestamps, path hints, and optional assistant thinking.
- gates_or_invariants: Bad JSONL lines are skipped, non-message entries ignored, only wanted tool names pass, `limit_mode` counts calls or events, `max_items` stops iteration, and unresolved calls are emitted only when configured (`scripts/tool_io.py:154-230`).
- dependencies_and_callers: Standalone Python utility using `pathlib`, dataclasses, JSON, and the local session file format.
- edge_cases_or_failure_modes: Session file disappearance is tolerated during listing; malformed entries are ignored; results without a pending call are skipped; `extract_path` only recognizes `path`, `file`, or `move` (`scripts/tool_io.py:294-386`).
- validation_or_tests: No direct test file inspected; behavior is deterministic and can be validated by feeding fixture JSONL transcripts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-146 `directory` `packages/natives/test`
- cursor: `[_]`
- core_role: Test suite for the native bindings package, covering runtime discovery/search/text/shell behavior rather than production implementation.
- algorithmic_behavior: Recursively includes tests for summarization, tree-sitter block ranges, key decoding, native grep/find/listWorkspace cache semantics, FIFO skipping, pty/shell timeout killing, HTML-to-Markdown conversion, macOS power assertions, AST match/edit, standalone binary native loader path resolution, public ESM export completeness, generated native npm leaf manifests, and Windows staging.
- inputs_outputs_state: Inputs are temporary fixtures, files/directories/FIFOs, glob/type filters, native loader path scenarios, generated manifests, and mocked platform/install paths. Outputs are assertions over search results, path candidate lists, exports, package manifests, timeout behavior, and extracted bundled native variants.
- gates_or_invariants: Hidden/gitignore behavior, `.git`/FIFO skipping, `maxResults=0`, cache invalidation on relative path, explicit leaf package precedence, Windows staging precedence, and Rust `js_name` version sentinel are enforced.
- dependencies_and_callers: Tests `@oh-my-pi/pi-natives` JS exports and Rust native behavior; supports callers in coding-agent tools (`find`, `grep`, `listWorkspace`, pty/shell).
- edge_cases_or_failure_modes: Standalone compiled binary extraction paths, npm leaf package fallback, stale version directory cleanup, ignored AGENTS.md behavior, detached background workloads, SIGTERM-ignoring processes, and incomplete source parse errors.
- validation_or_tests: The directory itself is validation; key files are `native.test.ts`, `issue-823-repro.test.ts`, `issue-892-repro.test.ts`, `npm-packages.test.ts`, and `windows-staging.test.ts`.
- skip_candidate: `yes: test-only directory; it validates native core algorithms but does not implement runtime behavior`

### OH_MY_HUMANIZE_MAIN-HZ-176 `file` `docs/toolconv/harmony.md`
- cursor: `[_]`
- core_role: Architecture documentation for OpenAI Harmony conversation/tool-call format and parser/renderer requirements.
- algorithmic_behavior: Specifies Harmony special tokens, message envelope, role/channel hierarchy, developer tool declaration syntax, function call format, tool result format, turn continuation, `<|return|>` normalization, OpenAI-compatible mapping, and parser gotchas (`docs/toolconv/harmony.md:15-224`).
- inputs_outputs_state: Inputs are system/developer/user/tool messages, JSON Schemas for tools, reasoning effort, generated assistant tokens, and stop tokens. Outputs are raw Harmony token streams, tool-call JSON bodies, OpenAI-compatible `finish_reason`/`tool_calls`, and stored normalized history.
- gates_or_invariants: Stop on both `<|return|>` and `<|call|>`; assistant messages require channels; tool result author is the tool name, not literal `tool`; keep preceding `analysis` across tool-call continuation but drop it after final turns (`docs/toolconv/harmony.md:61-64`, `docs/toolconv/harmony.md:191-211`).
- dependencies_and_callers: Documents `packages/ai/src/dialect/harmony.ts`, OpenAI `openai-harmony`, vLLM/SGLang parser flags, and tool schema rendering.
- edge_cases_or_failure_modes: Recipient may appear in role or channel header; `<|constrain|>json` is metadata, not validation; streaming parsers must handle partial UTF-8 and optional header fields; double-encoding function arguments breaks OpenAI mapping.
- validation_or_tests: Sources list reference format tests and fixtures; repo has dialect/tool-conversion tests under `packages/ai/test`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-206 `file` `docs/tools/web_search.md`
- cursor: `[_]`
- core_role: Runtime documentation for the coding-agent `web_search` tool’s provider selection, execution, formatting, limits, and error behavior.
- algorithmic_behavior: Describes `WebSearchTool.execute()` delegating to `executeSearch()`, resolving provider chains, sequential fallback, provider request params, renderability checks, `formatForLLM()`, normalized provider errors, and provider-specific adapters across Perplexity, Gemini, Anthropic, Codex, Z.AI, Exa, Jina, Kagi, Tavily, Brave, Kimi, Parallel, Synthetic, and SearXNG (`docs/tools/web_search.md:1-228`).
- inputs_outputs_state: Inputs are query, recency, limit, max tokens, temperature, num search results, provider settings, credentials, and abort signal. Outputs are a single text block plus structured `SearchRenderDetails` containing `SearchResponse` and optional error.
- gates_or_invariants: No-provider and all-failed cases return normal tool results with `Error: ...` rather than throwing; abort rethrows during fallback; explicit provider may fall back to auto chain if unavailable; excluded providers are never returned.
- dependencies_and_callers: Tied to `packages/coding-agent/src/web/search/index.ts`, provider registry/types/renderers, settings schema, built-in tool registration, and each provider adapter.
- edge_cases_or_failure_modes: Empty renderable provider responses become status-204 provider errors; Anthropic 404 remapping; auth failures normalized; Perplexity preserves `limit` vs `num_search_results`; SearXNG auth config can fail before HTTP.
- validation_or_tests: Assigned `web-search-gemini.test.ts` validates Gemini tool serialization; docs map to provider tests and adapter behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-236 `directory` `packages/ai/src/usage`
- cursor: `[_]`
- core_role: Usage/quota provider and credential-ranking subsystem for OAuth/API-backed providers.
- algorithmic_behavior: Recursively parses provider usage endpoints and rate-limit headers into common `UsageReport`/`UsageLimit` shapes, including Claude 5h/7d windows, Gemini tier buckets, GitHub Copilot quota headers, Google Antigravity usage, Kimi, OpenAI Codex usage/reset parsing, OpenCode Go, ZAI, and shared ranking helpers.
- inputs_outputs_state: Inputs are provider id, credential object, base URL, fetch implementation, headers, abort signal, retry hooks, and raw provider JSON/SSE responses. Outputs are normalized usage reports, limits with windows/reset times, account identity metadata, and ranking strategies used by auth selection.
- gates_or_invariants: Providers return `null` when unsupported or credentials missing; utilization is clamped; retryable status handling is bounded; aborts stop retry waits; ranking strategies expose primary/secondary window limits for weighted credential choice.
- dependencies_and_callers: Called by `AuthStorage` credential selection and usage cache tests; depends on provider auth headers, `toNumber`, logger hooks, and common `packages/ai/src/usage.ts` types.
- edge_cases_or_failure_modes: Missing usage data triggers bounded retries; profile fetch fills missing Claude identity; reset timestamps may arrive as headers or JSON; exhausted accounts fall back to earliest-unblocking account.
- validation_or_tests: Covered by `auth-storage-codex-selection.test.ts`, `claude-usage-*`, `google-antigravity-usage.test.ts`, `openai-codex-usage.test.ts`, and usage cache/history tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-266 `directory` `packages/coding-agent/src/internal-urls`
- cursor: `[_]`
- core_role: Internal URL routing framework for read/write access to agent outputs, artifacts, docs, history, local files, MCP resources, memory, GitHub issues/PRs, rules, skills, vaults, and OMP docs.
- algorithmic_behavior: Recursively contains protocol handlers, parser, router, JSON query engine, registry helpers, and types. Handlers implement `resolve`, optional `write`, and `complete`; the router dispatches by scheme; `parseInternalUrl` preserves raw host/path for namespaced hosts; `json-query` extracts nested JSON via path/query form.
- inputs_outputs_state: Inputs are internal URL strings, `ResolveContext`/`WriteContext`, session registries, cwd/settings, MCP manager, memory roots, artifacts dirs, and abort signals. Outputs are `InternalResource` objects with content, type, size, source path, notes, and completions.
- gates_or_invariants: Protocols validate host/path shape, block path traversal, pin artifact resolution to caller session where applicable, prevent combining agent path extraction and `?q=`, constrain local/memory paths within roots, and reject invalid issue/PR list states/limits.
- dependencies_and_callers: Used by read/write tools and autocomplete; depends on `AgentRegistry`, session history formatting, GitHub cache/tools, MCP manager, memory registry, Obsidian CLI, embedded docs index, and local protocol options.
- edge_cases_or_failure_modes: Missing artifact/session dirs, running agents without finalized outputs, malformed embedded docs index, invalid percent-encoded URL segments, PR diff slice out of range, vault disabled/missing Obsidian binary, and MCP resource URI template ambiguity.
- validation_or_tests: Assigned `parse-internal-url.test.ts` covers parser edge cases; debug protocol tests and marketplace tests indirectly exercise protocol behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-296 `directory` `packages/coding-agent/test/debug`
- cursor: `[_]`
- core_role: Debug subsystem regression suite for DAP launch/attach, log formatting/viewing, protocol probes, raw SSE buffering/pretty/report bundle, and terminal capability reporting.
- algorithmic_behavior: Uses fake DAP clients/adapters and temp fixtures to assert error aggregation, delayed socket startup, debugpy guidance, directory-program validation, terminal feature formatting, log viewer filtering/selection/chunked loading, and raw SSE parsing/reporting behavior.
- inputs_outputs_state: Inputs are mocked DAP adapter metadata, fake stderr/errors/events, log text, process start timestamps, terminal protocol detections, and SSE streams. Outputs are rejected errors, formatted log rows, selected-copy payloads, report bundles, and terminal state strings.
- gates_or_invariants: Launch/attach root cause must not be masked by `configurationDone`; unhandled rejection must not occur; terminal info must not leak raw escapes; log lines sanitize ANSI/control/tab content; older logs load without cursor instability.
- dependencies_and_callers: Validates `dap`, `DebugTool`, `debug/log-viewer`, `debug/log-formatting`, raw SSE utilities, and terminal detection/formatting used by coding-agent debug UI.
- edge_cases_or_failure_modes: Missing debugpy module, non-debugpy incidental messages, delayed Unix socket adapter, unsupported screen-to-scrollback clearing, logs spanning current-session boundary, and external older-log source loading.
- validation_or_tests: The directory is validation-only; files include `dap-launch-failures.test.ts`, `log-formatting.test.ts`, `log-viewer.test.ts`, `protocol-probe.test.ts`, `raw-sse-*`, and `terminal-info.test.ts`.
- skip_candidate: `yes: test-only directory; it validates debug algorithms but does not implement runtime behavior`

### OH_MY_HUMANIZE_MAIN-HZ-326 `directory` `packages/mnemopi/src/migrations`
- cursor: `[_]`
- core_role: Public migration barrel for Mnemopi migrations.
- algorithmic_behavior: Contains only `e6-triplestore-split.ts` re-exporting `../core/migrations/e6-triplestore-split` and `index.ts` re-exporting that migration; no local migration logic is implemented in this directory.
- inputs_outputs_state: Inputs and outputs are module exports; runtime migration state lives in the referenced core migration file outside this assigned path.
- gates_or_invariants: Barrel export surface must preserve migration module availability for package consumers.
- dependencies_and_callers: Depends on `packages/mnemopi/src/core/migrations/e6-triplestore-split`; callers import migration entries via `packages/mnemopi/src/migrations`.
- edge_cases_or_failure_modes: If the core migration moves or changes export names, this barrel breaks; otherwise no algorithmic branch behavior here.
- validation_or_tests: Migration behavior is expected to be tested via core Mnemopi migration/storage tests, not in this directory.
- skip_candidate: `yes: thin re-export directory; core algorithm is in the referenced core migration, not here`

### OH_MY_HUMANIZE_MAIN-HZ-356 `file` `crates/pi-natives/src/fs_cache.rs`
- cursor: `[_]`
- core_role: Rust native filesystem scan cache used by discovery/search tools.
- algorithmic_behavior: Defines `GlobMatch`, cache policy env vars, path normalization, skip rules, deterministic ignore walker, parallel visitor collection, TTL `get_or_scan`, `force_rescan`, and invalidation API (`crates/pi-natives/src/fs_cache.rs:31-145`, `crates/pi-natives/src/fs_cache.rs:246-451`).
- inputs_outputs_state: Inputs are root path, `ScanOptions`, cancel token, env policy (`FS_SCAN_CACHE_TTL_MS`, `FS_SCAN_EMPTY_RECHECK_MS`, `FS_SCAN_CACHE_MAX_ENTRIES`, `PI_GREP_WORKERS`), and optional invalidation path. Outputs are sorted `GlobMatch` entries with file type/mtime/size and cache age.
- gates_or_invariants: `resolve_search_path` requires an existing directory; `.git` is always skipped; `node_modules` skipped unless allowed; TTL zero disables caching; cache keys exclude `follow_links`; visitor heartbeats every 128 entries for cancellation.
- dependencies_and_callers: Uses `ignore::WalkBuilder`, `DashMap`, NAPI, and native task cancel token; called by native glob/find/grep/listWorkspace layers.
- edge_cases_or_failure_modes: FIFO/special files are skipped by `classify_file_type`; symlink metadata fallback handles metadata failures; invalidation canonicalizes existing parents for deleted/new files; oldest cache entry evicted when over limit.
- validation_or_tests: Inline tests cover FIFO skip, walker `.git`/`node_modules` pruning, and collect skip behavior; `packages/natives/test/native.test.ts` covers cache invalidation and empty cached result recheck behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-386 `file` `packages/agent/src/agent-loop.ts`
- cursor: `[_]`
- core_role: Core agent execution loop: model streaming, message normalization, tool execution, steering interrupts, deadlines, telemetry, and abort/error pairing.
- algorithmic_behavior: Exposes `agentLoop`, `agentLoopContinue`, detailed variants, `normalizeTools`, and `abortReasonText`; `runLoopBody` repeatedly injects pending steering/asides, streams assistant responses, executes runnable tool calls, appends tool results, handles paused turns, and drains follow-up messages (`packages/agent/src/agent-loop.ts:283`, `packages/agent/src/agent-loop.ts:558`, `packages/agent/src/agent-loop.ts:606`, `packages/agent/src/agent-loop.ts:678`).
- inputs_outputs_state: Inputs are `AgentContext`, new messages, model config, converter/stream function, tools, abort/deadline signals, steering/asides/follow-up callbacks, telemetry, and transform hooks. Outputs are `AgentEvent` stream entries, appended `AgentMessage[]`, tool result messages, telemetry spans, and terminal end events.
- gates_or_invariants: Tool-use blocks must be paired with tool results even on abort/error/length truncation; deadlines end the stream; steering queue is not drained on external abort; no-op/malformed tool results are coerced; intent field injection is optional and can be disabled by env.
- dependencies_and_callers: Depends on pi-ai streaming, dialect renderers/scanners, schema validators, telemetry helpers, `yieldIfDue`, and tool definitions. Called by coding-agent sessions and subagent/task flows.
- edge_cases_or_failure_modes: Harmony leak interruption retries/truncate-resume, stream interruption after content, incomplete tool-call retention on explicit abort, concurrent shared/exclusive tools, queued steering during interruptible tools, paused-turn continuation cap, and skipped placeholders for truncated tool calls.
- validation_or_tests: `packages/agent/test/yield.test.ts` covers yield primitives; broader behavior is validated by many `packages/ai`/coding-agent agent-loop regression tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-416 `file` `packages/agent/test/yield.test.ts`
- cursor: `[_]`
- core_role: Regression tests for cooperative yielding primitives used by the agent loop.
- algorithmic_behavior: Installs a fake clock and asserts `yieldIfDue` sleeps on first call, gates immediate callers, sleeps again after the interval, and that `ExponentialYield.race` returns racer values promptly and cancels losing sleeps.
- inputs_outputs_state: Inputs are fake time advances and promises; outputs are observed sleeps/resolution values and absence of loop-retaining timers.
- gates_or_invariants: Yield interval constants must prevent busy waiting without sleeping every call; losing sleep in `race` must be canceled.
- dependencies_and_callers: Tests `yieldIfDue`/`ExponentialYield`, which are called in `agent-loop.ts` during turn/tool loops.
- edge_cases_or_failure_modes: Immediate repeated callers, elapsed gate windows, and slow sleep promises that could keep the event loop alive.
- validation_or_tests: This file is itself the validation.
- skip_candidate: `yes: test-only file; validates scheduling/yield behavior but is not runtime implementation`

### OH_MY_HUMANIZE_MAIN-HZ-446 `file` `packages/ai/test/anthropic-retry.test.ts`
- cursor: `[_]`
- core_role: Retry classifier regression tests for Anthropic/provider transient errors.
- algorithmic_behavior: Asserts `isProviderRetryableError` retries transient rate-limit wording, stream parse/pre-content envelope failures, HTTP/2 internal stream errors, Bun socket closure, first-event timeout, and Copilot transient `model_not_supported` only for GitHub Copilot.
- inputs_outputs_state: Inputs are synthetic error messages/status/provider ids; outputs are boolean retryability expectations.
- gates_or_invariants: Post-content envelope failures, non-transient validation errors, and persistent account usage/quota limits must not be classified retryable.
- dependencies_and_callers: Validates retry decisions consumed by pi-ai streaming/request paths.
- edge_cases_or_failure_modes: Rate-limit wording that actually indicates persistent quota, provider-specific Copilot transient model availability, and stream failures before vs after content.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-476 `file` `packages/ai/test/auth-storage-codex-selection.test.ts`
- cursor: `[_]`
- core_role: Contract tests for OAuth credential selection/ranking across Codex and Claude accounts.
- algorithmic_behavior: Builds synthetic usage reports and credentials, repeatedly selects API keys, and asserts weighting by near-reset/fresh windows, exhaustion skipping, earliest-unblocking fallback, Spark Pro-vs-Plus routing, ranking timeout behavior, parallel refresh before selection, and Claude secondary drain-rate balancing.
- inputs_outputs_state: Inputs are mocked OAuth credentials, usage providers/reports, model ids, expiry timestamps, and selection counts. Outputs are selected API key distributions and refresh calls.
- gates_or_invariants: Exhausted accounts cannot win unless all are exhausted; slow usage ranking must not block first selection; equal-priority Claude accounts balance; strongest bucket is capped near 2x baseline.
- dependencies_and_callers: Validates `AuthStorage` selection, usage provider interfaces, and provider-specific ranking strategies in `packages/ai/src/usage`.
- edge_cases_or_failure_modes: Usage fetch failure returning null, expired candidates requiring refresh, single credential path, Plus fallback when no Pro connected, and all-exhausted fallback.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-506 `file` `packages/ai/test/github-copilot-anthropic-auth.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Anthropic Messages auth/header construction when routed through GitHub Copilot or OpenCode Go.
- algorithmic_behavior: Creates Copilot/OpenCode model fixtures and checks whether auth config uses `Authorization: Bearer`, `apiKey: null`, or `X-Api-Key`; verifies structured enterprise credentials, normalized base URLs, static header merge, beta header selection, content type/version headers, and `initiatorOverride` forwarding.
- inputs_outputs_state: Inputs are model definitions, structured credential values, request contexts, and mocked fetch capture. Outputs are request headers/base URLs/auth config assertions.
- gates_or_invariants: Copilot must not set `isOAuthToken`, must not duplicate auth headers after case-insensitive merge, and must not include fine-grained tool streaming beta.
- dependencies_and_callers: Validates `providers/anthropic*`, Copilot header helpers, and auth resolution for Anthropic-compatible providers.
- edge_cases_or_failure_modes: Enterprise credentials choosing enterprise base URL, trailing `/v1` normalization, and static headers overriding/merging with generated headers.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-536 `file` `packages/ai/test/issue-1701-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for forced `tool_choice` guard behavior across OpenAI-compatible APIs.
- algorithmic_behavior: Builds OpenAI Completions, OpenAI Responses, Azure Responses, and Codex Responses model fixtures; captures outgoing payloads with absent/present `todo` tool; asserts forced `tool_choice` is dropped when named tool is absent and retained when present.
- inputs_outputs_state: Inputs are contexts with/without target tool, forced tool choice, fake models, and captured fetch bodies. Outputs are payload tool names and `tool_choice` presence/absence.
- gates_or_invariants: Providers must never send a forced named tool choice if that tool is not in the advertised tool list.
- dependencies_and_callers: Validates OpenAI completions/responses request builders and tool-choice utilities.
- edge_cases_or_failure_modes: Azure and Codex response variants, custom fork/search tools coexisting with absent `todo`, and aborted signal helper in payload capture.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-566 `file` `packages/ai/test/models-json-no-local-endpoints.test.ts`
- cursor: `[_]`
- core_role: Generated catalog leak guard for bundled model metadata.
- algorithmic_behavior: Loads `models.json`, asserts no local-only provider blocks are bundled, and scans base URLs for loopback/private-network hosts.
- inputs_outputs_state: Input is generated catalog JSON; outputs are test failures listing leaked provider/base URL entries.
- gates_or_invariants: Loopback/private IPv4, localhost-like hosts, and local provider entries must not ship in the bundled catalog.
- dependencies_and_callers: Protects model catalog generation and runtime provider resolution in `packages/ai`/`packages/catalog`.
- edge_cases_or_failure_modes: Numeric private networks, loopback aliases, and generated local development endpoints accidentally entering published metadata.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-596 `file` `packages/ai/test/openai-responses-openrouter.test.ts`
- cursor: `[_]`
- core_role: Request-shape parity tests for OpenRouter pseudo APIs and OpenAI Responses.
- algorithmic_behavior: Captures pseudo chat and pseudo Responses payloads, compares Anthropic and non-Anthropic reasoning payloads, stop/frequency penalty handling, OpenRouter variant appending, provider routing preservation, reasoning disablement, max token defaults, header override precedence, and replay of native Responses history after pseudo OpenRouter turns.
- inputs_outputs_state: Inputs are synthetic OpenRouter models, contexts, tool/history messages, caller headers, and mock fetch responses. Outputs are captured request bodies/headers and assertions over model ids, reasoning, provider routing, and max token fields.
- gates_or_invariants: OpenRouter Responses should omit default `max_output_tokens` unless explicitly required/caller capped; caller headers override attribution/cache defaults; Chat-only fields are dropped for Responses.
- dependencies_and_callers: Validates OpenRouter compatibility logic in OpenAI chat/responses providers.
- edge_cases_or_failure_modes: Variant suffix only when final slash segment has no variant, mixed native/pseudo history replay, and direct-provider max-token behavior.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-626 `file` `packages/ai/test/schema-normalization.test.ts`
- cursor: `[_]`
- core_role: Schema adapter regression suite for provider compatibility and strict tool validation.
- algorithmic_behavior: Exercises enum merging, strict-mode sanitization, draft upgrades, Google normalization, MCP normalization, OpenAI Responses sanitization, empty-schema normalization, Zod leaked enum/literal/union recovery, local `$ref` inlining, unsupported regex lookaround stripping, and self-referential schema termination.
- inputs_outputs_state: Inputs are JSON Schema/Zod-like objects and model fixtures; outputs are normalized schemas and semantic assertions over properties, enums, anyOf, additionalProperties, required fields, and descriptions.
- gates_or_invariants: Boolean/empty schemas must retain semantics; property literally named `additionalProperties` must not be mistaken for the keyword; recursive schemas must not loop infinitely; invalid Zod residue must become valid JSON Schema.
- dependencies_and_callers: Validates `packages/ai/src/utils/schema/*`, provider request builders, and built-in tool schema compatibility.
- edge_cases_or_failure_modes: Object-valued enum deep equality, nullable/const combinations, draft-07 dependencies/contentSchema, non-array `oneOf`, and OpenAI unsupported regex features.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-656 `file` `packages/catalog/scripts/generated-policies.ts`
- cursor: `[_]`
- core_role: Catalog generation post-processing policy module for generated model specs.
- algorithmic_behavior: Applies generated model policies, rebakes thinking metadata, links OpenAI promotion targets, applies canonical limit fallbacks, handles provider-specific fallback/caps, infers apply-patch tool type, and assigns priority/limits for Codex/OpenAI/Anthropic/Copilot/Fireworks-like generated models (`packages/catalog/scripts/generated-policies.ts:69-320`).
- inputs_outputs_state: Input is mutable `ModelSpec<Api>[]`; outputs are in-place mutations to thinking policies, priorities, max token/context limits, fallback models, tool capabilities, and provider-specific metadata.
- gates_or_invariants: Generated catalog fixups must happen in source policy code, not direct `models.json` edits; canonical limit fallback should not overwrite explicit data incorrectly; Kimi K2 caps must match public ceiling.
- dependencies_and_callers: Called by `packages/catalog/scripts/generate-models.ts`; depends on identity classifiers and catalog model spec types.
- edge_cases_or_failure_modes: Multiple provider wire ids for same canonical family, missing upstream limits, OpenAI variants with priority ordering, and fallback model handling for Cloudflare AI Gateway.
- validation_or_tests: `packages/catalog/test/issue-1849-repro.test.ts` validates Kimi K2 cap policy; generated catalog tests validate bundled output.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-686 `file` `packages/catalog/test/issue-1849-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Fireworks/Fire Pass Kimi K2 max-token cap.
- algorithmic_behavior: Asserts Kimi K2.x public/wire ids are recognized, generated policy clamps candidate max tokens to published ceiling, leaves unrelated models untouched, and bundled Fireworks/Fire Pass catalog ships capped values.
- inputs_outputs_state: Inputs are model ids/specs and bundled catalog entries; outputs are max token assertions.
- gates_or_invariants: Kimi K2.x variants must not inherit unsafe excessive generation caps from upstream metadata.
- dependencies_and_callers: Validates `generated-policies.ts`, identity classification, and bundled catalog.
- edge_cases_or_failure_modes: Public vs provider wire model id aliases and unrelated model false positives.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-716 `file` `packages/coding-agent/bench/session-tree-nav.bench.ts`
- cursor: `[_]`
- core_role: Microbenchmark for session tree navigation/deduplication behavior.
- algorithmic_behavior: Builds synthetic session entries with many messages/code blocks, warms up functions, compares old two-walk behavior vs one-walk dedupe fix, and reports saved milliseconds/percentage.
- inputs_outputs_state: Inputs are generated `SessionEntry[]`, message ids, and iteration counts. Outputs are benchmark timings printed to stdout.
- gates_or_invariants: The intended invariant is that one traversal should produce equivalent navigation information with less work than two traversals.
- dependencies_and_callers: Uses session tree/navigation helpers in coding-agent bench context.
- edge_cases_or_failure_modes: Large transcripts with many code blocks where repeated walks amplify cost.
- validation_or_tests: Benchmark-only; not a pass/fail test unless manually interpreted.
- skip_candidate: `yes: benchmark artifact; useful performance evidence but not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-746 `file` `packages/coding-agent/test/advisor-toggle.test.ts`
- cursor: `[_]`
- core_role: Tests for per-session advisor model toggle state.
- algorithmic_behavior: Constructs sessions/settings and asserts advisor starts disabled, toggle enables runtime, explicit enable overrides default-off for current session only, toggle disables runtime, missing advisor model reports inactive, and sessions remain isolated under shared settings.
- inputs_outputs_state: Inputs are session settings and advisor model availability; outputs are advisor enabled/active flags and runtime state assertions.
- gates_or_invariants: Advisor enablement is session-local and cannot leak across sessions; active state requires an assigned advisor model.
- dependencies_and_callers: Validates `AgentSession` advisor controls and status/runtime integration.
- edge_cases_or_failure_modes: Shared `Settings` instance across sessions and explicit enable while default setting is off.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-776 `file` `packages/coding-agent/test/agent-session-python-cleanup.test.ts`
- cursor: `[_]`
- core_role: Regression suite for Python/eval kernel ownership cleanup during agent session lifecycle.
- algorithmic_behavior: Uses fake kernels and mocked sleeps to assert create-session failures do not dispose unrelated Python owners, shared retained kernels wait for active SDK Python work, dispose aborts tracked eval execution, retained ownership detaches after timeout, and new Python/eval starts are rejected once disposal begins.
- inputs_outputs_state: Inputs are fake kernel executions, session construction hooks, disposal timing, async hook yields, and concurrent eval calls. Outputs are disposal/abort calls, rejected start attempts, ownership state, and timing assertions.
- gates_or_invariants: Session disposal must not leak or kill unrelated owners; once dispose begins no new session-owned Python/eval work may start; active owned executions must be aborted or waited within timeout.
- dependencies_and_callers: Validates `AgentSession`, eval backend ownership, Python kernel registry, and user Python hook lifecycle.
- edge_cases_or_failure_modes: Failure before/after session construction, warmup race, dispose timeout, async hook returning after dispose starts, and concurrent active executions.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-806 `file` `packages/coding-agent/test/autolearn-tools-gating.test.ts`
- cursor: `[_]`
- core_role: Tests for autolearn/manage-skill tool availability and execution contracts.
- algorithmic_behavior: Builds sessions under different autolearn/memory settings; asserts manage_skill/learn gating, explicit restricted toolNames force-inclusion, subagent exclusion, file-backend learn support, managed SKILL.md create/delete/update validation, authored-skill shadow protection, lesson storage, managed skill minting, and partial-outcome errors.
- inputs_outputs_state: Inputs are settings, fake memory backend, skill payloads, managed skill filesystem paths, and Hindsight queue mode. Outputs are active tool sets, skill file changes, memory writes/queued messages, and tool result text/errors.
- gates_or_invariants: Autolearn disabled hides tools; learn requires memory/local backend; subagents cannot receive autolearn tools; managed skill names/bodies are schema-validated and cannot shadow authored skills.
- dependencies_and_callers: Validates autolearn tool factory, managed skills, memory backend interface, and active tool selection.
- edge_cases_or_failure_modes: Create without body, delete missing skill, invalid skill name after lesson store, Hindsight queued partial outcomes, and Mnemopi returning no id.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-836 `file` `packages/coding-agent/test/compaction.test.ts`
- cursor: `[_]`
- core_role: Large compaction subsystem contract tests.
- algorithmic_behavior: Tests token calculation, last assistant usage selection, compaction threshold decisions, remote/local compaction routing, OpenAI/Codex remote preserve data, filtering remote compact output, stale preserve clearing, cut-point selection, session context rebuild after compaction, snapcompact frame reattachment, model/thinking change tracking, and large-session fixture compaction.
- inputs_outputs_state: Inputs are synthetic `SessionEntry` messages/usages, compaction entries, model/thinking change entries, large fixture entries, settings, and mocked summarization/completion. Outputs are compaction decisions, cut indices, rebuilt session contexts, preserve data, and compacted summaries.
- gates_or_invariants: Aborted assistant usage is skipped; threshold honors configured percent/default reserve behavior; latest compaction wins; transcript option keeps full history; remote compaction must preserve provider-native replay metadata where required.
- dependencies_and_callers: Validates coding-agent compaction utilities, session context builder, OpenAI/Codex compact endpoints, and snapcompact integration.
- edge_cases_or_failure_modes: Split turns, no valid cut points, all messages fit, first kept entry at first message, stale remote preserve data after local compaction, and large real transcript shape.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-866 `file` `packages/coding-agent/test/git-process-config.test.ts`
- cursor: `[_]`
- core_role: Tests for safe git subprocess config.
- algorithmic_behavior: Mocks `Bun.spawn` calls and asserts read-only and mutating git commands disable fsmonitor/untracked cache, and pushes are scoped to a named refspec rather than following tags.
- inputs_outputs_state: Inputs are fake spawn calls, stdout/stderr streams, and git wrapper invocations. Outputs are captured command/env/args assertions.
- gates_or_invariants: Git operations should avoid repo fsmonitor/untracked cache side effects and `push` must not follow tags implicitly.
- dependencies_and_callers: Validates coding-agent git utilities used by tools, session management, commit, and workflows.
- edge_cases_or_failure_modes: Mutating vs read-only command paths and unsafe push defaults.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-896 `file` `packages/coding-agent/test/install-command.test.ts`
- cursor: `[_]`
- core_role: Tests for plugin/install command routing and local-path detection.
- algorithmic_behavior: Asserts `install` is registered as a top-level command, reserved management words are rejected only when bare, and `looksLikeLocalPath` recognizes relative/absolute/home/Windows/bare-existing directories while leaving npm specs and marketplace refs remote.
- inputs_outputs_state: Inputs are CLI args and candidate strings/filesystem dirs. Outputs are command recognition and boolean path classification.
- gates_or_invariants: Existing bare local directories must be treated as local installs; npm-style and marketplace-style specs must remain remote.
- dependencies_and_callers: Validates install command parser/dispatcher and marketplace/plugin install workflows.
- edge_cases_or_failure_modes: Windows drive prefixes, `~` paths, explicit relative paths, and reserved words with extra qualifiers.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-926 `file` `packages/coding-agent/test/issue-851-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Claude plugin `.mcp.json` flat-shape loading.
- algorithmic_behavior: Creates `.mcp.json` shapes where top-level keys are server names and asserts stdio/http transport entries register while entries without command/url are skipped.
- inputs_outputs_state: Inputs are project plugin MCP JSON files; outputs are loaded MCP server registrations.
- gates_or_invariants: Flat shape must be accepted in addition to nested config; invalid entries must not produce servers.
- dependencies_and_callers: Validates plugin/capability discovery and MCP manager inputs.
- edge_cases_or_failure_modes: HTTP transport via URL, absent command/url, and plugin format compatibility.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-956 `file` `packages/coding-agent/test/main-session-resolution-error.test.ts`
- cursor: `[_]`
- core_role: Tests for startup notice routing and missing session resolution errors.
- algorithmic_behavior: Builds resume/fork args, captures stdout/stderr, asserts startup notices go to stdout outside JSON mode and stderr in JSON mode, and verifies `createSessionManager` rejects invalid `--resume`/`--fork` combinations with `SessionResolutionError` and usage hints.
- inputs_outputs_state: Inputs are CLI args, settings stubs, and process output capture. Outputs are captured text and rejected errors.
- gates_or_invariants: JSON mode stdout must stay clean; missing session errors must include actionable usage hints unless the error is invalid `--fork --no-session`.
- dependencies_and_callers: Validates main session resolution/startup paths.
- edge_cases_or_failure_modes: Missing resume id, missing fork id, and incompatible fork/no-session flags.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-986 `file` `packages/coding-agent/test/model-registry-runtime-provider.test.ts`
- cursor: `[_]`
- core_role: Runtime provider registration/refresh tests for the model registry.
- algorithmic_behavior: Registers custom/runtime providers and asserts config validation before mutation, header/auth overrides persist across offline/online refresh, explicit thinking and wire facts are preserved, extension providers survive refresh cycles, API keys/custom handlers survive, re-registration replaces overlays, source handoff clears stale transport overrides, and source-scoped registrations can be cleared/synced.
- inputs_outputs_state: Inputs are provider configs, model overrides, extension source ids, refresh modes, headers/auth settings. Outputs are registry models, provider state, auth resolution, transport overrides, and cleared source entries.
- gates_or_invariants: Invalid provider config must not mutate state; runtime headers override modelOverrides; source handoff must not retain stale previous-source headers/auth.
- dependencies_and_callers: Validates model registry runtime-provider overlay system used by extensions/plugins.
- edge_cases_or_failure_modes: Multiple extension providers, headers-only overrides preserving baseUrl, transport-only source handoff, and online/offline refresh persistence.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1016 `file` `packages/coding-agent/test/repro-issue-1020-ctx-shutdown.test.ts`
- cursor: `[_]`
- core_role: Regression tests for extension `ctx.shutdown()` in interactive mode.
- algorithmic_behavior: Asserts `contextActions.shutdown` sets `InteractiveModeContext.shutdownRequested`, and `initHooksAndCustomTools` wires extension shutdown calls to that flag.
- inputs_outputs_state: Inputs are fake interactive context and hook/custom tool initialization. Outputs are `shutdownRequested` flag changes.
- gates_or_invariants: Extension-requested shutdown must signal the interactive context instead of being ignored.
- dependencies_and_callers: Validates extension runtime context actions and hook initialization.
- edge_cases_or_failure_modes: Async emit no-op context and shutdown request propagation through initialized hooks.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1046 `file` `packages/coding-agent/test/selector-settings-side-effects.test.ts`
- cursor: `[_]`
- core_role: Tests for runtime setting selector side effects on TUI components.
- algorithmic_behavior: Initializes in-memory settings and asserts changing git integration refreshes status line, while changing `tui.tight` invalidates UI and updates editor top border.
- inputs_outputs_state: Inputs are selector setting changes; outputs are callback invocations and component state changes.
- gates_or_invariants: Runtime settings mutations must propagate to visible UI immediately.
- dependencies_and_callers: Validates selector/settings controller interactions with status line/editor.
- edge_cases_or_failure_modes: Settings changes after initialization and component invalidation ordering.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1076 `file` `packages/coding-agent/test/status-line-model.test.ts`
- cursor: `[_]`
- core_role: Tests for advisor badge rendering in status line model segment.
- algorithmic_behavior: Builds `SegmentContext` and asserts active advisor appends a success-colored `++` badge while inactive advisor omits it.
- inputs_outputs_state: Inputs are advisorActive boolean and model context; outputs are rendered segment strings/styles.
- gates_or_invariants: Advisor badge reflects active runtime, not merely configured state.
- dependencies_and_callers: Validates status line rendering.
- edge_cases_or_failure_modes: Advisor inactive with otherwise normal model segment.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1106 `file` `packages/coding-agent/test/tiny-worker-env.test.ts`
- cursor: `[_]`
- core_role: Tests for tiny inference worker environment overlay.
- algorithmic_behavior: Asserts non-default persisted settings map to worker env vars when env absent, existing env wins over settings, and default sentinel/unset settings are omitted.
- inputs_outputs_state: Inputs are settings values and existing env map; outputs are overlay env vars.
- gates_or_invariants: Explicit environment variables have precedence; defaults should not bloat worker env.
- dependencies_and_callers: Validates worker spawning environment for tiny/local inference.
- edge_cases_or_failure_modes: Default sentinel values and unset settings.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1136 `file` `packages/collab-web/src/main.tsx`
- cursor: `[_]`
- core_role: Minimal React/Vite entrypoint for collab web UI.
- algorithmic_behavior: Locates DOM `#root` and mounts the application component through React rendering.
- inputs_outputs_state: Input is browser DOM root. Output is mounted React app state under the root element.
- gates_or_invariants: Requires `#root` to exist; no routing or business algorithm appears in this file.
- dependencies_and_callers: Depends on React/ReactDOM and local app component.
- edge_cases_or_failure_modes: Missing root element would prevent rendering.
- validation_or_tests: No direct test inspected for this tiny entrypoint.
- skip_candidate: `yes: bootstrap entrypoint only; not a core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1166 `file` `packages/hashline/test/landing-shift.test.ts`
- cursor: `[_]`
- core_role: Regression tests for hashline insert landing-shift algorithms.
- algorithmic_behavior: Applies patches to fixture text and asserts after-insert landing shifts move shallower bodies past closing lines, cross multiple closer levels, preserve same-depth inserts, never cross content lines, treat pure closers as neutral, skip incomparable indentation styles, avoid crossing other hunks, and handle `INS.BLK.POST` inward placement.
- inputs_outputs_state: Inputs are hashline patch strings and source text; outputs are transformed text and warnings.
- gates_or_invariants: Landing shift must be conservative around targeted lines and indentation-style mismatches; block-post inserts can be placed inside blocks when body depth proves intent.
- dependencies_and_callers: Validates `@oh-my-pi/hashline` patch application behavior consumed by coding-agent edit integration.
- edge_cases_or_failure_modes: Blank lines between anchor and closer, tabs vs spaces, nested trailing closers, empty blocks, and plain insert on closer remaining literal.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1196 `file` `packages/mnemopi/test/consolidate-fact-sibling-races.test.ts`
- cursor: `[_]`
- core_role: Tests for Mnemopi veracity consolidator sibling-write race semantics.
- algorithmic_behavior: Uses SQLite-backed `VeracityConsolidator` to assert `resolve_conflict` first-writer-wins, `resolve_conflict_by_facts` supersedes only losing fact, consolidation resolves high-confidence conflicts safely, serialized writes commit/rollback and respect caller-owned transactions, and stats/fact reads exclude superseded facts.
- inputs_outputs_state: Inputs are temp DB facts/conflicts/transactions. Outputs are fact states, supersession flags, consolidation results, and stats.
- gates_or_invariants: Conflict resolution must not supersede winning sibling facts twice; nested serialized writes must not corrupt caller transactions.
- dependencies_and_callers: Validates Mnemopi core consolidation/storage logic.
- edge_cases_or_failure_modes: Sibling write races, rollback behavior, nested transaction ownership, and high-confidence auto-resolution.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1226 `file` `packages/mnemopi/test/proactive-linking.test.ts`
- cursor: `[_]`
- core_role: Tests for proactive memory graph edge creation.
- algorithmic_behavior: Toggles proactive linking and asserts similar content creates `related_to` edges, unrelated content does not, shared extracted entities create `references` edges, per-remember options override default disabled state, and duplicate remember updates do not duplicate edges.
- inputs_outputs_state: Inputs are `BeamMemory` remember calls, extracted entities, env/default toggles. Outputs are `EpisodicGraph` related memory edge sets.
- gates_or_invariants: Linking is off by default and must dedupe edges.
- dependencies_and_callers: Validates Mnemopi memory graph/proactive linking behavior used by memory recall.
- edge_cases_or_failure_modes: Unrelated similarity false positives and duplicate updates.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1256 `file` `packages/natives/test/issue-823-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for standalone-binary native loader path resolution.
- algorithmic_behavior: Asserts compiled-binary mode can be detected from embedded addon presence, embedded-extracted candidates are ordered ahead of build-host candidates, user-data candidates are skipped outside standalone, platform leaf package candidates precede core nativeDir on npm installs, Windows staging precedence is retained, dev candidate list is unchanged without leaf package, and bundled native variants extract from a gzip archive while skipping current files.
- inputs_outputs_state: Inputs are fake native dirs, platform/arch/install-mode metadata, bundled archive contents, and candidate resolution inputs. Outputs are candidate path arrays and extracted files.
- gates_or_invariants: Standalone binary must not load build-host native addon accidentally; npm install should prefer platform leaf packages; extraction should avoid overwriting current files unnecessarily.
- dependencies_and_callers: Validates native loader/staging logic used by `@oh-my-pi/pi-natives`.
- edge_cases_or_failure_modes: Missing env/url markers, linux-x64 standalone, Windows staging, dev mode without leaf package, and multi-variant archive extraction.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1286 `file` `packages/snapcompact/research/exp14_bestgpt.py`
- cursor: `[_]`
- core_role: Research experiment runner for visual/text snapcompact evaluation against GPT-like models.
- algorithmic_behavior: Caches model calls, lays out document paragraphs into pages, renders document/grid image variants, submits QA calls, runs document-page or grid-chunk units in parallel, aggregates records, labels cells, and writes outputs (`packages/snapcompact/research/exp14_bestgpt.py:58-455`).
- inputs_outputs_state: Inputs are CLI args, cells spec, source paragraphs/questions, model configs, cache paths, and image rendering options. Outputs are rendered images, QA records, aggregate metrics, and experiment result files.
- gates_or_invariants: Cache keys include model/tag/payload; atomic image save avoids partial files; parallel executor batches units; output aggregation groups by condition/length/effort.
- dependencies_and_callers: Research-only script depending on PIL/image rendering, model call client utilities, concurrent futures, and local snapcompact experiment data.
- edge_cases_or_failure_modes: Long text wrapping/pagination, cache freshness, image size variants, multi-cell parsing, and failed model calls.
- validation_or_tests: No direct test; research script outputs metrics for manual/experimental validation.
- skip_candidate: `yes: research experiment script; algorithmic but not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1316 `file` `packages/snapcompact/research/snapcompact_materialize_viz.py`
- cursor: `[_]`
- core_role: Research visualization materializer for snapcompact experiment outputs.
- algorithmic_behavior: Resolves UI/mono fonts, crops answer regions from images based on condition metadata and answer indices, and drives a CLI `main()` to materialize visualization assets (`packages/snapcompact/research/snapcompact_materialize_viz.py:35-71`).
- inputs_outputs_state: Inputs are image paths, condition dicts, answer start/end positions, image size, and output args. Outputs are cropped PIL images/files.
- gates_or_invariants: Font fallback must be available; crop coordinates must remain within generated image dimensions.
- dependencies_and_callers: Research tooling using PIL and experiment JSON/image artifacts.
- edge_cases_or_failure_modes: Missing fonts/images, invalid answer ranges, and condition metadata mismatch.
- validation_or_tests: No direct automated test inspected.
- skip_candidate: `yes: research visualization helper, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1346 `file` `packages/stats/src/db.ts`
- cursor: `[_]`
- core_role: SQLite persistence/query layer for local observability dashboard stats.
- algorithmic_behavior: Initializes schema/backfills, tracks processed session file offsets, inserts message/user-message stats, calculates/backfills catalog costs, aggregates overall/model/folder/time-series/cost/behavior stats, repairs user message links, marks backfill completion, and maps rows back to typed stats (`packages/stats/src/db.ts:50-1070`).
- inputs_outputs_state: Inputs are session file offsets, message stats, user message stats, catalog models/costs, cutoff times, bucket sizes, and backfill flags. Outputs are DB writes, aggregate stats, recent requests/errors, cost series, and behavior metrics.
- gates_or_invariants: Backfill metadata prevents repeated expensive repairs unless reset; stored cost resolves from row or catalog; inserts return counts; unknown models/folders are normalized for grouping.
- dependencies_and_callers: Used by stats sync worker/dashboard; depends on Bun SQLite, model catalog, stats types, and local agent session ingestion.
- edge_cases_or_failure_modes: Missing catalog costs, stale backfill keys, priority premium request backfill, user-message link repair, cutoff filtering, and empty DB aggregate defaults.
- validation_or_tests: Stats package tests not assigned here; behavior is indirectly validated by dashboard/sync tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1376 `file` `packages/tui/src/kill-ring.ts`
- cursor: `[_]`
- core_role: Small TUI kill-ring buffer for cut/yank style text operations.
- algorithmic_behavior: Maintains a bounded list of killed text entries, rotates/yanks through recent entries, and caps storage at `MAX_ENTRIES = 60`.
- inputs_outputs_state: Inputs are killed text strings and yank/rotate calls. Outputs are current/rotated text values and internal entry/index updates.
- gates_or_invariants: Empty kills should not pollute history; ring length must not exceed max entries; index must stay valid after mutations.
- dependencies_and_callers: Used by TUI editor/input components.
- edge_cases_or_failure_modes: Empty ring yanks, repeated kills, and cap trimming.
- validation_or_tests: Covered indirectly by TUI editor tests; no dedicated kill-ring test observed in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1406 `file` `packages/tui/test/issue-1962-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for differential renderer behavior after dirty scrollback.
- algorithmic_behavior: Uses virtual terminal components to assert arrow-key frames do not clear and replay the whole transcript for focused updates, both normally and inside overlays.
- inputs_outputs_state: Inputs are mutable lines component, focused selector, key events, and captured terminal writes. Outputs are write buffers without excessive erase scrollback sequences.
- gates_or_invariants: Focused navigation frames must use stable incremental repaint, not full transcript clear/replay.
- dependencies_and_callers: Validates TUI renderer engine and overlay/focus interactions.
- edge_cases_or_failure_modes: Dirty scrollback state and overlay composition around focused components.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1436 `file` `packages/tui/test/render-stable-prefix.test.ts`
- cursor: `[_]`
- core_role: Contract tests for `RenderStablePrefix` differential rendering.
- algorithmic_behavior: Defines stable list/prompt components and asserts appended rows emit exactly once/in order, lowered floor repaints interior mutations, and cursor markers below stable prefix remain honored.
- inputs_outputs_state: Inputs are component rows, virtual terminal render cycles, and mutable rows. Outputs are captured terminal buffers and cursor positions.
- gates_or_invariants: Stable prefix may be reused only above the reported floor; appended rows must not duplicate; cursor semantics below stable prefix must survive.
- dependencies_and_callers: Validates TUI render engine optimization used by transcript rendering.
- edge_cases_or_failure_modes: Interior row mutation under a previously stable prefix and bottom component cursor changes.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1466 `file` `packages/tui/test/visible-width.test.ts`
- cursor: `[_]`
- core_role: Width-calculation parity tests for TUI visible width handling.
- algorithmic_behavior: Compares JS visible-width logic against native width engine across control/ANSI/tab/OSC 66 cases; asserts ANSI stripping, tab expansion, and OSC text-sizing scaling.
- inputs_outputs_state: Inputs are strings with escapes, tabs, ANSI sequences, and sizing payloads. Outputs are numeric widths.
- gates_or_invariants: Styled text measures as plain content; tabs use configured width; OSC 66 scale multiplier affects width.
- dependencies_and_callers: Validates TUI text measurement used by rendering/wrapping/truncation.
- edge_cases_or_failure_modes: BEL/ST terminated OSC sequences, escape stripping, and configured tab width.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1496 `file` `packages/utils/src/mermaid-ascii.ts`
- cursor: `[_]`
- core_role: Utility wrapper for rendering Mermaid diagrams to ASCII and extracting Mermaid blocks from Markdown.
- algorithmic_behavior: Exports `renderMermaidAscii`, safe nullable wrapper, and `extractMermaidBlocks` that returns Mermaid block source plus hash.
- inputs_outputs_state: Inputs are Mermaid source strings, render options, and Markdown text. Outputs are ASCII render strings/null and extracted block descriptors.
- gates_or_invariants: Safe wrapper returns null on render failure rather than throwing; block extraction identifies fenced Mermaid blocks.
- dependencies_and_callers: Wraps vendored `mermaid-ascii` renderer and hashing utility; used by docs/TUI/text rendering surfaces.
- edge_cases_or_failure_modes: Invalid Mermaid syntax and Markdown with multiple or malformed fences.
- validation_or_tests: Vendored validation file is assigned below; no direct test for wrapper in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1526 `file` `packages/utils/test/loop-phase.test.ts`
- cursor: `[_]`
- core_role: Tests for loop-phase stack tracking utility.
- algorithmic_behavior: Drains state, asserts empty stack undefined, nested push/pop exposes strict LIFO top labels, underflow pop stays undefined, `takeRecentLoopPhase` surfaces a popped phase once, and live phase takes precedence over recent slot.
- inputs_outputs_state: Inputs are phase labels and push/pop/take operations. Outputs are current/recent phase values.
- gates_or_invariants: Stack operations must be LIFO; underflow must be harmless; recent phase is one-shot unless a live phase exists.
- dependencies_and_callers: Validates utility used for event-loop/phase diagnostics.
- edge_cases_or_failure_modes: Empty pop, nested phases, and recent/live precedence.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1556 `file` `python/robomp/src/github_backend.py`
- cursor: `[_]`
- core_role: Python protocol interface for GitHub backend implementations.
- algorithmic_behavior: Defines `GitHubBackend` protocol methods for repository/issue/PR/comment/review/label/reaction/auth operations used by RoboMP components.
- inputs_outputs_state: Inputs are repo names, issue/PR numbers, comment/review ids, bodies, labels, assignees, and pagination/filter params. Outputs are backend-specific dict/list responses.
- gates_or_invariants: Implementations must satisfy method signatures so orchestrator/proxy code can swap direct GitHub vs proxy backends.
- dependencies_and_callers: Used by `python/robomp` GitHub client/proxy/orchestrator layers.
- edge_cases_or_failure_modes: Protocol-only file; runtime failures depend on concrete implementation auth/network behavior.
- validation_or_tests: Proxy endpoint tests exercise backend-compatible shapes indirectly.
- skip_candidate: `yes: type/protocol surface only; no runtime algorithm implemented here`

### OH_MY_HUMANIZE_MAIN-HZ-1586 `file` `python/robomp/tests/test_proxy_server.py`
- cursor: `[_]`
- core_role: HMAC, GitHub forwarding, and git workspace proxy server regression suite.
- algorithmic_behavior: Builds FastAPI app with mocked GitHub transport; signs requests; tests HMAC accept/reject, GitHub repo/issue/list/comment/review/label/reaction/close/PR endpoints, GitHub error passthrough, git clone/fetch/push workspace behavior, slot UID handling, head drift, workspace key mismatch, query mutation rejection, and oversized content-length handling.
- inputs_outputs_state: Inputs are temporary settings, bare upstream repos, signed HTTP requests, mocked GitHub responses, workspace clones, branch/head values, and slot ids. Outputs are HTTP status/payload assertions and local git branch/workspace state.
- gates_or_invariants: HMAC must cover method/path/query/body/timestamp; stale/bad/missing signatures reject; oversized bodies reject before read; git push requires expected head/workspace key/valid slot; upstream branch must not update on drift.
- dependencies_and_callers: Validates `robomp.proxy.server`, `GitHubClient`, proxy HMAC signing, sandbox workspace keying, and git helper functions.
- edge_cases_or_failure_modes: Safe directory and slot identity, missing alternates repair, malicious origin URL/repo mismatch, query replay mutation, 422 passthrough, and invalid slot UIDs.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1616 `directory` `packages/coding-agent/src/edit/hashline`
- cursor: `[_]`
- core_role: Coding-agent integration layer for the hashline edit patch format.
- algorithmic_behavior: Recursively includes native block resolution cache, read-only streaming diff preview, edit execution via hashline `Patcher`, filesystem adapter, model-facing params schema, and no-op loop guard. It parses `{input}`, validates snapshots, resolves block edits, preflights multi-section edits, writes via LSP writethrough, invalidates FS scan cache, attaches diagnostics/meta, and escalates repeated byte-identical no-ops (`execute.ts:155-237`, `filesystem.ts:43-130`, `diff.ts:248-290`).
- inputs_outputs_state: Inputs are tool-call input, `ToolSession`, cwd, file snapshot store, LSP batch/writethrough callbacks, abort signal, and current file contents. Outputs are `AgentToolResult` with text, diff, firstChangedLine, diagnostics, per-file results, and filesystem writes.
- gates_or_invariants: File creation rejected by hashline path (write tool owns creation); multi-section patches prepare all sections before any write; duplicate canonical targets reject; generated/plan-mode guards run before writes; repeated identical no-op reaches hard failure at limit 3.
- dependencies_and_callers: Used by coding-agent edit tool; depends on `@oh-my-pi/hashline`, `@oh-my-pi/pi-natives` `blockRangeAt`, LSP writethrough, plan-mode guard, auto-generated-file guard, snapshot store, and output-meta.
- edge_cases_or_failure_modes: Stale anchors recovered through read snapshot cache, missing snapshot tags, streaming partial ops, block resolution failures, same-file multi-section stale results, notebook serialization, and no-op edit loops.
- validation_or_tests: `packages/coding-agent/test/core/hashline.test.ts` and `packages/hashline/test/landing-shift.test.ts` validate executor and core patch semantics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1646 `directory` `packages/coding-agent/test/modes/theme`
- cursor: `[_]`
- core_role: Theme-mode regression tests.
- algorithmic_behavior: Tests settings list theme dirty labels/values and shimmer text crest color handling with raw ANSI color injection.
- inputs_outputs_state: Inputs are initialized theme, selected/changed flags, fake time, raw ANSI color options, and settings initialization mock. Outputs are themed ANSI strings.
- gates_or_invariants: Modified settings must stay dirty-colored even when selected; shimmer must preserve visible text after ANSI styling.
- dependencies_and_callers: Validates TUI theme helpers used by settings selector and shimmer rendering.
- edge_cases_or_failure_modes: Settings uninitialized path for shimmer and raw 24-bit ANSI color.
- validation_or_tests: Directory contains `settings-list-theme.test.ts` and `shimmer.test.ts`.
- skip_candidate: `yes: test-only directory`

### OH_MY_HUMANIZE_MAIN-HZ-1676 `file` `packages/agent/src/compaction/errors.ts`
- cursor: `[_]`
- core_role: Shared compaction cancellation/error outcome definitions.
- algorithmic_behavior: Defines `CompactionCancelledError` that preserves a user-facing reason and a `CompactionOutcome` union of `ok`, `cancelled`, or `failed`.
- inputs_outputs_state: Inputs are optional cancellation reason strings. Outputs are typed errors/outcome strings used by compaction callers.
- gates_or_invariants: Cancellation is semantically distinct from failure so callers can avoid treating user aborts as compaction defects.
- dependencies_and_callers: Used by agent/coding-agent compaction paths and status handling.
- edge_cases_or_failure_modes: Missing reason falls back to a default message; downstream must catch by class not message.
- validation_or_tests: Covered indirectly by compaction tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1706 `file` `packages/ai/src/dialect/gemma.ts`
- cursor: `[_]`
- core_role: Gemma in-band tool/thinking dialect scanner and renderer.
- algorithmic_behavior: `GemmaInbandScanner` incrementally scans text for `<|tool_call>` and thought channel tags, buffers tool bodies until close delimiters, parses `call: name { ... }` args, emits text/thinking/toolCall events, and render helpers produce tool calls, tool results, thinking blocks, and transcripts (`packages/ai/src/dialect/gemma.ts:38-376`).
- inputs_outputs_state: Inputs are streamed model text chunks, tool call/result structures, messages, and render options. Outputs are in-band scan events and Gemma-formatted prompt/transcript strings.
- gates_or_invariants: Tool names must match identifier regex; string delimiters and nested braces are skipped/matched; thinking scanning is optional via scanner options; parsing falls back through JSON-ish scalar/list/object coercion.
- dependencies_and_callers: Registered as a `DialectDefinition` for owned in-band tool calling in pi-ai/agent loop.
- edge_cases_or_failure_modes: Partial open/close tags across chunks, nested braces/strings, numeric/boolean/null scalar parsing, malformed call body, and unresolved close delimiter.
- validation_or_tests: Covered by dialect tests such as `gemini-gemma-dialect.test.ts` and tool inventory/in-band tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1736 `file` `packages/ai/src/providers/google-auth.ts`
- cursor: `[_]`
- core_role: Google Application Default Credentials access-token resolver for Vertex/Gemini providers.
- algorithmic_behavior: Loads ADC credentials from env/user files, handles service account JWT signing/exchange, authorized-user refresh token exchange, impersonated service account flows, metadata server token fetch, token POSTs, caching with refresh skew, in-flight request deduplication, shared timeout, and cache reset (`packages/ai/src/providers/google-auth.ts:22-312`).
- inputs_outputs_state: Inputs are ADC files/env vars, credential JSON, private keys, fetch implementation, abort signal, and current time. Outputs are bearer access tokens and cached token entries.
- gates_or_invariants: Cached token must not be within refresh skew; concurrent calls share one in-flight promise; metadata fetch uses Google metadata header; token resolve has 30s shared timeout.
- dependencies_and_callers: Used by Google Vertex/Gemini provider adapters; depends on WebCrypto RSA signing, Bun file reads, fetch, and OAuth token endpoints.
- edge_cases_or_failure_modes: Malformed ADC JSON, invalid PEM, missing refresh tokens, metadata server unavailable, aborts/timeouts, impersonation source credentials, and expired cached token.
- validation_or_tests: `packages/ai/src/providers/__tests__/google-auth.test.ts` and Google OAuth/validation tests cover this path.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1766 `file` `packages/ai/src/registry/amazon-bedrock.ts`
- cursor: `[_]`
- core_role: Provider registry descriptor for Amazon Bedrock.
- algorithmic_behavior: Exports `amazonBedrockProvider` with provider id/display metadata and registry integration values.
- inputs_outputs_state: Inputs are provider registry loading. Outputs are provider descriptor used for model/API selection.
- gates_or_invariants: Descriptor must match expected provider id and Bedrock API integration.
- dependencies_and_callers: Consumed by `packages/ai/src/registry/register-builtins`/registry index.
- edge_cases_or_failure_modes: Misconfigured descriptor prevents Bedrock provider discovery.
- validation_or_tests: Provider registry tests cover built-in registration.
- skip_candidate: `yes: descriptor-only file; no algorithm beyond registration metadata`

### OH_MY_HUMANIZE_MAIN-HZ-1796 `file` `packages/ai/src/registry/moonshot.ts`
- cursor: `[_]`
- core_role: Provider registry/login descriptor for Moonshot.
- algorithmic_behavior: Creates an API-key login flow and exports `moonshotProvider` descriptor with Moonshot provider metadata/base settings.
- inputs_outputs_state: Inputs are API key login credentials and provider registry initialization. Outputs are login handler and provider descriptor.
- gates_or_invariants: API-key auth must map to correct provider id and header semantics.
- dependencies_and_callers: Consumed by registry built-ins and Kimi/Moonshot search/auth integrations.
- edge_cases_or_failure_modes: Wrong provider id/base URL would break Moonshot model auth.
- validation_or_tests: Login/provider registry tests cover API key provider descriptors.
- skip_candidate: `yes: descriptor/login wiring only`

### OH_MY_HUMANIZE_MAIN-HZ-1826 `file` `packages/ai/src/registry/xiaomi-token-plan-sgp.ts`
- cursor: `[_]`
- core_role: Provider registry descriptor for Xiaomi token plan Singapore endpoint.
- algorithmic_behavior: Exports `xiaomiTokenPlanSgpProvider` metadata for registry discovery.
- inputs_outputs_state: Inputs are registry loading. Outputs are provider descriptor for Xiaomi SGP token plan.
- gates_or_invariants: Provider id and region endpoint naming must remain stable for credential/model resolution.
- dependencies_and_callers: Used by AI provider registry and Xiaomi token plan login/selection code.
- edge_cases_or_failure_modes: Descriptor drift breaks region-specific provider lookup.
- validation_or_tests: Provider registry tests cover descriptor loading.
- skip_candidate: `yes: descriptor-only file`

### OH_MY_HUMANIZE_MAIN-HZ-1856 `file` `packages/ai/src/utils/request-debug.ts`
- cursor: `[_]`
- core_role: Request/response debug capture wrapper for provider HTTP calls.
- algorithmic_behavior: Checks `PI_REQ_DEBUG`, reserves a debug file, wraps fetch, snapshots method/url/headers/body, writes request payload, clones/logs response metadata/body, preserves response metadata, and supports one-shot debug output path (`packages/ai/src/utils/request-debug.ts:53-382`).
- inputs_outputs_state: Inputs are fetch input/init, request body types, content type, env flag, optional next debug path, and responses. Outputs are JSON/debug files and wrapped `Response` objects.
- gates_or_invariants: Already-wrapped fetch is not wrapped twice; request body snapshot handles JSON/text/base64/unavailable forms; file reservation avoids overwrite collisions; response body must remain readable to caller via clone/reconstructed response.
- dependencies_and_callers: Used by provider adapters when request debugging is enabled; depends on Bun file APIs, `TextEncoder/Decoder`, Fetch API, and logger-like debug session types.
- edge_cases_or_failure_modes: Non-UTF8 body base64 fallback, streaming/unavailable bodies, file exists races, malformed content type, and preserving status/statusText/headers.
- validation_or_tests: `packages/ai/test/request-debug.test.ts` covers debug capture behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1886 `file` `packages/catalog/src/identity/selection.ts`
- cursor: `[_]`
- core_role: Canonical model variant selection utility.
- algorithmic_behavior: Builds stable candidate order maps and resolves a canonical variant from candidates using preferences over source rank, exact id, and original order (`packages/catalog/src/identity/selection.ts:16-36`).
- inputs_outputs_state: Inputs are `Model<Api>[]` candidates and `CanonicalVariantPreferences`. Outputs are selected canonical variant/model identity.
- gates_or_invariants: Selection must be deterministic; source ranks prefer curated/generated sources consistently while preserving order tie-breaks.
- dependencies_and_callers: Used by catalog identity/canonicalization logic.
- edge_cases_or_failure_modes: Duplicate candidate ids, unknown source ranks, and preference conflicts.
- validation_or_tests: Catalog identity/model selection tests cover behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1916 `file` `packages/coding-agent/src/capability/extension.ts`
- cursor: `[_]`
- core_role: Capability definition for Gemini-style extensions.
- algorithmic_behavior: Defines extension manifest/loaded extension shapes and registers `extensionCapability` with id, display metadata, key extractor, and validation for missing name/path (`packages/coding-agent/src/capability/extension.ts:13-47`).
- inputs_outputs_state: Inputs are parsed extension manifests and source metadata. Outputs are validated extension capability items.
- gates_or_invariants: Extension must have a name and path; MCP servers in manifests omit runtime `name/_source` until expansion.
- dependencies_and_callers: Used by capability discovery/providers, extension loader, MCP/tool/context integration.
- edge_cases_or_failure_modes: Missing manifest fields and malformed extension path/name.
- validation_or_tests: Extension/plugin tests indirectly cover capability loading.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1946 `file` `packages/coding-agent/src/cli/gallery-screenshot.ts`
- cursor: `[_]`
- core_role: CLI helper that renders `omp gallery` ANSI output to PNG screenshots through VHS.
- algorithmic_behavior: Checks `vhs`, chunks gallery sections by row budget, builds a VHS theme from TUI theme colors, writes temporary ANSI/tape files, runs VHS, validates PNG existence, cleans temp artifacts, resolves multi-image output paths, and computes chunk boundaries (`packages/coding-agent/src/cli/gallery-screenshot.ts:58-279`).
- inputs_outputs_state: Inputs are `GallerySection[]`, width/font/fontSize/out path, current theme, and VHS executable. Outputs are PNG file paths and temporary ANSI/tape/GIF files.
- gates_or_invariants: VHS is required; tall images are split under max height; CRLF line endings preserve rows; multi-output names get stable zero-padded suffixes.
- dependencies_and_callers: Called by gallery CLI `--screenshot`; depends on VHS, Bun shell/write, fs/os/path, `$which`, and theme.
- edge_cases_or_failure_modes: Missing VHS, VHS render failure, too-tall section getting its own image, theme lacking RGB background, and shell-quoted paths with apostrophes.
- validation_or_tests: No direct assigned test; helper functions are deterministic and suitable for unit testing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1976 `file` `packages/coding-agent/src/commands/auth-broker.ts`
- cursor: `[_]`
- core_role: CLI command class for `omp auth-broker`.
- algorithmic_behavior: Declares positional args/flags/examples, parses action/source/options, maps provider/source ambiguity for login/logout/import, initializes theme, and delegates to `runAuthBrokerCommand` (`packages/coding-agent/src/commands/auth-broker.ts:13-99`).
- inputs_outputs_state: Inputs are CLI args/flags. Outputs are command execution side effects through auth-broker CLI and help text when no action is provided.
- gates_or_invariants: Action is optional only to show help; provider flag means import override for `import` but provider/source for login/logout.
- dependencies_and_callers: Used by command registry; depends on pi-utils CLI framework, `cli/auth-broker-cli`, and theme initialization.
- edge_cases_or_failure_modes: Missing action, dry-run migration/import, include-disabled/import OAuth flags, and remote login via SSH `--via`.
- validation_or_tests: Auth-broker tests under `packages/ai/test/auth-broker-*` and coding-agent command registration cover adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2006 `file` `packages/coding-agent/src/commit/cli.ts`
- cursor: `[_]`
- core_role: Argument parser/help renderer for `omp commit`.
- algorithmic_behavior: Recognizes `commit` command, parses flags/aliases (`-c`, `-m`), sets booleans for push/dry-run/no-changelog/legacy, captures context/model values, exits on unknown or missing-value flags, and prints help (`packages/coding-agent/src/commit/cli.ts:4-85`).
- inputs_outputs_state: Inputs are raw argv strings. Outputs are `CommitCommandArgs`, process stdout/stderr, and exit on parse errors.
- gates_or_invariants: Non-`commit` returns undefined; value flags require a following non-flag token; unknown flags fail fast.
- dependencies_and_callers: Used by commit command entrypoint; depends on chalk and commit types.
- edge_cases_or_failure_modes: `--help` ignored by parser for caller help handling; positional non-flag extras are ignored.
- validation_or_tests: Commit CLI behavior covered indirectly by command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2036 `file` `packages/coding-agent/src/debug/log-viewer.ts`
- cursor: `[_]`
- core_role: Interactive model/component for viewing, filtering, selecting, expanding, copying, and loading coding-agent logs.
- algorithmic_behavior: Splits log text, inserts current-session boundary warnings, tracks visible log rows, filter query, process filter, cursor, selection anchor, expanded rows, external older-log loading, and renders a TUI component with controls/copy payloads (`packages/coding-agent/src/debug/log-viewer.ts:58-888`).
- inputs_outputs_state: Inputs are raw log text, process start/pid, optional older-log provider, keyboard events, and terminal width/height. Outputs are viewer rows, selected raw lines, sanitized copy payload, rendered TUI rows, and exit callbacks.
- gates_or_invariants: Empty lines are dropped; boundary warning appears only when older and current logs are visible; filtering clamps cursor/selection; copy strips ANSI/control; loading older keeps cursor stable.
- dependencies_and_callers: Used by debug/log UI command; depends on TUI components, log formatting helpers, and terminal input.
- edge_cases_or_failure_modes: External older logs, filtered-out selection anchor, process pid missing, expanded long rows, and current-session boundary after filtering.
- validation_or_tests: `packages/coding-agent/test/debug/log-viewer.test.ts` covers row construction, filtering, selection, loading, and copy sanitation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2066 `file` `packages/coding-agent/src/discovery/vscode.ts`
- cursor: `[_]`
- core_role: Capability discovery provider for VS Code MCP configuration.
- algorithmic_behavior: Registers an MCP capability provider that reads project `.vscode/mcp.json`, parses nested `{ mcp: { servers } }`, expands env vars, normalizes command/args/env/url/headers/transport/timeout, attaches source metadata, and returns warnings for read/JSON/config failures (`packages/coding-agent/src/discovery/vscode.ts:22-105`).
- inputs_outputs_state: Inputs are `LoadContext`, project config path, JSON content, and environment variables. Outputs are `MCPServer[]` plus warnings.
- gates_or_invariants: Project-only; invalid JSON/read failure warns; invalid server config warns/skips; transport limited to `stdio`, `sse`, or `http`.
- dependencies_and_callers: Used by capability discovery before MCP manager startup; depends on capability registry, fs helper, env expansion, and MCP capability types.
- edge_cases_or_failure_modes: Missing config, no `mcp.servers`, non-object entries, invalid transport, env vars inside nested fields.
- validation_or_tests: MCP discovery tests and issue-851 style plugin config tests cover adjacent config loading.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2096 `file` `packages/coding-agent/src/extensibility/legacy-pi-coding-agent-shim.ts`
- cursor: `[_]`
- core_role: Compatibility shim for legacy plugins importing the coding-agent package root.
- algorithmic_behavior: Marks tool definitions, creates legacy tool sessions, wraps built-in `read/bash/edit/write` tools as legacy tool definitions, exposes frontmatter parsing/stripping, `defineTool`, `createCodingTools`, `SettingsManager`, `Type`, and re-exports canonical package surface (`packages/coding-agent/src/extensibility/legacy-pi-coding-agent-shim.ts:23-128`).
- inputs_outputs_state: Inputs are cwd, legacy tool definitions, frontmatter content, tool call params/signals/updates. Outputs are marked tool definitions, built-in tool execution results, parsed frontmatter, and settings instances.
- gates_or_invariants: Built-in tool factories must be synchronous and available; hidden marker properties are non-enumerable; legacy session uses isolated settings and no UI/session file.
- dependencies_and_callers: Used by compiled/bundled plugin compatibility path; depends on built-in tools, settings, frontmatter parser, extension tool types, and TypeBox shim.
- edge_cases_or_failure_modes: Missing built-in tool, async factory unexpectedly returned, compiled BunFS package root compatibility covered by tests, and plugin imports under legacy scopes.
- validation_or_tests: `legacy-pi-bunfs-root.test.ts` covers related compiled root computation; extension tests cover tool shim behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2126 `file` `packages/coding-agent/src/internal-urls/omp-protocol.ts`
- cursor: `[_]`
- core_role: Internal `omp://` protocol handler for bundled documentation.
- algorithmic_behavior: Lists embedded doc filenames for `omp://`, resolves host+path to doc path, normalizes/removes `docs/` prefix, blocks absolute/traversal paths, reads embedded doc body, and suggests nearby docs on miss (`packages/coding-agent/src/internal-urls/omp-protocol.ts:19-94`).
- inputs_outputs_state: Inputs are internal URL and embedded docs index. Outputs are Markdown `InternalResource` listings or doc contents.
- gates_or_invariants: Absolute paths and `..` traversal are forbidden; empty `docs` routes to listing; completions expose doc filenames.
- dependencies_and_callers: Used by internal URL router/read tool; depends on `docs-index.ts`.
- edge_cases_or_failure_modes: Missing/corrupt docs index, filename not found, backslash normalization, and host/path combination.
- validation_or_tests: Internal URL parser tests cover URL raw fields; docs-index behavior is validated by build process.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2156 `file` `packages/coding-agent/src/mcp/manager.ts`
- cursor: `[_]`
- core_role: MCP server lifecycle and tool/resource discovery manager.
- algorithmic_behavior: Tracks MCP server connections, startup timeouts, reconnect burst limits, tool/resource/prompt loading, subscription post-action resolution, tool sorting, initialization/discovery, and manager factory creation (`packages/coding-agent/src/mcp/manager.ts:53-1326`).
- inputs_outputs_state: Inputs are configured MCP servers, discover options, auth/session context, transport configs, and callbacks. Outputs are loaded tools/resources/prompts, connection status, load results, subscriptions, and registered agent tools.
- gates_or_invariants: Startup timeout is short (`250ms`); reconnect bursts are capped; promises are tracked; tools sorted by name; resource subscription post-actions distinguish changed vs unchanged behavior.
- dependencies_and_callers: Used by coding-agent MCP tool/resource integration and internal `mcp://` protocol; depends on MCP SDK clients/transports, capability discovery, settings, logger, and tool schemas.
- edge_cases_or_failure_modes: Server startup failure, reconnect storms, tool list failure, unavailable resources/prompts, auth/env expansion, transport differences, and stale subscriptions.
- validation_or_tests: MCP manager/config behavior is covered by tests such as issue-851 repro and tool-discovery/provider schema compatibility.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2186 `file` `packages/coding-agent/src/modes/internal-url-autocomplete.ts`
- cursor: `[_]`
- core_role: Autocomplete helper for internal URL tokens in the TUI editor.
- algorithmic_behavior: Extracts the current URL-like prefix before cursor, splits scheme/rest, fuzzy matches candidates, scores suggestions, filters to max 25, checks internal prefixes, and applies a completion by replacing the active token (`packages/coding-agent/src/modes/internal-url-autocomplete.ts:13-125`).
- inputs_outputs_state: Inputs are text before cursor, router completions, supported schemes, and selected completion. Outputs are context objects, suggestion arrays, boolean prefix checks, and replacement text/cursor positions.
- gates_or_invariants: URL token regex stops at whitespace/quotes/brackets; fuzzy matching is ordered; non-internal schemes are ignored; max suggestions fixed.
- dependencies_and_callers: Used by interactive editor autocomplete; depends on internal URL router completions.
- edge_cases_or_failure_modes: Partial scheme, one/two slash forms, punctuation boundaries, empty rest, and fuzzy ties.
- validation_or_tests: Internal URL parser/autocomplete behavior indirectly covered by marketplace parse tests and editor autocomplete tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2216 `file` `packages/coding-agent/src/session/blob-store.ts`
- cursor: `[_]`
- core_role: Content-addressed blob store for externalizing binary/image data from session JSONL.
- algorithmic_behavior: Hashes data with SHA-256, writes canonical extensionless blobs, optionally creates extension sidecar via hardlink/copy, parses `blob:sha256:` refs, externalizes/restores image data URLs and base64 images sync/async, maps image MIME types to extensions, and logs missing blob warnings (`packages/coding-agent/src/session/blob-store.ts:6-255`).
- inputs_outputs_state: Inputs are buffers, base64 strings, data URLs, MIME types, and blob dir. Outputs are blob files, display paths, blob refs, buffers/base64/data URLs, and warning logs.
- gates_or_invariants: Extension names are sanitized and capped; content hash is over raw data; missing blobs return null/ref rather than crashing; image data URLs are stored as UTF-8 full strings to preserve transport history.
- dependencies_and_callers: Used by session persistence/reload for provider image data and tool result images; depends on Bun SHA/write/file and fs hardlinks.
- edge_cases_or_failure_modes: Hardlink failure falls back to copy; existing sidecar ignored; unknown image subtype derives extension; missing blob on restore returns ref/invalid base64 placeholder.
- validation_or_tests: `signature-persistence.test.ts` covers externalizing/restoring provider and tool-result image data.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2246 `file` `packages/coding-agent/src/slash-commands/types.ts`
- cursor: `[_]`
- core_role: Shared type contracts for slash command metadata, parsing, runtime context, and handlers.
- algorithmic_behavior: Defines command/subcommand specs, parsed invocation shape, handler result union, TUI vs text/ACP runtime interfaces, workflow monitor hooks, reload/config notification hooks, and ACP result shape (`packages/coding-agent/src/slash-commands/types.ts:9-145`).
- inputs_outputs_state: Inputs are command strings and runtime services; outputs are consumed/prompts, UI/ACP side effects, workflow graph output, and plugin reload/config notifications.
- gates_or_invariants: `undefined`/void means consumed; `{ prompt }` passes new user prompt; `handleTui` supersedes `handle` when both exist; function type unions preserve TypeScript compatibility.
- dependencies_and_callers: Used by built-in slash command registry, ACP dispatcher, and TUI dispatcher.
- edge_cases_or_failure_modes: Commands with arguments when `allowArgs=false`, ACP-specific descriptions/input hints, and runtime differences between TUI and non-TUI modes.
- validation_or_tests: `slash-commands/switch.test.ts` and slash parser/helper tests cover specific command dispatch.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2276 `file` `packages/coding-agent/src/task/types.ts`
- cursor: `[_]`
- core_role: Type/schema/event contract for task/subagent spawning and progress reporting.
- algorithmic_behavior: Defines environment-capped output limits, event bus channels/payloads, dynamic task tool schemas for flat/batch/isolation modes, label sanitization, spawn-depth gate, agent definitions, progress/result shapes, review data, and task tool details (`packages/coding-agent/src/task/types.ts:23-407`).
- inputs_outputs_state: Inputs are task params, agent definitions, settings/env caps, event payloads, progress updates, model overrides, and usage. Outputs are validated task params, progress/result objects, review summaries, and rendered labels.
- gates_or_invariants: Role input length capped; `oneLineLabel` collapses control/format/whitespace and truncates by code point; spawn recursion obeys max depth unless negative; task schema changes with isolation/batch flags.
- dependencies_and_callers: Used by task tool, workflow nodes, subagent HUD, event bus, and review extraction.
- edge_cases_or_failure_modes: Control/ANSI injection in labels, stale transcripts with flat params under batch mode, disabled isolation schema, detached vs sync subagents, retry state/failure surfacing.
- validation_or_tests: Task/tool-discovery/provider-schema compatibility tests validate schema exposure and progress contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2306 `file` `packages/coding-agent/src/tools/eval.ts`
- cursor: `[_]`
- core_role: Built-in `eval` tool implementation for persistent Python/JavaScript execution.
- algorithmic_behavior: Defines cell schema, renders model-facing description, resolves enabled backends, executes cells sequentially with per-cell idle timeout, pauses timeout during host bridge calls, streams output through `OutputSink`, sends incremental updates, handles reset/state persistence, captures JSON/image/status/markdown display outputs, resizes images, writes artifacts, and returns structured `EvalToolDetails` (`packages/coding-agent/src/tools/eval.ts:30-600`).
- inputs_outputs_state: Inputs are cell list, language/code/title/timeout/reset, tool session, abort signal, backend availability, output artifact allocator, and model image constraints. Outputs are text/image content, cell details, JSON outputs, status events, truncation metadata, artifacts, and errors.
- gates_or_invariants: Requires session unless proxy executor supplied; Python/JS can be disabled by settings/env; per-cell timeout clamps 1-3600 seconds; `assertEvalExecutionAllowed` gates starts; tool concurrency is exclusive; session tracks eval execution for cleanup.
- dependencies_and_callers: Used by coding-agent built-in tools and eval JS bridge; depends on eval backends, idle-timeout, output-meta/result, image resize/loading, and tool timeout helpers.
- edge_cases_or_failure_modes: Abort before/during execution, cancelled backend, nonzero exit in multi-cell stateful session, display image WebP exclusion, output truncation/artifact dumping, and backend unavailability.
- validation_or_tests: `eval-timeout.test.ts`, `prelude-agent.test.ts`, and Python cleanup tests cover timeout, bridge helper, and lifecycle behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2336 `file` `packages/coding-agent/src/tools/output-meta.ts`
- cursor: `[_]`
- core_role: Structured output metadata builder/formatter and tool wrapper for truncation/source/diagnostic notices.
- algorithmic_behavior: `OutputMetaBuilder` records truncation from `TruncationResult`, `OutputSummary`, or raw text; records source and limits/diagnostics; formatters produce full-output references, truncation notices, styled warnings, strip notices, spill large results to artifacts, and wrap tool execution to append notices (`packages/coding-agent/src/tools/output-meta.ts:26-748`).
- inputs_outputs_state: Inputs are tool results, output summaries, truncation direction/limits, settings, theme, artifact allocator, and diagnostics. Outputs are `OutputMeta`, appended notice text, artifact refs, styled warnings, and modified tool results.
- gates_or_invariants: No-op when not truncated or limits <=0; middle/head/tail ranges must be reconstructed accurately; large result spilling respects settings; wrappers avoid double wrapping via symbol.
- dependencies_and_callers: Used by read/grep/find/eval/edit/bash-style tools and renderers; depends on streaming-output truncators, settings defaults, logger, LSP diagnostic formatting, and render utilities.
- edge_cases_or_failure_modes: Middle elision ranges, head next offset, image content mixed with text, artifact spill failures, notice stripping, and malformed tool outputs.
- validation_or_tests: Provider schema compatibility and tool output tests cover exposed metadata paths indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2366 `file` `packages/coding-agent/src/tts/vocalizer.ts`
- cursor: `[_]`
- core_role: Streaming assistant speech vocalization controller.
- algorithmic_behavior: Lazily opens TTS stream on first text delta, pushes deltas, flushes trailing partials, speaks complete text, clears/aborts current synthesis and playback, ducks/unducks gain during user speech, serializes playback sessions through a promise chain, and swallows/logs synthesis/playback errors (`packages/coding-agent/src/tts/vocalizer.ts:39-162`).
- inputs_outputs_state: Inputs are assistant text deltas, speech settings, voice/model settings, user ducking events, and TTS chunks. Outputs are PCM writes to streaming audio player and playback lifecycle side effects.
- gates_or_invariants: No-op when speech disabled or text empty; sessions never overlap; clear stops audio immediately; duck state applies to current and newly opened players.
- dependencies_and_callers: Shared singleton used by event controller and ask/yield speech paths; depends on TTS client, streaming player, settings, and logger.
- edge_cases_or_failure_modes: Abort mid-stream, synthesis errors, player errors, user interruption, and sequential utterance ordering.
- validation_or_tests: No direct assigned test; behavior is inspectable through TTS/session tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2396 `file` `packages/coding-agent/src/utils/mupdf-wasm-embed.ts`
- cursor: `[_]`
- core_role: Autogenerated MuPDF WASM embed loader stub.
- algorithmic_behavior: Provides `loadEmbeddedMupdfWasm()` returning embedded bytes when generated by `scripts/embed-mupdf-wasm.ts`.
- inputs_outputs_state: Inputs are build-time embedded asset state. Output is optional `Uint8Array` of WASM bytes.
- gates_or_invariants: Header states autogenerated and not hand-edited; absence of embed returns undefined so callers can fallback.
- dependencies_and_callers: Used by PDF conversion/rendering paths needing MuPDF WASM.
- edge_cases_or_failure_modes: Missing embed in environments that expect bundled PDF support.
- validation_or_tests: PDF converter tests/build embedding process validate this indirectly.
- skip_candidate: `yes: generated asset stub; not hand-written core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2426 `file` `packages/coding-agent/src/workflow/monitor-history.ts`
- cursor: `[_]`
- core_role: Workflow graph monitor snapshot persistence helper.
- algorithmic_behavior: Builds workflow monitor health summary, sanitizes filename segments, writes monitor snapshots with timestamp/display mode/health/view data, and returns snapshot metadata (`packages/coding-agent/src/workflow/monitor-history.ts:29-70`).
- inputs_outputs_state: Inputs are workflow graph view, display mode, output directory/session ids, and time. Outputs are snapshot files and health objects.
- gates_or_invariants: Filename segments are sanitized to filesystem-safe forms; health derives counts/statuses from graph view.
- dependencies_and_callers: Used by workflow monitor/debug/history surfaces.
- edge_cases_or_failure_modes: Unsafe session/workflow ids, missing output dir, and empty workflow graphs.
- validation_or_tests: Workflow model-resolution tests validate adjacent workflow behavior; no direct monitor-history test inspected.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2456 `file` `packages/coding-agent/test/core/hashline.test.ts`
- cursor: `[_]`
- core_role: Regression suite for coding-agent hashline executor integration.
- algorithmic_behavior: Tests creation rejection, duplicate pure insert literal application, no-op diagnostics/escalation, multi-file preflight before writes, duplicate canonical target rejection, same-file multi-section original snapshot behavior, params schema shape/alias tolerance, stale-anchor recovery via read snapshot cache, post-edit snapshot capture, and replay rejection after in-session line rewrite.
- inputs_outputs_state: Inputs are temp files, hashline patch strings, file read cache/snapshot tags, tool sessions, settings, and executor options. Outputs are file contents, tool results, diffs, diagnostics, and thrown errors.
- gates_or_invariants: Hashline edit only updates existing files; multi-section write must be atomic after preflight; model-facing schema exposes only `input`; stale anchor recovery is allowed only when snapshot cache covers the anchor and line was not rewritten by prior edit.
- dependencies_and_callers: Validates `packages/coding-agent/src/edit/hashline/*`.
- edge_cases_or_failure_modes: Provider `_input` alias, extra provider fields, duplicate canonical paths, out-of-band file modification, missing cache coverage, and replay against rewritten line.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2486 `file` `packages/coding-agent/test/debug/terminal-info.test.ts`
- cursor: `[_]`
- core_role: Tests for terminal state collection and formatting.
- algorithmic_behavior: Asserts formatted terminal state surfaces detected protocols, geometry/cell size, scrollback strategy, multiplexer/env values, confirmed OSC-99 marker, and maps live protocol info to human-readable names without raw escapes.
- inputs_outputs_state: Inputs are sample terminal capability objects and live terminal constants. Outputs are formatted info strings and collected state fields.
- gates_or_invariants: Terminal info must never contain raw escape sequences for protocol names; absent env fields show `(unset)`.
- dependencies_and_callers: Validates debug terminal-info command and terminal capability detection.
- edge_cases_or_failure_modes: No multiplexer, unsupported screen-to-history, unconfirmed OSC-99, and live geometry passthrough.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2516 `file` `packages/coding-agent/test/extensibility/legacy-pi-bunfs-root.test.ts`
- cursor: `[_]`
- core_role: Regression tests for legacy plugin BunFS package-root computation.
- algorithmic_behavior: Asserts compiled BunFS root appends `packages` on Windows/POSIX, module-specific compiled import dirs are handled, production calls use host path implementation, npm prebuilt dist roots resolve to package root, and source package roots work when `PI_BUNDLED` is used outside dist.
- inputs_outputs_state: Inputs are Windows/POSIX `import.meta.dir`-like paths and path modules. Outputs are computed package root strings.
- gates_or_invariants: Compiled and bundled roots must resolve legacy shim files correctly across OS path semantics.
- dependencies_and_callers: Validates legacy extension shim/bundled compatibility helpers.
- edge_cases_or_failure_modes: Windows `B:\~BUN\root`, POSIX `/$bunfs/root`, dist vs source layouts, and Bun compiled semantics changes.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2546 `file` `packages/coding-agent/test/marketplace/parse-internal-url.test.ts`
- cursor: `[_]`
- core_role: Parser contract tests for internal URL raw host/path preservation.
- algorithmic_behavior: Tests standard `skill/agent/memory/local` URLs, paths, query/href, namespaced hosts with literal colons, percent-encoded host colons, empty hosts, ports, hyphens/dots, uppercase schemes, fragments, and invalid inputs.
- inputs_outputs_state: Inputs are URL strings. Outputs are `InternalUrl` fields (`rawHost`, `rawPathname`, `protocol`, `searchParams`, `href`) or thrown errors.
- gates_or_invariants: Raw host must not include query/path/fragment; colon namespacing must survive fallback parsing; invalid empty/non-URL inputs throw.
- dependencies_and_callers: Validates `packages/coding-agent/src/internal-urls/parse.ts`, used by marketplace/skill/internal URL flows.
- edge_cases_or_failure_modes: Multiple colons, mixed encoded/literal colons, empty host with path, uppercase scheme, valid port parsing, and fallback `searchParams` limitations.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2576 `file` `packages/coding-agent/test/session-manager/signature-persistence.test.ts`
- cursor: `[_]`
- core_role: Tests for session persistence of provider signatures, native history payloads, and externalized image blobs.
- algorithmic_behavior: Asserts oversized signatures are cleared not truncated, provider image data URLs externalize and restore across reload, tool result image blocks externalize/restore, and assistant replay metadata rehydrates in memory without rewriting session file.
- inputs_outputs_state: Inputs are session messages with signatures/images/native metadata and blob store paths. Outputs are persisted JSONL entries, blob files/refs, reloaded session messages, and file rewrite checks.
- gates_or_invariants: Signatures cannot be partially truncated; image data must be externalized losslessly; rehydration should not mutate persisted session file.
- dependencies_and_callers: Validates session manager and `BlobStore` behavior.
- edge_cases_or_failure_modes: Oversized signature payloads, provider vs tool result image formats, reload preservation, and in-memory-only replay metadata.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2606 `file` `packages/coding-agent/test/slash-commands/switch.test.ts`
- cursor: `[_]`
- core_role: Tests for `/model` and `/switch` slash command UI routing.
- algorithmic_behavior: Creates fake runtime and asserts `/model` opens role/thinking model setup picker while `/switch` opens temporary model selector mirroring `alt+p`.
- inputs_outputs_state: Inputs are slash command invocations and fake runtime callbacks. Outputs are selector open calls.
- gates_or_invariants: `/model` and `/switch` are distinct surfaces despite related model selection semantics.
- dependencies_and_callers: Validates slash command registry/handlers.
- edge_cases_or_failure_modes: Command alias/routing mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2636 `file` `packages/coding-agent/test/tool-discovery/tool-index.test.ts`
- cursor: `[_]`
- core_role: Tests for discoverable tool indexing, summaries, source grouping, and BM25 search.
- algorithmic_behavior: Builds fake agent/MCP tools and asserts MCP name detection, discoverable tool conversion, summary fallback/overrides, schema-key extraction from JSON/Zod schemas, collection/filtering by source, server summaries, tool selection by server, BM25 index build/search/limits/empty query behavior.
- inputs_outputs_state: Inputs are tool definitions, parameters, summary maps, source filters, server names, and search queries. Outputs are discoverable tool docs, summaries, names, and ranked matches.
- gates_or_invariants: Empty query throws; empty index returns empty; `mcp__` prefix infers MCP source; summary falls back to first 200 description chars.
- dependencies_and_callers: Validates tool discovery/index used by deferred tool search.
- edge_cases_or_failure_modes: Tools without server names, source override, Zod wire conversion, search miss, and limit enforcement.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2666 `file` `packages/coding-agent/test/tools/eval-timeout.test.ts`
- cursor: `[_]`
- core_role: Timeout regression test for eval tool compute cells.
- algorithmic_behavior: Constructs a test session and asserts a compute-only eval cell is bounded by plain wall-clock timeout without agent/completion bridge pauses.
- inputs_outputs_state: Inputs are eval cell timeout and JS/Python compute code. Outputs are timed-out tool result/error timing.
- gates_or_invariants: Compute work counts against timeout; bridge pause semantics must not accidentally suspend ordinary compute budget.
- dependencies_and_callers: Validates `EvalTool`, `IdleTimeout`, and backend execution timeout integration.
- edge_cases_or_failure_modes: Long-running compute without agent/completion calls.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2696 `file` `packages/coding-agent/test/tools/provider-schema-compatibility.test.ts`
- cursor: `[_]`
- core_role: Built-in tool schema compatibility tests across providers.
- algorithmic_behavior: Collects built-in/hidden tool schemas from a test session, adapts them through provider enforcement, formats issues, and asserts task/todo and all built-in schemas remain strict-compatible for OpenAI-style providers.
- inputs_outputs_state: Inputs are tool definitions and schema adapters. Outputs are compatibility issue arrays and failures with formatted diagnostics.
- gates_or_invariants: Built-in tool schemas must remain valid after provider-specific strict enforcement.
- dependencies_and_callers: Validates coding-agent tools plus pi-ai schema compatibility utilities.
- edge_cases_or_failure_modes: Hidden tools, task/todo strictness, and provider enforcement rewriting.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2726 `file` `packages/coding-agent/test/tools/web-search-gemini.test.ts`
- cursor: `[_]`
- core_role: Tests for Gemini web-search provider tool serialization.
- algorithmic_behavior: Uses SSE response fixture and captured request to assert default `googleSearch` tool is sent when no passthrough tools, passthrough `googleSearch` payload is preserved, and `codeExecution`/`urlContext` tools are included when provided.
- inputs_outputs_state: Inputs are search params/tools payloads and mocked Gemini SSE. Outputs are captured Gemini request JSON and search result.
- gates_or_invariants: Gemini search grounding tool serialization must preserve caller-provided tool payloads while providing sane default.
- dependencies_and_callers: Validates Gemini web search adapter documented in `docs/tools/web_search.md`.
- edge_cases_or_failure_modes: Multiple Gemini tool payload types and default-vs-passthrough behavior.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2756 `file` `packages/coding-agent/test/workflow/model-resolution.test.ts`
- cursor: `[_]`
- core_role: Tests for workflow node model/role resolution policy.
- algorithmic_behavior: Builds workflow specs and model fixtures; asserts workflow roles resolve through existing model role resolver with audit metadata, explicit node selectors override agent frontmatter, candidate selectors fall through, review nodes fail closed when model unavailable, parent active model fallback obeys policy, portable role defaults use parent when allowed, and workflow defaults precede agent frontmatter.
- inputs_outputs_state: Inputs are workflow source strings, available models, parent active model, node selectors, agent frontmatter, and fallback policy. Outputs are resolved model ids/providers/audit metadata or failures.
- gates_or_invariants: Review nodes fail closed without available requested model; explicit selectors take precedence; fallback to parent only when policy allows.
- dependencies_and_callers: Validates workflow runtime model selection and registry resolver integration.
- edge_cases_or_failure_modes: Candidate selector fallthrough, absent workflow model selection, portable node role defaults, and unavailable review models.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2786 `file` `packages/collab-web/src/tool-render/util.ts`
- cursor: `[_]`
- core_role: Shared utility functions for collab-web tool renderers.
- algorithmic_behavior: Provides record/string/number guards, display/truncate/whitespace/tab/ANSI/path normalization, language detection by extension/basename, result text/images/details extraction, args digest, and optional highlight.js accessor (`packages/collab-web/src/tool-render/util.ts:7-167`).
- inputs_outputs_state: Inputs are unknown tool args/results/details, paths, strings, and highlight global. Outputs are safe display strings, language ids, image arrays, details records, and digests.
- gates_or_invariants: ANSI is stripped for display helpers; home path shortens; result blocks are type-checked before extraction.
- dependencies_and_callers: Used by collab-web tool render components, including GitHub renderer.
- edge_cases_or_failure_modes: Unknown result shapes, paths without extensions, Dockerfile special-case, long args digests, and missing highlight.js.
- validation_or_tests: Tool renderer tests not assigned; GitHub renderer uses these utilities.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2816 `file` `packages/mnemopi/src/core/token-counter.ts`
- cursor: `[_]`
- core_role: Lightweight token and cost estimator for Mnemopi.
- algorithmic_behavior: Estimates token count from text length and estimates cost from per-model rate table with default fallback (`packages/mnemopi/src/core/token-counter.ts:1-21`).
- inputs_outputs_state: Inputs are text, token count, and model id. Outputs are estimated token integer and cost estimate object.
- gates_or_invariants: Unknown models use default rate; empty/short text still maps through estimator.
- dependencies_and_callers: Used by Mnemopi memory/cost diagnostics or budgeting.
- edge_cases_or_failure_modes: Approximation only; non-English/token-heavy text may diverge from true tokenizer.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2846 `file` `packages/tui/src/components/editor.ts`
- cursor: `[_]`
- core_role: Core multi-line TUI editor component with wrapping, history, autocomplete, selection, and key handling.
- algorithmic_behavior: Sanitizes loaded text, segments/wraps lines with width-aware chunks, maps offsets to visual columns, maintains editor state/history/undo stack, renders autocomplete/slash command select lists, handles cursor movement, text insertion/deletion, scrolling, focus, top border, history persistence, and selection/clipboard semantics (`packages/tui/src/components/editor.ts:33-3024`).
- inputs_outputs_state: Inputs are keyboard events, loaded text, dimensions, theme/border options, autocomplete providers, history storage, and callbacks. Outputs are rendered rows, cursor positions, submitted text, history updates, and component invalidations.
- gates_or_invariants: Undo stack capped at 100; loaded text sanitized; wrapping must respect grapheme/visible width; visual-column mapping must handle wide chars/tabs; fixed select-list layouts prevent unstable UI.
- dependencies_and_callers: Used by coding-agent interactive mode; depends on TUI primitives, text width/segmenter utilities, select lists, and history storage.
- edge_cases_or_failure_modes: Wide Unicode, ANSI/control sanitization, wrapped line cursor mapping, multiline paste, autocomplete overlays, history navigation, page scroll, and top-border updates from settings.
- validation_or_tests: TUI render/visible-width tests and selector side-effect tests validate adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2876 `file` `python/robomp/web/src/format.ts`
- cursor: `[_]`
- core_role: Frontend formatting helpers for RoboMP web UI.
- algorithmic_behavior: Formats durations, relative ages, shortened text, issue keys, issue/PR URLs, delivery ids, and timestamps.
- inputs_outputs_state: Inputs are seconds, ISO timestamps, unknown text values, repo/issue/PR ids, and delivery ids. Outputs are display strings and parsed `IssueRef`.
- gates_or_invariants: Missing values display em dash; long text is capped; issue key splitting handles null/undefined.
- dependencies_and_callers: Used by RoboMP web frontend components.
- edge_cases_or_failure_modes: Invalid/missing timestamps, short delivery ids, malformed issue keys.
- validation_or_tests: No direct assigned frontend tests.
- skip_candidate: `yes: UI formatting helper; low algorithmic core weight`

### OH_MY_HUMANIZE_MAIN-HZ-2906 `file` `crates/pi-shell/src/minimizer/filters/generic.rs`
- cursor: `[_]`
- core_role: Generic minimizer filter in the pi-shell crate.
- algorithmic_behavior: Implements a simple filter predicate/adapter for shell output minimization; small file with static/generic filtering logic.
- inputs_outputs_state: Inputs are minimizer text/events. Outputs are filtered/minimized data decisions.
- gates_or_invariants: Generic filter should be conservative and not remove required semantic output.
- dependencies_and_callers: Used by pi-shell minimizer pipeline.
- edge_cases_or_failure_modes: Over-filtering generic lines could hide useful command output.
- validation_or_tests: Not directly covered in assigned tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2936 `file` `packages/ai/src/registry/oauth/kimi.ts`
- cursor: `[_]`
- core_role: Kimi OAuth device-flow login and refresh implementation.
- algorithmic_behavior: Resolves OAuth host, builds/sanitizes device metadata headers, requests device authorization, polls token endpoint with interval/TTL and error handling, parses token payload to OAuth credentials, and refreshes tokens with skew (`packages/ai/src/registry/oauth/kimi.ts:14-237`).
- inputs_outputs_state: Inputs are OAuth controller callbacks, device id file/metadata, host env, fetch responses, refresh token, abort signal, and timer waits. Outputs are `OAuthCredentials`, user verification URLs/codes, and stored device id state.
- gates_or_invariants: Polling is bounded by device flow TTL; pending authorization waits by server/default interval; refresh requires refresh token; expiry skew avoids near-expired credentials.
- dependencies_and_callers: Used by provider registry OAuth login for Kimi/Moonshot-compatible accounts; depends on scheduler wait, os/device metadata, and auth storage callbacks.
- edge_cases_or_failure_modes: Authorization pending, slow_down-like waits, expired device code, malformed token payload, missing refresh token, and unsafe header values.
- validation_or_tests: OAuth/login tests cover similar providers; no assigned Kimi OAuth-specific test observed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2966 `file` `packages/coding-agent/src/autoresearch/tools/log-experiment.ts`
- cursor: `[_]`
- core_role: Autoresearch tool for logging experiment run results and managing keep/discard side effects.
- algorithmic_behavior: Opens active autoresearch storage, finds pending run, flags suspect prior runs, detects modified paths, computes scope deviations, optionally commits kept changes on autoresearch branch, reverts failed/discarded changes, merges parsed/overridden metrics and ASI, marks run logged, recomputes confidence/state, updates runtime/dashboard, disables tools at max experiments, and renders text/summary (`packages/coding-agent/src/autoresearch/tools/log-experiment.ts:55-521`).
- inputs_outputs_state: Inputs are metric/status/description/metrics/ASI/commit/justification/flag_runs, cwd/git state, storage session, runtime/dashboard, and pending run metadata. Outputs are stored run records, commits or reverts, dashboard updates, tool result details, warnings, and updated runtime state.
- gates_or_invariants: Requires active session and pending run; keep with dirty files auto-commits only on dedicated autoresearch branch; discard/crash/checks_failed revert only current iteration; scope deviations require justification warning; max experiments disables autoresearch tools.
- dependencies_and_callers: Used by autoresearch extension/tool runtime; depends on autoresearch storage/state/helpers/git, dashboard, and coding-agent custom tool interface.
- edge_cases_or_failure_modes: No active session, no pending run, git add/commit/reset/clean failure, off-branch dirty-path filtering, parsed metric mismatch, unjustified scope deviations, and flagged run session mismatch.
- validation_or_tests: No direct assigned test; algorithm can be tested with temp git repos and storage fixtures.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2996 `file` `packages/coding-agent/src/commit/changelog/generate.ts`
- cursor: `[_]`
- core_role: Agentic changelog entry generator.
- algorithmic_behavior: Renders static prompt templates with changelog/diff/stat context, calls `completeSimple` with a changelog tool schema, parses either tool call or JSON text payload, validates tool args, deduplicates/normalizes entries by category, and returns `ChangelogGenerationResult` (`packages/coding-agent/src/commit/changelog/generate.ts:14-101`).
- inputs_outputs_state: Inputs are model, API key, thinking level, changelog path/type, existing entries, git stat, diff, and prompt templates. Outputs are categorized changelog entries.
- gates_or_invariants: Prompts are static `.md` imports; entries are trimmed, trailing period removed, empty/duplicate case-insensitive entries dropped.
- dependencies_and_callers: Used by `omp commit` agentic changelog pipeline; depends on pi-ai completion/tool validation and commit prompt templates.
- edge_cases_or_failure_modes: Model returns text JSON instead of tool call; malformed JSON/tool args; duplicate categories/entries.
- validation_or_tests: Commit/changelog tests not assigned; parse/dedupe helpers are deterministic.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3026 `file` `packages/coding-agent/src/eval/__tests__/prelude-agent.test.ts`
- cursor: `[_]`
- core_role: Tests for JavaScript eval prelude `agent()` helper return-handle behavior.
- algorithmic_behavior: Loads eval prelude with fake `callTool`, invokes `agent()` with/without `returnHandle`, and asserts return-handle returns DAG node carrying `agent://` handle, default returns bare text, schema+returnHandle carries parsed data, and missing bridge details falls back to null handle.
- inputs_outputs_state: Inputs are prompts/options and mocked tool responses. Outputs are helper return values.
- gates_or_invariants: Backward-compatible default must remain bare text; `returnHandle` must surface agent output handle for DAG/eval composition.
- dependencies_and_callers: Validates eval JS prelude and task/agent bridge integration.
- edge_cases_or_failure_modes: Schema parsing combined with handle and bridge omitting details.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-3056 `file` `packages/coding-agent/src/extensibility/extensions/index.ts`
- cursor: `[_]`
- core_role: Barrel/export surface for extension APIs.
- algorithmic_behavior: Re-exports extension slash-command info/location/source types from `../slash-commands`.
- inputs_outputs_state: Inputs/outputs are TypeScript export surface only.
- gates_or_invariants: Maintains compatibility for extension imports.
- dependencies_and_callers: Used by extension/plugin authors.
- edge_cases_or_failure_modes: Removing/repointing export breaks extension type imports.
- validation_or_tests: Extension compilation/import tests cover this indirectly.
- skip_candidate: `yes: type barrel only`

### OH_MY_HUMANIZE_MAIN-HZ-3086 `file` `packages/coding-agent/src/markit/converters/pptx.ts`
- cursor: `[_]`
- core_role: PPTX-to-Markdown converter for Markit/document ingestion.
- algorithmic_behavior: Opens PPTX zip, parses presentation/relationship/slide/notes XML, orders slides, extracts shapes/text/tables/pictures, writes/exposes images, resolves notes, and emits Markdown with slide sections (`packages/coding-agent/src/markit/converters/pptx.ts:99-322`).
- inputs_outputs_state: Inputs are `.pptx` files/mime types, zip entries, XML documents, and output asset context. Outputs are Markdown text plus extracted image assets.
- gates_or_invariants: Handles only `.pptx`/PowerPoint MIME types; slide ordering follows presentation relationships; missing optional XML parts should not abort whole conversion.
- dependencies_and_callers: Used by Markit conversion pipeline; depends on zip/XML parsing helpers and converter interface.
- edge_cases_or_failure_modes: Slides without notes, missing relationships, tables with nested text, images with unknown extensions, and malformed Office XML.
- validation_or_tests: Markit converter tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3116 `file` `packages/coding-agent/src/modes/components/error-banner.ts`
- cursor: `[_]`
- core_role: TUI component for compact error banner rendering.
- algorithmic_behavior: Renders error text in a container with max 3 banner lines and theme styling (`packages/coding-agent/src/modes/components/error-banner.ts:7-16`).
- inputs_outputs_state: Inputs are error/message text and theme/container layout. Outputs are rendered TUI rows.
- gates_or_invariants: Banner line count is capped to prevent layout takeover.
- dependencies_and_callers: Used by interactive mode components/settings selectors.
- edge_cases_or_failure_modes: Long multi-line errors and narrow widths.
- validation_or_tests: UI component tests indirectly cover error rendering.
- skip_candidate: `yes: small UI rendering component; low algorithmic core weight`

### OH_MY_HUMANIZE_MAIN-HZ-3146 `file` `packages/coding-agent/src/modes/components/settings-selector.ts`
- cursor: `[_]`
- core_role: Interactive settings selector UI component.
- algorithmic_behavior: Implements text/select submenus, settings tabs/sidebar, status-line preview settings, callbacks, list rendering, editing/toggling values, dirty/default indication, and keyboard navigation (`packages/coding-agent/src/modes/components/settings-selector.ts:51-300+`).
- inputs_outputs_state: Inputs are settings runtime context, settings metadata, callbacks, key events, and theme. Outputs are settings mutations, reload/notify callbacks, rendered lists/previews, and submenu state.
- gates_or_invariants: Empty text input clears setting; modified values render dirty; sidebar width/tabs fixed; callbacks must fire for runtime side effects.
- dependencies_and_callers: Used by interactive settings UI; depends on settings schema/theme/list/select components.
- edge_cases_or_failure_modes: Invalid text input, clearing values, selected dirty value coloring, live preview updates, and tight-mode layout changes.
- validation_or_tests: `selector-settings-side-effects.test.ts` and theme settings-list tests validate side effects and dirty styling.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3176 `file` `packages/coding-agent/src/modes/controllers/ssh-command-controller.ts`
- cursor: `[_]`
- core_role: Controller for SSH-related interactive commands.
- algorithmic_behavior: Parses command text into parts, coordinates SSH command handling, and updates interactive context/session status based on command execution (`packages/coding-agent/src/modes/controllers/ssh-command-controller.ts:21-28+`).
- inputs_outputs_state: Inputs are raw command text and interactive context. Outputs are command actions/status/errors.
- gates_or_invariants: Command text is trimmed/split; unknown/malformed args should be surfaced rather than executed unsafely.
- dependencies_and_callers: Used by interactive mode command controller stack.
- edge_cases_or_failure_modes: Empty command, whitespace-only args, invalid SSH targets, and async command failures.
- validation_or_tests: Controller-specific tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3206 `file` `packages/coding-agent/src/slash-commands/helpers/parse.ts`
- cursor: `[_]`
- core_role: Shared slash-command parsing and helper utilities.
- algorithmic_behavior: Parses leading `/` commands using earliest whitespace or colon separator, returns consumed/usage results, parses subcommand verb/rest, normalizes error messages, and parses optional named scope args with user/project scope (`packages/coding-agent/src/slash-commands/helpers/parse.ts:16-68`).
- inputs_outputs_state: Inputs are command text/rest strings and runtime output callback. Outputs are parsed command/subcommand/scope objects or slash command results.
- gates_or_invariants: Non-slash/empty body returns null; invalid scope returns structured error; usage writes output and consumes command.
- dependencies_and_callers: Used by built-in slash command implementations.
- edge_cases_or_failure_modes: `/foo:bar`, multiple whitespace, missing name, invalid scope token, and thrown non-Error values.
- validation_or_tests: Slash command tests cover routing; parse helper behavior suitable for focused tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3236 `file` `packages/coding-agent/src/web/scrapers/crossref.ts`
- cursor: `[_]`
- core_role: Special web scraper for DOI/Crossref metadata.
- algorithmic_behavior: Extracts DOI from doi.org paths, fetches Crossref metadata, formats authors/date/abstract, converts abstract HTML to Markdown, and returns a special handler result (`packages/coding-agent/src/web/scrapers/crossref.ts:35-76`).
- inputs_outputs_state: Inputs are DOI URLs and fetch context. Outputs are Markdown metadata content or null to let generic scraping continue.
- gates_or_invariants: Only DOI hosts are handled; invalid/missing DOI returns null; abstract formatting is optional.
- dependencies_and_callers: Used by web scraper special-handler pipeline; depends on Crossref API and HTML-to-Markdown conversion.
- edge_cases_or_failure_modes: Encoded DOI path, missing author/date/abstract, Crossref failure, and abstract HTML cleanup.
- validation_or_tests: Web scraper tests not assigned for Crossref.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3266 `file` `packages/coding-agent/src/web/scrapers/ollama.ts`
- cursor: `[_]`
- core_role: Special web scraper for Ollama model pages.
- algorithmic_behavior: Validates Ollama hosts, parses model refs/tags, extracts meta description/parameter sizes/tags from HTML, fetches tags API, sorts/formats tags, collects parameter sizes, and returns Markdown model summary (`packages/coding-agent/src/web/scrapers/ollama.ts:28-159`).
- inputs_outputs_state: Inputs are Ollama URLs, HTML content, tags API responses, and model path parts. Outputs are model summary Markdown with tags/sizes/details.
- gates_or_invariants: Reserved root paths are excluded; only valid Ollama hostnames handled; tag counts are capped/formatted.
- dependencies_and_callers: Used by web scraper special-handler pipeline.
- edge_cases_or_failure_modes: Model refs with explicit tags, namespaced models, missing tags API, malformed HTML meta, and parameter size extraction duplicates.
- validation_or_tests: Web scraper tests not assigned for Ollama.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3296 `file` `packages/coding-agent/src/web/scrapers/vscode-marketplace.ts`
- cursor: `[_]`
- core_role: Special web scraper for VS Code Marketplace extension pages.
- algorithmic_behavior: Extracts itemName, posts Marketplace API request, maps stats, formats rating/download/install metadata, extracts repository link, and returns extension summary Markdown (`packages/coding-agent/src/web/scrapers/vscode-marketplace.ts:42-100+`).
- inputs_outputs_state: Inputs are Marketplace URLs and API JSON response. Outputs are extension metadata summary or null/error fallback.
- gates_or_invariants: Only marketplace.visualstudio.com hosts handled; missing itemName returns null; stats/properties are type-checked.
- dependencies_and_callers: Used by web scraper special-handler pipeline and marketplace/plugin discovery contexts.
- edge_cases_or_failure_modes: Publisher/name parsing, missing latest version properties, absent ratings/downloads, and repository link absent.
- validation_or_tests: Marketplace/plugin list tests cover UI side; scraper-specific tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3326 `file` `packages/coding-agent/test/modes/components/plugin-list-marketplace.test.ts`
- cursor: `[_]`
- core_role: Regression tests for plugin list/settings/detail marketplace UI.
- algorithmic_behavior: Asserts marketplace plugins render when no npm plugins installed, npm and marketplace entries render together with kind badges, shadowed marketplace entries/scope tags show, empty state mentions npm and marketplace install commands, Enter routes marketplace entry selection, toggling marketplace plugin awaits reload callback, Escape closes while loading, npm listing rejection still mounts marketplace list, and detail view exposes metadata/toggle/home-shortened paths.
- inputs_outputs_state: Inputs are plugin list fixtures, marketplace entries, enabled state, callbacks, and key events. Outputs are rendered text, selected entries, toggle calls, reload order, and close counts.
- gates_or_invariants: Marketplace UI remains useful if npm plugin listing fails; enable toggles must await reload; install paths shorten home to `~`.
- dependencies_and_callers: Validates plugin list/settings/detail components.
- edge_cases_or_failure_modes: Shadowed entries, loading state Escape, mixed plugin sources, and rejected npm list.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-3356 `file` `packages/coding-agent/test/modes/controllers/handoff-command.test.ts`
- cursor: `[_]`
- core_role: Tests for `/handoff` interactive command loading/cancellation behavior.
- algorithmic_behavior: Creates fake context/session, runs handoff generation, asserts a cancellable loader is shown, Escape aborts handoff and restores original editor escape handler, loader clears after completion, and session handoff receives prompt text.
- inputs_outputs_state: Inputs are command args, fake session `handoff`, abort callback, and editor escape handler. Outputs are status container children, abort call count, restored handler, and handoff call args.
- gates_or_invariants: Loader must be cancellable and cleanup must restore editor state whether aborted or completed.
- dependencies_and_callers: Validates handoff command controller and interactive editor/status integration.
- edge_cases_or_failure_modes: Escape during async handoff generation and completion cleanup.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-3386 `file` `packages/coding-agent/test/tools/web-scrapers/youtube-parallel.test.ts`
- cursor: `[_]`
- core_role: Regression test for YouTube scraper preferring Parallel extract.
- algorithmic_behavior: Initializes settings, spies fallback tool ensuring it is not called, invokes YouTube handler, and asserts Parallel content/method/final URL/contentType/notes are returned before `yt-dlp` fallback.
- inputs_outputs_state: Inputs are YouTube URL and mocked Parallel response. Outputs are scraper result and fallback call count.
- gates_or_invariants: Parallel extract success short-circuits local tool fallback.
- dependencies_and_callers: Validates YouTube special scraper and Parallel extract integration.
- edge_cases_or_failure_modes: Provider fetch auto setting and fallback avoidance.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: test-only file`

### OH_MY_HUMANIZE_MAIN-HZ-3416 `file` `packages/collab-web/src/tool-render/tools/github.tsx`
- cursor: `[_]`
- core_role: Collab-web renderer for GitHub tool calls/results.
- algorithmic_behavior: Formats salient args (issue/PR ids, repo, branch, labels), renders summary, args grid, job/run/check visual status, watch view, checkout rows, selected detail keys, and result body for GitHub tool outputs (`packages/collab-web/src/tool-render/tools/github.tsx:7-325`).
- inputs_outputs_state: Inputs are tool args/result/details including PRs, runs/jobs, checkouts, watch state, and GitHub fields. Outputs are React nodes with status classes/icons/text.
- gates_or_invariants: Success/failure/running conclusions map to visual classes; long hashes shorten; unknown args display safely through util helpers.
- dependencies_and_callers: Used by collab-web tool render registry; depends on renderer utilities.
- edge_cases_or_failure_modes: Missing/unknown result shapes, numeric issue ids, long SHA strings, mixed job conclusions, and absent details.
- validation_or_tests: Renderer-specific tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3446 `file` `packages/mnemopi/src/core/extraction/prompts.ts`
- cursor: `[_]`
- core_role: Static prompts for Mnemopi structured fact extraction.
- algorithmic_behavior: Exports system and user prompt templates instructing extraction of structured facts from conversation messages as JSON arrays.
- inputs_outputs_state: Inputs are conversation messages interpolated into template by caller. Outputs are prompt strings for LLM extraction.
- gates_or_invariants: Prompt requires JSON-only output and fact structure; no runtime parsing here.
- dependencies_and_callers: Used by Mnemopi extraction pipeline.
- edge_cases_or_failure_modes: Model non-JSON output handled by caller, not this file.
- validation_or_tests: Extraction tests not assigned.
- skip_candidate: `yes: static prompt constants, not algorithm implementation`

### OH_MY_HUMANIZE_MAIN-HZ-3476 `file` `packages/stats/src/client/ui/JsonBlock.tsx`
- cursor: `[_]`
- core_role: Collapsible JSON display component for stats dashboard UI.
- algorithmic_behavior: Renders a titled JSON block with initial collapsed state and toggle behavior.
- inputs_outputs_state: Inputs are `data`, `title`, and `initialCollapsed`. Outputs are React UI state and pretty JSON display.
- gates_or_invariants: JSON should be safely stringified for display; collapsed state hides body.
- dependencies_and_callers: Used by stats dashboard client.
- edge_cases_or_failure_modes: Non-serializable data could throw if not guarded by caller/component.
- validation_or_tests: No direct assigned test.
- skip_candidate: `yes: UI component; not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3506 `file` `packages/coding-agent/src/commit/agentic/tools/git-file-diff.ts`
- cursor: `[_]`
- core_role: Agentic commit helper tool for retrieving prioritized per-file git diffs.
- algorithmic_behavior: Scores file priority by extension/test/binary/manifest classes, truncates long diffs by keeping head/tail, sorts requested files by priority, caps total chars near 30k tokens, caches diffs by file/staged flag, fetches missing diffs from git, and returns text plus details (`packages/coding-agent/src/commit/agentic/tools/git-file-diff.ts:6-191`).
- inputs_outputs_state: Inputs are cwd, commit agent state, file list, staged flag, and git diff output. Outputs are combined diff text, truncated file list, cache hit count, and cached diffs.
- gates_or_invariants: Max 10 files by schema; binary files are lowest priority; staged defaults true; no diff returns `(no diff)`; truncation records affected files.
- dependencies_and_callers: Used by agentic commit pipeline; depends on git utility wrappers and commit agent state.
- edge_cases_or_failure_modes: Huge diffs, many requested files, test/docs prioritization, cached empty diffs, and binary extension requests.
- validation_or_tests: Commit agentic tool tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3536 `file` `packages/coding-agent/src/markit/converters/pdf/index.ts`
- cursor: `[_]`
- core_role: PDF-to-Markdown converter for Markit/document ingestion.
- algorithmic_behavior: Processes PDF text columns/images, converts pages to Markdown with image blocks inserted by Y coordinate, and handles PDF MIME/extensions (`packages/coding-agent/src/markit/converters/pdf/index.ts:25-46+`).
- inputs_outputs_state: Inputs are PDF file bytes/path and converter context. Outputs are Markdown content plus extracted image assets.
- gates_or_invariants: Handles `.pdf`/PDF MIME only; image placement is sorted by top-Y; text and images should preserve reading order as much as possible.
- dependencies_and_callers: Used by Markit conversion pipeline; depends on PDF extraction/MuPDF utilities.
- edge_cases_or_failure_modes: Multi-column layout ordering, image overlap, empty pages, scanned PDFs, and missing WASM/embed fallback.
- validation_or_tests: PDF converter tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3566 `file` `packages/coding-agent/src/web/search/providers/anthropic.ts`
- cursor: `[_]`
- core_role: Anthropic Messages API web-search provider adapter.
- algorithmic_behavior: Resolves search model/base/auth, builds system blocks, calls Anthropic Messages with `web_search_20250305` tool, parses response content into answer/sources/citations/search queries/usage/request id, parses page age, and exposes `searchAnthropic` plus `AnthropicProvider` (`packages/coding-agent/src/web/search/providers/anthropic.ts:35-332`).
- inputs_outputs_state: Inputs are query, system prompt, limit/num results, max tokens, temperature, API key/base URL/env/auth storage, and abort signal. Outputs are unified `SearchResponse`.
- gates_or_invariants: Search-specific env vars override chat credentials/base/model; default model is `claude-haiku-4-5`; num results collapses from `numSearchResults ?? limit`; missing credentials fail provider availability/search.
- dependencies_and_callers: Used by `web_search` provider chain; depends on Anthropic API wire schema, auth storage credential lookup, and search provider base types.
- edge_cases_or_failure_modes: 404 handled by caller error formatter, missing/invalid content blocks, page age parsing, citations without source metadata, and auth/base URL override precedence.
- validation_or_tests: Web search docs cover behavior; provider-level tests not assigned except schema/availability through web search suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3596 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/validate.ts`
- cursor: `[_]`
- core_role: Validation helper for Mermaid ASCII output line geometry.
- algorithmic_behavior: Defines diagonal character sets, detects whether ASCII output contains diagonals, finds diagonal positions with line/column/char/context info, and throws via `assertNoDiagonals` with optional context (`packages/utils/src/vendor/mermaid-ascii/ascii/validate.ts:12-104`).
- inputs_outputs_state: Inputs are ASCII diagram strings and optional context label. Outputs are booleans, diagonal position arrays, or thrown validation errors.
- gates_or_invariants: ASCII renderer output should avoid diagonal line glyphs when validator is used; line/column positions are derived from split lines.
- dependencies_and_callers: Used by vendored Mermaid ASCII rendering validation and wrapper utilities.
- edge_cases_or_failure_modes: Multi-line diagrams with diagonal glyphs in labels vs line art may be flagged; empty output returns no diagonals.
- validation_or_tests: Mermaid ASCII wrapper/renderer tests would cover this; no assigned direct test.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `120 section headings`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`