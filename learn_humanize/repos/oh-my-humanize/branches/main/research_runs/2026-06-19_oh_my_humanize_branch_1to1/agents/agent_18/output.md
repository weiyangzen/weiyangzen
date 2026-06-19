# agent_18 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-018 `file` `tsconfig.tools.json`
- cursor: `[_]`
- core_role: Tooling TypeScript project config for repository scripts.
- algorithmic_behavior: Extends `tsconfig.base.json`, enables composite/no-emit checking, allows `.ts` extension imports, and scopes checking to `scripts` plus native package generation.
- inputs_outputs_state: Inputs are TypeScript script files and base compiler options; output is type-check diagnostics only, no emitted JS/declarations.
- gates_or_invariants: `noEmit: true`, `emitDeclarationOnly: false`, `exclude: ["node_modules"]`.
- dependencies_and_callers: Used by `bun check`/tooling project references.
- edge_cases_or_failure_modes: Mis-scoped include can silently skip tool scripts; base config changes affect this config.
- validation_or_tests: Validated by TypeScript project checking, not a runtime test.
- skip_candidate: `yes: configuration-only, but it gates script/tooling algorithms`

### OH_MY_HUMANIZE_MAIN-HZ-048 `file` `docs/custom-tools.md`
- cursor: `[_]`
- core_role: Runtime contract for custom model-callable tools.
- algorithmic_behavior: Defines discovery, module factory contract, execution flow, schema validation, rendering hooks, session events, and cancellation semantics.
- inputs_outputs_state: Inputs are configured tool paths, SDK `customTools`, factory exports, Zod/TypeBox schemas, tool params, abort signals; outputs are registered `AgentTool` adapters, streamed updates, final content/details, and lifecycle callbacks.
- gates_or_invariants: Tool names globally unique; `.md`/`.json` metadata is not executable; relative paths resolve from `cwd`; loader starts no-op UI until `setUIContext`.
- dependencies_and_callers: References `CustomToolAdapter`, `discoverAndLoadCustomTools`, loader providers, SDK bootstrap, extension wrappers, and renderers.
- edge_cases_or_failure_modes: Duplicate names rejected; renderer failures are logged and fall back; `onSession` errors are warnings; aborted subprocess work must receive `signal`.
- validation_or_tests: Covered by custom tool/extension runner tests and loader contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-078 `file` `docs/tui.md`
- cursor: `[_]`
- core_role: TUI integration contract for extensions/custom tools/custom renderers.
- algorithmic_behavior: Specifies component render/input/focus lifecycle, overlay mounting, custom UI promise completion, cursor markers, keybinding matching, terminal-safe rendering, and renderer partial-state options.
- inputs_outputs_state: Inputs are `Component.render(width)`, raw key bytes, theme/keybindings, `done(result)`, renderer args/results; outputs are immutable render line arrays, mounted overlays/editor replacements, focused components, and resolved UI promises.
- gates_or_invariants: Components should return same array reference when unchanged; lines must be width-safe; external content sanitized/truncated; `done` called exactly once; `dispose` needed for owned resources.
- dependencies_and_callers: `packages/tui/src/tui.ts`, `utils.ts`, keybinding modules, `extension-ui-controller.ts`, `ToolExecutionComponent`, custom tool/extension/hook types.
- edge_cases_or_failure_modes: RPC/headless `custom()` unsupported; key releases ignored unless `wantsKeyRelease`; overlay must be hidden on completion; renderers must handle partial results.
- validation_or_tests: TUI, selector navigation, copy selector, and renderer tests exercise these contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-108 `file` `scripts/rate-edit-tool.py`
- cursor: `[_]`
- core_role: Evaluation harness for rating edit-tool behavior across models.
- algorithmic_behavior: Builds TypeScript/Rust/Python fixtures, materializes isolated workspaces, runs OMP model sessions, records streaming/progress/tool usage, collects model outputs, and performs oracle review aggregation.
- inputs_outputs_state: Inputs include CLI args, OMP binary, model list, fixture sources, API keys/results dirs; outputs include per-model result records, progress displays, combined reviews, and oracle review artifacts.
- gates_or_invariants: `TOOL_WHITELIST = ("read", "edit")`; workspace/reference fixtures are synchronized; progress formatting caps widths/snippets; model labels/status/token counters normalized.
- dependencies_and_callers: Uses `argparse`, `asyncio`, subprocess OMP invocations, dataclasses `ModelResult`/`ModelProgress`, `ModelRunRecorder`, and oracle review functions.
- edge_cases_or_failure_modes: Missing OMP binary, model failures/timeouts, malformed notifications, absent keys, workspace materialization errors, and oracle review failures.
- validation_or_tests: Self-validates via fixture diff/review output; no repo unit test found for this script.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-138 `directory` `packages/hashline/bench`
- cursor: `[_]`
- core_role: Benchmark directory for hashline recovery hot paths.
- algorithmic_behavior: `recovery-session-chain.ts` seeds snapshot chains, builds anchor patches, forces accept/reject replay regimes, checks recovery warnings/null results, then times `Recovery.tryRecover`.
- inputs_outputs_state: Inputs are synthetic file sizes, anchor counts, rewritten line positions, `HASHLINE_BENCH_ITERATIONS`; outputs are timing rows and sanity counts.
- gates_or_invariants: Accept cases must include `RECOVERY_SESSION_REPLAY_WARNING`; reject cases must return `null`; warmup runs before timing.
- dependencies_and_callers: Imports `InMemorySnapshotStore`, `parsePatch`, `Recovery` from `../src`; run manually as a Bun bench/probe.
- edge_cases_or_failure_modes: If fixture no longer forces three-way failure, benchmark aborts because it would measure the wrong path.
- validation_or_tests: Built-in sanity checks before timing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-168 `directory` `python/robomp/web`
- cursor: `[_]`
- core_role: Solid/Vite dashboard served by robomp FastAPI.
- algorithmic_behavior: Polls `/api/status` and `/api/logs`, renders runtime status, issue/event queues, running work, logs, stats, browse/search, trigger/retry/cancel actions, and syncs Vite output into server static assets.
- inputs_outputs_state: Inputs are server-injected config, API JSON, user filters/forms; outputs are reactive UI state, trigger/cancel POSTs, issue retry commands, and static bundle files.
- gates_or_invariants: `AUTH_HEADERS` only when replay enabled; polling interval fixed at 3000 ms; browse filters processed/hidden issues; Vite preserves `.gitkeep` and copies bundle to `src/static`.
- dependencies_and_callers: Solid `createResource`/signals, `api.ts`, `state.ts`, components `Browse`, `Events`, `Issues`, `Working`, `Logs`, `Stats`, `Trigger`, FastAPI static mount.
- edge_cases_or_failure_modes: API errors converted to `ApiError`; stale cache metadata displayed; cancel/trigger failures update shared trigger status; malformed config falls back to current origin.
- validation_or_tests: No direct web tests in assigned set; backend GitHub tests cover adjacent robomp API behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-198 `file` `docs/tools/resolve.md`
- cursor: `[_]`
- core_role: Resolve tool runtime contract for pending actions.
- algorithmic_behavior: Documents queued/standing resolve handlers, forced tool-choice queueing, apply/discard flow, requeue-on-apply-failure, metadata wrapping, hidden tool behavior, and abort handling.
- inputs_outputs_state: Inputs are `action`, `reason`, optional `extra`, current queued/standing handler; outputs are callback results with `details` augmented by action/reason/source metadata or default discard payload.
- gates_or_invariants: `apply` without pending action errors; `discard` without pending action succeeds; queued rejection returns `requeue`; `resolve` is hidden and added separately from normal tool filtering.
- dependencies_and_callers: `tools/resolve.ts`, custom pending actions, `agent-session` tool-choice queue, `ast-edit`, custom tool loader.
- edge_cases_or_failure_modes: Apply callback errors preserve/requeue pending action; non-`ToolError` apply failures wrap as `ToolError`; reject errors propagate.
- validation_or_tests: Resolve/plan approval behavior is exercised through event-controller and ACP/slash command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-228 `directory` `packages/agent/src/compaction`
- cursor: `[_]`
- core_role: Agent context compaction, branch summarization, pruning, shake, and remote-compaction subsystem.
- algorithmic_behavior: Calculates context thresholds, finds valid cut points, prepares summarization windows, generates/update summaries/handoffs, prunes superseded/useless tool results, shakes heavy regions, serializes conversations, and optionally delegates to OpenAI/generic remote compaction.
- inputs_outputs_state: Inputs are session entries, model/api key, context-window settings, previous compaction data, prompts, tool history, abort signal; outputs are `CompactionResult`, branch summaries, custom compaction messages, pruned/shaken in-memory entries, and preserve data.
- gates_or_invariants: Compaction disabled/off/contextWindow<=0 short-circuits; reserve is max configured or 15%; cut points avoid invalid tool-result splits; protected tools/skill reads are not pruned/shaken; remote timeout is 180s.
- dependencies_and_callers: `agent-session` calls `prepareCompaction`/`compact`; uses `instrumentedCompleteSimple`, tokenizer, OpenAI response history helpers, prompt markdown, and `snapcompact`.
- edge_cases_or_failure_modes: Last entry already compacted returns undefined; missing first-kept ID implies migration needed; failed remote compaction falls back; stale read selectors are superseded by bare-path reads.
- validation_or_tests: Compaction, snapcompact journal, branch/session, event-controller, and provider-stream tests cover visible contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-258 `directory` `packages/coding-agent/src/edit`
- cursor: `[_]`
- core_role: Main edit tool implementation for replace/patch/apply-patch/hashline/notebook/diff/rendering.
- algorithmic_behavior: Validates edit mode schemas, resolves plan-mode paths, reads/normalizes content, applies fuzzy/exact replacements or patch hunks, recovers hashline anchors, writes via LSP/deferred diagnostics, records snapshots/seen lines, renders previews/results, and streams partial diffs.
- inputs_outputs_state: Inputs are tool params, session settings, filesystem state, snapshots, LSP batch requests, abort signals; outputs are file writes, diffs, diagnostics, snapshot records, preview components, and tool result metadata.
- gates_or_invariants: Plan-mode write guard; `old_text` non-empty; no-op edits throw; duplicate/ambiguous matches error; BOM/line endings preserved; notebook cells validated; snapshot max bytes 4 MiB.
- dependencies_and_callers: `EditTool`, `HashlineFilesystem`, `@oh-my-pi/hashline`, `pi-natives` block resolver, LSP writethrough, render-utils, TUI renderer.
- edge_cases_or_failure_modes: Fuzzy thresholds, indentation/tab conversion, partial patch parsing, CRLF/BOM restoration, notebook marker escaping, stale snapshot recovery, and no-op loop guard.
- validation_or_tests: Conflict integration, LSP regressions, streaming preview, write preview expand, and edit-related tool tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-288 `directory` `packages/coding-agent/src/tui`
- cursor: `[_]`
- core_role: Coding-agent-specific TUI rendering primitives.
- algorithmic_behavior: Provides code/markdown cells, output blocks, file/tree lists, hyperlinks, status lines, width-aware text, padding/truncation/hash caching, and framed-block helpers.
- inputs_outputs_state: Inputs are theme, width, state/status, file entries, text blocks, image protocol info; outputs are terminal-safe render line arrays/components and OSC8 hyperlinks.
- gates_or_invariants: Uses visible-width measurement, tab replacement, truncation, stable caches via `Hasher`, and file/internal URL safety checks.
- dependencies_and_callers: Consumed by edit/task/tool renderers and mode components; depends on `pi-tui`, theme module, render-utils.
- edge_cases_or_failure_modes: Overwide ANSI text, Sixel image masks, disabled hyperlinks, internal URL resolution, background padding, and component cache invalidation.
- validation_or_tests: TUI tests plus task/edit renderer tests exercise layout and sanitization.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-318 `directory` `packages/coding-agent/test/utils`
- cursor: `[_]`
- core_role: Utility contract tests for clipboard, paste, git clone, image resize/vision fallback, jj, markit, and open helpers.
- algorithmic_behavior: Mocks platform/env/process/native APIs to verify OS-specific branching, enhanced paste parsing, image downscaling/fallback model routing, git clone behavior, and warning filtering.
- inputs_outputs_state: Inputs are fixture env vars, fake native returns, temp dirs/files, clipboard payloads; outputs are expected helper results, spawned command calls, and restored env/platform state.
- gates_or_invariants: Per-test cleanup restores mocks/env; no `mock.module`; image size/model capabilities drive fallback; command calls are inspected semantically.
- dependencies_and_callers: Tests utilities under `@oh-my-pi/pi-coding-agent/utils/*` and native bindings.
- edge_cases_or_failure_modes: WSL/PowerShell clipboard, terminal paste packet boundaries, invalid images, unavailable vision model, and platform-specific open commands.
- validation_or_tests: This directory is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-348 `file` `crates/pi-iso/src/windows_block_clone.rs`
- cursor: `[_]`
- core_role: Windows isolation backend using block clone/copy fallback semantics.
- algorithmic_behavior: Implements `IsolationBackend` with probe/start/stop, validates/canonicalizes dirs, prepares destination, recursively clones directories/files/symlinks, duplicates extents where supported, copies metadata best-effort, and maps unavailable errors.
- inputs_outputs_state: Inputs are lower/merged paths and Windows filesystem capabilities; outputs are populated merged tree or backend unavailability/errors.
- gates_or_invariants: Non-Windows probe/start/stop report unavailable; destination is removed/prepared; readonly bits cleared before deletion; metadata time copy is best effort.
- dependencies_and_callers: Isolation resolver/native `isoStart`/`isoStop`; Windows APIs for block clone/timestamps.
- edge_cases_or_failure_modes: Unsupported FS/block clone errors, symlink handling, readonly files, metadata failures, and non-Windows builds.
- validation_or_tests: Native iso tests likely cover backend resolution; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-378 `file` `crates/pi-shell/src/cancel.rs`
- cursor: `[_]`
- core_role: Shared cancellation/timeout token for pi-shell.
- algorithmic_behavior: Stores abort reason in atomic flag, exposes heartbeat timeout checks, abort-token weak handles, and typed abort reasons.
- inputs_outputs_state: Inputs are optional timeout duration and external `AbortToken.abort(reason)` calls; outputs are `Result` from `heartbeat`, `aborted` state, and cause mapping.
- gates_or_invariants: `AbortReason` is `repr(u8)`; weak abort token only works while flag alive; timeout reason differs from explicit abort.
- dependencies_and_callers: Shell/minimizer execution loops call `heartbeat`; external controllers hold `AbortToken`.
- edge_cases_or_failure_modes: Dropped parent token makes weak abort no-op; invalid u8 abort reason maps to failure; timeout checked only on heartbeat.
- validation_or_tests: Rust crate tests for shell cancellation/minimizer paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-408 `file` `packages/agent/test/proxy-stream-disconnect.test.ts`
- cursor: `[_]`
- core_role: Regression tests for proxy SSE disconnect handling.
- algorithmic_behavior: Creates streams that end without terminal done/error, collects events, and asserts error event plus resolved `stream.result()` with stop reason `error`.
- inputs_outputs_state: Inputs are mock `fetch` responses with partial SSE bodies; outputs are `AssistantMessageEvent` sequences and final stream result.
- gates_or_invariants: Server disconnect after start or mid-stream must not hang; missing terminal event becomes error.
- dependencies_and_callers: `streamProxy`, `ProxyMessageEventStream`, `FetchImpl`.
- edge_cases_or_failure_modes: Premature EOF without terminal frame, partial message state, async iterator timeout.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-438 `file` `packages/ai/test/anthropic-error-tool-result-image.test.ts`
- cursor: `[_]`
- core_role: Provider regression test for Anthropic error/tool-result image handling.
- algorithmic_behavior: Exercises transformation of tool result messages that contain image blocks during error paths.
- inputs_outputs_state: Inputs are Anthropic-style messages/tool results with image content; outputs are provider request/response behavior assertions.
- gates_or_invariants: Image content in tool results must remain valid provider payload even when adjacent to error semantics.
- dependencies_and_callers: Anthropic provider transform/message utilities.
- edge_cases_or_failure_modes: Tool-result image-only blocks, mixed content, provider errors.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-468 `file` `packages/ai/test/auth-gateway-openai-responses.test.ts`
- cursor: `[_]`
- core_role: Auth gateway OpenAI Responses compatibility tests.
- algorithmic_behavior: Encodes agent event streams into Responses SSE frames, verifies response lifecycle, tool call deltas/done frames, output indexing, model/status mapping, and incomplete responses.
- inputs_outputs_state: Inputs are synthetic `AssistantMessageEventStream` events; outputs are collected SSE frames and final response JSON.
- gates_or_invariants: Parallel tool deltas route by `contentIndex`; length stop emits `response.incomplete`, not completed; tool IDs/call IDs remain distinct.
- dependencies_and_callers: Auth gateway format module, OpenAI Responses encoder, event stream utilities.
- edge_cases_or_failure_modes: Late deltas after parallel starts, omitted args, tool-call ordering, length-limited streams.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-498 `file` `packages/ai/test/cursor-streaming-args.test.ts`
- cursor: `[_]`
- core_role: Cursor MCP streaming argument merge/order regression tests.
- algorithmic_behavior: Tests cumulative vs incremental `argsTextDelta`, streamed/completion argument merging, and content block ordering around completed tool calls.
- inputs_outputs_state: Inputs are partial tool-call start/delta/done events; outputs are final tool-call arguments, `partialJson`, emitted deltas, and content block arrays.
- gates_or_invariants: Cumulative snapshots replace prior prefix; genuine fragments append; empty snapshots skip emission; structured streamed args win over raw completion string.
- dependencies_and_callers: `mergeCursorMcpToolCallArgs`, `processInteractionUpdate`, `AssistantMessageEventStream`.
- edge_cases_or_failure_modes: Completion frame omits streamed keys, scalar completion overrides, raw string downgrade, issue #2615 tasks array.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-528 `file` `packages/ai/test/image-tool-result.test.ts`
- cursor: `[_]`
- core_role: Cross-provider e2e test for image content in tool results.
- algorithmic_behavior: Defines tools returning image-only or text+image results, drives a two-turn tool-call flow, and verifies vision-capable models describe the red circle fixture.
- inputs_outputs_state: Inputs are provider models/API keys, `red-circle.png`, tool schemas/results; outputs are assistant tool calls and final text descriptions.
- gates_or_invariants: Tests skip models without image input; first response must be `toolUse`; second must stop without error and mention expected visual features.
- dependencies_and_callers: `complete`, model catalog providers, OAuth token helpers.
- edge_cases_or_failure_modes: Provider-specific multimodal tool-result formatting and image-only content.
- validation_or_tests: This file is the validation; e2e portions depend on keys.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-558 `file` `packages/ai/test/json-schema-typescript.test.ts`
- cursor: `[_]`
- core_role: JSON schema to TypeScript renderer tests.
- algorithmic_behavior: Verifies object optionality/descriptions, enums/consts, arrays/tuples/records, nullable unions, local `$defs` refs, empty object schemas, and Zod wire pipeline conversion.
- inputs_outputs_state: Inputs are JSON Schema/Zod schemas; outputs are TypeScript type strings.
- gates_or_invariants: Required fields lack optional marker; descriptions become JSDoc; const/enum become literal unions.
- dependencies_and_callers: `jsonSchemaToTypeScript`, `toolWireSchema`, `zod/v4`.
- edge_cases_or_failure_modes: `$ref` resolution, `anyOf` nullability, additionalProperties records.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-588 `file` `packages/ai/test/openai-completions-upstream-provider.test.ts`
- cursor: `[_]`
- core_role: OpenAI completions upstream provider regression test.
- algorithmic_behavior: Exercises provider routing/formatting for upstream OpenAI completions behavior.
- inputs_outputs_state: Inputs are mocked provider/model/options; outputs are normalized AI responses or request assertions.
- gates_or_invariants: Completions provider must preserve upstream-compatible request/response shape.
- dependencies_and_callers: OpenAI completions provider registry.
- edge_cases_or_failure_modes: Missing/alternate upstream fields and provider compatibility.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-618 `file` `packages/ai/test/register-builtins.test.ts`
- cursor: `[_]`
- core_role: Built-in provider/model registration tests.
- algorithmic_behavior: Verifies built-in registries are registered and discoverable with expected provider definitions/options.
- inputs_outputs_state: Inputs are built-in registry module imports; outputs are registry contents and provider lookup assertions.
- gates_or_invariants: Built-in registration must be idempotent and include expected providers.
- dependencies_and_callers: AI registry/provider registration modules.
- edge_cases_or_failure_modes: Duplicate registration, missing provider aliases, default provider drift.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-648 `file` `packages/ai/test/utils-responses-id.test.ts`
- cursor: `[_]`
- core_role: OpenAI Responses ID utility tests.
- algorithmic_behavior: Verifies response/tool-call item IDs are generated/normalized consistently for stream encoding.
- inputs_outputs_state: Inputs are raw IDs/content indices/tool call IDs; outputs are stable response item IDs.
- gates_or_invariants: IDs must remain distinct where protocol requires `id` vs `call_id`.
- dependencies_and_callers: Responses utility functions.
- edge_cases_or_failure_modes: Missing IDs, duplicate call IDs, deterministic fallback.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-678 `file` `packages/catalog/test/generated-policies.test.ts`
- cursor: `[_]`
- core_role: Generated catalog policy regression tests.
- algorithmic_behavior: Applies generated model policies to synthetic catalog entries and asserts thinking metadata, pricing/cache multipliers, context windows, compatibility flags, promotion targets, and apply-patch tool type.
- inputs_outputs_state: Inputs are model records with provider/id overrides; outputs are mutated model policy fields.
- gates_or_invariants: Specific model families/providers pin long-context values; OpenCode tool-choice exceptions preserved; first-party GPT-5 Responses gets freeform apply_patch.
- dependencies_and_callers: `applyGeneratedModelPolicies`, catalog identity/model-thinking code.
- edge_cases_or_failure_modes: Upstream metadata drift, namespaced/dated IDs, fallback limits.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-708 `file` `packages/catalog/test/venice-provider.test.ts`
- cursor: `[_]`
- core_role: Venice provider catalog descriptor test.
- algorithmic_behavior: Verifies Venice provider metadata/resolution behavior.
- inputs_outputs_state: Inputs are Venice descriptor/model IDs; outputs are provider/catalog assertions.
- gates_or_invariants: Venice provider must expose expected API/default compatibility fields.
- dependencies_and_callers: Catalog provider descriptors/resolvers.
- edge_cases_or_failure_modes: Provider table drift or missing default model.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-738 `file` `packages/coding-agent/test/acp-builtins.test.ts`
- cursor: `[_]`
- core_role: ACP builtin slash-command contract test suite.
- algorithmic_behavior: Builds fake slash runtime and verifies command parsing/effects for todo, browser, compact, MCP, SSH, marketplace, model, usage, context, and jobs commands.
- inputs_outputs_state: Inputs are slash command strings and fake runtime/session state; outputs are `{ consumed: true }`, output text, settings mutations, spy calls, and todo state changes.
- gates_or_invariants: Unknown subcommands return usage/errors; `/browser visible` idempotently sets headless false; `/todo start` fuzzy matching prefers active pending tasks; model changes notify title.
- dependencies_and_callers: `executeAcpBuiltinSlashCommand`, slash helper modules, `MarketplaceManager`, MCP/SSH helpers.
- edge_cases_or_failure_modes: Missing args, unknown models, ambiguous todos, empty MCP/SSH config, TUI-only marketplace actions.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-768 `file` `packages/coding-agent/test/agent-session-magic-keywords.test.ts`
- cursor: `[_]`
- core_role: Agent session magic keyword behavior tests.
- algorithmic_behavior: Verifies session handling of special user inputs/magic keywords and resulting mode/session state.
- inputs_outputs_state: Inputs are user messages/commands; outputs are session state transitions and emitted behavior.
- gates_or_invariants: Magic keyword recognition must not corrupt normal message flow.
- dependencies_and_callers: `AgentSession`, interactive/session command handling.
- edge_cases_or_failure_modes: Keyword collisions with ordinary text and repeated transitions.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-798 `file` `packages/coding-agent/test/auth-storage-minimax-login.test.ts`
- cursor: `[_]`
- core_role: Auth storage test for MiniMax login credentials.
- algorithmic_behavior: Verifies provider login data persists/loads correctly for MiniMax.
- inputs_outputs_state: Inputs are auth DB/temp credentials; outputs are stored credential rows and lookup results.
- gates_or_invariants: Provider identity fields must round-trip without collision.
- dependencies_and_callers: `AuthStorage` and provider auth logic.
- edge_cases_or_failure_modes: Missing/invalid stored token metadata.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-828 `file` `packages/coding-agent/test/commit-model-selection-role-thinking.test.ts`
- cursor: `[_]`
- core_role: Commit model role/thinking selection regression test.
- algorithmic_behavior: Verifies commit command model resolution honors role-specific model and thinking settings.
- inputs_outputs_state: Inputs are settings/model roles; outputs are selected model/thinking parameters.
- gates_or_invariants: Commit model selection must not ignore role thinking level.
- dependencies_and_callers: Commit model-selection helpers and settings.
- edge_cases_or_failure_modes: Fallback model role vs active model mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-858 `file` `packages/coding-agent/test/extensions-runner.test.ts`
- cursor: `[_]`
- core_role: Extension runner lifecycle/tool/command integration tests.
- algorithmic_behavior: Loads extension definitions, registers commands/tools/hooks/renderers, drives events, and asserts extension runner state and output.
- inputs_outputs_state: Inputs are extension fixtures/runtime APIs/session events; outputs are registered capabilities, transformed events/results, and errors.
- gates_or_invariants: Extension registration must be isolated, deterministic, and not crash session on handler failures.
- dependencies_and_callers: Extension runner, custom tools, command loader, UI context, session events.
- edge_cases_or_failure_modes: Duplicate commands/tools, failing hooks, async lifecycle, cleanup/dispose.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-888 `file` `packages/coding-agent/test/input-controller-keybindings.test.ts`
- cursor: `[_]`
- core_role: Input controller keybinding tests.
- algorithmic_behavior: Simulates key sequences and verifies configured action routing for editor/input operations.
- inputs_outputs_state: Inputs are raw key bytes/keybinding configs; outputs are editor/controller state changes.
- gates_or_invariants: Custom keybindings override defaults without breaking core actions.
- dependencies_and_callers: Input controller, keybindings manager, editor state.
- edge_cases_or_failure_modes: Escape/interrupt, selector navigation, multiline input.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-918 `file` `packages/coding-agent/test/issue-2510-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for `/plan` mode toggle cycle.
- algorithmic_behavior: Creates fresh session/mode and invokes `/plan` three times, asserting transitions plan → paused → none.
- inputs_outputs_state: Inputs are repeated `/plan` slash commands; outputs are `planModeEnabled`, `planModePaused`, and persisted session context mode.
- gates_or_invariants: Third `/plan` must exit to `none`, not re-enter plan.
- dependencies_and_callers: `InteractiveMode`, `AgentSession`, `Settings`, `SessionManager`.
- edge_cases_or_failure_modes: State persistence drift across consecutive command invocations.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-948 `file` `packages/coding-agent/test/keybindings-selector-navigation.test.ts`
- cursor: `[_]`
- core_role: Selector navigation keybinding tests.
- algorithmic_behavior: Drives session selector/tree/user message selector/extension list/history search with configured select actions.
- inputs_outputs_state: Inputs are keybinding manager and selector fixtures; outputs are selected paths/messages/extensions.
- gates_or_invariants: Selectors use action IDs like `tui.select.down/up`, not hardcoded keys.
- dependencies_and_callers: `KeybindingsManager`, selector components, `HistoryStorage`.
- edge_cases_or_failure_modes: Page/home/end navigation and tree child selection.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-978 `file` `packages/coding-agent/test/memory-session-storage.test.ts`
- cursor: `[_]`
- core_role: In-memory session storage byte-slicing tests.
- algorithmic_behavior: Verifies append/write/stat/read-slice behavior mirrors file semantics with UTF-8 byte budgets.
- inputs_outputs_state: Inputs are virtual paths and text chunks; outputs are stored text, byte sizes, and prefix/suffix slices.
- gates_or_invariants: `statSync.size` is UTF-8 bytes; overwrite resets chunks; slices are byte-oriented even across multibyte boundaries.
- dependencies_and_callers: `MemorySessionStorage`.
- edge_cases_or_failure_modes: Materialized read followed by append, zero budgets, invalid UTF-8 boundary replacement.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1008 `file` `packages/coding-agent/test/prompt-format.test.ts`
- cursor: `[_]`
- core_role: Prompt formatting contract tests.
- algorithmic_behavior: Verifies pre/post-render whitespace handling, trailing trim, table compaction, ASCII symbol replacement, and HTML comment preservation.
- inputs_outputs_state: Inputs are prompt strings and render phase options; outputs are exact formatted strings.
- gates_or_invariants: Pre-render preserves Handlebars indentation/tabs, trims trailing whitespace, removes some blank lines; comments are not mutated.
- dependencies_and_callers: `prompt.format`.
- edge_cases_or_failure_modes: HTML comments spanning lines, arrows inside comments, table row replacement duplication.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1038 `file` `packages/coding-agent/test/sdk-mcp-instructions.test.ts`
- cursor: `[_]`
- core_role: Deferred UI MCP server instruction integration test.
- algorithmic_behavior: Creates agent session with deferred interactive MCP discovery and waits until connected server instructions join the system prompt.
- inputs_outputs_state: Inputs are temp MCP config, fixture server, session options; outputs are updated `session.systemPrompt`.
- gates_or_invariants: Initial prompt lacks instructions; once discovery connects, prompt includes server instructions and heading.
- dependencies_and_callers: `createAgentSession`, `MCPManager`, `AuthStorage`, `ModelRegistry`, `SessionManager`.
- edge_cases_or_failure_modes: Deferred UI discovery previously dropped instructions permanently.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1068 `file` `packages/coding-agent/test/snapcompact-savings-journal.test.ts`
- cursor: `[_]`
- core_role: Snapcompact savings journal tests.
- algorithmic_behavior: Records per-tool-result token savings, deduplicates by session/tool call, filters invalid records, and reads missing journal as empty.
- inputs_outputs_state: Inputs are savings records, model metadata, session file supplier, journal path; outputs are JSONL journal records.
- gates_or_invariants: Non-positive savings or missing session writes nothing; each tool result recorded once per session.
- dependencies_and_callers: `createSnapcompactSavingsRecorder`, `readSnapcompactSavingsJournal`.
- edge_cases_or_failure_modes: Re-imaged later requests, missing journal file.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1098 `file` `packages/coding-agent/test/theme-auto-detection.test.ts`
- cursor: `[_]`
- core_role: Auto theme detection fallback tests.
- algorithmic_behavior: Mocks terminal env/native macOS appearance observer and asserts theme selection/updates under Zellij and non-Zellij cases.
- inputs_outputs_state: Inputs are env vars, platform, native appearance values; outputs are current theme name and observer calls.
- gates_or_invariants: Terminal-reported appearance wins; COLORFGBG wins before macOS fallback in Zellij; Zellij fallback is macOS-only; observer stop called.
- dependencies_and_callers: Theme module, `detectMacOSAppearance`, `MacAppearanceObserver`, settings.
- edge_cases_or_failure_modes: Conflicting COLORFGBG, Linux+Zellij, fallback observer update.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1128 `file` `packages/coding-agent/test/write-streaming-preview-expand.test.ts`
- cursor: `[_]`
- core_role: Write/edit streaming preview expansion test.
- algorithmic_behavior: Verifies streaming write preview expands/rendering state as partial args/results arrive.
- inputs_outputs_state: Inputs are tool call/update events; outputs are rendered preview content and expanded state.
- gates_or_invariants: Preview-only fields must survive call/result rendering paths.
- dependencies_and_callers: Tool execution/edit renderer/event controller.
- edge_cases_or_failure_modes: Partially streamed JSON arguments and rebuilt transcript consistency.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1158 `file` `packages/hashline/src/stream.ts`
- cursor: `[_]`
- core_role: Hashline streaming parser/application support.
- algorithmic_behavior: Maintains streaming edit parse state and emits partial/complete sections for hashline inputs.
- inputs_outputs_state: Inputs are incremental hashline text chunks; outputs are parsed section/edit previews or parser state.
- gates_or_invariants: Must tolerate incomplete sections and only finalize well-formed edits.
- dependencies_and_callers: Coding-agent edit streaming/renderer and hashline execute path.
- edge_cases_or_failure_modes: Partial blocks, cursor anchors, incomplete final newline, malformed ranges.
- validation_or_tests: Hashline recovery/edit tests and streaming preview tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1188 `file` `packages/mnemopi/test/binary-vectors.test.ts`
- cursor: `[_]`
- core_role: Binary vector helper/store tests.
- algorithmic_behavior: Verifies MIB bit packing, int8 quantization, Hamming/score/cosine math, env vector type normalization, binary store CRUD/search/stats, and FastBinarySearch.
- inputs_outputs_state: Inputs are float vectors/env/db records; outputs are packed bytes, scores, search ordering, and stats.
- gates_or_invariants: Zero/NaN cosine falls back to 0; invalid vector type falls back; search ordering by distance/score.
- dependencies_and_callers: `binary-vectors`, vector store/search modules.
- edge_cases_or_failure_modes: Different vector lengths, deletes, compact byte stats.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1218 `file` `packages/mnemopi/test/migrate-triplestore-split.test.ts`
- cursor: `[_]`
- core_role: E6 triplestore split migration tests.
- algorithmic_behavior: Seeds legacy annotation triples, runs migration/dry-run/backups, asserts split rows, idempotency, duplicate tolerance, and pending detection.
- inputs_outputs_state: Inputs are SQLite DB rows and migration options; outputs are written counts, annotation rows, backups, logs.
- gates_or_invariants: Dry-run writes nothing; backup only when requested and not overwritten; duplicate annotations ignored; empty/non-annotation DB no-op.
- dependencies_and_callers: `migrate`, `hasPendingMigration`, bun sqlite.
- edge_cases_or_failure_modes: Unique index duplicates, reruns with new legacy rows, cheap pending scan.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1248 `file` `packages/natives/native/index.d.ts`
- cursor: `[_]`
- core_role: Type declaration contract for native bindings.
- algorithmic_behavior: Declares native APIs for PTY/process/shell, ast-grep, block ranges, clipboard/image/Sixel, tokenizer, grep/glob/search, ISO backends, keyboard parsing, minimizer, width/wrapping, and snapcompact rendering.
- inputs_outputs_state: Inputs are typed option objects and callbacks; outputs are promises/results/classes/enums consumed by TS packages.
- gates_or_invariants: API shape pins native/JS boundary; comments define behavior for callbacks, output modes, runtime install, and ISO availability.
- dependencies_and_callers: `packages/tui`, `coding-agent`, `ai`, `hashline`, `utils`, native N-API module.
- edge_cases_or_failure_modes: Declaration drift from native implementation, callback error conventions, platform-specific unavailable results.
- validation_or_tests: Native consumers and type checks validate this contract.
- skip_candidate: `yes: declaration surface, not implementation, but core boundary contract`

### OH_MY_HUMANIZE_MAIN-HZ-1278 `file` `packages/snapcompact/research/exp06_rolecolor.py`
- cursor: `[_]`
- core_role: Snapcompact research experiment for role/color image carriers.
- algorithmic_behavior: Assigns roles, chunks paragraphs, samples questions, renders role/tag/no-meta image carriers, runs model QA cells, scores role answers, aggregates token/cost/accuracy.
- inputs_outputs_state: Inputs are corpora, fonts, model keys, condition/length args; outputs are PNG carriers, JSON records, aggregates, cost summaries.
- gates_or_invariants: Fixed roles/tags/colors, atomic PNG creation, normalized role scoring, per-phase cost calculation.
- dependencies_and_callers: PIL, model call helpers, prompt files, research results dirs.
- edge_cases_or_failure_modes: Missing fonts/keys, image render failure, malformed answer role, API errors.
- validation_or_tests: Research script validates through run records/aggregate metrics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1308 `file` `packages/snapcompact/research/snapcompact_carrier_convergence.py`
- cursor: `[_]`
- core_role: Research probe comparing text/image carrier hidden-state convergence.
- algorithmic_behavior: Builds text/image prompts, captures last-token activations, computes row-wise cosine similarities, and summarizes layer/model convergence.
- inputs_outputs_state: Inputs are model/processor/device, text chunks, images, questions; outputs are NumPy vectors/similarity metrics/reports.
- gates_or_invariants: Image prompt includes carrier dimensions; cosine computed on aligned activation rows.
- dependencies_and_callers: Transformers/NumPy/PIL research stack.
- edge_cases_or_failure_modes: Model load/device mismatch, missing image, incompatible activation shapes.
- validation_or_tests: Research script self-checks by producing comparable metrics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1338 `file` `packages/snapcompact/research/snapcompact_viz_volume.py`
- cursor: `[_]`
- core_role: Visualization script for snapcompact tensor/volume results.
- algorithmic_behavior: Loads volume data, robust-normalizes values, renders 3D volume/projection/layer panels, and writes source data.
- inputs_outputs_state: Inputs are result arrays/summary metadata; outputs are rendered image artifacts and exported source data.
- gates_or_invariants: Quantile normalization clamps outliers; output dirs fixed under research results.
- dependencies_and_callers: NumPy, matplotlib 3D/color maps.
- edge_cases_or_failure_modes: Missing data dir, empty volume, label mismatch.
- validation_or_tests: Manual research artifact generation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1368 `file` `packages/tui/src/autocomplete.ts`
- cursor: `[_]`
- core_role: TUI autocomplete component/algorithm.
- algorithmic_behavior: Maintains suggestions, selection, filtering, rendering, and input handling for autocomplete UI.
- inputs_outputs_state: Inputs are query text/items/key events/width/theme; outputs are selected item callbacks and render rows.
- gates_or_invariants: Selection stays in bounds; rendering must be width-aware; invalid/empty suggestion sets handled.
- dependencies_and_callers: TUI input/editor components and key utilities.
- edge_cases_or_failure_modes: Long labels, no matches, rapid query changes, terminal width changes.
- validation_or_tests: Selector/keybinding and TUI tests exercise adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1398 `file` `packages/tui/test/emergency-restore-altscreen.test.ts`
- cursor: `[_]`
- core_role: Emergency terminal restore alt-screen gating tests.
- algorithmic_behavior: Mocks terminal writes and asserts `emergencyTerminalRestore()` only emits DECRST 1049 when alt screen is tracked active.
- inputs_outputs_state: Inputs are active terminal/alt-screen state; outputs are escape sequences written to stdout.
- gates_or_invariants: Graceful post-stop path without alt screen must not leave alternate screen; cursor show still emitted.
- dependencies_and_callers: `emergencyTerminalRestore`, `ProcessTerminal`, `setAltScreenActive`.
- edge_cases_or_failure_modes: Live-terminal crash vs post-stop path, state reset after restore.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1428 `file` `packages/tui/test/mouse.test.ts`
- cursor: `[_]`
- core_role: SGR mouse parser tests.
- algorithmic_behavior: Parses terminal mouse sequences into button/release/wheel/motion events with zero-based coords.
- inputs_outputs_state: Inputs are raw escape sequences; outputs are parsed event objects or `null`.
- gates_or_invariants: Non-mouse input returns null; releases are not clicks; wheel bit maps direction.
- dependencies_and_callers: `parseSgrMouse`.
- edge_cases_or_failure_modes: Bogus sequences, motion reports, wheel reports.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1458 `file` `packages/tui/test/test-themes.ts`
- cursor: `[_]`
- core_role: Shared theme fixtures for TUI tests.
- algorithmic_behavior: Exports default test theme values using chalk-compatible styling.
- inputs_outputs_state: Inputs are none/static theme definitions; outputs are reusable test theme objects.
- gates_or_invariants: Stable symbols/colors keep renderer snapshots deterministic.
- dependencies_and_callers: TUI/render tests import this helper.
- edge_cases_or_failure_modes: Theme drift can break unrelated renderer tests.
- validation_or_tests: Indirectly used by TUI tests.
- skip_candidate: `yes: test fixture data, not an algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1488 `file` `packages/utils/src/format.ts`
- cursor: `[_]`
- core_role: Shared human-readable formatting utilities.
- algorithmic_behavior: Formats durations, numbers, bytes, truncation, counts, ages, plurals, and percentages with compact thresholds.
- inputs_outputs_state: Inputs are numeric values/strings/labels; outputs are display strings.
- gates_or_invariants: Handles null/undefined age as dash; truncation uses ellipsis; byte/duration thresholds use fixed units.
- dependencies_and_callers: Shared UI/log/dashboard renderers.
- edge_cases_or_failure_modes: Negative/large values, boundary thresholds, singular/plural labels.
- validation_or_tests: Indirect UI tests; no assigned direct unit test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1518 `file` `packages/utils/test/dirs-python-gateway.test.ts`
- cursor: `[_]`
- core_role: Python gateway directory resolution tests.
- algorithmic_behavior: Sets isolated env/agent dir and asserts gateway dir uses XDG state for default profile and custom agent dir for custom profiles.
- inputs_outputs_state: Inputs are `XDG_STATE_HOME`, agent dir settings; outputs are resolved directory paths.
- gates_or_invariants: Custom profiles isolated from shared XDG state.
- dependencies_and_callers: `getPythonGatewayDir`, `setAgentDir`, dirs utilities.
- edge_cases_or_failure_modes: Env leakage across tests; custom profile path collision.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1548 `file` `python/robomp/src/__main__.py`
- cursor: `[_]`
- core_role: Python package entrypoint.
- algorithmic_behavior: Imports and invokes robomp CLI `main` when module is executed.
- inputs_outputs_state: Inputs are process argv/env handled by CLI; output is CLI exit behavior.
- gates_or_invariants: Only runs under `if __name__ == "__main__"`.
- dependencies_and_callers: `python -m robomp`.
- edge_cases_or_failure_modes: Import failure in CLI module.
- validation_or_tests: Covered indirectly by robomp CLI tests.
- skip_candidate: `yes: thin entrypoint wrapper`

