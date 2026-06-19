# agent_01 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- evidence_mode: read-only static inspection; no files modified; no test suites executed

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-001 `directory` `.`
- cursor: `[_]`
- core_role: Monorepo root for the Oh My Pi runtime: Bun workspaces, Rust crates, Python robomp services, docs, release scripts, tests, assets, and package manifests.
- algorithmic_behavior: Coordinates build/test/release through `package.json` scripts, Cargo workspace members in `Cargo.toml`, Python project metadata, and package-local exports; `packages/coding-agent` is the dominant implementation package, while `packages/ai`, `packages/catalog`, `packages/agent`, `packages/tui`, `packages/stats`, `packages/mnemopi`, `packages/utils`, and `crates/*` provide core runtime layers.
- inputs_outputs_state: Inputs are source files, manifests, session data paths, model catalogs, worker scripts, and CLI invocations; outputs are CLI binaries, stats dashboard, native addons, package tarballs, generated catalogs, exported HTML, and test results. Static tree scan found roughly 4,507 tracked source-like files, with most under `packages/`.
- gates_or_invariants: Root scripts enforce Bun-first workflows, Rust checks via `scripts/run-rs-task.ts`, install smoke tests via `scripts/install-tests/run-ci.sh`, and release packaging via `scripts/ci-release-publish.ts`; AGENTS rules prohibit direct edits to generated catalog JSON and require `bun check` instead of `tsc`.
- dependencies_and_callers: Root callers include CI scripts, release script, package-local CLIs, Rust native build tooling, Python `robomp`, and downstream package exports consumed by `omp`.
- edge_cases_or_failure_modes: This branch export lacks Git metadata, so Git inspection fails; generated/published package topology differs from source topology; compiled binaries must re-enter the single CLI worker host rather than separate worker entrypoints.
- validation_or_tests: Root `package.json` defines `test`, `check`, `ci:test:smoke`, `ci:test:install-methods`, Rust, Python, and release smoke gates; not executed in this research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-031 `directory` `packages/mnemopi`
- cursor: `[_]`
- core_role: Local SQLite memory engine package with CLI, MCP tools/server, embeddings, recall, beam memory, knowledge triples, banks, migrations, diagnostics, and disaster recovery.
- algorithmic_behavior: `src/core` stores and recalls memories using embeddings, vector indexes, FTS/token scoring, MMR/Weibull scoring, polyphonic recall, query cache/synonyms, extraction, consolidation, and veracity weighting; `src/cli.ts` and `src/mcp-tools.ts` expose those operations as commands and MCP tools.
- inputs_outputs_state: Inputs are text memories, metadata, banks, vectors, triples, scratchpad entries, env/runtime options, import/export JSON, and MCP JSON-RPC calls; outputs are memory IDs, recall results, stats, diagnostics, DB rows, exported JSON, and MCP tool responses.
- gates_or_invariants: DB open/migration helpers centralize schema setup; feature flags gate enhanced/polyphonic recall; embeddings can be disabled or routed to API/local provider; CLI validates numeric arguments and missing resources; consolidation clamps unknown veracity values.
- dependencies_and_callers: Depends on `bun:sqlite`, `@oh-my-pi/pi-ai`, `@oh-my-pi/pi-catalog`, `@oh-my-pi/pi-utils`, optional `fastembed`/`onnxruntime-node`; called by `mnemopi` CLI, MCP server, coding-agent memory tooling, and tests.
- edge_cases_or_failure_modes: Optional embedding initialization failures degrade to null embeddings and are logged; bank deletion may fail; import rejects malformed JSON; feature flags can be host-configured but env-overridden; recall behavior changes with vector availability.
- validation_or_tests: Recursive scan found 137 files including extensive tests for beam, recall, embeddings, migrations, plugins, MCP, diagnostics, recovery, and veracity; assigned test rows cover embedding failure logging and recall feature gates.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-061 `file` `docs/natives-media-system-utils.md`
- cursor: `[_]`
- core_role: Architecture documentation for native media/system utility boundaries between JS APIs and Rust `pi-natives` exports.
- algorithmic_behavior: Defines mapping from JS-facing operations to Rust modules, data format conversions, lifecycle/state transitions, unsupported operations, and platform caveats; it is a contract document rather than executable code.
- inputs_outputs_state: Inputs are images, PDFs, HTML, clipboard/system interactions, and command args; outputs are converted markdown/images, metadata, native return structs, errors, and resource lifecycle events.
- gates_or_invariants: Documents explicit conversion boundaries, platform caveats, unsupported operations, and error propagation so native wrappers do not silently hide platform failures.
- dependencies_and_callers: References `packages/natives`, `crates/pi-natives`, media/doc rendering paths, and system APIs consumed by coding-agent tools.
- edge_cases_or_failure_modes: Unsupported platform operations, native conversion failures, resource cleanup, media format mismatch, and runtime errors crossing JS/Rust FFI.
- validation_or_tests: Documentation-only; validation is indirect through native package tests and callers that depend on the described behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-091 `file` `scripts/ci-release-publish.ts`
- cursor: `[_]`
- core_role: Release publishing workflow script for preparing, packing, and publishing workspace packages and native leaf packages.
- algorithmic_behavior: Rewrites `package.json` publish fields from source paths to `dist`, adjusts `files`, applies publish-time `bin` rewrite, generates native optionalDependencies, packs tarballs with `bun pm pack`, publishes via `npm publish`, and treats already-published versions as nonfatal.
- inputs_outputs_state: Inputs are CLI flags such as `--dry-run`/`--native-leaf`, package manifests, native package tags, generated leaf metadata, and npm pack/publish results; outputs are mutated publish manifests during packaging, tarballs, npm publishes, and console status.
- gates_or_invariants: Native leaf tag must be present for leaf publishing; unknown package dirs throw; dry-run suppresses writes/publish; packed tarball must exist; publish errors are fatal except recognized “already published” output.
- dependencies_and_callers: Uses Bun Shell, `node:fs/promises`, `node:os`, `node:path`, and native package generator helpers; called by root `ci:release:publish` and `ci:release:publish-native-leaf`.
- edge_cases_or_failure_modes: Missing tarball, pack failure, npm publish failure, unsupported native tag, manifest rewrite drift, or optional dependency mismatch between core native package and generated leaf packages.
- validation_or_tests: Install/release smoke coverage is linked through `scripts/install-tests/run-ci.sh`; no script run in this research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-121 `directory` `crates/pi-shell/src`
- cursor: `[_]`
- core_role: Rust shell/process runtime plus output minimizer used by native command execution and terminal tooling.
- algorithmic_behavior: Provides cancellation tokens, command process/shell handling, Windows helpers, shell fixups, and a minimizer pipeline that detects command identity, analyzes shell plans, compiles TOML filter definitions, and applies command-specific output reductions.
- inputs_outputs_state: Inputs are shell command strings, process output, exit codes, minimizer config, TOML definitions, and env/platform info; outputs are process events, cancellation states, minimized output, outlines, and filter test outcomes.
- gates_or_invariants: Shell plan analysis rejects unsafe redirections/substitutions where needed; minimizer pipelines validate schema version and regex rules; command detection strips launch prefixes and global options before routing; filter behavior depends on exit code and command/subcommand.
- dependencies_and_callers: Uses `brush-parser`, `brush-core`, `tokio`, `regex`, `toml`, and platform crates; called through `crates/pi-natives` and higher-level coding-agent bash execution.
- edge_cases_or_failure_modes: Command substitution and redirection safety, wrapped commands (`env`, `sudo`, `time`, `npx`, `docker compose`), large/noisy logs, tool-specific locales, Windows path/process behavior, and cancellation races.
- validation_or_tests: Directory contains 118 assigned-source files including minimizer fixtures and many Rust unit tests in filter modules; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-151 `directory` `packages/stats/src`
- cursor: `[_]`
- core_role: Local observability dashboard backend, sync worker, SQLite aggregation layer, and React client for session/usage metrics.
- algorithmic_behavior: Parses session JSONL incrementally, stores assistant/user metrics and offsets, computes aggregate dashboards by time range, spawns stats sync workers through the worker-host contract, serves API/static dashboard routes, and renders client views for overview, models, costs, behavior, projects, requests, and errors.
- inputs_outputs_state: Inputs are session files, file mtimes/offsets, usage records, service-tier changes, user prompts, dashboard range/hash route, and API requests; outputs are SQLite rows, dashboard DTOs, HTML/static assets, JSON APIs, sync progress, and CLI summaries.
- gates_or_invariants: Worker dispatcher forbids dispatching to busy worker; embedded client archive extraction sanitizes paths; time range parsing defaults safely; parser tolerates partial JSONL; DB migrations/backfills run at init.
- dependencies_and_callers: Depends on `bun:sqlite`, React, Chart.js, `@oh-my-pi/pi-ai`, catalog cost data, and `@oh-my-pi/pi-utils`; called by `omp stats`, compiled smoke tests, server API, and dashboard client.
- edge_cases_or_failure_modes: Missing session files return empty parse results, stale offsets skip already-processed files, embedded client archive may be absent in source mode, worker ping/sync errors bubble, and static build may fail.
- validation_or_tests: Package scripts define check/build; smoke worker probe is used by root CI smoke; assigned UI/type files cover parts of this area.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-181 `file` `docs/tools/ast-edit.md`
- cursor: `[_]`
- core_role: Tool contract documentation for `ast_edit`, the structural code replacement tool.
- algorithmic_behavior: Describes source, inputs, outputs, flow, variants, side effects, limits, errors, and notes for AST-grep style edits; captures preview/apply semantics and replacement reporting.
- inputs_outputs_state: Inputs are file/glob targets, language/AST patterns, replacement templates, preview/apply flags, and cwd; outputs are markdown preview, diff-like replacement summaries, details metadata, and applied file mutations.
- gates_or_invariants: Documents caps, parse-error behavior, stale preview rejection, and explicit apply/preview split to prevent unintended writes.
- dependencies_and_callers: Tied to coding-agent `ast_edit` tool implementation and tests under `packages/coding-agent/test/tools/ast-edit.test.ts`.
- edge_cases_or_failure_modes: No matches, parse errors, stale preview cache, files outside cwd/globs, and replacement count/reporting edge cases.
- validation_or_tests: Assigned ast-edit test row exercises schema shape, line-number padding, preview queueing, stale preview rejection, glob scoping, and TLA+ fallback behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-211 `file` `scripts/install-tests/run-ci.sh`
- cursor: `[_]`
- core_role: Install-method CI smoke script that reproduces published package topology and validates source/link/tarball installs.
- algorithmic_behavior: Creates a temporary install workspace, configures Bun, builds/packs native leaf and core packages, rewrites coding-agent `bin` to `dist/cli.js`, writes dependency overrides to local tarballs, installs, asserts optional native leaf resolution, and runs smoke probes including `omp --smoke-test`.
- inputs_outputs_state: Inputs are repo build outputs, generated native leaf packages, package manifests, Bun install state, temp directories, and package tarballs; outputs are install workspace, packed tarballs, manifest rewrites/restores, and smoke-test pass/fail status.
- gates_or_invariants: Core native package must not bundle `.node`; platform leaf must arrive through optionalDependencies; published coding-agent manifest must point at bundled CLI; manifest changes are restored after packing.
- dependencies_and_callers: Called by root `ci:test:install-methods`; depends on Bun, package scripts, native package generator, and release publish helpers.
- edge_cases_or_failure_modes: Missing dashboard assets in npm/compiled distribution, worker-host entry regressions, optional native dependency resolution failure, or stale manifest rewrites.
- validation_or_tests: This script is itself a CI validation path; not executed in this research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-241 `directory` `packages/catalog/src/identity`
- cursor: `[_]`
- core_role: Model identity, family classification, canonical equivalence, provider priority, and reference resolution subsystem.
- algorithmic_behavior: Parses known model IDs (`classify.ts`), normalizes model-like segments/bracketed affixes (`id.ts`), maps families/dialects (`family.ts`, `dialect.ts`), builds canonical reference/equivalence indexes (`reference.ts`, `equivalence.ts`), ranks providers (`priority.ts`), and chooses preferred canonical variants (`selection.ts`).
- inputs_outputs_state: Inputs are model IDs, provider/model records, equivalence overrides/exclusions, bundled model lists, and provider priority preferences; outputs are parsed family/version structs, canonical IDs, suffix aliases, dialects, reference models, and selected variants.
- gates_or_invariants: Caches are bounded or memoized; canonical candidate generation strips only recognized markers; provider rank is stable; unknown IDs fall back rather than throwing.
- dependencies_and_callers: Used by catalog model manager, AI provider routing, thinking policies, stream healing, and display code; imports catalog model data and shared model types.
- edge_cases_or_failure_modes: Bracketed names, namespace suffixes, provider version suffixes, date suffixes, uppercase penalties, legacy Claude/GML ordering, zero-cost xAI OAuth references, and unknown model families.
- validation_or_tests: Catalog tests and AI issue repros exercise supported efforts and provider URL selection; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-271 `directory` `packages/coding-agent/src/mcp`
- cursor: `[_]`
- core_role: MCP client/config/transport/OAuth manager for connecting external Model Context Protocol servers into coding-agent tools.
- algorithmic_behavior: Loads and writes MCP configs, starts stdio/http transports, speaks JSON-RPC, manages startup events/timeouts/tool cache/tool bridge, discovers OAuth endpoints, stores/refreshes MCP OAuth credentials, integrates Smithery registry/auth/connect, and renders connection/tool state.
- inputs_outputs_state: Inputs are `.mcp.json`/settings configs, server commands/URLs/headers, OAuth metadata, access/refresh tokens, JSON-RPC requests, tool definitions, and abort signals; outputs are MCP connections, prepared configs, bearer headers, tool lists, cached bridge tools, UI render data, and startup events.
- gates_or_invariants: Stdio requires command, HTTP/SSE requires URL, refresh failures are classified definitive vs transient, timeouts use abort signals, and transport teardown must close subprocess/network state.
- dependencies_and_callers: Called by `AgentSession`, `/mcp` controller, ACP mode, capability system, and tests; depends on pi-ai AuthStorage, OAuth flow helpers, Smithery APIs, and transport modules.
- edge_cases_or_failure_modes: Revoked OAuth refresh token, transient network refresh failure, standalone `.mcp.json` discovery, connection timeout, malformed JSON-RPC, server disconnect, and stale tool cache.
- validation_or_tests: Assigned tests cover OAuth discovery, MCP manager refresh behavior, interactive `/mcp test`, and MCP connecting banner.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-301 `directory` `packages/coding-agent/test/extensibility`
- cursor: `[_]`
- core_role: Regression test suite for plugin/extensibility compatibility and custom command behavior.
- algorithmic_behavior: Exercises custom command loading (`custom-commands/ci-green.test.ts`, `review.test.ts`), extension model query behavior, legacy package remaps (`legacy-pi-ai-type-remap`, `legacy-pi-bunfs-root`, `legacy-pi-inplace-load`, `legacy-pi-override-fallback`), and TypeBox shim/remap compatibility.
- inputs_outputs_state: Inputs are fixture plugins/extensions, command definitions, old import shapes, TypeBox-style schemas, and plugin roots; outputs are test assertions for loaded commands, mapped imports, schema validation, and fallback behavior.
- gates_or_invariants: Backward compatibility must survive package rename/remap paths; plugin roots must resolve consistently; custom commands must expose expected behavior without leaking incompatible APIs.
- dependencies_and_callers: Tests target coding-agent discovery/extensibility/plugin loader and schema shim code; run under Bun test.
- edge_cases_or_failure_modes: Legacy extension code depending on old `pi-ai`/TypeBox names, root path substitution, in-place plugin loading, and override fallback collisions.
- validation_or_tests: Directory is validation-only; recursive scan found 9 test files.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-331 `directory` `packages/utils/src/vendor`
- cursor: `[_]`
- core_role: Vendored `mermaid-ascii` parser/rendering algorithms used by utility code to convert Mermaid diagrams into terminal-friendly ASCII output.
- algorithmic_behavior: Parses sequence/class/ER/xychart diagrams, validates diagram models, computes text metrics, routes edges/pathfinding, lays out grids/entities/classes, draws shapes to an ASCII canvas, and applies ANSI conversion.
- inputs_outputs_state: Inputs are Mermaid text, diagram-specific tokens/entities/relationships, terminal dimensions, and styling options; outputs are parsed ASTs, positioned diagrams, ASCII canvas strings, and rendered diagram text.
- gates_or_invariants: Validation modules enforce parseable diagram structure; routing/layout must preserve coordinates; shape modules constrain geometry to canvas bounds; vendored NOTICE records source attribution.
- dependencies_and_callers: Imported by `packages/utils` and downstream renderers that need ASCII Mermaid support; internal modules coordinate through `index.ts` and parser/type modules.
- edge_cases_or_failure_modes: Invalid Mermaid syntax, overlapping edges/nodes, multiline labels, ER cardinalities, unsupported diagrams, and terminal width limits.
- validation_or_tests: No assigned direct test for this directory; static recursive scan found 42 files including parsers, draw routines, routing, shapes, and types.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-361 `file` `crates/pi-natives/src/html.rs`
- cursor: `[_]`
- core_role: Rust native HTML-to-Markdown bridge exposed through `pi-natives`.
- algorithmic_behavior: Defines `HtmlToMarkdownOptions` with `clean_content` and `skip_images`; `html_to_markdown` chooses conversion options and calls `html_to_markdown_rs::convert_to_markdown`/clean conversion depending on flags.
- inputs_outputs_state: Input is HTML string plus optional options; output is markdown string wrapped in `napi::Result`.
- gates_or_invariants: Defaults both options to false; conversion errors propagate through Rust/NAPI result; image skipping and cleaning are explicit options.
- dependencies_and_callers: Depends on `html-to-markdown-rs` and `napi`; called by JS native wrappers and fetch/read HTML conversion tools.
- edge_cases_or_failure_modes: Malformed HTML, unsupported tags, large HTML input, image-heavy pages, and conversion library errors.
- validation_or_tests: Covered indirectly by native media/system utility docs and consumers; no direct test executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-391 `file` `packages/agent/src/proxy.ts`
- cursor: `[_]`
- core_role: Proxy streaming adapter that turns remote proxy SSE events into agent `AssistantMessageEventStream` events.
- algorithmic_behavior: `streamProxy` posts model/context/options to a proxy endpoint, reads SSE JSON, mutates a partial assistant message, maps content/thinking/tool-call deltas through `processProxyEvent`, computes usage cost, and emits terminal done/error events.
- inputs_outputs_state: Inputs are `Model`, agent `Context`, endpoint/api key/fetch/signal options, and proxy SSE event objects; outputs are `ProxyMessageEventStream` events and final `AssistantMessage`.
- gates_or_invariants: Requires successful HTTP response, terminal event detection, abort signal handling, content index validation, and event type mapping; non-OK response tries JSON error extraction.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-ai` types, `parseStreamingJson`, catalog `calculateCost`, and `readSseJson`; called where proxy model streams are used.
- edge_cases_or_failure_modes: HTTP proxy errors, malformed streaming JSON, missing terminal event, abort before/while reading body, invalid content index, and tool-call partial parsing failures.
- validation_or_tests: No assigned direct proxy test; behavior is indirectly covered by agent stream tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-421 `file` `packages/ai/src/auth-storage.ts`
- cursor: `[_]`
- core_role: Central credential, OAuth refresh, usage-reporting, credential rotation, backoff, and SQLite persistence engine for AI providers.
- algorithmic_behavior: `AuthStorage` manages runtime/config/env/fallback/API/OAuth credentials, dedupes OAuth identities, tracks generation changes, selects credentials with round-robin/session stickiness/backoff, refreshes OAuth tokens, fetches/merges usage reports, records usage/cost history, invalidates credentials, rotates session credentials, exports snapshots, and emits disable events.
- inputs_outputs_state: Inputs are provider IDs, API keys, OAuth credentials, refresh signals, session IDs, usage headers, SQLite rows, usage providers, and completion probes; outputs are active API keys/access tokens, credential snapshots, usage reports/history, disabled events, updated SQLite auth rows, and resolver functions.
- gates_or_invariants: Definitive OAuth failures are distinguished from transient failures; refresh skew is applied; session sticky cache uses credential IDs; duplicate OAuth identities are pruned; SQLite migrations/backfills preserve identity keys; usage cache has TTL and durable last-good retention.
- dependencies_and_callers: Depends on `bun:sqlite`, registry OAuth providers, usage providers for Claude/Gemini/Copilot/Codex/Kimi/Zai/Antigravity, rate-limit utils, logger, and provider definitions; called by streaming transports, CLI auth, ACP, MCP manager, and web search providers.
- edge_cases_or_failure_modes: Revoked refresh token, transient fetch failure, expired access token, no provider credentials, concurrent shared refresh, blocked credential retry windows, SQLite busy errors, cache corruption, duplicate account identities, and forced refresh races.
- validation_or_tests: Assigned tests cover force refresh/rotation, stream auth retry, MCP OAuth refresh, provider base URL/auth behavior, and usage-limit rotation; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-451 `file` `packages/ai/test/anthropic-tool-schema.test.ts`
- cursor: `[_]`
- core_role: Contract tests for Anthropic tool schema normalization.
- algorithmic_behavior: Feeds JSON Schema variants into `normalizeAnthropicToolSchema` and asserts SDK-compatible whitelist behavior, including moving unsupported schema keywords into descriptions, preserving supported constructs, and memoizing cyclic references.
- inputs_outputs_state: Inputs are schema objects with strings/numbers/arrays/objects/refs/defs/const/default/anyOf and unsupported keywords; outputs are normalized schema objects and reference identity checks.
- gates_or_invariants: Original schemas must not mutate; unsupported keys must not leak into final unsupported positions; circular refs must memoize; Anthropic SDK parity cases are preserved.
- dependencies_and_callers: Imports `normalizeAnthropicToolSchema` from `@oh-my-pi/pi-ai/providers/anthropic`; validates provider request-shaping code.
- edge_cases_or_failure_modes: Unknown formats, unsupported array/object constraints, cyclic properties, nested refs, prefixItems/items, and additionalProperties variants.
- validation_or_tests: This is a Bun test file with two describe blocks covering whitelist and Anthropic SDK transform parity.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-481 `file` `packages/ai/test/auth-storage-force-refresh-rotate.test.ts`
- cursor: `[_]`
- core_role: Regression tests for AuthStorage forced OAuth refresh and credential rotation.
- algorithmic_behavior: Registers a test OAuth provider, stores credentials in SQLite, calls `peekApiKey`, `forceRefreshCredentialById`, and `rotateSessionCredential`, and asserts refresh/rotation/backoff semantics.
- inputs_outputs_state: Inputs are synthetic OAuth credentials, mocked refresh callbacks, session IDs, auth/usage-limit errors, and SQLite store; outputs are refreshed access tokens, rotation boolean/object outcomes, usage-limit mark calls, and retry timestamps.
- gates_or_invariants: Normal `peekApiKey` must use cached access; forced refresh must mint and persist a new access token; auth errors rotate without usage-limit marking; usage-limit errors mark usage before switching; single-credential auth failure cannot rotate.
- dependencies_and_callers: Uses `AuthStorage`, `SqliteAuthCredentialStore`, `registerOAuthProvider`, and spies on `markUsageLimitReached`.
- edge_cases_or_failure_modes: Usage-limit vs auth error classification, no alternate credential, untouched session, already-blocked credential, missing active credential.
- validation_or_tests: Bun test file; not executed in research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-511 `file` `packages/ai/test/github-copilot-openai-base-url.test.ts`
- cursor: `[_]`
- core_role: Regression tests for GitHub Copilot OpenAI-compatible base URL/auth selection.
- algorithmic_behavior: Mocks fetch for chat completions and responses transports, passes regular/enterprise/business Copilot API-key JSON, and asserts requested URLs, authorization headers, and initiator headers.
- inputs_outputs_state: Inputs are bundled Copilot/OpenAI models, JSON API key payloads, mocked unauthorized responses, and test context; outputs are captured request URLs/headers and error stop reasons.
- gates_or_invariants: Default Copilot uses `api.githubcopilot.com`; enterprise URL maps to `copilot-api.<enterprise>`; business mode uses `api.business.githubcopilot.com`; token must be placed in Bearer auth; initiator is `agent`.
- dependencies_and_callers: Targets `streamOpenAICompletions`, `streamOpenAIResponses`, and catalog bundled model definitions.
- edge_cases_or_failure_modes: Responses vs chat endpoint paths, enterprise host derivation, business URL override, auth header extraction.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-541 `file` `packages/ai/test/issue-2315-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for MiniMax M2 / GPT-OSS reasoning effort catalog behavior.
- algorithmic_behavior: Captures OpenAI completions request payloads and asserts `getSupportedEfforts` and emitted `reasoning_effort` values for bundled/custom models.
- inputs_outputs_state: Inputs are built/bundled model specs, Effort settings, mocked SSE responses, and context; outputs are request JSON bodies and supported-effort arrays.
- gates_or_invariants: Unsupported reasoning tiers must be excluded from catalog policy; supported low/medium/high map correctly; unknown/custom max and none behavior is preserved.
- dependencies_and_callers: Uses `streamOpenAICompletions`, catalog `buildModel`, `getSupportedEfforts`, and bundled models.
- edge_cases_or_failure_modes: Model-specific effortMap absence, default effort selection, explicit unsupported/max/none effort emission.
- validation_or_tests: Bun issue repro test; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-571 `file` `packages/ai/test/ollama-cloud-login.test.ts`
- cursor: `[_]`
- core_role: Tests interactive Ollama Cloud API-key login flow.
- algorithmic_behavior: Calls `loginOllamaCloud` with prompt callbacks, asserts displayed auth URL/instructions/prompt metadata and returned API key, and rejects missing/empty prompt responses.
- inputs_outputs_state: Inputs are mock prompt callbacks and empty callback object; outputs are API key or thrown errors.
- gates_or_invariants: Interactive prompt is required; empty key is invalid; URL/instructions remain stable for users.
- dependencies_and_callers: Targets `@oh-my-pi/pi-ai/registry/ollama-cloud`.
- edge_cases_or_failure_modes: User cancels or submits empty API key; noninteractive environment.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-601 `file` `packages/ai/test/openai-responses-system-prompt.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI Responses API system/developer prompt routing.
- algorithmic_behavior: Captures request body from `streamOpenAIResponses` and asserts when system/developer messages are moved into `instructions` vs left in input, including proxy reasoning variants.
- inputs_outputs_state: Inputs are contexts containing system/developer/user messages and response-capable models; outputs are request body `instructions` and `input` arrays.
- gates_or_invariants: System prompts are stripped from input when routed to `instructions`; multiple system prompts join with blank line; developer prompts stay as developer messages unless proxy reasoning path uses instructions.
- dependencies_and_callers: Targets `streamOpenAIResponses`, catalog model builders, and provider request shaper.
- edge_cases_or_failure_modes: Empty/no system prompt, model family differences, proxy model prompt routing, developer-only contexts.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-631 `file` `packages/ai/test/stream-auth-retry.test.ts`
- cursor: `[_]`
- core_role: Tests `streamSimple` API-key resolver retry/rotation behavior on auth and usage-limit failures.
- algorithmic_behavior: Registers a custom API stream that can emit success/error streams, pushes keys through resolver contexts, and asserts retry sequence, event types, resolver errors, last-chance flags, and original error propagation.
- inputs_outputs_state: Inputs are mocked `ApiKeyResolver`, synthetic auth/usage-limit/google resource-exhausted errors, stream options, and custom model; outputs are assistant messages, captured keys/contexts/errors, or thrown original failures.
- gates_or_invariants: Retry only when resolver returns a new key; stream events should suppress failed attempt events; lastChance/context error must be accurate; missing API key stops before provider call.
- dependencies_and_callers: Targets `streamSimple`, custom API registry, `AssistantMessageEventStream`.
- edge_cases_or_failure_modes: Resolver throws, same key returned, usage-limit errors, Google resource exhausted text, no API key, original nonretryable errors.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-661 `file` `packages/catalog/src/index.ts`
- cursor: `[_]`
- core_role: Public catalog package barrel export.
- algorithmic_behavior: Re-exports catalog modules for compatibility, discovery, effort, identity, model cache/manager/thinking, bundled models, provider-model descriptors, variant collapse, and provider wire helpers.
- inputs_outputs_state: Inputs are imported module exports; output is consolidated public API surface for `@oh-my-pi/pi-catalog`.
- gates_or_invariants: Export order and star exports define package API; no runtime state or validation beyond module resolution.
- dependencies_and_callers: Consumed across `packages/ai`, `packages/coding-agent`, tests, and external users.
- edge_cases_or_failure_modes: Ambiguous/redundant exports or missing module path would break consumers.
- validation_or_tests: Type/package checks validate this indirectly.
- skip_candidate: `yes: pure barrel export; core API surface but no algorithmic logic`

### OH_MY_HUMANIZE_MAIN-HZ-691 `file` `packages/catalog/test/issue-772-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Xiaomi MiMo token-plan API key routing and dynamic model discovery.
- algorithmic_behavior: Mocks fetch, calls Xiaomi login/model-manager options with `tp-` and `sk-` keys, and asserts host routing plus dynamic model parsing/filtering.
- inputs_outputs_state: Inputs are token-plan vs standard API keys and mocked model/list responses; outputs are captured URLs and parsed model IDs.
- gates_or_invariants: `tp-` keys route to `token-plan-sgp.xiaomimimo.com`; standard keys route to `api.xiaomimimo.com`; bundled JSON must not include ASR model entry.
- dependencies_and_callers: Uses `loginXiaomi`, `xiaomiModelManagerOptions`, and `models.json`.
- edge_cases_or_failure_modes: Wrong host for token-plan key, ASR model leaking into text model catalog, empty data arrays.
- validation_or_tests: Bun issue repro test; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-721 `file` `packages/coding-agent/scripts/format-prompts.ts`
- cursor: `[_]`
- core_role: Prompt formatting maintenance script for coding-agent static prompt markdown files.
- algorithmic_behavior: Scans prompt files, formats prompt content with shared prompt formatter, and writes normalized content when invoked by maintainers.
- inputs_outputs_state: Inputs are static `.md` prompt files and formatting options; outputs are rewritten prompt files or no-op formatted state.
- gates_or_invariants: Prompts remain static assets rather than inline code; formatter preserves semantic structure while normalizing whitespace/symbols.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-utils/prompt` and coding-agent prompt directories; called manually or by maintenance scripts.
- edge_cases_or_failure_modes: Invalid prompt glob, accidental semantic formatting change, non-markdown prompt asset.
- validation_or_tests: Shared prompt formatter is covered by `packages/utils/test/prompt.test.ts`; script not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-751 `file` `packages/coding-agent/test/agent-session-acp-permission.test.ts`
- cursor: `[_]`
- core_role: Behavioral tests for ACP permission gating around `AgentSession` tools.
- algorithmic_behavior: Creates fake tools/session/client bridge, wraps tools through ACP permission policy, and asserts when permission prompts fire, cache, abort, reject, or bypass.
- inputs_outputs_state: Inputs are fake tool calls (`bash`, `delete`, `move`, `edit`, `write`, `ast_edit`, `read`), approval modes, bridge outcomes, and abort signals; outputs are bridge requests, tool execute counts, thrown ToolErrors, and permission metadata.
- gates_or_invariants: Read/edit/write/ast_edit normal operations bypass ACP; delete/move/bash are gated unless yolo policy applies; per-tool prompt policy can override yolo; unknown permission options fail closed; abort must not execute underlying tool.
- dependencies_and_callers: Targets `AgentSession`, `SessionManager`, `EditTool`, settings approval mode, client bridge permission API.
- edge_cases_or_failure_modes: Patch-mode delete overriding stale move metadata, always-allow cache, forever reject followed by ordinary edit, setClientBridge after active tools, permission pending status.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-781 `file` `packages/coding-agent/test/agent-session-role-thinking.test.ts`
- cursor: `[_]`
- core_role: Tests role/model switching and thinking-level behavior in `AgentSession`.
- algorithmic_behavior: Builds sessions with model roles and thinking config, switches roles, cycles thinking, exercises auto-thinking classifier success/failure, and asserts session/agent state persistence.
- inputs_outputs_state: Inputs are bundled models, settings role strings with effort suffixes, classifier mock results, and session files; outputs are role switch return objects, `thinkingLevel`, configured/auto-resolved state, and persisted session context.
- gates_or_invariants: Role-specific thinking can override current effort; explicit cycling updates `disableReasoning`; auto-thinking defers or resolves depending on streaming/compact model; fallback effort applies on classifier failure.
- dependencies_and_callers: Targets `AgentSession`, `ModelRegistry`, settings, `auto-thinking/classifier`, `AuthStorage`, `SessionManager`.
- edge_cases_or_failure_modes: Unsupported xhigh level, auto-thinking persistence across resume, classifier unavailable, compact/smol models, no thinking-capable model.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-811 `file` `packages/coding-agent/test/bash-execution-clamp.test.ts`
- cursor: `[_]`
- core_role: Tests terminal-visible-width clamping for bash output rendering.
- algorithmic_behavior: Calls private/renderer clamp behavior through `BashExecutionComponent`, feeding long ASCII/CJK/emoji/ANSI/combining strings and asserting omitted-column markers and widths.
- inputs_outputs_state: Inputs are synthetic display lines and theme/TUI stubs; outputs are clamped strings and visible-width measurements.
- gates_or_invariants: Clamp threshold is 4,000 visible columns; output must count grapheme/ANSI width correctly; exact/below-limit strings pass unchanged; over-limit strings include ellipsis and omitted visible-column count.
- dependencies_and_callers: Targets `BashExecutionComponent` and `pi-tui` `visibleWidth`.
- edge_cases_or_failure_modes: Wide CJK, emoji ZWJ, combining accents, ANSI escape zero width, very long single line memory safety.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-841 `file` `packages/coding-agent/test/custom-editor-keybindings.test.ts`
- cursor: `[_]`
- core_role: Tests custom editor keybinding precedence.
- algorithmic_behavior: Instantiates `CustomEditor`, simulates key handlers, and asserts retry/copy/custom callbacks fire or are suppressed according to binding precedence.
- inputs_outputs_state: Inputs are key events and callback spies; outputs are callback invocation counts.
- gates_or_invariants: Custom handler can consume retry binding; copy prompt binding must not trigger retry; theme/editor initialization must be complete.
- dependencies_and_callers: Targets `CustomEditor`, theme initialization, and keybinding matchers.
- edge_cases_or_failure_modes: Overlapping user-defined bindings, default retry binding, copy prompt action.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-871 `file` `packages/coding-agent/test/hindsight-client.test.ts`
- cursor: `[_]`
- core_role: Tests timestamp serialization for Hindsight API client requests.
- algorithmic_behavior: Mocks `globalThis.fetch`, sends API calls, extracts first timestamp from request body, and asserts local-offset ISO strings rather than `Z`.
- inputs_outputs_state: Inputs are Hindsight API payloads with timestamps; outputs are serialized JSON request bodies.
- gates_or_invariants: Timestamps must preserve local offset format and avoid UTC `Z` suffix.
- dependencies_and_callers: Targets `HindsightApi` client.
- edge_cases_or_failure_modes: Time zone offset formatting, Date serialization defaulting to UTC, missing timestamp.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-901 `file` `packages/coding-agent/test/interactive-mode-mcp-connecting.test.ts`
- cursor: `[_]`
- core_role: Tests InteractiveMode subscription to MCP connecting banner events.
- algorithmic_behavior: Builds an `InteractiveMode` harness, emits `MCP_CONNECTING_EVENT_CHANNEL` payloads on `EventBus`, and asserts status display, stale-event rejection, and malformed payload logging behavior.
- inputs_outputs_state: Inputs are MCP connecting event objects with server names and malformed payloads; outputs are `showStatus`, `logger.warn`, and `logger.error` spy calls.
- gates_or_invariants: Constructor-time subscription must exist before async MCP config loading; invalid event shape must reject safely without throwing into EventBus.
- dependencies_and_callers: Targets `InteractiveMode`, MCP startup events, `EventBus`, logger, theme, session scaffolding.
- edge_cases_or_failure_modes: Stale generation events, malformed event payload, async subscription race.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-931 `file` `packages/coding-agent/test/issue-956-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for interactive `/mcp test` against standalone `.mcp.json` config.
- algorithmic_behavior: Creates temp project MCP config, mocks `connectToServer`, `listTools`, and `disconnectServer`, runs `MCPCommandController`, and asserts it connects, lists tools, disconnects, refreshes/rendering without error.
- inputs_outputs_state: Inputs are `.mcp.json` config, mocked connection/tool list, controller callbacks; outputs are spy calls and UI render refresh.
- gates_or_invariants: Standalone project `.mcp.json` must be discovered; test action uses abort signal; connection must be disconnected after list.
- dependencies_and_callers: Targets MCP command controller, MCP client functions, project/config dirs.
- edge_cases_or_failure_modes: Missing config root, failed connection, no tool list, stale project dir env.
- validation_or_tests: Bun issue repro test; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-961 `file` `packages/coding-agent/test/mcp-manager-oauth-refresh.test.ts`
- cursor: `[_]`
- core_role: Regression tests for MCP OAuth refresh failure handling.
- algorithmic_behavior: Prepares MCP server config with OAuth credential ID, mocks `refreshMCPOAuthToken`, calls `MCPManager.prepareConfig`, and asserts bearer header/credential persistence behavior by failure class.
- inputs_outputs_state: Inputs are stale OAuth credential, mock refresh outcomes, token URL, AuthStorage SQLite store; outputs are prepared headers and remaining stored credential.
- gates_or_invariants: Definitive 400 invalid_grant and 401 failures must remove credential and omit stale bearer; transient network failure must keep stale access; successful refresh must persist fresh access/refresh.
- dependencies_and_callers: Targets `MCPManager`, pi-ai `AuthStorage`, `oauth-flow.refreshMCPOAuthToken`.
- edge_cases_or_failure_modes: Reauth loops from stale bearer, revoked refresh token, network failure, credential deletion.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-991 `file` `packages/coding-agent/test/oauth-discovery.test.ts`
- cursor: `[_]`
- core_role: Tests MCP OAuth discovery and auth-server extraction.
- algorithmic_behavior: Mocks fetch for RFC 8414 metadata/resource metadata, calls `discoverOAuthEndpoints` and `extractMcpAuthServerUrl`, and asserts endpoint discovery order and URL resolution.
- inputs_outputs_state: Inputs are MCP server URLs, auth-server URLs, `Mcp-Auth-Server` headers/errors, resource metadata JSON, and mocked fetch responses; outputs are OAuth endpoint objects and called URLs.
- gates_or_invariants: Origin-root well-known is tried first, path-prefixed relative well-known fallback is supported, RFC pathful issuer fallback is supported, resource metadata chain is followed, relative auth server resolves against server URL.
- dependencies_and_callers: Targets `mcp/oauth-discovery` helpers and fetch-mock test helper.
- edge_cases_or_failure_modes: Path-prefixed gateway, absolute auth server success, resource metadata with alternate auth server, malformed relative header without base URL.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1021 `file` `packages/coding-agent/test/rpc-client.start.test.ts`
- cursor: `[_]`
- core_role: Minimal test for RPC client provider validation on start.
- algorithmic_behavior: Constructs `RpcClient` with missing provider and asserts `start()` rejects with unknown-provider error.
- inputs_outputs_state: Input is invalid provider ID; output is rejected promise.
- gates_or_invariants: RPC start must fail early for unknown provider rather than starting broken session.
- dependencies_and_callers: Targets `modes/rpc/rpc-client`.
- edge_cases_or_failure_modes: Invalid provider config.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1051 `file` `packages/coding-agent/test/session-manager-immediate-persist.test.ts`
- cursor: `[_]`
- core_role: Tests immediate JSONL session persistence and materialization races.
- algorithmic_behavior: Creates temp `SessionManager`, appends user/assistant/custom entries, reads JSONL from disk, and asserts visible session file contents after appends/ensure-on-disk/shutdown.
- inputs_outputs_state: Inputs are messages, delayed atomic storage, custom workflow events, and temp session dirs; outputs are session JSONL files and list results.
- gates_or_invariants: Append must create/persist visible file immediately; entries appended during materialization must stay on visible file; pre-assistant empty sessions remain out of history; user-only sessions can persist.
- dependencies_and_callers: Targets `SessionManager`, `FileSessionStorage`, session JSONL storage.
- edge_cases_or_failure_modes: Race between ensureOnDisk and appends, shutdown before assistant response, delayed storage.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1081 `file` `packages/coding-agent/test/status-line-transparent.test.ts`
- cursor: `[_]`
- core_role: Tests transparent status-line background rendering.
- algorithmic_behavior: Builds `StatusLineComponent` with transparent setting toggled, renders borders, and asserts ANSI background codes/caps appear or are removed.
- inputs_outputs_state: Inputs are settings, theme, fake session, and component options; outputs are rendered ANSI strings.
- gates_or_invariants: Nontransparent mode includes theme background; transparent mode resets background with `\x1b[49m` and omits cap glyphs/background.
- dependencies_and_callers: Targets status-line component and theme/settings.
- edge_cases_or_failure_modes: ANSI background leakage into terminal, session accent caps in transparent mode.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1111 `file` `packages/coding-agent/test/tool-execution-memoization.test.ts`
- cursor: `[_]`
- core_role: Tests memoization for expensive tool-call/result rendering.
- algorithmic_behavior: Wraps custom tools with render spies, renders `ToolExecutionComponent` before/after changes, and asserts `renderResult`/`renderCall` recompute only when dirty keys change.
- inputs_outputs_state: Inputs are synthetic tool calls/results/args/theme and render widths; outputs are rendered frames and spy call counts.
- gates_or_invariants: Result shaping must not run before result exists; unchanged result/call render must reuse cache; arg/result changes invalidate cache.
- dependencies_and_callers: Targets `ToolExecutionComponent` and TUI rendering.
- edge_cases_or_failure_modes: Large result O(size) reshaping on every frame, stale rendered content after args/result mutation.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1141 `file` `packages/collab-web/test/markdown.test.tsx`
- cursor: `[_]`
- core_role: Tests transcript Markdown rendering in collab-web.
- algorithmic_behavior: Renders markdown to static HTML and asserts tree-like Unicode line breaks, list line preservation, and HTML escaping.
- inputs_outputs_state: Inputs are Korean/tree text, markdown list text, and unsafe HTML; outputs are static HTML strings.
- gates_or_invariants: Plain newline/tree characters should render as readable breaks; unsafe HTML must be escaped, not interpreted.
- dependencies_and_callers: Targets `components/transcript/Markdown`.
- edge_cases_or_failure_modes: Unicode box drawing in markdown, nested list line breaks, XSS through raw HTML.
- validation_or_tests: Bun/React server-render test; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1171 `file` `packages/mnemopi/src/cli.ts`
- cursor: `[_]`
- core_role: Command-line interface for Mnemopi memory operations.
- algorithmic_behavior: Parses commands (`store`, `recall`, `update`, `delete`, `export`, `import`, `stats`, `sleep`, `scratchpad`, `bank`, `diagnose`, `mcp`), resolves DB/data dir, opens/owns `BeamMemory`, validates arguments, formats output, flushes extractions, and closes owned memory.
- inputs_outputs_state: Inputs are CLI argv, optional test context/memory factory, import/export paths, memory content, source, importance, bank names, and db paths; outputs are exit codes, stdout/stderr text, memory DB mutations, export JSON, import stats, diagnostics.
- gates_or_invariants: Missing args throw usage errors; numeric args must parse finite/int; import file must exist and contain object JSON; update/delete fail when memory not found; bank `ValueError` maps to CLI failure.
- dependencies_and_callers: Depends on `BeamMemory`, `BankManager`, diagnostics, MCP server, config; called as `mnemopi` bin and by tests.
- edge_cases_or_failure_modes: Invalid JSON import, missing import path, no command, unknown command, bank conflict/not found, memory ownership cleanup after async recall.
- validation_or_tests: `packages/mnemopi/test/cli*.test.ts`, stats parity, errors parity, and assigned feature/embedding tests cover CLI-adjacent behavior; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1201 `file` `packages/mnemopi/test/embedding-failure-logging.test.ts`
- cursor: `[_]`
- core_role: Tests embedding provider failure logging severity.
- algorithmic_behavior: Temporarily configures local model env, injects failing local model initializer, calls `embed`, and asserts debug vs warn logging depending on runtime debug flag.
- inputs_outputs_state: Inputs are env snapshots, injected initializer error, runtime debug option; outputs are `embed` null result and logger spy calls.
- gates_or_invariants: Normal local model load failure logs debug with model context and does not warn; debug runtime escalates same failure to warn and avoids debug duplicate.
- dependencies_and_callers: Targets embeddings provider and runtime-options context; uses `logger`.
- edge_cases_or_failure_modes: Optional embedding backend unavailable, env contamination across tests, repeated provider reset.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1231 `file` `packages/mnemopi/test/recall-feature-flags.test.ts`
- cursor: `[_]`
- core_role: Tests host-configured and env-overridden recall feature flags.
- algorithmic_behavior: Calls `configureRecallFeatures`, then asserts `polyphonicRecallEnabled`, `enhancedRecallEnabled`, `polyphonicRecallIsEnabled`, `isEnhancedRecallEnabled`, and `isQueryCacheEnabled`.
- inputs_outputs_state: Inputs are partial feature flag objects and synthetic env maps; outputs are boolean gate values.
- gates_or_invariants: Defaults are off; host config enables gates when env unset; env vars override both directions; partial updates preserve unspecified flags.
- dependencies_and_callers: Targets Mnemopi config, polyphonic recall, and query-cache gates.
- edge_cases_or_failure_modes: Query cache requires enhanced recall plus caller flag, env override disabling configured true, partial flag updates.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1261 `file` `packages/snapcompact/research/anthropic_api.py`
- cursor: `[_]`
- core_role: Research helper for direct Anthropic API calls with text/image messages.
- algorithmic_behavior: Loads API key from `~/.env`, builds base64 PNG image blocks, posts Messages API requests with optional system and thinking effort, retries on transient status codes, and returns text/usage/stop reason.
- inputs_outputs_state: Inputs are prompt/messages, optional PNG path/system/effort/model/max tokens/retry count; outputs are text completion, usage dict, stop reason, or process exit error.
- gates_or_invariants: API key must exist; transient 429/5xx statuses retry with sleep; nonretry API errors exit with detail; image block media type is fixed to PNG.
- dependencies_and_callers: Uses Python stdlib `urllib`, `json`, `base64`, `Path`; likely imported by snapcompact research experiments.
- edge_cases_or_failure_modes: Missing key, HTTP error body decode, exhausted retries, image file missing, non-text content blocks.
- validation_or_tests: Research script; no automated test found.
- skip_candidate: `yes: research utility, not production runtime, though it implements API-call workflow logic`

