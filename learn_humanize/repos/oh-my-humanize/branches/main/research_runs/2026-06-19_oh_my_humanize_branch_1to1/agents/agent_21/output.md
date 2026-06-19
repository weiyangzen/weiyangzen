# agent_21 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-021 `directory` `crates/pi-natives`
- cursor: `[_]`
- core_role: Native Rust/N-API acceleration crate for coding-agent and sibling packages: AST search/edit, grep, globbing, text measurement, terminal/PTY/shell support, snapshot rendering, workspace listing, clipboard, power, crash, and native loading surfaces.
- algorithmic_behavior: Recursively contains algorithm modules such as `src/ast.rs`, `src/grep.rs`, `src/glob.rs`, `src/fs_cache.rs`, `src/text.rs`, `src/shell.rs`, `src/pty.rs`, `src/snapcompact.rs`, `src/tokens.rs`, and `src/workspace.rs`. `src/lib.rs` exports these to JS through `napi`; `build.rs` coordinates native build metadata and crate feature wiring.
- inputs_outputs_state: Inputs are JS calls carrying paths, patterns, command strings, terminal data, image/text buffers, and process options. Outputs are typed N-API structs, streams, shell events, match sets, text metrics, and rendered artifacts. State includes filesystem caches, native task promises, shell/PTY session lifecycle, embedded font data, and platform-specific runtime handles.
- gates_or_invariants: File traversal honors hidden/gitignore/node_modules gates; task APIs surface errors instead of panics; shell and PTY modules isolate process state; native APIs must remain ABI-compatible with JS loader expectations.
- dependencies_and_callers: Called from `packages/natives`, `packages/coding-agent`, TUI rendering, search/read/edit tools, shell execution, and Python native-cache tests. Depends on Rust crates for AST grep, terminal processing, text/image handling, and `napi`.
- edge_cases_or_failure_modes: Platform-specific native addon resolution, stale filesystem cache, unsupported AST languages, parse failures, command/session teardown, ANSI/Unicode width mismatch, large grep/text payload caps, and native binary variant mismatch.
- validation_or_tests: Covered indirectly by coding-agent search/read/apply-patch tests, TUI image/layout tests, Python native cache tests, and crate-level Rust validation tasks invoked by `scripts/run-rs-task.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-051 `file` `docs/mcp-config.md`
- cursor: `[_]`
- core_role: Architecture/runtime documentation for MCP configuration loading, storage, validation, authentication, and runtime discovery.
- algorithmic_behavior: Defines config precedence and locations such as `.omp/mcp.json`, `~/.omp/agent/mcp.json`, and profile-scoped config; describes schema writer behavior, server transport modes, disabled server handling, environment expansion, command resolution, and discovery precedence.
- inputs_outputs_state: Inputs are JSON config files, server definitions, auth metadata, environment variables, CLI setup operations, and profile context. Outputs are merged runtime MCP server descriptors, validation errors, persisted config updates, and auth/session state.
- gates_or_invariants: Server names and transports must validate; disabled servers stay configured but inactive; auth-sensitive fields are separated from ordinary config; pre-connect checks resolve env and commands before attempting server startup.
- dependencies_and_callers: Documents behavior implemented by `packages/coding-agent/src/mcp/config-writer.ts`, MCP command controller, settings/profile logic, and tool discovery/session wiring.
- edge_cases_or_failure_modes: Missing config files, malformed JSON, unsupported transport values, env var references that cannot resolve, duplicate server names, profile isolation mistakes, and stale server auth.
- validation_or_tests: Reflected by MCP config writer/controller tests and command conformance coverage; documentation provides the expected contract for runtime config behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-081 `file` `scripts/__init__.py`
- cursor: `[_]`
- core_role: Empty Python package marker for `scripts`.
- algorithmic_behavior: The file is zero bytes and contains no runtime algorithm, routing, monitor, validation, or state behavior.
- inputs_outputs_state: No inputs, outputs, or state transitions.
- gates_or_invariants: Only invariant is import/package marker presence if Python tooling treats `scripts` as a package.
- dependencies_and_callers: Potentially used by Python import discovery, but no direct algorithmic callers are present in the file.
- edge_cases_or_failure_modes: None in the file itself.
- validation_or_tests: No direct validation surface; classification as runtime script appears overbroad.
- skip_candidate: `yes: empty package marker with no executable or algorithmic content`

### OH_MY_HUMANIZE_MAIN-HZ-111 `file` `scripts/run-rs-task.ts`
- cursor: `[_]`
- core_role: Bun orchestration script for Rust-related repository tasks.
- algorithmic_behavior: Maps task names such as `check:rs`, `fix:rs`, `fmt:rs`, `lint:rs`, and `test:rs` to cargo/rustfmt commands; inspects `git status --porcelain -z` to skip non-format Rust tasks outside CI when no Rust-affecting paths changed; resolves `cargo` through `rustup which cargo`; prepends the active Rust toolchain bin dir to `PATH`; spawns selected task with inherited stdio.
- inputs_outputs_state: Inputs are task argv, CI env, git status, Rust toolchain availability, and repository file changes. Outputs are process exit code and console status messages. State is limited to computed task selection and environment overlay.
- gates_or_invariants: Unknown task fails; outside CI, expensive Rust commands are skipped unless Rust/crate files changed; cargo path must be found; child exit code propagates.
- dependencies_and_callers: Used by root/package scripts for Rust checks; depends on Bun shell/spawn, git, rustup, and cargo.
- edge_cases_or_failure_modes: Not a git repo, `rustup` missing, status parsing with rename paths, changed build files not recognized, child process signal/exit propagation, and inherited stdio noise.
- validation_or_tests: Validated by CI scripts that call Rust task aliases; no direct unit test observed in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-141 `directory` `packages/mnemopi/src`
- cursor: `[_]`
- core_role: Memory subsystem package implementing persistent semantic/episodic memory, recall, extraction, consolidation, embeddings, MCP tools, CLI, migrations, diagnostics, and runtime integration.
- algorithmic_behavior: Recursively includes `core/beam/*` SQLite-backed memory schema/store/recall/consolidation, `core/embeddings.ts`, vector math/indexing, extraction prompts/client/diagnostics, query intent/cache, episodic graph, triples, temporal parser, veracity consolidation, streaming sync, runtime options, CLI, MCP server/tools, disaster recovery, migrations, and utility modules.
- inputs_outputs_state: Inputs are conversations, dictionary imports, memory queries, embedding provider options, LLM extraction results, CLI/MCP requests, and SQLite DB paths. Outputs are recalled memories, facts, timelines, instructions, stats, diagnostics, and persisted DB records. State is held in SQLite tables, embedding caches, runtime `AsyncLocalStorage` options, migrations, and cost logs.
- gates_or_invariants: Migrations must be additive; embeddings must match configured variant; recall should respect bank/kind/time filters; import cleanup removes orphan vector episodes; schema indexes and FTS triggers preserve query behavior.
- dependencies_and_callers: Used by coding-agent memory integrations, MCP memory tools, CLI commands, tests under `packages/mnemopi/test`, and runtime options from `packages/coding-agent`.
- edge_cases_or_failure_modes: Embedding variant mismatch, orphan vector rows, stale query cache, incomplete migrations, malformed extracted facts, local LLM unavailability, temporal parsing ambiguity, and SQLite schema drift.
- validation_or_tests: Assigned tests cover CLI stats parity and orphan vector cleanup; schema/runtime options have direct assigned items.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-171 `file` `docs/toolconv/anthropic.md`
- cursor: `[_]`
- core_role: Tool-conversation architecture documentation for Anthropic Messages API conversion.
- algorithmic_behavior: Specifies Anthropic tool definitions in top-level `tools`, assistant `tool_use` blocks, user `tool_result` blocks, `stop_reason: tool_use`, streaming `input_json_delta`, thinking-block signatures, OpenAI-compatible mapping, and legacy XML behavior as informational.
- inputs_outputs_state: Inputs are internal tool definitions, message content blocks, streaming deltas, reasoning/thinking content, and tool result payloads. Outputs are Anthropic-compatible request/response blocks and normalized internal tool call/result events.
- gates_or_invariants: Tool result ordering must follow corresponding tool use; signed thinking blocks must be preserved; streaming JSON deltas must be accumulated before parsing; legacy XML should not drive modern conversion.
- dependencies_and_callers: Defines expected behavior for `packages/ai` dialect/provider conversion and duplicate-tool-result regression tests.
- edge_cases_or_failure_modes: Duplicate or orphan tool results, out-of-order tool blocks, partial JSON streaming, thinking signatures dropped during compaction, and provider-specific mismatch with OpenAI-style schemas.
- validation_or_tests: Covered by `packages/ai/test/duplicate-tool-results.test.ts`, Anthropic image/tool tests, and provider conversion regressions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-201 `file` `docs/tools/search.md`
- cursor: `[_]`
- core_role: Runtime documentation for the repository search tool algorithm and rendered output contract.
- algorithmic_behavior: Describes search inputs (`pattern`, `paths`, `i`, `gitignore`, `skip`), internal URL/archive/line selectors, native grep execution with timeout and context settings, hidden handling, result caps, grouped hashline/tree/detail output, and error behavior.
- inputs_outputs_state: Inputs are user search args, workspace paths, skip patterns, gitignore settings, internal URLs, and abort/timeout context. Outputs are grouped matches, line previews, hashline references, and error summaries.
- gates_or_invariants: Search should use native grep, hide by default, enforce caps/timeouts, respect path selectors and gitignore unless overridden, and sanitize/truncate rendered output.
- dependencies_and_callers: Documents coding-agent search/read rendering, native grep in `crates/pi-natives`, and tool renderer behavior.
- edge_cases_or_failure_modes: Too many matches, binary/hidden files, invalid regex, invalid internal selector, timeout, empty pattern, and truncated details.
- validation_or_tests: Related to assigned multi-search path tests and read-column truncation snapshots.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-231 `directory` `packages/ai/src/auth-broker`
- cursor: `[_]`
- core_role: Auth broker subsystem for remote credential snapshots, refresh, caching, and broker-backed account storage.
- algorithmic_behavior: Contains `server.ts` HTTP routes, `client.ts` broker client, `remote-store.ts` AuthStorage adapter, `snapshot-cache.ts` encrypted cache, `refresher.ts`, `wire-schemas.ts`, and shared `types.ts`. Server exposes unauthenticated health and bearer-protected snapshot/usage/credential routes, ETag/generation long-poll, SSE streaming, and background refresh.
- inputs_outputs_state: Inputs are broker URL/token, OAuth credentials, account records, refresh requests, ETags, and encrypted cache files. Outputs are validated snapshots, credential updates, refresh/disable/upload responses, and SSE/long-poll events. State includes generation counters, cached snapshots, refresh status, and AES-GCM cache entries.
- gates_or_invariants: Wire schemas reject unknown keys except approved OAuth extension fields; uploads reject remote refresh sentinels; broker mutations route through server; remote store forbids local writes; cache uses token-derived SHA-256 key and URL as AAD.
- dependencies_and_callers: Used by `packages/ai` AuthStorage, registry OAuth providers, coding-agent login/config flows, and dry-balance/auth diagnostics.
- edge_cases_or_failure_modes: SSE unsupported or 404 fallback, token mismatch, stale ETag, broker timeout, invalid snapshot schema, cache decrypt failure, remote write attempts, and refresh races.
- validation_or_tests: Assigned auth-storage identity and auth-related AI tests exercise identity/credential behavior; broker schemas are validation gates.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-261 `directory` `packages/coding-agent/src/exec`
- cursor: `[_]`
- core_role: Command execution subsystem for bash/shell tool calls and non-interactive environment normalization.
- algorithmic_behavior: Contains `bash-executor.ts`, `exec.ts`, and `non-interactive-env.ts`. `executeBash` uses native `Shell`, manages session reuse/quarantine, applies non-interactive env, wraps user shell commands, streams output through sinks, truncates/artifacts large output, supports minimizer options, and handles abort/teardown.
- inputs_outputs_state: Inputs are command text, cwd, env overrides, timeout/abort signals, shell/session options, and output minimizer settings. Outputs are exit status, stdout/stderr/render summaries, artifacts, and session state changes. State includes reusable shell sessions and quarantined failed sessions.
- gates_or_invariants: Disables pagers/prompts/color where appropriate; command execution must respect aborts and cwd; output caps protect TUI; shell sessions cannot be reused after unsafe failure.
- dependencies_and_callers: Called by bash tool runtime, workflow script runtime, eval runtime, and task tools. Depends on `crates/pi-natives` shell/PTY and `crates/pi-shell` minimizer.
- edge_cases_or_failure_modes: Interactive prompt hangs, shell startup failure, Windows UTF-8 env only when absent, artifact spillover, abort races, session desynchronization, and minimizer misclassification.
- validation_or_tests: Covered by eval process stdio capture, workflow eval/script runtime tests, task spawn tests, and shell minimizer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-291 `directory` `packages/coding-agent/src/workflow`
- cursor: `[_]`
- core_role: Workflow DSL/runtime engine for graph-based agent/script/human/review workflows.
- algorithmic_behavior: Recursively includes YAML/DSL definition parsing, state schema, JSON-pointer state read/write gates, condition evaluation, scheduler, runner, lifecycle persistence, runtime binding, node runtimes, prompt/model resolution, graph inspection, package loading, liveness, artifact registry, timeout handling, and workflow-specific tests.
- inputs_outputs_state: Inputs are workflow YAML, run snapshots, graph patches, state patches, activations, runtime capabilities, model assignments, prompts, and human/tool responses. Outputs are persisted runs, checkpoints, activations, artifacts, graph inspection summaries, lifecycle records, and node results.
- gates_or_invariants: Validates nodes/edges/waitFor/prompt/migrations/subflows; state patches are limited to allowed paths and size/schema; transcript/raw output writes are blocked; scheduler enforces limits and aborts; liveness blocks script-only stalled cycles after repeated activations without progress.
- dependencies_and_callers: Used by coding-agent workflow commands, eval tool runtime, session/task runtimes, monitor UI, and assigned workflow tests.
- edge_cases_or_failure_modes: Cyclic or invalid graphs, unsupported runtime host, stalled script cycles, invalid JSON pointer, oversized state, failed checkpoint, model resolution failure, and graph patch conflicts.
- validation_or_tests: Directory contains runner/session-runtime/shell-script-runtime/graph-view tests; assigned eval-tool-runtime and inspection item cover specific contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-321 `directory` `packages/collab-web/src/components`
- cursor: `[_]`
- core_role: React collaboration UI component set for displaying agent activity, session transcripts, shell chrome, composer, banners, toasts, and tool cards.
- algorithmic_behavior: `agents/AgentDrawer.tsx` polls transcript JSONL and exposes cancel/retry/send controls; `AgentsPanel.tsx` summarizes rows with current tool/activity/duration/cost/tokens; shell components render connect/header/composer/toasts; transcript components render Markdown, tool cards, active tool state, and memoized rows.
- inputs_outputs_state: Inputs are collab host websocket/API state, transcript entries, agent events, user composer text, command status, and tool-render payloads. Outputs are DOM views, user actions, and visual state transitions. State is held in React component state, polling timers, and CSS class-driven display state.
- gates_or_invariants: Transcript rendering must sanitize markdown/tool payloads; controls must reflect connection/session state; active tools should not duplicate historical rows; polling needs cleanup.
- dependencies_and_callers: Used by `packages/collab-web` app shell and `packages/coding-agent/src/collab/host.ts` wire protocol.
- edge_cases_or_failure_modes: Missing transcript files, stale agent status, websocket disconnects, oversized markdown/tool output, retry/cancel race, and CSS overflow.
- validation_or_tests: Fixture generation and tool-render tests provide contract examples; no direct component test in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-351 `file` `crates/pi-natives/src/ast.rs`
- cursor: `[_]`
- core_role: Native AST grep/match/edit implementation.
- algorithmic_behavior: Exports `ast_grep` at line 577, `ast_match` at line 738, and `ast_edit` at line 844. It normalizes search paths, resolves/infer languages, collects candidates through fs cache, compiles ast-grep patterns, sorts matches, reports parse errors non-fatally for search, and stages edit writes before flushing.
- inputs_outputs_state: Inputs are path/lang/pattern/rewrite/limit/dry-run options and file content. Outputs are match records, parse errors, replacement file changes, and write counts. State includes candidate lists and pending writes.
- gates_or_invariants: `normalize_pattern_list` rejects empty patterns at line 453; `normalize_rewrite_map` rejects empty rewrites at line 473; default find limit is 50; `ast_edit` defaults dry-run true and requires explicit language for ambiguous multi-language replacements.
- dependencies_and_callers: Depends on ast-grep language/parser APIs and native fs cache; called by JS native bindings for structural search/edit tools.
- edge_cases_or_failure_modes: Unsupported file extension, parse errors, stale empty fs cache forcing rescan, multiple unresolved languages, max replacements/files, and `fail_on_parse_error` edit gate.
- validation_or_tests: Covered by structural edit/search consumers and apply-patch/read/search regressions; Rust task script runs crate checks.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-381 `file` `crates/pi-shell/src/minimizer.rs`
- cursor: `[_]`
- core_role: Shell output minimizer coordinator.
- algorithmic_behavior: Defines `MinimizerCtx` at line 24, `MinimizerOutput` at line 37, and `apply` at line 147. It selects command-specific filters, computes output reductions, and returns raw/summary/fallback data depending on command plan and exit status.
- inputs_outputs_state: Inputs are command string/plan, stdout/stderr text, exit code, and minimizer context. Outputs are minimized text plus metadata about applied filters and raw preservation. State is per-call only.
- gates_or_invariants: Should never hide critical failures; preserves enough failure context on nonzero exit; only applies filters for supported command patterns.
- dependencies_and_callers: Uses `minimizer/plan.rs` and filters such as `filters/cargo.rs`; called from coding-agent bash executor.
- edge_cases_or_failure_modes: Unsupported shell syntax, huge logs, success output with warnings, command plan ambiguity, and over-aggressive filtering.
- validation_or_tests: Rust shell minimizer tests and bash executor output tests validate the visible contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-411 `file` `packages/agent/test/serialize-conversation.test.ts`
- cursor: `[_]`
- core_role: Regression validation for conversation serialization behavior.
- algorithmic_behavior: Test suite `serializeConversation — useless pairs` begins at line 39 and verifies pruning/retention of tool-call and result pairs during serialization.
- inputs_outputs_state: Inputs are constructed conversation/message entries with useful/useless tool pairs. Outputs are serialized conversations with expected entries retained or dropped. State is test-local.
- gates_or_invariants: Serialization must not emit useless pairs while preserving semantically required tool interactions.
- dependencies_and_callers: Exercises `packages/agent` conversation serializer used by agent runtime and compaction paths.
- edge_cases_or_failure_modes: Orphaned tool results, assistant tool calls without meaningful output, accidental deletion of needed context, and ordering changes.
- validation_or_tests: The file itself is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-441 `file` `packages/ai/test/anthropic-many-image-resize.test.ts`
- cursor: `[_]`
- core_role: Anthropic image payload resizing validation.
- algorithmic_behavior: Suite `Anthropic many-image payload resizing` begins at line 127 and checks many-image payload processing against provider limits and resize behavior.
- inputs_outputs_state: Inputs are messages containing multiple image blocks and provider/model constraints. Outputs are resized/converted request payloads and retained textual content. State is mocked/test-local image data.
- gates_or_invariants: Total image payload must fit provider policy without dropping required message structure; resizing should preserve MIME and ordering semantics.
- dependencies_and_callers: Exercises AI provider conversion and coding-agent image resize utilities.
- edge_cases_or_failure_modes: Too many images, oversized images, unsupported formats, repeated resize attempts, and message block ordering loss.
- validation_or_tests: The test file provides regression coverage for Anthropic request conversion.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-471 `file` `packages/ai/test/auth-storage-account-identity.test.ts`
- cursor: `[_]`
- core_role: AuthStorage account identity contract validation.
- algorithmic_behavior: Suite `AuthStorage.getOAuthAccountIdentity` begins at line 10 and verifies account identity extraction from stored OAuth credentials.
- inputs_outputs_state: Inputs are mocked auth storage records and provider/account metadata. Outputs are normalized account identity objects or absence values. State is test-local storage fixtures.
- gates_or_invariants: Identity lookup must be deterministic and should not confuse provider credentials or missing account fields.
- dependencies_and_callers: Exercises `packages/ai` AuthStorage used by OAuth registries, auth broker, and account selection.
- edge_cases_or_failure_modes: Missing identity claims, multiple accounts, malformed records, and provider mismatch.
- validation_or_tests: The assigned test is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-501 `file` `packages/ai/test/duplicate-tool-results.test.ts`
- cursor: `[_]`
- core_role: Comprehensive regression suite for duplicate/orphan tool-result handling and Codex-style abort handling.
- algorithmic_behavior: Contains suites `Duplicate Tool Results Regression` at line 29, `Orphan Tool Result (handoff/compaction) Regression` at line 584, and `Codex-style Abort Handling` at line 1082. It builds provider message histories and verifies tool calls/results are paired once.
- inputs_outputs_state: Inputs are synthetic conversations, tool calls, tool results, handoff/compaction states, and abort events. Outputs are provider-ready messages/events without duplicate tool results. State is test-local conversation history.
- gates_or_invariants: A tool result must correspond to exactly one tool call; orphaned results must be handled safely; abort handling must not corrupt subsequent provider payloads.
- dependencies_and_callers: Exercises AI dialect conversion for Anthropic/OpenAI/Codex-like flows and agent serialization.
- edge_cases_or_failure_modes: Duplicate result replay, compaction handoff leaving orphan result, tool-call ID mismatch, aborted turn with partial tool state.
- validation_or_tests: The file is the regression suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-531 `file` `packages/ai/test/issue-1207-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for DeepSeek V4 reasoning/tool continuation behavior.
- algorithmic_behavior: Suite `issue #1207 — DeepSeek V4 keeps reasoning with tools` starts at line 56 and reproduces a provider stream where reasoning must continue correctly around tool use.
- inputs_outputs_state: Inputs are mocked DeepSeek-style streaming events and tool interaction history. Outputs are normalized assistant/tool events and continuation decisions.
- gates_or_invariants: Reasoning content should not be lost or prematurely terminated when tool calls occur.
- dependencies_and_callers: Exercises AI provider conversion and streaming event handling.
- edge_cases_or_failure_modes: Reasoning blocks after tool calls, incomplete stream finalization, provider-specific event ordering.
- validation_or_tests: Direct issue regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-561 `file` `packages/ai/test/litellm-login.test.ts`
- cursor: `[_]`
- core_role: LiteLLM login behavior validation.
- algorithmic_behavior: Suite `LiteLLM login` begins at line 4 and verifies registry login/default token handling for LiteLLM-compatible configuration.
- inputs_outputs_state: Inputs are login options/env/config fixtures. Outputs are credential records or login prompts/defaults. State is test-local.
- gates_or_invariants: Login must produce usable auth config without leaking unrelated provider semantics.
- dependencies_and_callers: Exercises AI registry login path used by coding-agent authentication setup.
- edge_cases_or_failure_modes: Missing token, malformed base URL, and conflicting env/config credentials.
- validation_or_tests: The assigned test is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-591 `file` `packages/ai/test/openai-output-token-policy.test.ts`
- cursor: `[_]`
- core_role: OpenAI output token and gateway routing policy validation.
- algorithmic_behavior: Suites `resolveOpenAIOutputTokenParam` at line 25 and `applyOpenAIGatewayRouting` at line 120 validate max token parameter selection and gateway routing changes.
- inputs_outputs_state: Inputs are model metadata, provider options, token limits, and gateway routing settings. Outputs are request parameter choices and transformed provider routing config.
- gates_or_invariants: Should select the provider-correct output token field; gateway routing must not override incompatible explicit settings.
- dependencies_and_callers: Exercises OpenAI provider request builders and gateway routing helpers.
- edge_cases_or_failure_modes: Legacy `max_tokens` vs `max_completion_tokens`, model-specific unsupported params, and gateway route conflicts.
- validation_or_tests: The file itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-621 `file` `packages/ai/test/requires-effort.test.ts`
- cursor: `[_]`
- core_role: Thinking effort clamping validation.
- algorithmic_behavior: Suite `thinking.requiresEffort clamping` starts at line 57 and tests how requested effort is adjusted for models requiring explicit effort handling.
- inputs_outputs_state: Inputs are model thinking metadata and requested effort values. Outputs are clamped/normalized thinking configs. State is test-local.
- gates_or_invariants: Required effort models must not receive unsupported missing/low effort; unrelated models should not be over-constrained.
- dependencies_and_callers: Exercises catalog thinking policy and AI request configuration.
- edge_cases_or_failure_modes: `xhigh` unsupported by model, missing effort defaults, and false positives for non-thinking models.
- validation_or_tests: Direct policy regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-651 `file` `packages/ai/test/xhigh.test.ts`
- cursor: `[_]`
- core_role: Validation for `xhigh` reasoning effort support.
- algorithmic_behavior: Tests model/provider thinking config paths that accept, translate, or reject `xhigh`.
- inputs_outputs_state: Inputs are model definitions and requested reasoning effort. Outputs are normalized request effort values or validation errors. State is test-local.
- gates_or_invariants: `xhigh` must be preserved only where provider/model supports it and downgraded/rejected consistently elsewhere.
- dependencies_and_callers: Exercises AI/catalog thinking config consumed by coding-agent model selection.
- edge_cases_or_failure_modes: Provider effort enum mismatch, missing catalog flags, and accidental normalization to ordinary `high`.
- validation_or_tests: The file is direct regression coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-681 `file` `packages/catalog/test/google-vertex-discovery.test.ts`
- cursor: `[_]`
- core_role: Google Vertex model catalog discovery validation.
- algorithmic_behavior: Suite `google-vertex model catalog` starts at line 46 and validates discovery/resolution for Vertex catalog entries.
- inputs_outputs_state: Inputs are mocked/discovered provider model metadata and catalog descriptors. Outputs are normalized catalog models. State is fixture-local.
- gates_or_invariants: Discovery must map Vertex IDs, capabilities, and provider metadata consistently without corrupting bundled catalog assumptions.
- dependencies_and_callers: Exercises `packages/catalog` provider discovery used by `@oh-my-pi/pi-catalog`.
- edge_cases_or_failure_modes: Region/provider naming differences, missing metadata, unsupported models, and resolver fallback.
- validation_or_tests: The file is direct catalog validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-711 `file` `packages/catalog/test/zai-bundled-catalog.test.ts`
- cursor: `[_]`
- core_role: Zai bundled catalog validation.
- algorithmic_behavior: Suite `zai bundled catalog` starts at line 12 and checks that the bundled catalog contains expected Zai provider model data.
- inputs_outputs_state: Inputs are bundled model JSON/catalog accessors. Outputs are assertions about provider/model presence or metadata. State is static fixture/catalog state.
- gates_or_invariants: Bundled catalog must expose required Zai entries after generation.
- dependencies_and_callers: Exercises generated catalog consumed by AI model selection.
- edge_cases_or_failure_modes: Missing generated entry, wrong provider key, stale catalog regeneration.
- validation_or_tests: Direct catalog test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-741 `file` `packages/coding-agent/test/acp-initialize-conformance.test.ts`
- cursor: `[_]`
- core_role: ACP initialize protocol conformance validation.
- algorithmic_behavior: Suite `ACP initialize conformance` starts at line 173 and verifies the coding-agent ACP initialization handshake, capabilities, and response shape.
- inputs_outputs_state: Inputs are ACP initialize requests and mock host/session dependencies. Outputs are protocol responses and capability metadata. State is test-local session/server state.
- gates_or_invariants: Initialize must be idempotent/valid, report required capabilities, and reject malformed sequencing per ACP contract.
- dependencies_and_callers: Exercises coding-agent ACP server/session integration.
- edge_cases_or_failure_modes: Missing client info, repeated initialize, unsupported protocol version, and malformed capability payload.
- validation_or_tests: Direct conformance test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-771 `file` `packages/coding-agent/test/agent-session-message-pipeline.test.ts`
- cursor: `[_]`
- core_role: AgentSession message pipeline validation.
- algorithmic_behavior: Suite `AgentSession message pipeline` starts at line 54 and tests how user/assistant/tool events flow through the session pipeline.
- inputs_outputs_state: Inputs are mocked model streams, user messages, tool events, and session setup. Outputs are stored session entries, emitted events, and model requests. State includes test session history.
- gates_or_invariants: Message ordering, tool-call/result pairing, and session event emission must remain coherent.
- dependencies_and_callers: Exercises `packages/coding-agent/src/session/agent-session.ts` and AI conversion boundaries.
- edge_cases_or_failure_modes: Streaming partials, tool execution interleaving, aborted turns, and duplicate events.
- validation_or_tests: The file is direct validation of the pipeline.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-801 `file` `packages/coding-agent/test/autocomplete-max-visible.test.ts`
- cursor: `[_]`
- core_role: Autocomplete visibility setting validation.
- algorithmic_behavior: Suite `autocompleteMaxVisible setting` starts at line 11 and verifies max visible suggestion count handling.
- inputs_outputs_state: Inputs are settings values and autocomplete suggestion lists. Outputs are rendered/selected visible suggestions. State is test-local UI/controller state.
- gates_or_invariants: Configured max must cap visible suggestions without breaking selection behavior.
- dependencies_and_callers: Exercises coding-agent input/autocomplete components.
- edge_cases_or_failure_modes: Zero/negative values, too many suggestions, and selection index beyond visible range.
- validation_or_tests: Direct setting test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-831 `file` `packages/coding-agent/test/compaction-hooks.test.ts`
- cursor: `[_]`
- core_role: Compaction hook behavior validation.
- algorithmic_behavior: Tests session compaction hook registration/execution and resulting transcript/context behavior.
- inputs_outputs_state: Inputs are session entries, compaction triggers, and hook callbacks. Outputs are compacted history and hook side effects. State is test-local session state.
- gates_or_invariants: Hooks must run at the correct lifecycle point and not duplicate/drop required context.
- dependencies_and_callers: Exercises agent session compaction integration and extension hooks.
- edge_cases_or_failure_modes: Hook throwing, repeated compaction, stale transcript rebuild, and lost tool results.
- validation_or_tests: The file itself validates compaction hook contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-861 `file` `packages/coding-agent/test/file-lock.test.ts`
- cursor: `[_]`
- core_role: File-lock token ownership validation.
- algorithmic_behavior: Suite `file-lock token ownership (F1)` starts at line 23 and verifies token-based lock ownership semantics.
- inputs_outputs_state: Inputs are lock paths, tokens, acquire/release attempts, and simulated ownership changes. Outputs are acquire/release outcomes. State is filesystem lock content in test temp paths.
- gates_or_invariants: Only the owner token can release/update a lock; stale or mismatched tokens must not unlock.
- dependencies_and_callers: Exercises coding-agent file lock utility used by concurrent/session operations.
- edge_cases_or_failure_modes: Stale files, concurrent acquisition, token mismatch, and cleanup after failure.
- validation_or_tests: Direct lock regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-891 `file` `packages/coding-agent/test/input-controller-python-prefix.test.ts`
- cursor: `[_]`
- core_role: Python prompt-prefix input controller validation.
- algorithmic_behavior: Suite `InputController Python prompt prefix` starts at line 83 and verifies how Python-style prompt prefixes are detected/handled in input.
- inputs_outputs_state: Inputs are editor text lines and cursor state. Outputs are normalized submitted text or retained prefixes. State is test-local input controller state.
- gates_or_invariants: Prefix stripping must not corrupt ordinary text; multi-line Python prompts must be handled consistently.
- dependencies_and_callers: Exercises coding-agent interactive input controller.
- edge_cases_or_failure_modes: Mixed prompt prefixes, indentation, pasted REPL sessions, and cursor offset changes.
- validation_or_tests: Direct UI/input test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-921 `file` `packages/coding-agent/test/issue-816-repro.test.ts`
- cursor: `[_]`
- core_role: Plan mode pending model switch leak regression.
- algorithmic_behavior: Suite `issue #816 — plan mode pendingModelSwitch leak` starts at line 13 and reproduces state leakage around plan mode/model switching.
- inputs_outputs_state: Inputs are mode transitions and model switch requests. Outputs are session state and effective model selection. State is test-local session/mode state.
- gates_or_invariants: Pending model switch must not leak across plan-mode boundaries incorrectly.
- dependencies_and_callers: Exercises coding-agent mode/session model selection.
- edge_cases_or_failure_modes: Aborted model switch, nested mode entry, stale pending value, and unintended model use.
- validation_or_tests: Direct issue regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-951 `file` `packages/coding-agent/test/lsp-format-options.test.ts`
- cursor: `[_]`
- core_role: LSP formatting option detection validation.
- algorithmic_behavior: Suites `detectIndentFromContent` at line 23 and `resolveFormatOptions` at line 58 validate indentation inference and LSP format option construction.
- inputs_outputs_state: Inputs are file content, language/options, and editor settings. Outputs are tab/space/size format options. State is test-local.
- gates_or_invariants: Detected indentation should override defaults only with evidence; output must satisfy LSP format expectations.
- dependencies_and_callers: Exercises coding-agent LSP formatting helpers.
- edge_cases_or_failure_modes: Mixed tabs/spaces, empty files, unusual indentation widths, and missing user settings.
- validation_or_tests: Direct formatting tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-981 `file` `packages/coding-agent/test/mnemopi-embedding-variant.test.ts`
- cursor: `[_]`
- core_role: Mnemopi embedding variant config validation.
- algorithmic_behavior: Suite `loadMnemopiConfig embedding variant resolution` starts at line 13 and verifies how coding-agent loads/resolves memory embedding variant settings.
- inputs_outputs_state: Inputs are config/env fixtures. Outputs are resolved embedding provider/variant settings. State is test-local config.
- gates_or_invariants: Configured embedding variant must be respected and defaulted consistently.
- dependencies_and_callers: Exercises coding-agent memory integration and `packages/mnemopi` runtime options.
- edge_cases_or_failure_modes: Missing config, invalid variant, env override precedence, and stale defaults.
- validation_or_tests: Direct config regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1011 `file` `packages/coding-agent/test/read-column-truncation-snapshot.test.ts`
- cursor: `[_]`
- core_role: Snapshot validation for read-tool truncation and hashline rendering.
- algorithmic_behavior: Suite `read tool column truncation vs hashline snapshot` starts at line 83 and verifies column-limited read previews against expected hashline snapshots.
- inputs_outputs_state: Inputs are synthetic/read file contents and render widths. Outputs are rendered read previews/snapshots. State is snapshot fixture state.
- gates_or_invariants: Long lines must truncate by display width without breaking hashline/link semantics.
- dependencies_and_callers: Exercises read tool renderer, TUI truncation utilities, and hashline output.
- edge_cases_or_failure_modes: Unicode width, tabs, long paths, line suffix selectors, and terminal-width variance.
- validation_or_tests: Direct snapshot regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1041 `file` `packages/coding-agent/test/sdk-preloaded-extensions-isolation.test.ts`
- cursor: `[_]`
- core_role: SDK preloaded extension isolation regression.
- algorithmic_behavior: Suite `createAgentSession preloadedExtensions isolation (issue #2190)` starts at line 25 and verifies extension lists do not leak between SDK-created sessions.
- inputs_outputs_state: Inputs are session creation options with preloaded extensions. Outputs are isolated session extension state. State is per-session test state.
- gates_or_invariants: Extension arrays/registries must not share mutable state across sessions.
- dependencies_and_callers: Exercises `createAgentSession` SDK/session factory.
- edge_cases_or_failure_modes: Shared array mutation, global registry pollution, repeated session creation, and extension order leakage.
- validation_or_tests: Direct issue regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1071 `file` `packages/coding-agent/test/stats-dashboard-bundle.test.ts`
- cursor: `[_]`
- core_role: Distributed CLI stats dashboard asset validation.
- algorithmic_behavior: Suite `stats dashboard assets in distributed CLI builds` starts at line 4 and verifies expected stats dashboard bundle assets exist for CLI distribution.
- inputs_outputs_state: Inputs are package build/dist file paths. Outputs are assertions about asset presence. State is static filesystem fixture.
- gates_or_invariants: Distributed CLI must include required stats dashboard assets.
- dependencies_and_callers: Exercises packaging expectations for `packages/stats` and coding-agent CLI.
- edge_cases_or_failure_modes: Missing dist asset, path relocation, build script omission.
- validation_or_tests: Direct packaging smoke test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1101 `file` `packages/coding-agent/test/theme-spinner-frames.test.ts`
- cursor: `[_]`
- core_role: Theme spinner frame validation.
- algorithmic_behavior: Suite `theme symbols.spinnerFrames` starts at line 34 and verifies theme parsing/defaulting for spinner frames.
- inputs_outputs_state: Inputs are theme configs. Outputs are normalized spinner frame arrays. State is test-local.
- gates_or_invariants: Spinner frames must be non-empty valid strings and fallback safely on invalid theme data.
- dependencies_and_callers: Exercises coding-agent theme loader/rendering.
- edge_cases_or_failure_modes: Empty frames, non-string entries, malformed theme file, and default fallback.
- validation_or_tests: Direct theme test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1131 `file` `packages/collab-web/scripts/fixture.ts`
- cursor: `[_]`
- core_role: Deterministic fixture generator for collab-web sessions.
- algorithmic_behavior: Creates mock session headers, transcript entries, agent rows, progress events, subagent transcript data, and scripted turns for UI development/testing.
- inputs_outputs_state: Inputs are hardcoded fixture templates and timestamps/status variations. Outputs are fixture JSON/session files or in-memory records used by collab UI. State is deterministic fixture state.
- gates_or_invariants: Generated fixtures must match wire protocol shapes consumed by collab components.
- dependencies_and_callers: Used by collab-web development scripts and component rendering scenarios.
- edge_cases_or_failure_modes: Wire schema drift, unrealistic transcript ordering, missing agent event variants, and fixture timestamps becoming misleading.
- validation_or_tests: UI fixture consumers implicitly validate shape; no direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1161 `file` `packages/hashline/test/block.test.ts`
- cursor: `[_]`
- core_role: Hashline block edit parser/resolver regression suite.
- algorithmic_behavior: Suites cover `SWAP.BLK parsing` at line 34, `resolveBlockEdits` at line 57, patch section block edits at line 169, patcher integration at line 196, `DEL.BLK` at line 270, and `INS.BLK.POST` at line 320.
- inputs_outputs_state: Inputs are hashline block-edit specs and original text. Outputs are resolved patch operations and transformed text. State is test-local.
- gates_or_invariants: Block edit commands must parse unambiguously and apply to correct regions without corrupting unrelated content.
- dependencies_and_callers: Exercises `packages/hashline` patching used by coding-agent edit/apply workflows.
- edge_cases_or_failure_modes: Missing anchors, duplicate blocks, insertion position ambiguity, deletion span mismatch, and partial apply behavior.
- validation_or_tests: Direct block edit suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1191 `file` `packages/mnemopi/test/cli-stats-parity.test.ts`
- cursor: `[_]`
- core_role: Mnemopi CLI stats parity validation.
- algorithmic_behavior: Suites `CLI stats parity` at line 64 and `mnemopi-stats diagnostic behavior parity` at line 126 compare CLI-visible stats behavior to expected diagnostic behavior.
- inputs_outputs_state: Inputs are test DB contents and CLI/stat command invocations. Outputs are formatted stats/diagnostics. State is temporary mnemopi DB state.
- gates_or_invariants: CLI stats and diagnostic paths must report equivalent facts/counts.
- dependencies_and_callers: Exercises mnemopi CLI, stats computation, and diagnostic modules.
- edge_cases_or_failure_modes: Empty DB, migration differences, stale stats, and display formatting drift.
- validation_or_tests: Direct parity test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1221 `file` `packages/mnemopi/test/orphan-vec-episodes-cleanup.test.ts`
- cursor: `[_]`
- core_role: Vector episode cleanup regression.
- algorithmic_behavior: Suite `importFromDict vec_episodes cleanup` starts at line 43 and validates cleanup of orphan vector episode rows during dictionary import.
- inputs_outputs_state: Inputs are dictionary import fixtures and existing DB rows. Outputs are cleaned DB state and import result. State is temporary SQLite memory database.
- gates_or_invariants: Vector episode records must correspond to live episodic rows after import.
- dependencies_and_callers: Exercises mnemopi import/migration/vector store behavior.
- edge_cases_or_failure_modes: Orphan rows, duplicate imports, missing foreign references, and partial cleanup.
- validation_or_tests: Direct regression test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1251 `file` `packages/natives/native/loader-state.js`
- cursor: `[_]`
- core_role: Native addon loader and cache state machine.
- algorithmic_behavior: Detects compiled-binary/embedded-addon modes, resolves platform/variant addon filenames, stages Windows node_modules copies, extracts embedded tarballs safely, validates version sentinels, cleans stale caches, selects AVX2 modern/baseline variants, installs Tokio runtime, and exposes `loadNative()`.
- inputs_outputs_state: Inputs are platform/arch/env/Bun runtime info, package paths, embedded addon metadata, and native cache contents. Outputs are loaded native module exports and cache files. State includes loader cache, extracted addon dirs, sentinel files, and runtime installation flag.
- gates_or_invariants: Extraction must prevent unsafe paths; cache sentinel must match version; platform variant must match current runtime; compiled binary mode cannot assume source file layout.
- dependencies_and_callers: Used by `packages/natives` JS entrypoints and all consumers of Rust native bindings.
- edge_cases_or_failure_modes: Missing addon, stale cache, antivirus/Windows file lock, unsupported platform, AVX2 mismatch, broken embedded tarball, and Bun compiled binary path quirks.
- validation_or_tests: Python native-cache tests and distributed CLI smoke tests exercise loader behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1281 `file` `packages/snapcompact/research/exp09_cacheappend.py`
- cursor: `[_]`
- core_role: Research experiment for prompt-cache append/compact strategies.
- algorithmic_behavior: Runs experiment comparing append-optical and rewrite-compact prompt cache behavior, renders pages, asks QA, scores F1/cost/token metrics, and writes records/steps/matrix/summary artifacts.
- inputs_outputs_state: Inputs are experiment configs, document/page data, model responses, and scoring functions. Outputs are metrics summaries and artifact files. State is experiment-run local.
- gates_or_invariants: Experiment scoring must keep compared strategies and token/cost accounting consistent.
- dependencies_and_callers: Research-only script under snapcompact; informs algorithm tuning but is not production runtime path.
- edge_cases_or_failure_modes: Model nondeterminism, cache accounting drift, failed page rendering, scoring ambiguity, and artifact path collisions.
- validation_or_tests: Self-validating through generated summaries; no production test observed.
- skip_candidate: `yes: research experiment artifact, not production runtime code`

### OH_MY_HUMANIZE_MAIN-HZ-1311 `file` `packages/snapcompact/research/snapcompact_convergence_viz.py`
- cursor: `[_]`
- core_role: Research visualization script for snapcompact convergence.
- algorithmic_behavior: Reads summary/npz outputs, renders convergence matrices/curves/answers to PNG, and visualizes carrier convergence behavior.
- inputs_outputs_state: Inputs are experiment summary arrays and visualization options. Outputs are image files. State is local plotting state.
- gates_or_invariants: Visualization should align summary dimensions and labels before plotting.
- dependencies_and_callers: Used manually with snapcompact research artifacts; not called by runtime package.
- edge_cases_or_failure_modes: Missing arrays, shape mismatch, matplotlib/backend availability, and stale summary schema.
- validation_or_tests: No direct runtime validation; visual inspection of generated figures.
- skip_candidate: `yes: research visualization artifact, not production runtime code`

### OH_MY_HUMANIZE_MAIN-HZ-1341 `file` `packages/snapcompact/src/index.ts`
- cursor: `[_]`
- core_role: Minimal snapcompact package entrypoint.
- algorithmic_behavior: The file is 31 bytes and functions as an export/entry surface rather than an implementation body.
- inputs_outputs_state: No runtime state transitions inside this file beyond re-export/module exposure.
- gates_or_invariants: Export path must remain stable for consumers.
- dependencies_and_callers: Imported by snapcompact package consumers.
- edge_cases_or_failure_modes: Broken export path if implementation files move.
- validation_or_tests: Package import/build checks would catch missing export.
- skip_candidate: `yes: index/export surface only`

### OH_MY_HUMANIZE_MAIN-HZ-1371 `file` `packages/tui/src/editor-component.ts`
- cursor: `[_]`
- core_role: TUI editor component interface/contract definition.
- algorithmic_behavior: Defines editor component shape for TUI consumers rather than implementing editing behavior.
- inputs_outputs_state: Inputs/outputs are TypeScript type-level contracts for editor state/events; no runtime state machine in the file itself.
- gates_or_invariants: Implementers must satisfy the interface expected by TUI/editor consumers.
- dependencies_and_callers: Used by TUI component implementations and coding-agent interactive editor wiring.
- edge_cases_or_failure_modes: Contract drift between interface and implementations.
- validation_or_tests: Type checking validates the contract.
- skip_candidate: `yes: type contract only, not an algorithm implementation`

### OH_MY_HUMANIZE_MAIN-HZ-1401 `file` `packages/tui/test/image-budget.test.ts`
- cursor: `[_]`
- core_role: TUI inline image budget and Kitty protocol validation.
- algorithmic_behavior: Suites cover `ImageBudget` at line 39, Kitty delete/placement/transmit encoding, image budget integration, Unicode placeholders, and inline image budget behavior through line 646.
- inputs_outputs_state: Inputs are image IDs, cell dimensions, transmit/placement data, terminal width, and render frames. Outputs are encoded Kitty commands, budget decisions, and rendered placeholders. State is test-local image budget state.
- gates_or_invariants: Image budget must avoid over-transmitting, correctly encode terminal commands, and preserve placeholder layout.
- dependencies_and_callers: Exercises `packages/tui` image rendering used by coding-agent media/tool output.
- edge_cases_or_failure_modes: Reused image IDs, delete command encoding, Unicode cell width, overflow budget, and duplicate transmit tracking.
- validation_or_tests: Direct test suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1431 `file` `packages/tui/test/overlay-scroll.test.ts`
- cursor: `[_]`
- core_role: TUI overlay scrolling validation.
- algorithmic_behavior: Suite `TUI overlays` starts at line 122 and checks overlay rendering/scroll behavior.
- inputs_outputs_state: Inputs are overlay content, viewport dimensions, scroll actions, and keyboard/mouse events. Outputs are rendered frames and scroll offsets. State is test-local TUI overlay state.
- gates_or_invariants: Overlay scroll must remain bounded and not corrupt base layout.
- dependencies_and_callers: Exercises TUI overlay manager used by coding-agent modals/logs/help surfaces.
- edge_cases_or_failure_modes: Content shorter than viewport, max scroll, resize, nested overlay, and off-by-one clipping.
- validation_or_tests: Direct overlay test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1461 `file` `packages/tui/test/tight-layout.test.ts`
- cursor: `[_]`
- core_role: TUI tight-layout option validation.
- algorithmic_behavior: Suite `TUI Tight Layout option` starts at line 9 and verifies rendering differences under compact layout settings.
- inputs_outputs_state: Inputs are layout option flags and component trees. Outputs are rendered frame dimensions/content. State is test-local renderer state.
- gates_or_invariants: Tight layout should reduce spacing without breaking component boundaries.
- dependencies_and_callers: Exercises TUI renderer used by coding-agent terminal UI.
- edge_cases_or_failure_modes: Width underflow, component overlap, and inconsistent spacing.
- validation_or_tests: Direct layout test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1491 `file` `packages/utils/src/glob.ts`
- cursor: `[_]`
- core_role: Shared globbing utility.
- algorithmic_behavior: Uses Bun `Glob`, always excludes `.git`, excludes `node_modules` unless the pattern explicitly references it, optionally parses gitignore-like excludes, supports abort/timeout, and returns normalized relative paths.
- inputs_outputs_state: Inputs are root path, include patterns, exclude patterns/gitignore options, and abort signal. Outputs are matching relative paths. State is per-call pattern/exclusion matcher state.
- gates_or_invariants: Results should be normalized; `.git` must be excluded; abort and timeout should stop traversal.
- dependencies_and_callers: Used by coding-agent file discovery/search/workflow utilities and package scripts.
- edge_cases_or_failure_modes: Negated gitignore unsupported, duplicate matches, Windows path separators, broad globs over large trees, and timeout races.
- validation_or_tests: Indirectly covered by search/multi-search path tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1521 `file` `packages/utils/test/format.test.ts`
- cursor: `[_]`
- core_role: Duration formatting validation.
- algorithmic_behavior: Suite `formatDuration` starts at line 4 and verifies utility formatting for elapsed durations.
- inputs_outputs_state: Inputs are numeric durations. Outputs are formatted strings. State is pure/test-local.
- gates_or_invariants: Formatting must be stable across ranges and boundary values.
- dependencies_and_callers: Exercises shared utils consumed across CLI/TUI/status displays.
- edge_cases_or_failure_modes: Zero, sub-second, minute/hour boundaries, and rounding.
- validation_or_tests: Direct unit test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1551 `file` `python/robomp/src/cli.py`
- cursor: `[_]`
- core_role: Python CLI for robomp orchestration/proxy workflows.
- algorithmic_behavior: Defines Click commands such as `serve`, `triage`, `replay`, `status`, and `cleanup`; refuses orchestrator mode when `GITHUB_TOKEN` is set; requires proxy URL/HMAC for proxy-backed operations; waits for terminal job states.
- inputs_outputs_state: Inputs are CLI args/env, GitHub/proxy config, and task identifiers. Outputs are command status, server process execution, and cleanup/replay effects. State includes local CLI runtime and remote/proxy job status.
- gates_or_invariants: Secrets should stay in proxy process; orchestrator must not run with direct GitHub token; HMAC config required for proxy communication.
- dependencies_and_callers: Calls `python/robomp/src/proxy/server.py` and robomp orchestration modules; used by operators/automation.
- edge_cases_or_failure_modes: Missing env, proxy unavailable, job timeout, cleanup races, and accidental direct token exposure.
- validation_or_tests: Python native/proxy-related tests cover nearby infrastructure; no assigned direct CLI test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1581 `file` `python/robomp/tests/test_natives_cache.py`
- cursor: `[_]`
- core_role: Python validation for native cache/loader behavior.
- algorithmic_behavior: Tests native cache extraction/loading scenarios from Python-side integration, likely around compiled/native artifact cache handling.
- inputs_outputs_state: Inputs are temp cache directories, simulated native artifacts, env/path variants, and loader calls. Outputs are assertions on cache layout and load behavior. State is temporary filesystem cache.
- gates_or_invariants: Cache paths must be safe, versioned, and reusable; stale/incompatible artifacts should not be accepted.
- dependencies_and_callers: Exercises native loader behavior associated with `packages/natives/native/loader-state.js`.
- edge_cases_or_failure_modes: Stale cache, platform variant mismatch, missing sentinel, unsafe extraction, and concurrent cache access.
- validation_or_tests: The file is direct cache validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1611 `directory` `packages/coding-agent/src/commit/git`
- cursor: `[_]`
- core_role: Git diff parsing helpers for commit/analysis workflows.
- algorithmic_behavior: Directory contains `diff.ts`, which parses git diff/numstat/hunk data into structured change information for higher-level commit analysis and review features.
- inputs_outputs_state: Inputs are git diff text, numstat output, and file path metadata. Outputs are structured file changes, hunks, additions/deletions, and stats. State is per-parse.
- gates_or_invariants: Parser must preserve file paths and hunk boundaries while tolerating binary/rename/stat formats.
- dependencies_and_callers: Used by coding-agent commit generation/analysis modules and possibly collab/tool display.
- edge_cases_or_failure_modes: Renames, binary files, quoted paths, spaces/tabs in file names, no-newline markers, and malformed diff.
- validation_or_tests: Commit/patch regression tests indirectly cover diff application and analysis surfaces.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1641 `directory` `packages/coding-agent/src/web/search`
- cursor: `[_]`
- core_role: Web search provider abstraction, execution pipeline, and rendering.
- algorithmic_behavior: Contains provider registry, `executeSearch`, shared types/utils, renderers, and provider implementations for Anthropic, Brave, Codex, Exa, Gemini, Jina, Kagi, Kimi, Parallel, Perplexity, SearXNG, Synthetic, Tavily, and Zai. The chain resolves configured providers, applies preferred/excluded provider settings, falls back across providers, and formats answer/sources/citations/related queries.
- inputs_outputs_state: Inputs are search query/options, provider settings, AuthStorage, abort signal, and model/provider credentials. Outputs are normalized web search results, rendered content, citations, source lists, or classified errors. State includes provider config and auth lookups.
- gates_or_invariants: Providers must use the passed `AuthStorage`; aborts propagate; antigravity setting is guarded; no-renderable-content is an error; `ParallelProvider` uses hard timeout and classified HTTP errors.
- dependencies_and_callers: Called by coding-agent web/search tools and setup wizard; depends on `packages/ai` auth and provider clients.
- edge_cases_or_failure_modes: Missing credentials, provider timeout, empty results, unsupported provider, malformed citations, partial provider outage, and dynamic provider import failure.
- validation_or_tests: Assigned multi-search-path and web-scraper tests cover related web tooling; provider-specific tests likely exist outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1671 `file` `crates/pi-shell/src/minimizer/plan.rs`
- cursor: `[_]`
- core_role: Shell command plan classifier for output minimization.
- algorithmic_behavior: `analyze` at line 68 parses shell with `brush-parser`; `classify` at line 86 distinguishes single, piped, chain, compound, and unsupported commands; chain classification at line 126 segments safe `&&`/`;` commands; pipelines at line 266 are opaque.
- inputs_outputs_state: Input is shell command string. Output is `CommandPlan` with segment/subcommand data or unsupported classification. State is parse tree only.
- gates_or_invariants: Command/process substitution and here-docs are rejected for segmentation; only safe simple commands become segmentable.
- dependencies_and_callers: Used by `minimizer.rs` and command-specific filters.
- edge_cases_or_failure_modes: Complex quoting, redirects, process substitution, shell syntax parse failure, compound commands, and pipelines with hidden failure semantics.
- validation_or_tests: Shell minimizer tests validate classification indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1701 `file` `packages/ai/src/dialect/coercion.ts`
- cursor: `[_]`
- core_role: Tool argument and streaming-tag coercion helpers for AI dialect conversion.
- algorithmic_behavior: Builds argument shapes from tool schemas at line 10, resolves string-only args at line 28, decodes/coerces JSON values, mints tool call IDs at line 109, computes partial suffix overlaps for streaming tags at line 114, and normalizes Kimi function names at line 128.
- inputs_outputs_state: Inputs are inband tool schemas, raw streamed strings, tool/function names, and partial text. Outputs are coerced argument values, schema type sets, generated IDs, and overlap lengths. State is an incrementing ID counter.
- gates_or_invariants: Only decode JSON when schema indicates structured values; protect string-only schemas; overlap logic must not duplicate or drop partial tags.
- dependencies_and_callers: Used by AI dialect converters for OpenAI/Anthropic/Kimi-like tool calling.
- edge_cases_or_failure_modes: Invalid JSON, ambiguous schema unions, arrays/objects represented as strings, and provider function-name restrictions.
- validation_or_tests: Covered by duplicate tool-result/provider conversion tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1731 `file` `packages/ai/src/providers/azure-openai-responses.ts`
- cursor: `[_]`
- core_role: Azure OpenAI Responses API streaming provider implementation.
- algorithmic_behavior: `streamAzureOpenAIResponses` starts at line 73, resolves deployment/base/api-version, builds request params/tools/reasoning/tool choice, performs manual SSE streaming, repairs raw SSE events, and enforces first-event/idle watchdogs.
- inputs_outputs_state: Inputs are model config, stream options, auth/base URL/api version, messages/tools, and abort signals. Outputs are normalized assistant/tool/reasoning stream events. State includes stream parser/watchdog state.
- gates_or_invariants: Deployment name required; API version defaults to `v1`; first event timeout must fail clearly; provider errors finalize with details.
- dependencies_and_callers: Used by `packages/ai` provider registry for Azure Responses-compatible models.
- edge_cases_or_failure_modes: Missing deployment, malformed SSE chunks, idle stream, provider error event, unsupported tool choice, and auth/base URL mismatch.
- validation_or_tests: OpenAI output policy and provider stream tests cover related request behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1761 `file` `packages/ai/src/providers/synthetic.ts`
- cursor: `[_]`
- core_role: Synthetic provider shim for testing or synthetic OpenAI/Anthropic-style behavior.
- algorithmic_behavior: Provides a small provider implementation that routes synthetic model behavior through existing provider-like stream contracts.
- inputs_outputs_state: Inputs are synthetic model/options/messages. Outputs are normalized assistant stream events. State is minimal/provider-local.
- gates_or_invariants: Must preserve the same stream event shape as real providers so tests/runtime can swap it in.
- dependencies_and_callers: Used by AI tests, synthetic provider registry entries, and coding-agent dry/test flows.
- edge_cases_or_failure_modes: Diverging from real provider event contract, unsupported tool calls, and missing synthetic fixture behavior.
- validation_or_tests: AI stream/provider tests indirectly exercise synthetic behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1791 `file` `packages/ai/src/registry/lm-studio.ts`
- cursor: `[_]`
- core_role: LM Studio provider registry/login descriptor.
- algorithmic_behavior: Defines optional prompt login/default token behavior and registry metadata for LM Studio-compatible local server use.
- inputs_outputs_state: Inputs are provider settings/base URL/token prompt responses. Outputs are registry login/auth configuration. State is stored auth/config entries.
- gates_or_invariants: Local provider should work with default token behavior while allowing explicit configuration.
- dependencies_and_callers: Used by AI registry and coding-agent login/setup flows.
- edge_cases_or_failure_modes: LM Studio server missing, bad base URL, absent token, and model discovery mismatch.
- validation_or_tests: Login/provider registry tests cover similar registry paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1821 `file` `packages/ai/src/registry/wafer-serverless.ts`
- cursor: `[_]`
- core_role: Wafer Serverless provider registry descriptor.
- algorithmic_behavior: Registers Wafer Serverless provider with lazy OAuth login/auth behavior.
- inputs_outputs_state: Inputs are provider login/config requests. Outputs are auth configuration and provider descriptor metadata. State is stored OAuth/account data.
- gates_or_invariants: Auth flow should be invoked lazily and only when needed.
- dependencies_and_callers: Used by AI registry and coding-agent provider setup.
- edge_cases_or_failure_modes: Missing OAuth credentials, failed login, provider unavailable.
- validation_or_tests: Registry OAuth tests cover analogous flows.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1851 `file` `packages/ai/src/utils/openai-http.ts`
- cursor: `[_]`
- core_role: Shared OpenAI-compatible streaming HTTP helper.
- algorithmic_behavior: Defines `OpenAIHttpError` at line 32 and stream request helper interfaces at line 42; posts JSON request bodies with SSE `Accept`, uses retry defaults of 6 attempts, disables timeout at fetch layer, and extracts capped error details at line 135.
- inputs_outputs_state: Inputs are URL, headers/body, abort signal, retry config, and event parser. Outputs are stream handle/events or structured `OpenAIHttpError`. State is per-request retry/response state.
- gates_or_invariants: Error detail capped at 4096 chars; HTTP errors retain response/status/code; request must be JSON and SSE-compatible.
- dependencies_and_callers: Used by OpenAI-compatible providers including Azure, gateways, and local provider shims.
- edge_cases_or_failure_modes: Non-JSON error body, streaming disconnect, retry exhaustion, abort, large error payload, and provider-specific error shape.
- validation_or_tests: OpenAI provider tests exercise token/routing and HTTP error behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1881 `file` `packages/catalog/src/identity/id.ts`
- cursor: `[_]`
- core_role: Model ID normalization and segment extraction.
- algorithmic_behavior: Extracts model-like segments at line 16, chooses longest preferred segment at line 26, strips bracketed affixes including Chinese brackets at line 60, and returns stripped candidates/canonical affix-free IDs.
- inputs_outputs_state: Input is raw model ID string. Output is segment list, longest segment, or stripped candidate. State is pure.
- gates_or_invariants: Whitespace normalized; segment preference is longest then lexicographic; bracket stripping only occurs when affix markers exist.
- dependencies_and_callers: Used by catalog identity/classification and provider resolver logic.
- edge_cases_or_failure_modes: Bracketed marketing prefixes/suffixes, mixed punctuation, Chinese brackets, multiple model-like substrings, and empty strings.
- validation_or_tests: Catalog provider discovery/bundled catalog tests indirectly cover identity behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1911 `file` `packages/coding-agent/src/autoresearch/state.ts`
- cursor: `[_]`
- core_role: Autoresearch experiment state reconstruction and metrics helpers.
- algorithmic_behavior: Creates/clones experiment state, filters current results, finds baseline/best metrics, computes sorted median and confidence, builds state from session/run rows, reconstructs control state from session entries, and creates runtime stores.
- inputs_outputs_state: Inputs are session rows, run rows, session entries, metrics, and segment identifiers. Outputs are `ExperimentState`, reconstructed controls, confidence values, and runtime store snapshots. State includes session/runtime store maps.
- gates_or_invariants: Baseline/current segment filtering must be stable; metric calculations handle missing data; control entries must parse only valid data.
- dependencies_and_callers: Used by autoresearch workflows/controllers and session logs.
- edge_cases_or_failure_modes: Missing baseline, empty metric values, malformed control entries, stale segment numbers, and secondary metric mismatch.
- validation_or_tests: No assigned direct test; behavior validated by autoresearch workflow usage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1941 `file` `packages/coding-agent/src/cli/dry-balance-cli.ts`
- cursor: `[_]`
- core_role: Dry-balance account/model benchmarking CLI.
- algorithmic_behavior: Normalizes args, resolves auth/model targets, sends bounded benchmark requests, captures first-token and token throughput metrics, runs concurrent attempts via `mapConcurrent`, summarizes successes/failures, and formats table output.
- inputs_outputs_state: Inputs are command args, auth storage, model registry, runtime stream function, sample count, and concurrency. Outputs are benchmark summary text and per-account stats/failures. State includes progress sink counters and in-flight request results.
- gates_or_invariants: Positive integer normalization; default sample count/concurrency; model max token policy; errors are sanitized/truncated in display; concurrency bounded.
- dependencies_and_callers: CLI command path, AI auth/model registry, logger/TUI formatting utilities.
- edge_cases_or_failure_modes: Auth target missing, provider stream failure, no first token, timeout, all failures, and long account/error strings.
- validation_or_tests: Covered by CLI/runtime tests outside assigned set; function index shows export `formatDryBalanceText` at line 717 for testable formatting.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1971 `file` `packages/coding-agent/src/collab/host.ts`
- cursor: `[_]`
- core_role: Coding-agent collaboration host and wire-state publisher.
- algorithmic_behavior: `CollabHost` begins at line 109; debounces state/agent updates, filters wire-safe agent/session entry types, exposes transcript reads capped at 4 MiB, handles connect timeout, publishes bus channels, and derives display name.
- inputs_outputs_state: Inputs are interactive mode context, session events, transcript files, agent events, and client requests. Outputs are collab wire snapshots, transcript payloads, and bus notifications. State includes connection/session subscriptions and debounce timers.
- gates_or_invariants: Only whitelisted event/entry types are exposed; transcript reads are capped; state updates are debounced; connection timeout protects clients.
- dependencies_and_callers: Feeds `packages/collab-web` UI components and tool renderers.
- edge_cases_or_failure_modes: Oversized welcome image, stale transcript, reconnect race, missing session file, and event type drift.
- validation_or_tests: Collab fixture and web UI behavior validate expected shapes.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2001 `file` `packages/coding-agent/src/commands/update.ts`
- cursor: `[_]`
- core_role: CLI update command bridge.
- algorithmic_behavior: Initializes theme/context and calls the updater CLI with options such as `--force` and `--check`.
- inputs_outputs_state: Inputs are CLI flags and runtime context. Outputs are updater status/exit behavior. State is delegated to update implementation.
- gates_or_invariants: Must pass force/check flags correctly and initialize display theme before rendering update output.
- dependencies_and_callers: Called from coding-agent command registry; depends on update CLI helper.
- edge_cases_or_failure_modes: Updater unavailable, network/download failure, incompatible CLI distribution, and check-only mode accidentally mutating.
- validation_or_tests: CLI command tests may cover command wiring; no direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2031 `file` `packages/coding-agent/src/dap/index.ts`
- cursor: `[_]`
- core_role: DAP module export entrypoint.
- algorithmic_behavior: File is a tiny barrel/index surface for debug adapter protocol code.
- inputs_outputs_state: No local runtime state; exports determine module visibility.
- gates_or_invariants: Export path must remain stable.
- dependencies_and_callers: Imported by DAP consumers in coding-agent.
- edge_cases_or_failure_modes: Broken re-export after moving implementation.
- validation_or_tests: Type/build checks catch missing exports.
- skip_candidate: `yes: index/export surface only`

### OH_MY_HUMANIZE_MAIN-HZ-2061 `file` `packages/coding-agent/src/discovery/omp-plugins.ts`
- cursor: `[_]`
- core_role: OMP plugin discovery algorithm.
- algorithmic_behavior: Discovers installed/available plugins, resolves metadata, filters plugin candidates, and returns plugin descriptors for extensibility/marketplace flows.
- inputs_outputs_state: Inputs are plugin directories, package metadata, config, and environment. Outputs are discovered plugin records and diagnostics. State is filesystem-derived discovery cache/scan results.
- gates_or_invariants: Plugin descriptors must validate identity/shape; discovery should not execute untrusted plugin code just to list metadata.
- dependencies_and_callers: Used by plugin marketplace, custom commands/tools loader, and coding-agent extensibility setup.
- edge_cases_or_failure_modes: Invalid package metadata, duplicate plugin IDs, missing entrypoints, unreadable dirs, and incompatible plugin version.
- validation_or_tests: Marketplace CLI and custom tool loader tests cover adjacent plugin behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2091 `file` `packages/coding-agent/src/exec/non-interactive-env.ts`
- cursor: `[_]`
- core_role: Non-interactive process environment builder.
- algorithmic_behavior: Builds env overlays disabling pagers/prompts/color and setting CI/package-manager non-interactive flags; applies Windows UTF-8 env only when unset.
- inputs_outputs_state: Inputs are base env and platform. Outputs are normalized env map for subprocess execution. State is pure/per-call.
- gates_or_invariants: Should not overwrite explicit user env unnecessarily; must prevent pagers/prompts from hanging tool calls.
- dependencies_and_callers: Used by bash executor and workflow script runtime.
- edge_cases_or_failure_modes: User intentionally needs color/pager, Windows codepage behavior, package manager env conflicts, and inherited secret env preservation.
- validation_or_tests: Exec/workflow tests exercise command behavior with non-interactive settings.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2121 `file` `packages/coding-agent/src/internal-urls/issue-pr-protocol.ts`
- cursor: `[_]`
- core_role: Internal URL protocol parser/resolver for issues and pull requests.
- algorithmic_behavior: Parses internal issue/PR URL forms, normalizes repository/number references, and maps them to fetch/render operations for internal URL handling.
- inputs_outputs_state: Inputs are internal URLs, repository context, and selectors. Outputs are parsed protocol objects and resolved issue/PR fetch targets. State is per-parse.
- gates_or_invariants: Protocol parser must reject malformed or unsafe URLs and keep repo/number components explicit.
- dependencies_and_callers: Used by read/web/internal URL tools and GitHub issue/PR rendering.
- edge_cases_or_failure_modes: Ambiguous repo owner/name, missing number, invalid scheme, unsupported selector, and stale local repo context.
- validation_or_tests: Internal URL/read tests cover related behavior outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2151 `file` `packages/coding-agent/src/mcp/config-writer.ts`
- cursor: `[_]`
- core_role: MCP config file writer/validator.
- algorithmic_behavior: `withSchema` at line 14 adds schema metadata; `validateServerName` at line 63 enforces server-name rules; add/update/remove/list operations read JSON config with empty fallback, preserve `disabledServers`, write schema-bearing config, and invalidate filesystem cache.
- inputs_outputs_state: Inputs are config path, server name, server descriptor, and operation type. Outputs are updated config file contents or validation errors. State is JSON config on disk.
- gates_or_invariants: Server names allow safe alnum/`_`/`.`/`-` style names and max length around 100; duplicate add and update-missing are errors.
- dependencies_and_callers: Used by MCP command controller and config setup flows; documented by `docs/mcp-config.md`.
- edge_cases_or_failure_modes: Malformed JSON, duplicate server, invalid name, remove missing server, disabled server preservation, and schema path drift.
- validation_or_tests: MCP controller/config tests validate command-level behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2181 `file` `packages/coding-agent/src/modes/emoji-autocomplete.ts`
- cursor: `[_]`
- core_role: Emoji shortcode/emoticon autocomplete.
- algorithmic_behavior: Detects shortcode/emoticon prefixes at cursor, uses bucketed/binary-search style lookup over emoji data, builds up to 12 suggestions, and produces inline replacement edits.
- inputs_outputs_state: Inputs are editor text, cursor position, and emoji data. Outputs are autocomplete suggestions and replacement ranges/text. State is lookup tables.
- gates_or_invariants: Suggestions only appear at valid boundaries; replacement range must match detected token; max visible suggestions is capped.
- dependencies_and_callers: Used by coding-agent interactive input/autocomplete controller.
- edge_cases_or_failure_modes: Cursor mid-token, punctuation boundaries, duplicate aliases, multibyte emoji width, and no-match prefixes.
- validation_or_tests: Autocomplete setting tests cover suggestion visibility; emoji-specific behavior likely covered in component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2211 `file` `packages/coding-agent/src/session/agent-session.ts`
- cursor: `[_]`
- core_role: Central coding-agent session orchestrator.
- algorithmic_behavior: Coordinates session lifecycle, model requests, tool discovery/execution, MCP selection, prompt assembly, streaming event handling, message conversion, follow-up queues, compaction, retry/stop, model/thinking/service-tier cycling, tool output pruning, TTSR streaming guards, advisors, async jobs, and session persistence.
- inputs_outputs_state: Inputs are user messages, session options, model/provider streams, tool calls/results, MCP/tool registry state, settings, and abort/steer events. Outputs are transcript entries, UI events, model requests, tool executions, compactions, and session state updates. State is extensive: history, current turn, in-flight tools, model config, queues, advisors, jobs, and persistence handles.
- gates_or_invariants: Must preserve message/tool ordering, avoid duplicate tool results, sanitize/prune outputs, honor aborts and user steering, isolate per-session extensions, and keep compaction hooks consistent.
- dependencies_and_callers: Core of coding-agent CLI/SDK/ACP/collab; depends on `packages/ai`, `packages/agent`, MCP tooling, TUI event controllers, exec/search/read/edit tools, and settings.
- edge_cases_or_failure_modes: Streaming partial/tool interleaving, abort races, model switch leaks, tool result orphaning, compaction context loss, extension leakage, and stale async jobs.
- validation_or_tests: Covered by assigned message pipeline, compaction hooks, issue-816, SDK isolation, task/tool, and duplicate-tool-result tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2241 `file` `packages/coding-agent/src/session/yield-queue.ts`
- cursor: `[_]`
- core_role: Ordered async yield dispatcher for session events.
- algorithmic_behavior: Defines `YieldQueue` at line 32, with dispatcher/options interfaces, error formatting, queued payload dispatch, and likely drain/close behavior to serialize event emission.
- inputs_outputs_state: Inputs are payloads and dispatcher callbacks. Outputs are dispatched payload side effects and formatted errors. State is queue contents, running/closed flags, and error handling.
- gates_or_invariants: Dispatch should remain ordered; one failing payload should be reported without corrupting queue state.
- dependencies_and_callers: Used by AgentSession/session runtimes for event delivery.
- edge_cases_or_failure_modes: Dispatcher throw, enqueue while draining, close during dispatch, and backpressure.
- validation_or_tests: Agent session pipeline tests indirectly validate event ordering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2271 `file` `packages/coding-agent/src/task/parallel.ts`
- cursor: `[_]`
- core_role: Task parallelization helper.
- algorithmic_behavior: Manages concurrent task execution, likely batching or limiting worker functions and collecting results/errors for tool/task orchestration.
- inputs_outputs_state: Inputs are task descriptors/functions and concurrency/control options. Outputs are result arrays or aggregate errors. State is in-flight count and result collection.
- gates_or_invariants: Concurrency limit must be respected; result ordering/error propagation must match caller expectations.
- dependencies_and_callers: Used by coding-agent task tools/subagent spawning or parallel execution surfaces.
- edge_cases_or_failure_modes: Empty task list, early failure, abort propagation, and unhandled promise rejection.
- validation_or_tests: Assigned task spawn and task repair tests validate nearby task behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2301 `file` `packages/coding-agent/src/tools/conflict-detect.ts`
- cursor: `[_]`
- core_role: Git conflict marker scanner, URI parser, resolver, and formatter.
- algorithmic_behavior: `scanConflictLines` starts at line 56; `ConflictHistory` at line 190 stores discovered conflicts; `parseConflictUri` at line 281 parses `conflict://` references; `spliceConflict` at line 332 replaces recorded regions; formatting helpers render warnings/summaries at lines 581 and 655.
- inputs_outputs_state: Inputs are file lines/content, conflict URIs, replacement text, session history, and formatting options. Outputs are conflict blocks/entries, replaced content, rendered conflict regions, and warnings. State includes per-session conflict history.
- gates_or_invariants: Markers must form valid ours/base/theirs blocks; replacements must target the currently present region; URI scopes limited to ours/theirs/base.
- dependencies_and_callers: Used by edit/read tools and conflict-resolution workflows.
- edge_cases_or_failure_modes: Nested/partial conflict markers, CRLF, stale recorded region, missing base section, duplicate labels, and replacement newline normalization.
- validation_or_tests: Conflict behavior is likely covered by edit/apply-patch and tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2331 `file` `packages/coding-agent/src/tools/memory-edit.ts`
- cursor: `[_]`
- core_role: Memory edit tool implementation.
- algorithmic_behavior: Applies structured edits to remembered/user memory state, likely validating edit operations and persisting accepted changes through memory storage.
- inputs_outputs_state: Inputs are memory edit arguments and session/memory context. Outputs are changed memory records or tool result summaries. State is external memory store.
- gates_or_invariants: Edits must target existing memory entries or valid insertion paths; invalid operations should fail clearly.
- dependencies_and_callers: Used by coding-agent tools and mnemopi/memory integration.
- edge_cases_or_failure_modes: Missing memory backend, stale memory ID, malformed edit, concurrent memory update.
- validation_or_tests: Memory integration tests and mnemopi tests cover related persistence behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2361 `file` `packages/coding-agent/src/tts/runtime.ts`
- cursor: `[_]`
- core_role: Text-to-speech runtime constants/cache check.
- algorithmic_behavior: Defines Kokoro/runtime availability metadata and cache path/check helpers for TTS support.
- inputs_outputs_state: Inputs are runtime/cache location and environment. Outputs are availability booleans or runtime paths. State is filesystem cache presence.
- gates_or_invariants: TTS should only run when runtime assets are cached/available.
- dependencies_and_callers: Used by coding-agent TTS features.
- edge_cases_or_failure_modes: Missing model assets, corrupt cache, unsupported platform.
- validation_or_tests: TTS runtime likely validated by feature smoke tests outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2391 `file` `packages/coding-agent/src/utils/image-resize.ts`
- cursor: `[_]`
- core_role: Image resize/compression utility for provider payload constraints.
- algorithmic_behavior: Defines options at line 3, default max bytes around 500 KiB, WebP exclusion env check at line 40, candidate selection at line 48, resizing/compression pipeline, and `formatDimensionNote` at line 297.
- inputs_outputs_state: Inputs are image bytes, MIME type, max dimensions/bytes, and format options. Outputs are resized image bytes, MIME type, dimensions, and notes. State is per-call.
- gates_or_invariants: Preserve smallest acceptable candidate; respect max dimensions/bytes; skip WebP when excluded; surface notes when dimensions changed.
- dependencies_and_callers: Used by AI provider image payload preparation and coding-agent media handling.
- edge_cases_or_failure_modes: Unsupported format, image decode failure, impossible byte target, WebP excluded, animated image loss, and metadata removal.
- validation_or_tests: Anthropic many-image resize test validates provider-facing behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2421 `file` `packages/coding-agent/src/workflow/inspection.ts`
- cursor: `[_]`
- core_role: Workflow run/lifecycle inspection serializer.
- algorithmic_behavior: `buildWorkflowInspection` at line 162 compacts run snapshots into graph/activation/model summaries; `buildWorkflowLifecycleInspection` at line 214 compacts lifecycle families; helper functions compact attempts, activations, checkpoints, change requests, graph patch impact, and reason/edge strings.
- inputs_outputs_state: Inputs are `WorkflowRunSnapshot` and family snapshots. Outputs are compact inspection DTOs for UI/CLI/API. State is pure transformation.
- gates_or_invariants: Inspection must not expose huge raw transcript/output; graph revisions and pending patch proposals must be summarized consistently.
- dependencies_and_callers: Used by workflow monitor/display and eval/runtime tooling.
- edge_cases_or_failure_modes: Missing node/edge metadata, pending graph patch with partial preview, long reasons, and absent model assignments.
- validation_or_tests: Workflow eval/runtime and graph-view tests validate inspection-visible behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2451 `file` `packages/coding-agent/test/core/apply-patch-regression.test.ts`
- cursor: `[_]`
- core_role: Large regression suite for apply-patch parsing and patch application.
- algorithmic_behavior: Suites cover indentation adjustment, context-less hunk ambiguity, line hints, insertion fallbacks, seekSequence fallback, progressive context matching, unified diff numbers, Codex-style wrapped patches, file creation prefix stripping, EOF markers, nested anchors, long-line substrings, bench failures, trailing context, and context-only hunks.
- inputs_outputs_state: Inputs are patch text and original files. Outputs are transformed files or explicit errors. State is test temp files/patch parser state.
- gates_or_invariants: Patch application must be deterministic, reject ambiguity, preserve context-only lines, and not delete unrelated content.
- dependencies_and_callers: Exercises coding-agent apply-patch core used by edit tooling.
- edge_cases_or_failure_modes: Ambiguous anchors, wrapped patches, long lines, EOF markers, indentation, and context drift.
- validation_or_tests: The file is direct comprehensive validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2481 `file` `packages/coding-agent/test/debug/log-viewer.test.ts`
- cursor: `[_]`
- core_role: Debug log viewer model and copy payload validation.
- algorithmic_behavior: Suites `DebugLogViewerModel` at line 9 and `buildLogCopyPayload` at line 195 validate log loading/filtering/render data and copy payload formatting.
- inputs_outputs_state: Inputs are log lines/files and viewer operations. Outputs are model state, filtered rows, and copy text. State is test-local model state.
- gates_or_invariants: Viewer must handle log boundaries and copy only intended content.
- dependencies_and_callers: Exercises coding-agent debug log UI/model.
- edge_cases_or_failure_modes: Empty logs, long lines, level filters, invalid log entries, and copy range issues.
- validation_or_tests: Direct test file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2511 `file` `packages/coding-agent/test/eval/process-stdio-capture.test.ts`
- cursor: `[_]`
- core_role: JavaScript eval stdout/stderr capture validation.
- algorithmic_behavior: Suite `process.stdout/stderr capture in JS eval` starts at line 18 and verifies process stdio writes are captured during eval.
- inputs_outputs_state: Inputs are JS eval snippets writing to stdout/stderr. Outputs are captured output records/tool result content. State is test-local eval runtime.
- gates_or_invariants: Captured stdio should not leak to host console and should preserve stream ordering where expected.
- dependencies_and_callers: Exercises coding-agent eval tool runtime.
- edge_cases_or_failure_modes: Interleaved stdout/stderr, async writes, thrown errors after writes, and restoration of original process streams.
- validation_or_tests: Direct eval regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2541 `file` `packages/coding-agent/test/marketplace/cli.test.ts`
- cursor: `[_]`
- core_role: Marketplace CLI install-target classification validation.
- algorithmic_behavior: Suite `classifyInstallTarget` starts at line 8 and verifies parsing/classification of marketplace install target strings.
- inputs_outputs_state: Inputs are target strings. Outputs are classified plugin/source/marketplace target objects or errors. State is pure/test-local.
- gates_or_invariants: Ambiguous or invalid target strings must not be accepted silently.
- dependencies_and_callers: Exercises plugin marketplace CLI and types.
- edge_cases_or_failure_modes: Version suffixes, scoped names, URLs, local paths, invalid chars, and marketplace aliases.
- validation_or_tests: Direct classifier test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2571 `file` `packages/coding-agent/test/session-manager/migration.test.ts`
- cursor: `[_]`
- core_role: Session entry migration validation.
- algorithmic_behavior: Suite `migrateSessionEntries` starts at line 5 and verifies stored session entry migration behavior.
- inputs_outputs_state: Inputs are legacy session entries. Outputs are migrated current-shape entries. State is test-local data.
- gates_or_invariants: Migration must be idempotent and preserve semantic content.
- dependencies_and_callers: Exercises session manager storage migration.
- edge_cases_or_failure_modes: Unknown entry types, missing fields, version skew, and duplicate migration.
- validation_or_tests: Direct migration test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2601 `file` `packages/coding-agent/test/slash-commands/plan-history.test.ts`
- cursor: `[_]`
- core_role: Slash command history preservation validation.
- algorithmic_behavior: Suites `/plan history preservation when already active` at line 64 and `/goal history preservation when already active` at line 101 validate mode command behavior when already active.
- inputs_outputs_state: Inputs are slash command invocations and active mode/session history. Outputs are preserved or updated history entries. State is test-local session/mode state.
- gates_or_invariants: Re-entering active plan/goal mode must not erase relevant history.
- dependencies_and_callers: Exercises slash command handlers and interactive mode state.
- edge_cases_or_failure_modes: Duplicate activation, empty history, goal/plan cross-mode interaction, and stale active flag.
- validation_or_tests: Direct slash command test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2631 `file` `packages/coding-agent/test/task/task-spawn.test.ts`
- cursor: `[_]`
- core_role: Task spawn routing validation.
- algorithmic_behavior: Suite `task spawn routing` starts at line 85 and verifies how task spawn requests route to subagents/tools/sessions.
- inputs_outputs_state: Inputs are task spawn args, routing settings, and mock task/session dependencies. Outputs are spawned task descriptors/events. State is test-local task registry/session state.
- gates_or_invariants: Spawn routing must choose the correct target and preserve required args.
- dependencies_and_callers: Exercises coding-agent task tool and parallel task orchestration.
- edge_cases_or_failure_modes: Missing agent, invalid args, duplicate task ID, and wrong routing backend.
- validation_or_tests: Direct task routing test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2661 `file` `packages/coding-agent/test/tools/eval-agent-progress.test.ts`
- cursor: `[_]`
- core_role: Eval renderer progress placement validation.
- algorithmic_behavior: Suite `eval renderer: agent() progress below the cell box` starts at line 13 and verifies progress rendering location for agent calls inside eval output.
- inputs_outputs_state: Inputs are eval cell/tool progress events and render dimensions. Outputs are rendered UI snapshots/rows. State is test-local renderer state.
- gates_or_invariants: Progress must not overlap or appear inside the eval cell box incorrectly.
- dependencies_and_callers: Exercises coding-agent eval tool renderer and TUI layout.
- edge_cases_or_failure_modes: Long progress text, narrow width, nested agent calls, and final result replacement.
- validation_or_tests: Direct renderer test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2691 `file` `packages/coding-agent/test/tools/multi-search-path.test.ts`
- cursor: `[_]`
- core_role: Multi-search path handling validation.
- algorithmic_behavior: Tests search tool behavior across multiple paths and path argument variants.
- inputs_outputs_state: Inputs are search patterns and path arrays/strings. Outputs are grouped search results or errors. State is temp workspace/test files.
- gates_or_invariants: Multiple paths must be searched independently/consistently and invalid paths should be reported clearly.
- dependencies_and_callers: Exercises coding-agent search tool and native grep/glob path handling.
- edge_cases_or_failure_modes: Mixed files/directories, duplicate paths, missing paths, gitignore/hidden behavior, and path normalization.
- validation_or_tests: The file is direct search validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2721 `file` `packages/coding-agent/test/tools/task-repair-args.test.ts`
- cursor: `[_]`
- core_role: Task argument repair validation.
- algorithmic_behavior: Suites `repairDoubleEncodedJsonString` at line 5 and `repairTaskParams` at line 46 validate repairing double-encoded JSON/task parameter payloads.
- inputs_outputs_state: Inputs are malformed or double-encoded task args. Outputs are repaired parameter objects or unchanged values. State is pure/test-local.
- gates_or_invariants: Repair should handle common model encoding errors without accepting unsafe nonsense.
- dependencies_and_callers: Exercises task tool arg parsing/repair layer.
- edge_cases_or_failure_modes: Nested JSON strings, invalid JSON, partially encoded objects, and type mismatch.
- validation_or_tests: Direct repair tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2751 `file` `packages/coding-agent/test/workflow/eval-tool-runtime.test.ts`
- cursor: `[_]`
- core_role: Workflow eval tool runtime adapter validation.
- algorithmic_behavior: Suite `workflow eval tool runtime adapter` starts at line 30 and verifies eval tool behavior when invoked from workflow runtime.
- inputs_outputs_state: Inputs are workflow node/runtime eval requests and mock session/tool context. Outputs are eval results/artifacts/state patches. State is test-local workflow runtime.
- gates_or_invariants: Eval tool runtime must bridge workflow context without exposing unsupported host behavior.
- dependencies_and_callers: Exercises `packages/coding-agent/src/workflow/eval-tool-runtime.ts`.
- edge_cases_or_failure_modes: Missing runtime binding, eval error, stdout capture, artifact/state patch mismatch.
- validation_or_tests: Direct workflow test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2781 `file` `packages/collab-web/src/tool-render/index.ts`
- cursor: `[_]`
- core_role: Collab-web tool-render export entrypoint.
- algorithmic_behavior: Small barrel/index file exporting tool-render functionality to the collab UI.
- inputs_outputs_state: No local runtime state; exports only.
- gates_or_invariants: Public export path must remain stable.
- dependencies_and_callers: Imported by collab transcript/tool-card components.
- edge_cases_or_failure_modes: Broken export path after moving render modules.
- validation_or_tests: Build/type checks and UI render tests catch missing exports.
- skip_candidate: `yes: index/export surface only`

### OH_MY_HUMANIZE_MAIN-HZ-2811 `file` `packages/mnemopi/src/core/runtime-options.ts`
- cursor: `[_]`
- core_role: Mnemopi runtime option scoping.
- algorithmic_behavior: Uses `AsyncLocalStorage`-scoped runtime options for embeddings/LLM providers, provider function wrapping, debug flag access, and `isPiAiModel` detection.
- inputs_outputs_state: Inputs are runtime option objects, embedding/LLM provider callbacks, and model identifiers. Outputs are scoped provider behavior and option lookups. State is async-local runtime context.
- gates_or_invariants: Options should be scoped to the active async execution and not leak globally.
- dependencies_and_callers: Used by mnemopi core, coding-agent memory integration, and embedding variant config tests.
- edge_cases_or_failure_modes: Async context loss, nested overrides, provider function throwing, and model identification false positives.
- validation_or_tests: Assigned mnemopi embedding variant test validates config-facing behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2841 `file` `packages/swarm-extension/src/swarm/render.ts`
- cursor: `[_]`
- core_role: Swarm status renderer.
- algorithmic_behavior: Formats swarm status lines, per-agent statuses/durations/errors, and summary output for swarm extension UI.
- inputs_outputs_state: Inputs are swarm/agent progress records. Outputs are formatted text/render rows. State is pure formatting.
- gates_or_invariants: Must preserve status/error visibility while keeping lines readable.
- dependencies_and_callers: Used by swarm extension command/render pipeline.
- edge_cases_or_failure_modes: Missing duration, long agent names/errors, no agents, and mixed terminal statuses.
- validation_or_tests: Extension render tests likely cover formatting outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2871 `file` `python/robomp/src/proxy/server.py`
- cursor: `[_]`
- core_role: FastAPI GitHub/git proxy with HMAC protection.
- algorithmic_behavior: Exposes proxy endpoints for GitHub and git operations, authenticates requests with HMAC over path/query/body, caps body size, keeps PAT in process, checks push origin safety, runs git operations in threads with timeouts, and returns 409 on head drift.
- inputs_outputs_state: Inputs are HTTP requests, HMAC headers, repo/job args, GitHub token, and git refs. Outputs are HTTP JSON responses, git/GitHub side effects, and status/error codes. State includes server process config and temporary git operation state.
- gates_or_invariants: HMAC required; body cap enforced; PAT must not leave proxy; push must verify expected origin/head safety.
- dependencies_and_callers: Used by robomp CLI/orchestrator and automation workers.
- edge_cases_or_failure_modes: HMAC mismatch, replay/timestamp drift if implemented, large body, git timeout, push race/head drift, and token misconfiguration.
- validation_or_tests: Robomp tests validate adjacent native/proxy infrastructure.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2901 `file` `crates/pi-shell/src/minimizer/filters/cargo.rs`
- cursor: `[_]`
- core_role: Cargo-specific shell output minimizer filter.
- algorithmic_behavior: `supports` at line 8 gates supported subcommands; `filter` at line 27 dispatches build/test/fmt/nextest/install/clippy/general filters; successful tests are summarized; failures retain failure/error lines; clippy warnings are parsed/grouped by lint rule at lines 393 and 476.
- inputs_outputs_state: Inputs are cargo subcommand, command output text, and exit code. Outputs are condensed output. State is per-call parsed totals/warnings.
- gates_or_invariants: Nonzero/failure output must preserve useful diagnostics; success summaries should remove noise but keep totals/warnings.
- dependencies_and_callers: Used by `crates/pi-shell/src/minimizer.rs`, called from coding-agent bash executor.
- edge_cases_or_failure_modes: Generated warning rollups, nextest formats, clippy lint extraction, install summaries, ANSI noise, and mixed success/failure lines.
- validation_or_tests: Shell minimizer/cargo filter tests validate expected reductions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2931 `file` `packages/ai/src/registry/oauth/gitlab-duo.ts`
- cursor: `[_]`
- core_role: GitLab Duo OAuth registry flow.
- algorithmic_behavior: Implements OAuth PKCE login for GitLab Duo, supports env overrides for callback/client config, maps token response data into provider credentials, and refreshes tokens.
- inputs_outputs_state: Inputs are OAuth auth code/callback, verifier, env overrides, token responses, and refresh requests. Outputs are credential records and refreshed tokens. State is OAuth flow state and stored credentials.
- gates_or_invariants: PKCE verifier/state must match; token refresh must preserve account identity and expiry.
- dependencies_and_callers: Used by AI registry OAuth login and coding-agent auth setup.
- edge_cases_or_failure_modes: Callback mismatch, expired refresh token, missing env/client config, provider error response, and account identity absence.
- validation_or_tests: OAuth registry/auth-storage tests cover related account identity.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2961 `file` `packages/ai/src/utils/schema/wire.ts`
- cursor: `[_]`
- core_role: Tool schema normalization to provider wire JSON schema.
- algorithmic_behavior: Detects Zod/Ark schemas, converts Ark JSON AST to wire schema, post-processes JSON schema, rewrites nullable scalar `anyOf`, normalizes Ark comments, infers bare enum scalar types, closes declared objects, prunes Ark undefined union branches, and exposes `toolWireSchema` at line 627.
- inputs_outputs_state: Inputs are Zod, ArkType, JSON, or Tool schemas. Outputs are provider-compatible JSON schema records. State is transformed schema objects.
- gates_or_invariants: Empty/unconstrained schemas normalized carefully; integer bounds handled with safe integer constraints; object schemas can be closed to prevent extra props.
- dependencies_and_callers: Used by AI provider tool conversion and coding-agent custom tools.
- edge_cases_or_failure_modes: Undefined union branches, nullable scalar constraints, bare enums, comments in Ark keys, empty objects, recursive/complex schemas.
- validation_or_tests: Tool conversion and custom tool loader tests validate provider-facing schemas.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2991 `file` `packages/coding-agent/src/commit/analysis/index.ts`
- cursor: `[_]`
- core_role: Commit analysis export entrypoint.
- algorithmic_behavior: Tiny index/barrel file exposing commit analysis module surface.
- inputs_outputs_state: No local state; exports only.
- gates_or_invariants: Export path stability.
- dependencies_and_callers: Imported by commit-generation/analysis commands.
- edge_cases_or_failure_modes: Missing re-export after refactor.
- validation_or_tests: Type/build checks validate export presence.
- skip_candidate: `yes: index/export surface only`

### OH_MY_HUMANIZE_MAIN-HZ-3021 `file` `packages/coding-agent/src/eval/__tests__/completion-bridge.test.ts`
- cursor: `[_]`
- core_role: Eval completion bridge validation.
- algorithmic_behavior: Suites `runEvalCompletion` at line 176 and `completion() through eval runtimes` at line 347 validate completion helper behavior across eval runtime adapters.
- inputs_outputs_state: Inputs are eval completion calls, runtime mocks, prompts/options. Outputs are completion results/events/errors. State is test-local runtime/session state.
- gates_or_invariants: Completion bridge must pass supported options and surface runtime errors consistently.
- dependencies_and_callers: Exercises coding-agent eval completion bridge and workflow/eval runtimes.
- edge_cases_or_failure_modes: Missing runtime capability, streaming/non-streaming mismatch, option mapping, and provider errors.
- validation_or_tests: Direct bridge test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3051 `file` `packages/coding-agent/src/extensibility/custom-tools/loader.ts`
- cursor: `[_]`
- core_role: Custom tool discovery/loader.
- algorithmic_behavior: Loads user/plugin custom tool definitions, validates metadata/schema, binds runtime execution entrypoints, and produces tool descriptors for session/tool discovery.
- inputs_outputs_state: Inputs are custom tool files/plugin descriptors/config. Outputs are registered tool definitions and diagnostics. State includes loaded tool registry/cache.
- gates_or_invariants: Invalid tools should be rejected with clear diagnostics; loader must isolate plugin/tool definitions and preserve schema correctness.
- dependencies_and_callers: Used by extensibility system, plugin discovery, and AgentSession tool discovery.
- edge_cases_or_failure_modes: Duplicate names, invalid schema, missing entrypoint, module load failure, and unsafe side effects during load.
- validation_or_tests: Custom tools and marketplace tests cover related extensibility paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3081 `file` `packages/coding-agent/src/lsp/clients/lsp-linter-client.ts`
- cursor: `[_]`
- core_role: LSP linter client adapter.
- algorithmic_behavior: Connects to an LSP server/client and exposes lint/diagnostic operations for coding-agent.
- inputs_outputs_state: Inputs are file/document data, LSP client config, and lint requests. Outputs are diagnostics. State includes client connection/session.
- gates_or_invariants: Must handle server absence/failure and map diagnostics to expected coding-agent shape.
- dependencies_and_callers: Used by LSP integration and diagnostics UI/components.
- edge_cases_or_failure_modes: Server timeout, unsupported language, stale document version, and malformed diagnostics.
- validation_or_tests: LSP format and late diagnostics tests cover adjacent LSP behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3111 `file` `packages/coding-agent/src/modes/components/custom-editor.test.ts`
- cursor: `[_]`
- core_role: Custom editor component behavior validation.
- algorithmic_behavior: Suites `CustomEditor placeholder decoration` at line 56 and `CustomEditor space-hold push-to-talk` at line 68 validate editor decoration and push-to-talk interaction.
- inputs_outputs_state: Inputs are editor text/state and key/hold events. Outputs are rendered decorations and push-to-talk state changes. State is test-local editor component.
- gates_or_invariants: Placeholder decoration must not corrupt text; space-hold behavior must trigger only in intended contexts.
- dependencies_and_callers: Exercises coding-agent mode editor component.
- edge_cases_or_failure_modes: Empty editor, cursor movement, keyboard repeat, and conflicting shortcuts.
- validation_or_tests: Direct component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3141 `file` `packages/coding-agent/src/modes/components/read-tool-group.ts`
- cursor: `[_]`
- core_role: Read tool grouped renderer.
- algorithmic_behavior: Parses read args targets, resolves display targets/internal URLs, splits path selector specs, merges selector display parts, computes link paths/line anchors, ranks statuses, and implements `ReadToolGroupComponent` at line 288.
- inputs_outputs_state: Inputs are read tool call args/results/details, display width, and suffix resolution metadata. Outputs are TUI container rows, links, collapsed previews, and grouped status display. State is component render state.
- gates_or_invariants: Must sanitize/truncate previews, preserve internal URL/link line targets, and avoid ambiguous selector splitting.
- dependencies_and_callers: Used by coding-agent tool execution renderer.
- edge_cases_or_failure_modes: Commas inside line-range selectors, URL-like paths, suffix resolution mismatch, missing result details, and narrow terminal width.
- validation_or_tests: Read column truncation snapshot and late diagnostics/render tests cover related rendering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3171 `file` `packages/coding-agent/src/modes/controllers/mcp-command-controller.ts`
- cursor: `[_]`
- core_role: Interactive MCP command/login controller.
- algorithmic_behavior: Defines timeout helper at line 57, authorization link prompt component at line 67, connecting block at line 91, and `MCPCommandController` at line 158. It handles MCP connect/config/login flows, manual auth input provider, UI blocks, and server status feedback.
- inputs_outputs_state: Inputs are slash/command invocations, MCP server configs, OAuth/login callbacks, user pasted codes/URLs, and UI context. Outputs are UI blocks, config/auth updates, connection attempts, and status messages. State includes in-progress connection/auth operations.
- gates_or_invariants: Login prompts must time out/cleanup; headless manual input path must work; config writes must validate server names and transports.
- dependencies_and_callers: Uses MCP config writer, session MCP manager, auth/login providers, and interactive mode UI.
- edge_cases_or_failure_modes: Auth timeout, user cancels, invalid redirect URL/code, server connect failure, duplicate config, and stale connecting block.
- validation_or_tests: Assigned event-controller loader recovery and MCP conformance/config docs cover related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3201 `file` `packages/coding-agent/src/slash-commands/helpers/context-report.ts`
- cursor: `[_]`
- core_role: Context report helper for slash commands.
- algorithmic_behavior: Builds a report summarizing session/context state for command output, likely including token/message/tool/context usage.
- inputs_outputs_state: Inputs are session/context metadata. Outputs are formatted report text/rows. State is pure per-report.
- gates_or_invariants: Should omit sensitive/raw oversized data and keep formatting stable.
- dependencies_and_callers: Used by slash commands that inspect context.
- edge_cases_or_failure_modes: Missing context stats, very large values, and stale model metadata.
- validation_or_tests: Slash command tests cover nearby history behavior; no direct assigned report test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3231 `file` `packages/coding-agent/src/web/scrapers/choosealicense.ts`
- cursor: `[_]`
- core_role: Specialized scraper for choosealicense.com/license pages.
- algorithmic_behavior: Matches supported ChooseALicense host/path, fetches normalized license markdown/raw data, and returns readable scraper content or null on mismatch/failure.
- inputs_outputs_state: Inputs are URL and abort/signal context. Outputs are scraped markdown/document content or null. State is per-request.
- gates_or_invariants: Only supported host/path should be handled; failures should not break generic web flow.
- dependencies_and_callers: Used by coding-agent web scraper dispatcher.
- edge_cases_or_failure_modes: Unknown license slug, network failure, GitHub raw source changes, timeout, and malformed URL.
- validation_or_tests: Web scraper social/extended tests cover scraper framework; choosealicense likely has nearby tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3261 `file` `packages/coding-agent/src/web/scrapers/metacpan.ts`
- cursor: `[_]`
- core_role: Specialized scraper for MetaCPAN pages.
- algorithmic_behavior: Matches MetaCPAN host/path, calls appropriate API or page transforms, normalizes module/distribution documentation into readable text/markdown.
- inputs_outputs_state: Inputs are MetaCPAN URLs and fetch options. Outputs are scraped documentation content or null. State is per-request.
- gates_or_invariants: Host/path gate must prevent accidental handling of unrelated pages; API failures return controlled null/error behavior.
- dependencies_and_callers: Used by coding-agent web scraper dispatcher.
- edge_cases_or_failure_modes: Module name encoding, distribution/version paths, API rate/failure, missing docs, and timeout.
- validation_or_tests: Assigned web-scraper social extended tests validate scraper infrastructure.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3291 `file` `packages/coding-agent/src/web/scrapers/tldr.ts`
- cursor: `[_]`
- core_role: Specialized scraper for tldr command pages.
- algorithmic_behavior: Matches tldr platform URLs, resolves platform/page identifiers, fetches raw tldr content, and returns normalized command documentation.
- inputs_outputs_state: Inputs are tldr URLs and abort/signal. Outputs are markdown command examples or null. State is per-request.
- gates_or_invariants: Only valid tldr URL/platform/page forms should be fetched.
- dependencies_and_callers: Used by web scraper dispatcher and read/web tooling.
- edge_cases_or_failure_modes: Unknown platform, missing page, raw fetch failure, and malformed URL.
- validation_or_tests: Web scraper tests cover framework; tldr behavior likely included in scraper suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3321 `file` `packages/coding-agent/test/modes/components/late-diagnostics-message.test.ts`
- cursor: `[_]`
- core_role: Late diagnostics message component validation.
- algorithmic_behavior: Suite `LateDiagnosticsMessageComponent` starts at line 12 and verifies display of diagnostics that arrive after relevant UI events.
- inputs_outputs_state: Inputs are diagnostic messages and render context. Outputs are TUI rendered rows. State is test-local component state.
- gates_or_invariants: Late diagnostics should be visible without corrupting existing transcript/layout.
- dependencies_and_callers: Exercises coding-agent mode diagnostics UI and LSP/tool diagnostic paths.
- edge_cases_or_failure_modes: No diagnostics, multiple late messages, long diagnostic text, and narrow width.
- validation_or_tests: Direct component test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3351 `file` `packages/coding-agent/test/modes/controllers/event-controller-loader-recovery.test.ts`
- cursor: `[_]`
- core_role: Event controller loader recovery regression.
- algorithmic_behavior: Suite `EventController loader recovery after overflow maintenance` starts at line 109 and verifies loader recovery after transcript/event overflow maintenance.
- inputs_outputs_state: Inputs are event/controller state and overflow-maintenance scenarios. Outputs are recovered loader/controller behavior. State is test-local event controller/session state.
- gates_or_invariants: Overflow cleanup must not permanently break loader state or replay.
- dependencies_and_callers: Exercises interactive mode event controller and transcript rebuild paths.
- edge_cases_or_failure_modes: Missing preserved preview fields, overflow pruning, rebuild after maintenance, and stale loader cache.
- validation_or_tests: Direct regression test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3381 `file` `packages/coding-agent/test/tools/web-scrapers/social-extended.test.ts`
- cursor: `[_]`
- core_role: Extended web scraper validation.
- algorithmic_behavior: Tests social/extended web scraper matching and output normalization across supported scraper URLs.
- inputs_outputs_state: Inputs are URLs and mocked fetch responses. Outputs are normalized scraper results or null. State is test-local fetch fixtures.
- gates_or_invariants: Scrapers must only claim supported URLs and should return normalized text safely.
- dependencies_and_callers: Exercises web scraper modules including specialized scrapers.
- edge_cases_or_failure_modes: Host mismatch, malformed URL, API failure, empty response, and timeout.
- validation_or_tests: Direct scraper test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3411 `file` `packages/collab-web/src/tool-render/tools/edit.tsx`
- cursor: `[_]`
- core_role: Collab-web edit/apply-patch tool renderer.
- algorithmic_behavior: Extracts paths from hashline/apply_patch headers, computes operation counts and diff stats, renders per-file results/diagnostics, summary badges, and diff/body output.
- inputs_outputs_state: Inputs are edit tool call/result payloads, hashline/apply-patch text, diagnostics, and render context. Outputs are React UI elements for edit results. State is component-local render derivation.
- gates_or_invariants: Must avoid misreporting file paths/stats and keep diagnostics visible.
- dependencies_and_callers: Used by collab transcript `ToolCard` through tool-render registry.
- edge_cases_or_failure_modes: Wrapped patches, file creation/deletion, malformed headers, huge diffs, and missing result metadata.
- validation_or_tests: Collab fixture and apply-patch regression data validate expected shapes indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3441 `file` `packages/mnemopi/src/core/beam/schema.ts`
- cursor: `[_]`
- core_role: SQLite schema initializer/migrator for Beam memory.
- algorithmic_behavior: Creates working/episodic memory, scratchpad, FTS, facts/timelines/instructions, indexes, and triggers; uses additive migrations such as `addColumnIfMissing`; backfills `consolidated_at` and creates unconsolidated indexes after adding consolidation columns.
- inputs_outputs_state: Inputs are SQLite database connection and current schema state. Outputs are initialized/migrated tables, indexes, triggers, and backfilled rows. State is persistent SQLite schema/data.
- gates_or_invariants: Migrations must be idempotent/additive; FTS triggers and indexes must remain consistent with base tables.
- dependencies_and_callers: Used by mnemopi Beam store/recall/consolidation and tests importing dictionaries.
- edge_cases_or_failure_modes: Partial migration, missing columns, stale FTS triggers, incompatible old DB, and backfill performance on large DBs.
- validation_or_tests: Orphan vector cleanup and CLI stats tests exercise schema-backed behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3471 `file` `packages/stats/src/client/routes/index.ts`
- cursor: `[_]`
- core_role: Stats client route export entrypoint.
- algorithmic_behavior: Tiny index route module for stats client routing exports.
- inputs_outputs_state: No local algorithmic state; route exports only.
- gates_or_invariants: Export path must remain stable for stats client build.
- dependencies_and_callers: Used by stats dashboard client/router.
- edge_cases_or_failure_modes: Broken export after route refactor.
- validation_or_tests: Stats dashboard bundle test validates distributed asset presence.
- skip_candidate: `yes: index/export surface only`

### OH_MY_HUMANIZE_MAIN-HZ-3501 `directory` `packages/coding-agent/src/extensibility/custom-commands/bundled/ci-green`
- cursor: `[_]`
- core_role: Bundled custom command package for CI-green workflow guidance.
- algorithmic_behavior: Directory contains `index.ts`, registering or exporting a bundled custom command that likely drives a CI-green command prompt/workflow for making tests pass.
- inputs_outputs_state: Inputs are custom command invocation context and repo/session state. Outputs are command descriptor and command behavior/prompt. State is delegated to custom command runtime.
- gates_or_invariants: Bundled command must conform to custom command loader contract and not require external installation.
- dependencies_and_callers: Loaded by coding-agent extensibility custom commands system.
- edge_cases_or_failure_modes: Command descriptor drift, missing prompt metadata, and loader incompatibility.
- validation_or_tests: Custom command loader/marketplace tests cover adjacent extensibility behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3531 `file` `packages/coding-agent/src/extensibility/plugins/marketplace/types.ts`
- cursor: `[_]`
- core_role: Plugin marketplace type and ID utilities.
- algorithmic_behavior: Validates plugin name segments, builds/parses `name@marketplace` identifiers, and defines interfaces for catalog/source/registry/installed plugin records. Name regex allows lower alnum plus dot/hyphen with length limits around name 64 and ID 128.
- inputs_outputs_state: Inputs are plugin names, marketplace IDs, and catalog metadata. Outputs are parsed IDs, validation results, and typed records. State is pure.
- gates_or_invariants: Invalid names/IDs must be rejected before install/discovery.
- dependencies_and_callers: Used by plugin marketplace CLI, discovery, and install logic.
- edge_cases_or_failure_modes: Uppercase/invalid chars, too-long names, ambiguous `@`, duplicate marketplace IDs, and malformed catalog records.
- validation_or_tests: Marketplace CLI classifier test validates related target parsing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3561 `file` `packages/coding-agent/src/modes/setup-wizard/scenes/web-search.ts`
- cursor: `[_]`
- core_role: Setup wizard scene for web search provider selection.
- algorithmic_behavior: Builds a select list from settings schema options, checks provider availability, updates preferred provider setting, and refreshes host/setup state.
- inputs_outputs_state: Inputs are settings schema, provider availability/auth state, and user selection. Outputs are updated settings and wizard UI state. State is setup wizard scene state.
- gates_or_invariants: Only known providers should be selectable; unavailable providers need status feedback; setting updates must go through host/settings API.
- dependencies_and_callers: Uses web search provider definitions and coding-agent setup wizard framework.
- edge_cases_or_failure_modes: Provider removed from schema, auth missing, setting write failure, and stale availability.
- validation_or_tests: Setup wizard/provider tests likely cover scene behavior; web search provider directory is assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3591 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/index.ts`
- cursor: `[_]`
- core_role: Vendored Mermaid-to-ASCII renderer dispatch.
- algorithmic_behavior: Detects Mermaid diagram type, dispatches to xychart/sequence/class/ER/flowchart renderers, handles flowchart direction overrides, maps LR/RL to LR, flips BT canvases, and exports `renderMermaidAscii`.
- inputs_outputs_state: Inputs are Mermaid source text and render options/theme/color mode. Outputs are ASCII diagram text/canvas. State is per-render parser/canvas state.
- gates_or_invariants: Unsupported diagram types should fail gracefully; flowchart direction handling must preserve topology.
- dependencies_and_callers: Used by utils/markdown rendering surfaces that display Mermaid in terminal contexts.
- edge_cases_or_failure_modes: Invalid Mermaid syntax, unsupported type, direction mismatch, wide labels, and theme/color mode differences.
- validation_or_tests: Mermaid rendering tests outside assigned set likely validate; no assigned direct test.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `120 unique item evidence headings; item IDs are intentionally not repeated here so each assigned item_id appears exactly once in the output`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`

---

## Incremental Directory Refresh Addendum - oh-my-humanize/main bf4509d4f - OH_MY_HUMANIZE_MAIN-HZ-291

# agent_dir_06 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-291 `directory` `packages/coding-agent/src/workflow`
- cursor: `[_]`
- current_directory_core_role: `packages/coding-agent/src/workflow` owns the coding-agent workflow engine: package/artifact loading, freezing resource snapshots, definition/state validation, prompt resolution, runtime binding, graph scheduling, node execution adaptation, lifecycle event recording, checkpoint/restart state, graph/monitor projection, and script runtime environment setup. The central path is `runWorkflow()` in `runner.ts`, which starts a run-store record, materializes frozen resources, calls `runWorkflowScheduler()`, executes each node through `executeWorkflowNode()`, persists activation/run/lifecycle events, and decides whether the lifecycle attempt completes, fails, stops, or checkpoints.
- directory_level_delta_since_old_commit: The directory-level responsibility shifted from merely passing abort signals into node runtimes to actively enforcing stop/deadline progress at the runner boundary. Current `runner.ts` builds a combined workflow runtime signal when `maxRuntimeMs` is configured, propagates that signal to both scheduler stop logic and node execution, and wraps node runtime promises with `awaitWorkflowNodeExecution()` so an aborting node signal can settle the activation even when the runtime implementation ignores the abort. This lets lifecycle checkpoint creation proceed instead of waiting forever on a still-pending node promise. Adjacent headless CLI changes make `omp workflow start --cwd` authoritative for JavaScript eval script execution by temporarily `process.chdir(cwd)` around `AsyncFunction` execution and restoring the old cwd/`console.log` in `finally`; shell and agent headless runners already pass `cwd` to spawned processes.
- affected_descendant_algorithms: `runWorkflow()` now composes deadline and external abort signals before invoking the scheduler, cleans the timeout in `finally`, and still removes materialized frozen resources after execution. `workflowRuntimeSignal()` adds max-runtime timeout handling via `workflowMaxRuntimeStopReason(maxRuntimeMs)`, combining timeout with `options.signal`, `options.nodeAbortSignal`, and per-activation `nodeAbortSignalForActivation()`. `executeAndPersistActivation()` now selects `context.nodeAbortSignal ?? context.signal` as the execution signal, passes it to `executeWorkflowNode()`, and awaits through `awaitWorkflowNodeExecution()`; on abort it records run-store and lifecycle activation status as `aborted` rather than `failed`. `finishLifecycleAttempt()` now derives checkpoint reasons from activation limits or aborted scheduler signals, requests an attempt stop only if the lifecycle attempt is still running, and writes a checkpoint containing completed activation ids, aborted activation ids, current frontier, state, and source mapping. Scheduler interaction remains: scheduler marks aborted execution results as activation `aborted`, stops scheduling, and includes the aborted node id/frontier for restart.
- current_inputs_outputs_state: Inputs to the workflow runner are `WorkflowRunnerOptions`: host, parsed definition, run id, start node(s), runtime host, activation limits, initial/completed state for restarts, package root/frozen resources, model resolution options, lifecycle metadata, scheduler signal, node abort signal(s), and optional `maxRuntimeMs`. Runtime inputs to nodes include resolved prompts, frozen or loaded script code, materialized resource root, structured workflow context snapshots, model overrides, and the selected abort signal. Outputs are a `WorkflowRunnerResult` containing the run snapshot and scheduler result; side effects are append-only run-store events, append-only lifecycle events, activation records, state patches, attempt terminal/stop records, and checkpoint snapshots. Headless CLI JSON output reconstructs runs/families from those events and reports status, frontier, state keys, lifecycle attempts, and checkpoints.
- new_or_changed_gates_or_invariants: A stopped/checkpointed lifecycle attempt must not retain running activations; lifecycle `createWorkflowCheckpoint()` rejects checkpoints unless the attempt is stopped/stop-requested/failed and all referenced completed/aborted activations have matching terminal statuses. The runner now enforces this invariant by converting node-signal aborts, including ignored runtime aborts and max-runtime aborts, into aborted activation records before checkpointing. Stop/checkpoint classification is reason-driven: activation limit yields `"activation limit reached"`, aborted signals use the signal reason, and max runtime uses `"workflow max runtime elapsed after <ms>ms"`. If a scheduler signal aborts after a node completes, the runner records completed work and checkpoints downstream frontier nodes rather than scheduling them. If the node abort signal aborts during a node, that node is placed back on the checkpoint frontier and its activation id is listed in `abortedActivationIds`. Headless JavaScript script execution now treats the requested `--cwd` as the relative path root and restores cwd/console state after execution.
- dependencies_and_callers: Primary callers are `packages/coding-agent/src/cli/workflow-cli.ts` for headless `omp workflow start`, `packages/coding-agent/src/slash-commands/helpers/workflow.ts` for interactive/background slash workflows, ACP workflow integration, and workflow tests. `runner.ts` depends on `scheduler.ts` for graph execution and frontier calculation, `node-runtime.ts` for typed node dispatch, `session-runtime.ts` for converting node requests into eval/shell/agent/human runtime requests, `prompt-source.ts` for prompt materialization, `model-resolution.ts` for model audit/override selection, `run-store.ts` for run event persistence, `lifecycle.ts` for family/attempt/checkpoint events, `freeze.ts` resource snapshots, and `runtime-timeout.ts` for default timeout reason text. The headless CLI runtime adapter calls `createSessionWorkflowRuntimeHost()` with cwd-bound eval, shell, and agent task runners.
- edge_cases_or_failure_modes: The new abort wrapper intentionally rejects after an abort even if a runtime promise never resolves, preventing `/workflow stop` or max-runtime timeout from hanging forever. It delays rejection with a zero-delay timer, so a runtime that settles immediately during abort handling can still win and return its own result/error before forced abort rejection. If no frontier exists, `workflowCheckpointReason()` does not checkpoint a purely terminal aborted signal. `maxRuntimeMs` is active whenever defined; callers use the five-day default for CLI/slash workflow starts, while an explicit `0` would behave as an immediate timeout rather than “disabled”. Headless JS cwd handling uses process-global `process.chdir()` and process-global `console.log` capture; the current CLI passes one cwd for the whole run and restores both in `finally`, but concurrent in-process headless JS workflow starts with different cwd values would still be a global-state hazard. Frozen script file resolution remains package-root constrained and fails if a frozen resource-backed script file was not captured in the freeze.
- validation_or_tests: Static research only; no test execution was performed in this read-only pass. New or relevant pinning tests include `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts`, which verifies headless JS workflow scripts read relative to the requested `cwd` and that SIGINT produces stopped status plus a checkpoint frontier instead of leaving a live run. `packages/coding-agent/test/workflow/runner.test.ts` verifies separate scheduler and node abort signals, checkpointing deadline-aborted activations as `aborted` rather than failing attempts, checkpointing even when the node runtime ignores abort, and lifecycle checkpointing when `maxRuntimeMs` elapses. Existing lifecycle tests in `packages/coding-agent/test/workflow/lifecycle-store.test.ts` pin the lower-level invariant that checkpoints cannot be created while activations are still running. The changelog entries under `packages/coding-agent/CHANGELOG.md` explicitly document the fixed ignored-abort stop/checkpoint behavior and headless JS `--cwd` behavior.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-291`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
