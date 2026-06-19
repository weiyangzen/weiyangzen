# agent_20 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-020 `directory` `crates/pi-iso`
- cursor: `[_]`
- core_role: Cross-platform filesystem isolation crate for fast branch/worktree snapshots and diffs.
- algorithmic_behavior: `src/lib.rs` selects backend order by platform (`BackendKind::native`, `auto_order`, `resolve` around lines 68-140, 324-373); `diff.rs` uses git diff when possible, otherwise indexes and compares copied trees; backend modules implement APFS clonefile, Btrfs/ZFS snapshots, Linux reflink/overlayfs, Windows ProjFS/block clone, and recursive-copy fallback.
- inputs_outputs_state: Inputs are source/destination paths, backend preference, and lifecycle calls; outputs are isolated writable trees, backend probe status, rendered diffs, and cleanup side effects.
- gates_or_invariants: Backends validate destination safety, platform capability, and ownership of created mounts/snapshots before cleanup; `rcopy.rs` refuses unsafe destination layouts and applies dirty git state onto fallback copies.
- dependencies_and_callers: Depends on platform syscalls/CLIs (`clonefile`, `btrfs`, `zfs`, overlay mount/fuse, Windows APIs) plus git for worktree/diff paths.
- edge_cases_or_failure_modes: Unsupported filesystems, cross-device clone failures, stale overlay mounts, dirty worktrees, symlinks, binary files, missing git, and cleanup of partially-created snapshots.
- validation_or_tests: Backend code includes local unit checks; behavior is validated by crate consumers and fallback `rcopy` paths when native probes fail.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-050 `file` `docs/handoff-generation-pipeline.md`
- cursor: `[_]`
- core_role: Runtime design document for `/handoff` session-transfer generation.
- algorithmic_behavior: Documents command trigger/preflight, `AgentSession.handoff`, `generateHandoff`, cancellation, new-session creation, injected custom message, persistence, and UI state transitions; important flow points are lines 29-39, 44-95, 97-162, and 163-212.
- inputs_outputs_state: Inputs are current transcript/session state and optional user request; outputs are a generated handoff summary, new session metadata, queued message injection, and status indicators.
- gates_or_invariants: Blocks overlapping generation, supports abort, keeps cancelled handoffs from creating sessions, and treats handoff generation as non-normal user text.
- dependencies_and_callers: Tied to slash command handling, `AgentSession`, UI status, session manager, and custom message injection.
- edge_cases_or_failure_modes: Cancellation races, empty/failed summaries, persistence failures, and users starting work while handoff generation is pending.
- validation_or_tests: Documentation maps to session/handoff tests and UI cancellation behavior; no command execution was run in this research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-080 `file` `infra/tune-kata-runtime.sh`
- cursor: `[_]`
- core_role: Infrastructure runtime tuning script for Kata container defaults.
- algorithmic_behavior: SSHes to target host, backs up Kata config, regex-rewrites `default_vcpus`, `default_memory`, and `virtio_fs_extra_args`, verifies exactly one replacement per field, then smoke-boots a `kata-qemu` pod; key sections are lines 10-28, 30-64, and 67-80.
- inputs_outputs_state: Inputs are host/user/config path and tuning values; outputs are modified remote TOML config, backup file, grep verification, and smoke pod status.
- gates_or_invariants: Python patch helper exits if replacement count is not exactly one; `set -euo pipefail` gates shell failures.
- dependencies_and_callers: Depends on `ssh`, remote Python, `grep`, and `kubectl`.
- edge_cases_or_failure_modes: Missing SSH access, config format drift, non-unique TOML keys, Kubernetes smoke failure, and read-only or permission-denied remote files.
- validation_or_tests: Self-validates via replacement count and `kubectl run`; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-110 `file` `scripts/rewrite-system-prompt.ts`
- cursor: `[_]`
- core_role: Standalone prompt prose rewriter with structural-token preservation.
- algorithmic_behavior: Discovers prompt files, classifies verbatim/fragile lines, plans rewrite chunks, calls OpenRouter with retry and token-preservation checks, parses XML-ish responses, supports dry-run/write modes; key functions include `peel` lines 102-124, `isVerbatimLine` 136-151, `blockSkipMask` 175-207, `planRewrite` 210-224, `rewriteAll` 276-329, and rewriter retry logic 393-452.
- inputs_outputs_state: Inputs are prompt globs, CLI flags, model/API key, and prompt text; outputs are rewritten prompt files or dry-run diffs plus change counters.
- gates_or_invariants: Preserves fragile tokens, code fences, headings, handlebars-like tokens, XML tags, and prompt structure; refuses unsafe rewrites that drop protected tokens.
- dependencies_and_callers: Uses Bun file APIs, OpenRouter fetch, glob patterns, and static rewrite instructions.
- edge_cases_or_failure_modes: API failure, malformed model response, prompt token loss, overlarge chunks, binary/unsupported files, and generated dry-run-only operation.
- validation_or_tests: Has internal preservation checks and retries; no repo tests were run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-140 `directory` `packages/hashline/test`
- cursor: `[_]`
- core_role: Contract test suite for hashline parser, patcher, recovery, block edits, and diff previews.
- algorithmic_behavior: Covers format-v4 range anchors, snapshot tags, stale recovery, seen-line provenance, lenient header forms, boundary repair, landing-shift behavior, block resolver lowering, and compact diff rendering.
- inputs_outputs_state: Inputs are hashline patch text, snapshots, target file content, and optional block resolver; outputs are applied text, warnings, compact previews, and recovery success/failure.
- gates_or_invariants: Tests assert snapshot tag integrity, stale-anchor rejection, duplicate-boundary repair limits, abort sentinels, blank payload semantics, and block resolution line spans.
- dependencies_and_callers: Exercises `packages/hashline/src` parser/applier/patcher APIs used by coding-agent editing tools.
- edge_cases_or_failure_modes: Stale snapshot drift, duplicate opener/closer echoes, invalid payload contamination, cross-path snapshot misuse, repeated reads, and unresolved syntax blocks.
- validation_or_tests: Directory is itself validation; inspected describes in `block.test.ts`, `core-contracts.test.ts`, `patcher.test.ts`, `snapshots.test.ts`, and related files.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-170 `file` `crates/pi-shell/build.rs`
- cursor: `[_]`
- core_role: Build-time generator for bundled shell minimizer filter definitions.
- algorithmic_behavior: Reads sorted TOML files from minimizer defs, merges child tables while skipping duplicate `schema_version`, emits `builtin_filters.toml`, and adds Cargo rerun markers.
- inputs_outputs_state: Inputs are `defs/*.toml`; output is generated TOML in Cargo `OUT_DIR`.
- gates_or_invariants: Deterministic sort order and child `schema_version` suppression keep the combined filter catalog stable.
- dependencies_and_callers: Called by Cargo build for `pi-shell`.
- edge_cases_or_failure_modes: Missing defs directory, malformed IO, duplicate schema metadata, and nondeterministic file ordering if sort were removed.
- validation_or_tests: Covered indirectly by minimizer pipeline tests and build success.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-200 `file` `docs/tools/rewind.md`
- cursor: `[_]`
- core_role: Runtime design document for the `rewind` tool and transcript rollback.
- algorithmic_behavior: Describes tool input, deferred application at `turn_end`, transcript-prefix trim, `branchWithSummary`, hidden `rewind-report`, and resumed conversation state; key flow lines are 14-45 and side-effect/limit sections 51-95.
- inputs_outputs_state: Input is user-selected rewind target/report; outputs are branched session, trimmed transcript, injected summary, and hidden report metadata.
- gates_or_invariants: Rewind is deferred until safe turn boundary and does not restore filesystem, external processes, or arbitrary runtime state.
- dependencies_and_callers: Tied to checkpoint/rewind tools, session branching, transcript rebuild, and hidden message plumbing.
- edge_cases_or_failure_modes: Missing checkpoint, empty report, user expectations about filesystem rollback, and stale runtime side effects after transcript rollback.
- validation_or_tests: Backed by checkpoint/rewind tool behavior and session tests; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-230 `directory` `packages/agent/test/utils`
- cursor: `[_]`
- core_role: Test-only utility tools for agent runtime tests.
- algorithmic_behavior: `calculate.ts` evaluates math expressions via `new Function` and wraps them as `AgentToolResult`; `get-current-time.ts` formats local or timezone-specific time and returns UTC timestamp details.
- inputs_outputs_state: Inputs are expression strings or optional timezone; outputs are text tool content and details payloads.
- gates_or_invariants: Timezone helper throws a normalized invalid-timezone error; calculate forwards evaluation errors.
- dependencies_and_callers: Used by `packages/agent/test` suites as representative tool definitions.
- edge_cases_or_failure_modes: Unsafe arbitrary JS evaluation is acceptable only because this is test utility code; invalid timezone and malformed expressions error.
- validation_or_tests: These utilities support agent runtime tests rather than being validated directly.
- skip_candidate: `yes: test fixtures, not production algorithm, but they define representative tool contracts`

### OH_MY_HUMANIZE_MAIN-HZ-260 `directory` `packages/coding-agent/src/exa`
- cursor: `[_]`
- core_role: Exa MCP integration layer for search-style tool calls.
- algorithmic_behavior: `mcp-client.ts` finds API keys, normalizes MCP request payloads, fetches/caches schemas, calls Exa tools over HTTP, and formats search/generic responses; `types.ts` defines MCP and Exa response contracts.
- inputs_outputs_state: Inputs are API key, MCP tool args, server URL, and schema cache; outputs are tool definitions, formatted content, and structured response details.
- gates_or_invariants: Requires API key, validates HTTP status, distinguishes Exa search responses, and keeps schema fetching lazy.
- dependencies_and_callers: Used by Exa search provider/tool wrapper in coding-agent web search.
- edge_cases_or_failure_modes: Missing key, non-JSON response, schema fetch failure, empty results, and server error payloads.
- validation_or_tests: Covered through web/search provider tests and MCP tool wrapper paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-290 `directory` `packages/coding-agent/src/web`
- cursor: `[_]`
- core_role: Coding-agent web search and fetch/scrape subsystem.
- algorithmic_behavior: Contains provider selection/fallback (`search/provider.ts`), search execution/rendering (`search/index.ts`, `render.ts`), provider-specific adapters, Kagi/Parallel helpers, and site-specific scrapers that convert URLs/API responses into markdown.
- inputs_outputs_state: Inputs are search query/options, auth storage, URL, fetch timeout/signal, and provider settings; outputs are unified search results, rendered tool previews, markdown page bodies, metadata, or error text.
- gates_or_invariants: Providers must use passed `authStorage`; search fallback respects preferred/excluded providers; scrapers gate on host/path and return `null` to fall through; fetch uses size/time limits and abort signals.
- dependencies_and_callers: Used by web_search/web_fetch tools, Exa integration, auth storage, and TUI/collab renderers.
- edge_cases_or_failure_modes: Provider quota/auth failures, bot blocks, charset mismatch, huge responses, aborts, missing credentials, and scraper host spoofing.
- validation_or_tests: `packages/coding-agent/test/tools/web-scrapers/security.test.ts` validates security-sensitive scraper gating; provider behavior has package-local tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-320 `directory` `packages/coding-agent/test/workflow`
- cursor: `[_]`
- core_role: Contract tests for `.omhflow` DSL, runtime adapters, scheduler, persistence, graph view, and slash command surface.
- algorithmic_behavior: Tests definition parsing, condition DSL, compiler sequence/parallel/join/cycle rules, artifact registry/freezing, run/lifecycle stores, model resolution, node/session/task/eval/human/shell runtimes, scheduler activation, graph rendering, package loading, and end-to-end workflow execution.
- inputs_outputs_state: Inputs are workflow definitions, node graphs, runtime hosts, tool adapters, artifacts, and scheduler events; outputs are compiled plans, state transitions, run records, graph views, and tool/session invocations.
- gates_or_invariants: Asserts DAG validity, cycles rejected, artifact immutability, runtime adapter output shape, retry semantics, model fallback, lifecycle event ordering, and slash-command behavior.
- dependencies_and_callers: Validates `packages/coding-agent/src/workflow` and `/workflow` command integration.
- edge_cases_or_failure_modes: Duplicate IDs, missing refs, cyclic joins, bad prompt sources, failed shell/eval/task nodes, artifact mutation, and scheduler race conditions.
- validation_or_tests: Directory is the workflow validation suite; not executed here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-350 `file` `crates/pi-natives/src/appearance.rs`
- cursor: `[_]`
- core_role: Native macOS appearance detection and change observation.
- algorithmic_behavior: Reads CoreFoundation `AppleInterfaceStyle`, maps dark/light/no-preference, starts a runloop observer with notification/timer callbacks, dedupes events, and exports N-API detection/observer functions.
- inputs_outputs_state: Inputs are macOS defaults and notification events; outputs are appearance enum values and JS callback events.
- gates_or_invariants: Off-platform behavior is unavailable/no-op; observer context dedupes and cleans up on dispose.
- dependencies_and_callers: Depends on CoreFoundation, dispatch/runloop APIs, and N-API exports consumed by TUI theme handling.
- edge_cases_or_failure_modes: Missing defaults key, invalid CF values, runloop stop races, callback panics, and observer cleanup.
- validation_or_tests: Theme tests cover light/dark classification on JS side; native behavior is platform-gated.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-380 `file` `crates/pi-shell/src/lib.rs`
- cursor: `[_]`
- core_role: Crate export surface for shell execution, minimizer, process, cancellation, fixup, and Windows helpers.
- algorithmic_behavior: Re-exports module APIs and `brush::session::action::ChildSessionAction`.
- inputs_outputs_state: No local runtime state; controls which internal algorithms are public to dependents.
- gates_or_invariants: Export paths must remain stable for callers.
- dependencies_and_callers: Called by Rust crate consumers and generated bindings.
- edge_cases_or_failure_modes: Broken exports cause compile failures; no direct algorithm here.
- validation_or_tests: Covered by crate compilation and downstream imports.
- skip_candidate: `yes: barrel/export-only file, though it defines public API surface`

