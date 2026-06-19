# agent_28 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-028 `directory` `packages/coding-agent`
- cursor: `[_]`
- core_role: Primary CLI application package; recursively contains session runtime, TUI modes, tool execution, MCP/SSH/web integrations, workflow loader, extension/skill discovery, edit application, eval bridges, and tests.
- algorithmic_behavior: Coordinates user turns through `src/session`, interactive surfaces through `src/modes`/`src/tui`, tool adapters through `src/tools`, provider/model resolution through config and catalog imports, and integration surfaces such as MCP transports, web search/scrapers, workflow DSL loading, commit helpers, and async subagents.
- inputs_outputs_state: Inputs are CLI args, settings, session transcripts, model/provider streams, file system/workspace state, tool arguments, MCP messages, SSH host configs, and workflow artifacts; outputs are rendered TUI frames, session JSONL/artifacts, tool results, model messages, logs via centralized logger, and command exit behavior.
- gates_or_invariants: AGENTS rules apply here: no `console.*` in coding-agent runtime paths, static prompt `.md` imports, no dynamic type imports, ES `#private`, Bun-first APIs, sanitized TUI output, worker-host entry contract for compiled binaries.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-ai`, `pi-agent`, `pi-catalog`, `pi-tui`, `pi-utils`, native packages, Bun, SQLite, MCP, web fetchers, and command registry entrypoints; called by `omp` CLI and tests under `packages/coding-agent/test`.
- edge_cases_or_failure_modes: Compiled-binary worker entry routing, terminal rendering corruption from unsanitized output, model/provider auth failures, aborted tools, stale session state, workflow import cycles, MCP auth refresh, SSH ControlMaster compatibility, and extension/skill collisions.
- validation_or_tests: Extensive recursive test tree under `packages/coding-agent/test` plus source-local tests such as `src/eval/__tests__`; assigned item set includes representative regressions for model resolver, web search, MCP auth, SSH, workflow loader, edit guards, TUI renderers, and shutdown.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-058 `file` `docs/natives-architecture.md`
- cursor: `[_]`
- core_role: Architecture/runtime documentation for `@oh-my-pi/pi-natives` native addon loading and packaging.
- algorithmic_behavior: Describes the ESM loader/native addon split, optional platform leaf packages, embedded addon extraction for bundled binaries, version sentinel checks, candidate path resolution, CPU variants, Windows staging, and fallback/error flow.
- inputs_outputs_state: Inputs are runtime platform/arch/libc, package install layout, embedded artifacts, native addon version metadata, and filesystem extraction state; outputs are a loaded native binding or actionable load diagnostics.
- gates_or_invariants: Native ABI/version sentinel must match; platform package choice must be deterministic; compiled binary extraction must avoid stale or incompatible addons.
- dependencies_and_callers: Documents `packages/natives`, `crates/pi-natives`, package build scripts, and runtime import paths used by coding-agent/native consumers.
- edge_cases_or_failure_modes: Missing optional package, wrong CPU/libc variant, stale embedded addon, Windows file locking/staging, unsupported platform, and native load exceptions.
- validation_or_tests: Corroborated by `packages/natives/test/native.test.ts` and native build/embed scripts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-088 `file` `scripts/ci-release-build-binaries.ts`
- cursor: `[_]`
- core_role: CI release workflow script for compiling platform binaries and staging generated runtime assets.
- algorithmic_behavior: Selects targets from `--targets`/`RELEASE_TARGETS`, generates stats/docs/MuPDF/native embedded artifacts, invokes Bun compile per target, applies Darwin signing, and resets generated artifacts in `finally`.
- inputs_outputs_state: Inputs are target selectors, env vars, package sources, embedded artifact generators, and build output directory; outputs are release binaries and transient generated asset state.
- gates_or_invariants: Always cleans generated artifacts; target list must be recognized; release build must include required embedded runtime assets before compiling.
- dependencies_and_callers: Depends on Bun shell/build commands, package build scripts, native/doc/stats generators, and CI release pipeline.
- edge_cases_or_failure_modes: Unknown target, failed artifact generation, signing failure, compile failure, or cleanup failure after partial builds.
- validation_or_tests: CI release path plus smoke install tests cover compiled binary worker/artifact behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-118 `directory` `crates/pi-ast/src`
- cursor: `[_]`
- core_role: Rust tree-sitter/ast-grep core for syntax summarization, block range detection, syntactic boundary lookup, and structural search/edit.
- algorithmic_behavior: `summary.rs` builds an elidable syntax forest and BFS-expands nodes to a visible-line budget; `block.rs` finds block ranges/enclosing boundaries using tree-sitter points; `ops.rs` compiles ast-grep patterns/rewrites, walks files, validates overlap, and applies edits in reverse; `language/` maps languages to parsers.
- inputs_outputs_state: Inputs are source text, language hints/extensions, line windows, search patterns, rewrite rules, root paths/globs; outputs are summaries, block ranges, matches, edits, and language parse metadata.
- gates_or_invariants: Unsupported/empty/syntax-error sources fall back safely; block queries use 1-indexed lines and reject continuation/closing delimiter/error nodes; edits must not overlap.
- dependencies_and_callers: Depends on tree-sitter grammars, ast-grep, ignore/globset; called through native bindings by coding-agent file/search/edit tools.
- edge_cases_or_failure_modes: Zero-width grammar traps, malformed patterns, unknown languages, syntax errors, overlapping edits, ignored files, huge sources, and off-window boundary translation.
- validation_or_tests: Covered indirectly by native tests for summarize/blockRange/ast edit and by coding-agent tools using syntactic previews.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-148 `directory` `packages/snapcompact/src`
- cursor: `[_]`
- core_role: Deterministic conversation compaction package that turns discarded transcript history into text summaries plus image frames for provider-aware preservation.
- algorithmic_behavior: `snapcompact.ts` serializes messages/tool calls, normalizes unsupported glyphs, renders PNG frames, selects provider/model shapes, enforces image budgets, keeps overflow text tails, and returns compacted preserve data; prompts define summary/file-operation text templates.
- inputs_outputs_state: Inputs are transcript entries, provider/model identity, previous preserve data, first kept entry id, and options; outputs are summary text, frame images, details, and updated preserve data.
- gates_or_invariants: Validates `firstKeptEntryId`; pins first frame when evicting if possible; obeys provider image budget; folds controls/combining/surrogates and ANSI away before rendering.
- dependencies_and_callers: Depends on image rendering helpers and provider/model classification; called by agent compaction flows.
- edge_cases_or_failure_modes: Unknown provider shape fallback, oversized tool output/args, frame overflow, invalid kept entry id, unsupported glyphs, empty or mostly tool-result histories.
- validation_or_tests: Research scripts and package tests exercise provider shape/budget behavior; `packages/agent/src/compaction/messages.ts` integrates compaction messaging.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-178 `file` `docs/toolconv/pi-native.md`
- cursor: `[_]`
- core_role: Specification for pi-native tool-call serialization format.
- algorithmic_behavior: Defines XML-flavored `<call:NAME>` blocks, schema-driven coercion, attribute/element/body value forms, repeated elements for arrays, nested objects, and id-less positional result correlation.
- inputs_outputs_state: Inputs are model-generated pi-native syntax and tool schemas; outputs are parsed tool calls/results mapped to internal tool execution.
- gates_or_invariants: Parser must be lenient enough for streaming/model output but schema coercion must preserve tool argument types; result correlation is positional, not call-id based.
- dependencies_and_callers: Used by AI dialect/tool-conversion code and coding-agent tool execution design.
- edge_cases_or_failure_modes: Partial streamed tags, malformed nesting, ambiguous inline body values, arrays/objects with repeated elements, and model output that resembles XML but is not a call.
- validation_or_tests: Related tests live in AI schema/tool wire tests and coding-agent tool rendering/argument reveal tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-208 `file` `packages/stats/build.ts`
- cursor: `[_]`
- core_role: Build-time pipeline for the local stats dashboard client.
- algorithmic_behavior: Scans className strings to seed Tailwind candidates, compiles CSS, builds the React client with Bun, and writes `index.html` with early theme bootstrap.
- inputs_outputs_state: Inputs are client TSX/CSS sources and build config; outputs are static dashboard assets.
- gates_or_invariants: Generated HTML must include theme bootstrap and compiled asset references; class scanning must not miss dynamic CSS candidates needed by the dashboard.
- dependencies_and_callers: Depends on Bun build, Tailwind/PostCSS-style CSS pipeline, and `packages/stats/src/client`.
- edge_cases_or_failure_modes: Missing class candidates, build failure, stale output directory, or theme flash if bootstrap is absent.
- validation_or_tests: Exercised by stats build/packaging and compiled binary asset embedding.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-238 `directory` `packages/ai/test/helpers`
- cursor: `[_]`
- core_role: Test helper infrastructure for AI provider streaming/fetch contracts.
- algorithmic_behavior: `fetch-mock.ts` and `index.ts` provide mock fetch streams/responses, fixtures, and utility wiring so provider tests can assert wire payloads, aborts, retries, and stream events.
- inputs_outputs_state: Inputs are test-defined request/response fixtures; outputs are mocked fetch implementations, captured request payloads, and helper assertions.
- gates_or_invariants: Must preserve provider-facing request shape and signal propagation without global module leakage.
- dependencies_and_callers: Used by `packages/ai/test/*.test.ts` provider and schema tests.
- edge_cases_or_failure_modes: Consumed streams, aborted signals, incorrect mock headers/status, and state leakage between tests.
- validation_or_tests: The helper directory is itself validated by downstream AI tests using it.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-268 `directory` `packages/coding-agent/src/lib`
- cursor: `[_]`
- core_role: Small library-helper area for coding-agent runtime; currently includes `xai-http.ts`.
- algorithmic_behavior: Provides shared HTTP/provider utility behavior for XAI-compatible integrations, isolating request construction/response handling from command/UI code.
- inputs_outputs_state: Inputs are provider HTTP parameters and runtime settings; outputs are normalized HTTP calls or errors.
- gates_or_invariants: Keep provider-specific transport details out of UI/session surfaces.
- dependencies_and_callers: Imported by coding-agent provider/registry paths needing XAI HTTP behavior.
- edge_cases_or_failure_modes: Network failures, auth errors, malformed responses, and abort propagation.
- validation_or_tests: Covered indirectly by provider/model resolver and command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-298 `directory` `packages/coding-agent/test/edit`
- cursor: `[_]`
- core_role: Regression tests for edit snapshot and seen-line guard algorithms.
- algorithmic_behavior: `file-snapshot-store.test.ts` validates snapshot persistence/retrieval semantics; `seen-line-guard.test.ts` validates that edit operations respect previously observed line provenance and detect stale/unseen edits.
- inputs_outputs_state: Inputs are temporary files, snapshots, edit attempts, and line content; outputs are pass/fail assertions about accepted/rejected edit state.
- gates_or_invariants: Edits must be grounded in current/seen file content and avoid silently applying stale context.
- dependencies_and_callers: Tests coding-agent edit/hashline/file snapshot modules used by file edit tools.
- edge_cases_or_failure_modes: File changes between read and edit, missing snapshots, line-number drift, duplicate lines, and stale context.
- validation_or_tests: Directory is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-328 `directory` `packages/stats/src/client`
- cursor: `[_]`
- core_role: React client for local observability dashboard.
- algorithmic_behavior: Routes overview/models/costs/errors/requests/projects/behavior, fetches `/api/*` resources, caches/polls with `useResource`, builds view models for costs/performance/friction/folders, renders Chart.js charts, tables, drawers, and filters.
- inputs_outputs_state: Inputs are stats API JSON, hash route, time range, theme, and document visibility; outputs are dashboard UI state, API errors, charts/tables, and sync actions.
- gates_or_invariants: `useResource` JSON-keys cache entries, aborts prior fetches, limits cache to 64, and skips polling while hidden; API errors become `ApiError`.
- dependencies_and_callers: Bundled by `packages/stats/build.ts`, served by stats server, used by `packages/stats/src/index.ts`.
- edge_cases_or_failure_modes: Hidden-tab polling, stale cache, aborted fetches, empty datasets, API failures, request drawer missing row, and theme mismatch.
- validation_or_tests: Build plus route/view-model behavior; `Panel.tsx` is separately assigned as a presentational child.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-358 `file` `crates/pi-natives/src/glob_util.rs`
- cursor: `[_]`
- core_role: Native-side glob normalization and compilation helper.
- algorithmic_behavior: Normalizes backslashes, prefixes simple recursive patterns with `**/`, preserves patterns with slashes/leading `**`/exact brace unions, closes unbalanced braces, and compiles with literal separators.
- inputs_outputs_state: Inputs are user/tool glob strings; outputs are normalized glob patterns and compiled matchers.
- gates_or_invariants: Must avoid changing already path-qualified or recursive patterns; unbalanced braces are repaired before compilation.
- dependencies_and_callers: Used by pi-natives grep/list/search routines and tests.
- edge_cases_or_failure_modes: Windows separators, unclosed braces, brace unions, literal slash behavior, non-recursive patterns.
- validation_or_tests: Tests cover simple prefixing, unchanged path/recursive patterns, backslash normalization, unclosed braces, and compile success.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-388 `file` `packages/agent/src/append-only-context.ts`
- cursor: `[_]`
- core_role: Provider prompt-cache/append-only context manager.
- algorithmic_behavior: Maintains a stable prefix snapshot for system/tools with fingerprint/version, an append-only log, tail replacement/clear operations, and normalized provider message sync with rolling digest change detection.
- inputs_outputs_state: Inputs are provider messages, model identity, system/tool prefix, compaction state; outputs are append-only snapshots, invalidation decisions, and digest-tracked context state.
- gates_or_invariants: Invalidate on model change, prefix mutation, compaction shortening, or in-place rewrite; append-only entries must remain ordered.
- dependencies_and_callers: Used by agent runtime provider calls and compaction integration.
- edge_cases_or_failure_modes: Compacted arrays shorter than previous, tool-call content changes without length changes, tail replacement, and stale prefix cache.
- validation_or_tests: Covered through agent/session streaming and compaction tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-418 `file` `packages/ai/scripts/proto-extractor.py`
- cursor: `[_]`
- core_role: Utility script that reconstructs `.proto` definitions from generated Buf/protobuf JS bundles.
- algorithmic_behavior: Regex-scans generated file ranges, extracts filtered JSDoc comments, messages, fields, enums, services/methods, oneof/map/repeated/optional flags, scalar type numbers, and emits consolidated proto text with optional `--filter`.
- inputs_outputs_state: Inputs are generated JS bundle files and filters; outputs are `.proto` text or exit status.
- gates_or_invariants: Duplicate type handling and no matching files must fail deterministically; webpack noise is filtered from comments.
- dependencies_and_callers: Used by AI package maintenance around provider protocol definitions.
- edge_cases_or_failure_modes: Duplicate symbols, missing generated markers, webpack comments, unknown scalar encodings, empty filter results.
- validation_or_tests: Manual/script-level validation through generated proto diffs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-448 `file` `packages/ai/test/anthropic-stream-timeout.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Anthropic streaming first-event timeout and retry delay behavior.
- algorithmic_behavior: Builds mocked Anthropic event streams, stalled/rejected requests, abort-aware waiters, and drains microtasks to assert retry behavior and first-event timeout semantics.
- inputs_outputs_state: Inputs are mock streams, errors, abort signals, model/context fixtures; outputs are provider events, retry attempts, and thrown errors/assertions.
- gates_or_invariants: First event timeout should abort/retry only where configured; retry delays must follow provider retry rules without leaking aborted requests.
- dependencies_and_callers: Tests Anthropic provider implementation in `packages/ai`.
- edge_cases_or_failure_modes: No first event, rejected initial request, abort during wait, retry exhaustion, successful retry after stall.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-478 `file` `packages/ai/test/auth-storage-credential-disabled-event.test.ts`
- cursor: `[_]`
- core_role: Tests auth storage subscription events when credentials are disabled.
- algorithmic_behavior: Uses in-memory credential store, expired OAuth fixtures, failed refresh simulation, and `credential_disabled` subscription assertions.
- inputs_outputs_state: Inputs are serialized credentials, provider IDs, refresh failures; outputs are disabled credential state and emitted events.
- gates_or_invariants: Disabled events must fire exactly for credential invalidation paths and not be masked by env credentials.
- dependencies_and_callers: Tests `AuthStorage` and OAuth refresh handling.
- edge_cases_or_failure_modes: Expired token, invalid_grant, missing env suppression, duplicate disable, provider mismatch.
- validation_or_tests: This file validates the auth event contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-508 `file` `packages/ai/test/github-copilot-headers.test.ts`
- cursor: `[_]`
- core_role: Tests GitHub Copilot dynamic header construction and premium model metadata helpers.
- algorithmic_behavior: Exercises initiator inference, override parsing, vision-input detection, premium multiplier lookup, and final dynamic header assembly.
- inputs_outputs_state: Inputs are model IDs, messages with image/text content, env/config overrides; outputs are header objects and helper decisions.
- gates_or_invariants: Header values must be deterministic and not misclassify vision or premium-model state.
- dependencies_and_callers: Tests Copilot provider registry/header code.
- edge_cases_or_failure_modes: Empty override, unknown model, image content nested in messages, provider-specific initiator fallback.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-538 `file` `packages/ai/test/issue-1838-repro.test.ts`
- cursor: `[_]`
- core_role: Regression for Kimi k2.6 historical reasoning preservation across tool calls.
- algorithmic_behavior: Captures OpenAI-completions wire payloads for Moonshot/OpenRouter Kimi models and finds assistant wire messages containing reasoning.
- inputs_outputs_state: Inputs are model fixtures, previous assistant/tool messages, mock SSE; outputs are captured payload assertions.
- gates_or_invariants: Reasoning content must survive tool-call history transformation where provider/model supports it.
- dependencies_and_callers: Tests AI OpenAI-compatible completion adapter and catalog/model identity logic.
- edge_cases_or_failure_modes: Aborted signal, provider-specific Kimi flags, assistant messages with tool calls, missing reasoning fields.
- validation_or_tests: This file is the repro validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-568 `file` `packages/ai/test/null-max-tokens-fallback.test.ts`
- cursor: `[_]`
- core_role: Wire tests for providers when `maxTokens` is null/omitted.
- algorithmic_behavior: Creates completions/responses/Google error fixtures and asserts fallback request shaping rather than sending invalid null token limits.
- inputs_outputs_state: Inputs are contexts with null max token behavior and mock responses; outputs are request payload assertions and provider errors.
- gates_or_invariants: Providers must omit or default `max_tokens`/equivalent fields according to API contract.
- dependencies_and_callers: Tests OpenAI completions, OpenAI responses, and Google provider paths.
- edge_cases_or_failure_modes: API rejecting nulls, provider default differences, streaming SSE response parsing.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-598 `file` `packages/ai/test/openai-responses-parallel-tool-calls.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI Responses stream processing for parallel function-call items.
- algorithmic_behavior: Emits synthetic response stream events with multiple function calls and asserts tool lifecycle aggregation into assistant output.
- inputs_outputs_state: Inputs are stream events and model/context fixtures; outputs are processed assistant messages/tool call events.
- gates_or_invariants: Parallel function calls must preserve IDs/names/arguments and finish independently without clobbering each other.
- dependencies_and_callers: Tests `processResponsesStream` / OpenAI Responses adapter.
- edge_cases_or_failure_modes: Interleaved function-call deltas, missing final item, duplicated IDs, ordering of output items.
- validation_or_tests: This file validates the stream parser contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-628 `file` `packages/ai/test/schema-wire.test.ts`
- cursor: `[_]`
- core_role: Tests schema normalization from Zod/Ark/tool schemas to provider wire schemas.
- algorithmic_behavior: Covers `isZodSchema`, empty-schema normalization, nullable scalar normalization, open-record provider normalizers, nullable union decontamination, undefined-union pruning, and property order.
- inputs_outputs_state: Inputs are Zod/Ark schemas and tool definitions; outputs are normalized JSON schema/wire schema objects.
- gates_or_invariants: Empty object schemas must normalize consistently; nullable/undefined unions must map to provider-acceptable schemas; authored property order should be retained where relevant.
- dependencies_and_callers: Tests AI schema conversion used by tool-calling providers.
- edge_cases_or_failure_modes: Empty schemas, nullable scalars, open records, Ark unions, duplicate normalization paths.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-658 `file` `packages/catalog/src/effort.ts`
- cursor: `[_]`
- core_role: Defines user-facing reasoning effort enum and ordered values.
- algorithmic_behavior: Exports `Effort` values `minimal` through `xhigh` and `THINKING_EFFORTS` in ascending intensity order.
- inputs_outputs_state: Input is effort selection text; output is typed effort value/order used by model config.
- gates_or_invariants: Ordering is semantic and used by selectors/UI; enum strings must stay stable.
- dependencies_and_callers: Imported by catalog/model settings and coding-agent reasoning effort handling.
- edge_cases_or_failure_modes: Unknown effort strings must be rejected by callers; reordering would affect effort comparisons.
- validation_or_tests: Covered by model resolver/config tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-688 `file` `packages/catalog/test/issue-2113-repro.test.ts`
- cursor: `[_]`
- core_role: Regression for Moonshot Kimi k2.6 discovery and wire format.
- algorithmic_behavior: Builds Moonshot Kimi model fixtures, mock SSE response, and a `runHiTurn` helper to assert reasoning-capable model discovery/wire payload behavior.
- inputs_outputs_state: Inputs are catalog model IDs/reasoning flags, context, SSE chunks; outputs are provider messages and payload assertions.
- gates_or_invariants: Kimi k2.6 reasoning metadata and OpenAI-compatible wire format must align.
- dependencies_and_callers: Tests catalog identity/discovery plus AI OpenAI-compatible adapter.
- edge_cases_or_failure_modes: Reasoning disabled/enabled variants, missing model policy, malformed SSE.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-718 `file` `packages/coding-agent/scripts/build-binary.ts`
- cursor: `[_]`
- core_role: Local compiled `omp` binary build script.
- algorithmic_behavior: Embeds stats/docs/native/MuPDF artifacts, defines pinned Transformers.js version, externalizes native-heavy optional dependencies, includes legacy extension entrypoints, compiles with Bun, and resets artifacts in nested `finally`.
- inputs_outputs_state: Inputs are CLI package source, generated assets, Bun compile target/options; outputs are a compiled local binary and restored working tree asset state.
- gates_or_invariants: Generated embedded artifacts must exist during compile and be cleaned afterward; worker host contract must remain compatible with compiled single-entry CLI.
- dependencies_and_callers: Depends on Bun, package build scripts, native/docs/stats artifact generators.
- edge_cases_or_failure_modes: Missing embed asset, Bun compile failure, optional native dependency bundling, stale generated files after failure.
- validation_or_tests: Smoke probe `omp --smoke-test` and install CI validate compiled binary behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-748 `file` `packages/coding-agent/test/agent-dashboard-create-editor.test.ts`
- cursor: `[_]`
- core_role: Tests AgentDashboard create editor, layout, and tab navigation.
- algorithmic_behavior: Stubs stdout geometry, types text into dashboard, and asserts editor rendering/layout/navigation behavior under different terminal widths.
- inputs_outputs_state: Inputs are temp cwd, synthetic keystrokes, stdout columns/rows; outputs are rendered dashboard text and active tab/editor state.
- gates_or_invariants: Editor text must fit and dashboard layout must preserve tab navigation semantics.
- dependencies_and_callers: Tests coding-agent dashboard/TUI components.
- edge_cases_or_failure_modes: Narrow terminal geometry, ANSI stripping, tab focus changes, multi-line typed content.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-778 `file` `packages/coding-agent/test/agent-session-resolve-reminder.test.ts`
- cursor: `[_]`
- core_role: Tests session resolve reminder behavior.
- algorithmic_behavior: Creates agent session conditions and asserts reminder injection/selection logic when unresolved state needs surfacing.
- inputs_outputs_state: Inputs are session messages/state; outputs are reminder messages or absence thereof.
- gates_or_invariants: Reminder should appear only when unresolved work requires it and should not duplicate stale reminders.
- dependencies_and_callers: Tests `AgentSession` reminder logic.
- edge_cases_or_failure_modes: Empty session, already-resolved state, repeated reminders, streaming boundaries.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-808 `file` `packages/coding-agent/test/autoresearch-tools.test.ts`
- cursor: `[_]`
- core_role: Contract tests for autoresearch extension tools.
- algorithmic_behavior: Tests `init_experiment`, `run_experiment`, `log_experiment`, and `update_notes` using temp repos, dashboard stubs, harness stubs, completed run seeds, branch checkout, and markdown note updates.
- inputs_outputs_state: Inputs are tool arguments, cwd/git repo state, harness outputs, notes text; outputs are tool content blocks, run records, dashboard refresh state, and notes mutations.
- gates_or_invariants: Active session/storage required, git/run state must be coherent, notes updates append under `## Ideas` or replace body as specified.
- dependencies_and_callers: Tests `packages/coding-agent/src/autoresearch/tools/*`.
- edge_cases_or_failure_modes: Missing active session, bad repo state, failed harness, absent notes headings, branch checkout, duplicate run metadata.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-838 `file` `packages/coding-agent/test/config-spacing.test.ts`
- cursor: `[_]`
- core_role: Tests indentation resolver configuration behavior.
- algorithmic_behavior: Exercises indentation resolution for config/editor contexts so generated edits respect spacing rules.
- inputs_outputs_state: Inputs are config values/source text; outputs are indentation choices.
- gates_or_invariants: Resolved indentation must be deterministic and compatible with file style.
- dependencies_and_callers: Tests coding-agent config/edit formatting helpers.
- edge_cases_or_failure_modes: Tabs vs spaces, missing config, ambiguous indentation.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-868 `file` `packages/coding-agent/test/git-url.test.ts`
- cursor: `[_]`
- core_role: Tests Git URL/spec parsing.
- algorithmic_behavior: Validates `parseGitUrl` and `isGitSpec` against HTTPS, SSH, scp-like, owner/repo shorthand, branch/path selectors, and invalid strings.
- inputs_outputs_state: Inputs are user-supplied git specs; outputs are parsed repo URL/ref/path metadata or boolean classification.
- gates_or_invariants: Must not misclassify ordinary paths/URLs as clone specs; ref/path parsing must be stable.
- dependencies_and_callers: Tests coding-agent git/source loading helpers.
- edge_cases_or_failure_modes: Colons in paths, branch suffixes, GitHub shorthand, invalid hosts, trailing slashes.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-898 `file` `packages/coding-agent/test/interactive-mode-editor-component.test.ts`
- cursor: `[_]`
- core_role: Tests custom editor component injection in interactive mode.
- algorithmic_behavior: Defines a test modal editor class and asserts `InteractiveMode.setEditorComponent` swaps editor implementation correctly.
- inputs_outputs_state: Inputs are component class and interactive mode instance; outputs are active editor component behavior.
- gates_or_invariants: Editor replacement must be explicit and scoped, not leak unexpectedly.
- dependencies_and_callers: Tests interactive mode TUI editor integration.
- edge_cases_or_failure_modes: Multiple replacements, custom editor subclass, modal lifecycle.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-928 `file` `packages/coding-agent/test/issue-905-repro.test.ts`
- cursor: `[_]`
- core_role: Regression for `omp models` surfacing extension-registered providers.
- algorithmic_behavior: Sets up extension provider registration and invokes models listing path to ensure extension models are included.
- inputs_outputs_state: Inputs are extension/provider fixtures and command context; outputs are listed model/provider entries.
- gates_or_invariants: Extension-registered providers must participate in model discovery/listing.
- dependencies_and_callers: Tests coding-agent extension model registry and CLI models command.
- edge_cases_or_failure_modes: Provider not loaded, extension registration order, missing model metadata.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-958 `file` `packages/coding-agent/test/mcp-command-reauth.test.ts`
- cursor: `[_]`
- core_role: Tests `/mcp auth` command reauthorization flow.
- algorithmic_behavior: Stubs auth storage and MCP manager, expands env URLs, simulates auth errors, and asserts command behavior for reauth prompts/storage updates.
- inputs_outputs_state: Inputs are MCP server config, env vars, auth storage records, command args; outputs are runtime messages and credential state.
- gates_or_invariants: Raw server URLs must expand safely; auth errors trigger reauth; env/project dirs restored after tests.
- dependencies_and_callers: Tests MCP command controller and auth storage.
- edge_cases_or_failure_modes: Missing env var, auth failure text, fallback agent dir, manager override behavior.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-988 `file` `packages/coding-agent/test/model-resolver.test.ts`
- cursor: `[_]`
- core_role: Comprehensive tests for model selector parsing and resolution.
- algorithmic_behavior: Exercises default model picking, role value resolution, pattern parsing, agent pattern resolution, string resolution, override/CLI scope parsing, role aliases, `@upstream` routing selectors, available-model filters, and effort-tier aliases.
- inputs_outputs_state: Inputs are mock catalog/openrouter/codex models, canonical registry fixtures, selector strings, enabled patterns; outputs are resolved model/provider/role/effort choices or errors.
- gates_or_invariants: Provider/model ambiguity must be resolved predictably; aliases and scopes must not select disabled/unavailable models.
- dependencies_and_callers: Tests coding-agent model resolver and catalog integration.
- edge_cases_or_failure_modes: Overlapping model IDs across providers, fuzzy aliases, canonical variants, unavailable providers, invalid selectors, effort suffixes.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1018 `file` `packages/coding-agent/test/repro-issue-2600-shutdown-timeout.test.ts`
- cursor: `[_]`
- core_role: Regression for session shutdown handler timeout.
- algorithmic_behavior: Uses a hanging extension source and asserts session shutdown handling times out rather than blocking indefinitely.
- inputs_outputs_state: Inputs are extension code and shutdown lifecycle; outputs are completed shutdown/error handling within timeout.
- gates_or_invariants: Extension shutdown hooks cannot hang session disposal forever.
- dependencies_and_callers: Tests coding-agent extension/session shutdown lifecycle.
- edge_cases_or_failure_modes: Hanging promise, cleanup timeout, extension disposal ordering.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1048 `file` `packages/coding-agent/test/session-focus-controller.test.ts`
- cursor: `[_]`
- core_role: Tests focus management across main/subagent sessions.
- algorithmic_behavior: Builds session stubs, registry entries, async flushing, and asserts focus transitions depending on streaming state, parent relations, and registered subagents.
- inputs_outputs_state: Inputs are session registry state and focus events; outputs are active focused session IDs and callbacks.
- gates_or_invariants: Streaming sessions should not be disrupted incorrectly; parent/subagent focus rules must be stable.
- dependencies_and_callers: Tests `SessionFocusController`, `AgentRegistry`, and session UI coordination.
- edge_cases_or_failure_modes: Streaming session, detached subagent, parent-child registration, async focus changes.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1078 `file` `packages/coding-agent/test/status-line-path.test.ts`
- cursor: `[_]`
- core_role: Tests status-line path segment rendering.
- algorithmic_behavior: Builds path segment contexts with project dir/cwd and asserts shortening/path display behavior.
- inputs_outputs_state: Inputs are cwd/project/home paths and segment context; outputs are rendered status text.
- gates_or_invariants: Paths must be shortened safely and reflect project-relative context.
- dependencies_and_callers: Tests TUI status line renderer.
- edge_cases_or_failure_modes: Home directory abbreviation, project root, nested cwd, long paths.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1108 `file` `packages/coding-agent/test/tool-args-reveal.test.ts`
- cursor: `[_]`
- core_role: Tests progressive reveal of tool arguments in the TUI.
- algorithmic_behavior: Uses a recording args component/controller, partial JSON frames, and animation drains to assert smooth/instant argument preview behavior.
- inputs_outputs_state: Inputs are streamed partial tool-call frames; outputs are rendered arg fragments and render requests.
- gates_or_invariants: Preview must handle partial JSON before parsed args are complete and preserve reveal state.
- dependencies_and_callers: Tests tool execution/TUI render controller.
- edge_cases_or_failure_modes: Partial JSON boundaries, smooth animation disabled/enabled, repeated frames.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1138 `file` `packages/collab-web/test/codec.test.ts`
- cursor: `[_]`
- core_role: Tests collaborative web codec encryption/decryption vectors.
- algorithmic_behavior: Uses fixed key/sealed vectors to assert codec round-trips and compatibility with expected sealed payload format.
- inputs_outputs_state: Inputs are base64/url-safe key and sealed payload fixtures; outputs are decoded/plain or encoded/sealed values.
- gates_or_invariants: Codec output must remain compatible with existing vectors.
- dependencies_and_callers: Tests collab-web codec module.
- edge_cases_or_failure_modes: Bad key length, corrupt sealed payload, encoding variant mismatch.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1168 `file` `packages/hashline/test/patcher.test.ts`
- cursor: `[_]`
- core_role: Tests hashline patcher snapshot integrity and mandatory provenance.
- algorithmic_behavior: Asserts snapshot tag integrity, mandatory snapshot tag policy, and seen-line provenance around patch application.
- inputs_outputs_state: Inputs are source path/text, patch hunks, snapshot tags; outputs are accepted/rejected patch results.
- gates_or_invariants: Patches must carry valid snapshot/provenance data and not apply against unseen/stale lines.
- dependencies_and_callers: Tests hashline patcher used by coding-agent edit workflow.
- edge_cases_or_failure_modes: Tampered tags, missing tags, stale line provenance, duplicate paths.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1198 `file` `packages/mnemopi/test/degrade-vector.test.ts`
- cursor: `[_]`
- core_role: Tests episodic memory degradation invalidates stored vectors.
- algorithmic_behavior: Creates old ISO timestamps and inspects stored embeddings after degradation to ensure vector state is cleared/recomputed as expected.
- inputs_outputs_state: Inputs are memory records with timestamps/embeddings; outputs are degraded memory state and embedding storage assertions.
- gates_or_invariants: Degraded episodic memories must not retain stale embeddings.
- dependencies_and_callers: Tests mnemopi memory/vector persistence.
- edge_cases_or_failure_modes: Age thresholds, missing embedding, repeated degradation.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1228 `file` `packages/mnemopi/test/provider-all-15-tools.test.ts`
- cursor: `[_]`
- core_role: Tests provider-compatible MCP tool exposure and representative handlers.
- algorithmic_behavior: Collects tool names and asserts all 15 provider-compatible tools exist, then exercises representative handler behavior.
- inputs_outputs_state: Inputs are provider tool registry and handler args; outputs are tool name set and handler results.
- gates_or_invariants: Provider-facing tool count/names must remain stable for compatibility.
- dependencies_and_callers: Tests mnemopi provider MCP integration.
- edge_cases_or_failure_modes: Missing tool, renamed tool, handler schema mismatch.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1258 `file` `packages/natives/test/native.test.ts`
- cursor: `[_]`
- core_role: Broad native package integration contract.
- algorithmic_behavior: Exercises native summarization, block range, language aliases, key parsing, grep/glob/fuzzy search, ast edit, shell/pty, text/html processing, workspace listing, and related binding surfaces.
- inputs_outputs_state: Inputs are fixture source files, glob/search patterns, native API calls; outputs are summaries, matches, edits, PTY/shell results, parsed text/html.
- gates_or_invariants: Native binding must load and each exported operation must preserve expected shape/semantics.
- dependencies_and_callers: Tests `packages/natives` JS facade and `crates/pi-natives`.
- edge_cases_or_failure_modes: Missing binding, unsupported language, glob mismatch, PTY availability, platform variance.
- validation_or_tests: This file is the validation surface for native runtime.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1288 `file` `packages/snapcompact/research/exp16_bestfable.py`
- cursor: `[_]`
- core_role: Research script for snapcompact experimental compression/representation behavior.
- algorithmic_behavior: Runs an experimental fable/encoding pipeline to evaluate compact text/image preservation strategies.
- inputs_outputs_state: Inputs are research text/conversation samples and parameters; outputs are experiment metrics/artifacts.
- gates_or_invariants: Research-only script should not be used as runtime production path.
- dependencies_and_callers: Related to `packages/snapcompact/src`.
- edge_cases_or_failure_modes: Experiment fixture drift, non-deterministic model/research assumptions.
- validation_or_tests: Research evidence, not a package test.
- skip_candidate: `yes: research experiment script, not runtime algorithm despite informing snapcompact design`

