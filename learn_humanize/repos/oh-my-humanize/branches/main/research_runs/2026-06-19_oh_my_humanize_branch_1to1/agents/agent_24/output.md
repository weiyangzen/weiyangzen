# agent_24 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-024 `directory` `docs/tools`
- cursor: `[_]`
- core_role: Tool-contract documentation directory for coding-agent built-in tools. Recursively inspected all markdown specs under `docs/tools`, including `bash.md`, `browser.md`, `task.md`, `ast-grep.md`, `ast-edit.md`, `ask.md`, `checkpoint.md`, `debug.md`, `edit.md`, `eval.md`, `find.md`, `github.md`, `job.md`, `lsp.md`, `read.md`, `recall.md`, `retain.md`, `resolve.md`, `rewind.md`, `search.md`, `ssh.md`, `todo.md`, `web_search.md`, and `write.md`.
- algorithmic_behavior: The directory defines per-tool schemas, execution flow, mode variants, side effects, error mapping, timeout/cap behavior, and integration points. `docs/tools/bash.md:56` describes command normalization, interceptor approval, cwd validation, PTY/client-terminal/async routing, output artifact spilling, and timeout handling. `docs/tools/browser.md:87` describes browser-kind resolution, tab reuse, worker execution, cmux fallback, run timeout, screenshot/output artifact handling, and teardown. `docs/tools/ast-edit.md:116` documents preview-first AST rewrite behavior and reverse-order application after overlap checks.
- inputs_outputs_state: Inputs are tool arguments documented per file; outputs are model-facing `content` plus structured `details` or thrown tool errors. State includes session cwd, async job registry, browser tab registry, checkpoint state, memory backend, GitHub cache, MCP resources, LSP session, and UI state depending on tool.
- gates_or_invariants: Docs repeatedly encode gates such as UI-only availability for `ask`, top-level-only `checkpoint`, strict path/cwd resolution, timeout clamps, output preview limits, approval/interceptor checks, cancellation propagation, artifact caps, and no hidden raw filesystem leakage in rendered output.
- dependencies_and_callers: These docs point to corresponding implementations in `packages/coding-agent/src/tools/**`, config schemas, session managers, native functions, render utilities, and browser/eval workers. They are likely consumed by humans and by tool-authoring audits rather than imported at runtime.
- edge_cases_or_failure_modes: Headless UI tool use, timeout versus user cancellation, tool result truncation, parser errors, AST overlap, missing cwd, browser worker hang, PTY kill, stale caches, and artifact spilling are explicitly covered.
- validation_or_tests: Validation is indirect through linked tool tests under `packages/coding-agent/test/**`; directory itself is documentation. No tests were run in this read-only research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-054 `file` `docs/mcp-server-tool-authoring.md`
- cursor: `[_]`
- core_role: Architecture document for MCP server discovery, normalization, auth, tool bridging, and lifecycle.
- algorithmic_behavior: Defines config validation at `docs/mcp-server-tool-authoring.md:18`, discovery/precedence at `:46`, environment expansion at `:80`, auth/runtime value resolution at `:88`, MCP-to-agent tool bridge at `:117`, schema mapping at `:138`, execution mapping at `:142`, and operator lifecycle at `:154`.
- inputs_outputs_state: Inputs are `.mcp.json`-style config, transport definitions, env/header substitutions, OAuth credentials, server tool schemas, and runtime tool calls. Outputs are normalized server definitions, agent-callable tool definitions, runtime results, and user-visible diagnostics.
- gates_or_invariants: Valid transports, precedence rules, collision-safe naming, environment expansion boundaries, OAuth injection only where configured, and meaningful error surfaces are required.
- dependencies_and_callers: References MCP manager, config discovery, OAuth storage, custom tool bridge, and slash/operator commands. It coordinates with `packages/coding-agent/src/mcp/**`, discovery helpers, and internal URL/resource access.
- edge_cases_or_failure_modes: Transport misconfiguration, name collisions, stale auth values, unsupported schemas, bad header/env interpolation, and live update inconsistencies.
- validation_or_tests: Covered by MCP/tool-discovery tests elsewhere; this file is architectural evidence, not executable validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-084 `file` `scripts/ci-build-native.ts`
- cursor: `[_]`
- core_role: CI workflow script for building native package variants.
- algorithmic_behavior: `parseTargetVariants()` at `scripts/ci-build-native.ts:24` parses `PI_NATIVE_TARGET_VARIANTS` into `{target, variant}` records, splitting `target:variant` pairs with a default variant. `runNativeBuild()` at `:37` shells into `packages/natives` with variant env and runs `build:native`. `main()` at `:49` loops variants and labels build output.
- inputs_outputs_state: Input is environment variable `PI_NATIVE_TARGET_VARIANTS`; output is build command execution and native artifacts produced by package scripts. State is process env per variant.
- gates_or_invariants: Empty env defaults to `current`; each whitespace token becomes one build; target and variant are propagated as `PI_NATIVE_TARGET` and `PI_NATIVE_VARIANT`.
- dependencies_and_callers: Depends on Bun shell and `packages/natives` build scripts. Called by CI jobs.
- edge_cases_or_failure_modes: Malformed tokens still split permissively; downstream build script owns validation. Command failure aborts the script because Bun shell is not `.nothrow()`.
- validation_or_tests: No direct test found; CI execution is the practical validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-114 `file` `scripts/sync-versions.ts`
- cursor: `[_]`
- core_role: Version synchronization guard across monorepo packages.
- algorithmic_behavior: Reads root/package metadata, discovers workspace package directories, compares versions, and exits nonzero on mismatch. Anchors: package interfaces at `scripts/sync-versions.ts:11`, `PackageInfo` at `:18`, failure exit at `:57`.
- inputs_outputs_state: Inputs are package JSON files under the repo; outputs are synchronized writes or failure messages depending on script behavior around discovered package versions. State is filesystem package metadata.
- gates_or_invariants: Package versions should match root/package policy; missing or invalid package metadata should fail early rather than silently diverge.
- dependencies_and_callers: Uses `node:fs` and `node:path`; likely called by release or CI workflows.
- edge_cases_or_failure_modes: Missing package.json, malformed JSON, inconsistent versions, and package directories that do not meet expected shape.
- validation_or_tests: No direct test inspected; release/CI scripts exercise it.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-144 `directory` `packages/natives/native`
- cursor: `[_]`
- core_role: JavaScript/TypeScript loader surface for the native addon package.
- algorithmic_behavior: `index.js` loads native bindings once via `loadNative()` at `packages/natives/native/index.js:16` and re-exports generated symbols from `:19` through `:70`; enum constants start at `:72`. `loader-state.js` owns platform detection, candidate resolution, staging, embedded archive extraction, stale cache cleanup, AVX2/baseline variant selection, version sentinel validation, and aggregated load errors. Key helpers include `detectCompiledBinary()` at `loader-state.js:80`, `getAddonFilenames()` at `:95`, `shouldStageNodeModulesAddon()` at `:126`, `resolveLoaderCandidates()` at `:148`, `cleanupStaleNativeVersions()` at `:189`, and `extractEmbeddedAddonArchive()` at `:350`.
- inputs_outputs_state: Inputs are `process.platform`, `process.arch`, env vars such as `PI_NATIVE_VARIANT` and `XDG_DATA_HOME`, package version, embedded archive metadata, node_modules leaf packages, and cache directories. Output is a validated native binding object exported to JS consumers.
- gates_or_invariants: Supported platform tags are limited to Linux/macOS/Windows x64/arm64 at `loader-state.js:34`; archive extraction rejects unsafe paths and unsupported tar entry types at `:380` and `:383`; version sentinel verifies JS/native match via declarations around `index.d.ts:141`.
- dependencies_and_callers: Used by `@oh-my-pi/pi-natives` imports across coding-agent, tui, shell, and markit paths. Generated export block is maintained by `packages/natives/scripts/gen-enums.ts`.
- edge_cases_or_failure_modes: Missing leaf package, stale global native binary, Windows file locks requiring staging, compiled binary embedded payload, AVX2 detection failures, corrupt archive, unsafe archive filenames, and version mismatch.
- validation_or_tests: Loader pure helpers are testable via `loader-state.d.ts`; native declarations in `index.d.ts` define runtime contract for shell, grep, AST, image, token, and terminal functions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-174 `file` `docs/toolconv/gemma.md`
- cursor: `[_]`
- core_role: Tool-calling dialect specification for Gemma token-delimited calls.
- algorithmic_behavior: Defines special tokens at `docs/toolconv/gemma.md:7`, role/turn structure at `:25`, tool definition format at `:29`, call syntax at `:41`, parallel call behavior at `:66`, result encoding at `:70`, and parser gotchas at `:91`.
- inputs_outputs_state: Inputs are model text containing `call:NAME{...}`-style invocations and token delimiters; outputs are parsed tool-call names and JSON-ish arguments, plus serialized tool results.
- gates_or_invariants: Parser must handle string delimiters, bare scalars, booleans/null/numbers, multiple calls, and result turn placement without confusing prose for tool syntax.
- dependencies_and_callers: Coordinates with `packages/ai/src/dialect/factory.ts` and Gemma dialect scanner implementation.
- edge_cases_or_failure_modes: Bare enum-like strings, malformed delimiters, multiple calls, and scalar coercion ambiguity.
- validation_or_tests: Dialect parsing tests likely live under AI dialect tests, not assigned here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-204 `file` `docs/tools/task.md`
- cursor: `[_]`
- core_role: Contract documentation for the `task` tool and subagent spawning.
- algorithmic_behavior: Documents source files at `docs/tools/task.md:5`, input schema at `:27`, output result semantics at `:49`, execution flow at `:75`, modes at `:100`, side effects at `:111`, caps at `:132`, and error cases at `:143`.
- inputs_outputs_state: Inputs support flat and batch task shapes with agent, prompt, role, and task metadata. Outputs include subagent result content/details and task roster state. State includes spawned agent sessions, role labels, concurrency/batch accounting, and registry display.
- gates_or_invariants: `agent` is required; `role` is bounded and normalized for display; batch/task caps and agent availability constrain execution.
- dependencies_and_callers: Maps to `packages/coding-agent/src/task/**`, multi-agent tool registry, and task result rendering.
- edge_cases_or_failure_modes: Missing agent, invalid batch shape, role over length, unavailable subagent type, task failure, cancellation, and parallel subagent result aggregation.
- validation_or_tests: Task behavior is exercised by SDK/tool activation and task-related tests outside this specific doc.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-234 `directory` `packages/ai/src/providers`
- cursor: `[_]`
- core_role: Provider transport layer for AI APIs. Recursively inspected provider files including OpenAI Responses/Chat/Completions/Codex, Anthropic client/messages/shim, Bedrock, Google/Gemini/Vertex, Ollama, Cursor, GitLab Duo, Kimi, synthetic, schema files, auth headers, transform logic, AWS eventstream/SigV4, and provider tests.
- algorithmic_behavior: Each provider maps internal `Context`, `Model`, `Tool`, and message structures to a provider-specific HTTP/SSE/eventstream wire protocol, then decodes streams back into assistant events. Examples: Bedrock `streamBedrock` at `amazon-bedrock.ts:178` builds Converse Stream requests, disables thinking when forced tool choice conflicts at `:219`, signs/fetches, and decodes eventstream from `:325`. Anthropic client retries and timeout behavior is implemented in `anthropic-client.ts:207` and fetch loop at `:252`. `transformMessages()` at `transform-messages.ts:155` normalizes replay, thinking signatures, tool IDs, duplicate/orphan tool results, and cross-provider compatibility. `register-builtins.ts:303` defines lazy stream wrappers with first-event/idle watchdogs.
- inputs_outputs_state: Inputs are internal model/context/options, auth tokens, tools, system/developer messages, provider session state, and abort signals. Outputs are async assistant events, provider errors, rate-limit metadata, usage, and transformed replay payloads. State includes lazy module promises, session replay state, abort trackers, provider-specific options, and headers.
- gates_or_invariants: Schema validation for Anthropic/OpenAI server gateways, no orphan tool outputs, provider-compatible thinking/reasoning fields, timeout watchdogs, retryable status logic, auth header formation, image/vision guards, cache-control retention, and API-specific tool-choice constraints.
- dependencies_and_callers: Called by `packages/ai` stream APIs and coding-agent sessions. Depends on catalog model-thinking helpers, provider descriptors, `pi-utils` fetch/retry/logger helpers, OAuth/auth storage, and event stream utilities.
- edge_cases_or_failure_modes: Stalled first token, provider 400 due to replay grammar, invalid thinking signatures, duplicate tool call IDs, unsupported image input, proxy auth errors, Bedrock eventstream exceptions, Anthropic unknown content blocks, and unsupported model effort.
- validation_or_tests: Assigned tests cover Anthropic prefill, Fire Pass routing, Bedrock thinking display, OpenAI Responses replay, schema dereferencing, broker sentinel refresh, ZenMux login, xAI OAuth, and provider-specific tests under `providers/__tests__`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-264 `directory` `packages/coding-agent/src/goals`
- cursor: `[_]`
- core_role: Goal-mode runtime, state model, guided setup, and goal tool integration.
- algorithmic_behavior: `runtime.ts` manages goal lifecycle, prompt rendering, token/time accounting, pause/resume/drop/complete transitions, and budget steering. Key functions: `remainingTokens()` at `runtime.ts:56`, `goalTokenDelta()` at `:65`, `renderGoalPrompt()` at `:79`, and `GoalRuntime` at `:117`. `guided-setup.ts` runs an LLM-guided interview with schema/tool extraction through `runGuidedGoalTurn()` at `:64`. `tools/goal-tool.ts` exposes operations `create|get|complete|resume|drop` through ArkType schema at `:17` and executes against session runtime at `:78`.
- inputs_outputs_state: Inputs are user objectives, optional token budgets, usage deltas, session model, guided answers, and tool params. Outputs are goal prompts, runtime events, persisted goal/paused state, and tool responses with goal details.
- gates_or_invariants: Token budgets must be positive integers at `runtime.ts:107`; accounting applies only to active or budget-limited states; goal tool requires available runtime; guided setup requires a plan/slow/current model.
- dependencies_and_callers: Used by slash commands, interactive submission, session runtime, and tool registry. Prompts are static markdown imports, rendered via `prompt.render`.
- edge_cases_or_failure_modes: Budget exceeded transitions, interruption pause, prompt re-anchoring cache-write exclusion, missing model for guided setup, invalid guided JSON, and empty/missing objective.
- validation_or_tests: Goal behavior likely covered by goal runtime/tool tests outside assigned list; no direct test in this directory was assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-294 `directory` `packages/coding-agent/test/collab`
- cursor: `[_]`
- core_role: Contract tests for collaboration crypto, read-only permissions, session replication, and mid-turn steering.
- algorithmic_behavior: `crypto.test.ts` verifies seal/open, tamper rejection, link parsing/rendering, write-token handling, and wire envelopes. `read-only.test.ts` builds an in-memory relay/websocket harness at lines `35-205` and verifies view-link guests are read-only at `:270`. `session-replication.test.ts` checks replicated entries preserve inline image data for hooks while persisted rows externalize blobs at `:25`. `steer-queue.test.ts` starts a single-room relay at `:28` and verifies guest steer prompts become queued host messages at `:177`.
- inputs_outputs_state: Inputs are collab frames, room links, keys, guest names, write tokens, session entries, and prompts. Outputs are encrypted/decrypted frames, welcome state, prompt replies, replicated entries, and queued-message state.
- gates_or_invariants: Read-only guests cannot mutate; forged write tokens stay read-only; hook failures must not break persistence; foreign replicated ids are preserved; queued steer count reaches guest state.
- dependencies_and_callers: Exercises `collab/crypto`, `collab/host`, `collab/protocol`, `collab/relay-client`, and `SessionManager`.
- edge_cases_or_failure_modes: Tampered ciphertext, malformed legacy links, Foundation-reencoded deep links, forged tokens, nondeterministic broadcast frames, hook exceptions, and blob externalization boundaries.
- validation_or_tests: This directory is itself validation; no tests were executed during research.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-324 `directory` `packages/mnemopi/src/core`
- cursor: `[_]`
- core_role: Memory system core: storage, recall, extraction, embeddings, graph/triples, annotations, consolidation, query intent, temporal parsing, and beam memory.
- algorithmic_behavior: The directory coordinates memory ingestion, vector/binary embeddings, episodic graph, fact extraction, veracity consolidation, polyphonic recall, and migrations. `beam/schema.ts:24` initializes tables/indexes; `beam/store.ts:343` implements `remember()` with dedupe, trim, annotations, embeddings, and optional fact extraction; `binary-vectors.ts:120` binarizes embeddings and `:223` searches by Hamming-derived score; `embeddings.ts:253` handles API embedding requests and `:337` availability; `extraction/client.ts:52` wraps LLM fact extraction; `annotations.ts:226` implements annotation store; `migrations/e6-triplestore-split.ts:70` detects pending migration and `:145` migrates annotation-like triples.
- inputs_outputs_state: Inputs include memory content, metadata, session/channel/global scope, embeddings/runtime options, extraction API messages, queries, temporal options, and SQLite paths. Outputs are memory IDs, recall results with scores/voices, fact rows, annotations, embeddings, cost logs, diagnostics, and migrated tables.
- gates_or_invariants: SQL identifiers are validated; embeddings are scoped by active provider/model; stale embeddings are wiped/rebuilt; content sanitizer extracts oversized/high-entropy blobs; query time must be valid date/string/null; facts/annotations use confidence defaults and duplicate guards.
- dependencies_and_callers: Used by coding-agent memory tools/backends and tests. Depends on `bun:sqlite`, `pi-ai` auth/fetch, `pi-utils` logging, fastembed, vector math, and runtime option scopes.
- edge_cases_or_failure_modes: Missing embedding key, provider failure, interrupted embedding rebuild, concurrent fact consolidation, high-entropy content, noisy entity extraction, stale schema columns, circular or duplicate facts, and visibility filtering across session/global scopes.
- validation_or_tests: Assigned tests include `consolidate-fact-concurrency.test.ts`, `polyphonic-recall.test.ts`, and direct file `synonyms.ts`/`extraction/client.ts` coverage references.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-354 `file` `crates/pi-natives/src/crash_handler.rs`
- cursor: `[_]`
- core_role: Rust native crash diagnostics for panics and allocation failures.
- algorithmic_behavior: `install()` at `crates/pi-natives/src/crash_handler.rs:53` installs panic and allocation hooks once. It formats reports with `format_panic_report()` at `:93`, `format_alloc_report()` at `:106`, builds headers at `:120`, extracts payloads at `:149`, persists at `:159`, and resolves log paths at `:178`/`:187`.
- inputs_outputs_state: Inputs are panic hook info, allocation `Layout`, env vars for config/state dirs, home dir, pid, and current time. Outputs are native crash log files under resolved logs dir.
- gates_or_invariants: Hook install is guarded by `Once`; allocation hook active flag prevents recursion; log path resolution handles XDG/state/config conventions and platform fallback.
- dependencies_and_callers: Native crate startup calls this to improve post-abort diagnostics. Uses std panic/allocation hooks and filesystem env resolution.
- edge_cases_or_failure_modes: Non-string panic payloads, missing home dir, unwritable logs dir, allocation failure while formatting/persisting, and platform-specific XDG behavior.
- validation_or_tests: Unit tests begin at `:307` and cover report formatting, payload handling, path resolution, XDG env, and log filename construction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-384 `file` `crates/pi-shell/src/windows.rs`
- cursor: `[_]`
- core_role: Windows shell PATH normalization and Git/MSYS path support.
- algorithmic_behavior: `configure_windows_path()` at `crates/pi-shell/src/windows.rs:12` reads/modifies shell PATH. Helpers normalize paths at `:76`, discover Git installs via registry/where/path at `:97`, `:119`, `:135`, derive install root at `:152`, generate Git paths at `:177`, and translate MSYS path segments at `:233`.
- inputs_outputs_state: Inputs are Brush shell variables, Windows registry, `where git` output, PATH segments, and Git install roots. Output is updated shell PATH variable.
- gates_or_invariants: Paths are normalized consistently; Git command paths are only added when install roots are plausible; MSYS drive-like segments are detected by `is_drive_letter()` and `is_windows_style_path()`.
- dependencies_and_callers: Used by `pi-shell` shell initialization on Windows. Depends on `brush_core`, `winreg`, and command lookup.
- edge_cases_or_failure_modes: Missing registry keys, `where` unavailable, malformed MSYS paths, duplicate PATH entries, non-Windows-style segments.
- validation_or_tests: Tests at `:284` cover path normalization and MSYS/path detection behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-414 `file` `packages/agent/test/supersede-prune.test.ts`
- cursor: `[_]`
- core_role: Regression tests for compaction pruning of superseded/useless tool outputs.
- algorithmic_behavior: Helper constructors begin at `packages/agent/test/supersede-prune.test.ts:17`; read/tool result fixtures at `:57`; config builder at `:98`. Test groups cover key derivation at `:107`, tail-case pruning at `:135`, selector semantics at `:206`, protection/latest guards at `:250`, generic `pruneToolOutputs` at `:307`, useless-result pruning at `:369`, and small-result floor at `:507`.
- inputs_outputs_state: Inputs are synthetic session entries, read paths/selectors, tool results, timestamps, and prune configs. Outputs are pruned entry streams with exact placeholder text and preserved protected/latest entries.
- gates_or_invariants: Latest reads never prune; protected tool results are exempt; selector-free reads supersede selector reads but not vice versa; errors are not blanked; tiny useless results are kept when notice would cost more.
- dependencies_and_callers: Exercises `readToolSupersedeKey`, `pruneSupersededToolResults`, and `pruneToolOutputs` from agent compaction.
- edge_cases_or_failure_modes: Idle gap threshold, suffix-size threshold, already-pruned candidates, duplicate selectors, useless+superseded overlap.
- validation_or_tests: This is validation; direct tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-444 `file` `packages/ai/test/anthropic-prefill.test.ts`
- cursor: `[_]`
- core_role: Tests Anthropic message transformation for assistant prefill/replay and thinking preservation.
- algorithmic_behavior: Main describe at `packages/ai/test/anthropic-prefill.test.ts:12` covers appending a user `Continue.` when the final turn is assistant, repairing consecutive assistant turns, avoiding append after user, and preserving thinking/redacted thinking/signatures across transforms at `:124`, `:174`, and `:224`.
- inputs_outputs_state: Inputs are internal `AssistantMessage`/`UserMessage` arrays and model identity. Outputs are Anthropic-compatible message parameters.
- gates_or_invariants: Anthropic cannot receive final assistant-only prefill without a user continuation; redacted thinking and completed signatures must survive when replay-compatible; partial/aborted thinking signatures must be sanitized.
- dependencies_and_callers: Exercises `convertAnthropicMessages()` and `transformMessages()`.
- edge_cases_or_failure_modes: Dropped empty user messages, model-id changes, aborted turn during later output, and completed thinking before interruption.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-474 `file` `packages/ai/test/auth-storage-broker-no-sentinel.test.ts`
- cursor: `[_]`
- core_role: Tests broker-managed OAuth credential refresh boundaries.
- algorithmic_behavior: Test suite at `packages/ai/test/auth-storage-broker-no-sentinel.test.ts:13` sets temp auth storage and spies on provider refresh. `getOAuthAccess` refreshes expired broker credentials through the store hook only at `:51`; `getOAuthApiKey` refuses expired broker sentinels instead of provider-direct refresh at `:88`.
- inputs_outputs_state: Inputs are expired broker credential sentinels, provider definitions, refresh hooks, and auth store state. Outputs are refreshed access values or refused API key resolution.
- gates_or_invariants: Broker sentinel credentials must not bypass the broker by calling provider refresh directly.
- dependencies_and_callers: Exercises `AuthStorage` and OAuth utility refresh boundary.
- edge_cases_or_failure_modes: Expired credentials, missing broker hook, accidental direct refresh.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-504 `file` `packages/ai/test/firepass.test.ts`
- cursor: `[_]`
- core_role: Tests Fire Pass provider catalog routing and request payload defaults.
- algorithmic_behavior: Suite at `packages/ai/test/firepass.test.ts:22` verifies bundled Kimi model entry, friendly-id translation to router id at `:32`, xhigh effort forwarding at `:61`, max-token fallback at `:99`, and canonical router-id default behavior at `:136`.
- inputs_outputs_state: Inputs are model IDs, context messages, mocked SSE responses, and fetch intercepts. Outputs are captured OpenAI-completions request bodies and streamed assistant events.
- gates_or_invariants: Catalog-exposed effort must be passed verbatim; Kimi max_tokens default should apply when caller omits it; friendly IDs route to provider wire IDs.
- dependencies_and_callers: Exercises `streamOpenAICompletions()` and bundled catalog model entries.
- edge_cases_or_failure_modes: Missing max_tokens, canonical versus friendly model id, router model mismatch.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-534 `file` `packages/ai/test/issue-1373-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Bedrock Claude thinking display defaults.
- algorithmic_behavior: Helpers build adaptive/budget models at `packages/ai/test/issue-1373-repro.test.ts:18` and `:37`; payload capture at `:70`. Tests at `:87` through `:129` assert `thinkingDisplay` default/override behavior across Opus 4.7+, Fable/Mythos 5, older Opus 4.6, and budget-based models.
- inputs_outputs_state: Inputs are model ids, effort/thinking options, mocked aborted fetch signal. Outputs are captured Bedrock `additionalModelRequestFields`.
- gates_or_invariants: Newer adaptive-thinking models get summarized display by default; explicit omitted is honored; older models omit display to avoid Bedrock rejection.
- dependencies_and_callers: Exercises `streamBedrock()`, catalog thinking helpers, and Bedrock payload construction.
- edge_cases_or_failure_modes: Provider rejects unsupported `display`; silent streams when display omitted on supported models; budget thinking models require explicit display.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-564 `file` `packages/ai/test/model-cache.test.ts`
- cursor: `[_]`
- core_role: SQLite model-cache migration regression test.
- algorithmic_behavior: Test suite at `packages/ai/test/model-cache.test.ts:32`; `createModel()` fixture at `:12`. Main test at `:49` writes v2 cached models and verifies the next discovery can overwrite them.
- inputs_outputs_state: Inputs are temp SQLite DB, model records, and cache read/write calls. Outputs are preserved/upgraded model cache rows.
- gates_or_invariants: Existing v2 cache data should remain readable and future writes should replace it without schema corruption.
- dependencies_and_callers: Exercises `readModelCache()` and `writeModelCache()` from catalog model cache.
- edge_cases_or_failure_modes: Stale schema, incompatible cached JSON, overwrite after migration.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-594 `file` `packages/ai/test/openai-responses-history-payload.test.ts`
- cursor: `[_]`
- core_role: Comprehensive replay payload tests for OpenAI Responses and Codex Responses.
- algorithmic_behavior: Helpers create tokens/models/payloads at `packages/ai/test/openai-responses-history-payload.test.ts:15`, `:30`, and capture payloads at `:187`. Test suite from `:312` verifies developer instruction ordering, canonical instructions, native history replacement, warmed/cold provider session behavior, cross-provider isolation, incremental history building, phase preservation, id stripping, failed tool-call repair, and orphan output conversion at `:771`.
- inputs_outputs_state: Inputs are internal message histories, provider session state, assistant native payload metadata, tools/tool results, and mocked fetch. Outputs are Responses API `input` payloads and sanitized replay structures.
- gates_or_invariants: Replay-only ids must be stripped while call IDs are preserved; stale thinking signatures must not replay cold; function outputs without calls become assistant notes; failed calls must be rebuilt before tool results.
- dependencies_and_callers: Exercises `createOpenAIResponsesHistoryPayload()`, `streamOpenAIResponses()`, and `streamOpenAICodexResponses()`.
- edge_cases_or_failure_modes: Same-provider warmed state, cold state fallback, stale provider payloads, cross-provider metadata, orphan `function_call_output`, branch replay ending on tool call.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-624 `file` `packages/ai/test/schema-dereference.test.ts`
- cursor: `[_]`
- core_role: Tests JSON Schema `$ref` dereferencing used for tool schemas.
- algorithmic_behavior: Suite at `packages/ai/test/schema-dereference.test.ts:4` verifies non-object passthrough, no-def passthrough, `$defs` and legacy `definitions`, nested arrays/anyOf/oneOf, definition-to-definition refs, circular refs, external refs, sibling keywords, multi-use refs, and a write-memory schema pattern at `:211`.
- inputs_outputs_state: Inputs are JSON schema values; outputs are dereferenced schemas.
- gates_or_invariants: External refs are left untouched; circular refs break with empty object; sibling keywords remain.
- dependencies_and_callers: Exercises `dereferenceJsonSchema()` from AI schema utilities used by provider/tool wire schema mapping.
- edge_cases_or_failure_modes: Circular graphs, legacy definitions, nested unions, duplicated refs, external URLs.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-654 `file` `packages/ai/test/zenmux-login.test.ts`
- cursor: `[_]`
- core_role: Tests ZenMux login prompt and API-key validation flow.
- algorithmic_behavior: Suite at `packages/ai/test/zenmux-login.test.ts:5` mocks fetch and prompt callbacks. Tests validate settings URL opening and `/models` endpoint validation at `:6`, empty key rejection at `:44`, required `onPrompt` at `:52`, and surfaced endpoint errors at `:56`.
- inputs_outputs_state: Inputs are prompted API keys and mocked HTTP responses. Outputs are accepted credential or thrown validation errors.
- gates_or_invariants: Empty keys rejected; prompt callback required; key validated against models endpoint before storage.
- dependencies_and_callers: Exercises `loginZenMux()`.
- edge_cases_or_failure_modes: Missing prompt handler, endpoint non-OK, blank key.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-684 `file` `packages/catalog/test/issue-1617-repro.test.ts`
- cursor: `[_]`
- core_role: Catalog resolver regression for MiniMax M3 routing under opencode providers.
- algorithmic_behavior: Suite at `packages/catalog/test/issue-1617-repro.test.ts:28` locates descriptors for `opencode-zen` and `opencode-go`, then tests static resolution and live `/v1/models` refresh routing at `:60` and `:90`.
- inputs_outputs_state: Inputs are models.dev-style model rows and provider descriptors. Outputs are resolved model API classifications.
- gates_or_invariants: MiniMax M3 under these providers must route to `openai-completions`, not an incompatible endpoint.
- dependencies_and_callers: Exercises catalog provider descriptors/resolvers.
- edge_cases_or_failure_modes: Freshly discovered model IDs lacking static bundled metadata.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-714 `file` `packages/coding-agent/bench/edit-lsp-writethrough.bench.ts`
- cursor: `[_]`
- core_role: Benchmark harness for LSP writethrough edit latency.
- algorithmic_behavior: Generates TypeScript scratch bodies at `packages/coding-agent/bench/edit-lsp-writethrough.bench.ts:35`, times async calls at `:45`, creates deferred promises at `:57`, and exits explicitly at `:108`.
- inputs_outputs_state: Inputs are generated source edits and LSP writethrough/noop implementations. Outputs are timing measurements and scratch files.
- gates_or_invariants: Benchmark compares real `createLspWritethrough` against noop under repeatable generated edits.
- dependencies_and_callers: Depends on `../src/lsp`, filesystem temp paths, and benchmark invocation.
- edge_cases_or_failure_modes: LSP startup delay, diagnostic propagation, filesystem cleanup, generated intentional type diagnostic.
- validation_or_tests: Benchmark, not correctness test.
- skip_candidate: `yes: performance harness rather than production algorithm, though it targets a core edit/LSP path`

### OH_MY_HUMANIZE_MAIN-HZ-744 `file` `packages/coding-agent/test/acp-stdout-hygiene.test.ts`
- cursor: `[_]`
- core_role: Test for ACP command stdout JSON-RPC hygiene.
- algorithmic_behavior: Defines subprocess teardown at `packages/coding-agent/test/acp-stdout-hygiene.test.ts:28`, reads first stdout frame at `:86`, and verifies `initialize` response is first bytes on stdout at `:105`.
- inputs_outputs_state: Inputs are spawned ACP process streams and initialize request. Outputs are first JSON-RPC frame and stderr capture.
- gates_or_invariants: stdout must contain protocol frames only; logging/noise must go to stderr/logs to avoid ACP client breakage.
- dependencies_and_callers: Exercises CLI ACP startup path and terminal auth args.
- edge_cases_or_failure_modes: Startup warnings, logger console leakage, delayed frame parsing, process teardown.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-774 `file` `packages/coding-agent/test/agent-session-openai-responses-replay.test.ts`
- cursor: `[_]`
- core_role: AgentSession integration tests for OpenAI Responses replay metadata sanitization.
- algorithmic_behavior: Helpers build stale provider payloads at `packages/coding-agent/test/agent-session-openai-responses-replay.test.ts:35` and `:42`, persisted session harness at `:190`, and session harness at `:221`. Tests from `:291` through `:756` cover startup resume, `SessionManager.open`, forking, same-file reload, proxy-backed custom details, model changes, read-only session switch, branch navigation, and new session reset.
- inputs_outputs_state: Inputs are persisted session JSONL entries, assistant metadata, model registry/settings/auth storage, and session switching. Outputs are sanitized runtime messages and provider session state transitions.
- gates_or_invariants: Stale Responses-family assistant metadata is removed from loaded messages; user payloads are preserved; provider state is retained only when safe and reset on message/model changes.
- dependencies_and_callers: Exercises `createAgentSession`, `SessionManager`, `AuthStorage`, `ModelRegistry`, and AI replay payload utilities.
- edge_cases_or_failure_modes: Proxy-backed custom details, same-file reload diff only in metadata, read-only load-time sanitization, branch navigation reintroducing stale metadata.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-804 `file` `packages/coding-agent/test/autolearn-learn-local.test.ts`
- cursor: `[_]`
- core_role: Tests local learned-lesson storage/readback and learn tool write behavior.
- algorithmic_behavior: Storage tests begin at `packages/coding-agent/test/autolearn-learn-local.test.ts:17`, readback at `:147`, and tool behavior at `:218`. They verify whitespace normalization, redaction, dedupe/newest-first ordering, 100-lesson cap, empty filtering, prompt delimiter neutralization, oversize bounds, concurrent saves, local backend delegation/status, memory injection budgets, and learn tool write/approval tier.
- inputs_outputs_state: Inputs are lesson text, context, local settings/backend, and tool params. Outputs are `learned.md` content, injected memory context, and tool results/errors.
- gates_or_invariants: Secrets must be redacted before persistence; empty sanitized lessons are rejected; concurrent saves cannot lose data; summary budget can suppress lessons.
- dependencies_and_callers: Exercises local memory backend, learned lesson utilities, and `LearnTool`.
- edge_cases_or_failure_modes: Token split by delimiter, hand-edited raw learned file, oversized context, racing saves.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-834 `file` `packages/coding-agent/test/compaction-serialization.test.ts`
- cursor: `[_]`
- core_role: Tests conversation serialization used by compaction summaries.
- algorithmic_behavior: Suite at `packages/coding-agent/test/compaction-serialization.test.ts:5` verifies long tool results are truncated at `:6`, short tool results are preserved at `:27`, and assistant/user messages are not truncated at `:46`.
- inputs_outputs_state: Inputs are message arrays with tool/user/assistant content. Outputs are serialized text for summarization.
- gates_or_invariants: Tool output truncation should reduce context size without altering normal user/assistant text.
- dependencies_and_callers: Exercises `serializeConversation()` from agent compaction utilities.
- edge_cases_or_failure_modes: Large tool output overpowering summary context.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-864 `file` `packages/coding-agent/test/fuzzy.test.ts`
- cursor: `[_]`
- core_role: Tests TUI fuzzy matcher/filter scoring contract.
- algorithmic_behavior: `fuzzyMatch` tests at `packages/coding-agent/test/fuzzy.test.ts:4` cover empty query, query longer than text, exact match, ordered characters, case insensitivity, consecutive scoring, and word-boundary scoring. `fuzzyFilter` tests at `:57` cover unchanged empty query, filtering, sort ordering, and custom text getter.
- inputs_outputs_state: Inputs are query strings and item text. Outputs are match scores and filtered/sorted arrays.
- gates_or_invariants: Characters must appear in order; boundary/consecutive matches score better; empty query returns all items.
- dependencies_and_callers: Exercises `@oh-my-pi/pi-tui` fuzzy utilities used by selectors/search UI.
- edge_cases_or_failure_modes: Case variations, scattered matches, custom object matching.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-894 `file` `packages/coding-agent/test/input-controller-suspend.test.ts`
- cursor: `[_]`
- core_role: Tests Ctrl-Z suspend/resume behavior in interactive input controller.
- algorithmic_behavior: Context factory at `packages/coding-agent/test/input-controller-suspend.test.ts:16`; platform override at `:34`; tests at `:46` verify Windows no-op, POSIX `SIGTSTP` and `SIGCONT` resume hook, and cleanup when `process.kill` rejects.
- inputs_outputs_state: Inputs are platform, mocked process signal functions, and interactive context. Outputs are terminal restore/resume calls and listener registration/removal.
- gates_or_invariants: Windows must not send unsupported suspend signal; POSIX must restore terminal and redraw on resume; failed signal send cleans up.
- dependencies_and_callers: Exercises `InputController.handleCtrlZ`.
- edge_cases_or_failure_modes: `process.kill` throws, dangling SIGCONT listener, unsupported Windows signal.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-924 `file` `packages/coding-agent/test/issue-846-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test that memory startup stage failures are logged.
- algorithmic_behavior: Suite at `packages/coding-agent/test/issue-846-repro.test.ts:70`; main test at `:92` spies on `logger.error`, sets up model/session/registry, and triggers `startMemoryStartupTask()` stage failures.
- inputs_outputs_state: Inputs are temp dirs, mocked memory storage claims, fake model registry, and logger spy. Outputs are logged error calls with underlying reason.
- gates_or_invariants: Phase1 stage1 memory failures must be visible through centralized logger, not silently swallowed.
- dependencies_and_callers: Exercises `startMemoryStartupTask`, memory storage, `logger`, and model lookup.
- edge_cases_or_failure_modes: Multiple failed claims, async startup task error swallowing.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-954 `file` `packages/coding-agent/test/main-interactive-input.test.ts`
- cursor: `[_]`
- core_role: Tests interactive input routing, title prompt discovery, and CLI API key precedence.
- algorithmic_behavior: Input fixture at `packages/coding-agent/test/main-interactive-input.test.ts:17`; title prompt discovery tests at `:27`; API key precedence at `:40`; submission routing at `:69` covers synthetic continue, canceled optimistic submission, hidden custom prompt with follow-up, idle follow-up, steer intent, goal continuation, and plain streaming queue.
- inputs_outputs_state: Inputs are `SubmittedUserInput`, session/model/auth state, and project config files. Outputs are prompt calls, follow-up routing, and auth storage updates.
- gates_or_invariants: CLI API key overrides config for final session model provider; streaming submissions become follow-up/steer rather than illegal direct prompts; canceled optimistic submissions do not prompt.
- dependencies_and_callers: Exercises `discoverTitleSystemPromptFile`, `applyCliRuntimeApiKey`, and `submitInteractiveInput`.
- edge_cases_or_failure_modes: Race between idle/streaming, hidden custom submissions, goal continuation, provider key precedence.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-984 `file` `packages/coding-agent/test/model-registry-create.test.ts`
- cursor: `[_]`
- core_role: Tests `ModelRegistry.create()` factory and legacy config migration.
- algorithmic_behavior: Suite at `packages/coding-agent/test/model-registry-create.test.ts:10` verifies authStorage wiring and bundled model exposure at `:23`, legacy `models.json` to `models.yml` migration at `:38`, and idempotent second load at `:56`.
- inputs_outputs_state: Inputs are temp config files and auth storage. Outputs are registry instance and migrated config files.
- gates_or_invariants: Factory must sync constructor dependencies; migration runs before sync constructor and is idempotent.
- dependencies_and_callers: Exercises `ConfigFile`, `ModelRegistry`, `ModelsConfigSchema`, `AuthStorage`.
- edge_cases_or_failure_modes: Legacy config present, repeated migration, bundled model availability.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1014 `file` `packages/coding-agent/test/read-tool-group-freeze.test.ts`
- cursor: `[_]`
- core_role: Tests transcript freezing for grouped read tool rendering.
- algorithmic_behavior: Stub component at `packages/coding-agent/test/read-tool-group-freeze.test.ts:9`, success result at `:19`, tests at `:41`, `:63`, and `:82` verify late read result repaint, live pending state until settle, and sealing a never-resolved pending read.
- inputs_outputs_state: Inputs are read tool group component states and transcript container freeze checks. Outputs are render/finalization state.
- gates_or_invariants: Pending read previews must not freeze permanently; finalized groups should freeze only after all entries settle or are sealed.
- dependencies_and_callers: Exercises `ReadToolGroupComponent` and `TranscriptContainer`.
- edge_cases_or_failure_modes: Late result after pending preview, never-resolving read call.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1044 `file` `packages/coding-agent/test/sdk-tool-activation.test.ts`
- cursor: `[_]`
- core_role: Tests SDK session tool activation semantics for default-inactive extension tools and hidden tools.
- algorithmic_behavior: Extension factory at `packages/coding-agent/test/sdk-tool-activation.test.ts:18`; base options at `:71`; tests from `:101` cover excluding defaultInactive tools unless requested, explicit activation, required yield tool, hidden resolve tool in plan mode, dropping resolve when unused, and xAI TTS gated registration at `:202`/`:218`.
- inputs_outputs_state: Inputs are SDK session options, extension tool definitions, toolNames, settings, and plan/yield/TTS flags. Outputs are active/registered tool sets.
- gates_or_invariants: defaultInactive tools do not become active implicitly; hidden resolve remains only when plan/deferrable tooling needs it; TTS tool registration respects enablement.
- dependencies_and_callers: Exercises `createAgentSession`, extension API, `SessionManager`, `Settings`, `ModelRegistry`.
- edge_cases_or_failure_modes: Explicit toolNames excluding hidden helpers, plan mode hidden tool availability, TTS feature flag.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1074 `file` `packages/coding-agent/test/status-line-dispose-async-leak.test.ts`
- cursor: `[_]`
- core_role: Tests status line disposal guards against late async branch callbacks.
- algorithmic_behavior: Setup at `packages/coding-agent/test/status-line-dispose-async-leak.test.ts:29`; session fixture at `:46`; tests at `:99` and `:133` assert `#onBranchChange` is suppressed after `dispose()` when git branch promise/microtask resolves later.
- inputs_outputs_state: Inputs are mocked git branch responses and status line component lifecycle. Outputs are no late UI updates after disposal.
- gates_or_invariants: Disposed component must ignore async completions.
- dependencies_and_callers: Exercises `StatusLineComponent`, git utilities, settings/theme init.
- edge_cases_or_failure_modes: Promise resolves after dispose; IIFE microtask after dispose.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1104 `file` `packages/coding-agent/test/tiny-text.test.ts`
- cursor: `[_]`
- core_role: Tests title/tiny-text preprocessing for session title generation.
- algorithmic_behavior: `stripCodeBlocks` tests at `packages/coding-agent/test/tiny-text.test.ts:12`; `prepareTitleInput` at `:51`; `formatTitleUserMessage` at `:60`; `normalizeGeneratedTitle` at `:70`; `isLowSignalTitleInput` at `:94`.
- inputs_outputs_state: Inputs are user text, code fences, generated title strings, greetings/punctuation/emoji. Outputs are cleaned prose, title prompt content, normalized titles, or low-signal flags.
- gates_or_invariants: Fenced code is stripped unless message is essentially only code; inline code remains; bare none sentinel returns null; greetings/empty punctuation defer title generation.
- dependencies_and_callers: Exercises tiny text utilities used by title generation.
- edge_cases_or_failure_modes: Unterminated fences, pasted mockups, NFD/emoji low signal, title containing word none.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1134 `file` `packages/collab-web/src/app.tsx`
- cursor: `[_]`
- core_role: Main React application shell for collab guest web client.
- algorithmic_behavior: `App()` at `packages/collab-web/src/app.tsx:39` manages stored display name, deep-link hash, connection state, connect/leave/rejoin callbacks, visual viewport CSS variable updates, and renders connect versus session view. `Session()` at `:122` derives subagent count, selected drawer agent, handles agent disappearance, and composes header, banners, transcript, agents panel, composer, drawer, and toasts.
- inputs_outputs_state: Inputs are collab link, stored local name, hash URL, `GuestClient` snapshots, and selected agent id. Outputs are React UI and client lifecycle.
- gates_or_invariants: On leave, client closes and selection resets; selected agent is cleared if removed from snapshot; rejoin attempts client reconnect.
- dependencies_and_callers: Uses collab-web components, `GuestClient`, `useGuestSnapshot`, and tool render host.
- edge_cases_or_failure_modes: Hash link missing, visualViewport unavailable, agent removed while drawer open, reconnect after leave.
- validation_or_tests: Collab behavior validated by collab tests; web UI direct tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1164 `file` `packages/hashline/test/diff-preview.test.ts`
- cursor: `[_]`
- core_role: Tests compact diff preview generation.
- algorithmic_behavior: Suite at `packages/hashline/test/diff-preview.test.ts:4` checks current-line rendering and removed content omission, context renumbering at `:15`, long added-run collapse at `:22`, adjacent elision marker normalization at `:32`, and blank gap row cleanup at `:38`.
- inputs_outputs_state: Inputs are compact diff strings. Outputs are preview text and count metadata.
- gates_or_invariants: Removed content omitted but counts preserved; post-edit line numbers correct; long added runs collapse to head/marker/tail.
- dependencies_and_callers: Exercises `buildCompactDiffPreview()` from hashline.
- edge_cases_or_failure_modes: Adjacent elisions, blank separators, range expansion renumbering.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1194 `file` `packages/mnemopi/test/consolidate-fact-concurrency.test.ts`
- cursor: `[_]`
- core_role: Tests SQLite transaction/concurrency behavior for fact consolidation.
- algorithmic_behavior: DB fixture at `packages/mnemopi/test/consolidate-fact-concurrency.test.ts:8`; tests from `:20` assert repeated same SPO observations compound confidence into one row, distinct SPOs through separate connections are preserved, outer transactions are used instead of nested begin, mid-update errors rollback, and conflict-recording failure does not leak facts.
- inputs_outputs_state: Inputs are temp DB path, `VeracityConsolidator`, SPO observations, and injected failure paths. Outputs are fact rows/confidence and rollback state.
- gates_or_invariants: Consolidation must be serialized safely and transactional; partial writes must roll back.
- dependencies_and_callers: Exercises `VeracityConsolidator`, DB open/close helpers.
- edge_cases_or_failure_modes: Separate connections, nested transaction attempts, mid-update exception, conflict insert failure.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1224 `file` `packages/mnemopi/test/polyphonic-recall.test.ts`
- cursor: `[_]`
- core_role: Tests multi-voice recall fusion in mnemopi.
- algorithmic_behavior: Fixtures at `packages/mnemopi/test/polyphonic-recall.test.ts:39` and `:55`; suite at `:94` verifies gate read per call, four-voice RRF fusion and attribution order, per-voice gates without fake-success, session/global visibility filters, fact source hydration, and Beam-state engine caching/hydration.
- inputs_outputs_state: Inputs are Beam memory state, seeded memories/facts, recall gates, query options. Outputs are fused recall results with voice scores/source attribution.
- gates_or_invariants: Disabled voices produce no fake success; visibility limited to session/global; RRF preserves attribution order.
- dependencies_and_callers: Exercises `PolyphonicRecallEngine`, Beam memory, DB helpers.
- edge_cases_or_failure_modes: Per-call gate changes, fact sources outside visibility scope, cached engine reuse.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1254 `file` `packages/natives/scripts/gen-enums.ts`
- cursor: `[_]`
- core_role: Codegen script that syncs JS native export surface from TypeScript declarations.
- algorithmic_behavior: Regexes match declared classes/functions at `packages/natives/scripts/gen-enums.ts:30` and `:35`; `collectEnums()` at `:42` extracts enum members; `collectMatches()` at `:66` extracts class/function names; `buildGeneratedBlock()` at `:77` constructs the generated `index.js` export block; `generateEnumExports()` at `:111` writes updated exports.
- inputs_outputs_state: Inputs are `native/index.d.ts` and `native/index.js` marker block. Output is generated JS export constants and enum objects.
- gates_or_invariants: Only public declarations in d.ts are exported; marker block boundaries must exist; generated block order must be deterministic.
- dependencies_and_callers: Used by native build/release scripts after napi-rs d.ts generation.
- edge_cases_or_failure_modes: Regex mismatch for new declaration shapes, missing markers, enum formatting drift.
- validation_or_tests: Native export consistency is validated by build/runtime import tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1284 `file` `packages/snapcompact/research/exp12_arbitrage.py`
- cursor: `[_]`
- core_role: Research experiment script for snapcompact visual/token arbitrage probes.
- algorithmic_behavior: `mine()` at `packages/snapcompact/research/exp12_arbitrage.py:56` gathers mined data; `post_h()` at `:112` posts HTTP requests with retries; `probe_call()` at `:135` calls model APIs; `probe_pngs()` at `:169` creates probe images; `run_probes()` at `:183` runs model probes; `estimate_carriers()` at `:211` estimates carrier capacity; `derive()` at `:245` combines mined/probe data; `main()` at `:277` drives CLI.
- inputs_outputs_state: Inputs are CLI args, API keys, mined SQuAD data, PNG paths, HTTP model responses. Outputs are derived JSON/research metrics.
- gates_or_invariants: HTTP errors exit with detail; retries wrap transient failures; condition budgets derive from condition string.
- dependencies_and_callers: Depends on local `squad` module, PIL/image assets indirectly, and model endpoints. Not in main runtime path.
- edge_cases_or_failure_modes: API errors, missing images, invalid condition string, probe model failures.
- validation_or_tests: Research script; no test located.
- skip_candidate: `yes: research-only experiment, not shipped runtime behavior`

