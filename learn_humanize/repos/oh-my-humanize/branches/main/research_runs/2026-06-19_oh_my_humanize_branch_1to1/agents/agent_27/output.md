# agent_27 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-027 `directory` `packages/catalog`
- cursor: `[_]`
- core_role: Model catalog package: normalizes bundled and discovered provider model metadata into typed `Model` records, provider descriptors, identity/canonicalization, thinking/effort policy, host/wire helpers, and generated catalog build assets.
- algorithmic_behavior: Recursive inspection found 96 files. Main flows are `buildModel`/`buildCompat` construction in `src/build.ts:18`, generated model loading in `src/models.ts`/`models.json`, provider descriptor/discovery orchestration in `src/provider-models/*`, identity parsing/canonical equivalence in `src/identity/*`, schema-free utility coercions in `src/utils.ts`, thinking metadata inference in `src/model-thinking.ts:142`, and generator post-processing in `scripts/generate-models.ts:432`.
- inputs_outputs_state: Inputs are provider descriptors, discovered `/models` payloads, OAuth/env credentials, bundled `models.json`, model IDs, compat overrides, and settings-supplied provider order. Outputs are typed `Model<Api>` entries, resolved compat config, canonical selections, provider discovery options, thinking effort maps, host matching results, and generated bundled JSON.
- gates_or_invariants: Generated `src/models.json` is not hand-edited; provider/catalog fixes live in descriptors/resolvers/generator. Catalog imports should remain via `@oh-my-pi/pi-catalog`. Invariants include model identity stability, provider priority ordering, nullable limit semantics, explicit compat merging, generated policy rebaking, and effort support clamping.
- dependencies_and_callers: Used by `packages/ai` and `packages/coding-agent` model registries/auth/discovery. Depends on bundled JSON, provider discovery modules, OpenAI-compatible resolvers, Google/Ollama/Special providers, wire helpers for Codex/Gemini/GitHub Copilot, and tests across `packages/catalog/test`.
- edge_cases_or_failure_modes: Provider discovery may return incomplete limits, wrapper IDs, dated variants, enterprise Copilot hosts, Vertex authoritative project catalogs, Ollama native metadata, unsupported effort tiers, duplicate aliases, or stale generated policies. The package handles canonical fallback, generated policy overrides, synthetic model suppression, and host-specific URL detection.
- validation_or_tests: Broad package tests cover descriptors, issue regressions, provider-specific discovery, identity family parsing, model thinking, variant collapse, Copilot wire headers, generated policies, host matching, and build behavior; assigned `issue-2105` and `build.ts` items are direct examples.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-057 `file` `docs/natives-addon-loader-runtime.md`
- cursor: `[_]`
- core_role: Runtime design document for `@oh-my-pi/pi-natives` addon loading, compiled-binary extraction, variant selection, candidate probing, and failure diagnostics.
- algorithmic_behavior: Defines derived loader state and platform tag/variant selection at `docs/natives-addon-loader-runtime.md:25`; candidate fallback ordering at `:92`; embedded addon extraction lifecycle at `:116`; and full state transition graph at `:149`.
- inputs_outputs_state: Inputs are platform/arch/libc, package version sentinel, explicit native override, AVX2 runtime detection, compiled-binary metadata, user data dir, embedded archive manifest, and package/native directory paths. Outputs are loaded native exports or structured startup errors listing attempted paths.
- gates_or_invariants: Install/compiled paths validate a release sentinel export; workspace-dev skips sentinel validation. Loader prefers modern x64 with baseline fallback, never validates full export surface, and keeps unsupported-platform reporting until all candidates fail.
- dependencies_and_callers: Documents `packages/natives/native/index.js`, `loader-state.js`, `embedded-addons.js`, and package-level binary embedding.
- edge_cases_or_failure_modes: Unsupported platform, missing embedded payload, bad archive extraction, stale same-version binary, AVX2 mismatch, user data dir fallback failure, candidate require errors, and sentinel mismatch all become diagnostics.
- validation_or_tests: Loader behavior is indirectly covered by native public-surface and compiled binary smoke tests; doc gives exact expected diagnostic surfaces.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-087 `file` `scripts/ci-macos-upload-secrets.sh`
- cursor: `[_]`
- core_role: Operational workflow script for validating and uploading macOS signing/notarization secrets to GitHub Actions without exposing secret values.
- algorithmic_behavior: Parses `[dir] [--dry-run]` and env overrides at `scripts/ci-macos-upload-secrets.sh:23`; enforces exactly one `.p12` and `.p8` via `find_one` at `:41`; reads/trims required secret files at `:49`; derives key id from `AuthKey_<KEYID>.p8` at `:63`; validates the certificate with a throwaway keychain at `:78`; uploads via stdin-only `gh secret set` at `:104`.
- inputs_outputs_state: Inputs are signing dir, `OMP_SIGNING_DIR`, `OMP_REPO`, `.p12`, password, `.p8`, issuer id, optional key id, local `security`, `openssl`, and `gh`. Output is GitHub Actions secret state plus non-secret status lines.
- gates_or_invariants: Fails on missing dir, ambiguous files, empty values, key id derivation failure, invalid p12/password/no Developer ID identity, non-PEM `.p8`, or dry-run mode. Secret bytes never appear in argv or logs.
- dependencies_and_callers: Depends on macOS `security`, `openssl rand`, POSIX shell, `find`, `grep`, `base64`, and GitHub CLI.
- edge_cases_or_failure_modes: Multiple files matching a glob, OpenSSL legacy PKCS12 incompatibility avoided by `security import`, temp keychain cleanup best-effort, and upload failures propagated by `set -euo pipefail`.
- validation_or_tests: Self-validates certificate import and PEM marker before upload; no repository test observed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-117 `file` `scripts/trace-loader.ts`
- cursor: `[_]`
- core_role: Bun preload diagnostic plugin that traces project-local module resolution timing.
- algorithmic_behavior: Captures start timestamp and a `Set` of resolved specifiers at `scripts/trace-loader.ts:6`; registers `Bun.plugin` at `:9`; `onResolve` logs unique non-`node_modules`/non-`node:` paths with elapsed ms and returns `undefined` so normal resolution continues.
- inputs_outputs_state: Input is Bun module resolution events from a preloaded process. Output is stderr trace lines and an in-memory dedupe set.
- gates_or_invariants: Does not alter module loading; only filters out `node_modules` and builtin modules. Duplicate specifiers are skipped by set membership.
- dependencies_and_callers: Used manually via `bun --preload ./scripts/trace-loader.ts <script>`.
- edge_cases_or_failure_modes: Dedupe is by raw `args.path`, so different specifier spellings for same file can both log; cwd replacement only shortens paths containing `process.cwd()`.
- validation_or_tests: No direct test found; behavior is observable through stderr.
- skip_candidate: `yes: diagnostic helper, not production runtime logic`

### OH_MY_HUMANIZE_MAIN-HZ-147 `directory` `packages/snapcompact/research`
- cursor: `[_]`
- core_role: Research suite for Snapcompact experiments, carrier rendering, visual explanation, benchmark execution, pricing/accuracy aggregation, activation/logit-lens diagnostics, and prompt variants.
- algorithmic_behavior: Recursive scan found Python/TS experiment drivers (`run.py`, `exp01`-`exp22`, provider adapters, bench scripts), visualization scripts (`snapcompact_*_viz.py`), data/render helpers (`bdf.py`, `squad.py`, `providers.py`), and prompt templates. Core repeated pattern: build or transform text corpus, render carrier images, call model APIs, parse answers, score SQuAD-style EM/F1, aggregate token/cost metrics, and emit JSON/PNG/HTML artifacts.
- inputs_outputs_state: Inputs include API keys, prompts under `prompts/`, cached datasets, experiment conditions, image/text carriers, model names, pricing constants, and cache/fresh flags. Outputs include cached completions, scored records, visualizations, CSV/JSON summaries, and generated images.
- gates_or_invariants: Many scripts use deterministic seeds, cache keys, atomic image saves, exact answer spans, chunk/page bounds, and prompt-specific parsing. External API calls are generally guarded by cache/fresh flags but not production-grade retry/security policy.
- dependencies_and_callers: Depends on Python PIL/numpy/http clients/model-specific APIs, Bun for TS render helpers, local prompts, and SQuAD utilities. It is not called by the main CLI runtime in inspected paths.
- edge_cases_or_failure_modes: API key absence, model output parse failures, image/font availability, invalid answer spans, cache poisoning/staleness, high-cost API runs, and visual scripts assuming prior experiment artifacts.
- validation_or_tests: Validation is experimental scoring/aggregation inside scripts, not package test assertions.
- skip_candidate: `yes: research workspace with algorithms, but not shipped runtime`

### OH_MY_HUMANIZE_MAIN-HZ-177 `file` `docs/toolconv/kimi-k2.md`
- cursor: `[_]`
- core_role: Architecture documentation for Kimi K2 in-band tool-calling format and parser/API mapping requirements.
- algorithmic_behavior: Defines special markers at `docs/toolconv/kimi-k2.md:7`, role/turn structure at `:31`, tool definition JSON format at `:49`, tool-call and result blocks at `:65` and `:97`, OpenAI-compatible mapping at `:139`, and parser gotchas at `:160`.
- inputs_outputs_state: Inputs are model transcript messages, tool definitions, parallel tool call sections, and OpenAI-compatible API payloads. Outputs are assistant tool call records and tool result messages encoded with Kimi marker tokens.
- gates_or_invariants: Tool calls are delimited by `<|tool_calls_section_*|>` style tokens; deployment must use native `kimi_k2` parser or manually parse markers if engine fallback forces `deepseek_v3`.
- dependencies_and_callers: Relates to AI dialect/tool conversion code and provider gateway behavior for Kimi K2.
- edge_cases_or_failure_modes: Multiple parallel calls, missing native parser in engine fallback, token marker leakage, and manual parser requirements for compatibility deployments.
- validation_or_tests: No direct test named here, but AI stream markup healing and dialect tests likely validate adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-207 `file` `docs/tools/write.md`
- cursor: `[_]`
- core_role: Contract documentation for the coding-agent `write` tool across filesystem, internal URL, archive, SQLite, and conflict-resolution variants.
- algorithmic_behavior: Inputs are specified at `docs/tools/write.md:17`, outputs at `:40`, flow at `:55`, mode-specific algorithms at `:80`, side effects at `:140`, limits at `:159`, and errors at `:166`.
- inputs_outputs_state: Inputs are `path`, content/row payloads, archive inner paths, SQLite table/key selectors, and conflict URLs. Outputs are `AgentToolResult` details, diff/edit metadata, conflict resolution status, or validation errors. State changes include filesystem writes, archive rewrites, database mutations, conflict registry updates, session/memory/job/checkpoint writes, and cache invalidation.
- gates_or_invariants: Delegates writable internal URLs first, applies plan-mode/write permissions, invalidates FS caches, uses structured row handling for SQLite, and rejects unsupported paths/modes.
- dependencies_and_callers: Documents `packages/coding-agent/src/tools/write.ts`, `archives.ts`, `sqlite.ts`, `conflicts.ts`, and `fs-cache-invalidation.ts`.
- edge_cases_or_failure_modes: Archive entry addressing, SQLite insert/update/delete distinctions, conflict bulk resolution, permissions, binary/large content, and unsupported internal protocols.
- validation_or_tests: Tool tests around write/read/archive/sqlite/conflict behavior are referenced by doc scope; not all assigned here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-237 `directory` `packages/ai/src/utils`
- cursor: `[_]`
- core_role: Shared AI runtime utility layer for request debugging, streaming, retries, schema conversion/strict validation, tool-argument coercion, auth/header helpers, overflow detection, stream markup healing, and provider response handling.
- algorithmic_behavior: Key child roles include request capture/redaction in `request-debug.ts:79`, abort racing in `abort.ts:20`, event stream wrappers in `event-stream.ts:4`, idle/first-event watchdogs in `idle-iterator.ts:26`, retry-after parsing in `retry-after.ts:5`, Copilot error rewriting in `http-inspector.ts:79`, tool-choice mapping in `tool-choice.ts:46`, validation/coercion in `validation.ts:1259`, thinking-loop detection in `thinking-loop.ts:107`, markup healing in `stream-markup-healing.ts:45`, JSON schema validation in `schema/json-schema-validator.ts:581`, schema normalization/strict enforcement in `schema/normalize.ts:877` and `:1441`, and wire schema extraction in `schema/wire.ts:474`.
- inputs_outputs_state: Inputs are model/provider metadata, HTTP responses/errors/headers, streamed events, tool schemas, Zod/Ark/JSON schemas, tool call args, abort signals, and env toggles. Outputs are normalized schemas, validated/coerced arguments, stream events, structured errors, sanitized debug files, retry decisions, and provider-compatible headers.
- gates_or_invariants: Sensitive headers are redacted; strict schemas must add required/all object keys or downgrade; recursion caps prevent infinite `$ref`; idle timers avoid hung streams; aborts propagate through iterators; unsupported provider schema keywords are stripped or reported.
- dependencies_and_callers: Called by provider implementations, stream functions, tool execution validation, auth registries, and coding-agent model flows. Uses `@oh-my-pi/pi-catalog`, `@ark/schema`, Zod, Bun/Fetch primitives, and central logger.
- edge_cases_or_failure_modes: Malformed JSON, numeric/boolean strings, nested JSON strings, unknown root fields, boolean schemas, unsupported regex/lookaround, recursive refs, stream stalls, rate-limit headers, provider-specific schema restrictions, and leaked in-band tool markers.
- validation_or_tests: Assigned `schema-strict-mode.test.ts`, `github-copilot-error.test.ts`, `anthropic-stream-envelope.test.ts`, `issue-1776`, and retry/header tests cover major contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-267 `directory` `packages/coding-agent/src/irc`
- cursor: `[_]`
- core_role: In-process IRC-style message bus for lightweight mailbox delivery inside coding-agent.
- algorithmic_behavior: `bus.ts` defines `IrcMessage`, `IrcDeliveryReceipt`, a `MAILBOX_CAP` of 100 at `packages/coding-agent/src/irc/bus.ts:47`, and `IrcBus` at `:49` for publishing/delivering queued messages.
- inputs_outputs_state: Inputs are channel/message payloads and subscriber/mailbox operations. Outputs are delivery receipts and retained mailbox messages capped per channel/target.
- gates_or_invariants: Mailbox cap prevents unbounded growth; message IDs/timestamps preserve ordering semantics.
- dependencies_and_callers: Self-contained coding-agent utility; callers are internal session/collab/event surfaces when IRC-style delivery is enabled.
- edge_cases_or_failure_modes: Overflow drops/evicts older messages; absent subscribers rely on mailbox retention; concurrent publication depends on JS single-threaded map mutation.
- validation_or_tests: No direct assigned test observed; behavior can be validated through bus delivery ordering and cap tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-297 `directory` `packages/coding-agent/test/discovery`
- cursor: `[_]`
- core_role: Discovery regression suite for rules, agents, skills, MCP configs, plugins, profiles, disabled providers/extensions, frontmatter parsing, config roots, and third-party surfaces.
- algorithmic_behavior: Recursively contains tests for built-in RULES discovery (`builtin-rules-md.test.ts:65`), plugin discovery (`omp-plugins.test.ts:118`), Claude plugins/commands, GitHub skills/Copilot instructions, MCP profile/env expansion, context file dedup, agent field parsing, monorepo skills, disabled extension/provider filtering, and profile isolation.
- inputs_outputs_state: Inputs are temp project/user config trees, `.omp`, `RULES.md`, `.mcp.json`, plugin package manifests, skill files, provider flags, and env vars. Outputs are discovered `Rule`, `Agent`, `MCPServer`, plugin roots, warnings, and capability keys.
- gates_or_invariants: Nearest project scope wins, profiles isolate user-level config, disabled providers suppress discovery, project plugin entries shadow user entries, invalid MCP bare entries warn/skip, frontmatter gets parsed predictably, and dedup keys prevent duplicate context files.
- dependencies_and_callers: Tests `src/discovery/*`, marketplace/project scope logic, settings/profile config, extension/plugin loaders, and config root utilities.
- edge_cases_or_failure_modes: Nested monorepos, home-dir guards, relative plugin paths, linked plugins only in lockfiles, malformed mcp entries, disabled installed plugins, and provider-specific discovery precedence.
- validation_or_tests: This directory is itself validation; each test asserts externally visible discovery outputs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-327 `directory` `packages/mnemopi/src/util`
- cursor: `[_]`
- core_role: Utility layer for mnemopi environment parsing, IDs/hashes, LRU cache, datetime/recency math, and tokenization/FTS query construction.
- algorithmic_behavior: Env parsing handles truthy/falsey/int/float/one-of at `env.ts:6`; IDs provide SHA-256-derived and timestamp/nonce IDs at `ids.ts:1`; `lru.ts:1` implements bounded cache; datetime parsing/caching and recency decay live in `datetime.ts:10` and `:48`; regex utilities tokenize recall/fact matching and CJK FTS terms at `regex.ts:76`, `:89`, `:118`, `:144`.
- inputs_outputs_state: Inputs are process env, content strings, timestamps/query times, text queries, and cache keys. Outputs are typed env values, stable/generated IDs, cache hits/evictions, UTC ISO dates, temporal boost scores, token sets, expanded synonyms, and FTS query terms.
- gates_or_invariants: Env bools accept explicit true/false vocabularies; numeric parsers fall back on invalid values; LRU maintains max size; datetime parser normalizes date-only/TZ-less inputs; token filters remove stopwords and handle CJK specially.
- dependencies_and_callers: Used by mnemopi core storage/search/sanitization/provider layers.
- edge_cases_or_failure_modes: Invalid env numeric strings, date strings without zones, CJK without spaces, stopword-heavy queries, token punctuation, and cache churn.
- validation_or_tests: Mnemopi tests for content sanitizer/provider parity indirectly depend on these utilities; no direct assigned util test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-357 `file` `crates/pi-natives/src/glob.rs`
- cursor: `[_]`
- core_role: Native N-API glob search implementation with ignore semantics, file-type filtering, optional shared scan cache, cancellation, timeout, mtime sorting, and streaming callbacks.
- algorithmic_behavior: `GlobOptions` and `GlobResult` are defined at `crates/pi-natives/src/glob.rs:38` and `:69`; bounded top-N mtime heap logic at `:137`; symlink target filtering at `:158`; cached entry filtering at `:194`; parallel sorted visitor at `:260`; deterministic final ranking at `:332`; run pipeline at `:376`; public N-API entry at `:445`.
- inputs_outputs_state: Inputs are pattern, root path, file type, recursion/hidden/gitignore/cache/sort/node_modules flags, max results, timeout/signal, and optional callback. Outputs are `GlobResult.matches` plus streamed `GlobMatch` events.
- gates_or_invariants: Empty pattern becomes `*`; `.git` always skipped and `node_modules` skipped unless requested/mentioned; symlinks can match file/dir filters by target; mtime sort must scan full candidates or bounded per-thread heaps; cached empty results may trigger one stale-cache rescan.
- dependencies_and_callers: Depends on `ignore`, `globset`, native `fs_cache`, `glob_util`, and `task::CancelToken`. Called by JS native bindings for file discovery.
- edge_cases_or_failure_modes: Invalid root/pattern, zero max results, cancellation heartbeat, poisoned locks, unsupported symlink targets, stale cache empty result, finite sorted streaming partials as supersets, and path tie-breaking.
- validation_or_tests: Native glob behavior is covered through pi-natives and coding-agent discovery/search tests; assigned issue-892 protects public native export surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-387 `file` `packages/agent/src/agent.ts`
- cursor: `[_]`
- core_role: Core agent runtime facade that owns conversation state, model/tool configuration, streaming loop lifecycle, steering/follow-up queues, abort handling, provider metadata, and event emission.
- algorithmic_behavior: Default conversion and tool-choice refresh at `packages/agent/src/agent.ts:48` and `:58`; `Agent` state/queues initialized at `:290`; constructor wires runtime options at `:374`; external events mutate stream/pending state at `:673`; steering/follow-up enqueue/dequeue at `:766` and `:813`; prompt/continue gates at `:879` and `:931`; `#runLoop` builds `AgentLoopConfig` and consumes `agentLoop` events at `:964`; error/abort message synthesis at `:1162`; listener error isolation at `:1221`; Cursor tool-result split support starts at `:1254`.
- inputs_outputs_state: Inputs are user/agent messages, system prompt, model, tools, LLM stream function, API key resolver, hooks, metadata/session state, abort signal, steering/follow-up messages, and provider options. Outputs are mutated `AgentState`, appended messages, `AgentEvent`s, tool execution state, visible assistant errors, and telemetry/hook calls.
- gates_or_invariants: Rejects prompt/continue while streaming via `AgentBusyError`; requires a configured model and existing context for continue; steering/follow-up queues are one-at-a-time or all modes; pending tool calls always cleared in finally; listener exceptions are logged not thrown; `Promise.withResolvers()` is used for idle wait.
- dependencies_and_callers: Wraps `agentLoop`/`agentLoopContinue`, `streamSimple`, catalog models, tool definitions, telemetry, append-only context, central logger, and coding-agent session surfaces.
- edge_cases_or_failure_modes: Aborted requests, Anthropic output-blocked partials, partial assistant messages on stream interruption, Cursor server-side tool result ordering, dynamic tool-choice validity after tool list changes, hook failures, and queued steer delivery at yield boundaries.
- validation_or_tests: Assigned `agent-session-queued-steer-delivery.test.ts` validates queue delivery; many session/interactive tests exercise runtime state.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-417 `file` `packages/ai/scripts/cursor-log.py`
- cursor: `[_]`
- core_role: Diagnostic parser/formatter for Cursor-style JSONL logs and streamed deltas.
- algorithmic_behavior: Delta type extraction at `packages/ai/scripts/cursor-log.py:21`; noise filtering at `:36`; structured data formatting at `:66`; entry formatting at `:111`; text delta extraction at `:130`; coalescing adjacent entries at `:145`; JSONL parsing at `:189`; file processing/follow mode at `:203`; CLI main at `:234`.
- inputs_outputs_state: Inputs are log file path, verbose/follow/last flags, JSON entries with event/data fields. Outputs are human-readable formatted event lines and coalesced text chunks.
- gates_or_invariants: Noise events are suppressed unless verbose; malformed/non-interesting entries can return `None`; follow mode tails appended entries.
- dependencies_and_callers: Standalone Python diagnostic script using pathlib/json/time/argparse.
- edge_cases_or_failure_modes: Malformed JSON, missing delta fields, verbose noise toggles, follow read races, and large logs.
- validation_or_tests: No direct test found; validation is manual log inspection.
- skip_candidate: `yes: diagnostic script, not product runtime`

