# agent_22 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-022 `directory` `crates/pi-shell`
- cursor: `[_]`
- core_role: Rust shell support crate for process-tree control and output minimization.
- algorithmic_behavior: Coordinates cross-platform process references in `src/process.rs`, shell planning/detection in `src/minimizer/{plan,detect,engine,pipeline}.rs`, reusable text reductions in `src/minimizer/primitives.rs`, and command-specific filters under `src/minimizer/filters/**`.
- inputs_outputs_state: Inputs are PIDs/process groups, shell commands, captured stdout/stderr, exit codes, and TOML filter definitions. Outputs are process status/termination results and `MinimizerOutput` objects that may preserve original text for artifacts.
- gates_or_invariants: Process cleanup avoids killing the harness PGID, validates live process identity, and re-walks descendants before hard-kill. Minimization refuses unsafe chains, pipes, compound commands, too-large captures, disabled programs, and filter panics.
- dependencies_and_callers: Uses `libc`/platform process primitives, `tokio`, `serde`, `regex`, `toml`, built-in `defs/*.toml`, and native filters. JS/Bun shell wrappers consume this crate through native bindings/runtime shell execution.
- edge_cases_or_failure_modes: PID reuse, kernels without `/proc/*/children`, inherited process groups, shell `exec`/`source`/`alias` state mutation, interleaved chain output, malformed TOML regexes, binary/huge output, and command parse failures.
- validation_or_tests: `crates/pi-shell/tests/minimizer_fixtures.rs` and fixture trees validate minimizer output. `src/process.rs` has regression tests around inherited harness PGIDs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-052 `file` `docs/mcp-protocol-transports.md`
- cursor: `[_]`
- core_role: Architecture documentation for MCP protocol/transport algorithms.
- algorithmic_behavior: Defines the split between JSON-RPC/MCP method handling and `MCPTransport`, including transport selection, request ID correlation, notification flow, stdio lifecycle, HTTP/SSE session behavior, timeout/cancel handling, and retry ownership.
- inputs_outputs_state: Inputs are MCP config transport type, JSON-RPC messages, stdio lines, HTTP/SSE frames, session headers, auth refresh, and manager/client requests. Outputs are correlated responses, notifications, tool bridge failures, reconnect decisions, and surfaced errors.
- gates_or_invariants: Request IDs must correlate to pending promises; malformed payloads are isolated; transport-level reconnect is separate from manager/tool retry; HTTP errors preserve status/body; stdio disconnect/failure transitions are explicit.
- dependencies_and_callers: References implementation files in MCP protocol/client/manager/transport layers and documents boundaries consumed by `packages/coding-agent/src/mcp/**`.
- edge_cases_or_failure_modes: Malformed JSON, cancelled requests, backpressure, SSE disconnects, auth refresh failures, transport close, and retry loops at the wrong layer.
- validation_or_tests: Documentation sections at `docs/mcp-protocol-transports.md:59`, `:68`, `:104`, `:155`, and `:236` identify contracts for corresponding MCP tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-082 `file` `scripts/analyze_small_edits.py`
- cursor: `[_]`
- core_role: Session-log workflow analysis script for edit/ast_edit behavior.
- algorithmic_behavior: Parses recent tool invocations, builds completed edit records, summarizes diffs, classifies small successful edits and failure modes, tracks adjacency to prior edits, and reservoir-samples candidates for review.
- inputs_outputs_state: Inputs are `.omp/agent/sessions` logs via `tool_io`, CLI limits, `edit`/`ast_edit` invocations, result text, diffs, timestamps, and path hints. Outputs are JSON or console stats, top issue counts, and random samples.
- gates_or_invariants: Positive integer CLI args are enforced; unresolved invocations are ignored; small edits are limited to <=2 changed lines or <=4 tiny structural lines; failure classification uses regex categories.
- dependencies_and_callers: Depends on `scripts/tool_io.py` types and reservoir sampling; intended as an offline diagnostic script rather than runtime agent path.
- edge_cases_or_failure_modes: Missing diff, no result, blank-line-only changes, context mismatch, invalid patch shape, ambiguous targets, missing files, and JSON/text output modes.
- validation_or_tests: Internal pure functions around `summarize_diff`, `classify_*`, and `analyze_small_edits` are testable; no assigned direct test file observed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-112 `file` `scripts/setup-npm-trust.ts`
- cursor: `[_]`
- core_role: Release/setup workflow script for configuring npm trusted publishing.
- algorithmic_behavior: Collects publish package names, includes generated native leaf packages, checks npm version/login, optionally lists/dry-runs, bootstraps missing native placeholders, revokes old trust configs under `--force`, then runs `npm trust github`.
- inputs_outputs_state: Inputs are CLI flags, package manifests, native `LEAF_TARGETS`, `ci-release-publish.ts` package list, npm registry state, repo/workflow values, and interactive npm auth. Outputs are trust configurations, placeholder publishes, and summary counts.
- gates_or_invariants: Requires npm >= `11.16.0`; non-native missing packages are not bootstrapped; native placeholders use inert `0.0.0`; `--only` unmatched names warn; failed package operations drive nonzero exit.
- dependencies_and_callers: Uses Bun shell/spawn, `node:fs/promises`, `node:os`, generated native target list, and release package metadata.
- edge_cases_or_failure_modes: Multiple JSON objects from `npm trust list`, delayed npm visibility after placeholder publish, failed revoke, failed 2FA/login, invalid package subset, and missing workflow file warning.
- validation_or_tests: Behavior is self-validating through registry/npm exit codes; no assigned direct unit test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-142 `directory` `packages/mnemopi/test`
- cursor: `[_]`
- core_role: Contract test suite for mnemopi memory algorithms and provider parity.
- algorithmic_behavior: Recursively covers Beam memory store/recall/consolidation, SHMR harmonization, embeddings/vector indexes, temporal parsing/recall, MCP/provider tools, DeltaSync, CLI parity, content sanitization, plugin manager, graph tools, veracity, recovery, and feature flags.
- inputs_outputs_state: Inputs are in-memory/SQLite memory stores, synthetic memories, embeddings, LLM extraction stubs, CLI args, MCP requests, provider handlers, and env feature toggles. Outputs are stored facts/events, recall rankings, diagnostics, migrations, CLI text/JSON, and sync deltas.
- gates_or_invariants: Tests lock contracts around duplicate handling, vector fallback, allowed DeltaSync tables/columns, embedding failure logging, provider all-tools parity, import cleanup, and concurrency/id collision behavior.
- dependencies_and_callers: Exercises `packages/mnemopi/src/**`, especially `core/beam/store.ts` and `core/shmr.ts`, plus CLI/MCP/provider surfaces.
- edge_cases_or_failure_modes: Missing embeddings, multilingual ordering, orphan vector episodes, SQLite recovery, sibling write races, cache synonym expansion, bad content/data URIs, and optional local LLM/fastembed availability.
- validation_or_tests: Test names include `beam-store`, `beam-recall-unit`, `shmr`, `mcp-server`, `provider-all-15-tools`, `recovery`, `c25-deltasync-allowlist`, and `issue-1832-embedding-population`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-172 `file` `docs/toolconv/deepseek.md`
- cursor: `[_]`
- core_role: Wire-format specification for DeepSeek tool calling.
- algorithmic_behavior: Documents special Unicode control tokens, role/turn structure, tool definitions, tool call/result syntax, parallel calls, OpenAI-compatible mapping, parser gotchas, version differences, and DSML envelope handling.
- inputs_outputs_state: Inputs are rendered transcript messages, tools, tool results, DeepSeek special tokens, DSML invoke/parameter tags, and OpenAI-compatible request/response fields. Outputs are in-band tool-call text and parsed tool call/result objects.
- gates_or_invariants: Must preserve unusual fullwidth Unicode tokens; parser must support legacy and DSML variants; multiple calls and result ordering are documented; malformed/incomplete control tokens require careful scanning.
- dependencies_and_callers: Paired with `packages/ai/src/dialect/deepseek.ts`, whose scanner constants match the documented tokens.
- edge_cases_or_failure_modes: ASCII substitution of special tokens, partial streamed suffixes, multiple tool calls, version-specific DSML changes, JSON repair needs, and in-band thinking/tool-call collisions.
- validation_or_tests: Documentation headings at `docs/toolconv/deepseek.md:39`, `:137`, `:163`, `:261`, and `:344` map to scanner/render contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-202 `file` `docs/tools/search_tool_bm25.md`
- cursor: `[_]`
- core_role: Architecture documentation for deferred tool discovery using BM25.
- algorithmic_behavior: Specifies source metadata, inputs, outputs, flow, modes, side effects, caps, and errors for search over deferred tool metadata.
- inputs_outputs_state: Inputs are natural-language search query, optional limit, and deferred tool metadata. Outputs are ranked tool descriptions exposed for the next model call.
- gates_or_invariants: Limits/caps bound result count; errors are surfaced when metadata/search cannot complete; side effects are limited to exposing matching tools, not executing them.
- dependencies_and_callers: Corresponds to the `tool_search` tool surface used to discover deferred multi-agent tools.
- edge_cases_or_failure_modes: Empty queries, no matches, invalid limits, metadata unavailable, or rank ties.
- validation_or_tests: Spec sections at `docs/tools/search_tool_bm25.md:15`, `:22`, `:44`, `:83`, and `:103`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-232 `directory` `packages/ai/src/auth-gateway`
- cursor: `[_]`
- core_role: Provider-format HTTP gateway that injects stored auth and translates request/response formats through pi-ai.
- algorithmic_behavior: `http.ts` centralizes JSON/CORS/auth/header capture/cache-key resolution; `server.ts` routes `/v1/chat/completions`, `/v1/messages`, `/v1/responses`, `/v1/models`, `/v1/usage`, and credential checks; `types.ts` defines parsed request/options and format-module contracts.
- inputs_outputs_state: Inputs are HTTP requests, bearer tokens, provider-format bodies/headers, model registry resolution, AuthStorage credentials, and abort signals. Outputs are provider-format JSON/SSE responses, usage snapshots, model lists, and classified error envelopes.
- gates_or_invariants: Bearer auth uses constant-time token comparison; CORS is explicit; unsupported Codex sampling fields are dropped rather than rejected; prompt cache key precedence is body metadata then headers then derived UUID.
- dependencies_and_callers: Uses provider server modules, `streamSimple`, model catalog effort types, AuthStorage, `parseBind`, and logger.
- edge_cases_or_failure_modes: Missing/invalid auth, unsupported model, provider errors with embedded statuses, usage-limit phrasing misclassification, aborted requests, and no configured credentials.
- validation_or_tests: Covered indirectly by auth/gateway provider tests such as cache-affinity and OAuth storage tests; key functions at `http.ts:15`, `server.ts:64`, `server.ts:104`, `server.ts:179`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-262 `directory` `packages/coding-agent/src/export`
- cursor: `[_]`
- core_role: Conversation export/share subsystem.
- algorithmic_behavior: `share.ts` serializes sessions for sharing; `ttsr.ts` exports transcript/session records; `html/index.ts` builds static HTML using bundled templates/assets; `custom-share.ts` discovers user share hooks; `html/template.*` and vendored libs render the offline viewer.
- inputs_outputs_state: Inputs are session entries/header, HTML templates, custom share scripts, generated export path, and static assets. Outputs are HTML export files, share results, and optional custom share URLs/messages.
- gates_or_invariants: Custom hook search is restricted to candidate names; static export bundles local JS/CSS/vendor assets; template rendering must preserve transcript fidelity and avoid missing assets.
- dependencies_and_callers: Called by CLI export/share commands; uses Bun text imports/static files, session serializers, and optional project/global share hook.
- edge_cases_or_failure_modes: Missing custom hook, malformed hook return, unavailable share target, missing session data, and HTML asset path issues.
- validation_or_tests: No direct assigned test; export HTML is validated by static template inclusion and custom hook loader behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-292 `directory` `packages/coding-agent/test/capability`
- cursor: `[_]`
- core_role: Capability-system regression tests.
- algorithmic_behavior: `fs-special-files.test.ts` checks read behavior for special files; `rule-buckets.test.ts` checks rule bucketing behavior.
- inputs_outputs_state: Inputs are filesystem special paths/rules; outputs are read results and grouped rule buckets.
- gates_or_invariants: Special-file reads should not hang or corrupt capability decisions; rule bucketing must preserve expected grouping semantics.
- dependencies_and_callers: Exercises coding-agent capability modules that feed discovery/rule selection and filesystem tools.
- edge_cases_or_failure_modes: Device/special files, unreadable paths, and rule metadata combinations.
- validation_or_tests: `describe("capability/fs readFile on special files")` at `fs-special-files.test.ts:9`; `describe("bucketRules")` at `rule-buckets.test.ts:26`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-322 `directory` `packages/collab-web/src/lib`
- cursor: `[_]`
- core_role: Browser-side collab protocol/client library.
- algorithmic_behavior: Implements AES-GCM sealing/opening (`codec.ts`), envelope/link parsing (`link.ts`), ordered reconnecting socket transport (`socket.ts`), guest replica state machine (`client.ts`), incremental JSONL parsing, formatting helpers, and React external-store hook.
- inputs_outputs_state: Inputs are collab links, room keys, WebSocket binary/text messages, sealed frames, host snapshots/events/state/bus traffic, prompts, aborts, agent commands, transcript requests. Outputs are guest snapshots, sealed outgoing frames, parsed transcripts, notices, and UI-formatted values.
- gates_or_invariants: Room key must be 32 bytes; sealed frame must include IV+ciphertext; send/receive chains preserve order; fatal close codes do not reconnect; pending sends cap at 256; welcome timeout is 30s.
- dependencies_and_callers: Used by `packages/collab-web` React/Solid components; mirrors CLI collab protocol in `packages/coding-agent/src/collab/protocol.ts`.
- edge_cases_or_failure_modes: Bad key/corrupted frame, room missing/closed/full, host conflict, malformed control JSON, reconnect races, transcript timeout, read-only links, and welcome apply failure.
- validation_or_tests: Contracts are mirrored by local relay and collab protocol behavior; no assigned direct `collab-web/src/lib` test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-352 `file` `crates/pi-natives/src/block.rs`
- cursor: `[_]`
- core_role: N-API bridge for tree-sitter block-range algorithms.
- algorithmic_behavior: Exposes `block_range_at` and `enclosing_block_boundaries` by converting JS-facing options into `pi_ast::block` options and mapping errors to N-API `Error`.
- inputs_outputs_state: Inputs are source code, optional language/path, target line, and visible line ranges. Outputs are optional inclusive block ranges or boundary line lists.
- gates_or_invariants: Returns `null` for unrecognized language, out-of-range/blank lines, no named node, syntax errors, or parse failure; uses 1-indexed inclusive lines.
- dependencies_and_callers: Depends on `pi_ast::block`; called by JS native package for read/render block context.
- edge_cases_or_failure_modes: Unknown extension/language, syntax-error subtrees, blank lines, overlapping visible ranges, and indentation-language boundaries.
- validation_or_tests: Native block behavior is covered by read/multi-range and native tests elsewhere; key exports at `block.rs:38` and `block.rs:80`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-382 `file` `crates/pi-shell/src/process.rs`
- cursor: `[_]`
- core_role: Cross-platform process tree management.
- algorithmic_behavior: Opens stable process references, enumerates children/descendants, reads args/parent/group IDs, sends process/tree/group signals, terminates with graceful/hard waves, tracks new descendants relative to a baseline, and classifies safe termination targets.
- inputs_outputs_state: Inputs are PIDs, executable paths, signals, process group flag, graceful/timeout durations, and cancellation tokens. Outputs are `ProcessStatus`, signaled counts, termination success booleans, descendant PID sets, and `TerminationTargets`.
- gates_or_invariants: Linux uses pidfd identity checks and `/proc` fallback; process group kill refuses own PGID; target selection only adopts PGID when group leader is a new descendant; termination re-walks after grace.
- dependencies_and_callers: Used by shell/PTY/job cleanup and cancellation; depends on platform modules, `libc`, `tokio`, and `CancelToken`.
- edge_cases_or_failure_modes: PID reuse, EINTR polling, child forked from worker threads, missing `CONFIG_PROC_CHILDREN`, reparenting during grace, Windows lack of POSIX signals, inherited harness PGID.
- validation_or_tests: Regression tests at `process.rs:1694` cover inherited harness PGID selection; public functions at `process.rs:1274`, `:1468`, `:1511`, `:1550`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-412 `file` `packages/agent/test/shake.test.ts`
- cursor: `[_]`
- core_role: Tests transcript “shake” region selection and application.
- algorithmic_behavior: Builds synthetic session entries/messages/tool results, tests collection of removable/condensable regions for tool results, fenced blocks, XML blocks, useless results, and applies multi-region ordering.
- inputs_outputs_state: Inputs are `SessionMessageEntry`, assistant/tool messages, approximate token blocks, and `ShakeConfig`. Outputs are collected shake regions and transformed transcript content.
- gates_or_invariants: Token thresholds, region ordering, useless result detection, and config presets must avoid corrupting message structure.
- dependencies_and_callers: Exercises `collectShakeRegions`, `applyShakeRegions`, and shake config preset behavior in `packages/agent`.
- edge_cases_or_failure_modes: Large fenced/XML blocks, repeated tool results, multi-region overlaps/order, and useless result classification.
- validation_or_tests: Suites at `shake.test.ts:72`, `:121`, `:188`, `:206`, `:223`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-442 `file` `packages/ai/test/anthropic-mid-conversation-system.test.ts`
- cursor: `[_]`
- core_role: Tests Anthropic conversion of mid-conversation system/developer messages.
- algorithmic_behavior: Constructs Anthropic model specs and message sequences, then verifies system/developer prompt handling across turns.
- inputs_outputs_state: Inputs are user/developer/assistant messages and Anthropic model metadata. Outputs are converted Anthropic request payloads.
- gates_or_invariants: Anthropic system messages cannot appear in arbitrary mid-conversation positions; converter must preserve intended instruction content without invalid wire structure.
- dependencies_and_callers: Exercises Anthropic messages provider conversion.
- edge_cases_or_failure_modes: Developer messages after assistant turns, cross-model assistant history, and system prompt placement.
- validation_or_tests: `describe("Anthropic mid-conversation system messages")` at `anthropic-mid-conversation-system.test.ts:59`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-472 `file` `packages/ai/test/auth-storage-antigravity-selection.test.ts`
- cursor: `[_]`
- core_role: Tests Google Antigravity OAuth credential ranking in AuthStorage.
- algorithmic_behavior: Builds usage-limit windows/reports and credentials, then verifies account/project selection prioritizes usable Antigravity credentials.
- inputs_outputs_state: Inputs are `UsageLimit` windows, project IDs, account emails, OAuth credential records, and current time windows. Outputs are ranked/selected credentials.
- gates_or_invariants: Exceeded or cooling-down usage windows must lower priority; project/account association matters; stale/usable windows are compared consistently.
- dependencies_and_callers: Exercises `AuthStorage` selection logic for google-antigravity provider.
- edge_cases_or_failure_modes: Multiple projects, reset windows, expired windows, missing reports, and equal candidates.
- validation_or_tests: Suite at `auth-storage-antigravity-selection.test.ts:84`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-502 `file` `packages/ai/test/event-stream.test.ts`
- cursor: `[_]`
- core_role: Tests `AssistantMessageEventStream` behavior.
- algorithmic_behavior: Creates partial assistant messages and asserts stream event handling for assistant message deltas/completion.
- inputs_outputs_state: Inputs are synthetic partial assistant messages and pushed stream events. Outputs are stream consumers’ observed events/messages.
- gates_or_invariants: Partial message object shape and event order must remain stable.
- dependencies_and_callers: Exercises `packages/ai/src/utils/event-stream`.
- edge_cases_or_failure_modes: Empty partial text and done/error event consistency.
- validation_or_tests: `describe("AssistantMessageEventStream")` at `event-stream.test.ts:25`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-532 `file` `packages/ai/test/issue-1227-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for LiteLLM→Bedrock tool-history conversion.
- algorithmic_behavior: Captures provider payload for a Bedrock-style OpenAI completions model with assistant tool calls and tool results, reproducing `/btw` failure conditions.
- inputs_outputs_state: Inputs are Bedrock model spec, aborted signal helper, assistant tool-call history, and echo tool definition. Outputs are captured request payloads.
- gates_or_invariants: Tool-call histories must serialize into a Bedrock-compatible shape and not break after mid-conversation additions.
- dependencies_and_callers: Exercises OpenAI completions conversion and tool history normalization.
- edge_cases_or_failure_modes: Tool result pairing, aborted requests, and provider-specific LiteLLM Bedrock quirks.
- validation_or_tests: Suite at `issue-1227-repro.test.ts:84`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-562 `file` `packages/ai/test/minimax-code-login.test.ts`
- cursor: `[_]`
- core_role: Tests MiniMax Token Plan login provider wiring.
- algorithmic_behavior: Verifies login provider definition/flow for MiniMax code plan.
- inputs_outputs_state: Inputs are OAuth login callbacks/provider registry. Outputs are provider login invocation/credentials.
- gates_or_invariants: Provider ID/name and lazy login wiring must resolve to the expected MiniMax OAuth flow.
- dependencies_and_callers: Exercises `packages/ai/src/registry/minimax-code-cn.ts` and OAuth provider registry.
- edge_cases_or_failure_modes: Missing provider, failed lazy module resolution, and credential propagation.
- validation_or_tests: Suite at `minimax-code-login.test.ts:5`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-592 `file` `packages/ai/test/openai-responses-cache-affinity.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI Responses prompt-cache/session affinity.
- algorithmic_behavior: Creates SSE responses, captures dispatched headers/options for OpenAI, OpenRouter, and xAI OAuth responses models, and checks cache-key/session behavior.
- inputs_outputs_state: Inputs are model specs, request contexts, fetch captures, and stream events. Outputs are request headers and dispatched OpenAI Responses payload metadata.
- gates_or_invariants: Prompt cache keys must flow consistently into headers/options and be provider-compatible.
- dependencies_and_callers: Exercises OpenAI Responses provider and auth-gateway cache-affinity behavior.
- edge_cases_or_failure_modes: OpenRouter Responses models, xAI OAuth routing, missing cache key, and SSE finish handling.
- validation_or_tests: Suite at `openai-responses-cache-affinity.test.ts:183`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-622 `file` `packages/ai/test/schema-arktype.test.ts`
- cursor: `[_]`
- core_role: Tests ArkType schema detection, wire emission, and argument validation.
- algorithmic_behavior: Defines ArkType-backed tools, verifies schema recognition, converts ArkType to wire schema, and validates accepted/rejected tool arguments.
- inputs_outputs_state: Inputs are ArkType schemas, `Tool` objects, and tool argument objects. Outputs are JSON-schema-like wire schemas and validation results/errors.
- gates_or_invariants: Required fields, rejected values, and ArkType metadata must be honored without widening validation.
- dependencies_and_callers: Exercises `arkToWireSchema`, `isArkSchema`, and `validateToolArguments`.
- edge_cases_or_failure_modes: Invalid arguments, type refinements, empty descriptions, and schema emission differences.
- validation_or_tests: Suites at `schema-arktype.test.ts:33`, `:49`, `:99`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-652 `file` `packages/ai/test/xiaomi-oauth.test.ts`
- cursor: `[_]`
- core_role: Tests Xiaomi OAuth validation behavior.
- algorithmic_behavior: Verifies provider-specific OAuth credential/validation logic.
- inputs_outputs_state: Inputs are OAuth-like values and validation paths. Outputs are success/failure assertions.
- gates_or_invariants: Invalid Xiaomi auth state should be rejected; valid provider contract should be accepted.
- dependencies_and_callers: Exercises Xiaomi OAuth registry/helpers.
- edge_cases_or_failure_modes: Missing tokens, malformed responses, and provider mismatch.
- validation_or_tests: Suite at `xiaomi-oauth.test.ts:5`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-682 `file` `packages/catalog/test/hosts.test.ts`
- cursor: `[_]`
- core_role: Tests model host/endpoint matching predicates.
- algorithmic_behavior: Asserts host matching, model-to-host matching, and endpoint-shape predicates.
- inputs_outputs_state: Inputs are URLs/hosts/model descriptors. Outputs are boolean match decisions.
- gates_or_invariants: Host matching must avoid false positives while accepting intended provider endpoints.
- dependencies_and_callers: Exercises catalog host utilities used by provider discovery/resolution.
- edge_cases_or_failure_modes: Subdomain vs suffix confusion, endpoint shape differences, and host normalization.
- validation_or_tests: Suites at `hosts.test.ts:10`, `:29`, `:42`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-712 `file` `packages/catalog/test/zenmux-provider.test.ts`
- cursor: `[_]`
- core_role: Tests ZenMux provider catalog support.
- algorithmic_behavior: Temporarily manages `ZENMUX_API_KEY` env and validates provider availability/model behavior.
- inputs_outputs_state: Inputs are environment variables and catalog provider descriptors. Outputs are provider support assertions.
- gates_or_invariants: Env mutation is restored; provider entry must resolve only under expected conditions.
- dependencies_and_callers: Exercises catalog provider descriptors/resolution for ZenMux.
- edge_cases_or_failure_modes: Missing API key, stale env, and provider descriptor drift.
- validation_or_tests: Suite at `zenmux-provider.test.ts:19`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-742 `file` `packages/coding-agent/test/acp-lazy-startup.test.ts`
- cursor: `[_]`
- core_role: Tests ACP lazy startup behavior.
- algorithmic_behavior: Uses fake client/session/transport to verify ACP startup does not eagerly instantiate heavy session state until needed.
- inputs_outputs_state: Inputs are fake workspace tree, ACP client calls, model fixture, and writable transport close. Outputs are lifecycle/startup assertions.
- gates_or_invariants: ACP server should defer session creation; transport close should cleanly terminate; model and workspace data remain available when later requested.
- dependencies_and_callers: Exercises ACP server/session startup path.
- edge_cases_or_failure_modes: Premature session creation, transport close races, and missing workspace tree.
- validation_or_tests: Suite at `acp-lazy-startup.test.ts:158`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-772 `file` `packages/coding-agent/test/agent-session-model-persistence.test.ts`
- cursor: `[_]`
- core_role: Tests agent session model persistence.
- algorithmic_behavior: Verifies selected model information survives session save/reopen or state transitions.
- inputs_outputs_state: Inputs are session creation/options and model metadata. Outputs are persisted session records and restored model state.
- gates_or_invariants: Session model changes must be written in stable format and not lost across lifecycle operations.
- dependencies_and_callers: Exercises `AgentSession` and `SessionManager` persistence.
- edge_cases_or_failure_modes: Default model fallback, missing model metadata, and resumed sessions.
- validation_or_tests: Suite at `agent-session-model-persistence.test.ts:16`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-802 `file` `packages/coding-agent/test/autolearn-controller.test.ts`
- cursor: `[_]`
- core_role: Tests AutoLearn controller and instruction generation.
- algorithmic_behavior: Uses fake session/settings to verify learning nudges, event handling, cooldowns/thresholds, and rendered instructions.
- inputs_outputs_state: Inputs are captured nudges, fake session events, settings overrides, and action histories. Outputs are queued nudges/instructions.
- gates_or_invariants: Controller should not spam; settings should gate behavior; generated instructions must include the right memory/learning content.
- dependencies_and_callers: Exercises AutoLearn controller and `buildAutoLearnInstructions`.
- edge_cases_or_failure_modes: Disabled settings, repeated triggers, missing session state, and instruction formatting.
- validation_or_tests: Suites at `autolearn-controller.test.ts:66` and `:236`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-832 `file` `packages/coding-agent/test/compaction-lifecycle.test.ts`
- cursor: `[_]`
- core_role: Tests UI lifecycle around compaction execution.
- algorithmic_behavior: Builds interactive context around a compact function and checks lifecycle state changes while compaction runs/completes.
- inputs_outputs_state: Inputs are fake session compact callbacks and UI context. Outputs are lifecycle flags/render updates.
- gates_or_invariants: UI should show compaction progress and clear/transition correctly after completion or failure.
- dependencies_and_callers: Exercises interactive mode compaction orchestration.
- edge_cases_or_failure_modes: Compact promise rejection, missing session compact, and stale UI state.
- validation_or_tests: Suite at `compaction-lifecycle.test.ts:63`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-862 `file` `packages/coding-agent/test/file-mentions.test.ts`
- cursor: `[_]`
- core_role: Tests file mention path resolution.
- algorithmic_behavior: Creates temp dirs/files and verifies generated file mention messages resolve paths correctly.
- inputs_outputs_state: Inputs are cwd, file mention strings, temp paths. Outputs are mention messages and resolved content/path metadata.
- gates_or_invariants: Path resolution must stay within expected cwd semantics and generate stable mention messages.
- dependencies_and_callers: Exercises `generateFileMentionMessages`.
- edge_cases_or_failure_modes: Relative paths, missing files, temp cleanup, and special path shapes.
- validation_or_tests: Suite at `file-mentions.test.ts:21`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-892 `file` `packages/coding-agent/test/input-controller-skill-queue.test.ts`
- cursor: `[_]`
- core_role: Tests queued custom/skill display state across input, session, UI helper, and event controller paths.
- algorithmic_behavior: Builds stub/real sessions, queues custom steers/advisor notes/companion notices/user steers, and verifies derived chip metadata and refresh behavior.
- inputs_outputs_state: Inputs are skill files, queued messages, streaming flag, editor stubs, and event controller fixtures. Outputs are chip labels, queued display metadata, and UI/event refresh results.
- gates_or_invariants: Skill queue chips must survive transcript rebuild paths and distinguish custom/advisor/user/magic companion messages without stale display.
- dependencies_and_callers: Exercises `InputController`, `AgentSession`, `UiHelpers`, and `EventController`.
- edge_cases_or_failure_modes: Streaming state, multiple queue types, stale derived display, real session persistence, and skill command mapping.
- validation_or_tests: Suites at `input-controller-skill-queue.test.ts:105`, `:276`, `:473`, `:543`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-922 `file` `packages/coding-agent/test/issue-825-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for steer preview after compaction.
- algorithmic_behavior: Uses fake session/context and queued compaction messages to reproduce stuck preview behavior.
- inputs_outputs_state: Inputs are queued compaction messages and prompt options. Outputs are prompt/preview state transitions.
- gates_or_invariants: After compaction, steer preview should clear/update rather than stay stuck.
- dependencies_and_callers: Exercises compaction queue/UI prompt interaction.
- edge_cases_or_failure_modes: Streaming behavior modes, queued message replay, and fake session state drift.
- validation_or_tests: Suite at `issue-825-repro.test.ts:126`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-952 `file` `packages/coding-agent/test/lsp-render.test.ts`
- cursor: `[_]`
- core_role: Tests LSP diagnostic rendering.
- algorithmic_behavior: Verifies diagnostics are rendered into expected user-visible strings/layout.
- inputs_outputs_state: Inputs are diagnostic records. Outputs are rendered LSP strings/components.
- gates_or_invariants: Severity, path/range, and message formatting must remain stable.
- dependencies_and_callers: Exercises LSP renderer.
- edge_cases_or_failure_modes: Empty diagnostics, long messages, and formatting regressions.
- validation_or_tests: Suite at `lsp-render.test.ts:13`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-982 `file` `packages/coding-agent/test/model-discovery.test.ts`
- cursor: `[_]`
- core_role: Tests runtime model discovery.
- algorithmic_behavior: Verifies ModelRegistry discovers/merges runtime models from configured providers and environment.
- inputs_outputs_state: Inputs are registry config/env/provider discovery fixtures. Outputs are available model lists and resolution decisions.
- gates_or_invariants: Discovery should not duplicate models, should respect provider auth/config, and should preserve catalog identities.
- dependencies_and_callers: Exercises coding-agent ModelRegistry and catalog discovery integration.
- edge_cases_or_failure_modes: Missing keys, provider discovery failures, duplicate IDs, and custom config overlays.
- validation_or_tests: Suite at `model-discovery.test.ts:13`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1012 `file` `packages/coding-agent/test/read-multi-range.test.ts`
- cursor: `[_]`
- core_role: Tests read tool multi-range selector.
- algorithmic_behavior: Creates numbered file content and sessions, invokes read ranges, and checks text output for multiple line windows.
- inputs_outputs_state: Inputs are cwd/session, optional client bridge, numbered file contents, requested ranges. Outputs are `AgentToolResult<ReadToolDetails>` text.
- gates_or_invariants: Multi-range reads must preserve order, line numbering, truncation/formatting, and range boundaries.
- dependencies_and_callers: Exercises read tool and native block/boundary context helpers.
- edge_cases_or_failure_modes: Overlapping ranges, invalid ranges, empty files, and bridge interaction.
- validation_or_tests: Suite at `read-multi-range.test.ts:40`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1042 `file` `packages/coding-agent/test/sdk-session-isolation.test.ts`
- cursor: `[_]`
- core_role: Tests SDK session storage/environment isolation.
- algorithmic_behavior: Clears secret env patterns, builds TTSR rules, creates agent sessions, and verifies isolated storage/assistant output.
- inputs_outputs_state: Inputs are rule fixtures, environment variables, session creation calls. Outputs are assistant text and storage state assertions.
- gates_or_invariants: SDK sessions must not leak secrets or cross-contaminate storage/state.
- dependencies_and_callers: Exercises `createAgentSession` SDK surface.
- edge_cases_or_failure_modes: Secret env leakage, shared singleton state, and assistant message extraction.
- validation_or_tests: Suite at `sdk-session-isolation.test.ts:59`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1072 `file` `packages/coding-agent/test/status-line-cache-hit.test.ts`
- cursor: `[_]`
- core_role: Tests status-line cache-hit segment rendering.
- algorithmic_behavior: Builds segment contexts with usage stats and strips ANSI to verify text.
- inputs_outputs_state: Inputs are partial `usageStats`. Outputs are plain status-line segment strings.
- gates_or_invariants: Cache hit values should render only when meaningful and format consistently.
- dependencies_and_callers: Exercises status-line segment renderer.
- edge_cases_or_failure_modes: Missing usage, zero values, and ANSI styling.
- validation_or_tests: Suite at `status-line-cache-hit.test.ts:31`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1102 `file` `packages/coding-agent/test/tiny-device.test.ts`
- cursor: `[_]`
- core_role: Tests tiny model device selection.
- algorithmic_behavior: Verifies device setting maps to `PI_TINY_DEVICE` and selection behavior.
- inputs_outputs_state: Inputs are tiny model device settings and environment variables. Outputs are device mapping/env assertions.
- gates_or_invariants: User setting should map deterministically; unsupported/missing values should fall back safely.
- dependencies_and_callers: Exercises tiny inference configuration.
- edge_cases_or_failure_modes: CPU/GPU/device enum changes and env overrides.
- validation_or_tests: Suites at `tiny-device.test.ts:13` and `:40`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1132 `file` `packages/collab-web/scripts/local-relay.ts`
- cursor: `[_]`
- core_role: Offline WebSocket relay implementing the public collab relay contract.
- algorithmic_behavior: Serves `/r/<roomId>?role=host|guest`, creates rooms for hosts, assigns peer IDs to guests, forwards host envelopes by peer target/broadcast, rewrites guest envelopes to sender peer ID, emits peer control messages, and closes rooms on host disconnect.
- inputs_outputs_state: Inputs are WebSocket upgrade requests, binary envelopes, role query params, and optional `--port`. Outputs are forwarded binary frames, text control messages, close codes, and relay URL.
- gates_or_invariants: One host per room; guests cannot join missing rooms; room IDs match regex; guest frames shorter than 4 bytes ignored; stop closes all rooms.
- dependencies_and_callers: Uses Bun.serve and `src/lib/link` envelope helpers; used for local collab development/tests.
- edge_cases_or_failure_modes: Second host conflict `4009`, missing room `4004`, host close `4001`, invalid port, truncated envelopes.
- validation_or_tests: Contract documented in header and runtime checks in `startLocalRelay`; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1162 `file` `packages/hashline/test/boundary-repair.test.ts`
- cursor: `[_]`
- core_role: Tests boundary-balance patch repair.
- algorithmic_behavior: Applies diffs through `applyPatch` and verifies boundary repair and stale-snapshot recovery.
- inputs_outputs_state: Inputs are original text and diff strings. Outputs are repaired text plus warnings.
- gates_or_invariants: Patch application should preserve balanced structural boundaries or warn/repair deterministically.
- dependencies_and_callers: Exercises `packages/hashline/src` apply/repair algorithms.
- edge_cases_or_failure_modes: Stale snapshots, missing boundaries, malformed/context-shifted diffs, and warning propagation.
- validation_or_tests: Suites at `boundary-repair.test.ts:9` and `:347`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1192 `file` `packages/mnemopi/test/cli.test.ts`
- cursor: `[_]`
- core_role: Tests mnemopi CLI command handlers.
- algorithmic_behavior: Creates temp roots, captures output, invokes CLI handlers, and verifies command behavior.
- inputs_outputs_state: Inputs are CLI command args, temp data dirs, and captured stdout/stderr. Outputs are CLI text/state changes.
- gates_or_invariants: Commands should handle paths, state, and output consistently.
- dependencies_and_callers: Exercises mnemopi CLI layer.
- edge_cases_or_failure_modes: Missing data dir, command errors, and capture restoration.
- validation_or_tests: Suite at `cli.test.ts:32`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1222 `file` `packages/mnemopi/test/patterns.test.ts`
- cursor: `[_]`
- core_role: Tests memory compression and pattern detection.
- algorithmic_behavior: Feeds memory/text sequences into compression and pattern detection helpers and verifies semantic grouping/results.
- inputs_outputs_state: Inputs are memory entries/text snippets. Outputs are compressed memories and detected patterns.
- gates_or_invariants: Compression should preserve salient details; pattern detection should avoid false positives and identify recurring structure.
- dependencies_and_callers: Exercises mnemopi pattern utilities.
- edge_cases_or_failure_modes: Sparse inputs, repeated phrases, noise, and tiny corpora.
- validation_or_tests: Suites at `patterns.test.ts:9` and `:54`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1252 `file` `packages/natives/scripts/build-native.ts`
- cursor: `[_]`
- core_role: Native addon build/install pipeline for `pi-natives`.
- algorithmic_behavior: Resolves target platform/arch/x64 variant, sets Rust CPU flags, prepares napi build output dir, handles zigbuild target symlink, builds with napi, retries without sccache on storage failure, normalizes addon filename, strips/verifies ELF sections in CI, installs bindings, and generates enum exports.
- inputs_outputs_state: Inputs are env vars (`CROSS_TARGET`, `TARGET_*`, `CI`, `RUSTFLAGS`), host AVX2 detection, cargo metadata, napi binary, build artifacts. Outputs are `.node` addon, `index.d.ts`, generated enum exports, and console status.
- gates_or_invariants: x64 cross-builds require explicit variant; invalid variant throws; real target dirs are not clobbered; CI ELF must not contain `.symtab`, `.strtab`, `.debug_*`, `.zdebug_*`.
- dependencies_and_callers: Uses Bun shell, `@napi-rs/cli`, Rust crate `crates/pi-natives`, `scripts/host-detect`, and `gen-enums`.
- edge_cases_or_failure_modes: Missing napi binary, multiple/no generated addons, Windows loaded DLL replacement, cargo-zigbuild glibc suffix, unsupported ELF fields, sccache storage outage.
- validation_or_tests: Validated by build pipeline and smoke/install tests; core functions at `build-native.ts:31`, `:83`, `:113`, `:143`, `:226`, `:308`, `:391`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1282 `file` `packages/snapcompact/research/exp10_profiles.py`
- cursor: `[_]`
- core_role: Research script for snapcompact frame profile experiments.
- algorithmic_behavior: Evaluates/rendering profile choices for compaction readability/capacity, likely comparing shape/font/layout parameters used to derive production defaults.
- inputs_outputs_state: Inputs are experiment corpora/profile parameters; outputs are measurements/plots/tables for profile quality.
- gates_or_invariants: Research-only; should not be called in runtime compaction path.
- dependencies_and_callers: Informs `packages/snapcompact/src/snapcompact.ts` shape defaults.
- edge_cases_or_failure_modes: Dataset drift, model-specific OCR behavior, and non-production dependencies.
- validation_or_tests: Research artifact, not a test; production shape comments cite research lineage.
- skip_candidate: `yes: research experiment script rather than shipped runtime algorithm, though it informs runtime constants`

### OH_MY_HUMANIZE_MAIN-HZ-1312 `file` `packages/snapcompact/research/snapcompact_lockon_anatomy_viz.py`
- cursor: `[_]`
- core_role: Research visualization for snapcompact lock-on/anatomy behavior.
- algorithmic_behavior: Produces visual analysis of snapcompact frame/reader behavior for research.
- inputs_outputs_state: Inputs are research data or rendered frames; outputs are visualizations/diagnostic artifacts.
- gates_or_invariants: Not part of runtime; used to reason about compaction design.
- dependencies_and_callers: Research companion to `snapcompact.ts`.
- edge_cases_or_failure_modes: Visualization assumptions and stale research parameters.
- validation_or_tests: No runtime validation; supports design evidence.
- skip_candidate: `yes: research visualization, not core runtime implementation`

### OH_MY_HUMANIZE_MAIN-HZ-1342 `file` `packages/snapcompact/src/snapcompact.ts`
- cursor: `[_]`
- core_role: Deterministic image-frame conversation compaction algorithm.
- algorithmic_behavior: Selects provider/model-specific frame shape, normalizes transcript text, paginates into grid/doc frames, renders PNGs via native renderer, merges previous archives, preserves text tail beyond image budgets, and returns compaction summary/preserve data.
- inputs_outputs_state: Inputs are compaction preparation, model/API/provider, previous summary/archive/preserve data, file ops, shape/max-frame options, and messages. Outputs are summary, short summary, file-operation details, and `preserveData.snapcompact` archive frames/text tail.
- gates_or_invariants: Requires `firstKeptEntryId`; provider image budget clamps frames; previous oldest unpinned frames evict first; pages beyond budget are not rendered; unknown archive shapes are preserved; OpenAI remote compaction preserve data is stripped.
- dependencies_and_callers: Uses `renderSnapcompactPng` from `@oh-my-pi/pi-natives`, prompt templates, pi-ai message types, and compaction callers.
- edge_cases_or_failure_modes: Router image caps silently dropping images, provider switches/mixed shapes, previous text-summary migration, unrenderable Unicode, dim spans cut at page boundaries, overlarge text tails.
- validation_or_tests: Shape/normalization/render functions are testable; comments cite research benchmarks. Key exports at `snapcompact.ts:121`, `:231`, `:333`, `:392`, `:507`, `:535`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1372 `file` `packages/tui/src/fuzzy.ts`
- cursor: `[_]`
- core_role: Word-local fuzzy matching/ranking utility for TUI search/selectors.
- algorithmic_behavior: Normalizes camelCase/punctuation, builds compact/word indexes, scores exact/prefix/substring/character/acronym/token matches, applies phrase bonuses and alphanumeric swap variants, and filters/sorts items.
- inputs_outputs_state: Inputs are query strings, candidate text/items, and selector functions. Outputs are match booleans, numeric scores, and ranked filtered items.
- gates_or_invariants: Empty query matches with score 0; word-local matching avoids unrelated cross-word letter matches; lower score is better; compact phrase starts must align to word starts.
- dependencies_and_callers: Used by TUI components for fuzzy command/model/item search.
- edge_cases_or_failure_modes: Empty candidates, alphanumeric transpositions, acronym span too wide, long subsequence span, camelCase boundaries.
- validation_or_tests: No assigned direct fuzzy test, but selector tests indirectly cover UI search.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1402 `file` `packages/tui/test/image-render.test.ts`
- cursor: `[_]`
- core_role: Tests terminal image rendering.
- algorithmic_behavior: Verifies terminal graphics protocol detection/rendering and repeated probe panel graphics IDs.
- inputs_outputs_state: Inputs are terminal protocol state and sample images. Outputs are encoded image sequences/panels.
- gates_or_invariants: Image IDs should be independent; Windows Terminal Preview SIXEL detection should be correct.
- dependencies_and_callers: Exercises TUI terminal image renderer/protocol probe.
- edge_cases_or_failure_modes: Protocol unavailable, repeated images, Windows Terminal quirks.
- validation_or_tests: Suites at `image-render.test.ts:35` and `:231`; repeated ID test at `:46`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1432 `file` `packages/tui/test/process-terminal-headless.test.ts`
- cursor: `[_]`
- core_role: Tests headless ProcessTerminal suppression.
- algorithmic_behavior: Verifies process terminal behavior when no interactive terminal should render.
- inputs_outputs_state: Inputs are ProcessTerminal headless configuration/events. Outputs are suppressed render assertions.
- gates_or_invariants: Headless mode should not emit terminal UI artifacts.
- dependencies_and_callers: Exercises TUI process terminal component.
- edge_cases_or_failure_modes: Non-interactive environments and accidental render side effects.
- validation_or_tests: Suite at `process-terminal-headless.test.ts:25`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1462 `file` `packages/tui/test/truncate-to-width.test.ts`
- cursor: `[_]`
- core_role: Tests terminal visible-width truncation helpers.
- algorithmic_behavior: Asserts `truncateToWidth` and `visibleWidth` behavior for styled/wide text.
- inputs_outputs_state: Inputs are strings and width limits. Outputs are truncated strings and computed widths.
- gates_or_invariants: Visible width must ignore ANSI escapes and handle width budgets consistently.
- dependencies_and_callers: Exercises TUI rendering sanitation helpers.
- edge_cases_or_failure_modes: ANSI sequences, Unicode width, zero/short widths, and truncation marker behavior.
- validation_or_tests: Suites at `truncate-to-width.test.ts:4` and `:45`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1492 `file` `packages/utils/src/index.ts`
- cursor: `[_]`
- core_role: Shared utility package barrel plus JSON clone helper.
- algorithmic_behavior: Re-exports utility modules and implements `structuredCloneJSON`, which returns primitives directly, attempts `structuredClone` for plain objects/arrays, and falls back to `JSON.parse(JSON.stringify(value))`.
- inputs_outputs_state: Inputs are arbitrary values. Outputs are cloned values or module exports.
- gates_or_invariants: Non-objects return unchanged; plain object check uses prototype or arrays; fallback drops non-JSON data.
- dependencies_and_callers: Imported broadly across packages for utilities.
- edge_cases_or_failure_modes: Non-plain class instances fall to JSON clone, functions/symbols dropped by JSON, circular non-structured-clone values may fail.
- validation_or_tests: `packages/utils/test/install-id.test.ts` covers another utility; no direct clone test assigned.
- skip_candidate: `yes: mostly barrel export surface; only small clone helper is algorithmic`

### OH_MY_HUMANIZE_MAIN-HZ-1522 `file` `packages/utils/test/install-id.test.ts`
- cursor: `[_]`
- core_role: Tests install ID utility.
- algorithmic_behavior: Verifies `getInstallId` persistence/format behavior.
- inputs_outputs_state: Inputs are temp config/storage paths. Outputs are generated or read install IDs.
- gates_or_invariants: Install ID should be stable once created and valid in shape.
- dependencies_and_callers: Exercises runtime-install utility.
- edge_cases_or_failure_modes: Missing file, corrupted ID, repeated calls.
- validation_or_tests: Suite at `install-id.test.ts:17`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1552 `file` `python/robomp/src/config.py`
- cursor: `[_]`
- core_role: Env-driven typed configuration for robomp orchestrator and gh-proxy.
- algorithmic_behavior: Defines Pydantic settings for GitHub access, proxy mode, model pool, timeouts, retries, rate limits, paths, question autoclose, natives cache; validates blank secrets, PAT/proxy mutual exclusion, allowlists, retry delays, random model selection, path creation, and proxy-only loader.
- inputs_outputs_state: Inputs are environment variables and `.env`; outputs are cached `Settings`, proxy settings, parsed frozensets/tuples, retry delays, and filesystem dirs.
- gates_or_invariants: Must configure either direct PAT or proxy URL+HMAC, not both/neither; proxy URL/key must be paired; bot login non-empty; blank replay/token/proxy fields become disabled/invalid appropriately.
- dependencies_and_callers: Used by robomp orchestrator, dispatcher, GitHub backend/proxy, rate limiter, and workspace manager.
- edge_cases_or_failure_modes: Empty env secrets, comma-list coercion, invalid retry delay entries, proxy-only deployment without orchestrator fields, and jittered retry timing.
- validation_or_tests: Permission e2e and config tests cover downstream behavior; key validators at `config.py` settings class and `_validate_proxy_or_pat`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1582 `file` `python/robomp/tests/test_permissions_e2e.py`
- cursor: `[_]`
- core_role: Linux-root e2e tests for workspace slot permissions and native cache sharing.
- algorithmic_behavior: Creates bare upstream repos/workspaces, drops commands to slot UIDs, runs Bun/Biome/Cargo/Git flows, pushes branches, stages native artifacts, captures/populates shared natives cache, and verifies ownership/inode semantics.
- inputs_outputs_state: Inputs are temp repos, slot UIDs/GID, local git transport, database fixture, host tool bindings, commands. Outputs are commits, pushed branches, cache entries, file ownership/inodes, and command results.
- gates_or_invariants: Skipped unless `ROBOMP_PERMISSION_E2E=1`; requires Linux root and toolchain; shared cache root must be setgid; `.node` is hardlinked while companions are copied.
- dependencies_and_callers: Exercises `SandboxManager`, `host_tools`, `NativesCache`, local Git transport, and repo command environment.
- edge_cases_or_failure_modes: Root-owned stale Bun cache, retry slot after root push, Git safe.directory, hardlink rebuild isolation, companion rewrite isolation.
- validation_or_tests: Tests `test_slot_workspace_runs_bun_biome_cargo_and_git_after_root_reentry`, `test_git_pool_metadata_survives_root_push_and_retry_slot`, and `test_natives_cache_shares_artifacts_across_slot_workspaces`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1612 `directory` `packages/coding-agent/src/commit/map-reduce`
- cursor: `[_]`
- core_role: Commit-message/analysis map-reduce subsystem.
- algorithmic_behavior: `map-phase.ts` likely partitions changed files/diffs into map jobs; `reduce-phase.ts` combines partial analyses; `utils.ts` shares helpers; `index.ts` exports the subsystem.
- inputs_outputs_state: Inputs are commit analysis data/diffs/numstat and model/tool outputs. Outputs are reduced commit summaries/scope decisions.
- gates_or_invariants: Map/reduce phases should preserve file coverage and combine without losing evidence.
- dependencies_and_callers: Coordinates with `packages/coding-agent/src/commit/**` analysis and commit generation paths.
- edge_cases_or_failure_modes: Large diffs, partial map failures, duplicate/overlapping file groups, and reduction ambiguity.
- validation_or_tests: Related commit analysis/scope tests and commit workflow coverage; no direct assigned map-reduce test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1642 `directory` `packages/coding-agent/src/workflow/__tests__`
- cursor: `[_]`
- core_role: Workflow runtime/lifecycle tests.
- algorithmic_behavior: Tests `runWorkflow` lifecycle, session workflow runtime host review nodes, and shell-script runtime behavior.
- inputs_outputs_state: Inputs are workflow definitions, runtime hosts, review nodes, shell scripts, and session fixtures. Outputs are lifecycle events, activation status, and rendered/recorded workflow state.
- gates_or_invariants: Workflow runner must start/complete/fail activations in order, preserve review-node semantics, and execute shell runtime contracts.
- dependencies_and_callers: Exercises `packages/coding-agent/src/workflow/**`, especially lifecycle and runtime host code.
- edge_cases_or_failure_modes: Failed activations, stop/restart, review nodes, shell exit status.
- validation_or_tests: Suites at `runner.test.ts:10`, `session-runtime.test.ts:10`, and shell-script runtime file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1672 `file` `crates/pi-shell/src/minimizer/primitives.rs`
- cursor: `[_]`
- core_role: Reusable output compaction primitives for shell minimizer filters.
- algorithmic_behavior: Provides ANSI stripping, consecutive-line dedup, head/tail line capping, predicate line stripping, file grouping, command token checks, markdown badge/rule detection, listing compaction, and Unicode-safe line truncation with dropped-count marker.
- inputs_outputs_state: Inputs are command output strings, caps, predicates, token lists. Outputs are compacted strings and boolean classification results.
- gates_or_invariants: Truncation counts Unicode scalar chars, not bytes; `reduced` keeps minimum 1 for nonzero caps; group-by-file only accepts plausible `file:line` lines.
- dependencies_and_callers: Used by native minimizer filters under `crates/pi-shell/src/minimizer/filters/**`.
- edge_cases_or_failure_modes: ANSI CSI sequences, empty caps, repeated lines, blank lines, badge/rule lines, long Unicode lines, false file-line matches.
- validation_or_tests: Covered by minimizer fixture tests and filters that call these primitives.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1702 `file` `packages/ai/src/dialect/deepseek.ts`
- cursor: `[_]`
- core_role: DeepSeek in-band tool/thinking dialect scanner and renderer.
- algorithmic_behavior: Streaming state machine consumes special tokens, thinking spans, legacy tool calls, modern DeepSeek tool calls, and DSML invoke/parameter tags; emits text/thinking/tool start/end events; renders transcripts/tool calls/results.
- inputs_outputs_state: Inputs are streamed text chunks, messages, tool calls/results, and render options. Outputs are `InbandScanEvent[]`, rendered transcript strings, parsed arguments, and raw tool blocks.
- gates_or_invariants: Holds partial suffixes to avoid leaking partial tokens; strips control-token whitespace; JSON args parse with repair or `{}`; DSML non-string params parse JSON; flush finalizes thinking/reset states.
- dependencies_and_callers: Uses dialect prompt markdown, `parseJsonWithRepair`, coercion/rendering helpers, and dialect registry.
- edge_cases_or_failure_modes: Partial control tokens across chunks, legacy fenced args, malformed JSON, DSML ASCII/fullwidth variants, unterminated tool/thinking blocks.
- validation_or_tests: Spec documented in `docs/toolconv/deepseek.md`; scanner exports at `deepseek.ts:72`, render helpers around `:430`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1732 `file` `packages/ai/src/providers/cursor.ts`
- cursor: `[_]`
- core_role: Cursor Agent provider implementation over Connect/protobuf HTTP/2.
- algorithmic_behavior: Builds `AgentRunRequest`, frames protobuf messages, sends HTTP/2 Connect stream with heartbeats, parses server messages, streams text/thinking/tool calls into `AssistantMessageEventStream`, handles KV blob get/set, exec/tool requests, MCP calls, todo updates, shell streams, and conversation checkpoints.
- inputs_outputs_state: Inputs are Cursor API key, model/context/options, conversation ID/state cache, blob store, exec handlers, MCP tools, and abort signal. Outputs are assistant events/messages, tool results, exec replies, cached state/blobs, and usage/cost.
- gates_or_invariants: Requires API key; conversation state/blob stores keyed by conversation ID; frames are 5-byte header plus payload; end-stream errors parsed; completion waits for explicit `turnEnded`; handlers return rejected/error protobuf results when unavailable/failing.
- dependencies_and_callers: Uses generated Cursor protobuf schemas, `http2`, `AssistantMessageEventStream`, `parseStreamingJson`, model cost calculation, and cursor exec handler interfaces.
- edge_cases_or_failure_modes: Connect end-stream errors, malformed protobuf frames, missing handlers, tool result truncation, MCP arg bytes/JSON5 coercion, aborted request, debug log failures, partial tool JSON.
- validation_or_tests: Exported `resolveExecHandler` has test seam; provider behavior covered by cursor/provider tests outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1762 `file` `packages/ai/src/providers/transform-messages.ts`
- cursor: `[_]`
- core_role: Cross-provider message-history normalization.
- algorithmic_behavior: Deduplicates tool-call IDs, rewrites matching tool results, normalizes tool-call IDs for target model, strips/demotes thinking signatures by provider/model rules, drops orphan tool results or converts safe stale results to user notes, and synthesizes missing/aborted tool results.
- inputs_outputs_state: Inputs are canonical messages, target model, optional ID normalizer, length/suffix settings. Outputs are transformed message arrays valid for target provider.
- gates_or_invariants: Anthropic thinking replay rules preserved; official Anthropic signatures stripped when unsafe; tool result must immediately follow surviving tool calls; duplicate IDs capped to 64 chars per segment; truncated thinking-only assistant turns are dropped.
- dependencies_and_callers: Used by provider converters before request serialization.
- edge_cases_or_failure_modes: Responses composite IDs, delayed duplicate results, abandoned tool-use turns, aborted/error turns, stale orphan results after compaction, cross-model/cross-provider thinking.
- validation_or_tests: Regressions covered by AI provider tests including issue 1227 and Anthropic mid-conversation/system behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1792 `file` `packages/ai/src/registry/minimax-code-cn.ts`
- cursor: `[_]`
- core_role: MiniMax Token Plan provider definition.
- algorithmic_behavior: Defines provider ID/name and login function that lazily loads MiniMax OAuth flow.
- inputs_outputs_state: Inputs are OAuth login callbacks. Outputs are OAuth credentials from `loginMiniMaxCodeCn`.
- gates_or_invariants: Provider shape must satisfy `ProviderDefinition`.
- dependencies_and_callers: Used by AI auth/provider registry.
- edge_cases_or_failure_modes: Lazy module load failure or login failure.
- validation_or_tests: `packages/ai/test/minimax-code-login.test.ts`.
- skip_candidate: `yes: provider registry wiring; little local algorithm beyond deferred login delegation`

### OH_MY_HUMANIZE_MAIN-HZ-1822 `file` `packages/ai/src/registry/xai-oauth.ts`
- cursor: `[_]`
- core_role: xAI OAuth provider definition.
- algorithmic_behavior: Defines provider ID/name plus login and refresh-token functions that load xAI OAuth helpers on demand.
- inputs_outputs_state: Inputs are login callbacks or stored OAuth refresh credentials. Outputs are refreshed/login credentials.
- gates_or_invariants: Provider shape must satisfy `ProviderDefinition`; refresh uses `credentials.refresh`.
- dependencies_and_callers: Used by AI auth/provider registry and credential refresh logic.
- edge_cases_or_failure_modes: Missing refresh token, lazy load failure, provider refresh failure.
- validation_or_tests: Covered by provider/OAuth tests indirectly.
- skip_candidate: `yes: thin provider registry wiring`

### OH_MY_HUMANIZE_MAIN-HZ-1852 `file` `packages/ai/src/utils/openrouter-headers.ts`
- cursor: `[_]`
- core_role: Static OpenRouter request header helper.
- algorithmic_behavior: Returns `User-Agent`, referer/title/category, and cache headers using package version.
- inputs_outputs_state: Input is package version import. Output is header record.
- gates_or_invariants: Cache header TTL fixed to 3600; title/category stable.
- dependencies_and_callers: Used by OpenRouter provider request builders.
- edge_cases_or_failure_modes: Package version import failure or stale branding.
- validation_or_tests: No direct assigned test.
- skip_candidate: `yes: simple constant mapping, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1882 `file` `packages/catalog/src/identity/index.ts`
- cursor: `[_]`
- core_role: Barrel export for model identity helpers.
- algorithmic_behavior: Re-exports bundled/classify/dialect/equivalence/family/id/markers/priority/reference/selection modules.
- inputs_outputs_state: Inputs/outputs are module exports only.
- gates_or_invariants: Export surface must avoid ambiguity and preserve identity API.
- dependencies_and_callers: Imported by catalog consumers.
- edge_cases_or_failure_modes: Duplicate export names or missing module exports.
- validation_or_tests: Catalog identity tests elsewhere cover underlying modules.
- skip_candidate: `yes: pure barrel export, no local algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1912 `file` `packages/coding-agent/src/autoresearch/storage.ts`
- cursor: `[_]`
- core_role: SQLite persistence for autoresearch sessions and experiment runs.
- algorithmic_behavior: Creates/migrates schema, opens per-project DBs, caches storage instances, manages active sessions, updates session metadata, inserts/completes/logs/flags/abandons runs, and maps DB rows to typed rows.
- inputs_outputs_state: Inputs are cwd, session params, run params, metrics/ASI JSON, dirty paths, status fields. Outputs are `SessionRow`/`RunRow`, DB files under autoresearch project dirs, and cached storage.
- gates_or_invariants: WAL/busy timeout installed before lock-taking statements; schema version tracked; JSON list/metric fields serialized; required inserted rows are re-read or throw.
- dependencies_and_callers: Uses `bun:sqlite`, `getAutoresearchDbPath`, git helpers, and autoresearch controllers.
- edge_cases_or_failure_modes: SQLite busy/recovery, missing inserted row, invalid JSON legacy data, branch-specific active session lookup, pending run abandonment.
- validation_or_tests: Autoresearch behavior tests outside assigned set; key class at `storage.ts:38`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1942 `file` `packages/coding-agent/src/cli/extension-flags.ts`
- cursor: `[_]`
- core_role: Extension CLI flag reparsing and value injection.
- algorithmic_behavior: Reads extension-registered flags from runner, reparses raw args with those flag definitions, pushes parsed unknown flag values back to the runner, and returns extension-aware `Args`.
- inputs_outputs_state: Inputs are raw argv and `ExtensionFlagSink`. Outputs are parsed args or `null`, plus runner flag values.
- gates_or_invariants: No runner/no flags returns `null`; built-in shadowing is handled by seeded `parseArgs`; only parsed registered flags are set.
- dependencies_and_callers: Used during CLI startup after extensions load.
- edge_cases_or_failure_modes: String flags with separate value, `--flag=value`, boolean collisions with built-ins, and leaked flag values into prompt messages.
- validation_or_tests: Marketplace flag parsing test covers related ergonomics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1972 `file` `packages/coding-agent/src/collab/protocol.ts`
- cursor: `[_]`
- core_role: CLI collab wire protocol, envelope, and link handling.
- algorithmic_behavior: Defines encrypted collab frame union, packs/unpacks/rewrites peer envelopes, generates room IDs, formats compact/full/web links, normalizes relay origins, parses links including legacy/mangled forms, and extracts read-only/full write tokens.
- inputs_outputs_state: Inputs are relay URL, room ID, room key, optional write token, binary envelopes, and user-entered links. Outputs are links, parsed `{wsUrl, roomId, key, writeToken}`, and envelope payload/peer IDs.
- gates_or_invariants: Plain `ws://` allowed only for localhost; secret must decode to 32 or 48 bytes; room path must match `/r/<roomId>`; envelope needs at least 4 bytes.
- dependencies_and_callers: Used by collab host/guest CLI and mirrored in `packages/collab-web/src/lib`.
- edge_cases_or_failure_modes: `%23` legacy fragment mangling, scheme-less links, web deep links with fragment recursion, invalid base64url keys, and relay scheme rejection.
- validation_or_tests: Covered by collab web/local relay behavior; key functions at `protocol.ts:92`, `:119`, `:169`, `:187`, `:201`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2002 `file` `packages/coding-agent/src/commands/usage.ts`
- cursor: `[_]`
- core_role: CLI command wrapper for usage reports.
- algorithmic_behavior: Defines command flags and delegates parsed options to `runUsageCommand`.
- inputs_outputs_state: Inputs are `--json`, `--provider`, `--redact`, `--history`, `--days`. Outputs are usage command execution.
- gates_or_invariants: Flag defaults and types are enforced by CLI framework.
- dependencies_and_callers: `omp usage` command; depends on `../cli/usage-cli`.
- edge_cases_or_failure_modes: Invalid days/provider handled downstream.
- validation_or_tests: Usage CLI tests likely outside assigned set.
- skip_candidate: `yes: command wrapper; core behavior lives in usage CLI`

### OH_MY_HUMANIZE_MAIN-HZ-2032 `file` `packages/coding-agent/src/dap/session.ts`
- cursor: `[_]`
- core_role: Debug Adapter Protocol session manager.
- algorithmic_behavior: Launches/attaches DAP clients, manages one active session, performs initialize/configurationDone handshake, serializes breakpoint mutations, handles runInTerminal/startDebugging reverse requests, tracks output/threads/frames/status, supports continue/pause/step/stack/scopes/variables/evaluate/memory operations, and disposes idle sessions.
- inputs_outputs_state: Inputs are adapter configs, cwd/program/pid/host/port, breakpoints, DAP requests/events, abort signals, and timeouts. Outputs are session summaries, breakpoint records, output snapshots, DAP responses, and process spawns.
- gates_or_invariants: Only one active launch slot; breakpoint mutations queued; stop waiters subscribe before commands; output buffer capped at 128KiB; idle cleanup after 10 minutes; debugpy missing module maps to install hint.
- dependencies_and_callers: Uses `DapClient`, DAP type definitions, `ptree.spawn`, logger, and tool commands for debugging.
- edge_cases_or_failure_modes: Launch response blocked until configurationDone, initial stop races, unhandled waiters after Promise.race, dead adapters, output chunk O(n²) avoidance, missing threads/frame IDs.
- validation_or_tests: Protocol probe/debug tests cover adjacent behavior; class at `session.ts:249`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2062 `file` `packages/coding-agent/src/discovery/opencode.ts`
- cursor: `[_]`
- core_role: OpenCode compatibility discovery adapter.
- algorithmic_behavior: Loads OpenCode config/context files/MCP servers/skills/extensions/slash commands/settings and converts them into coding-agent discovery result items.
- inputs_outputs_state: Inputs are OpenCode config files, cwd/user/project locations, command toggle env/settings. Outputs are `LoadResult` items for context, MCP servers, skills, extension modules, slash commands, and settings.
- gates_or_invariants: JSON config load is tolerant; project/user command toggles can disable sources; MCP configs are extracted from supported shapes.
- dependencies_and_callers: Used by discovery/capability loader with provider ID `opencode`.
- edge_cases_or_failure_modes: Missing config, invalid JSON, unsupported MCP shape, disabled user/project commands, and module path issues.
- validation_or_tests: Model/discovery tests cover runtime discovery surfaces.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2092 `file` `packages/coding-agent/src/export/custom-share.ts`
- cursor: `[_]`
- core_role: Custom share hook discovery/loader.
- algorithmic_behavior: Finds `share.ts/js/mjs` candidates, loads a custom share function, normalizes returned result/string/undefined into share outcome.
- inputs_outputs_state: Inputs are generated HTML path and optional share script. Outputs are loaded hook metadata and custom share result.
- gates_or_invariants: Missing candidates return `null`; hook must export expected callable shape.
- dependencies_and_callers: Used by export/share command after HTML generation.
- edge_cases_or_failure_modes: No script, bad export, hook throws, invalid return shape.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2122 `file` `packages/coding-agent/src/internal-urls/json-query.ts`
- cursor: `[_]`
- core_role: JSON query parser/executor for internal URL extraction.
- algorithmic_behavior: Parses jq-like `.foo[0]["bar"]` query strings into tokens, applies them to JSON values, and converts URL path segments to query notation.
- inputs_outputs_state: Inputs are query strings, JSON-like data, and URL paths. Outputs are token arrays, selected JSON values, or query strings.
- gates_or_invariants: Missing `]`, empty `[]`, and unexpected tokens throw; numeric tokens require arrays; missing/null traversal returns `undefined`.
- dependencies_and_callers: Used by internal URL handlers and eval/read helpers.
- edge_cases_or_failure_modes: Percent-decoding failures, quoted bracket keys, numeric path segments, traversal into non-objects, special-key escaping.
- validation_or_tests: Eval helper local-root tests exercise internal URL resolution; parser at `json-query.ts:15`, executor at `:75`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2152 `file` `packages/coding-agent/src/mcp/config.ts`
- cursor: `[_]`
- core_role: MCP config loading, conversion, validation, and filtering.
- algorithmic_behavior: Loads MCP servers through capability discovery, converts canonical `MCPServer` to legacy config, applies disabled-server list, filters native Exa/browser duplicates while extracting Exa API keys, and validates transport configs.
- inputs_outputs_state: Inputs are cwd, options, discovered servers, disabled user config, server command/url/headers/env. Outputs are legacy `configs`, `sources`, and `exaApiKeys`.
- gates_or_invariants: Project config can be disabled; disabled or `enabled:false` servers are removed; Exa/browser filters preserve source metadata for remaining servers; stdio requires command, http/sse requires URL, command+URL conflicts.
- dependencies_and_callers: Uses capability system, `mcpCapability`, config writer, and MCP manager startup.
- edge_cases_or_failure_modes: Exa key in URL/args/env, browser package aliases, unknown server type, missing command/url, duplicate names.
- validation_or_tests: MCP config behavior tested elsewhere; key functions at `config.ts:95`, `:147`, `:175`, `:221`, `:250`, `:308`, `:348`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2182 `file` `packages/coding-agent/src/modes/gradient-highlight.ts`
- cursor: `[_]`
- core_role: ANSI gradient keyword highlighter for TUI/editor text.
- algorithmic_behavior: Lazily builds color palette per color mode, masks non-prose regions, scans highlight regex matches, paints matched characters across HSL stops, and restores foreground color.
- inputs_outputs_state: Inputs are text, reset SGR sequence, phase, and highlighter spec. Outputs are ANSI-colored text.
- gates_or_invariants: Probe regex fast-path skips work; phase wraps into `[0,1)`; SGR escapes are zero-width; code/markup masked text is not highlighted.
- dependencies_and_callers: Uses `maskNonProse` and active theme color mode.
- edge_cases_or_failure_modes: Negative phase, non-truecolor terminals, keywords in fenced code/XML, repeated same color stop coalescing.
- validation_or_tests: UI rendering tests indirectly cover visible width; no direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2212 `file` `packages/coding-agent/src/session/agent-storage.ts`
- cursor: `[_]`
- core_role: Unified SQLite storage for agent settings, model usage, and auth credentials.
- algorithmic_behavior: Opens singleton DBs with retry on SQLite busy, initializes/migrates settings/model usage schema, delegates credential store, hardens permissions, reads/writes settings, tracks model usage order/cache, and supports credential operations.
- inputs_outputs_state: Inputs are DB path, settings values, model keys, auth credentials. Outputs are persisted DB rows, settings objects, model usage list, and stored credential data.
- gates_or_invariants: Busy timeout before WAL; schema version 5; v1 blob settings migrate to per-key rows; v4→v5 table rebuild; open retries exponential backoff on busy errors.
- dependencies_and_callers: Used by coding-agent config/session/auth layers; depends on `bun:sqlite`, `SqliteAuthCredentialStore`, logger, and path helpers.
- edge_cases_or_failure_modes: Corrupt DB, unwritable directory, legacy settings invalid JSON, schema mismatch, SQLite busy recovery, stale model usage cache.
- validation_or_tests: `agent-session-model-persistence`, `sdk-session-isolation`, auth-storage tests cover effects.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2242 `file` `packages/coding-agent/src/slash-commands/acp-builtins.ts`
- cursor: `[_]`
- core_role: ACP/text-mode slash command advertisement and dispatch.
- algorithmic_behavior: Builds reserved builtin name/alias set, detects extension names shadowed by builtins or colon-prefix parsing, exports ACP-safe builtin commands, and executes matched builtins in text mode.
- inputs_outputs_state: Inputs are slash command text, builtin registry, runtime, and extension command names. Outputs are ACP command list, shadow decisions, and consumed/prompt results.
- gates_or_invariants: TUI-only commands without `handle` are not advertised; colon names whose prefix is a builtin are shadowed; unmatched commands return `false`.
- dependencies_and_callers: Used by ACP server and extension command filtering.
- edge_cases_or_failure_modes: Alias collision, `model:foo` style namespace collision, command returning undefined vs prompt.
- validation_or_tests: Slash command retry/ACP tests cover dispatch patterns.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2272 `file` `packages/coding-agent/src/task/persisted-revive.ts`
- cursor: `[_]`
- core_role: Cold-revive factory for persisted parked subagents.
- algorithmic_behavior: Peeks session init metadata from subagent JSONL, validates cwd exists, derives task depth through parent registry chain, reopens session, adopts artifact manager, creates MCP proxy tools, recreates subagent settings/session with persisted tools/schema/system prompt/spawns, clamps active tools, and syncs registry status on agent start/end.
- inputs_outputs_state: Inputs are persisted subagent ref, session file/init, parent session/auth/model/settings, registry, MCP manager. Outputs are async reviver returning live `AgentSession` or `undefined`.
- gates_or_invariants: Missing session file/init or missing cwd returns undefined; old files without persisted spawns deny respawning; revived subagent requires yield tool and no UI; active tools clamped to persisted list.
- dependencies_and_callers: Used by AgentLifecycleManager/AgentRegistry for hub/collab/resumed process references.
- edge_cases_or_failure_modes: Moved/merged worktree, broken parent chain cycles, missing MCP manager, stale tools, artifact adoption, idle-TTL registry status not clearing.
- validation_or_tests: Task/subagent lifecycle tests indirectly cover revive semantics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2302 `file` `packages/coding-agent/src/tools/context.ts`
- cursor: `[_]`
- core_role: Tool execution context merger for built-in/custom tools.
- algorithmic_behavior: Extends `AgentToolContext` with custom tool/UI/session fields and returns a merged context for each tool call.
- inputs_outputs_state: Inputs are base custom context, optional tool call, UI context, UI flag, tool names. Output is `AgentToolContext`.
- gates_or_invariants: Context is rebuilt per call; UI/tool names setters update stored fields.
- dependencies_and_callers: Used by tool execution/custom tools/extensions.
- edge_cases_or_failure_modes: Missing UI context and stale tool names if not updated.
- validation_or_tests: Custom tool tests indirectly cover context shape.
- skip_candidate: `yes: thin context plumbing, not a standalone core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2332 `file` `packages/coding-agent/src/tools/memory-recall.ts`
- cursor: `[_]`
- core_role: Agent recall tool over hindsight or mnemopi memory backends.
- algorithmic_behavior: Exposes strict ArkType `query`, gates creation by memory backend, executes scoped recall against mnemopi or Hindsight client, formats results with current time, marks empty results as useless, and logs/rethrows backend failures.
- inputs_outputs_state: Inputs are tool params, session settings/state, memory backend config. Outputs are `AgentToolResult` text/details/useless flag.
- gates_or_invariants: Tool only exists for `hindsight`/`mnemopi`; missing backend state throws; empty recall returns “No relevant memories found.”
- dependencies_and_callers: Used by tool registry/session when memory is enabled; depends on hindsight content formatters and mnemopi session state.
- edge_cases_or_failure_modes: Backend not initialized, recall client failure, no results, mnemopi scoped bank errors.
- validation_or_tests: Memory backend tests in mnemopi and tool registry coverage; class at `memory-recall.ts:14`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2362 `file` `packages/coding-agent/src/tts/streaming-player.ts`
- cursor: `[_]`
- core_role: Gapless streaming audio playback state machine for assistant speech.
- algorithmic_behavior: Selects persistent raw-PCM player commands, queues PCM chunks, drains in order, paces writes to stay at most 0.6s ahead, applies gain/ducking, falls back to per-file WAV playback, and stops by killing process/dropping queue.
- inputs_outputs_state: Inputs are platform, sample rate, Float32 PCM chunks, gain, ffmpeg/paplay/aplay availability. Outputs are audio playback side effects and drain completion.
- gates_or_invariants: macOS/Windows return no streaming backend; start is idempotent; stop is terminal; end waits for drain; queue wake uses `Promise.withResolvers`.
- dependencies_and_callers: Used by vocalizer/TTS pipeline; depends on Bun.spawn, `playAudioFile`, `encodeWav`, tool path lookup, logger.
- edge_cases_or_failure_modes: Missing player binaries, spawn/write/playback failure, buffered audio responsiveness, temp WAV cleanup, stop during sleep/drain.
- validation_or_tests: TTS tests outside assigned set; command selector at `streaming-player.ts:50`, class at `:83`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2392 `file` `packages/coding-agent/src/utils/image-vision-fallback.ts`
- cursor: `[_]`
- core_role: Text-model fallback for attached images.
- algorithmic_behavior: Saves each image to session local root using content hash, resolves a vision-capable model by role/default/active/first available priority, describes image with a one-shot vision call, and replaces image with text `<image path=...>` block containing description or fallback note.
- inputs_outputs_state: Inputs are image content, active model, model registry/settings/local roots, telemetry config, session ID, and abort signal. Outputs are `TextContent[]` blocks and saved image files.
- gates_or_invariants: Only image-capable models are selected; no API key means no description attempt; per-image failures do not throw beyond save; content-addressed names reuse identical images.
- dependencies_and_callers: Used before sending images to text-only models; depends on internal local URLs, model resolver, `instrumentedCompleteSimple`, prompts, telemetry.
- edge_cases_or_failure_modes: Unknown MIME extension, no vision model/key, vision call error/aborted/empty response, save failure, duplicate image data.
- validation_or_tests: Image attachment/inspect tool tests indirectly cover; key functions at `image-vision-fallback.ts:61`, `:104`, `:173`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2422 `file` `packages/coding-agent/src/workflow/lifecycle.ts`
- cursor: `[_]`
- core_role: Event-sourced workflow run lifecycle state machine.
- algorithmic_behavior: Appends lifecycle events for families/freezes/attempts/activations/change requests/stops/checkpoints/completion/failure, reconstructs snapshots from session entries, enforces change approval/application policy, validates checkpoints, and resolves restart frontiers through mappings/migrations.
- inputs_outputs_state: Inputs are workflow definitions/freezes, attempts, activation events, change request ops, checkpoint state/frontier/source mapping, and host append/getBranch. Outputs are run-family snapshots, errors, checkpoint/restart decisions, and event entries.
- gates_or_invariants: Attempt IDs unique; checkpoints require stopped/failed/stop-requested attempts with no running activations; terminal transitions forbidden from terminal states/running activations; restart requires applied freeze when changed and all frontier siblings ready.
- dependencies_and_callers: Used by workflow runner/session runtime and graph views/tests.
- edge_cases_or_failure_modes: Duplicate family/attempt events, missing freeze/checkpoint/attempt, unapproved changes, restart mapping misses, join nodes missing completed siblings, malformed custom entries ignored.
- validation_or_tests: `packages/coding-agent/src/workflow/__tests__` and `test/workflow/graph-view.test.ts`; key exports at `lifecycle.ts:370`, `:635`, `:699`, `:938`, `:1159`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2452 `file` `packages/coding-agent/test/core/apply-patch.test.ts`
- cursor: `[_]`
- core_role: Tests legacy and production apply-patch parsing/application.
- algorithmic_behavior: Parses legacy patch format, diff hunks, production `parseApplyPatch`, and applies patches across many file scenarios.
- inputs_outputs_state: Inputs are patch strings and temp cwd/files. Outputs are parse results, file contents, and errors.
- gates_or_invariants: Hunk parsing, sequence seeking, add/update/delete, simple replace, and production Codex patch behavior must remain stable.
- dependencies_and_callers: Exercises core patch application used by coding-agent edit/apply-patch tool.
- edge_cases_or_failure_modes: Missing context, malformed hunks, duplicate matches, add/delete files, EOF/newline behavior.
- validation_or_tests: Suites at `apply-patch.test.ts:47`, `:103`, `:167`, `:207`, `:296`, `:451`, `:577`, `:627`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2482 `file` `packages/coding-agent/test/debug/protocol-probe.test.ts`
- cursor: `[_]`
- core_role: Tests debug protocol probe rendering assets.
- algorithmic_behavior: Verifies RGB PNG encoding/sample image construction, unique graphics IDs for repeated probe panels, and large text line generation.
- inputs_outputs_state: Inputs are terminal protocol state and sample dimensions/text. Outputs are encoded image/probe panel strings.
- gates_or_invariants: Graphics IDs must be independent; generated lines must meet probe constraints.
- dependencies_and_callers: Exercises debug/protocol probe utilities.
- edge_cases_or_failure_modes: Repeated panels, protocol variations, large text generation.
- validation_or_tests: Suites at `protocol-probe.test.ts:24`, `:46`, `:67`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2512 `file` `packages/coding-agent/test/eval/runtime-global-dispose.test.ts`
- cursor: `[_]`
- core_role: Tests JS eval runtime global cleanup.
- algorithmic_behavior: Snapshots globals, runs runtime hooks, and asserts globals are restored/disposed.
- inputs_outputs_state: Inputs are global keys `__omp_import__`, `read` and runtime hooks. Outputs are global descriptor/state assertions.
- gates_or_invariants: Eval runtime must not leave helper globals behind after disposal.
- dependencies_and_callers: Exercises JS eval runtime.
- edge_cases_or_failure_modes: Existing global values, missing descriptors, and disposal after errors.
- validation_or_tests: Suite at `runtime-global-dispose.test.ts:45`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2542 `file` `packages/coding-agent/test/marketplace/dev-ergonomics.test.ts`
- cursor: `[_]`
- core_role: Tests marketplace plugin-dir flag parsing.
- algorithmic_behavior: Parses `--plugin-dir` values from args and checks forms.
- inputs_outputs_state: Inputs are CLI arg arrays. Outputs are parsed plugin directory list or undefined.
- gates_or_invariants: Separate and equals-style values must parse without swallowing unrelated args.
- dependencies_and_callers: Covers marketplace/dev extension flag ergonomics.
- edge_cases_or_failure_modes: Missing value, repeated flags, unknown args.
- validation_or_tests: Suite at `dev-ergonomics.test.ts:21`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2572 `file` `packages/coding-agent/test/session-manager/move-to.test.ts`
- cursor: `[_]`
- core_role: Tests session move-to behavior and quote stripping.
- algorithmic_behavior: Checks outer double quote stripping and `SessionManager.moveTo` preservation of headers/assistant entries.
- inputs_outputs_state: Inputs are session entries and target paths. Outputs are moved session files/entries.
- gates_or_invariants: Move should preserve session header and assistant history; quote stripping should be conservative.
- dependencies_and_callers: Exercises `SessionManager.moveTo`.
- edge_cases_or_failure_modes: Quoted paths, missing header, assistant entries during move.
- validation_or_tests: Suites at `move-to.test.ts:36` and `:62`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2602 `file` `packages/coding-agent/test/slash-commands/retry.test.ts`
- cursor: `[_]`
- core_role: Tests `/retry` slash command.
- algorithmic_behavior: Creates runtime fixture and verifies command retry behavior depending on whether retry is available/performed.
- inputs_outputs_state: Inputs are slash command runtime with `didRetry` state. Outputs are command result/consumption.
- gates_or_invariants: `/retry` should trigger runtime retry and produce correct result contract.
- dependencies_and_callers: Exercises slash command registry/handler.
- edge_cases_or_failure_modes: No retry available and repeated retry calls.
- validation_or_tests: Suite at `retry.test.ts:23`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2632 `file` `packages/coding-agent/test/task/worktree.test.ts`
- cursor: `[_]`
- core_role: Tests worktree isolation helpers.
- algorithmic_behavior: Runs git commands in temp repos and verifies worktree helper behavior.
- inputs_outputs_state: Inputs are temp git repos, worktree paths, branch names. Outputs are git command text and filesystem/worktree state.
- gates_or_invariants: Worktree operations must isolate task changes and preserve branch/repo invariants.
- dependencies_and_callers: Exercises task/worktree helper functions.
- edge_cases_or_failure_modes: Existing branches, dirty state, git command failures.
- validation_or_tests: Suite at `worktree.test.ts:33`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2662 `file` `packages/coding-agent/test/tools/eval-code-preview.test.ts`
- cursor: `[_]`
- core_role: Tests eval renderer code preview tail window.
- algorithmic_behavior: Verifies viewport/tail selection for cell code previews.
- inputs_outputs_state: Inputs are eval cell code strings and viewport constraints. Outputs are rendered preview text.
- gates_or_invariants: Long code previews should show the correct tail window without layout breakage.
- dependencies_and_callers: Exercises eval tool renderer.
- edge_cases_or_failure_modes: Long code cells, empty code, viewport changes.
- validation_or_tests: Suite at `eval-code-preview.test.ts:15`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2692 `file` `packages/coding-agent/test/tools/output-caps.test.ts`
- cursor: `[_]`
- core_role: Tests inline output byte capping.
- algorithmic_behavior: Generates lines and verifies `enforceInlineByteCap` elision markers/limits.
- inputs_outputs_state: Inputs are output strings and byte caps. Outputs are capped strings with marker.
- gates_or_invariants: Elision marker must include omitted byte count and cap by bytes, not just lines.
- dependencies_and_callers: Exercises tool output rendering/capping.
- edge_cases_or_failure_modes: Large output, line boundaries, marker regex.
- validation_or_tests: Suite at `output-caps.test.ts:22`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2722 `file` `packages/coding-agent/test/tools/todo.test.ts`
- cursor: `[_]`
- core_role: Tests Todo tool state transitions and rendering.
- algorithmic_behavior: Builds tool sessions, tests auto-start, ops operations, lenient init shapes, sticky window selection, description matching, phase collapsing, completed-task rendering, and malformed-args regression.
- inputs_outputs_state: Inputs are todo phases/items/tool call args. Outputs are session todo state and rendered call/result text.
- gates_or_invariants: Completed tasks render checked before strikethrough; malformed args should not crash; sticky window should select relevant tasks.
- dependencies_and_callers: Exercises `TodoTool` and renderer.
- edge_cases_or_failure_modes: Lenient input shapes, malformed args, phase collapse, description matching ambiguity.
- validation_or_tests: Suites at `todo.test.ts:35`, `:85`, `:104`, `:272`, `:310`, `:364`, `:419`, `:491`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2752 `file` `packages/coding-agent/test/workflow/graph-view.test.ts`
- cursor: `[_]`
- core_role: Large contract test suite for workflow graph ASCII rendering.
- algorithmic_behavior: Builds workflow definitions/families/freezes/bindings and verifies graph diagrams, connectors, split/merge buses, statuses, ANSI handling, and visible-column alignment.
- inputs_outputs_state: Inputs are `WorkflowDefinition`, `WorkflowRunFamilySnapshot`, `FlowFreeze`, runtime binding snapshots, and statuses. Outputs are rendered graph lines.
- gates_or_invariants: Connectors use one box-drawing baseline; split/merge buses centered; visible columns account for ANSI; node status rendering stable.
- dependencies_and_callers: Exercises workflow graph view renderer and lifecycle snapshot shapes.
- edge_cases_or_failure_modes: Branching/joins, centered bus alignment, ANSI width, single-node states, migration/checkpoint state.
- validation_or_tests: Suite at `graph-view.test.ts:19`; helper assertions at `:2469`, `:2481`, `:2490`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2782 `file` `packages/collab-web/src/tool-render/parts.tsx`
- cursor: `[_]`
- core_role: Shared React rendering primitives for collab tool outputs.
- algorithmic_behavior: Renders badges, paths, key/value grids, highlighted code/output blocks, result text/images, notes, diffs, invalid arg messages, and agent links.
- inputs_outputs_state: Inputs are tool result details, text/code/diff/images, paths, and render props. Outputs are React nodes.
- gates_or_invariants: Output line caps, syntax highlighting fallback, image opening, diff max lines, and tone styling must remain consistent.
- dependencies_and_callers: Used by collab-web tool renderers, including eval renderer.
- edge_cases_or_failure_modes: Missing result, invalid image data, long output/diff, unknown language, bare output mode.
- validation_or_tests: UI behavior indirectly covered by collab-web/tool renderer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2812 `file` `packages/mnemopi/src/core/shmr.ts`
- cursor: `[_]`
- core_role: Semantic Harmonized Memory Reconciliation algorithm.
- algorithmic_behavior: Initializes facts/beliefs schema, hashes or resolves embeddings, clusters items by cosine similarity, formats clusters for LLM, extracts/normalizes belief JSON, computes harmony scores, applies beliefs to SQLite, harmonizes batches iteratively, recalls beliefs, reflects, and logs resonance.
- inputs_outputs_state: Inputs are memory/fact/episode rows, text/embeddings, thresholds/env constants, Beam-like DB, optional LLM output. Outputs are belief rows, harmonization stats, recall rows, resonance logs.
- gates_or_invariants: Batch/iteration/threshold constants are env-configurable; minimum cluster size enforced; deterministic fallback beliefs exist; embedding dimension 384; schema created with indexes.
- dependencies_and_callers: Used by mnemopi memory harmonization and tested by `shmr.test.ts`.
- edge_cases_or_failure_modes: Missing/precomputed embeddings, malformed LLM JSON, low harmony score, empty clusters, duplicate belief IDs, absent tables.
- validation_or_tests: `packages/mnemopi/test/shmr.test.ts` covers embedding integration and deterministic helpers; exports at `shmr.ts:105`, `:165`, `:212`, `:294`, `:392`, `:507`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2842 `file` `packages/swarm-extension/src/swarm/schema.ts`
- cursor: `[_]`
- core_role: YAML parser/validator for swarm definitions.
- algorithmic_behavior: Parses raw swarm YAML into typed definition with agents/mode/name, validates mode/name/agents and reports errors.
- inputs_outputs_state: Inputs are YAML content and raw config shape. Outputs are `SwarmDefinition` or validation error list.
- gates_or_invariants: Valid modes are `pipeline`, `parallel`, `sequential`; swarm names match alphanumeric/dot/underscore/hyphen; agents must satisfy required shape.
- dependencies_and_callers: Used by swarm extension loading/execution.
- edge_cases_or_failure_modes: Invalid YAML, missing agents, bad mode/name, malformed agent config.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2872 `file` `python/robomp/web/src/App.tsx`
- cursor: `[_]`
- core_role: Solid web dashboard root for robomp.
- algorithmic_behavior: Starts polling on mount, stops on cleanup, wires retry handler to `runTrigger`, and composes dashboard sections.
- inputs_outputs_state: Inputs are component lifecycle and retry delivery IDs. Outputs are polling side effects and rendered dashboard tree.
- gates_or_invariants: Polling must stop on unmount; retry calls are fire-and-forget.
- dependencies_and_callers: Uses Solid components/state in `python/robomp/web/src`.
- edge_cases_or_failure_modes: Retry failures are not awaited/displayed here; polling lifecycle leak if cleanup fails.
- validation_or_tests: Web tests not assigned.
- skip_candidate: `yes: UI composition wrapper; core state/polling logic lives in imported modules`

### OH_MY_HUMANIZE_MAIN-HZ-2902 `file` `crates/pi-shell/src/minimizer/filters/cloud.rs`
- cursor: `[_]`
- core_role: Cloud/database/network output minimizer filter.
- algorithmic_behavior: Supports AWS/gcloud/psql/http transfer-like tools; compacts AWS JSON by service-specific extractors, prunes sensitive AWS fields, compacts S3 text, logs/events/EC2/DynamoDB/SQS/EKS, strips transfer progress, and summarizes psql tables/expanded rows.
- inputs_outputs_state: Inputs are command context, raw output, exit code. Outputs are minimized text labeled by filter result.
- gates_or_invariants: Caps rows/line chars; preserves important error lines; avoids minimizing machine-readable psql; strips sensitive keys; handles stdout pipes specially.
- dependencies_and_callers: Called by minimizer filter dispatch for cloud commands.
- edge_cases_or_failure_modes: Non-JSON text, malformed tables, long lines, transfer progress from curl/wget, AWS secret fields, empty arrays, epoch ms conversion.
- validation_or_tests: Unit tests in same file at `cloud.rs:1247`; fixtures under minimizer filters.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2932 `file` `packages/ai/src/registry/oauth/google-antigravity.ts`
- cursor: `[_]`
- core_role: Google Antigravity OAuth login/refresh flow.
- algorithmic_behavior: Runs Google OAuth with Antigravity client/scopes, discovers existing Cloud Code project via `loadCodeAssist`, provisions project via retrying `onboardUser` when missing, and refreshes tokens while preserving project ID.
- inputs_outputs_state: Inputs are OAuth controller, access/refresh token, project ID, Google API responses. Outputs are `OAuthCredentials` with access/refresh/expires/projectId.
- gates_or_invariants: Onboard retries max 5 with 2s delay; project ID read from string or object; default tier falls back to `legacy-tier`; refresh subtracts 5-minute expiry buffer.
- dependencies_and_callers: Used by Antigravity provider registry and AuthStorage selection tests.
- edge_cases_or_failure_modes: loadCodeAssist/onboard non-OK, operation never done, no project ID, refresh failure, missing refresh token.
- validation_or_tests: `auth-storage-antigravity-selection.test.ts` covers credential selection; login project discovery logic at `google-antigravity.ts:72`, `:111`, `:155`, `:171`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2962 `file` `packages/ai/src/utils/schema/zod-decontaminate.ts`
- cursor: `[_]`
- core_role: Defensive converter from serialized Zod instance leaks to JSON Schema.
- algorithmic_behavior: Detects Zod 4 instance-shaped nodes (`def.type` mirrors `node.type`), rewrites enum/literal/union/intersection/array/object/tuple/record/map/set/wrapper/scalar cases, strips toxic noise/nulls, recurses identity-preservingly, and avoids cycles with `WeakSet`.
- inputs_outputs_state: Inputs are unknown JSON-like schema values. Outputs are cleaned JSON Schema-ish values, preserving input reference when unchanged.
- gates_or_invariants: Only known Zod kinds with matching surface/inner type are rewritten; invalid JSON Schema `type` values removed or mapped; object-shaped `enum` removed unless converted.
- dependencies_and_callers: Used by schema/tool wire conversion before provider validation.
- edge_cases_or_failure_modes: Self-referential graphs, optional/default required detection, nullable with existing type arrays, unknown Zod kinds, null-valued invalid keys.
- validation_or_tests: Schema tests around provider tool validation; export at `zod-decontaminate.ts:293`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2992 `file` `packages/coding-agent/src/commit/analysis/scope.ts`
- cursor: `[_]`
- core_role: Commit scope candidate extraction from numstat.
- algorithmic_behavior: Normalizes paths/renames, excludes files, accumulates changed lines per meaningful component, ranks scope candidates, detects wide/cross-cutting changes, and classifies wide patterns like deps/docs/tests/error-handling/type-refactor/config.
- inputs_outputs_state: Inputs are `NumstatEntry[]` with additions/deletions/path. Outputs are scope candidate string and `isWide` boolean.
- gates_or_invariants: Zero measurable changes returns none; placeholder/skip dirs are ignored; wide when >=3 distinct roots or top candidate below threshold; suggests up to five >=10% candidates.
- dependencies_and_callers: Used by commit analysis/generation.
- edge_cases_or_failure_modes: Git rename brace syntax, root files, placeholder dirs, docs-heavy changes, package/Cargo dependency changes, file names with dots.
- validation_or_tests: Commit analysis tests outside assigned set; main export at `scope.ts:34`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3022 `file` `packages/coding-agent/src/eval/__tests__/helpers-local-roots.test.ts`
- cursor: `[_]`
- core_role: Tests eval JS helper internal URL root substitution.
- algorithmic_behavior: Creates helper contexts with injected local roots, writes/reads/appends `local://` files, rejects traversal and unsupported schemes, and verifies plain paths resolve against cwd.
- inputs_outputs_state: Inputs are helper contexts, internal URLs, file contents. Outputs are filesystem writes/reads and thrown errors.
- gates_or_invariants: `local://` must map under injected root; traversal escaping root is rejected; unsupported schemes reject; no literal `local:` directory under cwd.
- dependencies_and_callers: Exercises eval JS shared helpers.
- edge_cases_or_failure_modes: `../` traversal, unknown schemes, HTTPS URLs, relative/absolute plain paths.
- validation_or_tests: Suite at `helpers-local-roots.test.ts:22`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3052 `file` `packages/coding-agent/src/extensibility/custom-tools/types.ts`
- cursor: `[_]`
- core_role: Type contract for custom tool extension API.
- algorithmic_behavior: Defines pending actions, custom tool API/context/session events, render options, result types, custom tool shape, factories, load errors, and load results.
- inputs_outputs_state: Inputs/outputs are TypeScript structural contracts rather than runtime values.
- gates_or_invariants: Tool factories must return loaded custom tools with schema/details contracts; result rendering options define UI behavior.
- dependencies_and_callers: Used by custom tool loader/execution and extension authors.
- edge_cases_or_failure_modes: Type-only misuse, broad `any` in generic defaults, incompatible schema/result implementations.
- validation_or_tests: Custom tool extension tests elsewhere.
- skip_candidate: `yes: type definitions only; algorithm lives in loader/executor`

### OH_MY_HUMANIZE_MAIN-HZ-3082 `file` `packages/coding-agent/src/lsp/clients/swiftlint-client.ts`
- cursor: `[_]`
- core_role: Linter client adapter for SwiftLint JSON diagnostics.
- algorithmic_behavior: Runs `swiftlint`, parses violations, maps severity to diagnostic severity, and exposes results through `LinterClient`.
- inputs_outputs_state: Inputs are cwd/file paths and SwiftLint output JSON. Outputs are LSP-style diagnostics.
- gates_or_invariants: Severity parser maps known severities; process failures/invalid JSON should surface as lint errors or empty diagnostics depending implementation.
- dependencies_and_callers: Used by LSP/linter subsystem for Swift projects.
- edge_cases_or_failure_modes: SwiftLint missing, invalid JSON, unknown severity, path normalization.
- validation_or_tests: LSP render tests cover rendering, not client execution.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3112 `file` `packages/coding-agent/src/modes/components/custom-editor.ts`
- cursor: `[_]`
- core_role: Customized terminal editor with configurable keys and paste/image handling.
- algorithmic_behavior: Defines action key maps, bracketed paste markers, image path extraction/normalization, shell-escaped path unescaping, space-hold mechanical detection, and extends editor behavior.
- inputs_outputs_state: Inputs are key events, paste payloads, editor state, timestamps. Outputs are editor actions and extracted image paths.
- gates_or_invariants: Bracketed image path extraction recognizes image extensions and boundaries; shell escapes normalized; repeated space timing uses jitter/mechanical thresholds.
- dependencies_and_callers: Used by interactive mode input editor.
- edge_cases_or_failure_modes: Pasted quoted/shell-escaped paths, multiple image paths, bracketed paste boundaries, mechanical key repeat false positives.
- validation_or_tests: Input controller tests exercise editor interactions; key helpers at `custom-editor.ts:89`, `:120`, class at `:163`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3142 `file` `packages/coding-agent/src/modes/components/reset-usage-selector.ts`
- cursor: `[_]`
- core_role: TUI selector for resetting usage/account state.
- algorithmic_behavior: Displays selectable reset usage options with max visible cap and handles selection through container component logic.
- inputs_outputs_state: Inputs are account/usage options and keyboard events. Outputs are selection callbacks/rendered rows.
- gates_or_invariants: Visible list capped at 10; component state should track selection.
- dependencies_and_callers: Used by modes/components account/usage UI.
- edge_cases_or_failure_modes: More than 10 accounts, empty list, navigation bounds.
- validation_or_tests: Related logout account selector test covers similar component patterns.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3172 `file` `packages/coding-agent/src/modes/controllers/omfg-controller.ts`
- cursor: `[_]`
- core_role: Controller for generating/saving rule candidates from feedback.
- algorithmic_behavior: Builds OMFG requests, generates candidate rules, allows save/abort/reject/amend with feedback, supports project/global destinations, and limits attempts.
- inputs_outputs_state: Inputs are user request/feedback, parsed generated rule candidates, settings, UI prompts. Outputs are saved rules or amend/reject/abort decisions.
- gates_or_invariants: Max attempts is 3; destination choices are constrained to project/global; candidate must parse as generated rule.
- dependencies_and_callers: Used by interactive rule-generation mode.
- edge_cases_or_failure_modes: Generation failure, invalid rule parse, user abort, amend loop exhaustion, save path failures.
- validation_or_tests: Controller tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3202 `file` `packages/coding-agent/src/slash-commands/helpers/format.ts`
- cursor: `[_]`
- core_role: Formatting helpers for slash command output.
- algorithmic_behavior: Formats durations and renders ASCII progress bars using optional theme styling.
- inputs_outputs_state: Inputs are milliseconds, fraction, width, theme. Outputs are formatted strings.
- gates_or_invariants: Progress fraction is clamped/handled when undefined; theme defaults to unstyled.
- dependencies_and_callers: Used by slash command status/usage renderers.
- edge_cases_or_failure_modes: Non-finite durations/fractions, zero/short bar width.
- validation_or_tests: Slash command tests indirectly cover.
- skip_candidate: `yes: small formatting utility, not core workflow algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3232 `file` `packages/coding-agent/src/web/scrapers/cisa-kev.ts`
- cursor: `[_]`
- core_role: Special web scraper for CISA Known Exploited Vulnerabilities.
- algorithmic_behavior: Detects CVE IDs, fetches CISA KEV JSON feed, finds matching entries, and returns formatted vulnerability content.
- inputs_outputs_state: Inputs are URL/text with CVE, fetch timeout/signal, KEV feed JSON. Outputs are scraper result markdown/text or null/fallback.
- gates_or_invariants: CVE regex must match `CVE-YYYY-NNNN...`; fetch timeout respected; missing CVE/feed entry handled.
- dependencies_and_callers: Used by web fetch special handler system.
- edge_cases_or_failure_modes: CISA feed unavailable, invalid JSON, CVE absent/not in KEV, network timeout.
- validation_or_tests: Web scraper tests focus social handlers; CISA tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3262 `file` `packages/coding-agent/src/web/scrapers/musicbrainz.ts`
- cursor: `[_]`
- core_role: Special scraper for MusicBrainz artist/release/recording pages.
- algorithmic_behavior: Parses entity/MBID from MusicBrainz URLs, fetches API JSON, formats artist lifespan/disambiguation, release media/tracks, recording duration/credits, and caps track output.
- inputs_outputs_state: Inputs are MusicBrainz URLs, fetch timeout/signal, API responses. Outputs are markdown summaries.
- gates_or_invariants: Host must be `musicbrainz.org`; entity path must be artist/release/recording; max tracks is 50; user-agent set.
- dependencies_and_callers: Used by web fetch special handler system.
- edge_cases_or_failure_modes: Unsupported entity, fetch failure, missing fields, long releases, unknown duration/lifespan.
- validation_or_tests: Web scraper social tests do not cover MusicBrainz; functions at `musicbrainz.ts:70`, `:148`, `:163`, `:200`, `:215`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3292 `file` `packages/coding-agent/src/web/scrapers/twitter.ts`
- cursor: `[_]`
- core_role: Special handler for Twitter/X URLs via Nitter mirrors.
- algorithmic_behavior: Attempts configured Nitter instances for Twitter content and returns scraped/converted result.
- inputs_outputs_state: Inputs are Twitter/X URL, fetch timeout/signal. Outputs are special handler response or fallback.
- gates_or_invariants: Uses allowlist of Nitter instances; should tolerate instance failure.
- dependencies_and_callers: Used by web fetch special handler system.
- edge_cases_or_failure_modes: All mirrors fail, changed Twitter/Nitter markup, private/deleted posts.
- validation_or_tests: `packages/coding-agent/test/tools/web-scrapers/social.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3322 `file` `packages/coding-agent/test/modes/components/logout-account-selector.test.ts`
- cursor: `[_]`
- core_role: Tests logout account selector UI component.
- algorithmic_behavior: Verifies account selector behavior/rendering for logout flow.
- inputs_outputs_state: Inputs are account options and component events. Outputs are rendered/selected state.
- gates_or_invariants: Selector should present accounts and handle selection safely.
- dependencies_and_callers: Exercises modes component for account logout.
- edge_cases_or_failure_modes: Empty accounts, selection bounds, display formatting.
- validation_or_tests: Suite at `logout-account-selector.test.ts:11`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3352 `file` `packages/coding-agent/test/modes/controllers/event-controller-message-start.test.ts`
- cursor: `[_]`
- core_role: Tests EventController message_start and IRC expiry behavior.
- algorithmic_behavior: Creates user/IRC messages and contexts, verifies message_start handling and expiry of IRC/live blocks.
- inputs_outputs_state: Inputs are user messages, custom IRC messages, context flags. Outputs are event controller state/UI updates.
- gates_or_invariants: User role message starts should update correct live block; IRC expiry respects timestamps/live-block state.
- dependencies_and_callers: Exercises EventController.
- edge_cases_or_failure_modes: Existing live block above, stale IRC timestamps, message role differences.
- validation_or_tests: Suites at `event-controller-message-start.test.ts:61` and `:193`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3382 `file` `packages/coding-agent/test/tools/web-scrapers/social.test.ts`
- cursor: `[_]`
- core_role: Integration-gated tests for social web scrapers.
- algorithmic_behavior: Runs web scraper handlers when `WEB_FETCH_INTEGRATION` is set.
- inputs_outputs_state: Inputs are social URLs/network responses. Outputs are scraper result assertions.
- gates_or_invariants: Skipped unless integration env enabled to avoid network-dependent default suite.
- dependencies_and_callers: Exercises Twitter/social scraper handlers.
- edge_cases_or_failure_modes: Network/mirror failures and changed page markup.
- validation_or_tests: File-level skip constant at `social.test.ts:6`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3412 `file` `packages/collab-web/src/tool-render/tools/eval.tsx`
- cursor: `[_]`
- core_role: Collab-web renderer for eval/code-cell tool calls/results.
- algorithmic_behavior: Parses eval cells from cell tags, begin/end blocks, and legacy formats; tokenizes attrs; maps language aliases; extracts detail cells; renders summary/body with code/output cells.
- inputs_outputs_state: Inputs are tool args/result details/name. Outputs are React summary/body nodes and parsed `EvalCell[]`.
- gates_or_invariants: Supports multiple historical cell encodings; unknown/malformed args produce safe rendering; language aliases map py/js/ts.
- dependencies_and_callers: Uses shared render parts and collab tool renderer registry.
- edge_cases_or_failure_modes: Quoted attrs, missing end markers, legacy input, detail/result disagreement, long cell code/output.
- validation_or_tests: Eval preview test in coding-agent covers related renderer behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3442 `file` `packages/mnemopi/src/core/beam/store.ts`
- cursor: `[_]`
- core_role: Core Beam memory SQLite store operations.
- algorithmic_behavior: Normalizes metadata/trust/veracity, emits events, invalidates caches, detects duplicates, trims working memory, adds temporal annotations, optionally proactive-links/fact-extracts, reconciles embedding model, remembers single/batch memories, updates/invalidates/forgets/scratchpad/exports/imports.
- inputs_outputs_state: Inputs are `BeamMemoryState`, content, metadata/source/trust/veracity options, batch options, import data. Outputs are memory IDs, DB rows/stats, events, cache invalidations, exported/imported state.
- gates_or_invariants: Scratchpad max from env; duplicate content check; canonical veracity/trust tiers; embedding model reconciliation invalidates mismatched embeddings; batch ops transactional where needed.
- dependencies_and_callers: Used by mnemopi Beam facade/recall/consolidation; heavily tested by mnemopi suite.
- edge_cases_or_failure_modes: Fact extraction failures, ID collisions, sibling races, invalid import shape, orphan vector episodes, cache invalidation, metadata JSON coercion.
- validation_or_tests: `beam-store.test.ts`, `beam-recall-unit.test.ts`, `beam-consolidate-unit.test.ts`, parity tests under `packages/mnemopi/test`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3472 `file` `packages/stats/src/client/ui/AsyncBoundary.tsx`
- cursor: `[_]`
- core_role: Small UI boundary component for async stats client rendering.
- algorithmic_behavior: Wraps children with loading/error/render handling for async state.
- inputs_outputs_state: Inputs are async boundary props. Outputs are React nodes for loading/error/content.
- gates_or_invariants: Should render fallback for pending/error states.
- dependencies_and_callers: Used by stats dashboard UI.
- edge_cases_or_failure_modes: Missing fallback, thrown child errors depending implementation.
- validation_or_tests: Stats UI tests not assigned.
- skip_candidate: `yes: UI convenience wrapper, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3502 `directory` `packages/coding-agent/src/extensibility/custom-commands/bundled/review`
- cursor: `[_]`
- core_role: Bundled custom `/review` command implementation.
- algorithmic_behavior: Contains `index.ts` that registers/executes review command behavior, likely gathering diff/context and prompting a review workflow.
- inputs_outputs_state: Inputs are custom command invocation args, session/runtime context, repository changes. Outputs are review command prompt/result/action.
- gates_or_invariants: Must integrate as bundled custom command without shadowing builtins; review behavior should stay read/analysis oriented unless command specifies actions.
- dependencies_and_callers: Loaded by custom command extensibility subsystem.
- edge_cases_or_failure_modes: No diff, large diff, untracked files, command args ambiguity.
- validation_or_tests: Code-review behavior covered by slash/custom command tests outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3532 `file` `packages/coding-agent/src/markit/converters/pdf/columns.ts`
- cursor: `[_]`
- core_role: PDF text-box column layout detector.
- algorithmic_behavior: Analyzes text box x positions/gaps to infer single/two-column layout using minimum gap ratio/points and minimum boxes per column.
- inputs_outputs_state: Inputs are PDF `TextBox[]`. Outputs are `ColumnLayout`.
- gates_or_invariants: Requires enough boxes per column and gap thresholds before declaring columns.
- dependencies_and_callers: Used by markit PDF converter.
- edge_cases_or_failure_modes: Sparse pages, uneven columns, wide tables, marginalia, overlapping boxes.
- validation_or_tests: PDF converter tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3562 `file` `packages/coding-agent/src/modes/theme/defaults/index.ts`
- cursor: `[_]`
- core_role: Default TUI theme table.
- algorithmic_behavior: Exports `defaultThemes` object of color/style definitions.
- inputs_outputs_state: Inputs none at runtime beyond import. Outputs theme definitions.
- gates_or_invariants: Theme keys/colors must match theme system expectations.
- dependencies_and_callers: Used by theme loader/defaulting.
- edge_cases_or_failure_modes: Missing theme key or invalid color token.
- validation_or_tests: Theme/render tests elsewhere.
- skip_candidate: `yes: static data table, no algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3592 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/multiline-utils.ts`
- cursor: `[_]`
- core_role: Vendored ASCII multiline text drawing helpers.
- algorithmic_behavior: Splits labels into lines, computes max width/line count, and draws multiline text centered or left-aligned onto an ASCII canvas.
- inputs_outputs_state: Inputs are label strings, coordinates, widths, canvas. Outputs are mutated canvas text cells/lines.
- gates_or_invariants: Center/left placement should respect line widths and vertical line counts.
- dependencies_and_callers: Used by vendored Mermaid ASCII renderer.
- edge_cases_or_failure_modes: Empty labels, uneven line widths, narrow boxes, out-of-bounds canvas writes.
- validation_or_tests: Mermaid/ascii graph tests indirectly cover.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: OH_MY_HUMANIZE_MAIN-HZ-022, OH_MY_HUMANIZE_MAIN-HZ-052, OH_MY_HUMANIZE_MAIN-HZ-082, OH_MY_HUMANIZE_MAIN-HZ-112, OH_MY_HUMANIZE_MAIN-HZ-142, OH_MY_HUMANIZE_MAIN-HZ-172, OH_MY_HUMANIZE_MAIN-HZ-202, OH_MY_HUMANIZE_MAIN-HZ-232, OH_MY_HUMANIZE_MAIN-HZ-262, OH_MY_HUMANIZE_MAIN-HZ-292, OH_MY_HUMANIZE_MAIN-HZ-322, OH_MY_HUMANIZE_MAIN-HZ-352, OH_MY_HUMANIZE_MAIN-HZ-382, OH_MY_HUMANIZE_MAIN-HZ-412, OH_MY_HUMANIZE_MAIN-HZ-442, OH_MY_HUMANIZE_MAIN-HZ-472, OH_MY_HUMANIZE_MAIN-HZ-502, OH_MY_HUMANIZE_MAIN-HZ-532, OH_MY_HUMANIZE_MAIN-HZ-562, OH_MY_HUMANIZE_MAIN-HZ-592, OH_MY_HUMANIZE_MAIN-HZ-622, OH_MY_HUMANIZE_MAIN-HZ-652, OH_MY_HUMANIZE_MAIN-HZ-682, OH_MY_HUMANIZE_MAIN-HZ-712, OH_MY_HUMANIZE_MAIN-HZ-742, OH_MY_HUMANIZE_MAIN-HZ-772, OH_MY_HUMANIZE_MAIN-HZ-802, OH_MY_HUMANIZE_MAIN-HZ-832, OH_MY_HUMANIZE_MAIN-HZ-862, OH_MY_HUMANIZE_MAIN-HZ-892, OH_MY_HUMANIZE_MAIN-HZ-922, OH_MY_HUMANIZE_MAIN-HZ-952, OH_MY_HUMANIZE_MAIN-HZ-982, OH_MY_HUMANIZE_MAIN-HZ-1012, OH_MY_HUMANIZE_MAIN-HZ-1042, OH_MY_HUMANIZE_MAIN-HZ-1072, OH_MY_HUMANIZE_MAIN-HZ-1102, OH_MY_HUMANIZE_MAIN-HZ-1132, OH_MY_HUMANIZE_MAIN-HZ-1162, OH_MY_HUMANIZE_MAIN-HZ-1192, OH_MY_HUMANIZE_MAIN-HZ-1222, OH_MY_HUMANIZE_MAIN-HZ-1252, OH_MY_HUMANIZE_MAIN-HZ-1282, OH_MY_HUMANIZE_MAIN-HZ-1312, OH_MY_HUMANIZE_MAIN-HZ-1342, OH_MY_HUMANIZE_MAIN-HZ-1372, OH_MY_HUMANIZE_MAIN-HZ-1402, OH_MY_HUMANIZE_MAIN-HZ-1432, OH_MY_HUMANIZE_MAIN-HZ-1462, OH_MY_HUMANIZE_MAIN-HZ-1492, OH_MY_HUMANIZE_MAIN-HZ-1522, OH_MY_HUMANIZE_MAIN-HZ-1552, OH_MY_HUMANIZE_MAIN-HZ-1582, OH_MY_HUMANIZE_MAIN-HZ-1612, OH_MY_HUMANIZE_MAIN-HZ-1642, OH_MY_HUMANIZE_MAIN-HZ-1672, OH_MY_HUMANIZE_MAIN-HZ-1702, OH_MY_HUMANIZE_MAIN-HZ-1732, OH_MY_HUMANIZE_MAIN-HZ-1762, OH_MY_HUMANIZE_MAIN-HZ-1792, OH_MY_HUMANIZE_MAIN-HZ-1822, OH_MY_HUMANIZE_MAIN-HZ-1852, OH_MY_HUMANIZE_MAIN-HZ-1882, OH_MY_HUMANIZE_MAIN-HZ-1912, OH_MY_HUMANIZE_MAIN-HZ-1942, OH_MY_HUMANIZE_MAIN-HZ-1972, OH_MY_HUMANIZE_MAIN-HZ-2002, OH_MY_HUMANIZE_MAIN-HZ-2032, OH_MY_HUMANIZE_MAIN-HZ-2062, OH_MY_HUMANIZE_MAIN-HZ-2092, OH_MY_HUMANIZE_MAIN-HZ-2122, OH_MY_HUMANIZE_MAIN-HZ-2152, OH_MY_HUMANIZE_MAIN-HZ-2182, OH_MY_HUMANIZE_MAIN-HZ-2212, OH_MY_HUMANIZE_MAIN-HZ-2242, OH_MY_HUMANIZE_MAIN-HZ-2272, OH_MY_HUMANIZE_MAIN-HZ-2302, OH_MY_HUMANIZE_MAIN-HZ-2332, OH_MY_HUMANIZE_MAIN-HZ-2362, OH_MY_HUMANIZE_MAIN-HZ-2392, OH_MY_HUMANIZE_MAIN-HZ-2422, OH_MY_HUMANIZE_MAIN-HZ-2452, OH_MY_HUMANIZE_MAIN-HZ-2482, OH_MY_HUMANIZE_MAIN-HZ-2512, OH_MY_HUMANIZE_MAIN-HZ-2542, OH_MY_HUMANIZE_MAIN-HZ-2572, OH_MY_HUMANIZE_MAIN-HZ-2602, OH_MY_HUMANIZE_MAIN-HZ-2632, OH_MY_HUMANIZE_MAIN-HZ-2662, OH_MY_HUMANIZE_MAIN-HZ-2692, OH_MY_HUMANIZE_MAIN-HZ-2722, OH_MY_HUMANIZE_MAIN-HZ-2752, OH_MY_HUMANIZE_MAIN-HZ-2782, OH_MY_HUMANIZE_MAIN-HZ-2812, OH_MY_HUMANIZE_MAIN-HZ-2842, OH_MY_HUMANIZE_MAIN-HZ-2872, OH_MY_HUMANIZE_MAIN-HZ-2902, OH_MY_HUMANIZE_MAIN-HZ-2932, OH_MY_HUMANIZE_MAIN-HZ-2962, OH_MY_HUMANIZE_MAIN-HZ-2992, OH_MY_HUMANIZE_MAIN-HZ-3022, OH_MY_HUMANIZE_MAIN-HZ-3052, OH_MY_HUMANIZE_MAIN-HZ-3082, OH_MY_HUMANIZE_MAIN-HZ-3112, OH_MY_HUMANIZE_MAIN-HZ-3142, OH_MY_HUMANIZE_MAIN-HZ-3172, OH_MY_HUMANIZE_MAIN-HZ-3202, OH_MY_HUMANIZE_MAIN-HZ-3232, OH_MY_HUMANIZE_MAIN-HZ-3262, OH_MY_HUMANIZE_MAIN-HZ-3292, OH_MY_HUMANIZE_MAIN-HZ-3322, OH_MY_HUMANIZE_MAIN-HZ-3352, OH_MY_HUMANIZE_MAIN-HZ-3382, OH_MY_HUMANIZE_MAIN-HZ-3412, OH_MY_HUMANIZE_MAIN-HZ-3442, OH_MY_HUMANIZE_MAIN-HZ-3472, OH_MY_HUMANIZE_MAIN-HZ-3502, OH_MY_HUMANIZE_MAIN-HZ-3532, OH_MY_HUMANIZE_MAIN-HZ-3562, OH_MY_HUMANIZE_MAIN-HZ-3592
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`