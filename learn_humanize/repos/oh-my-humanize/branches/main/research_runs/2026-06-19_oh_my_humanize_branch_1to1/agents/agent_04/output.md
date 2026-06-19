# agent_04 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-004 `directory` `infra`
- cursor: `[_]`
- core_role: Self-hosted CI/Kata runner infrastructure and operational scripts.
- algorithmic_behavior: `reload-runner.sh` copies/builds the runner image, selects containerd or Docker backend, verifies baked tools, and rolls the ARC scale set; `tune-kata-runtime.sh` patches Kata runtime config and smoke boots a pod; `runner.Dockerfile` bakes CI dependencies.
- inputs_outputs_state: Inputs are env vars such as `CI_HOST`, ARC/Kata paths, image tags, and tool versions; outputs are remote image tags, patched Helm values/Kata config, and smoke-test status.
- gates_or_invariants: Requires `CI_HOST`; scripts use `set -euo pipefail`; backend is restricted to `auto|containerd|docker`; image verification checks `gh`, `fd`, `rg`, `magick`, `bun`, Rust, sccache, Zig, and cargo helpers.
- dependencies_and_callers: Uses SSH/SCP, BuildKit, nerdctl, Docker, k3s containerd, Helm, kubectl, ARC, Kata Containers; docs in `infra/docs` describe the same pipeline.
- edge_cases_or_failure_modes: Falls back from containerd to Docker only in `auto`; missing sockets/tools, failed runtime patch regexes, Helm rollout failure, or smoke pod timeout abort the flow.
- validation_or_tests: Runtime validation is embedded in shell smoke tests and documentation procedures; no package-local unit tests.
- skip_candidate: `yes: operational CI infrastructure rather than application runtime algorithm, but it defines validation workflow behavior.`

### OH_MY_HUMANIZE_MAIN-HZ-034 `directory` `packages/stats`
- cursor: `[_]`
- core_role: Local observability dashboard that parses session JSONL, stores metrics in SQLite, aggregates usage/cost/behavior stats, and serves a React dashboard.
- algorithmic_behavior: `parser.ts` incrementally parses session files from stored byte offsets; `db.ts` creates/migrates `messages`, `file_offsets`, `user_messages`, and `meta`, backfills costs and behavior fields, and exposes aggregate queries; `aggregator.ts` fans parsing through workers, applies offsets, and computes dashboard ranges; `server.ts` routes `/api/*` and static client assets.
- inputs_outputs_state: Inputs are session files, range selectors, sync requests, and SQLite state; outputs are dashboard API DTOs, time series, cost series, recent requests/errors, behavior metrics, and persisted offsets/backfill markers.
- gates_or_invariants: Idempotent inserts are keyed by `(session_file, entry_id)`; offsets are reset by backfill flags; range handling is limited to known windows; static extraction sanitizes archive paths; worker sync has ping smoke coverage.
- dependencies_and_callers: Uses Bun SQLite, `@oh-my-pi/pi-catalog` model costs, bundled client archive, Web Workers re-entering CLI host, React client routes/components, and tests under `packages/stats/test`.
- edge_cases_or_failure_modes: Handles truncated JSONL by parsing only complete entries, missing costs by catalog backfill, older rows via schema migration, embedded-client path traversal, worker crashes/timeouts, and invalid range fallbacks.
- validation_or_tests: Tests cover user metrics, behavior backfill, cost/range aggregation, priority premium requests, DB cost, and client view models.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-064 `file` `docs/natives-text-search-pipeline.md`
- cursor: `[_]`
- core_role: Architecture document for native text/search/AST/file-discovery pipelines.
- algorithmic_behavior: Describes regex search, glob/fuzzy discovery, ast-grep match/edit, shared `fs_cache`, ANSI text utilities, highlighting, and token counting, including JS API to Rust export mapping.
- inputs_outputs_state: Inputs are JS options, filesystem roots, glob/regex/AST patterns, cache state, and text buffers; outputs are shaped JS result arrays, highlighted text, counts, and utility results.
- gates_or_invariants: Documents malformed regex/glob handling, cache transitions, pure utility versus filesystem-dependent flows, and stale-result tradeoffs.
- dependencies_and_callers: References `packages/natives`, `crates/pi-natives`, Rust modules such as `grep`, `glob`, `ast`, `fs_cache`, `text`, `highlight`, and `tokens`.
- edge_cases_or_failure_modes: Notes malformed regex, malformed glob, AST failures, cache staleness, and filesystem scan failure behavior.
- validation_or_tests: Documentation itself is not executable; implementation validation lives in native/package tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-094 `file` `scripts/ci-update-brew-formula.ts`
- cursor: `[_]`
- core_role: Release automation script that renders a Homebrew formula from GitHub release asset digests.
- algorithmic_behavior: `parseArgs` extracts release tag and optional output path; `fetchAssets` shells to `gh release view`; `sha256For` validates `sha256:` digests; `renderFormula` emits Ruby formula blocks for macOS/Linux arm/intel assets.
- inputs_outputs_state: Inputs are CLI args, `OMP_REPO`, and GitHub release JSON; output is formula text to stdout or an `--out` path.
- gates_or_invariants: Requires all four assets, requires digest prefix `sha256:`, strips leading `v` from version, and uses Homebrew `using: :nounzip` because assets are bare binaries.
- dependencies_and_callers: Uses Bun Shell `$`, GitHub CLI, release workflow/tap checkout.
- edge_cases_or_failure_modes: Missing tag, missing `--out` value, failed `gh`, missing asset, or absent digest throws.
- validation_or_tests: Formula embeds `omp --version` test; no direct unit test for the script.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-124 `directory` `packages/agent/test`
- cursor: `[_]`
- core_role: Contract tests for the core agent loop, streaming, compaction, telemetry, context pruning, handoff, tool execution, and serialization.
- algorithmic_behavior: Tests simulate model streams, tool calls, aborts, steering queues, pause-turn retries, provider errors, append-only context fingerprints, compaction summaries, OTEL spans, proxy SSE disconnects, and pruning/shaking of large or superseded tool outputs.
- inputs_outputs_state: Inputs are mock models, mock tools, session messages, abort signals, telemetry configs, and compaction preparations; outputs are emitted events, final message arrays, spans, summaries, and serialized transcripts.
- gates_or_invariants: Protects one-at-a-time steering, deadline aborts, non-interruptible tool behavior, forced tool-choice refresh, in-place state identity, stable prefix fingerprints, protected tool outputs, and error-status propagation.
- dependencies_and_callers: Uses `@oh-my-pi/pi-agent-core`, mock AI providers, OTEL SDK test exporter, utility test tools in `test/utils`.
- edge_cases_or_failure_modes: Covers whitespace loops, harmony leakage, pause-turn caps, server disconnect without terminal SSE event, cyclic details in summaries, stale forced tools, and abort races.
- validation_or_tests: This directory is validation; no modifications were made.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-154 `directory` `packages/tui/bench`
- cursor: `[_]`
- core_role: Microbenchmarks comparing JS/native key parsing, terminal sequence matching, text layout, and sanitization implementations.
- algorithmic_behavior: `_jskey.ts` carries a JS key parser/matcher reference; `parse-key.ts` and `kitty-sequence.ts` compare native and JS paths over sample sequences; `sanitize.ts` compares regex/gated/skip-run sanitizers; `text-layout.ts` measures wrapping/truncation helpers.
- inputs_outputs_state: Inputs are hardcoded samples and iteration counts; outputs are console benchmark timings.
- gates_or_invariants: Benchmark loops use fixed sample sets and iteration constants; not part of production validation gates.
- dependencies_and_callers: Imports `@oh-my-pi/pi-natives` and `packages/tui/src` utilities.
- edge_cases_or_failure_modes: Benchmark-only code may drift from runtime parsers; no pass/fail semantics beyond runtime errors.
- validation_or_tests: Not formal tests; used for performance research.
- skip_candidate: `yes: benchmark harnesses rather than runtime algorithm surfaces, though they mirror key/sanitize algorithms.`