### OH_MY_HUMANIZE_MAIN-HZ-447 `file` `packages/ai/test/anthropic-stream-envelope.test.ts`
- cursor: `[_]`
- core_role: Contract tests for Anthropic stream envelope tolerance, strict tool fallback, raw SSE parsing, Umans gateway behavior, thinking blocks, and cache/tool metadata.
- algorithmic_behavior: Test helpers generate mock Anthropic events/SSE frames at `packages/ai/test/anthropic-stream-envelope.test.ts:75`-`:300`; suite starts at `:308`. It asserts duplicate `message_start` handling, escaped tool names, gateway web-search blocks/headers, literal thinking tag unwrapping, signed thinking preservation, unknown events, malformed retries, strict grammar fallback, malformed tool args finalization, and raw SSE degradation.
- inputs_outputs_state: Inputs are synthetic Anthropic streams, mock request functions, provider session state, tools/schemas, and model metadata. Outputs are `AssistantMessageEvent` sequences, strict-tools disabled state, request params/headers, and final assistant content.
- gates_or_invariants: Unknown/preamble events must not reset content; terminal stop wins over spliced reconnect; strict tools disable only for compiled grammar size errors; raw SSE malformed frames degrade best-effort rather than fail after content.
- dependencies_and_callers: Tests Anthropic provider stream implementation, schema strictness, gateway compat, provider session state, and catalog model build helper.
- edge_cases_or_failure_modes: Duplicate envelopes, missing usage/delta payloads, ping before start, unknown stop reason, null stop details, unterminated tool calls, malformed JSON args, and long-cache header gating.
- validation_or_tests: This file is validation; each `it` block from `:309` through `:1208` protects a stream contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-477 `file` `packages/ai/test/auth-storage-config-override.test.ts`
- cursor: `[_]`
- core_role: Tests precedence and attribution behavior for AuthStorage config-level API key overrides.
- algorithmic_behavior: Suite at `packages/ai/test/auth-storage-config-override.test.ts:13` sets up suppressed env and tests `setConfigApiKey`, runtime `--api-key`, removal, bulk clear, OAuth account UUID suppression, and credential source descriptions at lines `:46`, `:57`, `:68`, `:80`, `:95`, `:117`.
- inputs_outputs_state: Inputs are provider IDs, OAuth stored tokens, config override keys, runtime override keys, and auth storage state. Outputs are selected API key, account attribution metadata, and credential source labels.
- gates_or_invariants: Runtime override beats config override; config override beats OAuth; removing/clearing overrides restores OAuth; config override must not leak OAuth `account_uuid`.
- dependencies_and_callers: Tests AI auth storage and metadata resolver behavior used by agent/provider requests.
- edge_cases_or_failure_modes: Mixed auth sources, stale overrides, source description mismatch, and provider-scoped attribution leaks.
- validation_or_tests: The file is direct validation of auth precedence.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-507 `file` `packages/ai/test/github-copilot-error.test.ts`
- cursor: `[_]`
- core_role: Tests GitHub Copilot HTTP error rewriting to provide actionable auth/rollout messages without misclassifying credential state.
- algorithmic_behavior: Helper builds status errors at `packages/ai/test/github-copilot-error.test.ts:4`; suite at `:10` checks provider/status gates for 401/403 and 400 `model_not_supported` payloads.
- inputs_outputs_state: Inputs are provider string, original error message, error status/code/body. Outputs are original or rewritten user-facing message.
- gates_or_invariants: Only GitHub Copilot provider is rewritten; only relevant 401/403/400 model_not_supported cases change; 403 uses access-denied wording instead of auth-failed to avoid credential removal.
- dependencies_and_callers: Tests `rewriteCopilotError` in `packages/ai/src/utils/http-inspector.ts:79`.
- edge_cases_or_failure_modes: Non-Copilot providers, non-auth statuses, 400 without expected code, and rollout-gap guidance.
- validation_or_tests: Direct unit validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-537 `file` `packages/ai/test/issue-1776-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for MiniMax/OpenAI-completions streamed tool arguments where chunks can be object-shaped instead of JSON-string deltas.
- algorithmic_behavior: SSE response/mock fetch helpers at `packages/ai/test/issue-1776-repro.test.ts:6`; tool chunk builders at `:40`; suite at `:68` asserts object-shaped args are preserved and standard JSON-string delta assembly still works.
- inputs_outputs_state: Inputs are synthetic SSE chunks with `function.arguments` as object or string fragments. Outputs are assembled tool call arguments in assistant message events.
- gates_or_invariants: Object arguments must avoid serialization round-trip corruption; string deltas still concatenate/parse normally.
- dependencies_and_callers: Tests OpenAI completions stream parser for MiniMax-compatible providers.
- edge_cases_or_failure_modes: Mixed stream shapes, premature stop chunks, and tool argument parser assumptions.
- validation_or_tests: Direct regression validation for issue 1776.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-567 `file` `packages/ai/test/nanogpt-login.test.ts`
- cursor: `[_]`
- core_role: Tests NanoGPT API key login validation against model listing endpoint without requiring entitlement to a specific model.
- algorithmic_behavior: Suite at `packages/ai/test/nanogpt-login.test.ts:5` checks successful model endpoint validation at `:6` and propagation of validation errors at `:27`.
- inputs_outputs_state: Inputs are API key/login options and mocked models endpoint responses. Outputs are login success string/result or surfaced error.
- gates_or_invariants: Validation should prove key works via models endpoint, not by assuming a specific model is available.
- dependencies_and_callers: Tests `loginNanoGPT` from `packages/ai/src/registry/nanogpt.ts:5`.
- edge_cases_or_failure_modes: Model entitlement gaps and error bodies from provider.
- validation_or_tests: Direct login contract test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-597 `file` `packages/ai/test/openai-responses-orphan-repair.test.ts`
- cursor: `[_]`
- core_role: Tests repair of OpenAI Responses snapshots where function/custom tool calls have no matching output item.
- algorithmic_behavior: Suite at `packages/ai/test/openai-responses-orphan-repair.test.ts:8` asserts synthetic `function_call_output`, custom output repair, no-op when paired, and composition with output repair for tree-branch snapshots.
- inputs_outputs_state: Inputs are OpenAI Responses item arrays with tool calls/results. Outputs are repaired arrays satisfying API pairing requirements.
- gates_or_invariants: Every call must have exactly compatible output; paired calls remain unchanged; custom tool calls use custom output type.
- dependencies_and_callers: Tests OpenAI Responses transcript repair used before API submission.
- edge_cases_or_failure_modes: Orphan calls, custom tool calls, existing outputs, and nested snapshot repair.
- validation_or_tests: Direct repair contract test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-627 `file` `packages/ai/test/schema-strict-mode.test.ts`
- cursor: `[_]`
- core_role: Comprehensive validation suite for JSON schema normalization, strict-mode enforcement, validator unsupported keywords, meta-validation, and strict fallback behavior.
- algorithmic_behavior: `sanitizeSchemaForStrictMode` suite starts at `packages/ai/test/schema-strict-mode.test.ts:17`; `enforceStrictSchema` at `:491`; `tryEnforceStrictSchema` at `:713`; validator regressions at `:876`; meta-validator at `:965`; Zod root extras at `:1003`; unrepresentable open-branch fallback at `:1024`.
- inputs_outputs_state: Inputs are JSON/Zod-derived schemas with refs, nullable unions, defaults, allOf/anyOf, enum/const, object maps, unsupported keywords, malformed nodes, and values. Outputs are strict-compatible schema objects, downgrade decisions, validation issues, and preserved unknown root fields.
- gates_or_invariants: Strict mode requires closed objects and full required lists; defaults are inlined only when description exists; unrepresentable boolean/open schemas must fall back; unsupported validators reject real invalid values; recursion caps prevent accepting invalid ref chains.
- dependencies_and_callers: Tests `packages/ai/src/utils/schema/normalize.ts`, `json-schema-validator.ts`, meta-validator, wire/normalization paths, and tool argument validation.
- edge_cases_or_failure_modes: Mixed primitive enums, non-primitive const roots, self-referential refs, propertyNames/patternProperties/dependentRequired/if-then/prefixItems, optional unions, nullable MCP enum parameters, and shared branch reuse.
- validation_or_tests: This file is the primary validation surface for schema strict algorithms.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-657 `file` `packages/catalog/src/build.ts`
- cursor: `[_]`
- core_role: Constructs runtime `Model<TApi>` objects from generated/configured `ModelSpec<TApi>` and resolves compat defaults.
- algorithmic_behavior: `buildModel` at `packages/catalog/src/build.ts:18` spreads spec fields and sets `compat` via `resolveCompat`; `buildCompat` at `:29` exposes compat resolution alone.
- inputs_outputs_state: Inputs are `ModelSpec<TApi>` with api/provider/model fields and optional compat config. Outputs are `Model<TApi>` with resolved `compat`, preserving spec values.
- gates_or_invariants: Compat resolution is centralized through `resolveCompat`; type parameter ties API to compatible config shape.
- dependencies_and_callers: Used by bundled catalog loading, tests, provider registry, and model manager.
- edge_cases_or_failure_modes: Missing or partial compat config relies on resolver defaults; incorrect API type would break typed compat expectations.
- validation_or_tests: `packages/catalog/test/build.test.ts` and many model registry tests construct models through this helper.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-687 `file` `packages/catalog/test/issue-2105-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for AIML API built-in provider registration, transport/base URL, discovery filtering, and env credential resolution.
- algorithmic_behavior: Suite starts at `packages/catalog/test/issue-2105-repro.test.ts:9`; tests descriptor registration at `:10`, OpenAI-compatible completions transport/base URL at `:20`, chat-compatible model filtering at `:62`, and `AIMLAPI_API_KEY` env resolution at `:84`.
- inputs_outputs_state: Inputs are catalog provider descriptors, mocked discovery payloads, env vars, and provider/model registry calls. Outputs are descriptor metadata, models, transport URL, and credential resolution result.
- gates_or_invariants: AIML provider must exist as built-in, use OpenAI-compatible completions transport, target AIML base URL, filter incompatible IDs, and resolve documented env key.
- dependencies_and_callers: Tests catalog descriptors/openai-compatible discovery used by coding-agent model registry.
- edge_cases_or_failure_modes: Incompatible discovery IDs and missing env.
- validation_or_tests: Direct regression validation for issue 2105.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-717 `file` `packages/coding-agent/scripts/bench-guard.ts`
- cursor: `[_]`
- core_role: Boot performance guard script comparing current CLI startup median against a stored hyperfine baseline.
- algorithmic_behavior: Defines 5% regression threshold and baseline path at `packages/coding-agent/scripts/bench-guard.ts:23`; parses hyperfine median at `:28`; runs measurement at `:35`; update mode at `:49`; compares ratio/verdict at `:64`.
- inputs_outputs_state: Inputs are `hyperfine` output, `bench/boot-baseline.json`, `--update`, and command `PI_TIMING=x bun src/cli.ts`. Outputs are updated baseline or pass/fail verdict.
- gates_or_invariants: Current median must be within `1.05` baseline unless updating; missing/invalid hyperfine JSON fails.
- dependencies_and_callers: Used by developer/CI benchmarking; depends on Bun shell, hyperfine, baseline JSON.
- edge_cases_or_failure_modes: No hyperfine installed, noisy timing, missing baseline, and update accidentally replacing baseline.
- validation_or_tests: No direct test found; script behavior is self-verifying through exit code.
- skip_candidate: `yes: CI performance guard, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-747 `file` `packages/coding-agent/test/advisor-watchdog.test.ts`
- cursor: `[_]`
- core_role: Tests advisor prompt discovery and WATCHDOG.md composition.
- algorithmic_behavior: Suite at `packages/coding-agent/test/advisor-watchdog.test.ts:13` verifies discovering/appending `WATCHDOG.md`, resolving nested folders with depth sorting, and combining user-level/native project-level watchdog files.
- inputs_outputs_state: Inputs are temp directory trees with advisor/watchdog files and discovery context. Outputs are resolved prompt content/order.
- gates_or_invariants: Nested folders sort by depth; user and native project surfaces both contribute; advisor prompt must include watchdog content.
- dependencies_and_callers: Tests advisor mode prompt discovery in coding-agent.
- edge_cases_or_failure_modes: Multiple nesting levels, absent files, and precedence/order mistakes.
- validation_or_tests: Direct test file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-777 `file` `packages/coding-agent/test/agent-session-queued-steer-delivery.test.ts`
- cursor: `[_]`
- core_role: Tests AgentSession delivery of queued steering/follow-up messages across yield boundaries, settle drains, aborts, dequeue operations, and transcript tails.
- algorithmic_behavior: Harness types start at `packages/coding-agent/test/agent-session-queued-steer-delivery.test.ts:31`; suite at `:37`; scenarios at `:116`, `:141`, `:180`, `:209`, `:236`, `:275`.
- inputs_outputs_state: Inputs are collab steer messages, session queues, fake agent stream/yield behavior, abort events, and transcript tails. Outputs are delivered prompts, queue state, UI notices, and resumed work.
- gates_or_invariants: Steers landing at yield boundary must be delivered; stranded queue drains when session settles; aborting auto-continued turn still drains; dequeue restores ultrathink text and removes companion notice.
- dependencies_and_callers: Tests `AgentSession` over `packages/agent/src/agent.ts` queue APIs.
- edge_cases_or_failure_modes: Non-advisor custom transcript tails, fresh prompts with queued steer, mid-stream dequeue, and aborted queued turn.
- validation_or_tests: Direct regression suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-807 `file` `packages/coding-agent/test/autoresearch-state.test.ts`
- cursor: `[_]`
- core_role: Tests autoresearch metric math, SQLite storage round-trips, control state, slash command behavior, and accountability hook registration.
- algorithmic_behavior: Metric helpers at `packages/coding-agent/test/autoresearch-state.test.ts:54`; storage suite at `:115`; control state at `:375`; slash command harness at `:403` and tests at `:518`; hook test at `:585`.
- inputs_outputs_state: Inputs are experiment results, flags, metric directions, session/run DB rows, notes, dirty repo state, slash args, and fake runtime. Outputs are baseline/best/confidence values, persisted state, branch slug, notifications/errors, and hook registration state.
- gates_or_invariants: Flagged runs excluded from baseline/best/noise; confidence requires at least three valid runs and nonzero noise; latest control entry wins; dirty worktree aborts `/autoresearch`; post-hoc accountability replaces edit guards.
- dependencies_and_callers: Tests autoresearch storage/state/slash command modules and run-experiment control surfaces.
- edge_cases_or_failure_modes: Pending run abandonment, segment bumping, note updates, clean vs dirty repo, bare vs argument slash invocation.
- validation_or_tests: Direct validation suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-837 `file` `packages/coding-agent/test/config-cli.test.ts`
- cursor: `[_]`
- core_role: Tests CLI config schema handling for record, array, and numeric settings.
- algorithmic_behavior: Suite starts at `packages/coding-agent/test/config-cli.test.ts:31`; record JSON/text output at `:32`; setting/getting records at `:49`; arrays at `:64`; numeric idle compaction CLI parsing at `:78`.
- inputs_outputs_state: Inputs are temp config root/env, CLI values, JSON/text output modes. Outputs are persisted settings and rendered config values.
- gates_or_invariants: Record settings render as JSON with type in text output; arrays parse as JSON arrays; numeric settings coerce CLI strings to numbers.
- dependencies_and_callers: Tests coding-agent config CLI and `Settings`.
- edge_cases_or_failure_modes: Env config dir fallback, invalid JSON/type mismatches, and numeric coercion.
- validation_or_tests: Direct CLI schema test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-867 `file` `packages/coding-agent/test/git-reftable.test.ts`
- cursor: `[_]`
- core_role: Tests git reference resolution in reftable repositories/worktrees and git config trailing-comment parsing.
- algorithmic_behavior: Detects git `--ref-format` support at `packages/coding-agent/test/git-reftable.test.ts:8`; tests reftable repo refs at `:63`, config comments at `:105`, and reftable worktree refs at `:195`.
- inputs_outputs_state: Inputs are temporary git repos/worktrees with reftable ref storage and config content. Outputs are resolved HEAD/branch/reference metadata.
- gates_or_invariants: Ref resolution must not assume loose/packed refs; config parser must ignore trailing comments correctly.
- dependencies_and_callers: Tests coding-agent git utils used by sessions/tasks/status.
- edge_cases_or_failure_modes: Git versions without reftable support, reftable worktrees, and config values containing comments.
- validation_or_tests: Direct regression tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-897 `file` `packages/coding-agent/test/interactive-mode-default-plan-mode.test.ts`
- cursor: `[_]`
- core_role: Tests startup decision logic for entering plan mode by default.
- algorithmic_behavior: Tool helper at `packages/coding-agent/test/interactive-mode-default-plan-mode.test.ts:15`; suite at `:27`; cases at `:100`-`:190` cover enabled/default/restored/metadata/extension custom/compacted/restored mode off/global disabled.
- inputs_outputs_state: Inputs are settings, transcript state, startup metadata/custom entries, restored mode changes, and global plan mode flag. Outputs are interactive mode state.
- gates_or_invariants: Plan mode starts only for fresh sessions when enabled; restored conversation or explicit restored mode off suppresses it; startup metadata/custom entry alone is not conversation history.
- dependencies_and_callers: Tests `InteractiveMode` initialization and settings.
- edge_cases_or_failure_modes: Compacted session with no trailing message, extension custom entry, global disable, and restored mode_change.
- validation_or_tests: Direct UI mode lifecycle test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-927 `file` `packages/coding-agent/test/issue-899-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests ensuring synchronous git metadata reads survive transient `EINTR`.
- algorithmic_behavior: `makeEintrError` at `packages/coding-agent/test/issue-899-repro.test.ts:8`; suite at `:17`; tests no throw and bounded retry recovery at `:35` and `:52`.
- inputs_outputs_state: Inputs are mocked filesystem read errors for `.git/HEAD`. Outputs are resolved HEAD state or successful retry.
- gates_or_invariants: Transient `EINTR` must be retried within bounds and not crash sync metadata resolution.
- dependencies_and_callers: Tests git head resolution helper.
- edge_cases_or_failure_modes: Signal interruptions during sync reads and retry exhaustion.
- validation_or_tests: Direct regression suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-957 `file` `packages/coding-agent/test/markit-converters.test.ts`
- cursor: `[_]`
- core_role: Tests office/document conversion pipeline for DOCX/XLSX/PPTX/EPUB and unsupported formats.
- algorithmic_behavior: Fixture builders at `packages/coding-agent/test/markit-converters.test.ts:20`; suite at `:34`; tests DOCX paragraphs, XLSX tables/absolute rels, PPTX headings/images, EPUB spine/table normalization, and unsupported RTF at `:35`-`:154`.
- inputs_outputs_state: Inputs are synthetic zipped office/epub buffers and optional image output dir. Outputs are markdown content and extracted images or unsupported-format result.
- gates_or_invariants: Relationship targets resolve absolute and relative paths; images are extracted when requested; unsupported formats report cleanly instead of garbage.
- dependencies_and_callers: Tests `markit` converters used by fetch/read binary rendering.
- edge_cases_or_failure_modes: Absolute `/-prefixed` rel targets, `../media` PPTX image rels, non-root OPF base path, table normalization, and unsupported extension.
- validation_or_tests: Direct converter validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-987 `file` `packages/coding-agent/test/model-registry.test.ts`
- cursor: `[_]`
- core_role: Large integration-style contract suite for coding-agent model registry behavior, provider overrides, custom model merging, canonical equivalence, discovery cache, OAuth flags, disabled providers, thinking metadata, and variant collapse.
- algorithmic_behavior: Main suite starts at `packages/coding-agent/test/model-registry.test.ts:14`; canonical equivalence at `:223`; OpenRouter routed fallback at `:481`; baseUrl override at `:497`; provider compat at `:689`; custom merge at `:788`; thinking normalization at `:1193`; model overrides at `:1242`; Copilot OAuth alignment at `:1497`; disabled providers at `:1577`; OAuth provider auth at `:1837`; cached discovery at `:1837`; effort-tier collapse at `:2098`.
- inputs_outputs_state: Inputs are settings JSON, provider descriptors, custom models, model overrides, cached discovery records, OAuth/API key availability, provider order, and bundled catalog. Outputs are available/discoverable models, resolved canonical selections, merged provider/model fields, compat config, discovery refresh results, and auth flags.
- gates_or_invariants: Built-in models survive baseUrl overrides; same-ID custom replacement does not leak bundled headers/compat unexpectedly; overrides deep-merge where intended; disabled providers are excluded/skipped; authoritative discovery suppresses synthetic fallbacks; retired variant IDs re-key.
- dependencies_and_callers: Tests `ModelRegistry`, catalog package, settings, auth storage, provider discovery/cache, and registry refresh logic.
- edge_cases_or_failure_modes: Wrapper IDs, enterprise Copilot discovery host, stale nullable limit sentinels, custom discoverable refresh, provider-level auth defaults, OpenRouter routing suffixes, and gpt-5.4 hardcoded context policy.
- validation_or_tests: Primary validation surface for model registry.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1017 `file` `packages/coding-agent/test/repro-issue-1022-disabled-default-model.test.ts`
- cursor: `[_]`
- core_role: Regression test that path-scoped `enabledModels` constraints are respected by default model fallback.
- algorithmic_behavior: Empty workspace helper at `packages/coding-agent/test/repro-issue-1022-disabled-default-model.test.ts:21`; suite at `:25`; test at `:44` initializes settings and ensures disallowed provider is not selected.
- inputs_outputs_state: Inputs are cwd/agentDir config with enabledModels exclusions. Output is selected default model/provider.
- gates_or_invariants: Default fallback must not pick provider excluded by path-scoped enabled model settings.
- dependencies_and_callers: Tests settings/model selection logic.
- edge_cases_or_failure_modes: Empty workspace tree and provider fallback ordering.
- validation_or_tests: Direct regression validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1047 `file` `packages/coding-agent/test/session-color.test.ts`
- cursor: `[_]`
- core_role: Tests deterministic session accent color generation and contrast/hue constraints.
- algorithmic_behavior: Luminance/contrast helpers at `packages/coding-agent/test/session-color.test.ts:9`; generated names at `:20`; suites at `:27` and `:75` test determinism, warm/cool hue bands, vivid dark accents, AA-large contrast, dark-vs-light relation, and avoiding theme hues.
- inputs_outputs_state: Inputs are session names, dark/light theme surfaces, and real theme color lists. Outputs are accent hex colors.
- gates_or_invariants: Dark themes use warm hues; light themes use cool hues; light accents meet contrast and are not lighter than dark equivalents; theme hue collisions avoided.
- dependencies_and_callers: Tests status/session UI color helpers and Theme integration.
- edge_cases_or_failure_modes: Saturated theme hues, undefined surface, mid-light surfaces, many similar names.
- validation_or_tests: Direct color contract test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1077 `file` `packages/coding-agent/test/status-line-overflow.test.ts`
- cursor: `[_]`
- core_role: Tests status line session accent rendering and overflow/truncation decisions.
- algorithmic_behavior: Context/session helpers at `packages/coding-agent/test/status-line-overflow.test.ts:29` and `:72`; suites at `:93`, `:132`, `:167`; tests path ellipsis, monotonic width reduction, visible minimal segment, preserving/dropping git segment based on terminal width, and session accent gap painting.
- inputs_outputs_state: Inputs are segment context, path max length, branch/session name, terminal width, and settings. Outputs are rendered status line segments/styles.
- gates_or_invariants: Path shrinks before git is dropped; git only drops under extreme width; enough space is no-op; maxLength=4 still visible; session accent toggle changes gap color.
- dependencies_and_callers: Tests status line rendering and overflow algorithm.
- edge_cases_or_failure_modes: Very narrow terminals, short paths with large maxLength, tiny overflows, and no branch.
- validation_or_tests: Direct UI rendering validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1107 `file` `packages/coding-agent/test/title-generator.test.ts`
- cursor: `[_]`
- core_role: Tests conversation title generation across forced tool calls, marker fallback, prompt resolution, credential errors, reasoning budgets, and model role precedence.
- algorithmic_behavior: Model/settings helpers at `packages/coding-agent/test/title-generator.test.ts:8`; suite at `:53`; covers forced `set_title` at `:54`, bundled/custom prompt at `:84`/`:98`, text fallback at `:127`, greeting deferral at `:143`, none sentinel at `:153`, credential failures at `:177`/`:205`, reasoning-safe budget at `:236`, code block stripping at `:261`, marker mode and forced-tool rejection at `:281`/`:302`, title tag parsing at `:320`/`:336`, custom marker instruction at `:352`, and model role precedence at `:377`.
- inputs_outputs_state: Inputs are user messages, model capabilities, title prompt files, auth behavior, and mocked model responses. Outputs are title string or null plus logged errors.
- gates_or_invariants: Greetings can defer without model call; forced tool choice used only when supported; marker fallback parses tags/sentences safely; credentials errors return null; code blocks stripped before prompt.
- dependencies_and_callers: Tests title generator, model registry roles, prompt discovery, auth lookup, and LLM streaming.
- edge_cases_or_failure_modes: No tool call, missing title tags, unclosed title tag from truncated response, model rejects forced tool choice, and missing credentials.
- validation_or_tests: Direct title generation contract suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1137 `file` `packages/collab-web/test/client.test.ts`
- cursor: `[_]`
- core_role: Tests collaborative web guest client frame application and snapshot/state transitions.
- algorithmic_behavior: Fixtures at `packages/collab-web/test/client.test.ts:15`; suite at `:63`; tests invalid link, welcome/live/readOnly, message stream ghost start/end, active tool lifecycle, agent working reconciliation, bus progress, bye/error frames, and snapshot reference replacement.
- inputs_outputs_state: Inputs are host frames (`welcome`, message/tool/agent/progress/bye/error) and guest link. Outputs are client snapshot state, active tools, notices, progress map, and live/ended status.
- gates_or_invariants: Invalid links throw; message updates synthesize missed start; ghost persists until matching entry lands; state frame reconciles agent working state; snapshot object replaced per frame while internal reference stability is checked.
- dependencies_and_callers: Tests collab-web `GuestClient`.
- edge_cases_or_failure_modes: Missed message_start, out-of-order message_end, concurrent tools, read-only welcome, and error/bye handling.
- validation_or_tests: Direct client protocol validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1167 `file` `packages/hashline/test/leniency.test.ts`
- cursor: `[_]`
- core_role: Tests hashline patch format leniency, contamination rejection, body contracts, and duplicate boundary behavior.
- algorithmic_behavior: `applyPatch` helper at `packages/hashline/test/leniency.test.ts:4`; suites start at `:10`, `:62`, `:99`, `:176`, `:191`; they cover section headers, verb header forms, bare body auto-piping, line-number prefix stripping, delete/insert constraints, apply_patch/unified-diff contamination, and duplicate boundary payloads.
- inputs_outputs_state: Inputs are original text and hashline diffs. Outputs are patched text, warnings, or parse/application errors.
- gates_or_invariants: Canonical/alternate replace-delete-insert headers accepted; malformed snapshot tags rejected; bare rows warn/auto-prefix only under uniform conditions; delete cannot have body; contamination sentinels rejected.
- dependencies_and_callers: Tests hashline parser/apply engine.
- edge_cases_or_failure_modes: Paths with spaces, apply_patch-contaminated headers, numeric-keyed literal bodies, `+N:` payloads, orphan top-level plus text, and replacement boundary echoes.
- validation_or_tests: Direct format contract suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1197 `file` `packages/mnemopi/test/content-sanitizer.test.ts`
- cursor: `[_]`
- core_role: Tests content sanitizer data URI parsing, entropy heuristics, blob storage, and pass-through/extraction decisions.
- algorithmic_behavior: Temp blob dir helper at `packages/mnemopi/test/content-sanitizer.test.ts:26`; suites at `:32`, `:55`, `:78`, `:94`; tests data URI prefix detection, base64/default MIME parsing, invalid rejection, high-entropy detection, SHA-256 idempotent blob storage, and sanitization thresholds.
- inputs_outputs_state: Inputs are normal text, data URIs, large/high-entropy payloads, invalid base64, and blob dir env. Outputs are sanitized content plus extracted blob metadata/files.
- gates_or_invariants: Only data URI prefixes are parsed; invalid base64 rejected; large high-entropy base64-like payloads extracted while large prose remains inline; blob storage is content-addressed and idempotent.
- dependencies_and_callers: Tests mnemopi content sanitizer and util/env/blob behavior.
- edge_cases_or_failure_modes: Missing schemes, default MIME, hard cap overflow, random-looking text vs prose/repetition.
- validation_or_tests: Direct sanitizer suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1227 `file` `packages/mnemopi/test/provider-all-15-tools-parity.test.ts`
- cursor: `[_]`
- core_role: Tests provider-compatible mnemopi all-tools surface, JSON schemas, required args, mutation guards, export/import, and structured results.
- algorithmic_behavior: `schemaFor` helper at `packages/mnemopi/test/provider-all-15-tools-parity.test.ts:25`; suite at `:31`; tests schema validity at `:32`, required args at `:68`, missing-arg errors at `:78`, export/import into isolated bank at `:93`, and diagnose/validate/graph/shared handlers at `:126`.
- inputs_outputs_state: Inputs are provider tool names/args and isolated memory banks. Outputs are JSON schemas, user-facing errors, exported files, imported state, and structured provider results.
- gates_or_invariants: Missing required args must not mutate state; provider schemas must be valid JSON schema; export/import round-trip preserves provider data.
- dependencies_and_callers: Tests mnemopi provider tool registry and storage handlers.
- edge_cases_or_failure_modes: Missing args, invalid schemas, isolated bank import/export paths, and shared handler consistency.
- validation_or_tests: Direct provider parity suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1257 `file` `packages/natives/test/issue-892-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test ensuring pi-natives `.d.ts` public declarations are explicit ESM exports in runtime JS.
- algorithmic_behavior: Public symbol regex at `packages/natives/test/issue-892-repro.test.ts:20`; `readPublicSymbols` at `:22`; `esmExportsName` at `:34`; suite/test at `:40`-`:41`.
- inputs_outputs_state: Inputs are generated `native/index.d.ts` and `native/index.js`. Output is assertion that every declared public symbol appears in ESM exports.
- gates_or_invariants: Public type declarations and JS exports must stay in sync.
- dependencies_and_callers: Tests native package generated public surface.
- edge_cases_or_failure_modes: Missing JS export for declared class/function/enum.
- validation_or_tests: Direct regression validation for issue 892.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1287 `file` `packages/snapcompact/research/exp15_bestgemini.py`
- cursor: `[_]`
- core_role: Research experiment runner for comparing Snapcompact carriers on Gemini with document/page and grid chunk strategies, QA calls, aggregation, and reporting.
- algorithmic_behavior: Cache wrapper at `packages/snapcompact/research/exp15_bestgemini.py:53`; text wrapping/layout at `:74`/`:97`; page packing at `:118`; document color/rendering at `:131`/`:154`; QA call at `:194`; document page and grid chunk runs at `:229`/`:261`; aggregation at `:288`; `Runner` at `:311`; output cell printing and CLI main at `:376`/`:393`.
- inputs_outputs_state: Inputs are model ID, condition, paragraphs/questions/context, pricing, cache/fresh flags, rendered images. Outputs are per-question records, aggregate accuracy/cost stats, rendered images/cache files, and printed result cells.
- gates_or_invariants: Page packing respects line budgets; cache keys isolate payload/model; aggregation uses supplied input/output prices; render variants encode document roles/colors.
- dependencies_and_callers: Depends on PIL/image rendering, Gemini API/provider helpers, SQuAD utilities, local prompts/cache, and research data.
- edge_cases_or_failure_modes: Model/API failures, parse failures in QA response, font/image generation issues, stale cache, bad page bounds, and cost misconfiguration.
- validation_or_tests: Internal aggregation/printing only; no package test.
- skip_candidate: `yes: research experiment, not shipped runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1317 `file` `packages/snapcompact/research/snapcompact_pricing_viz.py`
- cursor: `[_]`
- core_role: Research visualization script for Snapcompact pricing/cost result presentation.
- algorithmic_behavior: Font helpers at `packages/snapcompact/research/snapcompact_pricing_viz.py:36` and `:46`; `main` at `:53` builds image visualization from hardcoded/loaded pricing metrics using PIL drawing.
- inputs_outputs_state: Inputs are pricing/experiment metrics and local font availability. Output is a generated visualization image.
- gates_or_invariants: Uses fallback font helpers and fixed layout assumptions.
- dependencies_and_callers: Depends on PIL and research outputs; not used by CLI runtime.
- edge_cases_or_failure_modes: Missing fonts, absent input data/artifacts, and fixed canvas overflow.
- validation_or_tests: Visual/manual validation only.
- skip_candidate: `yes: research visualization, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1347 `file` `packages/stats/src/embedded-client.ts`
- cursor: `[_]`
- core_role: Decodes embedded stats dashboard archive text for compiled/npm builds.
- algorithmic_behavior: `decodeEmbeddedClientArchive` at `packages/stats/src/embedded-client.ts:19` strips whitespace, rejects empty/non-base64 text, decodes base64, and verifies gzip magic bytes before returning a `Buffer`.
- inputs_outputs_state: Input is generated archive text from `embedded-client.generated.txt`. Output is gzip tar buffer or `null`.
- gates_or_invariants: Blank or legacy TypeScript stub content is treated as no embedded archive; decoded bytes must start with `0x1f 0x8b`.
- dependencies_and_callers: Used by stats package embedded client extraction/serving; generated by `scripts/generate-client-bundle.ts`.
- edge_cases_or_failure_modes: Whitespace in base64, invalid alphabet, non-gzip decoded bytes, legacy placeholder.
- validation_or_tests: Embedded archive behavior should be covered by stats bundle tests/smoke; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1377 `file` `packages/tui/src/kitty-graphics.ts`
- cursor: `[_]`
- core_role: Kitty graphics feature detection and Unicode placeholder encoding/rendering utilities.
- algorithmic_behavior: Placeholder constants at `packages/tui/src/kitty-graphics.ts:19`; support detection at `:76`; mutable feature flags at `:91`/`:95`; cell fit check at `:100`; virtual placement encoding at `:114`; grid encoding at `:132`; placeholder line rendering at `:160`.
- inputs_outputs_state: Inputs are terminal ID/env, image id/placement dimensions, rows/columns, and feature overrides. Outputs are Kitty placeholder strings/lines and feature booleans.
- gates_or_invariants: Placeholder cell count must not exceed row/column diacritic capacity; terminal support is gated by ID/env detection; feature flags can be overridden for tests/runtime.
- dependencies_and_callers: Used by TUI image component and terminal renderers.
- edge_cases_or_failure_modes: Unsupported terminals, too-large placeholder grids, stale env, and incorrect diacritic mapping causing image placement drift.
- validation_or_tests: TUI image/render tests cover behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1407 `file` `packages/tui/test/issue-1974-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for tmux scrollback rendering and live region repaint behavior.
- algorithmic_behavior: Component fixtures at `packages/tui/test/issue-1974-repro.test.ts:24`, `:47`, `:73`; env/probe helpers at `:95`-`:144`; suite at `:158`; tests scrolled-off streaming head committed exactly once, no ED3 in tmux, chrome not pushed into history, and cursor anchoring on no-append repaint.
- inputs_outputs_state: Inputs are virtual terminal, tmux env, live region content, scrollback state, viewport probes. Outputs are terminal buffer/history/cursor snapshots.
- gates_or_invariants: Tmux pane must not receive `CSI 3 J`; streaming content should enter history once; chrome below live block stays out of history; cursor remains anchored after repaint shifts.
- dependencies_and_callers: Tests TUI renderer, virtual terminal, native scrollback live region protocol.
- edge_cases_or_failure_modes: Unknown/stale viewport probes, tmux env, live region volatility, and duplicate history insertion.
- validation_or_tests: Direct regression suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1437 `file` `packages/tui/test/render-stress-harness.ts`
- cursor: `[_]`
- core_role: Large randomized/templated stress harness for TUI differential rendering, scrollback, overlays, cursor positioning, ANSI wrapping, env/platform modes, and replay diagnostics.
- algorithmic_behavior: Operation taxonomy at `packages/tui/test/render-stress-harness.ts:81`; scenario types at `:251`; terminal traits at `:285`; RNG at `:478`; stress model at `:595`; driver at `:1105`; viewport/scrollback expectations at `:2939` and `:2850`; overlay layout at `:3057`; scenario building at `:3377`; replay parsing/logging at `:3447`/`:3554`; execution at `:3989`; targeted regressions at `:4011` and `:4097`.
- inputs_outputs_state: Inputs are scenario seeds, platform/env/terminal/geometry modes, operation sequences, component text/overlays/cursor markers, env vars. Outputs are rendered terminal frames, expected frame objects, replay logs, success/failure diagnostics.
- gates_or_invariants: Expected viewport/scrollback must match terminal output, with allowances for combining mark drift; overlays composite deterministically; env/platform patches restore after run; replay logs reproduce failures.
- dependencies_and_callers: Used by TUI stress tests and virtual terminal renderer.
- edge_cases_or_failure_modes: Wide/emoji/Arabic combining text, ANSI links/backgrounds, huge scroll offsets, unknown viewport probes, tmux/termux/WSL/VTE/Ghostty envs, overlay anchoring, no-reflow resize, and preexisting scrollback.
- validation_or_tests: Harness itself powers stress validation; targeted exported regressions are callable tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1467 `file` `packages/tui/test/wrap-ansi.test.ts`
- cursor: `[_]`
- core_role: Tests ANSI-aware text wrapping style preservation/reset behavior.
- algorithmic_behavior: Suite at `packages/tui/test/wrap-ansi.test.ts:4`; underline tests at `:5`; background preservation at `:53`; strikethrough at `:102`; basic wrapping at `:129`.
- inputs_outputs_state: Inputs are styled strings and wrap widths. Outputs are wrapped strings with ANSI reset/preserve sequences.
- gates_or_invariants: Underline/strikethrough must reset at line ends without bleeding to padding; background and color survive wraps where intended; trailing whitespace beyond width truncates.
- dependencies_and_callers: Tests TUI `wrapTextWithAnsi`.
- edge_cases_or_failure_modes: Underline before text, whitespace before reset, nested underline inside background, color code preservation.
- validation_or_tests: Direct unit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1497 `file` `packages/utils/src/mime.ts`
- cursor: `[_]`
- core_role: Image MIME/dimension metadata detector for PNG, JPEG, GIF, and WebP headers, with sync/async file readers.
- algorithmic_behavior: Magic constants at `packages/utils/src/mime.ts:5`; PNG parser at `:31`; JPEG segment scan at `:48`; GIF parser at `:98`; WebP parser at `:110`; dispatcher at `:141`; sync/async readers at `:147`/`:154`.
- inputs_outputs_state: Inputs are header bytes or file paths plus optional max header bytes. Outputs are `{ mimeType,width,height }` metadata or `null`.
- gates_or_invariants: Only supported image MIME types are returned; reads are capped by default 256 KiB; parsers require format-specific magic and enough bytes.
- dependencies_and_callers: Used by image/file tooling across packages; depends on Buffer and file reads.
- edge_cases_or_failure_modes: Truncated headers, JPEG segment length errors, unsupported WebP chunk types, huge metadata before dimensions, and non-image files.
- validation_or_tests: Image metadata tests likely elsewhere; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1527 `file` `packages/utils/test/mermaid-ascii.test.ts`
- cursor: `[_]`
- core_role: Regression test for Mermaid ASCII rendering label collision preservation.
- algorithmic_behavior: Suite at `packages/utils/test/mermaid-ascii.test.ts:4`; test at `:5` asserts an existing emoji edge label remains when a later narrow label collides.
- inputs_outputs_state: Inputs are Mermaid diagram text with edge labels. Output is rendered ASCII string.
- gates_or_invariants: Earlier emoji/wide label content must not be overwritten by later narrow colliding label.
- dependencies_and_callers: Tests `renderMermaidAscii`, including vendor ASCII renderer.
- edge_cases_or_failure_modes: Wide glyph width/collision handling.
- validation_or_tests: Direct regression test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1557 `file` `python/robomp/src/github_client.py`
- cursor: `[_]`
- core_role: Async GitHub REST client and payload mapper for issues, PRs, comments, reviews, files, reactions, repo metadata, and retry/rate-limit errors.
- algorithmic_behavior: Data classes define result payloads at `python/robomp/src/github_client.py:21`-`:121`; retry-after parser at `:134`; `GitHubClient` starts at `:150`; payload mappers at `:512` through `:596`.
- inputs_outputs_state: Inputs are GitHub token, repo/issue/PR identifiers, REST JSON payloads, pagination params, and HTTP responses. Outputs are typed dataclass objects, API mutations, and `GitHubError` with status/rate limit details.
- gates_or_invariants: HTTP errors are surfaced with parsed retry-after; payload mappers normalize nested repo/issue/comment/review fields; client methods enforce GitHub endpoint shape.
- dependencies_and_callers: Used by `python/robomp` automation worker/queue system; depends on `httpx`.
- edge_cases_or_failure_modes: Rate limits, missing optional fields, pagination, deleted/renamed fields, non-JSON errors, and repo extraction from payload.
- validation_or_tests: Queue tests use stubs; direct GitHub client tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1587 `file` `python/robomp/tests/test_queue_cancel.py`
- cursor: `[_]`
- core_role: Async tests for robomp worker queue cancellation behavior.
- algorithmic_behavior: Stub GitHub/sandbox/transport classes at `python/robomp/tests/test_queue_cancel.py:28`; pool helper at `:42`; event row helper at `:53`; async tests exercise cancellation while work is pending/running.
- inputs_outputs_state: Inputs are fake settings/database/event rows, worker pool, cancellation triggers, and stub dependencies. Outputs are DB queue state, worker cancellation effects, and fired events.
- gates_or_invariants: Canceled queue items should not continue execution or leave inconsistent state; worker pool should handle cancellation without real GitHub/sandbox side effects.
- dependencies_and_callers: Tests robomp worker pool, database queue, settings, GitHub/sandbox abstractions.
- edge_cases_or_failure_modes: Cancel while worker awaits, duplicate delivery IDs, cleanup after cancellation.
- validation_or_tests: Direct pytest/async validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1617 `directory` `packages/coding-agent/src/edit/modes`
- cursor: `[_]`
- core_role: Coding-agent edit engine modes: robust apply-patch parser/expander, fuzzy/anchored patch application, and replace-mode matching.
- algorithmic_behavior: `apply-patch.ts` expands grammar AST into edit entries at `packages/coding-agent/src/edit/modes/apply-patch.ts:28`; `replace.ts` implements exact/trim/unicode/prefix/substring/fuzzy line and sequence matching with Levenshtein at `:305`, `findMatch` at `:476`, `seekSequence` at `:610`, and context line lookup at `:856`; `patch.ts` applies normalized patch operations with hunk fallbacks, ambiguity diagnostics, indentation adjustment, BOM/line-ending preservation, and LSP writethrough at `patch.ts:1049`, `:1410`, `:1465`, `:1745`; `apply-patch.lark` defines patch grammar.
- inputs_outputs_state: Inputs are patch/apply_patch/replace params, target files, cwd/session, optional LSP batch, fuzzy thresholds, abort signal. Outputs are `AgentToolResult` edit details, diffs/previews, diagnostics, warnings, changed files, or parse/match errors.
- gates_or_invariants: Plan-mode write permissions enforced; missing update/create diffs rejected; ambiguous matches require more context; partial-line matches must preserve discarded text; overlapping hunks rejected; BOM and line endings restored; dry run previews do not write.
- dependencies_and_callers: Used by edit/write/apply_patch tools and renderers; depends on Ark schemas, `@oh-my-pi/pi-utils`, LSP writethrough, TUI render utilities.
- edge_cases_or_failure_modes: Fuzzy false positives, repeated blocks, EOF insertions, CRLF/BOM files, rename same path, missing files, delete body misuse, LSP diagnostics, and streaming apply_patch previews.
- validation_or_tests: Assigned apply-patch renderer tests and hashline/edit tests validate UI and parser behavior; broader edit-mode tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1647 `directory` `packages/coding-agent/test/modes/utils`
- cursor: `[_]`
- core_role: Tests utility behavior for interactive mode initial transcript rendering and copy target extraction.
- algorithmic_behavior: `render-initial-messages.test.ts` fixtures start at `packages/coding-agent/test/modes/utils/render-initial-messages.test.ts:39`; suites at `:184`, `:201`, `:218` cover transcript source, clearTerminalHistory, and image replay. `copy-targets.test.ts` helpers at `:12`; suites at `:35`, `:49`, `:66`, `:94` cover code blocks, quote blocks, last command, and aggregate copy targets.
- inputs_outputs_state: Inputs are session transcripts, assistant messages/tool calls/images, terminal image protocol, and copy source definitions. Outputs are rendered components/chat container state and copy target lists.
- gates_or_invariants: Initial render must use correct transcript source, honor clear history, replay images only when supported, and generate stable copy targets from code/quotes/commands.
- dependencies_and_callers: Tests `UiHelpers.renderInitialMessages` and copy target utilities used by interactive TUI.
- edge_cases_or_failure_modes: Empty transcript, startup metadata, image content in transcript, unsupported terminal protocol, multiple code/quote blocks, and assistant tool calls.
- validation_or_tests: Directory is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1677 `file` `packages/agent/src/compaction/index.ts`
- cursor: `[_]`
- core_role: Barrel export surface for agent compaction modules.
- algorithmic_behavior: Re-exports compaction submodules at `packages/agent/src/compaction/index.ts:5`-`:13`, including branch summarization, compaction, entries, errors, messages, OpenAI formatting, pruning, shake, and utilities.
- inputs_outputs_state: No runtime state of its own; input is import path, output is module export namespace.
- gates_or_invariants: Uses star exports consistent with repo barrel convention; ambiguity would need removal of redundant paths.
- dependencies_and_callers: Imported by agent/coding-agent compaction consumers.
- edge_cases_or_failure_modes: Export name collisions if submodules introduce duplicates.
- validation_or_tests: Type/build checks validate barrel surface.
- skip_candidate: `yes: export barrel only, no algorithm beyond API routing`

