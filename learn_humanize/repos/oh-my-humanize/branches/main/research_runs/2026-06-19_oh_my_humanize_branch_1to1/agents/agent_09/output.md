# agent_09 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-009 `file` `AGENTS.md`
- cursor: `[_]`
- core_role: Repository-level behavioral contract for coding-agent work, package focus, style gates, worker entrypoint contract, logging/TUI safety, tests, changelog and release process.
- algorithmic_behavior: Defines rule precedence for human and automation workflows rather than executable code. Key algorithmic constraints include catalog import routing, worker-host re-entry (`cli.ts` hidden argv selectors), Bun-first execution, generated-model source-of-truth rules, tool-render sanitization, and test-contract criteria.
- inputs_outputs_state: Inputs are developer changes and command choices; outputs are permitted code patterns and validation commands. State gates include no direct `models.json` edits, no `console.*` in coding-agent, no worker-only entry modules, no `tsc`, and no commits unless requested.
- gates_or_invariants: Invariants include top-level static imports, ES `#private`, `Promise.withResolvers`, prompt Markdown files, star barrel exports, sanitized TUI output, `[Unreleased]` changelog entries only, and `bun check` validation.
- dependencies_and_callers: Applies to all repo work, especially `packages/coding-agent`, catalog generation, TUI renderers, worker spawn sites, tests, and release automation.
- edge_cases_or_failure_modes: Misinterpreting “agent” as the assistant instead of coding-agent; corrupting TUI via logging; broken compiled binary workers if direct worker entrypoints are introduced; stale generated catalog edits.
- validation_or_tests: Explicitly names `omp --smoke-test`, `ci:test:smoke`, `scripts/install-tests/run-ci.sh`, and focused package-local `bun check`/tests as validation surfaces.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-039 `directory` `packages/wire`
- cursor: `[_]`
- core_role: Dependency-free shared JSON wire contract for collaborative live sessions.
- algorithmic_behavior: Recursive inspection found `src/index.ts` plus constants test. The package defines message, session entry, event, state, agent snapshot, task bus, guest/host frame, link, envelope, and relay-control unions. Consumers tolerate unknown variants at JSON boundaries.
- inputs_outputs_state: Inputs are host/guest JSON frames and encrypted envelope payloads; outputs are typed frame shapes and constants. State is represented by `SessionState`, `AgentSnapshot`, participant lists, and transcript fetch offsets.
- gates_or_invariants: `COLLAB_PROTO=1`, 4-byte peer envelope header, 16-byte room id, 32-byte AES key, 16-byte write token, read-only links without write tokens, exact frame discriminants.
- dependencies_and_callers: Browser clients and coding-agent collab protocol import this package to avoid coding-agent runtime dependency; `packages/wire/test/constants.test.ts` pins public constants.
- edge_cases_or_failure_modes: Version mismatch rejection, absent write token forcing read-only behavior, unknown event/entry variants requiring tolerant defaults, transcript fetch gated by `hasSessionFile`.
- validation_or_tests: `packages/wire/test/constants.test.ts` asserts protocol number, prompt custom type, envelope length, room id size, and default relay URL.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-069 `file` `docs/rulebook-matching-pipeline.md`
- cursor: `[_]`
- core_role: Architecture document for rule discovery, normalization, precedence, bucket assignment, system prompt inclusion, and `rule://` resolution.
- algorithmic_behavior: Documents canonical `Rule`, provider discovery order, frontmatter parsing fallback, name-based deduplication, and `bucketRules` split into TTSR, always-apply, and rulebook rules.
- inputs_outputs_state: Inputs are config files from `.omp`, `.agent`, Cursor, Windsurf, Cline, plugin roots, and builtins. Outputs are `rulebookRules`, `alwaysApplyRules`, `TtsrManager` registrations, active-rule snapshots, and prompt blocks.
- gates_or_invariants: Rule identity is `rule.name`; provider precedence is first-wins by priority; TTSR takes priority when `condition` or `astCondition` registers; description is required for rulebook inclusion; `alwaysApply` injects raw content.
- dependencies_and_callers: References `capability/rule.ts`, `rule-buckets.ts`, discovery providers, `sdk.ts`, `system-prompt.ts`, `internal-urls/rule-protocol.ts`, and `utils/frontmatter.ts`.
- edge_cases_or_failure_modes: Invalid YAML falls back to simple key parsing; fallback strings can drop boolean metadata; glob-like `condition` becomes edit/write scope shorthand; rules without description/always/TTSR are not addressable.
- validation_or_tests: Behavioral coverage is implied by discovery/frontmatter/rule tests; this doc itself is the canonical explanatory surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-099 `file` `scripts/fix-changelogs.test.ts`
- cursor: `[_]`
- core_role: Regression tests for changelog normalization and release-note repair behavior.
- algorithmic_behavior: Exercises `collectPromotableAddedItemLines`, `fixChangelogContent`, and `runChangelogFixer` baseline pinning. Verifies duplicate `### Added` merging, released duplicate dropping, promotion from older sections to `[Unreleased]`, and respecting `CLOG_BASE_REF`.
- inputs_outputs_state: Inputs are changelog Markdown fixtures and git baseline configuration; outputs are transformed content plus counters (`promotedItems`, `mergedDuplicateHeadings`, `droppedReleasedDuplicates`) and changed-file lists.
- gates_or_invariants: Released sections are immutable; only promotable Added lines move; duplicates already in released sections are dropped; explicit baseline pin prevents accidental current-ref drift.
- dependencies_and_callers: Imports script functions from changelog fixer implementation; supports release workflow required by AGENTS.md.
- edge_cases_or_failure_modes: Released-only changelogs, duplicate unreleased headings, promoted lines already present in released history, and absent/explicit baseline refs.
- validation_or_tests: This file is the validation surface; assertions appear around lines 83, 134, 177, 249, and 311-320.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-129 `directory` `packages/catalog/src`
- cursor: `[_]`
- core_role: Core model catalog, model identity, discovery, compatibility, cost, and provider descriptor algorithms.
- algorithmic_behavior: Recursive inspection found builders (`build.ts`), compat builders (`compat/openai.ts`, `compat/anthropic.ts`), discovery clients (`codex`, `cursor`, `gemini`, `openai-compatible`), identity parsing/equivalence/priority, model cache/manager, generated models, provider descriptors/resolvers, thinking metadata, variant collapse, and wire constants.
- inputs_outputs_state: Inputs are bundled `models.json`, provider descriptors, discovered remote catalogs, auth/base URL config, model ids, usage records, and compat overrides. Outputs are normalized `Model`, `CompatOf`, provider rankings, canonical variants, thinking configs, cost totals, cache rows, and wire headers.
- gates_or_invariants: Generated `models.json` is read-only source output; compat resolution is API-specific; thinking efforts are clamped to supported tiers; cache schema version is migrated; provider descriptors determine default models and discovery factories.
- dependencies_and_callers: Used by `packages/ai` and `packages/coding-agent` for model selection, request shaping, provider discovery, thinking-level controls, and usage cost.
- edge_cases_or_failure_modes: Provider-specific non-chat model filtering, OpenAI-compatible reasoning format differences, alias/canonical collisions, unavailable discovery endpoints, stale cache schema, retired effort variants, and provider priority ties.
- validation_or_tests: Catalog tests include provider priority, model thinking, compat, discovery, and variant collapse coverage; assigned direct test `model-provider-priority.test.ts` pins rank behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-159 `directory` `packages/utils/src`
- cursor: `[_]`
- core_role: Shared runtime algorithms for process control, paths, env/profile resolution, retries, logging, frontmatter, streams, temp files, worker-host entrypoint, and Mermaid ASCII rendering.
- algorithmic_behavior: Recursive inspection found modules for abortable streams, CLI/env parsing, directory profile resolution, retry/backoff, formatters, frontmatter, glob/path grouping, JSON, logger/timing spans, process tree wrappers, runtime module resolution/install locks, text sanitization, snowflake ids, JSONL/SSE streams, tab/editorconfig indentation, and vendored Mermaid parser/renderer.
- inputs_outputs_state: Inputs include env files, filesystem paths, process streams, HTTP responses, Mermaid source, ANSI/text, module specifiers, and runtime install manifests. Outputs include safe env maps, resolved dirs, retry decisions, logs, grouped path text, parsed frontmatter, stream chunks/events, rendered ASCII diagrams, and worker inbox state.
- gates_or_invariants: Env names/values are filtered; profile names are normalized; path-within-root guards protect traversal; retry status/message patterns classify transient failures; runtime resolver is installed once via symbols; worker host entry is declared and consumed process-globally.
- dependencies_and_callers: Used across all packages, especially coding-agent tools/renderers, catalog fetchers, AI clients, worker spawning, logging, and TUI previews.
- edge_cases_or_failure_modes: Malformed `.env` lines, macOS path equivalence, stale install locks, transient socket closes, invalid Mermaid diagrams, overlong path components, and partial stream chunks.
- validation_or_tests: Assigned tests cover Mermaid edge styles and `stream.ts`; package tests also cover env, dirs, path tree, runtime install, logger, prompt, sanitize, snowflake, and ring behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-189 `file` `docs/tools/find.md`
- cursor: `[_]`
- core_role: Tool contract documentation for filesystem path discovery by glob.
- algorithmic_behavior: Defines `FindTool.execute` pipeline: delimiter expansion, path normalization, missing-path partitioning, glob parsing, root guard, limit/timeout clamp, local/native or delegated operation branch, streaming updates, dedup/sort, grouped formatting, and truncation metadata.
- inputs_outputs_state: Inputs are `paths`, `hidden`, `gitignore`, `limit`, `timeout`, and optional internal URLs/custom operations. Outputs are grouped path text plus `details` with files, counts, truncation, missing paths, and limit metadata.
- gates_or_invariants: Root `/` is forbidden; empty paths fail; limit is finite positive and clamped `1..200`; timeout clamps `0.5..60s`; local branch ignores node_modules/.git and respects gitignore by default.
- dependencies_and_callers: References `tools/find.ts`, `path-utils.ts`, `list-limit.ts`, `streaming-output.ts`, `tool-result.ts`, `output-meta.ts`, `tool-errors.ts`, native glob, and tool registry.
- edge_cases_or_failure_modes: Delimiter-containing existing paths, single vs multi missing paths, exact file passthrough, internal URL glob rejection, delegated operation parity gaps, timeout partial success, byte truncation.
- validation_or_tests: Tool tests in coding-agent validate built-in tool registration and internal URL search; this doc specifies expected external behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-219 `file` `scripts/session-stats/audit.ts`
- cursor: `[_]`
- core_role: Runtime audit script for session JSONL statistics, tool-use aggregation, spawn/waste classification, model-assisted verdicts, caching, and reporting.
- algorithmic_behavior: Parses CLI (`parseCli`), scans session files (`scanFile`), groups sessions (`discoverGroups`, `scanGroup`), aggregates usage/tools, builds digests, optionally calls an LLM classifier with schemas, validates/normalizes verdicts, caches verdicts, prints scan/verdict/aggregate reports, and exports JSON.
- inputs_outputs_state: Inputs are `~/.omp/agent/sessions`, since/model/concurrency/export flags, JSONL entries, tool args/results, and optional cache. Outputs are per-file scans, grouped session reports, waste verdicts, aggregate findings, console tables, and cache file entries.
- gates_or_invariants: Since parser supports relative windows; JSON schemas constrain classifier responses; cache keys include group id, digest, and model; map pool limits concurrency; truncated outputs are estimated from markers.
- dependencies_and_callers: Uses session file formats, pi-ai model completion, local cache path, and audit CLI invocation.
- edge_cases_or_failure_modes: Malformed JSONL, missing or huge files, orphan tool calls/results, classifier invalid JSON/schema mismatch, cache staleness, retry/waste false positives, absent sessions.
- validation_or_tests: Direct exports `parseSince`, `normalizeReadPath`, `scanFile` are unit-testable; runtime validation includes schema validators and normalized fallback verdicts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-249 `directory` `packages/coding-agent/src/capability`
- cursor: `[_]`
- core_role: Capability discovery, provider registration, deduplication, caching, and typed capability definitions for rules, skills, tools, MCP, hooks, prompts, extensions, settings, SSH, system prompts, and context files.
- algorithmic_behavior: `index.ts` defines `defineCapability`, `registerProvider`, `loadCapability`, provider filtering, disabled-provider persistence, info listing, reset/invalidate, and cache stats. Child files define per-capability identity keys and metadata schemas.
- inputs_outputs_state: Inputs are registered providers, `LoadContext`, settings, disabled provider ids, and capability-specific discovered objects. Outputs are `CapabilityResult` items/all/errors, shadowed metadata, persisted disabled provider state, and provider/capability info.
- gates_or_invariants: First provider result wins by key; provider priority and enabled state filter loading; settings must initialize persistence; `invalidate` clears path/cwd caches; capability keys are capability-specific.
- dependencies_and_callers: Used by discovery providers, SDK/session creation, extension UI, rulebook/TTSR pipeline, setup/settings, and plugin loading.
- edge_cases_or_failure_modes: Duplicate capability keys, provider failures reported without killing all providers, disabled providers lingering in settings, cache invalidation misses, shadowed items still visible in `all`.
- validation_or_tests: Discovery/plugin/rule tests validate provider loading and extension module behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-279 `directory` `packages/coding-agent/src/session`
- cursor: `[_]`
- core_role: Session persistence, transcript tree, storage backends, history, blob externalization, compaction/shaking, async output queues, session listing/resume/fork, and message utilities.
- algorithmic_behavior: `session-manager.ts` manages session ids, headers, entry indexes, disk writer queues, breadcrumbs, file rewrite/migration, branch/fork context, usage totals, artifacts, drafts, labels, model changes, and sanitized OpenAI replay metadata. Other files handle file/Redis/SQL storage, blob refs, session loading/listing, migrations, snapcompact inline transforms, tool-choice queues, and yield queues.
- inputs_outputs_state: Inputs are cwd, storage backend, JSONL entries, session files, messages, artifacts, blobs, branch ids, and settings. Outputs are session JSONL, in-memory entry tree, usage stats, artifact paths, breadcrumbs, blobs, recent-session listings, and resumable/forked managers.
- gates_or_invariants: Persist only after assistant history or forced creation; disk failure is sticky; JSONL writes serialize through queue; branch ids must exist; loaded cwd mismatch resets unless adopted; image payloads externalize; session listing derives status from suffix.
- dependencies_and_callers: Used by `AgentSession`, UI resume/fork flows, collab transcript fetch, task agents, history search, and storage adapters.
- edge_cases_or_failure_modes: Interrupted tool call tails, orphaned backup recovery, moved project breadcrumb resolution, stale context on revival, disk write failure, huge suffix status unknown, missing blob refs, incompatible session migrations.
- validation_or_tests: Assigned tests cover session status, manager fork/storage, blob store, yield queue, async job singleton, concurrent prompt guard, and unexpected-stop guard.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-309 `directory` `packages/coding-agent/test/registry`
- cursor: `[_]`
- core_role: Tests for agent registry lifecycle state machine.
- algorithmic_behavior: `agent-lifecycle.test.ts` validates parking, reviving, coalesced concurrent revival, stale context rejection, removing parked/running agents, main-agent exclusion from lifecycle, and in-progress parking visibility.
- inputs_outputs_state: Inputs are session stubs, reviver factories, registry refs, TTL, and disposal callbacks. Outputs are registry status transitions (`running`, `idle`, `parked`), session/sessionFile values, disposal counts, and thrown diagnostics.
- gates_or_invariants: Park detaches session but preserves session file; ensureLive revives once for concurrent callers; no reviver or stale context throws; main agent is not lifecycle-managed; removal disposes exactly once.
- dependencies_and_callers: Validates registry/lifecycle implementation used by Agent Hub and subagent management.
- edge_cases_or_failure_modes: Concurrent revival races, parked agent without reviver, stale context during revive, removing active vs parked agents, parking while UI reads state.
- validation_or_tests: Assertions in `agent-lifecycle.test.ts` lines 69-307 cover the lifecycle contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-339 `file` `crates/pi-ast/src/summary.rs`
- cursor: `[_]`
- core_role: Rust AST-based code summarizer that elides foldable spans while preserving structural context.
- algorithmic_behavior: `summarize_code` parses source by language, collects elidable trees (`collect_elidable_tree`), selects folded spans (`select_folded_spans`), normalizes spans, and builds kept/elided segments. It recognizes language-specific elidable and groupable node kinds.
- inputs_outputs_state: Inputs are source text, language/options, minimum body/comment lines, and folding thresholds. Outputs are `SummaryResult` with parsed/elided flags, language, line count, and `SummarySegment`s with text or elision.
- gates_or_invariants: Unparsed/unknown/short files return a single kept segment; spans are normalized within total lines; groupable runs can merge; oversized bodies can remain folded while important top-level keys stay visible.
- dependencies_and_callers: Used by native AST summary bindings and code-reading/preview workflows.
- edge_cases_or_failure_modes: Unsupported language, parse errors, comments vs declarations, JSON object dependencies, CSS style bodies, Fortran/Elisp/Rust/TS variations, line boundary off-by-one.
- validation_or_tests: Extensive inline Rust tests from line 921 onward validate TypeScript, Rust, comments, Fortran, Elisp, JSON, CSS, default thresholds, and unparsed fallback.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-369 `file` `crates/pi-natives/src/shell.rs`
- cursor: `[_]`
- core_role: N-API bridge for native shell execution, streaming chunks, minimization, cancellation, and bash fixups.
- algorithmic_behavior: Defines JS-facing option/result structs, converts to `pi-shell` core types, exposes `Shell::run`, `Shell::cancel`, `execute_shell`, `bridge_chunks`, and `apply_bash_fixups`. It batches streamed chunks for JS callbacks.
- inputs_outputs_state: Inputs are command/env/cwd/shell/minimizer options, cancellation requests, and output callbacks. Outputs are exit code, stdout/stderr/minimized text, cancellation flag, and fixup result.
- gates_or_invariants: `cancel` is idempotent; `bridge_chunks` stops on channel close; shell options convert typed env; detached/foreground child-session behavior is tested.
- dependencies_and_callers: Bridges Bun/JS coding-agent bash tool to Rust `pi-shell` runtime and minimizer.
- edge_cases_or_failure_modes: Cancelled long process, callback errors ignored non-blockingly, session detachment differences by tty/foreground, invalid env, command stream closure.
- validation_or_tests: Inline tests validate child-session action matrix and cancellation behavior around lines 367-481.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-399 `file` `packages/agent/test/append-only-context.test.ts`
- cursor: `[_]`
- core_role: Contract tests for append-only context management and stable prefix syncing in the agent runtime.
- algorithmic_behavior: Tests `StablePrefix`, `AppendOnlyLog`, `AppendOnlyContextManager`, fingerprint determinism, message sync, intent injection, tool examples injection, and mutation detection for tool calls.
- inputs_outputs_state: Inputs are message arrays, system/intent/tool-example context, and mutations; outputs are built context, synced messages, stable prefix fingerprints, and detected append-only deltas.
- gates_or_invariants: Prefix fingerprints must be deterministic; append-only logs must avoid rewriting stable context; sync detects tool-call mutation; injected intents/examples appear through build semantics.
- dependencies_and_callers: Validates `packages/agent` runtime context builder consumed by coding-agent sessions and providers.
- edge_cases_or_failure_modes: Mutating existing tool calls, rebuilding with injected system material, append-only divergence, stable prefix mismatch.
- validation_or_tests: Describes at lines 42, 154, 220, 369, 417, 593, 652, and 711 cover the contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-429 `file` `packages/ai/src/utils.ts`
- cursor: `[_]`
- core_role: Shared AI-provider normalization utilities for system prompts, tool-call ids, OpenAI Responses replay payloads, and cache retention.
- algorithmic_behavior: Normalizes system prompt inputs, sanitizes/truncates tool call IDs, maps call/item IDs for Responses API, strips `item_reference` and raw `id` fields for replay, normalizes replayed `call_id`s, validates provider-specific history payloads, and resolves cache retention from options/env.
- inputs_outputs_state: Inputs are prompt strings/arrays, raw ids, provider payloads, current/fallback provider, and `CacheRetention`. Outputs are prompt arrays, normalized call/item ids, sanitized `ResponseInput`, history payloads/items, and `"short"|"long"` retention.
- gates_or_invariants: IDs are limited to 64 chars; non-alphanumeric id chars are replaced; replay only accepted when payload provider matches current provider; `PI_CACHE_RETENTION=long` is backward-compatible default override.
- dependencies_and_callers: Used by OpenAI Responses providers, request replay, caching, and AI clients.
- edge_cases_or_failure_modes: Overlong ids, ids with unsupported prefixes, provider mismatch, empty/invalid prompts, `item_reference` replay rejection, missing fallback provider.
- validation_or_tests: Related tests cover orphan repair, tool-call ids, OpenAI Responses system prompt/history, and issue #931 reasoning mapping.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-459 `file` `packages/ai/test/auth-broker-wire.test.ts`
- cursor: `[_]`
- core_role: Wire-level tests for auth-broker HTTP/SSE credential synchronization.
- algorithmic_behavior: Creates server/client/storage harness, tests health, bearer auth, snapshot redaction, generation/ETag long-poll, forced refresh, disable, unknown routes, snapshot stream SSE frames, keepalive, unsupported stream detection, non-SSE rejection, and missing initial snapshot rejection.
- inputs_outputs_state: Inputs are OAuth credentials, bearer tokens, refresh mocks, HTTP requests, and SSE streams. Outputs are snapshots, redacted refresh sentinel, generation headers, upsert/remove frames, keepalive comments, and thrown client errors.
- gates_or_invariants: Snapshot requires auth; refresh tokens are never exposed; unchanged long-poll returns 304; refresh persists rotated real token while sending sentinel; disabled credential disappears and refresh returns 404.
- dependencies_and_callers: Validates auth broker server/client/storage and OAuth refresh utilities.
- edge_cases_or_failure_modes: Unauthorized access, long-poll wakeup, SSE stream without initial snapshot, 200 non-SSE endpoint, unsupported 404 stream, disable races.
- validation_or_tests: Assertions span lines 67-367 and are the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-489 `file` `packages/ai/test/aws-sigv4.test.ts`
- cursor: `[_]`
- core_role: Contract tests for AWS SigV4 signing helpers.
- algorithmic_behavior: Verifies date formatting, derived signing key, GET empty-body canonical signature, POST JSON body signature, and session-token inclusion.
- inputs_outputs_state: Inputs are credentials, region/service/date, request method/path/body/headers. Outputs are `x-amz-date`, `x-amz-content-sha256`, `authorization`, and optional security token headers.
- gates_or_invariants: Canonical hashes match AWS/Smithy reference; signed headers include session token when present.
- dependencies_and_callers: Validates Bedrock/AWS provider request signing.
- edge_cases_or_failure_modes: Empty body hash, JSON body hash, temporary credentials, header ordering/canonicalization.
- validation_or_tests: Assertions at lines 21-94 pin exact spec strings.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-519 `file` `packages/ai/test/google-oauth-hostname.test.ts`
- cursor: `[_]`
- core_role: Regression test for Google OAuth callback hostname binding.
- algorithmic_behavior: Constructs `GoogleOAuthFlow` and asserts callback hostname resolves to loopback `127.0.0.1`.
- inputs_outputs_state: Input is OAuth flow config; output is `callbackHostname`.
- gates_or_invariants: OAuth callback host should avoid ambiguous localhost binding by using explicit IPv4 loopback.
- dependencies_and_callers: Validates Google auth flow used by AI provider login.
- edge_cases_or_failure_modes: Hostname mismatch breaking redirect callback on some systems.
- validation_or_tests: Single assertion at line 21.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-549 `file` `packages/ai/test/issue-931-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for OpenAI Responses reasoning-effort mapping.
- algorithmic_behavior: Builds request payload for issue #931 and asserts `reasoning` maps high-level effort to provider wire value, e.g. `{ effort: "max", summary: "auto" }`.
- inputs_outputs_state: Inputs are model/options and request body; output is transformed payload.
- gates_or_invariants: Reasoning effort must use provider-supported wire value, not unrecognized internal enum.
- dependencies_and_callers: Validates OpenAI Responses/Codex request transformer and catalog thinking metadata.
- edge_cases_or_failure_modes: Invalid reasoning value causing provider 400.
- validation_or_tests: Assertion at line 68.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-579 `file` `packages/ai/test/openai-codex-usage.test.ts`
- cursor: `[_]`
- core_role: Tests for OpenAI Codex usage-limit parsing and reporting.
- algorithmic_behavior: Parses headers/body into usage reports, including primary/secondary limits, Spark tier labels/model ids, fallback from error headers, reset credits, and absent reset credits.
- inputs_outputs_state: Inputs are Codex rate-limit headers/error payloads. Outputs are usage reports with `limits`, scopes, labels, used fractions, reset times, and reset credit counts.
- gates_or_invariants: Main tier limit ids are stable; Spark uses tier/model scope; usage fractions are normalized; reset credits appear only when provided.
- dependencies_and_callers: Validates Codex response-handler/usage provider UI data.
- edge_cases_or_failure_modes: Partial headers, Spark-only limits, error responses, reset-credit omission.
- validation_or_tests: Assertions at lines 63-150.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-609 `file` `packages/ai/test/owned-stream-native-toolcall.test.ts`
- cursor: `[_]`
- core_role: Tests native in-band tool-call passthrough in owned streams.
- algorithmic_behavior: Wraps in-band tool stream, asserts native tool call is emitted with name/id/arguments, thinking content is preserved, stop reason becomes `toolUse`, and stream events include start/delta/end.
- inputs_outputs_state: Inputs are mock assistant streaming events with tool call markers. Outputs are final assistant message, tool call content, and event sequence.
- gates_or_invariants: Tool call identity and JSON args survive wrapping; thinking blocks are not dropped; tool-call stop reason is surfaced.
- dependencies_and_callers: Validates `wrapInbandToolStream` behavior for provider streams.
- edge_cases_or_failure_modes: Late real tool id, missing args chunks, thinking/tool interleaving.
- validation_or_tests: Assertions at lines 125-153.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-639 `file` `packages/ai/test/tool-call-without-result.test.ts`
- cursor: `[_]`
- core_role: Regression tests for sessions that continue after a tool call without a persisted result.
- algorithmic_behavior: Exercises provider/session replay where a previous response ended with a tool call; second response must not error and should produce text or another tool call.
- inputs_outputs_state: Inputs are message history with tool call but missing result. Outputs are subsequent assistant response content and stop reason.
- gates_or_invariants: Missing tool result cannot poison future turns; stop reason must be `stop` or `toolUse`, not `error`.
- dependencies_and_callers: Validates repair logic in Responses/Codex replay pipelines.
- edge_cases_or_failure_modes: Branching transcript at a tool-call node, aborted/crashed tool result, provider grammar rejection.
- validation_or_tests: Assertions at lines 55-90.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-669 `file` `packages/catalog/src/variant-collapse.ts`
- cursor: `[_]`
- core_role: Collapses provider model effort variants into canonical base models with aliases and thinking-effort surfaces.
- algorithmic_behavior: Defines variant families/tables, derives thinking-pair families, reconciles retired routing, refreshes collapsed thinking configs, collapses variants per provider/across providers, builds alias indexes, resolves provider/bare aliases, and exposes alias source ids.
- inputs_outputs_state: Inputs are provider ids, `ModelSpec`/`Model` arrays, variant family definitions, compat/thinking metadata. Outputs are collapsed specs/models, routed aliases, supported efforts, max token/context reconciliations, and alias hits.
- gates_or_invariants: Collapsed specs carry routing/alias metadata; efforts are derived from variants; retired variants still route; per-provider tables apply only to configured providers; alias index is memoized by symbol.
- dependencies_and_callers: Used by catalog generation/building and model selection to avoid surfacing duplicate thinking variants.
- edge_cases_or_failure_modes: Missing base or variant specs, retired ids, mismatched max tokens/context windows, bare alias collisions, provider mismatch.
- validation_or_tests: Catalog variant-collapse tests plus provider priority/selection tests protect this behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-699 `file` `packages/catalog/test/model-provider-priority.test.ts`
- cursor: `[_]`
- core_role: Tests provider priority ranking used for canonical model/provider choice.
- algorithmic_behavior: Calls `buildModelProviderPriorityRank` and asserts configured provider order overrides/defaults are respected.
- inputs_outputs_state: Inputs are configured provider order; output is rank map.
- gates_or_invariants: Explicit configured providers get stable precedence ahead of defaults.
- dependencies_and_callers: Supports catalog identity/selection algorithms.
- edge_cases_or_failure_modes: Provider tie/order regression producing unstable canonical choices.
- validation_or_tests: Single describe block at line 4.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-729 `file` `packages/coding-agent/src/index.ts`
- cursor: `[_]`
- core_role: Public SDK/barrel export surface for coding-agent.
- algorithmic_behavior: Re-exports TUI primitives, utils, zod, config, extensibility, LSP, main, modes, theme, SDK, session managers/storage/messages, task executor/types, tools, git utils, and selected components.
- inputs_outputs_state: Inputs are module imports; output is package public API.
- gates_or_invariants: Barrel shape controls consumer compatibility. It mostly uses star exports, with some type/named exports for compatibility.
- dependencies_and_callers: External SDK consumers, tests, plugin/custom-tool integrations.
- edge_cases_or_failure_modes: Export ambiguity, leaking internal modules, breaking type-only consumer imports.
- validation_or_tests: SDK and plugin tests indirectly validate public surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-759 `file` `packages/coding-agent/test/agent-session-concurrent.test.ts`
- cursor: `[_]`
- core_role: Large concurrency and turn-state regression suite for `AgentSession`.
- algorithmic_behavior: Tests prompt queuing, concurrent prompt guard, abort/drain behavior, reentrant prompt after agent end, async job delivery isolation, TTSR resume gates, tool abort messages, rule injection ordering, parallel tool result handling, and extension stop hooks.
- inputs_outputs_state: Inputs are mock models/tools/session harnesses, queued prompts, abort signals, TTSR rules, async jobs. Outputs are stream call counts, queue counts, session messages, tool results, reminders, and hook invocations.
- gates_or_invariants: Only one active prompt streams; queued prompts drain safely; `isStreaming` resets before reentry; TTSR aborts surface rule reminders not generic aborts; async jobs are per-session; extension stop fires once.
- dependencies_and_callers: Validates `AgentSession`, TTSR manager, async job manager, tool execution, event hooks, and message persistence.
- edge_cases_or_failure_modes: Race between turn end and queued prompt, TTSR after tool resume, multi-tool reminder dedup, model switching under continuation, job delivery cross-session leakage.
- validation_or_tests: Describes at lines 44 and 967; many assertions through line 1905.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-789 `file` `packages/coding-agent/test/agent-session-unexpected-stop-guard.test.ts`
- cursor: `[_]`
- core_role: Tests automatic continuation guard for unexpected model stops.
- algorithmic_behavior: Harnesses mock model and classifier to assert when classification runs, when reminder messages are injected, when continuation retries happen, and when max reminders/log warnings stop escalation.
- inputs_outputs_state: Inputs are mock responses, classifier boolean/error behavior, retry settings. Outputs are model call counts, assistant text, reminder messages, and logger warnings.
- gates_or_invariants: No classifier on normal stops; classifier-driven true triggers continuation; false does not; capped reminder count prevents infinite loops; tool-use or explicit continuations are exempt.
- dependencies_and_callers: Validates `unexpected-stop-classifier` integration in `AgentSession`.
- edge_cases_or_failure_modes: Classifier throws, repeated unexpected stops, stop after tool use, already continued turns.
- validation_or_tests: Assertions at lines 142-249.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-819 `file` `packages/coding-agent/test/cli-hide-thinking-flag.test.ts`
- cursor: `[_]`
- core_role: Tests CLI parsing for `--hide-thinking`.
- algorithmic_behavior: Parses args and asserts `hideThinking` is set when flag appears and coexists with model args.
- inputs_outputs_state: Inputs are argv arrays; output is parsed CLI options.
- gates_or_invariants: Flag is boolean, absent means undefined, does not consume following model value.
- dependencies_and_callers: Validates CLI option parser and UI thinking display behavior.
- edge_cases_or_failure_modes: Flag ordering with model argument.
- validation_or_tests: Assertions at lines 8-19.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-849 `file` `packages/coding-agent/test/emoji-autocomplete.test.ts`
- cursor: `[_]`
- core_role: Tests emoji autocomplete and inline replacement behavior in input controller helpers.
- algorithmic_behavior: Validates suggestion trigger parsing, prefix matching, URL/non-token rejection, max suggestion count, exact shortcode replacement, unknown shortcode rejection, and cursor updates after replacement.
- inputs_outputs_state: Inputs are typed text fragments and line/cursor state. Outputs are suggestion lists, replace length, inserted emoji, updated lines/cursor.
- gates_or_invariants: Suggestions require leading shortcode token; no replacement without closing colon; cap suggestions at 12; do not replace embedded text like `foo:joy:`.
- dependencies_and_callers: Used by interactive input UI.
- edge_cases_or_failure_modes: Bare colon, URLs, unknown emoji, prefix too broad, multibyte emoji cursor position.
- validation_or_tests: Assertions at lines 11-87.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-879 `file` `packages/coding-agent/test/hook-selector-overflow.test.ts`
- cursor: `[_]`
- core_role: TUI selector layout and keyboard behavior regression tests.
- algorithmic_behavior: Renders hook selector at narrow widths, asserts no overflow, description wrapping, scroll/count indicators, disabled rows, radio vs cursor visuals, multi-select checkboxes, and keyboard selection/cancel.
- inputs_outputs_state: Inputs are selector options, terminal widths, key events, disabled indices. Outputs are rendered lines, selected values, and visual markers.
- gates_or_invariants: Visible width must not exceed container; descriptions wrap below labels; cursor and radio/checkbox markers are distinct; disabled options render dim and do not select.
- dependencies_and_callers: Validates setup wizard/hook selector components.
- edge_cases_or_failure_modes: Long option text, overflow at width 50, scrolling selected row, disabled selected row, multi-select done row.
- validation_or_tests: Assertions at lines 31-299.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-909 `file` `packages/coding-agent/test/issue-1150-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for compiled/dev worker entrypoint routing.
- algorithmic_behavior: Reads release/dev build source and asserts worker entry modules are not embedded as separate literal entry strings.
- inputs_outputs_state: Inputs are build script/source text; output is absence/presence assertions.
- gates_or_invariants: Worker scripts must re-enter CLI host entrypoint, matching AGENTS.md worker-host contract.
- dependencies_and_callers: Validates worker spawn/build packaging after issue #1150.
- edge_cases_or_failure_modes: Reintroducing separate worker entrypoints in release/dev scripts.
- validation_or_tests: Assertions at lines 41 and 48.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-939 `file` `packages/coding-agent/test/issue-interrupt-and-flush-empty-messages.test.ts`
- cursor: `[_]`
- core_role: Regression test for empty submit while queued messages exist during interrupt.
- algorithmic_behavior: Simulates pending messages and empty submit, asserts abort is called with user interrupt label, prompt is not called, error not shown, and pending display/render update once.
- inputs_outputs_state: Inputs are mocked interactive handlers and queued state. Outputs are abort/prompt/render call counts.
- gates_or_invariants: Empty submit should flush interrupt state, not send empty prompt.
- dependencies_and_callers: Validates interactive mode input controller/session integration.
- edge_cases_or_failure_modes: Empty queued message causing accidental prompt or missing UI refresh.
- validation_or_tests: Assertions at lines 60-64.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-969 `file` `packages/coding-agent/test/mcp-startup-events.test.ts`
- cursor: `[_]`
- core_role: Cross-module contract test for MCP startup event/banner behavior.
- algorithmic_behavior: Verifies connecting-banner event semantics across MCP startup and interactive UI modules.
- inputs_outputs_state: Inputs are MCP startup event structures; outputs are banner-visible state.
- gates_or_invariants: Connecting state must be surfaced consistently for deferred MCP auto-discovery.
- dependencies_and_callers: Validates MCP manager, SDK startup events, and interactive mode banner.
- edge_cases_or_failure_modes: Missing startup event causing silent MCP connection delay.
- validation_or_tests: Describe block at line 20.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-999 `file` `packages/coding-agent/test/plugin-extensions-discovery.test.ts`
- cursor: `[_]`
- core_role: Plugin extension discovery and module resolution regression suite.
- algorithmic_behavior: Creates temp plugin packages/manifests and asserts command/tool extension discovery for package imports, legacy names, conditional exports, JSON schema, blocked private imports, side effects, directory/subdir/nested manifests, and `.d.ts` ignoring.
- inputs_outputs_state: Inputs are fake home/plugins directories, package manifests, export maps, module files. Outputs are discovered extensions, errors, command/tool maps, side-effect markers.
- gates_or_invariants: Uses temp homedir spy; no `mock.module`; node conditional wins; private `#` imports and blocked exports produce errors; declaration files do not execute; nested manifest decoys ignored.
- dependencies_and_callers: Validates plugin loader/runtime resolver/extensibility system.
- edge_cases_or_failure_modes: Windows absolute paths, conditional exports, package `imports`, side-effect modules, blocked subpath, nested decoy manifests.
- validation_or_tests: Assertions at lines 91-747.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1029 `file` `packages/coding-agent/test/sdk-async-job-manager-singleton.test.ts`
- cursor: `[_]`
- core_role: Tests singleton lifecycle of async job manager across SDK sessions.
- algorithmic_behavior: Creates concurrent sessions and asserts primary manager ownership, secondary session null snapshots, job delivery isolation, async bash disabled for secondary, cleanup after startup failure, and replacement session recovery.
- inputs_outputs_state: Inputs are SDK session instances, async job ids, bash execution calls. Outputs are singleton instance, job snapshots, thrown errors, and job counts.
- gates_or_invariants: Only primary top-level session owns async job manager; failed session startup must not leak singleton; secondary cannot run async bash.
- dependencies_and_callers: Validates SDK session creation and async job infrastructure.
- edge_cases_or_failure_modes: Concurrent session creation, startup exception, cross-session job delivery leakage.
- validation_or_tests: Assertions at lines 67-190.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1059 `file` `packages/coding-agent/test/setup-wizard-sign-in.test.ts`
- cursor: `[_]`
- core_role: Tests sign-in wizard login URL rendering and clipboard/focus behavior.
- algorithmic_behavior: Renders `SignInTab`, verifies full URL remains visible/no ellipsis, OSC8 hyperlink is present, browser open and clipboard copy calls happen, clipped body orders URL before auth-code input, and copy shortcut behavior works.
- inputs_outputs_state: Inputs are login URL, fake opener, clipboard spy, rendered width. Outputs are render lines, focus target, opened URLs, clipboard calls.
- gates_or_invariants: Login URL must be inspectable/copyable; authorization input remains after URL; copy must use full URL.
- dependencies_and_callers: Validates setup wizard UI and auth login flow.
- edge_cases_or_failure_modes: Long URL truncation hiding auth data, clipboard double-copy, lost focus target.
- validation_or_tests: Assertions at lines 67-136.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1089 `file` `packages/coding-agent/test/stt-preflight.test.ts`
- cursor: `[_]`
- core_role: Tests speech-to-text model cache checks and recording preflight.
- algorithmic_behavior: Validates `isSttModelCached` for model directories, and `STTController` start behavior with cached vs uncached models, progress status, recorder detection, and model changes.
- inputs_outputs_state: Inputs are fake cache dirs, recorder/downloader spies, selected STT model. Outputs are controller state, download calls, progress status lines.
- gates_or_invariants: Recording starts only after recorder ensured; uncached model triggers download; progress callback clears status after completion; model cache check uses selected model.
- dependencies_and_callers: Validates STT downloader, recorder, and controller.
- edge_cases_or_failure_modes: Parakeet vs Whisper cache layout, download in progress, switching model while idle/recording.
- validation_or_tests: Assertions at lines 42-169.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1119 `file` `packages/coding-agent/test/usage-row-placement.test.ts`
- cursor: `[_]`
- core_role: Tests token usage row placement in rendered session context.
- algorithmic_behavior: Builds session context with read tool groups and usage rows, asserts usage label appears after read group and only once; absence of usage keeps read group last.
- inputs_outputs_state: Inputs are synthetic session entries/tool groups/usage. Outputs are rendered component children and label placement.
- gates_or_invariants: Usage summary should not split read tool group and should not duplicate.
- dependencies_and_callers: Validates UI helper transcript rendering.
- edge_cases_or_failure_modes: Usage row inserted too early or duplicated.
- validation_or_tests: Assertions at lines 88-106.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1149 `file` `packages/hashline/src/input.ts`
- cursor: `[_]`
- core_role: Parser for hashline patch input sections and recovery headers.
- algorithmic_behavior: Tokenizes input, unquotes/normalizes paths, strips apply_patch path noise, recognizes recovery headers, splits raw sections, detects recognizable operations, parses section bodies into `PatchSection`, assembles `Patch`, and merges same-path sections.
- inputs_outputs_state: Inputs are hashline/apply-patch-like text and cwd. Outputs are normalized section paths, operation bodies, parsed patch sections, cursor metadata, and merged patch objects.
- gates_or_invariants: Paths are normalized relative to cwd; leading blank lines are stripped; recognizable operation check prevents fallback ambiguity; same-path sections merge in order.
- dependencies_and_callers: Used by hashline edit/diff tooling in coding-agent.
- edge_cases_or_failure_modes: Quoted paths, apply_patch failure headers, absolute vs relative paths, section separators inside content, duplicate paths, empty sections.
- validation_or_tests: Hashline/edit tests cover parser and diff behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1179 `file` `packages/mnemopi/test/ab-toggles.test.ts`
- cursor: `[_]`
- core_role: Tests A/B feature toggles for polyphonic recall voices.
- algorithmic_behavior: Constructs recall engine under env/config toggles and asserts vector, graph, fact, temporal, and combined recall voices are disabled/enabled as configured.
- inputs_outputs_state: Inputs are feature flags/env state and query/vector. Outputs are voice result arrays and recall result arrays.
- gates_or_invariants: Disabled voices return empty arrays; enabled voices return arrays; all-disabled recall returns empty.
- dependencies_and_callers: Validates mnemopi recall feature configuration.
- edge_cases_or_failure_modes: Env leakage between tests; partial voice enablement.
- validation_or_tests: Assertions at lines 55-89.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1209 `file` `packages/mnemopi/test/foundation.test.ts`
- cursor: `[_]`
- core_role: Foundation smoke test for memory persistence.
- algorithmic_behavior: Creates memory row and verifies id/content/source/timestamp/session/importance/veracity/created_at round-trip.
- inputs_outputs_state: Inputs are memory content and metadata. Outputs are SQLite row fields.
- gates_or_invariants: Stored values must round-trip exactly with default veracity `unknown`.
- dependencies_and_callers: Validates mnemopi core storage foundation.
- edge_cases_or_failure_modes: Missing row, metadata mismatch, timestamp drift.
- validation_or_tests: Assertions at lines 42-50.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1239 `file` `packages/mnemopi/test/temporal-recall.test.ts`
- cursor: `[_]`
- core_role: Tests temporal scoring and query-time parsing in recall.
- algorithmic_behavior: Verifies recency boosts, date parsing, temporal reranking vs no-temporal identity, explicit vs implicit query time equivalence, duration effects, and temporal score ordering.
- inputs_outputs_state: Inputs are timestamps, query time/date strings, memory records. Outputs are temporal scores, parsed `Date`s, ranked recall results.
- gates_or_invariants: Invalid time throws; temporal mode does not change result id set, only scores/ranking; explicit default query time matches implicit.
- dependencies_and_callers: Validates mnemopi temporal recall algorithms.
- edge_cases_or_failure_modes: Timezone offsets, bad date input, long/short decay windows.
- validation_or_tests: Assertions at lines 30-137.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1269 `file` `packages/snapcompact/research/diag_kimi_chunked.py`
- cursor: `[_]`
- core_role: Research diagnostic script for chunked Kimi visual/text recall experiments.
- algorithmic_behavior: Builds overlapping chunks, scores/selects chunks, calls model/provider helpers, and records diagnostic outputs for Kimi K2.6 on a fixed shape.
- inputs_outputs_state: Inputs are research fixtures, chunk ranges, model id, API/env config. Outputs are diagnostic records/results under research directories.
- gates_or_invariants: Chunk set is fixed; best chunk is selected by score; script is executable via `main()`.
- dependencies_and_callers: Uses snapcompact research provider/rendering utilities, not production runtime.
- edge_cases_or_failure_modes: Missing API key, missing fixtures/cache, model API failure, hard-coded chunk ranges stale.
- validation_or_tests: No dedicated tests found; research script output is manual evidence.
- skip_candidate: `yes: research/diagnostic script, not core product runtime, though it encodes experiment workflow`