### OH_MY_HUMANIZE_MAIN-HZ-1314 `file` `packages/snapcompact/research/snapcompact_logit_lens_viz.py`
- cursor: `[_]`
- core_role: Research visualization script for snapcompact logit-lens outputs.
- algorithmic_behavior: Font helpers at `packages/snapcompact/research/snapcompact_logit_lens_viz.py:32` and `:42`; `heat_fill()` at `:49` maps probability/hit status to colors; `main()` at `:57` parses input JSON and renders visualization.
- inputs_outputs_state: Inputs are CLI args and logit-lens JSON data. Outputs are image visualization files.
- gates_or_invariants: Probabilities are converted to heat colors; fonts fallback based on availability.
- dependencies_and_callers: Depends on PIL; research-only tooling for snapcompact experiments.
- edge_cases_or_failure_modes: Missing fonts, malformed JSON, invalid probability ranges.
- validation_or_tests: No direct test located.
- skip_candidate: `yes: visualization research utility rather than core production algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1344 `file` `packages/stats/scripts/generate-client-bundle.ts`
- cursor: `[_]`
- core_role: Build script embedding the stats web client bundle into a generated TS module.
- algorithmic_behavior: `collectFiles()` at `packages/stats/scripts/generate-client-bundle.ts:18` recursively gathers files; `buildArchiveBase64()` at `:33` normalizes relative paths and creates archive data; `main()` at `:54` drives bundling.
- inputs_outputs_state: Inputs are stats client build directory files. Output is generated base64 bundle source/artifact.
- gates_or_invariants: Relative paths are normalized with `/`; temp/archive creation must include all files deterministically enough for runtime serving.
- dependencies_and_callers: Depends on Bun shell and filesystem; called by stats package build.
- edge_cases_or_failure_modes: Missing build dir, archive command failure, path separator differences.
- validation_or_tests: Build pipeline validates generated bundle.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1374 `file` `packages/tui/src/keybindings.ts`
- cursor: `[_]`
- core_role: TUI keybinding definition, normalization, conflict detection, and global manager.
- algorithmic_behavior: `TUI_KEYBINDINGS` defaults at `packages/tui/src/keybindings.ts:57`; conflict type at `:139`; `canonicalKeyId()` at `:185`; alias expansion at `:217`; `KeybindingsManager` at `:242`; global setter/getter at `:328`/`:332`.
- inputs_outputs_state: Inputs are configured key IDs, parsed keys, keybinding names. Outputs are normalized key maps, lookup results, and conflict records.
- gates_or_invariants: Modifiers/case are canonicalized; aliases are expanded; config arrays normalize to lower-case ids; conflicts are detectable.
- dependencies_and_callers: Used by TUI input handling and coding-agent keybinding config/tests.
- edge_cases_or_failure_modes: Uppercase letters, modifier prefixes, duplicate aliases, unknown key IDs.
- validation_or_tests: Related tests in `packages/tui/test/input.test.ts` and plan overlay keybinding tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1404 `file` `packages/tui/test/input.test.ts`
- cursor: `[_]`
- core_role: Tests terminal input editing, paste, Unicode, Kitty protocol, and render width.
- algorithmic_behavior: Suite at `packages/tui/test/input.test.ts:14`; tests cover CJK/punctuation word movement at `:26` and `:64`, NBSP at `:76`, joiners at `:85`, Unicode punctuation at `:104`, Kitty backspace/digits/operators at `:123`/`:136`/`:148`, bracketed paste tab normalization at `:158`, tmux C0 decoding at `:171`, wide-char render width at `:186`, Korean NFC normalization at `:196`, cursor marker at `:236`, and OSC paste at `:250`.
- inputs_outputs_state: Inputs are key sequences and paste payloads. Outputs are input buffer text, cursor position, and rendered lines.
- gates_or_invariants: Render never exceeds width; paste normalizes tabs/NFC; Kitty release events must not double-delete; raw C0 tails do not leak.
- dependencies_and_callers: Exercises `Input`, key parsing, visible width, indentation utils.
- edge_cases_or_failure_modes: Wide chars, Korean decomposition, tmux re-encoding, keypad variants, non-bracketed paste transport.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1434 `file` `packages/tui/test/process-terminal-render.test.ts`
- cursor: `[_]`
- core_role: Tests process terminal renderer reflow on geometry changes.
- algorithmic_behavior: Suite at `packages/tui/test/process-terminal-render.test.ts:11`; tests verify OS-width reflow on resize when in-band resize inactive at `:19`, fallback when in-band report missed at `:30`, in-band geometry authority at `:46`, and split stdin reads at `:61`.
- inputs_outputs_state: Inputs are harness terminal sizes and in-band resize reports. Outputs are rendered terminal geometry.
- gates_or_invariants: In-band report wins when present; OS width fallback works when reports are absent/split.
- dependencies_and_callers: Exercises process terminal render harness and renderer.
- edge_cases_or_failure_modes: Split escape/report reads, mismatched OS and in-band widths.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1464 `file` `packages/tui/test/ttyid.test.ts`
- cursor: `[_]`
- core_role: Tests terminal identity derivation across multiplexers and terminals.
- algorithmic_behavior: Environment fixture at `packages/tui/test/ttyid.test.ts:15`; tests at `:36` verify CMUX, tmux, Kitty, Zellij, and WezTerm precedence plus path-safe Zellij session normalization.
- inputs_outputs_state: Inputs are env vars such as `CMUX_SURFACE_ID`, `TMUX_PANE`, `ZELLIJ_PANE_ID`, `KITTY_WINDOW_ID`, and `WEZTERM_PANE`. Output is terminal ID string.
- gates_or_invariants: Multiplexer IDs have defined precedence; empty values ignored; path separators normalized.
- dependencies_and_callers: Exercises `getTerminalId()`.
- edge_cases_or_failure_modes: Inherited outer terminal vars, empty cmux, Zellij session scoping.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1494 `file` `packages/utils/src/logger.ts`
- cursor: `[_]`
- core_role: Central logger and timing instrumentation utility.
- algorithmic_behavior: Directory creation at `packages/utils/src/logger.ts:21`; JSON error replacer at `:34`; Winston format/transports at `:53`, `:76`, `:87`, `:100`, and singleton at `:107`. Logging functions `error/warn/info/debug` at `:135`, `:148`, `:161`, `:174`; startup marker at `:190`; timing mode and printing at `:220`/`:244`; module load graph rendering at `:520`; `time()` overload at `:612`.
- inputs_outputs_state: Inputs are log messages/context, env timing flags, spans, module-load events. Outputs are rotated log files, optional console logs, timing summaries, and span state.
- gates_or_invariants: Error objects serialize message/stack/name/cause; transports can be reset; timing spans nest via AsyncLocalStorage; module-load summaries deduplicate/shorten paths.
- dependencies_and_callers: Used across packages, especially coding-agent where console logging is forbidden. Depends on winston, daily rotate file, dirs/timing-buffer utilities.
- edge_cases_or_failure_modes: Circular/complex context values, async span completion, module load buffer draining, file transport creation failure.
- validation_or_tests: `packages/utils/test/logger-error-serialization.test.ts` validates error serialization.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1524 `file` `packages/utils/test/logger-error-serialization.test.ts`
- cursor: `[_]`
- core_role: Tests logger serialization of Error fields.
- algorithmic_behavior: `waitForLogEntry()` at `packages/utils/test/logger-error-serialization.test.ts:36` polls rotated log file lines for target messages. Tests at `:53` and `:65` verify `Error.message`, `stack`, `name`, `cause`, and custom enumerable fields are preserved.
- inputs_outputs_state: Inputs are temporary logger file transport and Error objects. Outputs are JSON log entries.
- gates_or_invariants: Error metadata must not collapse to `{}` or lose cause/custom fields.
- dependencies_and_callers: Exercises `logger.setTransports()` and error/warn paths.
- edge_cases_or_failure_modes: Async log flush timing, nested Error cause.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1554 `file` `python/robomp/src/db.py`
- cursor: `[_]`
- core_role: SQLite persistence layer for RobOMP event/issue/submission/closure workflows.
- algorithmic_behavior: Schema constants create `events`, `issues`, `tool_calls`, `pr_review_comments`, `submissions`, and `pending_closures` tables at `python/robomp/src/db.py:35` through `:114`. `Database._txn()` at `:258` uses `BEGIN IMMEDIATE` with commit/rollback. Event methods record, claim, mark, retry, requeue, and list events from `:269` through `:651`. Issue methods upsert/query/update from `:658` through `:820`. Tool/review/submission/closure logic spans `:827` through `:1134`. Singleton helpers are at `:1151` and `:1161`.
- inputs_outputs_state: Inputs are webhook delivery IDs, event payloads, issue keys, repo/number, tool call payloads, review comments, login limits, pending closure rows. Outputs are row dataclasses and persisted state transitions.
- gates_or_invariants: Event claim excludes issues with running events; transactions rollback on failure; submissions enforce per-user/repo admission counts; closure claiming atomically marks due rows.
- dependencies_and_callers: Used by RobOMP workers/web app. Depends on sqlite3, dataclasses, threading, and JSON serialization.
- edge_cases_or_failure_modes: Stuck running reset, duplicate deliveries, stale pending closures, rate-limit admission, concurrent claimers, rollback on exception.
- validation_or_tests: Pragmas tests cover adjacent parsing; DB-specific tests not assigned here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1584 `file` `python/robomp/tests/test_pragmas.py`
- cursor: `[_]`
- core_role: Tests RobOMP pragma parsing and alias resolution.
- algorithmic_behavior: Tests at `python/robomp/tests/test_pragmas.py:11` through `:97` cover inline, multiple, stacked, equals-form, indented commands, mixed lines, path refs, missing values, dangling command abort, blank preservation, empty body, case normalization, and last-wins value. Alias tests at `:103` through `:144` cover model and thinking-level resolution.
- inputs_outputs_state: Inputs are issue/comment bodies with pragma-like lines. Outputs are parsed pragma maps, cleaned body, resolved model IDs/thinking levels.
- gates_or_invariants: Non-command path refs are not consumed; dangling command aborts line; last value wins; unknown thinking level rejected.
- dependencies_and_callers: Exercises RobOMP pragma parser and alias functions.
- edge_cases_or_failure_modes: Multiple commands one line, equals syntax, blank line preservation, full model IDs versus aliases.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1614 `directory` `packages/coding-agent/src/discovery/builtin-rules`
- cursor: `[_]`
- core_role: Built-in rule corpus for coding-agent discovery/lint guidance.
- algorithmic_behavior: Markdown rules define scoped edit/write guidance for Rust and TypeScript. `index.ts` imports all markdown as text at `packages/coding-agent/src/discovery/builtin-rules/index.ts:11` through `:28` and exposes `BUILTIN_RULE_SOURCES` at `:37`. Rules include no TypeScript `any`, no dynamic imports, no `ReturnType`, `Promise.withResolvers`, import-type usage, no inline cast member access, Rust `LazyLock`, `parking_lot`, result aliases, match ergonomics, and avoiding `Box::leak`.
- inputs_outputs_state: Inputs are source paths/tool scopes and rule names/frontmatter. Outputs are bundled rule sources consumed by discovery.
- gates_or_invariants: Built-ins are lowest-priority defaults; project/user rules with same name override; compiled binary embeds markdown text via static imports.
- dependencies_and_callers: Used by discovery/rule providers and prompt/tool rule injection in coding-agent.
- edge_cases_or_failure_modes: Duplicate rule names, scope mismatch, compiled binary lacking loose files if not statically imported.
- validation_or_tests: Indirectly tested by discovery/persistence and rule activation behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1644 `directory` `packages/coding-agent/test/modes/components`
- cursor: `[_]`
- core_role: TUI component regression suite for coding-agent interactive UI rendering and interaction.
- algorithmic_behavior: Recursively inspected component tests including session selector, user message selectors, tree selector, transcript container, copy selector, welcome, OAuth/logout selectors, assistant message error/mermaid/streaming, plan review overlay, segment track, hook selector slider, plugin marketplace list, compaction dividers/summaries, chat blocks, background task tool execution, history search, settings layout, and status/scope. `plan-review-overlay.test.ts:31` is the largest interaction model, testing option cursor, body scroll, ToC, annotations, external editor, mouse click/hover, and slider behavior.
- inputs_outputs_state: Inputs are component props, keyboard/mouse events, test themes/settings, session lists, transcript blocks, and plugin/session fixtures. Outputs are rendered ANSI text and callback invocations.
- gates_or_invariants: Text must fit/render correctly, disabled options skipped, scroll offsets stable, hover excludes disabled options, selectors preserve status/scope, streaming fast paths render without layout corruption.
- dependencies_and_callers: Exercises components under `packages/coding-agent/src/modes/components/**`, TUI renderer, theme/keybinding managers, and settings.
- edge_cases_or_failure_modes: Very long plans, viewport constraints, late diagnostics, empty selector states, last branch gutter, collapsed/expanded messages, hover clearing.
- validation_or_tests: This directory is validation; no tests run during research.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1674 `file` `packages/agent/src/compaction/compaction.ts`
- cursor: `[_]`
- core_role: Core conversation compaction/handoff summarization engine.
- algorithmic_behavior: Token accounting helpers at `packages/agent/src/compaction/compaction.ts:175`, `:179`, `:204`, threshold/reserve logic at `:218`, `:225`, `:231`; token estimation at `:263`; cut-point discovery at `:361`, turn start at `:403`, and `findCutPoint()` at `:445`; summary generation at `:622`; handoff prompt/render/generation at `:730`/`:737`; `prepareCompaction()` at `:869`; main `compact()` at `:983`; turn-prefix summary at `:1148`.
- inputs_outputs_state: Inputs are session entries/messages, usage, model/context window/settings, tools, telemetry, file-operation metadata, and additional context. Outputs are compaction result entries, summaries, handoff docs, branch summary messages, and updated message sequences.
- gates_or_invariants: Reserve tokens/thresholds clamp compaction; cut points avoid splitting tool-call/result contracts and branch/custom boundaries; summary responses must contain text; compaction can short-circuit when path already compacted.
- dependencies_and_callers: Used by agent runtime/coding-agent session compaction. Depends on pi-ai completion, catalog thinking/dialect helpers, snapcompact, tokenizer, prompt markdown files, telemetry.
- edge_cases_or_failure_modes: Missing text in summary response, invalid cut point, repeated compaction entries, long tool outputs, custom branch summaries, model-specific thinking effort.
- validation_or_tests: Assigned compaction serialization and supersede prune tests cover adjacent contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1704 `file` `packages/ai/src/dialect/factory.ts`
- cursor: `[_]`
- core_role: Dialect registry/factory for in-band tool-call scanners.
- algorithmic_behavior: Imports dialect definitions at `packages/ai/src/dialect/factory.ts:1` through `:13`; `getDialectDefinition()` at `:30` selects by dialect id; `createInbandScanner()` at `:34` instantiates scanner with options.
- inputs_outputs_state: Input is a `Dialect` string and scanner options. Output is dialect definition or scanner instance.
- gates_or_invariants: Dialect id must exist in static registry; scanner creation delegates to selected definition.
- dependencies_and_callers: Used by AI streaming/parser code for Anthropic, Gemini, Gemma, Harmony, Hermes, Kimi, Minimax, Qwen, XML, and pi dialects.
- edge_cases_or_failure_modes: Unknown dialect should fail through map lookup/undefined behavior depending implementation.
- validation_or_tests: Dialect-specific tests/doc specs validate behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1734 `file` `packages/ai/src/providers/github-copilot-headers.ts`
- cursor: `[_]`
- core_role: GitHub Copilot provider header/base-url/accounting helper.
- algorithmic_behavior: `resolveGitHubCopilotBaseUrl()` at `packages/ai/src/providers/github-copilot-headers.ts:14` parses API key/base URL; `inferCopilotInitiator()` at `:25` infers user/agent from last message/tool result; `hasCopilotVisionInput()` at `:55`; override header parser at `:71`; plan normalization at `:88`; premium multiplier/requests at `:92`/`:100`; `buildCopilotDynamicHeaders()` at `:113`.
- inputs_outputs_state: Inputs are API key, base URL, message history, headers, model pricing/multiplier and plan tier. Outputs are base URL, dynamic headers, initiator, vision flag, and premium request count.
- gates_or_invariants: Header override must be valid initiator; free plan multiplier defaults differently than paid; image input toggles vision header.
- dependencies_and_callers: Used by Copilot-compatible provider request construction. Depends on catalog GitHub Copilot parsing.
- edge_cases_or_failure_modes: Last block is tool_result, unknown plan tier, absent multiplier, invalid override header.
- validation_or_tests: Provider tests cover related Copilot behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1764 `file` `packages/ai/src/registry/aimlapi.ts`
- cursor: `[_]`
- core_role: Provider registry definition for AIML API.
- algorithmic_behavior: Exports `aimlApiProvider` at `packages/ai/src/registry/aimlapi.ts:3`, typed as `ProviderDefinition`, containing provider identity/config metadata.
- inputs_outputs_state: Input is registry import; output is provider definition for discovery/auth/model routing.
- gates_or_invariants: Provider id/config must match registry expectations.
- dependencies_and_callers: Used by provider registry aggregation.
- edge_cases_or_failure_modes: Misconfigured id/base URL would break provider discovery.
- validation_or_tests: Covered by registry/model resolution tests indirectly.
- skip_candidate: `yes: static provider descriptor, minimal algorithm beyond routing metadata`

### OH_MY_HUMANIZE_MAIN-HZ-1794 `file` `packages/ai/src/registry/minimax.ts`
- cursor: `[_]`
- core_role: Provider registry definition for MiniMax.
- algorithmic_behavior: Exports `minimaxProvider` at `packages/ai/src/registry/minimax.ts:3`, typed as `ProviderDefinition`.
- inputs_outputs_state: Input is registry import; output is provider definition used for auth/model routing.
- gates_or_invariants: Static provider id and config must remain consistent with catalog/provider model routes.
- dependencies_and_callers: Used by AI registry and catalog resolution paths.
- edge_cases_or_failure_modes: Static metadata drift versus actual provider endpoint.
- validation_or_tests: MiniMax routing covered by catalog issue regression.
- skip_candidate: `yes: static descriptor, not a substantial algorithm by itself`

### OH_MY_HUMANIZE_MAIN-HZ-1824 `file` `packages/ai/src/registry/xiaomi-token-plan-ams.ts`
- cursor: `[_]`
- core_role: Provider registry descriptor for Xiaomi token-plan AMS OAuth-backed provider.
- algorithmic_behavior: Exports `xiaomiTokenPlanAmsProvider` at `packages/ai/src/registry/xiaomi-token-plan-ams.ts:4`, with provider definition and OAuth callback typings.
- inputs_outputs_state: Inputs are registry discovery and OAuth callbacks; output is provider metadata.
- gates_or_invariants: Provider definition must satisfy registry schema and connect to OAuth login flow where configured.
- dependencies_and_callers: Used by AI provider registry/auth setup.
- edge_cases_or_failure_modes: Missing callback wiring or mismatched provider id.
- validation_or_tests: Indirect registry/auth tests.
- skip_candidate: `yes: mostly static provider metadata`

### OH_MY_HUMANIZE_MAIN-HZ-1854 `file` `packages/ai/src/utils/parse-bind.ts`
- cursor: `[_]`
- core_role: Bind-address parser utility for host/port CLI/config values.
- algorithmic_behavior: `parsePort()` at `packages/ai/src/utils/parse-bind.ts:12` validates numeric port range; `parseBind()` at `:36` parses raw string into `{host, port}` supporting bare port and host:port forms.
- inputs_outputs_state: Input is raw bind string. Output is parsed bind object.
- gates_or_invariants: Port must be all digits and in valid TCP range; empty/invalid forms throw.
- dependencies_and_callers: Used by server/callback bind configuration.
- edge_cases_or_failure_modes: Bare numeric port, IPv4/host with colon, nonnumeric port, out-of-range port, whitespace.
- validation_or_tests: No direct test assigned; behavior is small and deterministic.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1884 `file` `packages/catalog/src/identity/priority.ts`
- cursor: `[_]`
- core_role: Provider priority ranking for model identity resolution.
- algorithmic_behavior: `addProviderRank()` at `packages/catalog/src/identity/priority.ts:42` assigns first-seen rank; `buildModelProviderPriorityRank()` at `:48` builds map from optional configured order plus defaults.
- inputs_outputs_state: Input is optional provider order. Output is provider-to-rank map.
- gates_or_invariants: First occurrence wins; defaults fill remaining providers.
- dependencies_and_callers: Used by model identity/provider selection when multiple providers expose related model IDs.
- edge_cases_or_failure_modes: Duplicate configured providers, unknown provider ids, missing configured order.
- validation_or_tests: Catalog identity tests likely cover priority behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1914 `file` `packages/coding-agent/src/capability/context-file.ts`
- cursor: `[_]`
- core_role: Capability provider for context files.
- algorithmic_behavior: Defines `ContextFile` at `packages/coding-agent/src/capability/context-file.ts:14` and `contextFileCapability` at `:27` via `defineCapability`, likely normalizing file paths/source metadata.
- inputs_outputs_state: Inputs are discovered context file paths and `SourceMeta`. Outputs are capability items available to context loading.
- gates_or_invariants: Context file records include path and source; path handling uses `node:path`.
- dependencies_and_callers: Used by coding-agent capability/discovery system.
- edge_cases_or_failure_modes: Duplicate paths, relative versus absolute path normalization, invalid source metadata.
- validation_or_tests: Indirect discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1944 `file` `packages/coding-agent/src/cli/flag-tables.ts`
- cursor: `[_]`
- core_role: Declarative CLI flag parsing tables for coding-agent.
- algorithmic_behavior: Setter types/interfaces at `packages/coding-agent/src/cli/flag-tables.ts:45`; string setters begin at `:78` and map many flags in `STRING_SETTERS` at `:93`; optional flags at `:213`; flag sets exported at `:225`, `:239`, and valueless flags at `:261`.
- inputs_outputs_state: Inputs are CLI flag names/values and parse deps. Outputs are mutated `Args` result fields.
- gates_or_invariants: Comma-separated flags are trimmed/split; optional flags distinguish absent versus provided value; extension shadowable flags are whitelisted.
- dependencies_and_callers: Used by `parseArgs` and command classes.
- edge_cases_or_failure_modes: Missing values for required string flags, optional value ambiguity, CSV whitespace, invalid effort/model role values.
- validation_or_tests: CLI tests cover parsing behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1974 `file` `packages/coding-agent/src/commands/acp.ts`
- cursor: `[_]`
- core_role: CLI command adapter for ACP mode.
- algorithmic_behavior: `Acp` command class at `packages/coding-agent/src/commands/acp.ts:12` parses args, prepares terminal-auth args, and delegates to `runRootCommand`.
- inputs_outputs_state: Inputs are command argv and terminal auth prep. Output is root command execution in ACP mode.
- gates_or_invariants: ACP args must be parsed through standard parser; terminal auth args are injected before root command.
- dependencies_and_callers: Uses `Command`, `parseArgs`, `runRootCommand`, and `prepareAcpTerminalAuthArgs`.
- edge_cases_or_failure_modes: Bad CLI flags, terminal auth setup failure.
- validation_or_tests: ACP stdout hygiene test validates startup output contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2004 `file` `packages/coding-agent/src/commands/workflow.ts`
- cursor: `[_]`
- core_role: CLI command adapter for workflow subcommands.
- algorithmic_behavior: `Workflow` command class at `packages/coding-agent/src/commands/workflow.ts:10` defines flags/action handling and delegates to `resolveWorkflowCommandArgs()` and `runWorkflowCommand()`.
- inputs_outputs_state: Inputs are CLI action/flags. Outputs are workflow command execution results.
- gates_or_invariants: Workflow action must resolve to supported `WorkflowAction`; app name/flags integrated through CLI framework.
- dependencies_and_callers: Uses `@oh-my-pi/pi-utils/cli` and workflow CLI module.
- edge_cases_or_failure_modes: Unsupported action, missing required args, invalid flags.
- validation_or_tests: Workflow inspection tests cover adjacent workflow model behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2034 `file` `packages/coding-agent/src/debug/index.ts`
- cursor: `[_]`
- core_role: Interactive debug selector UI and debug action dispatcher.
- algorithmic_behavior: `formatFileHyperlink()` at `packages/coding-agent/src/debug/index.ts:66`; `DebugSelectorComponent` at `:74` builds a TUI menu for logs, profiler, heap/report bundles, raw SSE, protocol probe, terminal/system info, remote debugger, artifact cache, and session transcript blocks. `showDebugSelector()` at `:556` mounts it.
- inputs_outputs_state: Inputs are interactive mode context, session/log/profiler data, key selections. Outputs are debug overlays, reports, remote debugger server, opened paths, and terminal notifications.
- gates_or_invariants: Debug actions should use context-safe notifications and file hyperlinks; artifact/report generation must handle missing sessions/logs.
- dependencies_and_callers: Uses TUI components, profiler, raw-sse viewer, report bundle, terminal/system info, remote debugger.
- edge_cases_or_failure_modes: Missing logs/session dir, failed profiler/report creation, remote debugger startup failure.
- validation_or_tests: Raw SSE pretty test covers one debug subcomponent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2064 `file` `packages/coding-agent/src/discovery/ssh.ts`
- cursor: `[_]`
- core_role: SSH host discovery provider.
- algorithmic_behavior: `parsePort()` at `packages/coding-agent/src/discovery/ssh.ts:34`, `parseCompat()` at `:41`, `normalizeHost()` at `:50`, `loadSshJsonFile()` at `:87`, and provider `load()` at `:128` which dedupes sources, loads JSON, aggregates items/warnings.
- inputs_outputs_state: Inputs are SSH JSON config files from capability source levels. Outputs are normalized `SSHHost` capability items and warnings.
- gates_or_invariants: Ports and compat flags are normalized from string/boolean/number; env vars are expanded; duplicate source paths collapsed.
- dependencies_and_callers: Registers provider through capability discovery, uses `getSSHConfigPath`, `tryParseJson`, `readFile`, `expandTilde`, `expandEnvVarsDeep`.
- edge_cases_or_failure_modes: Invalid JSON, missing files, nonnumeric port, env expansion, duplicate host entries.
- validation_or_tests: SSH helper tests likely elsewhere; no direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2094 `file` `packages/coding-agent/src/export/ttsr.ts`
- cursor: `[_]`
- core_role: Transcript tool-scope rule injection/export manager.
- algorithmic_behavior: Types define match source/context/scope at `packages/coding-agent/src/export/ttsr.ts:14` through `:50`; `TtsrManager` at `:72` manages rules/injections. Around `:294` it checks regex stream conditions; at `:311` it compiles AST conditions with `astMatch` strictness.
- inputs_outputs_state: Inputs are transcript chunks, rule definitions, text/thinking/tool scopes, AST patterns, paths. Outputs are injection records, matched rule context, and exported TTSR content.
- gates_or_invariants: Rule matching respects source/scope and AST conditions; injected content should not repeat incorrectly; logger handles errors.
- dependencies_and_callers: Uses native `astMatch`, rule capability, settings, logger.
- edge_cases_or_failure_modes: Invalid AST pattern, stream-buffer partial match, tool-scope mismatch, path/language mismatch.
- validation_or_tests: Rule discovery tests indirectly cover related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2124 `file` `packages/coding-agent/src/internal-urls/mcp-protocol.ts`
- cursor: `[_]`
- core_role: Internal URL protocol handler for MCP resources.
- algorithmic_behavior: `escapeRegex()` at `packages/coding-agent/src/internal-urls/mcp-protocol.ts:5`; URI-template scoring at `:9`; resource URI extraction at `:23`; server resolution at `:34`; resource listing formatting at `:86`; `McpProtocolHandler` at `:103` implements protocol read/list behavior.
- inputs_outputs_state: Inputs are internal URLs and MCP manager resource/server registry. Outputs are internal resource content or formatted resource listing.
- gates_or_invariants: URI template match score favors literal chars/segments; target server resolved by matching known resources/templates; URL path extracts original resource URI.
- dependencies_and_callers: Uses `MCPManager` and internal URL protocol dispatch.
- edge_cases_or_failure_modes: Ambiguous templates, no matching server, malformed internal URL, unavailable MCP server.
- validation_or_tests: MCP protocol tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2154 `file` `packages/coding-agent/src/mcp/json-rpc.ts`
- cursor: `[_]`
- core_role: JSON-RPC/SSE HTTP client helper for MCP calls.
- algorithmic_behavior: `redactUrlForLog()` at `packages/coding-agent/src/mcp/json-rpc.ts:18` strips sensitive query params; `parseSSE()` at `:32` parses SSE data lines; `callMCP()` at `:80` sends JSON-RPC request and handles response.
- inputs_outputs_state: Inputs are URL, method, params, headers, abort/fetch options. Outputs are typed JSON-RPC response data or thrown/logged errors.
- gates_or_invariants: Sensitive query params redacted in logs; SSE data parsed from `data:` lines; JSON-RPC error responses map to failures.
- dependencies_and_callers: Used by MCP manager/client code. Depends on logger and fetch.
- edge_cases_or_failure_modes: Invalid SSE/JSON, HTTP error, redaction parse failure, abort.
- validation_or_tests: MCP tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2184 `file` `packages/coding-agent/src/modes/index.ts`
- cursor: `[_]`
- core_role: Barrel and postmortem safety setup for modes package.
- algorithmic_behavior: Imports emergency terminal restore and postmortem at `packages/coding-agent/src/modes/index.ts:1`; re-exports interactive and RPC modules at `:11` through `:13`.
- inputs_outputs_state: Input is module import; output is mode exports and side-effect setup.
- gates_or_invariants: Mode package import should establish terminal postmortem restore safety.
- dependencies_and_callers: Consumed by coding-agent mode imports.
- edge_cases_or_failure_modes: Misordered imports could reduce crash terminal recovery.
- validation_or_tests: TUI/process tests cover related behavior.
- skip_candidate: `yes: mostly export/side-effect wiring, not an algorithm-heavy unit`

### OH_MY_HUMANIZE_MAIN-HZ-2214 `file` `packages/coding-agent/src/session/auth-broker-config.ts`
- cursor: `[_]`
- core_role: Resolves auth broker client configuration from token file/config.
- algorithmic_behavior: Token path at `packages/coding-agent/src/session/auth-broker-config.ts:29`; `readTokenFile()` at `:33`; config YAML snapshot at `:45`; `readConfigYaml()` at `:50`; cached `resolveAuthBrokerConfig()` at `:88`; uncached resolver at `:103`.
- inputs_outputs_state: Inputs are agent dir token file, YAML config, environment-resolved config values. Output is `AuthBrokerClientConfig` or null.
- gates_or_invariants: Missing files return null through `isEnoent`; config values are resolved via central config resolver; invalid/missing endpoint/token disables broker config.
- dependencies_and_callers: Used by session auth storage/broker. Depends on `getAgentDir`, `getConfigRootDir`, Bun YAML, logger.
- edge_cases_or_failure_modes: Missing token file, invalid YAML, config value expansion failure, stale cache.
- validation_or_tests: Auth broker sentinel test covers downstream behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2244 `file` `packages/coding-agent/src/slash-commands/builtin-registry.ts`
- cursor: `[_]`
- core_role: Central registry and executor for built-in slash commands.
- algorithmic_behavior: Helper functions cover status refresh at `packages/coding-agent/src/slash-commands/builtin-registry.ts:66`, workflow monitor snapshot writer at `:77`, workflow progress mapping at `:97`, fast mode status at `:121`, collab link hints at `:140`, fresh session formatting at `:157`, usage reset at `:168`, debug subcommands at `:229`, shake parsing at `:258`, command definitions across the large registry body, completions at `:2221`, inline hints at `:2241`, command defs at `:2282`, public commands at `:2296`, internal specs at `:2323`, executor at `:2332`, and lookup at `:2419`.
- inputs_outputs_state: Inputs are parsed slash commands, runtime/session context, command args, plugin/marketplace/config/session state. Outputs are command results, UI overlays, settings changes, session state updates, collab links, debug reports, and workflow actions.
- gates_or_invariants: Reserved names set prevents collisions; collab guest allowlist gates commands; subcommand parsers return usage/errors; marketplace/plugin operations go through managers; status line refresh after state changes.
- dependencies_and_callers: Used by interactive input slash-command path. Coordinates with auth, settings, plugins, marketplace, collab, workflow, MCP/SSH/Todo helpers, stats dashboard, changelog, and session runtime.
- edge_cases_or_failure_modes: Unsupported subcommands, missing providers/accounts, plugin install/update failures, collab host absent, debug path resolution, workflow snapshot write failure.
- validation_or_tests: `/setup` tests, marketplace tests, workflow inspection tests, and collab tests cover important command paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2274 `file` `packages/coding-agent/src/task/repair-args.ts`
- cursor: `[_]`
- core_role: Repairs double-encoded JSON strings in task tool arguments.
- algorithmic_behavior: `hasDoubleEncodeSignature()` at `packages/coding-agent/src/task/repair-args.ts:43` detects structural escape signatures; `repairDoubleEncodedJsonString()` at `:68` unescapes; `repairTaskItem()` at `:82`; `repairTaskParams()` at `:100` maps top-level and batch task fields.
- inputs_outputs_state: Inputs are `TaskParams`/`TaskItem` with possibly double-encoded prompt/role fields. Outputs are repaired task params.
- gates_or_invariants: Only strings with structural escape signatures are repaired; batch and flat shapes both handled.
- dependencies_and_callers: Used by task tool argument normalization before spawning subagents.
- edge_cases_or_failure_modes: Legitimate escaped strings false-positive, nested batch arrays, partially encoded fields.
- validation_or_tests: Task tool tests likely cover repaired argument cases.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2304 `file` `packages/coding-agent/src/tools/eval-backends.ts`
- cursor: `[_]`
- core_role: Resolves allowed eval backends for a tool session.
- algorithmic_behavior: Interface at `packages/coding-agent/src/tools/eval-backends.ts:4`; `readEvalBackendsAllowance()` at `:10`; `resolveEvalBackends()` at `:21` combines session/settings flags.
- inputs_outputs_state: Inputs are `ToolSession` and flags/env via `$flag`. Output is boolean allowance for JS/Python or other eval backends.
- gates_or_invariants: Backend availability is session-scoped and flag-gated.
- dependencies_and_callers: Used by eval tool registration/execution.
- edge_cases_or_failure_modes: Missing settings/session fields, disabled backend despite tool call.
- validation_or_tests: Eval display and workflow helper tests cover eval behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2334 `file` `packages/coding-agent/src/tools/memory-render.ts`
- cursor: `[_]`
- core_role: TUI renderers for memory tools retain/recall/reflect.
- algorithmic_behavior: `retainContents()` at `packages/coding-agent/src/tools/memory-render.ts:37`; `resultText()` at `:41`; `queryHeader()` at `:46`; `retainComponent()` at `:59`; renderer exports for retain at `:78`, recall at `:111`, and reflect at `:158`.
- inputs_outputs_state: Inputs are tool args/results/details and theme/render options. Outputs are TUI components/status lines with truncated/expanded memory text.
- gates_or_invariants: Output lines use preview limits and truncation; result text is extracted from first text content block; expanded mode shows bounded lines.
- dependencies_and_callers: Used by coding-agent memory tool render registry. Depends on TUI Text, render utils, theme.
- edge_cases_or_failure_modes: Missing result content, long recall body, empty answers, collapsed/expanded render paths.
- validation_or_tests: Component render tests cover adjacent TUI behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2364 `file` `packages/coding-agent/src/tts/tts-protocol.ts`
- cursor: `[_]`
- core_role: Type-level protocol for local TTS worker communication.
- algorithmic_behavior: Defines progress statuses at `packages/coding-agent/src/tts/tts-protocol.ts:3`, file progress state at `:5`, progress events at `:10`, inbound worker messages at `:23`, outbound messages at `:36`, and transport interface at `:57`.
- inputs_outputs_state: Inputs are worker inbound commands such as init/speak/control and model keys. Outputs are progress/audio/error/ready events.
- gates_or_invariants: Message unions constrain worker host protocol and progress event shape.
- dependencies_and_callers: Used by TTS worker/client implementation.
- edge_cases_or_failure_modes: Unknown status/message type guarded by TypeScript consumers.
- validation_or_tests: SDK tool activation tests verify xAI TTS registration gate, not this local protocol directly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2394 `file` `packages/coding-agent/src/utils/lang-from-path.ts`
- cursor: `[_]`
- core_role: File extension/path to language identifier mapping.
- algorithmic_behavior: Static extension maps fill most of file; `themeExtensionKey()` at `packages/coding-agent/src/utils/lang-from-path.ts:191`, `lspExtensionKey()` at `:196`, `getLanguageFromPath()` at `:204`, and `detectLanguageId()` at `:223`.
- inputs_outputs_state: Input is file path. Output is highlight/theme language or LSP language id.
- gates_or_invariants: Extension lookup normalizes case/path; fallback detects by basename/extension.
- dependencies_and_callers: Used by syntax highlighting, diff rendering, LSP, markit/export.
- edge_cases_or_failure_modes: Multi-dot extensions, unknown extension, filenames without extension, theme versus LSP naming differences.
- validation_or_tests: Highlight/diff component tests indirectly cover language mapping.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2424 `file` `packages/coding-agent/src/workflow/model-resolution.ts`
- cursor: `[_]`
- core_role: Resolves model selection for workflow nodes.
- algorithmic_behavior: Public types at `packages/coding-agent/src/workflow/model-resolution.ts:17`; `resolveWorkflowNodeModel()` at `:73`; request selection at `:165`; `modelContextRequest()` at `:193`; default request at `:216`; portable parent override reason at `:224`; pattern resolver at `:236`; parent default at `:258`; unavailable policy at `:265`; audit creation at `:275`.
- inputs_outputs_state: Inputs are workflow definition/node, configured settings, parent/current/agent model overrides, registry, match preferences, and unavailable policy. Outputs are resolved model, source, audit trail, or fallback/fail result.
- gates_or_invariants: Review nodes default to fail policy; agent model override applies only agent nodes; portable parent defaults can be overridden; audits preserve source/reason.
- dependencies_and_callers: Used by workflow runtime/inspection. Depends on catalog model resolution and settings.
- edge_cases_or_failure_modes: Model unavailable, pattern not matched, missing parent active model, conflicting overrides.
- validation_or_tests: Workflow inspection tests summarize model assignments.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2454 `file` `packages/coding-agent/test/core/eval-workflow-helpers.integration.test.ts`
- cursor: `[_]`
- core_role: Integration tests for JS/Python eval workflow helper functions.
- algorithmic_behavior: Tests at `packages/coding-agent/test/core/eval-workflow-helpers.integration.test.ts:22`, `:34`, `:57`, `:72`, `:88`, and `:108` verify `parallel`, concurrency, `pipeline`, exception propagation, `log`/`phase` status events, and `local://` helper root resolution.
- inputs_outputs_state: Inputs are Python/eval snippets and temp roots. Outputs are eval results and status events.
- gates_or_invariants: `parallel` preserves input order while running concurrently; pipeline transforms stage-by-stage; local path helper stays under injected root.
- dependencies_and_callers: Exercises Python kernel executor and eval helper runtime.
- edge_cases_or_failure_modes: Thunk exception propagation, status event capture, local URL path resolution.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2484 `file` `packages/coding-agent/test/debug/raw-sse-pretty.test.ts`
- cursor: `[_]`
- core_role: Tests pretty expansion of raw SSE data lines.
- algorithmic_behavior: Wide object fixture at `packages/coding-agent/test/debug/raw-sse-pretty.test.ts:6`; tests at `:21`, `:42`, `:51`, `:58`, and `:64` verify wide JSON expansion, compact short payloads, fallback on non-JSON/invalid JSON, and preserving non-data lines.
- inputs_outputs_state: Inputs are raw SSE text lines. Outputs are formatted multi-line `data:` entries or original lines.
- gates_or_invariants: Rejoined expanded data remains JSON-equivalent; only wide valid JSON expands.
- dependencies_and_callers: Exercises `expandPrettyDataLines()` in debug raw SSE viewer.
- edge_cases_or_failure_modes: JSON-looking invalid text, comments/events, wide plain strings.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2514 `file` `packages/coding-agent/test/extensibility/ext-model-query.test.ts`
- cursor: `[_]`
- core_role: Tests extension model query API.
- algorithmic_behavior: Model fixture at `packages/coding-agent/test/extensibility/ext-model-query.test.ts:8`; registry fake at `:30`; tests from `:37` verify `list`, lazy `current`, `resolve`, settings-backed role aliases, and `family` grouping/canonical lineage.
- inputs_outputs_state: Inputs are fake registry/settings/current model getter and model strings. Outputs are model lists/current/resolved/family values.
- gates_or_invariants: Current model read is lazy; role aliases use same resolver path as core; family groups releases but separates vendors.
- dependencies_and_callers: Exercises `createExtensionModelQuery()`.
- edge_cases_or_failure_modes: Opaque proxy id family folding, live session model changes.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2544 `file` `packages/coding-agent/test/marketplace/fetcher.test.ts`
- cursor: `[_]`
- core_role: Tests plugin marketplace source classification, catalog parsing, and local fetch behavior.
- algorithmic_behavior: Source classification tests at `packages/coding-agent/test/marketplace/fetcher.test.ts:17`; catalog parse tests at `:75`; fetch tests at `:151`. They cover local path forms, URL/git/GitHub shorthand, bare-name suggestion, schema errors, extra-field preservation, object source, fixture directory resolution, `.omp-plugin` versus `.claude-plugin` precedence, and error paths.
- inputs_outputs_state: Inputs are source strings, JSON catalogs, fixture directories. Outputs are classified source objects and marketplace catalog data/errors.
- gates_or_invariants: Names must pass valid segment rules; missing required fields throw; `.omp-plugin/marketplace.json` preferred over `.claude-plugin`.
- dependencies_and_callers: Exercises marketplace fetcher/parser.
- edge_cases_or_failure_modes: Windows absolute paths, nonexistent relative paths, invalid JSON, neither candidate path exists.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2574 `file` `packages/coding-agent/test/session-manager/save-entry.test.ts`
- cursor: `[_]`
- core_role: Tests custom session entry persistence/traversal.
- algorithmic_behavior: Suite at `packages/coding-agent/test/session-manager/save-entry.test.ts:5`; main test at `:6` saves custom entries and checks tree traversal includes them, with custom entry retrieval at `:43`.
- inputs_outputs_state: Inputs are custom session entries. Outputs are session manager entries/tree traversal.
- gates_or_invariants: Custom entries must persist and participate in traversal, not only raw log storage.
- dependencies_and_callers: Exercises `SessionManager.saveCustomEntry`.
- edge_cases_or_failure_modes: Custom entry omitted from tree, entry type mismatch.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2604 `file` `packages/coding-agent/test/slash-commands/setup.test.ts`
- cursor: `[_]`
- core_role: Tests `/setup` and `/providers` slash command routing.
- algorithmic_behavior: Runtime fixture at `packages/coding-agent/test/slash-commands/setup.test.ts:8`; tests at `:27` verify autocomplete alias, `/setup`, `/setup providers`, `/providers`, unsupported setup scenes, and alias-specific usage.
- inputs_outputs_state: Inputs are slash command strings and fake runtime callbacks. Outputs are provider setup UI calls or usage messages.
- gates_or_invariants: `/providers` is an alias for provider setup; unsupported args do not call setup.
- dependencies_and_callers: Exercises built-in slash command registry/defs.
- edge_cases_or_failure_modes: Alias argument handling, usage text for unsupported scene.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2634 `file` `packages/coding-agent/test/tool-discovery/persistence.test.ts`
- cursor: `[_]`
- core_role: Tests discoverable tool index serialization/search round-trip.
- algorithmic_behavior: Suite at `packages/coding-agent/test/tool-discovery/persistence.test.ts:8` builds/searches a generic index without loss at `:28` and preserves source field in results at `:39`.
- inputs_outputs_state: Inputs are `DiscoverableTool` objects. Outputs are persisted/searchable index entries.
- gates_or_invariants: Tool metadata including source survives serialization/search.
- dependencies_and_callers: Exercises tool index persistence.
- edge_cases_or_failure_modes: Source field loss, search result mismatch.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2664 `file` `packages/coding-agent/test/tools/eval-display-text.test.ts`
- cursor: `[_]`
- core_role: Tests eval tool `display()` surfacing into model-visible content.
- algorithmic_behavior: Session/result fixtures at `packages/coding-agent/test/tools/eval-display-text.test.ts:8` and `:18`; red PNG fixture at `:37`; tests from `:48` cover JSON display text, interleaving stdout/display, image content blocks, downscaling images, no-output marker, and oversized display truncation.
- inputs_outputs_state: Inputs are mocked eval results with stdout/display/images. Outputs are tool result content text and image blocks.
- gates_or_invariants: Displayed images become `ImageContent`, not base64 text; oversize values truncate; no text output is explicit.
- dependencies_and_callers: Exercises `EvalTool`, eval index, Python kernel setting gates.
- edge_cases_or_failure_modes: Large display values, image downscale, no stdout/display.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2694 `file` `packages/coding-agent/test/tools/path-utils-dotdot-selector.test.ts`
- cursor: `[_]`
- core_role: Tests `..` line-range selector alias parsing.
- algorithmic_behavior: Suite at `packages/coding-agent/test/tools/path-utils-dotdot-selector.test.ts:5` verifies `N..M`, open-ended `N..`, comma-separated chunks, mixing separators, inverted range rejection, path/selector splitting, and not confusing `..` path segment with selector.
- inputs_outputs_state: Inputs are path strings and selector chunks. Outputs are parsed ranges or `ToolError`.
- gates_or_invariants: `..` is an inclusive range alias only in selector position; inverted ranges reject with same guard as `-`.
- dependencies_and_callers: Exercises path-utils selectors used by read/edit tools.
- edge_cases_or_failure_modes: Parent directory path segments, mixed separators, trailing open ranges.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2724 `file` `packages/coding-agent/test/tools/web-search-codex.test.ts`
- cursor: `[_]`
- core_role: Tests Codex-backed web search provider model selection and citation extraction.
- algorithmic_behavior: SSE fixtures at `packages/coding-agent/test/tools/web-search-codex.test.ts:14` through `:152`; search param/fetch mocks at `:190` and `:199`; tests from `:226` verify default model selection, blank env fallback, retry on unsupported default for ChatGPT accounts, explicit env model, no retry for explicit unsupported model, markdown/plain URL citations, balanced parentheses, punctuation stripping, streamed text fallback over image placeholder, placeholder error chain, and keeping annotation sources.
- inputs_outputs_state: Inputs are query/env/model/fetch responses. Outputs are search result answer/source list or thrown error to advance chain.
- gates_or_invariants: Explicit env model disables default retry; final image placeholders should not replace useful streamed answer; source extraction works without annotations.
- dependencies_and_callers: Exercises `searchCodex()`.
- edge_cases_or_failure_modes: Unsupported models, placeholder-only responses, markdown URLs with parentheses, plain URL punctuation.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2754 `file` `packages/coding-agent/test/workflow/inspection.test.ts`
- cursor: `[_]`
- core_role: Tests workflow inspection model generation.
- algorithmic_behavior: Host fixture at `packages/coding-agent/test/workflow/inspection.test.ts:48`; graph patch preview at `:60`; tests at `:79`, `:150`, and `:171` verify graph/state/activation/revision/model summaries, omission of legacy active-run graph patch proposals, and lifecycle family lineage/checkpoints/changes/bindings. Helpers `binding()` and `createFreeze()` at `:317`/`:329`.
- inputs_outputs_state: Inputs are workflow definitions, run-store host entries, freezes, bindings. Outputs are inspection summaries.
- gates_or_invariants: Inspection excludes legacy proposal noise; includes model assignments and lifecycle lineage.
- dependencies_and_callers: Exercises workflow definition parser, inspection builders, lifecycle inspection.
- edge_cases_or_failure_modes: Legacy graph patch entries, frozen lifecycle families, model assignment summaries.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2784 `file` `packages/collab-web/src/tool-render/standalone.tsx`
- cursor: `[_]`
- core_role: Standalone web component registration entry for tool render views.
- algorithmic_behavior: Imports `defineToolViewElement` at `packages/collab-web/src/tool-render/standalone.tsx:6` and registers custom element through module side effect.
- inputs_outputs_state: Input is module load in browser. Output is defined tool-view web component.
- gates_or_invariants: Must run once in standalone bundle context.
- dependencies_and_callers: Depends on `./element`; used by collab-web standalone tool renderer.
- edge_cases_or_failure_modes: Duplicate custom element registration handled by underlying element code if implemented.
- validation_or_tests: Tool renderer tests/components indirectly.
- skip_candidate: `yes: entrypoint wiring rather than core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2814 `file` `packages/mnemopi/src/core/synonyms.ts`
- cursor: `[_]`
- core_role: Query synonym expansion and normalization for recall.
- algorithmic_behavior: Synonym groups at `packages/mnemopi/src/core/synonyms.ts:1`, stop words at `:44`, reverse map builder at `:152`, `normalizeQuery()` at `:162`, `expandQuery()` at `:170`, and `getSynonyms()` at `:192`.
- inputs_outputs_state: Input is query or word. Outputs are normalized canonical query, expanded query text, or synonym list.
- gates_or_invariants: Stop words are skipped; reverse map maps variants to canonical group; expansion adds related terms.
- dependencies_and_callers: Used by mnemopi recall/token expansion.
- edge_cases_or_failure_modes: Unknown words, case normalization, stop-word-only query.
- validation_or_tests: Polyphonic recall tests cover synonym-influenced recall paths indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2844 `file` `packages/tui/src/components/box.ts`
- cursor: `[_]`
- core_role: TUI box layout component.
- algorithmic_behavior: `Box` class at `packages/tui/src/components/box.ts:14` wraps child component rendering with padding, optional width/height/background, and caching. Comment at `:91` notes background function output can change without reference changes, affecting cache invalidation.
- inputs_outputs_state: Inputs are child component, dimensions, padding/background options. Outputs are rendered lines with width/padding/background applied and cached.
- gates_or_invariants: Visible width is used for layout; padding/background applied per line; cache must account for render width and dynamic background.
- dependencies_and_callers: Used by TUI components throughout coding-agent.
- edge_cases_or_failure_modes: Dynamic background stale cache, wide characters, child render width changes.
- validation_or_tests: Component render suites indirectly validate box layout.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2874 `file` `python/robomp/web/src/config.ts`
- cursor: `[_]`
- core_role: Browser-side RobOMP web config reader.
- algorithmic_behavior: `readConfig()` at `python/robomp/web/src/config.ts:11` reads window/global config and derives `CONFIG` at `:32`, `AUTH_HEADERS` at `:34`, and `POLL_INTERVAL_MS` at `:38`.
- inputs_outputs_state: Inputs are injected web config values. Outputs are typed config, auth headers, and polling interval.
- gates_or_invariants: Replay auth header emitted only when replay enabled/configured.
- dependencies_and_callers: Used by RobOMP web frontend API polling.
- edge_cases_or_failure_modes: Missing injected config, replay disabled, token absent.
- validation_or_tests: No direct test assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2904 `file` `crates/pi-shell/src/minimizer/filters/docker.rs`
- cursor: `[_]`
- core_role: Output minimizer for Docker/Kubernetes/Helm command output.
- algorithmic_behavior: `supports()` at `crates/pi-shell/src/minimizer/filters/docker.rs:10`; `filter()` at `:41`; Docker/Kubectl/Helm routes at `:57`, `:95`, `:444`. It detects structured kubectl output at `:135`, explicit JSON/YAML flags at `:148`, non-table formats at `:192`, compacts pod/service JSON at `:261`/`:288`/`:359`, strips Helm noise at `:457`, detects compose options/log/list/lifecycle/up commands at `:509` through `:650`, compacts tables/logs/build progress at `:692`, `:728`, `:754`, and dedupes head/tail at `:811`.
- inputs_outputs_state: Inputs are command context, raw stdout/stderr text, and exit code. Outputs are minimized text preserving salient rows/errors.
- gates_or_invariants: Structured JSON/YAML explicitly requested is not over-compacted unless safe; logs are deduped; lifecycle/progress/listing commands have distinct policies.
- dependencies_and_callers: Used by shell minimizer pipeline in `pi-shell`.
- edge_cases_or_failure_modes: Compose option parsing, kubectl table versus JSON, glog prefixes, repeated blank lines, forbidden/error messages, long logs.
- validation_or_tests: Extensive unit tests from `:815` through `:1667` cover command variants and compaction cases.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2934 `file` `packages/ai/src/registry/oauth/google-oauth-shared.ts`
- cursor: `[_]`
- core_role: Shared Google OAuth callback flow implementation.
- algorithmic_behavior: `getUserEmail()` at `packages/ai/src/registry/oauth/google-oauth-shared.ts:22` fetches user info; `GoogleOAuthFlow` class at `:38` extends callback server flow; `runGoogleOAuthLogin()` at `:116` drives login.
- inputs_outputs_state: Inputs are OAuth flow config, callback request, code/token responses, fetch implementation. Outputs are `OAuthCredentials` with optional email/user metadata.
- gates_or_invariants: Validation-required URLs are detected/formatted; token exchange/userinfo errors surface through callbacks; flow uses configured scopes/client.
- dependencies_and_callers: Used by Google/Gemini OAuth providers. Depends on `OAuthCallbackFlow`, google validation utils.
- edge_cases_or_failure_modes: Validation required response, missing email, token exchange failure, callback timeout.
- validation_or_tests: OAuth tests for specific providers; Google shared flow indirectly covered.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2964 `file` `packages/coding-agent/src/advisor/__tests__/advisor.test.ts`
- cursor: `[_]`
- core_role: Comprehensive tests for advisor side-agent behavior, delivery, telemetry, queueing, and UI cards.
- algorithmic_behavior: Tests cover history formatting at `packages/coding-agent/src/advisor/__tests__/advisor.test.ts:23`, yield queue at `:49`, AdviseTool schema/callback at `:137`, delivery policy at `:158`, telemetry derivation at `:222`, runtime prompt/coalescing/context maintenance/backlog/reset/failure handling from `:253`, read-only tool allowlist at `:747`, message card rendering at `:758`, and delivery channel routing at `:821`.
- inputs_outputs_state: Inputs are agent messages, advisor notes/severity, runtime host, telemetry config, queue state, UI theme. Outputs are custom advisor messages, prompt batches, backlog/catchup state, rendered cards, and delivery decisions.
- gates_or_invariants: Concern/blocker can interrupt; nits queue; interrupt-immune turns suppress; backlog drops after repeated failures; advisor tools are read-only allowlist.
- dependencies_and_callers: Exercises advisor runtime/tool, session history formatter, yield queue, advisor UI component.
- edge_cases_or_failure_modes: Context maintenance failure, reset aborts in-flight prompt, catch-up wait cancellation, suppressed/idle delivery preservation.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2994 `file` `packages/coding-agent/src/commit/analysis/validation.ts`
- cursor: `[_]`
- core_role: Validates conventional commit analysis fields.
- algorithmic_behavior: `validateSummary()` at `packages/coding-agent/src/commit/analysis/validation.ts:8` enforces non-empty/max length; `validateScope()` at `:25` splits slash scopes and enforces segment regex at `:40`; `validateAnalysis()` at `:47` composes full validation.
- inputs_outputs_state: Inputs are generated summary/scope/analysis. Outputs are `ValidationResult` success/errors.
- gates_or_invariants: Scope segments must start alnum and contain lowercase alnum/hyphen/underscore; summary max length enforced.
- dependencies_and_callers: Used by commit analysis/generation flow.
- edge_cases_or_failure_modes: Empty summary, overly long summary, null scope, multi-segment invalid scope.
- validation_or_tests: Commit analysis tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3024 `file` `packages/coding-agent/src/eval/__tests__/js-context-manager.test.ts`
- cursor: `[_]`
- core_role: Tests JavaScript eval worker lifecycle and shutdown behavior.
- algorithmic_behavior: Session fixture at `packages/coding-agent/src/eval/__tests__/js-context-manager.test.ts:21`; timeout helper at `:42`; real worker exit wait at `:56`; fake worker at `:92`; suite at `:182` tests graceful close with refed user handles, reset waits for close, termination after close ack without exit, force-terminate on aborted in-flight run, and inline fallback when spawned worker startup errors.
- inputs_outputs_state: Inputs are eval sessions, fake/real workers, close/abort messages. Outputs are worker lifecycle events and process cleanup.
- gates_or_invariants: Reset should prefer graceful close when no in-flight abort; aborted run force-terminates; startup error falls back inline.
- dependencies_and_callers: Exercises JS context manager and executor.
- edge_cases_or_failure_modes: Worker acknowledges close but stays alive, refed handles, spawn startup error, aborted run.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3054 `file` `packages/coding-agent/src/extensibility/extensions/compact-handler.ts`
- cursor: `[_]`
- core_role: Extension API adapters for compact and model-set operations.
- algorithmic_behavior: `runExtensionCompact()` at `packages/coding-agent/src/extensibility/extensions/compact-handler.ts:15` calls session compaction if available; `runExtensionSetModel()` at `:35` sets session model if supported.
- inputs_outputs_state: Inputs are compact options or model. Outputs are boolean/successful session operations.
- gates_or_invariants: Operation only runs if session exposes capability method.
- dependencies_and_callers: Used by extension runtime APIs.
- edge_cases_or_failure_modes: Extension calls compact/setModel on incompatible session; model rejected by session.
- validation_or_tests: Ext model query tests cover related extension model APIs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3084 `file` `packages/coding-agent/src/markit/converters/epub.ts`
- cursor: `[_]`
- core_role: EPUB-to-Markdown converter for markit.
- algorithmic_behavior: `EpubConverter` at `packages/coding-agent/src/markit/converters/epub.ts:45`; MIME support at `:50`; conversion reads container/rootfile, parses OPF manifest/spine, extracts ordered XHTML, normalizes tables, and converts via Turndown. Spine order mapping at `:93`.
- inputs_outputs_state: Inputs are EPUB buffer/stream info. Outputs are `ConversionResult` markdown and metadata.
- gates_or_invariants: Only EPUB MIME/extensions supported; OPF manifest/spine must resolve content files; tables normalized before markdown conversion.
- dependencies_and_callers: Depends on `fast-xml-parser`, zip utilities, Turndown helpers, markit converter interface.
- edge_cases_or_failure_modes: Missing container/rootfile, absent spine item, malformed XML, missing manifest href, encrypted/unsupported EPUB content.
- validation_or_tests: Markit converter tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3114 `file` `packages/coding-agent/src/modes/components/diff.ts`
- cursor: `[_]`
- core_role: TUI diff renderer with intraline highlights, line numbers, indentation visualization, and syntax context.
- algorithmic_behavior: `visualizeIndent()` at `packages/coding-agent/src/modes/components/diff.ts:16`; `parseDiffLine()` at `:40`; `renderIntraLineDiff()` at `:55`; `renderDiff()` at `:108`; context line highlighting at `:242`.
- inputs_outputs_state: Input is unified/compact diff text plus render options. Output is ANSI/TUI formatted diff string.
- gates_or_invariants: Sanitizes text before rendering; parses prefixes/line numbers; highlights additions/removals/context differently; optional language highlighting by path.
- dependencies_and_callers: Uses `diff`, `sanitizeText`, theme/highlight, render-utils.
- edge_cases_or_failure_modes: Tabs/indent visualization, malformed diff lines, no newline, wide content, intraline changes.
- validation_or_tests: Hashline diff preview and component tests cover adjacent rendering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3144 `file` `packages/coding-agent/src/modes/components/session-selector.ts`
- cursor: `[_]`
- core_role: Interactive session history selector and search ranking UI.
- algorithmic_behavior: Status formatting at `packages/coding-agent/src/modes/components/session-selector.ts:29`; search text/tokenize/rank at `:49`, `:61`, `:80`; ranking merge at `:132`; `SessionList` component at `:161`; `SessionSelectorComponent` at `:469`.
- inputs_outputs_state: Inputs are session list, query string, history matcher, key events, selection state. Outputs are rendered list, selected session path, exit callbacks.
- gates_or_invariants: Recency ranking, fuzzy/history merge, viewport scrolling, interrupt/select key handling, path shortening.
- dependencies_and_callers: Used by selector controller and session resume UI. Depends on TUI, theme, keybinding matchers, session listing.
- edge_cases_or_failure_modes: Empty sessions, metadata-only/history-only matches, session path no longer present, viewport scrollbar.
- validation_or_tests: Session selector tests in modes/components directory validate viewport/status/scope/scrollbar behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3174 `file` `packages/coding-agent/src/modes/controllers/selector-controller.ts`
- cursor: `[_]`
- core_role: Orchestrates interactive overlays/selectors for settings, models, sessions, plugins, auth, copy, trees, and transcripts.
- algorithmic_behavior: `SelectorController` at `packages/coding-agent/src/modes/controllers/selector-controller.ts:74`; overlay completion callbacks start at `:92`/`:110`; plugin installed mapping at `:534`; history matcher at `:819`; OAuth provider selection at `:1064`; reset usage redemption at `:1194`; transcript renderer extension hook at `:1254`.
- inputs_outputs_state: Inputs are interactive context, settings, providers, plugin roots, session observer registry, session manager/storage, key selections. Outputs are overlays, settings mutations, provider enable/disable, session switches, logout/reset flows, copied content, and rendered transcript blocks.
- gates_or_invariants: Overlays close through handles/done callbacks; provider/plugin operations update caches; session selection uses history matching; reset/logout account lists are derived safely.
- dependencies_and_callers: Central UI controller used by interactive mode slash/menu actions.
- edge_cases_or_failure_modes: Provider not found, plugin registry path changes, session load failure, OAuth/login failure, reset redemption failure, overlay focus cleanup.
- validation_or_tests: Event controller and component tests cover many downstream interactions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3204 `file` `packages/coding-agent/src/slash-commands/helpers/marketplace-manager.ts`
- cursor: `[_]`
- core_role: Helper to construct marketplace manager with project registry context.
- algorithmic_behavior: `createMarketplaceManager()` at `packages/coding-agent/src/slash-commands/helpers/marketplace-manager.ts:16` resolves project registry path, clears plugin root caches as needed, and returns a `MarketplaceManager`.
- inputs_outputs_state: Input is slash command runtime. Output is marketplace manager bound to runtime/project.
- gates_or_invariants: Uses default project registry path resolution, not ad hoc path.
- dependencies_and_callers: Called by builtin slash registry marketplace commands.
- edge_cases_or_failure_modes: Registry path resolution failure, stale plugin cache.
- validation_or_tests: Marketplace fetcher tests cover parser/fetcher, not this helper directly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3234 `file` `packages/coding-agent/src/web/scrapers/coingecko.ts`
- cursor: `[_]`
- core_role: Special web scraper for CoinGecko pages/API rendering.
- algorithmic_behavior: `handleCoinGecko` at `packages/coding-agent/src/web/scrapers/coingecko.ts:33` recognizes CoinGecko URLs, loads/parses JSON/page data, builds formatted result, and `formatPrice()` at `:171` formats numeric prices.
- inputs_outputs_state: Inputs are URL, fetch/load helpers, CoinGecko response JSON. Outputs are `RenderResult` with coin price/market data text.
- gates_or_invariants: Nonmatching URLs return null; parsed numbers/dates formatted; invalid/missing response falls back/errors through handler contract.
- dependencies_and_callers: Used by web scraper dispatcher. Depends on `tryParseJson`, scraper `types` helpers.
- edge_cases_or_failure_modes: Missing price fields, malformed JSON, non-CoinGecko URL, fetch failure.
- validation_or_tests: Web scraper standards tests cover other scrapers; CoinGecko likely has adjacent tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3264 `file` `packages/coding-agent/src/web/scrapers/nuget.ts`
- cursor: `[_]`
- core_role: Special web scraper for NuGet package metadata.
- algorithmic_behavior: Type interfaces at `packages/coding-agent/src/web/scrapers/nuget.ts:5`; `handleNuGet` at `:41` parses NuGet package URLs, loads registration index/pages/items, chooses target entry, formats versions/published/dependencies. Dependency existence check at `:153`.
- inputs_outputs_state: Inputs are NuGet URL and registration JSON. Outputs are formatted package metadata `RenderResult`.
- gates_or_invariants: Nonmatching URLs return null; package id/version resolved from path; dependency groups optional; date/number formatting centralized.
- dependencies_and_callers: Used by web scraper dispatcher. Depends on `tryParseJson`, `loadPage`, and format helpers.
- edge_cases_or_failure_modes: Nested registration pages, missing version, no dependencies, malformed JSON, non-NuGet URL.
- validation_or_tests: Web scraper standards tests cover scraper dispatcher style; NuGet direct tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3294 `file` `packages/coding-agent/src/web/scrapers/utils.ts`
- cursor: `[_]`
- core_role: Shared scraper utilities for type guards, bounded binary fetch, and markit conversion.
- algorithmic_behavior: Basic guards at `packages/coding-agent/src/web/scrapers/utils.ts:9`, `:13`, `:19`; `readResponseWithLimit()` at `:31` streams response body with byte cap/abort; `fetchBinary()` at `:66` applies timeout and status handling; `convertWithMarkit()` at `:101` converts binary buffers.
- inputs_outputs_state: Inputs are URLs/responses/buffers/extensions/abort signals. Outputs are binary fetch success/failure or converted markdown.
- gates_or_invariants: `MAX_BYTES` cap enforced while streaming; timeout aborts request; non-OK responses return failure; markit conversion receives separate signal.
- dependencies_and_callers: Used by specialized web scrapers. Depends on `ToolAbortError`, markit conversion, scraper constants.
- edge_cases_or_failure_modes: Oversized response, no body, timeout, abort, conversion failure.
- validation_or_tests: Web scraper tests indirectly cover utilities.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3324 `file` `packages/coding-agent/test/modes/components/plan-review-overlay.test.ts`
- cursor: `[_]`
- core_role: Exhaustive interaction/render tests for plan review overlay.
- algorithmic_behavior: Render helper at `packages/coding-agent/test/modes/components/plan-review-overlay.test.ts:20`; suite at `:31`; tests cover rendering, Enter/up/down/cancel, slider left/right, external editor, long-plan scroll, content swap, no per-line ellipsis, ToC focus/tab, Down flow, one-line body scroll, section jump, delete/undo, annotate/refine, editor cancel, mouse click, deleted-section feedback, Shift-scroll, hover painting, and disabled hover.
- inputs_outputs_state: Inputs are plan content, options, keyboard/mouse events, editor callbacks. Outputs are rendered overlay, selected options, feedback events, annotations/deleted sections.
- gates_or_invariants: Disabled options skipped; body scroll exact; ToC omits single title heading; hover cannot target disabled option; annotations persist/cancel correctly.
- dependencies_and_callers: Exercises `PlanReviewOverlay`, keybindings, theme, hook selector slider.
- edge_cases_or_failure_modes: Very long body, focus region transitions, external editor null result, mouse row/column mapping.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3354 `file` `packages/coding-agent/test/modes/controllers/event-controller-superseded-agent-end.test.ts`
- cursor: `[_]`
- core_role: Regression tests for stale `agent_end` events in event controller.
- algorithmic_behavior: Context fixture at `packages/coding-agent/test/modes/controllers/event-controller-superseded-agent-end.test.ts:14`; suite at `:54`; tests at `:71` and `:95` verify stale agent_end after resumed turn start does not stop loader, while live turn final end tears loader down.
- inputs_outputs_state: Inputs are synthetic `AgentSessionEvent`s and TUI context. Outputs are loader visibility/state.
- gates_or_invariants: Agent end events are matched to live turn identity; superseded old events ignored.
- dependencies_and_callers: Exercises `EventController`.
- edge_cases_or_failure_modes: Race between resumed `agent_start` and stale previous `agent_end`.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3384 `file` `packages/coding-agent/test/tools/web-scrapers/standards.test.ts`
- cursor: `[_]`
- core_role: Tests standard documentation scrapers for RFC, cheat.sh, and tldr.
- algorithmic_behavior: Tests at `packages/coding-agent/test/tools/web-scrapers/standards.test.ts:9` through `:110` cover nonmatching URLs, RFC URL variants, cheat.sh/cht.sh topics, empty topic, tldr nested path rejection, tldr page fetch, and tldr alias.
- inputs_outputs_state: Inputs are URLs and mocked/real fetch handler behavior. Outputs are scraper result or null.
- gates_or_invariants: Scrapers must be domain/path selective; nested invalid tldr paths rejected; aliases normalized.
- dependencies_and_callers: Exercises `handleRfc`, `handleCheatSh`, `handleTldr`.
- edge_cases_or_failure_modes: Historical RFC domains, empty cheat topic, nested tldr paths.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3414 `file` `packages/collab-web/src/tool-render/tools/find.tsx`
- cursor: `[_]`
- core_role: Collab web renderer for `find` tool calls/results.
- algorithmic_behavior: `joinedGlobs()` at `packages/collab-web/src/tool-render/tools/find.tsx:8`; `Summary()` at `:14`; `Body()` at `:20`; `findRenderer` export at `:66`.
- inputs_outputs_state: Inputs are tool args/result details. Outputs are React nodes with badges, invalid-arg notes, result text, shortened/truncated paths/globs.
- gates_or_invariants: Non-string/invalid args render `InvalidArg`; paths are shortened/truncated; result text displayed through shared parts.
- dependencies_and_callers: Used by collab-web tool-render registry.
- edge_cases_or_failure_modes: Missing paths, array versus scalar globs, large result text.
- validation_or_tests: Web renderer tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3444 `file` `packages/mnemopi/src/core/extraction/client.ts`
- cursor: `[_]`
- core_role: LLM-backed structured fact extraction client.
- algorithmic_behavior: Defaults at `packages/mnemopi/src/core/extraction/client.ts:6`; fallback models at `:11`; `sleep()` at `:38`; auth header at `:44`; `ExtractionClient` at `:52`; `extractFacts()` at `:133`; alias method at `:184`.
- inputs_outputs_state: Inputs are chat messages, API key/base URL/model/fallback config, fetch implementation. Outputs are `ExtractedFact[]` with subject/predicate/object/timestamp/source/confidence.
- gates_or_invariants: Auth header required for API calls; fallback model list used on recoverable failures; response must parse to fact JSON.
- dependencies_and_callers: Used by mnemopi extraction pipeline and background fact extraction in Beam store.
- edge_cases_or_failure_modes: Rate limits/API errors, malformed JSON, empty extraction, fallback exhaustion.
- validation_or_tests: Fact concurrency tests cover storage after extraction; extraction client direct tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3474 `file` `packages/stats/src/client/ui/EmptyState.tsx`
- cursor: `[_]`
- core_role: Small presentational empty-state component for stats UI.
- algorithmic_behavior: `EmptyState` at `packages/stats/src/client/ui/EmptyState.tsx:9` renders a Lucide icon and message with optional className.
- inputs_outputs_state: Inputs are message, icon component, className. Output is React empty-state node.
- gates_or_invariants: Defaults to `Inbox` icon and "No data available".
- dependencies_and_callers: Used by stats dashboard UI.
- edge_cases_or_failure_modes: None significant beyond missing icon/message.
- validation_or_tests: UI smoke/build validates compilation.
- skip_candidate: `yes: presentational component with no core algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3504 `file` `packages/ai/src/registry/oauth/__tests__/xai-oauth.test.ts`
- cursor: `[_]`
- core_role: Tests xAI OAuth token expiry, endpoint validation, refresh, and token exchange.
- algorithmic_behavior: JWT helper at `packages/ai/src/registry/oauth/__tests__/xai-oauth.test.ts:8`; tests at `:14` cover exp parsing; endpoint validation at `:34`; refresh token guard at `:53`; flow redirect port at `:66`; token exchange missing access token at `:74`.
- inputs_outputs_state: Inputs are JWT strings, endpoint URLs, refresh token/fetch responses, OAuth flow config. Outputs are boolean expiry, validation success/error, refreshed credentials or thrown errors.
- gates_or_invariants: Non-HTTPS/non-xAI endpoints rejected; empty refresh token rejects before network; redirect URI pinned to allowlisted loopback port.
- dependencies_and_callers: Exercises `xai-oauth` registry flow.
- edge_cases_or_failure_modes: Empty/non-JWT token, expired token, missing access_token response, invalid endpoint host.
- validation_or_tests: Test file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3534 `file` `packages/coding-agent/src/markit/converters/pdf/grid.ts`
- cursor: `[_]`
- core_role: PDF table grid reconstruction algorithm from text boxes and line segments.
- algorithmic_behavior: Ray casting at `packages/coding-agent/src/markit/converters/pdf/grid.ts:39`; line grouping via `splitYLinesIntoGroups()` at `:138`; row cluster expansion at `:195`; cross-column text splitting at `:293`; cell building at `:387`; bordered table grid construction at `:397`; inferred hline-only tables at `:537`; pruning empty rows/cols at `:643`; diagram rejection at `:683`; public `resolveTableGrids()` at `:710`.
- inputs_outputs_state: Inputs are page number, `TextBox[]`, and PDF vector `Segment[]`. Outputs are table grids plus consumed text box IDs.
- gates_or_invariants: Axis epsilon separates vertical/horizontal segments; bridging vertical lines split row groups; diagrams are filtered; empty rows/columns pruned; cross-column boxes split by x-lines.
- dependencies_and_callers: Used by PDF markit converter table extraction.
- edge_cases_or_failure_modes: Sparse horizontal-only tables, multi-line cells, diagrams mistaken for tables, merged cells, imprecise PDF coordinates, text spanning columns.
- validation_or_tests: PDF converter tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3564 `file` `packages/coding-agent/src/tools/browser/cmux/rpc.ts`
- cursor: `[_]`
- core_role: RPC conversion helpers for cmux browser backend.
- algorithmic_behavior: Interfaces define cmux split/snapshot/eval/url/screenshot/geometry at `packages/coding-agent/src/tools/browser/cmux/rpc.ts:3` through `:62`; `GEOMETRY_SCRIPT` at `:72`; `cmuxSnapshotToObservation()` at `:75`; `serializeEval()` at `:116`; `mapWaitUntil()` at `:123`; cmux enable/kind resolution at `:129` and `:139`.
- inputs_outputs_state: Inputs are cmux snapshot pages/refs, eval function/args, waitUntil strings, env/settings/app options. Outputs are browser `Observation` entries, serialized JS, cmux kind selection.
- gates_or_invariants: Wait states map to cmux accepted `interactive|complete`; env override can force/disable cmux; snapshot refs convert to observation tree consistently.
- dependencies_and_callers: Used by browser tool cmux backend.
- edge_cases_or_failure_modes: Unsupported waitUntil, env override conflicts, missing cmux socket, non-serializable eval args.
- validation_or_tests: Browser tool tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3594 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/sequence.ts`
- cursor: `[_]`
- core_role: Vendored Mermaid sequence diagram to ASCII renderer.
- algorithmic_behavior: `classifyBoxChar()` at `packages/utils/src/vendor/mermaid-ascii/ascii/sequence.ts:20`; `renderSequenceAscii()` at `:30` parses diagram text, computes actor box widths/heights at `:57`/`:60`, lays out messages/notes/loops/blocks on canvas, and helper drawing functions start at `:214`, `:226`, `:241`. Block border rendering appears around `:388`.
- inputs_outputs_state: Inputs are Mermaid sequence text, ASCII config, color mode/theme. Outputs are rendered ASCII string with role/color metadata applied.
- gates_or_invariants: Lines/comments trimmed; display width handles wide text; actor spacing and block extents expand canvas; box chars classified for color roles.
- dependencies_and_callers: Used by markdown/assistant message Mermaid rendering through utils vendor path.
- edge_cases_or_failure_modes: Multiline labels, wide characters, nested blocks/notes, dashed arrows, canvas growth.
- validation_or_tests: Assistant-message Mermaid component tests in modes/components cover rendering integration.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `120 unique item sections`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`