### OH_MY_HUMANIZE_MAIN-HZ-184 `file` `docs/tools/browser.md`
- cursor: `[_]`
- core_role: Browser tool runtime documentation.
- algorithmic_behavior: Defines browser tool source files, shared inputs, `open`, `close`, and `run` actions, output shapes, flow, modes/variants, side effects, caps, and errors.
- inputs_outputs_state: Inputs include action, URL, page/session identifiers, JS snippets, timeouts, and attachment/launch modes; outputs include page state, script result, screenshots/console/network-derived data as documented.
- gates_or_invariants: Documents limits/caps, lifecycle ownership, attach versus launch behavior, and error conditions for browser/CDP paths.
- dependencies_and_callers: References coding-agent browser tool implementation and Playwright/CDP attachment.
- edge_cases_or_failure_modes: Notes close/run/open errors, launch/attach failures, cap handling, and side effects from browser state.
- validation_or_tests: Documentation; behavior is exercised by browser-related coding-agent tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-214 `file` `scripts/install-tests/tarball.dockerfile`
- cursor: `[_]`
- core_role: Docker integration test for npm tarball publish/install flow through Verdaccio.
- algorithmic_behavior: Installs Bun, Rust, Node, Verdaccio; builds native package; configures local registry; rewrites `workspace:*` deps to real versions in package manifests; publishes packages; installs `@oh-my-pi/pi-coding-agent`; verifies `omp --version`.
- inputs_outputs_state: Input is repository copy; state includes Verdaccio storage, rewritten temporary `package.json` files, and `/test/node_modules`; output is a built image layer that proves package installation works.
- gates_or_invariants: Publishes package list in dependency order, restores package manifests after each publish, and requires native build before publish.
- dependencies_and_callers: Used by install-tests/CI; depends on Debian, Bun, Rust nightly, Node 22, npm, Verdaccio, jq.
- edge_cases_or_failure_modes: Workspace version rewrite can miss new packages if list is stale; Verdaccio startup timing, native build failures, or `omp --version` failure break the image build.
- validation_or_tests: The Docker build itself is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-244 `directory` `packages/coding-agent/src/advisor`
- cursor: `[_]`
- core_role: Advisor side-channel runtime and `advise` tool.
- algorithmic_behavior: `AdviseTool` collects advisor notes and severity; delivery channel resolution chooses aside/steer/preserve based on severity and interrupt immunity; `AdvisorRuntime` buffers deltas and catches advisors up; `watchdog.ts` discovers watchdog instruction files.
- inputs_outputs_state: Inputs are advisor tool calls, severities, active turn state, session transcript deltas, and filesystem roots; outputs are advisor messages, telemetry, and delivered notes.
- gates_or_invariants: Read-only advisor tool names are whitelisted; interrupting severities are concern/blocker; interrupt-immune turns preserve notes instead of steering.
- dependencies_and_callers: Uses `AgentTool`, session runtime host, discovery paths, and advisor tests.
- edge_cases_or_failure_modes: Missing watchdog files, late advisor catchup, interrupt-immune tool turns, and malformed note batches are handled by channel selection/tests.
- validation_or_tests: `packages/coding-agent/src/advisor/__tests__/advisor.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-274 `directory` `packages/coding-agent/src/mnemopi`
- cursor: `[_]`
- core_role: Coding-agent memory backend adapter for `mnemopi`.
- algorithmic_behavior: Loads mnemopi lazily, computes memory bank scoping, wraps remember/recall/update/forget/invalidate operations across scoped banks, renders stats/diagnostics, resolves provider options, and maintains per-session state.
- inputs_outputs_state: Inputs are settings, agent dir, cwd, session messages, memory commands, bank config, and provider keys; outputs are memory blocks, diagnostics markdown, retained memory IDs, and DB files per bank.
- gates_or_invariants: Bank names are sanitized/truncated; scoped DB paths deduped; legacy banks can be extended; recall limits and importance values are clamped; state is attached to session via a symbol.
- dependencies_and_callers: Depends on `packages/mnemopi`, config settings, model registry/auth resolver, and memory backend interfaces.
- edge_cases_or_failure_modes: Missing optional mnemopi package, invalid bank names, stale DB files, provider resolution failure, and scoped/global fallback recall.
- validation_or_tests: Backed by mnemopi package tests plus coding-agent memory protocol/session behavior tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-304 `directory` `packages/coding-agent/test/internal-urls`
- cursor: `[_]`
- core_role: Regression tests for internal URL protocol routing and safety.
- algorithmic_behavior: Exercises `local://`, `memory://`, `history://`, `issue://`, `pr://`, `docs`, `mcp://`, `agent://`, `omp://`, and `vault://` handlers, including listing, resource reads, cache sharing, diff slicing, and editable resource marking.
- inputs_outputs_state: Inputs are fake sessions, temp dirs, protocol URLs, mock MCP managers, gh cache payloads, and vault CLI mocks; outputs are handler text/blob responses, MIME types, and editability metadata.
- gates_or_invariants: Blocks traversal/symlink escapes, validates URL shapes, preserves MCP query params, shares issue/PR cache, and distinguishes live versus parked/finalized agents.
- dependencies_and_callers: Uses `InternalUrlRouter`, GitHub cache/tool helpers, MCP manager shape, session refs, filesystem and vault protocol code.
- edge_cases_or_failure_modes: Invalid schemes, missing resources, stale issue cache fallback, unsupported templates, binary MCP blobs, bad diff indices, missing Obsidian binary, and disabled vault gate.
- validation_or_tests: This directory is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-334 `directory` `python/robomp/src/proxy`
- cursor: `[_]`
- core_role: FastAPI proxy for RoboMP workspace/GitHub operations.
- algorithmic_behavior: `server.py` validates JSON payloads, serializes domain objects, resolves tokens/HMAC keys, checks repository origin safety, maps GitHub/Git errors to JSON responses, and creates route handlers from settings; `__main__.py` loads settings and serves uvicorn.
- inputs_outputs_state: Inputs are HTTP requests, workspace/repo IDs, slot UID, review comments, settings env, git remotes, and auth tokens; outputs are JSON responses and error mappings.
- gates_or_invariants: Required fields are type-checked, slot UID must be int or null, string-list fields are validated, origin URL must match expected repo, HMAC key/token must resolve.
- dependencies_and_callers: Depends on FastAPI, robomp settings, GitHub client/errors, git command helpers, uvicorn entrypoint.
- edge_cases_or_failure_modes: Invalid field types, unsafe origin remotes, missing token/HMAC, GitHub API errors, head drift, and git command failures.
- validation_or_tests: Covered indirectly by `python/robomp/tests/test_worker.py` and proxy-specific tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-364 `file` `crates/pi-natives/src/lib.rs`
- cursor: `[_]`
- core_role: N-API native module root exporting Rust performance primitives.
- algorithmic_behavior: Declares native modules (`grep`, `glob`, `ast`, `text`, `highlight`, `tokens`, `pty`, etc.), installs a crash handler at module init, exposes a version sentinel, and on Windows installs a bounded Tokio runtime after load.
- inputs_outputs_state: Inputs are JS calls through N-API and host OS constraints; output is native function exports and runtime initialization side effects.
- gates_or_invariants: Version sentinel `__piNativesV16_0_9` must match JS loader expectation; Windows thread probing avoids panics under commit limits; module init must not spawn threads.
- dependencies_and_callers: Called by `packages/natives`; depends on napi-rs, Tokio, Rust native modules, and Windows-only custom runtime APIs.
- edge_cases_or_failure_modes: Mismatched `.node` version, Windows `os error 1455`, loader-lock deadlock, and crash diagnostics before native calls.
- validation_or_tests: Native package build/tests and loader checks validate sentinel/runtime behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-394 `file` `packages/agent/src/thinking.ts`
- cursor: `[_]`
- core_role: Defines canonical thinking-level enum-like constants for agent reasoning configuration.
- algorithmic_behavior: Exports `ThinkingLevel` values `low`, `medium`, `high`, `inherit`, `off`, and derived TypeScript types.
- inputs_outputs_state: Input is imported config/user selection; output is typed reasoning level passed through agent/model calls.
- gates_or_invariants: `ResolvedThinkingLevel` excludes `inherit`; callers must handle `off` and inheritance semantics.
- dependencies_and_callers: Used by agent compaction, model calls, coding-agent settings/extensions.
- edge_cases_or_failure_modes: Misinterpreting `inherit` as a concrete provider effort is prevented by type aliasing.
- validation_or_tests: Covered by `packages/agent/test/compaction-thinking-level.test.ts` and `packages/agent/test/agent.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-424 `file` `packages/ai/src/provider-details.ts`
- cursor: `[_]`
- core_role: Formats provider transport details for UI/debug display.
- algorithmic_behavior: `getProviderDetails` returns detail fields for model provider/base URL and OpenAI Codex transport reuse/websocket mode; helper functions format endpoints and booleans.
- inputs_outputs_state: Inputs are provider/model/transport context and optional session ID; output is `ProviderDetails` with labeled fields.
- gates_or_invariants: Omits empty/undefined fields; transport text is normalized via helper functions.
- dependencies_and_callers: Depends on model/provider types and OpenAI Codex transport details.
- edge_cases_or_failure_modes: Missing base URL, unset session ID, or unsupported transport details result in fewer fields rather than failure.
- validation_or_tests: Indirectly covered by provider/UI tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-454 `file` `packages/ai/test/apply-patch-freeform.test.ts`
- cursor: `[_]`
- core_role: Regression tests for freeform `apply_patch` tool conversion and streaming round-trip.
- algorithmic_behavior: Constructs OpenAI/Codex models and tools, validates grammar-based custom tool emission, tool choice mapping, stream receive of custom tool calls, dispatcher wire-name matching, and history replay.
- inputs_outputs_state: Inputs are mocked tools/models/SSE chunks/history messages; outputs are converted provider tool definitions and emitted tool-call events.
- gates_or_invariants: Freeform tools require grammar, preserve custom wire names, and round-trip custom tool call/output history without becoming JSON function tools.
- dependencies_and_callers: Uses AI conversion/stream code for OpenAI responses and Codex backend.
- edge_cases_or_failure_modes: Union tool schemas, strict versus non-strict tools, compact grammar literals, dispatcher naming mismatch, and custom call replay.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-484 `file` `packages/ai/test/auth-storage-sqlite-busy.test.ts`
- cursor: `[_]`
- core_role: Regression tests for SQLite busy error classification and auth credential store open behavior.
- algorithmic_behavior: Synthesizes busy-shaped errors and asserts `isSqliteBusyError`; tests `SqliteAuthCredentialStore.open` handling when SQLite reports busy/locked states.
- inputs_outputs_state: Inputs are error code/errno combinations and temp store open attempts; outputs are boolean classification or surfaced errors.
- gates_or_invariants: Only real busy/locked SQLite codes should follow the busy path; unrelated errors should not be masked.
- dependencies_and_callers: Auth storage SQLite implementation.
- edge_cases_or_failure_modes: Different SQLite busy code shapes and errno values.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-514 `file` `packages/ai/test/google-empty-response-retry.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Google/Vertex/Cloud Code Assist empty-response retry behavior.
- algorithmic_behavior: Builds mocked SSE responses and drains streams to assert retry on empty terminal responses and normal completion when text chunks arrive.
- inputs_outputs_state: Inputs are mocked GenAI/Vertex/CCA chunks and model contexts; outputs are assistant message events and final text.
- gates_or_invariants: Empty response retry applies to public/Vertex and CCA paths without duplicating successful content.
- dependencies_and_callers: Google provider streaming implementations.
- edge_cases_or_failure_modes: Empty terminal frames, multi-chunk streams, and CCA response shape variants.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-544 `file` `packages/ai/test/issue-826-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for Anthropic strict-tools opt-out through Vertex-style proxies.
- algorithmic_behavior: Captures provider parameters for an Anthropic model/tool context and verifies strict tool settings are omitted when proxy compatibility requires it.
- inputs_outputs_state: Inputs are model specs, bash tool schema, and abort signal; output is captured request params.
- gates_or_invariants: Vertex-style proxy compatibility must not send unsupported strict-tool flags.
- dependencies_and_callers: Anthropic provider request conversion.
- edge_cases_or_failure_modes: Aborted signal helper and proxy model metadata.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-574 `file` `packages/ai/test/openai-auth-header-precedence.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI-compatible auth header precedence.
- algorithmic_behavior: Mock fetch captures `Authorization` headers for responses calls with request API key versus model/default keys.
- inputs_outputs_state: Inputs are API keys, model config, and mock fetch; outputs are captured headers.
- gates_or_invariants: Explicit request API key should take precedence; auth should not be duplicated or overwritten unexpectedly.
- dependencies_and_callers: OpenAI responses provider auth handling.
- edge_cases_or_failure_modes: Calls with and without per-request key.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-604 `file` `packages/ai/test/openai-stream-terminal-close.test.ts`
- cursor: `[_]`
- core_role: Regression tests for terminal SSE frames without connection close.
- algorithmic_behavior: Creates never-closing and chunked SSE responses, verifies terminal frames cause stream completion without waiting for TCP close.
- inputs_outputs_state: Inputs are mocked SSE chunks for completions/responses; outputs are assistant stream results.
- gates_or_invariants: A terminal provider frame is sufficient to close logical stream.
- dependencies_and_callers: OpenAI completions and responses streaming parsers.
- edge_cases_or_failure_modes: Never-closing response bodies and split chunks.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-634 `file` `packages/ai/test/stream.test.ts`
- cursor: `[_]`
- core_role: Broad end-to-end streaming test harness for AI providers.
- algorithmic_behavior: Defines reusable flows for basic text, tool calls, streaming, thinking, image input, and multi-turn interactions across available models/providers.
- inputs_outputs_state: Inputs include real or configured credentials, provider models, calculator tool, and contexts; outputs are message events, usage, tool calls/results, and final assistant messages.
- gates_or_invariants: Provider streams must emit coherent events, validate tool args, support multi-turn state, and handle optional credential availability.
- dependencies_and_callers: Many provider registries, OAuth tokens, bundled model catalog, and AI stream API.
- edge_cases_or_failure_modes: Missing Bedrock/other credentials, provider-specific image/thinking behavior, and tool-call streaming differences.
- validation_or_tests: This file is validation, some cases are credential-gated.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-664 `file` `packages/catalog/src/model-thinking.ts`
- cursor: `[_]`
- core_role: Catalog reasoning/thinking policy inference and effort mapping.
- algorithmic_behavior: Derives `ThinkingConfig`, supported efforts, effort maps, control modes, mandatory reasoning, wire model IDs, and clamped/minimum efforts from model specs, providers, compat metadata, and parsed model identity.
- inputs_outputs_state: Inputs are `ModelSpec`/`Model`, `Api`, compat descriptors, model IDs, and requested `Effort`; outputs are supported effort arrays, wire reasoning fields, model ID overrides, and validation errors.
- gates_or_invariants: Filters effort maps to supported efforts, enforces provider-specific effort sets, maps Google/Anthropic adaptive effort values, and throws on unsupported requested effort.
- dependencies_and_callers: Imports catalog identity/classification, model types, provider compat descriptors; used by model resolver/provider request code.
- edge_cases_or_failure_modes: OpenAI o-series mandatory reasoning, Gemini 3 effort splits, Anthropic xhigh availability, DeepSeek/Groq/Fireworks/Z.ai/Ollama mappings, OpenRouter adaptive models, and omitted wire effort.
- validation_or_tests: Catalog resolver tests, including issue repros and generated model policies.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-694 `file` `packages/catalog/test/issue-887-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for opencode-go model resolver routing.
- algorithmic_behavior: Verifies 404-prone opencode-go IDs route to OpenAI completions for a specific base URL.
- inputs_outputs_state: Inputs are provider/base URL/model IDs; output is resolved API type.
- gates_or_invariants: Known opencode-go base URL requires compatibility override.
- dependencies_and_callers: Catalog provider-model resolver.
- edge_cases_or_failure_modes: Provider IDs that otherwise default to wrong API route.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-724 `file` `packages/coding-agent/scripts/omp.ts`
- cursor: `[_]`
- core_role: Bun preload shim for the development launcher.
- algorithmic_behavior: Reads `OMP_LAUNCH_CWD`, deletes it, and changes process cwd back before entrypoint imports snapshot project paths.
- inputs_outputs_state: Input is env var `OMP_LAUNCH_CWD`; output is process cwd side effect.
- gates_or_invariants: Swallows `chdir` failure so launcher still proceeds; removes env var to avoid leaking state.
- dependencies_and_callers: Used by `scripts/omp` dev launcher.
- edge_cases_or_failure_modes: Missing/invalid cwd, foreign project `bunfig.toml` preload issues.
- validation_or_tests: No direct test found; behavior documented in file header.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-754 `file` `packages/coding-agent/test/agent-session-bash-detach.test.ts`
- cursor: `[_]`
- core_role: End-to-end test that BashTool child processes run in their own session.
- algorithmic_behavior: Mock agent triggers bash calls, compares Python-reported session IDs/PIDs, and verifies detached/background handling through `AgentSession`.
- inputs_outputs_state: Inputs are mock model responses and bash commands; outputs are tool result text and process session IDs.
- gates_or_invariants: Bash children should not inherit host session in a way that breaks detachment/signal handling.
- dependencies_and_callers: AgentSession, BashTool, Python probe availability.
- edge_cases_or_failure_modes: Python unavailable, OS process session semantics, background task detachment.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-784 `file` `packages/coding-agent/test/agent-session-ssh-refresh.test.ts`
- cursor: `[_]`
- core_role: Tests AgentSession SSH tool refresh behavior.
- algorithmic_behavior: Creates a model/session and asserts SSH-related tools refresh when session state changes.
- inputs_outputs_state: Inputs are model/session settings; outputs are active tool lists or refreshed tool behavior.
- gates_or_invariants: SSH tool availability must track session connection state.
- dependencies_and_callers: AgentSession tool registry and SSH tool setup.
- edge_cases_or_failure_modes: Stale tools after session refresh.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-814 `file` `packages/coding-agent/test/bash-failure-result.test.ts`
- cursor: `[_]`
- core_role: Test for non-zero bash result propagation.
- algorithmic_behavior: Builds a `ToolSession`, runs a failing bash command, and checks result/error shape.
- inputs_outputs_state: Input is command string; output is tool result with failure metadata/text.
- gates_or_invariants: Non-zero exit must surface as a tool result error rather than disappearing.
- dependencies_and_callers: BashTool execution path.
- edge_cases_or_failure_modes: Exit code formatting and stderr/stdout capture.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-844 `file` `packages/coding-agent/test/edit-diff.test.ts`
- cursor: `[_]`
- core_role: Tests edit matching and diff generation.
- algorithmic_behavior: Exercises `findMatch`, indentation adjustment, hashline diff, and `computeEditDiff` behavior.
- inputs_outputs_state: Inputs are old/new text snippets and edit patterns; outputs are match spans and diff text/details.
- gates_or_invariants: Indentation is adjusted consistently; diff output should reflect intended edits without false matches.
- dependencies_and_callers: Coding-agent edit renderer/hashline utilities.
- edge_cases_or_failure_modes: Ambiguous matches, whitespace/indent differences, multi-line diffs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-874 `file` `packages/coding-agent/test/history-storage-search.test.ts`
- cursor: `[_]`
- core_role: Tests prompt history search storage.
- algorithmic_behavior: Seeds fresh history storage and asserts search results over prompts.
- inputs_outputs_state: Inputs are prompt strings; outputs are search result entries.
- gates_or_invariants: Storage is isolated per test and cleaned after.
- dependencies_and_callers: `HistoryStorage`.
- edge_cases_or_failure_modes: Empty search, ordering, duplicate/substring behavior.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-904 `file` `packages/coding-agent/test/interactive-mode-prompt-template-autocomplete.test.ts`
- cursor: `[_]`
- core_role: Regression tests for prompt-template autocomplete in interactive mode.
- algorithmic_behavior: Creates tools and interactive mode harness, then asserts autocomplete suggestions/behavior for prompt templates.
- inputs_outputs_state: Inputs are fake tools and editor text; outputs are autocomplete items.
- gates_or_invariants: Template autocomplete should not collide with tool autocomplete and should honor issue behavior noted by file name.
- dependencies_and_callers: InteractiveMode prompt/template autocomplete code.
- edge_cases_or_failure_modes: Prefix matching, disabled/unavailable tools, template syntax.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-934 `file` `packages/coding-agent/test/issue-973-legacy-pi-plugin.test.ts`
- cursor: `[_]`
- core_role: Regression test for legacy Pi plugin imports.
- algorithmic_behavior: Resolves current package paths and tests legacy specifier compatibility for plugin imports.
- inputs_outputs_state: Inputs are package resolution paths; output is successful import/compat assertions.
- gates_or_invariants: Legacy plugin specifiers must map to current coding-agent/extensibility modules.
- dependencies_and_callers: Plugin compatibility loader/shim.
- edge_cases_or_failure_modes: Package export map drift.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-964 `file` `packages/coding-agent/test/mcp-reconnect-storm.test.ts`
- cursor: `[_]`
- core_role: Regression test for MCP reconnect storm control.
- algorithmic_behavior: Uses a crash-after-init MCP fixture and Bun executable to assert reconnect behavior is bounded.
- inputs_outputs_state: Inputs are fixture path and MCP config; outputs are connection/reconnect events or counts.
- gates_or_invariants: A crashing MCP server must not cause unbounded reconnect storms.
- dependencies_and_callers: MCP manager/startup logic.
- edge_cases_or_failure_modes: Fast crash after initialization, repeated reconnect loop.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-994 `file` `packages/coding-agent/test/otel-export-probe.ts`
- cursor: `[_]`
- core_role: Small executable probe for OTEL export behavior.
- algorithmic_behavior: Starts a Bun HTTP server, creates an OTEL span, and likely validates export payload receipt.
- inputs_outputs_state: Inputs are OTEL env/config; outputs are HTTP-received spans and process exit status.
- gates_or_invariants: Span named `agent.llm_call` is emitted through configured exporter.
- dependencies_and_callers: OpenTelemetry API/SDK and CI probe runner.
- edge_cases_or_failure_modes: Exporter unreachable, server port/listen failure, missing flush.
- validation_or_tests: Probe itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1024 `file` `packages/coding-agent/test/rpc-host-uris.test.ts`
- cursor: `[_]`
- core_role: Tests RPC host URI bridge behavior.
- algorithmic_behavior: Registers host URI bridge with `InternalUrlRouter`, records emitted requests, and verifies response/cancel/error handling.
- inputs_outputs_state: Inputs are internal URL reads and mocked host responses; outputs are router results and JSON-RPC request records.
- gates_or_invariants: Host URI bridge must correlate responses and clean up pending requests.
- dependencies_and_callers: RPC mode host URI bridge and internal URL router.
- edge_cases_or_failure_modes: Missing responses, cancellation, duplicate handlers, malformed results.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1054 `file` `packages/coding-agent/test/session-persistence-images.test.ts`
- cursor: `[_]`
- core_role: Tests persistence of image content in session messages.
- algorithmic_behavior: Builds tool-result session entries containing text/image payloads and verifies serialization/storage preserves image content.
- inputs_outputs_state: Inputs are text/image content and session entries; outputs are persisted/reloaded message entries.
- gates_or_invariants: Image blocks keep `data` and `mimeType`; tool result entries retain content shape.
- dependencies_and_callers: Session storage/persistence format.
- edge_cases_or_failure_modes: Alternate image payload shape and mixed text/image content.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1084 `file` `packages/coding-agent/test/streaming-output.test.ts`
- cursor: `[_]`
- core_role: Tests output truncation and streaming sink buffering.
- algorithmic_behavior: Exercises byte/head/tail/middle truncation, line truncation, `TailBuffer`, `OutputSink`, truncation notices, head-retain mode, and per-line column caps.
- inputs_outputs_state: Inputs are strings, byte limits, temp dirs, image protocol env, and sink writes; outputs are retained text, artifact paths, notices, and preview content.
- gates_or_invariants: UTF-8 truncation must stay valid; notices must reflect omitted bytes/lines; cleanup restores env and temp dirs.
- dependencies_and_callers: Bash/eval streaming output render utilities.
- edge_cases_or_failure_modes: Multibyte boundaries, huge output, per-line caps, head-retain behavior, file artifact fallback.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1114 `file` `packages/coding-agent/test/truncate-to-width.test.ts`
- cursor: `[_]`
- core_role: Tests terminal-width truncation utility.
- algorithmic_behavior: Validates `truncateToWidth` on ANSI/wide/normal text cases.
- inputs_outputs_state: Inputs are strings and width limits; outputs are truncated strings.
- gates_or_invariants: Visible width, ANSI preservation, and ellipsis behavior must be consistent.
- dependencies_and_callers: TUI render sanitization utilities.
- edge_cases_or_failure_modes: Wide Unicode, ANSI sequences, zero/small width.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1144 `file` `packages/hashline/src/block.ts`
- cursor: `[_]`
- core_role: Resolves deferred structural block edits into concrete line edits.
- algorithmic_behavior: `hasBlockEdit` detects block edits; `resolveBlockEdits` calls an injected `BlockResolver` to map anchor lines to block spans, then emits insert/delete edits for replace/delete/insert-after-block operations.
- inputs_outputs_state: Inputs are parsed edits, file text, file path, resolver, and options; output is an edit list with no `block` variants plus optional warnings/resolution callbacks.
- gates_or_invariants: Unresolved replace/delete throws by default; preview mode can drop unresolved edits; single-line block spans are rejected; insert-after-block lowers to plain insert-after with warnings when unresolved.
- dependencies_and_callers: Depends on hashline types/messages and `STRUCTURAL_CLOSER_RE`; called by apply/preview boundaries.
- edge_cases_or_failure_modes: Missing resolver, unsupported language, blank/unparsable anchor, structural closer anchor, and single-line statement mistaken for a block.
- validation_or_tests: Covered by hashline/edit tests and callers such as coding-agent edit-diff tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1174 `file` `packages/mnemopi/src/diagnose.ts`
- cursor: `[_]`
- core_role: Mnemopi database diagnostics and integrity summary.
- algorithmic_behavior: Checks required tables/columns, SQLite integrity, row counts, env status, and emits diagnostic entries with pass/fail status.
- inputs_outputs_state: Inputs are DB path/options and environment; outputs are `DiagnosticSummary` with entries and counts.
- gates_or_invariants: Required tables/columns are enumerated; `passStatus`/`failStatus` derive summary state; safe count/integrity catches DB errors.
- dependencies_and_callers: Bun SQLite database and coding-agent mnemopi backend stats/diagnostics.
- edge_cases_or_failure_modes: Missing DB, missing tables/columns, integrity errors, count failures, absent env vars.
- validation_or_tests: Mnemopi diagnostics tests where present; used by backend status rendering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1204 `file` `packages/mnemopi/test/entities.test.ts`
- cursor: `[_]`
- core_role: Tests entity extraction and matching utilities.
- algorithmic_behavior: Validates edit distance, entity scoring, extraction of names/phrases/mentions/hashtags, stop-word filtering, oversized transcript skip, and similar entity sorting.
- inputs_outputs_state: Inputs are text snippets and entity lists; outputs are extracted/scored entities.
- gates_or_invariants: Lowercase prose, pure numbers, contaminated stop-word phrases, and substring duplicates are filtered.
- dependencies_and_callers: Mnemopi entity extraction module.
- edge_cases_or_failure_modes: Unicode edit distance, oversized raw transcripts, case-insensitive prefixes.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1234 `file` `packages/mnemopi/test/setup.ts`
- cursor: `[_]`
- core_role: Shared mnemopi test reset harness.
- algorithmic_behavior: Defines resettable module list and calls available reset functions before/after tests.
- inputs_outputs_state: Inputs are module exports; output is cleaned global/module state.
- gates_or_invariants: Resets memory, beam, LLM backend, and embeddings state to keep full suite safe.
- dependencies_and_callers: Mnemopi test runner setup.
- edge_cases_or_failure_modes: Missing reset functions are skipped by name checks.
- validation_or_tests: Enables validation across mnemopi tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1264 `file` `packages/snapcompact/research/bench_kimi.py`
- cursor: `[_]`
- core_role: Research benchmark for Kimi/Fireworks completion over planned chunks.
- algorithmic_behavior: Calls Fireworks completion API, plans input chunks, and benchmarks/saves response metadata.
- inputs_outputs_state: Inputs are messages, max tokens, API config/env, and chunk plan; outputs are response text, usage/metadata, and printed benchmark results.
- gates_or_invariants: Requires external credentials/network; chunk plan partitions data deterministically.
- dependencies_and_callers: Python research stack and Fireworks API.
- edge_cases_or_failure_modes: API failures, missing credentials, token limits.
- validation_or_tests: Research script; no automated unit test.
- skip_candidate: `yes: research experiment script, not production runtime.`

### OH_MY_HUMANIZE_MAIN-HZ-1294 `file` `packages/snapcompact/research/exp22_ttf6pt.py`
- cursor: `[_]`
- core_role: Research experiment rendering text into tiny TTF images and evaluating QA.
- algorithmic_behavior: Loads mono fonts, renders text images, caches payloads, asks QA units, aggregates records, and writes image artifacts atomically.
- inputs_outputs_state: Inputs are text/font sizes/questions/cache freshness; outputs are PNGs and aggregate result records.
- gates_or_invariants: Atomic saves avoid partial PNGs; cache keys memoize expensive calls.
- dependencies_and_callers: PIL/Pillow, local research data, external QA model path if configured.
- edge_cases_or_failure_modes: Missing font, image rendering errors, stale cache, QA call failures.
- validation_or_tests: Research script; no automated unit test.
- skip_candidate: `yes: research experiment, not product runtime.`

### OH_MY_HUMANIZE_MAIN-HZ-1324 `file` `packages/snapcompact/research/snapcompact_r2_metro.py`
- cursor: `[_]`
- core_role: Research plotting/analysis script for snapcompact R2 metro data.
- algorithmic_behavior: Loads benchmark data, smooths series with Catmull-Rom interpolation, formats values, and produces analysis/visualization outputs.
- inputs_outputs_state: Inputs are research data files; outputs are plotted/printed metrics.
- gates_or_invariants: Formatting and interpolation are deterministic over loaded data.
- dependencies_and_callers: Python plotting/data stack.
- edge_cases_or_failure_modes: Missing data files or malformed numeric values.
- validation_or_tests: Research script; no automated unit test.
- skip_candidate: `yes: research-only artifact.`

### OH_MY_HUMANIZE_MAIN-HZ-1354 `file` `packages/stats/src/user-metrics.ts`
- cursor: `[_]`
- core_role: Computes behavioral metrics from user prompt text for stats dashboard.
- algorithmic_behavior: Strips structured/code/XML/URL content, counts profanity, yelling, drama punctuation, anguish/blame/negation/repetition signals, lines, words, images, and derives message metrics.
- inputs_outputs_state: Input is raw user text; output is `UserMessageMetrics` or `EMPTY_USER_METRICS`.
- gates_or_invariants: Structured content is removed before prose metrics; regexes are global but counted safely; yelling requires minimum letters and uppercase ratio.
- dependencies_and_callers: Used by stats parser when extracting user message stats.
- edge_cases_or_failure_modes: ANSI escapes, image markers, quote lines, inline/fenced code, XML tags, URLs, file mentions, multiline prompts.
- validation_or_tests: `packages/stats/test/user-metrics.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1384 `file` `packages/tui/src/terminal-capabilities.ts`
- cursor: `[_]`
- core_role: Terminal capability detection, image protocol encoding, and notification formatting.
- algorithmic_behavior: Detects terminal ID/protocol support, synchronized output, hyperlinks, DECCARA, Kitty/iTerm2/Sixel image rendering, image dimensions, rows/fit, and OSC 99/9/bell notifications.
- inputs_outputs_state: Inputs are environment vars, terminal ID, image base64/MIME/dimensions, notification payloads; outputs are escape sequences, fallback strings, mutable `TERMINAL` state, and capability objects.
- gates_or_invariants: Image protocol can be forced; OSC99 payload bytes are capped/chunked; unsupported images fall back to text; hyperlink/synchronized output respect user overrides and multiplexer constraints.
- dependencies_and_callers: Uses `@oh-my-pi/pi-natives` for Sixel and kitty graphics helpers; TUI render components call it.
- edge_cases_or_failure_modes: Windows Terminal preview sixel support, tmux versions, invalid PNG/JPEG/GIF/WebP dimensions, unsafe OSC payload controls, headless/test runtime.
- validation_or_tests: TUI tests including hyperlink and resize behavior cover adjacent capability handling.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1414 `file` `packages/tui/test/issue-879-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for legacy Alt+Shift+letter key parsing.
- algorithmic_behavior: Asserts `matchesKey` and `parseKey` treat ESC+uppercase as `alt+shift+letter` in legacy mode.
- inputs_outputs_state: Inputs are terminal escape sequences; outputs are parsed key IDs/match booleans.
- gates_or_invariants: Legacy mode must preserve old Alt+Shift semantics.
- dependencies_and_callers: TUI key parser.
- edge_cases_or_failure_modes: ESC uppercase ambiguity.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1444 `file` `packages/tui/test/resize-viewport-defer.test.ts`
- cursor: `[_]`
- core_role: Tests resize rendering fast paths and deferred full rewrap.
- algorithmic_behavior: Simulates virtual terminal resize bursts, captures writes, and asserts viewport-only painting during drag, full history replay after settle, alternate-screen/in-place behavior, and env override handling.
- inputs_outputs_state: Inputs are env patches, virtual terminal dimensions, resize events; outputs are terminal write sequences and visible viewport lines.
- gates_or_invariants: Avoids relayout of off-screen history during drag; no pending settle paint after stop; Warp-specific path avoids alt screen/ED3 unless override says otherwise.
- dependencies_and_callers: TUI virtual terminal/render loop.
- edge_cases_or_failure_modes: Terminals re-reporting size on alt-screen toggle, resize burst cancellation, override env vars.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1474 `file` `packages/typescript-edit-benchmark/src/report.ts`
- cursor: `[_]`
- core_role: Generates markdown and JSON reports for TypeScript edit benchmark results.
- algorithmic_behavior: Formats task/run status, rates, errors, edit args, files, category/mutation/difficulty summaries, and score tables.
- inputs_outputs_state: Inputs are `BenchmarkResult` and `TaskResult` structures; outputs are markdown report text and JSON report object/string.
- gates_or_invariants: Markdown escaping, ghost completion detection, failure category grouping, and sorted summaries keep reports parseable.
- dependencies_and_callers: Benchmark runner result types and `@oh-my-pi/pi-utils` formatters.
- edge_cases_or_failure_modes: Missing fields, unknown tool errors, empty task groups, difficulty score formatting.
- validation_or_tests: No direct test found; report is benchmark artifact generation.
- skip_candidate: `yes: benchmark reporting, not product runtime, but it encodes evaluation aggregation logic.`

### OH_MY_HUMANIZE_MAIN-HZ-1504 `file` `packages/utils/src/ptree.ts`
- cursor: `[_]`
- core_role: Process tree spawning/execution utility with timeout/abort handling.
- algorithmic_behavior: Wraps `Bun.spawn` child process, tracks stdout/stderr, waits with abort/timeout, kills process trees, and exposes `spawn`, `exec`, and signal-combining helpers.
- inputs_outputs_state: Inputs are command arrays, cwd/env/stdin/stderr options, timeout and abort signals; outputs are `ExecResult` or typed errors.
- gates_or_invariants: Non-zero exits throw `NonZeroExitError`; aborts/timeouts have distinct error classes; signal combination propagates earliest abort.
- dependencies_and_callers: Bun subprocess API and callers needing robust process lifecycle.
- edge_cases_or_failure_modes: Process already exited, aborted wait, timeout kill, stream read failures, non-zero exit.
- validation_or_tests: Indirectly covered by process/tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1534 `file` `packages/utils/test/sanitize-text.test.ts`
- cursor: `[_]`
- core_role: Tests text sanitization utility.
- algorithmic_behavior: Asserts ANSI/OSC/DCS/control stripping, surrogate handling, replacement character policy, and CR normalization.
- inputs_outputs_state: Inputs are malformed/control-containing strings; outputs are sanitized strings.
- gates_or_invariants: Tabs and LF are preserved while unsafe controls are removed; original string instance returns when unchanged.
- dependencies_and_callers: `sanitizeText` used by TUI/tool rendering.
- edge_cases_or_failure_modes: Lone surrogates, malformed replacement chars, OSC BEL/ST termination, ESC final bytes, DEL.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1564 `file` `python/robomp/src/pragmas.py`
- cursor: `[_]`
- core_role: Parses RoboMP message pragma directives and resolves model/thinking aliases.
- algorithmic_behavior: `_parse_command_line` parses leading slash pragma tokens; `parse_pragmas` separates body from directives; helpers resolve pragma values, model aliases, and thinking levels.
- inputs_outputs_state: Input is message body text and model pool; output is cleaned body plus ordered pragma tuples and resolved aliases.
- gates_or_invariants: Command keys are lowercase/digit/dash/underscore and must start with a letter; malformed pragma line returns no parse; thinking aliases are normalized by lowercasing/removing whitespace.
- dependencies_and_callers: RoboMP worker/task runner.
- edge_cases_or_failure_modes: Invalid directive syntax, duplicate pragmas, unknown model aliases, unknown thinking values.
- validation_or_tests: Covered by `python/robomp/tests/test_worker.py`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1594 `file` `python/robomp/tests/test_worker.py`
- cursor: `[_]`
- core_role: Tests RoboMP worker RPC lifecycle, environment staging, reminders, cancellation, and native-cache capture.
- algorithmic_behavior: Uses async tests to assert task directives, resume/continue handling, staged agent home and XDG dirs, slot UID/env, hard timeout, cancellation hooks, PR-review reminders, dirty-state reminders, and native cache capture.
- inputs_outputs_state: Inputs are temp settings, mocked RPC clients, workspace dirs, timers, and git/native cache mocks; outputs are command args, env maps, reminder calls, statuses, and captured cache records.
- gates_or_invariants: Fresh triage seeds todos, resumed triage skips set-todos, hard timeout stops client, reminder budgets cap repeats, cache capture swallows non-critical failures.
- dependencies_and_callers: RoboMP worker module, settings fixtures, pytest async.
- edge_cases_or_failure_modes: Empty session JSONL, absent agent home, dirty worktree, PR classification quit early, timeout race, cache key/capture failures.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1624 `directory` `packages/coding-agent/src/extensibility/extensions`
- cursor: `[_]`
- core_role: Extension loading, API surface, event runner, model query, command/tool wrapping, and compact/model handlers.
- algorithmic_behavior: Loader discovers extension entries/manifests, loads factories, creates `ExtensionRuntime`; runner emits lifecycle/tool/message/credential events with timeouts; wrapper adapts registered extension tools; model API resolves models; command handler merges slash/custom/skill commands.
- inputs_outputs_state: Inputs are extension paths/manifests, session/settings/model registry, event bus, commands/tools, and extension UI requests; outputs are loaded extension records, registered handlers/tools, event results, and extension errors.
- gates_or_invariants: Extension handler timeout defaults to 30s; session shutdown timeout 2s; manifest paths must resolve inside extension root; legacy Pi specifier shim is installed for compatibility.
- dependencies_and_callers: Uses discovery capabilities, plugin loader, event bus, settings, session manager, `@oh-my-pi/pi-ai`, TUI types, TypeBox/Zod/ArkType.
- edge_cases_or_failure_modes: Missing/invalid package manifests, EACCES/ENOENT, handler timeout, shadowed/disabled extensions, legacy module import failures, unsafe manifest subpaths.
- validation_or_tests: Covered by plugin/extension discovery tests and issue-973 legacy plugin test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1654 `directory` `packages/mnemopi/src/core/beam`
- cursor: `[_]`
- core_role: Beam memory core: schema, storage, embedding/vector helpers, recall, episodic consolidation, and memory state class.
- algorithmic_behavior: `schema.ts` initializes tables/columns; `store.ts` remembers/updates/forgets working memories and schedules embeddings/fact extraction; `helpers.ts` handles FTS/vector search, metadata, scoring helpers; `recall.ts` combines FTS/vector/lexical/temporal/MMR ranking; `consolidate.ts` degrades/sleeps working memories into episodic/fact/timeline/KG tiers; `index.ts` wires `BeamMemory`.
- inputs_outputs_state: Inputs are content, metadata, scopes, timestamps, embeddings, query text/options, and DB state; outputs are memory IDs, recall results/context text, stats, exported/imported state, and event rows.
- gates_or_invariants: Importance/veracity/trust tier normalization, scratchpad caps, embedding model reconciliation, visibility filters, recency half-life, vector availability fallback, contaminated veracity handling, tier aging thresholds.
- dependencies_and_callers: Bun SQLite, mnemopi embeddings, extraction, episodic graph, annotations, migrations, vector index, config/env.
- edge_cases_or_failure_modes: Missing vector extension, disabled embeddings, duplicate memories, CJK/no-space FTS, stale embedding model, oversized episode consolidation, DB schema migration needs.
- validation_or_tests: Mnemopi package tests and integration consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1684 `file` `packages/agent/src/utils/yield.ts`
- cursor: `[_]`
- core_role: Cooperative event-loop yield and keepalive utilities for Bun.
- algorithmic_behavior: `EventLoopKeepalive` installs an unref interval; `yieldIfDue` sleeps at most every 50ms; `ExponentialYield` backs off sleeps and races them against work promises while cancelling loser timers.
- inputs_outputs_state: Inputs are optional abort signals and racer promises; outputs are delayed scheduling, returned racer values, and mutable backoff state.
- gates_or_invariants: `sleepAtLeast` retries premature wakeups; abort returns silently; activity resets backoff to minimum.
- dependencies_and_callers: Uses `node:timers/promises` scheduler; agent loop and bash executor hot paths.
- edge_cases_or_failure_modes: Bun busy-wait on unresolved promises, abort during sleep, N-API callbacks waking early, stray timers.
- validation_or_tests: `packages/agent/test/yield.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1714 `file` `packages/ai/src/dialect/minimax.ts`
- cursor: `[_]`
- core_role: Minimax dialect renderer/scanner definition for in-band tool calling.
- algorithmic_behavior: Renders tool calls as `<minimax:tool_call><invoke...>`, tool results as XML-like result/error blocks, thinking as delimited text, and transcripts through legacy text renderer; scanner config extends Anthropic in-band prefixes.
- inputs_outputs_state: Inputs are messages, tool calls, tool results, and tool schemas; outputs are prompt/transcript text and scanner instances.
- gates_or_invariants: XML attributes/text are escaped; string arguments preserve raw strings only when schema says string; all other args JSON-stringify.
- dependencies_and_callers: Anthropic in-band scanner/rendering helpers and Minimax prompt markdown.
- edge_cases_or_failure_modes: Wrapper tag detection, parameter escaping, string-vs-JSON argument shape.
- validation_or_tests: Covered by prompt-tools-loop dialect tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1744 `file` `packages/ai/src/providers/mock.ts`
- cursor: `[_]`
- core_role: Mock AI provider implementation for tests.
- algorithmic_behavior: `MockModel` stores handler source/state; `streamMock` registers mock API and runs handlers to emit text/thinking/tool/error/usage events, including sleeps and terminal errors.
- inputs_outputs_state: Inputs are iterable/async handler responses and model options; outputs are `AssistantMessageEvent` streams and usage/cost.
- gates_or_invariants: Pulls one handler per call, normalizes content types, generates tool call IDs, merges usage with zero-cost default, honors abort signals.
- dependencies_and_callers: AI provider registry and test suites across agent/coding-agent.
- edge_cases_or_failure_modes: Exhausted handler source, async handlers, delayed responses, abort during sleep, terminal provider errors.
- validation_or_tests: Heavily exercised by AI/agent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1774 `file` `packages/ai/src/registry/deepseek.ts`
- cursor: `[_]`
- core_role: DeepSeek provider login/descriptor.
- algorithmic_behavior: Creates API-key login, normalizes raw keys, and exports provider descriptor with login function.
- inputs_outputs_state: Inputs are raw API key/controller; output is normalized credential string/provider object.
- gates_or_invariants: API key normalization strips expected prefixes/formatting as implemented.
- dependencies_and_callers: OAuth/API key registry.
- edge_cases_or_failure_modes: Empty/malformed raw key.
- validation_or_tests: Indirect provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1804 `file` `packages/ai/src/registry/opencode-go.ts`
- cursor: `[_]`
- core_role: Minimal opencode-go provider descriptor.
- algorithmic_behavior: Exports provider metadata for registry use.
- inputs_outputs_state: Input is registry import; output is provider descriptor.
- gates_or_invariants: Descriptor shape must match registry expectations.
- dependencies_and_callers: Catalog/provider registry.
- edge_cases_or_failure_modes: Misconfigured descriptor causes resolver issues, covered by issue-887 test.
- validation_or_tests: `packages/catalog/test/issue-887-repro.test.ts`.
- skip_candidate: `yes: tiny descriptor, low algorithmic content.`