### OH_MY_HUMANIZE_MAIN-HZ-1707 `file` `packages/ai/src/dialect/glm.ts`
- cursor: `[_]`
- core_role: GLM dialect renderer/scanner for in-band tool calls, tool responses, and thinking tags.
- algorithmic_behavior: Marker constants at `packages/ai/src/dialect/glm.ts:28`; scanner state union at `:61`; `GLMInbandScanner` at `:78`; tag search helpers at `:373`; rendering helpers at `:392`-`:420`; dialect definition at `:445`.
- inputs_outputs_state: Inputs are streamed text fragments, `ToolCall`s, `DialectToolResult`s, transcript messages, and rendering options. Outputs are parsed tool call events/thinking/text or rendered GLM transcript strings.
- gates_or_invariants: Scanner state transitions distinguish outside/thinking/name/body/key/value; tags delimit args and responses; rendering must preserve tool arg shape and transcript role order.
- dependencies_and_callers: Used by AI dialect layer for GLM/Zhipu-compatible providers and tool-calling.
- edge_cases_or_failure_modes: Split tags across chunks, malformed arg tags, nested/unterminated thinking/tool tags, and mixed tool/text output.
- validation_or_tests: Catalog/provider Zhipu/GLM tests and stream markup tests cover adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1737 `file` `packages/ai/src/providers/google-gemini-cli.ts`
- cursor: `[_]`
- core_role: Stream provider implementation for Google Cloud Code Assist/Gemini CLI and Antigravity-compatible models, including OAuth credential parsing, endpoint fallback, SSE decoding, tool calls, thinking, retries, and request building.
- algorithmic_behavior: Credential schema/parsing at `packages/ai/src/providers/google-gemini-cli.ts:189` and `:225`; refresh check at `:259`; stream entry at `:337`; endpoint selection and last-good Antigravity state at `:390`; SSE response streaming at `:494`; text/thinking/tool-call event emission at `:529`-`:605`; finish/usage mapping at `:609` and `:624`; retry/endpoint loop at `:657`; Antigravity session/request helpers at `:828`-`:950`; `buildRequest` at `:950`.
- inputs_outputs_state: Inputs are model, context, OAuth API key JSON, project ID, provider session state, endpoint mode, headers, tools, abort signal, fetch override, payload/SSE hooks. Outputs are `AssistantMessageEventStream`, final assistant message, updated last-good endpoint, raw request dump/error messages, and costed usage.
- gates_or_invariants: Requires OAuth; expired credentials fail before POST; pre-response watchdog clears after headers; 429/5xx can fallback endpoints; empty streams retry; tool call IDs are generated if missing/duplicate; prompt block reasons throw; Claude thinking beta header only when needed.
- dependencies_and_callers: Depends on catalog Gemini headers/model wire profiles, SSE reader, retry, cost calculation, auth validation, stream helpers, and provider registry.
- edge_cases_or_failure_modes: Expired tokens, Antigravity daily vs sandbox fallback, empty response streams, prompt block feedback, SSE error chunks, duplicated tool IDs, finish reason error mapping, aborted wait/retry, validation-required URLs, and last response id leakage.
- validation_or_tests: Gemini thinking/Antigravity/catalog tests exercise request shape and stream behavior; no direct assigned provider test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1767 `file` `packages/ai/src/registry/anthropic.ts`
- cursor: `[_]`
- core_role: Provider registry descriptor for Anthropic OAuth/login and model/provider availability.
- algorithmic_behavior: `anthropicProvider` exported at `packages/ai/src/registry/anthropic.ts:6` with provider metadata and login/auth behavior.
- inputs_outputs_state: Inputs are registry discovery/login calls and Anthropic credentials. Outputs are provider descriptor consumed by auth/model registry.
- gates_or_invariants: Anthropic provider metadata must align with OAuth/API auth defaults and catalog models.
- dependencies_and_callers: Used by AI registry and coding-agent login/model flows.
- edge_cases_or_failure_modes: Misaligned provider id/auth type causes credential lookup/model availability issues.
- validation_or_tests: Auth storage override and model registry OAuth tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1797 `file` `packages/ai/src/registry/nanogpt.ts`
- cursor: `[_]`
- core_role: NanoGPT provider registry descriptor and API-key login validator.
- algorithmic_behavior: `loginNanoGPT` uses `createApiKeyLogin` at `packages/ai/src/registry/nanogpt.ts:5`; `nanogptProvider` metadata at `:18`.
- inputs_outputs_state: Inputs are NanoGPT API key and models endpoint response. Outputs are login success/error and provider registry entry.
- gates_or_invariants: Login validates via models endpoint rather than model entitlement.
- dependencies_and_callers: Used by `/login` and model registry; tested by `nanogpt-login.test.ts`.
- edge_cases_or_failure_modes: Provider validation endpoint errors, missing entitlement, invalid API key.
- validation_or_tests: Assigned NanoGPT login tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1827 `file` `packages/ai/src/registry/xiaomi.ts`
- cursor: `[_]`
- core_role: Xiaomi provider registry descriptor.
- algorithmic_behavior: `xiaomiProvider` exported at `packages/ai/src/registry/xiaomi.ts:4` with provider metadata.
- inputs_outputs_state: Inputs are registry queries/auth discovery. Output is provider descriptor.
- gates_or_invariants: Provider id/base auth fields must match catalog/provider definitions.
- dependencies_and_callers: Used by AI provider registry/model discovery.
- edge_cases_or_failure_modes: Misconfigured descriptor would make models unavailable or auth fail.
- validation_or_tests: Catalog Xiaomi filtering tests likely validate related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1857 `file` `packages/ai/src/utils/retry-after.ts`
- cursor: `[_]`
- core_role: Parses retry-after/rate-limit reset hints from headers/errors and formats retry-aware error messages.
- algorithmic_behavior: Public formatter at `packages/ai/src/utils/retry-after.ts:5`; header extraction at `:19` and `:31`; recursive header extraction at `:40`; case-insensitive header lookup at `:47`; `Retry-After` seconds/date parsing at `:62`; reset timestamp parsing at `:82`.
- inputs_outputs_state: Inputs are unknown errors and `Headers`/record-like headers. Outputs are retry-after milliseconds or error message with `retry-after-ms=` hint.
- gates_or_invariants: Existing hint in message is not duplicated; negative/invalid dates are ignored; reset headers support seconds or milliseconds.
- dependencies_and_callers: Used by provider retry/error handling.
- edge_cases_or_failure_modes: Nested error response headers, string records, HTTP date parsing, zero/negative reset deltas.
- validation_or_tests: Indirectly covered by provider error tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1887 `file` `packages/catalog/src/provider-models/bundled-references.ts`
- cursor: `[_]`
- core_role: Builds model-spec reference maps from bundled models for provider discovery fallback/metadata reuse.
- algorithmic_behavior: `toModelSpec` at `packages/catalog/src/provider-models/bundled-references.ts:11`; `createBundledReferenceMap` at `:16`; resolver factory at `:26`.
- inputs_outputs_state: Inputs are `Model<TApi>` entries and optional key function. Outputs are `Map<string, ModelSpec<TApi>>` and resolver function.
- gates_or_invariants: Converts runtime model back to mutable spec-like object while preserving relevant metadata; lookup keys must be stable.
- dependencies_and_callers: Used by OpenAI-compatible provider discovery and generator fallback.
- edge_cases_or_failure_modes: Duplicate keys overwrite earlier entries; missing reference means resolver returns undefined.
- validation_or_tests: Catalog provider tests for reference fallback and issue regressions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1917 `file` `packages/coding-agent/src/capability/fs.ts`
- cursor: `[_]`
- core_role: Cached filesystem capability utilities for discovery/config walk-up.
- algorithmic_behavior: Caches at `packages/coding-agent/src/capability/fs.ts:4`; path resolution at `:7`; cached file read at `:11`; cached dir entries/listing at `:37`/`:53`; walk-up at `:58`; repo root finding at `:84`; stats/clear/invalidate at `:97`-`:109`.
- inputs_outputs_state: Inputs are file/dir paths and predicates. Outputs are file text/null, dir entries, upward search result, repo root, and cache stats.
- gates_or_invariants: Paths are resolved before cache keys; missing files return null; invalidation targets caches for changed path.
- dependencies_and_callers: Used by discovery providers and capability scans.
- edge_cases_or_failure_modes: Stale cache without invalidation, permission/read errors, symlink/cwd resolution, and walk-up root termination.
- validation_or_tests: Discovery tests exercise behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1947 `file` `packages/coding-agent/src/cli/grep-cli.ts`
- cursor: `[_]`
- core_role: CLI wrapper for native grep/search functionality with argument parsing and formatted output.
- algorithmic_behavior: Args interface at `packages/coding-agent/src/cli/grep-cli.ts:11`; parser at `:25`; runner at `:70`; help at `:133`.
- inputs_outputs_state: Inputs are CLI args, pattern/path/options. Outputs are search results printed to stdout/stderr and exit status.
- gates_or_invariants: Parser returns undefined for help/invalid cases; runner delegates to native grep and honors options.
- dependencies_and_callers: CLI entry uses this command; depends on native grep/search utilities and output formatting.
- edge_cases_or_failure_modes: Missing pattern, invalid flags, no matches, binary files, path errors.
- validation_or_tests: Grep CLI tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1977 `file` `packages/coding-agent/src/commands/auth-gateway.ts`
- cursor: `[_]`
- core_role: CLI command class for auth gateway operations.
- algorithmic_behavior: `AuthGateway` command exported at `packages/coding-agent/src/commands/auth-gateway.ts:13`; it wires command-line invocation into auth gateway handling.
- inputs_outputs_state: Inputs are CLI flags/args and auth settings. Outputs are auth gateway process/result status.
- gates_or_invariants: Command lifecycle is mediated by Cliffy `Command`; errors propagate through command framework.
- dependencies_and_callers: Used by coding-agent CLI command registry.
- edge_cases_or_failure_modes: Missing auth config, port/startup failures, CLI misuse.
- validation_or_tests: Auth command tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2007 `file` `packages/coding-agent/src/commit/index.ts`
- cursor: `[_]`
- core_role: Commit command public module surface.
- algorithmic_behavior: Re-exports `runCommitCommand` from `./pipeline` at `packages/coding-agent/src/commit/index.ts:5`.
- inputs_outputs_state: No state of its own; import path maps to pipeline command implementation.
- gates_or_invariants: Export remains stable for callers.
- dependencies_and_callers: Used by CLI/slash command commit flows.
- edge_cases_or_failure_modes: Broken re-export if pipeline path changes.
- validation_or_tests: Build/type checks and commit command tests cover indirectly.
- skip_candidate: `yes: export shim only`