### OH_MY_HUMANIZE_MAIN-HZ-1578 `file` `python/robomp/tests/test_github_client.py`
- cursor: `[_]`
- core_role: Robomp GitHub client tests.
- algorithmic_behavior: Mocks HTTP responses to assert error mapping, redirect handling, repository resolution, issue/PR response parsing, and GitHubError messages.
- inputs_outputs_state: Inputs are mocked GitHub API responses/status/headers; outputs are exceptions or parsed client data.
- gates_or_invariants: 4xx maps to `GitHubError`; redirects without follow raise unless acceptable resolution path; clone/html URLs parsed.
- dependencies_and_callers: `GitHubClient`, `GitHubError`, HTTP mocking.
- edge_cases_or_failure_modes: Repository redirects, API error body messages, PR URL fields.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1608 `directory` `packages/coding-agent/src/commit/agentic`
- cursor: `[_]`
- core_role: Agentic commit planning/execution subsystem.
- algorithmic_behavior: Runs an agent with git overview/diff/hunk/recent/analyze/propose/split/changelog tools, validates conventional commit output, optionally splits commits in dependency order, applies changelog proposals, and falls back for trivial changes.
- inputs_outputs_state: Inputs are git diff/numstat, settings/auth/model registry, existing changelog entries, agent tool calls; outputs are commit proposals, split plans, changelog proposals, and actual git commits.
- gates_or_invariants: Summary max 72 chars; detail cap 6; split dependency graph must be acyclic; duplicate hunk/file selectors rejected; trivial whitespace/import-only detection bypasses full agent.
- dependencies_and_callers: Commit command invokes `runAgenticCommit`; depends on git utils, `createAgentSession`, model selection, changelog parser/applier.
- edge_cases_or_failure_modes: Invalid proposals, cyclic split deps, missing changelog, agent failure, hunk ambiguity, docs/test-heavy diffs.
- validation_or_tests: Commit model selection and related commit tests cover key contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1638 `directory` `packages/coding-agent/src/slash-commands/helpers`
- cursor: `[_]`
- core_role: Helper layer for ACP/TUI slash command implementations.
- algorithmic_behavior: Parses subcommands/options, formats usage/context/usage reports, manages MCP/SSH config, todo mutations/import/export, marketplace manager creation, workflow lifecycle/control, logout/reset/stats helpers.
- inputs_outputs_state: Inputs are parsed slash strings, runtime/session/settings, filesystem configs, workflow args; outputs are `SlashCommandResult`, output text, settings/config mutations, workflow activations.
- gates_or_invariants: Unknown subcommands return usage; scope parsing restricts user/project; workflow args validate limits/selectors; todo fuzzy matching title-cases and commits through runtime.
- dependencies_and_callers: Builtin slash registry and ACP executor call helpers; depends on MCP manager, plugin manager, workflow runtime/store, settings/session APIs.
- edge_cases_or_failure_modes: Missing args, ambiguous plugin scope, unavailable TUI-only commands, invalid workflow paths/change requests, disconnected MCP servers.
- validation_or_tests: `acp-builtins.test.ts`, workflow tests, helper-specific tests cover this directory.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1668 `file` `crates/pi-shell/src/minimizer/detect.rs`
- cursor: `[_]`
- core_role: Command identity detector for shell output minimization.
- algorithmic_behavior: Tokenizes shell command strings, strips launch/env/sudo/time/exec wrappers, normalizes program paths, skips global options, and detects program/subcommand identity for tools like git/cargo/npm/docker/aws.
- inputs_outputs_state: Inputs are command strings or tokens; outputs are `CommandIdentity { program, subcommand }` or `None`.
- gates_or_invariants: Wrapper stripping is allowlisted; option-value consumers skipped; compound command boundaries stop detection.
- dependencies_and_callers: Shell minimizer filters use identity to choose minimization strategy.
- edge_cases_or_failure_modes: Quoted args, env assignments, `.cmd/.bat` wrappers, docker compose normalization, AWS global option permutations, npx workspace value.
- validation_or_tests: Extensive inline Rust tests cover wrappers/globals/package managers/docker/aws.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1698 `file` `packages/ai/src/auth-gateway/types.ts`
- cursor: `[_]`
- core_role: Auth gateway request/server type contract.
- algorithmic_behavior: Defines parsed request options, tool choice, stream control, format module interface, server options/handle, and default bind.
- inputs_outputs_state: Inputs are provider request payloads, tools, model/effort/settings, auth gateway options; outputs are typed parsed requests and streaming formatter callbacks.
- gates_or_invariants: Tool choice union limited to auto/none/required/name; format modules expose parse/stream handlers.
- dependencies_and_callers: Auth gateway server, OpenAI Responses tests, pi-native client.
- edge_cases_or_failure_modes: Unknown provider payload shapes, malformed options/tools.
- validation_or_tests: Auth gateway OpenAI Responses test covers formatter contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1728 `file` `packages/ai/src/providers/aws-credentials.ts`
- cursor: `[_]`
- core_role: AWS credential resolution/cache implementation.
- algorithmic_behavior: Resolves credentials from env, shared ini profiles, SSO cache, credential_process, and IMDS; caches/inflights by profile/region with skew/TTL; supports invalidation.
- inputs_outputs_state: Inputs are env vars, profile/region, AWS config files, SSO token cache, process commands, abort signals; outputs are `ResolvedCredentials`.
- gates_or_invariants: Refresh skew 60s; file session creds TTL 5m; shared resolve timeout 30s; IMDS timeout 1s; credential_process tokenized safely.
- dependencies_and_callers: Bedrock/AWS providers, sigv4 client, `raceWithSignal`, Bun spawn/shell.
- edge_cases_or_failure_modes: Expired SSO token, malformed ini/process JSON, command tokenization quotes, IMDS unavailable, inflight rejection.
- validation_or_tests: Provider tests and credential unit tests outside assigned list likely cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1758 `file` `packages/ai/src/providers/pi-native-client.ts`
- cursor: `[_]`
- core_role: Client for pi native/auth-gateway streaming endpoint.
- algorithmic_behavior: Builds wire options/headers, resolves stream URL, posts chat request, decodes SSE JSON events into `AssistantMessageEventStream`, handles gateway HTTP errors, and synthesizes assistant fallback.
- inputs_outputs_state: Inputs are model, context, stream options, API key, fetch; outputs are assistant event stream and final message.
- gates_or_invariants: Non-wire option keys filtered; auth header only with API key; HTTP failures decoded to `AuthGatewayError`.
- dependencies_and_callers: Auth gateway provider registry, `readSseJson`, provider errors.
- edge_cases_or_failure_modes: Bad gateway error JSON/text, stream abort, missing endpoint, malformed SSE.
- validation_or_tests: Auth gateway streaming tests cover output protocol.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1788 `file` `packages/ai/src/registry/kilo.ts`
- cursor: `[_]`
- core_role: Kilo provider OAuth/device auth registration.
- algorithmic_behavior: Starts device auth, asks user to authorize, polls token endpoint at fixed interval, returns credentials with long expiry, and exports provider definition.
- inputs_outputs_state: Inputs are OAuth callbacks/fetch responses; outputs are `OAuthCredentials` and provider metadata.
- gates_or_invariants: Poll interval 5000 ms; one-year expiry fallback; pending authorization loops until success/failure.
- dependencies_and_callers: Provider registry OAuth login flow.
- edge_cases_or_failure_modes: Device auth failure, polling denial/timeout, malformed token response.
- validation_or_tests: Registry/provider auth tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1818 `file` `packages/ai/src/registry/vercel-ai-gateway.ts`
- cursor: `[_]`
- core_role: Vercel AI Gateway provider registration/login helper.
- algorithmic_behavior: Opens auth/API-key URL, prompts for gateway API key, validates non-empty input, and exports provider definition.
- inputs_outputs_state: Inputs are OAuth callbacks/user-entered key; outputs are API key string and provider metadata.
- gates_or_invariants: Empty/undefined key rejected by prompt flow.
- dependencies_and_callers: Provider registry login command.
- edge_cases_or_failure_modes: User cancellation or invalid key.
- validation_or_tests: Provider registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1848 `file` `packages/ai/src/utils/http-inspector.ts`
- cursor: `[_]`
- core_role: HTTP error/request inspection and message finalization utilities.
- algorithmic_behavior: Optionally dumps sanitized 400 requests, appends request context for parse/status errors, redacts sensitive headers, formats captured HTTP error payloads, and rewrites Copilot transient errors.
- inputs_outputs_state: Inputs are raw request dumps, errors, captured responses, provider name; outputs are final user-facing error messages and debug dump files.
- gates_or_invariants: Sensitive headers redacted; Bun test runtime considered; only selected errors get request context.
- dependencies_and_callers: Provider error handling/retry utilities/log dirs.
- edge_cases_or_failure_modes: Non-JSON error payloads, retry-after formatting, parse vs status errors, nested error message extraction.
- validation_or_tests: Provider error tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1878 `file` `packages/catalog/src/identity/dialect.ts`
- cursor: `[_]`
- core_role: Model-family preferred prompt dialect classifier.
- algorithmic_behavior: Maps model family tokens to dialects (`xml`, `markdown`, etc.) with fallback.
- inputs_outputs_state: Input is model ID; output is preferred dialect string.
- gates_or_invariants: Unknown families return `FALLBACK_DIALECT = "xml"`.
- dependencies_and_callers: Compaction serialization uses `preferredDialect(model.id)`.
- edge_cases_or_failure_modes: New family tokens fall back until mapped.
- validation_or_tests: Catalog identity/policy tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1908 `file` `packages/coding-agent/src/autoresearch/git.ts`
- cursor: `[_]`
- core_role: Autoresearch git branch/dirty-path management.
- algorithmic_behavior: Detects current autoresearch branch, ensures/allocates goal-derived branches, parses NUL/line git status, relativizes paths to workdir prefixes, and computes modified paths for runs.
- inputs_outputs_state: Inputs are extension API/git status output/workdir/goal; outputs are branch result objects and dirty path lists.
- gates_or_invariants: Branch prefix `autoresearch/`; branch name max 48; dirty workdir paths block branch setup with formatted list.
- dependencies_and_callers: Autoresearch extension/workflow code and git utils.
- edge_cases_or_failure_modes: Rename/copy status, quoted paths, untracked files, nested workdir prefixes, branch name collisions.
- validation_or_tests: Autoresearch/git parser tests likely adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1938 `file` `packages/coding-agent/src/cli/claude-trace-cli.ts`
- cursor: `[_]`
- core_role: CLI/debug proxy for capturing Claude messages traffic.
- algorithmic_behavior: Runs a local MITM HTTP/TLS proxy, parses HTTP messages/chunked bodies, captures `/messages` exchanges, drives a PTY Claude session, and formats captured request/response.
- inputs_outputs_state: Inputs are CLI args, proxy host/port, TLS cert/key, PTY command/message; outputs are captured exchange structures and formatted trace text.
- gates_or_invariants: Body parser handles none/fixed/chunked/until-end; background model requests filtered; timeout/default dimensions fixed.
- dependencies_and_callers: Debug CLI command, `PtySession`, `net`, `tls`, `zlib`, `xterm/headless`.
- edge_cases_or_failure_modes: CONNECT parsing, gzip decoding, incomplete chunked bodies, PTY shutdown timeout, proxy socket errors.
- validation_or_tests: Trace parser tests likely; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1968 `file` `packages/coding-agent/src/cli/worktree-cli.ts`
- cursor: `[_]`
- core_role: CLI for listing/clearing coding-agent worktrees.
- algorithmic_behavior: Scans worktree dir, classifies dirs as PR checkout/task isolation/empty/stray, formats details, clears selected entries, and reads branch metadata.
- inputs_outputs_state: Inputs are CLI options, filesystem dirs, `.git` metadata; outputs are console listing/removals.
- gates_or_invariants: Clear filters by kind; missing dirs handled; worktree classification uses `.git` entry/branch files.
- dependencies_and_callers: Worktree CLI command, git utils, `getWorktreesDir`.
- edge_cases_or_failure_modes: Broken git files, empty dirs, stale/stray dirs, removal errors.
- validation_or_tests: Worktree CLI tests if present; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1998 `file` `packages/coding-agent/src/commands/tiny-models.ts`
- cursor: `[_]`
- core_role: CLI command wrapper for tiny model actions.
- algorithmic_behavior: Defines allowed actions `download`/`list`, parses CLI args/flags, and delegates to `runTinyModelsCommand`.
- inputs_outputs_state: Inputs are CLI action/flags; outputs are tiny-model command behavior.
- gates_or_invariants: Action limited to declared tuple.
- dependencies_and_callers: Command registry and `cli/tiny-models-cli`.
- edge_cases_or_failure_modes: Unknown action or missing model args.
- validation_or_tests: CLI smoke tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2028 `file` `packages/coding-agent/src/config/settings.ts`
- cursor: `[_]`
- core_role: Central settings loader/state/hook system.
- algorithmic_behavior: Loads capability/settings files, path-scoped arrays, defaults/schema, in-memory/file-backed settings, file locks, get/set by typed paths, hook signaling, and global proxy initialization.
- inputs_outputs_state: Inputs are cwd/agentDir/settings capability files/env/test options; outputs are `Settings` instance, persisted YAML/settings state, hook callbacks.
- gates_or_invariants: Path-scoped settings match normalized prefixes; global proxy blocks before init; hooks update theme/symbol/colorblind/append-only/hindsight signals.
- dependencies_and_callers: Almost all coding-agent runtime modules read `settings`; discovery capability, `AgentStorage`, theme, edit mode.
- edge_cases_or_failure_modes: Concurrent writes, invalid YAML, uninitialized proxy access, path-prefix matching, test reset.
- validation_or_tests: Many tests initialize/reset settings; theme and task render tests exercise hooks/settings.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2058 `file` `packages/coding-agent/src/discovery/index.ts`
- cursor: `[_]`
- core_role: Discovery subsystem registration barrel.
- algorithmic_behavior: Imports capability and provider modules for side-effect registration, then re-exports discovery APIs and capability types.
- inputs_outputs_state: Inputs are module load order; outputs are populated discovery provider registries.
- gates_or_invariants: Registration imports must run before callers use discovery; types exported from canonical capability modules.
- dependencies_and_callers: SDK/session startup, custom tools/commands/plugins/context discovery.
- edge_cases_or_failure_modes: Missing side-effect import disables a provider.
- validation_or_tests: Discovery/extension/MCP tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2088 `file` `packages/coding-agent/src/exa/types.ts`
- cursor: `[_]`
- core_role: Type contract for Exa MCP/search wrappers.
- algorithmic_behavior: Defines MCP tool wrappers, call responses, search result/response shapes.
- inputs_outputs_state: Inputs are Exa/MCP JSON responses; outputs are typed structures for wrappers.
- gates_or_invariants: Schema fields typed through `TSchema`.
- dependencies_and_callers: Exa integration code and MCP wrappers.
- edge_cases_or_failure_modes: Provider response shape drift.
- validation_or_tests: Type checks and Exa integration tests.
- skip_candidate: `yes: type-only contract`