### OH_MY_HUMANIZE_MAIN-HZ-1834 `file` `packages/ai/src/usage/google-antigravity.ts`
- cursor: `[_]`
- core_role: Google Antigravity usage/quota provider and credential ranking strategy.
- algorithmic_behavior: Fetches available models/quota info, parses quota windows/amounts/status, scopes limits to model counters, and ranks credentials by relevant remaining limits.
- inputs_outputs_state: Inputs are usage fetch params, access token/API endpoint, credential ranking context; outputs are `UsageReport`, `UsageLimit` ranking, and provider metadata.
- gates_or_invariants: Remaining fractions are clamped; endpoint/path constants fixed; access token resolves from params; one-day window logic for counter keys.
- dependencies_and_callers: AI usage provider framework, credential ranking.
- edge_cases_or_failure_modes: Missing access token, HTTP errors, absent quota info, malformed fractions/windows, model-specific counter mismatch.
- validation_or_tests: Indirect usage/ranking tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1864 `file` `packages/ai/src/utils/validation.ts`
- cursor: `[_]`
- core_role: Single entrypoint for tool-call argument validation and conservative coercion.
- algorithmic_behavior: Builds cached validation contexts from Zod/ArkType/JSON Schema, normalizes optional nulls, validates, flattens issues, coerces schema-directed type drift, drops unrecognized keys, retries up to five passes, and throws formatted errors on failure.
- inputs_outputs_state: Inputs are tool definitions and `ToolCall.arguments`; output is parsed/coerced argument object with unknown root fields preserved.
- gates_or_invariants: Schema remains source of truth; `MAX_COERCION_PASSES` is 5; JSON healing is bounded; pointer operations address nested fields; no invented values.
- dependencies_and_callers: ArkType, Zod v4, JSON Schema validator, schema conversion/stamps; called before agent tool dispatch.
- edge_cases_or_failure_modes: Numeric/boolean/string drift, JSON-stringified arrays/objects, malformed JSON containers, optional nulls, union branches, unknown keys, nested encoded JSON depth cap.
- validation_or_tests: AI tool validation tests, apply-patch freeform tests, and agent tool-call tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1894 `file` `packages/catalog/src/provider-models/special.ts`
- cursor: `[_]`
- core_role: Special model-manager option factories for providers with custom discovery/management.
- algorithmic_behavior: Builds OpenAI Codex, Cursor, and Z.ai model manager options, including lazy discovery imports and config passthrough.
- inputs_outputs_state: Inputs are provider-specific config objects; outputs are `ModelManagerOptions`.
- gates_or_invariants: Lazy discovery is wrapped with `once` to avoid repeated imports.
- dependencies_and_callers: Catalog provider descriptors/model manager.
- edge_cases_or_failure_modes: Missing discovery module or unsupported provider config.
- validation_or_tests: Catalog provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1924 `file` `packages/coding-agent/src/capability/rule.ts`
- cursor: `[_]`
- core_role: Canonical rule capability and TTSR condition/scope parser.
- algorithmic_behavior: Normalizes frontmatter arrays/strings, splits scoped tokens while respecting parentheses/brackets/braces/quotes, infers file-glob conditions into edit/write tool scopes, and tracks active rules globally.
- inputs_outputs_state: Inputs are rule frontmatter/content/source metadata; outputs are `Rule` objects with condition/astCondition/scope and active rule snapshot.
- gates_or_invariants: Rule validation requires name/path/content; bundled defaults have lowest priority; glob shorthand emits `tool:edit` and `tool:write` scopes plus catch-all condition.
- dependencies_and_callers: Capability system, rule discovery, internal rule URL handlers, TTSR.
- edge_cases_or_failure_modes: Empty arrays, duplicate tokens, quoted commas in scope, regex-like condition mistaken for glob avoided by heuristic.
- validation_or_tests: Rule/capability tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1954 `file` `packages/coding-agent/src/cli/read-cli.ts`
- cursor: `[_]`
- core_role: CLI command implementation for reading files through the agent read tool path.
- algorithmic_behavior: Accepts read command args, constructs/dispatches read operation, and prints output.
- inputs_outputs_state: Inputs are CLI path/range/raw args; output is rendered file content or errors.
- gates_or_invariants: Uses read tool behavior rather than ad hoc file reads to keep selectors/rendering consistent.
- dependencies_and_callers: CLI command registry and read tool.
- edge_cases_or_failure_modes: Missing files, invalid range selectors, path errors.
- validation_or_tests: Covered indirectly by CLI/read tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1984 `file` `packages/coding-agent/src/commands/gallery.ts`
- cursor: `[_]`
- core_role: CLI command to launch/render gallery fixtures.
- algorithmic_behavior: Defines a Clipanion command class that invokes gallery fixture runtime.
- inputs_outputs_state: Inputs are CLI args/options; output is gallery UI/render fixture display.
- gates_or_invariants: Command shape must match registry expectations.
- dependencies_and_callers: Coding-agent command registry and gallery fixture modules.
- edge_cases_or_failure_modes: Missing fixture or render width.
- validation_or_tests: Gallery fixture tests/visual checks if present.
- skip_candidate: `yes: command wrapper with low algorithmic content.`

