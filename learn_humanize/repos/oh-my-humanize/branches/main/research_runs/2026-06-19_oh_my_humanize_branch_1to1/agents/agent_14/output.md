# agent_14 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-014 `file` `rust-analyzer.toml`
- cursor: `[_]`
- core_role: Rust workspace tooling configuration, not runtime code.
- algorithmic_behavior: Configures rust-analyzer import insertion/rewrite behavior: crate-level grouping, enforced granularity, prelude preference, and `crate` prefix at `rust-analyzer.toml:1-5`.
- inputs_outputs_state: Input is rust-analyzer’s import assist/rewrite pipeline over Rust source files; output is editor/tooling import organization. No repo runtime state is mutated by this file.
- gates_or_invariants: Import granularity is enforced and grouped by crate; `preferNoStd = false` and `preferPrelude = true` bias import choices.
- dependencies_and_callers: Consumed by rust-analyzer in editor or CI tooling contexts for Rust files under `crates/*`.
- edge_cases_or_failure_modes: Misclassification risk is high for runtime analysis because this affects developer tooling only. Bad settings can produce unwanted import rewrites, not runtime failures.
- validation_or_tests: No direct test file; validated implicitly by rust-analyzer behavior while editing Rust crates.
- skip_candidate: `yes: tooling-only configuration, no application algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-044 `file` `docs/ai-schema-normalize.md`
- cursor: `[_]`
- core_role: Architecture contract for provider-specific JSON Schema normalization before tool schemas are sent to model APIs.
- algorithmic_behavior: Documents unified walkers in `packages/ai/src/utils/schema/normalize.ts`, entry points like `normalizeSchemaForGoogle`, `normalizeSchemaForCCA`, `normalizeSchemaForMCP`, OpenAI strict-mode sanitization/enforcement, and dispatcher mappings at `docs/ai-schema-normalize.md:13-54`.
- inputs_outputs_state: Inputs are JSON Schema, Zod-emitted shapes, MCP `inputSchema`, provider tool definitions, and strict-mode flags. Outputs are provider-compatible schemas, strict-mode metadata, or fallback empty object schemas. State includes static fingerprint cache behavior for catalog model resolution at `docs/ai-schema-normalize.md:138-160`.
- gates_or_invariants: Normalizer must upgrade/dereference, camel-case snake-case keys, collapse nullable forms, strip unsupported provider keys, run `isValidJsonSchema` for CCA fallback, and fail-open strict enforcement only when enforcement throws (`docs/ai-schema-normalize.md:60-107`).
- dependencies_and_callers: References `normalize.ts`, `adapt.ts`, `meta-validator.ts`, provider transports, MCP tool bridge, and catalog `model-cache.ts`.
- edge_cases_or_failure_modes: Covers `$ref` sibling merge precedence, recursive refs, `oneOf` to `anyOf`, nullable wrapping, type arrays, and strict-mode fallback on incompatible keywords (`docs/ai-schema-normalize.md:109-136`).
- validation_or_tests: Backed by `packages/ai/test/google-tool-schema.test.ts`, `packages/ai/test/anthropic-alignment.test.ts`, and `packages/ai/src/utils/schema/meta-validator.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-074 `file` `docs/slash-command-internals.md`
- cursor: `[_]`
- core_role: Runtime design document for slash-command discovery, deduplication, autocomplete surfacing, and prompt expansion in `packages/coding-agent`.
- algorithmic_behavior: Defines capability-based command loading, provider priorities, first-wins deduplication, source-specific paths, frontmatter parsing, bundled fallbacks, interactive refresh, prompt pipeline order, and expansion semantics (`docs/slash-command-internals.md:21-244`).
- inputs_outputs_state: Inputs are command markdown files, provider registries, extension commands, skill commands, prompt templates, and user slash text. Outputs are `SlashCommand` capability items, `FileSlashCommand` runtime objects, autocomplete entries, transformed prompt text, or handled command side effects.
- gates_or_invariants: Highest provider priority wins; project/user precedence varies by provider; native frontmatter parse failures are fatal while user/project failures warn and fallback; streaming prompts require explicit `"steer"` or `"followUp"` behavior (`docs/slash-command-internals.md:23-48`, `121-124`, `223-235`).
- dependencies_and_callers: Points to `src/extensibility/slash-commands.ts`, capability registry, discovery providers, `AgentSession.prompt`, interactive controllers, and UI helpers (`docs/slash-command-internals.md:5-19`).
- edge_cases_or_failure_modes: Unknown slash commands pass through as ordinary prompts, unmatched quotes are tolerated, no continuous watcher exists, and extension/custom command errors are treated as handled (`docs/slash-command-internals.md:200-244`).
- validation_or_tests: Covered by slash-command tests such as `packages/coding-agent/test/slash-commands/btw.test.ts`, command expansion tests, and discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-104 `file` `scripts/inline-functions.ts`
- cursor: `[_]`
- core_role: AST rewrite utility that inlines small top-level TypeScript helper functions into call sites while preserving semantics.
- algorithmic_behavior: Uses `ts-morph` to find non-exported top-level function declarations, reject unsafe shapes, invert leading guard clauses, substitute parameters, hoist effectful args, rename colliding locals, apply replacements bottom-up, and optionally format/write or show diff. Key functions include `isPureExpr` at `scripts/inline-functions.ts:215`, `negate` at `314`, `analyze` at `594`, `collectCandidates` at `733`, `buildReplacement` at `836`, `inlineFile` at `948`, and CLI driver at `984`.
- inputs_outputs_state: Inputs are source file paths and flags like `--write`, `--name`, `--max-statements`, `--list`, and `--strict-effects`. Outputs are inlined source text, dry-run diffs, candidate listings, or formatted files. State is the in-memory ts-morph project and replacement plan list.
- gates_or_invariants: Skips exported, async, generator, generic, overloaded, recursive, `this`/`super`/`arguments`, `var`, parameter writes, escaping return/break/continue, non-statement call sites, spread args, shadowed free names, and excessive tail statements.
- dependencies_and_callers: Depends on Bun shell, `node:fs/promises`, `node:path`, `node:util.parseArgs`, `ts-morph`, `biome`, and `git diff --no-index`.
- edge_cases_or_failure_modes: Guard inversion preserves sequential guard short-circuiting; default mode treats plain property access as pure while strict mode hoists member access; malformed CLI flags and invalid max statements set `process.exitCode`.
- validation_or_tests: No direct test observed; script self-documents correctness constraints and relies on dry-run diff plus formatter.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-134 `directory` `packages/coding-agent/test`
- cursor: `[_]`
- core_role: Primary contract test suite for the coding-agent package.
- algorithmic_behavior: Recursively contains 905 files spanning session lifecycle, tool execution, LSP, MCP, browser tools, config, task/subagent orchestration, workflow runtime, telemetry, setup, update, SSH, web search/scrapers, TUI integration, and regression repros.
- inputs_outputs_state: Inputs are Bun test fixtures, mocked sessions/transports, temporary repos/files, mocked workers, and fake providers. Outputs are assertions over user-visible state transitions, rendered text, protocol frames, tool results, persisted session records, and error mapping.
- gates_or_invariants: Enforces full-suite-safe mocks, no global module leaks, deterministic ordering, resource cleanup, bounded retries, schema compatibility, and render sanitization across many subsystems.
- dependencies_and_callers: Tests package exports from `@oh-my-pi/pi-coding-agent`, sibling packages, local fixtures, mocked MCP/RPC/worker transports, and temporary filesystem state.
- edge_cases_or_failure_modes: Contains targeted regressions for empty stops, silent aborts, worker host re-entry, split internal URL selectors, issue/PR protocols, web scrapers, async jobs, and workspace tree truncation.
- validation_or_tests: This directory is validation; focused examples include `packages/coding-agent/test/agent-session-empty-stop-guard.test.ts`, `async-job-manager.test.ts`, `workspace-tree.test.ts`, and `tools/*`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-164 `directory` `python/omp-rpc/tests`
- cursor: `[_]`
- core_role: Python-side RPC client and protocol conformance tests.
- algorithmic_behavior: Recursively contains `test_client.py`, `test_host_uris.py`, `test_protocol.py`, `test_user_group.py`, and package init. It validates command builder options, prompt lifecycle, typed listeners, host tool/URI bridging, UI round trips, event parsing, stop behavior, and process-group termination.
- inputs_outputs_state: Inputs are fake RPC server frames, host callbacks, Python client commands, and subprocess/server fixtures. Outputs are parsed protocol objects, client events, exceptions, and shutdown state.
- gates_or_invariants: Protocol parsing rejects invalid thinking levels, invalid effort, invalid system prompt shapes, invalid extension UI methods, and invalid assistant done reasons (`python/omp-rpc/tests/test_protocol.py:185-272`).
- dependencies_and_callers: Depends on Python `unittest`/`pytest`, `RpcClient`, fake server helpers, and CLI subprocesses.
- edge_cases_or_failure_modes: Tests id-less error correlation, listener exceptions, bounded stderr history, event-history overflow, stop unblocking waiters, read/write host URI handler errors, and user/group threading.
- validation_or_tests: This directory is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-194 `file` `docs/tools/lsp.md`
- cursor: `[_]`
- core_role: Runtime contract for the `lsp` tool: diagnostics, navigation, refactor, capabilities, and raw LSP requests.
- algorithmic_behavior: Documents inputs/actions, result shape, config loading, server routing, client creation, diagnostics caching, open-file sync, action-specific flows, and timeout behavior. Source map and flow start at `docs/tools/lsp.md:5-52`.
- inputs_outputs_state: Inputs are action, file/glob, line/column/symbol, rename target, query, args, timeout. Outputs are text plus `LspToolDetails`, diagnostics, symbols, locations, code actions, rename edits, status, capabilities, or raw response.
- gates_or_invariants: Tool registration is gated by session and `settings.get("lsp.enabled")`; config is cached per cwd; routing selects extension/basename matches and primary servers before linters; validation failures often return ordinary failed tool results instead of throwing (`docs/tools/lsp.md:43-51`).
- dependencies_and_callers: References `src/tools/lsp.ts`, `src/lsp/config.ts`, `client.ts`, default server definitions, custom linter clients, tool registration, and timeout clamping (`docs/tools/lsp.md:7-21`).
- edge_cases_or_failure_modes: Handles absent servers, stale diagnostics, client startup failures, custom linter routing exclusions, project-load progress, and aborts via `ToolAbortError`.
- validation_or_tests: Backed by `packages/coding-agent/test/tools/lsp-*` tests and `packages/coding-agent/test/task/subagent-lsp.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-224 `file` `scripts/session-stats/read_optimizer.py`
- cursor: `[_]`
- core_role: Offline optimizer for read-tool line-window configuration using historical stats DB replay.
- algorithmic_behavior: Parses read selectors, loads `ss_tool_calls`/`ss_tool_results`, groups calls by `(session,file)`, replays candidate configs with coverage intervals, estimates token/call savings, computes Pareto/recommended configs, prints summaries, and plots `read-optimizer.png`. Key functions: `parse_path_selector` at `scripts/session-stats/read_optimizer.py:125`, `parse_call` at `167`, `requested_interval` at `221`, `add_interval` at `261`, `replay` at `316`, `pareto` at `446`, and `main` at `565`.
- inputs_outputs_state: Inputs are `~/.omp/stats.db`, date/grid CLI flags, current read defaults, and historical read call rows. Outputs are terminal reports and `scripts/session-stats/out/read-optimizer.png`. State includes per-file coverage interval lists and replay counters.
- gates_or_invariants: Skips invalid JSON/path, URLs, directories, and non-text extensions without selectors; clamps token-per-line; requires DB existence; enforces truncation constraints when ranking.
- dependencies_and_callers: Uses Python stdlib, SQLite, matplotlib, numpy, and current coding-agent read defaults embedded in constants.
- edge_cases_or_failure_modes: Missing DB exits; malformed selector falls back to `other`; byte-limit estimate can cap token estimate; unmodelled raw/conflicts calls are charged directly.
- validation_or_tests: No direct test observed; intended as research/analysis script with deterministic replay output.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-254 `directory` `packages/coding-agent/src/config`
- cursor: `[_]`
- core_role: Coding-agent configuration, settings, model registry/resolution, keybindings, config files, MCP schema, file locks, and dynamic provider discovery.
- algorithmic_behavior: Recursively contains 16 files and 12,610 lines. Major roles: settings schema/default/UI metadata (`settings-schema.ts`), runtime settings singleton and hooks (`settings.ts`), model registry/discovery/resolution (`model-registry.ts`, `model-discovery.ts`, `model-resolver.ts`), provider model config validation (`models-config.ts`), config file migration/loading (`config-file.ts`), command-backed config value resolution (`resolve-config-value.ts`), keybindings migration/rendering (`keybindings.ts`), and lock files (`file-lock.ts`).
- inputs_outputs_state: Inputs are YAML/JSON config files, env vars, provider auth, model catalogs, cwd/profile scope, keybinding files, and command strings. Outputs are typed settings, available models, selected model roles, provider configs, lock acquisition/release, and normalized keybinding maps.
- gates_or_invariants: ArkType schemas validate models/settings; config migration preserves loaded paths; model resolution applies aliases, scopes, enabled/disabled filters, auth fallback, and thinking selectors; file lock stale detection uses pid/token data.
- dependencies_and_callers: Used by CLI startup, sessions, tools, tiny worker env, auth broker, update/setup flows, model selection UI, and discovery providers.
- edge_cases_or_failure_modes: Covers stale locks, command config cache/inflight dedupe, path-scoped arrays, provider auth modes, OpenRouter routing suffixes, Ollama/llama.cpp discovery, disabled providers, and keybinding migrations.
- validation_or_tests: Covered by `packages/coding-agent/test/config-*`, `settings-*`, `keybindings-*`, model selection, profile, and discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-284 `directory` `packages/coding-agent/src/tiny`
- cursor: `[_]`
- core_role: Local tiny-model subsystem for title generation, memory completion, and auto-thinking local classification.
- algorithmic_behavior: Recursively contains device/dtype normalization, model registries, title text normalization, client/worker protocol, subprocess lifecycle, and HuggingFace Transformers worker. Key files: `device.ts`, `dtype.ts`, `models.ts`, `text.ts`, `title-client.ts`, `title-protocol.ts`, `worker.ts`.
- inputs_outputs_state: Inputs are settings/env (`providers.tinyModelDevice`, dtype), prompt text, model keys, download/generate requests, and worker messages. Outputs are titles, completions, progress events, pongs, errors, and smoke-test results. State includes a singleton `TinyTitleClient`, pending request map, worker subprocess, `pipelines` cache, and serialized `generateQueue`.
- gates_or_invariants: Darwin WebGPU is avoided by CPU ordering; dtype/device env values are normalized; local title input is stripped/truncated; worker host re-entry uses `__omp_worker_tiny_inference`; failed worker requests trigger recycling and queued completion faulting.
- dependencies_and_callers: Depends on `@huggingface/transformers`, settings, worker host entry, prompts, auto-thinking classifier, title generator, and memory tools.
- edge_cases_or_failure_modes: Low-signal inputs return sentinel/no title; compiled runtime preparation can fail; model load falls back across devices; stop criteria scans recent decoded tokens.
- validation_or_tests: Covered by `tiny-device.test.ts`, `tiny-dtype.test.ts`, `tiny-text.test.ts`, `tiny-title-generator.test.ts`, `tiny-worker-env.test.ts`, and `issue-1940-repro.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-314 `directory` `packages/coding-agent/test/task`
- cursor: `[_]`
- core_role: Focused contract tests for task/subagent spawning, batching, rendering, worktree isolation, LSP inheritance, and subprocess guard behavior.
- algorithmic_behavior: Recursively contains task tool tests for schema gating, async job spawning, batch normalization, role specialization, output naming, coordination advisories, autoloaded skills, yield reminders, wall-clock/request budgets, nested live rendering, progress sorting, and worktree merge/stash behavior.
- inputs_outputs_state: Inputs are mocked agents, task tool args, temporary repos, schema fixtures, async job manager, role strings, and rendered component state. Outputs are spawn results, progress details, warnings, stderr, job states, rendered rows, and isolated worktree outcomes.
- gates_or_invariants: Enforces no `schema` per-call arg, required batch context, duplicate ID rejection, request budget steer/abort, max runtime abort, yield reminder retries, subagent LSP disabled by default, and worktree preservation of user dirty state.
- dependencies_and_callers: Tests `TaskTool`, executor, renderers, task commands, worktree helpers, model registry/auth forwarding, and TUI rendering.
- edge_cases_or_failure_modes: Handles missing yields, null yields, malformed yield slot shape, late successful yield after timeout, nested snapshots pointing at themselves, duplicate names, role max length, and baseline dirty state committed by isolated task.
- validation_or_tests: This directory is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-344 `file` `crates/pi-iso/src/linux_reflink.rs`
- cursor: `[_]`
- core_role: Linux reflink isolation backend for copy-on-write workspace isolation.
- algorithmic_behavior: Defines `LinuxReflinkBackend` and exposes it as an `IsolationBackend` via `backend()` (`crates/pi-iso/src/linux_reflink.rs:18-25`). Linux-only blocks probe/copy using platform reflink behavior; non-Linux blocks return unavailable errors.
- inputs_outputs_state: Inputs are source/destination paths and backend probe calls. Outputs are `ProbeResult`, copied/reflinked filesystem trees, backend kind metadata, or `IsoError` on unsupported platforms. State is filesystem state only.
- gates_or_invariants: `#[cfg(target_os = "linux")]` gates real implementation; non-Linux code paths avoid pretending reflink is available.
- dependencies_and_callers: Implements shared `IsolationBackend` trait from `crate::{BackendKind, IsoResult, IsolationBackend, ProbeResult}` and is used by task worktree isolation helpers.
- edge_cases_or_failure_modes: Filesystem may not support reflinks even on Linux; cross-device copies, symlinks, directory traversal, and platform unavailability are failure surfaces.
- validation_or_tests: Indirectly covered by `packages/coding-agent/test/task/worktree.test.ts`, especially native backend contract mapping and unavailable-backend retry behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-374 `file` `crates/pi-natives/src/text.rs`
- cursor: `[_]`
- core_role: Native text-width, truncation, slicing, wrapping, and segment extraction algorithms exposed to JS via N-API.
- algorithmic_behavior: Implements UTF-16 visible width calculation, ANSI SGR state tracking, OSC 66 metadata/payload scaling, grapheme width handling, macOS Hangul correction, ANSI-preserving wrap, truncate, slice, segment extraction, and `visible_width`. Public N-API functions are at `wrap_text_with_ansi` `crates/pi-natives/src/text.rs:1124`, `truncate_to_width` `1139`, `slice_with_width` `1453`, `extract_segments` `1674`, and `visible_width` `1711`.
- inputs_outputs_state: Inputs are JS strings, width budgets, tab widths, ellipsis mode, ranges, and segment selectors. Outputs are strings, `SliceResult`, `ExtractSegmentsResult`, wrapped line arrays, and width counts. Internal state includes `AnsiState`, pending ANSI reset emission, and interval/segment traversal.
- gates_or_invariants: Tab width clamps to 1..16; ANSI/APC/OSC are zero-width except declared payload display; active SGR is re-emitted across slices/wraps; grapheme clusters are not split on simple paths.
- dependencies_and_callers: Depends on `napi`, `smallvec`, `unicode_segmentation`, `unicode_width`; used by TUI/render utilities for terminal-safe display.
- edge_cases_or_failure_modes: Handles BEL/ST-terminated APC, unclassified escapes in long words, combining marks, wide chars, emoji VS16, tabs, OSC66 scaled partial slices, and early-exit limit.
- validation_or_tests: Built-in Rust tests at `crates/pi-natives/src/text.rs:1717-1937` cover visible width, OSC66, ANSI, slices, and wrapping.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-404 `file` `packages/agent/test/handoff.test.ts`
- cursor: `[_]`
- core_role: Tests handoff/compaction prompt generation in the agent core.
- algorithmic_behavior: Imports `AUTO_HANDOFF_THRESHOLD_FOCUS`, `generateHandoff`, and `renderHandoffPrompt` from compaction (`packages/agent/test/handoff.test.ts:3`) and validates how prior messages/tool calls are summarized for a handoff.
- inputs_outputs_state: Inputs are synthetic agent messages, assistant messages, tool calls, and model metadata. Outputs are handoff prompt text and generated summary behavior.
- gates_or_invariants: Ensures handoff threshold and prompt rendering preserve the contract expected by downstream sessions.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-agent-core/compaction`, `@oh-my-pi/pi-ai` types, Bun test spies, and mocked completion behavior.
- edge_cases_or_failure_modes: Covers dropped/retained context around tool calls and focus threshold behavior.
- validation_or_tests: This file is itself validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-434 `file` `packages/ai/test/anthropic-alignment.test.ts`
- cursor: `[_]`
- core_role: Large alignment suite for Anthropic and Anthropic-compatible request shaping.
- algorithmic_behavior: Validates request fingerprint headers, Claude Code OAuth defaults, cache control placement, max token clamping, beta headers, metadata/device IDs, tool name escaping, strict tool schemas, Cloudflare/Foundry gateway behavior, sampling/thinking rules, task budgets, and cch attestation. Test names span `packages/ai/test/anthropic-alignment.test.ts:141-2092`.
- inputs_outputs_state: Inputs are model specs, auth modes, env/header overrides, tools, messages, metadata, and mocked fetch bodies. Outputs are generated Anthropic request payloads, headers, errors, and stream behavior.
- gates_or_invariants: OAuth/API-key paths diverge deliberately; max tokens clamp to Claude Code cap only for OAuth; strict marking only applies to allowlisted compatible tools; gateway auth overrides caller headers.
- dependencies_and_callers: Exercises Anthropic provider conversion, schema normalization, auth/gateway code, model identity, and stream/cch helpers.
- edge_cases_or_failure_modes: Handles invalid metadata, uppercase hex user hash, tool prefix round trips, open object maps, unsupported schema constraints, incomplete mTLS cert/key pairs, forced tool choice with thinking, and non-Anthropic API bases.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-464 `file` `packages/ai/test/auth-gateway-classify-error.test.ts`
- cursor: `[_]`
- core_role: Tests gateway error classification into status/type buckets.
- algorithmic_behavior: Validates explicit `status`, embedded status extraction, status keyword recognition, rate-limit wording, Codex usage-limit wording, abort classification, and fallback upstream errors (`packages/ai/test/auth-gateway-classify-error.test.ts:5-109`).
- inputs_outputs_state: Inputs are Error objects/messages with status/code wording. Outputs are classified status and type such as authentication, rate limit, invalid request, request aborted, or upstream.
- gates_or_invariants: Incidental three-digit numbers must not be treated as status unless status-like context exists; 400 GenerateContentRequest is not rate-limited.
- dependencies_and_callers: Exercises auth gateway error classifier used by provider/auth proxy paths.
- edge_cases_or_failure_modes: CamelCase/compound "rate" substrings must not match; AbortError maps to 499.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-494 `file` `packages/ai/test/claude-usage-retry.test.ts`
- cursor: `[_]`
- core_role: Tests Claude usage provider retry/backoff contract.
- algorithmic_behavior: Covers retry on 429/503, no retry on 401/404, max retry exhaustion, honoring Retry-After, abortable sleep, and stale lastPayload fallback (`packages/ai/test/claude-usage-retry.test.ts:34-161`).
- inputs_outputs_state: Inputs are mocked HTTP status sequences, retry-after headers, abort signals, and payloads. Outputs are usage response, null, or abort behavior.
- gates_or_invariants: Permanent credential errors do not retry; transient errors retry only up to max; abort signal interrupts backoff.
- dependencies_and_callers: Exercises Claude usage provider around provider registry/account usage UI.
- edge_cases_or_failure_modes: Stale-but-valid payload can be returned when retries exhaust.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-524 `file` `packages/ai/test/google-tool-schema.test.ts`
- cursor: `[_]`
- core_role: Tests Google/Gemini and Cloud Code Assist Claude tool schema normalization.
- algorithmic_behavior: Validates CCA keyword stripping/collapse/fallback, Google sanitizer parity, enum type inference, propertyOrdering propagation, `$ref` cycle handling, snake_case to camelCase conversion, nullable/null union handling, and malformed-keyword fallback (`packages/ai/test/google-tool-schema.test.ts:27-818`).
- inputs_outputs_state: Inputs are mixed JSON Schema/JTD/Zod-like tool schemas and model/provider choices. Outputs are sanitized `parameters` or `parametersJsonSchema` objects.
- gates_or_invariants: CCA Claude must use full normalizer; Google path retains appropriate `anyOf`; snake_case collisions intentionally let snake_case overwrite camelCase.
- dependencies_and_callers: Exercises schema normalizer, Google provider conversion, and CCA Claude path.
- edge_cases_or_failure_modes: Handles properties literally named `properties`, mixed enum/unconstrained unions, recursive refs, bare null schemas, and typeless enums.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-554 `file` `packages/ai/test/issue-967-vision-guard.test.ts`
- cursor: `[_]`
- core_role: Regression tests ensuring non-vision models do not receive image payloads.
- algorithmic_behavior: Tests OpenAI chat-completions, OpenAI Responses, Codex Responses, Anthropic, and Google payload builders strip images when the model lacks vision support (`packages/ai/test/issue-967-vision-guard.test.ts:130-264`).
- inputs_outputs_state: Inputs are messages containing image content and non-vision model specs. Outputs are provider payloads without unsupported image blocks.
- gates_or_invariants: Vision capability controls image inclusion consistently across user and tool-result payloads.
- dependencies_and_callers: Exercises provider message transformation across AI package transports.
- edge_cases_or_failure_modes: Tool-result images are stripped as well as user images; multiple providers are covered.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-584 `file` `packages/ai/test/openai-completions-error-finish-reason.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI completions streaming error finish-reason handling.
- algorithmic_behavior: Verifies `finish_reason: error` maps to retryable error behavior and remains an error even if tool calls appeared earlier (`packages/ai/test/openai-completions-error-finish-reason.test.ts:57-74`).
- inputs_outputs_state: Inputs are mocked streaming chunks with finish reasons and optional tool calls. Outputs are provider errors/retryable classification.
- gates_or_invariants: Error finish reason wins over partial tool-call state.
- dependencies_and_callers: Exercises OpenAI completions provider stream parser.
- edge_cases_or_failure_modes: Prevents tool-call presence from masking provider error termination.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-614 `file` `packages/ai/test/provider-registry.test.ts`
- cursor: `[_]`
- core_role: Tests AI provider registry auth/login/refresh surface.
- algorithmic_behavior: Validates env-key map merging, multi-var env fallback order, login provider list filtering, paste-code login derivation, refresh dispatch, and runtime extension provider login handling (`packages/ai/test/provider-registry.test.ts:32-80`).
- inputs_outputs_state: Inputs are provider descriptors, legacy env names, runtime registered providers, and auth modes. Outputs are env-key map, login list, paste-code set, refreshed credentials, or unchanged API-key providers.
- gates_or_invariants: Env-only model providers are excluded from login; API-key providers bypass refreshers.
- dependencies_and_callers: Exercises provider registry used by auth CLI, setup, and model provider auth flows.
- edge_cases_or_failure_modes: Runtime extension providers must be dispatchable without catalog registration.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-644 `file` `packages/ai/test/transform-messages-dedup.test.ts`
- cursor: `[_]`
- core_role: Tests deduplication of OpenAI Responses composite tool call IDs.
- algorithmic_behavior: Builds assistant/tool-result messages, transforms them, and asserts duplicate composite IDs are made distinct while corresponding result IDs track the transformed call IDs (`packages/ai/test/transform-messages-dedup.test.ts:13-83`).
- inputs_outputs_state: Inputs are assistant tool calls and tool result messages with duplicate IDs. Outputs are transformed call/result IDs.
- gates_or_invariants: Only the `call_id` segment is suffixed so wire IDs stay parseable and result linkage is preserved.
- dependencies_and_callers: Exercises `transformMessages` and `normalizeResponsesToolCallId`.
- edge_cases_or_failure_modes: Duplicate composite IDs could otherwise collapse tool results or corrupt Responses replay.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-674 `file` `packages/catalog/test/descriptors.test.ts`
- cursor: `[_]`
- core_role: Tests provider descriptor registry/default model map.
- algorithmic_behavior: Asserts standard descriptors exist, special-managed providers are excluded, default model values are correct, and descriptor factories preserve provider identity (`packages/catalog/test/descriptors.test.ts:4-27`).
- inputs_outputs_state: Inputs are `PROVIDER_DESCRIPTORS` and `DEFAULT_MODEL_PER_PROVIDER`. Outputs are provider manager option objects and assertions.
- gates_or_invariants: `openai-codex` is not a regular descriptor but has default model; `kagi` is not in default model map.
- dependencies_and_callers: Exercises catalog provider descriptor tables used by model registry/discovery.
- edge_cases_or_failure_modes: Prevents provider identity drift in factory output.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-704 `file` `packages/catalog/test/ollama-provider.test.ts`
- cursor: `[_]`
- core_role: Tests Ollama provider discovery and reasoning/tool-forcing behavior.
- algorithmic_behavior: Validates `/api/show` context and thinking capability extraction, unsupported reasoning level remapping, forced tool selection narrowing, and reasoning effort backfill in `buildModel` (`packages/catalog/test/ollama-provider.test.ts:14-198`).
- inputs_outputs_state: Inputs are mocked Ollama model metadata, tool choices, and stale model specs. Outputs are built model capabilities and transformed tool options.
- gates_or_invariants: Explicit overrides win; non-Ollama providers remain untouched; missing Ollama defaults are backfilled.
- dependencies_and_callers: Exercises catalog Ollama resolver/provider model policy and OpenAI-compatible local model behavior.
- edge_cases_or_failure_modes: Handles non-reasoning models, stale specs lacking compat info, and `whenThinking` variants.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-734 `file` `packages/coding-agent/src/telemetry-export.ts`
- cursor: `[_]`
- core_role: OpenTelemetry trace export initialization/flush bridge for coding-agent.
- algorithmic_behavior: Checks env enablement, lazily imports/registers Node tracer provider/exporter, schedules batch exporting, hooks postmortem cleanup, and exposes flush. Key functions: `isTelemetryExportEnabled` at `packages/coding-agent/src/telemetry-export.ts:43`, `initTelemetryExport` at `53`, `registerProvider` at `83`, and `flushTelemetryExport` at `142`.
- inputs_outputs_state: Inputs are OTEL env vars and runtime shutdown signals. Outputs are registered tracer provider/exporter and flushed trace data. State includes module-level `provider` and `initPromise`.
- gates_or_invariants: Disabled when OTEL traces exporter contains `none`; init is single-flight; cleanup is centralized through postmortem rather than raw process handlers (`packages/coding-agent/src/telemetry-export.ts:119-134`).
- dependencies_and_callers: Depends on `@opentelemetry/sdk-trace-node`, pi-utils logger/postmortem, and CLI startup telemetry path.
- edge_cases_or_failure_modes: Dynamic dependency load can fail; double init should coalesce; flushing before init should be harmless.
- validation_or_tests: Covered by `packages/coding-agent/test/telemetry-export.test.ts` and `otel-export-probe.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-764 `file` `packages/coding-agent/test/agent-session-empty-stop-guard.test.ts`
- cursor: `[_]`
- core_role: Regression tests for auto-retrying empty assistant stop turns.
- algorithmic_behavior: Tests retry after tool result, tool-use stop without tool/text, thinking-only stops, orphaned tool-use removal, retry cap, auto-retry state cleanup, budget preservation, and normal stop bypass (`packages/coding-agent/test/agent-session-empty-stop-guard.test.ts:164-380`).
- inputs_outputs_state: Inputs are mocked assistant stop messages and session event streams. Outputs are retry decisions, transcript cleanup, and budget state.
- gates_or_invariants: Empty stop retry cap is three; valid tool-use/text stops do not retry.
- dependencies_and_callers: Exercises `AgentSession` stop classifier/retry behavior.
- edge_cases_or_failure_modes: Prevents infinite retry loops and orphaned tool-use stops on cap hit.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-794 `file` `packages/coding-agent/test/async-job-manager.test.ts`
- cursor: `[_]`
- core_role: Tests async background job state machine and delivery behavior.
- algorithmic_behavior: Validates progress forwarding, error delivery, cancellation, max running cap, queued jobs, retention eviction, delivery acknowledgement, dispose, scoped drain, owner-specific cancellation, and smart poll-wait escalation (`packages/coding-agent/test/async-job-manager.test.ts:4-459`).
- inputs_outputs_state: Inputs are job runners, progress callbacks, owner IDs, timers, and cancellation requests. Outputs are job status, result text, progress updates, pending deliveries, and wait durations.
- gates_or_invariants: Queued jobs do not count toward running cap until marked running; callback errors are swallowed; owner-scoped drains isolate matching jobs.
- dependencies_and_callers: Exercises `AsyncJobManager` used by task/background agent workflows.
- edge_cases_or_failure_modes: Retention timers, completed jobs during cancelAll, in-flight delivery timeout, and per-owner poll escalation.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-824 `file` `packages/coding-agent/test/client-resources.test.ts`
- cursor: `[_]`
- core_role: Tests MCP client resource/list/template/read/subscription behavior.
- algorithmic_behavior: Validates unsupported-resource empty results, resource/template caching, pagination, binary blobs, capability predicates, and subscription/unsubscription error tolerance (`packages/coding-agent/test/client-resources.test.ts:21-176`).
- inputs_outputs_state: Inputs are mocked MCP connection capabilities and responses. Outputs are resource arrays, templates, read contents, and subscription calls.
- gates_or_invariants: Cache is reused on second call; failed individual subscription operations do not throw globally.
- dependencies_and_callers: Exercises MCP client resource helpers and mock transport utilities.
- edge_cases_or_failure_modes: Handles binary content and absent subscribe capability.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-854 `file` `packages/coding-agent/test/extension-flag-dispatch.test.ts`
- cursor: `[_]`
- core_role: Tests CLI extension flag scanning around end-of-options marker.
- algorithmic_behavior: Ensures raw argv scanning stops at `--`, including after a string extension flag (`packages/coding-agent/test/extension-flag-dispatch.test.ts:23-40`).
- inputs_outputs_state: Inputs are argv arrays with extension flag definitions. Outputs are parsed messages and extension flag sink state.
- gates_or_invariants: `--` remains end-of-options and later `--foo` tokens become positional messages, not flags.
- dependencies_and_callers: Exercises CLI args/extension flag dispatch.
- edge_cases_or_failure_modes: Prevents extension flags from consuming user prompt text after `--`.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-884 `file` `packages/coding-agent/test/initial-message.test.ts`
- cursor: `[_]`
- core_role: Tests initial message assembly from stdin, files, and CLI text.
- algorithmic_behavior: Verifies `buildInitialMessage` combines stdin/file text/first CLI message and leaves plain CLI messages untouched when no extra input exists (`packages/coding-agent/test/initial-message.test.ts:15-32`).
- inputs_outputs_state: Inputs are stdin text, initial file contents, and CLI message array. Outputs are assembled initial prompt text.
- gates_or_invariants: Additional sources are only prepended/combined when present; plain message path stays exact.
- dependencies_and_callers: Exercises CLI startup prompt construction.
- edge_cases_or_failure_modes: Prevents double wrapping or unexpected prompt mutation.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-914 `file` `packages/coding-agent/test/issue-1940-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for tiny local model worker failure recovery.
- algorithmic_behavior: Tests custom system prompt forwarding, worker recycling after local model error, recovered subsequent completion, and queued completion faulting on failed worker recycle (`packages/coding-agent/test/issue-1940-repro.test.ts:36-107`).
- inputs_outputs_state: Inputs are fake tiny worker outbound messages and local title/completion requests. Outputs are title/completion results or errors, plus worker lifecycle state.
- gates_or_invariants: A failed model execution must release/recycle the worker process and not leave queued requests hanging.
- dependencies_and_callers: Exercises `TinyTitleClient` and tiny worker protocol.
- edge_cases_or_failure_modes: Unknown local model failure and queued request drain.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-944 `file` `packages/coding-agent/test/js-eval-worker-host-reentry.test.ts`
- cursor: `[_]`
- core_role: Smoke test for JS eval worker host re-entry through hidden CLI argv.
- algorithmic_behavior: Boots eval worker through source CLI hidden arg path and expects ready response (`packages/coding-agent/test/js-eval-worker-host-reentry.test.ts:7-38`).
- inputs_outputs_state: Inputs are worker host script path and hidden argv selector. Output is `{ kind: "ready" }` or failure/timeout.
- gates_or_invariants: Worker entry must re-enter CLI rather than relying on a separate bundled entrypoint.
- dependencies_and_callers: Exercises `workerHostEntry` contract and JS eval worker protocol.
- edge_cases_or_failure_modes: Catches compiled/source worker startup drift.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-974 `file` `packages/coding-agent/test/mcp-tool-ordering.test.ts`
- cursor: `[_]`
- core_role: Tests stable MCP tool ordering.
- algorithmic_behavior: Asserts lexicographic sort, insertion-order independence, in-place mutation/reference preservation, idempotent repeated sorts, and empty/single-element handling (`packages/coding-agent/test/mcp-tool-ordering.test.ts:11-65`).
- inputs_outputs_state: Inputs are arrays of MCP tool-like objects. Outputs are sorted arrays.
- gates_or_invariants: Sort returns same reference and produces total deterministic order.
- dependencies_and_callers: Exercises `sortMCPToolsByName` in MCP manager.
- edge_cases_or_failure_modes: Empty and singleton arrays remain valid.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1004 `file` `packages/coding-agent/test/profile-alias.test.ts`
- cursor: `[_]`
- core_role: Tests shell profile alias/function installer.
- algorithmic_behavior: Validates bash/zsh/fish/PowerShell function rendering, source invocation targeting, config path selection, previous block replacement, malformed managed block refusal, shadow/reserved-word rejection, shell detection, missing config handling, and profile name validation (`packages/coding-agent/test/profile-alias.test.ts:8-330`).
- inputs_outputs_state: Inputs are shell env vars, profile names, config files, and invocation paths. Outputs are updated shell config blocks or errors.
- gates_or_invariants: Refuses to shadow base `omp`, refuses malformed managed blocks, and validates reserved words before writing shell code.
- dependencies_and_callers: Exercises setup/profile alias installer.
- edge_cases_or_failure_modes: Windows PowerShell vs pwsh detection, XDG/ZDOTDIR paths, malformed block without end marker.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1034 `file` `packages/coding-agent/test/sdk-extensions-per-session-binding.test.ts`
- cursor: `[_]`
- core_role: Tests SDK extension instances are bound per session.
- algorithmic_behavior: Loads same extension twice with distinct event buses/runtime contexts and asserts distinct `Extension`/API instances and binding records (`packages/coding-agent/test/sdk-extensions-per-session-binding.test.ts:21-83`).
- inputs_outputs_state: Inputs are temporary extension package and two session runtimes. Outputs are extension arrays, runtime objects, and binding captures.
- gates_or_invariants: Extension/API/runtime must not be reused across parent and subagent sessions.
- dependencies_and_callers: Exercises `loadExtensions` and extension runtime initialization.
- edge_cases_or_failure_modes: Prevents session event bus leakage across subagents.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1064 `file` `packages/coding-agent/test/silent-abort-print-mode.test.ts`
- cursor: `[_]`
- core_role: Regression tests for print-mode abort/error output.
- algorithmic_behavior: Ensures silent abort marker is not written to stderr or nonzero exit, real errors do write stderr and exit nonzero, and thinking blocks print only when enabled (`packages/coding-agent/test/silent-abort-print-mode.test.ts:49-110`).
- inputs_outputs_state: Inputs are mocked print-mode runs and abort/error conditions. Outputs are stderr, exit calls, and printed thinking content.
- gates_or_invariants: Silent abort is treated as clean user-facing stop; real errors preserve failure exit.
- dependencies_and_callers: Exercises print-mode CLI/session run path.
- edge_cases_or_failure_modes: Prevents internal silent-abort sentinel leakage.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1094 `file` `packages/coding-agent/test/system-prompt-model.test.ts`
- cursor: `[_]`
- core_role: Tests optional model identifier in system prompt and prompt refresh on model changes.
- algorithmic_behavior: Validates model line rendering/omission and prompt rebuild only when `includeModelInPrompt` is enabled (`packages/coding-agent/test/system-prompt-model.test.ts:23-135`).
- inputs_outputs_state: Inputs are model metadata, settings, and model change events. Outputs are system prompt text and rebuild calls.
- gates_or_invariants: Model change should not rebuild prompt when setting is disabled.
- dependencies_and_callers: Exercises AgentSession system prompt construction and settings hooks.
- edge_cases_or_failure_modes: Prevents stale or undesired model identity in prompt.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1124 `file` `packages/coding-agent/test/workspace-tree.test.ts`
- cursor: `[_]`
- core_role: Tests workspace tree summarization used in prompt/context.
- algorithmic_behavior: Verifies mtime sorting, truncation marker/newest/oldest retention, depth cap, hidden/excluded/gitignored skipping, hard line cap, root uncapped option, AGENTS.md discovery depth, gitignored AGENTS.md exceptions, stable absolute mtime rendering, and relative ages for tool output (`packages/coding-agent/test/workspace-tree.test.ts:31-215`).
- inputs_outputs_state: Inputs are temporary directory trees, mtimes, ignore patterns, and render options. Outputs are rendered tree strings and discovered AGENTS.md files.
- gates_or_invariants: Prompt-cache tree uses stable absolute mtimes; hidden/excluded/gitignored paths are filtered except AGENTS.md surfacing rules.
- dependencies_and_callers: Exercises workspace tree builder used by system context.
- edge_cases_or_failure_modes: Hard line cap and depth cap prevent prompt blowups; ignored directory boundaries are respected.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1154 `file` `packages/hashline/src/patcher.ts`
- cursor: `[_]`
- core_role: Hashline patch application engine for safe file edits with hash/snapshot/recovery checks.
- algorithmic_behavior: Prepares sections, validates file hashes, detects duplicate canonical paths, resolves block edits, applies edits, merges warnings, attempts recovery, writes updated content, and returns per-section results. Key structures/functions include `PreparedSection` at `packages/hashline/src/patcher.ts:92`, `assertSectionHashPresent` at `121`, `assertUniqueCanonicalPaths` at `142`, `Patcher` at `161`, and `commit` at `289`.
- inputs_outputs_state: Inputs are parsed patch sections, filesystem abstraction, snapshot store, current file content, and options. Outputs are `PatcherApplyResult`, `PatchSectionResult`, file writes, warnings, or mismatch errors. State includes prepared section canonical path, normalized content, line endings, and recovery result.
- gates_or_invariants: Requires hash for anchor-scoped edits, blocks duplicate canonical paths in one patch, preserves BOM/line endings, and refuses unsafe block/local edit ambiguity.
- dependencies_and_callers: Depends on hashline apply/block/format/fs/input/messages/mismatch/normalize/recovery/snapshots modules and used by coding-agent edit/write tools.
- edge_cases_or_failure_modes: Handles missing files, stale snapshots, head/tail drift warnings, block edit resolution, line ending restoration, and hash mismatch recovery.
- validation_or_tests: Covered by coding-agent core/hashline/apply-patch/write tests and hashline package tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1184 `file` `packages/mnemopi/test/beam-index.test.ts`
- cursor: `[_]`
- core_role: Tests BeamMemory public hub wiring.
- algorithmic_behavior: Verifies index methods delegate to beam module implementations (`packages/mnemopi/test/beam-index.test.ts:4-5`).
- inputs_outputs_state: Inputs are imported BeamMemory hub calls. Outputs are delegated method results or spy assertions.
- gates_or_invariants: Public index API must remain wired to implementation modules.
- dependencies_and_callers: Exercises `@oh-my-pi/pi-mnemopi` beam index exports.
- edge_cases_or_failure_modes: Catches barrel/API drift rather than algorithm internals.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1214 `file` `packages/mnemopi/test/local-llm.test.ts`
- cursor: `[_]`
- core_role: Tests local/remote LLM adapter selection for mnemopi.
- algorithmic_behavior: Validates remote availability/OpenAI-compatible HTTP, local GGUF unavailable fallback, host backend priority, host prompt rendering, chunk budget expansion, constructor-scoped completion function/model, and `llm:false` override (`packages/mnemopi/test/local-llm.test.ts:42-145`).
- inputs_outputs_state: Inputs are env/config, host backend, remote URL, completion function, and pi-ai Model instance. Outputs are completion responses, availability flags, and budget values.
- gates_or_invariants: Host backend can short-circuit remote; explicit false disables remote defaults.
- dependencies_and_callers: Exercises mnemopi local LLM TypeScript port.
- edge_cases_or_failure_modes: Ensures constructor scope beats global remote settings.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1244 `file` `packages/mnemopi/test/veracity-consolidation.test.ts`
- cursor: `[_]`
- core_role: Tests veracity consolidator database ownership.
- algorithmic_behavior: Ensures `VeracityConsolidator` does not close a caller-owned Bun SQLite `Database` handle (`packages/mnemopi/test/veracity-consolidation.test.ts:5-15`).
- inputs_outputs_state: Inputs are caller-created DB and consolidator lifecycle. Output is continued DB usability.
- gates_or_invariants: Ownership boundary: injected DB remains caller-owned.
- dependencies_and_callers: Exercises mnemopi veracity consolidation.
- edge_cases_or_failure_modes: Prevents accidental close/dispose of shared DB.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1274 `file` `packages/snapcompact/research/exp02_surprisal.py`
- cursor: `[_]`
- core_role: Research experiment for surprisal/visual text compression conditions.
- algorithmic_behavior: Transforms text by disemvoweling/filtering, renders surprisal-shaded images, plans chunks, caches model calls, runs chunk QA, aggregates cost/quality metrics, and drives parallel tasks from CLI (`packages/snapcompact/research/exp02_surprisal.py:83-392`).
- inputs_outputs_state: Inputs are SQuAD-like context/questions, model names, lengths, conditions, API keys/cache, and rendering parameters. Outputs are PNGs, per-record JSON/cache entries, CSV/aggregate metrics, and summary stats.
- gates_or_invariants: Numeric/digit-adjacent tokens are preserved in transform; chunks are planned by flow/condition/size; cached calls are keyed by payload unless fresh.
- dependencies_and_callers: Depends on `squad`, PIL/image rendering helpers, concurrent futures, and provider API helpers.
- edge_cases_or_failure_modes: API failures, malformed model answers, cache invalidation, missing keys, and large rendering workloads.
- validation_or_tests: Research script; no formal tests observed.
- skip_candidate: `yes: research experiment script, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1304 `file` `packages/snapcompact/research/snapcompact_3d_activation_viz.py`
- cursor: `[_]`
- core_role: Research visualization script for 3D activation/surprisal-style panels.
- algorithmic_behavior: Normalizes/downsamples arrays, draws 3D matplotlib surfaces, crops source images, fits panels into a composite canvas, and emits visual artifact. Key functions include `norm_quantile`, `downsample`, `style_3d`, `draw_surface`, `crop_with_box`, and `render_matplotlib_panel` (`packages/snapcompact/research/snapcompact_3d_activation_viz.py:35-150`).
- inputs_outputs_state: Inputs are numpy arrays/images and layout parameters. Outputs are PIL/matplotlib-rendered visualization images.
- gates_or_invariants: Quantile normalization controls outliers; downsampling preserves column budget; crop/paste fits into fixed boxes.
- dependencies_and_callers: Uses numpy, matplotlib, PIL.
- edge_cases_or_failure_modes: Empty arrays, extreme outliers, missing fonts/images, and fixed layout overflow.
- validation_or_tests: Research script; no formal tests observed.
- skip_candidate: `yes: visualization research artifact, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1334 `file` `packages/snapcompact/research/snapcompact_viz_glass_stack.py`
- cursor: `[_]`
- core_role: Research visualization script for glass-stack Snapcompact graphics.
- algorithmic_behavior: Builds layered visual panels from rendered/cropped images and metrics, likely for explanatory diagrams rather than runtime execution.
- inputs_outputs_state: Inputs are image artifacts, layout constants, colors, and labels. Outputs are generated visual image files.
- gates_or_invariants: Fixed canvas/layout geometry and image-fit constraints.
- dependencies_and_callers: Depends on Python imaging/matplotlib-style stack used by Snapcompact research scripts.
- edge_cases_or_failure_modes: Missing source image/assets or text overflow in fixed layout.
- validation_or_tests: Research script; no formal tests observed.
- skip_candidate: `yes: visualization research artifact, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1364 `file` `packages/tui/bench/kitty-sequence.ts`
- cursor: `[_]`
- core_role: Microbenchmark comparing native and JS Kitty keyboard sequence matching.
- algorithmic_behavior: Defines sample sequences, JS matcher, benchmark loop, and compares `matchesKittySequence` from natives against parser behavior (`packages/tui/bench/kitty-sequence.ts:1-27`).
- inputs_outputs_state: Inputs are fixed terminal escape sequences and iteration count. Outputs are benchmark timings.
- gates_or_invariants: Expected codepoint/modifier matching must align between native and JS behavior.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-natives` and TUI key parser.
- edge_cases_or_failure_modes: Escape sequence variants with lock masks and modifier bits.
- validation_or_tests: Benchmark only; related behavior covered by TUI key tests.
- skip_candidate: `yes: benchmark, not production algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1394 `file` `packages/tui/test/container-memo.test.ts`
- cursor: `[_]`
- core_role: Tests render memoization for TUI container/box components.
- algorithmic_behavior: Validates stable render array reference on memo hits, invalidation on child changes/add/remove/clear/invalidate/width change, continued child render calls, and bg function output changes (`packages/tui/test/container-memo.test.ts:32-165`).
- inputs_outputs_state: Inputs are component trees, widths, child mutations, and background function outputs. Outputs are rendered row arrays and reference identity assertions.
- gates_or_invariants: Memo cache must be invalidated on structural/content/width/background changes while preserving render calls.
- dependencies_and_callers: Exercises `Container` and `Box` rendering algorithms in TUI.
- edge_cases_or_failure_modes: Ref-stable children with changed output, unchanged content after invalidate, and width-dependent cache keys.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1424 `file` `packages/tui/test/loop-watchdog.test.ts`
- cursor: `[_]`
- core_role: Tests event loop blockage watchdog logging.
- algorithmic_behavior: Validates late tick logging with phase/overshoot, silence on deadline ticks, sustained-block dedupe, stop short-circuit, recent phase attribution, re-arm after recovery, generation mismatch, timer unref, and cancellation (`packages/tui/test/loop-watchdog.test.ts:49-207`).
- inputs_outputs_state: Inputs are fake timers/phases and watchdog options. Outputs are logger warnings and timer handle interactions.
- gates_or_invariants: One warning per sustained block; stale generation ticks do not re-arm parallel chains; timers are unref’d.
- dependencies_and_callers: Exercises `LoopWatchdog` and loop phase stack in pi-utils.
- edge_cases_or_failure_modes: Finished phase attribution and start/stop/start races.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1454 `file` `packages/tui/test/streaming-scrollback-defer.test.ts`
- cursor: `[_]`
- core_role: Tests TUI native scrollback handling for live streaming regions.
- algorithmic_behavior: Ensures mutable live-region head rows remain transient, scrolled-off sealed/durable prefixes commit exactly once, no ED3 during streaming, resize erases mis-wrapped scrollback, interested children receive committed rows, and duplicate snapshots are avoided (`packages/tui/test/streaming-scrollback-defer.test.ts:125-595`).
- inputs_outputs_state: Inputs are live region render frames, viewport sizes, resize events, and durable snapshot blocks. Outputs are terminal operations/native scrollback history.
- gates_or_invariants: Streaming must not clear terminal with ED3; committed prefix accounting is stable under cap/collapse/drift.
- dependencies_and_callers: Exercises TUI renderer native scrollback integration.
- edge_cases_or_failure_modes: Tall all-live block, lower sibling live markers, mid-stream collapse, capped frame, and resize while streaming.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1484 `file` `packages/utils/src/color.ts`
- cursor: `[_]`
- core_role: Shared color conversion and luminance utilities.
- algorithmic_behavior: Implements hex/RGB/HSV/HSL conversions, hue shifts, HSV adjustments, ANSI 16/256 palette conversion, and luma/relative luminance calculations. Public functions include `hexToRgb`, `rgbToHex`, `rgbToHsv`, `hsvToRgb`, `hslToHex`, `colorLuma`, and `relativeLuminance` (`packages/utils/src/color.ts:15-298`).
- inputs_outputs_state: Inputs are hex strings, RGB/HSV/HSL values, ANSI palette indexes. Outputs are converted colors or luminance values. No persistent state.
- gates_or_invariants: Handles palette ranges, clamps/normalizes channels, and returns undefined for unparseable palette values.
- dependencies_and_callers: Used by theme/TUI/stats/export color logic.
- edge_cases_or_failure_modes: Invalid hex, ANSI indexes outside palette, hue wrap, and gamma-correct luminance.
- validation_or_tests: Indirectly covered by theme/export/stats tests; no direct color test observed in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1514 `file` `packages/utils/src/which.ts`
- cursor: `[_]`
- core_role: Cached executable lookup with macOS Xcode shim avoidance.
- algorithmic_behavior: Defines Xcode bin deny/prefix lists, resolves developer dirs, builds macOS tool path map, exposes `whichFresh` and `$which` with cache policies (`packages/utils/src/which.ts:21-215`).
- inputs_outputs_state: Inputs are command names, Bun `WhichOptions`, platform, PATH, and cache policy. Outputs are executable paths or null. State is `toolCache`, `macosToolPaths`, and command option cache keys.
- gates_or_invariants: On Darwin, avoids misleading Xcode shims for common tools and preserves cache invalidation behavior.
- dependencies_and_callers: Depends on Bun.which, `node:fs/os/path`; used by CLI update/setup, auth broker, tool availability checks, and provider discovery.
- edge_cases_or_failure_modes: Xcode path detection failure, PATH changes with stale cache, and command names matching Xcode prefixes.
- validation_or_tests: Indirectly covered by setup/update/tool availability tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1544 `file` `python/omp-rpc/tests/test_protocol.py`
- cursor: `[_]`
- core_role: Tests Python RPC protocol frame parsing and validation.
- algorithmic_behavior: Validates session state parsing, agent end notification, extension UI request, todo reminder, assistant text filtering, invalid thinking/effort/system prompt shapes, invalid UI method, invalid assistant done reason, and deep clone of nested messages (`python/omp-rpc/tests/test_protocol.py:17-330`).
- inputs_outputs_state: Inputs are raw JSON-like protocol frames. Outputs are typed Python protocol objects or validation errors.
- gates_or_invariants: Thinking level/model effort enums and system prompt shapes are strict; assistant text excludes thinking by default.
- dependencies_and_callers: Exercises Python `omp_rpc` protocol classes/parsers.
- edge_cases_or_failure_modes: Deep cloning avoids retained event mutation.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1574 `file` `python/robomp/tests/conftest.py`
- cursor: `[_]`
- core_role: Shared pytest fixtures for robomp backend/dashboard tests.
- algorithmic_behavior: Ensures dashboard bundle exists, opens temp path for slot traversal, builds baseline env/proxy env, constructs `Settings`, and creates DB fixture (`python/robomp/tests/conftest.py:29-150`).
- inputs_outputs_state: Inputs are tmp paths, monkeypatch env, pytest fixtures. Outputs are env dicts, settings objects, and database handles.
- gates_or_invariants: Test env is isolated to temp dirs and baseline variables are consistently set.
- dependencies_and_callers: Used by Python `robomp` test suite.
- edge_cases_or_failure_modes: Missing dashboard bundle and temp path traversal setup.
- validation_or_tests: Fixture support file; validated by dependent robomp tests.
- skip_candidate: `yes: test fixture support, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1604 `directory` `packages/coding-agent/src/autoresearch/tools`
- cursor: `[_]`
- core_role: Autoresearch tool suite for experiment lifecycle: initialize, run, log, and update notes.
- algorithmic_behavior: Recursively contains `init-experiment.ts`, `run-experiment.ts`, `log-experiment.ts`, and `update-notes.ts`. Tools create experiment state/harness, execute harness commands with tail/progress capture, record metrics and keep/discard/crash outcomes, commit/revert scoped changes, detect scope deviations, and replace/append research notes.
- inputs_outputs_state: Inputs are tool args (`name`, metrics, status, timeout, notes body), cwd git state, storage DB, harness command, and modified paths. Outputs are tool result text/details, experiment rows, commits/reverts, notes updates, and progress details.
- gates_or_invariants: `log_experiment` requires justification for scope-deviating kept runs, reverts failed/discarded experiments, truncates ASI values, and keeps tool names consistent (`packages/coding-agent/src/autoresearch/tools/log-experiment.ts:37-506`).
- dependencies_and_callers: Depends on autoresearch storage/state/git helpers, bash executor, render utils, pi-tui, and task/session tool framework.
- edge_cases_or_failure_modes: Dirty workdir detection, missing storage/session, harness timeout, tail truncation, commit failures, and notes section insertion around `## Ideas`.
- validation_or_tests: Covered by autoresearch tests such as `packages/coding-agent/test/autoresearch-tools.test.ts` and state tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1634 `directory` `packages/coding-agent/src/modes/rpc`
- cursor: `[_]`
- core_role: Headless/RPC mode protocol, client, host tool/URI bridges, and subagent event registry.
- algorithmic_behavior: Recursively contains host tool adapter/bridge, host URI protocol handler/bridge, RPC client, RPC server mode loop, subagent registry/transcript reader, and frame types. It validates/normalizes frames, dispatches commands, streams agent/session events, registers host tools/URI schemes, handles UI requests, session changes, skill commands, and subagent subscriptions.
- inputs_outputs_state: Inputs are JSONL RPC commands, prompts, host tool/URI definitions, session events, extension UI requests, and subagent lifecycle/progress events. Outputs are RPC responses/frames, tool call/cancel requests, URI read/write requests, prompt results, and state updates.
- gates_or_invariants: Host URI schemes must match URI scheme regex; client frame guards validate response/event types; subagent transcript references are pruned; local-only prompt results are watched/reported.
- dependencies_and_callers: Depends on `AgentSession`, extension runner, slash commands, event bus, `@oh-my-pi/pi-agent-core`, `@oh-my-pi/pi-ai`, and Python `omp-rpc` client.
- edge_cases_or_failure_modes: Unknown/invalid frames, host handler errors, cancellation, read-only URI write rejection, local-only prompt commands, session branch/switch resets, and subagent event retention limits.
- validation_or_tests: Covered by `packages/coding-agent/test/rpc*.test.ts`, `rpc-host-tools.test.ts`, `rpc-host-uris.test.ts`, `rpc-subagents.test.ts`, and Python `python/omp-rpc/tests`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1664 `directory` `python/robomp/web/src/components`
- cursor: `[_]`
- core_role: SolidJS dashboard components for robomp status, issues, browsing, logs, triggers, and running work.
- algorithmic_behavior: Recursively contains `Browse`, `Events`, `GlassCard`, `Header`, `IssueLink`, `Issues`, `Logs`, `Pill`, `Stats`, `Trigger`, and `Working`. Components fetch/render API data, format issue keys/ages/durations, trigger/cancel deliveries, and display status cards/tables.
- inputs_outputs_state: Inputs are API responses, status resources, config, user trigger/cancel actions, and component props. Outputs are SolidJS JSX UI, links, pills, stats, and action side effects.
- gates_or_invariants: `Working` merges running events with inflight cancel IDs, `IssueLink`/`PrLink` generate URLs, `Browse` handles empty/error states, and trigger/cancel calls update shared state.
- dependencies_and_callers: Depends on robomp web API/state/types/format modules and SolidJS.
- edge_cases_or_failure_modes: API errors, empty lists, null timestamps, inflight cancel state, and invalid/missing issue keys.
- validation_or_tests: Web component behavior is indirectly covered by robomp web/build tests; `IssueLink.tsx` is also assigned separately.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1694 `file` `packages/ai/src/auth-broker/wire-schemas.ts`
- cursor: `[_]`
- core_role: ArkType wire schema definitions for auth broker HTTP/SSE API.
- algorithmic_behavior: Defines credential schemas, snapshot entries/responses, stream events, health, usage report shapes, refresh/disable/upload request/response schemas (`packages/ai/src/auth-broker/wire-schemas.ts:21-238`).
- inputs_outputs_state: Inputs are unknown JSON payloads crossing auth broker boundary. Outputs are validated typed payloads or ArkType errors. No mutable state except imported sentinel semantics.
- gates_or_invariants: Writable credentials distinguish OAuth/API key; remote snapshot OAuth uses `REMOTE_REFRESH_SENTINEL`; usage units/status/windows are constrained enums/objects.
- dependencies_and_callers: Depends on `arktype` and auth storage sentinel; used by auth broker server/client and coding-agent auth CLI.
- edge_cases_or_failure_modes: Rejects malformed credential uploads, invalid usage shapes, and unknown stream event variants.
- validation_or_tests: Covered by auth broker/client/import/snapshot tests and gateway tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1724 `file` `packages/ai/src/providers/anthropic-messages-server-schema.ts`
- cursor: `[_]`
- core_role: Server-side schema for Anthropic Messages-compatible request validation.
- algorithmic_behavior: ArkType schemas for cache control, image sources, text/image/thinking/tool blocks, system blocks, user/assistant messages, tools, tool choice, thinking config, task budgets, and full request (`packages/ai/src/providers/anthropic-messages-server-schema.ts:23-247`).
- inputs_outputs_state: Inputs are unknown Anthropic Messages request bodies. Outputs are typed `MessageCreateParams`-compatible values or validation errors.
- gates_or_invariants: Known block types are structured; `unknownContentBlockSchema` allows forward-compatible unknown block types while preserving known-type validation.
- dependencies_and_callers: Depends on Anthropic SDK types and `arktype`; used by Anthropic-compatible server/proxy validation.
- edge_cases_or_failure_modes: Tool result content unions, image source variants, unknown block pass-through, thinking/output config bounds.
- validation_or_tests: Covered by Anthropic alignment/provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1754 `file` `packages/ai/src/providers/openai-responses-server.ts`
- cursor: `[_]`
- core_role: OpenAI Responses-compatible server adapter for parsing incoming requests and encoding responses/streams.
- algorithmic_behavior: Parses request body/headers into internal `ParsedRequest`, maps tool choice/tools/messages/content, creates IDs, builds response envelopes/output items/usage, formats errors, and encodes SSE events for message/reasoning/function/custom tool streams. Key functions: `parseRequest` at `packages/ai/src/providers/openai-responses-server.ts:260`, `encodeResponse` at `680`, and `encodeStream` at `725`.
- inputs_outputs_state: Inputs are OpenAI Responses HTTP body, headers, internal assistant messages/events, requested model ID, and stream control. Outputs are parsed internal request, JSON response envelope, or SSE event text. State includes per-stream open message/reasoning/function call tracking and warning booleans for unsupported image/file/reasoning summary features.
- gates_or_invariants: Reasoning effort/service tier/tool choice values are validated; unsupported image/file features warn once; stop reason maps to response status; function/custom call IDs are normalized for wire output.
- dependencies_and_callers: Depends on auth gateway request types, schema tools, logger, ArkType, and AI message types.
- edge_cases_or_failure_modes: Handles missing assistant placeholder, flattened function output arrays, reasoning summary deltas, custom tool input deltas, incomplete/failed statuses, and unsupported input blocks.
- validation_or_tests: Covered by OpenAI Responses replay/vision/error tests and provider server tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1784 `file` `packages/ai/src/registry/groq.ts`
- cursor: `[_]`
- core_role: Groq provider registry descriptor.
- algorithmic_behavior: Small registry file declaring Groq provider metadata/env key mapping for the AI provider registry.
- inputs_outputs_state: Inputs are provider registry load and env key lookup. Outputs are provider definition entries.
- gates_or_invariants: Provider ID/env key must match catalog/provider registry expectations.
- dependencies_and_callers: Used by provider registry/auth surface and model registry.
- edge_cases_or_failure_modes: Misconfigured env key would break Groq auth discovery.
- validation_or_tests: Indirectly covered by `packages/ai/test/provider-registry.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1814 `file` `packages/ai/src/registry/together.ts`
- cursor: `[_]`
- core_role: Together provider registry descriptor.
- algorithmic_behavior: Declares Together provider auth/env metadata used by registry login/env-key surfaces.
- inputs_outputs_state: Inputs are provider registry initialization and env lookup. Outputs are provider definition metadata.
- gates_or_invariants: Provider ID and env names must align with catalog descriptors.
- dependencies_and_callers: Used by AI provider registry, coding-agent model/auth flows.
- edge_cases_or_failure_modes: Missing/incorrect env metadata prevents automatic credential pickup.
- validation_or_tests: Indirectly covered by provider registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1844 `file` `packages/ai/src/utils/event-stream.ts`
- cursor: `[_]`
- core_role: Async event stream primitive and assistant-message event collector.
- algorithmic_behavior: `EventStream` implements async iterable push/end/error collection; `AssistantMessageEventStream` specializes it to collect assistant events into an assistant message (`packages/ai/src/utils/event-stream.ts:4-118`).
- inputs_outputs_state: Inputs are pushed events, errors, end result, and async iterator consumption. Outputs are yielded events or final result. State includes internal queue, waiters, ended/error flags, and result.
- gates_or_invariants: Iterator resolves pending waits in order; errors propagate; final assistant collector preserves message event semantics.
- dependencies_and_callers: Used by provider streaming implementations.
- edge_cases_or_failure_modes: Consumer waiting before events, events before consumer, error before/after end, and multiple waiters.
- validation_or_tests: Indirectly covered by provider streaming tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1874 `file` `packages/catalog/src/discovery/index.ts`
- cursor: `[_]`
- core_role: Barrel export for catalog discovery modules.
- algorithmic_behavior: Re-exports discovery APIs from sibling modules; no local algorithm beyond module surface composition.
- inputs_outputs_state: Inputs are TypeScript import requests. Outputs are exported discovery symbols. No runtime state.
- gates_or_invariants: Maintains public import path compatibility.
- dependencies_and_callers: Used by callers importing `@oh-my-pi/pi-catalog/discovery`.
- edge_cases_or_failure_modes: Bad barrel export can break consumers at compile/runtime import resolution.
- validation_or_tests: Indirectly covered by catalog tests and package type checks.
- skip_candidate: `yes: barrel surface only, no independent algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1904 `file` `packages/coding-agent/src/auto-thinking/classifier.ts`
- cursor: `[_]`
- core_role: Classifies prompt difficulty to select reasoning effort automatically.
- algorithmic_behavior: Prepares/clips classifier input, runs online model or local tiny model, parses difficulty level/bucket text, clamps effort, and extracts assistant text. Key functions: `classifyDifficulty` at `packages/coding-agent/src/auto-thinking/classifier.ts:61`, `classifyOnline` at `71`, `classifyLocal` at `112`, `parseDifficultyLevel` at `135`, `parseDifficultyBucket` at `152`, and `prepareClassifierInput` at `186`.
- inputs_outputs_state: Inputs are user prompt text, settings, model registry, and classifier model selection. Outputs are `Effort`. State is only local call state plus tiny worker use.
- gates_or_invariants: Input clipped to 6,000 chars with head/tail split; answers constrained to tiny token budgets; local and online paths clamp to supported effort.
- dependencies_and_callers: Depends on pi-ai `completeSimple`, model resolver, settings, tiny model client, and static prompt markdown.
- edge_cases_or_failure_modes: Unparseable classifier output falls back; local model errors may need fallback; long prompts are head/tail clipped.
- validation_or_tests: Covered by `packages/coding-agent/test/auto-thinking-classifier.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1934 `file` `packages/coding-agent/src/cli/auth-broker-cli.ts`
- cursor: `[_]`
- core_role: CLI command implementation for auth broker serve/token/login/logout/status/import/migrate/list actions.
- algorithmic_behavior: Parses action flags, ensures broker token, starts broker server, performs local/remote OAuth login, imports clproxy credentials, migrates old auth storage into broker, lists/logout/status credentials, and dispatches action in `runAuthBrokerCommand`. Key functions span `runServe` at `packages/coding-agent/src/cli/auth-broker-cli.ts:121`, `runLogin` at `179`, `runImport` at `537`, `runMigrate` at `675`, and dispatcher at `856`.
- inputs_outputs_state: Inputs are CLI flags, token file, provider choice, OAuth metadata, credential files, broker snapshot, and user prompts. Outputs are console/status text, token file writes, broker uploads/disables, and migrated credentials.
- gates_or_invariants: Action must be known; provider selection is validated; import provider can be overridden; migration avoids duplicates by credential identity.
- dependencies_and_callers: Depends on pi-ai auth broker/client/storage, pi-utils paths/logger, Bun shell, readline, crypto, filesystem.
- edge_cases_or_failure_modes: Missing token, unavailable broker, duplicate credentials, clproxy expiry parsing, provider mismatch, dry-run remote login.
- validation_or_tests: Covered by auth broker CLI/import/status tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1964 `file` `packages/coding-agent/src/cli/update-cli.ts`
- cursor: `[_]`
- core_role: Self-update CLI implementation for npm/Bun, Homebrew, mise, and binary replacement installs.
- algorithmic_behavior: Parses update args, resolves install method/target, fetches latest release/npm metadata, compares versions, verifies installed version, sweeps stale backups, atomically replaces binaries, builds install/upgrade args, and runs update. Key functions: `parseUpdateArgs` at `packages/coding-agent/src/cli/update-cli.ts:85`, `resolveUpdateMethod` at `198`, `getLatestRelease` at `241`, `replaceBinaryForUpdate` at `424`, and `runUpdateCommand` at `605`.
- inputs_outputs_state: Inputs are current binary path, PATH, package managers, registry/GitHub data, platform/arch, force/check flags. Outputs are update commands, replaced binary, verification result, printed help/status. State includes backup files and downloaded binary temp state.
- gates_or_invariants: Binary replacement verifies expected version; stale backups matching version-like pattern are swept; method selection avoids lexical path confusion via realpath checks.
- dependencies_and_callers: Depends on Bun shell, `node:fs/os/path/stream`, pi-utils `$which`, theme, npm/GitHub/Homebrew/mise.
- edge_cases_or_failure_modes: Unsupported native tags, failed verification, stale backups, symlink/path containment, package manager missing, network failure.
- validation_or_tests: Covered by `packages/coding-agent/test/update-cli.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1994 `file` `packages/coding-agent/src/commands/setup.ts`
- cursor: `[_]`
- core_role: CLI command wrapper for onboarding setup components.
- algorithmic_behavior: Parses setup args, initializes theme/root command dependencies, and delegates to `runSetupCommand`; `COMPONENTS` includes `python` and `speech` (`packages/coding-agent/src/commands/setup.ts:10-31`).
- inputs_outputs_state: Inputs are CLI args and optional dependency overrides. Outputs are setup command side effects/help output.
- gates_or_invariants: Component choices are constrained to declared setup components.
- dependencies_and_callers: Depends on CLI command framework, setup CLI, root command runner, theme initialization.
- edge_cases_or_failure_modes: Invalid args render command help; delegated setup can fail per component.
- validation_or_tests: Covered by setup command and setup wizard tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2024 `file` `packages/coding-agent/src/config/models-config.ts`
- cursor: `[_]`
- core_role: Models config file validation wrapper.
- algorithmic_behavior: Defines provider validation modes/interfaces and `validateProviderConfiguration`, checking model/provider consistency before `ModelsConfigFile` loads config through `ConfigFile` with `ModelsConfigSchema` (`packages/coding-agent/src/config/models-config.ts:14-107`).
- inputs_outputs_state: Inputs are parsed models config objects and provider validation config. Outputs are validation errors/warnings or accepted config.
- gates_or_invariants: Provider config must not define invalid combinations for runtime/register contexts; schema validation gates file load.
- dependencies_and_callers: Depends on `ConfigFile`, `ModelsConfigSchema`, and model registry/provider loading.
- edge_cases_or_failure_modes: Unsupported provider auth/discovery combinations or bad model definitions surface as config errors.
- validation_or_tests: Covered by config and model registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2054 `file` `packages/coding-agent/src/discovery/cursor.ts`
- cursor: `[_]`
- core_role: Cursor IDE configuration discovery provider for MCP servers, rules, and settings.
- algorithmic_behavior: Registers provider `cursor`, parses Cursor MCP server config, loads rules, transforms `.mdc` rules, and loads settings (`packages/coding-agent/src/discovery/cursor.ts:35-149`).
- inputs_outputs_state: Inputs are Cursor config/rule files and discovery context. Outputs are `LoadResult<MCPServer>`, `Rule`, and settings capability items.
- gates_or_invariants: Provider priority is 50; JSON parse failures are isolated into warnings; `.mdc` content is transformed into rule capability items.
- dependencies_and_callers: Depends on capability registry, capability fs reader, MCP/rule/settings capabilities, discovery helpers, and `tryParseJson`.
- edge_cases_or_failure_modes: Missing/invalid Cursor config, malformed MCP server entries, and rule file parse failures.
- validation_or_tests: Covered by discovery tests for IDE/import provider behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2084 `file` `packages/coding-agent/src/eval/session-id.ts`
- cursor: `[_]`
- core_role: Deterministic default session identifier for eval/tool execution context.
- algorithmic_behavior: Exports `defaultEvalSessionId(session)` based on `ToolSession`-like `cwd` and optional `getSessionFile` (`packages/coding-agent/src/eval/session-id.ts:1-8`).
- inputs_outputs_state: Inputs are cwd and session file path. Output is a string ID. No mutable state.
- gates_or_invariants: Session file presence disambiguates persisted sessions; cwd provides fallback scope.
- dependencies_and_callers: Used by JS/Python eval tooling to key sessions.
- edge_cases_or_failure_modes: Missing session file can collapse to cwd-level ID.
- validation_or_tests: Indirectly covered by eval/core tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2114 `file` `packages/coding-agent/src/hindsight/state.ts`
- cursor: `[_]`
- core_role: Hindsight memory recall/retain session state manager.
- algorithmic_behavior: Implements `HindsightRetainQueue` with batch size/flush interval and `HindsightSessionState` that ensures banks, extracts transcript messages, recalls memory, queues retains, flushes, and logs failures (`packages/coding-agent/src/hindsight/state.ts:23-191`).
- inputs_outputs_state: Inputs are agent session transcript, hindsight config/API, memory item inputs, and bank scope. Outputs are recall outcomes, retained memory writes, and queue flushes. State includes pending retain items, timer, flush promise, and per-session recall state.
- gates_or_invariants: Retain flushes batch at 16 items or 5 seconds; failures log without corrupting session control flow.
- dependencies_and_callers: Depends on hindsight bank/client/config/transcript modules and AgentSession.
- edge_cases_or_failure_modes: API failures, missing bank, flush races, and shutdown flush ordering.
- validation_or_tests: Covered by hindsight/autolearn/memory tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2144 `file` `packages/coding-agent/src/lsp/startup-events.ts`
- cursor: `[_]`
- core_role: Shared event-channel/type definitions for LSP startup events.
- algorithmic_behavior: Exports channel name `lsp:startup` and union event type for server startup info (`packages/coding-agent/src/lsp/startup-events.ts:1-13`).
- inputs_outputs_state: Inputs are LSP startup server info objects. Outputs are typed event payloads. No mutable state.
- gates_or_invariants: Event channel string is centralized to avoid mismatched publisher/subscriber names.
- dependencies_and_callers: Used by LSP startup/status UI and event bus.
- edge_cases_or_failure_modes: Type drift can break event consumers.
- validation_or_tests: Indirectly covered by LSP tests and startup UI tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2174 `file` `packages/coding-agent/src/memory-backend/resolve.ts`
- cursor: `[_]`
- core_role: Resolves configured memory backend implementation.
- algorithmic_behavior: Reads settings and returns local or off backend (`packages/coding-agent/src/memory-backend/resolve.ts:19`).
- inputs_outputs_state: Input is `Settings`; output is `MemoryBackend`. No persistent state in resolver.
- gates_or_invariants: Unsupported/disabled setting falls back to off backend rather than throwing during normal operation.
- dependencies_and_callers: Depends on `local-backend`, `off-backend`, and memory tools/session code.
- edge_cases_or_failure_modes: Misconfigured setting should not crash memory-disabled sessions.
- validation_or_tests: Covered by memory tools/backend tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2204 `file` `packages/coding-agent/src/plan-mode/plan-protection.ts`
- cursor: `[_]`
- core_role: Read-tool protection matcher for plan-mode `PLAN.md`.
- algorithmic_behavior: Normalizes local scheme paths and detects when protected tool reads target the active plan reference path; exposes `createPlanReadMatcher` (`packages/coding-agent/src/plan-mode/plan-protection.ts:1-25`).
- inputs_outputs_state: Inputs are protected tool context and dynamic plan reference path getter. Output is boolean match decision.
- gates_or_invariants: `local://PLAN.md` alias is treated as plan target; read path extraction uses compaction tool protection helper.
- dependencies_and_callers: Used by plan-mode/compaction protection around read tools.
- edge_cases_or_failure_modes: Local scheme normalization avoids alias bypass; stale getter output could misclassify.
- validation_or_tests: Covered by plan-mode guard tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2234 `file` `packages/coding-agent/src/session/shake-types.ts`
- cursor: `[_]`
- core_role: Types and summary formatter for context shake/elision results.
- algorithmic_behavior: Defines shake modes/result counters and `formatShakeSummary` (`packages/coding-agent/src/session/shake-types.ts:9-27`).
- inputs_outputs_state: Inputs are shake result counts/byte stats. Output is human-readable summary string.
- gates_or_invariants: Summary should reflect removed images/elided text consistently.
- dependencies_and_callers: Used by session shake/strip image flows.
- edge_cases_or_failure_modes: Zero counts and mixed modes.
- validation_or_tests: Covered by `shake.test.ts` and strip-image tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2264 `file` `packages/coding-agent/src/task/commands.ts`
- cursor: `[_]`
- core_role: Workflow/task slash-command discovery and template expansion helper.
- algorithmic_behavior: Loads bundled `init.md`, discovers slash commands via capability, parses frontmatter into `WorkflowCommand`, looks up commands by name, expands `$@` in command content, and clears bundled cache (`packages/coding-agent/src/task/commands.ts:15-130`).
- inputs_outputs_state: Inputs are cwd, command capability items, command markdown/frontmatter, and user input. Outputs are command list, selected command, and expanded prompt text. State includes `bundledCommandsCache`.
- gates_or_invariants: Bundled command cache is lazy; discovered commands preserve source metadata; `$@` substitution keeps user input literal where appropriate.
- dependencies_and_callers: Depends on slash command capability/discovery, prompt rendering, and task workflow setup.
- edge_cases_or_failure_modes: Missing frontmatter fields fallback; command not found returns undefined; user input containing `$` must not be recursively expanded.
- validation_or_tests: Covered by `packages/coding-agent/test/task/commands.test.ts` and slash command internals tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2294 `file` `packages/coding-agent/src/tools/bash-interceptor.ts`
- cursor: `[_]`
- core_role: Bash command interception rule evaluator.
- algorithmic_behavior: Compiles configured regex rules and checks a normalized command against default/custom rules, returning intercept result with message/action when matched (`packages/coding-agent/src/tools/bash-interceptor.ts:8-57`).
- inputs_outputs_state: Inputs are bash command string and `BashInterceptorRule[]`. Output is `InterceptionResult` or no match. No persistent state.
- gates_or_invariants: Invalid regex rules must not crash normal command checking; first matching rule wins.
- dependencies_and_callers: Depends on `DEFAULT_BASH_INTERCEPTOR_RULES` from settings schema; used by bash tool/interactive command execution.
- edge_cases_or_failure_modes: Regex syntax errors, multiline/whitespace normalization, and overlapping rules.
- validation_or_tests: Covered by `packages/coding-agent/test/tools/bash-interceptor.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2324 `file` `packages/coding-agent/src/tools/jtd-to-json-schema.ts`
- cursor: `[_]`
- core_role: Converts JSON Type Definition fragments to JSON Schema and normalizes mixed schema nodes.
- algorithmic_behavior: Maps JTD primitives, recursively converts `elements`, `properties`, optional properties, enum, discriminator/mapping, refs/definitions, detects JTD schemas, normalizes nested JTD inside JSON Schema nodes, and returns normalized schema/error (`packages/coding-agent/src/tools/jtd-to-json-schema.ts:22-209`).
- inputs_outputs_state: Inputs are unknown schema objects. Outputs are JSON Schema-like objects or error string. No persistent state.
- gates_or_invariants: User properties named like JTD keywords must not be mistaken for structural JTD unless node shape qualifies.
- dependencies_and_callers: Depends on `jtd-utils`; used by tools/custom schema ingestion.
- edge_cases_or_failure_modes: Mixed JTD/JSON Schema, nested fragments, keyword collisions, invalid primitive names.
- validation_or_tests: Covered by `packages/coding-agent/test/tools/jtd-to-json-schema.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2354 `file` `packages/coding-agent/src/tools/tts.ts`
- cursor: `[_]`
- core_role: Text-to-speech custom tool with local Kokoro and xAI backends.
- algorithmic_behavior: Defines tool schema, resolves backend by preference/mp3/credentials, maps local WAV output path, calls xAI HTTP synthesis or local TTS client, encodes WAV, writes output, and returns details (`packages/coding-agent/src/tools/tts.ts:18-231`).
- inputs_outputs_state: Inputs are text, output path, voice/model/backend/codec settings, xAI credentials, and local TTS settings. Outputs are audio files and tool result details. State includes settings-derived preferences only.
- gates_or_invariants: xAI text max length is 15,000; mp3 requires xAI; local output path coerces to `.wav`; voice/model values are validated against known sets.
- dependencies_and_callers: Depends on pi-ai auth, settings, xAI HTTP helper, local TTS client, WAV encoder, and path utilities.
- edge_cases_or_failure_modes: Missing xAI creds, unsupported voice/model, local synthesis failure, output extension substitution.
- validation_or_tests: Covered by TTS CLI/tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2384 `file` `packages/coding-agent/src/utils/enhanced-paste.ts`
- cursor: `[_]`
- core_role: OSC 5522 enhanced paste parser/controller for terminal paste text/image data.
- algorithmic_behavior: Detects OSC 5522 packets, parses metadata, chooses best MIME, requests listing/read packets, dispatches image/text handlers, and resets state across packet sequences. Key functions/classes: `isOsc5522Packet`, `parseOsc5522Packet`, `choosePasteMime`, and `EnhancedPasteController` (`packages/coding-agent/src/utils/enhanced-paste.ts:3-164`).
- inputs_outputs_state: Inputs are terminal escape packet strings and handler callbacks. Outputs are `ImageContent` or text callbacks. State tracks listing/read request phases and selected MIME.
- gates_or_invariants: Image MIME priority is png/jpeg/webp/gif; text fallback is `text/plain`; packet metadata must decode base64 correctly.
- dependencies_and_callers: Used by input controller/paste handling.
- edge_cases_or_failure_modes: Malformed base64, unsupported MIME, missing listing, packet terminator variants BEL/ST.
- validation_or_tests: Covered by `packages/coding-agent/test/utils/enhanced-paste.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2414 `file` `packages/coding-agent/src/workflow/display.ts`
- cursor: `[_]`
- core_role: Workflow node role/display label formatter.
- algorithmic_behavior: Converts workflow node IDs/roles into human-friendly work item labels, semantic roles, review/program roles, namespace-stripped titles, and acronym-aware title case (`packages/coding-agent/src/workflow/display.ts:1-94`).
- inputs_outputs_state: Inputs are workflow node objects and node IDs. Outputs are display strings for workflow UI/task labels. No persistent state.
- gates_or_invariants: Semantic regex matching maps investigative/build/review/setup patterns to stable roles.
- dependencies_and_callers: Used by workflow graph/UI and task tool runtime.
- edge_cases_or_failure_modes: Unusual node IDs, acronym preservation, namespace splitting with `__`.
- validation_or_tests: Covered by workflow graph/display tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2444 `file` `packages/coding-agent/test/cli/completions.test.ts`
- cursor: `[_]`
- core_role: Tests shell completion generation/dispatch for the CLI.
- algorithmic_behavior: Validates completions command behavior, option/command suggestions, and shell-specific output contracts.
- inputs_outputs_state: Inputs are completion argv/env scenarios. Outputs are completion script or candidate lists.
- gates_or_invariants: Completion output must remain parseable by target shell and not include invalid flags.
- dependencies_and_callers: Exercises CLI completions module.
- edge_cases_or_failure_modes: Nested commands, unknown flags, partial tokens.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2474 `file` `packages/coding-agent/test/core/python-kernel-env.test.ts`
- cursor: `[_]`
- core_role: Tests Python kernel environment construction.
- algorithmic_behavior: Validates env propagation/isolation for Python kernel/core execution.
- inputs_outputs_state: Inputs are session/tool env settings and Python kernel launch options. Outputs are observed environment variables inside kernel process.
- gates_or_invariants: Kernel env should include required tool variables without leaking or dropping user-provided values unexpectedly.
- dependencies_and_callers: Exercises coding-agent Python execution core.
- edge_cases_or_failure_modes: Missing PATH/python env, conflicting env overrides.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2504 `file` `packages/coding-agent/test/discovery/pi-config-dir.test.ts`
- cursor: `[_]`
- core_role: Tests pi config directory discovery behavior.
- algorithmic_behavior: Validates config dir resolution for project/user/plugin profile paths.
- inputs_outputs_state: Inputs are temporary cwd/config dirs and env/profile settings. Outputs are discovered config paths.
- gates_or_invariants: Project-scoped config should be preferred where appropriate without leaking unrelated dirs.
- dependencies_and_callers: Exercises discovery helper/config dir logic.
- edge_cases_or_failure_modes: Missing dirs, profile isolation, path ordering.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2534 `file` `packages/coding-agent/test/internal-urls/issue-pr-protocol.test.ts`
- cursor: `[_]`
- core_role: Tests internal `issue://` and `pr://` protocol handlers.
- algorithmic_behavior: Validates issue/PR cache resolution, stale fallback, `gh` fallback without `stateReason`, comments suppression cache rows, invalid URL errors, PR reviews, path segment rejection, diff listing/all/file slicing, shared diff invocation, listing with query params, and cross-handler cache sharing (`packages/coding-agent/test/internal-urls/issue-pr-protocol.test.ts:156-497`).
- inputs_outputs_state: Inputs are internal URLs, mocked GitHub CLI/API outputs, cache state, and query params. Outputs are rendered markdown, text/plain diffs, or friendly errors.
- gates_or_invariants: Diff file indexes are 1-indexed; invalid state errors rather than falling back; empty/dot/dotdot path segments rejected.
- dependencies_and_callers: Exercises internal URL protocol handlers, GitHub cache, and `gh` wrappers.
- edge_cases_or_failure_modes: Soft-expired cache, no session repo, PR with no changes, non-decimal/out-of-range diff index, repo named `diff`.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2564 `file` `packages/coding-agent/test/registry/agent-lifecycle.test.ts`
- cursor: `[_]`
- core_role: Tests agent lifecycle manager adoption, parking, revival, and release.
- algorithmic_behavior: Validates idle TTL parking, running/idle timer transitions, `ensureLive` revive/coalescing/errors, cold revive via persisted factory, declined/failed revive behavior, release cleanup, Main no-op, parking state timing, and zero TTL behavior (`packages/coding-agent/test/registry/agent-lifecycle.test.ts:38-295`).
- inputs_outputs_state: Inputs are agent refs, timers, revivers, session files, lifecycle status changes. Outputs are parked/live/disposed state and errors.
- gates_or_invariants: Main is never adopted/parked; concurrent revive coalesces; failed cold revive is not sticky.
- dependencies_and_callers: Exercises agent registry/lifecycle used by subagents and history.
- edge_cases_or_failure_modes: Park dispose in-flight, transcript-only parked refs, unknown IDs with `history://` guidance.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2594 `file` `packages/coding-agent/test/slash-commands/btw.test.ts`
- cursor: `[_]`
- core_role: Tests `/btw` interactive slash command routing.
- algorithmic_behavior: Ensures full question and raw multi-word suffix after `/btw` are routed through interactive handler (`packages/coding-agent/test/slash-commands/btw.test.ts:20-31`).
- inputs_outputs_state: Inputs are interactive slash command strings. Outputs are handler calls/prompt routing.
- gates_or_invariants: Suffix text must not be truncated or reparsed incorrectly.
- dependencies_and_callers: Exercises slash command controller/interactive mode.
- edge_cases_or_failure_modes: Multi-word argument preservation.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2624 `file` `packages/coding-agent/test/task/spawn-advisory.test.ts`
- cursor: `[_]`
- core_role: Tests task spawn specialization advisory behavior.
- algorithmic_behavior: Validates generic role-less spawn nudges, max-depth silence, role presence silence, whitespace-only role handling, duplicate generic agent nudges, non-generic silence, and session suppression (`packages/coding-agent/test/task/spawn-advisory.test.ts:18-108`).
- inputs_outputs_state: Inputs are task spawn args, depth/capacity, role strings, and suppression flag. Outputs are advisory text or undefined.
- gates_or_invariants: Advisory only appears when it can improve subagent specialization and spawn capacity remains.
- dependencies_and_callers: Exercises task tool advisory generation.
- edge_cases_or_failure_modes: Whitespace role and cloned same agent.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2654 `file` `packages/coding-agent/test/tools/browser-readable.test.ts`
- cursor: `[_]`
- core_role: Tests readable content extraction from browser pages.
- algorithmic_behavior: Validates article-style and docs-style main content extraction (`packages/coding-agent/test/tools/browser-readable.test.ts:4-25`).
- inputs_outputs_state: Inputs are HTML/page content fixtures. Outputs are markdown/readable text.
- gates_or_invariants: Extractor should prioritize meaningful article/main content over chrome/nav.
- dependencies_and_callers: Exercises browser readable extraction tool path.
- edge_cases_or_failure_modes: Docs pages with main content layouts.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2684 `file` `packages/coding-agent/test/tools/jtd-to-json-schema.test.ts`
- cursor: `[_]`
- core_role: Tests JTD-to-JSON-Schema conversion.
- algorithmic_behavior: Validates elements/primitive conversion, nested JTD fragment normalization inside JSON Schema, and user-named properties colliding with JTD keywords (`packages/coding-agent/test/tools/jtd-to-json-schema.test.ts:4-72`).
- inputs_outputs_state: Inputs are JTD/mixed schema objects. Outputs are JSON Schema objects.
- gates_or_invariants: Keyword-like user property names are preserved as properties, not parsed as JTD structure.
- dependencies_and_callers: Exercises `packages/coding-agent/src/tools/jtd-to-json-schema.ts`.
- edge_cases_or_failure_modes: Nested JTD and int32 primitive mapping.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2714 `file` `packages/coding-agent/test/tools/split-internal-url-sel.test.ts`
- cursor: `[_]`
- core_role: Tests selector peeling from internal URL paths.
- algorithmic_behavior: Validates no-selector identity, line-range/raw/compound selectors, malformed `:-N`, skill URLs, non-selector tails, scheme separator stop, and opaque `mcp://` handling (`packages/coding-agent/test/tools/split-internal-url-sel.test.ts:4-121`).
- inputs_outputs_state: Inputs are URL/path strings with optional selector suffixes. Outputs are base URL and selector pieces.
- gates_or_invariants: `mcp://` URIs are opaque by default; unknown schemes are not peeled.
- dependencies_and_callers: Exercises path selector parsing for read/internal URL tools.
- edge_cases_or_failure_modes: Degenerate `mcp://:1-50`, escaped suffixes, trailing slash integer suffixes.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2744 `file` `packages/coding-agent/test/utils/open.test.ts`
- cursor: `[_]`
- core_role: Tests platform-aware open path/URL behavior.
- algorithmic_behavior: Validates WSL mount file opening through `wslview` with Windows path, URL opening through `xdg-open`, and fallback to `xdg-open` when `wslview` is unavailable (`packages/coding-agent/test/utils/open.test.ts:90-122`).
- inputs_outputs_state: Inputs are file paths/URLs, platform/env detection, available commands. Outputs are spawned opener commands.
- gates_or_invariants: Only existing WSL mount files are path-converted; URLs stay URL-shaped.
- dependencies_and_callers: Exercises open utility and command lookup.
- edge_cases_or_failure_modes: Missing `wslview`, WSL mount conversion, URL vs file distinction.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2774 `file` `packages/collab-web/src/lib/jsonl.ts`
- cursor: `[_]`
- core_role: Incremental JSONL parser for collab web streaming client.
- algorithmic_behavior: `parseJsonl(text, carry)` prepends carry, splits on newline, parses complete lines as JSON, and returns parsed items plus unfinished carry (`packages/collab-web/src/lib/jsonl.ts:8-9`).
- inputs_outputs_state: Inputs are streamed text chunk and prior carry. Outputs are `items` and new `carry`. State is externalized as carry string.
- gates_or_invariants: Incomplete trailing line is not parsed until next chunk.
- dependencies_and_callers: Used by collab-web client streaming transcript/event ingestion.
- edge_cases_or_failure_modes: Malformed complete JSON line throws; chunk boundaries inside JSON are handled by carry.
- validation_or_tests: Indirectly covered by collab web streaming/session replication tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2804 `file` `packages/mnemopi/src/core/orchestrator.ts`
- cursor: `[_]`
- core_role: Orchestrates memory recall by embedding query and linear beam recall.
- algorithmic_behavior: Converts orchestration options to linear recall options and calls embedding/beam recall to return simplified recall results (`packages/mnemopi/src/core/orchestrator.ts:32-39`).
- inputs_outputs_state: Inputs are query text, beam memory state, recall options. Outputs are orchestrated recall results with metadata omitted/reshaped. No persistent state beyond beam.
- gates_or_invariants: Recall options conversion preserves top-k/filters while hiding lower-level scoring details.
- dependencies_and_callers: Depends on `embedQuery` and beam recall modules.
- edge_cases_or_failure_modes: Embedding failure, empty beam, no matches.
- validation_or_tests: Indirectly covered by mnemopi beam/local tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2834 `file` `packages/stats/src/client/css.d.ts`
- cursor: `[_]`
- core_role: TypeScript declaration shim for CSS imports in stats client.
- algorithmic_behavior: Declares CSS module import type; no runtime algorithm.
- inputs_outputs_state: Input is TypeScript compiler resolving `.css`; output is compile-time type compatibility. No state.
- gates_or_invariants: Enables TS/Vite import of CSS without type errors.
- dependencies_and_callers: Used by stats React client build.
- edge_cases_or_failure_modes: Missing declaration would produce compile-time CSS import errors.
- validation_or_tests: Covered by stats dashboard build/type checks.
- skip_candidate: `yes: compile-time declaration only`