### OH_MY_HUMANIZE_MAIN-HZ-1318 `file` `packages/snapcompact/research/snapcompact_qwen_control_intervention.py`
- cursor: `[_]`
- core_role: Research script for Qwen/control interventions in snapcompact evaluation.
- algorithmic_behavior: Compares intervention/control variants for compaction behavior and measures outcomes across research samples.
- inputs_outputs_state: Inputs are model/control settings and sample data; outputs are experiment measurements/logs.
- gates_or_invariants: Experimental assumptions should not be treated as runtime contract.
- dependencies_and_callers: Related to snapcompact research, not imported by runtime source.
- edge_cases_or_failure_modes: Model availability, random/evaluation variance, stale fixtures.
- validation_or_tests: Research output only.
- skip_candidate: `yes: research-only experiment script`

### OH_MY_HUMANIZE_MAIN-HZ-1348 `file` `packages/stats/src/index.ts`
- cursor: `[_]`
- core_role: Stats package public/CLI entrypoint.
- algorithmic_behavior: Exports aggregator/server/db modules and implements stats commands for JSON/summary/server output with sync progress and local dashboard startup.
- inputs_outputs_state: Inputs are CLI flags, local stats database, sync settings; outputs are JSON summaries, terminal summaries, server/dashboard lifecycle.
- gates_or_invariants: CLI output format must match requested mode; sync progress goes to appropriate streams.
- dependencies_and_callers: Depends on stats DB, aggregator, server, client assets; called by `omp stats` and package consumers.
- edge_cases_or_failure_modes: Missing DB, sync failure, server port conflict, no data.
- validation_or_tests: Covered by stats package tests/build and coding-agent stats smoke paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1378 `file` `packages/tui/src/latex-block.ts`
- cursor: `[_]`
- core_role: Display LaTeX parser/layout for terminal block rendering.
- algorithmic_behavior: Parses display math/environment wrappers, splits rows, builds `Box` layouts with width/baseline, renders `\frac` variants with bars, aligns nested boxes/scripts, and delegates simple inline conversion to `latexToUnicode`.
- inputs_outputs_state: Inputs are LaTeX strings; outputs are terminal line arrays from `latexToBlock` or Unicode inline text.
- gates_or_invariants: Box baseline/width math must keep fractions aligned and trimmed; display parser must avoid overlapping lines.
- dependencies_and_callers: Used by TUI markdown/math rendering.
- edge_cases_or_failure_modes: Nested braces, environments, multi-row equations, scripts, malformed LaTeX, non-fraction commands.
- validation_or_tests: Covered by TUI rendering tests and stress oracles.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1408 `file` `packages/tui/test/issue-2034-repro.test.ts`
- cursor: `[_]`
- core_role: Regression for chunking large terminal writes on Windows ConPTY.
- algorithmic_behavior: Builds large full-paint strings and asserts write chunking prevents ConPTY breakage.
- inputs_outputs_state: Inputs are line counts/lengths and terminal output strings; outputs are chunked writes/assertions.
- gates_or_invariants: Windows terminal writes must stay below problematic chunk sizes while preserving bytes/order.
- dependencies_and_callers: Tests TUI renderer/write path.
- edge_cases_or_failure_modes: Huge paints, ESC sequences, Windows-specific terminal behavior.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1438 `file` `packages/tui/test/render-stress-oracles.test.ts`
- cursor: `[_]`
- core_role: Tests render stress oracle helpers.
- algorithmic_behavior: Uses ESC/BEL fixture strings to validate oracle helpers for terminal output stress comparisons.
- inputs_outputs_state: Inputs are ANSI/OSC-containing output strings; outputs are normalized/oracle assertions.
- gates_or_invariants: Oracle helpers must preserve semantically meaningful terminal controls and detect invalid output.
- dependencies_and_callers: Supports TUI renderer regression tests.
- edge_cases_or_failure_modes: ANSI split points, BEL/OSC sequences, large output.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1468 `file` `packages/typescript-edit-benchmark/src/bun-imports.d.ts`
- cursor: `[_]`
- core_role: Type declaration for imported `.tar.gz` assets.
- algorithmic_behavior: Declares a module pattern so TypeScript can type asset imports as strings.
- inputs_outputs_state: Inputs are `.tar.gz` import specifiers; output is compile-time default `string` type.
- gates_or_invariants: Declaration must remain broad enough for benchmark asset imports.
- dependencies_and_callers: TypeScript edit benchmark build/typecheck.
- edge_cases_or_failure_modes: Missing declaration causes TS import errors.
- validation_or_tests: Typecheck/build only.
- skip_candidate: `yes: compile-time declaration stub only, no runtime core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1498 `file` `packages/utils/src/module-timer.ts`
- cursor: `[_]`
- core_role: Bun preload module-load timing instrumentation.
- algorithmic_behavior: When `PI_TIMING` is set, installs a Bun plugin that instruments TS/TSX source with start/end markers, records static import edges via `Bun.resolveSync`, and pushes inclusive/body timings into a global buffer.
- inputs_outputs_state: Inputs are module paths/source contents and env `PI_TIMING`; outputs are module load timing records with path/start/duration/body/imports.
- gates_or_invariants: TS/TSX-only interception avoids breaking CJS `.js`; shebangs are preserved; resolver errors are observational and not swallowed from real runtime.
- dependencies_and_callers: Depends on Bun plugin API and `timing-buffer`; drained by logger timing output.
- edge_cases_or_failure_modes: Modules throwing before completion marker, top-level await, dynamic imports, compiled binary where onLoad never fires, import regex false positives.
- validation_or_tests: Exercised in dev timing runs; documented coverage limits in file comments.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1528 `file` `packages/utils/test/path-tree.test.ts`
- cursor: `[_]`
- core_role: Tests grouped path formatting helper.
- algorithmic_behavior: Asserts `formatGroupedPaths` compacts path lists into readable tree/grouped output.
- inputs_outputs_state: Inputs are path arrays; outputs are formatted grouped strings.
- gates_or_invariants: Formatting should preserve path identity while reducing repetition.
- dependencies_and_callers: Tests utils path-tree helper used in user-facing summaries.
- edge_cases_or_failure_modes: Shared prefixes, single files, empty list, nested paths.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1558 `file` `python/robomp/src/github_events.py`
- cursor: `[_]`
- core_role: Typed GitHub webhook parsing, authorization, rate-limit, and dispatch routing.
- algorithmic_behavior: Verifies `X-Hub-Signature-256` HMAC, extracts repo/submitter/mentions, detects bots/reviewer bots, parses maintainer directives/pragmas, routes issues/comments/PR/review events to queue tasks or skips with reasons.
- inputs_outputs_state: Inputs are event type, webhook payload, allowlist, bot login, maintainers, reviewer bots, PR issue resolver; output is immutable `RouteDecision`.
- gates_or_invariants: Repo must be allowlisted; PR comments on incoming contributor PRs are skipped; implementation authorization is maintainer/OWNER-gated; HMAC compare is constant-time.
- dependencies_and_callers: Depends on `robomp.db.issue_key` and `robomp.pragmas.parse_pragmas`; called by webhook receiver/queue.
- edge_cases_or_failure_modes: Missing repo/number, draft/bot PRs, bot/self comments, unresolved PR-to-issue mapping fallback, malformed signature, reviewer bot directives.
- validation_or_tests: Covered by robomp event routing tests; assigned queue shutdown tests validate downstream worker behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1588 `file` `python/robomp/tests/test_queue_shutdown.py`
- cursor: `[_]`
- core_role: Tests WorkerPool graceful shutdown drain/kill behavior.
- algorithmic_behavior: Directly creates `WorkerPool`, stub GitHub/sandbox/git transport, in-flight tasks, cancel hooks, and assertions around `stop()` drain windows and `_run_event` shutdown branches.
- inputs_outputs_state: Inputs are settings/db rows/tasks/events; outputs are task cancellation state and DB event states/errors.
- gates_or_invariants: Drain should allow short tasks; kill hooks fire after timeout; hookless in-flight tasks must be cancelled; only shutdown-cancelled deliveries suppress failure marking.
- dependencies_and_callers: Tests `robomp.queue.WorkerPool`, `Database`, `SlotPool`.
- edge_cases_or_failure_modes: Non-root semaphore concurrency, slow pre-hook task, genuine failure during drain, shutdown-cancelled delivery, DB row left running for reset.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1618 `directory` `packages/coding-agent/src/eval/__tests__`
- cursor: `[_]`
- core_role: Source-local tests for JS/eval bridge, context manager, kernels, budget, completion, helpers, and timeouts.
- algorithmic_behavior: Exercises agent bridge calls, bridge timeout/idle timeout, budget enforcement, completion bridge protocol, local-root helper resolution, JS context manager lifecycle, kernel spawn, and prelude agent behavior.
- inputs_outputs_state: Inputs are eval code snippets, bridge messages, budgets/deadlines, local roots; outputs are eval results, bridge events, spawned kernel state, timeout/cancel assertions.
- gates_or_invariants: Eval bridge must isolate context, respect budgets/timeouts, and cleanly propagate completion/status events.
- dependencies_and_callers: Tests `packages/coding-agent/src/eval` and JS/Python bridge surfaces.
- edge_cases_or_failure_modes: Idle kernel, spawn failure, timeout, budget overrun, helper root missing, bridge protocol mismatch.
- validation_or_tests: Directory itself is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1648 `directory` `packages/coding-agent/test/tools/web-scrapers`
- cursor: `[_]`
- core_role: Domain scraper regression suite for web tool special handlers.
- algorithmic_behavior: Covers academic, business, dev platforms, docs, finance/media, git hosting, package managers/registries, research, security, social, StackExchange, standards, Wikipedia, and YouTube scraper behavior including parallel YouTube handling.
- inputs_outputs_state: Inputs are domain URLs and mocked fetch/HTML/API payloads; outputs are markdown/text extraction results or null/fallback behavior.
- gates_or_invariants: Each handler should match only supported URLs and fail soft on fetch/parse failures.
- dependencies_and_callers: Tests `packages/coding-agent/src/web/scrapers/*` and web tool routing.
- edge_cases_or_failure_modes: Unsupported URL shape, API failure, missing metadata, malformed HTML, rate/parallel handling, domain-specific variants.
- validation_or_tests: Directory itself is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1678 `file` `packages/agent/src/compaction/messages.ts`
- cursor: `[_]`
- core_role: Message construction helpers for agent compaction flow.
- algorithmic_behavior: Builds compaction request/context messages from discarded transcript and preserve data, coordinating summary/detail text with model-facing compaction prompts.
- inputs_outputs_state: Inputs are transcript entries, preserve summaries/details, and compaction config; outputs are normalized messages for compaction model turns.
- gates_or_invariants: Must preserve necessary system/tool context while minimizing discarded history; message roles/content must match provider expectations.
- dependencies_and_callers: Used by agent compaction manager and snapcompact integration.
- edge_cases_or_failure_modes: Empty discarded history, prior summary tails, tool-call/result pairing, provider message role differences.
- validation_or_tests: Covered by agent compaction/session tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1708 `file` `packages/ai/src/dialect/harmony.ts`
- cursor: `[_]`
- core_role: Harmony dialect renderer and streaming in-band scanner.
- algorithmic_behavior: `HarmonyInbandScanner` tracks `outside/header/body` states, recognizes Harmony tokens, emits text/thinking/tool lifecycle events, holds partial suffix overlaps, parses headers/recipients, mints tool IDs, and repairs JSON args on tool end.
- inputs_outputs_state: Inputs are streamed Harmony text chunks and messages/tools for rendering; outputs are scan events, rendered dialect prompt/messages, tool call objects.
- gates_or_invariants: Incomplete control tokens must be buffered; non-assistant blocks are skipped; tool args parse failures degrade to `{}`.
- dependencies_and_callers: Uses dialect coercion/rendering utilities and `harmony.md`; called by AI provider dialect adapters.
- edge_cases_or_failure_modes: Token split across chunks, malformed headers, nested/unknown tokens, non-assistant messages, truncated tool args.
- validation_or_tests: Covered by AI dialect/tool streaming tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1738 `file` `packages/ai/src/providers/google-shared.ts`
- cursor: `[_]`
- core_role: Shared Gemini/Vertex/Claude-on-Google request conversion and stream consumption.
- algorithmic_behavior: Converts internal messages/tools to Google content/config, preserves valid thought signatures, handles Gemini 3 multimodal tool responses vs older buffering, consumes streams into text/thinking/tool events, maps finish reasons/usage/cost/errors, and builds generateContent params.
- inputs_outputs_state: Inputs are model/context/messages/tools/options/fetch streams; outputs are Google request payloads, streamed assistant events, usage, cost, errors.
- gates_or_invariants: Thought signatures only preserved for same provider/model and valid base64; finish reason is required; empty response retry policy is bounded.
- dependencies_and_callers: Used by Google/Gemini/Vertex providers in `packages/ai`.
- edge_cases_or_failure_modes: Blocked response, in-stream error, missing finish reason, image tool results on older Gemini, Claude tool IDs under Google, aborts.
- validation_or_tests: Covered by AI provider wire/stream tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1768 `file` `packages/ai/src/registry/api-key-login.ts`
- cursor: `[_]`
- core_role: Shared API-key paste login factory for non-OAuth providers.
- algorithmic_behavior: Opens auth instructions, prompts for key, trims/validates non-empty input, optionally validates against OpenAI-compatible, Anthropic-compatible, or models endpoint strategy, and returns key.
- inputs_outputs_state: Inputs are provider login config and OAuthController callbacks; output is validated API key string or thrown error.
- gates_or_invariants: Requires `onPrompt`; abort after prompt cancels; empty keys rejected; validation strategy controls endpoint probe.
- dependencies_and_callers: Used by provider registry entries for API-key providers.
- edge_cases_or_failure_modes: Missing prompt callback, cancelled signal, validation failure, whitespace-only key.
- validation_or_tests: Covered by auth/provider login tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1798 `file` `packages/ai/src/registry/nvidia.ts`
- cursor: `[_]`
- core_role: NVIDIA provider API-key login/registry definition.
- algorithmic_behavior: Prompts user for `nvapi-*` key, validates via OpenAI-compatible request to NVIDIA integration endpoint, but skips non-auth validation endpoint failures while rejecting 401/403.
- inputs_outputs_state: Inputs are OAuthController callbacks and API key text; output is trimmed key and provider definition.
- gates_or_invariants: Empty key and missing prompt callback fail; auth failures remain fatal; optional validation failures can continue.
- dependencies_and_callers: Depends on `validateOpenAICompatibleApiKey`; registered as provider `nvidia`.
- edge_cases_or_failure_modes: Validation endpoint unavailable, non-401/403 errors, cancelled signal, bad key.
- validation_or_tests: Covered by provider login/auth tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1828 `file` `packages/ai/src/registry/zai.ts`
- cursor: `[_]`
- core_role: Z.AI provider API-key login/registry definition.
- algorithmic_behavior: Prompts for API key, rejects empty/cancelled input, validates against Z.AI OpenAI-compatible endpoint with `glm-5.2`, and exports provider metadata.
- inputs_outputs_state: Inputs are OAuthController callbacks and pasted key; output is trimmed validated key.
- gates_or_invariants: Validation is mandatory; missing prompt callback/empty key/cancel fail.
- dependencies_and_callers: Depends on `validateOpenAICompatibleApiKey`; provider registry uses `zaiProvider`.
- edge_cases_or_failure_modes: Bad key, validation API failure, cancellation.
- validation_or_tests: Covered by provider login/auth tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1858 `file` `packages/ai/src/utils/retry.ts`
- cursor: `[_]`
- core_role: Copilot-specific retry wrapper for transient model/backend errors.
- algorithmic_behavior: Detects Copilot HTTP 400 `model_not_supported`, retries Copilot requests up to 3 attempts with linear base delay, also handles retryable errors with `Retry-After` capped at 30s, and honors caller abort.
- inputs_outputs_state: Inputs are async request callback, provider id, abort signal, optional base delay; output is request result or last error.
- gates_or_invariants: No-op for non-Copilot; callback must create fresh request each attempt; aborted signal surfaces original error and stops retry.
- dependencies_and_callers: Uses `extractHttpStatusFromError`, `isRetryableError`, retry-after helpers; called by Copilot provider.
- edge_cases_or_failure_modes: Consumed async iterables, rate limits without retry-after, long retry-after, final-attempt failure, abort during wait.
- validation_or_tests: Covered by Copilot provider/retry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1888 `file` `packages/catalog/src/provider-models/descriptor-types.ts`
- cursor: `[_]`
- core_role: Type and helper definitions for provider catalog/runtime model discovery descriptors.
- algorithmic_behavior: Defines descriptor shapes, catalog discovery config, provider catalog entries, and guards for catalog-capable/unauthenticated discovery.
- inputs_outputs_state: Inputs are provider descriptor objects; outputs are typed descriptor decisions for runtime discovery and generation.
- gates_or_invariants: `catalogDiscovery` membership controls generator participation; unauthenticated discovery falls back to descriptor/provider flags.
- dependencies_and_callers: Used by provider descriptor tables and `generate-models.ts`.
- edge_cases_or_failure_modes: Catalog-only vs runtime manager providers, special model managers, missing env vars, unauthenticated providers.
- validation_or_tests: Covered by catalog provider/generator tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1918 `file` `packages/coding-agent/src/capability/hook.ts`
- cursor: `[_]`
- core_role: Capability descriptor for pre/post tool execution hooks.
- algorithmic_behavior: Defines hook shape and uses `defineCapability` with key/extension-id derivation plus validation of name/path/type/tool.
- inputs_outputs_state: Inputs are discovered hook metadata; outputs are validated `Hook` capability entries.
- gates_or_invariants: Type must be `pre` or `post`; name/path/tool are required; key must include type/tool/name.
- dependencies_and_callers: Used by capability discovery and extension system.
- edge_cases_or_failure_modes: Missing hook fields, invalid hook type, duplicate keys.
- validation_or_tests: Covered by capability/discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1948 `file` `packages/coding-agent/src/cli/grievances-cli.ts`
- cursor: `[_]`
- core_role: CLI for listing, cleaning, and manually pushing auto-QA tool grievances.
- algorithmic_behavior: Opens auto-QA SQLite DB, queries/deletes grievances by id/tool/all, enforces mutually exclusive clean selectors, resets autoincrement after full delete, drains unpushed grievances with progress bar and consent bypass for manual push.
- inputs_outputs_state: Inputs are CLI options, DB rows, settings, push endpoint; outputs are JSON/status lines, DB mutations, push result.
- gates_or_invariants: Exactly one clean selector required; no DB is handled as empty/skipped; non-TTY progress bar no-ops.
- dependencies_and_callers: Depends on `Settings`, `openAutoQaDb`, `flushGrievances`; called by `omp grievances`.
- edge_cases_or_failure_modes: Missing DB, selector conflict, sqlite_sequence missing, endpoint unconfigured, push failure.
- validation_or_tests: Covered by CLI/auto-QA tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1978 `file` `packages/coding-agent/src/commands/bench.ts`
- cursor: `[_]`
- core_role: Oclif-style command wrapper for model benchmarking.
- algorithmic_behavior: Parses model args and flags (`runs`, `max-tokens`, `prompt`, `json`) and delegates to `runBenchCommand`.
- inputs_outputs_state: Inputs are CLI selectors/flags; outputs are benchmark results from bench CLI.
- gates_or_invariants: Models arg is required and multiple; defaults are runs=1/maxTokens=512.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-utils/cli` and `../cli/bench-cli`.
- edge_cases_or_failure_modes: Invalid integer flags, unresolved model selectors, benchmark provider failures.
- validation_or_tests: Covered by command/bench tests or manual CLI.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2008 `file` `packages/coding-agent/src/commit/message.ts`
- cursor: `[_]`
- core_role: Formats conventional commit messages from analysis.
- algorithmic_behavior: Builds `type(scope): summary` header and optional bullet body from analysis details.
- inputs_outputs_state: Inputs are `ConventionalAnalysis` and summary string; output is commit message text.
- gates_or_invariants: Scope only included when present; details are trimmed bullet lines.
- dependencies_and_callers: Used by commit automation/agentic commit flow.
- edge_cases_or_failure_modes: Empty details, whitespace in detail text, missing scope.
- validation_or_tests: Covered by commit helper tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2038 `file` `packages/coding-agent/src/debug/protocol-probe.ts`
- cursor: `[_]`
- core_role: Terminal protocol smoke-test component.
- algorithmic_behavior: Generates deterministic RGB PNG bytes with PNG chunks/CRC/zlib, builds OSC 66 large-text samples, truecolor bars, protocol labels, and renders a component panel exercising SGR, OSC 8, OSC 66, image protocols, and notifications.
- inputs_outputs_state: Inputs are terminal capability flags and image budget; outputs are TUI component lines and base64 PNG sample.
- gates_or_invariants: PNG encoding must be valid; large text reserves vertical rows; text/image protocol fallback labels reflect `TERMINAL`.
- dependencies_and_callers: Depends on `pi-tui`, `DynamicBorder`, theme; used by debug menu.
- edge_cases_or_failure_modes: Unsupported terminal protocols, zero/one-pixel image dimensions, image budget exhaustion, truecolor off.
- validation_or_tests: Manual debug probe plus TUI image/render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2068 `file` `packages/coding-agent/src/edit/diff.ts`
- cursor: `[_]`
- core_role: Diff generation/parsing and edit-application helpers.
- algorithmic_behavior: Generates numbered diffs with old/new coordinates and first changed line, adds off-window syntactic/bracket context, parses unified hunks/wrappers/metadata/line hints, normalizes gaps, finds matches, adjusts indentation, and normalizes file text/BOM/LF.
- inputs_outputs_state: Inputs are old/new text, hunks, file paths, edit blocks, syntactic context; outputs are diff rows, parsed hunks, replacement operations, and edited text.
- gates_or_invariants: Only real non-contiguous source gaps remain; invalid hunk headers and ambiguous/missing context are rejected; line numbers are 1-indexed.
- dependencies_and_callers: Used by coding-agent edit tools and hashline/snapshot guards.
- edge_cases_or_failure_modes: Multi-file markers, EOF marker, top-of-file marker, duplicate contexts, CRLF/BOM, indentation drift, line hints less than 1.
- validation_or_tests: Covered by edit tests, hashline patcher tests, and native syntactic context tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2098 `file` `packages/coding-agent/src/extensibility/skills.ts`
- cursor: `[_]`
- core_role: Skill discovery/loading/prompt construction.
- algorithmic_behavior: Loads active skills from capability discovery, custom dirs, and managed auto-learn dirs; dedupes symlinks by realpath; applies source toggles, include/ignore globs, disabled extension IDs; resolves authored-vs-managed name collisions; builds `/skill:<name>` prompt message by stripping frontmatter and adding metadata.
- inputs_outputs_state: Inputs are settings, skill directories/files, capability sources; outputs are `Skill` entries, warnings, active global snapshot, and prompt messages.
- gates_or_invariants: Authored skills win over managed; custom dirs run before managed shadowing; managed metadata sanitized; active skills support `skill://`.
- dependencies_and_callers: Used by extensibility/command prompt system and skill slash commands.
- edge_cases_or_failure_modes: Symlink duplicates, invalid frontmatter, missing `SKILL.md`, name collisions, disabled extensions, glob filtering.
- validation_or_tests: Covered by skill/extensibility tests and fixtures.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2128 `file` `packages/coding-agent/src/internal-urls/registry-helpers.ts`
- cursor: `[_]`
- core_role: Helpers for internal URL handlers that resolve agent registry/artifact references.
- algorithmic_behavior: Snapshots unique artifact directories from registered sessions and finds agent refs by exact or case-insensitive ID.
- inputs_outputs_state: Inputs are global `AgentRegistry` entries; outputs are artifact dir arrays or `AgentRef`.
- gates_or_invariants: Artifact dirs are deduped; live `sessionManager.getArtifactsDir()` is preferred over session-file fallback.
- dependencies_and_callers: Used by internal URL protocol handlers.
- edge_cases_or_failure_modes: Detached transcript-only agents, missing session file, duplicate parent/subagent artifact dirs.
- validation_or_tests: Covered by internal URL/agent registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2158 `file` `packages/coding-agent/src/mcp/oauth-discovery.ts`
- cursor: `[_]`
- core_role: MCP auth error analysis and OAuth endpoint discovery.
- algorithmic_behavior: Detects auth errors by status/text, extracts `Mcp-Auth-Server`, parses OAuth endpoints from JSON and `WWW-Authenticate`, classifies auth as OAuth/API key/unknown, follows RFC 9728 protected-resource metadata and well-known authorization-server URLs with dedupe.
- inputs_outputs_state: Inputs are thrown errors and server URLs/fetch; outputs are auth detection results and discovered endpoint metadata.
- gates_or_invariants: Visited issuer/resource URLs are deduped; API-key-vs-OAuth classification depends on concrete endpoint evidence.
- dependencies_and_callers: Used by MCP manager/reauth commands/transports.
- edge_cases_or_failure_modes: Relative auth server URLs, malformed JSON, missing metadata, path-prefixed issuers, redirect/fetch failure, auth challenge variants.
- validation_or_tests: Covered by MCP auth command/authorization tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2188 `file` `packages/coding-agent/src/modes/magic-keywords.ts`
- cursor: `[_]`
- core_role: TUI highlighting/detection for special magic keywords.
- algorithmic_behavior: Scans text for configured keywords and applies phase-based highlighting with optional reset color.
- inputs_outputs_state: Inputs are text, reset ANSI, animation phase; outputs are highlighted text or boolean detection.
- gates_or_invariants: Matching must preserve original text outside keyword spans.
- dependencies_and_callers: Used by interactive mode render components.
- edge_cases_or_failure_modes: Multiple keywords, ANSI reset interactions, case/word-boundary behavior.
- validation_or_tests: Covered by modes/TUI tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2218 `file` `packages/coding-agent/src/session/codex-auto-reset.ts`
- cursor: `[_]`
- core_role: Reactive Codex reset-credit auto-redeem predicate/coordinator.
- algorithmic_behavior: Evaluates whether to prompt/auto-redeem based on mode, provider, model class, identity, fresh usage report, weekly exhaustion, reset timing, credits/reserve, duplicate attempt keys, cooldowns, and in-flight promises.
- inputs_outputs_state: Inputs are usage reports, account identity, model/provider, prior attempts, now time, config; outputs are redeem/skip decisions and coordinator state mutations.
- gates_or_invariants: Only OpenAI Codex non-spark path; report freshness 10 minutes; weekly exhausted threshold exact ID/used fraction; reset time must be plausible/not too soon.
- dependencies_and_callers: Used by `AgentSession` Codex usage/reset handling.
- edge_cases_or_failure_modes: Stale/mismatched report, no credits, secondary limit not exhausted, cooldown, duplicate block key, implausible reset time.
- validation_or_tests: Covered by session Codex auto-reset tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2248 `file` `packages/coding-agent/src/ssh/connection-manager.ts`
- cursor: `[_]`
- core_role: SSH connection/control/master and host metadata manager.
- algorithmic_behavior: Validates key permissions, builds common SSH args, supports ControlMaster on non-Windows, deduplicates concurrent `ensureConnection`, probes OS/shell/compat info, persists host JSON, invalidates metadata and closes connections.
- inputs_outputs_state: Inputs are host target configs, platform, key paths, cached host info; outputs are remote command strings, control sockets, cached/persisted host metadata.
- gates_or_invariants: Key permissions must be strict; ControlMaster disabled on Windows; host info version controls refresh; pending connection map avoids duplicate connects.
- dependencies_and_callers: Used by SSH tool, slash command helper, ACP integrations.
- edge_cases_or_failure_modes: Missing ssh binary, loose key permissions, stale control socket, Windows shell compat, probe failure, concurrent connects.
- validation_or_tests: `packages/coding-agent/test/ssh/connection-manager.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2278 `file` `packages/coding-agent/src/tiny/device.ts`
- cursor: `[_]`
- core_role: Tiny local model device preference normalization and load-order logic.
- algorithmic_behavior: Normalizes device setting strings, resolves default preferences, excludes unsafe Darwin worker WebGPU orders, provides UI setting values/options, and maps setting to env value.
- inputs_outputs_state: Inputs are user/device settings and platform constraints; outputs are preferred device and load-order arrays.
- gates_or_invariants: CPU fallback is always available; Darwin WebGPU worker path is guarded; unknown device strings normalize to undefined.
- dependencies_and_callers: Used by tiny inference worker/model loading settings.
- edge_cases_or_failure_modes: Unsupported device, default setting, Darwin unsafe WebGPU, env mapping.
- validation_or_tests: Covered by tiny inference smoke and settings tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2308 `file` `packages/coding-agent/src/tools/file-recorder.ts`
- cursor: `[_]`
- core_role: Tracks files/directories touched by tool operations and formats result paths.
- algorithmic_behavior: Creates a recorder closure with add/list semantics and formats paths relative to base/cwd with directory markers.
- inputs_outputs_state: Inputs are file paths, isDirectory flag, base path, cwd; outputs are recorded path list and formatted path strings.
- gates_or_invariants: Recording should dedupe stable path entries; formatted output should remain user-readable and cwd-aware.
- dependencies_and_callers: Used by file tools to report changed/read paths.
- edge_cases_or_failure_modes: Directory vs file suffix, paths outside cwd, repeated records.
- validation_or_tests: Covered by tool read/write tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2338 `file` `packages/coding-agent/src/tools/path-utils.ts`
- cursor: `[_]`
- core_role: Path normalization, selector parsing, and search-scope resolution for tools.
- algorithmic_behavior: Normalizes Unicode spaces, `@`, file URLs, tilde, Windows aliases, local/internal URLs; parses selectors (`:N`, `:N-M`, `:N+K`, `:raw`, `:conflicts`, compound); resolves internal URLs, partitions missing paths, builds glob filters/multi-targets/exact files.
- inputs_outputs_state: Inputs are user path strings, cwd, internal URL router, filesystem state; outputs are normalized paths/selectors/search scopes and missing-path partitions.
- gates_or_invariants: `mcp://` stays opaque; external URLs rejected for filesystem search; internal URL globs rejected; `/` maps to cwd; ENOENT is swallowed only during partitioning.
- dependencies_and_callers: Used by read/search/edit tools and internal URL router.
- edge_cases_or_failure_modes: Selector-like URI tails, disjoint roots, raw/range conflicts, Windows drives, nonexistent paths, immutable internal sources.
- validation_or_tests: Covered by tool path/search/read tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2368 `file` `packages/coding-agent/src/tui/code-cell.ts`
- cursor: `[_]`
- core_role: Renders terminal code/markdown cells for coding-agent UI.
- algorithmic_behavior: Resolves status state, formats header/meta, sanitizes terminal lines, collapses carriage returns, truncates/wraps content, and renders markdown cell variants.
- inputs_outputs_state: Inputs are code/markdown cell options and theme; outputs are arrays of styled terminal lines.
- gates_or_invariants: Terminal output must be sanitized and stable-width; status state controls header styling.
- dependencies_and_callers: Used by TUI components displaying code/tool output.
- edge_cases_or_failure_modes: Carriage-return progress lines, ANSI content, long lines, empty content, status transitions.
- validation_or_tests: Covered by TUI and tool rendering tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2398 `file` `packages/coding-agent/src/utils/session-color.ts`
- cursor: `[_]`
- core_role: Deterministic session accent color selection.
- algorithmic_behavior: Hashes session names to target hues, avoids occupied theme hues, adjusts hue ranges for dark/light contexts, caps luminance for contrast, and maps hex accents to ANSI.
- inputs_outputs_state: Inputs are session name, theme color hexes, optional surface luminance; outputs are accent hex and ANSI color.
- gates_or_invariants: Minimum contrast and hue-distance constraints should avoid unreadable/conflicting accents.
- dependencies_and_callers: Used by session/agent UI rendering.
- edge_cases_or_failure_modes: Invalid hex, low saturation theme colors, crowded hue space, missing accent hex.
- validation_or_tests: Covered by TUI/session color tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2428 `file` `packages/coding-agent/src/workflow/package-loader.ts`
- cursor: `[_]`
- core_role: Loads YAML workflow packages and `.omhflow` artifacts into executable DSL structures.
- algorithmic_behavior: Validates artifact path/extension/frontmatter, parses exactly one fenced workflow block, detects import cycles, compiles DSL, merges metadata, parses change requests, policies, imports, resource prefixes, and capabilities.
- inputs_outputs_state: Inputs are workflow file paths/source YAML/DSL/imports; outputs are `WorkflowPackage`/`WorkflowArtifact` objects or `WorkflowPackageError`.
- gates_or_invariants: `.omhflow` must be a file with YAML frontmatter and one workflow block; import stack rejects cycles; checkpoint/change policy conflicts rejected.
- dependencies_and_callers: Depends on workflow DSL compiler/types; used by workflow command/runtime.
- edge_cases_or_failure_modes: Missing path, bad frontmatter/YAML/JSON, duplicate path/file change request, invalid timeout, import cycle, bad external module path.
- validation_or_tests: `packages/coding-agent/test/workflow/package-loader.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2458 `file` `packages/coding-agent/test/core/js-executor.test.ts`
- cursor: `[_]`
- core_role: Tests JS executor behavior.
- algorithmic_behavior: Creates fake tools, extracts JSON/status events, and asserts `executeJs` results for code execution, tool use, display/status events, timeout/cancel/error handling.
- inputs_outputs_state: Inputs are JS snippets and executor options; outputs are `JsResult` data/events/errors.
- gates_or_invariants: Executor must return structured data, truncate/spill output, and mark cancellations/timeouts distinctly.
- dependencies_and_callers: Tests `packages/coding-agent/src/eval/js/executor.ts`.
- edge_cases_or_failure_modes: Tool error, timeout, abort, non-JSON output, thrown exception.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2488 `file` `packages/coding-agent/test/discovery/agent-fields.test.ts`
- cursor: `[_]`
- core_role: Tests agent field parsing from discovery metadata.
- algorithmic_behavior: Asserts `parseAgentFields` handles valid/invalid field shapes.
- inputs_outputs_state: Inputs are metadata records/text; outputs are parsed agent field objects.
- gates_or_invariants: Required fields and types must be validated before creating agent definitions.
- dependencies_and_callers: Tests discovery subsystem.
- edge_cases_or_failure_modes: Missing names, malformed values, extra fields.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2518 `file` `packages/coding-agent/test/extensibility/legacy-pi-override-fallback.test.ts`
- cursor: `[_]`
- core_role: Regression for legacy pi compatibility package-root override validation.
- algorithmic_behavior: Sets up legacy override/fallback conditions and asserts validation falls back correctly for compatibility packages.
- inputs_outputs_state: Inputs are package-root override config; outputs are accepted fallback or validation errors.
- gates_or_invariants: Legacy compatibility should not break package-root resolution when override is absent/invalid.
- dependencies_and_callers: Tests extensibility compatibility loader.
- edge_cases_or_failure_modes: Invalid override path, missing package root, legacy package layout.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2548 `file` `packages/coding-agent/test/marketplace/registry.test.ts`
- cursor: `[_]`
- core_role: Tests marketplace plugin registry validation and CRUD.
- algorithmic_behavior: Validates name segments, builds/parses plugin IDs, performs registry/installed plugin CRUD, and checks registry file I/O including Claude registry format.
- inputs_outputs_state: Inputs are plugin IDs/names/files; outputs are registry objects, installed plugin records, persisted JSON/YAML.
- gates_or_invariants: Plugin IDs must be parseable and safe; registry file writes/reads must preserve schema.
- dependencies_and_callers: Tests marketplace registry modules.
- edge_cases_or_failure_modes: Invalid name segment, malformed registry file, duplicate plugin, installed-state mismatch.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2578 `file` `packages/coding-agent/test/session-manager/title-source-persistence.test.ts`
- cursor: `[_]`
- core_role: Tests session title source persistence in session headers.
- algorithmic_behavior: Reads header entries from session JSONL and asserts title source metadata survives save/load transitions.
- inputs_outputs_state: Inputs are session title updates and transcript entries; outputs are persisted header fields.
- gates_or_invariants: Title source must be written once and restored without corruption.
- dependencies_and_callers: Tests session manager persistence.
- edge_cases_or_failure_modes: Missing header, title overwrite, reload from disk.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2608 `file` `packages/coding-agent/test/ssh/connection-manager.test.ts`
- cursor: `[_]`
- core_role: Tests SSH command building and ControlMaster support gates.
- algorithmic_behavior: Creates loose key fixtures, asserts remote command argument construction, key permission validation, and platform-specific ControlMaster support.
- inputs_outputs_state: Inputs are host configs/platform/key paths; outputs are ssh command strings or validation errors.
- gates_or_invariants: Loose keys rejected; ControlMaster disabled on Windows; options escaped correctly.
- dependencies_and_callers: Tests `src/ssh/connection-manager.ts`.
- edge_cases_or_failure_modes: Spaces in command/path, username/port/key options, unsupported platform.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2638 `file` `packages/coding-agent/test/tools/approval-mode.test.ts`
- cursor: `[_]`
- core_role: Tests `tools.approvalMode` setting behavior.
- algorithmic_behavior: Builds empty workspace/session stubs and asserts tool approval decisions/rendered messages under different approval settings.
- inputs_outputs_state: Inputs are settings, tool requests, workspace tree; outputs are tool results or approval prompts.
- gates_or_invariants: Approval mode must gate tool execution consistently.
- dependencies_and_callers: Tests coding-agent tools execution policy.
- edge_cases_or_failure_modes: Missing workspace, disabled approvals, strict approval mode, text output formatting.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2668 `file` `packages/coding-agent/test/tools/fetch-jina-stall.test.ts`
- cursor: `[_]`
- core_role: Regression for HTML-to-text Jina fallback starvation.
- algorithmic_behavior: Simulates a stalled Jina fetch and asserts local fallback rendering still proceeds instead of starving.
- inputs_outputs_state: Inputs are URL/HTML fetch behavior and timeout; outputs are rendered text fallback.
- gates_or_invariants: Remote conversion stalls must not block local fallback indefinitely.
- dependencies_and_callers: Tests web fetch/render tool.
- edge_cases_or_failure_modes: Hanging remote service, fallback ordering, timeout handling.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2698 `file` `packages/coding-agent/test/tools/read-fs-not-abortable.test.ts`
- cursor: `[_]`
- core_role: Tests plain file/directory reads ignore already-aborted signals.
- algorithmic_behavior: Creates session/cwd fixtures and aborted signals, then asserts filesystem reads still return content for local non-network operations.
- inputs_outputs_state: Inputs are local files/directories and abort signal; outputs are text tool results.
- gates_or_invariants: Local read tools should not be prematurely cancelled by stale abort signals.
- dependencies_and_callers: Tests read filesystem tool.
- edge_cases_or_failure_modes: Already-aborted signal, directory vs file, missing file.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2728 `file` `packages/coding-agent/test/tools/web-search-parallel.test.ts`
- cursor: `[_]`
- core_role: Tests parallel web search execution.
- algorithmic_behavior: Asserts multiple web search operations can run concurrently and preserve independent results.
- inputs_outputs_state: Inputs are parallel search requests/providers; outputs are search result arrays/content.
- gates_or_invariants: Parallel calls must not share mutable state incorrectly.
- dependencies_and_callers: Tests web search tool dispatcher.
- edge_cases_or_failure_modes: Provider latency differences, result ordering, shared abort signal.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2758 `file` `packages/coding-agent/test/workflow/package-loader.test.ts`
- cursor: `[_]`
- core_role: Tests workflow package/artifact loader.
- algorithmic_behavior: Creates temp workflow files/artifacts and asserts valid load, invalid path/extension/frontmatter, workflow block count, imports, policies, metadata merge, resource prefixing, and change request parsing.
- inputs_outputs_state: Inputs are YAML/`.omhflow` sources and import graphs; outputs are loaded artifacts/packages or `WorkflowPackageError`.
- gates_or_invariants: Exactly one workflow block, valid frontmatter, no cycles, valid policy/change request schema.
- dependencies_and_callers: Tests `src/workflow/package-loader.ts`.
- edge_cases_or_failure_modes: Import cycles, duplicate changes, bad timeout, malformed YAML, missing import.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2788 `file` `packages/mnemopi/src/core/annotations.ts`
- cursor: `[_]`
- core_role: SQLite-backed memory annotation store and filters.
- algorithmic_behavior: Normalizes rows/content, filters noisy mentions/facts, initializes annotations schema, inserts/upserts annotations with constraint handling, imports/query annotations, and exposes convenience add/query APIs.
- inputs_outputs_state: Inputs are annotation rows/inputs, SQLite DB path/connection, query filters; outputs are stored rows, import stats, filtered annotation results.
- gates_or_invariants: Minimum fact length and stop-word filters reduce noise; duplicate content comparisons avoid redundant writes; SQLite constraints are handled explicitly.
- dependencies_and_callers: Depends on `bun:sqlite`/db path helpers; used by mnemopi memory core.
- edge_cases_or_failure_modes: Noisy entity mentions, too-short facts, constraint conflicts, invalid row IDs, missing DB.
- validation_or_tests: Covered by mnemopi annotation/provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2818 `file` `packages/mnemopi/src/core/typed-memory.ts`
- cursor: `[_]`
- core_role: Regex/priority-based memory type classifier.
- algorithmic_behavior: Defines memory type constants/order, compiled regex patterns with priorities/confidence, confidence boosters, classification for single/batch content, type priority lookup, consolidation eligibility, and decay rates.
- inputs_outputs_state: Inputs are memory text/type names; outputs are `TypeMatch`, priority, consolidation boolean, decay rate.
- gates_or_invariants: Pattern priority/confidence order drives deterministic classification; unknown types fall back safely.
- dependencies_and_callers: Used by mnemopi memory ingestion/retrieval/degradation.
- edge_cases_or_failure_modes: Multiple matching patterns, weak confidence, unknown type, booster overlap.
- validation_or_tests: Covered by mnemopi typed memory/degrade/provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2848 `file` `packages/tui/src/components/input.ts`
- cursor: `[_]`
- core_role: Single-line terminal input component.
- algorithmic_behavior: Implements grapheme-aware cursor movement, insertion/deletion/backspace, word navigation, kill ring/yank/yank-pop, undo, bracketed paste, paste sanitization/NFC normalization, horizontal scrolling, and cursor rendering.
- inputs_outputs_state: Inputs are key events/paste text/value state; outputs are updated input buffer/cursor/rendered line and callbacks.
- gates_or_invariants: Grapheme clusters must not split; pasted text sanitized; cursor must remain visible in horizontal viewport.
- dependencies_and_callers: Used by TUI prompts/editors.
- edge_cases_or_failure_modes: Wide characters, combining marks, multi-line paste, kill/yank cycles, undo stack, terminal width changes.
- validation_or_tests: Covered by TUI input tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2878 `file` `python/robomp/web/src/state.ts`
- cursor: `[_]`
- core_role: SolidJS dashboard state manager for robomp web UI.
- algorithmic_behavior: Creates status/log resources, polling loop with tick state/error, trigger status signal, and functions to run trigger/cancel API operations with state transitions.
- inputs_outputs_state: Inputs are API responses, polling interval, trigger/cancel inputs; outputs are resources/signals and UI status states.
- gates_or_invariants: `startPolling` avoids duplicate intervals; `stopPolling` clears; trigger/cancel errors surface as status error.
- dependencies_and_callers: Depends on `api` and SolidJS `createResource/createSignal`; used by robomp web components.
- edge_cases_or_failure_modes: Poll fetch failure, concurrent trigger, cancel failure, stale interval.
- validation_or_tests: Covered by robomp web/UI tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2908 `file` `crates/pi-shell/src/minimizer/filters/git.rs`
- cursor: `[_]`
- core_role: Git command output minimizer for shell transcript compression.
- algorithmic_behavior: Dispatches by git subcommand; summarizes status/log/diff/branch/tag/commit/push/pull/fetch/stash/worktree outputs, preserves diagnostics, strips progress noise, caps lists/lines, and passes through machine/custom formats.
- inputs_outputs_state: Inputs are git argv/stdout/stderr/status; outputs are condensed human-readable summaries or passthrough output.
- gates_or_invariants: Porcelain/machine formats and custom `--format`/`--pretty` must not be corrupted; path/status counts must remain accurate.
- dependencies_and_callers: Used by pi-shell minimizer called by coding-agent shell tool output handling.
- edge_cases_or_failure_modes: Rebase/cherry-pick/revert/bisect/am/sparse/merge states, `/dev/null` diffs, non-listing confirmations, ref updates, lock/noise lines.
- validation_or_tests: Covered by pi-shell minimizer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2938 `file` `packages/ai/src/registry/oauth/openai-codex.ts`
- cursor: `[_]`
- core_role: OpenAI Codex/ChatGPT OAuth browser and device-code flows.
- algorithmic_behavior: Generates PKCE authorization URL on fixed localhost port/path, exchanges auth code, formats token endpoint errors, decodes JWT profile/account claims, runs device-code polling with bounded attempts/safety margin, and refreshes credentials.
- inputs_outputs_state: Inputs are OAuth controller callbacks, auth code/device code, token responses, refresh token; outputs are `OAuthCredentials` with access/refresh/expires/account/email metadata.
- gates_or_invariants: Callback port 1455/path fixed to allowlist; access/refresh/expires required; device polling bounded at 120; 403/404 pending handled in device flow.
- dependencies_and_callers: Uses callback server, PKCE, OpenAI header values, fetch; registered for OpenAI Codex provider auth.
- edge_cases_or_failure_modes: Busy callback port, token JSON error, malformed JWT, device expiry, pending/slow auth, refresh failure.
- validation_or_tests: Covered by OpenAI Codex auth tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2968 `file` `packages/coding-agent/src/autoresearch/tools/update-notes.ts`
- cursor: `[_]`
- core_role: Autoresearch tool for updating active session notes.
- algorithmic_behavior: Validates args with ArkType, requires storage and active session, appends ideas under `## Ideas` or replaces notes body, persists notes, rebuilds runtime/dashboard state, and renders sanitized preview/details.
- inputs_outputs_state: Inputs are tool args (`notes`/`idea` style), session storage, dashboard; outputs are updated notes markdown and tool content/details.
- gates_or_invariants: Active session/storage required; idea append uses `## Ideas`; preview is sanitized/truncated.
- dependencies_and_callers: Used by autoresearch extension tool registry; tested by `autoresearch-tools.test.ts`.
- edge_cases_or_failure_modes: Missing session, no notes body, absent Ideas heading, invalid args.
- validation_or_tests: `packages/coding-agent/test/autoresearch-tools.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2998 `file` `packages/coding-agent/src/commit/changelog/parse.ts`
- cursor: `[_]`
- core_role: Parses `## [Unreleased]` changelog sections for commit tooling.
- algorithmic_behavior: Finds unreleased heading, stops at next `##`, collects `###` subsections and bullet entries into structured section data.
- inputs_outputs_state: Input is changelog markdown; output is `UnreleasedSection` or thrown error.
- gates_or_invariants: Missing unreleased section throws; subsection headings drive grouping.
- dependencies_and_callers: Used by commit/changelog automation.
- edge_cases_or_failure_modes: Unbracketed heading, no bullets, next release heading, malformed section order.
- validation_or_tests: Covered by commit/changelog tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3028 `file` `packages/coding-agent/src/eval/js/executor.ts`
- cursor: `[_]`
- core_role: Persistent JavaScript eval executor wrapper.
- algorithmic_behavior: Combines caller abort with timeout/deadline, executes code in VM context, routes output/status/display events through `OutputSink`, truncates/spills artifacts, hides timeout control events, and maps timeout/cancel/error results.
- inputs_outputs_state: Inputs are JS code and executor options; outputs are `JsResult` with exit code/data/events/artifacts/error.
- gates_or_invariants: Timeout/cancel returns cancelled with worker-reset annotation; non-abort exceptions become exitCode 1; legacy timeout and deadline compose.
- dependencies_and_callers: Used by eval tools/bridge; tested by JS executor tests.
- edge_cases_or_failure_modes: Abort before/during execution, timeout, thrown stack, oversized output, display/status events.
- validation_or_tests: `packages/coding-agent/test/core/js-executor.test.ts` and `src/eval/__tests__`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3058 `file` `packages/coding-agent/src/extensibility/extensions/model-api.ts`
- cursor: `[_]`
- core_role: Extension API adapter for querying registered models.
- algorithmic_behavior: Builds model query function exposed to extensions, mediating extension requests through model registry/catalog data.
- inputs_outputs_state: Inputs are model query parameters and extension context; outputs are model metadata/results.
- gates_or_invariants: Extensions receive normalized model data without direct registry mutation.
- dependencies_and_callers: Used by extension host/extensibility APIs.
- edge_cases_or_failure_modes: Unknown provider/model, disabled provider, stale registry.
- validation_or_tests: Covered by extension model/provider tests including issue 905.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3088 `file` `packages/coding-agent/src/mcp/transports/http.ts`
- cursor: `[_]`
- core_role: MCP JSON-RPC HTTP/SSE transport.
- algorithmic_behavior: POSTs JSON-RPC 2.0 requests/notifications, starts optional SSE listener with bounded startup timeout, tracks session ID/connection state, processes background SSE notifications/server requests, retries auth once on 401/403, drains piggybacked SSE responses, and closes with DELETE.
- inputs_outputs_state: Inputs are MCP HTTP/SSE config, requests, headers, auth callback, aborts; outputs are JSON-RPC responses, notifications, server-request replies, session close.
- gates_or_invariants: Startup timeout disabled when MCP timeout=0; SSE iterator must continue after matching response; refreshed headers persist.
- dependencies_and_callers: Used by MCP manager; depends on fetch/SSE parser and auth discovery.
- edge_cases_or_failure_modes: 401/403 reauth, SSE startup hang, piggybacked server requests, 202 notifications, close during read, missing session ID.
- validation_or_tests: Covered by MCP transport/auth tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3118 `file` `packages/coding-agent/src/modes/components/execution-shared.ts`
- cursor: `[_]`
- core_role: Shared TUI helpers for execution-mode components.
- algorithmic_behavior: Builds execution frames, collapsed previews, status footers, and maps exit/cancel state to execution status.
- inputs_outputs_state: Inputs are preview text, status, exit code, cancellation flag, theme; outputs are TUI components/lines/status labels.
- gates_or_invariants: Cancelled state overrides exit code; preview line count is bounded.
- dependencies_and_callers: Used by bash/python/execution components.
- edge_cases_or_failure_modes: Empty preview, long output, undefined exit code, cancelled with nonzero exit.
- validation_or_tests: Covered by modes/TUI execution tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3148 `file` `packages/coding-agent/src/modes/components/skill-message.ts`
- cursor: `[_]`
- core_role: TUI component for displaying skill-use messages.
- algorithmic_behavior: Renders skill message content inside a container with themed formatting.
- inputs_outputs_state: Inputs are skill metadata/message text; outputs are terminal component render lines.
- gates_or_invariants: Rendering should fit within TUI component contract and avoid raw unsanitized overflow.
- dependencies_and_callers: Used by modes when skill prompts/messages are shown.
- edge_cases_or_failure_modes: Long skill names/messages, missing metadata.
- validation_or_tests: Covered by modes/component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3178 `file` `packages/coding-agent/src/modes/controllers/tan-command-controller.ts`
- cursor: `[_]`
- core_role: Controller for `/tan` background task agent command.
- algorithmic_behavior: Validates work/model/async manager/persisted session, forks session under parent artifacts, registers async job, creates headless agent session with inherited model/tools/settings/MCP proxy, prompts it, parks or aborts registry entry, and sends background dispatch breadcrumb.
- inputs_outputs_state: Inputs are `/tan` work text and interactive mode context; outputs are async job, cloned session JSONL/artifacts, registry status, custom message.
- gates_or_invariants: Requires persisted parent session and active model; aborted job disposes/unregisters; successful job parks transcript-only agent.
- dependencies_and_callers: Uses `SessionManager`, SDK session creation, `AgentRegistry`, async job manager, background TAN prompt.
- edge_cases_or_failure_modes: Empty work, no model, async disabled, fork/create failure, signal abort before/during prompt, cleanup clone files.
- validation_or_tests: Covered by modes/controller/session tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3208 `file` `packages/coding-agent/src/slash-commands/helpers/ssh.ts`
- cursor: `[_]`
- core_role: ACP/text-mode `/ssh` slash command handler.
- algorithmic_behavior: Parses `/ssh add/list/remove/help`, validates add args and port integers, reads user/project SSH configs, lists project entries before user with duplicate suppression, writes/removes hosts, refreshes SSH tool.
- inputs_outputs_state: Inputs are parsed slash command args and runtime cwd/session; outputs are command results and config file mutations.
- gates_or_invariants: Add requires name and `--host`; `--port` must be integer 1-65535; scope must be `project` or `user`.
- dependencies_and_callers: Uses SSH config writer, slash parse helpers, `getSSHConfigPath`; called by slash command dispatcher.
- edge_cases_or_failure_modes: Unknown option/subcommand, missing option value, duplicate host across scopes, config read/write failure.
- validation_or_tests: Covered by slash-command/SSH tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3238 `file` `packages/coding-agent/src/web/scrapers/discogs.ts`
- cursor: `[_]`
- core_role: Special web scraper for Discogs release/master pages.
- algorithmic_behavior: Parses release/master URLs, fetches Discogs API, formats artists/tracks/credits/formats/labels/metadata into markdown, and returns null on mismatch/fetch/parse failure.
- inputs_outputs_state: Inputs are Discogs URLs and fetch responses; outputs are markdown page content or null.
- gates_or_invariants: Only supported Discogs URL shapes are handled; track/credit/format formatting has output limits.
- dependencies_and_callers: Used by web scraper router/tool; tested by web-scraper suite.
- edge_cases_or_failure_modes: Master vs release response shape, missing artists/tracks, API failure, malformed JSON.
- validation_or_tests: `packages/coding-agent/test/tools/web-scrapers/*`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3268 `file` `packages/coding-agent/src/web/scrapers/opencorporates.ts`
- cursor: `[_]`
- core_role: Special web scraper for OpenCorporates company pages.
- algorithmic_behavior: Parses `/companies/{jurisdiction}/{number}`, fetches API, formats company details/officers/addresses into markdown, and provides fallback markdown on API/parse/payload failure.
- inputs_outputs_state: Inputs are OpenCorporates URL/fetch; outputs are company markdown or fallback/null.
- gates_or_invariants: Jurisdiction/company number must be extracted from URL; fallback should still identify the company target.
- dependencies_and_callers: Used by web scraper router/tool.
- edge_cases_or_failure_modes: Missing company payload, API fail, malformed JSON, no officers/address.
- validation_or_tests: Web scraper tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3298 `file` `packages/coding-agent/src/web/scrapers/wikidata.ts`
- cursor: `[_]`
- core_role: Special web scraper for Wikidata entity pages.
- algorithmic_behavior: Parses Q-id, fetches EntityData JSON, extracts localized labels/descriptions/aliases/sitelinks/claims, resolves referenced entity labels in batches of 50, formats time/quantity/coordinate/entity values, and limits properties/values.
- inputs_outputs_state: Inputs are Wikidata URLs/API responses/fetch; outputs are markdown entity summaries.
- gates_or_invariants: Only Q-id URLs handled; claim output bounded; referenced labels batched.
- dependencies_and_callers: Used by web scraper router/tool.
- edge_cases_or_failure_modes: Missing entity, unknown datavalue type, precision-specific dates, missing labels, batch fetch failure.
- validation_or_tests: Web scraper/Wikipedia tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3328 `file` `packages/coding-agent/test/modes/components/session-selector-scope.test.ts`
- cursor: `[_]`
- core_role: Tests session selector scope toggle UI.
- algorithmic_behavior: Creates session fixtures with cwd/title and asserts scope toggle behavior and tab rendering.
- inputs_outputs_state: Inputs are session list and key interactions; outputs are visible session selection/filter state.
- gates_or_invariants: Scope toggle must not hide intended current/related sessions incorrectly.
- dependencies_and_callers: Tests modes session selector component.
- edge_cases_or_failure_modes: Same title different cwd, tab key, empty selection.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3358 `file` `packages/coding-agent/test/modes/controllers/mcp-authorization-link.test.ts`
- cursor: `[_]`
- core_role: Tests MCP authorization link prompt rendering.
- algorithmic_behavior: Extracts OSC 8 link URI from rendered prompt and asserts long auth URL is embedded correctly.
- inputs_outputs_state: Inputs are authorization URL text; outputs are terminal hyperlink sequences/render text.
- gates_or_invariants: Auth link must preserve full URI while displaying safely.
- dependencies_and_callers: Tests MCP authorization prompt component/controller.
- edge_cases_or_failure_modes: Long URL truncation, OSC/BEL wrapping, unsupported terminal fallback.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3388 `file` `packages/coding-agent/test/web/search/abort-and-timeout.test.ts`
- cursor: `[_]`
- core_role: Tests hard timeout and abort propagation in web search.
- algorithmic_behavior: Asserts `withHardTimeout`, Anthropic/Brave provider signal wiring, and `executeSearch` abort behavior across fallback loops.
- inputs_outputs_state: Inputs are fake providers/storage/session/abort signals; outputs are results, `ToolAbortError`, or provider error content.
- gates_or_invariants: Provider fetch receives composed signal; abort stops fallback loop; normal provider errors can be returned as content.
- dependencies_and_callers: Tests web search provider/dispatcher code including Brave.
- edge_cases_or_failure_modes: Timeout, caller abort, empty provider fallback, provider error vs abort error.
- validation_or_tests: This file is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3418 `file` `packages/collab-web/src/tool-render/tools/inspect-image.tsx`
- cursor: `[_]`
- core_role: Renderer for `inspect_image` tool output in collab web UI.
- algorithmic_behavior: Extracts target path/url/model/mime/question from args/result details, shortens/truncates display, renders badges, image previews, and text result.
- inputs_outputs_state: Inputs are tool args/result record; outputs are React summary/body nodes.
- gates_or_invariants: Missing target renders invalid-arg; question normalized/truncated to 200; result text limited to 8 lines.
- dependencies_and_callers: Uses collab-web renderer parts/utilities; called by tool-render registry.
- edge_cases_or_failure_modes: Missing path/url, malformed details, long question/path, absent images/text.
- validation_or_tests: Covered by collab-web tool renderer tests.
- skip_candidate: `yes: UI renderer only, not a core runtime algorithm, though it maps tool result data`

### OH_MY_HUMANIZE_MAIN-HZ-3448 `file` `packages/mnemopi/src/core/migrations/index.ts`
- cursor: `[_]`
- core_role: Migration barrel export.
- algorithmic_behavior: Re-exports migration module `e6-triplestore-split`.
- inputs_outputs_state: Input is import of migrations index; output is exported migration symbols.
- gates_or_invariants: Barrel must expose migration modules for migration runner discovery.
- dependencies_and_callers: Used by mnemopi migration loading.
- edge_cases_or_failure_modes: Missing export hides migration.
- validation_or_tests: Covered by migration tests/import checks.
- skip_candidate: `yes: barrel export only, no standalone algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3478 `file` `packages/stats/src/client/ui/Panel.tsx`
- cursor: `[_]`
- core_role: Presentational panel wrapper for stats dashboard UI.
- algorithmic_behavior: Renders optional title/subtitle/actions header and body children with CSS classes.
- inputs_outputs_state: Inputs are React props/children; outputs are React DOM structure.
- gates_or_invariants: Header omitted when no title/subtitle/actions; `title` prop omits native div title collision.
- dependencies_and_callers: Used by stats dashboard routes/components.
- edge_cases_or_failure_modes: Empty header fields, custom className merge.
- validation_or_tests: Covered indirectly by stats client render/build.
- skip_candidate: `yes: presentational component only`

### OH_MY_HUMANIZE_MAIN-HZ-3508 `file` `packages/coding-agent/src/commit/agentic/tools/git-overview.ts`
- cursor: `[_]`
- core_role: Commit-agent tool for summarizing git change scope.
- algorithmic_behavior: Snapshots changed files, stat/numstat, scope candidates, filters lock files, optionally includes untracked files, and stores overview in commit agent state.
- inputs_outputs_state: Inputs are repo cwd/options and git status/stat output; outputs are overview tool result and state fields.
- gates_or_invariants: Lock files filtered unless relevant; untracked inclusion is optional.
- dependencies_and_callers: Used by agentic commit workflow tools.
- edge_cases_or_failure_modes: Non-git cwd, large diff, untracked noise, lockfile-only changes.
- validation_or_tests: Covered by commit agent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3538 `file` `packages/coding-agent/src/markit/converters/pdf/types.ts`
- cursor: `[_]`
- core_role: Type definitions for PDF conversion/extraction pipeline.
- algorithmic_behavior: Defines bounds, text boxes, vector segments, resolved table cells/grids, image regions, page content, and content block shapes.
- inputs_outputs_state: Inputs are imported types by PDF extractor modules; outputs are compile-time structural contracts.
- gates_or_invariants: Coordinate-system comments distinguish PDF bottom-left and MuPDF top-left fields.
- dependencies_and_callers: Used by markit PDF converter implementation.
- edge_cases_or_failure_modes: Type drift between extractor/rendering modules.
- validation_or_tests: Covered by TypeScript checks and PDF converter tests.
- skip_candidate: `yes: type definitions only, no runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3568 `file` `packages/coding-agent/src/web/search/providers/brave.ts`
- cursor: `[_]`
- core_role: Brave Search provider implementation.
- algorithmic_behavior: Reads `BRAVE_API_KEY`, maps recency to Brave freshness codes, clamps result count to 10/20, performs fetch with hard timeout signal, classifies HTTP errors, builds snippets from result fields, and maps Brave JSON to unified `SearchResponse`.
- inputs_outputs_state: Inputs are query/count/recency/search params, API key, fetch/signal; outputs are normalized search results or provider errors.
- gates_or_invariants: Missing API key disables provider; count is bounded; composed signal must propagate to fetch.
- dependencies_and_callers: Extends `SearchProvider`; used by web search dispatcher.
- edge_cases_or_failure_modes: API 401/429/5xx, missing web results, abort/timeout, unsupported recency.
- validation_or_tests: `packages/coding-agent/test/web/search/abort-and-timeout.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3598 `file` `packages/utils/src/vendor/mermaid-ascii/class/parser.ts`
- cursor: `[_]`
- core_role: Mermaid class diagram parser for ASCII rendering vendor module.
- algorithmic_behavior: Parses `classDiagram` lines into classes, namespaces, class bodies, annotations, members, inline attributes, and relationships with cardinality/labels; maps arrow syntax to UML relationship type and marker side.
- inputs_outputs_state: Inputs are normalized Mermaid lines; outputs are `ClassDiagram` with classes/relationships/namespaces.
- gates_or_invariants: Classes are deduped by ID; relationship parsing ensures endpoint classes exist; member parser separates methods vs attributes.
- dependencies_and_callers: Used by mermaid-ascii renderer; depends on multiline BR normalization and class diagram types.
- edge_cases_or_failure_modes: Nested namespace limitations, generic class names, reversed arrows, labels/cardinality with `<br>`, malformed members.
- validation_or_tests: Covered by mermaid-ascii/parser/render tests where present.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 120 unique item IDs
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`