### OH_MY_HUMANIZE_MAIN-HZ-1291 `file` `packages/snapcompact/research/exp19_bestglm.py`
- cursor: `[_]`
- core_role: Research experiment for optimizing visual document rendering profiles for `z-ai/glm-4.6v`.
- algorithmic_behavior: Builds SQuAD-derived grid/doc pages, renders bitmap text with font/color variants, sends PNG QA prompts to LLM providers, parses numbered/unstructured answers, scores exact/F1, aggregates token/cost metrics, merges records, and writes result summaries/matrices.
- inputs_outputs_state: Inputs are CLI args for models/lengths/conditions/font/size/render-only/workers, SQuAD paragraphs/questions, cached render/provider helpers, API keys; outputs are PNGs, JSONL records, matrix CSV, summary JSON, and console summaries.
- gates_or_invariants: Conditions must be known; render cache avoids rewriting existing PNGs; parser falls back when GLM omits numbering; aggregation handles empty records; render-only avoids model calls.
- dependencies_and_callers: Depends on PIL, local research modules `squad`, `bdf`, `final`, `providers`, `run`; called manually for snapcompact experiments.
- edge_cases_or_failure_modes: Provider/API failure, answer count mismatch, cache collisions, render-only with missing tasks, long words, no records, old record merge conflicts.
- validation_or_tests: Research script; no automated test found.
- skip_candidate: `yes: experiment script rather than shipped core algorithm, though it contains substantive evaluation logic`