### OH_MY_HUMANIZE_MAIN-HZ-2037 `file` `packages/coding-agent/src/debug/profiler.ts`
- cursor: `[_]`
- core_role: CPU profile and heap snapshot helpers for coding-agent debug tooling.
- algorithmic_behavior: CPU profile interfaces at `packages/coding-agent/src/debug/profiler.ts:5`; markdown formatter at `:40`; `startCpuProfile` at `:115`; heap snapshot types and generator at `:144`/`:152`.
- inputs_outputs_state: Inputs are runtime profiler data/heap state. Outputs are markdown profile summaries and heap snapshot data.
- gates_or_invariants: Formatter expects Chrome/V8 profile JSON shape; profile session exposes stop/finalization.
- dependencies_and_callers: Debug commands and diagnostics use this module; depends on Bun/V8 profiler APIs and logger.
- edge_cases_or_failure_modes: Malformed profile JSON, missing timing samples, huge heap snapshots, profiling unsupported runtime.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2067 `file` `packages/coding-agent/src/discovery/windsurf.ts`
- cursor: `[_]`
- core_role: Discovery provider for Windsurf MCP servers and rules.
- algorithmic_behavior: Provider constants at `packages/coding-agent/src/discovery/windsurf.ts:29`; server config parser at `:37`; `loadMCPServers` at `:63`; `loadRules` at `:100`.
- inputs_outputs_state: Inputs are Windsurf config files/rule directories and load context. Outputs are `MCPServer` and `Rule` discovery results plus warnings.
- gates_or_invariants: Server entries must parse to supported command/url config; rules are loaded from expected Windsurf locations with provider metadata.
- dependencies_and_callers: Discovery framework calls provider; depends on file capability utilities and config parsing.
- edge_cases_or_failure_modes: Missing config, malformed server entries, unsupported shapes, inaccessible rule files.
- validation_or_tests: Discovery test directory likely covers analogous providers; no direct Windsurf assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2097 `file` `packages/coding-agent/src/extensibility/shared-events.ts`
- cursor: `[_]`
- core_role: Shared type contract for extension event payloads and hook result shapes across session, context, agent, turn, compaction, retry, TTS, todo, and tool events.
- algorithmic_behavior: Session event interfaces start at `packages/coding-agent/src/extensibility/shared-events.ts:28`; tree/goal events at `:108` and `:144`; union at `:150`; context/agent/turn at `:177`-`:204`; compaction/retry/TTS/todo/tool event results at `:216`-`:356`.
- inputs_outputs_state: Inputs are runtime event data emitted by session/agent/tool layers. Outputs are typed extension hook payloads and result objects that can mutate/cancel/augment behavior.
- gates_or_invariants: Event result types define what extensions may change; before-events expose cancellation/override fields while after-events are observational.
- dependencies_and_callers: Used by extension runtime/API and event bus.
- edge_cases_or_failure_modes: Extension returns malformed result, missing event fields, and version drift between runtime emitter and shared event type.
- validation_or_tests: Extensibility tests validate loader/event behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2127 `file` `packages/coding-agent/src/internal-urls/parse.ts`
- cursor: `[_]`
- core_role: Parser for internal URL strings preserving scheme/host/path/query/hash components for coding-agent internal protocols.
- algorithmic_behavior: Regexes at `packages/coding-agent/src/internal-urls/parse.ts:14`; `parseInternalUrl` at `:23` splits scheme/host/path and parses query/hash without relying solely on `URL`.
- inputs_outputs_state: Input is URL-like string. Output is `InternalUrl` structure.
- gates_or_invariants: Scheme must match URL scheme pattern; host/path extraction handles missing components.
- dependencies_and_callers: Used by tools/write/read/internal URL dispatch.
- edge_cases_or_failure_modes: No scheme, empty host, encoded query/hash, unusual scheme characters.
- validation_or_tests: Internal URL tool tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2157 `file` `packages/coding-agent/src/mcp/oauth-credentials.ts`
- cursor: `[_]`
- core_role: Credential lookup/removal helpers for managed MCP OAuth credentials.
- algorithmic_behavior: Lookup interface at `packages/coding-agent/src/mcp/oauth-credentials.ts:12`; URL-derived credential IDs at `:19`; authorization-header gate at `:29`; server lookup at `:34`; generic lookup at `:62`; refresh material selection at `:76`; removal helpers at `:83` and `:95`.
- inputs_outputs_state: Inputs are MCP server config, server URL, credential store, and auth config. Outputs are credential IDs, selected stored credential/config refresh material, or removal side effects.
- gates_or_invariants: Explicit Authorization header suppresses managed OAuth; lookup tries URL-derived IDs; removal only targets managed credential IDs.
- dependencies_and_callers: Used by MCP client/auth flows and credential extraction.
- edge_cases_or_failure_modes: Missing server URL, multiple possible credential IDs, config-vs-stored refresh material precedence, and stale credentials.
- validation_or_tests: MCP discovery/profile tests cover config; OAuth-specific tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2187 `file` `packages/coding-agent/src/modes/loop-limit.ts`
- cursor: `[_]`
- core_role: Parser/runtime for loop mode iteration/time limits.
- algorithmic_behavior: Config/runtime types at `packages/coding-agent/src/modes/loop-limit.ts:1`; unit map at `:23`; arg parser at `:41`; duration parser at `:72`; runtime creation at `:90`; iteration/duration consumption at `:101`/`:111`; descriptions at `:115`/`:122`.
- inputs_outputs_state: Inputs are user arg string and current time. Outputs are parsed config or error string, runtime counters/deadline, boolean continue/expired decisions, and human descriptions.
- gates_or_invariants: Supports count and duration units; invalid parse returns message; iteration limit decrements until exhausted; duration compares against deadline.
- dependencies_and_callers: Used by interactive loop mode/slash command.
- edge_cases_or_failure_modes: Unknown units, zero/negative amounts, combined syntax ambiguity, time boundary exactly at deadline.
- validation_or_tests: Loop mode tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2217 `file` `packages/coding-agent/src/session/client-bridge.ts`
- cursor: `[_]`
- core_role: Interface contract for host/client bridge capabilities: permissions and terminal management.
- algorithmic_behavior: Defines capability, permission tool call, option/outcome, terminal status/output/handle/create params, and `ClientBridge` interface at `packages/coding-agent/src/session/client-bridge.ts:12`-`:73`.
- inputs_outputs_state: Inputs are permission requests and terminal create commands. Outputs are permission decisions and terminal handles/output streams.
- gates_or_invariants: Permission options are constrained to allow/reject once/always; terminal handle must expose write/resize/kill/status/output semantics.
- dependencies_and_callers: Used by session managers and external UI/client integrations.
- edge_cases_or_failure_modes: Bridge not present, rejected permissions, terminal exit/stream errors.
- validation_or_tests: Client bridge tests not assigned.
- skip_candidate: `yes: type contract only, no implementation algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2247 `file` `packages/coding-agent/src/ssh/config-writer.ts`
- cursor: `[_]`
- core_role: Read/update/write helper for OpenSSH config host blocks.
- algorithmic_behavior: Types at `packages/coding-agent/src/ssh/config-writer.ts:10`; reader at `:27`; writer at `:48`; host name validation at `:66`; add/update/remove/list at `:85`, `:124`, `:157`, `:180`.
- inputs_outputs_state: Inputs are config path, host name, host config fields. Outputs are parsed config object, modified config file, validation message, or host list.
- gates_or_invariants: Host names are validated; add/update/remove operate on named Host blocks; write serializes config predictably.
- dependencies_and_callers: SSH setup commands use this module; depends on Bun/fs path operations.
- edge_cases_or_failure_modes: Duplicate host blocks, comments/unknown directives preservation limits, invalid host names, missing file.
- validation_or_tests: SSH config tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2277 `file` `packages/coding-agent/src/task/worktree.ts`
- cursor: `[_]`
- core_role: Task isolation and branch integration engine for capturing baselines/deltas, applying nested repo patches, materializing isolated workspaces, committing task branches, merging branches, and cleanup.
- algorithmic_behavior: Baseline types at `packages/coding-agent/src/task/worktree.ts:14`; repo root gate at `:30`; nested repo discovery at `:46`; untracked patch capture with concurrency limit at `:83`; synthetic tree/delta generation at `:107`/`:139`; nested patch application at `:192`; isolation mode mapping at `:239`/`:261`; `ensureIsolation` PAL fallback loop at `:310`; branch commit at `:379`; sequential cherry-pick merge with stash/lock at `:440`; branch cleanup at `:510`.
- inputs_outputs_state: Inputs are cwd/repo root, baseline state, isolation backend preference, task id/description, patch diffs, nested repos, and branches. Outputs are isolation handle, root/nested patches, task branch commits, merge results, conflicts/stash conflicts, and cleaned branches.
- gates_or_invariants: Requires git repo; excludes submodules as nested repos; dirty state is captured into synthetic trees; unavailable native isolation backends fall back; merges serialize with repo lock and stash uncommitted changes; cleanup attempts backend stop then removes base dir.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-natives` isolation, git utils, worktree dir utilities, logger, and task execution flows.
- edge_cases_or_failure_modes: Nested repos disappear, untracked binary diffs, no root changes but nested changes, git apply failure with logged patch head, cherry-pick conflicts, stash pop conflicts after successful commits, unavailable isolation backends.
- validation_or_tests: Worktree/task tests not assigned directly; behavior is exercised by task/session integration.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2307 `file` `packages/coding-agent/src/tools/fetch.ts`
- cursor: `[_]`
- core_role: URL read/fetch tool implementation with URL normalization/selectors, special site handlers, HTTP fetch, HTML/text/feed/JSON rendering, binary dispatch, image inlining, markit conversion, caching/artifacts, and TUI renderers.
- algorithmic_behavior: URL parser at `packages/coding-agent/src/tools/fetch.ts:179`; MIME/extension classification at `:257`-`:308`; HTML alternate/feed/link extraction at `:410`-`:526`; HTML reader chain at `:608`; binary dispatch helpers at `:753`-`:888`; special handlers at `:1028`; main `renderUrl` pipeline at `:1060`; read URL cache/artifact functions at `:1560`-`:1687`; `executeReadUrl` at `:1702`; TUI renderers at `:1778` and `:1792`.
- inputs_outputs_state: Inputs are tool session, URL/path with optional selectors/raw mode, settings, abort signal, fetch override, model image constraints, HTTP response content type/body. Outputs are text/image `AgentToolResult`, read metadata, cache entry/artifact for truncation, and rendered TUI component.
- gates_or_invariants: `pi-internal://` never externally fetched; special handlers skipped in raw mode; unsupported/too-large/invalid images return metadata; raw mode skips text shaping but binary handling still applies; large output truncates head and persists artifact; cache scoped by session file/cwd and raw flag.
- dependencies_and_callers: Uses web fetch/loadPage, markit converters, archive/sqlite/notebook renderers, special scrapers, settings/storage, image resize, TUI render utilities, and LRU cache.
- edge_cases_or_failure_modes: Collapsed schemes, content-disposition extension hints, mislabeled binary, skipped body for binary types, low-quality JS-heavy HTML, markdown/feed alternates, llms.txt fallback, aborted fetch, unsupported WebP for model, and artifact materialization misses.
- validation_or_tests: Assigned `fetch-binary-dispatch.test.ts`, Kagi/search tests, scraper tests, and markit tests cover major branches.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2337 `file` `packages/coding-agent/src/tools/output-schema-validator.ts`
- cursor: `[_]`
- core_role: Builds and formats JSON-schema output validators for tool results or structured output expectations.
- algorithmic_behavior: Interfaces at `packages/coding-agent/src/tools/output-schema-validator.ts:19`; `buildOutputValidator` at `:51`; failure summary at `:80`; required extraction/missing computation at `:91`/`:97`; issue headline/all issue formatting at `:111`/`:124`.
- inputs_outputs_state: Inputs are unknown schema and output value. Outputs are validator object/result, missing required fields, and user-facing issue summaries.
- gates_or_invariants: Invalid schema produces build failure; required fields only apply to object values; issue formatting is compact and actionable.
- dependencies_and_callers: Uses AI JSON schema validator utilities; called by tool output schema enforcement.
- edge_cases_or_failure_modes: Non-object outputs, malformed schemas, multiple validation issues, no issue details.
- validation_or_tests: Tool schema validation tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2367 `file` `packages/coding-agent/src/tts/wav.ts`
- cursor: `[_]`
- core_role: Encodes Float32 PCM samples into 16-bit PCM WAV bytes.
- algorithmic_behavior: WAV constants at `packages/coding-agent/src/tts/wav.ts:1`; `encodeWav` at `:14`; ASCII chunk writer at `:56`.
- inputs_outputs_state: Inputs are `Float32Array` samples and sample rate. Output is `Uint8Array` WAV file with RIFF/WAVE/fmt/data headers.
- gates_or_invariants: Samples are clamped to int16 range; header byte counts and little-endian fields must match PCM16 mono format.
- dependencies_and_callers: Used by TTS/audio output paths.
- edge_cases_or_failure_modes: NaN/out-of-range sample values, huge arrays, invalid sample rate.
- validation_or_tests: TTS WAV tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2397 `file` `packages/coding-agent/src/utils/open.ts`
- cursor: `[_]`
- core_role: Cross-platform helper to open URLs/paths, including WSL local path conversion.
- algorithmic_behavior: URL scheme pattern at `packages/coding-agent/src/utils/open.ts:6`; WSL path resolver at `:8`; `openPath` at `:35`.
- inputs_outputs_state: Input is URL or local path. Output is launched platform opener process side effect.
- gates_or_invariants: Existing WSL local paths are converted appropriately; URL schemes are detected before treating as path.
- dependencies_and_callers: Used by CLI/UI commands that open files/URLs; depends on platform opener commands.
- edge_cases_or_failure_modes: Missing opener, WSL path not existing, paths that look like schemes, spaces/shell escaping.
- validation_or_tests: Open utility tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2427 `file` `packages/coding-agent/src/workflow/node-runtime.ts`
- cursor: `[_]`
- core_role: Runtime dispatcher for workflow graph node execution across agent, script, human, and review node kinds.
- algorithmic_behavior: Node input/output/host types at `packages/coding-agent/src/workflow/node-runtime.ts:5`; dispatcher `executeWorkflowNode` at `:85`; agent execution at `:106`; script at `:134`; script context snapshot at `:165`; human at `:192`; review at `:212`; review verdict state path at `:253`.
- inputs_outputs_state: Inputs are workflow node, activation, state, resources, host adapters, abort signal. Outputs are workflow state patches, review verdict output, or runtime errors.
- gates_or_invariants: Unknown node kinds error; review verdicts must be among declared gates; review verdicts can be written to declared state path; abort signals are passed to host adapters.
- dependencies_and_callers: Used by workflow engine; tests supply host adapters.
- edge_cases_or_failure_modes: Missing host adapter, invalid review verdict, script resource context mismatch, abort propagation.
- validation_or_tests: Assigned `workflow/node-runtime.test.ts` covers dispatch and verdict mapping.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2457 `file` `packages/coding-agent/test/core/helpers.ts`
- cursor: `[_]`
- core_role: Test helper providing fake Python kernel executor.
- algorithmic_behavior: `FakeKernel` class at `packages/coding-agent/test/core/helpers.ts:4` implements `PythonKernelExecutor` for tests.
- inputs_outputs_state: Inputs are fake execution requests. Outputs are mocked kernel responses/state.
- gates_or_invariants: Designed for deterministic tests, not production.
- dependencies_and_callers: Used by coding-agent core tests that need Python kernel abstraction.
- edge_cases_or_failure_modes: Helper may not emulate full kernel behavior; tests should only rely on explicit fake behavior.
- validation_or_tests: Helper supports tests; not independently tested.
- skip_candidate: `yes: test helper, not core runtime`