### OH_MY_HUMANIZE_MAIN-HZ-2014 `file` `packages/coding-agent/src/config/api-key-resolver.ts`
- cursor: `[_]`
- core_role: Central API-key resolver retry/rotation policy.
- algorithmic_behavior: `createApiKeyResolver` returns a resolver that gets initial key, force-refreshes same account after first auth error, and rotates session credential on last chance before resolving again.
- inputs_outputs_state: Inputs are provider, session ID, base URL, model ID, error/lastChance/signal; output is API key string or undefined.
- gates_or_invariants: Account rotation ignores retry-after for sibling switch; `forceRefresh` used only after non-final error; model-form overload derives hints externally.
- dependencies_and_callers: Model registry/auth storage and provider request retry paths.
- edge_cases_or_failure_modes: No key, no sibling credential, abort during rotation, account-rate-limit/auth errors.
- validation_or_tests: Auth/credential rotation tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2044 `file` `packages/coding-agent/src/debug/terminal-info.ts`
- cursor: `[_]`
- core_role: Collects and formats terminal runtime diagnostics.
- algorithmic_behavior: Detects multiplexer from env, maps image/notify protocols to names, collects terminal capability state, and formats yes/no diagnostic lines.
- inputs_outputs_state: Inputs are env and runtime terminal state; output is `TerminalStateInfo` and formatted text.
- gates_or_invariants: Unknown protocols are normalized through maps; booleans are formatted consistently.
- dependencies_and_callers: TUI terminal capabilities and debug command.
- edge_cases_or_failure_modes: Missing env, unknown multiplexer, null protocols.
- validation_or_tests: Indirect terminal debug tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2074 `file` `packages/coding-agent/src/edit/renderer.ts`
- cursor: `[_]`
- core_role: Renderer for edit/apply_patch tool calls, streaming previews, and final results.
- algorithmic_behavior: Extracts partial JSON paths/text, renders headers, previews plain text/diffs, summarizes hashline/apply_patch inputs, wraps diff lines, and renders single/multi-file success/error results.
- inputs_outputs_state: Inputs are tool call args, partial JSON, diff previews, edit results, render context, TUI theme/width; outputs are sanitized/truncated render lines/components.
- gates_or_invariants: Preview line/width caps; file paths are shortened/truncated; missing `*** End Patch` has special error; diff stats suffix derived from diff content.
- dependencies_and_callers: TUI tool renderer registry, hashline/LSP batch request, render-utils sanitization.
- edge_cases_or_failure_modes: Partial streamed JSON strings, missing paths, multi-file previews, failed patch parse, long file names, terminal width constraints.
- validation_or_tests: `edit-diff.test.ts` and tool execution render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2104 `file` `packages/coding-agent/src/goals/index.ts`
- cursor: `[_]`
- core_role: Barrel export for guided goals runtime/state/tool modules.
- algorithmic_behavior: Re-exports goal runtime, state, and goal tool modules.
- inputs_outputs_state: No runtime state; output is module export surface.
- gates_or_invariants: Barrel must avoid duplicate ambiguous exports.
- dependencies_and_callers: Imports by coding-agent goal features.
- edge_cases_or_failure_modes: Export path drift.
- validation_or_tests: Guided-goal tests validate downstream modules.
- skip_candidate: `yes: pure barrel, no direct algorithm.`