### OH_MY_HUMANIZE_MAIN-HZ-410 `file` `packages/agent/test/run-summary.test.ts`
- cursor: `[_]`
- core_role: Regression tests for agent run-summary aggregation and delivery.
- algorithmic_behavior: Exercises run summary creation, tool coverage, onRunEnd delivery, skipped/nonfatal paths, and summary formatting.
- inputs_outputs_state: Inputs are synthetic agent/tool events; outputs are summary messages and callback payloads.
- gates_or_invariants: Summary must include observed tool results, avoid fatalizing callback failures, and preserve externally visible run contract.
- dependencies_and_callers: Validates `packages/agent` runtime event summarization.
- edge_cases_or_failure_modes: Missing tool data, skipped tools, callback exceptions, and summary duplication.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-440 `file` `packages/ai/test/anthropic-fast-mode.test.ts`
- cursor: `[_]`
- core_role: Tests Anthropic fast-mode service-tier selection.
- algorithmic_behavior: Verifies Claude-only speed priority, fallback clearing, unsupported-mode classifier, and request-body effects.
- inputs_outputs_state: Inputs are model/provider metadata and fast-mode options; outputs are provider request params or errors.
- gates_or_invariants: Fast mode must not leak to unsupported providers and must be cleared when fallback rules require it.
- dependencies_and_callers: Validates Anthropic provider adapter and service-tier mapping.
- edge_cases_or_failure_modes: Unsupported service tier, non-Claude model, and fallback transitions.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-470 `file` `packages/ai/test/auth-retry.test.ts`
- cursor: `[_]`
- core_role: Tests authentication retry/refresh behavior in AI providers.
- algorithmic_behavior: Covers static keys, resolver keys, OAuth access refresh, key rotation, and auth-error classification.
- inputs_outputs_state: Inputs are mocked provider fetch failures and key sources; outputs are retry attempts, refreshed tokens, or propagated errors.
- gates_or_invariants: Retry only on auth-classified failures and must not endlessly retry.
- dependencies_and_callers: Validates `packages/ai` request execution and provider auth plumbing.
- edge_cases_or_failure_modes: Refresh failure, wrong classifier, stale token reuse, and non-auth errors.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-500 `file` `packages/ai/test/dialect-thinking.test.ts`
- cursor: `[_]`
- core_role: Tests parsing and normalization of provider thinking/reasoning dialects.
- algorithmic_behavior: Round-trips Gemini/Gemma/Kimi/Pi reasoning tags and flushes unterminated thinking blocks.
- inputs_outputs_state: Inputs are streamed provider chunks; outputs are normalized text/reasoning deltas.
- gates_or_invariants: Thinking must not leak into user-visible text except through explicit reasoning channels.
- dependencies_and_callers: Validates AI dialect stream adapters.
- edge_cases_or_failure_modes: Unterminated tags, duplicate chunks, nested/partial tag boundaries, and provider-specific marker differences.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-530 `file` `packages/ai/test/issue-1203-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for MiniMax cumulative reasoning duplication.
- algorithmic_behavior: Feeds provider chunks with `<think>` behavior and asserts deduped cumulative reasoning/text output.
- inputs_outputs_state: Inputs are synthetic streamed chunks; outputs are normalized assistant deltas.
- gates_or_invariants: Cumulative reasoning must not emit duplicated prior content.
- dependencies_and_callers: Validates MiniMax/OpenAI-compatible stream dialect code.
- edge_cases_or_failure_modes: Repeated prefixes, think-tag transitions, and empty deltas.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-560 `file` `packages/ai/test/kilo-login.test.ts`
- cursor: `[_]`
- core_role: Tests Kilo OAuth/device login flow.
- algorithmic_behavior: Covers device approval, rate-limit handling, denied auth, and token surface.
- inputs_outputs_state: Inputs are mocked device-code and polling responses; outputs are login result or user-facing error.
- gates_or_invariants: Polling must respect denial/rate-limit states and stop on terminal states.
- dependencies_and_callers: Validates AI registry login integration.
- edge_cases_or_failure_modes: Expired/denied code, slow_down, malformed response, and missing token.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-590 `file` `packages/ai/test/openai-max-output-tokens-cap.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI/OpenRouter output-token cap behavior.
- algorithmic_behavior: Verifies max-output-token capping, OpenRouter omission behavior, and Kimi exception handling.
- inputs_outputs_state: Inputs are model context/cap metadata and requested token budgets; outputs are request payload token fields.
- gates_or_invariants: Provider-specific caps must not over-request and must omit fields where provider expects omission.
- dependencies_and_callers: Validates OpenAI-compatible provider request shaping.
- edge_cases_or_failure_modes: Unknown context, Kimi model exception, OpenRouter pass-through, and cap lower than request.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-620 `file` `packages/ai/test/request-debug.test.ts`
- cursor: `[_]`
- core_role: Tests one-shot request debug capture.
- algorithmic_behavior: Captures next fetch request/response, raw response bodies, cancellation partials, and provider wrapping.
- inputs_outputs_state: Inputs are debug toggles and mocked fetch responses; outputs are captured debug artifacts.
- gates_or_invariants: Capture is next-request scoped and must preserve useful data on cancelled/failed responses.
- dependencies_and_callers: Validates AI fetch/request instrumentation.
- edge_cases_or_failure_modes: Partial streams, aborted fetch, provider wrapper layers, and no response body.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-650 `file` `packages/ai/test/xai-oauth-effort-strip.test.ts`
- cursor: `[_]`
- core_role: Tests xAI OAuth request shaping around reasoning effort.
- algorithmic_behavior: Ensures effort/reasoning fields are stripped or encoded only when supported by the OAuth-backed xAI model.
- inputs_outputs_state: Inputs are xAI model metadata and OAuth provider config; outputs are normalized request payloads.
- gates_or_invariants: Unsupported effort must not be sent to no-dial reasoner variants.
- dependencies_and_callers: Validates xAI OAuth provider adapter.
- edge_cases_or_failure_modes: Unsupported model family and accidental effort leakage.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-680 `file` `packages/catalog/test/github-copilot-wire.test.ts`
- cursor: `[_]`
- core_role: Tests GitHub Copilot catalog wire identity.
- algorithmic_behavior: Validates host/enterprise endpoint parsing and API key handling.
- inputs_outputs_state: Inputs are Copilot registry/provider configs; outputs are resolved endpoint/key metadata.
- gates_or_invariants: Enterprise and public hosts must resolve without corrupting auth identity.
- dependencies_and_callers: Validates catalog/provider descriptors consumed by AI registry.
- edge_cases_or_failure_modes: Enterprise URL variants and key-prefix parsing.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-710 `file` `packages/catalog/test/xai-oauth-bundle.test.ts`
- cursor: `[_]`
- core_role: Tests bundled xAI OAuth catalog entries.
- algorithmic_behavior: Asserts curated model IDs, composer non-reasoning behavior, and max-token/context metadata.
- inputs_outputs_state: Inputs are bundled catalog descriptors; outputs are model identity and capability assertions.
- gates_or_invariants: xAI OAuth bundle must expose intended defaults without generated JSON drift.
- dependencies_and_callers: Validates catalog model bundle used by coding-agent model selection.
- edge_cases_or_failure_modes: Missing curated model, wrong reasoning flag, and bad context size.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-740 `file` `packages/coding-agent/test/acp-event-mapper.test.ts`
- cursor: `[_]`
- core_role: Tests ACP event mapping from coding-agent session events.
- algorithmic_behavior: Verifies message IDs, final-text de-duplication, command/eval source mapping, diff and terminal content, replay args/location, and discriminator rejection.
- inputs_outputs_state: Inputs are internal session events; outputs are ACP protocol event objects.
- gates_or_invariants: Mapper must preserve stable IDs and reject invalid discriminated unions.
- dependencies_and_callers: Validates ACP bridge/event adapter.
- edge_cases_or_failure_modes: Duplicate final messages, missing locations, malformed event type, and streamed terminal data.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-770 `file` `packages/coding-agent/test/agent-session-mcp-discovery.test.ts`
- cursor: `[_]`
- core_role: Tests AgentSession MCP discovery and tool activation.
- algorithmic_behavior: Covers search-index caching, active tools, manual deactivation, activate-all, persisted/restored selections, baselines, server outages, and artifact spill/truncate.
- inputs_outputs_state: Inputs are MCP server/tool/resource definitions and session settings; outputs are active tool lists, discovery artifacts, and restored selections.
- gates_or_invariants: Manual deactivations and baselines must survive discovery refresh; outage artifacts must not corrupt active state.
- dependencies_and_callers: Validates coding-agent MCP manager/session integration.
- edge_cases_or_failure_modes: Large discovery payloads, stale server data, reconnect outages, and selection persistence.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-800 `file` `packages/coding-agent/test/auto-thinking-classifier.test.ts`
- cursor: `[_]`
- core_role: Tests automatic thinking-level classifier behavior.
- algorithmic_behavior: Parses classifier config, maps online/local labels, applies budget floors, and clamps output to model support.
- inputs_outputs_state: Inputs are user prompt/model support/settings; outputs are selected thinking level or disabled reasoning.
- gates_or_invariants: Classifier labels must be parsed safely and clamped to model-supported ranges.
- dependencies_and_callers: Validates thinking auto-selection used before agent turns.
- edge_cases_or_failure_modes: Unsupported levels, malformed config, budget below floor, and local classifier fallback.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-830 `file` `packages/coding-agent/test/commit-split-hunk-validation.test.ts`
- cursor: `[_]`
- core_role: Tests commit-split hunk/line selector validation.
- algorithmic_behavior: Rejects unmatched hunk selectors and line selectors while allowing deferred changelog proposals.
- inputs_outputs_state: Inputs are commit split proposal selectors; outputs are accepted/rejected validation results.
- gates_or_invariants: Commit splitting must not stage invisible or unmatched hunks.
- dependencies_and_callers: Validates commit assistant split logic.
- edge_cases_or_failure_modes: Selector drift, hunk mismatch, and changelog-only deferred edits.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-860 `file` `packages/coding-agent/test/fast-mode-scope.test.ts`
- cursor: `[_]`
- core_role: Tests fast-mode service-tier scoping in coding-agent settings.
- algorithmic_behavior: Maps service tiers to provider/model requests and ensures fast mode is scoped to intended providers.
- inputs_outputs_state: Inputs are settings/model selections; outputs are resolved request options.
- gates_or_invariants: Fast mode must not globally affect unsupported providers.
- dependencies_and_callers: Validates coding-agent model/request preparation.
- edge_cases_or_failure_modes: Provider mismatch and stale fast-mode setting.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-890 `file` `packages/coding-agent/test/input-controller-orphan-submit.test.ts`
- cursor: `[_]`
- core_role: Regression tests for input submission when no active waiter exists.
- algorithmic_behavior: Ensures typed prompts are not swallowed in idle gaps, streaming races use steer semantics, and editor text/images are restored on dispatch failure.
- inputs_outputs_state: Inputs are editor text, pending images, mocked session state, and callback presence; outputs are prompt calls, queued messages, or restored editor drafts.
- gates_or_invariants: User input must remain recoverable across orphan-submit races.
- dependencies_and_callers: Validates `InputController.setupEditorSubmitHandler`.
- edge_cases_or_failure_modes: Missing `onInputCallback`, background stream starts between Enter and dispatch, extension-command rejection, and image buffers.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-920 `file` `packages/coding-agent/test/issue-775-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for default model thinking behavior.
- algorithmic_behavior: Reproduces issue 775 around default thinking selection and asserts expected model/thinking config.
- inputs_outputs_state: Inputs are model defaults/settings; outputs are resolved thinking state.
- gates_or_invariants: Default reasoning settings must be stable and compatible with selected model.
- dependencies_and_callers: Validates model initialization/thinking configuration.
- edge_cases_or_failure_modes: Missing default, unsupported thinking, and config regression.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-950 `file` `packages/coding-agent/test/loop-limit.test.ts`
- cursor: `[_]`
- core_role: Tests loop-mode limit parsing and runtime stop behavior.
- algorithmic_behavior: Parses loop limit settings and verifies auto-loop stops after configured turn count.
- inputs_outputs_state: Inputs are loop commands/settings and turn events; outputs are loop state transitions.
- gates_or_invariants: Loop must not run unbounded after reaching limit.
- dependencies_and_callers: Validates loop mode controller/session integration.
- edge_cases_or_failure_modes: Invalid limit, zero/empty limit, and off-by-one loop termination.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-980 `file` `packages/coding-agent/test/mnemopi-bank-derivation.test.ts`
- cursor: `[_]`
- core_role: Tests mnemopi bank derivation and legacy/global bank inclusion.
- algorithmic_behavior: Verifies per-project/per-project-tagged bank names, scoped DB paths, and recall bank inclusion.
- inputs_outputs_state: Inputs are mnemopi config scoping options; outputs are bank lists and DB paths.
- gates_or_invariants: Scoped retention writes must stay project-local while recall may include shared banks.
- dependencies_and_callers: Validates `packages/coding-agent/src/mnemopi/state.ts`.
- edge_cases_or_failure_modes: Legacy base bank, duplicate banks, and global/project bank equality.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1010 `file` `packages/coding-agent/test/read-acp-fs.test.ts`
- cursor: `[_]`
- core_role: Tests ACP filesystem read bridge.
- algorithmic_behavior: Exercises file read ranges and ACP-facing output format.
- inputs_outputs_state: Inputs are file paths/ranges; outputs are read content or errors.
- gates_or_invariants: Range boundaries and filesystem access must match ACP contract.
- dependencies_and_callers: Validates read tool ACP adapter.
- edge_cases_or_failure_modes: Missing files, invalid ranges, and path handling.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1040 `file` `packages/coding-agent/test/sdk-move-cwd.test.ts`
- cursor: `[_]`
- core_role: Tests SDK tool behavior after working-directory moves.
- algorithmic_behavior: Ensures tools execute from the moved/current session directory rather than stale startup cwd.
- inputs_outputs_state: Inputs are cwd changes and SDK tool calls; outputs are resolved file/tool operations.
- gates_or_invariants: Runtime cwd must be session-current for tools.
- dependencies_and_callers: Validates SDK embedding/session cwd handling.
- edge_cases_or_failure_modes: Stale cwd capture and relative path drift.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1070 `file` `packages/coding-agent/test/startup-splash.test.ts`
- cursor: `[_]`
- core_role: Tests startup splash gating/render behavior.
- algorithmic_behavior: Verifies splash visibility conditions and render output.
- inputs_outputs_state: Inputs are settings/environment/session state; outputs are splash/no-splash UI.
- gates_or_invariants: Splash must not appear in disallowed contexts.
- dependencies_and_callers: Validates coding-agent startup UI.
- edge_cases_or_failure_modes: Quiet/noninteractive startup and settings overrides.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1100 `file` `packages/coding-agent/test/theme-islight.test.ts`
- cursor: `[_]`
- core_role: Tests theme light/dark classification and exports.
- algorithmic_behavior: Classifies themes by color data and validates exported defaults.
- inputs_outputs_state: Inputs are theme definitions; outputs are `isLight` classification and default theme metadata.
- gates_or_invariants: Theme classification must stay stable for TUI contrast choices.
- dependencies_and_callers: Validates theme subsystem and native appearance integration expectations.
- edge_cases_or_failure_modes: Ambiguous colors, missing fields, and default export drift.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1130 `file` `packages/collab-web/scripts/build-tool-views.ts`
- cursor: `[_]`
- core_role: Build script bundling collab/web tool renderers for HTML exports.
- algorithmic_behavior: Runs `Bun.build` on `standalone.tsx`, extracts JS/CSS artifacts, inlines CSS injection, escapes `</script`, writes generated bundle, and exits on build failure; see lines 15-48.
- inputs_outputs_state: Inputs are React renderer sources and CSS; output is `packages/coding-agent/src/export/html/tool-views.generated.js`.
- gates_or_invariants: Build must produce JS; inline script escape prevents early HTML script termination.
- dependencies_and_callers: Used by `bun run build:tool-views` and coding-agent HTML export.
- edge_cases_or_failure_modes: Build logs/failure, missing JS artifact, CSS-only output, and unsafe `</script` byte sequence.
- validation_or_tests: Validated by build script execution in package workflows; not run here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1160 `file` `packages/hashline/src/types.ts`
- cursor: `[_]`
- core_role: Core data contracts for hashline parser, applier, patcher, streaming, compact diff, and block resolver.
- algorithmic_behavior: Defines anchors/cursors, concrete insert/delete edits, deferred block edits, apply results with block resolutions, snapshot split/stream options, and injected `BlockResolver` contract; block edit semantics are documented around lines 43-62 and resolver contract around lines 152-169.
- inputs_outputs_state: Inputs/outputs are type-level contracts consumed by hashline implementation and host integration.
- gates_or_invariants: Deferred block edits must be resolved before `applyEdits`; anchors are 1-indexed; block resolver returns `null` on unsupported/invalid syntax.
- dependencies_and_callers: Used across hashline parser/applier/patcher and coding-agent editing tools.
- edge_cases_or_failure_modes: Out-of-range anchors, unresolved block spans, stale snapshots, and host resolver absence.
- validation_or_tests: `packages/hashline/test` validates these contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1190 `file` `packages/mnemopi/test/cli-errors-parity.test.ts`
- cursor: `[_]`
- core_role: Tests mnemopi CLI error parity.
- algorithmic_behavior: Ensures CLI paths surface consistent errors for equivalent failure conditions.
- inputs_outputs_state: Inputs are CLI args/config states; outputs are exit/error messages.
- gates_or_invariants: Error text and exit semantics must be stable enough for users/scripts.
- dependencies_and_callers: Validates mnemopi CLI wrapper behavior.
- edge_cases_or_failure_modes: Missing args/config, invalid commands, and mismatch between command paths.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1220 `file` `packages/mnemopi/test/orchestrator.test.ts`
- cursor: `[_]`
- core_role: Tests mnemopi recall orchestration gates.
- algorithmic_behavior: Verifies polyphonic/linear recall orchestration and feature gates.
- inputs_outputs_state: Inputs are recall config and memory data; outputs are orchestrated recall results.
- gates_or_invariants: Feature flags must select correct recall path and maintain result shape.
- dependencies_and_callers: Validates mnemopi orchestrator code used by coding-agent memory.
- edge_cases_or_failure_modes: Disabled enhanced recall, empty memory, and mixed recall modes.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1250 `file` `packages/natives/native/loader-state.d.ts`
- cursor: `[_]`
- core_role: Type declaration for native addon loader state and helper algorithms.
- algorithmic_behavior: Declares contracts for compiled-binary detection, addon filename selection, node_modules staging, loader candidate resolution, stale cleanup, embedded archive extraction, and `loadNative`.
- inputs_outputs_state: Inputs are platform tags, env/import metadata, native dirs, embedded archive records; outputs are booleans, candidate paths, extracted paths, and loaded native module record.
- gates_or_invariants: Declaration-only; invariants live in JS implementation but types capture expected input/output surface.
- dependencies_and_callers: Used by native loader TypeScript consumers.
- edge_cases_or_failure_modes: Type drift from implementation would compile incorrectly; no runtime logic here.
- validation_or_tests: Covered by native loader tests/build if present; not executable in this file.
- skip_candidate: `yes: declaration-only API contract, not implementation`

### OH_MY_HUMANIZE_MAIN-HZ-1280 `file` `packages/snapcompact/research/exp08_foveate.py`
- cursor: `[_]`
- core_role: Research experiment for foveated two-tier reading over SQuAD chunks.
- algorithmic_behavior: Renders dense 5x8 archive images, asks model to answer or request zoom, parses row/phrase zoom requests, locates fuzzy phrases, merges/clamps row bands, renders 8x13 zoom crops, merges second-turn answers, scores EM/F1, and aggregates cost; key routines are `parse_zoom` lines 89-99, `locate_phrase` 102-122, `merge_bands` 125-134, `run_cell_chunk` 156-263, and `aggregate` 271-297.
- inputs_outputs_state: Inputs are SQuAD paragraphs, model list, prompts, API keys, chunk sizes, and cache flags; outputs are PNGs, JSONL records, matrix CSV, and summary JSON.
- gates_or_invariants: Truncated LLM responses are not cached; unresolved zoom requests become `UNREADABLE`; band slices are clamped to archive rows.
- dependencies_and_callers: Depends on local `squad`, `bdf`, `providers`, and `run` helpers plus Pillow and LLM APIs.
- edge_cases_or_failure_modes: Missing API keys, invalid zoom phrases, oversized zoom bands, truncated completions, empty question chunks, and cache corruption.
- validation_or_tests: Research script self-scores against SQuAD metrics and baseline table; not part of runtime CI.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1310 `file` `packages/snapcompact/research/snapcompact_convergence_extras.py`
- cursor: `[_]`
- core_role: Research visualization generator for carrier-convergence experiment outputs.
- algorithmic_behavior: Loads summary/NPZ arrays, computes shared PCA frame via SVD, renders funnel snapshots, pair-distance bars, and animated cross-similarity GIF; main routines are `render_funnel` lines 75-150 and `render_gif` 152-182.
- inputs_outputs_state: Inputs are `summary.json` and `carrier_convergence.npz`; outputs are `convergence-funnel.png` and `diagonal-emerges.gif`.
- gates_or_invariants: Uses best-layer metadata to keep projections comparable and creates output directories before save.
- dependencies_and_callers: Depends on NumPy and Pillow; manually run research asset tool.
- edge_cases_or_failure_modes: Missing NPZ keys, empty layers, absent fonts, and image save errors.
- validation_or_tests: Visual output is the validation artifact; not runtime CI.
- skip_candidate: `yes: research visualization, not product runtime, but algorithmic enough to document`

### OH_MY_HUMANIZE_MAIN-HZ-1340 `file` `packages/snapcompact/research/squad.py`
- cursor: `[_]`
- core_role: SQuAD dataset loader/sampler/scorer for snapcompact experiments.
- algorithmic_behavior: Downloads/caches dev-v1.1, flattens paragraphs, builds passage flow offsets, samples evenly spread questions inside chunk bounds, parses numbered answers, and implements official-ish EM/F1 normalization; see lines 14-67 and 73-120.
- inputs_outputs_state: Inputs are cache path, paragraph list, chunk range, answer text, and gold answers; outputs are flattened passages, sampled question records, parsed answers, and metric dicts.
- gates_or_invariants: Passages straddling chunk boundaries are skipped to avoid cut answers; scoring normalizes punctuation/articles/case.
- dependencies_and_callers: Used by `exp08_foveate.py` and related research scripts.
- edge_cases_or_failure_modes: Network download failure, empty eligible chunks, missing numbered answers, and zero token overlap.
- validation_or_tests: Metrics are deterministic; not runtime CI.
- skip_candidate: `yes: research helper, not product runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1370 `file` `packages/tui/src/deccara.ts`
- cursor: `[_]`
- core_role: Terminal renderer optimizer for rectangular SGR background fills.
- algorithmic_behavior: Parses final ANSI lines, tracks background SGR state, proves trailing full-width padding can be dropped, coalesces adjacent rows into DECCARA rectangles, and emits only byte-saving plans; key functions are `encodeDeccara` lines 43-45, `analyzeBgFillLine` 137-212, and `planDeccaraFills` 240-314.
- inputs_outputs_state: Inputs are final rendered ANSI lines, screen width, and first screen row; outputs are shortened line texts plus DECSACE-wrapped DECCARA sequence.
- gates_or_invariants: Bails on OSC/non-SGR CSI/malformed SGR/default or mixed background/partial-width lines; never emits a plan that increases byte count.
- dependencies_and_callers: Used by TUI renderer; depends on `visibleWidth`.
- edge_cases_or_failure_modes: Hyperlinks/images, colon-form colors, unterminated CSI, wide glyph widths, all-space rows, and scrollback-bound rendering.
- validation_or_tests: Covered by TUI rendering tests and DECCARA-specific behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1400 `file` `packages/tui/test/fuzzy.test.ts`
- cursor: `[_]`
- core_role: Tests fuzzy matching behavior for long tokens.
- algorithmic_behavior: Asserts long-token fuzzy matching remains bounded and useful.
- inputs_outputs_state: Inputs are candidate/query strings; outputs are match scores/results.
- gates_or_invariants: Matching should not degrade or explode on long input.
- dependencies_and_callers: Validates TUI fuzzy search/autocomplete logic.
- edge_cases_or_failure_modes: Very long single tokens and poor token boundaries.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1430 `file` `packages/tui/test/overlay-focus.test.ts`
- cursor: `[_]`
- core_role: Tests overlay focus routing in TUI.
- algorithmic_behavior: Exercises overlay focus stack and input dispatch.
- inputs_outputs_state: Inputs are focusable overlay components and key events; outputs are focused component state and routed events.
- gates_or_invariants: Overlay focus must restore correctly and avoid leaking input to background components.
- dependencies_and_callers: Validates TUI modal/overlay behavior used by coding-agent.
- edge_cases_or_failure_modes: Nested overlays, dismissed overlays, and stale focus target.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1460 `file` `packages/tui/test/text.test.ts`
- cursor: `[_]`
- core_role: Minimal test for TUI text component mutation.
- algorithmic_behavior: Verifies `Text.setText` changes rendered content/state.
- inputs_outputs_state: Input is replacement text; output is updated component text.
- gates_or_invariants: Component mutation must be observable.
- dependencies_and_callers: Validates basic TUI text component.
- edge_cases_or_failure_modes: Tiny low-risk test; no complex edge cases.
- validation_or_tests: This file is validation.
- skip_candidate: `yes: very small component smoke test, not core algorithm by itself`