### OH_MY_HUMANIZE_MAIN-HZ-2864 `file` `python/omp-rpc/src/omp_rpc/__init__.py`
- cursor: `[_]`
- core_role: Python RPC client package surface and implementation entry.
- algorithmic_behavior: Exports/implements client-facing RPC helpers, protocol types, and convenience APIs used by Python consumers.
- inputs_outputs_state: Inputs are RPC server command paths, prompts, host tool/URI callbacks, and JSONL frames. Outputs are client commands/events and typed parsed results.
- gates_or_invariants: Package API must remain stable for tests importing `RpcClient` and protocol helpers.
- dependencies_and_callers: Exercised by `python/omp-rpc/tests/test_client.py`, `test_protocol.py`, `test_host_uris.py`, and `test_user_group.py`.
- edge_cases_or_failure_modes: Startup failures, malformed frames, stop behavior, listener mutation/errors.
- validation_or_tests: Covered by the `python/omp-rpc/tests` directory.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2894 `directory` `packages/utils/src/vendor/mermaid-ascii/ascii`
- cursor: `[_]`
- core_role: Vendored Mermaid-to-ASCII rendering engine.
- algorithmic_behavior: Recursively contains canvas/role-canvas manipulation, graph conversion, grid layout, edge routing/bundling/pathfinding, shape rendering, class/ER/sequence/XY chart renderers, ANSI/HTML colorization, diagonal validation, and shared types. Important modules include `canvas.ts`, `converter.ts`, `draw.ts`, `edge-routing.ts`, `edge-bundling.ts`, `pathfinder.ts`, `shapes/*`, `class-diagram.ts`, `er-diagram.ts`, `sequence.ts`, and `xychart.ts`.
- inputs_outputs_state: Inputs are parsed Mermaid graph/diagram structures, ASCII config, color mode, theme, and labels. Outputs are ASCII canvas strings with optional ANSI/HTML color and role metadata. State is local graph/canvas/grid/path structures.
- gates_or_invariants: Canvas merge handles junctions/wide chars; pathfinding avoids occupied grid cells; shape registry maps node shapes to dimensions/render/attachment; validation rejects diagonal lines.
- dependencies_and_callers: Depends on vendored Mermaid parsers/types and text metrics; used by utilities rendering diagrams to terminal/text.
- edge_cases_or_failure_modes: Wide labels, subgraph nesting, self-references, bundled edges, diagonal avoidance, HTML escaping, terminal color capability.
- validation_or_tests: Indirectly covered by diagram rendering tests; specific assigned files `class-diagram.ts` and `shapes/rectangle.ts` provide deeper evidence.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2924 `file` `packages/ai/src/providers/__tests__/openai-codex-error.test.ts`
- cursor: `[_]`
- core_role: Tests Codex Responses error event classification/formatting.
- algorithmic_behavior: Validates retryable code extraction from nested/top-level fields, message-based retry detection, response.error fallback, mistyped fields tolerance, provider stream error creation, and response-failure formatting (`packages/ai/src/providers/__tests__/openai-codex-error.test.ts:4-75`).
- inputs_outputs_state: Inputs are raw Codex failure events with varied error shapes. Outputs are retryable booleans and provider error objects.
- gates_or_invariants: Nested `error.code` takes precedence over top-level code; malformed fields do not crash parse.
- dependencies_and_callers: Exercises OpenAI Codex Responses provider error handling.
- edge_cases_or_failure_modes: Absent/unknown codes, non-object raw error, non-error failures.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2954 `file` `packages/ai/src/utils/schema/meta-validator.ts`
- cursor: `[_]`
- core_role: Lightweight structural JSON Schema validator for normalized tool schemas.
- algorithmic_behavior: Recursively checks plain objects, type keyword validity, unique JSON enum/const values, schema arrays/maps, numeric integer constraints, and memoizes cycle visits via epoch stamps; public `isValidJsonSchema` at `packages/ai/src/utils/schema/meta-validator.ts:161`.
- inputs_outputs_state: Input is unknown schema. Output is boolean validity. State uses epoch stamping through `epochNext`/`once`.
- gates_or_invariants: Type names are constrained; schema arrays/maps recurse; duplicate JSON values rejected where uniqueness matters.
- dependencies_and_callers: Depends on schema equality/stamp helpers; used by schema normalization fallback, especially CCA path.
- edge_cases_or_failure_modes: Cycles, non-plain objects, invalid type arrays, bad numeric bounds, duplicate enum values.
- validation_or_tests: Covered by Google/tool schema normalization tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2984 `file` `packages/coding-agent/src/commit/agentic/fallback.ts`
- cursor: `[_]`
- core_role: Fallback conventional commit analysis/proposal generator from changed file stats.
- algorithmic_behavior: Infers commit type from file paths/extensions, summarizes changed paths, and builds fallback commit proposal (`packages/coding-agent/src/commit/agentic/fallback.ts:5-87`).
- inputs_outputs_state: Inputs are numstat entries. Outputs are `ConventionalAnalysis`, summary string, and `CommitProposal`.
- gates_or_invariants: Test/doc/config/style path patterns bias type selection; extension parsing normalizes file class.
- dependencies_and_callers: Used when agentic commit analysis LLM is unavailable or fails.
- edge_cases_or_failure_modes: Mixed file types, unknown extensions, no files.
- validation_or_tests: Covered by commit command/agentic tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3014 `file` `packages/coding-agent/src/edit/hashline/params.ts`
- cursor: `[_]`
- core_role: Parameter/type definitions for hashline edit integration.
- algorithmic_behavior: Defines the parameter shape used by hashline edit tools; no complex local algorithm.
- inputs_outputs_state: Inputs are edit/hashline tool arguments. Outputs are typed params for downstream patcher. No state.
- gates_or_invariants: Centralizes parameter contract to keep renderer/tool/parser aligned.
- dependencies_and_callers: Used by coding-agent edit/hashline modules and tests.
- edge_cases_or_failure_modes: Type drift can desynchronize tool schema and patcher expectations.
- validation_or_tests: Covered by hashline/edit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3044 `file` `packages/coding-agent/src/export/html/index.ts`
- cursor: `[_]`
- core_role: Session transcript HTML export generator.
- algorithmic_behavior: Loads/caches HTML template, generates theme vars, builds session data, collects subsessions, renders HTML with CSS/JS/tool views, exports from current session or file, reconstructs workflow inspections, and redacts freeze snapshots (`packages/coding-agent/src/export/html/index.ts:24-307`).
- inputs_outputs_state: Inputs are session manager/file, entries, theme, output options, workflow lifecycle entries. Outputs are HTML file/string. State includes cached template and filesystem output.
- gates_or_invariants: Missing session paths handled via `isEnoent`; export colors derive readable backgrounds; workflow freeze snapshots are redacted for HTML export.
- dependencies_and_callers: Depends on session manager/loader, workflow lifecycle/run-store, theme, template assets, tool views, filesystem.
- edge_cases_or_failure_modes: Missing subsession files, invalid colors, absent theme, private workflow data redaction.
- validation_or_tests: Covered by `packages/coding-agent/test/export/html-workflow-export.test.ts` and export subsession tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3074 `file` `packages/coding-agent/src/extensibility/plugins/marketplace-auto-update.ts`
- cursor: `[_]`
- core_role: Schedules plugin marketplace auto-update/notification work.
- algorithmic_behavior: `scheduleMarketplaceAutoUpdate` defers `runMarketplaceAutoUpdate`, which uses marketplace options and logs failures (`packages/coding-agent/src/extensibility/plugins/marketplace-auto-update.ts:11-19`).
- inputs_outputs_state: Inputs are mode/cwd/options. Outputs are plugin update side effects or notifications. State is timer/deferred async work.
- gates_or_invariants: Modes are constrained to `off`, `notify`, or `auto`; off should avoid update side effects.
- dependencies_and_callers: Depends on plugin marketplace/project dir utilities and logger.
- edge_cases_or_failure_modes: Async update failure must not crash startup.
- validation_or_tests: Covered by plugin marketplace/extension tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3104 `file` `packages/coding-agent/src/modes/components/branch-summary-message.ts`
- cursor: `[_]`
- core_role: TUI component rendering branch summary messages.
- algorithmic_behavior: `BranchSummaryMessageComponent` composes markdown/text/spacer elements with theme markdown styles (`packages/coding-agent/src/modes/components/branch-summary-message.ts:1-9`).
- inputs_outputs_state: Input is `BranchSummaryMessage`; output is rendered TUI rows. State is component tree only.
- gates_or_invariants: Markdown rendering uses current theme.
- dependencies_and_callers: Used by interactive mode transcript rendering for branch summaries.
- edge_cases_or_failure_modes: Long markdown must be handled by Markdown component.
- validation_or_tests: Covered by UI/render tests around branch/session messages.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3134 `file` `packages/coding-agent/src/modes/components/omfg-panel.ts`
- cursor: `[_]`
- core_role: TUI panel component for OMFG state/content display.
- algorithmic_behavior: Defines state union and `OmfgPanelComponent`, sanitizes tabs, renders markdown/content inside dynamic border (`packages/coding-agent/src/modes/components/omfg-panel.ts:1-21`).
- inputs_outputs_state: Inputs are panel state/content/theme/TUI. Outputs are rendered rows. State is component state.
- gates_or_invariants: Raw content is passed through `replaceTabs` before rendering to protect terminal layout.
- dependencies_and_callers: Depends on pi-tui components, markdown theme, dynamic border, render utils.
- edge_cases_or_failure_modes: Empty/loading/error states and tab-containing content.
- validation_or_tests: Covered by slash command `/omfg` and component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3164 `file` `packages/coding-agent/src/modes/components/workflow-graph.ts`
- cursor: `[_]`
- core_role: Complex TUI workflow graph/dashboard renderer.
- algorithmic_behavior: Renders workflow graph blocks at full/compact density, dashboard headers/body, workbench/focus/operator rail, flow lens, diagram clipping, collapsed rows, action mapping, context height fitting, flow map hints, legend, and live agent tabs. Key functions start at `renderWorkflowGraphBlock` `packages/coding-agent/src/modes/components/workflow-graph.ts:153`, layout at `290`, workbench at `487`, action kinds at `594`, clipping/fitting at `1135-1497`, and controls at `1508`.
- inputs_outputs_state: Inputs are `WorkflowGraphView`, width/height budget, display mode, active agents/nodes/edges/actions/theme. Outputs are terminal row strings and native scrollback live-region metadata. State is component-local selected view/action and derived layout.
- gates_or_invariants: Minimum height/width budgets, compact profiles, row clipping markers, action priority ordering, selected-agent targeting, back-edge detection, and glyph/status mapping must stay stable.
- dependencies_and_callers: Depends on pi-tui component interfaces, workflow monitor display mode, theme, and workflow graph view model.
- edge_cases_or_failure_modes: Tiny viewports, ultrawide panes, hidden diagram rows, duplicate rail/focus controls, live work vs completed graph, partial node box trimming.
- validation_or_tests: Covered by workflow graph/component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3194 `file` `packages/coding-agent/src/modes/utils/context-usage.ts`
- cursor: `[_]`
- core_role: Computes and renders context usage breakdown for interactive mode.
- algorithmic_behavior: Estimates skill/tool/system/message tokens, computes context breakdown, plans 20x10 grid cells, builds legend lines, and renders a context usage visualization (`packages/coding-agent/src/modes/utils/context-usage.ts:13-399`).
- inputs_outputs_state: Inputs are `AgentSession`, model context window, tools, skills, messages, compaction settings, and theme. Outputs are token counts, category breakdown, rendered grid/legend. No persistent state.
- gates_or_invariants: Reserve tokens and compaction thresholds are included; grid cell allocation must represent categories without exceeding fixed cell count.
- dependencies_and_callers: Depends on pi-agent compaction/token estimation, pi-ai schema serialization, snapcompact savings estimates, theme.
- edge_cases_or_failure_modes: Missing tools/skills/messages, very small context windows, estimates exceeding capacity.
- validation_or_tests: Covered by `packages/coding-agent/test/modes/context-usage.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3224 `file` `packages/coding-agent/src/web/scrapers/arxiv.ts`
- cursor: `[_]`
- core_role: Special web scraper for arXiv pages/PDFs.
- algorithmic_behavior: Extracts arXiv ID, loads API/page metadata, formats published date/title/authors/summary, optionally fetches PDF and converts with Markit (`packages/coding-agent/src/web/scrapers/arxiv.ts:8-65`).
- inputs_outputs_state: Inputs are arXiv URL, timeout, abort signal. Outputs are `RenderResult` markdown/text or null. State is per-request fetch buffers.
- gates_or_invariants: Only arXiv-compatible URLs are handled; PDF conversion respects timeout/signal.
- dependencies_and_callers: Depends on scraper `types`, binary fetch, Markit conversion, web fetch pipeline.
- edge_cases_or_failure_modes: Missing API entry, PDF fetch/conversion failure, abort, invalid URL.
- validation_or_tests: Covered by web scraper academic/research tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3254 `file` `packages/coding-agent/src/web/scrapers/index.ts`
- cursor: `[_]`
- core_role: Registry/export surface for special web scrapers.
- algorithmic_behavior: Imports dozens of domain handlers, re-exports selected scraper utilities, and builds ordered `specialHandlers` array (`packages/coding-agent/src/web/scrapers/index.ts:6-164`).
- inputs_outputs_state: Inputs are URLs routed through handlers. Output is first handler render result or null by upstream dispatcher. State is static handler order.
- gates_or_invariants: Handler order can affect routing; GitHub and many package/research/social/security handlers are registered centrally.
- dependencies_and_callers: Used by web fetch/search tools to special-case known domains.
- edge_cases_or_failure_modes: Misordered handlers can shadow more specific domains; missing export breaks tests.
- validation_or_tests: Covered by extensive `packages/coding-agent/test/tools/web-scrapers/*`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3284 `file` `packages/coding-agent/src/web/scrapers/semantic-scholar.ts`
- cursor: `[_]`
- core_role: Special scraper for Semantic Scholar paper pages/API.
- algorithmic_behavior: Extracts paper ID, loads Semantic Scholar API/page JSON, formats title/authors/year/citation/reference counts/abstract (`packages/coding-agent/src/web/scrapers/semantic-scholar.ts:5-47`).
- inputs_outputs_state: Inputs are Semantic Scholar URL, timeout, signal. Outputs are rendered paper metadata or null.
- gates_or_invariants: `extractPaperId` must only accept supported paper URL shapes.
- dependencies_and_callers: Depends on `tryParseJson`, scraper types/buildResult/loadPage.
- edge_cases_or_failure_modes: Invalid ID, missing fields, failed API/page load, malformed JSON.
- validation_or_tests: Covered by web scraper research/academic tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3314 `file` `packages/coding-agent/test/modes/components/background-tan-message.test.ts`
- cursor: `[_]`
- core_role: Tests compact background TAN dispatch message rendering.
- algorithmic_behavior: Ensures one compact line with job ID/work preview and truncates overlong preview into a single pill (`packages/coding-agent/test/modes/components/background-tan-message.test.ts:20-38`).
- inputs_outputs_state: Inputs are background TAN dispatch data and preview text. Outputs are rendered TUI line(s).
- gates_or_invariants: Raw notice text must not leak; line remains single compact row.
- dependencies_and_callers: Exercises background TAN message component.
- edge_cases_or_failure_modes: Overlong work preview truncation.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3344 `file` `packages/coding-agent/test/modes/controllers/bash-command.test.ts`
- cursor: `[_]`
- core_role: Tests interactive `!` bash shortcut command.
- algorithmic_behavior: Verifies `!` commands run through configured user shell (`packages/coding-agent/test/modes/controllers/bash-command.test.ts:15-22`).
- inputs_outputs_state: Inputs are interactive command text and shell config. Outputs are shell execution requests.
- gates_or_invariants: Shortcut uses user shell, not hardcoded shell.
- dependencies_and_callers: Exercises interactive bash command controller.
- edge_cases_or_failure_modes: Shell path/config mismatch.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3374 `file` `packages/coding-agent/test/tools/web-scrapers/git-hosting.test.ts`
- cursor: `[_]`
- core_role: Tests GitHub/gist/actions/commit web scraper parsing and rendering.
- algorithmic_behavior: Validates repo root/blob/tree/issues/pulls/gist fetches, invalid host rejection, gist metadata/content, rate-limit handling, Actions run/job URL classification, commit URL classification, and timestamp stripping (`packages/coding-agent/test/tools/web-scrapers/git-hosting.test.ts:12-280`).
- inputs_outputs_state: Inputs are GitHub/gist URLs and mocked API responses. Outputs are rendered markdown or parsed URL classifications.
- gates_or_invariants: Non-GitHub hosts return null; Actions run/job IDs must be numeric; commit SHA can be full or abbreviated.
- dependencies_and_callers: Exercises GitHub and gist special scrapers.
- edge_cases_or_failure_modes: Nonexistent gist, invalid gist ID, workflow files not runs/jobs, BOM/timestamp log cleanup.
- validation_or_tests: This file is validation by construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3404 `file` `packages/collab-web/src/components/transcript/Transcript.tsx`
- cursor: `[_]`
- core_role: React transcript renderer for collaborative web UI.
- algorithmic_behavior: Renders user/assistant/tool rows, thinking blocks, text/image content, active tools, memoized entry rows, token stats, and scroll behavior. Key functions include `Row`, `ThinkingBlock`, `MsgContent`, `AssistantBody`, memoized `EntryRow`, and exported `Transcript` (`packages/collab-web/src/components/transcript/Transcript.tsx:12-244`).
- inputs_outputs_state: Inputs are session entries, tool results, active tools, and render host. Outputs are React nodes for transcript UI. State includes expanded/collapsed thinking/tool sections and scroll refs.
- gates_or_invariants: `entryRowEqual` avoids unnecessary rerenders while preserving active/result changes.
- dependencies_and_callers: Depends on pi-wire types, tool render host, Markdown, ToolCard, client active tool state.
- edge_cases_or_failure_modes: Mixed text/image content arrays, redacted thinking, active tool result association, memo equality drift.
- validation_or_tests: Covered by collab web transcript/session replication tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3434 `file` `packages/collab-web/src/tool-render/tools/web-search.tsx`
- cursor: `[_]`
- core_role: Web-search tool renderer for collab web UI.
- algorithmic_behavior: Extracts domains, formats age, renders summary, source rows, badges, query/provider details, notes/errors, and result text using shared tool-render parts (`packages/collab-web/src/tool-render/tools/web-search.tsx:7-42`).
- inputs_outputs_state: Inputs are tool args/details/result payload. Outputs are React nodes representing tool call/result.
- gates_or_invariants: Invalid/missing args render as invalid arg UI; URLs are truncated/domainized.
- dependencies_and_callers: Depends on tool-render parts/utilities and web search tool details.
- edge_cases_or_failure_modes: Bad URLs, unknown ages, missing sources, non-record details.
- validation_or_tests: Covered by collab web/tool-render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3464 `file` `packages/stats/src/client/routes/BehaviorRoute.tsx`
- cursor: `[_]`
- core_role: Stats dashboard route for behavior/model metrics.
- algorithmic_behavior: Fetches behavior dashboard stats, builds summary panel, chart panel with metric selector, model table, expandable detail rows, breakdown charts, and trend lookup (`packages/stats/src/client/routes/BehaviorRoute.tsx:38-578`).
- inputs_outputs_state: Inputs are active/range/refresh props, API stats, user metric/table expansion state, system theme. Outputs are React chart/table panels.
- gates_or_invariants: Rates divide by message counts safely; time series bucket and chart colors stay consistent.
- dependencies_and_callers: Depends on stats API/data view models, Chart.js, UI components, date-fns, theme hook.
- edge_cases_or_failure_modes: Zero messages, missing model trend, empty data, inactive route.
- validation_or_tests: Covered by stats dashboard bundle/client tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3494 `file` `python/robomp/web/src/components/IssueLink.tsx`
- cursor: `[_]`
- core_role: SolidJS link components for issue and PR URLs in robomp dashboard.
- algorithmic_behavior: Defines `IssueLink` and `PrLink`, rendering anchors from `issueUrl`/`prUrl` helpers (`python/robomp/web/src/components/IssueLink.tsx:5-30`).
- inputs_outputs_state: Inputs are owner/repo/number props. Outputs are JSX anchor elements.
- gates_or_invariants: Uses shared formatter so URL construction is centralized.
- dependencies_and_callers: Used by robomp `Events`, `Issues`, `Working` components.
- edge_cases_or_failure_modes: Invalid repo/number props produce bad links if caller passes bad data.
- validation_or_tests: Covered indirectly by robomp web component/build tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3524 `file` `packages/coding-agent/src/export/html/vendor/marked.min.js`
- cursor: `[_]`
- core_role: Vendored minified Marked Markdown parser used by HTML transcript export.
- algorithmic_behavior: Contains lexer/tokenizer/parser/renderer pipeline for Markdown blocks/inline tokens, extension hooks, async parsing, renderer methods, and error handling; minified source includes classes for tokenizer/lexer/parser and exported `marked` API.
- inputs_outputs_state: Inputs are Markdown strings and Marked options/extensions. Outputs are HTML strings/tokens. Internal state includes lexer token arrays/link maps and parser renderer state.
- gates_or_invariants: Input must be string; silent mode returns error HTML; parser throws token-not-found errors otherwise.
- dependencies_and_callers: Used by exported HTML template JavaScript to render transcript Markdown offline.
- edge_cases_or_failure_modes: Malformed Markdown extension, async option mismatch, infinite lexer loop detection, unsafe HTML depending on renderer configuration.
- validation_or_tests: Covered indirectly by HTML export tests.
- skip_candidate: `yes: vendored third-party minified library, not repo-authored algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3554 `file` `packages/coding-agent/src/modes/setup-wizard/scenes/glyph.ts`
- cursor: `[_]`
- core_role: Setup wizard scene for choosing terminal glyph/symbol preset.
- algorithmic_behavior: Defines glyph presets/items, controller with keyboard/mouse selection, commits `setSymbolPreset`, and exports scene (`packages/coding-agent/src/modes/setup-wizard/scenes/glyph.ts:5-109`).
- inputs_outputs_state: Inputs are setup host, select list events, symbol preset. Outputs are UI scene and persisted theme symbol preset. State includes select list/controller current selection.
- gates_or_invariants: Preset values limited to `nerd`, `unicode`, `ascii`.
- dependencies_and_callers: Depends on pi-tui select list and theme symbol preset APIs.
- edge_cases_or_failure_modes: Mouse selection and commit failure; unsupported terminal glyph display.
- validation_or_tests: Covered by setup wizard/theme tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3584 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/class-diagram.ts`
- cursor: `[_]`
- core_role: Mermaid class diagram to ASCII renderer.
- algorithmic_behavior: Parses class diagrams, formats members, builds class box sections, maps relationship markers, places class nodes, draws boxes/relationships on canvas, roles chars for coloring, and returns canvas string (`packages/utils/src/vendor/mermaid-ascii/ascii/class-diagram.ts:22-152`).
- inputs_outputs_state: Inputs are Mermaid class diagram text, ASCII config, color mode/theme. Outputs are ASCII class diagram string. State includes placed classes, relationship marker data, canvas/role canvas.
- gates_or_invariants: Comment lines are filtered; member visibility/type formatting preserved; relationship markers depend on type and direction.
- dependencies_and_callers: Depends on class parser/types, canvas/draw/multiline/text metrics, shape corners.
- edge_cases_or_failure_modes: Long labels/members, relationship direction, unsupported relationship markers, disconnected classes.
- validation_or_tests: Covered by vendored diagram rendering tests or downstream diagram snapshots.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3614 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/rectangle.ts`
- cursor: `[_]`
- core_role: Rectangle shape renderer and attachment-point calculator for Mermaid ASCII engine.
- algorithmic_behavior: Computes box dimensions from label and shape options, renders rectangle canvas with corners/borders/text, computes attachment points by direction, and exports `rectangleRenderer` (`packages/utils/src/vendor/mermaid-ascii/ascii/shapes/rectangle.ts:26-166`).
- inputs_outputs_state: Inputs are label, shape render options, direction, and corner style. Outputs are `ShapeDimensions`, canvas, and drawing coordinate attachment point.
- gates_or_invariants: Text width uses display-width cell conversion; attachment logic distinguishes up/down/left/right/diagonal/middle directions.
- dependencies_and_callers: Depends on canvas creation, edge direction equality, corners, split lines, and text metrics.
- edge_cases_or_failure_modes: Wide characters, multiline labels, ASCII vs Unicode corners, diagonal attachment directions.
- validation_or_tests: Covered indirectly by Mermaid ASCII rendering tests.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `121 item evidence sections counted above; each assigned row was represented as one section`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`

---

## Incremental Directory Refresh Addendum - oh-my-humanize/main bf4509d4f - OH_MY_HUMANIZE_MAIN-HZ-134

# agent_dir_07 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-134 `directory` `packages/coding-agent/test`
- cursor: `[_]`
- current_directory_core_role: `packages/coding-agent/test` is the package-wide contract suite for the coding-agent CLI/runtime. Its `test/workflow/` subtree specifically owns observable workflow behavior: definition parsing, scheduler traversal, node runtime adapter dispatch, shell/script runtime execution, lifecycle/run-store persistence, checkpoint/restart state, graph views, slash commands, and end-to-end workflow scenarios. The changed descendant `test/workflow/runner.test.ts` is the main runner-level contract file tying scheduler results to persisted run/lifecycle events.
- directory_level_delta_since_old_commit: The direct in-directory delta is concentrated in `packages/coding-agent/test/workflow/runner.test.ts` and expands runner coverage around interruption and deadline behavior. The suite now pins that workflow stop/cancellation produces restartable lifecycle checkpoints rather than failed attempts, including cases where the active node is aborted by a separate node-level signal, where the node runtime ignores the abort and never resolves, and where `maxRuntimeMs` elapses. The broader diff also adds CLI-side coverage outside this directory for headless JS scripts running from the requested `--cwd`; within this assigned directory, existing workflow script runtime tests already define the package-level expectation that workflow scripts run relative to the workflow/session cwd.
- affected_descendant_algorithms: The affected algorithms are workflow runner activation execution, scheduler stop/frontier calculation, lifecycle checkpoint materialization, run-store activation persistence, and script runtime cwd contracts. Runner behavior now distinguishes the scheduler stop signal from the per-node abort signal, races node execution against node abort/deadline so an ignored abort cannot hang the workflow, persists `activation_aborted` records, and emits checkpoints whose frontier can restart at the aborted or unscheduled node. Headless workflow start behavior also depends on cwd propagation through CLI start, session runtime host creation, and eval script execution.
- current_inputs_outputs_state: Runner tests construct workflow definitions from inline YAML, use in-memory `WorkflowRunStoreHost` entries, provide runtime host stubs for agent/review/script nodes, pass lifecycle metadata with frozen flow snapshots and runtime binding snapshots, and drive behavior with `AbortController` signals, `maxActivations`, `maxRuntimeMs`, and completed activation snapshots. Observable outputs are `runWorkflow()` scheduler activations, activation statuses/errors/reasons, scheduler frontier node ids, reconstructed workflow run state, reconstructed lifecycle attempts, and checkpoint records containing completed/aborted activation ids, frontier ids, state, and source mapping. Script/cwd contracts use temp workspaces and file reads to prove relative file access lands in the requested cwd.
- new_or_changed_gates_or_invariants: A scheduler stop signal must stop downstream scheduling without necessarily aborting the current node when a dedicated node abort signal exists. A node abort/deadline must persist the activation as `aborted`, not `failed`, and frozen lifecycle attempts must become `stopped` with a checkpoint. If a node runtime ignores abort and leaves its promise pending, the runner must still resolve promptly by rejecting from the abort signal and checkpointing. `maxRuntimeMs` must abort both workflow scheduling and node execution with the stable reason `workflow max runtime elapsed after <n>ms`, then clear its timer. Checkpoints may include `abortedActivationIds` and must not be created while lifecycle activations remain `running`. Headless JS eval scripts must execute from the requested cwd and restore process cwd/console state afterward.
- dependencies_and_callers: The changed tests exercise `src/workflow/runner.ts`, which calls `runWorkflowScheduler()` from `src/workflow/scheduler.ts`, `executeWorkflowNode()` from `src/workflow/node-runtime.ts`, prompt/resource/model helpers, run-store appenders from `src/workflow/run-store.ts`, and lifecycle functions from `src/workflow/lifecycle.ts`. CLI start in `src/cli/workflow-cli.ts` is the headless caller: it resolves `--cwd`, loads/freeze packages, builds `createSessionWorkflowRuntimeHost()`, passes scheduler and node abort signals into `runWorkflow()`, and reports JSON status/frontier/checkpoints. Related runtime coverage in this directory includes `test/workflow/shell-script-runtime.test.ts`, `test/workflow/node-runtime.test.ts`, `test/workflow/scheduler.test.ts`, and larger slash-command/graph-view checkpoint tests.
- edge_cases_or_failure_modes: Important failure modes are aborts raised after an activation starts but before downstream scheduling, node runtimes that reject with the abort reason, node runtimes that never settle after abort, `maxRuntimeMs` expiring during a running node, missing node abort signal falling back to scheduler signal, and checkpoint creation failing if the lifecycle attempt still has running activations. Cwd-sensitive failures include JS eval reading from the artifact/resource directory instead of the requested workspace, not restoring `process.cwd()` after eval errors, or leaking a mocked `console.log`. Signal listener cleanup is also pinned by CLI tests so SIGINT/SIGTERM handlers do not remain registered after headless start exits.
- validation_or_tests: Inspected current `packages/coding-agent/test` recursively at directory level, with focused reads of `test/workflow/runner.test.ts`, `test/workflow/node-runtime.test.ts`, `test/workflow/shell-script-runtime.test.ts`, and `test/workflow/scheduler.test.ts`, plus changed caller tests in `src/cli/__tests__/workflow-cli.test.ts` and implementation in `src/workflow/runner.ts` / `src/cli/workflow-cli.ts`. The key pinned tests are runner cases for dedicated node abort signals, deadline-aborted lifecycle activations, ignored aborts that still checkpoint, and `maxRuntimeMs` checkpointing; CLI tests pin headless JS cwd execution and SIGINT checkpointing. No source files were edited and no test command was run for this read-only research task.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-134`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