### OH_MY_HUMANIZE_MAIN-HZ-2134 `file` `packages/coding-agent/src/irc/bus.ts`
- cursor: `[_]`
- core_role: Process-global agent-to-agent mailbox and delivery bus.
- algorithmic_behavior: Sends messages to live/parked agents, revives parked sessions, injects into waiters or session asides/wake turns, buffers failed deliveries, supports wait/inbox semantics, and relays to main UI.
- inputs_outputs_state: Inputs are sender/recipient/body/reply metadata and wait filters; outputs are delivery receipts, mailbox messages, and resolved waiter promises.
- gates_or_invariants: Mailbox cap is 100; successful injection does not also buffer; parked agents revive lazily; aborted/unknown agents fail.
- dependencies_and_callers: `AgentRegistry`, `AgentLifecycleManager`, session `deliverIrcMessage`, Snowflake IDs, logger.
- edge_cases_or_failure_modes: Recipient disposed mid-delivery, async-execution-disabled auto-reply path, waiter filtering by sender, parked revival failure.
- validation_or_tests: Agent/IRC tool tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2164 `file` `packages/coding-agent/src/mcp/startup-events.ts`
- cursor: `[_]`
- core_role: MCP startup event channel helpers.
- algorithmic_behavior: Exports channel constant, formats connecting message from server names, and validates event shape.
- inputs_outputs_state: Input is server names or unknown event data; output is formatted message or type guard boolean.
- gates_or_invariants: Event is valid only when `serverNames` is string array.
- dependencies_and_callers: MCP startup UI/event bus.
- edge_cases_or_failure_modes: Empty server list, malformed data.
- validation_or_tests: MCP reconnect/startup tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2194 `file` `packages/coding-agent/src/modes/runtime-init.ts`
- cursor: `[_]`
- core_role: Initializes extensions into an `AgentSession` runtime.
- algorithmic_behavior: Loads/discovers extensions, registers tools/handlers/widgets/hooks, sends initial extension messages/actions, and wires extension send actions to session prompt/custom message flows.
- inputs_outputs_state: Inputs are session, settings, cwd, extension paths, event bus; outputs are initialized extension runner/tool state and optional user/extension messages.
- gates_or_invariants: Extension send action is constrained to `extension_send` or `extension_send_user`; initialization handles no-extension case.
- dependencies_and_callers: Extension loader/runner and session runtime.
- edge_cases_or_failure_modes: Extension load errors, missing paths, handler failures.
- validation_or_tests: Extension/plugin discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2224 `file` `packages/coding-agent/src/session/session-dump-format.ts`
- cursor: `[_]`
- core_role: Formats session transcript dumps as markdown text.
- algorithmic_behavior: Builds tool inventory, renders header metadata, appends markdown transcript with roles/tool calls/results and content handling.
- inputs_outputs_state: Inputs are session messages, tool info, options; output is markdown dump text.
- gates_or_invariants: Tool inventory is deduped/sorted; transcript renderer handles custom/tool content branches.
- dependencies_and_callers: Session export/dump commands.
- edge_cases_or_failure_modes: Unknown message types, image content, tool result arrays, missing tool info.
- validation_or_tests: Session persistence/export tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2254 `file` `packages/coding-agent/src/stt/asr-worker.ts`
- cursor: `[_]`
- core_role: Speech-to-text worker for transformers.js and sherpa-onnx models.
- algorithmic_behavior: Lazily installs/loads runtimes, caches loaded models, downloads sherpa model files with progress, falls back device/dtype load order, transcribes batch audio and streaming endpointer segments, and emits progress/log/result/error messages.
- inputs_outputs_state: Inputs are worker transport messages, audio floats, STT model key, language/task options, endpointer events; outputs are transcript text/progress events and model cache state.
- gates_or_invariants: Whisper chunks use 30s windows with 5s stride; sample rate fixed at 16k; model load is serialized by `runOnModel`; progress is coalesced every 4MB for downloads.
- dependencies_and_callers: `@huggingface/transformers`, `sherpa-onnx-node`, tiny runtime install helpers, STT protocol/models/endpointer.
- edge_cases_or_failure_modes: Missing optional runtime, compiled binary runtime install, model download failure, device fallback, streaming session cancellation, pump race.
- validation_or_tests: STT smoke/runtime tests where configured.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2284 `file` `packages/coding-agent/src/tiny/worker.ts`
- cursor: `[_]`
- core_role: Local tiny text-generation worker for titles and memory completions.
- algorithmic_behavior: Lazily installs/loads transformers.js, caches pipelines by model key, applies device/dtype fallback, builds chat/completion prompts, stops on title close text, normalizes generated titles, and serializes queued requests.
- inputs_outputs_state: Inputs are worker messages, model key, prompt text/system prompt, max token settings; outputs are generated title/completion and progress/log events.
- gates_or_invariants: Title generation max 20 new tokens; completion max 1024; stop decode window is 32 tokens; runtime resolution is deferred until needed.
- dependencies_and_callers: `@huggingface/transformers`, tiny model config/device/dtype/text helpers, runtime install utilities.
- edge_cases_or_failure_modes: Missing runtime/model, compiled binary dependency install, bad generated title, request queue error propagation.
- validation_or_tests: Tiny worker smoke probe via CLI smoke test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2314 `file` `packages/coding-agent/src/tools/gh.ts`
- cursor: `[_]`
- core_role: GitHub tool implementing repo/issue/PR/search/run/watch/checkout/push workflows.
- algorithmic_behavior: Defines schema and `GithubTool`; parses GitHub URLs/date bounds/limits, resolves default repo, shells to `gh`/git, caches issue/PR views, parses unified PR diffs, watches actions runs/jobs/logs, formats markdown results, saves large artifacts, and mutates git worktrees/remotes for PR checkout/push.
- inputs_outputs_state: Inputs are tool params, cwd/session settings, gh CLI output, git state, GitHub API JSON; outputs are text results, details objects, artifacts, local worktrees/remotes, and cache entries.
- gates_or_invariants: Search limit max 50; log tail max 200; read-only ops set separates safe operations; run-watch has poll failure/no-runs limits; repo resolution is memoized; stateReason fallback retries without optional field.
- dependencies_and_callers: Agent tool system, `gh` CLI, git utils, GitHub cache, tool-result/error helpers.
- edge_cases_or_failure_modes: Older gh missing fields, rate limiting, ambiguous repo, PR URL parsing, worktree path collisions, run pending/failure/success states, failed job log fetch, quoted diff paths.
- validation_or_tests: GitHub cache invalidation, internal issue/pr URL tests, and gh-related tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2344 `file` `packages/coding-agent/src/tools/resolve.ts`
- cursor: `[_]`
- core_role: Tool for suspending a run until an external/user resolution is provided.
- algorithmic_behavior: Queues resolve handlers, runs resolve invocation against session/update callback, renders waiting/resolved state, and exposes `ResolveTool`.
- inputs_outputs_state: Inputs are resolve params and queued handler; outputs are tool result/details and TUI renderer lines.
- gates_or_invariants: Missing handler or aborted signal must surface a tool error; invocation state is correlated through queue.
- dependencies_and_callers: AgentTool, ToolSession, renderer helpers.
- edge_cases_or_failure_modes: Handler throws, no queued handler, cancellation.
- validation_or_tests: Resolve/workflow tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2374 `file` `packages/coding-agent/src/tui/tree-list.ts`
- cursor: `[_]`
- core_role: Renders generic tree lists for TUI dashboards.
- algorithmic_behavior: Walks tree nodes with indentation/connector prefixes and applies theme formatting for labels/status.
- inputs_outputs_state: Inputs are item tree, child selector, render callbacks, theme; output is array of terminal lines.
- gates_or_invariants: Stable tree traversal order follows input order; width/format callbacks own truncation.
- dependencies_and_callers: TUI extension dashboard/hub-style components.
- edge_cases_or_failure_modes: Empty children, deep nesting, long labels.
- validation_or_tests: Indirect UI tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2404 `file` `packages/coding-agent/src/utils/tools-manager.ts`
- cursor: `[_]`
- core_role: Ensures auxiliary external tools are available by locating, downloading, or installing them.
- algorithmic_behavior: Maps tool names to platform assets/repos, resolves local tool paths, fetches latest GitHub release metadata, downloads binaries with timeout, installs Python packages, handles Termux package names, and returns executable path.
- inputs_outputs_state: Inputs are tool name, platform/arch, signal, silent options; outputs are paths under tools dir or undefined.
- gates_or_invariants: Download timeout 120s; metadata timeout 5s; ffmpeg asset names are platform/arch-gated; tool path lookup checks known locations.
- dependencies_and_callers: GitHub release APIs, filesystem, Python package tooling, environment/platform helpers.
- edge_cases_or_failure_modes: Unsupported platform/arch, download failure, missing executable, Termux package fallback, aborted install.
- validation_or_tests: Tool manager tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2434 `file` `packages/coding-agent/src/workflow/runtime-timeout.ts`
- cursor: `[_]`
- core_role: Shared workflow max-runtime constant and stop-reason formatter.
- algorithmic_behavior: Exports five-day default max runtime and a formatted stop reason string.
- inputs_outputs_state: Input is runtime ms; output is stop reason text.
- gates_or_invariants: Default is exactly `5 * 24 * 60 * 60 * 1000`.
- dependencies_and_callers: Workflow scheduler/runtime.
- edge_cases_or_failure_modes: None beyond caller-supplied ms formatting.
- validation_or_tests: Scheduler tests indirectly.
- skip_candidate: `yes: tiny constant/helper, minimal algorithm.`