### OH_MY_HUMANIZE_MAIN-HZ-1299 `file` `packages/snapcompact/research/parity_render.ts`
- cursor: `[_]`
- core_role: Small research parity renderer entrypoint.
- algorithmic_behavior: Renders or compares snapcompact parity fixtures using local research utilities.
- inputs_outputs_state: Inputs are fixture/render parameters; outputs are parity render artifacts.
- gates_or_invariants: Intended as deterministic research output generation.
- dependencies_and_callers: Snapcompact research tooling.
- edge_cases_or_failure_modes: Missing fixtures or renderer dependencies.
- validation_or_tests: No assigned test; manual parity artifact comparison.
- skip_candidate: `yes: research helper, not runtime core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1329 `file` `packages/snapcompact/research/snapcompact_token_entry_viz.py`
- cursor: `[_]`
- core_role: Visualization script for snapcompact token-entry vectors and screenshots.
- algorithmic_behavior: Loads fonts/data, formats vector heads, draws vector bars, composes image panels, and writes a visualization artifact from `main()`.
- inputs_outputs_state: Inputs are research JSON/images and font files. Outputs are PNG visualization and possibly source data.
- gates_or_invariants: Falls back to default fonts; vector text displays first six values; layout is static.
- dependencies_and_callers: PIL/ImageDraw and snapcompact research results.
- edge_cases_or_failure_modes: Missing fonts/data, malformed vector heads, image write failure.
- validation_or_tests: No dedicated automated tests found.
- skip_candidate: `yes: visualization evidence script rather than product runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1359 `file` `packages/stats/test/priority-premium-requests.test.ts`
- cursor: `[_]`
- core_role: Tests premium-request backfill for priority service-tier stats.
- algorithmic_behavior: Seeds stats entries, computes dashboard/request stats, validates premium request counts/fractions, per-request backfill, and duplicate-safe incremental updates.
- inputs_outputs_state: Inputs are stats DB rows with priority tiers and usage. Outputs are aggregate totals, request usage premiumRequests, and updated stats rows.
- gates_or_invariants: Priority requests count as premium; partial request fraction can be `0.33`; reruns are idempotent and do not duplicate rows.
- dependencies_and_callers: Validates stats database backfill and dashboard calculations.
- edge_cases_or_failure_modes: Mixed service tiers, rerun after marker line, missing premium field.
- validation_or_tests: Assertions at lines 96-210.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1389 `file` `packages/tui/test/abort-collapse-gap.test.ts`
- cursor: `[_]`
- core_role: TUI regression test for layout after abort collapse.
- algorithmic_behavior: Renders terminal viewport scenarios and asserts row contents after collapsed abort blocks do not leave unexpected gaps.
- inputs_outputs_state: Inputs are synthetic TUI components/events. Outputs are viewport rows.
- gates_or_invariants: Collapsing aborted content must preserve expected adjacent rows and spacing.
- dependencies_and_callers: Validates TUI differential renderer/layout.
- edge_cases_or_failure_modes: Extra blank row/gap after abort collapse.
- validation_or_tests: Viewport equality assertions at lines 87 and 104.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1419 `file` `packages/tui/test/kitty-keyboard-da1-ordering.test.ts`
- cursor: `[_]`
- core_role: Tests terminal progressive-enhancement ordering for Kitty keyboard protocol and DA1.
- algorithmic_behavior: Simulates terminal writes/responses, asserts initial `CSI ? u`/DA1 order, enables or disables Kitty protocol based on response, and restores/disables in correct order.
- inputs_outputs_state: Inputs are terminal capability response bytes. Outputs are writes and `kittyProtocolActive`.
- gates_or_invariants: Query order must be `\x1b[?u\x1b[c`; supported terminal uses Kitty enable not modifyOtherKeys; unsupported uses modifyOtherKeys.
- dependencies_and_callers: Validates ProcessTerminal keyboard initialization.
- edge_cases_or_failure_modes: Wrong ordering can confuse terminals; enable/disable sequence mismatch.
- validation_or_tests: Assertions at lines 24-67.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1449 `file` `packages/tui/test/sgr-coalesce.test.ts`
- cursor: `[_]`
- core_role: Tests ANSI SGR coalescing optimization preserves terminal rendering.
- algorithmic_behavior: Coalesces adjacent SGR sequences, respects reset/boundaries, caps parameter token count, and compares rendered viewport/foreground/background before and after coalescing.
- inputs_outputs_state: Inputs are ANSI strings. Outputs are coalesced ANSI and viewport/color columns.
- gates_or_invariants: Coalescing must reduce mergeable runs without changing rendered output; parameter list cap avoids terminal issues.
- dependencies_and_callers: Validates TUI renderer optimization.
- edge_cases_or_failure_modes: Reset semantics, OSC/non-SGR boundaries, conflicting foreground colors, excessive param tokens.
- validation_or_tests: Assertions at lines 25-107.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1479 `file` `packages/typescript-edit-benchmark/test/runner.test.ts`
- cursor: `[_]`
- core_role: Tests benchmark result aggregation/reporting for TypeScript edit benchmark runner.
- algorithmic_behavior: Validates summary counts, zero-run reports, diff report formatting, failure categorization, best run selection, token summaries/percentiles, ghost runs, one-shot success stats, and conversation dump artifact copying.
- inputs_outputs_state: Inputs are benchmark task/run fixtures and artifact paths. Outputs are `BenchmarkResult`, Markdown reports, dumps, copied artifacts.
- gates_or_invariants: Pending tasks have no runs; raw input not leaked as JSON; best run index chosen by success/token logic; percentiles deterministic; dump paths sanitized.
- dependencies_and_callers: Validates benchmark runner/report generation.
- edge_cases_or_failure_modes: Zero runs, flaky tasks, failed best run, ghost run, weird task ids in dump path.
- validation_or_tests: Assertions at lines 87-413.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1509 `file` `packages/utils/src/stream.ts`
- cursor: `[_]`
- core_role: Shared stream parsing utilities for byte/text concatenation, JSONL, lines, and SSE.
- algorithmic_behavior: Implements Bun JSONL chunk compatibility, `ConcatSink`, text/byte stream reading, line iteration, SSE event parsing with comments/id/event/retry/data handling, lenient JSONL parse, and observer notification.
- inputs_outputs_state: Inputs are `ReadableStream<Uint8Array>`, strings, byte chunks, SSE lines. Outputs are strings, parsed JSON objects, line strings, `ServerSentEvent`s, and parser state.
- gates_or_invariants: Handles partial chunks across boundaries; SSE flush only emits events with data; observer errors do not break parsing; lenient JSONL skips invalid/blank lines.
- dependencies_and_callers: Used by process execution, auth broker SSE, web/AI streams, and tools.
- edge_cases_or_failure_modes: Split UTF-8 sequences, trailing partial JSONL, comments/empty SSE lines, invalid retry fields, stream cancellation.
- validation_or_tests: Stream behavior is covered indirectly by auth-broker wire and provider streaming tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1539 `file` `packages/wire/src/index.ts`
- cursor: `[_]`
- core_role: Source file for collab live-session protocol wire types and constants.
- algorithmic_behavior: Defines content/message/session-entry/event/state/agent/bus/frame/envelope/link/relay-control TypeScript shapes. It intentionally has no runtime codec, keeping JSON boundary tolerant.
- inputs_outputs_state: Inputs are JSON frames from host/guest and relay; outputs are typed discriminated unions and constants.
- gates_or_invariants: `COLLAB_PROTO=1`; full links include write token, view links do not; host frames include welcome/entry/event/state/bus/agents/transcript/bye/error; guest frames include hello/prompt/abort/agent-cmd/fetch-transcript.
- dependencies_and_callers: Imported by collab web client and coding-agent protocol tests.
- edge_cases_or_failure_modes: Unknown variants must be skipped by consumers; missing write token denies mutating frames; transcript fetch offset must advance via `newSize`.
- validation_or_tests: `packages/wire/test/constants.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1569 `file` `python/robomp/src/server.py`
- cursor: `[_]`
- core_role: FastAPI server for Robomp GitHub webhook orchestration, event persistence, replay, issue browse cache, manual triage/retry/cancel, and dashboard endpoints.
- algorithmic_behavior: Builds state, verifies proxy mode/HMAC signatures, queues webhook deliveries, deduplicates by delivery id, mutates issue browse cache, exposes health/ready, replay endpoints, issue browsing with cache, manual action endpoints, stats/dashboard HTML/API, logs, and app factory.
- inputs_outputs_state: Inputs are settings, GitHub webhook headers/body, replay token, issue refs, state params, manual action payloads. Outputs are HTTP JSON/HTML responses, queued events, event DB rows, issue cache entries, and transport/orchestrator state.
- gates_or_invariants: HMAC signature required; allowlist enforced for manual issue actions; replay token gates replay/trigger; only inactive events replay; state filter must be open/closed/all; uninitialized ready returns 503.
- dependencies_and_callers: Uses FastAPI, GitHub backend, proxy transport, storage, orchestrator, UI renderer.
- edge_cases_or_failure_modes: Invalid signature/JSON, duplicate delivery skipped, unknown delivery, active delivery replay conflict, GitHub/network errors, disabled replay, cache miss, manual triage conflicts.
- validation_or_tests: No assigned direct tests; behavior visible through HTTP error codes and JSON state responses.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1599 `directory` `packages/ai/src/providers/openai-codex`
- cursor: `[_]`
- core_role: OpenAI Codex request/response adaptation for Responses/Codex backend.
- algorithmic_behavior: `request-transformer.ts` forces `store=false` and streaming, filters `item_reference`, strips item ids, repairs orphan tool call/output pairs, prepends developer messages, strips image detail for Responses Lite, disables parallel tool calls there, and maps reasoning config/context. `response-handler.ts` parses Codex error JSON/headers into friendly messages and rate-limit metadata.
- inputs_outputs_state: Inputs are `RequestBody`, `Model`, Codex options, developer prompt, HTTP responses. Outputs are transformed request bodies and `CodexApiError`/`CodexErrorInfo`.
- gates_or_invariants: Missing tool outputs get placeholder outputs; orphan outputs become assistant messages; Responses Lite defaults reasoning context to `all_turns`; usage/rate-limit headers are normalized.
- dependencies_and_callers: Used by OpenAI Codex provider/client and usage reporting.
- edge_cases_or_failure_modes: Provider 400 on orphan tool grammar, overlong orphan outputs truncated to 16k, non-JSON error body, usage-limit/rate-limit friendly message calculation.
- validation_or_tests: Assigned Codex usage, issue #931, tool-call-without-result, and owned-stream native tool-call tests cover key behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1629 `directory` `packages/coding-agent/src/markit/converters`
- cursor: `[_]`
- core_role: Document-to-Markdown conversion algorithms for DOCX, EPUB, PPTX, XLSX, and PDF.
- algorithmic_behavior: Recursively inspected converters parse zip/XML or PDF structured text, extract text/images/tables, infer layout, remove headers/footers/page numbers, render tables/headings/paragraphs, and produce Markdown blocks.
- inputs_outputs_state: Inputs are binary document bytes and MIME/extensions. Outputs are Markdown text, extracted page/table/image structures, and rendered image regions.
- gates_or_invariants: Converter matches by extension/MIME; PDF table grid limits columns and prunes empty rows/cols; image region min area; header/footer detection requires repeated zones; XLSX/PPTX shared strings/relationships resolved.
- dependencies_and_callers: Used by markit/read tooling for document ingestion.
- edge_cases_or_failure_modes: Complex PDF tables, diagrams misdetected as tables, missing relationships, malformed XML, OCR-like boxes spanning columns, repeated page numbers.
- validation_or_tests: Conversion behavior is likely covered by markit/read tests; no assigned direct test in this set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1659 `directory` `packages/stats/src/client/data`
- cursor: `[_]`
- core_role: Frontend data formatting and resource hooks for stats dashboard.
- algorithmic_behavior: Contains chart constants, numeric/cost/percent/duration/rate/relative-time formatters, hash-route hook, resource fetch hook, and view-model transforms.
- inputs_outputs_state: Inputs are API data, browser hash, fetch state, timestamps, numeric usage values. Outputs are formatted strings, chart data, route state, and resource loading/error/value state.
- gates_or_invariants: Formatters handle null durations/rates; hash route stays client-side; resource hook tracks loading/error lifecycle.
- dependencies_and_callers: Used by `packages/stats` React dashboard client.
- edge_cases_or_failure_modes: Null values, stale fetch, invalid hash, compact number/cost precision.
- validation_or_tests: Stats client view-model tests cover adjacent data transforms; assigned `charts.ts` is a tiny constant export.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1689 `file` `packages/ai/src/auth-broker/refresher.ts`
- cursor: `[_]`
- core_role: Background OAuth credential refresh loop for auth-broker.
- algorithmic_behavior: `AuthBrokerRefresher` starts immediate/interval sweeps, reloads storage, selects OAuth credentials expiring within skew, refreshes them concurrently, disables definitive OAuth failures, logs transient failures, and exposes schedule.
- inputs_outputs_state: Inputs are `AuthStorage`, refresh skew/interval, clock. Outputs are refreshed credentials, disabled credentials, schedule fields, logs.
- gates_or_invariants: Single-flight tick guard via `#running`; only OAuth credentials with finite `expires` before deadline refresh; definitive failures disable credential; `stop` clears timer.
- dependencies_and_callers: Auth broker server uses it to keep remote snapshot credentials fresh.
- edge_cases_or_failure_modes: Overlapping ticks, storage reload failure, invalid expires, definitive vs transient error classification.
- validation_or_tests: Auth-broker wire tests exercise manual refresh/SSE; refresher-specific tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1719 `file` `packages/ai/src/dialect/thinking.ts`
- cursor: `[_]`
- core_role: In-band scanner for `<think>`/`<thinking>` text streams.
- algorithmic_behavior: Maintains buffer and active close tag, emits text before open tags, thinking start/delta/end events, holds partial tag suffixes across chunks, and flushes unfinished thinking as thinking content.
- inputs_outputs_state: Inputs are streamed text chunks and final flush. Outputs are `InbandScanEvent`s.
- gates_or_invariants: Earliest open tag wins; partial suffix overlap prevents premature text emission; empty deltas ignored; unfinished close tag at flush still emits `thinkingEnd`.
- dependencies_and_callers: Used by AI dialect stream wrappers.
- edge_cases_or_failure_modes: Tags split across chunks, nested/competing tag forms, missing close tag, empty feed.
- validation_or_tests: Thinking/in-band stream tests cover dialect scanning.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1749 `file` `packages/ai/src/providers/openai-chat-server.ts`
- cursor: `[_]`
- core_role: OpenAI chat-completions compatible parser/encoder for auth gateway/server mode.
- algorithmic_behavior: `parseRequest` validates schema, maps system/developer/user/assistant/tool/function messages to pi-ai context, decodes data URLs, tracks tool names by id, builds tool definitions/options, normalizes stop/tool choice/reasoning/service tier/cache key. `encodeResponse` and `encodeStream` map assistant messages/events back to chat completion JSON/SSE chunks.
- inputs_outputs_state: Inputs are OpenAI chat request bodies/headers, assistant messages/event streams, abort controls. Outputs are parsed request context/options, non-stream JSON responses, SSE chunks, and error responses.
- gates_or_invariants: Schema errors throw; `max_completion_tokens` wins; `include_usage` lives in `extra`; tool result images are hoisted to user image messages; malformed tool args become `__raw`; finish reason maps tool calls to `tool_calls`.
- dependencies_and_callers: Auth gateway OpenAI-compatible server path and SDK clients.
- edge_cases_or_failure_modes: Missing tool names, data URL non-base64, unknown content parts dropped/degraded, late tool id/name corrective chunk, stream cancellation, stream ends without done.
- validation_or_tests: OpenAI chat/gateway/pi-native tests cover parse/encode/error behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1779 `file` `packages/ai/src/registry/gitlab-duo.ts`
- cursor: `[_]`
- core_role: Provider registry descriptor for GitLab Duo.
- algorithmic_behavior: Exports `gitlabDuoProvider` metadata/config for auth/model registry.
- inputs_outputs_state: Inputs are registry loading; output is provider descriptor.
- gates_or_invariants: Provider id and login/config metadata must match registry expectations.
- dependencies_and_callers: AI provider registry.
- edge_cases_or_failure_modes: Misconfigured descriptor causing login/model lookup failure.
- validation_or_tests: Registry/builtin provider tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1809 `file` `packages/ai/src/registry/qianfan.ts`
- cursor: `[_]`
- core_role: Qianfan provider login and registry descriptor.
- algorithmic_behavior: `loginQianfan` opens Baidu Qianfan API key URL via `OAuthController`, validates captured key by trying configured validation model/base URL, and exports `qianfanProvider`.
- inputs_outputs_state: Inputs are controller callbacks and API key. Outputs are stored credential string or provider descriptor.
- gates_or_invariants: Validation model/base URL are fixed; invalid keys fail login; auth URL is user-facing.
- dependencies_and_callers: AI registry/login flow and Qianfan model manager.
- edge_cases_or_failure_modes: User cancels, invalid key, network validation failure.
- validation_or_tests: Login/provider registry tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1839 `file` `packages/ai/src/usage/opencode-go.ts`
- cursor: `[_]`
- core_role: Usage provider for opencode-go cost windows.
- algorithmic_behavior: Sums usage costs over fixed hour/day windows, computes used fractions/status, reset times, and builds `UsageLimit` entries.
- inputs_outputs_state: Inputs are usage cost history entries and current time. Outputs are usage report limits with used amounts/fractions/reset.
- gates_or_invariants: Window limits are provider-scoped; status thresholds derive from used fraction; resetsAt is first entry outside/inside window boundary.
- dependencies_and_callers: Stats/status-line usage reporting.
- edge_cases_or_failure_modes: Empty history, boundary timestamps, over-limit usage.
- validation_or_tests: Usage provider tests likely cover adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1869 `file` `packages/catalog/src/compat/openai.ts`
- cursor: `[_]`
- core_role: Resolves OpenAI-compatible and OpenAI Responses compatibility defaults for providers/models.
- algorithmic_behavior: Detects reasoning disable modes, stream markup healing patterns, strict tool mode support, idle timeouts, effort maps, service-tier/headers quirks, Responses-only fields, OpenRouter routing, and builds resolved compat objects from model specs.
- inputs_outputs_state: Inputs are provider/base URL/model id/spec compat config. Outputs are `ResolvedOpenAICompat`, `ResolvedOpenAIResponsesCompat`, and `ResolvedOpenRouterCompat`.
- gates_or_invariants: Provider/model heuristics override defaults; Ollama effort map merges; strict mode support depends on host; special providers like DeepSeek/Kimi/GLM/Minimax get idle/healing/reasoning behavior.
- dependencies_and_callers: Catalog build and AI provider request/stream handling.
- edge_cases_or_failure_modes: Misclassified host URL, unsupported strict tools, reasoning effort mismatch, DSML/Kimi markup leaks, OpenRouter routing differences.
- validation_or_tests: OpenAI compat policy, stream markup healing, reasoning-loop, and provider tests validate behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1899 `file` `packages/coding-agent/src/advisor/index.ts`
- cursor: `[_]`
- core_role: Tiny barrel/export entry for advisor module.
- algorithmic_behavior: Re-exports advisor public surface only; no internal algorithm in this file.
- inputs_outputs_state: Input is module import; output is advisor exports.
- gates_or_invariants: Public API path remains stable.
- dependencies_and_callers: Consumers importing `advisor`.
- edge_cases_or_failure_modes: Broken export path.
- validation_or_tests: Indirect compile/type checks.
- skip_candidate: `yes: barrel-only file, not an algorithm itself`