### OH_MY_HUMANIZE_MAIN-HZ-1321 `file` `packages/snapcompact/research/snapcompact_r2_crystal.py`
- cursor: `[_]`
- core_role: Research visualization generator for animated logit-lens GIFs.
- algorithmic_behavior: Loads lens JSON and image carrier, validates layer/grid assumptions, crops image cells, renders per-layer frames with token probabilities, confidence meter, stage labels, control/target comparison, glow effects, and writes animated GIF plus final PNG.
- inputs_outputs_state: Inputs are research JSON, carrier image, fonts, constants for answer token/layer count; outputs are `crystal.gif` and `crystal_final.png`.
- gates_or_invariants: Asserts 29 layers, 56 image grid, expected answer token; carrier image must be 1568x1568; token labels sanitized for display.
- dependencies_and_callers: Uses PIL and local data files under snapcompact research results; manual research visualization path.
- edge_cases_or_failure_modes: Missing fonts, malformed JSON, unexpected layer count/token, carrier size mismatch, nonprintable token strings.
- validation_or_tests: Research script; no automated test found.
- skip_candidate: `yes: research visualization artifact generator, not shipped runtime behavior`

### OH_MY_HUMANIZE_MAIN-HZ-1351 `file` `packages/stats/src/shared-types.ts`
- cursor: `[_]`
- core_role: Shared dashboard DTO type definitions for stats backend/client.
- algorithmic_behavior: Declares aggregate, model/folder, time-series, cost, dashboard, and behavior metrics shapes; no runtime algorithm.
- inputs_outputs_state: Inputs are TypeScript type consumers; outputs are compile-time contracts for API/client data.
- gates_or_invariants: Field names/optional nullability form the API schema expected by client and server.
- dependencies_and_callers: Used by stats aggregator, DB queries, server API, and React client routes/components.
- edge_cases_or_failure_modes: Type drift between backend responses and client expectations.
- validation_or_tests: Type checks validate indirectly.
- skip_candidate: `yes: type-only contract; no executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1381 `file` `packages/tui/src/mouse.ts`
- cursor: `[_]`
- core_role: SGR mouse escape sequence parser and routing interface.
- algorithmic_behavior: `parseSgrMouse` matches SGR mouse reports, parses button/col/row, derives release/wheel/motion/leftClick booleans, and returns null for nonmouse input.
- inputs_outputs_state: Input is raw terminal input string; output is `SgrMouseEvent` or null.
- gates_or_invariants: Only SGR pattern is accepted; release is encoded by trailing `m`; wheel/motion/left click are derived from button bit fields.
- dependencies_and_callers: Used by TUI components that implement `MouseRoutable`.
- edge_cases_or_failure_modes: Non-SGR escape data, malformed numeric fields, wheel/motion button combinations, 1-based terminal coordinates.
- validation_or_tests: Covered indirectly by TUI interaction tests; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1411 `file` `packages/tui/test/issue-2095-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Windows ConPTY render settle behavior after full repaint.
- algorithmic_behavior: Forces `process.platform` to win32, renders tall content through `TUI`/virtual terminal, fires spinner-like render storms, and asserts settle-window coalescing, forced render preemption, stop cleanup, and scheduler timer behavior.
- inputs_outputs_state: Inputs are virtual terminal size, tall component output, custom render scheduler/timers, render requests; outputs are write captures and full redraw counters.
- gates_or_invariants: After a full paint exceeding viewport height, non-forced renders inside 150ms settle window coalesce into one trailing render; forced renders bypass; `stop()` cancels pending trailing render.
- dependencies_and_callers: Targets `pi-tui` renderer, `VirtualTerminal`, render scheduler.
- edge_cases_or_failure_modes: Windows Terminal viewport drift, 30Hz spinner storm, Ctrl+L reset during settle, pending timers after stop.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1441 `file` `packages/tui/test/render-stress-scheduler.ts`
- cursor: `[_]`
- core_role: Test helper implementing deterministic render scheduling under stress.
- algorithmic_behavior: Records immediate/render callbacks, advances virtual time, drains callbacks in rounds, and throws if the scheduler does not settle after 100 rounds.
- inputs_outputs_state: Inputs are scheduled callbacks and virtual terminal flush state; outputs are callback execution and deterministic time progression.
- gates_or_invariants: `drain()` must terminate; canceled render callbacks are skipped; time increments by 1 per drain cycle.
- dependencies_and_callers: Used by TUI stress/regression tests.
- edge_cases_or_failure_modes: Infinite rescheduling loop, canceled callback retained, virtual terminal flush pending.
- validation_or_tests: Helper is validated indirectly by TUI tests.
- skip_candidate: `yes: test infrastructure helper, not product runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1471 `file` `packages/typescript-edit-benchmark/src/in-process-client.ts`
- cursor: `[_]`
- core_role: In-process benchmark client for driving coding-agent sessions without spawning the CLI.
- algorithmic_behavior: Discovers shared AuthStorage/ModelRegistry with settings overrides, constructs `AgentSession`, forwards agent events to listeners, prompts/follow-ups, changes thinking level, aborts, exposes stats/messages/state, and disposes session/MCP manager.
- inputs_outputs_state: Inputs are benchmark options, cwd/model/thinking/tool variant settings, prompts, event listeners; outputs are session events, assistant text, stats, messages, state snapshot, and cleanup.
- gates_or_invariants: `start()` must initialize session before operations; event listener unsubscribe removes listener; dispose cleans session and MCP manager; edit settings are applied only when non-auto.
- dependencies_and_callers: Depends on coding-agent SDK exports, `AuthStorage`, `ModelRegistry`, `AgentSession`, benchmark runner.
- edge_cases_or_failure_modes: Missing auth/model infra, listener throwing, prompt before start, session disposal race, MCP manager cleanup.
- validation_or_tests: Benchmark utility; validated indirectly by benchmark runs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1501 `file` `packages/utils/src/postmortem.ts`
- cursor: `[_]`
- core_role: Process cleanup and fatal error/postmortem handler utility.
- algorithmic_behavior: Registers cleanup callbacks, runs them once by reason, wires main-thread process handlers for exit/SIGINT/SIGTERM/uncaught errors/rejections, optionally opens inspector on fatal, formats fatal errors, and provides `cleanup()`/`quit()`.
- inputs_outputs_state: Inputs are registered callbacks, process signals/errors, manual cleanup calls, stdout state; outputs are cleanup callback execution, logs, process exit, and unregister functions.
- gates_or_invariants: Callbacks are armed once; cleanup stage prevents registering live cleanup during cleanup; errors from cleanup are logged not thrown; worker threads get reduced exit handling.
- dependencies_and_callers: Uses `node:inspector`, `node:worker_threads`, shared logger; called by runtime components needing reliable cleanup.
- edge_cases_or_failure_modes: Cleanup callback rejection, repeated cleanup, registering during cleanup, fatal exception while inspector already open, stdout drain before exit.
- validation_or_tests: No assigned direct test; behavior is system-level.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1531 `file` `packages/utils/test/prompt.test.ts`
- cursor: `[_]`
- core_role: Tests shared prompt formatting/rendering helpers.
- algorithmic_behavior: Calls `prompt.format`, `prompt.compile`, and `prompt.render` to assert ASCII symbol replacement, RFC 2119 normalization, table/blank/XML/Handlebars formatting, compile cache, brace ambiguity, and `join` helper behavior.
- inputs_outputs_state: Inputs are prompt strings/templates and render contexts; outputs are formatted/rendered strings and cached compiled template identity.
- gates_or_invariants: Markdown comments/code fences preserve literal tokens; RFC normalization skips bold/code where appropriate; pre-render vs post-render Handlebars blank handling differs; compile cache returns same object for same template.
- dependencies_and_callers: Targets `@oh-my-pi/pi-utils/prompt`, used by static prompt imports across coding-agent and commit tools.
- edge_cases_or_failure_modes: Symbol replacement inside comments/code, ellipsis grouping, XML blank stripping, triple brace ambiguity, non-array join.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1561 `file` `python/robomp/src/manual_triage.py`
- cursor: `[_]`
- core_role: Manual issue triage enqueue helper for robomp.
- algorithmic_behavior: Parses issue references/URLs, builds stable manual delivery IDs, fetches GitHub issue/repo payload, rejects PRs, inserts/replaces inactive events in DB, detects active conflicts, and waits for terminal event state with timeout polling.
- inputs_outputs_state: Inputs are issue refs, `Database`, `GitHubBackend`, issue number/repo, timeout/poll interval; outputs are delivery IDs, queued DB events, terminal `EventRow`/None, or typed exceptions.
- gates_or_invariants: Accepted refs must be `owner/repo#NN` or GitHub issue URLs; PR payloads are rejected; queued/running existing manual events conflict; inactive events can be replaced; terminal states are `done/failed/skipped`.
- dependencies_and_callers: Depends on robomp DB and GitHub backend; called by server trigger endpoints and tests.
- edge_cases_or_failure_modes: Invalid issue ref, repo not issue, active manual event, replace race, deleted row while waiting, timeout with current state.
- validation_or_tests: Covered by `python/robomp/tests/test_server.py` parse/ref/trigger/wait tests; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1591 `file` `python/robomp/tests/test_server.py`
- cursor: `[_]`
- core_role: End-to-end FastAPI/server regression suite for robomp dashboard, JSON APIs, webhooks, triggers, browse cache, and manual triage.
- algorithmic_behavior: Seeds DB fixtures, constructs FastAPI `TestClient`, mocks GitHub transports, signs webhook payloads, calls dashboard/API/trigger/webhook/browse endpoints, and asserts runtime counts, issue state, logs, rate limits, caching, and retry behavior.
- inputs_outputs_state: Inputs are test settings/env, SQLite DB rows, mocked GitHub issue/repo API responses, signed webhook bodies, replay tokens; outputs are HTTP responses, DB event/issue rows, cache states, and assertions.
- gates_or_invariants: Dashboard config token injection must not leak template marker; trigger requires replay token when enabled; repo allowlist enforced; active events conflict; PR issue payload rejected; rate limits vary by submitter association; browse cache honors forced refresh and webhook updates.
- dependencies_and_callers: Targets `robomp.server.create_app`, DB, GitHub client/backend, manual triage helpers, sandbox transport, FastAPI TestClient/httpx.
- edge_cases_or_failure_modes: Missing log file, garbage JSONL lines, unknown delivery retry, bad trigger mode, per-repo browse failure, cache hit recomputing processed flag, unknown PR comment directive.
- validation_or_tests: Pytest file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1621 `directory` `packages/coding-agent/src/export/html`
- cursor: `[_]`
- core_role: Standalone HTML export renderer assets for coding-agent transcripts/sessions.
- algorithmic_behavior: `index.ts` packages transcript/session data into `template.html` with `template.css`/`template.js`; browser-side JS loads shared data and uses vendored `marked`/`highlight` for markdown/code rendering.
- inputs_outputs_state: Inputs are transcript/export data, markdown/code content, static template assets; outputs are self-contained or share-loaded HTML export pages.
- gates_or_invariants: Vendor assets must be included for offline rendering; template paths must resolve in packaged/compiled builds; exported content must render without live CLI.
- dependencies_and_callers: Called by coding-agent export commands; depends on collab/tool render conventions and vendored browser libraries.
- edge_cases_or_failure_modes: Missing vendor assets, script/template mismatch, large transcript rendering, unsafe markdown rendering handled by client-side renderer constraints.
- validation_or_tests: No assigned direct test; package install smoke helps catch missing assets indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1651 `directory` `packages/collab-web/src/components/shell`
- cursor: `[_]`
- core_role: Collab web shell UI components for connection, composer, header, banners, toasts, and shell styling.
- algorithmic_behavior: React components render the collaborative host/guest shell, input composer, connection screen, status/header controls, notification banners/toasts, and CSS layout.
- inputs_outputs_state: Inputs are connection/session state, composer text/files/events, banners/toast data; outputs are React DOM and user interaction callbacks.
- gates_or_invariants: Shell components must keep host/guest workflow visible and avoid losing composer state; CSS controls responsive shell layout.
- dependencies_and_callers: Used by `packages/collab-web/src/app.tsx` and related client code.
- edge_cases_or_failure_modes: Disconnected state, empty composer, toast lifecycle, narrow viewport layout.
- validation_or_tests: Collab-web markdown test is assigned; no direct shell component test found in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1681 `file` `packages/agent/src/compaction/shake.ts`
- cursor: `[_]`
- core_role: Token-saving “shake” compaction algorithm for session entries.
- algorithmic_behavior: Collects shakeable regions from tool results and text blocks, scans fenced code/XML blocks, counts tokens, protects recent/protected tools, computes savings, and applies replacements in reverse order.
- inputs_outputs_state: Inputs are session entries, shake config, tool-call matchers, replacement text; outputs are `ShakeRegion` records and in-place modified session entries.
- gates_or_invariants: Useless non-error tool results can be replaced; code/XML block ranges are merged; minimum token/savings thresholds gate regions; protected/recent entries are skipped; block replacements preserve text slots.
- dependencies_and_callers: Depends on tokenizer, compaction entries, tool-call collection/protection helpers; called by agent compaction pipeline.
- edge_cases_or_failure_modes: Unclosed fences/XML tags, overlapping ranges, non-text content blocks, missing block slots, replacing multiple regions in same text.
- validation_or_tests: Compaction tests likely cover indirectly; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1711 `file` `packages/ai/src/dialect/index.ts`
- cursor: `[_]`
- core_role: Barrel export for AI dialect subsystem.
- algorithmic_behavior: Re-exports dialect catalog, coercion, examples, factory, history, inventory, owned-stream, rendering `renderDelimitedThinking`, and types.
- inputs_outputs_state: Inputs are module exports; output is public dialect API surface.
- gates_or_invariants: Consumers rely on stable export names; no runtime state.
- dependencies_and_callers: Used by stream markup healing, provider dialect rendering, and external callers.
- edge_cases_or_failure_modes: Missing export breaks imports.
- validation_or_tests: Type checks validate indirectly.
- skip_candidate: `yes: pure barrel export; no local algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1741 `file` `packages/ai/src/providers/google.ts`
- cursor: `[_]`
- core_role: Google Generative AI stream provider adapter.
- algorithmic_behavior: Defines `streamGoogle` that wraps shared Gemini streaming with Google Generative Language base URL, resolves `GEMINI_API_KEY`/options key, and builds URL/headers/fetch params.
- inputs_outputs_state: Inputs are model/context/options and API key; outputs are `AssistantMessageEventStream` from shared Gemini streaming.
- gates_or_invariants: Missing API key throws explicit Google Generative AI error; default base is `https://generativelanguage.googleapis.com/v1beta`; options fetch is passed through.
- dependencies_and_callers: Uses `getEnvApiKey` and `streamGeminiShared`.
- edge_cases_or_failure_modes: Missing key, invalid base URL handled downstream, fetch override.
- validation_or_tests: Provider tests likely indirect; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1771 `file` `packages/ai/src/registry/cerebras.ts`
- cursor: `[_]`
- core_role: Cerebras provider registry descriptor and API-key login helper.
- algorithmic_behavior: Creates an API-key login flow with Cerebras-specific instructions and exports provider definition metadata.
- inputs_outputs_state: Inputs are OAuth login callbacks/prompted API key; outputs are provider definition and stored API key credential.
- gates_or_invariants: API-key prompt must return nonempty key through shared `createApiKeyLogin`; provider ID must match registry expectations.
- dependencies_and_callers: Depends on `createApiKeyLogin`; used by provider registry/auth flows.
- edge_cases_or_failure_modes: Empty API key, noninteractive login, provider not registered.
- validation_or_tests: Registry/login tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1801 `file` `packages/ai/src/registry/openai-codex-device.ts`
- cursor: `[_]`
- core_role: OpenAI Codex device OAuth provider descriptor.
- algorithmic_behavior: Exports provider definition whose login and refresh handlers lazily load OpenAI Codex OAuth functions and delegate to device login/token refresh.
- inputs_outputs_state: Inputs are OAuth login callbacks or stored refresh credentials; outputs are OAuth credentials or refreshed credentials.
- gates_or_invariants: Login method is OAuth; refresh uses `credentials.refresh`; missing/failed dynamic module load or refresh propagates.
- dependencies_and_callers: Used by provider registry and AuthStorage OAuth flows.
- edge_cases_or_failure_modes: Missing refresh token, OAuth device login failure, lazy import failure.
- validation_or_tests: Auth/OAuth tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1831 `file` `packages/ai/src/usage/claude.ts`
- cursor: `[_]`
- core_role: Claude OAuth usage-report fetcher, parser, and ranking strategy.
- algorithmic_behavior: Normalizes Anthropic OAuth base URL, retries usage fetch on 429/5xx with Retry-After/backoff, parses 5h/7d/opus/sonnet buckets and rate-limit headers, fetches profile identity, builds usage limits/statuses, and ranks credentials by utilization/reset.
- inputs_outputs_state: Inputs are OAuth usage credentials, base URL, fetch/logger/signal context, response headers/payloads; outputs are `UsageReport`, parsed rate-limit reports, and ranking metrics.
- gates_or_invariants: Only Anthropic OAuth credentials are supported; missing usage data returns null; aborts return null; utilization must be numeric; reports include account metadata when available.
- dependencies_and_callers: Used by AuthStorage usage providers and credential ranking; depends on Anthropic provider version/header constants and usage types.
- edge_cases_or_failure_modes: Retryable status exhaustion, malformed payload, missing org/profile, abort signal, Retry-After date/seconds parsing.
- validation_or_tests: AuthStorage usage/rotation tests indirectly exercise usage ranking and limits; no direct assigned Claude usage test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1861 `file` `packages/ai/src/utils/stream-markup-healing.ts`
- cursor: `[_]`
- core_role: Heals leaked in-band tool/thinking markup from streaming model text.
- algorithmic_behavior: Wraps an in-band scanner for Kimi/DSML/thinking patterns, feeds text chunks, returns cleaned text or ordered text/thinking/tool-call events, collects synthesized tool calls, flushes remaining scanner state, and detects model/provider patterns requiring healing.
- inputs_outputs_state: Inputs are provider/model IDs and text chunks; outputs are cleaned text events, thinking deltas, `HealedToolCall` objects, completion flags, and pattern selection.
- gates_or_invariants: Tool-call IDs are synthesized with random IDs; `sectionTerminated` tracks Kimi section end; model pattern detection prioritizes thinking tags before Kimi/DSML.
- dependencies_and_callers: Uses catalog identity `isDeepseekModelIdOrName`, dialect scanner factory, and streaming providers.
- edge_cases_or_failure_modes: Partial chunks splitting tags/JSON, leaked DSML fullwidth/ASCII closing tags, MiniMax thinking tags, false-positive model ID matches.
- validation_or_tests: Stream/provider tests indirectly cover; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1891 `file` `packages/catalog/src/provider-models/index.ts`
- cursor: `[_]`
- core_role: Barrel export for provider-model descriptor/resolver modules.
- algorithmic_behavior: Re-exports descriptor types, descriptors, Google/Ollama/OpenAI-compatible/special provider model helpers.
- inputs_outputs_state: Inputs are module exports; output is public provider-model API surface.
- gates_or_invariants: Export paths must remain stable for generator/tests; no runtime logic.
- dependencies_and_callers: Used by catalog generator, model manager, provider-specific tests, and imports following repo convention.
- edge_cases_or_failure_modes: Missing export breaks resolver imports.
- validation_or_tests: Type checks and catalog tests validate indirectly.
- skip_candidate: `yes: pure barrel export; no local algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1921 `file` `packages/coding-agent/src/capability/mcp.ts`
- cursor: `[_]`
- core_role: Capability definition for MCP server declarations.
- algorithmic_behavior: Defines `MCPServer` schema-like interface and `mcpCapability` validator that checks required name, command/url presence, and transport-specific requirements.
- inputs_outputs_state: Inputs are MCP server capability records and source metadata; outputs are validation error string or success.
- gates_or_invariants: Server must have name; at least command or URL; `stdio` requires command; `http`/`sse` requires URL.
- dependencies_and_callers: Used by capability registry/discovery/plugin rules to ingest MCP server definitions.
- edge_cases_or_failure_modes: Missing transport with URL/command ambiguity, invalid stdio/http config.
- validation_or_tests: Covered indirectly by discovery/extensibility tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1951 `file` `packages/coding-agent/src/cli/plugin-cli.ts`
- cursor: `[_]`
- core_role: CLI command dispatcher for plugin marketplace/install/list/link/doctor/features/config/enable/disable workflows.
- algorithmic_behavior: Parses `plugin` argv into action/flags, routes to marketplace manager or plugin manager handlers, installs local/marketplace/npm plugins, upgrades/uninstalls/list/links, validates/fixes doctor checks, toggles features, reads/writes config, and emits JSON or human text.
- inputs_outputs_state: Inputs are CLI args/flags (`--json`, `--fix`, `--force`, `--dry-run`, `--local`, `--scope`, feature/config flags), plugin specs/paths, marketplace sources; outputs are console/JSON status, plugin registry changes, feature/config mutations.
- gates_or_invariants: Unknown action returns undefined/help path; scope limited to `user`/`project`; install requires specs; feature/config validation uses schema; doctor errors set nonzero process exit when unresolved.
- dependencies_and_callers: Uses `PluginManager`, MarketplaceManager, install target classifier, settings/theme helpers; called by coding-agent CLI.
- edge_cases_or_failure_modes: Empty args, invalid scope, plugin not installed, dry-run install, marketplace source missing, config validation failure, duplicate local link.
- validation_or_tests: Extensibility/marketplace tests cover plugin root substitution and plugin compatibility; no assigned direct CLI plugin test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1981 `file` `packages/coding-agent/src/commands/completions.ts`
- cursor: `[_]`
- core_role: CLI command generating shell completions.
- algorithmic_behavior: Validates shell arg (`bash`, `zsh`, `fish`), loads command constructors, builds completion spec, and prints generated completion script.
- inputs_outputs_state: Inputs are CLI config/args and registered commands; output is shell completion text.
- gates_or_invariants: Unsupported shell throws; root command is `launch`; command registry loading must succeed.
- dependencies_and_callers: Uses `@oh-my-pi/pi-utils/cli`, `completion-gen`, `cli-commands`.
- edge_cases_or_failure_modes: Missing shell arg, unknown shell, command constructor load failure.
- validation_or_tests: CLI completion behavior likely covered by command tests; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2011 `file` `packages/coding-agent/src/commit/shared-llm.ts`
- cursor: `[_]`
- core_role: Shared LLM tool schema/parser for conventional commit analysis.
- algorithmic_behavior: Builds ArkType tool schema for commit category/details, creates a conventional analysis tool definition, extracts tool call or text JSON from assistant message, parses payload, and normalizes analysis.
- inputs_outputs_state: Inputs are assistant messages and tool description strings; outputs are `ConventionalAnalysisTool` and normalized `ConventionalAnalysis`.
- gates_or_invariants: Tool-call payload is preferred when present; fallback parses text content as JSON; invalid payload surfaces via parser/normalizer.
- dependencies_and_callers: Used by commit analysis/generation flows; depends on pi-ai schema/tool validation and commit utils.
- edge_cases_or_failure_modes: Missing tool call, malformed JSON text, invalid category/detail shape.
- validation_or_tests: Commit tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2041 `file` `packages/coding-agent/src/debug/remote-debugger.ts`
- cursor: `[_]`
- core_role: JavaScriptCore remote debugger lifecycle helper.
- algorithmic_behavior: Reserves or validates a port, starts Bun JSC remote debugger, probes listening socket, memoizes active/starting debugger info, and exposes reset hook for tests.
- inputs_outputs_state: Inputs are optional host/port/start function; outputs are debugger host/port/URL info or errors.
- gates_or_invariants: Single active debugger reused; concurrent starts share `starting`; explicit port already in use errors before start; listener must come up within probe deadline.
- dependencies_and_callers: Uses `bun:jsc`, `node:net`; called by debug commands or runtime flags.
- edge_cases_or_failure_modes: Port race, debugger never listening, starter throws non-Error, concurrent start.
- validation_or_tests: Reset hook indicates test coverage exists; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2071 `file` `packages/coding-agent/src/edit/normalize.ts`
- cursor: `[_]`
- core_role: Text/indent normalization utilities for fuzzy edits.
- algorithmic_behavior: Counts leading whitespace, detects minimum indent/indent char/profile, normalizes Unicode punctuation, builds fuzzy comparison strings, converts tab indent to spaces when actual file differs, computes uniform indent deltas, and adjusts replacement indentation.
- inputs_outputs_state: Inputs are old/actual/new text blocks and lines; outputs are normalized strings or indentation-adjusted replacement text.
- gates_or_invariants: Mixed indentation or mismatched chars generally disable adjustment; indentation-only rewrites return unchanged; tab-to-space conversion only when old/new are tab-only and actual is space-only with consistent unit.
- dependencies_and_callers: Used by edit/write/patch fuzzy replacement paths; imports TUI padding helpers.
- edge_cases_or_failure_modes: Empty lines, Unicode confusables, mixed tabs/spaces, uniform whole-block indent shifts, actual file diverging from old text.
- validation_or_tests: Edit/ast-edit/fuzzy tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2101 `file` `packages/coding-agent/src/extensibility/typebox.ts`
- cursor: `[_]`
- core_role: TypeBox compatibility shim implemented on top of ArkType-like schemas.
- algorithmic_behavior: Creates schema objects with hidden validators/metadata, supports safeParse/toJSON, validates strings/numbers/arrays/tuples/objects/unions/intersections/records/literals/enums/formats/options, handles optional/nullable/additionalProperties, and emits JSON Schema-compatible objects.
- inputs_outputs_state: Inputs are schema builder calls and arbitrary data; outputs are schema objects, JSON schemas, safeParse success/failure, and validated data.
- gates_or_invariants: Validation failures are symbol-marked; object required keys derive from optional markers; `additionalProperties` can be false/true/schema; uniqueItems compares JSON values; formats include email/url/uuid/date/time/IP.
- dependencies_and_callers: Used by extension/plugin compatibility layer and tests; depends on `areJsonValuesEqual`.
- edge_cases_or_failure_modes: Empty union/intersection, enum numeric reverse mappings, record key validation, array uniqueness, schema metadata cloning, unsupported format pass-through.
- validation_or_tests: Assigned extensibility TypeBox shim/remap tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2131 `file` `packages/coding-agent/src/internal-urls/skill-protocol.ts`
- cursor: `[_]`
- core_role: Internal `skill://` URL resolver for active skills.
- algorithmic_behavior: Validates relative paths, resolves skill name and optional path against active skill base dir, checks file existence, returns content/path/type metadata, and completes available skill URLs.
- inputs_outputs_state: Inputs are parsed internal URL objects and active skill registry; outputs are `InternalResource` with content type/path/text or completion entries.
- gates_or_invariants: Skill name required; unknown skill errors with available list; absolute/path traversal disallowed; resolved path must stay under skill dir; missing file errors.
- dependencies_and_callers: Depends on `getActiveSkills` and internal URL protocol types; used by URL resolving/read paths.
- edge_cases_or_failure_modes: Encoded traversal, empty skill name, base-dir equality, non-markdown content type, unknown skills.
- validation_or_tests: Skill/internal URL tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2161 `file` `packages/coding-agent/src/mcp/smithery-auth.ts`
- cursor: `[_]`
- core_role: Smithery API key and CLI auth session helper.
- algorithmic_behavior: Creates/polls Smithery CLI auth sessions via `fetch`, normalizes API keys from env or `smithery.json`, saves/clears key under agent dir, and exposes login URL.
- inputs_outputs_state: Inputs are `SMITHERY_API_KEY`, `SMITHERY_URL`, agent-dir JSON file, session IDs; outputs are auth session JSON, poll response, API key string, saved/removed file.
- gates_or_invariants: Empty key rejected; 404/410 polling means expired session; ENOENT on key read/clear is nonfatal; failed read logs warning and returns undefined.
- dependencies_and_callers: Used by Smithery connect/registry MCP flows; depends on `getAgentDir`, logger, `isEnoent`.
- edge_cases_or_failure_modes: Expired auth session, file missing, malformed JSON, env key whitespace, fetch non-OK.
- validation_or_tests: MCP/Smithery flows likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2191 `file` `packages/coding-agent/src/modes/orchestrate.ts`
- cursor: `[_]`
- core_role: Orchestrate keyword detection/highlighting and notice import.
- algorithmic_behavior: Imports static orchestrate notice prompt, detects standalone `orchestrate` in prose using `keywordInProse`, and exports gradient highlighter config.
- inputs_outputs_state: Inputs are user text and static notice markdown; outputs are boolean detection and highlighter tokens.
- gates_or_invariants: Regex requires word boundaries/no adjacent nonspace; prose detection avoids code/markdown false positives through helper.
- dependencies_and_callers: Used by interactive mode or UI logic that reacts to “orchestrate”.
- edge_cases_or_failure_modes: Code blocks, punctuation, uppercase/lowercase behavior via regex/helper, substrings like “orchestrated”.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2221 `file` `packages/coding-agent/src/session/messages.ts`
- cursor: `[_]`
- core_role: Session message conversion/sanitization utilities and custom message type definitions.
- algorithmic_behavior: Defines special custom message types, abort labels, queue chip internal field stripping, steering-message wrapping via static prompt template, image stripping, bash/python execution text conversion, OpenAI responses history sanitization, and conversion of session messages to LLM messages.
- inputs_outputs_state: Inputs are agent/session messages, tool output metadata, file attachments, steering user messages, abort error strings; outputs are sanitized messages, LLM message array, text representations, and removed-image counts.
- gates_or_invariants: Excluded messages are dropped from context; steering wrapper only applies to trailing steering user messages; image blocks/files can be removed; OpenAI thinking signatures are stripped from rehydrated history.
- dependencies_and_callers: Used by `AgentSession`, session manager, model prompt construction, and UI transcript rendering; depends on pi-ai message types and prompt template.
- edge_cases_or_failure_modes: Mixed text/image content, file attachments with images, silent/user interrupt aborts, internal detail fields leaking, empty steering content.
- validation_or_tests: Agent-session and role/thinking tests exercise conversion indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2251 `file` `packages/coding-agent/src/ssh/utils.ts`
- cursor: `[_]`
- core_role: Small SSH string utility module.
- algorithmic_behavior: Sanitizes host names to filesystem/display-safe tokens and builds `user@host` targets when username is provided.
- inputs_outputs_state: Inputs are host names and optional username; outputs are sanitized host segment or SSH target string.
- gates_or_invariants: Empty sanitized host falls back to `remote`.
- dependencies_and_callers: Used by SSH tool/session code.
- edge_cases_or_failure_modes: Host names containing only unsafe chars, absent username.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2281 `file` `packages/coding-agent/src/tiny/text.ts`
- cursor: `[_]`
- core_role: Text preprocessing and normalization for tiny-model title generation.
- algorithmic_behavior: Truncates title input to 2,000 chars, strips fenced code blocks when enough prose remains, formats XML-wrapped user message, detects low-signal filler/numeric-only input, normalizes generated title first line, drops sentinel `none`, and title-cases output.
- inputs_outputs_state: Inputs are user messages and generated title strings; outputs are prompt-ready text or normalized title/null.
- gates_or_invariants: Code stripping requires minimum remaining chars; empty/filler messages are low-signal; sentinel `none` suppresses title.
- dependencies_and_callers: Used by tiny inference/title generation paths.
- edge_cases_or_failure_modes: Huge messages, all-code messages, unclosed fences, filler-only prompts, lowercase title casing with Unicode letters.
- validation_or_tests: Tiny title tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2311 `file` `packages/coding-agent/src/tools/gh-cache-invalidation.ts`
- cursor: `[_]`
- core_role: Detects mutating `gh issue/pr` shell commands and invalidates GitHub tool cache.
- algorithmic_behavior: Tokenizes shell command segments respecting quotes/escapes/separators, detects `gh issue|pr <mutating-subcmd>`, extracts issue/PR number and repo from args/URLs/`-R`, and calls invalidation by number or repo.
- inputs_outputs_state: Input is raw bash command string; output is cache invalidation side effect.
- gates_or_invariants: Only known mutating subcommands trigger; value-taking flags are skipped; nonpositive/non-safe numbers ignored; early return if command lacks `gh`.
- dependencies_and_callers: Depends on `github-cache` invalidation functions; called after bash commands.
- edge_cases_or_failure_modes: Quoted URLs, semicolon/pipeline segments, `--repo=`, issue/pr URLs, flags with values before target number.
- validation_or_tests: GitHub cache/tool tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2341 `file` `packages/coding-agent/src/tools/render-utils.ts`
- cursor: `[_]`
- core_role: Shared TUI rendering/sanitization utilities for coding-agent tool renderers.
- algorithmic_behavior: Resolves image preview sizes, caps/truncates preview lines, formats status icons/badges/meta/errors/code frames/diagnostics/diff stats/screenshots/parse errors, truncates diffs by hunks/context, shortens paths, creates cached components/rendered strings, and identifies LSP batch requests.
- inputs_outputs_state: Inputs are raw tool output/error/diff/diagnostic/paths/theme/render width/settings/tool-call context; outputs are sanitized strings/components/metadata and cached render results.
- gates_or_invariants: Error text is tab-replaced and width-truncated; previews obey `PREVIEW_LIMITS`/`TRUNCATE_LENGTHS`; diff truncation preserves change hunks; parse errors are deduped/capped; LSP batch only for edit/write with other writes.
- dependencies_and_callers: Used by most tool renderers; depends on pi-tui `replaceTabs`, `truncateToWidth`, settings, theme, image resize helpers.
- edge_cases_or_failure_modes: ANSI/tabs/long paths, huge diffs, malformed diagnostics, missing workdir, duplicate parse errors, cache invalidation.
- validation_or_tests: Assigned read renderer, bash clamp, tool memoization, and TUI sanitization-adjacent tests cover consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2371 `file` `packages/coding-agent/src/tui/index.ts`
- cursor: `[_]`
- core_role: Barrel export for coding-agent TUI helper components/utilities.
- algorithmic_behavior: Re-exports code-cell, file-list, hyperlink, output-block, status-line, tree-list, types, utils, and width-aware-text.
- inputs_outputs_state: Inputs are module exports; output is public internal TUI API surface.
- gates_or_invariants: Stable exports prevent import breakage; no runtime logic.
- dependencies_and_callers: Used by coding-agent modes/components/tools.
- edge_cases_or_failure_modes: Missing export path.
- validation_or_tests: Type checks indirect.
- skip_candidate: `yes: pure barrel export; no local algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2401 `file` `packages/coding-agent/src/utils/thinking-display.ts`
- cursor: `[_]`
- core_role: Canonicalization helper for thinking display messages.
- algorithmic_behavior: Trims text and returns empty string when content consists only of dots, ellipsis, spaces, tabs, or line breaks; otherwise returns trimmed text.
- inputs_outputs_state: Input is nullable text; output is canonical string.
- gates_or_invariants: Null/undefined/empty returns empty; punctuation-only ellipsis/dots are hidden.
- dependencies_and_callers: Used by ACP thinking/live message display.
- edge_cases_or_failure_modes: Unicode ellipsis, mixed whitespace, meaningful text with dots.
- validation_or_tests: ACP/message rendering tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2431 `file` `packages/coding-agent/src/workflow/run-store.ts`
- cursor: `[_]`
- core_role: Event-sourced workflow run persistence/reconstruction layer.
- algorithmic_behavior: Appends workflow custom entries for run start, state patch, graph patch proposal, activation start/completion/failure/abort; reconstructs runs by replaying valid events and applying state patches.
- inputs_outputs_state: Inputs are `WorkflowRunStoreHost`, definitions, graph revisions, patch operations, activation snapshots/outputs/errors; outputs are custom JSONL entries and reconstructed `WorkflowRunSnapshot` objects.
- gates_or_invariants: Run ID must be unique; event validation checks event type/runId and required fields; unknown/invalid custom entries are ignored; activation completion/failure/abort only update existing activations.
- dependencies_and_callers: Used by workflow scheduler/runner/session runtime; depends on workflow state patcher and session custom entries.
- edge_cases_or_failure_modes: Duplicate run start, missing activation start, invalid event data in transcript, graph patch actor validation, out-of-order events.
- validation_or_tests: Assigned reference-flow replicas and session immediate-persist tests exercise workflow events.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2461 `file` `packages/coding-agent/test/core/js-workflow-helpers.test.ts`
- cursor: `[_]`
- core_role: Tests JavaScript eval workflow helper APIs exposed in sandboxed execution.
- algorithmic_behavior: Runs JS snippets with `executeJs`, inspects status events, and asserts workflow logging/phase helpers and goal-token budget helper values.
- inputs_outputs_state: Inputs are code snippets, fake `ToolSession`, session file, optional goal state/usage; outputs are JS result exit code/output and workflow status events.
- gates_or_invariants: Helpers must log workflow events with correct payload; goal budget helper returns configured budget/used/remaining; inactive goal falls back to session output tokens/no ceiling.
- dependencies_and_callers: Targets JS executor/context manager and workflow helper injection.
- edge_cases_or_failure_modes: Goal mode inactive, budget absent, session usage fallback, VM context disposal.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2491 `file` `packages/coding-agent/test/discovery/builtin-defaults.test.ts`
- cursor: `[_]`
- core_role: Tests built-in default rule provider and TTSR matching behavior.
- algorithmic_behavior: Loads built-in rules, asserts provider source/unique names/conditions/scopes/interrupt modes, adds selected rules to `TtsrManager`, and matches snippets/tool contexts.
- inputs_outputs_state: Inputs are built-in rules, file paths, snippets, and tool source contexts; outputs are matched rule names and provider priority assertions.
- gates_or_invariants: Every rule needs condition or astCondition and scope; provider IDs must match built-in defaults; AST conditions must match intended TypeScript snippets only.
- dependencies_and_callers: Targets capability/rule discovery and TTSR manager.
- edge_cases_or_failure_modes: Duplicate rules, missing scope, false-positive AST match, provider priority ordering.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2521 `file` `packages/coding-agent/test/goals/goal-mode-integration.test.ts`
- cursor: `[_]`
- core_role: Integration tests for interactive goal mode lifecycle and tool exposure.
- algorithmic_behavior: Builds `InteractiveMode`/`AgentSession` harness, toggles goal mode, sets/replaces goals, simulates streaming guards, adjusts budgets, pauses/resumes, completes via goal tool, and asserts state/tool list/session events.
- inputs_outputs_state: Inputs are slash commands/menu selections, streaming state, goal objectives/budgets, goal tool calls; outputs are goal state, warnings/status messages, active tool names, and custom session entries.
- gates_or_invariants: Goal tool is exposed only while active; goal and plan modes are mutually exclusive; streaming defers input submission; paused goals reject new objectives/budget adjustment; completion exits before next tool rebuild.
- dependencies_and_callers: Targets goal tool/runtime, InteractiveMode, AgentSession, createTools, SessionManager.
- edge_cases_or_failure_modes: Continuation tick during streaming, paused goal mutation, completion state cleanup race, preserving usage when changing budget.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2551 `file` `packages/coding-agent/test/marketplace/substitute-plugin-root.test.ts`
- cursor: `[_]`
- core_role: Tests plugin-root placeholder substitution.
- algorithmic_behavior: Calls `substitutePluginRoot` on strings, arrays, objects, nested structures, primitives, and no-var inputs.
- inputs_outputs_state: Inputs contain `${CLAUDE_PLUGIN_ROOT}` and `${OMP_PLUGIN_ROOT}` placeholders plus root path; outputs are recursively substituted values.
- gates_or_invariants: Both placeholder names map to same plugin root; primitives/null/undefined pass through; no-var string unchanged.
- dependencies_and_callers: Targets discovery marketplace/plugin config substitution.
- edge_cases_or_failure_modes: Nested arrays/objects, multiple placeholders in one string, unsupported value types.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2581 `file` `packages/coding-agent/test/session/blob-store.test.ts`
- cursor: `[_]`
- core_role: Tests image blob storage and display-path behavior.
- algorithmic_behavior: Stores image bytes, asserts content hash/ref/path/display extension, reads stored bytes, resolves image data, and checks MIME extension mapping.
- inputs_outputs_state: Inputs are image bytes and MIME types; outputs are blob hash/path/displayPath/ref/base64 data.
- gates_or_invariants: Raw blob path ends with hash; display path adds extension; unsupported MIME returns undefined extension; stored/display bytes match original.
- dependencies_and_callers: Targets session `BlobStore` and image resolution helpers.
- edge_cases_or_failure_modes: MIME unknown, duplicate content hash, display extension mismatch.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2611 `file` `packages/coding-agent/test/task/commands.test.ts`
- cursor: `[_]`
- core_role: Tests workflow command `$@` expansion.
- algorithmic_behavior: Builds command object and calls `expandCommand` with normal and shell-special input.
- inputs_outputs_state: Inputs are instruction template strings and user argument text; outputs are expanded command text.
- gates_or_invariants: `$@` placeholders are replaced exactly; shell metacharacters in argument are not shell-expanded/escaped by this helper.
- dependencies_and_callers: Targets task command expansion.
- edge_cases_or_failure_modes: Multiple placeholders, argument containing `$`, `&`, quotes, backticks.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2641 `file` `packages/coding-agent/test/tools/ast-edit.test.ts`
- cursor: `[_]`
- core_role: Tests `ast_edit` schema, preview/apply flow, stale preview detection, glob scoping, and fallback parsing.
- algorithmic_behavior: Creates tools, inspects wire schema/strict adaptation, executes `ast_edit` with temp files, queues preview actions, applies replacements, mutates files to force staleness, and asserts output/diff/details.
- inputs_outputs_state: Inputs are TS/TLA+ files, AST pattern/replacement ops, source globs, preview queue choices; outputs are tool results, details metadata, queued pending action, and file contents.
- gates_or_invariants: Schema hides preview and requires `pat/out`; preview must not apply; apply requires matching preview; stale preview applies nothing; globs restrict source dir and ignore outside/JS files.
- dependencies_and_callers: Targets createTools `ast_edit`, ToolChoiceQueue, schema adaptation, filesystem.
- edge_cases_or_failure_modes: Line-number padding, stale content hash, multiple files, parse errors, TLA+ fallback.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2671 `file` `packages/coding-agent/test/tools/fetch-url-selectors.test.ts`
- cursor: `[_]`
- core_role: Tests URL target selector parser for fetch/read URL syntax.
- algorithmic_behavior: Calls `parseReadUrlTarget` with local paths, normal URLs, raw/range suffixes, ports, invalid selectors, and malformed single-slash URLs.
- inputs_outputs_state: Inputs are target strings; outputs are parsed URL/range/raw objects, null, or thrown errors.
- gates_or_invariants: Local/relative paths return null; raw/range suffixes can appear in either order; multiple range groups throw; URL ports are not mistaken for line selectors.
- dependencies_and_callers: Targets fetch tool URL parser.
- edge_cases_or_failure_modes: `:raw:1-120`, `:1-120:raw`, port `:8080`, `:abc`, malformed `https:/`.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2701 `file` `packages/coding-agent/test/tools/read-renderer.test.ts`
- cursor: `[_]`
- core_role: Tests read tool renderer hyperlinks and framing.
- algorithmic_behavior: Renders read call/result components, extracts terminal hyperlinks/text, and asserts local/file/HTTP link URIs plus standard tool container padding.
- inputs_outputs_state: Inputs are read result/call args, file paths, line ranges, fetch metadata, theme/settings; outputs are rendered ANSI/hyperlink strings.
- gates_or_invariants: Link text omits line suffix while URI includes `?line=`; local scheme renders stable display; fetch result links final URL; framed results sit inside tool container borders.
- dependencies_and_callers: Targets `readToolRenderer`, `ToolExecutionComponent`, theme/settings.
- edge_cases_or_failure_modes: Local URL display, path with range, fetched final URL, ANSI/hyperlink extraction.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2731 `file` `packages/coding-agent/test/tools/windows-drive-alias.test.ts`
- cursor: `[_]`
- core_role: Tests Windows drive alias path normalization.
- algorithmic_behavior: Calls `normalizeWindowsDriveAliasPath` with `/c`, `/mnt/d/...`, invalid aliases, non-win32 platform, and backslash paths.
- inputs_outputs_state: Inputs are path strings and platform strings; outputs are normalized Windows paths or unchanged originals.
- gates_or_invariants: Only win32 forward-slash `/x` and `/mnt/x` forms map to drive paths; root/dev/mnt-without-drive/backslash paths remain unchanged.
- dependencies_and_callers: Targets path-utils used by tools on Windows.
- edge_cases_or_failure_modes: Uppercase drive letter, root alias, Linux platform, backslash false positives.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2761 `file` `packages/coding-agent/test/workflow/reference-flow-replicas.test.ts`
- cursor: `[_]`
- core_role: Integration replicas for workflow freeze/load/run/reconstruction behavior.
- algorithmic_behavior: Writes reference `.omhflow` workflows/prompts, freezes artifacts, loads/runs workflows with a host capturing events, checks node/edge/resource snapshots, activation counts/state, and prompt resolution using latest outputs.
- inputs_outputs_state: Inputs are generated workflow files, prompt files, mock runtime host results, captured run-store entries; outputs are frozen artifacts, scheduler activations, reconstructed run state, and resolved prompts.
- gates_or_invariants: Freeze captures expected nodes/resources; workflow activations follow graph conditions; review prompts use latest accepted output; no failed activation error expected.
- dependencies_and_callers: Targets workflow freeze/package-loader/prompt-source/runner/run-store.
- edge_cases_or_failure_modes: Iterative humanize rounds, KDA promotion decision, latest-output selection, graph conditions, temp cleanup.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2791 `file` `packages/mnemopi/src/core/chat-normalize.ts`
- cursor: `[_]`
- core_role: Chat text normalization/filter for memory extraction.
- algorithmic_behavior: Expands contractions, lowercases/ASCII-normalizes non-ASCII runs, strips edge punctuation, collapses repeated chars, drops filler-only/too-short messages, optionally adds implicit subjects for fragments, and computes extraction rate with dropped samples.
- inputs_outputs_state: Inputs are chat strings and `add_implicit_subjects` option; outputs are normalized string/null arrays and extraction-rate stats.
- gates_or_invariants: Empty/filler messages return null; one-word messages require length >5; two-word fragments can get `i am` prefix only for known starters.
- dependencies_and_callers: Used by Mnemopi extraction/memory ingestion.
- edge_cases_or_failure_modes: Non-ASCII text replaced by spaces, repeated character spam, contractions, short fragments, punctuation-only input.
- validation_or_tests: Text/extraction tests likely cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2821 `file` `packages/mnemopi/src/core/veracity-consolidation.ts`
- cursor: `[_]`
- core_role: Knowledge fact consolidation, veracity aggregation, confidence update, and conflict resolution engine.
- algorithmic_behavior: Computes stable fact IDs from subject/predicate/object, clamps/aggregates veracity by weighted majority, initializes SQLite tables, serializes nested writes, consolidates incoming facts by updating confidence/sources or inserting new rows, records contradictions, resolves conflicts, summarizes high-confidence facts, and exposes stats.
- inputs_outputs_state: Inputs are facts, veracity/source/confidence, SQLite connection/path, conflict decisions; outputs are consolidated fact rows, conflict rows, summaries, stats, and DB mutations.
- gates_or_invariants: Fact ID inputs must be nonempty strings; invalid veracity logs/clamps to unknown; transaction nesting is tracked; conflict resolution ignores already-resolved conflicts; confidence capped at 1.0.
- dependencies_and_callers: Depends on `bun:sqlite`, `openDatabase`, Node crypto; used by memory/triples consolidation.
- edge_cases_or_failure_modes: DB already in transaction, invalid veracity, duplicate sources, conflicting facts, resolving with unrelated winning ID, unknown subject summary.
- validation_or_tests: `packages/mnemopi/test/veracity-consolidation.test.ts` and conflict/concurrency tests cover; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2851 `file` `packages/tui/src/components/scroll-view.ts`
- cursor: `[_]`
- core_role: Scrollable viewport component with keyboard scrolling and optional scrollbar.
- algorithmic_behavior: Maintains lines/height/scroll offset/total rows, clamps offset, handles up/down/page/home/end keys, truncates/replaces tabs per line, and renders a track/thumb scrollbar when needed.
- inputs_outputs_state: Inputs are line arrays, viewport height/width, scrollbar options/theme, key data; outputs are rendered visible lines and updated scroll offset.
- gates_or_invariants: Offset clamped to max; height zero renders empty; scrollbar mode normalizes boolean/auto/always/never; glyphs must be width 1 or fallback.
- dependencies_and_callers: Used by TUI selectors/panels; depends on key matcher and text width/truncation utils.
- edge_cases_or_failure_modes: Total rows differing from line count, narrow width with scrollbar, invalid glyph width, page scroll boundaries.
- validation_or_tests: Session selector viewport and TUI tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2881 `directory` `packages/coding-agent/src/commit/agentic/tools`
- cursor: `[_]`
- core_role: Tool suite for agentic commit analysis, changelog proposal, conventional commit proposal, and split commit planning.
- algorithmic_behavior: Provides git overview/diff/hunk/recent-commit tools, task-based file analysis, changelog proposal validation, commit proposal validation, and split-commit grouping/dependency validation; `index.ts` assembles tools based on options.
- inputs_outputs_state: Inputs are cwd, staged file lists, git diffs/hunks/numstat, model registry/auth/settings, commit/changelog params; outputs are markdown summaries, cached diffs, file observations, validated proposals, warnings/errors, and split commit plans.
- gates_or_invariants: Binary/lock files are deprioritized/excluded; diff output is token/line capped; changelog paths must be target/unique; commit analysis validates type/scope/details; split commits must cover staged files exactly once and dependencies must be acyclic/valid.
- dependencies_and_callers: Used by commit agentic mode; depends on git utils, commit analysis validators, TaskTool, prompt templates, and custom tool framework.
- edge_cases_or_failure_modes: Huge diffs, binary files, missing diff cache, duplicate changelog path, invalid hunk selectors, dependency cycles, unstaged/unknown files.
- validation_or_tests: Commit/agentic tests likely cover; no assigned direct directory test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2911 `file` `crates/pi-shell/src/minimizer/filters/gt.rs`
- cursor: `[_]`
- core_role: `gt` command output minimizer filter.
- algorithmic_behavior: Supports specific `gt` subcommands, parses command output, drops noisy lines, keeps actionable summaries/errors/status information, and returns `MinimizerOutput` with compacted content.
- inputs_outputs_state: Inputs are minimizer context, raw stdout/stderr text, and exit code; output is minimized shell output.
- gates_or_invariants: Filter only applies to supported `gt` invocations; failure output preserves diagnostics more aggressively than success output.
- dependencies_and_callers: Called by `crates/pi-shell/src/minimizer/filters/mod.rs` through minimizer engine; depends on primitives and context.
- edge_cases_or_failure_modes: Unrecognized subcommand, localized/noisy output, command failure requiring full context, empty output.
- validation_or_tests: Rust minimizer filter tests/fixtures cover adjacent filters; no direct execution here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2941 `file` `packages/ai/src/registry/oauth/pkce.ts`
- cursor: `[_]`
- core_role: PKCE verifier/challenge generator for OAuth flows.
- algorithmic_behavior: Generates random verifier bytes, base64url encodes them, computes SHA-256 digest with WebCrypto, and returns verifier plus S256 challenge.
- inputs_outputs_state: Input is none; output is `{ verifier, challenge }`.
- gates_or_invariants: Challenge is SHA-256 over verifier and base64url encoded; verifier randomness comes from `crypto.getRandomValues`.
- dependencies_and_callers: Used by OAuth login flows in provider registry.
- edge_cases_or_failure_modes: WebCrypto unavailable, base64url encoding compatibility.
- validation_or_tests: OAuth flow tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2971 `file` `packages/coding-agent/src/cli/gallery-fixtures/agentic.ts`
- cursor: `[_]`
- core_role: Static gallery fixture data for agentic UI/tool rendering examples.
- algorithmic_behavior: Defines sample usage objects and `agenticFixtures` records containing representative tool calls/results/transcript states for gallery rendering.
- inputs_outputs_state: Inputs are static fixture constants; outputs are fixture objects consumed by gallery CLI/UI.
- gates_or_invariants: Fixture shapes must match `GalleryFixture` and tool detail types.
- dependencies_and_callers: Imported by gallery fixture index/CLI tooling; depends on task/IRC detail types.
- edge_cases_or_failure_modes: Fixture drift from renderer detail schema, stale usage fields.
- validation_or_tests: Gallery/build checks indirectly validate shape.
- skip_candidate: `yes: static fixture data; no runtime algorithm beyond object construction`

### OH_MY_HUMANIZE_MAIN-HZ-3001 `file` `packages/coding-agent/src/commit/map-reduce/map-phase.ts`
- cursor: `[_]`
- core_role: Map phase for commit map-reduce file observation.
- algorithmic_behavior: Filters excluded files, concurrently processes diffs with bounded concurrency, skips binary files with placeholder observations, builds context headers, truncates diffs to token limit, calls LLM with static prompts and reasoning effort, retries failed calls, parses up to five observation lines, and returns per-file observations.
- inputs_outputs_state: Inputs are model/API key/context files/diffs/thinking level/fetch/auth/session; outputs are `FileObservation` records with observations/errors/truncated diff markers.
- gates_or_invariants: Max file tokens 50k, context files 20, concurrency 5, timeout 120s, retries 3; excluded files are omitted; binary files do not call LLM.
- dependencies_and_callers: Used by commit map-reduce pipeline; depends on `completeSimple`, static prompts, token truncation, exclusions.
- edge_cases_or_failure_modes: LLM timeout/failure, malformed/no observations, large commits, huge diff truncation, retry exhaustion.
- validation_or_tests: Commit map-reduce tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3031 `file` `packages/coding-agent/src/eval/js/worker-core.ts`
- cursor: `[_]`
- core_role: Core runtime for JS evaluation worker transport.
- algorithmic_behavior: Handles inbound run/tool-reply/close messages, lazily creates `JsRuntime` with tool-call hooks, tracks active runs and pending tool calls, posts results/errors/tool requests, delivers tool replies, and rejects pending calls on close/dispose.
- inputs_outputs_state: Inputs are worker protocol messages, JS code, filename, session snapshot, tool replies; outputs are transport frames for run result/error/tool call and rejected promises.
- gates_or_invariants: Runtime snapshot initialized once; pending tool calls are keyed by generated IDs; close rejects all pending calls; error payloads preserve name/stack.
- dependencies_and_callers: Used by eval JS worker host; depends on `JsRuntime`, worker protocol types, `ToolError`.
- edge_cases_or_failure_modes: Tool reply for unknown ID, run throwing, worker close during pending tool call, multiple concurrent runs.
- validation_or_tests: Assigned JS workflow helper tests exercise eval worker behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3061 `file` `packages/coding-agent/src/extensibility/extensions/wrapper.ts`
- cursor: `[_]`
- core_role: Wraps registered/extension tools with approval checks and extension lifecycle hooks.
- algorithmic_behavior: Adapts registered tool definitions to `AgentTool`, proxies render/execute calls, enforces approval prompts, runs extension `tool_call` handlers that can block, executes the underlying tool, then runs `tool_result` handlers that can modify content/details or clear/raise errors.
- inputs_outputs_state: Inputs are tool definitions, params, signal/update callback, runner context, settings/approval mode; outputs are `AgentToolResult`, modified result, or thrown denial/block errors.
- gates_or_invariants: Approval-required tools need UI handlers unless runner lacks UI; denied approval throws; blocking handler reason surfaces; result handlers can only clear errors by returning `isError:false`.
- dependencies_and_callers: Used by extension manager/tool registry; depends on approval logic, tool proxy, extension runner.
- edge_cases_or_failure_modes: Extension handler throws, no UI for approval, approval signal abort, tool execution error then result handler modifies, malformed handler result.
- validation_or_tests: Extensibility tests cover plugin/wrapper compatibility indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3091 `file` `packages/coding-agent/src/modes/acp/acp-agent.ts`
- cursor: `[_]`
- core_role: Agent Client Protocol server-side adapter for coding-agent sessions.
- algorithmic_behavior: Implements ACP initialize/auth/session lifecycle/prompt/cancel/config/mode/ext methods, manages sessions by ID/cwd, queues prompt turns, maps session events to ACP updates, handles skill/builtin slash commands, plan approval resolution, MCP servers, plugin reload, available commands, thinking/model config options, and async delivery drain/cancel cleanup.
- inputs_outputs_state: Inputs are ACP requests, prompt blocks/images, cwd/session IDs, MCP servers, config changes, slash command text, client form capabilities; outputs are ACP responses/notifications/session updates/tool updates/config updates and coding-agent session state changes.
- gates_or_invariants: Cwd must be absolute and match loaded session; prompt queue serializes turns; closed sessions throw lifecycle error; plan mode config must be available; model/thinking IDs must resolve; cancel cleanup has timeout; malformed ext methods throw.
- dependencies_and_callers: Depends on ACP SDK types/connection, `AgentSession`, `SessionManager`, MCP manager, settings, extension loading, skills, slash commands, plan mode, workflow runtime.
- edge_cases_or_failure_modes: Prompt while streaming, session close during prompt, fork/load unavailable while prompt in progress, stale bootstrap update, client lacking form support, local plan file missing, cancellation races.
- validation_or_tests: Assigned ACP permission tests and goal/mode tests cover portions; no full ACP test run here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3121 `file` `packages/coding-agent/src/modes/components/hook-editor.ts`
- cursor: `[_]`
- core_role: TUI editor component for hook/prompt text input.
- algorithmic_behavior: Wraps an editor inside a dynamic border, handles prompt-style vs hook-style key behavior, submits on Enter/Ctrl+Enter depending mode, supports paste, cancel, and opening external editor with current text.
- inputs_outputs_state: Inputs are prefill/options/TUI/key data/pasted text/external editor result; outputs are editor state changes, submit/cancel callbacks, and rerenders.
- gates_or_invariants: Prompt style Enter submits; hook style Ctrl+Enter submits and Enter inserts newline; interrupt cancels; external editor only opens when configured and result non-null.
- dependencies_and_callers: Used by interactive hook editors; depends on pi-tui Editor/Container, keybinding matchers, external-editor utility.
- edge_cases_or_failure_modes: Ctrl+Enter encoding variants, absent editor command, external editor cancelled, prompt-style multiline constraints.
- validation_or_tests: Custom editor/keybinding tests cover nearby behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3151 `file` `packages/coding-agent/src/modes/components/thinking-selector.ts`
- cursor: `[_]`
- core_role: TUI selector for thinking effort levels.
- algorithmic_behavior: Builds `SelectList` items from available `Effort` values with metadata labels/descriptions, selects current index if present, and invokes select/cancel callbacks.
- inputs_outputs_state: Inputs are available efforts, current value, callbacks; outputs are selected effort or cancel callback.
- gates_or_invariants: Current index is selected only if found; values cast back to `Effort`.
- dependencies_and_callers: Used by interactive settings/model controls; depends on pi-tui `SelectList` and thinking metadata.
- edge_cases_or_failure_modes: Current value absent from available list, empty levels.
- validation_or_tests: Role/thinking tests indirectly cover selection choices.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3181 `file` `packages/coding-agent/src/modes/rpc/host-tools.ts`
- cursor: `[_]`
- core_role: RPC bridge for tools executed by an external host.
- algorithmic_behavior: Adapts host tool definitions to `AgentTool`, sends execution/cancel frames with unique IDs, tracks pending calls, resolves/rejects on result frames, forwards update frames, aborts on signal, and rejects all pending on shutdown.
- inputs_outputs_state: Inputs are host tool definitions, params, signals, result/update frames; outputs are RPC frames, partial updates, promises resolving to tool results, or abort errors.
- gates_or_invariants: Result/update frames must have `host_tool_*` type and valid result shape; unknown pending ID returns false; abort sends cancel and rejects once.
- dependencies_and_callers: Used by RPC mode client/server host-tool integration; depends on `Snowflake`, tool proxy.
- edge_cases_or_failure_modes: Host never replies, signal abort before/after request, duplicate result, update after completion, rejectAllPending on disconnect.
- validation_or_tests: RPC client tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3211 `file` `packages/coding-agent/src/slash-commands/helpers/usage-report.ts`
- cursor: `[_]`
- core_role: Formats OAuth/provider usage reports for slash-command output.
- algorithmic_behavior: Fetches usage reports from active provider, filters to active account, groups by provider, formats accounts/limits/amounts/reset durations/status bars/notes inside a code block, and falls back to no-report guidance.
- inputs_outputs_state: Inputs are slash command runtime, provider ID, active account identity, usage reports/limits; output is markdown text.
- gates_or_invariants: Only reports matching active account are rendered when identity available; saved reset duration only shown when positive; providers without fetcher return fallback.
- dependencies_and_callers: Used by slash command usage/account reporting; depends on usage format helpers and active account matcher.
- edge_cases_or_failure_modes: No provider/fetcher, empty reports, limits missing amounts, reset already elapsed, multiple accounts.
- validation_or_tests: Slash command tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3241 `file` `packages/coding-agent/src/web/scrapers/docs-rs.ts`
- cursor: `[_]`
- core_role: Special web scraper that renders `docs.rs` rustdoc JSON as compact markdown.
- algorithmic_behavior: Parses docs.rs URLs into crate/version/module/item targets, reads/writes rustdoc JSON cache, fetches gzipped rustdoc with byte cap/abort support, resolves modules/items/reexports, renders Rust types/signatures/generics/items/modules/impl methods/trait impls/variants into markdown result metadata.
- inputs_outputs_state: Inputs are docs.rs URL, fetch/loadPage result, cache dir, abort signal; outputs are `RenderResult` markdown with fetched/cache metadata or null.
- gates_or_invariants: Only `docs.rs` URLs with crate/version/module shape accepted; `crate` pages ignored; download capped by `MAX_BYTES`; cache path segments sanitized; traversal through module path must find items.
- dependencies_and_callers: Used by web fetch/scraper pipeline; depends on `gunzipSync`, docs cache dir, logger, `buildResult`.
- edge_cases_or_failure_modes: Missing rustdoc JSON, cache corruption, large downloads, reexports, restricted visibility, complex Rust type JSON, item not found.
- validation_or_tests: Web scraper tests likely indirect; no assigned direct docs-rs test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3271 `file` `packages/coding-agent/src/web/scrapers/osv.ts`
- cursor: `[_]`
- core_role: Special web scraper for OSV vulnerability pages.
- algorithmic_behavior: Recognizes `osv.dev/vulnerability/<id>` URLs, fetches JSON, formats summary/aliases/dates/severity/details/affected ranges/versions/references/credits into markdown, and returns scraper result metadata.
- inputs_outputs_state: Inputs are OSV URL and fetch/loadPage result; outputs are markdown vulnerability report or null.
- gates_or_invariants: Host/path must match OSV vulnerability route; non-OK or unparsable JSON returns null; ISO dates formatted; empty sections omitted.
- dependencies_and_callers: Used by web fetch/scraper pipeline; depends on scraper types and `tryParseJson`.
- edge_cases_or_failure_modes: Missing fields, withdrawn vulnerabilities, multiple affected packages/ranges, malformed API JSON.
- validation_or_tests: Web scraper tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3301 `file` `packages/coding-agent/src/web/search/index.ts`
- cursor: `[_]`
- core_role: Web search tool/custom tool orchestration across provider chain.
- algorithmic_behavior: Defines search schema, resolves provider chain, executes providers in order with abort checks, formats provider errors, rejects empty renderable content, converts search responses to LLM text, renders call/result, and exposes CLI/custom tool entry points.
- inputs_outputs_state: Inputs are query/num_results/provider/auth/session/signal; outputs are tool result content/details, CLI search text, or provider error summaries.
- gates_or_invariants: No configured providers returns error result; auth/HTTP errors are formatted by provider; abort is checked between providers; response must include answer/sources/citations/related questions/search queries.
- dependencies_and_callers: Used by `web_search` tool, custom tool registry, CLI search; depends on provider registry, settings, auth discovery, prompt text, renderers.
- edge_cases_or_failure_modes: Provider unavailable, 401/403 auth failure, Anthropic 404 special case, all providers fail, provider returns empty content.
- validation_or_tests: Assigned Perplexity web search tests and Gemini provider file cover provider behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3331 `file` `packages/coding-agent/test/modes/components/session-selector-viewport.test.ts`
- cursor: `[_]`
- core_role: Tests session selector rendering stays within terminal viewport.
- algorithmic_behavior: Builds titled session lists and `SessionSelectorComponent` with row getters, renders at different row counts, and counts visible entries.
- inputs_outputs_state: Inputs are fake sessions and viewport row counts; outputs are rendered line arrays.
- gates_or_invariants: Rendered lines must never exceed terminal rows; at least two entries visible; larger viewport shows more entries; missing row getter defaults safely.
- dependencies_and_callers: Targets session selector component and theme.
- edge_cases_or_failure_modes: Multiline titled sessions, `/resume` overflow, no viewport getter.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3361 `file` `packages/coding-agent/test/modes/controllers/selector-controller-logout.test.ts`
- cursor: `[_]`
- core_role: Tests logout account selector controller behavior.
- algorithmic_behavior: Creates test selector/editor container, fake stored credentials, invokes selector flow, and asserts `removeCredential`, `refresh`, error/present calls, and remaining credential list.
- inputs_outputs_state: Inputs are stored OAuth credential rows, selected account, mocked auth storage; outputs are credential deletion call, refreshed UI state, and present/error callbacks.
- gates_or_invariants: Selected credential ID/provider must be removed; refresh must run; UI should present next state and not show error.
- dependencies_and_callers: Targets `SelectorController`, `LogoutAccountSelectorComponent`, AuthStorage interface.
- edge_cases_or_failure_modes: Multiple accounts, selected row removal, failed removeCredential path likely elsewhere.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3391 `file` `packages/coding-agent/test/web/search/perplexity.test.ts`
- cursor: `[_]`
- core_role: Tests Perplexity web search request/response behavior across API key, OAuth, and anonymous modes.
- algorithmic_behavior: Mocks Perplexity chat/responses/OAuth/anonymous endpoints, captures bodies/headers, calls `searchPerplexity`, and asserts request shape, fallback URLs, related questions, response parsing, auth mode, and provider availability.
- inputs_outputs_state: Inputs are query/options/authStorage mocks/fetch mocks/SSE events; outputs are captured request bodies/headers and `SearchResponse`.
- gates_or_invariants: API-key mode sets pro search options and fallback via OpenRouter; responses API uses max output/source mapping; OAuth uses cookie not authorization; anonymous uses browser UA and no auth/cookie; explicit availability differs from normal availability.
- dependencies_and_callers: Targets Perplexity provider and search orchestration.
- edge_cases_or_failure_modes: Fallback after API failure, related questions absent/present, no auth, OAuth token source, anonymous source/citation parsing.
- validation_or_tests: Bun test file; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3421 `file` `packages/collab-web/src/tool-render/tools/lsp.tsx`
- cursor: `[_]`
- core_role: React renderer for LSP tool calls/results in collab-web.
- algorithmic_behavior: Parses diagnostics and locations with regexes, maps severity to tone, renders summary args and body rows with capped row count, badges, paths, positions, and normalized messages.
- inputs_outputs_state: Inputs are tool args/result text/details; outputs are React nodes for summary/body.
- gates_or_invariants: Diagnostic format requires `file:line:col [severity] message`; locations require `file:line:col`; max rows capped at 24; invalid args render as `InvalidArg`.
- dependencies_and_callers: Used by collab-web tool renderer registry; depends on shared render parts/utilities.
- edge_cases_or_failure_modes: Nonmatching result text, too many diagnostics/locations, unknown severity, missing args.
- validation_or_tests: Tool renderer build/tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3451 `file` `packages/stats/src/client/app/RangeControl.tsx`
- cursor: `[_]`
- core_role: Stats dashboard time-range selector UI component.
- algorithmic_behavior: Renders buttons for range options (`1h`, `24h`, `7d`, `30d`, `90d`, `all`) and calls `onChange` when user selects a range.
- inputs_outputs_state: Inputs are current `TimeRange`, `onChange`, optional className; output is React button group.
- gates_or_invariants: Active value gets selected class/aria state; options are fixed list.
- dependencies_and_callers: Used by stats dashboard top bar/layout.
- edge_cases_or_failure_modes: Unknown current range would render no selected option.
- validation_or_tests: UI behavior indirect.
- skip_candidate: `yes: simple presentational UI; minimal algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3481 `file` `packages/stats/src/client/ui/Skeleton.tsx`
- cursor: `[_]`
- core_role: Stats dashboard loading skeleton component.
- algorithmic_behavior: Builds inline style width/height and renders a div with variant/class data attributes.
- inputs_outputs_state: Inputs are variant/width/height/className props; output is React div.
- gates_or_invariants: Variant defaults to `text`; style only includes provided dimensions.
- dependencies_and_callers: Used by stats client async/loading states.
- edge_cases_or_failure_modes: Invalid CSS size prop passed by caller.
- validation_or_tests: UI build/type checks indirect.
- skip_candidate: `yes: presentational component; no core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3511 `file` `packages/coding-agent/src/commit/agentic/tools/propose-commit.ts`
- cursor: `[_]`
- core_role: Agentic commit tool for validating and storing a proposed conventional commit.
- algorithmic_behavior: Accepts commit type/scope/summary/body/details/files, normalizes details, gathers staged files, builds proposal response, validates analysis with commit validation helpers, updates commit agent state when valid, and returns validation errors/warnings/content.
- inputs_outputs_state: Inputs are proposed commit params and git staged files; outputs are valid/invalid response and state `proposedCommit`.
- gates_or_invariants: Proposed files must align with staged files through validation; summary/type/details are validated; state only updates when response valid.
- dependencies_and_callers: Used by commit agentic tool suite; depends on git utils and commit analysis validators.
- edge_cases_or_failure_modes: Invalid type/scope/summary, missing staged files, duplicate/unknown files, validation warnings.
- validation_or_tests: Commit agent tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3541 `file` `packages/coding-agent/src/modes/components/extensions/index.ts`
- cursor: `[_]`
- core_role: Barrel export for extension mode UI components.
- algorithmic_behavior: Re-exports extension dashboard, list, inspector panel, state manager, and types.
- inputs_outputs_state: Inputs are module exports; output is aggregated import surface.
- gates_or_invariants: Stable paths for UI imports; no runtime logic.
- dependencies_and_callers: Used by ACP/interactive extension UI code.
- edge_cases_or_failure_modes: Missing export path.
- validation_or_tests: Type/build checks indirect.
- skip_candidate: `yes: pure barrel export; no local algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3571 `file` `packages/coding-agent/src/web/search/providers/gemini.ts`
- cursor: `[_]`
- core_role: Gemini/Google OAuth-backed web search provider implementation.
- algorithmic_behavior: Finds Gemini OAuth access from `google-gemini-cli` or `google-antigravity`, builds Cloud Code API tools, selects endpoint/fallbacks, posts streaming SSE requests with retries/timeouts/rate-limit budget, parses text chunks, grounding sources/citations/search queries/usage/model version, trims results, and returns `SearchResponse`.
- inputs_outputs_state: Inputs are query/search/tool params, auth storage OAuth access/project ID, fetch implementation, endpoint mode, token limits/temperature; outputs are answer text, sources, citations, usage, search queries, provider ID/auth mode.
- gates_or_invariants: Requires OAuth access and project ID; Antigravity endpoint may fallback daily/sandbox; 429/5xx retry/fallback; no body throws provider error; result sources capped by `num_results`.
- dependencies_and_callers: Used by web search provider chain; depends on pi-ai `withOAuthAccess`, `fetchWithRetry`, provider error classification, timeout helpers.
- edge_cases_or_failure_modes: Missing OAuth, endpoint-specific failure, malformed SSE data, grounding chunk index mismatch, duplicate source URLs, rate limits.
- validation_or_tests: Web search tests likely cover provider registry; no assigned direct Gemini test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3601 `file` `packages/utils/src/vendor/mermaid-ascii/er/types.ts`
- cursor: `[_]`
- core_role: Type definitions for vendored Mermaid ER diagram parser/layout.
- algorithmic_behavior: Declares ER diagram entities, attributes, cardinality, relationships, and positioned layout shapes; no runtime code.
- inputs_outputs_state: Inputs are TypeScript consumers; outputs are compile-time types for ER parsing/rendering.
- gates_or_invariants: Cardinality union constrains legal relationship endpoints; positioned types add coordinates.
- dependencies_and_callers: Used by vendored ER parser and ASCII renderer.
- edge_cases_or_failure_modes: Type drift with parser output.
- validation_or_tests: Type checks indirect.
- skip_candidate: `yes: type-only vendored definitions; no executable algorithm`

## Worker Self-Test
- assigned_items_seen: `121 evidence headings were produced for 121 assigned rows`
- missing_items: `0`
- duplicate_items: `0`
- checklist_cursor_policy: `all item cursors use [_]; no item was marked as master-accepted`
- final_worker_status: `complete`