### OH_MY_HUMANIZE_MAIN-HZ-2464 `file` `packages/coding-agent/test/core/python-executor-lifecycle.test.ts`
- cursor: `[_]`
- core_role: Tests Python executor kernel lifecycle management.
- algorithmic_behavior: Asserts per-call kernels shut down, session kernels reuse/reset/restart, failures restart dead kernels, and concurrent resets coalesce.
- inputs_outputs_state: Inputs are mocked kernel manager/execution results; outputs are lifecycle call counts and returned execute results.
- gates_or_invariants: Dead retained sessions must restart even without shutdown confirmation; concurrent resets must not throw reset-in-progress.
- dependencies_and_callers: Python executor lifecycle.
- edge_cases_or_failure_modes: Dead kernel after execution failure, missing shutdown confirmation, reset race.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2494 `file` `packages/coding-agent/test/discovery/claude-plugins.test.ts`
- cursor: `[_]`
- core_role: Tests Claude plugin registry parsing and discovery.
- algorithmic_behavior: Parses registry JSON, lists plugin roots, reads manifests for skills/commands, enforces scope precedence, caches results, and tests agent discovery precedence.
- inputs_outputs_state: Inputs are temp plugin registries/manifests; outputs are discovered roots, warnings, skills/commands/agents.
- gates_or_invariants: Invalid JSON/missing version/plugins return null; manifest paths resolving outside plugin root are ignored; project-scoped plugin agent wins over user-scoped.
- dependencies_and_callers: Plugin discovery/agent discovery.
- edge_cases_or_failure_modes: Multiple entries per plugin ID, invalid plugin ID, missing install path, `commands` versus `slash-commands` precedence.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2524 `file` `packages/coding-agent/test/goals/guided-goal.test.ts`
- cursor: `[_]`
- core_role: Tests guided goal setup/model selection and structured response handling.
- algorithmic_behavior: Creates session/harness, chooses plan/slow/current model fallback, validates malformed responses, obfuscates/deobfuscates secrets, and salvages objectives at turn cap.
- inputs_outputs_state: Inputs are mocked models/responses/settings/transcripts; outputs are selected model, draft objective/question, and errors.
- gates_or_invariants: Plan model preferred, slow fallback next, current model fallback preserves disabled reasoning, malformed structured responses rejected.
- dependencies_and_callers: Guided goal runtime/tool.
- edge_cases_or_failure_modes: Missing role models, secret echo, question without objective at cap.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2554 `file` `packages/coding-agent/test/modes/context-usage.test.ts`
- cursor: `[_]`
- core_role: Tests context usage/token reporting.
- algorithmic_behavior: Asserts ArkType schema token estimation uses wire JSON Schema and snapcompact section renders savings/skip reasons/wire totals or hides when inactive.
- inputs_outputs_state: Inputs are tool schemas and context usage data; outputs are rendered usage text/metrics.
- gates_or_invariants: Text-only models are inactive; section omitted when no snapcompact setting is on.
- dependencies_and_callers: Context usage renderer.
- edge_cases_or_failure_modes: ArkType internals leaking into token count.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2584 `file` `packages/coding-agent/test/session/redis-session-storage-manager.test.ts`
- cursor: `[_]`
- core_role: Tests Redis-backed session storage integration.
- algorithmic_behavior: Uses fake Redis to persist assistant messages, reopen sessions, and list Redis-backed sessions for cwd.
- inputs_outputs_state: Inputs are fake usage/messages/session manager actions; outputs are reloaded sessions and list entries.
- gates_or_invariants: Appended assistant messages persist and reload via `open`; list is cwd-scoped.
- dependencies_and_callers: SessionManager and RedisSessionStorage.
- edge_cases_or_failure_modes: Fake Redis ordering/hash/list behavior.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2614 `file` `packages/coding-agent/test/task/discovery.test.ts`
- cursor: `[_]`
- core_role: Tests task/agent discovery filtering.
- algorithmic_behavior: Creates OMP and Claude agent markdown fixtures and asserts OMP agents load while Claude Code custom agents are skipped.
- inputs_outputs_state: Inputs are fixture markdown files; outputs are discovered agents.
- gates_or_invariants: Discovery must distinguish supported OMP agents from Claude custom agents.
- dependencies_and_callers: Agent discovery.
- edge_cases_or_failure_modes: Mixed agent formats in same search roots.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2644 `file` `packages/coding-agent/test/tools/bash-command-fixup.test.ts`
- cursor: `[_]`
- core_role: Tests bash command normalization/fixups.
- algorithmic_behavior: Verifies stripping harmless trailing `head`/`tail`, redundant `2>&1`, and compound-command variants while preserving semantic pipelines.
- inputs_outputs_state: Inputs are bash command strings; outputs are fixup result command/metadata.
- gates_or_invariants: Only harmless output-limiting/redundant redirection is stripped; semantics-bearing pipelines remain unchanged.
- dependencies_and_callers: Bash tool command fixup.
- edge_cases_or_failure_modes: Compound commands, quoted syntax, pipelines whose behavior depends on head/tail.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2674 `file` `packages/coding-agent/test/tools/gh-cache-invalidation.test.ts`
- cursor: `[_]`
- core_role: Tests GitHub cache invalidation from shell `gh` mutations.
- algorithmic_behavior: Seeds issue/PR cache and asserts `invalidateGithubCacheForBashCommand` drops relevant entries for close/merge commands, URL args, `--repo`, chained commands, and fallback scopes.
- inputs_outputs_state: Inputs are bash command strings and cache rows; outputs are remaining/invalidated cache IDs.
- gates_or_invariants: Read-only `gh issue view` is ignored; bare number can invalidate across repos; `--repo` scopes invalidation.
- dependencies_and_callers: GitHub cache and bash command observer.
- edge_cases_or_failure_modes: Quoted URLs, value-taking flags, no positional PR merge fallback.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2704 `file` `packages/coding-agent/test/tools/report-tool-issue.test.ts`
- cursor: `[_]`
- core_role: Tests grievance/report-tool-issue queue flushing.
- algorithmic_behavior: Uses temp SQLite DB, push settings, env overrides, and mock fetch to verify consent gating, endpoint gating, bearer header, batch draining, cooldown, concurrency collapse, and failure preservation.
- inputs_outputs_state: Inputs are grievance rows/settings/env/fetch responses; outputs are pushed flags, result status, and HTTP payloads.
- gates_or_invariants: No network without consent/endpoint; 200 marks rows pushed; 5xx preserves rows; concurrent callers share in-flight push.
- dependencies_and_callers: Report tool issue storage/flusher.
- edge_cases_or_failure_modes: Mid-flight inserts, backlog bigger than batch size, mid-batch failure, failure cooldown.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2734 `file` `packages/coding-agent/test/tui/hyperlink.test.ts`
- cursor: `[_]`
- core_role: Tests OSC 8 hyperlink generation and internal URL resolution.
- algorithmic_behavior: Toggles hyperlink modes/env, extracts link URIs, and asserts file/URI/URL hyperlink behavior, encoding, ANSI preservation, no double wrapping, and internal URL fallback.
- inputs_outputs_state: Inputs are paths, URLs, mode settings, terminal capability stubs; outputs are OSC 8-wrapped or plain strings.
- gates_or_invariants: `off` disables; `always` ignores TTY; `auto` respects `NO_COLOR` and terminal support; control bytes prevent URI wrapping.
- dependencies_and_callers: TUI hyperlink helpers and internal URL router.
- edge_cases_or_failure_modes: Spaces/reserved bytes, relative paths, line/col query params, malformed URLs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2764 `file` `packages/coding-agent/test/workflow/scheduler.test.ts`
- cursor: `[_]`
- core_role: Tests workflow activation scheduler graph semantics.
- algorithmic_behavior: Runs synthetic workflow graphs to assert linear order, conditional edges, output-condition evaluation, schema/state scope enforcement, loops/activation limits, joins, sibling concurrency, cancellation, and graph patch rejection.
- inputs_outputs_state: Inputs are workflow YAML/DSL strings and host callbacks; outputs are captured activation entries/frontier/results.
- gates_or_invariants: State patches apply before outgoing edge evaluation; writes outside declared scope fail; joins wait for declared parents; active-run graph patches are rejected.
- dependencies_and_callers: Workflow runtime scheduler.
- edge_cases_or_failure_modes: Looped joins, cancellation after completion, per-node activation limit, parallel activation cancellation.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2794 `file` `packages/mnemopi/src/core/embeddings.ts`
- cursor: `[_]`
- core_role: Mnemopi embedding provider abstraction and local/API embedding execution.
- algorithmic_behavior: Resolves active embedding options, detects disabled state, chooses API versus local fastembed model, caches query embeddings, embeds batches, exposes availability, dimensions, model identity, and test provider overrides.
- inputs_outputs_state: Inputs are texts, env/config/model name/API key/provider; outputs are Float32 vectors or null and cached provider/model state.
- gates_or_invariants: Query cache keyed by provider/model/options; known model dimensions map; API key availability gates API models; test runtime behavior can disable local.
- dependencies_and_callers: `fastembed`, `@oh-my-pi/pi-ai` auth/http helpers, OpenRouter headers, mnemopi runtime options.
- edge_cases_or_failure_modes: Missing API key, provider unavailable, unsupported model dimensions, local model init failure, embedding API HTTP errors.
- validation_or_tests: Mnemopi embedding tests through setup reset.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2824 `file` `packages/mnemopi/src/dr/recovery.ts`
- cursor: `[_]`
- core_role: Disaster recovery for mnemopi SQLite databases.
- algorithmic_behavior: Computes default paths, creates compressed backups with metadata/checksum, restores backups via temp files and sidecar cleanup, performs emergency restore, verifies integrity, lists/rotates backups, and health-checks.
- inputs_outputs_state: Inputs are DB path, backup dir, env, backup files; outputs are backup/restore/rotate/health result objects and filesystem side effects.
- gates_or_invariants: SQLite header is verified; restore snapshots current DB first; sidecar files are removed/restored carefully; backup timestamps are unique.
- dependencies_and_callers: Bun SQLite, filesystem/path/zlib/crypto, mnemopi config/db helpers.
- edge_cases_or_failure_modes: Missing files, invalid backup gzip/SQLite, restore failure requiring current snapshot rollback, sidecar WAL/SHM/journal handling.
- validation_or_tests: Recovery tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2854 `file` `packages/tui/src/components/spacer.ts`
- cursor: `[_]`
- core_role: TUI component rendering a fixed number of blank lines.
- algorithmic_behavior: Caches an array of empty strings and invalidates cache when line count changes.
- inputs_outputs_state: Input is line count; output is `readonly string[]` of blank lines.
- gates_or_invariants: `setLines` no-ops when unchanged; `render` ignores width.
- dependencies_and_callers: TUI layout components.
- edge_cases_or_failure_modes: Negative/non-integer line counts are not guarded here; callers should pass sane values.
- validation_or_tests: Indirect component rendering tests.
- skip_candidate: `yes: simple layout utility, minimal core algorithm.`