### OH_MY_HUMANIZE_MAIN-HZ-2118 `file` `packages/coding-agent/src/internal-urls/docs-index.ts`
- cursor: `[_]`
- core_role: Embedded docs index decoder/loader for internal URLs.
- algorithmic_behavior: Decodes embedded compressed docs index, falls back to reading docs from disk, memoizes index, lists filenames, and returns embedded doc content.
- inputs_outputs_state: Inputs are generated embed string or repo docs files; outputs are `DocsIndex`, filenames, doc text promises.
- gates_or_invariants: Invalid embed returns null/fallback; memoized singleton avoids repeated disk reads.
- dependencies_and_callers: Internal URL resolver/read tool docs support; Bun `Glob`, zlib gunzip.
- edge_cases_or_failure_modes: Corrupt embed, missing docs, async gunzip failure.
- validation_or_tests: Internal URL protocol test covers adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2148 `file` `packages/coding-agent/src/markit/registry.ts`
- cursor: `[_]`
- core_role: Document conversion registry for Markit.
- algorithmic_behavior: Registers converters for docx/epub/pdf/pptx/xlsx, selects by extension/stream info, and delegates conversion.
- inputs_outputs_state: Inputs are file paths/streams/options; outputs are `ConversionResult`.
- gates_or_invariants: Unsupported formats must return/throw consistently; converter list ordered by capability.
- dependencies_and_callers: Read/markit document ingestion.
- edge_cases_or_failure_modes: Unknown extension, converter failure, binary stream metadata mismatch.
- validation_or_tests: Markit warning tests cover part of pipeline.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2178 `file` `packages/coding-agent/src/mnemopi/config.ts`
- cursor: `[_]`
- core_role: Mnemopi backend config and memory-bank scoping logic.
- algorithmic_behavior: Loads settings into backend config, computes global/per-project/per-project-tagged bank scope, extends recall with legacy banks, sanitizes/limits bank names, and token-truncates recall text.
- inputs_outputs_state: Inputs are settings, agentDir, cwd, DB paths; outputs are `MnemopiBackendConfig`, bank names/tags, recall bank list.
- gates_or_invariants: Legacy bank scan limit 64; bank names sanitized/limited; shared bank defaults to `default`.
- dependencies_and_callers: Mnemopi integration and memory tools.
- edge_cases_or_failure_modes: Legacy DB only has cwd, invalid configured bank, long project paths, token truncation boundary.
- validation_or_tests: Mnemopi tests cover adjacent storage/vector behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2208 `file` `packages/coding-agent/src/secrets/index.ts`
- cursor: `[_]`
- core_role: Secret loading and environment secret collection.
- algorithmic_behavior: Loads YAML secret entries from config, validates entries, compiles regexes, and scans env vars matching secret-like names with minimum value length.
- inputs_outputs_state: Inputs are cwd/agentDir secrets files and process env; outputs are `SecretEntry[]`.
- gates_or_invariants: Env secret names match key/secret/token/password/auth patterns; min value length 8; invalid YAML entries skipped/warned.
- dependencies_and_callers: Secret obfuscator/log sanitization.
- edge_cases_or_failure_modes: Missing files, malformed YAML, invalid regex entries, short env values.
- validation_or_tests: Secret/obfuscation tests likely; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2238 `file` `packages/coding-agent/src/session/streaming-output.ts`
- cursor: `[_]`
- core_role: Streaming output buffering, truncation, artifact spill, and preview updates.
- algorithmic_behavior: Provides UTF-8-safe head/tail/middle truncation, line/byte caps, inline byte cap with artifact footer, `TailBuffer`, `OutputSink`, artifact head+tail ring writing, and `streamTailUpdates`.
- inputs_outputs_state: Inputs are streamed chunks/bytes/options/artifact allocator/update callback; outputs are sanitized tail text, truncation notices, artifact files, summaries, and streaming tool updates.
- gates_or_invariants: Default max 3000 lines/50 KiB/512 columns; UTF-8 boundaries preserved; artifact cap disabled by default; pending chunks flushed on dump.
- dependencies_and_callers: Bash/Python/SSH/browser tools and renderers; `sanitizeText`, Sixel sanitizer, `formatBytes`.
- edge_cases_or_failure_modes: Long line split across chunks, huge chunk over threshold, artifact sink opens asynchronously, middle elision marker accuracy, zero tail budget.
- validation_or_tests: Strip-output notice, write streaming preview, task/tool output tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2268 `file` `packages/coding-agent/src/task/name-generator.ts`
- cursor: `[_]`
- core_role: Human-readable task/subagent name generator.
- algorithmic_behavior: Combines large adjective/noun lists, capitalizes parts, tracks used names, retries for uniqueness, and resets test state.
- inputs_outputs_state: Inputs are random source/global used set; outputs are generated task names.
- gates_or_invariants: Names are unique until reset/exhaustion fallback.
- dependencies_and_callers: Task/subagent display IDs.
- edge_cases_or_failure_modes: Exhausting combinations, deterministic tests requiring `resetTaskNames`.
- validation_or_tests: Task render/eval tests consume generated IDs indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2298 `file` `packages/coding-agent/src/tools/browser.ts`
- cursor: `[_]`
- core_role: Browser automation tool exposed to the agent.
- algorithmic_behavior: Validates browser params, opens/reuses/closes tabs, acquires headless/spawned/connected/cmux browsers, runs tab code, captures displays/screenshots, caps text output, and saves over-cap artifacts.
- inputs_outputs_state: Inputs are `open`/`close`/`run` params, session settings, code, timeout, abort signal; outputs are tool content/details, screenshots, tab registry mutations, artifact IDs.
- gates_or_invariants: `run` requires non-empty code; tab bound to different browser kind errors; close-all can kill; timeout clamped; approval details truncate URL/code.
- dependencies_and_callers: Browser registry/tab supervisor/cmux/readable helpers, `enforceInlineByteCap`, tool result builder.
- edge_cases_or_failure_modes: Abort mapping, missing tab, large JSON display, artifact allocation failure, kind mismatch, app target/viewport handling.
- validation_or_tests: Browser slash ACP tests and browser tool tests outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2328 `file` `packages/coding-agent/src/tools/list-limit.ts`
- cursor: `[_]`
- core_role: Shared list limiting helper for tool outputs.
- algorithmic_behavior: Applies a maximum item count and returns visible items plus omitted count/meta.
- inputs_outputs_state: Inputs are item array and limit options; outputs are `ListLimitResult<T>`.
- gates_or_invariants: Limit values normalized; omitted count never negative.
- dependencies_and_callers: Tools that list files/resources/results.
- edge_cases_or_failure_modes: Zero/undefined limits, exact-boundary item counts.
- validation_or_tests: Tool listing tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2358 `file` `packages/coding-agent/src/tts/index.ts`
- cursor: `[_]`
- core_role: Barrel export for TTS subsystem.
- algorithmic_behavior: Re-exports downloader, models, runtime, client, protocol, worker, vocalizer, and WAV modules.
- inputs_outputs_state: Inputs are module imports; outputs are consolidated public TTS API.
- gates_or_invariants: Export surface must stay in sync with TTS modules.
- dependencies_and_callers: Speech/vocalizer mode and worker consumers.
- edge_cases_or_failure_modes: Missing export breaks downstream imports.
- validation_or_tests: Type checks and speech tests.
- skip_candidate: `yes: barrel only`

