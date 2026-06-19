# agent_13 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-013 `file` `bunfig.toml`
- cursor: `[_]`
- core_role: Workspace-level Bun runtime/test/install configuration that affects module loading, dependency resolution, and root test discovery.
- algorithmic_behavior: Disables telemetry, forces hoisted/exact installs, sets text loaders for `.md`, `.py`, and `.lark`, and excludes large/generated/runtime directories from `bun test` traversal (`bunfig.toml:1`, `bunfig.toml:3`, `bunfig.toml:10`, `bunfig.toml:15`).
- inputs_outputs_state: Input is Bun’s config loader; output is install/test/runtime behavior. No mutable state beyond toolchain interpretation.
- gates_or_invariants: `minimumReleaseAge = 259200` gates new package versions except Bun typings; `pathIgnorePatterns` prevents test walking into Python, docs, worktrees, dist, target, etc. (`bunfig.toml:4`, `bunfig.toml:18`).
- dependencies_and_callers: Consumed by Bun install, Bun runtime loaders, and `bun test`.
- edge_cases_or_failure_modes: If loaders are removed, prompt/script imports as text can fail; if ignores are loosened, root tests can enter cloned/scratch repos.
- validation_or_tests: Indirectly validated by all Bun test and runtime import paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-043 `directory` `scripts/session-stats`
- cursor: `[_]`
- core_role: Offline analytics toolkit for session JSONL/SQLite stats, tool usage, read optimization, search relevance, selector coverage, harmony edit backtests, and LLM-assisted audit.
- algorithmic_behavior: Recursively inspected 27 files: Python analyzers (`analyze.py`, `read_optimizer.py`, `harmony_backtest.py`, selector/search scripts), plotting scripts, TypeScript audit CLI/test, and generated PNG outputs. Key functions classify edits, aggregate usage, replay read configs, scan assistant/tool rows, and render matplotlib reports (`scripts/session-stats/analyze.py:119`, `scripts/session-stats/read_optimizer.py:565`, `scripts/session-stats/harmony_backtest.py:447`, `scripts/session-stats/audit.ts:310`).
- inputs_outputs_state: Inputs are `~/.omp` session/stat stores, SQLite rows, CLI flags, and optional LLM classifier model. Outputs are console reports, JSON exports/cache, and PNG artifacts under `scripts/session-stats/out`.
- gates_or_invariants: Read-only DB opens, time filters, binary/large file checks, cache keys, schema validation for verdicts, and sweep/recommendation Pareto rules.
- dependencies_and_callers: Depends on Python `sqlite3`, `matplotlib`, `numpy`, Bun test/runtime, and pi-ai classifier calls in `audit.ts`.
- edge_cases_or_failure_modes: Missing DB, malformed JSON args, incomplete edit markup, unavailable classifier, stale cache, and generated `out/*.png` being analysis artifacts rather than source algorithms.
- validation_or_tests: `scripts/session-stats/audit.test.ts` covers audit parser/scanner behavior; plots and reports are manually/CLI validated.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-073 `file` `docs/session.md`
- cursor: `[_]`
- core_role: Architecture contract for coding-agent session persistence, JSONL entry model, migration expectations, and context reconstruction.
- algorithmic_behavior: Defines session file layout, header/entry taxonomy, append-only tree semantics, `leafId` branch navigation, blob store, terminal breadcrumbs, and loader/migration responsibilities (`docs/session.md:18`, `docs/session.md:33`, `docs/session.md:63`, `docs/session.md:106`).
- inputs_outputs_state: Inputs are session JSONL files, blob refs, cwd/session metadata, and old-version records. Outputs are migrated in-memory sessions and reconstructed LLM context.
- gates_or_invariants: Header first line, one JSON object per line, parent tree via `id`/`parentId`, entries append-only, missing `version` means v1, and `parentSession` is opaque metadata (`docs/session.md:65`, `docs/session.md:88`, `docs/session.md:104`).
- dependencies_and_callers: Documents `packages/coding-agent/src/session/session-manager.ts`, `session-loader.ts`, `session-context.ts`, `session-storage.ts`, `blob-store.ts`.
- edge_cases_or_failure_modes: Old malformed files, branch-from-root `"root"` marker, blob externalization/truncation, and best-effort path migration.
- validation_or_tests: Session storage/context tests and internal URL history tests indirectly enforce this contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-103 `file` `scripts/inline-functions.test.ts`
- cursor: `[_]`
- core_role: Regression test suite for the inline-functions refactoring script.
- algorithmic_behavior: Uses `ts-morph` Project setup to test guard inversion, argument substitution, strict side-effect handling, multiple call-site behavior, safety skips, type soundness, formatting, hoisted temp names, and object shorthand preservation (`scripts/inline-functions.test.ts:1`, `scripts/inline-functions.test.ts:30`, `scripts/inline-functions.test.ts:110`, `scripts/inline-functions.test.ts:205`).
- inputs_outputs_state: Inputs are synthetic TypeScript source strings and `Options`; output is transformed code plus expected skip behavior.
- gates_or_invariants: Inlining must preserve semantics, avoid unsafe side effects/collisions, and not degrade formatting or type behavior.
- dependencies_and_callers: Tests `scripts/inline-functions.ts`, `bun:test`, and `ts-morph`.
- edge_cases_or_failure_modes: Local-name collisions, multiple call sites, guardless transforms, object shorthand, and strict effect mode false positives/negatives.
- validation_or_tests: This file is the validation surface for the script.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-133 `directory` `packages/coding-agent/src`
- cursor: `[_]`
- core_role: Primary CLI implementation root for coding-agent: session runtime, TUI modes, tools, workflow engine, task/subagent orchestration, discovery, config, MCP, LSP, web, commit automation, and eval backends.
- algorithmic_behavior: Recursively inspected inventory of 1268 files. Major algorithmic clusters include `session` persistence/replay, `task` subagent execution, `workflow` DAG/runtime parsing, `tools` command/tool implementations, `modes` TUI controllers/components, `commit` message/changelog synthesis, `discovery` provider loading, `eval` JS/Python kernels, `web` search/scrapers, and `extensibility` plugins.
- inputs_outputs_state: Inputs include CLI args, settings, prompts, model registry, session JSONL, tool calls, MCP/plugin manifests, files, browsers, web responses, and subprocess streams. Outputs include TUI frames, tool results, session entries, background jobs, workflow state, plugin registrations, commits, and exported artifacts.
- gates_or_invariants: Central invariants include no raw console logging in TUI paths, sanitized render output, typed tool schemas, session append-only semantics, async job caps, task recursion/isolation gates, workflow reference validation, and config schema validation.
- dependencies_and_callers: Called by CLI commands under `packages/coding-agent/src/commands`, SDK/RPC, tests under `packages/coding-agent/test`, and sibling packages `pi-ai`, `pi-agent-core`, `pi-tui`, `pi-utils`, `pi-natives`, `pi-catalog`.
- edge_cases_or_failure_modes: Cross-cutting risks include stale session migrations, unsanitized output corrupting TUI, leaked async jobs, plugin install rollback failure, tool timeout/cancellation races, malformed workflow YAML, and provider/model mismatch.
- validation_or_tests: Broad package tests cover agent sessions, MCP, plugin discovery, workflow, task, TUI components, tools, and scrapers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-163 `directory` `python/omp-rpc/src`
- cursor: `[_]`
- core_role: Python RPC SDK/client bridge for driving coding-agent sessions, host tools, host URI handlers, and typed protocol events.
- algorithmic_behavior: Recursively inspected 6 files. `client.py` manages subprocess lifecycle, pending requests, listener/error events, bounded history, prompt turn coordination, and request/response parsing; `protocol.py` defines typed messages/events and parse helpers; `host_tools.py` and `host_uris.py` register decorators and normalize host return payloads (`python/omp-rpc/src/omp_rpc/client.py:334`, `python/omp-rpc/src/omp_rpc/protocol.py:267`, `python/omp-rpc/src/omp_rpc/host_tools.py:62`, `python/omp-rpc/src/omp_rpc/host_uris.py:75`).
- inputs_outputs_state: Inputs are JSON RPC payloads, subprocess stdout/stderr, host tool callbacks, URI reads, and agent messages. Outputs are typed dataclasses/TypedDicts, normalized JSON result objects, notifications, and raised protocol/timeout/process errors.
- gates_or_invariants: JSON clone helpers reject non-JSON values; literal/type parsers validate protocol discriminants; client guards concurrency and process lifecycle.
- dependencies_and_callers: Python consumers import `RpcClient`, `host_tool`, `host_uri`, and protocol helpers from `omp_rpc`.
- edge_cases_or_failure_modes: Malformed JSON, missing fields, subprocess exit, request timeout, host callback exceptions, and invalid host URI result shapes.
- validation_or_tests: `python/omp-rpc/tests/test_host_uris.py` validates host URI normalization and bridge behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-193 `file` `docs/tools/job.md`
- cursor: `[_]`
- core_role: Contract documentation for the `job` tool and async job manager behavior.
- algorithmic_behavior: Specifies `poll`, `cancel`, and `list` inputs; describes manager lookup, cancellation-before-poll flow, watch-set resolution, `Promise.race` wait behavior, progress updates, delivery suppression, and final grouping (`docs/tools/job.md:15`, `docs/tools/job.md:46`, `docs/tools/job.md:63`, `docs/tools/job.md:67`).
- inputs_outputs_state: Inputs are job IDs and tool args; outputs are text sections plus `details.jobs` and optional `details.cancelled`.
- gates_or_invariants: `list` is read-only and mutually exclusive; other-agent jobs are invisible; cancelled jobs abort via `AbortController`; non-running jobs are acknowledged to suppress follow-up delivery (`docs/tools/job.md:19`, `docs/tools/job.md:43`, `docs/tools/job.md:70`).
- dependencies_and_callers: Documents `tools/job.ts`, `async/job-manager.ts`, `tools/bash.ts`, `task/index.ts`, `sdk.ts`, and settings schema.
- edge_cases_or_failure_modes: Empty watch sets, missing IDs, timeout as non-error snapshot, completion delivery duplication, and job manager absence.
- validation_or_tests: Async job/tool tests and docs consistency with `job-manager.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-223 `file` `scripts/session-stats/plot_tools.py`
- cursor: `[_]`
- core_role: Session-stat plotting script for tool token/call behavior.
- algorithmic_behavior: Connects to SQLite, selects top tools, fetches daily/per-call series, smooths arrays, computes weekly medians, and renders panels for total tokens, call counts, mean per call, cumulative tokens, weekly medians, and histograms (`plot_tools.py:48`, `plot_tools.py:65`, `plot_tools.py:82`, `plot_tools.py:197`, `plot_tools.py:219`).
- inputs_outputs_state: Inputs are DB rows and CLI args; outputs are matplotlib PNG charts under the stats output directory.
- gates_or_invariants: Case normalization SQL, finite/nan-aware smoothing, top-N tool filtering, and explicit time-axis formatting.
- dependencies_and_callers: Uses `sqlite3`, `numpy`, `matplotlib`, and stats DB schema produced by session stats sync.
- edge_cases_or_failure_modes: Empty tool sets, sparse daily rows, NaN median windows, missing DB, and non-normalized tool names.
- validation_or_tests: Manual graph generation; indirectly covered by script execution in stats analysis workflow.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-253 `directory` `packages/coding-agent/src/commit`
- cursor: `[_]`
- core_role: Commit automation subsystem for conventional analysis, agentic commit planning, changelog updates, diff parsing, split commits, and model selection.
- algorithmic_behavior: Recursively inspected 56 files. Key roles: `pipeline.ts` runs commit command; `git/diff.ts` parses numstat/file diffs/hunks; `analysis/*` derives conventional type/scope/summary; `agentic/*` creates an agent session with commit tools; `changelog/*` detects and applies Unreleased entries; `map-reduce/*` handles large diffs; prompts are static markdown (`packages/coding-agent/src/commit/git/diff.ts:3`, `packages/coding-agent/src/commit/agentic/index.ts:27`, `packages/coding-agent/src/commit/changelog/index.ts:40`).
- inputs_outputs_state: Inputs are git diffs/status/numstat, model registry/settings, changelog files, and user confirmation. Outputs are commit messages, staged commits, changelog edits, split plans, warnings, and agent state.
- gates_or_invariants: Excluded files filtered, summary length/style validation, dependency ordering for split commits, changelog category normalization, and rollback/error handling.
- dependencies_and_callers: Invoked by `commands/commit.ts` and CLI commit path; depends on git utils, pi-ai/pi-agent-core, pi-tui, settings/model registry.
- edge_cases_or_failure_modes: Huge diffs, binary/lock files, invalid split dependencies, changelog boundary ambiguity, model failure, and malformed tool proposals.
- validation_or_tests: Commit-related tests plus agentic validation utilities; no edits were made in this research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-283 `directory` `packages/coding-agent/src/task`
- cursor: `[_]`
- core_role: Subagent/task tool subsystem for spawning bundled or discovered agents, parallel batches, isolation, output capture, revive, rendering, and task schemas.
- algorithmic_behavior: Recursively inspected 15 files. `types.ts` defines schemas/statuses and role bounds; `index.ts` validates spawn shapes, recursion/read-only gates, and job scheduling; `executor.ts` runs subagents and bridges MCP/tool calls; `worktree.ts` captures baselines/delta patches and chooses isolation backend; `parallel.ts` provides concurrency pool/semaphore (`packages/coding-agent/src/task/types.ts:83`, `packages/coding-agent/src/task/index.ts:239`, `packages/coding-agent/src/task/worktree.ts:128`, `packages/coding-agent/src/task/parallel.ts:26`).
- inputs_outputs_state: Inputs are task tool params, agent definitions, settings, cwd/git state, session/tool registry, and abort signals. Outputs are `SingleResult`, progress events, async jobs, patches, nested repo commits, and rendered tool cards.
- gates_or_invariants: Recursion caps, batch enablement, isolation enablement, role length max, read-only agent detection, job manager availability, concurrency limits, and abort propagation.
- dependencies_and_callers: Called by `TaskTool`; coordinates with `AsyncJobManager`, `AgentRegistry`, `pi-natives` isolation, git utils, prompts, and TUI renderer.
- edge_cases_or_failure_modes: Dirty/nested repos, missing git root, failed isolation backend, aborted batches, missing yield warnings, double-encoded JSON args, and parked subagent revive errors.
- validation_or_tests: `role-specialization.test.ts`, task render tests, async/session tests, and SSH/IRC tests touch related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-313 `directory` `packages/coding-agent/test/ssh`
- cursor: `[_]`
- core_role: SSH subsystem regression tests for connection management and command execution.
- algorithmic_behavior: Recursively inspected 2 tests: `connection-manager.test.ts` and `ssh-executor.test.ts`, covering SSH connection lifecycle, executor behavior, error paths, and command result contracts.
- inputs_outputs_state: Inputs are mocked SSH configs/commands; outputs are connection state assertions and execution result assertions.
- gates_or_invariants: Ensures connection reuse/cleanup and executor failure mapping behave predictably.
- dependencies_and_callers: Tests coding-agent SSH modules used by SSH commands/tools.
- edge_cases_or_failure_modes: Connection failure, command failure, cleanup after errors, and invalid connection metadata.
- validation_or_tests: Directory itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-343 `file` `crates/pi-iso/src/lib.rs`
- cursor: `[_]`
- core_role: Rust isolation backend abstraction and resolver for task worktree isolation.
- algorithmic_behavior: Defines `BackendKind`, auto-order per OS, `ProbeResult`, `IsoError`, `IsolationBackend` trait, backend lookup, default kind, and `resolve(preferred)` fallback logic (`crates/pi-iso/src/lib.rs:47`, `crates/pi-iso/src/lib.rs:127`, `crates/pi-iso/src/lib.rs:225`, `crates/pi-iso/src/lib.rs:338`).
- inputs_outputs_state: Inputs are preferred backend and host platform/probe results. Outputs are selected backend, available candidates, and errors/reasons.
- gates_or_invariants: Preferred backend must probe available or resolver falls through; auto-order is platform-specific; fallback ultimately uses rcopy when native isolation unavailable.
- dependencies_and_callers: Used by pi-natives and coding-agent task isolation (`worktree.ts`).
- edge_cases_or_failure_modes: Unsupported platform, backend probe unavailable, no candidates, and snapshot/merge errors propagated as `IsoError`.
- validation_or_tests: Rust crate tests and coding-agent task isolation behavior indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-373 `file` `crates/pi-natives/src/task.rs`
- cursor: `[_]`
- core_role: N-API async task/cancellation bridge between Rust native operations and JS promises.
- algorithmic_behavior: Maps abort reasons, wraps `AbortSignal` into `CancelToken`, exposes `AbortToken`, and provides `blocking`/`future` helpers around `napi::Task`/`AsyncTask` (`crates/pi-natives/src/task.rs:43`, `crates/pi-natives/src/task.rs:77`, `crates/pi-natives/src/task.rs:153`, `crates/pi-natives/src/task.rs:209`).
- inputs_outputs_state: Inputs are optional JS abort signal and Rust closures/futures. Outputs are JS promises or native cancellation state.
- gates_or_invariants: Abort listener is wired when signal is supplied; cancellation reason conversions preserve user vs timeout distinctions.
- dependencies_and_callers: Used by pi-natives APIs for grep/text/PTY/isolation operations consumed by coding-agent.
- edge_cases_or_failure_modes: Aborted signal before run, JS signal conversion failure, blocking task panics/errors, and env lifetime constraints.
- validation_or_tests: Native integration tests and downstream task/PTY tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-403 `file` `packages/agent/test/compaction-thinking-level.test.ts`
- cursor: `[_]`
- core_role: Regression suite for compaction summarizer thinking-level propagation.
- algorithmic_behavior: Asserts Anthropic default reasoning stays high, `ThinkingLevel.Off` disables reasoning, low propagates, inherit folds to default, and xai/grok-build clamps high to undefined across all three summarizer calls (`compaction-thinking-level.test.ts:76`, `compaction-thinking-level.test.ts:191`).
- inputs_outputs_state: Inputs are test messages, model selection, and thinking level. Outputs are captured `complete` call options.
- gates_or_invariants: User explicit off must be honored; historical default preserved when undefined; unsupported model/provider clamps.
- dependencies_and_callers: Tests pi-agent-core compaction and pi-ai complete path.
- edge_cases_or_failure_modes: Fan-out summarizers diverging in reasoning config, provider-specific unsupported reasoning.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-433 `file` `packages/ai/test/anthropic-abandoned-tooluse-replay.test.ts`
- cursor: `[_]`
- core_role: Anthropic message conversion regression tests for abandoned/aborted tool-use replay.
- algorithmic_behavior: Builds synthetic Anthropic histories and asserts signed thinking is preserved for genuine/latest surviving tool-use turns, downgraded for historical invalid turns, and truncated final blocks are stripped while completed signed thinking remains (`anthropic-abandoned-tooluse-replay.test.ts:103`).
- inputs_outputs_state: Inputs are assistant/tool messages with thinking signatures/tool calls. Outputs are wire blocks for Anthropic.
- gates_or_invariants: Anthropic signed thinking must remain wire-valid; abandoned mid-stream blocks cannot corrupt replay.
- dependencies_and_callers: Tests `convertAnthropicMessages`.
- edge_cases_or_failure_modes: Gateway base URL, trailing truncated thinking, interleaved aborted turns, historical end_turn tool-use.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-463 `file` `packages/ai/test/auth-gateway-cache-key.test.ts`
- cursor: `[_]`
- core_role: Cache-key resolution tests for auth gateway prompt caching.
- algorithmic_behavior: Verifies precedence: body `prompt_cache_key`, metadata key/session/conversation IDs, headers, then undefined; ignores empty/non-string fields (`auth-gateway-cache-key.test.ts:4`).
- inputs_outputs_state: Inputs are request body and headers. Output is resolved string key or undefined.
- gates_or_invariants: Body fields outrank headers; invalid/empty values are ignored.
- dependencies_and_callers: Tests `resolvePromptCacheKey` in auth gateway HTTP layer.
- edge_cases_or_failure_modes: Null body, string body, empty strings, non-string fields, alternate header spellings.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-493 `file` `packages/ai/test/claude-usage-headers.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Claude OAuth usage request headers and usage parsing.
- algorithmic_behavior: Asserts usage endpoint receives bearer auth, Claude CLI user-agent, required anthropic-beta tokens, and does not fabricate reset timestamps when omitted (`claude-usage-headers.test.ts:31`).
- inputs_outputs_state: Inputs are mocked fetch response and OAuth token. Outputs are usage report and captured request headers.
- gates_or_invariants: Header fingerprint must align with Claude Code; missing reset times remain undefined.
- dependencies_and_callers: Tests `claudeUsageProvider` and `claudeCodeVersion`.
- edge_cases_or_failure_modes: Case-insensitive header lookup, omitted usage reset windows.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-523 `file` `packages/ai/test/google-tool-choice.test.ts`
- cursor: `[_]`
- core_role: Tests Google tool-choice mapping and GenerateContent serialization.
- algorithmic_behavior: Maps `required` to Google `any`, named tool/function choices to `ANY` allow-list, omits config for default auto, and emits functionCallingConfig for explicit choices (`google-tool-choice.test.ts:7`, `google-tool-choice.test.ts:38`).
- inputs_outputs_state: Inputs are generic `ToolChoice`, tools, context, and model. Outputs are Google request config.
- gates_or_invariants: Auto should rely on Google defaults; forced named tools must restrict allowed function names.
- dependencies_and_callers: Tests `mapGoogleToolChoice` and `buildGoogleGenerateContentParams`.
- edge_cases_or_failure_modes: OpenAI-shaped function choice, undefined choice, default auto config pollution.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-553 `file` `packages/ai/test/issue-959-repro.test.ts`
- cursor: `[_]`
- core_role: Reproduction test for DeepSeek chat-template token leakage.
- algorithmic_behavior: Streams mocked OpenAI-completions chunks and asserts visible text strips `<｜Assistant｜>` markers, including markers split across chunks (`issue-959-repro.test.ts:35`).
- inputs_outputs_state: Inputs are mocked streamed chunks and DeepSeek model. Output is sanitized assistant text.
- gates_or_invariants: Provider-specific leaked template markers must not reach user-visible content.
- dependencies_and_callers: Tests `streamOpenAICompletions`.
- edge_cases_or_failure_modes: Partial marker across chunks and multilingual text preservation.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-583 `file` `packages/ai/test/openai-completions-disable-reasoning.test.ts`
- cursor: `[_]`
- core_role: Tests reasoning disablement/dialect translation for OpenAI-compatible completions providers.
- algorithmic_behavior: Asserts lowest effort for generic models, Fireworks `none`, OpenRouter disabled object, Qwen `enable_thinking`, Qwen chat-template kwargs, and Z.AI thinking type toggles under forced tool choice (`openai-completions-disable-reasoning.test.ts:87`).
- inputs_outputs_state: Inputs are model specs, effort settings, and tool choices. Outputs are request payloads.
- gates_or_invariants: Forced tool choice can disable incompatible thinking paths; provider dialects must receive their expected fields.
- dependencies_and_callers: Tests `streamOpenAICompletions`.
- edge_cases_or_failure_modes: Provider-specific disable literals, chat-template args, forced tool-choice incompatibility.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-613 `file` `packages/ai/test/provider-fetch-override.test.ts`
- cursor: `[_]`
- core_role: Tests per-call fetch override routing.
- algorithmic_behavior: Verifies OpenAI completions calls hit `/chat/completions` and OpenAI responses calls hit `/responses` through the supplied `StreamOptions.fetch` override (`provider-fetch-override.test.ts:27`).
- inputs_outputs_state: Inputs are override fetch and model/context. Outputs are captured URL calls and stream result.
- gates_or_invariants: Provider code must not bypass injected fetch.
- dependencies_and_callers: Tests `streamOpenAICompletions` and `streamOpenAIResponses`.
- edge_cases_or_failure_modes: Wrong provider path or global fetch usage.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-643 `file` `packages/ai/test/transcript-render.test.ts`
- cursor: `[_]`
- core_role: Dialect transcript rendering tests.
- algorithmic_behavior: Asserts native transcript serialization for harmony, qwen3, GLM, Anthropic legacy, and literal thinking-envelope handling (`transcript-render.test.ts:52`).
- inputs_outputs_state: Inputs are generic messages/usage and dialect definitions. Outputs are rendered transcript strings.
- gates_or_invariants: Each dialect must produce distinct native syntax and avoid double-wrapping thinking blocks.
- dependencies_and_callers: Tests `getDialectDefinition().renderTranscript`.
- edge_cases_or_failure_modes: Sibling literal thinking envelopes, tool call/result channel formatting.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-673 `file` `packages/catalog/test/canonical-limit-fallback.test.ts`
- cursor: `[_]`
- core_role: Catalog generated-policy tests for context/max-token fallback from canonical models.
- algorithmic_behavior: Verifies proxy models with null limits inherit from canonical first-party references, skips zero-cost xai-oauth subscription entries, matches bare model segments across namespaces, and leaves holes null if no reference exists (`canonical-limit-fallback.test.ts:32`).
- inputs_outputs_state: Inputs are provider/model specs. Outputs are mutated/filled limits.
- gates_or_invariants: Never use subscription/zero-cost entries as canonical source; only fill null/unknown fields from valid family matches.
- dependencies_and_callers: Tests `applyCanonicalLimitFallback`.
- edge_cases_or_failure_modes: Namespace variance, both fields null, no canonical match.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-703 `file` `packages/catalog/test/ollama-cloud-provider.test.ts`
- cursor: `[_]`
- core_role: Integration-style provider tests for Ollama Cloud model discovery and chat streaming.
- algorithmic_behavior: Tests env API key resolution, `/api/tags` and `/api/show` discovery, metadata fallback, GLM reasoning mapping, chat streaming of thinking/text/tool calls/usage, tool-choice mapping, image/history payload conversion, and stripping thinking from replayed assistant messages (`ollama-cloud-provider.test.ts:60`, `ollama-cloud-provider.test.ts:212`, `ollama-cloud-provider.test.ts:407`).
- inputs_outputs_state: Inputs are mocked Ollama Cloud HTTP responses, tools, context, and models. Outputs are discovered models and streamed events/results.
- gates_or_invariants: Authorization header required; individual show failures tolerated; tool stop reason maps to `toolUse`; ordered system messages preserved.
- dependencies_and_callers: Tests catalog Ollama provider options plus pi-ai stream/simple APIs.
- edge_cases_or_failure_modes: Missing metadata, show failure, multimodal payloads, tool call streaming, reasoning max for GLM.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-733 `file` `packages/coding-agent/src/system-prompt.ts`
- cursor: `[_]`
- core_role: System prompt assembly pipeline for coding-agent sessions.
- algorithmic_behavior: Loads/dedupes context files and always-apply rules, resolves prompt input or file content, gathers system info/GPU/terminal, loads skills, renders tool inventory, applies personality/project prompt templates, and handles prep timeouts/fallbacks (`system-prompt.ts:41`, `system-prompt.ts:225`, `system-prompt.ts:277`, `system-prompt.ts:427`).
- inputs_outputs_state: Inputs are cwd/home, context files, skills settings, tool metadata, prompts, env, model info, workspace tree, and optional overrides. Output is `BuildSystemPromptResult` with message blocks and metadata.
- gates_or_invariants: `NULL_PROMPT` bypass, timeout for prep tasks, exact-content dedupe, project/user prompt precedence, prompt source dedupe against always-apply rules.
- dependencies_and_callers: Used by session/SDK startup; depends on discovery capabilities, workspace tree, pi-ai dialect inventory, pi-utils prompt renderer.
- edge_cases_or_failure_modes: Missing files, ENAMETOOLONG/ENOENT treating input as literal, GPU probes timing out/failing, duplicate rules, tool metadata absent.
- validation_or_tests: `system-prompt-math.test.ts`, prompt tests, and session prompt tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-763 `file` `packages/coding-agent/test/agent-session-eager-todo.test.ts`
- cursor: `[_]`
- core_role: Tests eager todo enforcement in agent sessions.
- algorithmic_behavior: Uses mocked agent/session setup to observe prompt injection and todo tool behavior around assistant output requiring todo creation (`agent-session-eager-todo.test.ts:86`).
- inputs_outputs_state: Inputs are assistant messages/tool calls and settings/session state. Outputs are observed prompt calls and todo-related session effects.
- gates_or_invariants: Eager todo guidance must be injected when conditions warrant and avoid duplicate/incorrect enforcement.
- dependencies_and_callers: Tests `AgentSession`, `TodoTool`, model registry/settings, and prompt `eager-todo.md`.
- edge_cases_or_failure_modes: Existing todo state, assistant tool-call timing, session conversion to LLM messages.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-793 `file` `packages/coding-agent/test/artifacts-sanitization.test.ts`
- cursor: `[_]`
- core_role: Tests artifact manager sanitization of tool type/path-ish identifiers.
- algorithmic_behavior: Creates temp artifact manager instances and asserts unsafe tool-type strings are sanitized before filesystem use (`artifacts-sanitization.test.ts:7`).
- inputs_outputs_state: Inputs are tool type names and temp directories. Outputs are artifact paths/files.
- gates_or_invariants: Tool identifiers must not enable path traversal or invalid filenames.
- dependencies_and_callers: Tests `ArtifactManager`.
- edge_cases_or_failure_modes: Slashes, special chars, platform path separators.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-823 `file` `packages/coding-agent/test/client-prompts.test.ts`
- cursor: `[_]`
- core_role: MCP client prompt API tests.
- algorithmic_behavior: Tests `listPrompts`, `getPrompt`, and server prompt capability detection using mock transport/connection (`client-prompts.test.ts:6`, `client-prompts.test.ts:64`, `client-prompts.test.ts:135`).
- inputs_outputs_state: Inputs are MCP prompt list/get mock responses. Outputs are prompt arrays/results or capability booleans.
- gates_or_invariants: Client must handle prompt APIs and unsupported servers correctly.
- dependencies_and_callers: Tests MCP client functions and MCP type shapes.
- edge_cases_or_failure_modes: Missing prompt capability, malformed server response, prompt argument/result mapping.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-853 `file` `packages/coding-agent/test/extension-dashboard-state.test.ts`
- cursor: `[_]`
- core_role: Tests extension dashboard disabled-state projection.
- algorithmic_behavior: Asserts `applyDisabledExtensionsToState` mutates/marks dashboard extension state according to disabled extension config (`extension-dashboard-state.test.ts:32`).
- inputs_outputs_state: Inputs are dashboard state and extension lists. Output is transformed state.
- gates_or_invariants: Disabled extensions must be reflected without losing unrelated dashboard metadata.
- dependencies_and_callers: Tests modes extension state manager.
- edge_cases_or_failure_modes: Missing extension entries, mixed enabled/disabled state.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-883 `file` `packages/coding-agent/test/image-webp-exclusion.test.ts`
- cursor: `[_]`
- core_role: Tests model-aware WebP image filtering.
- algorithmic_behavior: Uses a 1x1 PNG base fixture and bundled models to assert WebP-lacking models are detected and images are normalized/excluded appropriately (`image-webp-exclusion.test.ts:23`, `image-webp-exclusion.test.ts:49`).
- inputs_outputs_state: Inputs are image blocks and model metadata. Outputs are normalized context images.
- gates_or_invariants: Models without WebP support must not receive WebP payloads.
- dependencies_and_callers: Tests image loading/normalization utilities and catalog model metadata.
- edge_cases_or_failure_modes: Mixed image formats, model support flags missing/stale.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-913 `file` `packages/coding-agent/test/issue-1606-repro.test.ts`
- cursor: `[_]`
- core_role: Reproduction test ensuring tiny title model runs in isolated subprocess.
- algorithmic_behavior: Verifies `createTinyTitleSubprocess` and `TINY_WORKER_ARG` spawn path points at isolated subprocess machinery rather than loading the tiny model in-process (`issue-1606-repro.test.ts:21`).
- inputs_outputs_state: Inputs are subprocess creation params. Outputs are process/argv assertions.
- gates_or_invariants: Tiny model must not pollute main process module graph/resources.
- dependencies_and_callers: Tests tiny title client.
- edge_cases_or_failure_modes: Wrong entrypoint/argv causing in-process load or worker mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-943 `file` `packages/coding-agent/test/join-patch.test.ts`
- cursor: `[_]`
- core_role: Tests git patch joining/formatting utility.
- algorithmic_behavior: Asserts `patch` helper joins patch fragments into expected combined patch output (`join-patch.test.ts:4`).
- inputs_outputs_state: Inputs are patch fragments. Output is joined patch text.
- gates_or_invariants: Patch concatenation must preserve valid diff boundaries.
- dependencies_and_callers: Tests `utils/git`.
- edge_cases_or_failure_modes: Empty fragments, missing newlines, malformed joins.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-973 `file` `packages/coding-agent/test/mcp-timeout.test.ts`
- cursor: `[_]`
- core_role: Tests MCP timeout configuration resolution.
- algorithmic_behavior: Manipulates `OMP_MCP_TIMEOUT_MS`, spies logger, and asserts `isMCPTimeoutEnabled` and `resolveMCPTimeoutMs` handle defaults, invalid values, and disabled/positive timeouts (`mcp-timeout.test.ts:15`).
- inputs_outputs_state: Inputs are env var values. Outputs are booleans, timeout ms, and warnings.
- gates_or_invariants: Invalid env values should warn/fallback; timeout can be disabled according to config rules.
- dependencies_and_callers: Tests MCP timeout module and logger.
- edge_cases_or_failure_modes: Empty, nonnumeric, zero/negative values, env restoration.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1003 `file` `packages/coding-agent/test/plugin-manifest-paths.test.ts`
- cursor: `[_]`
- core_role: Tests plugin manifest path resolution.
- algorithmic_behavior: Creates temp plugin manifest fixtures and verifies manifest entries resolve relative paths correctly (`plugin-manifest-paths.test.ts:22`).
- inputs_outputs_state: Inputs are plugin package dirs/manifests. Outputs are resolved installed plugin/manifest paths.
- gates_or_invariants: Manifest paths must be canonicalized relative to plugin root, not cwd.
- dependencies_and_callers: Tests plugin manifest loader/manager types.
- edge_cases_or_failure_modes: Relative paths, temp package roots, missing files.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1033 `file` `packages/coding-agent/test/sdk-dialect.test.ts`
- cursor: `[_]`
- core_role: Tests SDK dialect resolution.
- algorithmic_behavior: Asserts `resolveDialect` maps SDK options/model defaults into the expected dialect result (`sdk-dialect.test.ts:4`).
- inputs_outputs_state: Inputs are dialect arguments. Output is dialect identifier/definition.
- gates_or_invariants: SDK callers must receive stable dialect resolution.
- dependencies_and_callers: Tests coding-agent SDK.
- edge_cases_or_failure_modes: Undefined or unsupported dialect options.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1063 `file` `packages/coding-agent/test/silent-abort-overlay-render.test.ts`
- cursor: `[_]`
- core_role: Regression test for agent hub overlay handling of silent abort marker.
- algorithmic_behavior: Builds fake observable session/registry state and asserts silent abort marker does not render as noisy user-visible content while overlay status remains coherent (`silent-abort-overlay-render.test.ts:61`).
- inputs_outputs_state: Inputs are session messages/events and registry state. Output is rendered overlay text.
- gates_or_invariants: Silent abort marker must be filtered from UI display.
- dependencies_and_callers: Tests `AgentHubOverlayComponent`, settings/theme, `SILENT_ABORT_MARKER`.
- edge_cases_or_failure_modes: Aborted sessions, overlay refresh, marker embedded in transcript.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1093 `file` `packages/coding-agent/test/system-prompt-math.test.ts`
- cursor: `[_]`
- core_role: Regression test for math formatting in generated system prompt.
- algorithmic_behavior: Builds system prompt in temp home/cwd and checks mathematical formatting is preserved in prompt content (`system-prompt-math.test.ts:16`).
- inputs_outputs_state: Inputs are temp config/context and empty workspace tree. Output is system prompt blocks.
- gates_or_invariants: Prompt renderer must not corrupt math syntax.
- dependencies_and_callers: Tests `buildSystemPrompt`.
- edge_cases_or_failure_modes: Markdown/prompt renderer escaping math delimiters.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1123 `file` `packages/coding-agent/test/workflow-command.test.ts`
- cursor: `[_]`
- core_role: Tests workflow CLI command registration and argument resolution.
- algorithmic_behavior: Verifies workflow is top-level subcommand and `resolveWorkflowCommandArgs`/`buildHeadlessAgentTaskArgs` map CLI args correctly (`workflow-command.test.ts:6`, `workflow-command.test.ts:29`).
- inputs_outputs_state: Inputs are argv arrays. Outputs are resolved command args/headless task args.
- gates_or_invariants: Workflow command must be registered and preserve intended arg forwarding.
- dependencies_and_callers: Tests `cli-commands`, `workflow-cli`, and command module.
- edge_cases_or_failure_modes: Subcommand misclassification, dropped flags, headless arg mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1153 `file` `packages/hashline/src/parser.ts`
- cursor: `[_]`
- core_role: Hashline patch parser/executor converting line-oriented edit syntax into structured edits.
- algorithmic_behavior: Tokenizes feed/end streams through `Executor`, validates ranges, expands delete/replace ranges, handles pending payloads/deferred blanks, detects apply_patch/diff contamination, strips hashline prefixes for bare payloads, and emits edits plus warnings (`parser.ts:19`, `parser.ts:44`, `parser.ts:108`, `parser.ts:398`).
- inputs_outputs_state: Input is hashline diff text. Output is `{ edits, warnings }`.
- gates_or_invariants: Delete targets take no body, blocks/inserts require payload, duplicate delete anchors are rejected, minus rows and apply-patch syntax are rejected with actionable errors.
- dependencies_and_callers: Depends on tokenizer/format/prefix helpers and is used by hashline edit execution.
- edge_cases_or_failure_modes: Bare literal body ambiguity, empty insert/block, overlapping deletes, streaming parse termination, apply-patch contamination.
- validation_or_tests: Hashline parser/edit tests elsewhere; this file enforces core parser semantics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1183 `file` `packages/mnemopi/test/beam-helpers.test.ts`
- cursor: `[_]`
- core_role: Tests memory/beam helper queries, weights, lexical/FTS/temporal/language/vector fallback behavior.
- algorithmic_behavior: Uses in-memory SQLite to assert helper IDs, metadata, lexical and FTS ranking, temporal/language helpers, and vector fallback contracts (`beam-helpers.test.ts:26`, `beam-helpers.test.ts:51`, `beam-helpers.test.ts:98`, `beam-helpers.test.ts:116`).
- inputs_outputs_state: Inputs are test DB rows/query params. Outputs are beam result rows/scores/metadata.
- gates_or_invariants: Helper results must carry correct IDs/weights and degrade sensibly without vector support.
- dependencies_and_callers: Tests mnemopi beam helper modules.
- edge_cases_or_failure_modes: Empty FTS, language filters, temporal cutoffs, vector fallback absence.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1213 `file` `packages/mnemopi/test/llm-backends.test.ts`
- cursor: `[_]`
- core_role: Tests host LLM backend registry.
- algorithmic_behavior: Asserts backend registration/resolution and environment cleanup via `afterEach` (`llm-backends.test.ts:12`).
- inputs_outputs_state: Inputs are backend config/env. Outputs are resolved backend behavior.
- gates_or_invariants: Registry must resolve only supported backends and restore global state after tests.
- dependencies_and_callers: Tests mnemopi LLM backend code.
- edge_cases_or_failure_modes: Unsupported backend, env leakage.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1243 `file` `packages/mnemopi/test/vector-index.test.ts`
- cursor: `[_]`
- core_role: Tests exact vector index search.
- algorithmic_behavior: Builds an exact vector index and asserts search returns expected nearest vectors/order (`vector-index.test.ts:4`).
- inputs_outputs_state: Inputs are embedding vectors/query. Outputs are ranked search results.
- gates_or_invariants: Exact index must preserve deterministic similarity ordering.
- dependencies_and_callers: Tests `buildExactVectorIndex` and `searchExactVectorIndex`.
- edge_cases_or_failure_modes: Empty or dimensional mismatch cases likely covered in implementation, not extensive here.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1273 `file` `packages/snapcompact/research/exp01_patchalign.py`
- cursor: `[_]`
- core_role: Research experiment driver for patch-alignment prompt/image conditions.
- algorithmic_behavior: Caches model calls, parses image condition names, ensures SQuAD data, runs cell chunks through LLM providers, aggregates records and pricing, and writes CSV/JSON results (`exp01_patchalign.py:71`, `exp01_patchalign.py:87`, `exp01_patchalign.py:102`, `exp01_patchalign.py:161`).
- inputs_outputs_state: Inputs are SQuAD samples, rendered font/image contexts, model/provider keys, cache, and CLI args. Outputs are experiment records/results.
- gates_or_invariants: Cache key includes model/tag/payload; condition parser expects structured names; chunking bounds dataset ranges.
- dependencies_and_callers: Depends on local research modules `squad`, `bdf`, `providers`, `run`.
- edge_cases_or_failure_modes: Missing API key/data, stale cache, malformed condition, provider failure.
- validation_or_tests: Research script; no formal tests found.
- skip_candidate: `yes: research experiment code, algorithmic but not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1303 `file` `packages/snapcompact/research/snapcompact_3d_activation_html.py`
- cursor: `[_]`
- core_role: Research visualization generator for 3D activation surfaces.
- algorithmic_behavior: Downsamples arrays, normalizes quantiles, embeds images as data URIs, adds Plotly surfaces, and writes an HTML explainer (`snapcompact_3d_activation_html.py:21`, `snapcompact_3d_activation_html.py:33`, `snapcompact_3d_activation_html.py:44`, `snapcompact_3d_activation_html.py:68`).
- inputs_outputs_state: Inputs are numpy activation arrays/images/data dir. Output is Plotly HTML.
- gates_or_invariants: Quantile normalization bounds values; downsample preserves column target.
- dependencies_and_callers: Depends on `numpy`, `plotly`, local research outputs.
- edge_cases_or_failure_modes: Missing arrays/images, degenerate quantiles, large HTML output.
- validation_or_tests: Research script; no formal tests found.
- skip_candidate: `yes: visualization research artifact, not core product runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1333 `file` `packages/snapcompact/research/snapcompact_viz_explainer.py`
- cursor: `[_]`
- core_role: Research image renderer explaining snapcompact data/activation behavior.
- algorithmic_behavior: Loads fonts, computes colors, crops answer regions, draws cards/arrows/heatmaps/tensor ribbons/token grids/metrics, wraps text, saves source metrics, and renders a final image (`snapcompact_viz_explainer.py:41`, `snapcompact_viz_explainer.py:143`, `snapcompact_viz_explainer.py:179`, `snapcompact_viz_explainer.py:306`).
- inputs_outputs_state: Inputs are image/summary/array files. Outputs are PNG/explainer assets and metrics.
- gates_or_invariants: Crops clamp around answer cell box; color ramps normalize; fallback fonts supported.
- dependencies_and_callers: Depends on PIL and numpy.
- edge_cases_or_failure_modes: Missing fonts/assets, invalid summary coordinates, array shape mismatch.
- validation_or_tests: Research script; no formal tests found.
- skip_candidate: `yes: research visualization, not production core runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1363 `file` `packages/tui/bench/_jskey.ts`
- cursor: `[_]`
- core_role: Keyboard parsing benchmark/reference implementation for TUI key IDs and Kitty protocol sequences.
- algorithmic_behavior: Defines key ID unions/maps, legacy escape sequences, modifier masks, Kitty parsed sequence handling, cached key parsing, and event type tracking (`_jskey.ts:25`, `_jskey.ts:145`, `_jskey.ts:293`, `_jskey.ts:480`).
- inputs_outputs_state: Inputs are terminal escape bytes/Kitty protocol data. Outputs are normalized key event identities.
- gates_or_invariants: Legacy modifier sequences and Kitty event types must map consistently; cache avoids repeated parse cost.
- dependencies_and_callers: Bench file for pi-tui key handling.
- edge_cases_or_failure_modes: Ctrl-symbol sequences, app cursor mode, release/repeat events, unknown sequences.
- validation_or_tests: Related `stdin-buffer.test.ts` covers parsing behavior.
- skip_candidate: `yes: benchmark/reference copy rather than package runtime entrypoint`

### OH_MY_HUMANIZE_MAIN-HZ-1393 `file` `packages/tui/test/container-dispose.test.ts`
- cursor: `[_]`
- core_role: Tests TUI `Container.dispose` child cleanup contract.
- algorithmic_behavior: Creates container/component fixtures and asserts dispose cascades as expected (`container-dispose.test.ts:8`).
- inputs_outputs_state: Inputs are component tree instances. Output is disposal state.
- gates_or_invariants: Containers must release child resources once and not leak.
- dependencies_and_callers: Tests `Container` from pi-tui.
- edge_cases_or_failure_modes: Nested disposal and idempotence.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1423 `file` `packages/tui/test/loop-watchdog-wiring.test.ts`
- cursor: `[_]`
- core_role: Tests TUI loop watchdog wiring.
- algorithmic_behavior: Spies `LoopWatchdog`, creates TUI with virtual terminal, and verifies watchdog integration (`loop-watchdog-wiring.test.ts:16`).
- inputs_outputs_state: Inputs are TUI init options. Output is watchdog invocation/cleanup assertions.
- gates_or_invariants: TUI loop should wire watchdog without leaking after each test.
- dependencies_and_callers: Tests `TUI`, `LoopWatchdog`, `VirtualTerminal`.
- edge_cases_or_failure_modes: Missing watchdog start/stop and test spy leakage.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1453 `file` `packages/tui/test/stdin-buffer.test.ts`
- cursor: `[_]`
- core_role: Tests terminal stdin buffering/key decoding behavior.
- algorithmic_behavior: Exercises `StdinBuffer` under normal, escape, bracketed/Kitty, paste, and buffering conditions; toggles Kitty protocol active state (`stdin-buffer.test.ts:12`).
- inputs_outputs_state: Inputs are byte chunks/escape sequences. Outputs are parsed key/input events.
- gates_or_invariants: Partial sequences must buffer until complete; Kitty protocol state affects parsing; afterEach restores global state.
- dependencies_and_callers: Tests pi-tui stdin buffer/key modules.
- edge_cases_or_failure_modes: Split escape sequences, ambiguous ESC timing, Kitty protocol release events, paste boundaries.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1483 `file` `packages/utils/src/cli.ts`
- cursor: `[_]`
- core_role: Shared CLI command/flag parser and help renderer.
- algorithmic_behavior: Defines `Flags`, `Args`, typed command metadata, abstract `Command`, `renderRootHelp`, `renderCommandHelp`, and `run` dispatch over command entries (`packages/utils/src/cli.ts:35`, `packages/utils/src/cli.ts:70`, `packages/utils/src/cli.ts:142`, `packages/utils/src/cli.ts:389`).
- inputs_outputs_state: Inputs are argv, command constructors, and CLI config. Outputs are parsed flag/arg values, help text, or command execution.
- gates_or_invariants: Flag descriptors constrain boolean/string/integer parsing; command lookup and help paths avoid running command code.
- dependencies_and_callers: Used by coding-agent command classes such as `commands/say.ts`.
- edge_cases_or_failure_modes: Unknown commands/flags, integer parsing, help invocation, missing required args.
- validation_or_tests: Indirect via command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1513 `file` `packages/utils/src/type-guards.ts`
- cursor: `[_]`
- core_role: Tiny shared unknown-value guard helpers.
- algorithmic_behavior: Provides `isRecord`, `asRecord`, and `toError` (`type-guards.ts:1`).
- inputs_outputs_state: Inputs are unknown values. Outputs are narrowed record, nullable record, or Error.
- gates_or_invariants: Arrays/null are not records; non-Error thrown values become `Error(String(value))`.
- dependencies_and_callers: Shared utilities across packages.
- edge_cases_or_failure_modes: Null, arrays, primitive thrown values.
- validation_or_tests: Indirect only.
- skip_candidate: `yes: utility leaf, not a core algorithm by itself`

### OH_MY_HUMANIZE_MAIN-HZ-1543 `file` `python/omp-rpc/tests/test_host_uris.py`
- cursor: `[_]`
- core_role: Tests Python host URI decorator/normalization and RPC bridge.
- algorithmic_behavior: Defines helper and bridge test classes validating `normalize_read_result`, `host_uri` registration, and client/server host URI requests (`test_host_uris.py:92`, `test_host_uris.py:135`).
- inputs_outputs_state: Inputs are host URI read return values and RPC requests. Outputs are normalized payloads or bridge responses.
- gates_or_invariants: Host URI results must normalize to JSON object with content/details/error shape.
- dependencies_and_callers: Tests `omp_rpc.RpcClient`, `host_uri`, and `host_uris.normalize_read_result`.
- edge_cases_or_failure_modes: Plain strings, dict payloads, error values, bridge timeouts/process lifecycle.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1573 `file` `python/robomp/tests/__init__.py`
- cursor: `[_]`
- core_role: Empty Python package marker for robomp tests.
- algorithmic_behavior: No executable behavior; zero-byte file.
- inputs_outputs_state: No inputs/outputs/state.
- gates_or_invariants: Only affects Python package discovery.
- dependencies_and_callers: Python test discovery/import machinery.
- edge_cases_or_failure_modes: None beyond package import semantics.
- validation_or_tests: Not a test body.
- skip_candidate: `yes: empty package marker misclassified as core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1603 `directory` `packages/coding-agent/src/advisor/__tests__`
- cursor: `[_]`
- core_role: Advisor subsystem tests.
- algorithmic_behavior: Recursively inspected 1 file, `advisor.test.ts`, which validates advisory runtime/tool/watchdog behavior for coding-agent’s advisor feature.
- inputs_outputs_state: Inputs are advisor test fixtures and mocked runtime state. Outputs are assertions on advice/tool behavior.
- gates_or_invariants: Advisor should trigger/report only under expected conditions and handle runtime failures.
- dependencies_and_callers: Tests `advisor/advise-tool.ts`, `advisor/runtime.ts`, `advisor/watchdog.ts`.
- edge_cases_or_failure_modes: Watchdog timeout, advisor runtime errors, duplicate advice.
- validation_or_tests: Directory itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1633 `directory` `packages/coding-agent/src/modes/controllers`
- cursor: `[_]`
- core_role: TUI controller layer coordinating user input, commands, events, selectors, MCP auth, SSH, todo, streaming reveal, and tool-argument reveal.
- algorithmic_behavior: Recursively inspected 16 files. Controllers include `command-controller.ts` for slash commands/usage rendering, `event-controller.ts` for session event handling and IRC visibility TTL, `input-controller.ts` for keystroke/input state, `mcp-command-controller.ts` for OAuth/manual MCP flows, `selector-controller.ts`, `session-focus-controller.ts`, and specialized command controllers (`packages/coding-agent/src/modes/controllers/event-controller.ts:47`, `mcp-command-controller.ts:158`, `selector-controller.ts:74`).
- inputs_outputs_state: Inputs are key events, session events, command text, settings, auth callbacks, and UI state. Outputs are TUI mutations, chat blocks, command effects, auth prompts, and session focus changes.
- gates_or_invariants: Command parsing must avoid invalid state transitions; MCP OAuth uses timeouts/manual tips; live IRC card count/TTL bounded.
- dependencies_and_callers: Used by interactive modes/components and session runtime.
- edge_cases_or_failure_modes: Concurrent auth flows, stale event cards, narrow terminal rendering, invalid slash command args, selector cancellation.
- validation_or_tests: Component/controller tests cover workflow graph, welcome, streaming fast-path, and related UI behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1663 `directory` `packages/utils/src/vendor/mermaid-ascii`
- cursor: `[_]`
- core_role: Vendored Mermaid-to-ASCII parser/rendering engine.
- algorithmic_behavior: Recursively inspected 42 files: parsers for flow/class/ER/sequence/xychart, ASCII canvas/grid/pathfinder/edge routing, shape renderers, ANSI colorization, text metrics, and validation. Entry renders Mermaid text into ASCII diagrams through parser and renderer modules (`packages/utils/src/vendor/mermaid-ascii/ascii/canvas.ts:17`, `ascii/shapes/index.ts:32`, `xychart/parser.ts`, `ascii/index.ts`).
- inputs_outputs_state: Inputs are Mermaid diagram strings and render options. Outputs are ASCII/ANSI diagram strings and intermediate canvases.
- gates_or_invariants: Canvas bounds, wide-char cell accounting, shape registry defaults, diagram-specific parser validation, and ASCII/unicode mode selection.
- dependencies_and_callers: Used by theme/markdown rendering utilities and tests under `packages/utils/test/mermaid`.
- edge_cases_or_failure_modes: Unsupported Mermaid syntax, wide characters, edge routing collisions, xychart zero/single data points.
- validation_or_tests: `packages/utils/test/mermaid/xychart.test.ts` covers xychart rendering.
- skip_candidate: `yes: vendored third-party subsystem, algorithmic but not authored core logic`

### OH_MY_HUMANIZE_MAIN-HZ-1693 `file` `packages/ai/src/auth-broker/types.ts`
- cursor: `[_]`
- core_role: Auth broker API type and constant contract.
- algorithmic_behavior: Defines health, refresher schedule, snapshot/usage/refresh/disable/upload request-response shapes, snapshot stream event union, API prefix, bind address, refresh intervals, cache TTL, keepalive, and idle timeout (`auth-broker/types.ts:13`, `auth-broker/types.ts:77`, `auth-broker/types.ts:109`).
- inputs_outputs_state: Inputs/outputs are HTTP/SSE JSON payloads shared by broker client/server.
- gates_or_invariants: Event kinds constrained to `snapshot`, `entry`, `removed`; defaults centralize timing.
- dependencies_and_callers: Auth broker server/client and CLI use these shapes.
- edge_cases_or_failure_modes: Type drift between server and client, TTL/keepalive mismatch.
- validation_or_tests: Auth broker tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1723 `file` `packages/ai/src/providers/anthropic-client.ts`
- cursor: `[_]`
- core_role: Lightweight Anthropic Messages HTTP client with retries, timeout, and error mapping.
- algorithmic_behavior: Builds auth/default headers, supports streaming request creation, retries retryable status/network failures, parses retry-after headers, applies exponential jitter backoff, aborts on caller signal/timeout, and maps non-ok responses to `AnthropicApiError` (`anthropic-client.ts:128`, `anthropic-client.ts:145`, `anthropic-client.ts:207`, `anthropic-client.ts:251`).
- inputs_outputs_state: Inputs are API key/token/base URL, message params, fetch options, and abort signal. Output is `Response` wrapped by `AnthropicApiRequest`.
- gates_or_invariants: Does not overwrite caller-provided auth headers; max retries/timeouts bounded; 408/409/429/5xx retry unless header overrides.
- dependencies_and_callers: Used by Anthropic provider implementation; depends on `ProviderHttpError`, `FetchImpl`, `scheduler.wait`.
- edge_cases_or_failure_modes: Retry-after date/seconds parsing, abort during sleep/fetch, timeout vs caller abort distinction, non-JSON error response.
- validation_or_tests: Anthropic provider tests and usage header tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1753 `file` `packages/ai/src/providers/openai-responses-server-schema.ts`
- cursor: `[_]`
- core_role: ArkType schema mirror for OpenAI Responses request/server item shapes.
- algorithmic_behavior: Defines input/output content block schemas, message/reasoning/function/custom tool items, tool schemas, hosted tool/tool choice schemas, reasoning/stop schema, and overall `openaiResponsesRequestSchema` (`openai-responses-server-schema.ts:25`, `openai-responses-server-schema.ts:140`, `openai-responses-server-schema.ts:170`, `openai-responses-server-schema.ts:237`).
- inputs_outputs_state: Input is unknown request-like data. Output is typed inference or schema errors.
- gates_or_invariants: Restricts role/type unions, tool choice literals/objects, allowed hosted tool entries, reasoning config, and stop values.
- dependencies_and_callers: Used by OpenAI Responses provider/gateway validation; depends on `arktype` and OpenAI SDK types.
- edge_cases_or_failure_modes: Custom tool call item shape, file/image blocks, hosted tool type expansion, SDK/server schema drift.
- validation_or_tests: OpenAI responses tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1783 `file` `packages/ai/src/registry/google.ts`
- cursor: `[_]`
- core_role: Provider registry descriptor for Google.
- algorithmic_behavior: Exports `googleProvider` with provider metadata (`registry/google.ts:3`).
- inputs_outputs_state: Static descriptor input to provider registry. Output is available provider definition.
- gates_or_invariants: Provider ID/name must match registry expectations.
- dependencies_and_callers: Imported by provider registry.
- edge_cases_or_failure_modes: Descriptor drift from actual Google provider implementation.
- validation_or_tests: Provider registry tests indirectly.
- skip_candidate: `yes: tiny static descriptor, not an algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1813 `file` `packages/ai/src/registry/tavily.ts`
- cursor: `[_]`
- core_role: Tavily provider registry descriptor and login helper.
- algorithmic_behavior: Opens Tavily auth URL via OAuth callbacks, waits for API key entry, and exports provider definition (`registry/tavily.ts:4`, `registry/tavily.ts:12`, `registry/tavily.ts:39`).
- inputs_outputs_state: Inputs are OAuth login callbacks. Output is API key string and provider metadata.
- gates_or_invariants: Login flow depends on callback-provided user/API key; provider auth mode must align with registry.
- dependencies_and_callers: Used by provider registry/OAuth setup.
- edge_cases_or_failure_modes: User cancels/does not provide key, browser open failure.
- validation_or_tests: Indirect provider setup tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1843 `file` `packages/ai/src/utils/anthropic-auth.ts`
- cursor: `[_]`
- core_role: Anthropic auth/base URL/header resolution helper.
- algorithmic_behavior: Resolves base URL from env, detects OAuth tokens, builds auth config for API key vs OAuth/foundry, constructs search headers and request URL (`anthropic-auth.ts:33`, `anthropic-auth.ts:45`, `anthropic-auth.ts:60`, `anthropic-auth.ts:75`).
- inputs_outputs_state: Inputs are API key/token, base URL, env/foundry state. Outputs are header map and URL.
- gates_or_invariants: OAuth tokens use bearer auth; standard API keys use `x-api-key`; base URL defaults to Anthropic API.
- dependencies_and_callers: Used by Anthropic provider/search/usage paths.
- edge_cases_or_failure_modes: Token prefix ambiguity, foundry env behavior, trailing slash URL normalization.
- validation_or_tests: Anthropic and Claude usage tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1873 `file` `packages/catalog/src/discovery/gemini.ts`
- cursor: `[_]`
- core_role: Gemini model discovery client/normalizer.
- algorithmic_behavior: Fetches paginated Google Generative Language models, validates resilient schema, filters to `generateContent`, normalizes IDs/names/limits/input/reasoning, uses bundled model references when present, detects token cycles, and sorts models (`gemini.ts:73`, `gemini.ts:141`, `gemini.ts:177`, `gemini.ts:235`).
- inputs_outputs_state: Inputs are API key, fetch impl, base URL/page size/max pages. Output is `ModelSpec[]` or null on failure.
- gates_or_invariants: Empty API key returns null; non-ok/malformed responses return null; repeated page token breaks loop.
- dependencies_and_callers: Catalog discovery/generation for Gemini provider.
- edge_cases_or_failure_modes: Bad schema rows, unsupported methods, duplicate model IDs, page token loop, missing limits.
- validation_or_tests: Catalog discovery tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1903 `file` `packages/coding-agent/src/async/job-manager.ts`
- cursor: `[_]`
- core_role: Process-global async background job registry, cancellation, polling, delivery, and retention manager.
- algorithmic_behavior: Registers bash/task jobs, enforces active cap excluding queued jobs, tracks owner IDs, aborts cancellation, enqueues completion delivery, suppresses watched/acknowledged deliveries, evicts retained jobs, and manages smart poll wait escalation (`job-manager.ts:96`, `job-manager.ts:154`, `job-manager.ts:251`, `job-manager.ts:16`).
- inputs_outputs_state: Inputs are job runner callbacks, owner filters, cancel/list/poll calls, and completion callbacks. State is maps/sets for jobs, deliveries, watched IDs, eviction timers, poll escalation. Outputs are job IDs, snapshots, delivery callbacks, and errors.
- gates_or_invariants: Disposed manager rejects registration; max running jobs clamped >=1; queued jobs do not consume active slots; owner filters block cross-agent cancellation/listing.
- dependencies_and_callers: Used by `tools/job.ts`, async bash, task scheduling, SDK follow-up delivery.
- edge_cases_or_failure_modes: Progress callback failure logged, cancelled job resolves/rejects after abort, delivery retry loop, stale retained jobs, repeated poll escalation reset.
- validation_or_tests: Job tool docs/tests and async task behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1933 `file` `packages/coding-agent/src/cli/args.ts`
- cursor: `[_]`
- core_role: Coding-agent CLI argv parser and help text builder.
- algorithmic_behavior: Parses modes, prompts, model/thinking/tool flags, extension flags, profile bootstrap boundaries, `--flag=value`, boolean/string extension flag semantics, and unrecognized flag reporting (`args.ts:97`, `args.ts:113`, `args.ts:252`, `args.ts:264`).
- inputs_outputs_state: Inputs are argv and extension flag descriptors. Output is `Args` object plus unrecognized flags/help text.
- gates_or_invariants: Separator/profile boundary handling; extension flags consume values according to descriptor; thinking effort parsed via shared parser.
- dependencies_and_callers: Used by `cli.ts` startup and command registry.
- edge_cases_or_failure_modes: `--flag=value` for extension flags, missing string values, command args after separator, unknown flags.
- validation_or_tests: CLI/workflow command tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1963 `file` `packages/coding-agent/src/cli/ttsr-cli.ts`
- cursor: `[_]`
- core_role: CLI for testing/listing/scanning TTSR rules.
- algorithmic_behavior: Reads snippets from file/stdin/arg, loads TTSR rules/settings or isolated rule file, evaluates regex and AST conditions, lists rule metadata, scans files with glob/path/tool scopes, binary/large/unreadable skips, AST prefilters, JSON/text reporting, and summary stats (`ttsr-cli.ts:143`, `ttsr-cli.ts:545`, `ttsr-cli.ts:753`, `ttsr-cli.ts:971`).
- inputs_outputs_state: Inputs are CLI args, snippets, rule markdown/settings, scan directories, file contents. Outputs are console/JSON reports and skip/match summaries.
- gates_or_invariants: Disabled/builtin filtering, source validation, max scan bytes, binary probe, AST eligibility by language.
- dependencies_and_callers: Used by `commands/ttsr.ts`; depends on native `astMatch`/`glob`, discovery/settings, `TtsrManager`.
- edge_cases_or_failure_modes: Invalid regex/AST patterns, unreadable files, no relevant rules, large files, stdin absence.
- validation_or_tests: TTSR/rule-bucket tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1993 `file` `packages/coding-agent/src/commands/say.ts`
- cursor: `[_]`
- core_role: CLI command for text-to-speech synthesis/playback/output.
- algorithmic_behavior: Defines `Say` command class using shared CLI flags/args, settings, TTS client, WAV encoding, temp paths, audio playback, and cleanup (`commands/say.ts:18`).
- inputs_outputs_state: Inputs are text/model/audio options. Outputs are audio playback or file/encoded WAV behavior.
- gates_or_invariants: Temp files must be removed; TTS client shutdown handled.
- dependencies_and_callers: Registered CLI command; depends on `tts-client`, `tts/player`, `tts/wav`, settings.
- edge_cases_or_failure_modes: TTS failure, playback failure, temp cleanup, unsupported audio output.
- validation_or_tests: TTS command tests not directly assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2023 `file` `packages/coding-agent/src/config/models-config-schema.ts`
- cursor: `[_]`
- core_role: ArkType schema for user/provider/model configuration.
- algorithmic_behavior: Defines routing schemas, OpenAI-compatible fields, effort/thinking controls, model definition/override schemas, provider discovery/auth/config, equivalence config, and root `ModelsConfigSchema` (`models-config-schema.ts:10`, `models-config-schema.ts:67`, `models-config-schema.ts:120`, `models-config-schema.ts:260`).
- inputs_outputs_state: Input is unknown parsed config. Output is typed `ModelsConfig` or validation errors.
- gates_or_invariants: Effort literals ordered, auth limited to apiKey/none/oauth, provider config fields constrained.
- dependencies_and_callers: Used by model config loader/resolver.
- edge_cases_or_failure_modes: Invalid routing config, unsupported thinking mode, malformed provider discovery.
- validation_or_tests: Config/model tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2053 `file` `packages/coding-agent/src/discovery/codex.ts`
- cursor: `[_]`
- core_role: Discovery provider for OpenAI Codex-compatible config surfaces.
- algorithmic_behavior: Reads project/user Codex dirs and TOML, extracts MCP server definitions with env/header/bearer token env resolution, context files, prompts, rules, tools, hooks, settings, skills, slash commands, and extension modules into capability items with warnings (`discovery/codex.ts:41`, `discovery/codex.ts:115`, `discovery/codex.ts:142`, `discovery/codex.ts:432`).
- inputs_outputs_state: Inputs are load context, `.codex` files/config, env vars. Outputs are capability load results and warnings.
- gates_or_invariants: Invalid TOML returns null; missing content skipped; env variables only included if present; tool timeout only if positive.
- dependencies_and_callers: Registered with capability discovery; consumed by system prompt/tool setup.
- edge_cases_or_failure_modes: Malformed TOML, missing env vars, project/user precedence, invalid MCP shape.
- validation_or_tests: Discovery tests including plugin/capability surfaces.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2083 `file` `packages/coding-agent/src/eval/index.ts`
- cursor: `[_]`
- core_role: Barrel for eval backends.
- algorithmic_behavior: Star-exports backend/types and default exports JS/Python backends (`eval/index.ts:1`).
- inputs_outputs_state: Static module exports only.
- gates_or_invariants: Barrel paths must stay aligned with backend modules.
- dependencies_and_callers: Imported by eval tools and external consumers.
- edge_cases_or_failure_modes: Broken export path after refactor.
- validation_or_tests: Eval backend tests indirectly.
- skip_candidate: `yes: barrel module, not algorithmic itself`

### OH_MY_HUMANIZE_MAIN-HZ-2113 `file` `packages/coding-agent/src/hindsight/mental-models.ts`
- cursor: `[_]`
- core_role: Hindsight memory mental-model seeding/rendering/diff subsystem.
- algorithmic_behavior: Resolves built-in seeds by scope, ensures seeds exist, loads/render mental model snapshots under character budget, summarizes models, and computes bounded line LCS-style diffs (`mental-models.ts:89`, `mental-models.ts:142`, `mental-models.ts:215`, `mental-models.ts:353`).
- inputs_outputs_state: Inputs are bank scope/config, model summaries/content, render budget. Outputs are seeded models, prompt blocks, summaries, and diffs.
- gates_or_invariants: Render budget has minimum content room; first-turn deadline/refresh interval constants; duplicate seeds detected by `seedAlreadyExists`.
- dependencies_and_callers: Hindsight bank/config and prompts.
- edge_cases_or_failure_modes: Too many models causing truncation, duplicate seed matching, very large content diff capped.
- validation_or_tests: Hindsight tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2143 `file` `packages/coding-agent/src/lsp/render.ts`
- cursor: `[_]`
- core_role: Renderer for LSP tool calls/results in TUI.
- algorithmic_behavior: Sanitizes call/result text, renders headers/request metadata, parses code blocks/hover/diagnostics/references/symbols/generic output, truncates collapsed previews, and exports `lspToolRenderer` (`lsp/render.ts:34`, `lsp/render.ts:98`, `lsp/render.ts:289`, `lsp/render.ts:663`).
- inputs_outputs_state: Inputs are LSP params/result text/render options/theme. Outputs are `Text` or framed block components.
- gates_or_invariants: Tabs/newlines sanitized, expanded/collapsed display limits, diagnostic severity maps to colors.
- dependencies_and_callers: Used by LSP tools/render registry; depends on TUI/theme/render-utils.
- edge_cases_or_failure_modes: Empty content, malformed diagnostic lines, huge reference/symbol lists, markdown code block parsing.
- validation_or_tests: TUI renderer tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2173 `file` `packages/coding-agent/src/memory-backend/off-backend.ts`
- cursor: `[_]`
- core_role: No-op memory backend implementation.
- algorithmic_behavior: Exports `offBackend` satisfying `MemoryBackend` with disabled/no-op behavior (`off-backend.ts:8`).
- inputs_outputs_state: Inputs are memory API calls; outputs are empty/no-op results.
- gates_or_invariants: Memory-off mode must not persist or recall data.
- dependencies_and_callers: Used when memory backend disabled.
- edge_cases_or_failure_modes: Callers expecting non-null memory data.
- validation_or_tests: Memory backend tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2203 `file` `packages/coding-agent/src/plan-mode/plan-handoff.ts`
- cursor: `[_]`
- core_role: Loader for overall plan references in plan mode.
- algorithmic_behavior: Resolves local protocol URLs to paths, reads referenced plan files, and returns title/path/content or null on ENOENT (`plan-handoff.ts:5`, `plan-handoff.ts:23`).
- inputs_outputs_state: Inputs are `OverallPlanReference` and local protocol options. Output is loaded plan reference data.
- gates_or_invariants: Missing file is tolerated as null; non-ENOENT errors propagate.
- dependencies_and_callers: Plan mode handoff/protection flow and internal URL resolver.
- edge_cases_or_failure_modes: Invalid local URL, deleted plan file, permission/read error.
- validation_or_tests: Plan-mode protection tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2233 `file` `packages/coding-agent/src/session/session-storage.ts`
- cursor: `[_]`
- core_role: File and memory storage abstraction for session JSONL and related session files.
- algorithmic_behavior: Provides `FileSessionStorageWriter` with append/write/flush/close/error tracking, `FileSessionStorage` with exists/stat/glob/read/peek/atomic replace/delete/writer, and `MemorySessionStorage` with chunked byte accounting/head-tail slicing (`session-storage.ts:58`, `session-storage.ts:128`, `session-storage.ts:304`, `session-storage.ts:481`).
- inputs_outputs_state: Inputs are paths, byte chunks, write flags, glob patterns. State is file descriptors or memory file map/chunks. Outputs are reads, stats, writers, and file mutations.
- gates_or_invariants: Writer rejects after close/error; atomic replace has move-aside/cleanup path; memory slicing uses UTF-8 decoder for byte ranges.
- dependencies_and_callers: Used by session manager/loader/listing/history and tests.
- edge_cases_or_failure_modes: Short writes, EPERM rename fallback, ENOENT cleanup, multi-byte UTF-8 slice boundaries, finalizer cleanup.
- validation_or_tests: Session/history/internal URL tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2263 `file` `packages/coding-agent/src/task/agents.ts`
- cursor: `[_]`
- core_role: Bundled/custom subagent definition parser and registry cache.
- algorithmic_behavior: Builds embedded agent content from markdown/frontmatter, parses agent fields, validates required frontmatter, caches bundled agents, and exposes lookup/map helpers (`task/agents.ts:44`, `task/agents.ts:75`, `task/agents.ts:101`, `task/agents.ts:130`).
- inputs_outputs_state: Inputs are agent markdown/frontmatter/source metadata. Outputs are `AgentDefinition[]`, maps, or parsing errors.
- gates_or_invariants: Missing/invalid agent frontmatter raises `AgentParsingError`; cache can be cleared for tests.
- dependencies_and_callers: Used by task discovery/tool and role specialization tests.
- edge_cases_or_failure_modes: Duplicate names, malformed frontmatter, blank prompt content.
- validation_or_tests: `role-specialization.test.ts` and task discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2293 `file` `packages/coding-agent/src/tools/bash-interactive.ts`
- cursor: `[_]`
- core_role: Interactive bash PTY runner and overlay renderer.
- algorithmic_behavior: Normalizes PTY capture chunks, maps Kitty/key input to terminal escape sequences, manages overlay write queue/flush, handles escape cancellation, resizes PTY to viewport, streams output through `OutputSink`, and returns `BashInteractiveResult` (`bash-interactive.ts:29`, `bash-interactive.ts:46`, `bash-interactive.ts:106`, `bash-interactive.ts:298`).
- inputs_outputs_state: Inputs are command/cwd/env/settings, TUI input, PTY output, abort signal. State is PTY session, overlay queue, terminal buffer, output sink. Outputs are rendered overlay and summary/result.
- gates_or_invariants: Escape kills running PTY; output sanitized with optional sixel passthrough; terminal dimensions tracked; finished guard prevents double completion.
- dependencies_and_callers: Used by bash tool interactive mode; depends on pi-natives PTY, xterm headless, TUI/theme.
- edge_cases_or_failure_modes: Kitty release events ignored, resize errors, timed out/killed states, binary/sixel output, aborted signals.
- validation_or_tests: Bash/tool rendering tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2323 `file` `packages/coding-agent/src/tools/json-tree.ts`
- cursor: `[_]`
- core_role: Compact/expanded JSON argument tree renderer for tool calls.
- algorithmic_behavior: Formats scalars, inline args within width, hides internal arg keys, recursively renders JSON tree lines with max depth/line/scalar limits (`json-tree.ts:9`, `json-tree.ts:16`, `json-tree.ts:30`, `json-tree.ts:87`).
- inputs_outputs_state: Inputs are unknown JSON-ish args, width/theme/expanded flag. Outputs are string lines.
- gates_or_invariants: Hidden keys include intent and partial JSON; collapsed/expanded caps avoid oversized UI.
- dependencies_and_callers: Tool renderers and TUI components.
- edge_cases_or_failure_modes: Long strings, circular/non-JSON objects, narrow widths, deeply nested arrays/objects.
- validation_or_tests: Tool renderer tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2353 `file` `packages/coding-agent/src/tools/tool-timeouts.ts`
- cursor: `[_]`
- core_role: Central timeout caps/defaults for selected tools.
- algorithmic_behavior: Defines `TOOL_TIMEOUTS`, derived `ToolWithTimeout`, and `clampTimeout(tool, rawTimeout)` (`tool-timeouts.ts:1`, `tool-timeouts.ts:10`, `tool-timeouts.ts:26`).
- inputs_outputs_state: Inputs are tool ID and optional raw timeout. Output is bounded timeout.
- gates_or_invariants: Raw timeout clamped to tool min/max/default.
- dependencies_and_callers: Used by tool execution timeout paths.
- edge_cases_or_failure_modes: Undefined, NaN, below min, above max.
- validation_or_tests: Tool timeout behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2383 `file` `packages/coding-agent/src/utils/edit-mode.ts`
- cursor: `[_]`
- core_role: Edit-mode normalization and resolution helper.
- algorithmic_behavior: Defines edit mode literals/default, normalizes strings, and resolves session edit mode with env/settings fallback (`edit-mode.ts:3`, `edit-mode.ts:16`, `edit-mode.ts:31`).
- inputs_outputs_state: Inputs are env, settings-like object, session-like object. Output is selected edit mode.
- gates_or_invariants: Only known mode IDs accepted; default is `hashline`.
- dependencies_and_callers: Edit tools/session setup.
- edge_cases_or_failure_modes: Invalid env/config mode, null mode.
- validation_or_tests: Edit mode tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2413 `file` `packages/coding-agent/src/workflow/definition.ts`
- cursor: `[_]`
- core_role: Workflow YAML parser and static validator.
- algorithmic_behavior: Parses YAML into `WorkflowDefinition`, models, nodes, edges, resources, capabilities, migrations, subflows, prompt/script sources, and conditions; validates edge/node references, waitFor references, prompt references, migration targets, and subflow targets (`workflow/definition.ts:166`, `workflow/definition.ts:217`, `workflow/definition.ts:257`, `workflow/definition.ts:395`).
- inputs_outputs_state: Input is YAML source and optional path. Output is typed definition or `WorkflowDefinitionError`.
- gates_or_invariants: Duplicate node IDs rejected; edges array required; node types/resource kinds constrained; condition parser diagnostics surfaced with source path.
- dependencies_and_callers: Workflow loader/runner/CLI; depends on workflow condition/state-schema parsers.
- edge_cases_or_failure_modes: Malformed YAML, unknown node refs, invalid condition state refs, fallback verdict misuse, subflow mismatch.
- validation_or_tests: Workflow runner/session/runtime/graph tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2443 `file` `packages/coding-agent/test/capability/rule-buckets.test.ts`
- cursor: `[_]`
- core_role: Tests capability rule bucketing and TTSR integration.
- algorithmic_behavior: Builds synthetic rules and asserts `bucketRules` classifies rules into proper default/TTSR/runtime buckets (`rule-buckets.test.ts:26`).
- inputs_outputs_state: Inputs are `Rule` arrays and TTSR manager. Outputs are bucketed rule sets.
- gates_or_invariants: Builtin/provider IDs and rule fields determine bucket placement.
- dependencies_and_callers: Tests `capability/rule-buckets` and `TtsrManager`.
- edge_cases_or_failure_modes: Empty conditions, builtin defaults, overlapping buckets.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2473 `file` `packages/coding-agent/test/core/python-kernel-display.test.ts`
- cursor: `[_]`
- core_role: Tests Python kernel display rendering.
- algorithmic_behavior: Asserts `renderKernelDisplay` formats Python display payloads as expected (`python-kernel-display.test.ts:4`).
- inputs_outputs_state: Inputs are display payloads. Outputs are rendered strings/blocks.
- gates_or_invariants: Display output must preserve useful content without corrupting UI.
- dependencies_and_callers: Tests eval Python kernel display helper.
- edge_cases_or_failure_modes: Empty displays, MIME/value selection.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2503 `file` `packages/coding-agent/test/discovery/omp-plugins.test.ts`
- cursor: `[_]`
- core_role: Tests OMP plugin discovery provider.
- algorithmic_behavior: Creates temp user/project/plugin dirs and verifies project/user settings extensions, CLI injection, file extension entrypoints, relative paths, invalid MCP entries, installed/disabled/linked plugin discovery (`omp-plugins.test.ts:118`, `omp-plugins.test.ts:191`, `omp-plugins.test.ts:230`).
- inputs_outputs_state: Inputs are temp settings, package/plugin manifests, `.mcp.json`. Outputs are discovered capability items/warnings.
- gates_or_invariants: Disabled plugins do not contribute; invalid bare MCP entries warn/skip; relative paths resolve against project cwd.
- dependencies_and_callers: Tests discovery provider and capability registry.
- edge_cases_or_failure_modes: Linked plugin only in lockfile, file entry with no siblings, installed node_modules layout.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2533 `file` `packages/coding-agent/test/internal-urls/history-protocol.test.ts`
- cursor: `[_]`
- core_role: Tests internal `history://` URL protocol.
- algorithmic_behavior: Builds fake registry/session files and asserts history URL routing resolves transcript/session history content/errors (`history-protocol.test.ts:69`).
- inputs_outputs_state: Inputs are internal URL paths and temp session storage. Outputs are routed content or errors.
- gates_or_invariants: Unknown agent/session and missing transcript should produce clear errors.
- dependencies_and_callers: Tests `InternalUrlRouter`, `AgentRegistry`, session entries.
- edge_cases_or_failure_modes: Unknown agent, no session file, bad history target, missing transcript.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2563 `file` `packages/coding-agent/test/plan-mode/plan-protection.test.ts`
- cursor: `[_]`
- core_role: Tests compaction/shake protection for plan reads.
- algorithmic_behavior: Verifies `createPlanReadMatcher` protects `local://PLAN.md` and current titled plan aliases/selectors, reacts to retitle, rejects non-plan/non-read tools, and prevents plan read pruning/shaking (`plan-protection.test.ts:32`, `plan-protection.test.ts:121`).
- inputs_outputs_state: Inputs are tool contexts and compaction entries. Outputs are match booleans and pruned/shake results.
- gates_or_invariants: Plan read survives compaction while ordinary reads can be pruned.
- dependencies_and_callers: Tests plan-mode protection and pi-agent-core compaction pruning/shake.
- edge_cases_or_failure_modes: Single-slash local URL, selector suffixes, renamed plan path, false positives like `PLAN.md.bak`.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2593 `file` `packages/coding-agent/test/session/yield-queue.test.ts`
- cursor: `[_]`
- core_role: Tests session yield queue behavior.
- algorithmic_behavior: Asserts enqueue during streaming defers, idle enqueue schedules debounced flush, stale entries drop, null build suppresses injection, failures isolate by kind, order preserved, and lazy drain snapshots/clears (`yield-queue.test.ts:52`).
- inputs_outputs_state: Inputs are queued entries/builders/staleness checks. Outputs are streaming messages or idle batches.
- gates_or_invariants: Queue flush must not inject stale/null entries; one kind failure cannot abort other kinds.
- dependencies_and_callers: Tests `YieldQueue`.
- edge_cases_or_failure_modes: Streaming vs idle race, lazy drain after staleness, registration order.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2623 `file` `packages/coding-agent/test/task/role-specialization.test.ts`
- cursor: `[_]`
- core_role: Tests task role/specialization feature.
- algorithmic_behavior: Verifies display-name fallback/truncation, control character collapse, prompt role preamble rendering, task schema role bounds, and approval details surfacing role (`role-specialization.test.ts:20`, `role-specialization.test.ts:73`, `role-specialization.test.ts:88`, `role-specialization.test.ts:124`).
- inputs_outputs_state: Inputs are role strings, task params, prompts. Outputs are labels, schema parse results, approval lines.
- gates_or_invariants: Role label cap 80, input cap 256, surrogate pairs not split, blank roles omitted.
- dependencies_and_callers: Tests task types/schema and `TaskTool`.
- edge_cases_or_failure_modes: Zero-width/control chars, minimal truncation cap, batch task roles.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2653 `file` `packages/coding-agent/test/tools/browser-op-tracking.test.ts`
- cursor: `[_]`
- core_role: Tests browser operation tracking diagnostics and screenshot format inference.
- algorithmic_behavior: Asserts screenshot operations are labeled by distinguishing args, inflight summaries order/name helpers with durations, empty inflight summary is blank, and path extension maps to capture format (`browser-op-tracking.test.ts:9`, `browser-op-tracking.test.ts:41`).
- inputs_outputs_state: Inputs are operation maps and file paths. Outputs are diagnostic strings and image format literals.
- gates_or_invariants: Unknown/missing extension falls back to png; diagnostics must attribute timeout to still-running helpers.
- dependencies_and_callers: Tests browser tool tracking helpers.
- edge_cases_or_failure_modes: Uppercase extension, selector labels, empty maps.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2683 `file` `packages/coding-agent/test/tools/irc.test.ts`
- cursor: `[_]`
- core_role: Tests inter-agent IRC bus/tool.
- algorithmic_behavior: Covers live delivery, waking/reviving parked agents, sibling relay to main UI, unknown/aborted failures, wait filters/timeouts/abort/FIFO, mailbox cap/drain/peek, and `IrcTool` list/send/wait/inbox contracts (`irc.test.ts:97`, `irc.test.ts:116`, `irc.test.ts:353`).
- inputs_outputs_state: Inputs are fake registry/sessions/messages/tool calls. Outputs are receipts, delivered messages, unread counts, tool result details.
- gates_or_invariants: Mailbox cap 100 drops oldest; await cannot broadcast or self-send; waiters cleaned after timeout/abort.
- dependencies_and_callers: Tests `IrcBus`, `IrcTool`, registry/lifecycle/session types.
- edge_cases_or_failure_modes: Parked reviver absence/error, stale buffered mail, recipient delivery errors, depth cap.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2713 `file` `packages/coding-agent/test/tools/search-tool-bm25.test.ts`
- cursor: `[_]`
- core_role: Tests BM25 tool-discovery tool.
- algorithmic_behavior: Verifies cached search index use, ranked match activation, union of selected tools across searches, skipping already-selected tools before limit, invalid input rejection, disabled discovery rejection, builtin discovery mode, and description rendering (`search-tool-bm25.test.ts:74`, `search-tool-bm25.test.ts:213`).
- inputs_outputs_state: Inputs are query/limit/session tool corpus/settings. Outputs are tool result content/details and selected tool state.
- gates_or_invariants: Empty query/limit 0 invalid; discovery disabled errors; selected tools persist/union.
- dependencies_and_callers: Tests `SearchToolBm25Tool` and description renderer.
- edge_cases_or_failure_modes: Exhausted matches, builtins mixed with MCP, cached index vs raw tools.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2743 `file` `packages/coding-agent/test/utils/markit-mupdf-warnings.test.ts`
- cursor: `[_]`
- core_role: Tests Markit/PDF warning routing.
- algorithmic_behavior: Converts a warning PDF buffer and asserts recoverable MuPDF warnings go to file logger, not console, while content conversion succeeds (`markit-mupdf-warnings.test.ts:41`).
- inputs_outputs_state: Inputs are PDF buffer and extension. Outputs are conversion result and logger/console calls.
- gates_or_invariants: Recoverable warnings must not corrupt TUI via console error.
- dependencies_and_callers: Tests `convertBufferWithMarkit` and logger.
- edge_cases_or_failure_modes: Warning text from native converter, console leakage.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2773 `file` `packages/collab-web/src/lib/format.ts`
- cursor: `[_]`
- core_role: Formatting helpers for collab web UI.
- algorithmic_behavior: Formats token counts, USD costs, durations, relative time, percentages, shortened paths, and generic message text extraction (`format.ts:4`, `format.ts:16`, `format.ts:22`, `format.ts:63`).
- inputs_outputs_state: Inputs are numbers/timestamps/paths/messages. Outputs are display strings.
- gates_or_invariants: Null percent displays fallback; home-ish paths shortened by segment logic.
- dependencies_and_callers: Used by collab-web transcript/dashboard components.
- edge_cases_or_failure_modes: Unknown message shape, tiny/large costs, invalid timestamps.
- validation_or_tests: Web component tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2803 `file` `packages/mnemopi/src/core/mmr.ts`
- cursor: `[_]`
- core_role: Maximal Marginal Relevance reranking helper.
- algorithmic_behavior: Computes Jaccard similarity over token sets and reranks candidates by relevance/diversity tradeoff using `lambda`, returning selected items/scores (`mmr.ts:9`, `mmr.ts:22`).
- inputs_outputs_state: Inputs are result items with text/score, limit/lambda/similarity function. Output is reranked result array.
- gates_or_invariants: Diversity penalty compares against already selected results; generic type preserves item fields.
- dependencies_and_callers: Used by mnemopi retrieval/reranking.
- edge_cases_or_failure_modes: Empty candidates, duplicate text, lambda extremes, zero-token text.
- validation_or_tests: Mnemopi tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2833 `file` `packages/stats/src/client/api.ts`
- cursor: `[_]`
- core_role: Browser client API wrapper for stats dashboard.
- algorithmic_behavior: Defines `ApiError`, fetches overview/model/cost/requests/errors/details/sync/behavior/folder stats from `/api` endpoints, and parses JSON with status checking (`api.ts:12`, `api.ts:34`, `api.ts:68`).
- inputs_outputs_state: Inputs are range/limit/id and abort signal. Outputs are typed dashboard data or `ApiError`.
- gates_or_invariants: Non-OK HTTP responses become `ApiError`; defaults include `24h` and limit 50.
- dependencies_and_callers: Used by stats React/Solid client data hooks/components.
- edge_cases_or_failure_modes: Abort, non-JSON error, server status errors.
- validation_or_tests: Stats client tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2863 `file` `packages/utils/test/mermaid/xychart.test.ts`
- cursor: `[_]`
- core_role: Tests vendored Mermaid ASCII xychart renderer.
- algorithmic_behavior: Verifies bar/line/mixed/horizontal charts, titles/axes, single/two/zero/large values, axis markers, Unicode vs ASCII mode characters (`xychart.test.ts:22`, `xychart.test.ts:79`, `xychart.test.ts:236`, `xychart.test.ts:283`).
- inputs_outputs_state: Inputs are Mermaid xychart definitions and render options. Outputs are ASCII diagram strings.
- gates_or_invariants: ASCII mode must not emit Unicode blocks/corners; line charts use staircase routing, not dot markers.
- dependencies_and_callers: Tests `renderMermaidASCII`.
- edge_cases_or_failure_modes: Single point, all zeros, large values, mixed chart series.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2893 `directory` `packages/coding-agent/src/web/search/providers`
- cursor: `[_]`
- core_role: Web search provider adapters for multiple upstream search APIs and synthetic/internal providers.
- algorithmic_behavior: Recursively inspected 16 files: base provider interface, Brave, Exa, Gemini, Kagi, Kimi, Parallel, Perplexity, SearXNG, Tavily, Z.ai, Anthropic/Codex search, synthetic provider, and shared utils. Providers normalize params, build requests, parse responses/errors, synthesize answers/sources, clamp result counts/timeouts, and map provider-specific fields to `SearchResponse` (`providers/base.ts:58`, `providers/exa.ts:312`, `providers/parallel.ts:164`, `providers/codex.ts:68`).
- inputs_outputs_state: Inputs are query/recency/domains/result count/API keys/fetch overrides. Outputs are normalized answer/results/sources/errors.
- gates_or_invariants: Provider-specific max result caps, auth requirements, API error parsing, URL/source normalization, and fallback model selection for Codex search.
- dependencies_and_callers: Used by web search tool and search provider registry.
- edge_cases_or_failure_modes: Missing API keys, malformed provider payloads, empty results, retryable default model failures, MCP fallback parsing.
- validation_or_tests: Search tool tests and provider-specific tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2923 `file` `packages/ai/src/providers/__tests__/google-auth.test.ts`
- cursor: `[_]`
- core_role: Tests Vertex/Google ADC impersonated service account token flow.
- algorithmic_behavior: Rejects malformed impersonation URL before network, signs RS256 JWT for service-account source credential, exchanges JWT bearer assertion, calls IAMCredentials generateAccessToken, and validates request bodies/headers (`google-auth.test.ts:34`, `google-auth.test.ts:82`).
- inputs_outputs_state: Inputs are ADC JSON/temp files and mocked fetch. Outputs are access token and captured HTTP calls.
- gates_or_invariants: Malformed URLs cause `RangeError` without fetch; source credential uses JWT bearer grant, not refresh grant.
- dependencies_and_callers: Tests `getVertexAccessToken` and cache reset.
- edge_cases_or_failure_modes: URL validation, JWT signing, IAM URL reconstruction.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2953 `file` `packages/ai/src/utils/schema/json-schema-validator.ts`
- cursor: `[_]`
- core_role: JSON Schema value validator used for schema-constrained tool/output checks.
- algorithmic_behavior: Validates primitive types, nullable, const/enum, anyOf/oneOf/allOf/not/if-then-else, local `$ref`, object keywords, array keywords, string regex/length, number bounds/multipleOf, and returns structured issues (`json-schema-validator.ts:161`, `json-schema-validator.ts:330`, `json-schema-validator.ts:435`, `json-schema-validator.ts:581`).
- inputs_outputs_state: Inputs are schema and value. Output is `{ success, issues }` or boolean helper.
- gates_or_invariants: `$ref` depth max 64, seen-pair cycle guard, JSON pointer decoding, unevaluated keyword warning only once.
- dependencies_and_callers: Used by AI schema validation/output validation paths.
- edge_cases_or_failure_modes: Cyclic refs/value graphs, invalid regex, oneOf multiple matches, floating multipleOf precision.
- validation_or_tests: Schema validator tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2983 `file` `packages/coding-agent/src/commit/agentic/agent.ts`
- cursor: `[_]`
- core_role: Runs the agentic commit-planning session and renders progress.
- algorithmic_behavior: Creates commit tools/session with system/user prompts, streams session events, renders assistant/tool messages to console, tracks state until commit/changelog proposal complete, and sends reminder messages if needed (`commit/agentic/agent.ts:38`, `agent.ts:184`, `agent.ts:285`, `agent.ts:291`).
- inputs_outputs_state: Inputs are cwd, model/settings/auth, diff metadata, changelog entries, and require-changelog flag. Output is `CommitAgentState`.
- gates_or_invariants: Proposal completeness requires commit proposal and optional changelog proposal; tool args truncated for display.
- dependencies_and_callers: Used by `commit/agentic/index.ts`; depends on SDK session, commit tools, prompts, model registry.
- edge_cases_or_failure_modes: Agent fails to call proposal tools, long tool args, markdown render issues, model/auth failures.
- validation_or_tests: Commit agentic tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3013 `file` `packages/coding-agent/src/edit/hashline/noop-loop-guard.ts`
- cursor: `[_]`
- core_role: Guard against repeated no-op hashline edits.
- algorithmic_behavior: Maintains per-session/canonical-path no-op entries keyed by patch input hash, increments repeat counts, flags hard limit at 3, resets per file, and hashes patch inputs (`noop-loop-guard.ts:40`, `noop-loop-guard.ts:47`, `noop-loop-guard.ts:71`, `noop-loop-guard.ts:97`).
- inputs_outputs_state: Inputs are session owner, canonical path, patch input. State is session-scoped guard map. Outputs are record result/warning/limit status.
- gates_or_invariants: `NOOP_HARD_LIMIT = 3`; canonical path partitions counts; reset clears path entry.
- dependencies_and_callers: Used by hashline edit execution.
- edge_cases_or_failure_modes: Same no-op repeated with whitespace-equivalent but different hash, session missing guard map.
- validation_or_tests: Hashline no-op tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3043 `file` `packages/coding-agent/src/eval/py/tool-bridge.ts`
- cursor: `[_]`
- core_role: Local HTTP bridge allowing Python eval kernels to call session tools.
- algorithmic_behavior: Maintains registrations by session/run, lazily starts bridge server, dispatches JSON requests to JS `callSessionTool`, returns status events/results, and supports unregister/dispose (`eval/py/tool-bridge.ts:30`, `tool-bridge.ts:137`, `tool-bridge.ts:158`, `tool-bridge.ts:169`).
- inputs_outputs_state: Inputs are Python HTTP requests, session/run IDs, tool call payloads. State is registration map and server promise. Outputs are JSON responses and status events.
- gates_or_invariants: Calls require matching registration; server is singleton; dispose closes server/reset state.
- dependencies_and_callers: Python eval runner/prelude and JS eval tool bridge.
- edge_cases_or_failure_modes: Missing registration, malformed JSON, tool call error, server startup failure.
- validation_or_tests: Eval bridge tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3073 `file` `packages/coding-agent/src/extensibility/plugins/manager.ts`
- cursor: `[_]`
- core_role: Plugin install/link/uninstall/config/validation manager.
- algorithmic_behavior: Validates package/git specs, reads runtime config/overrides/package deps, installs via npm, resolves git package names, validates extension exports/manifests/features/settings, rolls back failed installs, links local plugins, lists/checks installed plugins, and parses setting values (`plugins/manager.ts:46`, `manager.ts:113`, `manager.ts:326`, `manager.ts:917`).
- inputs_outputs_state: Inputs are plugin specs, paths, runtime config, manifests, npm output, feature/settings args. Outputs are installed plugin records, config changes, validation results/errors.
- gates_or_invariants: Rejects shell metacharacters, invalid package names, unknown features/settings, missing extension files, failed npm exits.
- dependencies_and_callers: Used by plugin CLI and discovery; depends on parser/loader/runtime config/git-url helpers.
- edge_cases_or_failure_modes: npm install succeeds but package missing, git dependency key unknown, rollback failure, linked package without manifest, disabled features.
- validation_or_tests: Plugin manifest/path and discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3103 `file` `packages/coding-agent/src/modes/components/bordered-loader.ts`
- cursor: `[_]`
- core_role: TUI component wrapping cancellable loader in dynamic border.
- algorithmic_behavior: `BorderedLoader` composes `CancellableLoader`, `DynamicBorder`, text/spacer components, and theme (`bordered-loader.ts:6`).
- inputs_outputs_state: Inputs are TUI/theme/loader state. Output is rendered component tree.
- gates_or_invariants: Loader cancellation/status must propagate through component.
- dependencies_and_callers: Used by modes/components during long-running operations.
- edge_cases_or_failure_modes: Narrow layout, disposal/cancel propagation.
- validation_or_tests: Component tests indirectly.
- skip_candidate: `yes: UI composition leaf, little algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3133 `file` `packages/coding-agent/src/modes/components/oauth-selector.ts`
- cursor: `[_]`
- core_role: Interactive OAuth credential/provider selector component.
- algorithmic_behavior: Lists OAuth providers/credentials, handles up/down/cancel/select keybindings, displays credential origins, scrolls visible window capped at 10, and triggers auth-storage/provider actions (`oauth-selector.ts:18`, `oauth-selector.ts:38`).
- inputs_outputs_state: Inputs are providers, auth storage credentials, key events. State is selected index/scroll/credential list. Outputs are selected provider/credential action and rendered rows.
- gates_or_invariants: Max visible rows, cancel key handling, origin labels constrained.
- dependencies_and_callers: Used by login/auth UI; depends on pi-ai OAuth provider list and TUI select/keybinding utilities.
- edge_cases_or_failure_modes: No providers, many credentials requiring scroll, cancelled selection, stale auth storage.
- validation_or_tests: OAuth UI tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3163 `file` `packages/coding-agent/src/modes/components/workflow-graph.test.ts`
- cursor: `[_]`
- core_role: Tests workflow graph TUI display modes.
- algorithmic_behavior: Asserts collapsed dashboard rows are short/restorable, focused interruption action is prioritized in narrow mode, compact mode shorter than full, and operator actions remain visible in very short compact mode (`workflow-graph.test.ts:8`).
- inputs_outputs_state: Inputs are workflow graph view fixtures and component width/height. Outputs are rendered text lines.
- gates_or_invariants: Critical `/workflow` operator commands must remain visible under compact/collapsed constraints.
- dependencies_and_callers: Tests `WorkflowGraphComponent`.
- edge_cases_or_failure_modes: Narrow/short terminal layouts, focused node display.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3193 `file` `packages/coding-agent/src/modes/theme/theme.ts`
- cursor: `[_]`
- core_role: TUI theme engine: symbols, colors, ANSI, theme loading, auto theme, highlighting, and sub-theme adapters.
- algorithmic_behavior: Defines Unicode/Nerd/ASCII symbol maps and spinners, validates theme JSON, resolves color variables/circular refs, detects color mode/background, constructs `Theme`, loads builtin/custom themes, watches theme files, handles auto dark/light, symbol presets, colorblind adjustment, highlight cache, markdown/select/editor themes (`theme.ts:233`, `theme.ts:977`, `theme.ts:1414`, `theme.ts:2110`, `theme.ts:2723`).
- inputs_outputs_state: Inputs are theme JSON/settings/env/terminal appearance/code. State includes global `theme`, current name, watcher, epoch, caches. Outputs are ANSI-styled strings, symbols, color maps, sub-theme objects.
- gates_or_invariants: Missing theme colors rejected; circular var refs rejected; superseded async theme loads ignored; colorblind mode transforms added color.
- dependencies_and_callers: Used throughout TUI renderers; depends on pi-tui theme types, pi-utils color helpers, native highlighter.
- edge_cases_or_failure_modes: Invalid color values, custom theme parse errors, stale watcher, dumb terminal, concurrent theme changes.
- validation_or_tests: Welcome/workflow/streaming component tests and theme tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3223 `file` `packages/coding-agent/src/web/scrapers/artifacthub.ts`
- cursor: `[_]`
- core_role: Special web scraper for Artifact Hub package pages.
- algorithmic_behavior: Parses Artifact Hub URLs, loads package API/page data, normalizes maintainers/links/repository/package fields, formats package metadata into markdown result (`artifacthub.ts:57`).
- inputs_outputs_state: Inputs are URL/fetch context. Output is `RenderResult` or null.
- gates_or_invariants: Non-ArtifactHub/home/search URLs return null; JSON parse failures handled.
- dependencies_and_callers: Used by web fetch/scraper dispatcher; tested by finance-media integration tests.
- edge_cases_or_failure_modes: Missing package fields, www subdomain, API/page load failure.
- validation_or_tests: `finance-media.test.ts` includes ArtifactHub URL cases.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3253 `file` `packages/coding-agent/src/web/scrapers/iacr.ts`
- cursor: `[_]`
- core_role: Special scraper for IACR ePrint/PDF resources.
- algorithmic_behavior: Matches IACR URLs, fetches binary PDFs when appropriate, converts via Markit, otherwise loads page content, and returns markdown render result (`iacr.ts:8`).
- inputs_outputs_state: Inputs are IACR URL and fetch/markit utilities. Output is markdown content or null.
- gates_or_invariants: Non-IACR URLs ignored; binary conversion path selected for PDFs.
- dependencies_and_callers: Web scraper dispatcher; depends on `fetchBinary`, `convertWithMarkit`, `loadPage`.
- edge_cases_or_failure_modes: PDF conversion warnings/failures, non-PDF page fallback, invalid IACR URL.
- validation_or_tests: Web scraper tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3283 `file` `packages/coding-agent/src/web/scrapers/sec-edgar.ts`
- cursor: `[_]`
- core_role: Special scraper for SEC EDGAR company/filing pages.
- algorithmic_behavior: Parses SEC filing/company data, loads JSON/page data, formats company/filing metadata into markdown, and returns special render result (`sec-edgar.ts:15`, `sec-edgar.ts:157`).
- inputs_outputs_state: Inputs are SEC URL and loaded JSON/text. Output is `RenderResult` or null.
- gates_or_invariants: SEC URL matching and JSON parse fallback determine handling.
- dependencies_and_callers: Web scraper dispatcher; depends on `tryParseJson`, `loadPage`, `buildResult`.
- edge_cases_or_failure_modes: Missing filing fields, SEC HTML vs JSON variants, invalid accession/company IDs.
- validation_or_tests: Web scraper tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3313 `file` `packages/coding-agent/test/modes/components/assistant-message-streaming-fastpath.test.ts`
- cursor: `[_]`
- core_role: Tests assistant message streaming fast-path renderer equivalence.
- algorithmic_behavior: Compares incremental render reuse to teardown render for growing thinking/text streams, suppresses dot-only reasoning placeholders, rebuilds after invalidate, handles redacted thinking index shifts, error trailers, and visibility toggles (`assistant-message-streaming-fastpath.test.ts:56`).
- inputs_outputs_state: Inputs are assistant message content variants. Outputs are rendered line arrays/component identity checks.
- gates_or_invariants: Fast path must render byte-equivalent output to full rebuild while preserving/rebuilding children at correct times.
- dependencies_and_callers: Tests `AssistantMessageComponent`, Markdown/TUI, settings/theme.
- edge_cases_or_failure_modes: Empty-to-filled block, redacted thinking inserted mid-stream, error after text, invalidation.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3343 `file` `packages/coding-agent/test/modes/components/welcome.test.ts`
- cursor: `[_]`
- core_role: Tests welcome component tip selection.
- algorithmic_behavior: Asserts standard tip for non-unicode preset and 10% nerdfont tip probability path under unicode preset using mocked randomness/settings (`welcome.test.ts:6`).
- inputs_outputs_state: Inputs are theme symbol preset/random values. Output is selected welcome tip.
- gates_or_invariants: Special nerdfont tip only under unicode preset/probability path.
- dependencies_and_callers: Tests `WelcomeComponent`, settings/theme.
- edge_cases_or_failure_modes: Randomness determinism, theme preset switching.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3373 `file` `packages/coding-agent/test/tools/web-scrapers/finance-media.test.ts`
- cursor: `[_]`
- core_role: Integration tests for selected web scrapers.
- algorithmic_behavior: Tests CoinGecko, Discogs, and ArtifactHub handlers return null for irrelevant/home/search pages and fetch/format real pages when `WEB_FETCH_INTEGRATION` is enabled (`finance-media.test.ts:6`, `finance-media.test.ts:24`, `finance-media.test.ts:70`, `finance-media.test.ts:110`).
- inputs_outputs_state: Inputs are URLs and live network fetch (guarded). Outputs are scraper `RenderResult`s.
- gates_or_invariants: Integration gated by env; contentType expected `text/markdown`.
- dependencies_and_callers: Tests scraper handlers.
- edge_cases_or_failure_modes: Network unavailable, page layout/API drift, www subdomain.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3403 `file` `packages/collab-web/src/components/transcript/ToolCard.tsx`
- cursor: `[_]`
- core_role: Collab web transcript tool-result card component.
- algorithmic_behavior: Memoized React component renders tool name, summary text via `messageText`, and body via `ToolView` with host (`ToolCard.tsx:7`, `ToolCard.tsx:19`).
- inputs_outputs_state: Inputs are `ToolResultMessage` and render host. Output is React node.
- gates_or_invariants: Tool view receives full message/host; summary normalized by shared formatter.
- dependencies_and_callers: Collab web transcript UI.
- edge_cases_or_failure_modes: Unknown tool result shape, long text display delegated to renderers.
- validation_or_tests: Collab web UI tests indirectly.
- skip_candidate: `yes: thin UI wrapper, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3433 `file` `packages/collab-web/src/tool-render/tools/todo.tsx`
- cursor: `[_]`
- core_role: Collab web renderer for todo tool results.
- algorithmic_behavior: Maps task statuses to icons, formats Roman numerals, extracts details records, renders summary/body rows for todo phases/items/statuses with normalized/truncated text (`todo.tsx:7`, `todo.tsx:16`, `todo.tsx:142`).
- inputs_outputs_state: Inputs are tool render props/details. Output is React summary/body.
- gates_or_invariants: Status limited to pending/in_progress/completed/abandoned; text normalized/truncated for UI.
- dependencies_and_callers: Collab web tool-render registry.
- edge_cases_or_failure_modes: Missing details, unknown status, many tasks.
- validation_or_tests: Collab web renderer tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3463 `file` `packages/stats/src/client/data/view-models.ts`
- cursor: `[_]`
- core_role: Stats dashboard view-model builders.
- algorithmic_behavior: Builds cost summary totals, model performance lookup/series, behavior summary, and folder rows from API data (`view-models.ts:48`, `view-models.ts:75`, `view-models.ts:127`, `view-models.ts:162`).
- inputs_outputs_state: Inputs are API stats arrays. Outputs are UI-ready summary/series/rows.
- gates_or_invariants: Aggregates preserve range metadata; folders rows extend server stats.
- dependencies_and_callers: Stats client components.
- edge_cases_or_failure_modes: Empty series, missing model keys, zero totals.
- validation_or_tests: Stats client tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3493 `file` `python/robomp/web/src/components/Header.tsx`
- cursor: `[_]`
- core_role: SolidJS header component for robomp web UI.
- algorithmic_behavior: Renders runtime/status metadata using signals/resources, last tick state/error, config, and duration formatting (`Header.tsx:14`, `Header.tsx:90`).
- inputs_outputs_state: Inputs are Solid resources/signals and runtime info. Output is JSX header.
- gates_or_invariants: Conditional rendering via `Show`; meta props format values.
- dependencies_and_callers: robomp web app.
- edge_cases_or_failure_modes: Missing runtime info, fetch error, stale last tick.
- validation_or_tests: Web UI tests not assigned.
- skip_candidate: `yes: UI display component outside primary coding-agent core`

### OH_MY_HUMANIZE_MAIN-HZ-3523 `file` `packages/coding-agent/src/export/html/vendor/highlight.min.js`
- cursor: `[_]`
- core_role: Vendored minified Highlight.js bundle for HTML export syntax highlighting.
- algorithmic_behavior: Contains language grammars, regex matchers, emitter, and highlight registration/minified runtime (`highlight.min.js:174`, `highlight.min.js:327`, `highlight.min.js:1211`).
- inputs_outputs_state: Inputs are code strings/language names in HTML export. Outputs are highlighted HTML tokens/classes.
- gates_or_invariants: Frozen/internal grammar objects and language registry semantics are upstream Highlight.js behavior.
- dependencies_and_callers: Used by coding-agent HTML export.
- edge_cases_or_failure_modes: Unsupported language, illegal lexeme handling, minified vendor drift.
- validation_or_tests: HTML export tests indirectly.
- skip_candidate: `yes: third-party vendored minified library, not authored core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3553 `file` `packages/coding-agent/src/modes/components/status-line/types.ts`
- cursor: `[_]`
- core_role: Type contract for status-line rendering segments/presets.
- algorithmic_behavior: Defines collab status, segment settings/options/context, rendered segment, segment renderer interface, separator and preset definitions (`status-line/types.ts:8`, `status-line/types.ts:46`, `status-line/types.ts:91`, `status-line/types.ts:105`).
- inputs_outputs_state: Inputs/outputs are typed data passed between status-line components and segment renderers.
- gates_or_invariants: Segment context centralizes session/settings/collab/theme/width/time values.
- dependencies_and_callers: Status-line renderer components and settings schema.
- edge_cases_or_failure_modes: Type drift between settings and renderer implementation.
- validation_or_tests: Status-line tests indirectly.
- skip_candidate: `yes: type-only contract, not executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3583 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/canvas.ts`
- cursor: `[_]`
- core_role: Canvas core for vendored Mermaid ASCII renderer.
- algorithmic_behavior: Creates/copies/resizes canvases and role canvases, sets/merges char roles, merges junction characters, overlays canvases, converts to string with ANSI/color options, flips vertically, draws wide-character text, and sizes from grid (`canvas.ts:17`, `canvas.ts:66`, `canvas.ts:216`, `canvas.ts:242`, `canvas.ts:316`).
- inputs_outputs_state: Inputs are canvas grids, coordinates, strings, roles, color/theme options. Outputs are mutated/new canvases or rendered strings.
- gates_or_invariants: Bounds checks avoid out-of-range writes; junction map preserves line intersections; wide char metrics add pad cells.
- dependencies_and_callers: Used by Mermaid ASCII diagram renderers.
- edge_cases_or_failure_modes: Wide Unicode text, overlapping lines, negative/out-of-bounds coords, ANSI color role merge.
- validation_or_tests: Mermaid xychart tests indirectly.
- skip_candidate: `yes: vendored subsystem file, but algorithmic rendering core`

### OH_MY_HUMANIZE_MAIN-HZ-3613 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/index.ts`
- cursor: `[_]`
- core_role: Shape registry dispatcher for Mermaid ASCII nodes.
- algorithmic_behavior: Registers rectangle, diamond, circle, state, rounded, stadium, hexagon, and special shape renderers; exposes renderer lookup, render, dimension, and attachment point helpers (`shapes/index.ts:32`, `shapes/index.ts:59`, `shapes/index.ts:67`, `shapes/index.ts:81`, `shapes/index.ts:93`).
- inputs_outputs_state: Inputs are shape type, dimensions, labels, direction/options. Outputs are rendered canvas/dimensions/attachment coordinates.
- gates_or_invariants: Unknown shape falls back through registry/default behavior.
- dependencies_and_callers: Used by Mermaid ASCII draw/render pipeline.
- edge_cases_or_failure_modes: Unsupported shape names, attachment direction mismatches, label size overflow.
- validation_or_tests: Mermaid renderer tests indirectly.
- skip_candidate: `yes: vendored subsystem file, though algorithmic dispatcher`

## Worker Self-Test
- assigned_items_seen: 121 item sections emitted, one for each assigned ID from `OH_MY_HUMANIZE_MAIN-HZ-013` through `OH_MY_HUMANIZE_MAIN-HZ-3613`
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`

---

## Incremental Directory Refresh Addendum - oh-my-humanize/main bf4509d4f - OH_MY_HUMANIZE_MAIN-HZ-133

# agent_dir_04 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-133 `directory` `packages/coding-agent/src`
- cursor: `[_]`
- current_directory_core_role: `packages/coding-agent/src` is the main coding-agent CLI/runtime source tree. For workflows, this directory owns `.omhflow` artifact lookup/loading/freezing, workflow CLI command handling, session/headless runtime adapters, scheduler/runner orchestration, model/runtime binding, lifecycle/checkpoint event persistence, run-store reconstruction, prompt/resource materialization, graph/inspection rendering, and slash-command workflow control.
- directory_level_delta_since_old_commit: The changed source shifts headless workflow starts from simple run execution toward stop-aware, resumable lifecycle execution. `src/cli/workflow-cli.ts` now resolves the requested workflow cwd once, threads it into flow lookup and every headless runtime adapter, runs JavaScript workflow scripts relative to that cwd, preserves structured top-level script returns, installs `SIGINT`/`SIGTERM` abort handling for `omp workflow start`, passes that abort signal to both scheduler and node execution, and applies a default workflow runtime cap. `src/workflow/runner.ts` now composes explicit stop signals with max-runtime timeout signals, supports separate scheduler-stop and node-abort signals, races node execution against abort so an abort-ignoring runtime cannot keep the workflow alive forever, records aborted activations, and checkpoints stopped lifecycle attempts instead of failing them.
- affected_descendant_algorithms: Affected algorithms are CLI flag normalization and `workflow` command dispatch; headless artifact start validation; default start-node discovery; headless runtime binding availability checks; JS eval script execution; shell script spawning; headless agent task spawning; workflow runner signal composition; per-activation node abort selection; activation persistence; lifecycle attempt finish classification; checkpoint frontier/source mapping; and JSON/human output summarization for headless starts.
- current_inputs_outputs_state: Inputs now include `--cwd`, `--max-runtime-ms`, `--run-id`, `--family-id`, `--start`, activation limits, frozen `.omhflow` artifacts, frozen resource snapshots, runtime host adapters, scheduler stop signals, node abort signals, and optional per-activation node abort signals. `handleStart` normalizes cwd with `path.resolve(command.flags.cwd ?? getProjectDir())`; flow resolution and runtime execution use that cwd. JS scripts execute inside a temporary `process.chdir(cwd)` with `console.log` captured and restored; shell scripts and headless agent tasks use `Bun.spawn({ cwd, signal })`, with agent tasks launched through `launch --cwd <cwd>`. Outputs include stdout text/JSON, reconstructed run/family summaries, activation state patches, `activation_aborted` events, lifecycle stop/checkpoint records, frontier node ids, and materialized frozen resource directories exposed to script runtime context/env.
- new_or_changed_gates_or_invariants: Headless `workflow start` requires a frozen `.omhflow` artifact rather than a raw authoring package. Requested cwd must be consistently used for path resolution and headless execution. CLI signal listeners must be removed after the run. Max runtime aborts must use the shared `workflow max runtime elapsed after <n>ms` reason and clear their timer on completion. Scheduler stop and node abort are separate concepts: scheduler stop prevents downstream scheduling, while node abort is passed into the active runtime. Aborted node activations are persisted as `aborted`, not `failed`, and lifecycle attempts that stop due to activation limits, interrupt signals, node abort/deadline, or max runtime must record stop/checkpoint evidence with completed and aborted activation ids. Checkpoint creation must not happen while lifecycle activations remain running.
- dependencies_and_callers: `src/commands/workflow.ts` registers `workflow`/`flow`, including `--cwd` and `--max-runtime-ms`, then calls `resolveWorkflowCommandArgs` and `runWorkflowCommand`. `workflow-cli.ts` depends on artifact registry/package loader/freeze, session runtime adapters, runtime binding diagnostics, `DEFAULT_WORKFLOW_MAX_RUNTIME_MS`, and `runWorkflow`. `runner.ts` depends on scheduler abort/frontier behavior, node-runtime signal forwarding, lifecycle stop/checkpoint APIs, run-store activation persistence APIs, prompt/resource resolution, model resolution, and runtime-timeout reason formatting. Interactive slash workflow helpers also call `runWorkflow` with stop controllers, node abort controllers, per-activation abort signals, and the same default max-runtime behavior, so the runner changes affect both headless CLI and TUI/slash workflow execution.
- edge_cases_or_failure_modes: JS eval cwd handling mutates process-global cwd and `console.log`; it restores both in `finally`, but concurrent headless JS script activations in the same process can still race or bleed cwd/output because the scheduler can run multiple ready activations. JS eval abort is runner-level only; async ignored promises can be checkpointed, but CPU-bound JS that blocks the event loop cannot be preempted until it yields. Shell and agent child processes receive abort signals through `Bun.spawn`, but the runner still protects lifecycle completion if an adapter ignores abort. Abort reasons are preserved from the first combined signal that fires. If a stop arrives after the graph has no frontier, checkpointing is not triggered by `workflowCheckpointReason`; completed graphs remain completion candidates.
- validation_or_tests: `src/cli/__tests__/workflow-cli.test.ts` pins headless `.omhflow` start behavior, frozen resource delivery to shell scripts, JavaScript script execution from requested `--cwd`, structured JS top-level returns, `SIGINT` conversion into a stopped run/checkpoint, and signal listener cleanup. `test/workflow/runner.test.ts` pins activation-limit checkpointing, cancellation frontier checkpointing, dedicated node abort signal forwarding, deadline-aborted activation checkpointing when the runtime throws, deadline-aborted checkpointing when the runtime ignores abort, and max-runtime checkpoint reasons. `test/workflow-command.test.ts` pins typed propagation of `cwd` and `maxRuntimeMs` and confirms headless agent tasks preserve `launch --cwd`. Tests were inspected for research evidence; no source edits were made.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-133`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