### OH_MY_HUMANIZE_MAIN-HZ-2884 `directory` `packages/coding-agent/src/export/html/vendor`
- cursor: `[_]`
- core_role: Bundled minified third-party browser libraries for HTML export rendering.
- algorithmic_behavior: Contains `highlight.min.js` for syntax highlighting and `marked.min.js` for Markdown parsing in exported HTML.
- inputs_outputs_state: Inputs are markdown/code in exported HTML runtime; outputs are browser-rendered HTML/highlighting.
- gates_or_invariants: Vendor files are static/minified and should not be locally edited unless upgrading vendor versions.
- dependencies_and_callers: HTML export feature.
- edge_cases_or_failure_modes: Vendor library bugs or version drift.
- validation_or_tests: HTML export tests/visual checks if present.
- skip_candidate: `yes: vendored generated/minified assets, not local algorithm source.`

### OH_MY_HUMANIZE_MAIN-HZ-2914 `file` `crates/pi-shell/src/minimizer/filters/lint.rs`
- cursor: `[_]`
- core_role: Rust output minimizer for type-checker/linter logs.
- algorithmic_behavior: Claims lint/typecheck programs, strips ANSI/noise, preserves machine-readable output, reshapes ESLint stylish rows, groups diagnostics by file/code, summarizes top rules/codes, and head/tail truncates grouped output.
- inputs_outputs_state: Inputs are minimizer context, raw output, exit code; outputs are passthrough or transformed minimized text with original length.
- gates_or_invariants: JSON/machine-readable output is preserved; JS frame noise stripping is gated to JS lint programs; max grouped output uses `head_tail_lines`.
- dependencies_and_callers: `pi-shell` minimizer primitives/detect pipeline.
- edge_cases_or_failure_modes: ESLint stylish parsing, tsc diagnostic forms, pyright banners, code frames, gutter lines, dotted versions, path-like grouping.
- validation_or_tests: Rust minimizer tests in crate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2944 `file` `packages/ai/src/registry/oauth/xai-oauth.ts`
- cursor: `[_]`
- core_role: xAI OAuth login and refresh flow.
- algorithmic_behavior: Validates discovery/token endpoints, fetches OIDC discovery with timeout, builds authorize URL, runs callback flow, detects expiring JWT access tokens, exchanges auth code, and refreshes tokens.
- inputs_outputs_state: Inputs are OAuth controller callbacks, refresh token, fetch override, JWTs; outputs are `OAuthCredentials`.
- gates_or_invariants: Endpoint protocol/host validation; client skew for access token expiry; fixed client ID/scope/redirect; discovery/token request timeouts.
- dependencies_and_callers: AI OAuth registry and `OAuthCallbackFlow`.
- edge_cases_or_failure_modes: Invalid URLs, discovery missing endpoints, expired/near-expired JWT, token HTTP failure, callback cancellation.
- validation_or_tests: OAuth provider tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2974 `file` `packages/coding-agent/src/cli/gallery-fixtures/fs.ts`
- cursor: `[_]`
- core_role: Filesystem tool gallery fixtures for UI rendering.
- algorithmic_behavior: Builds static read/write/grouped-read fixture states and renders grouped read components at widths/expanded states.
- inputs_outputs_state: Inputs are fixture state/width/expanded flag; outputs are gallery render lines/results.
- gates_or_invariants: Fixture args are deterministic and exercise repeated ranges/grouped paths.
- dependencies_and_callers: Gallery command/UI fixture runner.
- edge_cases_or_failure_modes: Fixture drift from real tool result shape.
- validation_or_tests: Visual/gallery checks.
- skip_candidate: `yes: fixture/demo data, not runtime algorithm.`