### OH_MY_HUMANIZE_MAIN-HZ-2487 `file` `packages/coding-agent/test/discovery/agent-discovery-disabled-providers.test.ts`
- cursor: `[_]`
- core_role: Tests agent discovery respects disabled provider settings for Claude plugins.
- algorithmic_behavior: Plugin agent markdown fixture at `packages/coding-agent/test/discovery/agent-discovery-disabled-providers.test.ts:14`; suite at `:22`; enabled and disabled cases at `:69` and `:74`.
- inputs_outputs_state: Inputs are temp plugin agent files and discovery provider settings. Outputs are discovered agent list.
- gates_or_invariants: Claude plugin agents appear only when `claude-plugins` provider is enabled.
- dependencies_and_callers: Tests discovery framework and disabled provider filtering.
- edge_cases_or_failure_modes: Provider disabled while files exist, plugin metadata parsing.
- validation_or_tests: Direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2517 `file` `packages/coding-agent/test/extensibility/legacy-pi-inplace-load.test.ts`
- cursor: `[_]`
- core_role: Regression tests for loading legacy `pi` extensions in-place while remapping imports and preserving asset/dependency resolution.
- algorithmic_behavior: Temp package writer at `packages/coding-agent/test/extensibility/legacy-pi-inplace-load.test.ts:23`; suite at `:34`; tests relative HTML/CSS asset resolution, native extension `node_modules`, legacy `pi-ai` subpath remap, rewriting relative imported source modules, and not rewriting siblings outside graph.
- inputs_outputs_state: Inputs are synthetic extension packages with assets/modules/deps/imports. Outputs are loaded extension behavior and resolved asset/module content.
- gates_or_invariants: `__dirname`-relative assets must resolve from real extension dir; legacy imports remap only inside loaded graph; own deps load natively.
- dependencies_and_callers: Tests extension loader/import remapper.
- edge_cases_or_failure_modes: Relative submodule CSS, `../src` modules, sibling files outside graph, legacy subpath mappings.
- validation_or_tests: Direct extensibility regression suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2547 `file` `packages/coding-agent/test/marketplace/project-scope.test.ts`
- cursor: `[_]`
- core_role: Tests project-scoped plugin registry path resolution and plugin root shadowing.
- algorithmic_behavior: Entry helper at `packages/coding-agent/test/marketplace/project-scope.test.ts:30`; `resolveActiveProjectRegistryPath` suite at `:42`; plugin root shadowing suite at `:137`.
- inputs_outputs_state: Inputs are temp dirs with `.omp`, `.git`, home guard, installed plugin entries. Outputs are registry file path and plugin root list.
- gates_or_invariants: Walk-up finds nearest `.omp`, falls back to `.git`, ignores home `.git`, canonical root path is stable, project plugin ID shadows user plugin ID.
- dependencies_and_callers: Tests marketplace/project registry discovery and Claude plugin root listing.
- edge_cases_or_failure_modes: Nested `.omp`, no project root, home dir false positive, duplicate plugin IDs across scopes.
- validation_or_tests: Direct project scope test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2577 `file` `packages/coding-agent/test/session-manager/subagent-breadcrumb.test.ts`
- cursor: `[_]`
- core_role: Tests session manager breadcrumb isolation between parent sessions and subagent artifact sessions.
- algorithmic_behavior: Breadcrumb/session helpers at `packages/coding-agent/test/session-manager/subagent-breadcrumb.test.ts:16` and `:25`; suite at `:41`; tests parent `--continue` retention at `:80` and stale subagent breadcrumb recovery at `:101`.
- inputs_outputs_state: Inputs are breadcrumb files, parent/subagent JSONL sessions, cwd. Outputs are resolved continuation session.
- gates_or_invariants: Subagent session opened in same terminal must not steal parent continue breadcrumb; stale breadcrumb pointing inside artifacts is recovered.
- dependencies_and_callers: Tests SessionManager session discovery/continuation.
- edge_cases_or_failure_modes: Stale artifact paths, parent/subagent same terminal, JSONL suffix handling.
- validation_or_tests: Direct regression test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2607 `file` `packages/coding-agent/test/slash-commands/tan.test.ts`
- cursor: `[_]`
- core_role: Tests `/tan` slash command routing and raw suffix preservation.
- algorithmic_behavior: Runtime helper at `packages/coding-agent/test/slash-commands/tan.test.ts:5`; suite at `:20`; tests full work item routing at `:21` and multi-word suffix preservation at `:31`.
- inputs_outputs_state: Inputs are slash command text and fake runtime. Outputs are handler invocation payload.
- gates_or_invariants: Full suffix after `/tan` is preserved exactly enough for handler use.
- dependencies_and_callers: Tests slash command registry/handler.
- edge_cases_or_failure_modes: Multi-word suffix, whitespace trimming.
- validation_or_tests: Direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2637 `file` `packages/coding-agent/test/tools/apply-patch-renderer.test.ts`
- cursor: `[_]`
- core_role: Tests TUI rendering/preview behavior for `apply_patch` tool calls and results.
- algorithmic_behavior: Theme/render wait helpers at `packages/coding-agent/test/tools/apply-patch-renderer.test.ts:11` and `:18`; suite at `:43`; tests renderer registration, edit UI result rendering, path/operation/file-count hints, streaming missing end-marker suppression, parse error preview, preview diffs, immediate arg update refresh, and diff separator alignment.
- inputs_outputs_state: Inputs are apply_patch tool args/partial args/results and render context. Outputs are TUI components/text previews.
- gates_or_invariants: Streaming input should not show missing end-marker errors prematurely; malformed complete input shows parse preview; preview refresh bypasses debounce; edit renderer, not generic fallback, is used.
- dependencies_and_callers: Tests tool renderer registry, apply_patch parser/preview, TUI edit renderer.
- edge_cases_or_failure_modes: Partial JSON/tool args, malformed patches, multi-file hints, separator alignment.
- validation_or_tests: Direct renderer test suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2667 `file` `packages/coding-agent/test/tools/fetch-binary-dispatch.test.ts`
- cursor: `[_]`
- core_role: Tests URL read binary dispatch for archives, SQLite, notebooks, unrenderable binaries, UTF-8 octet streams, and hinted binary refetch failure.
- algorithmic_behavior: Session and fetch stubs at `packages/coding-agent/test/tools/fetch-binary-dispatch.test.ts:15`-`:62`; fixture builders at `:69`/`:83`; suite at `:101`; cases at `:114`-`:204`.
- inputs_outputs_state: Inputs are stubbed remote bytes/content-types/content-disposition and tool session. Outputs are text/image tool result content and metadata notices.
- gates_or_invariants: Remote zip lists entries instead of decoded bytes; hinted binary refetch failures return metadata; SQLite/notebook renderers handle bytes; valid UTF-8 octet-stream remains text.
- dependencies_and_callers: Tests `executeReadUrl`/`fetch.ts` binary dispatch, archive/sqlite/notebook renderers.
- edge_cases_or_failure_modes: Unrenderable binary, failed second binary fetch, MIME vs extension hints, octet-stream text.
- validation_or_tests: Direct fetch binary contract suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2697 `file` `packages/coding-agent/test/tools/read-directory-range.test.ts`
- cursor: `[_]`
- core_role: Regression tests that read tool directory listings honor line selectors/ranges.
- algorithmic_behavior: Output/session helpers at `packages/coding-agent/test/tools/read-directory-range.test.ts:10` and `:17`; suite at `:32`; tests full listing, `:start-end`, `:start`, and beyond-end notice at `:49`, `:58`, `:70`, `:81`.
- inputs_outputs_state: Inputs are temp directory with many files and read path selectors. Outputs are sliced directory listing text or clear notice.
- gates_or_invariants: Offset selectors must not be silently dropped; beyond-end returns explanatory notice, not empty body.
- dependencies_and_callers: Tests read tool directory listing path selector logic.
- edge_cases_or_failure_modes: Off-by-one range, start-to-end selector, range beyond file count.
- validation_or_tests: Direct regression suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2727 `file` `packages/coding-agent/test/tools/web-search-kagi.test.ts`
- cursor: `[_]`
- core_role: Tests Kagi web search provider error mapping, response parsing, auth header, and availability.
- algorithmic_behavior: Fake auth storage at `packages/coding-agent/test/tools/web-search-kagi.test.ts:7`; error suite at `:19`; parsing suite at `:63`; availability suite at `:226`.
- inputs_outputs_state: Inputs are mocked Kagi HTTP responses, credentials, categorized data, direct_answer, empty data. Outputs are provider result objects/errors and availability boolean.
- gates_or_invariants: Auth failures map to compact provider-tagged errors; non-JSON errors fall back to text; categorized search/video/news/related results parse; Authorization uses Bearer.
- dependencies_and_callers: Tests Kagi search provider.
- edge_cases_or_failure_modes: Empty 5xx body, non-JSON error body, empty data object, missing credential.
- validation_or_tests: Direct provider test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2757 `file` `packages/coding-agent/test/workflow/node-runtime.test.ts`
- cursor: `[_]`
- core_role: Tests workflow node runtime adapter dispatch and review verdict state patching.
- algorithmic_behavior: Workflow fixtures at `packages/coding-agent/test/workflow/node-runtime.test.ts:6`; activation helper at `:51`; suite at `:61`; tests agent dispatch, script/human dispatch, abort signal pass-through, valid review verdict mapping, state path writes, and invalid verdict rejection at `:62`-`:196`.
- inputs_outputs_state: Inputs are parsed workflow nodes, activation/state/resources, fake host adapters, abort signals. Outputs are host calls, state patches, or runtime errors.
- gates_or_invariants: Node kinds dispatch to dedicated adapters; review verdicts must be declared gates; state path writes exactly where declared.
- dependencies_and_callers: Tests `workflow/node-runtime.ts`.
- edge_cases_or_failure_modes: Invalid review verdict, missing gates, abort signal propagation.
- validation_or_tests: Direct workflow runtime validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2787 `file` `packages/mnemopi/src/core/aaak.ts`
- cursor: `[_]`
- core_role: Text compaction/encoding utility mapping categories and phrases to compact tokens.
- algorithmic_behavior: Category and phrase maps at `packages/mnemopi/src/core/aaak.ts:1` and `:17`; structural replacements at `:49`; reverse map helper at `:71`; phrase sorting at `:83`; literal replacement at `:86`; category/phrase/structural/paren transforms at `:90`, `:101`, `:109`, `:117`; `encode` at `:121`.
- inputs_outputs_state: Input is text. Output is compacted/encoded text with category prefixes, phrase substitutions, structural replacements, and compact parentheses.
- gates_or_invariants: Longer phrases are sorted first to prevent shorter replacements from preempting; reverse maps derive decode lookup constants.
- dependencies_and_callers: Used by mnemopi compaction/search/display flows.
- edge_cases_or_failure_modes: Overlapping phrase replacements, case sensitivity, structural replacements interacting with phrase map.
- validation_or_tests: Mnemopi tests likely cover via core behavior; no direct assigned aaak test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2817 `file` `packages/mnemopi/src/core/triples.ts`
- cursor: `[_]`
- core_role: SQLite-backed triple store for mnemopi facts with default path migration, CRUD/query/import/export, and legacy DB copy.
- algorithmic_behavior: Triple row/options types at `packages/mnemopi/src/core/triples.ts:7`; path resolution at `:72`-`:117`; `initTriples` at `:120`; normalization helpers at `:156`-`:217`; `TripleStore` class at `:224`; top-level `addTriple` and `queryTriples` at `:431` and `:445`.
- inputs_outputs_state: Inputs are database path/env, triple fields, query filters, import rows, time/source/confidence options. Outputs are stored/query `TripleRow`s, import stats, and default DB files.
- gates_or_invariants: Legacy DB is copied to new default path when appropriate; required import text fields are normalized; same-content checks avoid duplicate import behavior; dates default to today/created_at.
- dependencies_and_callers: Used by mnemopi core/provider tools; depends on Bun SQLite/database APIs and fs/path.
- edge_cases_or_failure_modes: Legacy path migration failure, missing required fields, null/undefined content, duplicate rows, invalid confidence/date filters.
- validation_or_tests: Provider parity tests exercise write/query/import/export behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2847 `file` `packages/tui/src/components/image.ts`
- cursor: `[_]`
- core_role: TUI component for inline image rendering with Kitty graphics, budgets, transmission IDs, and placeholder lines.
- algorithmic_behavior: Image options at `packages/tui/src/components/image.ts:16`; ID seed at `:42`; `ImageBudget` class at `:63`; cap normalization at `:296`; `Image` component at `:301`.
- inputs_outputs_state: Inputs are image data/mime/dimensions/options/theme/budget and terminal capabilities. Outputs are TUI render output, Kitty transmit sequences, placeholder lines, and tracked image IDs.
- gates_or_invariants: Default max inline images is 8; budget prevents too many transmissions; terminal protocol support determines output strategy; dimensions/caps are normalized.
- dependencies_and_callers: Uses Kitty graphics helpers, TUI component system, terminal capability detection.
- edge_cases_or_failure_modes: Unsupported terminal, image budget exhausted, huge images, duplicate IDs, placeholder grid too large.
- validation_or_tests: TUI render/image tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2877 `file` `python/robomp/web/src/main.tsx`
- cursor: `[_]`
- core_role: Web app bootstrap entrypoint for robomp UI.
- algorithmic_behavior: Gets `#app` element at `python/robomp/web/src/main.tsx:6` and mounts React app/root.
- inputs_outputs_state: Input is browser DOM containing `#app`. Output is mounted web UI.
- gates_or_invariants: Requires app container to exist.
- dependencies_and_callers: Vite/React web bundle entry.
- edge_cases_or_failure_modes: Missing root element causes mount failure.
- validation_or_tests: Web UI tests not assigned.
- skip_candidate: `yes: bootstrap glue only`