### OH_MY_HUMANIZE_MAIN-HZ-1929 `file` `packages/coding-agent/src/capability/system-prompt.ts`
- cursor: `[_]`
- core_role: Capability definition for system prompt files.
- algorithmic_behavior: Defines `SystemPrompt` shape and `systemPromptCapability` key/display behavior.
- inputs_outputs_state: Inputs are discovered system prompt objects; output is capability-keyed items.
- gates_or_invariants: Key is prompt name/path as defined by capability; capability id controls provider merging.
- dependencies_and_callers: Capability loader, native/extension discovery, system prompt builder.
- edge_cases_or_failure_modes: Duplicate prompt keys shadowed by provider precedence.
- validation_or_tests: Discovery/system prompt tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1959 `file` `packages/coding-agent/src/cli/ssh-cli.ts`
- cursor: `[_]`
- core_role: CLI command implementation for managing SSH host config.
- algorithmic_behavior: Dispatches `add`, `remove`, `list`; validates required names/hosts; writes/removes user/project SSH config entries; prints host tables; supports cwd/command/shell options.
- inputs_outputs_state: Inputs are `SSHCommandArgs` and settings/config paths. Outputs are updated SSH host config and terminal output.
- gates_or_invariants: Action must be known; add requires host name/host; remove requires name; list formats configured hosts.
- dependencies_and_callers: CLI command registry and SSH tool host loader.
- edge_cases_or_failure_modes: Missing required args, duplicate host names, empty config, invalid scope.
- validation_or_tests: SSH tool/CLI tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1989 `file` `packages/coding-agent/src/commands/launch.ts`
- cursor: `[_]`
- core_role: Launch command workflow for starting configured commands/processes.
- algorithmic_behavior: Parses launch settings, resolves command entries, spawns/monitors selected process, and routes output/errors into CLI/TUI flow.
- inputs_outputs_state: Inputs are launch command args/settings/env. Outputs are spawned process state and command result.
- gates_or_invariants: Command must exist; process errors are surfaced; environment/cwd are resolved before spawn.
- dependencies_and_callers: CLI command registry and process utilities.
- edge_cases_or_failure_modes: Unknown launch target, spawn failure, nonzero exit, missing cwd/env.
- validation_or_tests: Command/launch tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2019 `file` `packages/coding-agent/src/config/model-discovery.ts`
- cursor: `[_]`
- core_role: Runtime model discovery for local/proxy/OpenAI-compatible providers.
- algorithmic_behavior: Normalizes Ollama/llama.cpp/OpenAI base URLs, extracts context/input capability metadata, dispatches discovery by provider type, fetches Ollama tags/show, llama.cpp props/models, OpenAI `/models`, and proxy models, applying defaults and timeouts.
- inputs_outputs_state: Inputs are provider config, auth/base URLs, fetch implementation, env overrides. Outputs are discovered model specs/metadata.
- gates_or_invariants: Default max tokens vary by API; positive numeric parsing filters invalid values; base URLs get native endpoint paths; discovery returns empty/undefined on unsupported provider type.
- dependencies_and_callers: Settings/model registry discovery UI and catalog/provider managers.
- edge_cases_or_failure_modes: Ollama host env with missing scheme/port, invalid metadata, unavailable server, non-array model response, context override invalid.
- validation_or_tests: Discovery helpers/model selection tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2049 `file` `packages/coding-agent/src/discovery/builtin.ts`
- cursor: `[_]`
- core_role: Native OMP discovery provider for config, MCP, prompts, skills, slash commands, rules, extensions, hooks, tools, settings, and context files.
- algorithmic_behavior: Finds user/project config dirs, ancestor dirs, nearest project config, loads JSON/Markdown/module files per capability, normalizes sticky rules, managed skills, extension modules, hooks/tools, settings, and context files with provider metadata.
- inputs_outputs_state: Inputs are cwd, agent dir/home config dirs, filesystem files, settings. Outputs are `LoadResult` arrays for each capability.
- gates_or_invariants: Provider priority 100; project/user search order is explicit; sticky `RULES.md` forced always apply; nearest project sticky rule only; config dirs must be non-empty.
- dependencies_and_callers: Capability registry and discovery index.
- edge_cases_or_failure_modes: Missing config dirs, invalid frontmatter, module load failures, ancestor walk boundaries, duplicate rule names, malformed settings.
- validation_or_tests: Rulebook doc and discovery/frontmatter/plugin tests validate behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2079 `file` `packages/coding-agent/src/eval/budget-bridge.ts`
- cursor: `[_]`
- core_role: Eval bridge that exposes token/output budget state to evaluated code.
- algorithmic_behavior: `runEvalBudget` reads current budget from options/session and returns structured budget result under bridge name `__budget__`.
- inputs_outputs_state: Inputs are ignored args plus `EvalBudgetBridgeOptions`. Outputs are `EvalBudgetResult` with total/spent/hard budget.
- gates_or_invariants: Bridge name is stable; result mirrors session budget without mutation.
- dependencies_and_callers: JS/Python eval tools and session budget accounting.
- edge_cases_or_failure_modes: Missing budget data should return safe defaults.
- validation_or_tests: Eval/tool tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2109 `file` `packages/coding-agent/src/hindsight/client.ts`
- cursor: `[_]`
- core_role: HTTP client for Hindsight memory/mental-model API.
- algorithmic_behavior: `HindsightApi` builds requests, serializes query params, prunes undefined fields, handles JSON/error responses, and exposes retain/recall/reflect/bank/document/mental-model CRUD and refresh operations.
- inputs_outputs_state: Inputs are API URL/config, memory items/options, query filters, document/model options. Outputs are typed response objects or `HindsightError`.
- gates_or_invariants: Requests use user agent; undefined query/body fields pruned; memory item builder formats metadata/date; safe JSON parse protects error paths.
- dependencies_and_callers: Coding-agent memories/hindsight integrations.
- edge_cases_or_failure_modes: Non-JSON response, HTTP error status, date formatting local offset, empty optional fields, malformed API payload.
- validation_or_tests: Hindsight/memory integration tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2139 `file` `packages/coding-agent/src/lsp/edits.ts`
- cursor: `[_]`
- core_role: Applies and validates LSP text/workspace edits.
- algorithmic_behavior: Sorts and validates non-overlapping edits, applies text edits to strings/files, flattens workspace edits, plans document create/rename/delete/edit operations, and applies workspace edit under cwd.
- inputs_outputs_state: Inputs are `TextEdit`, `WorkspaceEdit`, file paths, cwd. Outputs are modified files and changed path list.
- gates_or_invariants: Overlapping ranges throw; edits apply reverse-sorted to preserve offsets; document changes are sequenced; paths resolve under cwd where applicable.
- dependencies_and_callers: LSP tool and refactor/code action workflows.
- edge_cases_or_failure_modes: Overlapping edits, invalid ranges, rename/delete conflicts, missing files, mixed changes/documentChanges forms.
- validation_or_tests: LSP/edit tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2169 `file` `packages/coding-agent/src/memories/index.ts`
- cursor: `[_]`
- core_role: Memory startup/consolidation/learned-lessons pipeline.
- algorithmic_behavior: Starts background memory startup, builds developer instructions, clears/enqueues memory data, runs phase 1 extraction over session threads, phase 2 consolidation model, syncs artifacts, applies skill files/rollout summaries, saves learned lessons with injection neutralization, and resolves memory model/config.
- inputs_outputs_state: Inputs are agent dir, cwd, settings, session threads/messages, model outputs, memory config. Outputs are raw memories, rollout summaries, skill files, learned.md, watermarks, logs/fallback states.
- gates_or_invariants: Runtime config limits threads/messages/tokens; only persistable response items included; secrets redacted; schemas require exact keys; learned lessons capped count/content/context; per-file path sanitized.
- dependencies_and_callers: Agent session startup, memory tools, model manager, skill system.
- edge_cases_or_failure_modes: Invalid model JSON, phase 2 failure fallback, secret leakage, prompt injection in learned lessons, empty threads, concurrent learned writes, token budget overflow.
- validation_or_tests: Memory-related tests in mnemopi/coding-agent indirectly cover; no assigned direct memory test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2199 `file` `packages/coding-agent/src/modes/types.ts`
- cursor: `[_]`
- core_role: Shared interactive-mode type contracts.
- algorithmic_behavior: Defines submitted input, queued compaction messages, todo status/phases, selector dialog options, and `InteractiveModeContext` callbacks/state dependencies.
- inputs_outputs_state: Inputs/outputs are typed UI/session payloads rather than runtime logic.
- gates_or_invariants: Todo statuses are fixed union; context interface controls mode/component integration boundaries.
- dependencies_and_callers: Interactive mode components, todo UI, selectors, controllers.
- edge_cases_or_failure_modes: Type mismatch breaks component contracts.
- validation_or_tests: Type checking and mode tests.
- skip_candidate: `yes: type-contract file with minimal algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-2229 `file` `packages/coding-agent/src/session/session-manager.ts`
- cursor: `[_]`
- core_role: Main session persistence and transcript tree manager.
- algorithmic_behavior: Mints session ids, manages `SessionEntryIndex`, opens/flushes disk writers, conditionally creates files, adopts/loads sessions, rewrites/migrates files, tracks usage, artifacts/blobs/drafts, labels, branches/forks, breadcrumbs, and recent sessions.
- inputs_outputs_state: Inputs are cwd, storage, entries/messages, branch ids, artifacts, blobs. Outputs are session file JSONL, in-memory entries/tree, usage stats, draft/artifact paths, forked managers, and listing/resume results.
- gates_or_invariants: Disk failure sticky; file creation gated by assistant history/force; branch targets must exist; writes serialize through queue; breadcrumb remembers session root; loaded OpenAI replay metadata sanitization can require rewrite.
- dependencies_and_callers: `AgentSession`, UI resume/fork, collab, task agents, session listing/storage.
- edge_cases_or_failure_modes: Header cwd mismatch, moved project, orphaned backups, artifact/session move partial failure, missing branch id, stale breadcrumb, ENOENT draft/blob paths.
- validation_or_tests: Assigned `session-status`, async singleton, concurrent, unexpected-stop, and registry lifecycle tests exercise related contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2259 `file` `packages/coding-agent/src/stt/recorder.ts`
- cursor: `[_]`
- core_role: Cross-platform speech recording process detection/start/verification.
- algorithmic_behavior: Detects sox/ffmpeg/arecord/powershell, builds platform-specific recording commands, verifies process liveness, starts file or streaming recording, stops/kills process, verifies nonempty recording file.
- inputs_outputs_state: Inputs are output path, platform/tools, audio devices. Outputs are `RecordingHandle`/`StreamingRecordingHandle`, recorded file bytes, and errors.
- gates_or_invariants: Recorder must be available; Windows PowerShell path uses MCI script; liveness verified after spawn; recording file size must be positive.
- dependencies_and_callers: STT controller/preflight and voice input UI.
- edge_cases_or_failure_modes: Missing recorder, unsupported OS/device, process exits immediately, zero-byte file, stream stderr, PowerShell script failure.
- validation_or_tests: Assigned `stt-preflight.test.ts` covers controller/cache integration; recorder tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2289 `file` `packages/coding-agent/src/tools/ast-edit.ts`
- cursor: `[_]`
- core_role: AST-aware edit tool wrapper around native ast-grep edit operations.
- algorithmic_behavior: Validates schema, runs one or more ast edit targets, aggregates results, maps modified/matched counts, formats structured tool results, and renders compact/expanded diff previews with pattern previews.
- inputs_outputs_state: Inputs are target paths, language/pattern/replacement/options. Outputs are changed files, match counts, errors, grouped preview lines, and tool details.
- gates_or_invariants: Target execution aggregates by call; renderer truncates using preview limits; errors are surfaced as tool errors; pattern preview sanitized.
- dependencies_and_callers: Tool registry, native ast edit, TUI renderer.
- edge_cases_or_failure_modes: No matches, invalid pattern/language, partial target failures, large diff preview, path sanitization.
- validation_or_tests: Tools registry and edit tests indirectly cover; native ast-grep tests likely separate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2319 `file` `packages/coding-agent/src/tools/inspect-image-renderer.ts`
- cursor: `[_]`
- core_role: TUI renderer for inspect-image tool results.
- algorithmic_behavior: Builds question preview line, renders collapsed/expanded model output lines with fixed line/width limits, and applies theme styling.
- inputs_outputs_state: Inputs are inspect image args/details/result and theme. Outputs are render lines.
- gates_or_invariants: Question/output preview widths are capped; collapsed lines limited to 4 and expanded to 16.
- dependencies_and_callers: Inspect-image tool UI rendering.
- edge_cases_or_failure_modes: Long question/output overflow.
- validation_or_tests: Tool renderer snapshot tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2349 `file` `packages/coding-agent/src/tools/ssh.ts`
- cursor: `[_]`
- core_role: SSH execution tool and renderer.
- algorithmic_behavior: Loads configured SSH hosts, formats description, quotes remote paths per shell, builds remote command with cwd, executes through SSH host info, returns tool result/details, and renders command preview/output.
- inputs_outputs_state: Inputs are host, command, optional cwd, session host config. Outputs are remote stdout/stderr/exit details and TUI lines.
- gates_or_invariants: Tool only loads when hosts configured; cwd quoting is shell-specific; host entry formatting hides missing descriptions.
- dependencies_and_callers: SSH CLI config, tool registry, remote execution.
- edge_cases_or_failure_modes: Unknown host, shell quoting differences, remote command failure, no hosts available.
- validation_or_tests: SSH CLI/tool tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2379 `file` `packages/coding-agent/src/utils/changelog.ts`
- cursor: `[_]`
- core_role: Parses package changelogs and tracks last-seen changelog version.
- algorithmic_behavior: `parseChangelog` extracts version/date/sections/items, `compareVersions` sorts semver-ish entries, `getNewEntries` filters after last version, and read/write helpers persist last version under agent dir.
- inputs_outputs_state: Inputs are changelog path/content and last version. Outputs are `ChangelogEntry[]`, filtered entries, and saved marker file.
- gates_or_invariants: Missing path/file returns empty; version comparison numeric; marker path comes from config dirs.
- dependencies_and_callers: Startup changelog display/notification.
- edge_cases_or_failure_modes: Malformed headings, unreleased sections, missing marker, nonnumeric versions.
- validation_or_tests: Changelog fixer tests adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2409 `file` `packages/coding-agent/src/workflow/agent-task-id.ts`
- cursor: `[_]`
- core_role: Tiny workflow constant/identifier helper for agent task ids.
- algorithmic_behavior: Exposes stable task id symbol/string used by workflow tooling.
- inputs_outputs_state: No dynamic inputs; output is exported identifier.
- gates_or_invariants: Value stability matters for workflow state.
- dependencies_and_callers: Workflow task runtime.
- edge_cases_or_failure_modes: Renaming breaks persisted references.
- validation_or_tests: Workflow task runtime tests indirect.
- skip_candidate: `yes: constant-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2439 `file` `packages/coding-agent/src/workflow/state-schema.ts`
- cursor: `[_]`
- core_role: Parser and validator for workflow state schema declarations and writes.
- algorithmic_behavior: Parses schema object into JSON-pointer type map, validates writes against exact/nested schema, checks whether condition paths are declared, resolves nearest schema ancestors, parses/escapes JSON pointers, and maps runtime values to schema value types.
- inputs_outputs_state: Inputs are unknown schema values, labels, state write paths/values. Outputs are `WorkflowStateSchema`, validation success or `WorkflowStateSchemaError`, and condition path booleans.
- gates_or_invariants: Schema shape must be object mapping pointers to expected types; nested writes must satisfy declared descendants; type names are fixed union.
- dependencies_and_callers: Workflow task tool/runtime state validation.
- edge_cases_or_failure_modes: Invalid pointer escaping, writing object where child path has incompatible schema, undeclared condition path, arrays/null type distinctions.
- validation_or_tests: Assigned `task-tool-runtime.test.ts` covers workflow runtime adapter; schema-specific tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2469 `file` `packages/coding-agent/test/core/python-executor-timeout.test.ts`
- cursor: `[_]`
- core_role: Regression test for Python executor cancellation/timeout.
- algorithmic_behavior: Runs a timed-out Python eval cell and asserts result is cancelled, has no exit code, and output includes timeout message.
- inputs_outputs_state: Inputs are Python code and timeout. Outputs are execution result flags/output.
- gates_or_invariants: Timeout must be reported as cancellation, not normal exit.
- dependencies_and_callers: Python eval/executor tool.
- edge_cases_or_failure_modes: Hung kernel/process, missing timeout text.
- validation_or_tests: Assertions at lines 31-33.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2499 `file` `packages/coding-agent/test/discovery/helpers.test.ts`
- cursor: `[_]`
- core_role: Tests frontmatter parsing used by discovery/rules/prompts.
- algorithmic_behavior: Validates simple key-value, YAML lists, multiline strings, nested objects, mixed YAML, missing/invalid/empty frontmatter, and kebab-case to camelCase normalization.
- inputs_outputs_state: Inputs are Markdown strings. Outputs are `{ frontmatter, body }`.
- gates_or_invariants: Invalid YAML falls back to simple parser; body strips frontmatter; keys normalize to camelCase.
- dependencies_and_callers: Discovery helpers and utils frontmatter parser.
- edge_cases_or_failure_modes: Unclosed arrays, no frontmatter, empty frontmatter, nested YAML.
- validation_or_tests: Assertions at lines 15-147.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2529 `file` `packages/coding-agent/test/helpers/sqlite-inspect.ts`
- cursor: `[_]`
- core_role: Test helper for inspecting SQLite rows.
- algorithmic_behavior: Opens SQLite DB and runs small inspection query/helper for tests.
- inputs_outputs_state: Inputs are DB path/query/table; outputs are rows.
- gates_or_invariants: Test-only utility; should not mutate DB beyond inspection.
- dependencies_and_callers: Session/storage/stats tests.
- edge_cases_or_failure_modes: Missing DB/table.
- validation_or_tests: Helper itself is used by tests.
- skip_candidate: `yes: test helper, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2559 `file` `packages/coding-agent/test/modes/orchestrate.test.ts`
- cursor: `[_]`
- core_role: Tests orchestrate keyword detection/highlighting and slash command filtering.
- algorithmic_behavior: Validates lower-case standalone `orchestrate` detection, ignores uppercase/inflections/code/paths, highlights detected word, validates system notice shape, and removes slash command.
- inputs_outputs_state: Inputs are user text/command list. Outputs are booleans, highlighted ANSI text, notice string, filtered command names.
- gates_or_invariants: Detection is case-sensitive and context-aware; code spans/blocks ignored; notice has XML-like wrapper.
- dependencies_and_callers: Interactive orchestrate mode trigger.
- edge_cases_or_failure_modes: File paths, punctuation, code blocks, similar ultrathink keyword.
- validation_or_tests: Assertions at lines 18-89.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2589 `file` `packages/coding-agent/test/session/session-status.test.ts`
- cursor: `[_]`
- core_role: Tests session listing status derivation from JSONL tails.
- algorithmic_behavior: Creates session files with different tail states and asserts statuses: complete, interrupted tool use/result, aborted, error, pending, unknown, huge unknown.
- inputs_outputs_state: Inputs are session JSONL fixtures. Outputs are status map from `SessionManager.list`.
- gates_or_invariants: Tail derivation must classify pending tool calls as interrupted and header-only/huge truncated files as unknown.
- dependencies_and_callers: Session listing/resume UI.
- edge_cases_or_failure_modes: Huge file suffix not enough to classify, tool call without result, aborted/error messages.
- validation_or_tests: Assertions at lines 67-87.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2619 `file` `packages/coding-agent/test/task/output-manager.test.ts`
- cursor: `[_]`
- core_role: Tests deterministic subagent/task output id allocation.
- algorithmic_behavior: Allocates repeated names with numeric suffixes, preserves different names, handles parent prefixes, and resumes from existing allocations.
- inputs_outputs_state: Inputs are desired names and optional parent/existing ids. Outputs are allocated unique ids.
- gates_or_invariants: First name unchanged; repeats append `-2`, `-3`; parent prefix becomes `Parent.Child`.
- dependencies_and_callers: Task/subagent output manager.
- edge_cases_or_failure_modes: Existing ids, nested parent naming, collisions.
- validation_or_tests: Assertions at lines 15-66.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2649 `file` `packages/coding-agent/test/tools/browser-attach.test.ts`
- cursor: `[_]`
- core_role: Tests browser/Electron CDP target selection.
- algorithmic_behavior: Validates discovered CDP page targets preferred over `browser.pages`, fallback behavior, matcher miss diagnostics, and connected CDP URL normalization/rejection.
- inputs_outputs_state: Inputs are fake browser targets/pages and CDP URL. Outputs are selected page or thrown diagnostic.
- gates_or_invariants: WebSocket CDP URL is rejected with actionable message; HTTP URL normalized without trailing slash.
- dependencies_and_callers: Browser attach tool.
- edge_cases_or_failure_modes: No usable target, matcher misses, browser exposes only pages fallback.
- validation_or_tests: Assertions at lines 37-67.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2679 `file` `packages/coding-agent/test/tools/index.test.ts`
- cursor: `[_]`
- core_role: Tests built-in tool registry composition and mode gating.
- algorithmic_behavior: Calls `createTools` under modes/settings and asserts inclusion/exclusion of eval/bash/read/edit/search/find/lsp/task/todo/web/resolve/yield/ask/goal/hidden BM25 tools.
- inputs_outputs_state: Inputs are tool settings/modes/review/plan/tool filters. Outputs are tool name arrays and hidden tool map.
- gates_or_invariants: Resolve is broadly present; fetch/vim absent; plan/review modes restrict tools; async/ask/yield gates apply; hidden tools stay hidden.
- dependencies_and_callers: Coding-agent tool registry and mode system.
- edge_cases_or_failure_modes: Tool accidentally exposed in restricted mode, missing resolve, hidden tool leakage.
- validation_or_tests: Assertions at lines 73-267.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2709 `file` `packages/coding-agent/test/tools/search-internal-urls.test.ts`
- cursor: `[_]`
- core_role: Tests search tool behavior over internal URL resolvers and virtual content.
- algorithmic_behavior: Resolves internal URLs to content/ranges, searches virtual/log/tool docs/artifacts, filters log levels, formats internal vs filesystem match headers, handles missing artifacts, line numbers, pagination/no-more-results.
- inputs_outputs_state: Inputs are patterns, paths including internal URLs, fake resolvers/artifacts. Outputs are search result text/details/errors.
- gates_or_invariants: Internal URL headers differ from file headers; line numbers increase and dedupe; missing artifact throws; no-more page reports total files not no matches.
- dependencies_and_callers: Search tool, internal URL router, artifact handling.
- edge_cases_or_failure_modes: Range-limited virtual content, mixed file/internal output, log filtering, pagination exhaustion.
- validation_or_tests: Assertions at lines 118-370.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2739 `file` `packages/coding-agent/test/utils/git-clone.test.ts`
- cursor: `[_]`
- core_role: Tests git clone helper checkout of explicit SHA.
- algorithmic_behavior: Creates repo, clones with non-tip SHA, tip SHA, and invalid SHA; asserts checkout result and cleanup on failure.
- inputs_outputs_state: Inputs are upstream URL, target dir, SHA. Outputs are target HEAD or thrown error and removed target dir.
- gates_or_invariants: Non-tip SHA checkout must work; invalid SHA cleans target.
- dependencies_and_callers: Git clone utility used by workflows/plugins/remote tasks.
- edge_cases_or_failure_modes: Tip SHA fast path, non-tip detached checkout, failed checkout cleanup.
- validation_or_tests: Assertions at lines 61-76.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2769 `file` `packages/coding-agent/test/workflow/task-tool-runtime.test.ts`
- cursor: `[_]`
- core_role: Tests workflow task tool runtime adapter.
- algorithmic_behavior: Mocks `TaskTool.create`, invokes workflow adapter, validates params/data mapping, disables async in child settings, sets completion lifecycle to park, and propagates abort signal.
- inputs_outputs_state: Inputs are workflow runtime args/session/settings/signal. Outputs are task results, exit codes, captured child session settings and signal.
- gates_or_invariants: Parent settings remain unchanged; child async disabled; park lifecycle set; abort signal is forwarded.
- dependencies_and_callers: Workflow runtime and task tool integration.
- edge_cases_or_failure_modes: Parent setting mutation, dropped abort signal, wrong task params.
- validation_or_tests: Assertions at lines 84-284.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2799 `file` `packages/mnemopi/src/core/index.ts`
- cursor: `[_]`
- core_role: Public barrel for mnemopi core APIs.
- algorithmic_behavior: Re-exports recall feature config, banks, beam, memory, and selected core modules.
- inputs_outputs_state: Inputs are imports; output is public core API.
- gates_or_invariants: Stable export surface.
- dependencies_and_callers: Mnemopi consumers/tests.
- edge_cases_or_failure_modes: Missing export breaks consumers.
- validation_or_tests: Foundation/temporal/beam tests indirect.
- skip_candidate: `yes: barrel-only file`

### OH_MY_HUMANIZE_MAIN-HZ-2829 `file` `packages/mnemopi/src/util/ids.ts`
- cursor: `[_]`
- core_role: Memory id generation helpers.
- algorithmic_behavior: `sha256Hex16` hashes content to 16 hex chars; `generateId` combines timestamp/nonce/hash-ish data; `stableMemoryId` derives deterministic id from content/source.
- inputs_outputs_state: Inputs are strings/bytes, optional source/date. Outputs are compact ids.
- gates_or_invariants: Stable id deterministic for same content/source; generated id includes monotonic/random nonce to avoid collisions.
- dependencies_and_callers: Mnemopi memory storage/entity creation.
- edge_cases_or_failure_modes: Content collision risk limited by 16 hex chars; counter overflow unlikely.
- validation_or_tests: ID collision/consolidation tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2859 `file` `packages/utils/test/mermaid/edge-styles.test.ts`
- cursor: `[_]`
- core_role: Tests Mermaid ASCII edge style rendering.
- algorithmic_behavior: Renders solid/dotted/thick edges in Unicode and ASCII modes, with labels and mixed graph styles, and asserts expected line glyphs/labels/nodes.
- inputs_outputs_state: Inputs are Mermaid graph snippets and render options. Outputs are ASCII/Unicode strings.
- gates_or_invariants: Solid uses `─`/`-`, dotted uses `┄`/`.`/`┆`, thick uses `━`/`=`/`┃`; labels survive.
- dependencies_and_callers: Vendored Mermaid ASCII renderer.
- edge_cases_or_failure_modes: Mixed styles in same graph, vertical dotted/thick edges, ASCII fallback.
- validation_or_tests: Assertions at lines 15-146.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2889 `directory` `packages/coding-agent/src/modes/components/status-line`
- cursor: `[_]`
- core_role: Status line rendering system for interactive mode.
- algorithmic_behavior: Contains component lifecycle, preset definitions, segment renderers, separators, token-rate calculation, git utilities, context thresholds, and shared types. Renders configurable segments from `SegmentContext`.
- inputs_outputs_state: Inputs are session/model/context/git/cost/time/collab/subagent/usage settings. Outputs are rendered segment strings with colors/separators and memoized context/git data.
- gates_or_invariants: Presets define stable segment order; context warning thresholds combine percent and absolute tokens; git-backed segments avoid unnecessary work when absent; token rate needs minimum duration.
- dependencies_and_callers: Interactive mode UI and status-line settings.
- edge_cases_or_failure_modes: Unknown preset, null context window, scratch path classification, git failure, usage reset formatting.
- validation_or_tests: Status-line path and usage-row tests cover adjacent UI behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2919 `file` `crates/pi-shell/src/minimizer/filters/python.rs`
- cursor: `[_]`
- core_role: Output minimizer for Python tools (`pytest`, `mypy`, `ruff format`).
- algorithmic_behavior: Detects supported Python tool/subcommand, filters pytest output preserving failure/error bodies and compact summary, handles success noise, caps failure/error counts separately, summarizes mypy diagnostics, and compacts ruff format output.
- inputs_outputs_state: Inputs are command context, raw stdout/stderr text, exit code. Outputs are minimized text and metadata.
- gates_or_invariants: Real assertion tracebacks are preserved before collection-error banners; max pytest failures is 10; success output reduces to summary; ruff unchanged/reformat lines compacted.
- dependencies_and_callers: Native shell minimizer used by bash tool.
- edge_cases_or_failure_modes: Huge pytest progress noise, XFAIL/XPASS, collection errors exceeding cap, mixed failures/errors, verbose pass lines, ruff no-op.
- validation_or_tests: Inline tests from line 419 through 715 validate supports, pytest failures/success/caps, mypy, ruff, and collection-error prioritization.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2949 `file` `packages/ai/src/utils/schema/draft.ts`
- cursor: `[_]`
- core_role: JSON Schema draft upgrade utility to 2020-12.
- algorithmic_behavior: Converts refs, copies/merges schema maps, combines schemas, upgrades tuple/prefix items, converts dependencies to dependentRequired/dependentSchemas, handles nullable variants, detects whether upgrade is needed with cycle guards, and performs cached recursive upgrade.
- inputs_outputs_state: Inputs are arbitrary JSON schema objects. Outputs are upgraded schema or original object, and boolean upgrade-needed result.
- gates_or_invariants: WeakMap prevents cycles; non-schema value keys are not recursively upgraded; `$schema` updated to 2020-12 when needed; nullability preserved.
- dependencies_and_callers: AI tool/schema strict mode and provider schema normalization.
- edge_cases_or_failure_modes: Recursive schemas, mixed dependencies, `items` arrays, nullable `type`, `anyOf` null variant, `$ref` conversion.
- validation_or_tests: Schema dereference/strict mode tests likely cover adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2979 `file` `packages/coding-agent/src/cli/gallery-fixtures/search.ts`
- cursor: `[_]`
- core_role: Gallery fixture definitions for search tool demos.
- algorithmic_behavior: Exports predefined search fixtures with args/results for CLI gallery rendering.
- inputs_outputs_state: Inputs are fixture keys; output is `GalleryFixture` map.
- gates_or_invariants: Fixture shape must match gallery renderer.
- dependencies_and_callers: CLI gallery/demo mode.
- edge_cases_or_failure_modes: Stale fixture schema or unrealistic output.
- validation_or_tests: Gallery tests likely indirect.
- skip_candidate: `yes: static fixture data, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3009 `file` `packages/coding-agent/src/edit/hashline/diff.ts`
- cursor: `[_]`
- core_role: Computes hashline edit preview diffs for full patches and sections.
- algorithmic_behavior: Reads original section text (with small cache), resolves preview edits, detects anchor-scoped edits, applies preview edits, creates mismatch errors, inserts cursor line, builds streaming section diffs, and exposes `computeHashlineSectionDiff`/`computeHashlineDiff`.
- inputs_outputs_state: Inputs are patch sections, file paths, streaming flag, edit list. Outputs are diff text/metadata and errors.
- gates_or_invariants: Cached reads key by mtime/size with max 8 entries; mismatch errors include expected/current context; streaming diff handles cursor insertion.
- dependencies_and_callers: Hashline edit UI/tool preview.
- edge_cases_or_failure_modes: File changed since preview, anchor mismatch, streaming partial edit, large file cache eviction.
- validation_or_tests: Hashline edit-per-file diff tests adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3039 `file` `packages/coding-agent/src/eval/py/prelude.ts`
- cursor: `[_]`
- core_role: Tiny Python eval prelude export.
- algorithmic_behavior: Contains static prelude string used by Python eval runtime.
- inputs_outputs_state: No dynamic input; output is prelude content.
- gates_or_invariants: Must stay syntactically valid for injected Python.
- dependencies_and_callers: Python eval executor.
- edge_cases_or_failure_modes: Invalid prelude breaks every Python cell.
- validation_or_tests: Python executor timeout/eval tests indirect.
- skip_candidate: `yes: static prelude, minimal algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3069 `file` `packages/coding-agent/src/extensibility/plugins/index.ts`
- cursor: `[_]`
- core_role: Barrel for plugin extensibility modules.
- algorithmic_behavior: Re-exports doctor, git-url, loader, manager, marketplace, parser, and types.
- inputs_outputs_state: Inputs are imports; output is public plugin module surface.
- gates_or_invariants: Export paths stable for SDK/plugins.
- dependencies_and_callers: Plugin tests and consumers.
- edge_cases_or_failure_modes: Missing re-export breaks public API.
- validation_or_tests: Plugin extension discovery tests indirect.
- skip_candidate: `yes: barrel-only file`

### OH_MY_HUMANIZE_MAIN-HZ-3099 `file` `packages/coding-agent/src/modes/components/agent-hub.ts`
- cursor: `[_]`
- core_role: Interactive Agent Hub overlay for viewing/controlling main and subagents.
- algorithmic_behavior: Registers persisted subagents from session files, paginates/sorts agent refs, sanitizes transcript/output lines, handles keyboard navigation/tap windows, chats/kills/revives agents through remote or lifecycle deps, incrementally reads transcript files, and refreshes debounced chat state.
- inputs_outputs_state: Inputs are agent registry, lifecycle, session file dirs, remote APIs, keyboard/mouse events. Outputs are overlay render lines, selected agent state, chat actions, lifecycle commands, transcript snippets.
- gates_or_invariants: Page size 15; line width clamped; status order running/idle/parked/aborted; workflow operator tasks identified specially; incremental file reads track byte offsets.
- dependencies_and_callers: Interactive mode agent management and collab/subagent registry.
- edge_cases_or_failure_modes: Missing session file, stale persisted subagent refs, remote command failure, parked revival race, long lines, left-tap timing.
- validation_or_tests: Registry lifecycle tests and Agent Hub UI tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3129 `file` `packages/coding-agent/src/modes/components/logout-account-selector.ts`
- cursor: `[_]`
- core_role: TUI selector for choosing accounts to log out.
- algorithmic_behavior: Renders up to 10 visible accounts, tracks selection/navigation, handles confirm/cancel keys, and emits selected account.
- inputs_outputs_state: Inputs are account list and key events. Outputs are rendered rows and selection/cancel callbacks.
- gates_or_invariants: Max visible rows 10; selected row highlighted; disabled/empty handling via component state.
- dependencies_and_callers: Setup/account logout UI.
- edge_cases_or_failure_modes: Overflow account list, no accounts, cancelled selection.
- validation_or_tests: Selector overflow tests cover similar component behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3159 `file` `packages/coding-agent/src/modes/components/user-message-selector.ts`
- cursor: `[_]`
- core_role: TUI component for selecting previous user messages.
- algorithmic_behavior: Builds `UserMessageList`, renders sanitized/truncated message rows, handles navigation/search/selection/cancel, and wraps in selector container.
- inputs_outputs_state: Inputs are user message items and keyboard events. Outputs are selected message or cancellation plus rendered list.
- gates_or_invariants: Text is sanitized and width-limited; selection index remains in bounds; render width drives truncation.
- dependencies_and_callers: Interactive message reuse/history UI.
- edge_cases_or_failure_modes: Empty list, very long/multiline messages, cursor bounds.
- validation_or_tests: Selector and input-controller tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3189 `file` `packages/coding-agent/src/modes/setup-wizard/startup-splash.ts`
- cursor: `[_]`
- core_role: Startup splash overlay component.
- algorithmic_behavior: Renders splash component, owns overlay focus, waits for user/timeout flow via `runStartupSplash`.
- inputs_outputs_state: Inputs are run options and input events. Outputs are rendered splash and resolved promise.
- gates_or_invariants: Focus owner must release cleanly; splash should not block indefinitely when dismissed.
- dependencies_and_callers: Setup wizard startup.
- edge_cases_or_failure_modes: Focus leak, never-resolved splash.
- validation_or_tests: Setup wizard tests indirectly cover startup UI.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3219 `file` `packages/coding-agent/src/tools/browser/tab-protocol.ts`
- cursor: `[_]`
- core_role: Shared protocol types for browser tab worker transport.
- algorithmic_behavior: Defines worker init payloads, observations, screenshots, session snapshots, inbound/outbound worker messages, tool replies, ready info, run errors, and transport interface.
- inputs_outputs_state: Inputs/outputs are typed worker messages and transferable payloads.
- gates_or_invariants: Discriminated message types are stable; errors use `RunErrorPayload`; transport exposes post/close hooks.
- dependencies_and_callers: Browser tab worker and browser tools.
- edge_cases_or_failure_modes: Protocol mismatch between host and worker.
- validation_or_tests: Browser tool tests indirect.
- skip_candidate: `yes: protocol type file, minimal runtime logic`

### OH_MY_HUMANIZE_MAIN-HZ-3249 `file` `packages/coding-agent/src/web/scrapers/hackage.ts`
- cursor: `[_]`
- core_role: Special web scraper for Hackage package pages.
- algorithmic_behavior: Compares versions, extracts Cabal fields/description, parses cabal content, fetches package/version metadata, and returns normalized special-handler content.
- inputs_outputs_state: Inputs are Hackage URLs/fetch responses. Outputs are scraped Markdown/text metadata.
- gates_or_invariants: Version compare numeric-ish; cabal fields parsed by name; unsupported URLs fall through.
- dependencies_and_callers: Web scraper special-handler registry.
- edge_cases_or_failure_modes: Missing cabal file, unusual version strings, multiline descriptions, network errors.
- validation_or_tests: Web scraper academic tests cover adjacent scrapers; Hackage likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3279 `file` `packages/coding-agent/src/web/scrapers/repology.ts`
- cursor: `[_]`
- core_role: Special web scraper for Repology package pages/API.
- algorithmic_behavior: Formats package status, prettifies repo names, fetches Repology package data, groups/sorts versions/repos/statuses, and returns Markdown summary.
- inputs_outputs_state: Inputs are Repology URL/package name/fetch JSON. Outputs are package version/status summary content.
- gates_or_invariants: Status strings map to indicators; repo names prettified; unsupported/malformed URLs fall through.
- dependencies_and_callers: Web scraper special-handler registry.
- edge_cases_or_failure_modes: Empty package data, unknown status, API/network failure, malformed JSON.
- validation_or_tests: Web scraper tests adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3309 `file` `packages/coding-agent/test/extensibility/custom-commands/ci-green.test.ts`
- cursor: `[_]`
- core_role: Tests custom command output for CI-green release guidance.
- algorithmic_behavior: Mocks git tags and asserts command text includes latest alpha tag when present and omits timeout boilerplate; handles no-tag case.
- inputs_outputs_state: Inputs are tag list. Outputs are generated command prompt/text.
- gates_or_invariants: Tag-dependent content must be conditional.
- dependencies_and_callers: Custom command extension system.
- edge_cases_or_failure_modes: No tags, stale hardcoded timeout text.
- validation_or_tests: Assertions at lines 38-48.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3339 `file` `packages/coding-agent/test/modes/components/tree-selector-last-branch-gutter-2325.test.ts`
- cursor: `[_]`
- core_role: Regression test for tree selector branch gutter rendering.
- algorithmic_behavior: Builds tree selector rows and asserts last branch uses `└─`, chain columns remain stable, child rows do not show stale vertical bars, and sibling rows use correct branch connectors.
- inputs_outputs_state: Inputs are tree nodes/messages. Outputs are rendered rows.
- gates_or_invariants: Last branch gutter must terminate; descendants align under stable chain columns.
- dependencies_and_callers: Tree selector component/session branch UI.
- edge_cases_or_failure_modes: Last branch vertical line leakage, nested sibling misalignment.
- validation_or_tests: Assertions at lines 84-106.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3369 `file` `packages/coding-agent/test/tools/web-scrapers/academic.test.ts`
- cursor: `[_]`
- core_role: Tests academic web scraper special handlers.
- algorithmic_behavior: Provides sample URLs/HTML/JSON and asserts Semantic Scholar/arXiv-like scraping content/methods, fallback, and extracted metadata.
- inputs_outputs_state: Inputs are academic URLs and mocked fetch responses. Outputs are scraper result method/content.
- gates_or_invariants: Academic handlers must identify method and include title/metadata; unsupported pages return null/fallback.
- dependencies_and_callers: Web search/scraper pipeline.
- edge_cases_or_failure_modes: Missing metadata, malformed pages, network failures.
- validation_or_tests: Assertions begin at lines 17-25 and continue through file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3399 `file` `packages/collab-web/src/components/shell/ConnectScreen.tsx`
- cursor: `[_]`
- core_role: React connection screen for collab web client.
- algorithmic_behavior: Renders default name input, error message, and connect form; calls `onConnect` with chosen display name.
- inputs_outputs_state: Inputs are defaultName/error/user input. Outputs are React UI and submit callback.
- gates_or_invariants: Form submit should prevent default and preserve entered name.
- dependencies_and_callers: Collab web shell.
- edge_cases_or_failure_modes: Empty name, displayed connection error.
- validation_or_tests: Collab web tests likely indirect.
- skip_candidate: `yes: UI form component, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3429 `file` `packages/collab-web/src/tool-render/tools/search-bm25.tsx`
- cursor: `[_]`
- core_role: React renderer for BM25 search tool output in collab web.
- algorithmic_behavior: Parses unknown result matches into typed `Bm25Match`, normalizes string lists, renders summary from args/result, and body with file matches/snippets.
- inputs_outputs_state: Inputs are tool args/result unknown JSON. Outputs are React summary/body nodes.
- gates_or_invariants: Unknown match values are filtered; string lists only include strings; renderer must tolerate malformed result.
- dependencies_and_callers: Collab web tool-render registry.
- edge_cases_or_failure_modes: Missing matches, non-string snippets, malformed score/path.
- validation_or_tests: Tool renderer tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3459 `file` `packages/stats/src/client/data/charts.ts`
- cursor: `[_]`
- core_role: Tiny chart data constant module.
- algorithmic_behavior: Exports chart-related constants/config used by stats client.
- inputs_outputs_state: No dynamic input; output is constant values.
- gates_or_invariants: Constant names/values stable for charts.
- dependencies_and_callers: Stats dashboard charts.
- edge_cases_or_failure_modes: Incorrect constant affecting display.
- validation_or_tests: Stats client tests indirect.
- skip_candidate: `yes: constant-only UI data file`

