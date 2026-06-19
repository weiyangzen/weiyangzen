# agent_10 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-010 `file` `Cargo.toml`
- cursor: `[_]`
- core_role: Rust workspace policy surface for `crates/*`, including `pi-iso`, `pi-natives`, and `pi-shell`.
- algorithmic_behavior: Defines resolver `3`, excludes vendored brush crates from workspace traversal, patches `brush-core`/`brush-builtins`, and centralizes release/CI/dev/local profile behavior. Shared dependency versions gate native algorithms for isolation, SIXEL, AST grep, shell minimization, image processing, tokenization, and tree-sitter parsing.
- inputs_outputs_state: Input is Cargo’s workspace graph and selected profile; output is crate resolution, lint levels, optimization/LTO/codegen/debug behavior, and dependency feature sets. State is declarative, not runtime mutable.
- gates_or_invariants: Rust 2024 edition, workspace version `16.0.9`, release panic abort, CI thin LTO, strict Clippy correctness/suspicious denies, and feature-pinned dependencies for NAPI, tree-sitter languages, image formats, shell parsing, and terminal protocols.
- dependencies_and_callers: Consumed by `cargo` and all workspace crates under `crates/*`; related native callers are JS/Bun package bindings through `pi-natives`.
- edge_cases_or_failure_modes: Mis-pinned shared deps can affect every native algorithm; vendored patch paths must exist; profile changes can hide debug info or alter binary size/performance.
- validation_or_tests: Validated indirectly by Cargo builds/tests and crate-level tests such as APFS/SIXEL/minimizer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-040 `directory` `python/omp-rpc`
- cursor: `[_]`
- core_role: Python client SDK for driving the OMP agent as a subprocess over typed JSON-RPC, with host tool and virtual URI extension bridges.
- algorithmic_behavior: `src/omp_rpc/protocol.py` defines typed payloads, literal validators, JSON clone/normalization, and parsers; `client.py` starts the CLI process, tracks pending requests, consumes async events, coordinates prompt lifecycle, terminates process groups, dispatches host tools/URIs, and bounds error history; `host_tools.py` normalizes text/image tool results; `host_uris.py` normalizes custom URI read/write results.
- inputs_outputs_state: Inputs are CLI command, JSON-RPC frames, listener registrations, prompt commands, host tool parameters, and host URI URLs/content. Outputs are parsed events, typed command results, callbacks, tool updates, URI result frames, and subprocess lifecycle errors. State includes pending requests, prompt coordinator, bounded histories, subprocess handle, process-group id, registered host bridges, and cancellation events.
- gates_or_invariants: Validates JSON-serializable objects, string keys, literal enums, unique request matching, non-overlapping prompt collectors, URI content types, host URI schemes, and cancellation before update delivery. `_terminate_process_group` kills descendants so agent-spawned grandchildren do not leak.
- dependencies_and_callers: Python consumers import `omp_rpc`; tests under `python/omp-rpc/tests` cover protocol parsing, host URI behavior, user/group parsing, and client behavior.
- edge_cases_or_failure_modes: RPC timeouts, process exit while pending, unmatched remote errors, listener failures, cancelled host tools/URI reads, unsupported virtual edit flows, and Windows fallback where process groups are unavailable.
- validation_or_tests: `tests/test_protocol.py`, `test_client.py`, `test_host_uris.py`, and `test_user_group.py`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-070 `file` `docs/session-operations-export-share-fork-resume.md`
- cursor: `[_]`
- core_role: Architecture document defining session export, dump, share, fork, resume, continue, and session-switch algorithms.
- algorithmic_behavior: Documents the operation matrix, interactive slash command flows, CLI export, encrypted/default share phases, fork preconditions/session-level flow, resume/continue resolution, runtime cwd mutation, event emissions, cancellation points, and non-persistent session behavior.
- inputs_outputs_state: Inputs include session ids/paths, output paths, clipboard/share handlers, fork/resume CLI flags, current project cwd, session manager, and persisted JSONL. Outputs include HTML/dump/share artifacts, copied clipboard content, forked sessions, selected resumed sessions, runtime cwd/settings/plugin cache changes, and events.
- gates_or_invariants: Guards cross-project fork prompts, unsupported file args in RPC-style modes, non-persistent behaviors, session switching cache resets, and cancellation surfaces.
- dependencies_and_callers: References implementation files in `packages/coding-agent/src/main.ts`, slash commands, export/share modules, session manager/listing, and UI session picker.
- edge_cases_or_failure_modes: Cross-project resume decline, stale cwd-derived plugin/settings caches, share handler fallback, custom tool `onSession` hooks, and cancellation during switch/fork.
- validation_or_tests: Contracts are exercised by session tests under `packages/coding-agent/test/session`, fork/resume tests, and CLI/session manager tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-100 `file` `scripts/fix-changelogs.ts`
- cursor: `[_]`
- core_role: Release workflow script that normalizes package changelogs and protects immutable historical release sections.
- algorithmic_behavior: Parses changelog documents into releases/subsections/items, ensures an Unreleased section, orders subsections, removes unreleased duplicates of released items, reconstructs historical release sections from `refs/clog` when needed, extracts promotable added-item lines from git diff, supports check/write/update modes, and prints fix counters.
- inputs_outputs_state: Inputs are `packages/*/CHANGELOG.md`, git diff/baseline history, CLI mode flags, and optional paths. Outputs are rewritten changelog content, changed summaries, counters, CLI exit status, and diagnostics. State is per-document parse tree plus diff-derived candidate maps.
- gates_or_invariants: Released sections are immutable unless recovered from baseline; subsection order is fixed; duplicate list items are dropped only when semantically identical; malformed headings/items stay in extra lines rather than being silently discarded.
- dependencies_and_callers: Uses Bun shell/glob and `node:path`; called by release automation per repo rules.
- edge_cases_or_failure_modes: Missing `refs/clog`, malformed Markdown, duplicate headings, multi-line list items, added release headings in diffs, no baseline, and check mode detecting but not writing changes.
- validation_or_tests: Validated by release/check scripts and changelog-related package tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-130 `directory` `packages/catalog/test`
- cursor: `[_]`
- core_role: Contract test suite for model catalog identity, provider descriptors, discovery, compatibility, thinking metadata, and generated policy behavior.
- algorithmic_behavior: Recursively covers provider descriptors, model-manager resolution, generated policies, thinking variants, identity family parsing, provider priority, host/base URL behavior, bundled catalogs, discovery null limits, provider-specific regressions, OAuth bundle compatibility, and variant collapse across providers.
- inputs_outputs_state: Inputs are bundled/generated catalog data, synthetic `ModelSpec`s, resolver/descriptors, discovery fixtures, and provider-specific IDs. Outputs are assertions over resolved model specs, limits, wire IDs, thinking configs, provider metadata, aliases, and cache/discovery behavior.
- gates_or_invariants: Catalog imports must come from `@oh-my-pi/pi-catalog/*`; generated JSON is not the direct edit target; provider ids, limits, fallback policies, priority, dialects, and thinking options must remain stable under upstream metadata shifts.
- dependencies_and_callers: Exercises `packages/catalog/src`, provider-model descriptors/resolvers, model-thinking helpers, identity classification, and compatibility builders used by `packages/ai` and `packages/coding-agent`.
- edge_cases_or_failure_modes: Provider upstream changes, duplicate/variant aliases, null limits, incompatible signing requirements, model id affixes, stale generated policies, and provider default drift.
- validation_or_tests: This directory is itself the validation surface; notable files include `model-thinking.test.ts`, `variant-collapse.test.ts`, provider tests, and issue regression tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-160 `directory` `packages/utils/test`
- cursor: `[_]`
- core_role: Utility contract suite for shared formatting, environment, logging, runtime install, stream, path tree, mermaid ASCII rendering, prompt handling, worker host, and tab/spacing support.
- algorithmic_behavior: Tests env parsing, retry fetch, logger serialization/startup, loop phase, install id, ring buffers, path trees, sanitize text, stream reading, CLI help, color formatting, Python gateway dirs, worker host entry semantics, and mermaid-to-ASCII golden output including Unicode/ASCII fixtures.
- inputs_outputs_state: Inputs are synthetic envs, temp dirs, fixture Mermaid graphs, streams, errors, runtime paths, and formatting values. Outputs are normalized strings, logs, diagrams, parsed paths, retries, and worker host dispatch guarantees.
- gates_or_invariants: Tests must not poison global env or Bun state; fixtures define exact ASCII/Unicode diagram output; worker host tests pin single-entry worker contract.
- dependencies_and_callers: Validates `packages/utils/src` plus vendored Mermaid ASCII utilities used by TUI/renderers and worker host logic used by coding-agent CLI workers.
- edge_cases_or_failure_modes: Global env leakage, terminal width/ANSI issues, stream chunk boundaries, Mermaid graph edge cases, and platform-specific path/runtime differences.
- validation_or_tests: All files in `packages/utils/test`, including `mermaid/*`, `worker-host.test.ts`, `stream.test.ts`, `logger-*`, and `spacing.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-190 `file` `docs/tools/github.md`
- cursor: `[_]`
- core_role: Tool contract documentation for the GitHub tool modes.
- algorithmic_behavior: Defines inputs, outputs, flow, modes/variants, side effects, caps, and error surfaces for `repo_view`, `pr_create`, `pr_checkout`, `pr_push`, issue/PR/code/commit/repo search, and workflow run watch.
- inputs_outputs_state: Inputs include mode-specific repo/ref/query/PR/workflow parameters and GitHub auth/context. Outputs include structured tool results, created PRs, checked-out worktrees, pushed branches, search results, and watched run status.
- gates_or_invariants: Mode dispatch must validate required parameters, respect result caps, distinguish side-effecting modes, and surface GitHub API/CLI errors clearly.
- dependencies_and_callers: Documents behavior implemented in coding-agent GitHub tool/CLI integration and consumed by agent tool prompts/renderers.
- edge_cases_or_failure_modes: Missing auth, ambiguous repos, invalid refs/PR numbers, GitHub pagination, search caps, run timeout/failure/cancellation, and checkout path conflicts.
- validation_or_tests: Validated indirectly through GitHub tool tests and tool renderer/CLI behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-220 `file` `scripts/session-stats/harmony_backtest.py`
- cursor: `[_]`
- core_role: Offline analyzer/backtester for detecting structured edit/harmony signals in session statistics databases.
- algorithmic_behavior: Opens SQLite read-only, scans tool and assistant rows, detects marker evidence, parses legacy and current edit boundaries, classifies actions for tools, evaluates text/tool rows, aggregates counters, prints examples, and optionally writes JSON reports.
- inputs_outputs_state: Inputs are SQLite session stats DBs, CLI filters/limits, raw tool argument JSON, assistant text, and tool names. Outputs are `ToolBacktest`/`TextBacktest` records, summaries, examples, counters, and JSON report data.
- gates_or_invariants: Read-only DB URI, complete JSON detection before parsing, fenced-code awareness, marker confidence labels, script mismatch checks, row filters, and bounded examples.
- dependencies_and_callers: Uses Python stdlib `sqlite3`, `argparse`, `json`, regex; supports session-stat research and regression analysis for edit syntax.
- edge_cases_or_failure_modes: Truncated JSON args, loose legacy boundaries, fenced blocks, mixed scripts, missing columns, no primary text extraction, and malformed edit ranges.
- validation_or_tests: Manual research script; validation is by running against real stats DBs and inspecting summaries/reports.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-250 `directory` `packages/coding-agent/src/cli`
- cursor: `[_]`
- core_role: CLI command surface and startup argument routing for the primary coding-agent package.
- algorithmic_behavior: Contains argument parsing/tables, model/config/auth/plugin/setup/stats/workflow/worktree commands, file argument processing, session picking, startup cwd resolution, gallery fixture/rendering, web/search/grep/read/shell helpers, trace capture, update/usage commands, and command-specific validators.
- inputs_outputs_state: Inputs are raw argv, config/settings, cwd/session dirs, env vars, file args, extension flags, and command options. Outputs are parsed `Args`, command executions, startup notices, session selection results, processed prompt/file/image inputs, generated completions, and command-specific stdout/stderr.
- gates_or_invariants: Protocol modes reject `@file`; extension flags are applied before unrecognized flag reporting; startup cwd must be real and scoped; CLI commands avoid corrupting TUI rendering; `startup-cwd.ts` normalizes home/project paths.
- dependencies_and_callers: Called by `packages/coding-agent/src/main.ts` and `cli.ts`; depends on settings, model registry, discovery, session manager, plugin manager, stats, TUI gallery, and Bun shell where applicable.
- edge_cases_or_failure_modes: Ambiguous optional flags, stale extension flags, missing sessions, cross-project resume, startup cwd absent, hidden command selectors, hanging trace commands, and file/image resize failures.
- validation_or_tests: `src/cli/__tests__`, `flag-tables.test.ts`, CLI-specific tests, gallery renderer tests, and root command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-280 `directory` `packages/coding-agent/src/slash-commands`
- cursor: `[_]`
- core_role: Interactive slash-command registry, parsers, builtins, helpers, and marketplace command handling.
- algorithmic_behavior: Resolves available commands, executes builtin/ACP commands, parses command arguments, formats command output, handles active OAuth accounts/logout, MCP helpers, SSH helpers, stats dashboard, todo operations, workflow help, marketplace install parsing, and command metadata types.
- inputs_outputs_state: Inputs are slash text, current session/context/settings, auth storage, MCP/state helpers, and command args. Outputs are command result messages, UI state changes, auth mutations, todo/workflow changes, logout reports, marketplace install actions, and ACP responses.
- gates_or_invariants: Builtin registry controls supported names; parsers enforce command-specific syntax; helpers avoid ambiguous account selection; todo helper uses content-addressed tasks; workflow helper returns known workflow command docs.
- dependencies_and_callers: Used by interactive mode, ACP builtin bridge, `main.ts` startup shortcut path, session/auth/MCP/workflow subsystems.
- edge_cases_or_failure_modes: Unknown command, malformed marketplace source, missing OAuth identity, no MCP server configured, logout of inactive accounts, and ambiguous task content.
- validation_or_tests: `helpers/workflow-help.test.ts`, `acp-builtins.test.ts`, custom command review tests, and slash command integration tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-310 `directory` `packages/coding-agent/test/session`
- cursor: `[_]`
- core_role: Session persistence/lifecycle contract tests for blob stores, emit isolation, Redis/SQL storage, fork/status/history/dump formats, thinking display, and yield queues.
- algorithmic_behavior: Exercises storage managers, file/SQL/Redis backends, session initialization/peek, dump/history formatting, fork semantics, event listener isolation, thinking block display, and queued yield behavior.
- inputs_outputs_state: Inputs are temp session stores, synthetic messages/usages, Redis/SQL adapters, and session entries. Outputs are persisted/reloaded sessions, statuses, dumps, histories, forked sessions, event emissions, and queue state.
- gates_or_invariants: Storage backends must preserve ordering/metadata, fork copies expected state, emit listeners isolate failures, status reflects lifecycle accurately, and migrations keep old sessions loadable.
- dependencies_and_callers: Tests `session-manager`, `session-storage`, SQL/Redis storage, history/dump formatters, and session entry migration code.
- edge_cases_or_failure_modes: Missing blobs, duplicate listeners, storage backend availability, stale session ids, migration boundaries, and cross-backend serialization differences.
- validation_or_tests: All files under `packages/coding-agent/test/session`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-340 `file` `crates/pi-iso/src/apfs.rs`
- cursor: `[_]`
- core_role: macOS APFS clonefile isolation backend.
- algorithmic_behavior: Implements `IsolationBackend` for APFS: `probe()` is available only on macOS, `start()` canonicalizes an existing source dir, creates destination parent, removes stale destination, calls `libc::clonefile`, maps unsupported volume errors to unavailable, and `stop()` recursively removes the cloned tree.
- inputs_outputs_state: Inputs are lower/source path and merged/destination path. Outputs are cloned copy-on-write directory tree or `IsoError`; stop outputs cleanup success/error. State is filesystem tree only.
- gates_or_invariants: Source must exist and be a directory; destination is never overwritten without removal; paths must not contain NUL bytes; non-macOS start returns unavailable while stop is a no-op success.
- dependencies_and_callers: Uses `libc::clonefile`, `std::fs`, and crate traits `IsolationBackend`, `IsoError`, `ProbeResult`.
- edge_cases_or_failure_modes: Non-APFS/unsupported volume (`ENOTSUP`, `EOPNOTSUPP`, `EXDEV`), non-dir source, parent creation failure, stale destination removal failure, and NUL path bytes.
- validation_or_tests: Covered by crate isolation backend tests/builds and platform-specific smoke usage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-370 `file` `crates/pi-natives/src/sixel.rs`
- cursor: `[_]`
- core_role: NAPI native function for terminal SIXEL image encoding.
- algorithmic_behavior: `encode_sixel` validates nonzero dimensions, decodes image bytes with guessed format, resizes with Lanczos3 when needed, converts to RGBA, then encodes with `icy_sixel::sixel_encode`.
- inputs_outputs_state: Inputs are encoded image bytes plus target width/height. Output is a SIXEL escape sequence string or NAPI error. State is transient decoded/resized image buffer.
- gates_or_invariants: Width and height must be greater than zero; input must be decodable as supported image format; encoder failures become explicit error reasons.
- dependencies_and_callers: Depends on `image`, `icy_sixel`, NAPI bindings; called by TUI/native image rendering paths.
- edge_cases_or_failure_modes: Unknown image format, corrupted image bytes, zero dimensions, resize/encode failure, and large image memory pressure.
- validation_or_tests: `packages/tui/test/sixel-probe.test.ts` and native build/tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-400 `file` `packages/agent/test/compaction-error-status.test.ts`
- cursor: `[_]`
- core_role: Regression tests for propagating compaction model error status into agent compaction outcomes.
- algorithmic_behavior: Builds assistant stop/error messages and compaction preparations, spies AI stream behavior, and asserts compaction failures preserve relevant status/message instead of flattening all failures.
- inputs_outputs_state: Inputs are synthetic `AgentMessage`s, mocked assistant messages with error status, and compaction preparations. Outputs are asserted compaction results/error metadata.
- gates_or_invariants: Error status must survive through handoff/compaction layers; normal assistant stop content remains success path.
- dependencies_and_callers: Exercises `@oh-my-pi/pi-agent-core` compaction APIs and `@oh-my-pi/pi-ai` stream behavior.
- edge_cases_or_failure_modes: Missing status, undefined error status, handoff messages around compaction, and provider-specific error message mapping.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-430 `file` `packages/ai/test/abort-source-tracker.test.ts`
- cursor: `[_]`
- core_role: Tests abort source attribution helper.
- algorithmic_behavior: Creates abort source tracker, aborts different controller/signal combinations, and asserts source classification reflects the first/expected abort path.
- inputs_outputs_state: Inputs are `AbortSignal`s and abort actions. Outputs are tracked source labels/state.
- gates_or_invariants: Aborted state must be deterministic; pre-aborted and later-aborted signals should not lose attribution.
- dependencies_and_callers: Exercises `createAbortSourceTracker` in AI utility abort handling used by stream providers.
- edge_cases_or_failure_modes: Multiple abort sources, already-aborted signals, and listener cleanup.
- validation_or_tests: This test file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-460 `file` `packages/ai/test/auth-gateway-anthropic-caching.test.ts`
- cursor: `[_]`
- core_role: E2E-style contract for Anthropic auth-gateway prompt/cache behavior.
- algorithmic_behavior: Checks gateway availability, sends Anthropic-style requests with repeated large system text, extracts assistant text/usage, and verifies caching/accounting behavior through the gateway.
- inputs_outputs_state: Inputs are auth gateway URL/env model, Anthropic request body, and message blocks. Outputs are Anthropic responses and usage fields.
- gates_or_invariants: Skips/guards when gateway unavailable; response text extraction must find assistant text; cache usage should reflect repeated system material.
- dependencies_and_callers: Uses auth-gateway E2E helper and Anthropic-compatible gateway server.
- edge_cases_or_failure_modes: Missing gateway, unavailable credentials, usage shape drift, streaming/non-streaming response differences, and provider rate limits.
- validation_or_tests: This file; environment-gated E2E.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-490 `file` `packages/ai/test/azure-openai-responses-stream.test.ts`
- cursor: `[_]`
- core_role: Tests Azure OpenAI Responses streaming conversion.
- algorithmic_behavior: Builds Azure model fixtures, mock SSE responses, assistant messages, and fetch stubs; verifies stream events, signatures, tool handling, and abort behavior for `azure-openai-responses`.
- inputs_outputs_state: Inputs are SSE event arrays, mock fetch responses, model spec, context/tools, and abort signals. Outputs are assistant events/messages and captured request behavior.
- gates_or_invariants: SSE parsing must preserve text/signatures, honor aborts, and shape Azure request/response compatibility.
- dependencies_and_callers: Exercises AI provider stream implementation for Azure Responses API.
- edge_cases_or_failure_modes: Malformed SSE, missing signature, aborted signal, tool event ordering, and provider-specific model specs.
- validation_or_tests: This test file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-520 `file` `packages/ai/test/google-oauth-validation-url.test.ts`
- cursor: `[_]`
- core_role: Tests Google OAuth validation URL extraction and account verification flow.
- algorithmic_behavior: Parses validation URL from Google HTML/JSON-ish response bodies, stubs token/userinfo endpoints, and verifies `GoogleOAuthFlow` surfaces account verification requirements correctly.
- inputs_outputs_state: Inputs are validation response bodies, OAuth flow config, token/userinfo stubs, and controller callbacks. Outputs are extracted URL, credentials, or verification errors.
- gates_or_invariants: Validation URL extraction must tolerate embedded JSON; token and userinfo account identity must match expected project/account flow.
- dependencies_and_callers: Exercises `GoogleOAuthFlow` and `extractGoogleValidationUrl`.
- edge_cases_or_failure_modes: Missing validation URL, unexpected response shapes, email mismatch, failed token/userinfo requests.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-550 `file` `packages/ai/test/issue-945-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for OpenCode Go `tool_choice` compatibility.
- algorithmic_behavior: Uses a bundled OpenAI-compatible model, synthetic echo tool, and mocked stream call to verify request shaping does not send incompatible tool choice fields.
- inputs_outputs_state: Inputs are context, tool schema, model, and aborted signal helper. Outputs are captured request compatibility assertions.
- gates_or_invariants: Tool schema and `tool_choice` handling must match OpenCode Go expectations.
- dependencies_and_callers: Exercises `streamOpenAICompletions`.
- edge_cases_or_failure_modes: Strict tool schemas, provider dialect deviations, and aborted request path.
- validation_or_tests: This regression file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-580 `file` `packages/ai/test/openai-codex.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI Codex OAuth headers, tool schema conversion, request transformation, orphan tool repair, reasoning effort validation, and error parsing.
- algorithmic_behavior: Builds Codex models, transforms request bodies, converts tools, validates header constants, parses `CodexApiError`, and asserts repair logic for tool calls/results.
- inputs_outputs_state: Inputs are tools, request bodies, Codex model fixtures, headers, and error payloads. Outputs are transformed request JSON, converted tool schemas, repaired messages, and parsed errors.
- gates_or_invariants: Codex headers must be exact, reasoning efforts constrained, orphan tool-call repair deterministic, and errors preserve status/details.
- dependencies_and_callers: Exercises `providers/openai-codex/*`, `openai-codex-responses`, and catalog wire constants.
- edge_cases_or_failure_modes: Invalid reasoning effort, missing tool results, malformed error bodies, custom tool schemas, and OAuth header drift.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-610 `file` `packages/ai/test/parse-streaming-json-throttled.test.ts`
- cursor: `[_]`
- core_role: Tests throttled streaming JSON parser behavior.
- algorithmic_behavior: Feeds partial JSON chunks through throttled parsing utilities and asserts update coalescing/parse boundaries.
- inputs_outputs_state: Inputs are streaming text chunks and throttle behavior. Outputs are parsed partial/final JSON states and callback counts.
- gates_or_invariants: Parser must not emit invalid object states as complete; throttling must preserve final value.
- dependencies_and_callers: Exercises AI streaming JSON utility used for tool-call previews.
- edge_cases_or_failure_modes: Chunk boundaries inside strings/objects, delayed final parse, and malformed partial payloads.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-640 `file` `packages/ai/test/tool-examples.test.ts`
- cursor: `[_]`
- core_role: Tests rendering of in-band tool examples for model dialect prompts.
- algorithmic_behavior: Builds `InbandTool` examples and asserts `renderToolExamples` emits expected semantic content/format.
- inputs_outputs_state: Inputs are tool definitions/examples. Output is rendered prompt/example text.
- gates_or_invariants: Tool examples must be stable and include tool names/arguments without malformed serialization.
- dependencies_and_callers: Exercises `src/dialect/examples` and `src/dialect/types`.
- edge_cases_or_failure_modes: Missing examples, special JSON values, and formatting drift consumed by prompts.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-670 `file` `packages/catalog/test/anthropic-copilot-signing-compat.test.ts`
- cursor: `[_]`
- core_role: Regression test that GitHub Copilot Anthropic-compatible endpoints are treated as signing endpoints.
- algorithmic_behavior: Builds Anthropic-compatible model specs and asserts `buildAnthropicCompat` sets Copilot signing compatibility.
- inputs_outputs_state: Inputs are provider/model spec overrides. Outputs are compat config assertions.
- gates_or_invariants: GitHub Copilot must not be treated like a generic Anthropic endpoint when request signing is required.
- dependencies_and_callers: Exercises `packages/catalog/src/compat/anthropic`.
- edge_cases_or_failure_modes: Provider id drift and compat flags missing for Copilot.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-700 `file` `packages/catalog/test/model-thinking.test.ts`
- cursor: `[_]`
- core_role: Core model-thinking derivation/runtime helper test suite.
- algorithmic_behavior: Builds model fixtures and asserts thinking config derivation, supported effort sets, wire model id resolution, generated policy application, runtime helpers, and variant behavior.
- inputs_outputs_state: Inputs are `ModelSpec`s, provider ids, efforts, and thinking metadata. Outputs are normalized thinking configs, supported efforts, wire model ids, and policy-modified models.
- gates_or_invariants: Thinking support must be inferred consistently across providers; unsupported efforts rejected/fallback; wire ids must match variant policies.
- dependencies_and_callers: Exercises `@oh-my-pi/pi-catalog/model-thinking`, `effort`, and build helpers used by AI/coding-agent model selection.
- edge_cases_or_failure_modes: Provider-specific reasoning variants, xhigh support, unknown models, generated policy drift, and alias collapse.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-730 `file` `packages/coding-agent/src/main.ts`
- cursor: `[_]`
- core_role: Main coding-agent startup orchestrator for CLI, interactive, print, RPC, and ACP modes.
- algorithmic_behavior: Initializes logging/theme/startup cwd, auth storage, model registry, settings, plugin roots, extension flags, model scopes, session manager, telemetry, session options, file/stdin processing, create-session flow, background model refresh, RPC/ACP/interactive/print dispatch, session picker/resume/fork handling, startup watchdog, and clean shutdown.
- inputs_outputs_state: Inputs are parsed/raw args, env vars, cwd/config files, auth storage, model registry, session files, plugin dirs, stdin/file args, and dependencies. Outputs are sessions, TUI/print/RPC/ACP execution, startup notices, process exits, notifications, model fallback messages, and persisted lifecycle hooks.
- gates_or_invariants: Protocol modes own stdin and reject file args; `--api-key` requires a selected model; unrecognized extension-aware flags exit with usage error; cross-project resume resets project dir/plugin/settings caches; non-interactive no-model exits with setup guidance.
- dependencies_and_callers: Called by `cli.ts` through `main(args)`; coordinates `Settings`, `ModelRegistry`, discovery, `SessionManager`, `createAgentSession`, interactive/print/RPC/ACP modes, plugin marketplace updates, and telemetry.
- edge_cases_or_failure_modes: Startup hangs, stale plugin roots after cwd switch, declined cross-project resume, missing model/auth, bad export path, malformed extension flags, session resolution errors, and mode-specific stdin conflicts.
- validation_or_tests: CLI/root command tests including `cli-max-time-flag.test.ts`, ACP/MCP/session tests, setup wizard tests, and print/interactive integration tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-760 `file` `packages/coding-agent/test/agent-session-context-promotion.test.ts`
- cursor: `[_]`
- core_role: Tests AgentSession context promotion behavior when provider/model state changes.
- algorithmic_behavior: Builds sessions with mock agent/model registry/auth storage and asserts provider session state/context is promoted or retained across model transitions.
- inputs_outputs_state: Inputs are synthetic assistant messages, provider session state, bundled models, temp dirs, and session manager. Outputs are session context/state assertions.
- gates_or_invariants: Context promotion must not lose provider state; model transitions must preserve compatible state and avoid inappropriate promotion.
- dependencies_and_callers: Exercises `AgentSession`, `ModelRegistry`, `SessionManager`, and `AuthStorage`.
- edge_cases_or_failure_modes: Missing provider state, incompatible model/provider, resumed sessions, and cleanup of temp dirs.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-790 `file` `packages/coding-agent/test/agent-session-user-shortcut-hooks.test.ts`
- cursor: `[_]`
- core_role: Tests user shortcut hooks for AgentSession command interception.
- algorithmic_behavior: Spies Python and bash executors/extensions, creates sessions, and asserts shortcuts route to the expected execution path without normal model turn leakage.
- inputs_outputs_state: Inputs are user shortcut messages, session fixtures, extension runner stubs, and executor spies. Outputs are invoked hooks/executors and session events.
- gates_or_invariants: Shortcut hooks must run before normal agent loop; disabled/unknown shortcuts must not trigger; hooks must clean up.
- dependencies_and_callers: Exercises `AgentSession`, bash executor, Python executor, extension runner.
- edge_cases_or_failure_modes: Hook errors, overlapping shortcuts, executor cancellation, and temp session isolation.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-820 `file` `packages/coding-agent/test/cli-max-time-flag.test.ts`
- cursor: `[_]`
- core_role: Tests CLI `--max-time` parsing and propagation to session creation.
- algorithmic_behavior: Parses args, invokes `runRootCommand` with injected session dependencies, and asserts max-time flag becomes create-session option.
- inputs_outputs_state: Inputs are CLI args and temp settings/auth state. Outputs are parsed args and captured `CreateAgentSessionOptions`.
- gates_or_invariants: `--max-time` must parse as intended and not be treated as prompt text or unknown flag.
- dependencies_and_callers: Exercises `cli/args` and `main.runRootCommand`.
- edge_cases_or_failure_modes: Missing value, interaction with print/interactive modes, and cleanup of temp dirs.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-850 `file` `packages/coding-agent/test/event-controller-abort-render.test.ts`
- cursor: `[_]`
- core_role: Tests abort labeling/render behavior in the interactive event controller.
- algorithmic_behavior: Builds assistant message fixtures, synthetic interactive context, and event controller events; asserts silent/user-interrupt abort labels render correctly.
- inputs_outputs_state: Inputs are assistant messages with abort/error metadata and settings. Outputs are rendered components/messages and labels.
- gates_or_invariants: Silent abort markers should suppress noisy labels; user interrupts should show user-facing label; settings reset after tests.
- dependencies_and_callers: Exercises `EventController`, session message helpers, and settings/theme behavior.
- edge_cases_or_failure_modes: Missing abort reason, silent marker, explicit user interrupt label, and message-end ordering.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-880 `file` `packages/coding-agent/test/image-b64poly.test.ts`
- cursor: `[_]`
- core_role: Minimal test for `Buffer.toBase64` availability/polyfill behavior.
- algorithmic_behavior: Asserts base64 conversion on Buffer works in the runtime.
- inputs_outputs_state: Input is Buffer data; output is base64 string.
- gates_or_invariants: Runtime image/base64 helpers need a stable Buffer base64 method.
- dependencies_and_callers: Supports image handling tests/tools.
- edge_cases_or_failure_modes: Runtime missing polyfill/API.
- validation_or_tests: This file.
- skip_candidate: `yes: tiny runtime-compat smoke rather than a core algorithm itself`

### OH_MY_HUMANIZE_MAIN-HZ-910 `file` `packages/coding-agent/test/issue-1215-legacy-pi-ai-import.test.ts`
- cursor: `[_]`
- core_role: Regression test for extension loading when legacy `@mariozechner/pi-ai` import resolution fails.
- algorithmic_behavior: Creates temp extension/tool fixture, loads extensions, and asserts legacy import compatibility survives `getResolvedSpecifier` failure.
- inputs_outputs_state: Inputs are temp plugin files and extension loader. Outputs are loaded extension/tool registrations.
- gates_or_invariants: Legacy plugin imports must remain compatible; loader should not crash on resolver failure.
- dependencies_and_callers: Exercises extensibility extension loader.
- edge_cases_or_failure_modes: Missing legacy package, resolver failure, stale tool name, and temp cleanup.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-940 `file` `packages/coding-agent/test/job-poll-displacement.test.ts`
- cursor: `[_]`
- core_role: Tests lifecycle of waiting-poll tool blocks and EventController displacement.
- algorithmic_behavior: Creates `ToolExecutionComponent`s with polling statuses and asserts consecutive waiting polls are displaced/updated rather than accumulating stale UI blocks.
- inputs_outputs_state: Inputs are job status sequences, fake TUI/context, and tool execution events. Outputs are component state/render lifecycle assertions.
- gates_or_invariants: Running/completed/failed/cancelled status transitions must map to stable UI; consecutive polls should displace correctly.
- dependencies_and_callers: Exercises `ToolExecutionComponent` and `EventController`.
- edge_cases_or_failure_modes: Cancelled/error statuses, multiple consecutive polls, and render request timing.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-970 `file` `packages/coding-agent/test/mcp-startup-no-block.test.ts`
- cursor: `[_]`
- core_role: Regression test that MCP startup does not block on a server hanging during initialization.
- algorithmic_behavior: Starts `MCPManager` with fixture server that hangs during init and asserts startup proceeds/non-blocking behavior.
- inputs_outputs_state: Inputs are MCP stdio server config and hanging Bun fixture. Outputs are manager startup state and timeout-safe assertions.
- gates_or_invariants: MCP manager must isolate slow/hung servers and avoid blocking agent startup.
- dependencies_and_callers: Exercises `src/mcp/manager` and MCP stdio transport.
- edge_cases_or_failure_modes: Hung child process, startup timeout, process cleanup, and stdio pipe backpressure.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1000 `file` `packages/coding-agent/test/plugin-install-git.test.ts`
- cursor: `[_]`
- core_role: Tests plugin manager install behavior for git sources.
- algorithmic_behavior: Stubs Bun subprocess/streams and utility path lookups, runs `PluginManager.install`, and asserts git source classification/install behavior.
- inputs_outputs_state: Inputs are package/git source strings, temp plugin dirs, mocked subprocess results. Outputs are installed plugin metadata and filesystem state assertions.
- gates_or_invariants: Git sources must be cloned/handled distinctly from npm package names; failed subprocesses must surface errors; install path must be safe.
- dependencies_and_callers: Exercises extensibility plugin manager and pi-utils helpers.
- edge_cases_or_failure_modes: Empty streams, git failures, invalid package/source names, and cleanup.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1030 `file` `packages/coding-agent/test/sdk-autolearn-active-tools.test.ts`
- cursor: `[_]`
- core_role: Tests SDK session creation activates auto-learn tools correctly.
- algorithmic_behavior: Creates agent sessions with temp settings/model registry/auth storage and asserts active tool list includes/excludes auto-learn tool behavior.
- inputs_outputs_state: Inputs are session creation options, model, temp agent dir. Outputs are `AgentSession` tool activation state.
- gates_or_invariants: SDK-created sessions must honor auto-learn active tool semantics, not just CLI sessions.
- dependencies_and_callers: Exercises `createAgentSession`, `ModelRegistry`, `Settings`, `SessionManager`.
- edge_cases_or_failure_modes: Missing settings, cleanup of long-lived session, and tool discovery timing.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1060 `file` `packages/coding-agent/test/setup-wizard.test.ts`
- cursor: `[_]`
- core_role: Setup wizard scene selection, persistence, mouse routing, theme/glyph/web-search, and onboarding trigger test suite.
- algorithmic_behavior: Builds fake interactive contexts/scenes, drives `SetupWizardComponent`, tests version/minVersion scene gating, persisted setup version, mouse events, preview renderers, glyph preset selection, web search provider preferences, and `runOnboardingSetup`.
- inputs_outputs_state: Inputs are settings, fake context, scene controllers, mouse/key events, search provider options. Outputs are wizard state, persisted settings, rendered previews, and setup trigger decisions.
- gates_or_invariants: Scenes run only when version/shouldRun permits; setup completion persists; mouse/key routing goes to active scene; theme/glyph settings mutate correctly.
- dependencies_and_callers: Exercises setup command, wizard overlay, setup scenes, theme, web search types/settings.
- edge_cases_or_failure_modes: Skipped scenes, scene errors, stale setup version, narrow render widths, and provider preference defaults.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1090 `file` `packages/coding-agent/test/subagent-hud-render.test.ts`
- cursor: `[_]`
- core_role: Tests subagent HUD line rendering.
- algorithmic_behavior: Builds observable session/progress/lifecycle payloads and asserts `renderSubagentHudLines` formats active/detached progress within terminal columns.
- inputs_outputs_state: Inputs are sessions, progress payloads, lifecycle metadata, columns, and theme. Outputs are HUD string lines.
- gates_or_invariants: Detached and active agents must display distinctly; long descriptions must fit columns; lifecycle/progress ordering stable.
- dependencies_and_callers: Exercises interactive mode HUD rendering and event bus types.
- edge_cases_or_failure_modes: Narrow columns, missing progress, multiple sessions, and detached agents.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1120 `file` `packages/coding-agent/test/utilities.ts`
- cursor: `[_]`
- core_role: Shared test utilities for constructing coding-agent sessions/tools.
- algorithmic_behavior: Creates temp directories, auth/model/settings/session managers, bundled model sessions, tool sessions, and E2E key helpers for tests.
- inputs_outputs_state: Inputs are model/session options and temp dirs. Outputs are configured `AgentSession`, `ToolSession`, `ModelRegistry`, and cleanup handles.
- gates_or_invariants: Tests receive isolated Snowflake/session ids and temp state; E2E keys resolved consistently.
- dependencies_and_callers: Imported by coding-agent tests needing realistic session/tool setup.
- edge_cases_or_failure_modes: Missing E2E keys, temp cleanup, session disposal, and auth/model initialization.
- validation_or_tests: Indirectly validated by dependent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1150 `file` `packages/hashline/src/messages.ts`
- cursor: `[_]`
- core_role: Central message/diagnostic formatter for hashline edit patch failures and warnings.
- algorithmic_behavior: Formats anchored mismatch context, block unresolved messages, duplicate/coalesced swap warnings, empty body/delete/insert diagnostics, landing-shift warnings, recovery warnings, missing snapshot tag messages, unseen lines, and block single-line guidance.
- inputs_outputs_state: Inputs are anchor lines, file lines, section paths, line ranges, block ops, and resolver state. Outputs are deterministic human-readable diagnostics/warnings.
- gates_or_invariants: Messages encode edit grammar rules: swap needs added body, delete takes no body, block ops require resolvable blocks, line ranges compact, and warnings preserve actionable context.
- dependencies_and_callers: Used by hashline parser/executor and coding-agent edit tool rendering.
- edge_cases_or_failure_modes: Unseen lines, unresolved blocks, body rows on delete, repeated hunks targeting same range, snapshot drift, and external recovery.
- validation_or_tests: Hashline/edit tests and edit tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1180 `file` `packages/mnemopi/test/annotations.test.ts`
- cursor: `[_]`
- core_role: Tests persistent annotation store behavior for mnemopi.
- algorithmic_behavior: Creates temp DBs, opens annotation store, creates/updates/queries annotations and links, and asserts persistence/cleanup.
- inputs_outputs_state: Inputs are temp SQLite paths and annotation data. Outputs are stored annotation rows and query results.
- gates_or_invariants: Annotation ids, metadata, and link behavior must round-trip through DB.
- dependencies_and_callers: Exercises mnemopi annotation store and DB opener.
- edge_cases_or_failure_modes: Temp DB cleanup, duplicate annotations, missing links, and afterEach cleanup.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1210 `file` `packages/mnemopi/test/graph-tools.test.ts`
- cursor: `[_]`
- core_role: Tests episodic graph CRUD, traversal, scoring, and proactive links.
- algorithmic_behavior: Opens in-memory graph DB, inserts graph edges/nodes, traverses links, scores relationships, and validates proactive-link ranking.
- inputs_outputs_state: Inputs are `GraphEdge` fixtures and DB operations. Outputs are graph query/traversal/scoring results.
- gates_or_invariants: Edge weights/types and traversal semantics must be stable; graph close is quiet.
- dependencies_and_callers: Exercises `EpisodicGraph` and mnemopi DB.
- edge_cases_or_failure_modes: Missing nodes, duplicate edges, scoring ties, and DB cleanup.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1240 `file` `packages/mnemopi/test/text-utilities.test.ts`
- cursor: `[_]`
- core_role: Tests token/cost/chat normalization utilities.
- algorithmic_behavior: Verifies token estimation, cost logging/stat aggregation, chat normalization, batch normalization, and extraction-rate computation.
- inputs_outputs_state: Inputs are text/chat fixtures, temp cost logs, and token/cost values. Outputs are normalized messages, cost stats, token estimates, and extraction metrics.
- gates_or_invariants: Cost logs must aggregate accurately; chat normalization must preserve semantic text while normalizing shape.
- dependencies_and_callers: Exercises mnemopi core utilities.
- edge_cases_or_failure_modes: Empty messages, temp file cleanup, mixed chat formats, and cost precision.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1270 `file` `packages/snapcompact/research/diag_kimi_forensics.py`
- cursor: `[_]`
- core_role: Research diagnostic for Kimi/Snapcompact forensic analysis.
- algorithmic_behavior: Loads research helpers, reads/compares model output artifacts, and prints forensic diagnostics around Kimi behavior.
- inputs_outputs_state: Inputs are local research data/files and CLI args. Outputs are printed diagnostic summaries.
- gates_or_invariants: Requires research helper import path and expected artifact shapes.
- dependencies_and_callers: Uses `squad` research module and Python stdlib.
- edge_cases_or_failure_modes: Missing artifacts, missing API/research helper path, malformed JSON.
- validation_or_tests: Manual research script, not automated.
- skip_candidate: `yes: research diagnostic script, not product runtime path`

### OH_MY_HUMANIZE_MAIN-HZ-1300 `file` `packages/snapcompact/research/providers.py`
- cursor: `[_]`
- core_role: Provider-call helper layer for Snapcompact research experiments.
- algorithmic_behavior: Encodes images/base64, builds provider requests, performs HTTP calls with retries/timing, parses JSON responses, and normalizes provider outputs/usage for experiments.
- inputs_outputs_state: Inputs are provider keys, messages, image paths/bytes, model names, and request params. Outputs are provider response dicts, usage/cost fields, and error reports.
- gates_or_invariants: Requires API keys, handles HTTP errors, and keeps provider-specific wire formats isolated from experiment scripts.
- dependencies_and_callers: Used by multiple `packages/snapcompact/research/*.py` experiments.
- edge_cases_or_failure_modes: Rate limits, HTTP failures, invalid JSON, missing keys, image encoding failures, and provider schema drift.
- validation_or_tests: Manual research execution.
- skip_candidate: `yes: research support code, not shipped runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1330 `file` `packages/snapcompact/research/snapcompact_viz_atlas.py`
- cursor: `[_]`
- core_role: Visualization generator for Snapcompact atlas research results.
- algorithmic_behavior: Reads CSV/JSON experiment outputs, uses NumPy/Matplotlib to compute visual layouts/metrics, and renders atlas-style plots.
- inputs_outputs_state: Inputs are experiment result files and CLI options. Outputs are image/plot artifacts.
- gates_or_invariants: Data columns/shapes must match expected experiment schema; output dirs must be writable.
- dependencies_and_callers: Uses Matplotlib, NumPy, CSV/JSON; called manually in research workflows.
- edge_cases_or_failure_modes: Missing fonts/data, bad numeric values, empty result sets, and plot sizing.
- validation_or_tests: Manual visual inspection.
- skip_candidate: `yes: research visualization, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1360 `file` `packages/stats/test/user-metrics.test.ts`
- cursor: `[_]`
- core_role: Tests user-message metrics computation.
- algorithmic_behavior: Calls `computeUserMessageMetrics` with message fixtures and asserts empty/default and aggregate metrics.
- inputs_outputs_state: Inputs are user message text/events. Outputs are `EMPTY_USER_METRICS` or computed metrics.
- gates_or_invariants: Empty input returns stable empty metrics; computed counts/rates must remain deterministic.
- dependencies_and_callers: Exercises `@oh-my-pi/omp-stats/user-metrics`.
- edge_cases_or_failure_modes: Empty messages, mixed message types, and metric division by zero.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1390 `file` `packages/tui/test/autocomplete.test.ts`
- cursor: `[_]`
- core_role: Tests combined autocomplete provider and slash completion sync.
- algorithmic_behavior: Builds temp filesystem/options providers, requests completions, verifies merge/order/filter behavior, and tests synchronous slash completion helper.
- inputs_outputs_state: Inputs are typed prefixes, temp dirs/files, completion providers. Outputs are completion lists and selected suggestions.
- gates_or_invariants: Completion ordering/filtering must be stable; provider failures must not poison other providers; slash completions must remain synchronous where required.
- dependencies_and_callers: Exercises `@oh-my-pi/pi-tui/autocomplete`.
- edge_cases_or_failure_modes: Hidden files, path separators, duplicate completions, provider errors, and cleanup.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1420 `file` `packages/tui/test/latex-block.test.ts`
- cursor: `[_]`
- core_role: Tests LaTeX-to-terminal block rendering for stacked display fractions.
- algorithmic_behavior: Toggles terminal true-color capability, renders LaTeX fractions, strips VT controls where needed, and asserts terminal block output semantics.
- inputs_outputs_state: Inputs are LaTeX strings and terminal capability flags. Outputs are rendered block strings.
- gates_or_invariants: Fraction layout must remain legible and deterministic across color modes.
- dependencies_and_callers: Exercises `latexToBlock` and terminal capability module.
- edge_cases_or_failure_modes: No true-color, nested/stacked fractions, ANSI stripping.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1450 `file` `packages/tui/test/sixel-probe.test.ts`
- cursor: `[_]`
- core_role: Tests TUI SIXEL capability probing.
- algorithmic_behavior: Mutates terminal info/env/TTY descriptors in a controlled way, uses virtual terminal, and asserts image protocol selection/probe behavior.
- inputs_outputs_state: Inputs are env vars, TTY flags, terminal image protocol settings. Outputs are detected protocol/capability state.
- gates_or_invariants: Probe must restore globals after each test; Windows Terminal/session cases and non-TTY must be handled.
- dependencies_and_callers: Exercises `TERMINAL`, `TUI`, and image protocol controls.
- edge_cases_or_failure_modes: Global terminal state leakage, non-TTY stdio, preconfigured protocol, WT_SESSION override.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1480 `file` `packages/typescript-edit-benchmark/test/verify.test.ts`
- cursor: `[_]`
- core_role: Tests benchmark expected-file verifier.
- algorithmic_behavior: Creates temp expected/actual files, runs `verifyExpectedFiles`, and asserts matching/missing/different file behavior.
- inputs_outputs_state: Inputs are temp filesystem trees and expected file definitions. Outputs are verification result/errors.
- gates_or_invariants: Verifier must detect byte/semantic mismatches and missing files deterministically.
- dependencies_and_callers: Exercises `@oh-my-pi/typescript-edit-benchmark/verify`.
- edge_cases_or_failure_modes: Missing directories, path normalization, multiple mismatches, and temp cleanup.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1510 `file` `packages/utils/src/tab-spacing.ts`
- cursor: `[_]`
- core_role: Shared indentation/tab-width resolver with `.editorconfig` support.
- algorithmic_behavior: Parses `.editorconfig`, matches glob sections, walks parent chains with root cutoff, caches parsed files/chains/indentation, resolves indent style/size/tab width, detects overlong path components, and exposes default tab width/formatting APIs.
- inputs_outputs_state: Inputs are file path, project dir, `.editorconfig` contents, default width. Outputs are numeric indentation and formatting options (`tabSize`, `insertSpaces`, trim/final newline settings). State is module-level caches and default width.
- gates_or_invariants: Tab width clamped between 1 and 16; invalid positive integers ignored; path components over 255 bytes avoid filesystem probes; editorconfig glob braces repaired; missing files degrade to default.
- dependencies_and_callers: Used by LSP format options and rendering/edit utilities; depends on `node:fs`, `node:path`, `isFsError`.
- edge_cases_or_failure_modes: Invalid `.editorconfig`, unclosed braces, relative/absolute path resolution, Windows separators, root boundaries, overlong paths, and cache staleness.
- validation_or_tests: `packages/utils/test/spacing.test.ts` and LSP format tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1540 `file` `packages/wire/test/constants.test.ts`
- cursor: `[_]`
- core_role: Tests collab wire protocol constants.
- algorithmic_behavior: Imports wire constants and asserts exported values remain stable.
- inputs_outputs_state: Inputs are constants. Outputs are equality assertions.
- gates_or_invariants: Protocol constant drift is caught before client/server mismatch.
- dependencies_and_callers: Exercises `packages/wire` constants used by collab packages.
- edge_cases_or_failure_modes: Accidental rename/value change.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1570 `file` `python/robomp/src/slot_pool.py`
- cursor: `[_]`
- core_role: Async slot allocator for robomp workers.
- algorithmic_behavior: Initializes unique slot IDs into an `asyncio.Queue`; `acquire()` returns `None` when no fixed slots exist or waits for an available slot; `release()` validates checkout ownership before returning slot to queue.
- inputs_outputs_state: Inputs are iterable slot UIDs and release UID. Outputs are acquired UID/`None` and queue state. State includes tuple of slots, available queue, checked-out set.
- gates_or_invariants: Slot UIDs must be unique; only acquired slots may be released; `None` release is valid only for empty pool mode.
- dependencies_and_callers: Used by Python robomp scheduler/server logic needing bounded slot concurrency.
- edge_cases_or_failure_modes: Duplicate slot IDs, releasing unknown slot, acquiring from empty fixed pool, and leaked checked-out slots.
- validation_or_tests: Covered by robomp tests/manual workflows.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1600 `directory` `packages/ai/src/registry/oauth`
- cursor: `[_]`
- core_role: OAuth provider registry implementations and shared OAuth flow primitives for AI providers.
- algorithmic_behavior: Contains provider login/refresh controllers for Anthropic, GitHub Copilot, GitLab Duo, Google Gemini CLI/Antigravity, Kimi, MiniMax, OpenAI Codex, opencode, Perplexity, Wafer, xAI, Xiaomi, Cursor; shared callback server, PKCE, Google OAuth helpers, types, static callback HTML, and index exports.
- inputs_outputs_state: Inputs are OAuth callbacks, browser/device codes, tokens, provider endpoints, env/config, fetch responses. Outputs are OAuth credentials/API keys, account metadata, registered providers, and validation errors.
- gates_or_invariants: PKCE verifier/challenge correctness, callback server state validation, provider-specific token exchange/refresh, account/project identity capture, and safe error propagation.
- dependencies_and_callers: Used by AI registry/provider auth and coding-agent login/setup/model registry. Tests include `__tests__/xai-oauth.test.ts` and provider-specific tests elsewhere.
- edge_cases_or_failure_modes: Expired/invalid refresh tokens, callback timeout, provider validation URL requirements, enterprise/project metadata, token endpoint drift, and browser/manual auth fallback.
- validation_or_tests: Provider OAuth tests in `packages/ai/test` plus local `__tests__`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1630 `directory` `packages/coding-agent/src/mcp/transports`
- cursor: `[_]`
- core_role: MCP transport implementations for stdio and HTTP/SSE connections.
- algorithmic_behavior: `stdio.ts` spawns/configures MCP server processes and frames JSON-RPC over stdio; `http.ts` connects to streamable HTTP/SSE endpoints; `index.ts` exports transport creation. Both coordinate connection lifecycle, message IO, and errors for MCP manager.
- inputs_outputs_state: Inputs are MCP server configs, environment/command args, URLs, headers, JSON-RPC messages, abort/dispose signals. Outputs are transport objects, incoming messages, process/HTTP errors, and cleanup state.
- gates_or_invariants: Transport kind must match config; stdio child process lifecycle is owned/disposed; HTTP URLs/headers must be valid; startup must not block the whole agent.
- dependencies_and_callers: Used by `src/mcp/manager` and tests such as `mcp-startup-no-block.test.ts`.
- edge_cases_or_failure_modes: Hanging stdio init, process exit, malformed JSON frames, network/SSE disconnect, auth headers, and disposal races.
- validation_or_tests: MCP startup and discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1660 `directory` `packages/stats/src/client/routes`
- cursor: `[_]`
- core_role: React route layer for stats dashboard data views.
- algorithmic_behavior: Routes fetch resources for overview, costs, errors, models, projects, requests, and behavior; transform API data into summaries/tables/charts; memoize derived series; expose segmented controls and detail callbacks; `index.ts` barrel-exports routes.
- inputs_outputs_state: Inputs are active flag, time range, refresh trigger, API responses, and click handlers. Outputs are panels, charts, tables, status pills, and route UI state.
- gates_or_invariants: Inactive routes avoid unnecessary resource work; derived values handle nulls/empty series; chart/table formatting uses shared formatters.
- dependencies_and_callers: Used by stats client shell/router; depends on `../api`, `../data/view-models`, formatters, Chart.js, UI components.
- edge_cases_or_failure_modes: Empty datasets, null costs/durations, model color assignment, long tables, refresh races, and theme changes.
- validation_or_tests: Stats client tests plus `user-metrics.test.ts` for related data logic.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1690 `file` `packages/ai/src/auth-broker/remote-store.ts`
- cursor: `[_]`
- core_role: Client-side remote auth credential store mirroring an auth broker snapshot without exposing refresh tokens.
- algorithmic_behavior: Maintains in-memory snapshot, consumes SSE snapshot streams or long-polls fallback, applies full/entry/removed events by generation, exposes read-only `AuthCredentialStore`, routes remote upsert/replace/delete through broker, refreshes OAuth through broker, coalesces/caches usage reports, and matches usage reports by provider/account/email/project.
- inputs_outputs_state: Inputs are `AuthBrokerClient`, initial snapshots, stream events, credential mutations, usage requests, abort signals. Outputs are credential lists, broker-upload/disable calls, refreshed OAuth credentials with sentinel refresh, usage reports, and callbacks. State includes snapshot generation, cache maps, usage inflight promise, streaming flags, background abort/closed state.
- gates_or_invariants: Mutating local store methods throw; older stream generations ignored; stream unsupported latches to long-poll; usage cache TTL is 15s; per-caller abort does not cancel shared usage fetch; refresh token stays broker-side.
- dependencies_and_callers: Implements `AuthCredentialStore` for `AuthStorage`; depends on auth-broker client/types and usage types.
- edge_cases_or_failure_modes: Stream 404, stale stream events, broker write failures, concurrent usage callers with one aborting, disabled credential propagation failure, and identity mismatch in usage reports.
- validation_or_tests: Auth broker/gateway tests and usage ranking tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1720 `file` `packages/ai/src/dialect/types.ts`
- cursor: `[_]`
- core_role: Shared type definitions for AI dialect/in-band tool rendering.
- algorithmic_behavior: Declares structured types for dialect tools/examples/messages rather than runtime control flow.
- inputs_outputs_state: Inputs are TypeScript consumers’ type parameters; outputs are compile-time contracts.
- gates_or_invariants: Tool/example shapes must align with dialect renderers and provider converters.
- dependencies_and_callers: Used by `dialect/examples`, tests such as `tool-examples.test.ts`, and provider prompt construction.
- edge_cases_or_failure_modes: Type drift between examples, schema rendering, and provider converters.
- validation_or_tests: Typecheck plus `tool-examples.test.ts`.
- skip_candidate: `yes: compile-time schema surface, minimal runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1750 `file` `packages/ai/src/providers/openai-chat-wire.ts`
- cursor: `[_]`
- core_role: OpenAI Chat Completions wire type surface.
- algorithmic_behavior: Defines TypeScript interfaces/unions for request/response messages, content parts, tool calls, tool choice, logprobs, stream chunks, audio, prediction, web search options, and create params.
- inputs_outputs_state: Inputs are provider request/response JSON structures; outputs are compile-time wire contracts used by provider implementation.
- gates_or_invariants: Wire fields must match OpenAI-compatible chat schema; streaming/non-streaming params remain distinct; custom/function tool variants are represented.
- dependencies_and_callers: Used by OpenAI-compatible provider code and tests.
- edge_cases_or_failure_modes: Provider schema drift, missing union member, optional field mismatch.
- validation_or_tests: Provider tests in `packages/ai/test` and TypeScript checks.
- skip_candidate: `yes: wire type definitions, not active runtime logic`

### OH_MY_HUMANIZE_MAIN-HZ-1780 `file` `packages/ai/src/registry/google-antigravity.ts`
- cursor: `[_]`
- core_role: Provider definition for Google Antigravity OAuth-backed registry entry.
- algorithmic_behavior: Exposes provider metadata and login/getApiKey behavior by delegating to Google Antigravity OAuth credentials.
- inputs_outputs_state: Inputs are OAuth callbacks/credentials. Outputs are provider definition and API key/access token.
- gates_or_invariants: Provider id/name/API key derivation must match Antigravity catalog/discovery expectations.
- dependencies_and_callers: Used by AI registry and catalog Antigravity discovery/model manager.
- edge_cases_or_failure_modes: Missing credentials, token refresh failure, provider id mismatch.
- validation_or_tests: Google OAuth/Antigravity tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1810 `file` `packages/ai/src/registry/qwen-portal.ts`
- cursor: `[_]`
- core_role: Qwen portal provider login/validation definition.
- algorithmic_behavior: `loginQwenPortal` delegates to OpenAI-compatible API-key validation against `https://portal.qwen.ai/v1` using validation model `coder-model`; exports provider definition with auth URL and callbacks.
- inputs_outputs_state: Inputs are OAuth/API-key controller callbacks. Outputs are validated API key string and provider metadata.
- gates_or_invariants: Key must validate against configured base URL/model before acceptance.
- dependencies_and_callers: Uses `validateOpenAICompatibleApiKey`; consumed by provider registry and setup/login flows.
- edge_cases_or_failure_modes: Invalid key, network failure, validation model unavailable, base URL changes.
- validation_or_tests: Provider registry/model tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1840 `file` `packages/ai/src/usage/shared.ts`
- cursor: `[_]`
- core_role: Shared usage numeric coercion helper.
- algorithmic_behavior: Exports `toNumber`, returning a finite number only when input is numeric/parseable as finite number.
- inputs_outputs_state: Input is unknown value; output is `number | undefined`.
- gates_or_invariants: Non-finite, nonnumeric, and empty values should not become usage numbers.
- dependencies_and_callers: Used by usage parsers across providers.
- edge_cases_or_failure_modes: Numeric strings, `NaN`, `Infinity`, null/undefined, and booleans.
- validation_or_tests: Usage parsing tests.
- skip_candidate: `yes: tiny helper, included because usage parsing depends on it`

### OH_MY_HUMANIZE_MAIN-HZ-1870 `file` `packages/catalog/src/discovery/antigravity.ts`
- cursor: `[_]`
- core_role: Antigravity model discovery client/parser for catalog.
- algorithmic_behavior: Defines arktype schemas for Antigravity API response, fetches `/v1internal:fetchAvailableModels` from primary/sandbox endpoints, sends Antigravity user agent and bearer token, parses model groups/sorts, deny-lists known bad IDs, normalizes token limits with defaults, and returns `ModelSpec`s.
- inputs_outputs_state: Inputs are access token/fetch implementation/endpoints/base URL. Outputs are discovered model specs or null/empty discovery states. State is local fetch attempt order only.
- gates_or_invariants: Response must match schema; endpoints trim trailing slashes; context/max tokens fallback to defaults; denylisted models excluded.
- dependencies_and_callers: Used by provider model manager/descriptors and `ModelRegistry` discovery.
- edge_cases_or_failure_modes: Primary endpoint failure with sandbox fallback, invalid JSON/schema, missing token limits, denied model ids, HTTP auth errors.
- validation_or_tests: `packages/catalog/test/variant-collapse.test.ts` Antigravity sections and provider discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1900 `file` `packages/coding-agent/src/advisor/runtime.ts`
- cursor: `[_]`
- core_role: Runtime coordinator for advisor agent catch-up and deltas.
- algorithmic_behavior: Tracks pending deltas, session history token estimates, catchup waiters, and host/agent interactions so an advisor can receive formatted session history and incremental updates.
- inputs_outputs_state: Inputs are `AgentMessage`s, advisor agent interface, runtime host, and history changes. Outputs are advisor prompts/events, catch-up completion, and logs. State includes pending deltas and waiter list.
- gates_or_invariants: Advisor must not receive inconsistent history; token estimates bound catch-up context; failures logged without crashing main session.
- dependencies_and_callers: Used by AgentSession advisor toggle/runtime; depends on compaction token estimator and session history markdown formatter.
- edge_cases_or_failure_modes: Advisor unavailable, catch-up race, token overflow, waiter rejection, and host disposal.
- validation_or_tests: Advisor tests such as `advisor-toggle.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1930 `file` `packages/coding-agent/src/capability/tool.ts`
- cursor: `[_]`
- core_role: Capability definition for custom extension tools.
- algorithmic_behavior: Declares `CustomTool` shape and registers `toolCapability` through generic capability system.
- inputs_outputs_state: Inputs are discovered extension tool definitions. Outputs are normalized/registered tool capabilities.
- gates_or_invariants: Tool definitions must carry name/description/schema/source metadata expected by capability loader.
- dependencies_and_callers: Used by discovery providers including Claude plugins and OMP extensions.
- edge_cases_or_failure_modes: Missing schema/source metadata, duplicate names, loader validation errors.
- validation_or_tests: Extension/custom tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1960 `file` `packages/coding-agent/src/cli/startup-cwd.ts`
- cursor: `[_]`
- core_role: Applies startup working-directory CLI behavior.
- algorithmic_behavior: Resolves requested cwd/project paths, normalizes comparisons, handles home/project dir, verifies directories with fs, and calls `setProjectDir`.
- inputs_outputs_state: Inputs are parsed CLI args and current project/home dirs. Outputs are updated project dir or errors.
- gates_or_invariants: Startup cwd must resolve to an existing directory; no-op when equivalent to current project dir; path normalization avoids duplicate cwd state.
- dependencies_and_callers: Called early by `runRootCommand`.
- edge_cases_or_failure_modes: Missing path, file instead of directory, permission error, tilde/home differences, and symlinks/case normalization.
- validation_or_tests: CLI startup/root tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1990 `file` `packages/coding-agent/src/commands/models.ts`
- cursor: `[_]`
- core_role: Command wrapper exposing models CLI through command registry.
- algorithmic_behavior: Defines command args/flags and delegates resolution/execution to `cli/models-cli`.
- inputs_outputs_state: Inputs are command args. Outputs are model listing/config command results.
- gates_or_invariants: Flags must match CLI parser expectations and app naming.
- dependencies_and_callers: Used by command registry; depends on `pi-utils/cli` and `models-cli`.
- edge_cases_or_failure_modes: Flag drift between wrapper and implementation.
- validation_or_tests: CLI model command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2020 `file` `packages/coding-agent/src/config/model-registry.ts`
- cursor: `[_]`
- core_role: Central runtime model catalog/auth/discovery registry for coding-agent.
- algorithmic_behavior: Loads bundled models, config models, cached provider discoveries, implicit local providers, runtime extension providers, provider/model overrides, OAuth provider registrations, dynamic model managers, canonical model index, available-model filtering, auth resolution, provider discovery status, selector suppression, and background refresh.
- inputs_outputs_state: Inputs are auth storage, models config file, bundled catalog, model cache DB, settings, env vars, extension provider registrations, dynamic fetchers, and requested provider/model selectors. Outputs are model lists, canonical selections, API key resolvers, discovery states, registered custom APIs/OAuth providers, and suppressed selector state.
- gates_or_invariants: Command-backed API keys resolve lazily; keyless providers return `kNoAuth`; runtime providers survive refresh cycles; authoritative fresh cache can replace bundled provider rows; disabled provider settings filter availability; canonical queries are linear-time with prebuilt filters.
- dependencies_and_callers: Used by `main.ts`, SDK session creation, setup/model picker, providers, extensions, and auth flows; imports catalog values from `pi-catalog`.
- edge_cases_or_failure_modes: Config parse errors, stale caches, discovery network failure, provider handoff between extensions, dynamic model fetch auth, command API key failure, suppressed selectors expiring, and canonical variant ambiguity.
- validation_or_tests: Model registry/config/provider tests across coding-agent/catalog/ai packages.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2050 `file` `packages/coding-agent/src/discovery/claude-plugins.ts`
- cursor: `[_]`
- core_role: Discovery provider for Claude Code Marketplace plugin contents.
- algorithmic_behavior: Resolves plugin directories, reads manifests/files, ensures paths remain within plugin root, substitutes plugin-root variables, and registers discovered hooks, MCP servers, skills, slash commands, and custom tools with capability system.
- inputs_outputs_state: Inputs are plugin roots/manifests and load context. Outputs are capability registrations and load results.
- gates_or_invariants: Paths must not escape plugin root; provider priority is below local Claude discovery so user overrides win; invalid plugin files log/skip rather than crash all discovery.
- dependencies_and_callers: Used by discovery initialization and plugin marketplace install flow.
- edge_cases_or_failure_modes: Broken manifest, symlink/path traversal, duplicate capability names, missing files, malformed MCP/tool definitions.
- validation_or_tests: Plugin/custom command tests and discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2080 `file` `packages/coding-agent/src/eval/completion-bridge.ts`
- cursor: `[_]`
- core_role: Structured completion bridge for JS/Python evaluation helpers to call LLMs.
- algorithmic_behavior: Defines completion args schema, resolves tier model (`smol`/default/slow), chooses reasoning effort supported by model, calls instrumented completion, extracts text/tool structured payloads, enforces timeout pause, and maps errors to `ToolError`.
- inputs_outputs_state: Inputs are tool session, prompt/messages/tools/tier/schema, model registry/session model, and runtime status hooks. Outputs are completion text/JSON/tool result events and status updates.
- gates_or_invariants: Tier must resolve to available model; structured tool name is fixed; unsupported effort omitted; bridge timeout protects evaluator.
- dependencies_and_callers: Used by JS/Python eval runtimes and tool bridge helpers.
- edge_cases_or_failure_modes: No model for tier, invalid JSON payload, missing tool call, model timeout, telemetry errors.
- validation_or_tests: Eval/bridge tests and workflow/evaluator tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2110 `file` `packages/coding-agent/src/hindsight/config.ts`
- cursor: `[_]`
- core_role: Hindsight feature configuration resolver.
- algorithmic_behavior: Parses booleans/integers/strings from env/settings, validates retain mode, recall budget, scoping, preamble, and enable flags, then returns normalized hindsight config.
- inputs_outputs_state: Inputs are `Settings` and env vars. Outputs are `HindsightConfig`.
- gates_or_invariants: Only known retain modes/budgets/scopings accepted; invalid env values ignored/logged; defaults applied consistently.
- dependencies_and_callers: Used by hindsight/memory recall subsystem.
- edge_cases_or_failure_modes: Malformed env integers/booleans, unknown setting values, disabled feature with partial config.
- validation_or_tests: Hindsight config tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2140 `file` `packages/coding-agent/src/lsp/format-options.ts`
- cursor: `[_]`
- core_role: Resolves LSP formatting options from content and editorconfig.
- algorithmic_behavior: Detects indentation from file content by counting leading tabs/spaces and GCD of space indents, falls back to editorconfig formatting, and returns `tabSize`, `insertSpaces`, trim, and final newline options.
- inputs_outputs_state: Inputs are file path and content. Outputs are LSP formatting option object.
- gates_or_invariants: Default fallback is 2 spaces/insert spaces; editorconfig can override; content detection avoids zero/invalid sizes.
- dependencies_and_callers: Uses `getEditorConfigFormatting` from utils; consumed by LSP formatting/edit flows.
- edge_cases_or_failure_modes: Mixed indentation, empty files, tabs plus spaces, editorconfig missing/invalid.
- validation_or_tests: LSP formatting tests and tab-spacing tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2170 `file` `packages/coding-agent/src/memories/storage.ts`
- cursor: `[_]`
- core_role: SQLite job/data store for memory consolidation pipeline.
- algorithmic_behavior: Opens/migrates DB tables, upserts memory threads, ensures stage1/global jobs, claims stage1 jobs with retry/lease semantics, enqueues global watermarks, records stage1 success/no-output/failure, claims global phase2 jobs, heartbeats, lists outputs, and marks global success/failure/unowned failure.
- inputs_outputs_state: Inputs are DB path, threads, worker IDs, cwd, limits, timestamps, outputs/errors. Outputs are claims, output rows, job status mutations, and DB rows. State is SQLite tables for threads/jobs/outputs.
- gates_or_invariants: Retry counts decrement on failure; claims are worker-owned; global job keyed by cwd; stage outputs feed global phase; heartbeat extends ownership.
- dependencies_and_callers: Used by memory/hindsight background processing.
- edge_cases_or_failure_modes: Stale leases, concurrent workers, no output success, failed unowned global job, retry exhaustion, and DB close/cleanup.
- validation_or_tests: Memory storage/pipeline tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2200 `file` `packages/coding-agent/src/modes/ultrathink.ts`
- cursor: `[_]`
- core_role: Ultrathink keyword detection/highlighting and system notice.
- algorithmic_behavior: Imports static notice prompt, detects standalone `ultrathink` in prose with regex/prose guard, and exports gradient highlighter.
- inputs_outputs_state: Inputs are user text/markdown tokens. Outputs are boolean detection, notice text, and highlighted spans.
- gates_or_invariants: Keyword must be standalone and in prose, not inside code-ish contexts.
- dependencies_and_callers: Used by modes/markdown UI and prompt injection logic.
- edge_cases_or_failure_modes: Punctuation/case, code blocks, substrings, and markdown parsing quirks.
- validation_or_tests: Similar workflow mode tests; ultrathink-specific tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2230 `file` `packages/coding-agent/src/session/session-migrations.ts`
- cursor: `[_]`
- core_role: File session entry migration logic.
- algorithmic_behavior: Generates missing IDs, migrates V1 to V2 and V2 to V3 entries, updates headers to current session version, and applies migrations in-place.
- inputs_outputs_state: Inputs are file session entries. Outputs are mutated entries and boolean indicating migration.
- gates_or_invariants: Generated IDs must be unique in existing map; migrations should preserve messages/content while adding required metadata.
- dependencies_and_callers: Used by session storage load path.
- edge_cases_or_failure_modes: Missing header, duplicate ids, unknown future version, malformed compaction/file entries.
- validation_or_tests: Session storage/history/migration tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2260 `file` `packages/coding-agent/src/stt/stt-controller.ts`
- cursor: `[_]`
- core_role: Speech-to-text recording/transcription lifecycle controller.
- algorithmic_behavior: Maintains `idle`/`recording`/`transcribing` state, toggles recording, ensures model cache/download, starts/stops STT stream, writes temp audio, transcribes, inserts text into editor, and logs/errors.
- inputs_outputs_state: Inputs are editor adapter, toggle options, settings, ASR stream events, model specs. Outputs are editor text insertion, state changes, temp files, and logs.
- gates_or_invariants: Cannot start while transcribing; model must be cached/downloaded; stream handle must be stopped/disposed; temp files cleaned where possible.
- dependencies_and_callers: Uses STT client/downloader/models/transcriber and interactive editor.
- edge_cases_or_failure_modes: Download failure, stream start/stop failure, empty transcription, concurrent toggles, temp file errors, and editor insertion failure.
- validation_or_tests: STT/controller tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2290 `file` `packages/coding-agent/src/tools/ast-grep.ts`
- cursor: `[_]`
- core_role: Agent tool for AST-aware code search.
- algorithmic_behavior: Defines arktype schema for pattern/lang/scope/output controls, resolves search scope, calls native `astGrep`, records file snapshots/seen lines, formats grouped/hashline output, supports abort, emits updates, and renders TUI results.
- inputs_outputs_state: Inputs are AST pattern, language/file type, path/glob scope, output options, tool session cwd, abort signal. Outputs are tool result text/details, file recorder metadata, snapshots, and renderer components.
- gates_or_invariants: Search scope must stay in allowed project paths; invalid params become `ToolError`; output preview uses limits; hashline headers include file hashes.
- dependencies_and_callers: Uses `pi-natives` AST grep, hashline, file recorder, grouped file output, TUI renderer.
- edge_cases_or_failure_modes: Invalid pattern/lang, no matches, binary/ignored files, abort during native search, large result truncation, and path display mode.
- validation_or_tests: AST/search tool tests and invalid regex/search tests adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2320 `file` `packages/coding-agent/src/tools/inspect-image.ts`
- cursor: `[_]`
- core_role: Vision-model tool for inspecting an image and returning text analysis.
- algorithmic_behavior: Validates params, resolves model preference/role alias, requires image-capable model, builds static prompt template, calls `completeSimple`/instrumented completion with image content, extracts text, emits updates, and renders via image renderer export.
- inputs_outputs_state: Inputs are image path/base64/content, user question, model option, session model registry/settings. Outputs are textual inspection result, details, and errors.
- gates_or_invariants: Selected model must support image input; prompt content comes from `.md` templates; forbidden/model errors become `ToolError`; telemetry resolved.
- dependencies_and_callers: Uses `pi-ai`, model resolver, prompt templates, commit text extraction, tool session.
- edge_cases_or_failure_modes: Text-only model, missing image, invalid model selector, provider forbidden response, empty assistant text.
- validation_or_tests: `packages/coding-agent/test/tools/inspect-image.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2350 `file` `packages/coding-agent/src/tools/todo.ts`
- cursor: `[_]`
- core_role: Structured session todo tool and renderer.
- algorithmic_behavior: Applies ordered operations (`init`, `start`, `done`, `drop`, `rm`, `append`, `view`) to phased tasks, enforces single in-progress task, rejects duplicate task/phase init, supports Markdown round-trip, selects sticky todo windows, matches subagent descriptions, computes completion transitions, persists phases to session, and renders TUI summaries/animations.
- inputs_outputs_state: Inputs are todo ops, current session phases, session entries, markdown text, render args, theme/frame. Outputs are updated phases, text summary, details, completed transition metadata, markdown, and TUI components.
- gates_or_invariants: Tasks are referenced by content; duplicate tasks are rejected to avoid unaddressable operations; batches with any error are discarded wholesale; pure view does not normalize or persist; one task is auto-promoted to in-progress.
- dependencies_and_callers: Used as agent tool, slash todo helper, sticky panel, session history.
- edge_cases_or_failure_modes: Missing task/phase/list, duplicate append items, `task-123` mistaken IDs, malformed streaming JSON render args, unknown markdown markers, empty lists.
- validation_or_tests: Todo/slash/render tests and session todo tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2380 `file` `packages/coding-agent/src/utils/clipboard.ts`
- cursor: `[_]`
- core_role: Cross-platform clipboard text/image utility.
- algorithmic_behavior: Detects display/WSL, writes text via native clipboard or platform commands, reads image via native or PowerShell script, reads text with fallback scripts, logs failures, and normalizes clipboard image result.
- inputs_outputs_state: Inputs are text strings and current OS/display/clipboard contents. Outputs are clipboard side effects, read text, image object/null, and logs.
- gates_or_invariants: Prefer native APIs; WSL/PowerShell scripts bounded by timeout; no display path handled; errors logged without TUI corruption.
- dependencies_and_callers: Used by `/dump`, copy/share features, image paste flows; depends on `pi-natives`, logger, child command execution.
- edge_cases_or_failure_modes: Headless Linux, WSL interop missing, PowerShell timeout, unsupported image format, command failure.
- validation_or_tests: Clipboard-related interactive/manual tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2410 `file` `packages/coding-agent/src/workflow/artifact-registry.ts`
- cursor: `[_]`
- core_role: Registry for builtin/installed/external workflow artifacts.
- algorithmic_behavior: Computes workflow directories from env/default/builtin roots, resolves named/path flow specs, lists specs, installs workflow artifacts by freezing source into install root, uninstalls, expands home, safe-names flows, and cleans empty install containers.
- inputs_outputs_state: Inputs are flow name/path/source, cwd, registry options, filesystem roots. Outputs are resolved `WorkflowFlowSpec`, installed artifact metadata, installed files, and removals.
- gates_or_invariants: Named flow lookup checks installed/external/builtin candidates; install source must exist and be flow-like; safe flow name prevents unsafe paths.
- dependencies_and_callers: Used by workflow CLI/runner/setup; depends on package loader/freeze and config dirs.
- edge_cases_or_failure_modes: Missing flow, ambiguous name, path outside expected roots, invalid source, uninstall of absent flow, and cleanup errors.
- validation_or_tests: Workflow e2e and artifact registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2440 `file` `packages/coding-agent/src/workflow/state.ts`
- cursor: `[_]`
- core_role: Workflow state read/patch/activation-output validator.
- algorithmic_behavior: Reads state object, applies JSON-pointer patch operations, validates activation output shape, enforces allowed write scopes, detects conflicting writes, blocks oversized inline values/summaries, validates artifact references, and rejects raw transcript fields.
- inputs_outputs_state: Inputs are workflow state, patch operations, activation output, and access policy. Outputs are patched state or `WorkflowStateError`.
- gates_or_invariants: Pointer scopes control read/write; duplicate/conflicting patch paths rejected; inline bytes capped; artifact references must be references, not raw blobs; raw transcript fields forbidden.
- dependencies_and_callers: Used by workflow runner/node runtime/session runtime.
- edge_cases_or_failure_modes: Invalid JSON pointer escaping, writing outside scope, oversize strings, non-record activation output, raw transcript leakage.
- validation_or_tests: Workflow e2e and state tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2470 `file` `packages/coding-agent/test/core/python-executor.lifecycle.test.ts`
- cursor: `[_]`
- core_role: Tests Python executor kernel session lifecycle.
- algorithmic_behavior: Defines fake kernel, invokes `executePython`, disposes all kernel sessions, and asserts sessions are reused/cleaned according to lifecycle rules.
- inputs_outputs_state: Inputs are Python code/session identifiers and fake kernel results. Outputs are kernel execute/dispose calls and executor results.
- gates_or_invariants: Kernel sessions must not leak; dispose-all clears active sessions; execution result shape preserved.
- dependencies_and_callers: Exercises `eval/py/executor`.
- edge_cases_or_failure_modes: Kernel failure, stale session, dispose after execution, and multiple sessions.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2500 `file` `packages/coding-agent/test/discovery/mcp-json.test.ts`
- cursor: `[_]`
- core_role: Tests standalone `mcp.json` OAuth env expansion in discovery.
- algorithmic_behavior: Writes temp MCP JSON configs with env placeholders, loads MCP capability, and asserts expanded server definitions.
- inputs_outputs_state: Inputs are temp config files and env placeholder names. Outputs are `MCPServer` capability data.
- gates_or_invariants: OAuth env expansion must occur for standalone MCP JSON without leaking literal placeholders.
- dependencies_and_callers: Exercises discovery capability loader and MCP capability.
- edge_cases_or_failure_modes: Missing env, malformed JSON, temp home cleanup, and placeholder syntax.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2530 `file` `packages/coding-agent/test/helpers/temp-home-cleanup.ts`
- cursor: `[_]`
- core_role: Test helper for cleaning temp home/agent dirs.
- algorithmic_behavior: Returns an after-test cleanup closure that removes temp home paths based on mutable test state.
- inputs_outputs_state: Inputs are getter for temp-home state. Output is cleanup side effect.
- gates_or_invariants: Only removes paths recorded in state; tolerates unset state.
- dependencies_and_callers: Used by tests that mutate home/agent dirs.
- edge_cases_or_failure_modes: Missing path, repeated cleanup, filesystem removal failure.
- validation_or_tests: Indirect through tests.
- skip_candidate: `yes: test hygiene helper, not product algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2560 `file` `packages/coding-agent/test/modes/workflow.test.ts`
- cursor: `[_]`
- core_role: Tests workflow keyword detection/highlighting and notice.
- algorithmic_behavior: Initializes theme, calls `containsWorkflow`, `highlightWorkflow`, and asserts `WORKFLOW_NOTICE` content.
- inputs_outputs_state: Inputs are text/markdown strings. Outputs are booleans/highlighted strings/notice text.
- gates_or_invariants: Keyword detection should respect prose boundaries and not match unintended substrings/code contexts.
- dependencies_and_callers: Exercises workflow mode helper.
- edge_cases_or_failure_modes: Case/punctuation, code blocks, substrings, and theme initialization.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2590 `file` `packages/coding-agent/test/session/sql-session-storage-manager.test.ts`
- cursor: `[_]`
- core_role: Tests `SessionManager` with SQLite session storage.
- algorithmic_behavior: Creates fake usage, stores sessions through SQL backend, and asserts listing/status/metadata aggregation.
- inputs_outputs_state: Inputs are session entries/usages and SQLite storage. Outputs are manager query/list results.
- gates_or_invariants: SQL storage must preserve usage and session metadata consumed by manager.
- dependencies_and_callers: Exercises `SessionManager`, `SqlSessionStorage`, Bun SQL.
- edge_cases_or_failure_modes: SQLite cleanup, usage aggregation, missing sessions.
- validation_or_tests: This file plus directory session tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2620 `file` `packages/coding-agent/test/task/render-call.test.ts`
- cursor: `[_]`
- core_role: Tests task tool streaming call preview renderer.
- algorithmic_behavior: Initializes theme/settings, passes partial `TaskParams` to `taskToolRenderer`, and asserts compact render output.
- inputs_outputs_state: Inputs are task call args and theme. Outputs are rendered component strings.
- gates_or_invariants: Streaming preview must handle partial args and fit display.
- dependencies_and_callers: Exercises task renderer.
- edge_cases_or_failure_modes: Missing description, long text, partial JSON during streaming.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2650 `file` `packages/coding-agent/test/tools/browser-cmux-kind.test.ts`
- cursor: `[_]`
- core_role: Tests browser cmux kind resolution.
- algorithmic_behavior: Calls `resolveCmuxKind` with inputs and asserts kind classification.
- inputs_outputs_state: Inputs are cmux/browser kind values. Outputs are resolved kind.
- gates_or_invariants: Browser tool must choose expected cmux transport variant.
- dependencies_and_callers: Exercises browser tool exports.
- edge_cases_or_failure_modes: Unknown/undefined kind and aliases.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2680 `file` `packages/coding-agent/test/tools/inspect-image.test.ts`
- cursor: `[_]`
- core_role: Tests inspect image tool execution and renderer.
- algorithmic_behavior: Builds vision/text-only models and session stubs, stubs `completeSimple`, invokes `InspectImageTool`, and asserts success/error/render behavior.
- inputs_outputs_state: Inputs are tiny PNG, image params, model choices, stubbed completions. Outputs are tool results/details/errors/rendered text.
- gates_or_invariants: Text-only model rejected; vision model passes image content; forbidden completion maps to tool error; renderer sanitizes output.
- dependencies_and_callers: Exercises `InspectImageTool`, renderer, model settings.
- edge_cases_or_failure_modes: Forbidden provider response, empty completion, invalid image/model, and renderer sanitization.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2710 `file` `packages/coding-agent/test/tools/search-invalid-regex.test.ts`
- cursor: `[_]`
- core_role: Tests search tool invalid regex handling.
- algorithmic_behavior: Creates temp session/cwd, invokes `SearchTool` with invalid regex, and asserts `ToolError`/error message behavior.
- inputs_outputs_state: Inputs are regex query and temp files. Outputs are thrown/captured tool error.
- gates_or_invariants: Invalid regex should fail cleanly, not crash native search or return misleading results.
- dependencies_and_callers: Exercises `SearchTool`.
- edge_cases_or_failure_modes: Regex syntax errors, temp cwd cleanup, settings reset.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2740 `file` `packages/coding-agent/test/utils/image-resize.test.ts`
- cursor: `[_]`
- core_role: Tests image resize utility defaults and environment wiring.
- algorithmic_behavior: Builds small/oversized PNG/WebP fixtures, calls `resizeImage`, and asserts resizing thresholds, format handling, and env-controlled behavior.
- inputs_outputs_state: Inputs are base64 images and env/settings. Outputs are resized/skipped image data and metadata.
- gates_or_invariants: Small images should not resize unnecessarily; oversized images resize under configured bounds; env flags alter behavior predictably.
- dependencies_and_callers: Exercises `utils/image-resize` used by file/image prompt processing.
- edge_cases_or_failure_modes: Invalid env values, WebP/PNG handling, zero/large dimensions, and before/after env cleanup.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2770 `file` `packages/coding-agent/test/workflow/workflow-e2e.test.ts`
- cursor: `[_]`
- core_role: End-to-end workflow runner/regression suite.
- algorithmic_behavior: Parses workflow definitions, builds runtime host/store, runs workflows with agent-routed and humanize fallback loops, reconstructs runs, inspects lifecycle, checkpoint activations, bindings, and flow freezes.
- inputs_outputs_state: Inputs are workflow DSL sources, model fixtures, runtime host captures, activation/checkpoint data. Outputs are run entries, lifecycle inspections, reconstructed state, and assertions.
- gates_or_invariants: Workflow scheduler/runner must preserve activation order, bindings, loop routing, checkpoint reconstruction, and fallback semantics.
- dependencies_and_callers: Exercises workflow definition/parser, runner, scheduler, node runtime, session runtime, inspection, run store.
- edge_cases_or_failure_modes: Loops, fallback routing, checkpoint replay, missing bindings, completed activation filtering.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2800 `file` `packages/mnemopi/src/core/llm-backends.ts`
- cursor: `[_]`
- core_role: LLM backend abstraction for mnemopi.
- algorithmic_behavior: Defines backend interfaces/adapters for chat/completion calls used by mnemopi memory logic.
- inputs_outputs_state: Inputs are normalized chat prompts/model config. Outputs are backend responses/usage.
- gates_or_invariants: Backend contract abstracts provider-specific call shape from memory algorithms.
- dependencies_and_callers: Used by mnemopi core pipelines.
- edge_cases_or_failure_modes: Missing backend, provider errors, response normalization drift.
- validation_or_tests: Mnemopi tests and integration usage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2830 `file` `packages/mnemopi/src/util/lru.ts`
- cursor: `[_]`
- core_role: Small LRU cache utility.
- algorithmic_behavior: Maintains insertion/access ordering, evicts least-recently-used entries when capacity exceeded, and exposes get/set/delete/clear behavior.
- inputs_outputs_state: Inputs are keys/values/capacity. Outputs are cached values and eviction state.
- gates_or_invariants: Capacity bounds enforced; get refreshes recency; delete/clear update size.
- dependencies_and_callers: Used by mnemopi caching paths.
- edge_cases_or_failure_modes: Zero/negative capacity, overwrite existing key, eviction order.
- validation_or_tests: Utility tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2860 `file` `packages/utils/test/mermaid/formatting.test.ts`
- cursor: `[_]`
- core_role: Tests Mermaid ASCII formatting output.
- algorithmic_behavior: Feeds Mermaid diagrams through formatter and asserts output formatting/golden expectations.
- inputs_outputs_state: Inputs are Mermaid diagram strings/fixtures. Outputs are ASCII/Unicode formatted diagrams.
- gates_or_invariants: Formatting must preserve layout and readable graph structure.
- dependencies_and_callers: Exercises vendored Mermaid ASCII renderer used by utils/TUI.
- edge_cases_or_failure_modes: Multiline labels, spacing, Unicode vs ASCII mode.
- validation_or_tests: This file plus golden fixtures.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2890 `directory` `packages/coding-agent/src/modes/setup-wizard/scenes`
- cursor: `[_]`
- core_role: Individual setup wizard scenes and tabs.
- algorithmic_behavior: `splash/outro` animate wizard entry/exit; `providers` coordinates sign-in and web-search tabs; `sign-in` drives provider auth UI; `web-search` stores search provider preferences; `theme` previews/selects themes; `glyph` selects symbol preset; `types` defines scene/controller host contracts.
- inputs_outputs_state: Inputs are key/mouse events, settings/context, provider/search/theme options, dimensions/time. Outputs are rendered components, settings mutations, scene results, and tab selection state.
- gates_or_invariants: Scene controllers receive focus/routing only while active; render must fit terminal width; settings changes persist through host; tabs/scenes report done/skipped.
- dependencies_and_callers: Used by `wizard-overlay.ts` and setup command/tests.
- edge_cases_or_failure_modes: Narrow terminals, mouse routing, unavailable providers, skipped sign-in, theme preview overflow, glyph fallback.
- validation_or_tests: `setup-wizard.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2920 `file` `crates/pi-shell/src/minimizer/filters/ruby.rs`
- cursor: `[_]`
- core_role: Ruby tool output minimizer for shell command summaries.
- algorithmic_behavior: Detects Ruby tool/subcommand (`rspec`, `minitest`, `rubocop`, `rake`, generic test), strips noise, compacts RSpec text/JSON failures, limits rendered failures, extracts summaries, compacts RuboCop autocorrect output, preserves relevant Rake abort frames, and returns minimized output based on exit code.
- inputs_outputs_state: Inputs are program/subcommand, raw stdout/stderr text, exit code, minimizer context. Outputs are compacted `MinimizerOutput` text.
- gates_or_invariants: Only supports Ruby-related tools; success output can be reduced to summary; failure output keeps actionable locations/exceptions; rendered failure/frame caps avoid giant logs.
- dependencies_and_callers: Used by `pi-shell` minimizer pipeline for bash/tool rendering.
- edge_cases_or_failure_modes: JSON formatter output, coverage banners, gem backtraces, multiline failures, aborted rake tasks, RuboCop autocorrect lines, empty output.
- validation_or_tests: pi-shell minimizer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2950 `file` `packages/ai/src/utils/schema/equality.ts`
- cursor: `[_]`
- core_role: JSON-schema equality/merge helper for schema normalization.
- algorithmic_behavior: Deep-compares JSON values, merges compatible enum schemas, extracts `anyOf` variants, and merges property schemas while preserving compatible alternatives.
- inputs_outputs_state: Inputs are unknown schema fragments. Outputs are boolean equality, merged schema object/null, or merged property schema.
- gates_or_invariants: Only JSON-object schemas merge; enum compatibility must be exact/compatible; incompatible schemas remain separate via variants.
- dependencies_and_callers: Used by strict schema/tool schema normalization.
- edge_cases_or_failure_modes: Different property order, duplicate enum values, non-object schemas, nested arrays/objects.
- validation_or_tests: Schema strict/compatibility tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2980 `file` `packages/coding-agent/src/cli/gallery-fixtures/shell.ts`
- cursor: `[_]`
- core_role: Static gallery fixtures for shell tool renderer states.
- algorithmic_behavior: Exports shell fixture records for renderer gallery snapshots; contains sample args/results rather than runtime control flow.
- inputs_outputs_state: Inputs are selected fixture names. Outputs are predefined gallery fixture objects.
- gates_or_invariants: Fixture shape must match `GalleryFixture` and renderer expectations.
- dependencies_and_callers: Used by gallery CLI/screenshots.
- edge_cases_or_failure_modes: Fixture drift from renderer schema.
- validation_or_tests: Gallery command/render tests.
- skip_candidate: `yes: static visual fixture data, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3010 `file` `packages/coding-agent/src/edit/hashline/execute.ts`
- cursor: `[_]`
- core_role: Hashline edit executor that applies parsed patch sections and returns tool/LSP diagnostics.
- algorithmic_behavior: Validates unique canonical paths, prepares/narrows LSP batch requests, applies hashline patch sections through `HashlineFilesystem`, formats block resolution diagnostics, detects no-change edits and repeated no-op loops, records snapshots, generates diffs, and returns per-file edit results.
- inputs_outputs_state: Inputs are hashline params, tool session, filesystem, LSP batch request, writethrough callbacks. Outputs are `AgentToolResult`, per-file results, diagnostics, diffs, and snapshot state.
- gates_or_invariants: Duplicate canonical paths rejected; no-change loop guard caps repeated noops; LSP batch only runs on last relevant request; mismatch errors surface as `ToolError`.
- dependencies_and_callers: Used by edit tool; depends on `@oh-my-pi/hashline`, file snapshot store, LSP, diff generator.
- edge_cases_or_failure_modes: Hash mismatch, block unresolved, duplicate files, no changes, repeated no-op hard limit, LSP diagnostics failures.
- validation_or_tests: Hashline/edit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3040 `file` `packages/coding-agent/src/eval/py/runner.py`
- cursor: `[_]`
- core_role: Long-lived Python evaluation kernel runner.
- algorithmic_behavior: Reads JSON requests from stdin, transforms IPython-style magics/shell escapes into executable Python, captures stdout/stderr with stream proxies, runs sync/async code, supports line/cell magics (`pip`, `cd`, `time`, `timeit`, `writefile`, shell), emits display MIME bundles/images/matplotlib figures, handles SIGINT, applies per-request runtime cwd/env, watches parent process, and returns structured frames.
- inputs_outputs_state: Inputs are request frames with source/runtime data and stdin code. Outputs are JSON frames for stream/status/display/result/error. State includes namespace, stream buffers, execution context, cwd/env, and signal mode.
- gates_or_invariants: All emitted frames JSON-serializable; stream capture tied to request id; parent watchdog exits orphaned runner; magic parsing preserves continuations; SIGINT behavior differs idle vs executing.
- dependencies_and_callers: Used by coding-agent Python executor and eval tools.
- edge_cases_or_failure_modes: Top-level await, matplotlib backends, shell command errors, pip install status, interrupted execution, malformed request JSON, parent death, binary image coercion.
- validation_or_tests: `python-executor.lifecycle.test.ts` and eval tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3070 `file` `packages/coding-agent/src/extensibility/plugins/installer.ts`
- cursor: `[_]`
- core_role: Plugin install/uninstall/list/link filesystem installer.
- algorithmic_behavior: Validates package names, installs packages into agent plugins dir, extracts package name, uninstalls plugin dirs, lists installed plugins by metadata, and links local plugin paths.
- inputs_outputs_state: Inputs are package name/git/local path and agent/project dirs. Outputs are installed plugin metadata, filesystem writes/removals/symlinks.
- gates_or_invariants: Package names must match safe regex; local paths resolved; install dir under agent plugins; missing paths handled.
- dependencies_and_callers: Used by plugin manager/CLI and marketplace install parser.
- edge_cases_or_failure_modes: Invalid package name, install subprocess failure, missing package metadata, symlink conflicts, uninstall absent plugin.
- validation_or_tests: `plugin-install-git.test.ts` and plugin manager tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3100 `file` `packages/coding-agent/src/modes/components/assistant-message.ts`
- cursor: `[_]`
- core_role: TUI component for assistant messages, thinking, images, and errors.
- algorithmic_behavior: Canonicalizes assistant content, renders markdown/text/image blocks, shows thinking dots/blocks with animation, truncates transcript error previews, resolves abort labels, applies image budget/protocol options, and composes TUI containers.
- inputs_outputs_state: Inputs are `AssistantMessage`, image budget/options, thinking renderer/theme. Outputs are TUI component tree.
- gates_or_invariants: Raw transcript errors are preview-limited; abort reasons honor silent/user labels; images respect terminal protocol/budget; markdown uses theme.
- dependencies_and_callers: Used by interactive transcript/event controller.
- edge_cases_or_failure_modes: Missing image protocol, huge error text, hidden thinking, aborted message without reason, malformed image content.
- validation_or_tests: Event-controller abort render and TUI rendering tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3130 `file` `packages/coding-agent/src/modes/components/mcp-add-wizard.ts`
- cursor: `[_]`
- core_role: Interactive wizard for adding MCP servers.
- algorithmic_behavior: Maintains multi-step state for transport/auth/scope/config, sanitizes display text, renders forms/lists, validates stdio/http/sse fields, handles OAuth/manual/env/header auth, writes server config, and reports OAuth result.
- inputs_outputs_state: Inputs are key/mouse events, OAuth options, server config fields, scope, auth values. Outputs are MCP config additions, UI state transitions, OAuth result, and rendered components.
- gates_or_invariants: Transport/auth combinations must be valid; display width capped; secrets routed to env/header as chosen; scope controls user/project write target.
- dependencies_and_callers: Used by MCP setup/add flows and interactive mode.
- edge_cases_or_failure_modes: Invalid URL/command, missing env var name/header, OAuth cancellation, narrow terminal, duplicate server name.
- validation_or_tests: MCP wizard/setup tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3160 `file` `packages/coding-agent/src/modes/components/user-message.ts`
- cursor: `[_]`
- core_role: TUI component for rendering user messages.
- algorithmic_behavior: Formats user content with theme, handles text/images/file mentions as appropriate, and produces transcript component output.
- inputs_outputs_state: Inputs are user message content and theme/display options. Outputs are TUI components.
- gates_or_invariants: User text must fit/sanitize for terminal rendering; images use shared image options.
- dependencies_and_callers: Used by interactive transcript rendering.
- edge_cases_or_failure_modes: Long user text, image/file content, terminal width.
- validation_or_tests: Transcript rendering tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3190 `file` `packages/coding-agent/src/modes/setup-wizard/wizard-overlay.ts`
- cursor: `[_]`
- core_role: Overlay controller/component for setup wizard scene sequencing.
- algorithmic_behavior: Runs splash, transition, scene, outro phases; centers/clamps/indents lines; generates dissolve frames with deterministic row noise; routes focus/key/mouse to active scene controller; advances scenes and persists completion.
- inputs_outputs_state: Inputs are scene list, interactive context, dimensions/time, key/mouse events. Outputs are overlay render frames, scene lifecycle calls, and final done state.
- gates_or_invariants: Minimum content width; scene margins; focus ownership; phase transitions timed; done phase removes overlay.
- dependencies_and_callers: Used by setup onboarding; depends on setup scenes, welcome logo, theme.
- edge_cases_or_failure_modes: No scenes, scene skip/done, narrow terminal, rapid events during transitions, controller disposal.
- validation_or_tests: `setup-wizard.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3220 `file` `packages/coding-agent/src/tools/browser/tab-supervisor.ts`
- cursor: `[_]`
- core_role: Browser tab lifecycle supervisor for Puppeteer/headless and cmux-backed tabs.
- algorithmic_behavior: Serializes tab acquisition by name, spawns/initializes workers or cmux tabs, manages tab map/pending runs/dialog policy, runs code with snapshots/timeouts, dispatches session tool calls from worker, releases/force-kills/orphan-closes tabs, drops headless tabs, wraps Bun/inline workers, and maps worker error payloads.
- inputs_outputs_state: Inputs are tab name, browser handle, acquire/run/release options, worker messages, tool session, abort signals. Outputs are acquired page/session, run results/snapshots, released tab counts, worker messages, and errors. State includes `tabs`, acquire chains, pending run callbacks, worker handles.
- gates_or_invariants: One acquire chain per tab name; run requires existing tab; timeout races protect hung workers; last-surface close error handled; worker host entry fallback supported.
- dependencies_and_callers: Used by browser tools; depends on Puppeteer, cmux, tool bridge, worker host, logger.
- edge_cases_or_failure_modes: Worker init failure, browser target close, orphan targets, concurrent acquire/release, timeout, dialog handling, screenshot dir expansion, worker crash.
- validation_or_tests: Browser tool tests including cmux kind.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3250 `file` `packages/coding-agent/src/web/scrapers/hackernews.ts`
- cursor: `[_]`
- core_role: Special web scraper for Hacker News URLs.
- algorithmic_behavior: Detects HN item URLs, fetches Firebase API item/comment/story data, decodes HTML entities/text, formats timestamps, loads linked pages where applicable, and builds normalized render results.
- inputs_outputs_state: Inputs are URL, timeout, abort signal. Outputs are `RenderResult` with story/comment metadata/text.
- gates_or_invariants: Only HN URLs handled; API responses parsed safely; timestamps formatted; HTML text decoded.
- dependencies_and_callers: Used by web scraper dispatcher.
- edge_cases_or_failure_modes: Deleted/dead HN items, missing fields, API timeout, malformed JSON, nested comments, linked page load failure.
- validation_or_tests: Web scraper tests including business/HN-adjacent coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3280 `file` `packages/coding-agent/src/web/scrapers/rfc.ts`
- cursor: `[_]`
- core_role: Special web scraper for RFC documents.
- algorithmic_behavior: Extracts RFC number from URL, loads metadata/text, cleans RFC boilerplate/control text, parses JSON metadata when available, and builds normalized result.
- inputs_outputs_state: Inputs are RFC URL, timeout, abort signal. Outputs are cleaned RFC markdown/text render result.
- gates_or_invariants: Only recognized RFC paths handled; RFC number extraction must succeed; JSON metadata parse is optional/safe.
- dependencies_and_callers: Used by web scraper dispatcher.
- edge_cases_or_failure_modes: Unknown RFC URL shape, missing metadata, very large RFC text, malformed JSON.
- validation_or_tests: Web scraper tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3310 `file` `packages/coding-agent/test/extensibility/custom-commands/review.test.ts`
- cursor: `[_]`
- core_role: Tests custom command review behavior.
- algorithmic_behavior: Builds custom command fixtures, invokes review command flow, and asserts command parsing/rendering/execution contracts.
- inputs_outputs_state: Inputs are custom command definitions and simulated sessions. Outputs are command results/prompts/tool calls.
- gates_or_invariants: Review command must load extension command definitions and preserve expected args/context.
- dependencies_and_callers: Exercises extensibility custom commands and slash command integration.
- edge_cases_or_failure_modes: Missing command file, malformed command args, command shadowing, review output formatting.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3340 `file` `packages/coding-agent/test/modes/components/tree-selector-overflow.test.ts`
- cursor: `[_]`
- core_role: Tests tree selector overflow rendering.
- algorithmic_behavior: Constructs tree selector items with long labels/limited width and asserts render output truncates/fits.
- inputs_outputs_state: Inputs are tree items and terminal dimensions. Outputs are rendered lines.
- gates_or_invariants: Selector text must not overflow terminal/container width.
- dependencies_and_callers: Exercises setup/selector TUI component.
- edge_cases_or_failure_modes: Long labels, narrow width, nested tree indentation.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3370 `file` `packages/coding-agent/test/tools/web-scrapers/business.test.ts`
- cursor: `[_]`
- core_role: Tests business/news-style web scraper handling.
- algorithmic_behavior: Feeds representative business/news pages or fixtures into scraper and asserts cleaned extraction/render result.
- inputs_outputs_state: Inputs are URLs/HTML fixtures. Outputs are scraper result text/metadata.
- gates_or_invariants: Scraper must remove boilerplate and keep article-relevant content.
- dependencies_and_callers: Exercises web scraper dispatcher/special handlers.
- edge_cases_or_failure_modes: Paywall/boilerplate, missing metadata, malformed HTML.
- validation_or_tests: This file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3400 `file` `packages/collab-web/src/components/shell/HeaderBar.tsx`
- cursor: `[_]`
- core_role: Collab web header/status component.
- algorithmic_behavior: Renders session/project snapshot metadata, subagent count, rail toggle, leave action, percent/path formatting, and icons.
- inputs_outputs_state: Inputs are guest snapshot, subagent count, rail-open flag, toggle/leave callbacks. Outputs are React nodes and callback invocations.
- gates_or_invariants: Path/percent display uses shared formatting; buttons expose clear actions.
- dependencies_and_callers: Used by collab web shell; depends on lucide icons and format helpers.
- edge_cases_or_failure_modes: Missing snapshot fields, long paths, zero subagents, rail state mismatch.
- validation_or_tests: Collab web UI tests/build.
- skip_candidate: `yes: presentational UI component with light formatting, not core agent algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3430 `file` `packages/collab-web/src/tool-render/tools/search.tsx`
- cursor: `[_]`
- core_role: Collab web renderer for search tool calls/results.
- algorithmic_behavior: Extracts paths/pattern/counts from args/details, renders badges, invalid args, notes, summary, and result body text.
- inputs_outputs_state: Inputs are tool render props, args, result/details. Outputs are React nodes for summary/body.
- gates_or_invariants: Unknown arg types handled safely; paths shortened; result text extracted through shared util.
- dependencies_and_callers: Used by collab web tool-render registry.
- edge_cases_or_failure_modes: Missing pattern, invalid paths/count, empty result, unexpected details shape.
- validation_or_tests: Collab web renderer tests/build.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3460 `file` `packages/stats/src/client/data/formatters.ts`
- cursor: `[_]`
- core_role: Stats dashboard numeric/time formatting helpers.
- algorithmic_behavior: Formats integers, compact numbers, costs with digit rules, percents, durations, tokens/sec, and relative time.
- inputs_outputs_state: Inputs are numeric/timestamp values. Outputs are display strings.
- gates_or_invariants: Null durations/tokens return placeholder; costs use small-value precision; relative time delegates to date-fns.
- dependencies_and_callers: Used by stats routes/components.
- edge_cases_or_failure_modes: Null, zero, tiny costs, large counts, old/future timestamps.
- validation_or_tests: Stats UI/data tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3490 `file` `python/robomp/web/src/components/Browse.tsx`
- cursor: `[_]`
- core_role: Robomp web browse/search component.
- algorithmic_behavior: Maintains browse query/result/loading/error state, calls API, formats ages/status pills, triggers runs, and renders browse response cards.
- inputs_outputs_state: Inputs are UI filters/query actions and API responses. Outputs are React UI state, API calls, run triggers.
- gates_or_invariants: Empty response baseline; API errors surfaced distinctly; configured values from `CONFIG`; trigger actions routed through shared state.
- dependencies_and_callers: Used by robomp web app.
- edge_cases_or_failure_modes: API failure, empty results, stale loading state, trigger failure, long item text.
- validation_or_tests: Web app build/manual tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3520 `file` `packages/coding-agent/src/eval/js/shared/runtime.ts`
- cursor: `[_]`
- core_role: Shared JavaScript evaluation runtime.
- algorithmic_behavior: Creates helper/prelude environment, rewrites imports, evaluates code with async support, captures console/stdout/stderr through hooks, coerces display images/base64, loads local modules, manages global key ownership/snapshots to isolate concurrent runs, patches stdio once, and formats console args.
- inputs_outputs_state: Inputs are code, cwd/context, runtime hooks/options, helper calls, global/prelude keys. Outputs are run results, display/status events, captured logs, module results. State includes runtime globals, helper bundle, async local storage, global owner stacks.
- gates_or_invariants: Strict base64 detection avoids accidental image coercion; global key ownership prevents overlapping runtimes from corrupting global state; patched stdio routes only active run output.
- dependencies_and_callers: Used by JS eval executor/tool bridge and browser/tool runtime helpers.
- edge_cases_or_failure_modes: Concurrent evals, import rewrite errors, local module resolution, console formatting cycles, decimal CSV mistaken for base64, global restoration after error.
- validation_or_tests: JS eval/runtime tests and workflow/eval tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3550 `file` `packages/coding-agent/src/modes/components/status-line/segments.ts`
- cursor: `[_]`
- core_role: Status-line segment computation/render helpers.
- algorithmic_behavior: Builds model/session/git/cwd/task/usage/status segments, truncates/adapts to terminal width, applies theme colors/icons, and composes segment display metadata.
- inputs_outputs_state: Inputs are interactive context/session state, terminal width, theme, model/status values. Outputs are status line segments/strings.
- gates_or_invariants: Segments must fit available width; paths shortened; usage/model metadata optional-safe.
- dependencies_and_callers: Used by interactive status line component.
- edge_cases_or_failure_modes: Narrow terminal, missing git/model/session, long paths, high usage values.
- validation_or_tests: Status line/render tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3580 `file` `packages/coding-agent/src/web/search/providers/utils.ts`
- cursor: `[_]`
- core_role: Shared utilities for web search providers.
- algorithmic_behavior: Finds stored credentials for provider, creates hard-timeout abort signals, maps provider result documents to normalized search sources with age seconds, and classifies provider HTTP errors including quota/credit exhaustion.
- inputs_outputs_state: Inputs are agent storage, provider id, abort signal, raw search result fields, HTTP status/body. Outputs are credential, abort signal, normalized `SearchSource`s, and `SearchProviderError`.
- gates_or_invariants: Search hard timeout defaults to 60s; error classification distinguishes auth/quota/general failures; date conversion handles missing dates.
- dependencies_and_callers: Used by search provider implementations.
- edge_cases_or_failure_modes: Missing credential, already aborted signal, quota text variants, invalid dates, network timeouts.
- validation_or_tests: Web search provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3610 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/corners.ts`
- cursor: `[_]`
- core_role: Mermaid ASCII node-shape corner character lookup.
- algorithmic_behavior: Defines per-shape Unicode/ASCII corner character mappings and returns selected corners via `getCorners(shape, useAscii)`.
- inputs_outputs_state: Inputs are Mermaid ASCII node shape and ASCII/Unicode flag. Output is `CornerChars`.
- gates_or_invariants: Every supported `AsciiNodeShape` must have both ASCII and Unicode corner sets.
- dependencies_and_callers: Used by vendored Mermaid ASCII shape rendering.
- edge_cases_or_failure_modes: Unknown shape, missing mapping, ASCII/Unicode mismatch.
- validation_or_tests: Mermaid ASCII formatting/golden tests.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 121 item sections present: OH_MY_HUMANIZE_MAIN-HZ-010, OH_MY_HUMANIZE_MAIN-HZ-040, OH_MY_HUMANIZE_MAIN-HZ-070, OH_MY_HUMANIZE_MAIN-HZ-100, OH_MY_HUMANIZE_MAIN-HZ-130, OH_MY_HUMANIZE_MAIN-HZ-160, OH_MY_HUMANIZE_MAIN-HZ-190, OH_MY_HUMANIZE_MAIN-HZ-220, OH_MY_HUMANIZE_MAIN-HZ-250, OH_MY_HUMANIZE_MAIN-HZ-280, OH_MY_HUMANIZE_MAIN-HZ-310, OH_MY_HUMANIZE_MAIN-HZ-340, OH_MY_HUMANIZE_MAIN-HZ-370, OH_MY_HUMANIZE_MAIN-HZ-400, OH_MY_HUMANIZE_MAIN-HZ-430, OH_MY_HUMANIZE_MAIN-HZ-460, OH_MY_HUMANIZE_MAIN-HZ-490, OH_MY_HUMANIZE_MAIN-HZ-520, OH_MY_HUMANIZE_MAIN-HZ-550, OH_MY_HUMANIZE_MAIN-HZ-580, OH_MY_HUMANIZE_MAIN-HZ-610, OH_MY_HUMANIZE_MAIN-HZ-640, OH_MY_HUMANIZE_MAIN-HZ-670, OH_MY_HUMANIZE_MAIN-HZ-700, OH_MY_HUMANIZE_MAIN-HZ-730, OH_MY_HUMANIZE_MAIN-HZ-760, OH_MY_HUMANIZE_MAIN-HZ-790, OH_MY_HUMANIZE_MAIN-HZ-820, OH_MY_HUMANIZE_MAIN-HZ-850, OH_MY_HUMANIZE_MAIN-HZ-880, OH_MY_HUMANIZE_MAIN-HZ-910, OH_MY_HUMANIZE_MAIN-HZ-940, OH_MY_HUMANIZE_MAIN-HZ-970, OH_MY_HUMANIZE_MAIN-HZ-1000, OH_MY_HUMANIZE_MAIN-HZ-1030, OH_MY_HUMANIZE_MAIN-HZ-1060, OH_MY_HUMANIZE_MAIN-HZ-1090, OH_MY_HUMANIZE_MAIN-HZ-1120, OH_MY_HUMANIZE_MAIN-HZ-1150, OH_MY_HUMANIZE_MAIN-HZ-1180, OH_MY_HUMANIZE_MAIN-HZ-1210, OH_MY_HUMANIZE_MAIN-HZ-1240, OH_MY_HUMANIZE_MAIN-HZ-1270, OH_MY_HUMANIZE_MAIN-HZ-1300, OH_MY_HUMANIZE_MAIN-HZ-1330, OH_MY_HUMANIZE_MAIN-HZ-1360, OH_MY_HUMANIZE_MAIN-HZ-1390, OH_MY_HUMANIZE_MAIN-HZ-1420, OH_MY_HUMANIZE_MAIN-HZ-1450, OH_MY_HUMANIZE_MAIN-HZ-1480, OH_MY_HUMANIZE_MAIN-HZ-1510, OH_MY_HUMANIZE_MAIN-HZ-1540, OH_MY_HUMANIZE_MAIN-HZ-1570, OH_MY_HUMANIZE_MAIN-HZ-1600, OH_MY_HUMANIZE_MAIN-HZ-1630, OH_MY_HUMANIZE_MAIN-HZ-1660, OH_MY_HUMANIZE_MAIN-HZ-1690, OH_MY_HUMANIZE_MAIN-HZ-1720, OH_MY_HUMANIZE_MAIN-HZ-1750, OH_MY_HUMANIZE_MAIN-HZ-1780, OH_MY_HUMANIZE_MAIN-HZ-1810, OH_MY_HUMANIZE_MAIN-HZ-1840, OH_MY_HUMANIZE_MAIN-HZ-1870, OH_MY_HUMANIZE_MAIN-HZ-1900, OH_MY_HUMANIZE_MAIN-HZ-1930, OH_MY_HUMANIZE_MAIN-HZ-1960, OH_MY_HUMANIZE_MAIN-HZ-1990, OH_MY_HUMANIZE_MAIN-HZ-2020, OH_MY_HUMANIZE_MAIN-HZ-2050, OH_MY_HUMANIZE_MAIN-HZ-2080, OH_MY_HUMANIZE_MAIN-HZ-2110, OH_MY_HUMANIZE_MAIN-HZ-2140, OH_MY_HUMANIZE_MAIN-HZ-2170, OH_MY_HUMANIZE_MAIN-HZ-2200, OH_MY_HUMANIZE_MAIN-HZ-2230, OH_MY_HUMANIZE_MAIN-HZ-2260, OH_MY_HUMANIZE_MAIN-HZ-2290, OH_MY_HUMANIZE_MAIN-HZ-2320, OH_MY_HUMANIZE_MAIN-HZ-2350, OH_MY_HUMANIZE_MAIN-HZ-2380, OH_MY_HUMANIZE_MAIN-HZ-2410, OH_MY_HUMANIZE_MAIN-HZ-2440, OH_MY_HUMANIZE_MAIN-HZ-2470, OH_MY_HUMANIZE_MAIN-HZ-2500, OH_MY_HUMANIZE_MAIN-HZ-2530, OH_MY_HUMANIZE_MAIN-HZ-2560, OH_MY_HUMANIZE_MAIN-HZ-2590, OH_MY_HUMANIZE_MAIN-HZ-2620, OH_MY_HUMANIZE_MAIN-HZ-2650, OH_MY_HUMANIZE_MAIN-HZ-2680, OH_MY_HUMANIZE_MAIN-HZ-2710, OH_MY_HUMANIZE_MAIN-HZ-2740, OH_MY_HUMANIZE_MAIN-HZ-2770, OH_MY_HUMANIZE_MAIN-HZ-2800, OH_MY_HUMANIZE_MAIN-HZ-2830, OH_MY_HUMANIZE_MAIN-HZ-2860, OH_MY_HUMANIZE_MAIN-HZ-2890, OH_MY_HUMANIZE_MAIN-HZ-2920, OH_MY_HUMANIZE_MAIN-HZ-2950, OH_MY_HUMANIZE_MAIN-HZ-2980, OH_MY_HUMANIZE_MAIN-HZ-3010, OH_MY_HUMANIZE_MAIN-HZ-3040, OH_MY_HUMANIZE_MAIN-HZ-3070, OH_MY_HUMANIZE_MAIN-HZ-3100, OH_MY_HUMANIZE_MAIN-HZ-3130, OH_MY_HUMANIZE_MAIN-HZ-3160, OH_MY_HUMANIZE_MAIN-HZ-3190, OH_MY_HUMANIZE_MAIN-HZ-3220, OH_MY_HUMANIZE_MAIN-HZ-3250, OH_MY_HUMANIZE_MAIN-HZ-3280, OH_MY_HUMANIZE_MAIN-HZ-3310, OH_MY_HUMANIZE_MAIN-HZ-3340, OH_MY_HUMANIZE_MAIN-HZ-3370, OH_MY_HUMANIZE_MAIN-HZ-3400, OH_MY_HUMANIZE_MAIN-HZ-3430, OH_MY_HUMANIZE_MAIN-HZ-3460, OH_MY_HUMANIZE_MAIN-HZ-3490, OH_MY_HUMANIZE_MAIN-HZ-3520, OH_MY_HUMANIZE_MAIN-HZ-3550, OH_MY_HUMANIZE_MAIN-HZ-3580, OH_MY_HUMANIZE_MAIN-HZ-3610
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`

---

## Incremental Directory Refresh Addendum - oh-my-humanize/main bf4509d4f - OH_MY_HUMANIZE_MAIN-HZ-250

# agent_dir_05 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-250 `directory` `packages/coding-agent/src/cli`
- cursor: `[_]`
- current_directory_core_role:
  The `packages/coding-agent/src/cli` directory is the coding-agent command adapter layer. For workflows, `workflow-cli.ts` owns the non-TUI `omp workflow` execution surface: it normalizes command args, dispatches `list` / `freeze` / `start` / `install` / `uninstall`, resolves flow names or artifact paths relative to `--cwd` or `getProjectDir()`, loads and freezes `.omhflow` artifacts, constructs a headless workflow runtime host, maps lifecycle/run output into text or JSON, and converts known package/registry failures into concise stderr messages without stack traces. The command class in `src/commands/workflow.ts` lazy-loads this directory module and defines the public flags that become `WorkflowCommandArgs`.
- directory_level_delta_since_old_commit:
  The changed CLI responsibility is concentrated in headless `workflow start`. Start now treats the requested cwd as the execution cwd for JS workflow scripts, not only as a path-resolution base. `runHeadlessEvalScript(cwd, code, language)` temporarily calls `process.chdir(cwd)` around JS eval execution, captures `console.log`, formats returned values, and restores both `console.log` and the previous process cwd in `finally`. This aligns JS eval script behavior with shell and agent nodes, which already spawn with `cwd`.
  The CLI also now owns interrupt-to-abort wiring for headless starts. `handleStart` creates a `WorkflowStartSignalController` from `process` or an injected test signal target, passes the same signal as both `signal` and `nodeAbortSignal` into `runWorkflow`, and disposes listeners after the run completes. This makes SIGINT/SIGTERM stop both downstream scheduling and the currently running node, allowing lifecycle checkpointing rather than leaving a live or hanging headless attempt.
  Although `packages/coding-agent/src/workflow/runner.ts` is outside this assigned directory, the CLI delta depends on its new behavior: runner combines `maxRuntimeMs` deadlines with scheduler and node abort signals, treats aborted node execution as `aborted` rather than `failed`, creates stopped-attempt checkpoints for aborted/frontier state, and wraps node execution so ignored aborts still unblock after an abort checkpoint path.
- affected_descendant_algorithms:
  `resolveWorkflowCommandArgs` continues to map public CLI flags into typed workflow command flags, including `--cwd`, `--max-runtime-ms`, activation caps, run/family IDs, `--start`, `--json`, and `--force`.
  `handleStart` is the main affected algorithm: resolve cwd; resolve/load/freeze artifact; compute default root start nodes; create in-memory run store; build headless runtime host; create runtime binding snapshot; reject unavailable human/headless bindings unless `maxActivations === 0`; attach start signal; run `runWorkflow` with package root, frozen resources, activation limits, lifecycle metadata, max runtime, scheduler abort signal, and node abort signal; reconstruct run/family evidence; derive user-facing status; emit JSON or text.
  `createWorkflowStartSignalController` is a new/changed support algorithm for converting process `SIGINT`/`SIGTERM` events into a single abort reason string like `workflow interrupted by SIGINT`, while guaranteeing listener removal through `dispose`.
  `runHeadlessEvalScript` is now cwd-sensitive. It rejects Python eval scripts, runs JS code through `AsyncFunction`, captures console output and return values, and restores global process state even on script failure.
  The headless shell and agent task adapters remain part of the same start algorithm: shell uses `Bun.spawn(["sh", "-c", code], { cwd, signal, env: workflowScriptEnvironment(...) })`; agent task builds a nested CLI launch command with `--cwd`.
- current_inputs_outputs_state:
  Inputs are workflow action, target args, and flags from `omp workflow` / `omp flow`; `OMHFLOW_DIR` may affect named flow lookup; cwd defaults to `getProjectDir()` but may be overridden with `--cwd`.
  `list` outputs discovered flow specs as text or `{ flows }` JSON.
  `freeze` outputs freeze ID, graph/resource counts, and flow info as text or JSON.
  `install` / `uninstall` output installed/uninstalled flow metadata and use cwd for source resolution where relevant.
  `start` accepts only frozen distributable `.omhflow` artifacts for headless starts. It outputs run summary and frontier as text, or JSON with `flow`, `run`, `families`, and `runs`. The JSON run object includes status, activation counts, frontier node IDs, and effective `maxRuntimeMs`. Family JSON includes freezes, attempts, checkpoints, and change request summaries. Run JSON includes run IDs, activation counts, and sorted state keys.
  Runtime outputs from scripts/tasks are converted into workflow activation outputs through `createSessionWorkflowRuntimeHost`; state patches and single-write structured data then flow through the runner/state validation layer.
- new_or_changed_gates_or_invariants:
  Headless `workflow start` must use a `.omhflow` artifact path; raw workflow directories or `workflow.yml` packages are rejected with `Workflow start requires a frozen .omhflow artifact...`.
  Headless JS script relative file access is now invariantly relative to the requested run cwd during script execution. The process cwd must be restored afterward, and `console.log` capture must also be restored.
  SIGINT/SIGTERM listeners must be one-shot, must abort only once, and must be removed after `runWorkflow` settles.
  Headless start must pass an abort signal to both workflow scheduling and node execution so a signal can stop scheduling and abort in-flight shell/agent/script work.
  Default max runtime remains applied at the CLI boundary: `command.flags.maxRuntimeMs ?? DEFAULT_WORKFLOW_MAX_RUNTIME_MS`.
  Known `WorkflowArtifactRegistryError` and `WorkflowPackageError` failures remain user-facing stderr messages with `process.exitCode = 1`, not stack traces.
  A binding availability gate still prevents headless starts for human-node flows, except the explicit `maxActivations === 0` path can bypass execution-time binding failure.
- dependencies_and_callers:
  Public caller: `packages/coding-agent/src/commands/workflow.ts` defines the `workflow` command and `flow` alias, parses flags through the command framework, then calls `resolveWorkflowCommandArgs(...)` and `runWorkflowCommand(...)`.
  Workflow CLI depends on `artifact-registry` for list/resolve/install/uninstall, `package-loader` and `freeze` for artifact loading/freezing, `runtime-binding` for headless capability checks, `session-runtime` for adapting workflow nodes to CLI shell/eval/task runners, `runner` for scheduler/lifecycle execution, and `run-store`/`lifecycle` reconstruction for output evidence.
  The new signal behavior depends on `runWorkflow` honoring `signal`, `nodeAbortSignal`, and `maxRuntimeMs`. Runner now combines CLI interrupt signals with deadline signals and reports aborted activations/checkpoints in lifecycle state.
  Headless shell execution depends on Bun process spawning and `workflowScriptEnvironment`; headless JS eval depends on process-wide cwd and console overrides, so it is intentionally serialized within one eval call and restored in `finally`.
- edge_cases_or_failure_modes:
  A JS workflow script that reads relative paths with `Bun.file("...")` previously risked reading from the parent process cwd; it now reads from `--cwd`. Failure mode remains that `process.chdir(cwd)` will fail if the cwd does not exist or is inaccessible, returning an eval error result.
  Because JS eval changes process cwd and `console.log` globally during execution, concurrent in-process headless JS evals would contend for process-global state. The current CLI start path runs within one headless workflow invocation, but this remains a relevant concurrency caution for future parallel eval execution.
  If a workflow node runtime ignores abort, runner-side abort wrapping is required so CLI SIGINT/deadline can still checkpoint instead of hanging forever.
  If SIGINT/SIGTERM arrives after listeners are disposed, the workflow run is unaffected by this controller. If both arrive, only the first abort reason is preserved.
  For shell nodes, abort depends on Bun spawn signal behavior; nonzero exit maps stderr or `exit code N` into workflow node failure unless the runner observes the abort signal and records an aborted activation.
  Human-node flows are still unavailable in headless CLI and surface as binding errors rather than attempting interaction.
  `WorkflowPackageError` from non-artifact starts is intentionally caught and printed without source stack traces.
- validation_or_tests:
  `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts` now includes a cwd contract test: a frozen JS workflow script reads `marker.txt` from a separate requested `--cwd` workspace and must complete with state key `marker`.
  The same CLI test file includes a SIGINT checkpoint contract test: a fake signal target emits `SIGINT` while a shell script sleeps; JSON output must show run status `stopped`, frontier `["hold"]`, stopped family attempt, checkpoint frontier `["hold"]`, and zero remaining SIGINT/SIGTERM listeners.
  Existing CLI tests also pin stackless ambiguous flow/package errors, rejection of non-artifact headless starts, and frozen resource availability to headless shell scripts.
  Related runner tests in `packages/coding-agent/test/workflow/runner.test.ts` pin the lower-level contracts the CLI now relies on: cancellation checkpoints downstream scheduling, dedicated node abort signals remain separate from scheduler stop signals, deadline-aborted lifecycle activations are checkpointed instead of failing attempts, runtimes that ignore abort still unblock into an aborted checkpoint, and `maxRuntimeMs` creates stopped attempts with abort reason `workflow max runtime elapsed after 1ms`.
  I did not execute tests in this read-only research pass; evidence is from direct source inspection of the current export.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-250`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