### OH_MY_HUMANIZE_MAIN-HZ-3004 `file` `packages/coding-agent/src/commit/utils/exclusions.ts`
- cursor: `[_]`
- core_role: Commit file exclusion helper.
- algorithmic_behavior: `isExcludedFile` filters known generated/lock/excluded names and suffixes; `filterExcludedFiles` removes matching PR/file entries.
- inputs_outputs_state: Input is path or `{filename}` list; output is boolean or filtered list.
- gates_or_invariants: Lock suffixes `.lock.yml`, `.lock.yaml`, `-lock.yml`, `-lock.yaml` are excluded.
- dependencies_and_callers: Commit/PR tooling.
- edge_cases_or_failure_modes: Path normalization is caller responsibility; suffix-only matching can exclude same-named files anywhere.
- validation_or_tests: Commit tooling tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3034 `file` `packages/coding-agent/src/eval/py/display.ts`
- cursor: `[_]`
- core_role: Normalizes Python kernel display outputs for UI/tool results.
- algorithmic_behavior: Converts notebook display MIME bundles into normalized text/image/HTML-like output shape and trims display text.
- inputs_outputs_state: Inputs are kernel display content records; outputs are `{output, mimeType}` style render data.
- gates_or_invariants: Text is normalized before render; unsupported content is handled gracefully.
- dependencies_and_callers: Python eval executor/rendering.
- edge_cases_or_failure_modes: Missing MIME keys, binary/image content, malformed display payload.
- validation_or_tests: Python executor/eval tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3064 `file` `packages/coding-agent/src/extensibility/hooks/runner.ts`
- cursor: `[_]`
- core_role: Runs configured extensibility hooks with error reporting.
- algorithmic_behavior: `HookRunner` executes hook commands/events, emits hook errors to listeners, and re-exports `execCommand` for hook execution.
- inputs_outputs_state: Inputs are hooks, event payloads, execution options; outputs are hook results/errors and listener callbacks.
- gates_or_invariants: Hook errors are captured through typed listener instead of crashing caller.
- dependencies_and_callers: Hook capability, exec command helper, extension/runtime hooks.
- edge_cases_or_failure_modes: Command failure, timeout/abort, malformed hook config.
- validation_or_tests: Hook/extension tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3094 `file` `packages/coding-agent/src/modes/acp/acp-mode.ts`
- cursor: `[_]`
- core_role: Starts Agent Client Protocol mode.
- algorithmic_behavior: Creates ACP connection with a session factory and runs it, optionally with an initial session.
- inputs_outputs_state: Inputs are cwd/session factory and optional initial session; output is a never-returning ACP mode promise.
- gates_or_invariants: `runAcpMode` returns `Promise<never>` because control stays in protocol loop.
- dependencies_and_callers: ACP mode entrypoint and session factory.
- edge_cases_or_failure_modes: Connection creation/session factory failure.
- validation_or_tests: ACP integration tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3124 `file` `packages/coding-agent/src/modes/components/hook-selector.ts`
- cursor: `[_]`
- core_role: Interactive TUI selector component for hooks/options.
- algorithmic_behavior: Normalizes options, wraps lines preserving leading spaces, filters options, renders outlined list and slider segments, and handles focus/keyboard interaction.
- inputs_outputs_state: Inputs are options, sliders, theme, selection/filter state, key events; outputs are rendered lines and selection callbacks.
- gates_or_invariants: Option labels/values normalized; wrapping keeps indentation; component state controls focus/selection.
- dependencies_and_callers: TUI container/components and hook/extension UI.
- edge_cases_or_failure_modes: Empty option sets, long labels, narrow widths, filter no-match state.
- validation_or_tests: UI/component tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3154 `file` `packages/coding-agent/src/modes/components/tool-execution.ts`
- cursor: `[_]`
- core_role: Live/final TUI renderer for tool execution.
- algorithmic_behavior: Stabilizes streaming diffs, resolves edit modes, merges streamed text args, animates spinner, builds render context, renders tool-specific previews/results/images/JSON trees, freezes detached background tasks, and manages native scrollback live regions.
- inputs_outputs_state: Inputs are tool call snapshots/results/progress, partial JSON, render context, theme, terminal capabilities, width; outputs are TUI component tree/lines and live-region probes.
- gates_or_invariants: Spinner frame constants; image output sanitized with optional sixel passthrough; JSON tree depth/line/scalar caps; edit previews strip trailing unbalanced removals to reduce jitter.
- dependencies_and_callers: TUI primitives, edit renderers, tool renderer registry, render-utils sanitization, terminal image helpers.
- edge_cases_or_failure_modes: Partial streamed args, detached task freeze, image dimension fallback, streaming apply_patch jitter, missing result, long output, background final result after freeze.
- validation_or_tests: `tool-execution-background-task.test.ts` and TUI rendering tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3184 `file` `packages/coding-agent/src/modes/rpc/rpc-mode.ts`
- cursor: `[_]`
- core_role: Headless JSON stdin/stdout RPC mode for embedding the agent.
- algorithmic_behavior: Parses RPC commands, emits responses/events, bridges host tools/URIs, tracks extension UI requests, handles session changes, skill commands, local-only prompt reporting, subagent subscriptions, editor requests, and initializes extensions.
- inputs_outputs_state: Inputs are JSONL commands and session/events; outputs are JSON responses, agent events, extension UI requests, host tool/URI requests/cancels.
- gates_or_invariants: Commands use correlation IDs; skill command requires `/skill:` and enabled setting; host tool definitions are normalized; local-only prompt result is reported separately.
- dependencies_and_callers: AgentSession, EventBus, extension runtime, host tool/URI bridges, subagent registry, OAuth providers.
- edge_cases_or_failure_modes: Pending extension response rejection, session switch cancellation, local-only prompt when no agent invoked, malformed dialog response, unsupported subscription level.
- validation_or_tests: RPC host URI tests and RPC mode integrations.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3214 `file` `packages/coding-agent/src/tools/browser/attach.ts`
- cursor: `[_]`
- core_role: Browser/CDP attach and process cleanup helpers.
- algorithmic_behavior: Finds free CDP ports, waits for CDP readiness, parses existing CDP args, probes reusable ports, selects Electron/page targets, gracefully kills process trees, and kills existing browser processes by executable path.
- inputs_outputs_state: Inputs are ports, CDP URL, Playwright browser/pages, matcher, executable path, abort signal; outputs are selected page, boolean readiness, killed count.
- gates_or_invariants: Attach target skip pattern avoids devtools/internal pages; free port binds before release; wait loops respect timeout/signal.
- dependencies_and_callers: Browser tool launch/attach implementation, Playwright, process tree utility.
- edge_cases_or_failure_modes: Port races, CDP not ready, multiple pages, matcher misses, process kill grace timeout.
- validation_or_tests: Browser tool tests/doc.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3244 `file` `packages/coding-agent/src/web/scrapers/flathub.ts`
- cursor: `[_]`
- core_role: Special web scraper for Flathub app pages.
- algorithmic_behavior: Extracts app ID from pathname, fetches AppStream data, normalizes strings/numbers, derives installs/permissions/releases/screenshots, picks best screenshot, and returns special search/scrape response.
- inputs_outputs_state: Inputs are URL/path/fetch context; outputs are structured app metadata and sources/images.
- gates_or_invariants: Numeric parsing returns null on invalid values; screenshot choice prefers largest area.
- dependencies_and_callers: Web scraper special handler framework.
- edge_cases_or_failure_modes: Invalid app path, missing AppStream fields, absent screenshots/releases, fetch failure.
- validation_or_tests: Web scraper tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3274 `file` `packages/coding-agent/src/web/scrapers/pubmed.ts`
- cursor: `[_]`
- core_role: Special web scraper for PubMed/NCBI records.
- algorithmic_behavior: Uses NCBI headers and URL data to fetch/parse PubMed metadata and produce normalized special handler output.
- inputs_outputs_state: Inputs are PubMed URL/search context; outputs are article metadata/snippets/source content.
- gates_or_invariants: NCBI headers identify requests; handler returns only for supported PubMed shapes.
- dependencies_and_callers: Web scraper special handler framework.
- edge_cases_or_failure_modes: Missing PubMed ID, NCBI fetch failure, malformed article metadata.
- validation_or_tests: Web scraper tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3304 `file` `packages/coding-agent/src/web/search/types.ts`
- cursor: `[_]`
- core_role: Shared web search provider types and response schemas.
- algorithmic_behavior: Defines provider IDs/preferences/labels, type guards, normalized search response/citation/source/usage structures, provider error, and upstream response shapes for Anthropic/Perplexity.
- inputs_outputs_state: Inputs are provider preference strings and upstream API JSON; outputs are typed normalized structures used by providers.
- gates_or_invariants: `auto` is excluded from concrete provider ID; provider preference guard allows `auto`; options list determines order.
- dependencies_and_callers: Search providers such as Tavily/Kimi/Perplexity/Anthropic.
- edge_cases_or_failure_modes: Unknown provider strings, upstream response variant drift.
- validation_or_tests: Search provider tests, including Tavily/Kimi.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3334 `file` `packages/coding-agent/test/modes/components/tool-execution-background-task.test.ts`
- cursor: `[_]`
- core_role: Tests detached/background tool rendering freeze behavior.
- algorithmic_behavior: Builds progress/final snapshots and asserts live redraws stop while detached, partial updates freeze, but final result still applies.
- inputs_outputs_state: Inputs are tool execution snapshots; outputs are component render/probe state.
- gates_or_invariants: Detached live task keeps progress bytes static and drops post-freeze partial snapshots.
- dependencies_and_callers: `ToolExecutionComponent`.
- edge_cases_or_failure_modes: Final result arriving after freeze.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3364 `file` `packages/coding-agent/test/modes/controllers/tan-command-controller.test.ts`
- cursor: `[_]`
- core_role: Tests background “tan” command controller behavior.
- algorithmic_behavior: Creates command context, rejects empty work, forks/clones sessions, dispatches background jobs, handles abort, registers under Main, and parks finished tan agents.
- inputs_outputs_state: Inputs are command text, session/model mocks, job registry signals; outputs are dispatched jobs, cloned agent parentage, registry entries.
- gates_or_invariants: In-flight turn is not disturbed while streaming; parent of tan clone is spawning agent; abort signal aborts cloned agent.
- dependencies_and_callers: TanCommandController, Agent Hub/registry.
- edge_cases_or_failure_modes: Empty request, streaming state, breadcrumb suppression, job ID receipt timing.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3394 `file` `packages/coding-agent/test/web/search/tavily.test.ts`
- cursor: `[_]`
- core_role: Tests Tavily search request body semantics.
- algorithmic_behavior: Asserts request body omits `topic`, handles recency as `time_range`, includes core fields, and integration mock verifies upstream payload.
- inputs_outputs_state: Inputs are query/recency/max results and mock fetch; outputs are request JSON and normalized search result.
- gates_or_invariants: Recency must not switch Tavily to `topic=news`.
- dependencies_and_callers: Tavily search provider.
- edge_cases_or_failure_modes: Recency unset, upstream API payload shape.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3424 `file` `packages/collab-web/src/tool-render/tools/memory-retain.tsx`
- cursor: `[_]`
- core_role: Web UI renderer for memory retain tool results.
- algorithmic_behavior: Parses retain items from args, renders summary badges and body rows with normalized/truncated text and result output.
- inputs_outputs_state: Inputs are tool render props, args, details/result text; outputs are React nodes.
- gates_or_invariants: Invalid args render `InvalidArg`; text is whitespace-normalized, tabs replaced, and truncated.
- dependencies_and_callers: Collab web tool renderer registry.
- edge_cases_or_failure_modes: Missing/invalid retain item arrays, long content, absent result text.
- validation_or_tests: Web renderer tests if present.
- skip_candidate: `yes: presentation layer, not core algorithm, but sanitizes tool output.`

### OH_MY_HUMANIZE_MAIN-HZ-3454 `file` `packages/stats/src/client/app/TopBar.tsx`
- cursor: `[_]`
- core_role: Stats dashboard top navigation bar component.
- algorithmic_behavior: Renders menu button, current route label, range control, sync button, and theme toggle.
- inputs_outputs_state: Inputs are section, range, sync state, theme, and callbacks; output is React UI.
- gates_or_invariants: Route metadata comes from `routes`; callbacks are passed through.
- dependencies_and_callers: Stats React app layout.
- edge_cases_or_failure_modes: Unknown section route label fallback depends on route map.
- validation_or_tests: Client view/component tests indirectly.
- skip_candidate: `yes: UI composition only, little algorithmic content.`

### OH_MY_HUMANIZE_MAIN-HZ-3484 `file` `packages/swarm-extension/src/swarm/__tests__/executor.test.ts`
- cursor: `[_]`
- core_role: Test for swarm extension subprocess execution auth behavior.
- algorithmic_behavior: Mocks subprocess result and asserts `executeSwarmAgent` does not pass `authStorage` when `modelRegistry` is provided.
- inputs_outputs_state: Inputs are executor options/model registry; outputs are runSubprocess call args.
- gates_or_invariants: Model registry path owns auth; authStorage must not be forwarded redundantly.
- dependencies_and_callers: Swarm extension executor.
- edge_cases_or_failure_modes: Option precedence regression.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3514 `file` `packages/coding-agent/src/commit/agentic/tools/split-commit.ts`
- cursor: `[_]`
- core_role: Agentic tool for proposing split commits from changed files/hunks.
- algorithmic_behavior: Defines schemas for hunk/file/commit items, builds a tool that validates commit plans, hunk selectors, file membership, dependencies, and returns structured split-commit response/errors.
- inputs_outputs_state: Inputs are changed files/diffs and model-proposed commit plan; outputs are validated commit groupings or error text.
- gates_or_invariants: Hunk selectors must reference valid files/hunks; dependencies must point to earlier/valid commits and avoid impossible ordering; each file change shape is schema-checked.
- dependencies_and_callers: Agentic commit workflow.
- edge_cases_or_failure_modes: Duplicate hunks, missing files, out-of-range dependencies, selecting `all` plus specific hunks.
- validation_or_tests: Commit agentic tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3544 `file` `packages/coding-agent/src/modes/components/extensions/types.ts`
- cursor: `[_]`
- core_role: Type/state helpers for extension dashboard UI.
- algorithmic_behavior: Defines extension/provider/tree/flat item/dashboard callback types; `makeExtensionId`, `parseExtensionId`, and `sourceFromMeta` convert between extension IDs and metadata.
- inputs_outputs_state: Inputs are extension kind/name/source metadata; outputs are stable IDs, parsed IDs, and UI source labels.
- gates_or_invariants: Extension IDs use kind/name encoding and parse only recognized shape.
- dependencies_and_callers: Extension dashboard components.
- edge_cases_or_failure_modes: Names containing separators if parser is strict, unknown source metadata.
- validation_or_tests: Extension dashboard tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3574 `file` `packages/coding-agent/src/web/search/providers/kimi.ts`
- cursor: `[_]`
- core_role: Kimi web search provider.
- algorithmic_behavior: Resolves API base/key, calls Kimi coding search endpoint with timeout/result count, maps Kimi results into normalized `SearchResponse`, and exposes `KimiProvider`.
- inputs_outputs_state: Inputs are query, num results, timeout, API key/base URL, fetch override; outputs are normalized sources/citations/usage.
- gates_or_invariants: Default results 10, max 20, timeout 30s; query/key strings are trimmed; missing key errors through provider error path.
- dependencies_and_callers: Search provider framework and `SearchResponse` types.
- edge_cases_or_failure_modes: Missing API key, upstream non-OK response, malformed result fields, timeout/abort.
- validation_or_tests: Search tests where configured.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3604 `file` `packages/utils/src/vendor/mermaid-ascii/xychart/colors.ts`
- cursor: `[_]`
- core_role: Color utilities for vendored Mermaid ASCII xychart rendering.
- algorithmic_behavior: Converts hex/RGB/HSL, validates hex colors, detects dark background, mixes colors, and selects series colors from accent/background.
- inputs_outputs_state: Inputs are hex colors, series index, ratio/background; outputs are hex colors and booleans.
- gates_or_invariants: Invalid hex rejected by `isValidHex`; fallback accent is blue-500.
- dependencies_and_callers: Mermaid ASCII xychart renderer.
- edge_cases_or_failure_modes: Invalid hex, short/long color formats, dark/light contrast.
- validation_or_tests: Vendor/renderer tests if present.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `121 unique Item Evidence headings`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`