### OH_MY_HUMANIZE_MAIN-HZ-2907 `file` `crates/pi-shell/src/minimizer/filters/gh.rs`
- cursor: `[_]`
- core_role: Output minimizer for GitHub CLI commands, preserving raw mode when necessary and extracting useful PR/issue/check/run information.
- algorithmic_behavior: Subcommand support at `crates/pi-shell/src/minimizer/filters/gh.rs:8`; main filter at `:25`; raw-mode preservation at `:50`; PR/issue filtering at `:89`; checks filtering at `:107`; run filtering at `:172`; markdown noise removal at `:180`; failure signal detection at `:226`.
- inputs_outputs_state: Inputs are minimizer context, gh subcommand, raw output, and exit code. Outputs are minimized output with retained failure signals or raw output when unsafe.
- gates_or_invariants: Raw mode is preserved for commands/options where minimization would lose semantics; failure signals keep relevant lines.
- dependencies_and_callers: Used by pi-shell command output minimizer.
- edge_cases_or_failure_modes: Markdown-heavy issue bodies, check failures, nonzero exit output, subcommands with machine-readable output, false failure signal positives.
- validation_or_tests: pi-shell minimizer tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2937 `file` `packages/ai/src/registry/oauth/minimax-code.ts`
- cursor: `[_]`
- core_role: OAuth/API-key style login flow for MiniMax Code international and China endpoints.
- algorithmic_behavior: Auth/API constants at `packages/ai/src/registry/oauth/minimax-code.ts:19`; `loginMiniMaxCode` at `:31`; shared base URL flow at `:35`; CN variant at `:80`.
- inputs_outputs_state: Inputs are OAuth controller, region/base URLs, user token entry/validation model. Outputs are stored/validated credential string.
- gates_or_invariants: Region-specific auth/API URLs must match; validation uses `MiniMax-M3`.
- dependencies_and_callers: Used by AI registry login for MiniMax Code providers.
- edge_cases_or_failure_modes: Wrong regional endpoint, invalid token, validation request failure.
- validation_or_tests: Login tests not assigned for MiniMax.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2967 `file` `packages/coding-agent/src/autoresearch/tools/run-experiment.ts`
- cursor: `[_]`
- core_role: Autoresearch tool that runs experiment commands, captures output/progress, records metrics, and renders status/results.
- algorithmic_behavior: Ark schema at `packages/coding-agent/src/autoresearch/tools/run-experiment.ts:28`; `createRunExperimentTool` at `:47`; subprocess executor at `:269`; run text builder at `:344`; status renderer at `:385`; detail type guards at `:399` and `:404`.
- inputs_outputs_state: Inputs are command/cwd/timeout/metric metadata, session state/storage, abort signal, and progress output. Outputs are tool result details, experiment DB rows, captured stdout/stderr preview, metric/best state, and TUI status text.
- gates_or_invariants: Args schema validates command shape; subprocess respects abort/timeout; output preview is bounded; run details must type-check for renderer.
- dependencies_and_callers: Used by autoresearch slash/tool framework; depends on storage/state math, Bun process APIs, TUI theme.
- edge_cases_or_failure_modes: Nonzero exit, timeout, abort, missing metric, long output, invalid details in renderer.
- validation_or_tests: Assigned autoresearch-state tests cover state and command hook behavior; run-experiment-specific tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2997 `file` `packages/coding-agent/src/commit/changelog/index.ts`
- cursor: `[_]`
- core_role: Agentic changelog proposal/application flow for commit pipeline.
- algorithmic_behavior: Constants at `packages/coding-agent/src/commit/changelog/index.ts:11`; `runChangelogFlow` at `:40`; `applyChangelogProposals` at `:98`; diff truncation at `:139`; existing entry formatting at `:144`; entry application/deletion/merge/render/normalize at `:157`-`:226`.
- inputs_outputs_state: Inputs are package changelog paths, diff text, proposal entries/deletions, max diff chars, and LLM/agent proposal source. Outputs are updated Unreleased sections and proposal records.
- gates_or_invariants: Diff is truncated to max chars; entries are normalized into known changelog sections; deletions and merges preserve section ordering under Unreleased.
- dependencies_and_callers: Used by commit command pipeline and changelog category constants.
- edge_cases_or_failure_modes: Missing Unreleased section, duplicate entries, deletion misses, overlong diffs, unknown sections.
- validation_or_tests: Changelog/commit tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3027 `file` `packages/coding-agent/src/eval/js/context-manager.ts`
- cursor: `[_]`
- core_role: Manages persistent JavaScript eval worker sessions, reset/dispose, run dispatch, tool-call bridge, abort/timeout handling, worker-host spawning, and inline fallback.
- algorithmic_behavior: Public execution/reset/dispose at `packages/coding-agent/src/eval/js/context-manager.ts:82`, `:126`, `:133`; smoke worker probe at `:154`; per-run pending state at `:178`; session acquisition/startup and inline retry at `:233`; init handshake at `:294`; message routing at `:337`; tool-call bridge at `:365`; pending settlement at `:391`; kill/cleanup at `:402`; worker spawn via `workerHostEntry` at `:486`; Bun worker wrapper/close handshake at `:501`; inline fallback at `:572`.
- inputs_outputs_state: Inputs are session key/id, cwd, code, filename, local roots, tool session, run state callbacks, reset flag, timeout, abort signal. Outputs are eval result, display/text callbacks, tool replies, worker session cache, or errors.
- gates_or_invariants: Concurrent resets coalesce; worker `ready` listener attaches before init; init timeout is enforced; abort kills worker to interrupt sync code; failed real worker falls back to inline once; pending tool calls are aborted on kill.
- dependencies_and_callers: Used by JS eval tool/cells; depends on worker protocol/core, tool caller, worker host entry contract, logger, Snowflake IDs.
- edge_cases_or_failure_modes: Bun worker load crash after constructor, dropped ready messages, worker close timeout, inline fallback cannot interrupt sync loops, tool call after run settled, concurrent reset/start races.
- validation_or_tests: Smoke test path plus JS eval tests elsewhere; workflow worker-host rules apply.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3057 `file` `packages/coding-agent/src/extensibility/extensions/loader.ts`
- cursor: `[_]`
- core_role: Extension runtime/loader/discovery implementation for loading extension factories, registering handlers, resolving extension entrypoints, and scanning configured extension dirs.
- algorithmic_behavior: Factory extraction at `packages/coding-agent/src/extensibility/extensions/loader.ts:47`; runtime class at `:62`; concrete API at `:124`; extension creation/load at `:271`/`:285`; factory loader at `:317`; multi-load at `:333`; manifest read at `:365`; entry resolution at `:389`; directory discovery at `:445`; configured path discovery at `:495`; discover-and-load at `:579`.
- inputs_outputs_state: Inputs are extension paths/dirs, cwd, package manifests, event bus, module exports. Outputs are loaded extension records, registered handlers, API callbacks, load errors/warnings.
- gates_or_invariants: Runtime must initialize before API use; extension files/manifests determine entrypoints; handler registration is async-safe; discovery filters valid extension files/dirs.
- dependencies_and_callers: Used by coding-agent extensibility system; tested by legacy-pi in-place load.
- edge_cases_or_failure_modes: Missing package manifest, invalid default export, relative imports/assets, legacy import remapping, disabled extensions, duplicate handlers, load failure isolation.
- validation_or_tests: Assigned legacy extension loader tests validate key paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3087 `file` `packages/coding-agent/src/markit/converters/xlsx.ts`
- cursor: `[_]`
- core_role: XLSX-to-Markdown converter for markit document rendering.
- algorithmic_behavior: Converter class at `packages/coding-agent/src/markit/converters/xlsx.ts:48`; text and array helpers at `:164` and `:170`. It reads workbook/shared strings/relationships/worksheets and emits markdown tables.
- inputs_outputs_state: Inputs are XLSX zip/package buffer and relationship XML. Outputs are markdown sheet sections/tables.
- gates_or_invariants: Supports `.xlsx` extension and official MIME; relationship targets map sheets; shared string rich text resolves to text.
- dependencies_and_callers: Used by markit conversion pipeline and fetch binary dispatch.
- edge_cases_or_failure_modes: Absolute relationship target, missing shared strings, empty rows/cells, rich text runs, multiple sheets.
- validation_or_tests: Assigned markit converters tests cover XLSX table and absolute rel target.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3117 `file` `packages/coding-agent/src/modes/components/eval-execution.ts`
- cursor: `[_]`
- core_role: TUI component for displaying Python/JS eval execution previews and output.
- algorithmic_behavior: Display constants at `packages/coding-agent/src/modes/components/eval-execution.ts:19`; language type at `:22`; `EvalExecutionComponent` at `:24`.
- inputs_outputs_state: Inputs are execution language, code/status/output details, theme. Outputs are rendered TUI component lines.
- gates_or_invariants: Preview lines and max display chars are bounded to avoid UI overflow.
- dependencies_and_callers: Used by eval mode/tool UI.
- edge_cases_or_failure_modes: Long output, many lines, ANSI/control text, error state.
- validation_or_tests: UI tests not assigned directly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3147 `file` `packages/coding-agent/src/modes/components/show-images-selector.ts`
- cursor: `[_]`
- core_role: Small TUI selector component for show-images mode/state.
- algorithmic_behavior: `ShowImagesSelectorComponent` class at `packages/coding-agent/src/modes/components/show-images-selector.ts:8`.
- inputs_outputs_state: Inputs are selector state/options/theme. Outputs are rendered selector UI and user selection changes.
- gates_or_invariants: Component should render available image-display choices consistently with mode state.
- dependencies_and_callers: Used by interactive mode image display controls.
- edge_cases_or_failure_modes: Empty options, narrow terminal, theme color mismatch.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3177 `file` `packages/coding-agent/src/modes/controllers/streaming-reveal.ts`
- cursor: `[_]`
- core_role: Controller for progressively revealing streamed assistant content in the TUI at a stable frame rate while handling thinking visibility and grapheme-safe slicing.
- algorithmic_behavior: Timing/step constants at `packages/coding-agent/src/modes/controllers/streaming-reveal.ts:7`; grapheme counting/cache at `:22`; block unit counter at `:49`; slicing at `:73`; visible unit counting at `:86`; display message builder at `:118`; step sizing at `:143`; controller class at `:147`.
- inputs_outputs_state: Inputs are assistant message content blocks, hide-thinking flag, target component, timers/backlog. Outputs are partial display messages and component updates.
- gates_or_invariants: Grapheme boundaries are preserved; thinking blocks can be hidden; minimum/catchup step prevents stalled reveal while smoothing backlog; cache limits repeated counting.
- dependencies_and_callers: Used by interactive mode streaming assistant renderer.
- edge_cases_or_failure_modes: Emoji/combining graphemes, hidden thinking with visible text, sudden large backlog, content block type transitions.
- validation_or_tests: UI controller tests not directly assigned; input-controller expansion and segment tests cover adjacent controllers/components.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3207 `file` `packages/coding-agent/src/slash-commands/helpers/reset-usage.ts`
- cursor: `[_]`
- core_role: Helper for formatting Codex reset-credit usage accounts and redeem outcomes.
- algorithmic_behavior: Provider constant at `packages/coding-agent/src/slash-commands/helpers/reset-usage.ts:8`; account type at `:11`; account conversion at `:28`; redeem outcome description at `:49`.
- inputs_outputs_state: Inputs are reset credit account statuses and redeem outcome. Outputs are UI/account summaries and human-readable outcome strings.
- gates_or_invariants: Provider ID is fixed to `openai-codex`; outcome labels should be user-facing and account-specific.
- dependencies_and_callers: Used by slash commands around reset usage/credits.
- edge_cases_or_failure_modes: Empty accounts, unknown outcome variant, missing labels.
- validation_or_tests: Slash command tests not assigned for reset usage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3237 `file` `packages/coding-agent/src/web/scrapers/devto.ts`
- cursor: `[_]`
- core_role: Special URL handler for Dev.to article pages.
- algorithmic_behavior: Article response interface at `packages/coding-agent/src/web/scrapers/devto.ts:4`; `handleDevTo` special handler at `:26` fetches/parses Dev.to API/article data into readable markdown.
- inputs_outputs_state: Inputs are URL, timeout, abort signal, optional storage/fetch via handler context. Outputs are `FetchRenderResult` for matching Dev.to URLs or null for non-match/failure.
- gates_or_invariants: Only Dev.to article URL patterns are handled; falls back to generic fetch when not matched.
- dependencies_and_callers: Loaded by `fetch.ts` special handlers.
- edge_cases_or_failure_modes: Slug/API mismatch, missing article fields, network failure, non-article Dev.to URLs.
- validation_or_tests: Web scraper tests not assigned for Dev.to.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3267 `file` `packages/coding-agent/src/web/scrapers/open-vsx.ts`
- cursor: `[_]`
- core_role: Special URL handler for Open VSX extension pages.
- algorithmic_behavior: API payload interfaces at `packages/coding-agent/src/web/scrapers/open-vsx.ts:5`; `handleOpenVsx` at `:28` detects Open VSX URLs and formats extension metadata/readme/download links.
- inputs_outputs_state: Inputs are Open VSX URLs, timeout, abort signal. Outputs are readable markdown result or null.
- gates_or_invariants: Only valid Open VSX extension URL shapes are handled; API failures fall through/return handled failure.
- dependencies_and_callers: Loaded by fetch special handler chain.
- edge_cases_or_failure_modes: Missing namespace/name, missing files/readme, API not found, malformed URL.
- validation_or_tests: No assigned Open VSX test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3297 `file` `packages/coding-agent/src/web/scrapers/w3c.ts`
- cursor: `[_]`
- core_role: Special URL handler for W3C specification metadata.
- algorithmic_behavior: JSON access helpers at `packages/coding-agent/src/web/scrapers/w3c.ts:8`-`:19`; shortname extraction at `:25`; status normalization at `:46`; editor extraction at `:58`; `handleW3c` at `:72`.
- inputs_outputs_state: Inputs are W3C spec URLs and API JSON. Outputs are markdown with title/status/editors/links or null.
- gates_or_invariants: Shortname must be extractable; status normalized to code/label; editor payload must be array/object safe.
- dependencies_and_callers: Fetch special URL handler chain.
- edge_cases_or_failure_modes: Unrecognized pathname, missing JSON fields, status variants, malformed editors payload.
- validation_or_tests: No assigned W3C test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3327 `file` `packages/coding-agent/test/modes/components/segment-track.test.ts`
- cursor: `[_]`
- core_role: Tests segmented track palette/rendering and contrast foreground selection.
- algorithmic_behavior: Segment fixture at `packages/coding-agent/test/modes/components/segment-track.test.ts:13`; palette suite at `:25`; render suite at `:40`; contrast suite at `:75`.
- inputs_outputs_state: Inputs are theme and segment labels/active index. Outputs are ANSI-colored track strings.
- gates_or_invariants: Palette colors are pairwise distinct, start from theme accent, do not exceed requested count, active segment is bold chip with background, foreground has high contrast.
- dependencies_and_callers: Tests mode segment-track component and theme contrast helper.
- edge_cases_or_failure_modes: Too few theme colors, active index movement, fill contrast over arbitrary RGB.
- validation_or_tests: Direct UI component test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3357 `file` `packages/coding-agent/test/modes/controllers/input-controller-tool-expansion.test.ts`
- cursor: `[_]`
- core_role: Regression test for input controller tool output expansion forcing full display reset.
- algorithmic_behavior: Suite at `packages/coding-agent/test/modes/controllers/input-controller-tool-expansion.test.ts:5`; test at `:6` verifies expanding children bypasses frozen snapshots.
- inputs_outputs_state: Inputs are controller/tool output child state. Outputs are expansion state and display reset request.
- gates_or_invariants: Expansion must force full display reset to avoid stale/frozen snapshots.
- dependencies_and_callers: Tests interactive input controller.
- edge_cases_or_failure_modes: Child expansion without reset leaving old UI.
- validation_or_tests: Direct regression test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3387 `file` `packages/coding-agent/test/tools/web-scrapers/youtube.test.ts`
- cursor: `[_]`
- core_role: Tests YouTube special scraper URL parsing, metadata extraction, transcript handling, canonicalization, and formatting helpers.
- algorithmic_behavior: Integration skip flag at `packages/coding-agent/test/tools/web-scrapers/youtube.test.ts:4`; tests non/invalid YouTube, watch/short/youtu.be/shorts/embed/v/mobile/playlist URL handling, yt-dlp availability, transcripts, canonical URL, subtitle source, duration/view/date/description formatting at `:7`-`:197`.
- inputs_outputs_state: Inputs are YouTube URL variants and optionally yt-dlp responses. Outputs are scraper result/null and formatted metadata.
- gates_or_invariants: Non-YouTube/invalid returns null; video ID extraction normalizes many URL forms; long descriptions truncate; unavailable yt-dlp returns appropriate response.
- dependencies_and_callers: Tests YouTube scraper special handler used by fetch.
- edge_cases_or_failure_modes: Mobile/www prefixes, playlist URLs with video ID, missing transcripts/subtitles, yt-dlp absent.
- validation_or_tests: Direct scraper suite, integration-gated where necessary.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3417 `file` `packages/collab-web/src/tool-render/tools/goal.tsx`
- cursor: `[_]`
- core_role: Collab-web renderer for goal/autoresearch-style tool details.
- algorithmic_behavior: Goal extraction at `packages/collab-web/src/tool-render/tools/goal.tsx:17`; op/status formatting at `:33` and `:44`; number/duration formatting at `:59`/`:71`; token line at `:82`; Summary/Body components at `:89`/`:107`; renderer export at `:141`.
- inputs_outputs_state: Inputs are tool render props with args/result details. Outputs are React nodes for summary/body with status tones, counts, durations, token metrics.
- gates_or_invariants: Unknown/missing details return null/fallback; status maps to tone; numeric formatting guards non-numeric values.
- dependencies_and_callers: Used by collab-web tool renderer registry.
- edge_cases_or_failure_modes: Missing result details, unknown op/status, zero/NaN durations/tokens.
- validation_or_tests: Collab-web renderer tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3447 `file` `packages/mnemopi/src/core/migrations/e6-triplestore-split.ts`
- cursor: `[_]`
- core_role: Migration for splitting legacy triplestore rows into annotations/triples with backup/copy support.
- algorithmic_behavior: Annotation kinds at `packages/mnemopi/src/core/migrations/e6-triplestore-split.ts:5`; options/types at `:8`; placeholder/table/copy/init helpers at `:35`-`:53`; pending detection at `:70`; row classification at `:93`; kind counts at `:116`; row migration at `:122`; public `migrate` at `:145`.
- inputs_outputs_state: Inputs are SQLite database/path and migration options. Outputs are migrated DB rows, annotation tables, counts, and optional backup/copy.
- gates_or_invariants: Migration only proceeds when pending; annotation tables are initialized; classification separates annotation kinds from triple candidates.
- dependencies_and_callers: Used by mnemopi core migrations/startup.
- edge_cases_or_failure_modes: Missing tables, partial migration, backup copy failure, unknown annotation kind, serialization requirements.
- validation_or_tests: Migration tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3477 `file` `packages/stats/src/client/ui/MetricCluster.tsx`
- cursor: `[_]`
- core_role: Stats dashboard UI component for grouped metric display.
- algorithmic_behavior: Props at `packages/stats/src/client/ui/MetricCluster.tsx:11`; `MetricCluster` component at `:15` renders provided stats.
- inputs_outputs_state: Inputs are stats/metrics prop. Outputs are React UI.
- gates_or_invariants: Component expects valid stats shape; display is deterministic from props.
- dependencies_and_callers: Used by stats client UI.
- edge_cases_or_failure_modes: Missing stats, large values, responsive layout.
- validation_or_tests: Stats UI tests not assigned.
- skip_candidate: `yes: presentational UI component, minimal algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3507 `file` `packages/coding-agent/src/commit/agentic/tools/git-hunk.ts`
- cursor: `[_]`
- core_role: Agentic commit tool that selects specific diff hunks by 1-based index for staging/commit planning.
- algorithmic_behavior: Hunk index schema at `packages/coding-agent/src/commit/agentic/tools/git-hunk.ts:6`; tool schema at `:8`; hunk selection at `:14`; custom tool factory at `:20`.
- inputs_outputs_state: Inputs are cwd, file path, optional requested hunk indices, current file hunks. Outputs are selected hunk content/details as tool result.
- gates_or_invariants: Hunk indices are 1-based; missing requested indices should not select unintended hunks; schema validates numeric indices.
- dependencies_and_callers: Used by agentic commit pipeline and diff hunk utilities.
- edge_cases_or_failure_modes: Out-of-range hunk index, empty hunks, file path not in diff.
- validation_or_tests: Commit agentic tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3537 `file` `packages/coding-agent/src/markit/converters/pdf/render.ts`
- cursor: `[_]`
- core_role: PDF content renderer that converts extracted text boxes/tables into Markdown with heading, paragraph, table, page-number, and sparse-column heuristics.
- algorithmic_behavior: Table markdown renderer at `packages/coding-agent/src/markit/converters/pdf/render.ts:57`; sparse column normalization at `:81`; subheader promotion at `:122`; modal font/body heuristics at `:181`; line grouping at `:200`; heading prefixes at `:255`; heading/paragraph merge at `:271`/`:300`; page number removal at `:339`; detached first-column tables at `:361`; `renderPageContent` at `:461`.
- inputs_outputs_state: Inputs are PDF text boxes, table grids, page dimensions/metadata. Outputs are markdown content blocks/page text.
- gates_or_invariants: Text line grouping uses Y tolerance; body font modal drives heading detection; tables escape pipes and normalize sparse shifts; page numbers are removed heuristically.
- dependencies_and_callers: Used by PDF markit converter and fetch document conversion.
- edge_cases_or_failure_modes: Multi-column sparse tables, detached first columns, wrapped paragraphs, consecutive headings, full-width ASCII, false page-number removal, tiny fonts.
- validation_or_tests: Markit converter tests indirectly cover conversion; PDF-specific tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3567 `file` `packages/coding-agent/src/web/search/providers/base.ts`
- cursor: `[_]`
- core_role: Abstract base contract for web search providers.
- algorithmic_behavior: Search param interface at `packages/coding-agent/src/web/search/providers/base.ts:14`; abstract `SearchProvider` at `:58` defines provider identity/availability/search behavior.
- inputs_outputs_state: Inputs are query/search params and provider credentials. Outputs are normalized search response/results.
- gates_or_invariants: Providers implement availability checks and search method consistently.
- dependencies_and_callers: Extended by Kagi/other search providers and web search tool.
- edge_cases_or_failure_modes: Missing credentials, provider-specific unsupported params, network failures.
- validation_or_tests: Kagi provider tests validate subclass contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3597 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/xychart.ts`
- cursor: `[_]`
- core_role: Vendor ASCII renderer for Mermaid XY charts, including vertical/horizontal plots, line drawing, legends, roles, colors, ticks, and canvas conversion.
- algorithmic_behavior: Plot constants and glyph maps at `packages/utils/src/vendor/mermaid-ascii/ascii/xychart.ts:25`; color/role helpers at `:66`/`:73`; entry `renderXYChartAscii` at `:89`; vertical render at `:109`; horizontal at `:271`; staircase line drawing at `:421`/`:533`; legend at `:621`; canvas helpers at `:674`; colorization at `:776`; data/category/tick helpers at `:832`-`:872`.
- inputs_outputs_state: Inputs are Mermaid `XYChart`, theme, orientation/options. Outputs are ASCII/Unicode chart string with optional color roles.
- gates_or_invariants: Canvas bounds guard writes; tick values are “nice”; category labels align to data count; roles/colors map through theme; legends draw within plot area.
- dependencies_and_callers: Used by `renderMermaidAscii` in utils.
- edge_cases_or_failure_modes: Empty/uneven series, long labels, negative/ranged values, horizontal vs vertical orientation, Unicode vs ASCII fallback, label collisions.
- validation_or_tests: Assigned Mermaid ASCII collision test covers adjacent renderer behavior.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `120 section headings under Item Evidence`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`