### OH_MY_HUMANIZE_MAIN-HZ-3489 `file` `packages/utils/src/vendor/mermaid-ascii/types.ts`
- cursor: `[_]`
- core_role: Shared Mermaid graph/render type definitions.
- algorithmic_behavior: Defines graph/node/edge/subgraph/position/render option interfaces and edge/node shape/style unions.
- inputs_outputs_state: Inputs/outputs are type-level contracts for parsed and positioned diagrams.
- gates_or_invariants: Shape/style unions constrain parser/renderer compatibility.
- dependencies_and_callers: Vendored Mermaid parser/converter/renderer.
- edge_cases_or_failure_modes: Type drift between parser and renderer.
- validation_or_tests: Mermaid edge/golden tests validate runtime users.
- skip_candidate: `yes: type-only definitions, no runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3519 `file` `packages/coding-agent/src/eval/js/shared/rewrite-imports.ts`
- cursor: `[_]`
- core_role: JavaScript/TypeScript eval source transformer for imports, globals, TS stripping, and wrapper generation.
- algorithmic_behavior: Lazily loads Babel parser, rewrites static imports into `__omp_import__` calls, collects/rewrites module specifiers, rewrites dynamic imports, demotes top-level lexical declarations, optionally publishes globals, returns final expression, detects async wrapper needs, strips TypeScript via Bun transpiler, and wraps code for eval.
- inputs_outputs_state: Inputs are JS/TS source and transform options. Outputs are rewritten source, collected specifiers, or wrapped executable code.
- gates_or_invariants: Parse failures fall back conservatively; dynamic import callee preserves native fallback; lexical binding names collected recursively; execution boundaries avoid rewriting nested functions/classes incorrectly.
- dependencies_and_callers: JS eval worker/runtime.
- edge_cases_or_failure_modes: TSX syntax, import attributes, destructuring bindings, top-level await, final expression ambiguity, dynamic import nested in strings/comments avoided by AST.
- validation_or_tests: Eval JS tests likely cover; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3549 `file` `packages/coding-agent/src/modes/components/status-line/presets.ts`
- cursor: `[_]`
- core_role: Status line preset definitions and lookup.
- algorithmic_behavior: Defines `STATUS_LINE_PRESETS` mapping preset names to segment/separator/layout definitions and `getPreset`.
- inputs_outputs_state: Input is preset name; output is preset definition.
- gates_or_invariants: Preset names must exist; segment ids must match renderer registry.
- dependencies_and_callers: Status line component/settings.
- edge_cases_or_failure_modes: Unknown preset or stale segment id.
- validation_or_tests: Status-line tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3579 `file` `packages/coding-agent/src/web/search/providers/tavily.ts`
- cursor: `[_]`
- core_role: Tavily web search provider implementation.
- algorithmic_behavior: Finds API key, builds bounded request body, calls Tavily search endpoint, maps API results to common search response, extracts error messages, and defines `TavilyProvider`.
- inputs_outputs_state: Inputs are search params (`query`, max results, topic/include fields) and API key/env/settings. Outputs are normalized search results or errors.
- gates_or_invariants: Default result count 5, max 20; request body includes only supported params; missing API key prevents provider use.
- dependencies_and_callers: Web search provider registry.
- edge_cases_or_failure_modes: API error body, malformed result, missing key, over-limit result count, network failure.
- validation_or_tests: Web search/search provider tests indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3609 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/circle.ts`
- cursor: `[_]`
- core_role: Circle shape renderer for Mermaid ASCII nodes.
- algorithmic_behavior: Exports `circleRenderer` that renders a circular-ish box shape into canvas/role canvas using node dimensions and theme roles.
- inputs_outputs_state: Inputs are shape render context/node dimensions. Outputs are canvas characters/roles.
- gates_or_invariants: Shape renderer must satisfy `ShapeRenderer` interface and align with grid/canvas dimensions.
- dependencies_and_callers: Mermaid ASCII draw/shape registry.
- edge_cases_or_failure_modes: Small node dimensions, Unicode/ASCII mode mismatch, role canvas misalignment.
- validation_or_tests: Mermaid golden/edge-style tests indirectly cover shape rendering.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 121 item evidence sections counted, one per assigned non-`none` row.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`