### OH_MY_HUMANIZE_MAIN-HZ-2388 `file` `packages/coding-agent/src/utils/file-mentions.ts`
- cursor: `[_]`
- core_role: `@file` mention extraction and auto-context generation.
- algorithmic_behavior: Extracts sanitized mentions, resolves paths, reads text/image/dir listings within byte limits, records snapshots/numbered hashline text, resizes images, and returns file mention messages.
- inputs_outputs_state: Inputs are user text, cwd, snapshot store, filesystem; outputs are `FileMentionMessage` blocks with text/images/listings.
- gates_or_invariants: Mention boundary/punctuation stripping; text max 5 MiB, image max 25 MiB, dir default limit 500; paths resolved through read-path rules.
- dependencies_and_callers: Session user-message preprocessing, hashline snapshot utilities, image resize/metadata.
- edge_cases_or_failure_modes: Nonexistent paths, huge files/images, directories with many entries, punctuation around mentions.
- validation_or_tests: File mention/image resize utility tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2418 `file` `packages/coding-agent/src/workflow/graph-view.test.ts`
- cursor: `[_]`
- core_role: Workflow graph view test.
- algorithmic_behavior: Builds a workflow family with running program node and asserts focused interrupt guidance/action strings.
- inputs_outputs_state: Inputs are synthetic `WorkflowRunFamilySnapshot`; outputs are graph view focus/actions.
- gates_or_invariants: Running program node exposes `/workflow interrupt ... --deadline-ms 30000` control.
- dependencies_and_callers: `buildWorkflowGraphView`.
- edge_cases_or_failure_modes: Missing focused running node or stale attempt/node IDs.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2448 `file` `packages/coding-agent/test/collab/session-replication.test.ts`
- cursor: `[_]`
- core_role: Collaboration session replication tests.
- algorithmic_behavior: Verifies session events/messages replicate across collaboration boundary.
- inputs_outputs_state: Inputs are source session events/state; outputs are replicated guest/session state assertions.
- gates_or_invariants: Ordering and message identity must be preserved.
- dependencies_and_callers: Collab/session replication modules.
- edge_cases_or_failure_modes: Partial streams, reconnect/state rebuild, duplicate events.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2478 `file` `packages/coding-agent/test/core/turn-budget.test.ts`
- cursor: `[_]`
- core_role: Turn budget accounting tests.
- algorithmic_behavior: Verifies per-turn token/budget calculations and enforcement behavior.
- inputs_outputs_state: Inputs are synthetic usage/context/budget settings; outputs are budget decisions.
- gates_or_invariants: Remaining/overflow calculations must be stable at boundaries.
- dependencies_and_callers: Core turn/session budget logic.
- edge_cases_or_failure_modes: Missing usage, zero/negative budget, near-threshold values.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2508 `file` `packages/coding-agent/test/eval/agent-bridge.test.ts`
- cursor: `[_]`
- core_role: Public eval agent bridge forwarding test.
- algorithmic_behavior: Mocks task discovery/executor and asserts `runEvalAgent` forwards session-scoped MCP/local protocol options and parent agent ID.
- inputs_outputs_state: Inputs are eval prompt/agent type and fake session; outputs are `runSubprocess` options.
- gates_or_invariants: Parent session options must propagate to subagent bridge.
- dependencies_and_callers: `runEvalAgent`, task discovery/executor.
- edge_cases_or_failure_modes: Missing session option forwarding breaks eval runtime behavior.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2538 `file` `packages/coding-agent/test/internal-urls/omp-protocol.test.ts`
- cursor: `[_]`
- core_role: Internal `omp://` protocol tests.
- algorithmic_behavior: Verifies parsing/resolution of OMP internal URLs.
- inputs_outputs_state: Inputs are internal URL strings; outputs are resolved protocol/path data.
- gates_or_invariants: Invalid protocol/path rejected or undefined; valid docs/internal paths normalize predictably.
- dependencies_and_callers: Internal URL resolver/read tooling.
- edge_cases_or_failure_modes: Malformed URL, unsupported authority/path.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2568 `file` `packages/coding-agent/test/session-manager/file-operations.test.ts`
- cursor: `[_]`
- core_role: Session manager file operation tests.
- algorithmic_behavior: Exercises session file creation/resume/new-session/close behavior and persistence semantics.
- inputs_outputs_state: Inputs are temp session directories and session operations; outputs are session file paths/existence/content state.
- gates_or_invariants: Fresh new session path can be reserved without existing file; resume returns prior session file; close persists expected state.
- dependencies_and_callers: `SessionManager`, session storage.
- edge_cases_or_failure_modes: Missing previous session, file existence races, in-memory vs persisted sessions.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2598 `file` `packages/coding-agent/test/slash-commands/issue-943-type-repro.ts`
- cursor: `[_]`
- core_role: Compile-time slash command registry repro.
- algorithmic_behavior: Imports builtin registry so strict TypeScript checks command registry typing.
- inputs_outputs_state: Inputs are TS type checker; outputs are compile pass/failure.
- gates_or_invariants: Registry type relationships must remain valid.
- dependencies_and_callers: `executeBuiltinSlashCommand`.
- edge_cases_or_failure_modes: Type-only regressions not visible at runtime.
- validation_or_tests: `bun check` validates.
- skip_candidate: `yes: type-check repro, no runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2628 `file` `packages/coding-agent/test/task/task-progress-render.test.ts`
- cursor: `[_]`
- core_role: Task tool progress renderer tests.
- algorithmic_behavior: Renders task progress/results and asserts stable rows, glyph/color choices, assignment markdown, ordering, collapsed summaries, and detail-less success/error states.
- inputs_outputs_state: Inputs are `TaskToolDetails`, progress/result objects, theme/settings; outputs are rendered strings/components.
- gates_or_invariants: Running/pending rows use agent dot not spinner; rows static across time; unfinished/problem rows visible in collapsed view; finalized sorted by runtime.
- dependencies_and_callers: `taskToolRenderer`, theme/settings.
- edge_cases_or_failure_modes: Shimmer disabled, validation failures without details, many agents collapsed.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2658 `file` `packages/coding-agent/test/tools/conflict-integration.test.ts`
- cursor: `[_]`
- core_role: Edit/conflict integration tests.
- algorithmic_behavior: Exercises edit tools against conflict/recovery scenarios and asserts safe outputs/errors.
- inputs_outputs_state: Inputs are temp files, patch/replace/hashline edits; outputs are file contents, diagnostics, tool result details.
- gates_or_invariants: Conflicting/stale edits must not corrupt files; recovery gates must preserve user changes.
- dependencies_and_callers: Edit tool, hashline recovery, file snapshot store.
- edge_cases_or_failure_modes: Merge conflicts, stale anchors, ambiguous replacements.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2688 `file` `packages/coding-agent/test/tools/lsp-regressions.test.ts`
- cursor: `[_]`
- core_role: LSP/edit regression suite.
- algorithmic_behavior: Runs edit/write scenarios with LSP diagnostics/deferred writethrough and asserts diagnostics/output behavior.
- inputs_outputs_state: Inputs are temp projects/files and edit calls; outputs are modified files, diagnostics metadata, and rendered/tool results.
- gates_or_invariants: LSP must not block valid writes incorrectly; diagnostics attached consistently; regressions around batching/deferred handles pinned.
- dependencies_and_callers: Edit modes, LSP subsystem, tool session.
- edge_cases_or_failure_modes: Deferred diagnostics, batch edits, language server absence/failure.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2718 `file` `packages/coding-agent/test/tools/strip-output-notice.test.ts`
- cursor: `[_]`
- core_role: Output notice/truncation tests.
- algorithmic_behavior: Verifies stripped/truncated tool output notices preserve useful metadata and format.
- inputs_outputs_state: Inputs are long outputs/truncation results; outputs are notice strings/tool content.
- gates_or_invariants: Notices should state shown range/bytes and artifact path when available.
- dependencies_and_callers: `streaming-output`, render-utils/tool output formatting.
- edge_cases_or_failure_modes: Partial last lines, full-output artifacts, head vs tail notices.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2748 `file` `packages/coding-agent/test/workflow/condition.test.ts`
- cursor: `[_]`
- core_role: Workflow condition DSL tests.
- algorithmic_behavior: Evaluates comparison/boolean/existence expressions against state/output context and rejects arbitrary function calls.
- inputs_outputs_state: Inputs are condition strings and context objects; outputs are booleans or `WorkflowConditionError`.
- gates_or_invariants: Only allowed `exists(...)` calls; no JavaScript execution; kebab-case paths supported.
- dependencies_and_callers: `evaluateWorkflowCondition`.
- edge_cases_or_failure_modes: Unknown paths, boolean negation/and/or, arbitrary `readFile` call rejection.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2778 `file` `packages/collab-web/src/tool-render/ToolView.tsx`
- cursor: `[_]`
- core_role: Collab web generic tool renderer host.
- algorithmic_behavior: Normalizes raw args/intents, resolves a tool-specific renderer, manages expanded state, and renders summary/body with sanitized result-like data.
- inputs_outputs_state: Inputs are tool name, raw args/result, host capabilities; outputs are React nodes for summary/body.
- gates_or_invariants: Args must be object-like; ANSI/tabs stripped/replaced before display via utilities.
- dependencies_and_callers: Collab web transcript/tool rendering registry.
- edge_cases_or_failure_modes: Unknown tool renderer, invalid args, missing result.
- validation_or_tests: Collab web renderer tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2808 `file` `packages/mnemopi/src/core/query-cache.ts`
- cursor: `[_]`
- core_role: Multi-tier query result cache for enhanced recall.
- algorithmic_behavior: Normalizes queries, serves exact tier1 hits, embedding tier2/3 hits by cosine/Jaccard thresholds, word-overlap tier4 hits, persists rows in SQLite, expires by TTL, evicts by max size, and tracks stats.
- inputs_outputs_state: Inputs are query strings, optional embeddings/results/db path/env; outputs are cached result arrays, hits/misses/stats, SQLite rows.
- gates_or_invariants: Cache disabled unless enhanced recall and useCache; cosine >=0.88 tier2, >=0.78 plus Jaccard >=0.15 tier3; word overlap >=70% and at least 2 words tier4.
- dependencies_and_callers: Mnemopi recall pipeline, `cosineSimilarity`, bun sqlite.
- edge_cases_or_failure_modes: Corrupt persisted rows ignored, TTL expiry, maxSize zero, persistence failures, empty embeddings.
- validation_or_tests: Mnemopi recall/cache tests likely; binary vector tests cover related math.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2838 `file` `packages/swarm-extension/src/swarm/dag.ts`
- cursor: `[_]`
- core_role: Swarm dependency graph and wave builder.
- algorithmic_behavior: Builds node dependency map, infers default dependencies when explicit deps absent, detects cycles with DFS, and creates execution waves topologically.
- inputs_outputs_state: Inputs are `SwarmDefinition`; outputs are dependency map, cycle path or null, wave arrays.
- gates_or_invariants: Cycles block execution; explicit deps alter default behavior.
- dependencies_and_callers: Swarm extension scheduler/executor.
- edge_cases_or_failure_modes: Missing node IDs, self-cycles, disconnected nodes, mixed explicit/implicit deps.
- validation_or_tests: Swarm DAG tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2868 `file` `python/omp-rpc/src/omp_rpc/protocol.py`
- cursor: `[_]`
- core_role: Python RPC protocol type/parse layer for OMP.
- algorithmic_behavior: Defines TypedDict/dataclass contracts for messages, events, tools, session state, stats, extension UI/errors, and parse helpers that validate/clone JSON values into typed Python objects.
- inputs_outputs_state: Inputs are JSON payloads from JS/RPC and local image paths; outputs are typed dataclasses/messages/content blocks.
- gates_or_invariants: Literal fields validated against allowed sets; JSON values cloned to safe primitives; optional fields type-checked; arbitrary non-JSON rejected.
- dependencies_and_callers: Python OMP RPC client/runtime and eval bridge.
- edge_cases_or_failure_modes: Unknown notification fallback, malformed assistant events, invalid todo phases/model info, image file MIME/base64 handling.
- validation_or_tests: Python RPC/eval tests cover protocol parsing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2898 `directory` `packages/utils/src/vendor/mermaid-ascii/xychart`
- cursor: `[_]`
- core_role: Mermaid xychart parser/types/color utilities for ASCII/SVG rendering.
- algorithmic_behavior: Parses `xychart-beta` lines into typed axes/series, detects horizontal mode/title/ranges/categories, derives y-axis range, and generates/mixes chart color palettes.
- inputs_outputs_state: Inputs are preprocessed Mermaid lines and theme hex colors; outputs are `XYChart` structures and hex colors.
- gates_or_invariants: Invalid/missing y range falls back to derived or 0..100; valid hex requires six digits; y range gets 10% padding.
- dependencies_and_callers: Mermaid ASCII renderer.
- edge_cases_or_failure_modes: Empty series, numeric parse `NaN`, missing axis labels, invalid hex color.
- validation_or_tests: Mermaid-ascii tests likely; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2928 `file` `packages/ai/src/registry/oauth/callback-server.ts`
- cursor: `[_]`
- core_role: OAuth localhost callback flow server.
- algorithmic_behavior: Starts Bun server on localhost callback path, opens authorization, validates callback state/code, renders success/error HTML, supports manual pasted callback input, and races timeout.
- inputs_outputs_state: Inputs are OAuth credentials/options, callback URL/query, expected state, manual input; outputs are `{ code, state }` or rejected error.
- gates_or_invariants: Default timeout 300s; callback path `/callback`; state must match; server stopped on completion/error.
- dependencies_and_callers: OAuth provider login flows.
- edge_cases_or_failure_modes: Port conflicts, timeout, wrong state, missing code, user cancellation/manual parse.
- validation_or_tests: OAuth provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2958 `file` `packages/ai/src/utils/schema/strict-tool-validation.ts`
- cursor: `[_]`
- core_role: Strict JSON schema validation scanner for tool schemas.
- algorithmic_behavior: Recursively walks JSON schema nodes and returns first strict-mode violation path/message.
- inputs_outputs_state: Input is unknown schema; output is violation string or null.
- gates_or_invariants: Type declarations checked against known JSON schema types; child schema keys and arrays recursively inspected.
- dependencies_and_callers: Tool wire schema/provider strict validation.
- edge_cases_or_failure_modes: Unknown schema shapes, nested `$defs`, `anyOf`/`oneOf`/`allOf`, dependent schemas.
- validation_or_tests: Schema tests cover related renderer/wire behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2988 `file` `packages/coding-agent/src/commit/agentic/trivial.ts`
- cursor: `[_]`
- core_role: Trivial diff classifier for commit fallback.
- algorithmic_behavior: Scans diff lines and classifies whitespace-only or import-only changes with commit type/scope hints.
- inputs_outputs_state: Input is unified diff string; output is `TrivialChangeResult` or null.
- gates_or_invariants: Only added/removed empty/whitespace/import/export/require/module lines qualify.
- dependencies_and_callers: Agentic commit fallback path.
- edge_cases_or_failure_modes: Mixed non-import changes, comments near imports, generated diffs with metadata lines.
- validation_or_tests: Commit tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3018 `file` `packages/coding-agent/src/eval/__tests__/agent-bridge.test.ts`
- cursor: `[_]`
- core_role: Comprehensive eval `agent()` bridge tests.
- algorithmic_behavior: Verifies agent selection, spawn restrictions/depth cap, plan-mode block, option forwarding, LSP disabling, success/error mapping, abort reason surfacing, JS/Python eval runtime integration, parallel concurrency bounds, and structured output parsing.
- inputs_outputs_state: Inputs are fake sessions/settings/agents/eval scripts; outputs are tool results, executor options, thrown errors, eval process output.
- gates_or_invariants: Eval max depth enforced; plan mode cannot spawn; `task.maxConcurrency` bounds parallel; subagents force LSP off.
- dependencies_and_callers: `runEvalAgent`, eval runtime bridge, task executor/discovery/output manager.
- edge_cases_or_failure_modes: Empty stderr aborts, rejected parallel calls, unknown agent, spawn allowlist mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3048 `file` `packages/coding-agent/src/extensibility/custom-commands/loader.ts`
- cursor: `[_]`
- core_role: Custom slash command discovery/loader.
- algorithmic_behavior: Discovers command module indexes in user/project config dirs, loads Bun modules, injects shared API, validates command shape, loads bundled commands, and handles override/conflict rules.
- inputs_outputs_state: Inputs are cwd/agentDir command dirs and module factories; outputs are loaded commands plus path/error records.
- gates_or_invariants: Command must have name/description/execute; bundled commands load first and may be overridden; user/project name conflicts error.
- dependencies_and_callers: Slash command registry, bundled review/green commands, config dirs, exec helper.
- edge_cases_or_failure_modes: Missing dirs ignored; invalid module export; import failure; duplicate command names.
- validation_or_tests: Extensions/custom command tests and ACP builtins.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3078 `file` `packages/coding-agent/src/goals/tools/goal-tool.ts`
- cursor: `[_]`
- core_role: Agent tool for creating/updating/inspecting goals.
- algorithmic_behavior: Validates goal operations, mutates session goal state, reports completion budgets/remaining tokens, renders goal status blocks.
- inputs_outputs_state: Inputs are goal tool params, session goal runtime, token budget; outputs are tool content/details and TUI components.
- gates_or_invariants: Create params require objective; token budget validated; unknown goal ops throw `ToolError`.
- dependencies_and_callers: Goal runtime/state, tool registry, TUI renderer.
- edge_cases_or_failure_modes: Missing active goal, invalid token budget, exhausted completion budget.
- validation_or_tests: Goal tool tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3108 `file` `packages/coding-agent/src/modes/components/compaction-summary-message.ts`
- cursor: `[_]`
- core_role: TUI components for compaction/handoff summary messages.
- algorithmic_behavior: Renders summary dividers, compaction summaries, handoff documents, and extracts relevant custom message text.
- inputs_outputs_state: Inputs are compaction/custom messages and render width/theme; outputs are markdown/box components lines.
- gates_or_invariants: Handoff extraction isolates document section; divider rendering width-aware.
- dependencies_and_callers: Event/chat rebuild rendering for compaction/handoff messages.
- edge_cases_or_failure_modes: Missing/unknown custom message content, narrow widths.
- validation_or_tests: Compaction/message renderer tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3138 `file` `packages/coding-agent/src/modes/components/plugin-selector.ts`
- cursor: `[_]`
- core_role: TUI plugin selection component.
- algorithmic_behavior: Wraps `SelectList` in a bordered container, maps plugin items to labels/details, handles selection/cancel, and splits plugin IDs.
- inputs_outputs_state: Inputs are plugin items/callbacks/key input; outputs are selected plugin/cancel callbacks and render lines.
- gates_or_invariants: Plugin ID parsing expects `name@marketplace` with optional scope.
- dependencies_and_callers: Marketplace TUI commands/setup flows.
- edge_cases_or_failure_modes: Invalid plugin IDs, empty lists, long labels.
- validation_or_tests: Selector/navigation and marketplace tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3168 `file` `packages/coding-agent/src/modes/controllers/event-controller.ts`
- cursor: `[_]`
- core_role: Interactive mode session-event to TUI-state controller.
- algorithmic_behavior: Subscribes to agent events, manages streaming assistant components, grouped read previews, tool execution blocks, args reveal, TTS, pinned errors, auto-compaction/retry loaders, todo updates, IRC card expiry, and idle compaction scheduling.
- inputs_outputs_state: Inputs are `AgentSessionEvent`s and interactive context; outputs are chat/status/editor mutations, pending tool map changes, vocalizer calls, render requests.
- gates_or_invariants: Transcript anchors reset on session switch; read grouping breaks on visible assistant content; pending tools sealed on abort/error; IRC cards only removed while in live region; resolve plan approval triggers plan handler.
- dependencies_and_callers: `InteractiveMode`, `ToolExecutionComponent`, `AssistantMessageComponent`, settings, TTS vocalizer, compaction UI.
- edge_cases_or_failure_modes: Superseded `agent_end`, partial JSON args reveal, silent abort suppression, background async tools, repeated job poll displacement, duplicate custom messages.
- validation_or_tests: Event-controller args reveal, copy selector, task render, and issue regression tests cover key behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3198 `file` `packages/coding-agent/src/modes/utils/tools-markdown.ts`
- cursor: `[_]`
- core_role: Markdown table builder for available tools.
- algorithmic_behavior: Escapes table cells and renders tool names/descriptions into markdown.
- inputs_outputs_state: Inputs are tool bindings; output is markdown string.
- gates_or_invariants: Pipe/newline characters escaped/replaced to preserve table shape.
- dependencies_and_callers: Prompt/UI helpers that display tool lists.
- edge_cases_or_failure_modes: Tool descriptions with pipes/newlines.
- validation_or_tests: Prompt/tool markdown tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3228 `file` `packages/coding-agent/src/web/scrapers/brew.ts`
- cursor: `[_]`
- core_role: Special web scraper for Homebrew formula/cask pages.
- algorithmic_behavior: Fetches Brew JSON/page data, extracts formula/cask metadata and install counts, and builds a rendered result.
- inputs_outputs_state: Inputs are Brew URL, timeout, abort signal; outputs are `RenderResult` markdown/text.
- gates_or_invariants: 30-day install analytics parsed when present.
- dependencies_and_callers: Web scraper dispatcher, `loadPage`, `buildResult`, `formatNumber`.
- edge_cases_or_failure_modes: Formula vs cask shape differences, missing analytics, fetch timeout.
- validation_or_tests: Package registry scraper tests cover web scrapers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3258 `file` `packages/coding-agent/src/web/scrapers/mastodon.ts`
- cursor: `[_]`
- core_role: Special web scraper for Mastodon statuses/accounts.
- algorithmic_behavior: Detects Mastodon instance, loads API/page data, formats status/account content, media attachments, boosts, counts, and dates into markdown.
- inputs_outputs_state: Inputs are Mastodon URL, timeout, abort signal; outputs are rendered account/status result.
- gates_or_invariants: Instance check uses well-known/node info; HTML converted to basic markdown; counts formatted.
- dependencies_and_callers: Web scraper dispatcher, `tryParseJson`, `loadPage`.
- edge_cases_or_failure_modes: Non-Mastodon host, private/deleted status, missing account fields/media, malformed JSON.
- validation_or_tests: Web scraper tests likely cover package registries more than Mastodon.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3288 `file` `packages/coding-agent/src/web/scrapers/spotify.ts`
- cursor: `[_]`
- core_role: Special web scraper for Spotify URLs.
- algorithmic_behavior: Parses OpenGraph HTML, fetches oEmbed, infers content type, formats title/author/duration/thumbnail/embed metadata.
- inputs_outputs_state: Inputs are Spotify URL, timeout, abort signal; outputs are rendered media result.
- gates_or_invariants: Content type derived from URL path; duration formatted when available.
- dependencies_and_callers: Web scraper dispatcher, `loadPage`, `buildResult`.
- edge_cases_or_failure_modes: Missing oEmbed fields, unknown content type, private/unavailable content.
- validation_or_tests: Web scraper tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3318 `file` `packages/coding-agent/test/modes/components/copy-selector.test.ts`
- cursor: `[_]`
- core_role: Copy selector component tests.
- algorithmic_behavior: Simulates selector state/input and verifies copied selections/labels.
- inputs_outputs_state: Inputs are selectable items/key events; outputs are selected/copied values.
- gates_or_invariants: Copy selector navigation/selection must remain deterministic.
- dependencies_and_callers: Mode component copy selector.
- edge_cases_or_failure_modes: Empty selection, cancel, long labels.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3348 `file` `packages/coding-agent/test/modes/controllers/event-controller-args-reveal.test.ts`
- cursor: `[_]`
- core_role: Event-controller partial args reveal regression tests.
- algorithmic_behavior: Drives streaming tool-call events and asserts partial JSON args remain visible and correctly revealed.
- inputs_outputs_state: Inputs are assistant/tool-call update events with partial args; outputs are pending tool component render args.
- gates_or_invariants: Preview-only `partialJson` must be preserved through live and rebuilt render paths.
- dependencies_and_callers: `EventController`, `ToolArgsRevealController`, tool execution component.
- edge_cases_or_failure_modes: JSON object not closed, custom wire names, large streamed args.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3378 `file` `packages/coding-agent/test/tools/web-scrapers/package-registries.test.ts`
- cursor: `[_]`
- core_role: Web scraper package registry tests.
- algorithmic_behavior: Mocks package registry pages/API responses and verifies scraper output for package metadata.
- inputs_outputs_state: Inputs are registry URLs and fake HTTP responses; outputs are markdown/render results.
- gates_or_invariants: Registry-specific handlers must not fall through incorrectly.
- dependencies_and_callers: Web scraper dispatcher and package handlers.
- edge_cases_or_failure_modes: Missing fields, fetch errors, package not found.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3408 `file` `packages/collab-web/src/tool-render/tools/bash.tsx`
- cursor: `[_]`
- core_role: Collab web renderer for bash tool calls/results.
- algorithmic_behavior: Builds shell-safe env prefix, detects async details/artifact notices, renders command summary, badges, text/images, cwd/exit metadata.
- inputs_outputs_state: Inputs are bash args/result/details; outputs are React summary/body nodes.
- gates_or_invariants: Env tokens shell-quoted unless safe; artifact notice recognized as `artifact://` ID; invalid args render fallback.
- dependencies_and_callers: Collab `ToolView` registry and parts/util helpers.
- edge_cases_or_failure_modes: Non-record env/details, long commands/output, async running/completed/failed state.
- validation_or_tests: Collab renderer tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3438 `file` `packages/mnemopi/src/core/beam/helpers.ts`
- cursor: `[_]`
- core_role: Helper algorithms for Mnemopi beam search/recall.
- algorithmic_behavior: Provides scoring, normalization, candidate manipulation, and utility helpers for beam-style memory retrieval.
- inputs_outputs_state: Inputs are candidate memories/scores/config; outputs are ranked/filtered helper results.
- gates_or_invariants: Score math and filtering must be stable for recall determinism.
- dependencies_and_callers: Mnemopi core beam search modules.
- edge_cases_or_failure_modes: Empty candidates, tied scores, malformed metadata.
- validation_or_tests: Mnemopi tests cover recall/vector behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3468 `file` `packages/stats/src/client/routes/OverviewRoute.tsx`
- cursor: `[_]`
- core_role: Stats dashboard overview route.
- algorithmic_behavior: Fetches overview stats/recent requests, memoizes chart/table data, renders metrics, line chart, recent request table, and loading/error boundaries.
- inputs_outputs_state: Inputs are active flag, time range, refresh trigger, API data; outputs are React UI and request-click callbacks.
- gates_or_invariants: Uses `useResource` for async state; chart theme adapts to system theme; inactive route can suppress fetch/render.
- dependencies_and_callers: Stats client router, API/data formatters, Chart.js components.
- edge_cases_or_failure_modes: Empty data, failed API, theme changes, refresh races.
- validation_or_tests: Stats client tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3498 `file` `python/robomp/web/src/components/Stats.tsx`
- cursor: `[_]`
- core_role: Robomp dashboard event-state stats component.
- algorithmic_behavior: Reads status resource event counts and renders cards for ordered event states with accent colors.
- inputs_outputs_state: Inputs are `statusResource()?.stats.events`; outputs are Solid JSX counters.
- gates_or_invariants: Missing counts default to zero; order fixed by `EVENT_STATE_ORDER`.
- dependencies_and_callers: `state.ts`, `types.ts`, app dashboard.
- edge_cases_or_failure_modes: Unknown event states ignored; loading state shows zeroes.
- validation_or_tests: Web UI not directly tested in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3528 `file` `packages/coding-agent/src/extensibility/plugins/marketplace/manager.ts`
- cursor: `[_]`
- core_role: Plugin marketplace manager.
- algorithmic_behavior: Adds/removes/updates marketplace catalogs, lists available plugins, installs/uninstalls/enables/upgrades plugins across user/project scopes, caches plugin sources, writes embedded LSP config, compares versions, and clears plugin caches.
- inputs_outputs_state: Inputs are marketplace sources/catalogs, plugin IDs, scope/force options, registries/cache dirs; outputs are registry entries, installed plugin summaries, cached plugin dirs, update lists.
- gates_or_invariants: Duplicate marketplace names rejected; catalog rename drift blocks update; URL marketplaces cannot install relative plugin sources; project installs shadow enabled user installs; shared install paths deleted only when unreferenced.
- dependencies_and_callers: Marketplace slash/TUI helpers, plugin discovery, cache/fetcher/source-resolver/registry helpers.
- edge_cases_or_failure_modes: Installed in both scopes requires explicit scope; disabled state preserved on reinstall; stale refresh failures swallowed; semver compare falls back to inequality.
- validation_or_tests: ACP marketplace tests and extension/plugin tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3558 `file` `packages/coding-agent/src/modes/setup-wizard/scenes/splash.ts`
- cursor: `[_]`
- core_role: Setup wizard splash animation renderer.
- algorithmic_behavior: Renders starfield/sky/water/logo frames, clamps/centers lines, applies gradient shine, and falls back to compact splash for small terminal sizes.
- inputs_outputs_state: Inputs are width/height/elapsedMs; outputs are terminal line arrays.
- gates_or_invariants: Min scene size 56x22; tick 33 ms; splash duration 2600 ms; lines truncated to width.
- dependencies_and_callers: Setup wizard scene runner, theme/welcome logo.
- edge_cases_or_failure_modes: Narrow/short terminals, ANSI width, animation phase boundaries.
- validation_or_tests: TUI setup tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3588 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/edge-routing.ts`
- cursor: `[_]`
- core_role: ASCII graph edge direction/path/label routing.
- algorithmic_behavior: Determines start/end directions, handles self references, calls pathfinder, merges paths, computes label lines/width, and direction comparisons/opposites.
- inputs_outputs_state: Inputs are graph layout, edge endpoints/labels/direction; outputs are edge path coordinates and label placement.
- gates_or_invariants: Direction chosen from relative node positions/effective graph direction; label width uses display width.
- dependencies_and_callers: Mermaid ASCII renderer grid/pathfinder/types.
- edge_cases_or_failure_modes: Self-edges, reversed graph direction, overlapping paths, multi-cell labels.
- validation_or_tests: Mermaid ASCII rendering tests likely.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3618 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/state.ts`
- cursor: `[_]`
- core_role: ASCII renderers for Mermaid state start/end shapes.
- algorithmic_behavior: Renders start/end state circles/targets on a canvas and maps connection directions to border/corner glyphs.
- inputs_outputs_state: Inputs are shape dimensions/options/directions; outputs are canvas glyphs.
- gates_or_invariants: Direction equality via edge-routing helpers; canvas dimensions fixed by shape renderer contract.
- dependencies_and_callers: Mermaid ASCII shape registry/canvas/types.
- edge_cases_or_failure_modes: Incoming/outgoing edge direction combinations, tiny dimensions.
- validation_or_tests: Mermaid ASCII shape rendering tests likely.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 121 item evidence headings above
- missing_items: none detected
- duplicate_items: none detected
- final_worker_status: `complete`