### OH_MY_HUMANIZE_MAIN-HZ-1490 `file` `packages/utils/src/fs-error.ts`
- cursor: `[_]`
- core_role: Type-safe filesystem error classifier helpers.
- algorithmic_behavior: Defines `FsError` and guards for `ENOENT`, `EACCES`, `EISDIR`, `ENOTDIR`, `EEXIST`, `ENOTEMPTY`, plus generic `hasFsCode`; see lines 19-56.
- inputs_outputs_state: Input is unknown thrown value; output is typed boolean narrowing.
- gates_or_invariants: Requires `err instanceof Error` and string `code` before narrowing.
- dependencies_and_callers: Used across Bun/file IO error handling.
- edge_cases_or_failure_modes: Non-Error throwables and platform-specific codes.
- validation_or_tests: Covered indirectly by callers and fetch/file utility tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1520 `file` `packages/utils/test/fetch-retry.test.ts`
- cursor: `[_]`
- core_role: Tests fetch retry utility.
- algorithmic_behavior: Verifies retry behavior and override hooks.
- inputs_outputs_state: Inputs are mocked fetch failures/responses and retry options; outputs are retry count/result/error.
- gates_or_invariants: Retries must stop according to policy and preserve final failure.
- dependencies_and_callers: Validates shared fetch retry used by networked packages.
- edge_cases_or_failure_modes: Exhausted retries, successful later retry, and custom retry override.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1550 `file` `python/robomp/src/cancellation.py`
- cursor: `[_]`
- core_role: Per-event cancellation scope for Python robomp workers.
- algorithmic_behavior: Uses a `contextvars.ContextVar` to store `(sink, delivery_id)` for the current event; worker code registers/unregisters cancel hooks that arm/disarm the pool; functions are lines 35-65.
- inputs_outputs_state: Inputs are worker pool sink, delivery id, and hook callable; output is sink-side cancellation registration state.
- gates_or_invariants: No active context is a no-op; reset token must close the same scope.
- dependencies_and_callers: Shared by `WorkerPool` and worker/task execution without importing queue internals.
- edge_cases_or_failure_modes: Missing context, forgotten unregister, wrong reset token, and cancellation hook raising.
- validation_or_tests: `python/robomp/tests/test_host_tools.py` covers abort/cancellation contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1580 `file` `python/robomp/tests/test_host_tools.py`
- cursor: `[_]`
- core_role: Large contract suite for robomp GitHub/repo host tools.
- algorithmic_behavior: Tests repo-command env scrubbing/slot UID, GitHub comments/PR open/review tools, repro recording, abort signaling, issue/PR classification, label setting, branch identity gates, dirty-worktree checks, fix/check/push flows, force-with-lease recovery, and comment suffix scheduling.
- inputs_outputs_state: Inputs are temp repos, database rows, mocked GitHub/command calls, issue/PR metadata, and tool args; outputs are DB transitions, comments, labels, subprocess calls, and rejected tool results.
- gates_or_invariants: Enforces identity checks before push/PR, required PR template sections, closes keyword, clean worktree, `bun check`/fix gates, review-mode restrictions, and valid classification labels/ranks.
- dependencies_and_callers: Validates Python robomp host tools and GitHub proxy/orchestrator behavior.
- edge_cases_or_failure_modes: Root chown behavior, cleanup transport failure, idempotent abort, invalid branch slugs, failed check/fix, wrong identity scan range, and skip-check policy.
- validation_or_tests: This file is validation; representative tests start at lines 109, 575, 1415, 1764, 1957, and 2714.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1610 `directory` `packages/coding-agent/src/commit/changelog`
- cursor: `[_]`
- core_role: Commit-time changelog detection, generation, parsing, and application subsystem.
- algorithmic_behavior: `detect.ts` finds nearest changelog per staged file while skipping changelog edits; `parse.ts` extracts `[Unreleased]`; `generate.ts` prompts an LLM with diff/stat and validates tool/JSON response; `index.ts` truncates diffs, merges/dedupes entries, applies deletions, rewrites sections, and stages changed changelogs.
- inputs_outputs_state: Inputs are cwd, staged files, diff/stat, model/API key, proposals, dry-run flag; outputs are updated changelog paths and staged files.
- gates_or_invariants: Missing or unparsable changelogs are skipped with warnings; entries are normalized, case-insensitive deduped, and rendered only under `[Unreleased]`.
- dependencies_and_callers: Used by commit assistant flow, git utilities, prompt templates, and `completeSimple`.
- edge_cases_or_failure_modes: No staged files, no nearest changelog, huge diffs, LLM malformed output, missing file, and duplicate/deleted entries.
- validation_or_tests: Commit-split and commit assistant tests cover parts of this flow.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1640 `directory` `packages/coding-agent/src/web/scrapers`
- cursor: `[_]`
- core_role: Site-specific URL fetch/render handlers for coding-agent web fetch.
- algorithmic_behavior: Exports `SpecialHandler` list; each scraper gates on hostname/path, fetches official/public APIs or HTML, normalizes metadata/content to markdown through shared `buildResult`, and returns `null` for nonmatches/fallback.
- inputs_outputs_state: Inputs are URL, timeout, abort signal, and optional auth storage; outputs are `RenderResult` markdown/metadata or `null`.
- gates_or_invariants: Shared `types.ts` enforces bot-block user-agent rotation, timeout/size caps, charset decoding, retry-after handling, and HTML-to-markdown conversion.
- dependencies_and_callers: Used by web fetch tool; individual handlers cover package registries, docs, social/news, CVE/security, scholarly, media, and marketplace sources.
- edge_cases_or_failure_modes: Host spoofing, private/missing API data, non-JSON/XML fallback, bot blocks, oversized downloads, aborts, and malformed pages.
- validation_or_tests: `test/tools/web-scrapers/security.test.ts` covers NVD/OSV security gating and integration flags.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1670 `file` `crates/pi-shell/src/minimizer/pipeline.rs`
- cursor: `[_]`
- core_role: Declarative output minimizer pipeline engine.
- algorithmic_behavior: Parses TOML pipeline definitions, compiles regex/schema stages, applies ordered transformations: ANSI strip, replacements, match-output short-circuit, keep/strip lines, replace-after, line truncation, head/tail, max-lines, and empty-output fallback.
- inputs_outputs_state: Inputs are command output, exit code, context, and TOML definitions; outputs are minimized text or skipped/no-op.
- gates_or_invariants: Schema version parsing, regex compile failures, exit-code skips, stage order, and test definitions gate valid pipelines.
- dependencies_and_callers: Used by shell execution/minimizer stack; generated builtin filters come from `build.rs`.
- edge_cases_or_failure_modes: Malformed TOML, bad regex, zero-length output, over-aggressive stripping, and line-limit truncation.
- validation_or_tests: Pipeline `run_tests` support and Rust unit tests validate filter behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1700 `file` `packages/ai/src/dialect/catalog.ts`
- cursor: `[_]`
- core_role: In-band tool catalog prompt renderer for AI dialects.
- algorithmic_behavior: Converts tool definitions into JSON function records using `toolWireSchema`, renders catalog plus dialect instructions into static prompt template; core logic is lines 9-29.
- inputs_outputs_state: Inputs are tool definitions and dialect prompt; output is rendered system/developer prompt text.
- gates_or_invariants: Tool schemas are serialized through shared wire schema, not ad-hoc prompt text.
- dependencies_and_callers: Used by AI dialects that expose tools in-band rather than native function-calling.
- edge_cases_or_failure_modes: Empty tool set, schema serialization drift, and unsupported schema fields.
- validation_or_tests: Covered by dialect/tool-call tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1730 `file` `packages/ai/src/providers/aws-sigv4.ts`
- cursor: `[_]`
- core_role: AWS Signature Version 4 request signer.
- algorithmic_behavior: Implements SHA/HMAC helpers, signing key derivation, canonical path/query/header hashing, unsignable-header filtering, and `Authorization` header generation; key functions are around lines 74-218.
- inputs_outputs_state: Inputs are request URL/method/headers/body, credentials, region, service, and timestamp; outputs are signed headers/request.
- gates_or_invariants: Canonicalization must be stable; unsignable headers are excluded; payload hash and credential scope must match AWS spec.
- dependencies_and_callers: Used by Bedrock/AWS provider adapters.
- edge_cases_or_failure_modes: Header casing, query encoding, temporary session tokens, empty body, path escaping, and clock skew.
- validation_or_tests: Covered by provider request tests where Bedrock signing is exercised.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1760 `file` `packages/ai/src/providers/register-builtins.ts`
- cursor: `[_]`
- core_role: Lazy provider registration and stream watchdog infrastructure.
- algorithmic_behavior: Caches dynamic provider module promises, builds provider-specific loaders, forwards async streams through first-event/idle watchdogs, tracks aborts, and creates lazy stream wrappers; key areas are cache/loaders around lines 139-215 and stream forwarding 217-326.
- inputs_outputs_state: Inputs are model/provider request params, abort signals, provider loaders; outputs are registered provider factories and guarded streams.
- gates_or_invariants: First-event/idle timeouts surface provider-specific errors; aborts should not become provider timeout noise.
- dependencies_and_callers: Used by AI registry setup for OpenAI, Anthropic, Gemini, Bedrock, etc.
- edge_cases_or_failure_modes: Slow module import, provider hang before first event, idle stream, abort race, and loader failure.
- validation_or_tests: Request debug/auth/provider tests exercise lazy stream paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1790 `file` `packages/ai/src/registry/litellm.ts`
- cursor: `[_]`
- core_role: LiteLLM API-key login provider.
- algorithmic_behavior: Prompts user through registry callbacks, trims/rejects empty key, returns static key auth metadata, and marks provider as not OAuth.
- inputs_outputs_state: Input is user-provided key; output is registry auth result.
- gates_or_invariants: Empty key is rejected; no OAuth refresh contract is claimed.
- dependencies_and_callers: Used by AI registry login flow.
- edge_cases_or_failure_modes: Cancelled prompt and blank input.
- validation_or_tests: Covered by registry login tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1820 `file` `packages/ai/src/registry/wafer-pass.ts`
- cursor: `[_]`
- core_role: Registry descriptor for WaferPass login.
- algorithmic_behavior: Lazy-imports `loginWaferPass` and exposes provider login definition.
- inputs_outputs_state: Inputs are registry login callbacks; output is delegated WaferPass login result.
- gates_or_invariants: Keeps WaferPass login module off startup path until invoked.
- dependencies_and_callers: Used by AI registry provider list.
- edge_cases_or_failure_modes: Dynamic loader failure and provider module drift.
- validation_or_tests: Covered by registry login/provider tests if WaferPass is exercised.
- skip_candidate: `yes: thin registry adapter, not substantive algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1850 `file` `packages/ai/src/utils/json-parse.ts`
- cursor: `[_]`
- core_role: Resilient JSON parsing/repair utility for model/provider output.
- algorithmic_behavior: Repairs invalid escapes/control chars, parses with repair fallback, parses partial streaming JSON, and throttles parse attempts to avoid O(N^2) streaming behavior.
- inputs_outputs_state: Inputs are raw JSON-ish strings/chunks; outputs are parsed values or parse errors/null partials.
- gates_or_invariants: Repair is conservative and preserves valid JSON; streaming parser throttles by content growth.
- dependencies_and_callers: Used by tool-call/structured-output parsing.
- edge_cases_or_failure_modes: Unterminated strings, invalid escape sequences, control chars, partial objects, and repeated streaming prefixes.
- validation_or_tests: Covered by AI dialect/tool parsing tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1880 `file` `packages/catalog/src/identity/family.ts`
- cursor: `[_]`
- core_role: Memoized model-family classification and thinking-variant helpers.
- algorithmic_behavior: Classifies Kimi/Claude/Qwen/Gemma/Grok/OpenAI/GLM/MiniMax families, exposes support predicates for effort/thinking/system-message behavior, returns family tokens, and finds/strips thinking variant tokens.
- inputs_outputs_state: Input is model ID/name/provider metadata; output is boolean family capability or normalized token.
- gates_or_invariants: Memoization avoids repeated regex work; support predicates centralize model-specific policy.
- dependencies_and_callers: Used by catalog, AI provider request shaping, and coding-agent thinking UI.
- edge_cases_or_failure_modes: New model naming conventions, aliases, provider prefixes, and thinking suffix ambiguity.
- validation_or_tests: Catalog tests cover model bundle policies and reasoning support.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1910 `file` `packages/coding-agent/src/autoresearch/index.ts`
- cursor: `[_]`
- core_role: Built-in autoresearch extension state machine.
- algorithmic_behavior: Registers experiment tools/commands/shortcuts, rehydrates runtime from branch/session storage, toggles mode, ensures `autoresearch/*` branch, injects setup/runtime prompts before agent start, auto-resumes pending runs on agent end, and clears/reset sessions; see command flow lines 126-225, agent-end resume 257-292, prompt injection 294-412, and clear flow 414-456.
- inputs_outputs_state: Inputs are slash args, session branch/control entries, storage rows, run summaries, and lifecycle events; outputs are active tools, dashboard state, system prompts, user messages, and reset worktree/storage state.
- gates_or_invariants: Mode only applies on matching branch; storage is not created on untouched sessions; clear resets only when on autoresearch branch or forced.
- dependencies_and_callers: Uses extension API, git helpers, dashboard, storage/state builders, and prompt templates.
- edge_cases_or_failure_modes: Manual branch switch, pending run after agent end, storage missing, reset failure, legacy artifact cleanup failure, and duplicated tool activation.
- validation_or_tests: Autoresearch-specific behavior is covered by extension/workflow tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1940 `file` `packages/coding-agent/src/cli/config-cli.ts`
- cursor: `[_]`
- core_role: `omp config` command parser and settings mutator.
- algorithmic_behavior: Parses list/get/set/reset/path/help subcommands, schema-converts string values to typed settings, and dispatches handlers for settings store operations.
- inputs_outputs_state: Inputs are CLI args and settings schema; outputs are printed config values, changed settings, or reset state.
- gates_or_invariants: Rejects unknown keys, invalid typed values, and unsupported command forms.
- dependencies_and_callers: Used by CLI command registry and settings module.
- edge_cases_or_failure_modes: Boolean/number parsing, arrays/objects, missing value, and invalid key.
- validation_or_tests: CLI config tests cover command behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1970 `file` `packages/coding-agent/src/collab/guest.ts`
- cursor: `[_]`
- core_role: Guest-side collab live-session replica controller.
- algorithmic_behavior: Parses join link, connects websocket, writes host snapshot to replica JSONL, switches session without chdir, applies frames in arrival order via a promise chain, mirrors host state/agents/EventBus, routes prompts/abort/transcript requests to host, synthesizes missing assistant `message_start`, and restores local session on leave.
- inputs_outputs_state: Inputs are collab link, encrypted frames, local UI/session context, and guest commands; outputs are replica session file, UI state, mirrored registry, host commands, and restored session state.
- gates_or_invariants: Read-only links reject prompts/agent commands; commands allowed locally are whitelisted; no host cwd chdir; frames ignored before welcome/after leave.
- dependencies_and_callers: Uses `CollabSocket`, protocol crypto, session manager, event controller, AgentRegistry, and status line.
- edge_cases_or_failure_modes: Welcome timeout, reconnect resync, orphan stream deltas, pending transcript timeout, host bye/error, stale loading state, and unsaved previous sessions.
- validation_or_tests: Covered by collab session tests and live guest behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2000 `file` `packages/coding-agent/src/commands/ttsr.ts`
- cursor: `[_]`
- core_role: CLI command wrapper for Time-Traveling Stream Rules inspection/testing/scanning.
- algorithmic_behavior: Parses `list/test/scan`, maps flags into `TtsrCommandArgs`, treats positional existing file as test snippet file, supports stdin/file/rule/source/tool/path/verbose/json/no-gitignore/max-bytes, and delegates to `runTtsrCommand`; see lines 75-123.
- inputs_outputs_state: Inputs are CLI args/flags and snippet/file content; outputs are TTSR command results through CLI runner.
- gates_or_invariants: `--file` overrides positional; action determines whether test or scan args are populated.
- dependencies_and_callers: Uses `@oh-my-pi/pi-utils/cli` and `../cli/ttsr-cli`.
- edge_cases_or_failure_modes: Positional ambiguity, missing files, invalid source/action option, and scan limits.
- validation_or_tests: Covered by CLI/TTSR tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2030 `file` `packages/coding-agent/src/dap/config.ts`
- cursor: `[_]`
- core_role: Debug Adapter Protocol adapter selection/config resolution.
- algorithmic_behavior: Normalizes adapter defaults, resolves commands, lists available adapters, matches by extension/root markers, sorts launch candidates, selects attach adapter by explicit name/port/preference, and applies launch overrides for Go/dlv.
- inputs_outputs_state: Inputs are cwd, adapter name, program path/kind, port, and default adapter table; outputs are resolved adapter command/config/overrides.
- gates_or_invariants: Invalid adapter configs are dropped; unavailable commands are not returned; explicit adapter name wins.
- dependencies_and_callers: Used by debug tool/session launch and attach flows.
- edge_cases_or_failure_modes: Extensionless binaries, root-marker ties, missing commands, directory launch, and attach port selecting debugpy.
- validation_or_tests: Debug tool tests cover launch/attach rendering and behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2060 `file` `packages/coding-agent/src/discovery/omp-extension-roots.ts`
- cursor: `[_]`
- core_role: Discovery algorithm for OMP extension/plugin root directories.
- algorithmic_behavior: Merges injected CLI roots, settings roots, scope dirs, and installed plugin roots; resolves paths, checks directories, and returns extension roots.
- inputs_outputs_state: Inputs are cwd/settings/config root/injected roots; outputs are existing root paths.
- gates_or_invariants: Non-directories are skipped; injected roots can be cleared; path resolution avoids invalid roots.
- dependencies_and_callers: Used by extension loader/discovery.
- edge_cases_or_failure_modes: Missing settings, relative paths, inaccessible directories, duplicate roots, and stale installed plugin records.
- validation_or_tests: Extension discovery tests cover root resolution where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2090 `file` `packages/coding-agent/src/exec/exec.ts`
- cursor: `[_]`
- core_role: Small process execution wrapper around `ptree.exec`.
- algorithmic_behavior: Runs a command with cwd/signal/timeout, optionally allows nonzero/abort, and returns stdout/stderr/code/killed fields.
- inputs_outputs_state: Inputs are command args and exec options; outputs are normalized execution result.
- gates_or_invariants: Nonzero/abort handling is controlled by options rather than ad-hoc caller behavior.
- dependencies_and_callers: Used by coding-agent execution helpers.
- edge_cases_or_failure_modes: Timeout, abort, killed process, nonzero exit, and stderr capture.
- validation_or_tests: Execution tool tests cover command behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2120 `file` `packages/coding-agent/src/internal-urls/index.ts`
- cursor: `[_]`
- core_role: Public export surface for internal URL protocol router modules.
- algorithmic_behavior: Re-exports protocol handlers for `agent://`, `memory://`, `skill://`, `mcp://`, `local://`, artifacts/history/issues/rules/vault, parser, router, and types; comments describe process-global stateless handler model.
- inputs_outputs_state: No local state; output is module export surface.
- gates_or_invariants: Protocol handler exports must remain stable for consumers.
- dependencies_and_callers: Used by read/link resolution and input-controller large paste `local://` flow.
- edge_cases_or_failure_modes: Export drift breaks protocol resolution; no direct runtime logic here.
- validation_or_tests: Internal URL tests cover individual protocol modules.
- skip_candidate: `yes: index/barrel file, though it documents routing architecture`

### OH_MY_HUMANIZE_MAIN-HZ-2150 `file` `packages/coding-agent/src/mcp/client.ts`
- cursor: `[_]`
- core_role: MCP client connection, capability, tool/resource/prompt API.
- algorithmic_behavior: Creates stdio/HTTP/SSE transports, initializes with protocol version and roots capability, opens SSE before initialized notification, applies optional timeouts, paginates tools/resources/templates/prompts, calls tools, reads/subscribes resources, and handles optional templates `-32601` as empty; key flows are lines 90-199 and 276-509.
- inputs_outputs_state: Inputs are server config, abort signal, request handlers, cursors, tool args, resource URIs; outputs are `MCPServerConnection`, cached capabilities/items, call/read results.
- gates_or_invariants: Unsupported capabilities return empty; standard `ping`/`roots/list` server requests are handled; timeouts close pending transport.
- dependencies_and_callers: Used by MCP manager and AgentSession discovery/tool execution.
- edge_cases_or_failure_modes: Initialization abort, SSE listener race, optional method not found, pagination failures, subscribe rejection, and stale caches.
- validation_or_tests: `agent-session-mcp-discovery.test.ts` and MCP tests validate discovery/caching/outage behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2180 `file` `packages/coding-agent/src/mnemopi/state.ts`
- cursor: `[_]`
- core_role: Coding-agent mnemopi session state, scoped bank, recall, retain, and lifecycle manager.
- algorithmic_behavior: Lazily loads mnemopi modules, attaches state to sessions, resolves scoped retain/recall/global banks, merges recall results by id/content, broadens shared-bank fallback queries, injects first-turn recall context, retains transcripts on cadence/end, edits memories, consolidates/flushes on dispose; important areas are class lines 114-419 and bank/merge helpers 421-598.
- inputs_outputs_state: Inputs are session, backend config, messages, recall queries, memory edit args; outputs are recall context, retained memories, edited memory status, DB paths, and closed/consolidated resources.
- gates_or_invariants: Aliased subagents share resources but do not double-retain; auto recall runs once per first turn; retained transcript skips empty content; dispose may skip consolidation for clear.
- dependencies_and_callers: Uses mnemopi core, hindsight transcript/query helpers, session events, and config.
- edge_cases_or_failure_modes: Lazy module not loaded, recall target failure, duplicate banks, global/project token pollution, episodic memory update/forget ineligibility, and consolidation failure.
- validation_or_tests: `mnemopi-bank-derivation.test.ts` and mnemopi tests cover scoped banks/recall.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2210 `file` `packages/coding-agent/src/secrets/regex.ts`
- cursor: `[_]`
- core_role: Secret regex compiler for configured redaction patterns.
- algorithmic_behavior: Parses slash-delimited `/pattern/flags` or raw pattern strings, dedupes/merges flags, and enforces global `g`.
- inputs_outputs_state: Input is config regex string; output is `RegExp`.
- gates_or_invariants: All compiled regexes are global so repeated redaction works.
- dependencies_and_callers: Used by secret scanning/redaction paths.
- edge_cases_or_failure_modes: Invalid regex syntax, embedded slash flags, duplicate flags, and raw strings.
- validation_or_tests: Secret/redaction tests cover usage where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2240 `file` `packages/coding-agent/src/session/unexpected-stop-classifier.ts`
- cursor: `[_]`
- core_role: Classifies unexpected assistant `stop` events without tool calls.
- algorithmic_behavior: Checks candidate stop reason/text/tool-call absence, dispatches online or local tiny classifier based on settings, sends minimal yes/no prompt, and parses yes/no result.
- inputs_outputs_state: Inputs are stop reason, assistant text, tool calls, settings, model/API key; output is boolean unexpected-stop classification.
- gates_or_invariants: Only classifies `stop` with text and no tool calls; unsupported/missing classifier config disables or falls back.
- dependencies_and_callers: Used by session retry/stop handling; depends on smol/tiny inference and AI completion.
- edge_cases_or_failure_modes: Classifier timeout/failure, reasoning model max-token behavior, ambiguous output, missing API key, and local tiny unavailable.
- validation_or_tests: Stop/retry tests cover classifier behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2270 `file` `packages/coding-agent/src/task/output-manager.ts`
- cursor: `[_]`
- core_role: Allocates unique subagent/task output artifact IDs.
- algorithmic_behavior: Scans existing markdown artifacts, respects parent prefixes, extracts first filename segment, and allocates suffixes like `-2` for collisions.
- inputs_outputs_state: Inputs are artifact directory, parent id/prefix, desired base id; output is unique artifact id/path.
- gates_or_invariants: Existing artifacts and sibling prefixes are considered before allocation.
- dependencies_and_callers: Used by task/subagent output persistence.
- edge_cases_or_failure_modes: Existing files with dotted names, parent-child prefixes, missing artifact dir, and repeated allocations.
- validation_or_tests: Task/session-manager tests cover label/output behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2300 `file` `packages/coding-agent/src/tools/checkpoint.ts`
- cursor: `[_]`
- core_role: Checkpoint and rewind tool definitions/gates.
- algorithmic_behavior: Creates checkpoint tool only for eligible main sessions, rejects subagents/active checkpoint, returns goal/startedAt; creates rewind tool only when checkpoint exists and report is nonempty, returns report/rewound.
- inputs_outputs_state: Inputs are session/tool context and goal/report args; outputs are checkpoint state or rewind report.
- gates_or_invariants: Top-level-only, no nested active checkpoint, no rewind without checkpoint, no empty rewind report.
- dependencies_and_callers: Implements tools described by `docs/tools/rewind.md`.
- edge_cases_or_failure_modes: Subagent use, duplicate checkpoint, missing checkpoint, empty report, and session state mismatch.
- validation_or_tests: Tool/session tests cover checkpoint/rewind behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2330 `file` `packages/coding-agent/src/tools/match-line-format.ts`
- cursor: `[_]`
- core_role: Formats grep/search match lines for plain and hashline modes.
- algorithmic_behavior: Emits line markers with `*`/space status and `LINE:content` or `LINE|content` separators depending on mode.
- inputs_outputs_state: Inputs are line number/content/match flag/format; output is formatted line string.
- gates_or_invariants: Stable delimiters allow downstream parser/renderers to distinguish exact matches.
- dependencies_and_callers: Used by search/read tool render paths.
- edge_cases_or_failure_modes: Content containing separators and non-matching context lines.
- validation_or_tests: Tool rendering/search tests cover output formatting.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2360 `file` `packages/coding-agent/src/tts/player.ts`
- cursor: `[_]`
- core_role: Cross-platform audio playback command selector/runner.
- algorithmic_behavior: Chooses platform playback commands, spawns player, handles abort with SIGTERM/SIGKILL, collects failures, and cleans temp files.
- inputs_outputs_state: Inputs are audio file path and abort signal; output is successful playback or aggregated error.
- gates_or_invariants: Tries platform-appropriate commands in order and cleans up regardless of outcome.
- dependencies_and_callers: Used by TTS command/runtime.
- edge_cases_or_failure_modes: Missing playback command, abort during playback, hung process, Windows/macOS/Linux command differences, and cleanup failure.
- validation_or_tests: TTS tests cover command behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2390 `file` `packages/coding-agent/src/utils/image-loading.ts`
- cursor: `[_]`
- core_role: Image input loading/conversion/resizing utility.
- algorithmic_behavior: Excludes WebP for unsupported models, checks size limits, converts unsupported image formats, sequentially resizes context images, loads path/mime/data into base64 image content and notes.
- inputs_outputs_state: Inputs are image path/cwd/model/resize settings; outputs are `ImageContent`, MIME, and optional note/warning.
- gates_or_invariants: Enforces max image size and model format support before sending.
- dependencies_and_callers: Used by input controller, image paste, and multimodal prompts.
- edge_cases_or_failure_modes: Missing file, oversized image, unsupported/corrupt format, resize failure, WebP model exclusion, and MIME inference failure.
- validation_or_tests: `display-image-coerce.test.ts` and image tests cover conversion/coercion.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2420 `file` `packages/coding-agent/src/workflow/human-tool-runtime.ts`
- cursor: `[_]`
- core_role: Workflow human-input adapter backed by interactive AskTool.
- algorithmic_behavior: Creates a human node runner that requires interactive mode, asks a single `response` question with approve/reject options, maps selected/custom input into output, and returns fallback text when absent.
- inputs_outputs_state: Inputs are workflow human request and AskTool; outputs are response text plus selected/custom details.
- gates_or_invariants: Throws when no AskTool is available; custom input wins over selected option.
- dependencies_and_callers: Used by workflow runtime human nodes and tested by `human-tool-runtime.test.ts`.
- edge_cases_or_failure_modes: Noninteractive workflow run, user dismissal, no selected option, and custom-input absence.
- validation_or_tests: `packages/coding-agent/test/workflow/human-tool-runtime.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2450 `file` `packages/coding-agent/test/core/apply-patch-adverserial.test.ts`
- cursor: `[_]`
- core_role: Adversarial tests for apply-patch handling.
- algorithmic_behavior: Exercises malformed/confusing patch inputs and validates safe failure or correct application.
- inputs_outputs_state: Inputs are adversarial patch strings and target files; outputs are applied changes or structured errors.
- gates_or_invariants: Patch parser must not accept ambiguous/destructive malformed hunks.
- dependencies_and_callers: Validates core apply-patch tool behavior.
- edge_cases_or_failure_modes: Bad context, spoofed headers, path confusion, and malformed hunk boundaries.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2480 `file` `packages/coding-agent/test/debug/log-formatting.test.ts`
- cursor: `[_]`
- core_role: Tests debug/log formatting sanitization.
- algorithmic_behavior: Asserts log/debug text is formatted and sanitized for UI consumption.
- inputs_outputs_state: Inputs are log records/errors; outputs are formatted display strings.
- gates_or_invariants: Logs must not corrupt TUI display with raw control/tab/path content.
- dependencies_and_callers: Validates debug rendering/log formatting helpers.
- edge_cases_or_failure_modes: Control chars, tabs, long lines, and error objects.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2510 `file` `packages/coding-agent/test/eval/display-image-coerce.test.ts`
- cursor: `[_]`
- core_role: Tests image coercion for eval/display flows.
- algorithmic_behavior: Verifies image inputs are coerced into displayable/supported formats.
- inputs_outputs_state: Inputs are image data/path variants; outputs are normalized image payloads.
- gates_or_invariants: Unsupported formats must be converted or rejected consistently.
- dependencies_and_callers: Validates image-loading/eval display pipeline.
- edge_cases_or_failure_modes: Unsupported MIME, missing file, bad data, and resize/coercion failure.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2540 `file` `packages/coding-agent/test/marketplace/cache.test.ts`
- cursor: `[_]`
- core_role: Tests plugin marketplace cache and path traversal defenses.
- algorithmic_behavior: Validates cache read/write, source validation, and path escape rejection.
- inputs_outputs_state: Inputs are marketplace plugin metadata/source paths; outputs are cached entries or rejected resolutions.
- gates_or_invariants: Plugin cache must not allow traversal outside expected root.
- dependencies_and_callers: Validates extensibility marketplace source/cache logic.
- edge_cases_or_failure_modes: Malformed source, stale cache, missing plugin, and traversal paths.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2570 `file` `packages/coding-agent/test/session-manager/labels.test.ts`
- cursor: `[_]`
- core_role: Tests session label set/clear/tree/branch behavior.
- algorithmic_behavior: Verifies labels persist, clear, show in tree/branch contexts, and exclude inappropriate context.
- inputs_outputs_state: Inputs are session label commands/state; outputs are session metadata and UI/tree views.
- gates_or_invariants: Labels should not leak across unrelated branches/sessions.
- dependencies_and_callers: Validates session manager label handling.
- edge_cases_or_failure_modes: Clearing labels, branch changes, tree rendering, and context exclusion.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2600 `file` `packages/coding-agent/test/slash-commands/omfg.test.ts`
- cursor: `[_]`
- core_role: Tests `/omfg` slash-command suffix routing.
- algorithmic_behavior: Verifies command suffix parsing and routed behavior.
- inputs_outputs_state: Inputs are `/omfg` command strings; outputs are command dispatch results.
- gates_or_invariants: Suffixes must map only to intended handlers.
- dependencies_and_callers: Validates slash command registry/path.
- edge_cases_or_failure_modes: Unknown suffix and malformed command text.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2630 `file` `packages/coding-agent/test/task/task-schema.test.ts`
- cursor: `[_]`
- core_role: Tests task schema validation.
- algorithmic_behavior: Validates single-spawn and task payload shape constraints.
- inputs_outputs_state: Inputs are task tool/schema payloads; outputs are accepted task spec or validation errors.
- gates_or_invariants: Invalid multi-spawn or malformed task payloads are rejected before execution.
- dependencies_and_callers: Validates task tool schema.
- edge_cases_or_failure_modes: Missing fields, wrong types, and multiple spawn requests.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2660 `file` `packages/coding-agent/test/tools/edit-renderer.test.ts`
- cursor: `[_]`
- core_role: Tests edit/apply-patch renderer preview behavior.
- algorithmic_behavior: Covers streaming hashline previews, apply_patch previews, stats, result cache, and renderer consistency.
- inputs_outputs_state: Inputs are tool call args, partial args, and results; outputs are rendered preview/final UI text.
- gates_or_invariants: Streaming and rebuilt transcript render paths must agree.
- dependencies_and_callers: Validates coding-agent tool rendering for edit/apply_patch.
- edge_cases_or_failure_modes: Partial JSON, hashline stats mismatch, cached result reuse, and missing final result.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2690 `file` `packages/coding-agent/test/tools/multi-path-missing.test.ts`
- cursor: `[_]`
- core_role: Tests multi-path tool missing-file tolerance.
- algorithmic_behavior: Allows partial success when some paths are missing but rejects when all requested paths are missing.
- inputs_outputs_state: Inputs are path lists and filesystem state; outputs are result content or error.
- gates_or_invariants: At least one existing path is required for success.
- dependencies_and_callers: Validates multi-file read/search tools.
- edge_cases_or_failure_modes: All missing, some missing, and mixed path order.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2720 `file` `packages/coding-agent/test/tools/task-async-fallback.test.ts`
- cursor: `[_]`
- core_role: Tests task tool async fallback behavior.
- algorithmic_behavior: Ensures task tool falls back correctly when async execution path is unavailable or delayed.
- inputs_outputs_state: Inputs are task tool invocation and mocked runtime capabilities; outputs are fallback result or queued async state.
- gates_or_invariants: Task execution should not fail solely because preferred async path is unavailable.
- dependencies_and_callers: Validates task tool runtime.
- edge_cases_or_failure_modes: Missing async manager, delayed result, and fallback output.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2750 `file` `packages/coding-agent/test/workflow/dsl-compiler.test.ts`
- cursor: `[_]`
- core_role: Focused tests for `.omhflow` structured DSL compiler.
- algorithmic_behavior: Verifies modules, sequence, parallel, join, cycles, multiple blocks, templates, `retry_until`, and parallel review retries.
- inputs_outputs_state: Inputs are DSL documents; outputs are compiled workflow graph and validation errors.
- gates_or_invariants: Graph must be acyclic, references resolved, and retry/join semantics explicit.
- dependencies_and_callers: Validates workflow compiler used by runtime and slash command.
- edge_cases_or_failure_modes: Cycles, duplicate blocks, unresolved refs, bad templates, and retry predicate errors.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2780 `file` `packages/collab-web/src/tool-render/generic.tsx`
- cursor: `[_]`
- core_role: Fallback React renderer for tools without dedicated views.
- algorithmic_behavior: Summarizes args via `argsDigest`, JSON-stringifies args safely, renders args code block, result images, and result text; see lines 7-29.
- inputs_outputs_state: Inputs are tool args/result props; outputs are React summary/body nodes.
- gates_or_invariants: JSON stringify failure falls back to `String(args)`; empty `{}` args are hidden.
- dependencies_and_callers: Used by collab web/HTML tool rendering.
- edge_cases_or_failure_modes: Circular args, image-only results, huge result text, and missing result.
- validation_or_tests: Covered by collab-web render tests/build.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2810 `file` `packages/mnemopi/src/core/recall-diagnostics.ts`
- cursor: `[_]`
- core_role: Recall diagnostics accumulator and explainer.
- algorithmic_behavior: Tracks calls, fallback usage, true-empty calls, per-tier hit counts, fallback rates, reset/snapshot, and human-readable explanations; core class lines 44-122.
- inputs_outputs_state: Inputs are tier hit counts and call/fallback events; outputs are `RecallDiagnosticsSnapshot` and explanation strings.
- gates_or_invariants: Unknown tiers and negative hit counts throw; fallback rates clamp to 1.
- dependencies_and_callers: Used by mnemopi recall instrumentation.
- edge_cases_or_failure_modes: No calls, invalid tier labels, and reset boundaries.
- validation_or_tests: Mnemopi tests cover recall diagnostics where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2840 `file` `packages/swarm-extension/src/swarm/pipeline.ts`
- cursor: `[_]`
- core_role: Swarm pipeline wave/iteration orchestrator.
- algorithmic_behavior: Initializes per-agent result buckets, loops target iterations, executes waves sequentially with agents in each wave in parallel, updates state tracker/progress, aggregates errors, and returns completed/failed/aborted result; see `run` lines 56-120 and `#runIteration` 122-204.
- inputs_outputs_state: Inputs are swarm definition, waves, workspace, abort signal, model/settings, state tracker; outputs are pipeline state updates, logs, per-agent results, errors.
- gates_or_invariants: Abort checked before iterations/waves; per-agent exceptions become failed `SingleResult` rather than crashing the whole wave.
- dependencies_and_callers: Uses `executeSwarmAgent` and `StateTracker`.
- edge_cases_or_failure_modes: Aborted run, failed agent, fatal orchestrator error, empty waves, and model override handling.
- validation_or_tests: Swarm extension tests cover pipeline behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2870 `file` `python/robomp/src/proxy/__main__.py`
- cursor: `[_]`
- core_role: CLI entrypoint for robomp GitHub proxy server.
- algorithmic_behavior: Loads proxy-only settings, reports config errors as exit code 2, verifies GitHub token and HMAC key, configures logging/paths, creates FastAPI app, and runs uvicorn; lines 15-55.
- inputs_outputs_state: Inputs are env/config and `serve` command; output is running proxy process or config error.
- gates_or_invariants: Proxy mode must not require orchestrator-only settings but must require token/HMAC key.
- dependencies_and_callers: Uses Click, Uvicorn, `load_proxy_settings`, and `create_proxy_app`.
- edge_cases_or_failure_modes: Missing secrets, invalid config, path creation failure, and server bind failure.
- validation_or_tests: Python proxy/host tool tests validate related config behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2900 `file` `crates/pi-shell/src/minimizer/filters/bun.rs`
- cursor: `[_]`
- core_role: Bun command output classifier/minimizer.
- algorithmic_behavior: Routes Bun/package/test/build/lint/CPP/JS-tool invocations to specific filters, parses wrapper subcommands, compacts `bun check` diagnostics/package summaries/timeouts, strips build noise while preserving important failures, and includes unit tests for routing.
- inputs_outputs_state: Inputs are command context, raw output, exit code; outputs are minimized output or `None`.
- gates_or_invariants: Nonzero important diagnostics are preserved; package subcommands route differently from `bun run` tool invocations.
- dependencies_and_callers: Used by pi-shell minimizer registry and command-output rendering.
- edge_cases_or_failure_modes: Wrapper options with values, command chains, timeout text, build noise, nonzero child exits, and package/tool name ambiguity.
- validation_or_tests: Rust tests in the file validate subcommand routing and compaction examples.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2930 `file` `packages/ai/src/registry/oauth/github-copilot.ts`
- cursor: `[_]`
- core_role: GitHub Copilot OAuth/device-flow registry implementation.
- algorithmic_behavior: Builds public/enterprise URLs, starts device flow, polls for GitHub access token, refreshes Copilot token, discovers API endpoint, enables models in batches, and returns login metadata.
- inputs_outputs_state: Inputs are registry callbacks, enterprise domain, device auth responses, and Copilot API responses; outputs are OAuth token/config and enabled model metadata.
- gates_or_invariants: Polling handles device-flow errors; model enablement is batched; endpoint discovery precedes model use.
- dependencies_and_callers: Used by AI registry login for GitHub Copilot.
- edge_cases_or_failure_modes: Denied/expired device code, enterprise host mismatch, token refresh failure, endpoint discovery failure, and partial model enablement.
- validation_or_tests: `github-copilot-wire.test.ts` covers wire/catalog aspects; OAuth tests cover auth flow patterns.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2960 `file` `packages/ai/src/utils/schema/typescript.ts`
- cursor: `[_]`
- core_role: JSON Schema to TypeScript-ish renderer for human/tool docs.
- algorithmic_behavior: Renders literals, unions, JSDoc descriptions, arrays, objects, required/optional fields, enums, and root `$defs`.
- inputs_outputs_state: Input is JSON schema; output is TypeScript-like type string.
- gates_or_invariants: Unknown schema forms fall back safely; required fields control optional marker.
- dependencies_and_callers: Used by tool schema display/prompting.
- edge_cases_or_failure_modes: Nested arrays/objects, enum mixed types, missing type, additional defs, and description escaping.
- validation_or_tests: Schema rendering tests cover output where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2990 `file` `packages/coding-agent/src/commit/analysis/conventional.ts`
- cursor: `[_]`
- core_role: LLM-backed conventional commit analysis helper.
- algorithmic_behavior: Imports static prompts, defines conventional commit tool schema, renders user prompt from diff/context, calls `completeSimple` with max tokens/reasoning, and parses tool/JSON response.
- inputs_outputs_state: Inputs are diff/context/model/API key/thinking level; output is conventional commit analysis result.
- gates_or_invariants: Uses static `.md` prompts and typed tool schema to constrain response.
- dependencies_and_callers: Used by commit assistant analysis pipeline.
- edge_cases_or_failure_modes: Malformed LLM response, missing tool call, oversized diff, and unsupported reasoning level.
- validation_or_tests: Commit analysis tests cover conventional parsing where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3020 `file` `packages/coding-agent/src/eval/__tests__/budget-bridge.test.ts`
- cursor: `[_]`
- core_role: Tests evaluation budget bridge.
- algorithmic_behavior: Verifies budget settings/limits propagate into eval execution.
- inputs_outputs_state: Inputs are eval config/budget options; outputs are constrained eval request/runtime state.
- gates_or_invariants: Budget bridge must not drop or overrun configured limits.
- dependencies_and_callers: Validates coding-agent eval subsystem.
- edge_cases_or_failure_modes: Missing budget, zero/low budget, and default fallback.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3050 `file` `packages/coding-agent/src/extensibility/custom-tools/index.ts`
- cursor: `[_]`
- core_role: Barrel for custom tool loader/types/wrapper modules.
- algorithmic_behavior: Re-exports custom tools module surface (`loader`, `types`, `wrapper`) only; lines 1-7.
- inputs_outputs_state: No runtime state; output is public import path.
- gates_or_invariants: Export surface stability.
- dependencies_and_callers: Used by extension/custom tool loading consumers.
- edge_cases_or_failure_modes: Export drift breaks imports.
- validation_or_tests: Custom-tool loader tests cover underlying modules, not this barrel.
- skip_candidate: `yes: export-only barrel`

### OH_MY_HUMANIZE_MAIN-HZ-3080 `file` `packages/coding-agent/src/lsp/clients/index.ts`
- cursor: `[_]`
- core_role: LSP client factory/cache facade.
- algorithmic_behavior: Exports clients, caches clients by `serverName:cwd`, creates via factory/default, and clears/disposing clients.
- inputs_outputs_state: Inputs are server name, cwd, optional factory; outputs are cached LSP client instances.
- gates_or_invariants: Same server/cwd returns same client until clear; clear disposes resources.
- dependencies_and_callers: Used by coding-agent LSP integrations.
- edge_cases_or_failure_modes: Factory failure, cwd cache collision, stale disposed client, and clear-all cleanup.
- validation_or_tests: LSP tests cover client behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3110 `file` `packages/coding-agent/src/modes/components/countdown-timer.ts`
- cursor: `[_]`
- core_role: TUI countdown timer component.
- algorithmic_behavior: Tracks deadline, starts interval ticks every second, renders remaining time, supports reset and dispose.
- inputs_outputs_state: Inputs are duration/deadline callbacks; outputs are rendered timer text and tick invalidations.
- gates_or_invariants: Dispose clears interval; reset updates deadline.
- dependencies_and_callers: Used by setup/mode UI components needing countdown.
- edge_cases_or_failure_modes: Timer drift, expired timer, repeated reset, and leaked interval.
- validation_or_tests: Component tests cover timer behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3140 `file` `packages/coding-agent/src/modes/components/queue-mode-selector.ts`
- cursor: `[_]`
- core_role: TUI selector for queue execution mode.
- algorithmic_behavior: Creates a `SelectList` for `one-at-a-time`/`all`, preselects current mode, wires change callbacks, and exposes current selection.
- inputs_outputs_state: Inputs are current mode and callback; output is selected queue mode.
- gates_or_invariants: Only two known queue modes are selectable.
- dependencies_and_callers: Used by coding-agent queue setup UI.
- edge_cases_or_failure_modes: Invalid current mode fallback and callback failure.
- validation_or_tests: UI selector tests cover similar component behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3170 `file` `packages/coding-agent/src/modes/controllers/input-controller.ts`
- cursor: `[_]`
- core_role: Main interactive input/keybinding dispatcher for coding-agent TUI.
- algorithmic_behavior: Registers editor/global key handlers, handles Escape/Ctrl-C/D/Z, detects double-left agent hub gesture, routes Enter through extensions/slash/skill/bash/python/collab/loop/compaction/streaming/normal prompt paths, queues steer/follow-up messages, restores queued messages with image marker shifts, manages paste/image/large-paste/local attachments, and cycles model/thinking/tool expansion.
- inputs_outputs_state: Inputs are editor text, pending images, key events, clipboard payloads, session state, focused agent/collab state; outputs are prompt calls, queued messages, tool commands, UI state, session history, local attachments, aborts, and restored drafts.
- gates_or_invariants: Focused subagent blocks main-only commands; collab guest blocks host-only/local execution and read-only prompts; compaction queues instead of dispatching; failed dispatch restores text/images; large-paste file refs use `local://`.
- dependencies_and_callers: Uses settings, session manager, slash registry, image loading/resizing, enhanced paste, title generation, and internal URL local root.
- edge_cases_or_failure_modes: Orphan submit with no waiter, background stream race, image path over SSH, transient Windows screenshot paths, modal paste focus, terminal arrow burst false positives, Ctrl+C shutdown hard abort, and queued image marker renumbering.
- validation_or_tests: `input-controller-orphan-submit.test.ts`, paste/image tests, hook selector tests, and mode/controller tests cover key paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3200 `file` `packages/coding-agent/src/slash-commands/helpers/active-oauth-account.ts`
- cursor: `[_]`
- core_role: Helper for matching active OAuth account usage-limit metadata.
- algorithmic_behavior: Normalizes account identity and matches usage limits/reports by account id, email, project id, or metadata scope.
- inputs_outputs_state: Inputs are OAuth account and usage-limit records; output is matched active account/report.
- gates_or_invariants: Matching prefers concrete account/project identifiers over loose metadata.
- dependencies_and_callers: Used by slash commands that display OAuth account/usage status.
- edge_cases_or_failure_modes: Missing identity, multiple accounts, project-scoped limits, and email/account mismatch.
- validation_or_tests: OAuth slash-command tests cover usage display where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3230 `file` `packages/coding-agent/src/web/scrapers/chocolatey.ts`
- cursor: `[_]`
- core_role: Chocolatey package URL scraper.
- algorithmic_behavior: Gates on Chocolatey package URLs, queries NuGet OData, parses JSON or XML fallback, formats package metadata/install command/dependencies into markdown, and returns `null` on nonmatch/failure.
- inputs_outputs_state: Inputs are package URL, timeout, abort signal; outputs are package markdown `RenderResult`.
- gates_or_invariants: Only Chocolatey package hosts/paths are handled; failures fall through to generic fetch.
- dependencies_and_callers: Used by web fetch scraper registry.
- edge_cases_or_failure_modes: Missing package, OData JSON failure, XML fallback mismatch, package ID casing, and network abort.
- validation_or_tests: Web scraper tests cover gating patterns.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3260 `file` `packages/coding-agent/src/web/scrapers/mdn.ts`
- cursor: `[_]`
- core_role: MDN documentation scraper.
- algorithmic_behavior: Gates on MDN docs paths, maps page URL to MDN `/index.json`, converts sections/metadata into markdown, and returns null for failures; key lines are 111-168.
- inputs_outputs_state: Inputs are MDN URL and fetch controls; output is markdown documentation page.
- gates_or_invariants: Only recognized MDN docs URLs are handled; API parse failure falls back.
- dependencies_and_callers: Used by web fetch scraper registry.
- edge_cases_or_failure_modes: Locale/path variants, missing index JSON, section structure drift, and network failure.
- validation_or_tests: Web scraper tests cover security/gating.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3290 `file` `packages/coding-agent/src/web/scrapers/terraform.ts`
- cursor: `[_]`
- core_role: Terraform Registry module/provider scraper.
- algorithmic_behavior: Gates module/provider URLs, calls registry API, renders modules with inputs/outputs/resources/deps/submodules caps, renders provider docs grouped by category; key sections are 68-97, 99-213, and 215-277.
- inputs_outputs_state: Inputs are Terraform Registry URL and fetch controls; output is registry markdown.
- gates_or_invariants: Caps noisy lists; nonmatching or failing requests return null.
- dependencies_and_callers: Used by web fetch scraper registry.
- edge_cases_or_failure_modes: Registry API drift, missing provider docs, module namespace/name/provider ambiguity, and huge metadata lists.
- validation_or_tests: Web scraper tests cover gating patterns.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3320 `file` `packages/coding-agent/test/modes/components/hook-selector-slider.test.ts`
- cursor: `[_]`
- core_role: Tests model slider behavior in hook selector component.
- algorithmic_behavior: Verifies slider state, option selection, and rendering behavior.
- inputs_outputs_state: Inputs are selector options/model states/key events; outputs are selected option and rendered slider.
- gates_or_invariants: Slider must reflect active model and update predictably.
- dependencies_and_callers: Validates mode UI hook selector.
- edge_cases_or_failure_modes: Empty options, wraparound, and active-index mismatch.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3350 `file` `packages/coding-agent/test/modes/controllers/event-controller-interrupt.test.ts`
- cursor: `[_]`
- core_role: Tests aborted-turn working message rendering/event handling.
- algorithmic_behavior: Verifies event controller handles interruption/abort events and working messages correctly.
- inputs_outputs_state: Inputs are synthetic session events; outputs are UI/event-controller state.
- gates_or_invariants: Aborted turns must not leave stale working indicators.
- dependencies_and_callers: Validates event controller in interactive mode.
- edge_cases_or_failure_modes: Interrupt during streaming and stale loading state.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3380 `file` `packages/coding-agent/test/tools/web-scrapers/security.test.ts`
- cursor: `[_]`
- core_role: Security tests for web scraper URL gating.
- algorithmic_behavior: Validates NVD/OSV and related scraper host/path matching, plus optional integration fetches under `WEB_FETCH_INTEGRATION`.
- inputs_outputs_state: Inputs are benign/malicious URLs and optional network integration flag; outputs are handled/null scraper results.
- gates_or_invariants: Scrapers must not accept spoofed hosts or unsafe URL patterns.
- dependencies_and_callers: Validates `packages/coding-agent/src/web/scrapers`.
- edge_cases_or_failure_modes: Hostname spoofing, path confusion, and public API failure.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3410 `file` `packages/collab-web/src/tool-render/tools/debug.tsx`
- cursor: `[_]`
- core_role: Dedicated React renderer for debug/DAP tool calls.
- algorithmic_behavior: Extracts session snapshot from result details, summarizes action/program/file/target, renders scalar args, expression/custom args, snapshot status/location/configuration-needed, and result text; key routines are `snapshotOf` lines 22-40, `Summary` 60-78, and `Body` 113-209.
- inputs_outputs_state: Inputs are debug tool args/result; outputs are React summary/body.
- gates_or_invariants: Snapshot fields are type-checked before rendering; long targets/args are truncated.
- dependencies_and_callers: Used by collab-web/HTML tool renderer registry.
- edge_cases_or_failure_modes: Missing snapshot, nonnumeric line/column, circular custom args, and long expressions.
- validation_or_tests: Render/build tests cover component output.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3440 `file` `packages/mnemopi/src/core/beam/recall.ts`
- cursor: `[_]`
- core_role: Hybrid memory recall engine for mnemopi beam memory.
- algorithmic_behavior: Tokenizes/expands synonyms, builds FTS/vector/fallback candidates, applies temporal/current boosts, veracity and degradation weights, lexical relevance, cross-tier summary dedupe, coverage/MMR reranking, recall-count updates, enhanced recall with facts, and context formatting; key functions are `scoreCandidate` lines 678-767, `recall` 915-966, `recallEnhanced` 1001-1026, and `factRecall` 1077-1173.
- inputs_outputs_state: Inputs are beam DB state, query, topK, filters/weights/options; outputs are ranked `RecallResult[]` and formatted context.
- gates_or_invariants: `topK <= 0` returns empty; invalid query time throws; session/fact visibility scopes apply; low lexical+dense candidates are dropped.
- dependencies_and_callers: Uses embeddings, MMR, query intent, synonyms, temporal parser, SQLite beam state.
- edge_cases_or_failure_modes: Missing FTS/vector tables, embedding disabled, malformed embeddings, empty query, current/latest queries, fact table schema with/without scope, and recall-count update scope.
- validation_or_tests: Mnemopi orchestrator and recall tests validate feature gates and result shape.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3470 `file` `packages/stats/src/client/routes/RequestsRoute.tsx`
- cursor: `[_]`
- core_role: Stats dashboard route for recent requests.
- algorithmic_behavior: Polls recent requests every 30s when active, memoizes table columns, formats model/provider/time/tokens/cost/duration/status, renders mobile cards, and emits request-click callbacks; see lines 15-123.
- inputs_outputs_state: Inputs are active flag, refresh trigger, API response; outputs are table/mobile UI rows and selected request id.
- gates_or_invariants: Fetch only when route is active; failed requests render danger status.
- dependencies_and_callers: Uses stats API, resource hook, formatters, DataTable, Panel, StatusPill.
- edge_cases_or_failure_modes: Missing request id, error messages, empty list, inactive route, and polling refresh.
- validation_or_tests: Stats UI tests cover route/resource behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3500 `file` `python/robomp/web/src/components/Working.tsx`
- cursor: `[_]`
- core_role: Solid component showing currently running robomp work.
- algorithmic_behavior: Merges running events with inflight-only keys, dedupes by issue/delivery key, formats elapsed time/model/last tool/attempt, and gates cancel button on replay enabled and not inflight-only; core helpers lines 24-77 and render lines 79-160.
- inputs_outputs_state: Inputs are status resource running events/inflight list and config; outputs are table rows and cancel requests.
- gates_or_invariants: Confirm dialog gates cancellation; inflight-only rows cannot be cancelled from this UI.
- dependencies_and_callers: Uses status state, `runCancel`, format helpers, issue links, and shared UI components.
- edge_cases_or_failure_modes: Missing issue key, invalid started timestamp, stale inflight key, replay disabled, and cancel failure.
- validation_or_tests: Web component tests cover dashboard behavior where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3530 `file` `packages/coding-agent/src/extensibility/plugins/marketplace/source-resolver.ts`
- cursor: `[_]`
- core_role: Marketplace plugin source resolver with path safety.
- algorithmic_behavior: Resolves relative sources within marketplace/root/plugin root, enforces path-is-within guards, clones object sources by URL/GitHub/git-subdir with sha/ref, rejects unsupported npm/default unknown sources, and verifies resolved directories.
- inputs_outputs_state: Inputs are plugin source spec, marketplace/root/plugin root, cache/clone settings; outputs are resolved plugin directory.
- gates_or_invariants: Relative paths must remain inside allowed roots; failed clone cleanup prevents stale partial source.
- dependencies_and_callers: Used by plugin marketplace installer/cache.
- edge_cases_or_failure_modes: Path traversal, unsupported source type, clone failure, missing directory, ref/sha mismatch, and cleanup failure.
- validation_or_tests: `marketplace/cache.test.ts` covers cache/path traversal behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3560 `file` `packages/coding-agent/src/modes/setup-wizard/scenes/types.ts`
- cursor: `[_]`
- core_role: Type contracts for setup wizard scene/tab controllers.
- algorithmic_behavior: Defines scene result, host API, controller lifecycle/mouse routing, tab modal/render/input API, and scene mount/shouldRun contract; lines 4-57.
- inputs_outputs_state: Inputs/outputs are type-level UI controller interfaces and scene results.
- gates_or_invariants: Modal tabs must own keyboard input and prevent parent tab switching/finish while modal.
- dependencies_and_callers: Used by setup wizard scene implementations.
- edge_cases_or_failure_modes: Contract drift can break lifecycle/focus/mouse routing; no runtime code here.
- validation_or_tests: Setup wizard component tests validate implementations.
- skip_candidate: `yes: type-only contract file, no executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3590 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/grid.ts`
- cursor: `[_]`
- core_role: Grid-based layout engine for vendored Mermaid-to-ASCII renderer.
- algorithmic_behavior: Converts grid to drawing coordinates, reserves 3x3 node blocks with collision shifting, computes shape-aware column/row sizes, handles subgraph membership/direction/bounds/offsets, places roots/children level-by-level, bundles/routes edges, determines labels, draws nodes, and sizes canvases; key routines are `reserveSpotInGrid` lines 75-103, subgraph bounds 266-377, and `createMapping` 394-564.
- inputs_outputs_state: Input is parsed `AsciiGraph`; output is mutated graph with grid coordinates, drawing coordinates, edge paths, node drawings, canvas sizes, and subgraph boxes.
- gates_or_invariants: Nodes occupy reserved 3x3 regions; disconnected/non-topological placement loop breaks on no progress; subgraph offsets prevent negative drawing coordinates.
- dependencies_and_callers: Uses canvas, edge routing/bundling, shape dimensions, and draw helpers.
- edge_cases_or_failure_modes: Grid collisions, mixed LR/TD subgraph direction, external incoming edges to subgraphs, disconnected nodes, overlapping subgraphs, and bundled-edge label placement.
- validation_or_tests: Mermaid ASCII renderer tests cover layout rendering where present.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 120 item-evidence headings audited against the scheduler table, each represented once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`