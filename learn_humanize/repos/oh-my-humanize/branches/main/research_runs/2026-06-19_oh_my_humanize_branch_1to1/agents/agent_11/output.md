# agent_11 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-011 `file` `README.md`
- cursor: `[_]`
- core_role: Behavior-defining top-level contract for the CLI, SDK/RPC/ACP modes, built-in tools, workflow artifacts, and session semantics.
- algorithmic_behavior: Documents command routing, tool execution surfaces, session storage/resume flows, model/provider selection, workflow editing, MCP, LSP/DAP/eval/search/hashline behavior, and TUI expectations.
- inputs_outputs_state: Inputs are CLI flags, slash commands, SDK/RPC/ACP calls, prompts, files, and tool calls; outputs are session JSONL entries, tool cards, filesystem changes, responses, workflow files, and UI state.
- gates_or_invariants: Published tool behavior must match implementation; destructive or privileged actions require permission/approval gates; workflow and session state are persistent contracts.
- dependencies_and_callers: Points to `packages/coding-agent/src/sdk.ts`, modes, tools, workflow runtime, session manager, provider clients, and docs under `docs/`.
- edge_cases_or_failure_modes: Documentation can drift from code; because it defines user-visible behavior, drift is an algorithmic risk even though the file is prose.
- validation_or_tests: Indirectly covered by the assigned coding-agent, ai, agent, catalog, and TUI tests that assert the documented contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-041 `directory` `python/robomp`
- cursor: `[_]`
- core_role: Python GitHub automation orchestrator for event intake, queueing, sandboxed worker execution, PR/issue triage/review, host-side tools, and web dashboard.
- algorithmic_behavior: `server.py` wires FastAPI routes, HMAC webhook ingestion, manual trigger/cancel/status endpoints, worker pool, sandbox manager, proxies, and autoclose scheduler; `github_events.py` classifies GitHub events and directives; `db.py` maintains SQLite WAL queues and issue/PR mappings; `queue.py` serializes work per issue and manages slots; `worker.py` drives `omp_rpc`; `tasks.py` hydrates GitHub context and chooses triage/review/comment/conversation actions; `sandbox.py`, `host_tools.py`, `slot_pool.py`, `cancellation.py`, proxy clients, config/persona, tests, and web UI complete the runtime.
- inputs_outputs_state: Inputs are GitHub webhook payloads, maintainer comments, config/env, dashboard/manual triggers, DB rows, sandbox filesystem state, and RPC model output; outputs are DB event transitions, GitHub comments/reviews/labels/closures/PRs, tool-call audit rows, worker logs, and dashboard state.
- gates_or_invariants: HMAC and allowlist gates protect ingestion; per-issue in-flight serialization prevents concurrent conflicting work; slot pool and sandbox UID/chown/safe.directory rules isolate workers; dirty workspace reminders and cancellation hooks guard task lifecycle; PR handling is gated to safe bot-owned branches.
- dependencies_and_callers: Depends on FastAPI, GitHub REST/GraphQL wrappers, SQLite, `omp_rpc`, local git worktrees, host tool registry, and React dashboard under `python/robomp/web`.
- edge_cases_or_failure_modes: Restart recovery must reconcile queued/running rows; failed workers need retry/backoff; sandbox git worktree setup is brittle; visual inspection flagged fragile PR-close and worktree command paths that deserve syntax/runtime validation.
- validation_or_tests: Directory includes focused Python tests plus web components; behavior is also exercised by webhook/task smoke paths when the service runs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-071 `file` `docs/session-switching-and-recent-listing.md`
- cursor: `[_]`
- core_role: Architecture documentation for recent session listing, `--resume`, `--continue`, selector behavior, and live session switching.
- algorithmic_behavior: Defines how recent sessions are discovered, sorted, scoped by cwd, selected, and switched; describes `AgentSession.switchSession` lifecycle: pre-switch hook, abort/flush, session file replacement, context rebuild, tool/system prompt refresh, model/thinking/service-tier restoration, and UI reconciliation.
- inputs_outputs_state: Inputs are session IDs/files, cwd filters, CLI flags, TUI selectors, and persisted JSONL headers; outputs are selected session paths, updated session manager state, rebuilt agent context, and UI transcript state.
- gates_or_invariants: Switches must flush and abort safely before replacing the active session; cwd handling must avoid accidental relocation; recent listing must be stable and avoid stale/broken entries.
- dependencies_and_callers: Documents `SessionManager`, selector controller, CLI resume/continue paths, `AgentSession.switchSession`, model restoration, and TUI transcript rebuilding.
- edge_cases_or_failure_modes: Missing files, relocated sessions, stale cwd metadata, active streaming turns, and model/API unavailability during restore are the main failure modes.
- validation_or_tests: Covered by `packages/coding-agent/test/session-manager/*`, session switching/resume tests, and ACP/session tests in the assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-101 `file` `scripts/fix-test-imports.ts`
- cursor: `[_]`
- core_role: Repository maintenance codemod for rewriting test imports to package public subpaths.
- algorithmic_behavior: Scans package `test`/`tests` trees, parses relative import specifiers, resolves them against package `src`, skips assets/non-source imports, maps internal paths to package public subpaths, and reports or writes changes depending on `--write`.
- inputs_outputs_state: Inputs are package directories, source/test paths, import strings, and CLI write mode; outputs are a dry-run report or rewritten test files.
- gates_or_invariants: Only rewrites imports that resolve under the same package source tree and to recognized source module extensions; dry-run is default.
- dependencies_and_callers: Uses Bun/TypeScript script execution, filesystem traversal, path resolution, and package naming conventions.
- edge_cases_or_failure_modes: Regex-based import rewriting can miss unusual syntax; asset imports and ambiguous extensions are intentionally skipped.
- validation_or_tests: Validation is by dry-run output and subsequent package checks; no direct assigned test file specifically targets this script.
- skip_candidate: `yes: maintenance codemod rather than runtime core, but it affects test routing contracts`

### OH_MY_HUMANIZE_MAIN-HZ-131 `directory` `packages/coding-agent/bench`
- cursor: `[_]`
- core_role: Benchmark harnesses for performance-sensitive coding-agent algorithms.
- algorithmic_behavior: Contains `edit-lsp-writethrough.bench.ts`, `rendering.ts`, and `session-tree-nav.bench.ts` to measure LSP write-through/edit paths, renderer costs, and session tree navigation behavior.
- inputs_outputs_state: Inputs are synthetic benchmark fixtures and local package code; outputs are timing/performance measurements, not product state.
- gates_or_invariants: Benchmarks should preserve realistic algorithm inputs and avoid mutating persistent user state.
- dependencies_and_callers: Depends on coding-agent LSP/edit/session-tree/rendering modules and Bun benchmark execution.
- edge_cases_or_failure_modes: Benchmark drift can hide performance regressions if fixtures stop matching real workloads.
- validation_or_tests: Bench scripts are performance validation assets; they are not correctness tests.
- skip_candidate: `yes: benchmark-only directory, useful for algorithm performance but not runtime behavior`

### OH_MY_HUMANIZE_MAIN-HZ-161 `directory` `packages/wire/src`
- cursor: `[_]`
- core_role: Shared wire protocol contract for collaboration relay/client/host traffic.
- algorithmic_behavior: `index.ts` defines protocol constants, room/key/write-token byte sizes, relay/share URLs, envelope sizes, participant/session/agent snapshot shapes, control messages, guest frames, and collaboration prompt/message types.
- inputs_outputs_state: Inputs are serialized JSON/binary frames and relay control data; outputs are typed frame/control structures used by host, guest, relay, and web client.
- gates_or_invariants: Constant byte sizes and protocol version must match crypto/link parsing in `packages/coding-agent/src/collab`; frame discriminants must remain stable across packages.
- dependencies_and_callers: Called by coding-agent collab host/guest/crypto/protocol, collab web client, and relay-side code.
- edge_cases_or_failure_modes: Any incompatible type or constant change breaks live collaboration handshakes or decryption.
- validation_or_tests: Covered indirectly by collab protocol/link parsing and client behavior tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-191 `file` `docs/tools/inspect_image.md`
- cursor: `[_]`
- core_role: Tool architecture document for image inspection behavior and vision fallback.
- algorithmic_behavior: Defines `inspect_image` decision flow: input path/URL normalization, image loading, MIME/type checks, resizing, model capability selection, prompt construction, and fallback/error handling.
- inputs_outputs_state: Inputs are image references, optional prompt text, model settings/capabilities, and file/network data; outputs are vision model responses or structured tool errors.
- gates_or_invariants: Must validate image accessibility/type/size, choose a vision-capable model, avoid unsupported MIME payloads, and preserve user intent in the prompt.
- dependencies_and_callers: Documents coding-agent image input normalization, vision fallback utilities, provider clients, and tool renderer behavior.
- edge_cases_or_failure_modes: Unsupported image formats, oversized images, model without vision support, network fetch failure, and missing local file.
- validation_or_tests: Assigned tests include `image-input-normalization.test.ts` and `image-vision-fallback.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-221 `file` `scripts/session-stats/optimize_read_config.py`
- cursor: `[_]`
- core_role: Offline optimizer for read-tool/session statistics and read configuration tuning.
- algorithmic_behavior: Replays SQLite session stats, parses read selectors/footers/truncation markers, aggregates token/line coverage per file/session, simulates page/line/byte/summarizer policies, sweeps parameter grids, and produces plots/recommendations.
- inputs_outputs_state: Inputs are stats database rows, read output text, token estimates, and tuning grids; outputs are aggregate metrics, charts, and recommended config values.
- gates_or_invariants: Must parse truncation/footer formats consistently, group by session/file, and compare candidate policies against common coverage metrics.
- dependencies_and_callers: Uses Python SQLite/data analysis stack and session-stats data produced by coding-agent usage.
- edge_cases_or_failure_modes: Malformed read output, missing stats rows, token estimator mismatch, and workload sampling bias can distort recommendations.
- validation_or_tests: Validation is analytic reproducibility; no direct runtime test assigned.
- skip_candidate: `yes: research/optimization script rather than runtime core, but it analyzes read algorithm behavior`

### OH_MY_HUMANIZE_MAIN-HZ-251 `directory` `packages/coding-agent/src/collab`
- cursor: `[_]`
- core_role: Live collaboration host/guest protocol implementation for shared sessions.
- algorithmic_behavior: `crypto.ts` generates room keys/write tokens and AES-256-GCM seals frames; `protocol.ts` packs envelopes, formats/parses compact/web links, validates relay origins, and distinguishes read-only/full links; `relay-client.ts` manages reconnecting WebSocket transport with send/receive ordering; `host.ts` broadcasts session entries/events/state/agent snapshots and handles guest prompt/abort/agent commands; `guest.ts` writes replica session files, resumes through normal session machinery, applies frames, and restores local session on leave.
- inputs_outputs_state: Inputs are relay URLs, room links, encrypted frames, session events, SessionManager entries, agent registry snapshots, guest prompts, and transcript fetch offsets; outputs are encrypted envelopes, replicated JSONL files, ACP-like UI state, status-line overrides, host-side prompts/aborts, and transcript chunks.
- gates_or_invariants: Room key stays in link fragment/secret; write token is timing-safe checked; read-only peers cannot mutate; frame application is serialized; welcome snapshot precedes later frames; reconnect resyncs from a fresh welcome.
- dependencies_and_callers: Uses `@oh-my-pi/pi-wire`, `AgentSession`, `SessionManager`, event bus, agent registry/lifecycle, TUI interactive context, and collab web client.
- edge_cases_or_failure_modes: Bad key/corrupt frame is fatal; relay close codes stop reconnect; oversized welcome strips images; transcript replies are capped and trimmed to full JSONL lines; session switch ends host share.
- validation_or_tests: Covered indirectly by collab client/protocol tests and session-switching behavior; no single assigned collab unit test was in this batch.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-281 `directory` `packages/coding-agent/src/ssh`
- cursor: `[_]`
- core_role: SSH host configuration, connection management, remote command execution, host probing, and optional sshfs mounting.
- algorithmic_behavior: `config-writer.ts` reads/writes `ssh.json` atomically and validates host names; `connection-manager.ts` validates key permissions, builds SSH args, manages ControlMaster sockets, probes/caches host OS/shell/compat info, and cleans up postmortem; `ssh-executor.ts` streams remote stdout/stderr into `OutputSink` with truncation/artifact support and abort/timeout handling; `sshfs-mount.ts` mounts/unmounts remote filesystems; `utils.ts` sanitizes host names and targets.
- inputs_outputs_state: Inputs are SSH host configs, key paths, commands, timeout/abort signals, remote paths, and cached host metadata; outputs are remote execution results, cached host info JSON, mounted paths, logs, and cleanup side effects.
- gates_or_invariants: Host names and key permissions are validated; ControlMaster disabled on Windows; active/pending connection maps dedupe starts; compat shell is only enabled when detected; output is bounded by settings.
- dependencies_and_callers: Called by coding-agent SSH tools and collab web SSH renderer; depends on `ssh`, `sshfs`, Bun shell, `ptree`, settings, and postmortem cleanup.
- edge_cases_or_failure_modes: Missing binaries, insecure key permissions, stale ControlMaster sockets, host probe failures, Windows shell mismatch, mount failures, abort races, and output truncation.
- validation_or_tests: Renderer tests cover web display; runtime needs integration tests with fake SSH or controlled host for full validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-311 `directory` `packages/coding-agent/test/session-manager`
- cursor: `[_]`
- core_role: Behavioral regression suite for session manager algorithms.
- algorithmic_behavior: Tests context building, continue relocation, drafts, file operations, labels, migrations, move-to/rewrite/rename EPERM handling, save entries, session IDs, signature persistence, subagent breadcrumbs, title-source persistence, tree traversal, and usage statistics.
- inputs_outputs_state: Inputs are temporary session files/directories, JSONL entries, cwd/session metadata, and simulated filesystem failures; outputs are persisted session records, listings, labels, paths, signatures, and traversal results.
- gates_or_invariants: Session IDs/signatures remain stable, migrations preserve data, relocations are explicit, tree traversal does not corrupt parent/child relationships, and failed filesystem operations surface correctly.
- dependencies_and_callers: Targets `SessionManager`, session listing, session paths, JSONL persistence, usage stats, and related helpers.
- edge_cases_or_failure_modes: EPERM rename, missing/moved files, corrupt metadata, subagent breadcrumbs, stale cwd, and title-source precedence.
- validation_or_tests: The directory itself is validation evidence for session algorithms.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-341 `file` `crates/pi-iso/src/btrfs.rs`
- cursor: `[_]`
- core_role: Rust isolation backend for btrfs snapshot-based workspaces.
- algorithmic_behavior: Probes `btrfs version`, starts by canonicalizing a lower directory, clearing destination, creating a read/write btrfs subvolume snapshot, and cleaning up on failure; stop deletes the subvolume/tree. Non-Linux returns unavailable/no-op stop behavior.
- inputs_outputs_state: Inputs are lower/destination paths and platform capabilities; outputs are snapshot directories or unsupported/failure errors plus cleanup side effects.
- gates_or_invariants: Only Linux can use btrfs; destination is removed before snapshot; failed start cleans partial destination; stop is idempotent enough for cleanup.
- dependencies_and_callers: Uses Rust filesystem/process helpers and btrfs CLI; called by isolation selection logic in the native/iso crate.
- edge_cases_or_failure_modes: Missing btrfs binary, non-btrfs filesystem, permission errors, canonicalization failure, partial snapshot creation, and delete failure.
- validation_or_tests: Requires Linux+btrfs integration validation; non-Linux behavior is explicitly guarded.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-371 `file` `crates/pi-natives/src/snapcompact.rs`
- cursor: `[_]`
- core_role: Native renderer converting compact text/page representations into PNG images.
- algorithmic_behavior: Parses BDF/hex fonts, maps text into row-major or document/two-column grids, applies sentence hue cycling, dim markers, full-block handling, line repeat bands, optional stretch via Lanczos3 resize, and indexed/RGB PNG encoding; `render_snapcompact_png` validates options and returns base64 Latin-1 PNG data.
- inputs_outputs_state: Inputs are text/page content, font bytes, variant/options, columns/cell sizes, and palette decisions; output is encoded PNG bytes/string.
- gates_or_invariants: Validates dimensions, font availability, columns, cell grid, and palette bit depth; cycle guards avoid malformed font/render state.
- dependencies_and_callers: Uses Rust image/PNG/font parsing utilities and is consumed by `packages/snapcompact` or native bindings.
- edge_cases_or_failure_modes: Invalid fonts, oversized dimensions, Unicode marker handling, stretch artifacts, palette overflow, and visual inspection flagged a possibly duplicated `height` parameter that should be compiler-validated.
- validation_or_tests: Research visualization scripts and native tests/consumers provide validation; compile checks would catch signature issues.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-401 `file` `packages/agent/test/compaction-file-ops.test.ts`
- cursor: `[_]`
- core_role: Regression specification for extracting file-operation context during compaction.
- algorithmic_behavior: Tests read-selector stripping, extraction of file operations from messages, URL-scheme exclusion, computation of file lists, and formatting `<files>` output.
- inputs_outputs_state: Inputs are synthetic transcript/message strings with file paths/selectors/URLs; outputs are normalized file operation lists and formatted summaries.
- gates_or_invariants: URL-like paths are not treated as local files; selectors are stripped consistently; formatted output is stable for downstream compaction prompts.
- dependencies_and_callers: Targets agent compaction utilities used when summarizing conversation/file context.
- edge_cases_or_failure_modes: Ambiguous colon selectors, URL schemes, duplicated file references, and malformed message text.
- validation_or_tests: This file is the validation suite for the compaction file-op parser.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-431 `file` `packages/ai/test/abort.test.ts`
- cursor: `[_]`
- core_role: Regression specification for AI client abort handling.
- algorithmic_behavior: Exercises abort propagation through streaming/request paths and ensures cancellation surfaces as the expected error/termination behavior rather than a normal completion.
- inputs_outputs_state: Inputs are fake fetch/streaming providers and `AbortSignal`s; outputs are rejected promises, stopped streams, or classified abort errors.
- gates_or_invariants: Abort must be observed promptly, not double-resolve, and not mask unrelated provider errors.
- dependencies_and_callers: Targets `packages/ai` provider/client abort utilities used by coding-agent sessions and tools.
- edge_cases_or_failure_modes: Already-aborted signals, mid-stream abort, abort during retry/wait, and cleanup of listeners.
- validation_or_tests: The file itself validates abort semantics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-461 `file` `packages/ai/test/auth-gateway-anthropic-messages.test.ts`
- cursor: `[_]`
- core_role: Regression suite for Anthropic Messages auth-gateway request/stream translation.
- algorithmic_behavior: Tests parsing incoming gateway requests, shaping Anthropic message payloads, encoding streamed deltas/envelopes, and mapping errors/tool/image cases.
- inputs_outputs_state: Inputs are gateway HTTP-like bodies, message/tool/image fixtures, and fake upstream events; outputs are transformed Anthropic requests, encoded stream chunks, and formatted errors.
- gates_or_invariants: Message roles/content blocks and tool-use ordering must be preserved; auth-gateway wire format must remain compatible with Anthropic clients.
- dependencies_and_callers: Targets `packages/ai` auth gateway and Anthropic message encoder/decoder paths.
- edge_cases_or_failure_modes: Image/tool result hoisting, malformed request bodies, upstream errors, streaming envelope boundaries, and legacy message shapes.
- validation_or_tests: This file is direct validation for the Anthropic gateway algorithm.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-491 `file` `packages/ai/test/callback-server-manual-input.test.ts`
- cursor: `[_]`
- core_role: Regression spec for OAuth/callback manual input fallback behavior.
- algorithmic_behavior: Tests callback server flows where browser redirect or local callback capture requires manual code/input handling.
- inputs_outputs_state: Inputs are simulated callback/manual input events; outputs are resolved auth data or handled errors.
- gates_or_invariants: Manual input must not hang indefinitely and must map callback data into the expected auth response.
- dependencies_and_callers: Targets AI auth callback server utilities used by provider OAuth flows.
- edge_cases_or_failure_modes: Missing code, timeout, user cancellation, and duplicate callback/manual submissions.
- validation_or_tests: The file itself validates the manual-input branch.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-521 `file` `packages/ai/test/google-system-prompt.test.ts`
- cursor: `[_]`
- core_role: Regression spec for Google provider system prompt shaping.
- algorithmic_behavior: Tests how system/developer prompt content is serialized into Google/Gemini request structures.
- inputs_outputs_state: Inputs are model messages with system content; outputs are Google-compatible request payload fields.
- gates_or_invariants: System prompt must land in the supported Google field and not be duplicated or dropped.
- dependencies_and_callers: Targets Google provider request construction used by pi-ai clients.
- edge_cases_or_failure_modes: Empty system messages, multiple system segments, mixed message roles, and provider-specific prompt constraints.
- validation_or_tests: The file is the focused validation for Google system prompt handling.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-551 `file` `packages/ai/test/issue-955-repro.test.ts`
- cursor: `[_]`
- core_role: Issue regression fixture for a previously broken AI provider behavior.
- algorithmic_behavior: Reproduces issue #955 with the minimal request/response conditions needed to lock the fix.
- inputs_outputs_state: Inputs are issue-specific model/message/provider fixtures; outputs are expected transformed payloads or errors.
- gates_or_invariants: The historical failure mode must not reappear.
- dependencies_and_callers: Depends on the provider/client code implicated by issue #955.
- edge_cases_or_failure_modes: Narrow regression may not cover adjacent provider variants.
- validation_or_tests: This file is the validation artifact.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-581 `file` `packages/ai/test/openai-compat-policy.test.ts`
- cursor: `[_]`
- core_role: Regression suite for OpenAI-compatible provider policy resolution.
- algorithmic_behavior: Tests policy decisions for OpenAI-compatible models/providers, including request-shaping capabilities, tool/schema behavior, and compatibility flags.
- inputs_outputs_state: Inputs are provider/model descriptors and policy inputs; outputs are resolved compatibility policies.
- gates_or_invariants: Provider-specific policy must be deterministic and preserve expected overrides.
- dependencies_and_callers: Targets OpenAI compatibility policy code in `packages/ai` and catalog descriptors.
- edge_cases_or_failure_modes: Ambiguous provider IDs, missing descriptors, model-specific overrides, and retired/alias models.
- validation_or_tests: This file directly validates policy resolution.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-611 `file` `packages/ai/test/pi-native-client.test.ts`
- cursor: `[_]`
- core_role: Regression suite for pi-native client wire protocol.
- algorithmic_behavior: Tests request shape, endpoint normalization, header/auth behavior, option stripping, stream event handling, error formatting, and abort behavior.
- inputs_outputs_state: Inputs are client config, fake fetch responses/SSE chunks, request options, and abort signals; outputs are HTTP requests, parsed stream events, usage/errors, and cancellation outcomes.
- gates_or_invariants: Unsupported options must not leak to the native endpoint; headers and endpoint paths must be stable; stream parsing must preserve event order.
- dependencies_and_callers: Targets pi-ai native client used by coding-agent model calls.
- edge_cases_or_failure_modes: Malformed stream frames, provider HTTP errors, missing endpoint, abort mid-stream, and option incompatibility.
- validation_or_tests: This file is direct client validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-641 `file` `packages/ai/test/tool-inventory.test.ts`
- cursor: `[_]`
- core_role: Regression spec for rendering/serializing tool inventories.
- algorithmic_behavior: Tests `renderToolInventory` output from tool descriptors, ensuring names/descriptions/parameters appear in expected semantic form.
- inputs_outputs_state: Inputs are tool definitions; outputs are inventory text/structures used in prompts or diagnostics.
- gates_or_invariants: Tool inventory must be complete, stable enough for prompt consumers, and avoid malformed schema text.
- dependencies_and_callers: Targets pi-ai tool inventory utilities used by agent prompt construction.
- edge_cases_or_failure_modes: Missing descriptions, duplicate tool names, schema edge cases, and ordering changes.
- validation_or_tests: This file is the validation suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-671 `file` `packages/catalog/test/azure-provider.test.ts`
- cursor: `[_]`
- core_role: Regression spec for Azure provider descriptor/discovery behavior.
- algorithmic_behavior: Tests Azure model/provider configuration, API identity, model limits, or catalog resolution expectations.
- inputs_outputs_state: Inputs are Azure provider descriptors/configs; outputs are normalized provider/model metadata.
- gates_or_invariants: Azure-specific endpoints and model metadata must not be confused with generic OpenAI descriptors.
- dependencies_and_callers: Targets `packages/catalog` provider descriptors/resolvers used by model selection.
- edge_cases_or_failure_modes: Deployment/model ID ambiguity, missing limits, and provider aliasing.
- validation_or_tests: This file is direct catalog validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-701 `file` `packages/catalog/test/nanogpt-model-limits.test.ts`
- cursor: `[_]`
- core_role: Regression spec for NanoGPT model limit metadata.
- algorithmic_behavior: Verifies catalog-derived limits for NanoGPT models and expected fallback behavior.
- inputs_outputs_state: Inputs are catalog entries/descriptors; outputs are context/output token limit assertions.
- gates_or_invariants: Generated/discovered limits must remain sane and provider-specific overrides must apply.
- dependencies_and_callers: Targets catalog model metadata used by model resolver and context estimation.
- edge_cases_or_failure_modes: Missing upstream metadata, renamed model IDs, and fallback limit drift.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-731 `file` `packages/coding-agent/src/sdk.ts`
- cursor: `[_]`
- core_role: Central factory for constructing an `AgentSession` and all runtime dependencies.
- algorithmic_behavior: Pins auth storage to the model registry, subscribes credential-disabled bridge before model resolution, parallel-loads settings/context/workspace/prompts/slash commands/skills, resolves model/thinking/service tier, builds `ToolSession`, tool registry, MCP manager, extension runner, advisor/session state, LSP warmup, memory/autolearn, MCP callbacks, deferred discovery, async yield queues, and cleanup handlers.
- inputs_outputs_state: Inputs are cwd/settings/session paths/model selectors/provider credentials/context files/extensions/MCP configs; outputs are live `AgentSession`, `Agent`, `ToolSession`, registry entries, yield queues, and disposers.
- gates_or_invariants: Auth-storage identity must be shared; model restore must not synchronously require missing API keys; MCP discovery may be deferred; cleanup must unsubscribe/dispose LSP/MCP/memory queues; session model/thinking restoration observes precedence.
- dependencies_and_callers: Called by CLI/TUI/ACP/SDK entrypoints; depends on `packages/agent`, `packages/ai`, catalog, tools, MCP, LSP, session manager, settings, extensions, skills, and memory backend.
- edge_cases_or_failure_modes: Missing credentials, disabled providers during startup, late extension providers, failed MCP discovery, unavailable model fallback, stale session model, and disposal races; visual inspection showed a duplicated assignment line worth syntax/check validation.
- validation_or_tests: Assigned SDK/session tests include credential-disabled bridge, eager compaction, MCP discovery/profile, and session storage compatibility.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-761 `file` `packages/coding-agent/test/agent-session-eager-compaction.test.ts`
- cursor: `[_]`
- core_role: Regression suite for eager compaction reminders in `AgentSession`.
- algorithmic_behavior: Tests that task/todo reminders and compaction-related state are emitted after compaction at the correct time.
- inputs_outputs_state: Inputs are simulated session turns/messages/todos/compaction triggers; outputs are reminder events/messages and preserved session state.
- gates_or_invariants: Eager compaction must not drop required task/todo context or duplicate reminders.
- dependencies_and_callers: Targets `AgentSession` compaction integration and reminder scheduling.
- edge_cases_or_failure_modes: Compaction during active tasks, empty reminders, repeated compactions, and queued messages.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-791 `file` `packages/coding-agent/test/agent-storage-sqlite-compat.test.ts`
- cursor: `[_]`
- core_role: Regression spec for agent storage SQLite compatibility.
- algorithmic_behavior: Verifies storage reads/writes/migrations against SQLite-backed session or agent state.
- inputs_outputs_state: Inputs are temporary SQLite stores and session/storage records; outputs are persisted and retrieved rows/metadata.
- gates_or_invariants: Schema compatibility and migration behavior must preserve existing state.
- dependencies_and_callers: Targets coding-agent storage abstractions and SQLite compatibility code.
- edge_cases_or_failure_modes: Missing tables, legacy schemas, nullable columns, and migration idempotence.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-821 `file` `packages/coding-agent/test/cli-print-thoughts-flag.test.ts`
- cursor: `[_]`
- core_role: Regression spec for CLI `--print-thoughts` flag handling.
- algorithmic_behavior: Asserts flag parsing/configuration maps to thinking-output display behavior.
- inputs_outputs_state: Inputs are CLI args/config state; outputs are boolean/option state consumed by print mode.
- gates_or_invariants: Flag must not be ignored or inverted.
- dependencies_and_callers: Targets CLI option parsing and print-mode setup.
- edge_cases_or_failure_modes: Default behavior, explicit false/true, and interaction with model thinking settings.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-851 `file` `packages/coding-agent/test/event-controller-error-banner.test.ts`
- cursor: `[_]`
- core_role: Regression suite for TUI event-controller provider error banners.
- algorithmic_behavior: Tests pinning, restoring, clearing, and rendering of provider error status/banner state across events.
- inputs_outputs_state: Inputs are simulated provider/session events; outputs are status container/banner state and rendered messages.
- gates_or_invariants: Error banners must not disappear prematurely, duplicate, or survive after clear conditions.
- dependencies_and_callers: Targets event controller and TUI status/error rendering.
- edge_cases_or_failure_modes: Repeated errors, stream recovery, end-of-turn cleanup, and restored transcript state.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-881 `file` `packages/coding-agent/test/image-input-normalization.test.ts`
- cursor: `[_]`
- core_role: Regression spec for normalizing image inputs before model/tool submission.
- algorithmic_behavior: Tests local/URL/base64-like image references, MIME inference, and normalized content blocks.
- inputs_outputs_state: Inputs are user image arguments or embedded content; outputs are normalized image content accepted by providers.
- gates_or_invariants: Valid images are preserved; invalid paths/types fail predictably; normalization must not corrupt text content.
- dependencies_and_callers: Targets coding-agent image utilities and inspect/vision flows.
- edge_cases_or_failure_modes: Missing files, unsupported MIME, extensionless paths, data URLs, and mixed text/image prompt blocks.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-911 `file` `packages/coding-agent/test/issue-1401-repro.test.ts`
- cursor: `[_]`
- core_role: Issue regression fixture for a coding-agent behavior from issue #1401.
- algorithmic_behavior: Recreates the issue-specific sequence and asserts the corrected observable outcome.
- inputs_outputs_state: Inputs are targeted session/tool/model fixtures; outputs are expected session events or results.
- gates_or_invariants: The historical bug must remain fixed.
- dependencies_and_callers: Depends on the affected coding-agent module path for issue #1401.
- edge_cases_or_failure_modes: Narrow regression may not generalize beyond the captured repro.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-941 `file` `packages/coding-agent/test/job-renderer-preview.test.ts`
- cursor: `[_]`
- core_role: Regression suite for task/job renderer preview extraction.
- algorithmic_behavior: Tests task-result envelope parsing, collapse/expand display, preview text selection, and nested job result rendering.
- inputs_outputs_state: Inputs are synthetic tool/job result payloads; outputs are TUI render lines/cards.
- gates_or_invariants: Preview renderers must preserve useful result summaries without overflowing or showing malformed envelopes.
- dependencies_and_callers: Targets job/task renderer components in coding-agent TUI modes.
- edge_cases_or_failure_modes: Nested live results, malformed envelopes, large outputs, and collapsed preview truncation.
- validation_or_tests: This file is direct renderer validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-971 `file` `packages/coding-agent/test/mcp-stdio-transport.test.ts`
- cursor: `[_]`
- core_role: Regression suite for MCP stdio transport lifecycle.
- algorithmic_behavior: Tests command resolution, child process spawning, JSON-RPC frame writing/reading, notification handling, close/error behavior, and cleanup.
- inputs_outputs_state: Inputs are fake MCP server commands, stdin/stdout frames, and close/error events; outputs are transport messages, connection state, and errors.
- gates_or_invariants: Frames must be serialized exactly, process lifecycle must close cleanly, and notifications must not break request handling.
- dependencies_and_callers: Targets coding-agent MCP stdio transport used by MCP manager/tool discovery.
- edge_cases_or_failure_modes: Missing command, malformed frames, premature process exit, stderr noise, and close races.
- validation_or_tests: This file is direct transport validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1001 `file` `packages/coding-agent/test/plugin-install-local.test.ts`
- cursor: `[_]`
- core_role: Regression spec for local plugin installation workflow.
- algorithmic_behavior: Tests installing plugins from local paths, registry/config updates, and error handling around invalid plugin sources.
- inputs_outputs_state: Inputs are temporary plugin directories and install commands; outputs are plugin registry entries, copied/linked plugin state, or install errors.
- gates_or_invariants: Local installs must validate plugin metadata and not corrupt existing registry state.
- dependencies_and_callers: Targets plugin install command and extension discovery helpers.
- edge_cases_or_failure_modes: Missing manifest, duplicate plugin, invalid path, and stale registry cache.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1031 `file` `packages/coding-agent/test/sdk-credential-disabled-bridge.test.ts`
- cursor: `[_]`
- core_role: Regression suite for SDK credential-disabled event bridge.
- algorithmic_behavior: Tests fan-out, buffering before startup completion, disposal, error handling, and authStorage identity for credential-disabled events.
- inputs_outputs_state: Inputs are fake auth/model registry events and session creation timing; outputs are session notices/provider disable handling and subscription cleanup.
- gates_or_invariants: Credential-disabled events must not be lost, duplicated, or delivered after disposal; SDK must share registry auth storage.
- dependencies_and_callers: Targets `createAgentSession` in `sdk.ts`, model registry, auth storage, and provider disable paths.
- edge_cases_or_failure_modes: Event before session ready, multiple sessions, thrown handlers, startup failure, and disposed session.
- validation_or_tests: This file is direct validation for the bridge.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1061 `file` `packages/coding-agent/test/shake.test.ts`
- cursor: `[_]`
- core_role: Regression suite for `AgentSession` shake behavior.
- algorithmic_behavior: Tests the session “shake” operation that nudges/retries/continues a stuck or pending state.
- inputs_outputs_state: Inputs are simulated session states and messages; outputs are prompts/events/state transitions from shake.
- gates_or_invariants: Shake must only trigger in supported states and preserve transcript integrity.
- dependencies_and_callers: Targets `AgentSession` control flow and session event handling.
- edge_cases_or_failure_modes: Streaming state, aborting state, empty transcript, and repeated shake calls.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1091 `file` `packages/coding-agent/test/system-prompt-dedup.test.ts`
- cursor: `[_]`
- core_role: Regression spec for system prompt de-duplication.
- algorithmic_behavior: Tests prompt assembly so repeated system prompt sections are removed or merged without losing required instructions.
- inputs_outputs_state: Inputs are context/system prompt fragments; outputs are final model prompt messages.
- gates_or_invariants: Duplicate prompt content must not inflate context, while distinct required instructions remain present.
- dependencies_and_callers: Targets prompt assembly in coding-agent/session creation.
- edge_cases_or_failure_modes: Slightly different duplicate sections, session restore, extension-added prompts, and model-specific system message handling.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1121 `file` `packages/coding-agent/test/visual-truncate.test.ts`
- cursor: `[_]`
- core_role: Regression spec for visual width truncation.
- algorithmic_behavior: Tests truncating display strings according to terminal visual width rather than byte/string length.
- inputs_outputs_state: Inputs are strings with wide characters/ANSI/long text; outputs are width-bounded display strings.
- gates_or_invariants: Truncation must not split ANSI/state incorrectly or exceed target visual width.
- dependencies_and_callers: Targets coding-agent TUI truncation helpers.
- edge_cases_or_failure_modes: CJK/wide glyphs, zero-width sequences, ANSI escapes, and very small widths.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1151 `file` `packages/hashline/src/mismatch.ts`
- cursor: `[_]`
- core_role: Hashline mismatch/error construction for patch anchoring failures.
- algorithmic_behavior: Parses line anchors, validates bounds, computes recognized/unrecognized hash guidance, and formats `MismatchError` context around failed patch anchors.
- inputs_outputs_state: Inputs are file text, expected hash/anchor metadata, line ranges, and patch context; outputs are structured mismatch errors and human-readable diagnostics.
- gates_or_invariants: Line references must be in bounds; recognized hashes produce relocation guidance; unknown hashes produce safer failure messaging.
- dependencies_and_callers: Used by hashline patch application and coding-agent edit/hashline filesystem adapter.
- edge_cases_or_failure_modes: Out-of-range line numbers, file edits between read/write, unrecognized hashes, repeated lines, and missing context.
- validation_or_tests: Covered by hashline/edit tests and coding-agent edit-path regressions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1181 `file` `packages/mnemopi/test/beam-consolidate-unit.test.ts`
- cursor: `[_]`
- core_role: Regression suite for memory beam consolidation.
- algorithmic_behavior: Tests consolidation, sleep/degradation, fact extraction, and memory update behavior in the mnemopi beam memory system.
- inputs_outputs_state: Inputs are memory/fact fixtures, timestamps, and consolidation calls; outputs are updated memory records, facts, and scores.
- gates_or_invariants: Consolidation must preserve identity-relevant facts, degrade stale entries correctly, and avoid duplicate or contradictory memory writes.
- dependencies_and_callers: Targets mnemopi beam/consolidation core.
- edge_cases_or_failure_modes: Sibling races, stale facts, contradictory facts, empty extraction, and scoring thresholds.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1211 `file` `packages/mnemopi/test/identity-memory-parity.test.ts`
- cursor: `[_]`
- core_role: Regression spec for identity memory parity.
- algorithmic_behavior: Tests that identity-related memory/fact behavior remains consistent across storage or recall implementations.
- inputs_outputs_state: Inputs are identity memory fixtures; outputs are recalled/serialized memory structures and parity assertions.
- gates_or_invariants: Identity facts must not be lost or transformed differently across paths.
- dependencies_and_callers: Targets mnemopi identity memory and recall paths.
- edge_cases_or_failure_modes: Duplicate identity facts, casing/tokenization differences, and storage backend differences.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1241 `file` `packages/mnemopi/test/triples-data-dir.test.ts`
- cursor: `[_]`
- core_role: Regression spec for triples data directory handling.
- algorithmic_behavior: Tests where triples/graph memory data is stored, loaded, and isolated.
- inputs_outputs_state: Inputs are temp data dirs and memory triples; outputs are persisted files/records and loaded graph data.
- gates_or_invariants: Data directory selection must be deterministic and isolated between tests/sessions.
- dependencies_and_callers: Targets mnemopi triples storage.
- edge_cases_or_failure_modes: Missing dirs, stale data, environment overrides, and path collisions.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1271 `file` `packages/snapcompact/research/diag_kimi_mono.py`
- cursor: `[_]`
- core_role: Research diagnostic script for snapcompact/Kimi monochrome rendering or decoding.
- algorithmic_behavior: Produces diagnostic outputs for visual/encoding analysis of snapcompact pages under a Kimi/monochrome scenario.
- inputs_outputs_state: Inputs are research fixtures/text/images; outputs are diagnostic files/prints for manual comparison.
- gates_or_invariants: Should preserve reproducible parameters for comparing render variants.
- dependencies_and_callers: Related to `crates/pi-natives/src/snapcompact.rs` and snapcompact research tools.
- edge_cases_or_failure_modes: Research script can drift from production renderer; environment dependencies may be implicit.
- validation_or_tests: Manual/visual diagnostic validation, not an automated runtime test.
- skip_candidate: `yes: research diagnostic, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1301 `file` `packages/snapcompact/research/render_pages.ts`
- cursor: `[_]`
- core_role: Research helper for rendering snapcompact pages.
- algorithmic_behavior: Loads page/text inputs and invokes rendering paths to generate image artifacts for inspection.
- inputs_outputs_state: Inputs are page fixtures/options; outputs are rendered page image files or buffers.
- gates_or_invariants: Must pass options consistently to the renderer for reproducible comparisons.
- dependencies_and_callers: Depends on snapcompact/native rendering APIs.
- edge_cases_or_failure_modes: Fixture paths, native binding availability, and output directory assumptions.
- validation_or_tests: Visual/research validation only.
- skip_candidate: `yes: research helper, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1331 `file` `packages/snapcompact/research/snapcompact_viz_circuit.py`
- cursor: `[_]`
- core_role: Research visualization script for snapcompact circuit/encoding analysis.
- algorithmic_behavior: Generates visual representations of snapcompact encoding/rendering concepts for analysis.
- inputs_outputs_state: Inputs are configuration/fixtures; outputs are visual diagrams/images.
- gates_or_invariants: Visualization parameters should map consistently to the renderer being studied.
- dependencies_and_callers: Related to snapcompact native renderer and research scripts.
- edge_cases_or_failure_modes: Visual output can become stale relative to production algorithm; dependencies may be local.
- validation_or_tests: Manual visual validation.
- skip_candidate: `yes: research visualization, not runtime core`

### OH_MY_HUMANIZE_MAIN-HZ-1361 `file` `packages/swarm-extension/src/cli.ts`
- cursor: `[_]`
- core_role: CLI entrypoint for executing a swarm extension pipeline.
- algorithmic_behavior: Reads YAML path from argv, parses/validates swarm definition, builds dependency graph, detects cycles, computes execution waves, creates state tracker/model registry/settings, runs `PipelineController`, periodically dumps progress, and renders final progress.
- inputs_outputs_state: Inputs are YAML definition, workspace path, auth/model state, and pipeline graph; outputs are state tracker updates, progress text, and process exit success/failure.
- gates_or_invariants: Definition validation and cycle detection must pass before execution; workspace path is resolved relative to definition file.
- dependencies_and_callers: Depends on swarm parser/validator/graph/state/pipeline modules, catalog model registry, settings, and auth discovery.
- edge_cases_or_failure_modes: Missing YAML arg, invalid config, graph cycles, missing credentials, and pipeline failure.
- validation_or_tests: Validated by swarm extension tests or manual CLI runs; no assigned test specifically covers this file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1391 `file` `packages/tui/test/chat-simple.ts`
- cursor: `[_]`
- core_role: TUI test/demo for simple chat rendering.
- algorithmic_behavior: Constructs a minimal chat UI scenario to exercise layout/rendering behavior.
- inputs_outputs_state: Inputs are sample chat messages/events; outputs are terminal render frames.
- gates_or_invariants: Basic chat components should render without layout corruption.
- dependencies_and_callers: Uses `packages/tui` components/rendering primitives.
- edge_cases_or_failure_modes: Terminal size assumptions and visual-only regressions.
- validation_or_tests: This file is a test/demo validation asset.
- skip_candidate: `yes: simple TUI fixture/demo rather than core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1421 `file` `packages/tui/test/latex-to-unicode.test.ts`
- cursor: `[_]`
- core_role: Regression suite for LaTeX/math-to-Unicode rendering.
- algorithmic_behavior: Tests ANSI color preservation, bare math environment detection, symbol replacements, and rendering math in text.
- inputs_outputs_state: Inputs are markdown/LaTeX strings with ANSI and math syntax; outputs are Unicode-rendered text.
- gates_or_invariants: ANSI scopes must survive conversion; bare math environments must be detected; symbol replacements must be stable.
- dependencies_and_callers: Targets TUI markdown/math rendering utilities.
- edge_cases_or_failure_modes: Nested ANSI, malformed LaTeX, bare environments, and unsupported symbols.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1451 `file` `packages/tui/test/slash-autocomplete-viewport.test.ts`
- cursor: `[_]`
- core_role: Regression suite for slash autocomplete viewport/repaint behavior.
- algorithmic_behavior: Tests popup layout and repaint behavior under viewport constraints and native terminal clear/ED3 risks.
- inputs_outputs_state: Inputs are slash command candidates and viewport sizes; outputs are render frames and cursor/viewport state.
- gates_or_invariants: Autocomplete must not corrupt scrollback or render outside viewport.
- dependencies_and_callers: Targets TUI autocomplete/list rendering.
- edge_cases_or_failure_modes: Unknown viewport, small terminals, native clear behavior, and resize/repaint races.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1481 `file` `packages/utils/src/abortable.ts`
- cursor: `[_]`
- core_role: Shared abort utilities for promises and streams.
- algorithmic_behavior: Defines `AbortError`, `createAbortableStream` that cancels a source reader and errors the controller on abort, and `untilAborted` using `Promise.withResolvers()` to resolve/reject on abort lifecycle.
- inputs_outputs_state: Inputs are streams, abort signals, and optional reasons; outputs are abort-aware streams/promises/errors.
- gates_or_invariants: Abort listeners must be cleaned up; source reader cancellation should occur once; abort reason should map consistently.
- dependencies_and_callers: Used by package utilities and long-running AI/tool streams.
- edge_cases_or_failure_modes: Already-aborted signals, stream cancellation errors, double abort, and listener leaks.
- validation_or_tests: Covered by abort-related tests in ai/coding-agent packages.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1511 `file` `packages/utils/src/temp.ts`
- cursor: `[_]`
- core_role: Shared temporary directory lifecycle utility.
- algorithmic_behavior: Wraps temp dir creation and cleanup with async/sync disposal and Windows retry behavior for `EBUSY`, `EPERM`, and `ENOTEMPTY`.
- inputs_outputs_state: Inputs are temp prefixes/paths and cleanup calls; outputs are filesystem temp dirs and removal side effects.
- gates_or_invariants: Cleanup should be idempotent and robust to transient Windows filesystem locks.
- dependencies_and_callers: Used by tests, tools, and runtime code needing temporary workspaces.
- edge_cases_or_failure_modes: Locked files, nested dirs, repeated cleanup, and process exit cleanup gaps.
- validation_or_tests: Covered indirectly by tests using temp utilities and platform-specific cleanup behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1541 `file` `python/omp-rpc/tests/__init__.py`
- cursor: `[_]`
- core_role: Python test package marker.
- algorithmic_behavior: No substantive algorithm; makes the tests directory importable as a package.
- inputs_outputs_state: No runtime inputs or outputs beyond Python import/package discovery.
- gates_or_invariants: Must remain valid Python.
- dependencies_and_callers: Used by Python test discovery/import machinery.
- edge_cases_or_failure_modes: Empty marker can be misclassified as core because it sits under tests.
- validation_or_tests: Test discovery only.
- skip_candidate: `yes: package marker with no core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1571 `file` `python/robomp/src/tasks.py`
- cursor: `[_]`
- core_role: Task entrypoint layer for Robomp GitHub issue/PR/comment/review workflows.
- algorithmic_behavior: Implements `triage_issue`, `review_pr`, `handle_comment`, `handle_review`, `handle_pr_conversation`, and `cleanup_workspace`; hydrates full issue/PR threads, maps PRs back to issues, decides whether to bootstrap/reopen/finalize, builds prompts/reminders, and gates direct PR work to safe bot-owned same-repo branches.
- inputs_outputs_state: Inputs are DB event payloads, GitHub issue/PR/comment/review data, repository sandbox state, worker/model output, and host tools; outputs are GitHub comments/reviews/PR updates, DB state changes, worker prompts, and cleanup actions.
- gates_or_invariants: Maintainer/bot directives and PR ownership checks determine task route; finalized issues can be reopened only under allowed triggers; direct PR handling is restricted for safety.
- dependencies_and_callers: Called by `worker.py`/queue execution; depends on GitHub client, DB, host tools, sandbox/workspace, and prompt/persona utilities.
- edge_cases_or_failure_modes: Missing issue/PR mapping, deleted comments, closed/finalized issues, non-bot PR branches, dirty workspace cleanup, and visual inspection flagged a possible stray parenthesis near a close-PR skip path requiring parser validation.
- validation_or_tests: Covered by Robomp tests and live webhook/manual trigger scenarios.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1601 `directory` `packages/ai/src/utils/schema`
- cursor: `[_]`
- core_role: Provider-compatible JSON Schema normalization, validation, and tool-parameter wire conversion.
- algorithmic_behavior: `wire.ts` converts Zod/ArkType/JSON Schema to provider wire schemas; `draft.ts` upgrades old drafts; `dereference.ts` resolves refs; `normalize.ts` strips/renames fields, collapses nullable/combiner shapes, normalizes for Google/CCA/MCP/Moonshot/OpenAI Responses, and enforces OpenAI strict mode; `compatibility.ts` audits provider rules; `strict-tool-validation.ts` quarantines enum/const/type contradictions; `fields.ts`, `spill.ts`, `stamps.ts`, `equality.ts`, `typescript.ts`, `zod-decontaminate.ts`, and validators provide support.
- inputs_outputs_state: Inputs are tool parameter schemas from Zod, ArkType, TypeBox/plain JSON, MCP, or extensions; outputs are normalized JSON Schema objects, strict-mode schemas, compatibility violations, or fallback schemas.
- gates_or_invariants: Avoid cycles, preserve literal enum/default data, only recurse into schema-valued positions, strip provider-forbidden fields, require strict object `additionalProperties:false`/`required`, and fail open/fallback when residual incompatibilities remain.
- dependencies_and_callers: Used by pi-ai provider request builders, tool inventory, OpenAI/Google/Anthropic-compatible clients, MCP tool registration, and tests.
- edge_cases_or_failure_modes: Circular schemas, JSON-roundtripped Zod impostors, ArkType AST variants, nullable unions, nested/pure `anyOf`, `$ref` siblings, unsupported regex lookarounds, schema maps, and enum/type contradictions.
- validation_or_tests: Covered by OpenAI tool strict mode, OpenAI compatibility, provider schema, and tool inventory tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1631 `directory` `packages/coding-agent/src/modes/acp`
- cursor: `[_]`
- core_role: Agent Client Protocol mode implementation for editor/agent integrations.
- algorithmic_behavior: `acp-mode.ts` opens stdio JSON-RPC connection; `acp-agent.ts` implements initialize/auth/session CRUD/list/resume/fork/close, mode/config updates, prompt queueing, cancellation cleanup, extension elicitation, slash/skill/builtin command handling, MCP config, replay/bootstrap notifications, usage, and extension methods; `acp-event-mapper.ts` maps agent events/tools/todos/diffs/resources/terminal content to ACP session updates; `acp-client-bridge.ts` routes editor FS/terminal/permission calls; `terminal-auth.ts` handles auth flag.
- inputs_outputs_state: Inputs are ACP JSON-RPC requests, client capabilities, prompts/resources/images, session IDs/cwd, MCP servers, model/thinking options, and agent events; outputs are ACP responses/session notifications, session files, tool updates, plan updates, and elicitation requests.
- gates_or_invariants: cwd must be absolute; prompt turns are serialized; cancel occupies the turn until abort cleanup finishes; fork is blocked while a prompt is in flight; bootstrap updates are delayed to avoid client races; read-only/local command sets are enforced where applicable.
- dependencies_and_callers: Used by `omp acp`/editor integrations; depends on AgentSession, SessionManager, MCPManager, extensions, slash commands, workflow runtime, plan mode, settings, and ACP SDK.
- edge_cases_or_failure_modes: Client notification race, cancel timeout, late async job deliveries, session closed while queued, prompt resource conversion, unsupported auth/config/mode IDs, replay of tool args, and stale live message IDs.
- validation_or_tests: Assigned tests cover ACP internal URLs/protocol, approved plan, session storage/listing, and command/tool mapping behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1661 `directory` `packages/stats/src/client/ui`
- cursor: `[_]`
- core_role: Shared React UI primitives for the stats dashboard.
- algorithmic_behavior: Components such as `AsyncBoundary`, `DataTable`, `EmptyState`, `ErrorState`, `JsonBlock`, `MetricCluster`, `Panel`, `RequestDrawer`, `SegmentedControl`, `Skeleton`, and `StatusPill` implement dashboard display, loading/error boundaries, formatting, and interaction controls.
- inputs_outputs_state: Inputs are React props, fetched stats data, errors, selected segments, and JSON payloads; outputs are rendered DOM UI state.
- gates_or_invariants: Components should handle loading/error/empty states and avoid crashing on malformed display data.
- dependencies_and_callers: Used by stats client pages and hooks.
- edge_cases_or_failure_modes: Very large JSON, empty datasets, narrow layouts, and invalid status values.
- validation_or_tests: UI is validated by dashboard tests/manual rendering; this directory is mostly presentational.
- skip_candidate: `yes: presentational dashboard UI, not a core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1691 `file` `packages/ai/src/auth-broker/server.ts`
- cursor: `[_]`
- core_role: Local/remote auth broker HTTP/SSE server for credential snapshots and operations.
- algorithmic_behavior: Serves bearer-protected health, snapshot long-poll with ETag/generation waits, snapshot SSE stream with keepalive and entry/removed events, usage reporting, refresh/disable/upload routes, and generation gate scheduling.
- inputs_outputs_state: Inputs are HTTP requests, bearer tokens, auth storage snapshots, credential changes, usage data, and refresher schedules; outputs are JSON snapshots, SSE events, refresh/disable/upload side effects, and HTTP errors.
- gates_or_invariants: Bearer auth protects endpoints; snapshot generation/ETag drives caching and long-poll; SSE must clean listeners on close; refresh scheduling computes `rotatesInMs`.
- dependencies_and_callers: Used by auth storage broker clients and SDK sessions; depends on AuthStorage, usage store, HTTP server, and logger.
- edge_cases_or_failure_modes: Long-poll timeout, disconnected SSE clients, stale ETags, auth failure, malformed upload, refresh errors, and visual inspection flagged a duplicated parameter in one helper signature worth type-check validation.
- validation_or_tests: Covered by auth-broker wire/cache/remote-store tests in the ai package.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1721 `file` `packages/ai/src/dialect/xml.ts`
- cursor: `[_]`
- core_role: XML in-band tool/thinking dialect adapter.
- algorithmic_behavior: Selects Anthropic or DeepSeek-style XML tagsets, scans model output for invocations/thinking, and renders tool transcript blocks such as `<invoke>` and `<parameter>`.
- inputs_outputs_state: Inputs are assistant text/tool calls and dialect selection; outputs are parsed tool-call structures or XML transcript strings.
- gates_or_invariants: Must preserve parameter text escaping/structure and identify only supported tags for the selected dialect.
- dependencies_and_callers: Used by AI provider adapters that support XML/in-band tool calling.
- edge_cases_or_failure_modes: Malformed XML, nested tags, partial streaming output, and dialect mismatch.
- validation_or_tests: Covered by provider/tool-call tests that exercise XML-compatible models.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1751 `file` `packages/ai/src/providers/openai-codex-responses.ts`
- cursor: `[_]`
- core_role: OpenAI Codex Responses provider implementation with SSE/WebSocket streaming and recovery.
- algorithmic_behavior: Builds Responses requests from model context, strips unsupported max-token fields, applies service tier/reasoning/tool-choice/schema policies, chooses WebSocket when supported, falls back to SSE on fatal/retry-budget transport errors, streams output items/reasoning/text/tool args, detects whitespace tool loops, recovers previous-response-not-found/provider retryable errors, tracks turn state for tool continuations, and finalizes usage/pricing/service tier data.
- inputs_outputs_state: Inputs are model messages, tools, options, previous response state, abort signals, HTTP/WebSocket events, and provider errors; outputs are streamed agent content blocks, tool calls, usage, retry/fallback state, and provider errors.
- gates_or_invariants: Caller abort and internal idle/first-event timeouts are combined; tool args are keyed by item id/output index; only continuation turns carry previous response state; WebSocket queue/ping/close state must stay ordered; retryable errors are classified narrowly.
- dependencies_and_callers: Used by pi-ai model registry/provider runtime and coding-agent sessions; depends on schema normalization, OpenAI compatibility policy, usage/pricing, WebSocket/SSE clients, and auth.
- edge_cases_or_failure_modes: Whitespace-loop retries, dropped terminal events, reconnect/fallback, malformed event payloads, previous response expiry, provider error streams, tool arg deltas arriving without IDs, and usage finalization after failure.
- validation_or_tests: Covered by OpenAI compat/policy, strict tool schema, abort, pi-native/client, and issue regression tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1781 `file` `packages/ai/src/registry/google-gemini-cli.ts`
- cursor: `[_]`
- core_role: Registry descriptor/adapter for Google Gemini CLI provider integration.
- algorithmic_behavior: Defines provider registration metadata or discovery hook for Gemini CLI-backed models.
- inputs_outputs_state: Inputs are registry/provider initialization data; outputs are provider descriptor entries consumed by model registry.
- gates_or_invariants: Provider ID and model metadata must match registry expectations.
- dependencies_and_callers: Used by `packages/ai/src/registry/registry.ts` provider assembly.
- edge_cases_or_failure_modes: Missing external CLI, provider ID drift, and incomplete capability metadata.
- validation_or_tests: Covered indirectly by registry/model resolution tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1811 `file` `packages/ai/src/registry/registry.ts`
- cursor: `[_]`
- core_role: Provider registry assembly for pi-ai.
- algorithmic_behavior: Collects provider descriptors, exposes lookup/list behavior, and coordinates provider registration for auth/model selection.
- inputs_outputs_state: Inputs are built-in provider modules and registry query keys; outputs are provider descriptors/clients for runtime use.
- gates_or_invariants: Provider IDs must be unique and descriptors must be available before model resolution.
- dependencies_and_callers: Called by model registry, coding-agent SDK, and provider-specific clients.
- edge_cases_or_failure_modes: Duplicate IDs, missing provider modules, and stale descriptors.
- validation_or_tests: Covered by provider registry/catalog tests and runtime model resolution tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1841 `file` `packages/ai/src/usage/zai.ts`
- cursor: `[_]`
- core_role: Z.AI usage/quota fetch and parsing helper.
- algorithmic_behavior: Calls Z.AI usage endpoints, parses token/request limits, status thresholds, and optional model usage metadata into internal usage report structures.
- inputs_outputs_state: Inputs are API keys/fetch responses; outputs are quota/usage records and status classifications.
- gates_or_invariants: Missing/invalid fields should degrade gracefully; thresholds must map consistently to usage state.
- dependencies_and_callers: Used by usage reporting for Z.AI provider and auth/model UI.
- edge_cases_or_failure_modes: HTTP errors, changed response shape, missing model metadata, exhausted quota, and parse failures.
- validation_or_tests: Covered indirectly by usage/provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1871 `file` `packages/catalog/src/discovery/codex.ts`
- cursor: `[_]`
- core_role: Codex model discovery and normalization for the catalog.
- algorithmic_behavior: Fetches `/codex/models` with fallback to `/models`, fetches client version fallback metadata, normalizes entries into `ModelSpec` with reasoning/input/default limits, priority, websocket preference, and provider-specific metadata.
- inputs_outputs_state: Inputs are Codex API model responses and optional NPM/client metadata; outputs are catalog model specs.
- gates_or_invariants: Discovery must tolerate missing endpoints and normalize IDs/limits consistently; generated catalog should not be hand-edited.
- dependencies_and_callers: Called by catalog generation/discovery scripts and provider descriptors.
- edge_cases_or_failure_modes: Endpoint unavailable, malformed model entries, missing limits, model renames, and visual inspection flagged a duplicated local declaration line worth check validation.
- validation_or_tests: Covered by catalog/provider discovery tests and generated model checks.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1901 `file` `packages/coding-agent/src/advisor/watchdog.ts`
- cursor: `[_]`
- core_role: Watchdog instruction discovery for advisor behavior.
- algorithmic_behavior: Discovers user/project `WATCHDOG.md`, expands `@` imports, and sorts instructions user-first then project ancestors from root to leaf.
- inputs_outputs_state: Inputs are cwd, filesystem watchdog files, and import references; outputs are ordered watchdog content/messages.
- gates_or_invariants: Imported files must be resolved safely and order must be deterministic.
- dependencies_and_callers: Used by advisor/session creation in `sdk.ts`.
- edge_cases_or_failure_modes: Missing files, circular imports, broken `@` references, and ancestor ordering mistakes.
- validation_or_tests: Covered indirectly by advisor/context tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1931 `file` `packages/coding-agent/src/capability/types.ts`
- cursor: `[_]`
- core_role: Type contract for capability provider discovery and validation.
- algorithmic_behavior: Defines provider capability records, sources, priorities, deduplication/validation metadata, and extension points.
- inputs_outputs_state: Inputs are provider/extension capability declarations; outputs are typed capability objects consumed by registry/discovery code.
- gates_or_invariants: Capability IDs/source metadata must be stable for priority and dedup behavior.
- dependencies_and_callers: Used by capability registry, extension discovery, and provider enable/disable paths.
- edge_cases_or_failure_modes: Type-only file can be misclassified, but wrong contracts still break runtime integration.
- validation_or_tests: Compile/type checking and capability-related tests validate this contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1961 `file` `packages/coding-agent/src/cli/stats-cli.ts`
- cursor: `[_]`
- core_role: CLI command implementation for stats dashboard/server operations.
- algorithmic_behavior: Parses stats CLI options, starts or communicates with stats service, and routes dashboard/status behavior.
- inputs_outputs_state: Inputs are CLI args/settings/env and existing stats service state; outputs are server process/status URLs or terminal messages.
- gates_or_invariants: Must avoid conflicting ports/processes and respect configured paths.
- dependencies_and_callers: Used by coding-agent CLI command registry; depends on stats package server/client utilities.
- edge_cases_or_failure_modes: Port in use, stale process, missing browser/server assets, and invalid args.
- validation_or_tests: Covered indirectly by CLI/stats tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1991 `file` `packages/coding-agent/src/commands/plugin.ts`
- cursor: `[_]`
- core_role: Plugin command routing for coding-agent CLI/slash command surface.
- algorithmic_behavior: Dispatches plugin-related operations such as install/list/update/remove or registry actions to plugin helpers.
- inputs_outputs_state: Inputs are command args and plugin registry/config state; outputs are plugin registry mutations and user-facing command results.
- gates_or_invariants: Plugin names/paths must be validated and command errors surfaced clearly.
- dependencies_and_callers: Called by CLI/slash command command registry; depends on extensibility/plugin install modules.
- edge_cases_or_failure_modes: Invalid local path, duplicate plugin, missing registry, and install failure.
- validation_or_tests: Covered by `plugin-install-local.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2021 `file` `packages/coding-agent/src/config/model-resolver.ts`
- cursor: `[_]`
- core_role: Model selector matching and resolution engine for coding-agent.
- algorithmic_behavior: Resolves CLI/settings/session model selectors using exact provider/id matches, canonical IDs, bare ID matches, aliases, retired names, provider fuzzy/substring/date ranking, `:thinking` suffixes, `@upstream` routing for supported providers, role aliases like `pi/default`, enabled-model filters, and auth fallback for subagents.
- inputs_outputs_state: Inputs are selectors, available models, settings/defaults, provider auth status, session model metadata, and enabled scopes; outputs are resolved model/API/thinking/service-tier selections or structured errors.
- gates_or_invariants: Catalog import conventions and provider identity must be respected; enabled-model filters constrain results; thinking suffixes and upstream routing are parsed only where valid.
- dependencies_and_callers: Used by `sdk.ts`, CLI model flags, settings UI, subagent/model role resolution, and catalog/model registry.
- edge_cases_or_failure_modes: Ambiguous selectors, retired aliases, unavailable credentials, duplicate model IDs across providers, unsupported upstream suffix, and visual inspection showed a duplicated filter line needing type-check confirmation.
- validation_or_tests: Covered by model resolver, provider/catalog, and session restore tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2051 `file` `packages/coding-agent/src/discovery/claude.ts`
- cursor: `[_]`
- core_role: Discovery adapter for Claude-related local/remote provider configuration.
- algorithmic_behavior: Discovers Claude installations/configs/credentials/models and maps them into coding-agent provider/model availability.
- inputs_outputs_state: Inputs are filesystem config, env, external CLI state, and catalog descriptors; outputs are discovered provider/model entries or auth hints.
- gates_or_invariants: Discovery must avoid leaking secrets and must tolerate missing Claude installations.
- dependencies_and_callers: Used by model discovery and SDK session startup.
- edge_cases_or_failure_modes: Changed Claude config layout, missing CLI, malformed credential files, and stale discovered entries.
- validation_or_tests: Covered by discovery tests and provider auth/model resolution tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2081 `file` `packages/coding-agent/src/eval/concurrency-bridge.ts`
- cursor: `[_]`
- core_role: Bridge from task settings to eval concurrency limits.
- algorithmic_behavior: Reads `task.maxConcurrency`; returns parallel/pipeline limit, with `0` treated as unbounded.
- inputs_outputs_state: Inputs are settings/session values; outputs are numeric concurrency limits for eval/task execution.
- gates_or_invariants: Limit mapping must be deterministic and preserve unbounded semantics.
- dependencies_and_callers: Used by eval runtime/pipeline execution.
- edge_cases_or_failure_modes: Undefined/invalid setting, `0` unbounded, and negative/non-number values if not sanitized upstream.
- validation_or_tests: Covered indirectly by eval/task concurrency tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2111 `file` `packages/coding-agent/src/hindsight/content.ts`
- cursor: `[_]`
- core_role: Content preparation for hindsight/memory recall and retention.
- algorithmic_behavior: Strips memory tags, formats current memories/time, builds/truncates recall queries, and prepares transcript content for retention.
- inputs_outputs_state: Inputs are conversation transcript, memory snippets, timestamps, and token/length limits; outputs are prompt-ready recall/retention text blocks.
- gates_or_invariants: Memory tags must not leak into model-visible text incorrectly; recall queries must be bounded.
- dependencies_and_callers: Used by memory backend/autolearn/hindsight integration in coding-agent sessions.
- edge_cases_or_failure_modes: Empty transcript, huge transcript, malformed memory tags, and truncation losing important context.
- validation_or_tests: Covered indirectly by memory/hindsight tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2141 `file` `packages/coding-agent/src/lsp/index.ts`
- cursor: `[_]`
- core_role: Language-server integration and LSP tool implementation.
- algorithmic_behavior: Manages LSP warmup, client creation, file refresh/open/save sync, diagnostics freshness, formatting, rename/file actions, hover/references, writethrough batching, deferred late diagnostics, status rendering, and linter fallback.
- inputs_outputs_state: Inputs are tool params, files, cwd, server configs, LSP/linter diagnostics, abort/timeout signals, and batch requests; outputs are tool results, formatted diagnostics, file writes, LSP edits, and deferred diagnostic events.
- gates_or_invariants: Diagnostics capture min versions before sync and wait for exact document version or settled unversioned publish; status distinguishes configured vs started servers; write-through has timeout fallback; readonly/write actions are permission-classified.
- dependencies_and_callers: Used by LSP tool, edit/hashline filesystem, SDK warmup, and TUI renderers; depends on server config, `lspmux`, filesystem, and diagnostics formatters.
- edge_cases_or_failure_modes: Server startup failure, stale diagnostics, unversioned servers, formatter errors, batch flush timing, rename destination conflicts, and late diagnostics after tool completion.
- validation_or_tests: Covered by LSP/edit writethrough benches and coding-agent LSP/edit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2171 `file` `packages/coding-agent/src/memory-backend/index.ts`
- cursor: `[_]`
- core_role: Memory backend barrel/entry contract.
- algorithmic_behavior: Re-exports or selects memory backend implementations for session use.
- inputs_outputs_state: Inputs are imports from session startup; outputs are memory backend API exports.
- gates_or_invariants: Export surface must remain stable for `sdk.ts` and memory consumers.
- dependencies_and_callers: Called by SDK/session memory initialization.
- edge_cases_or_failure_modes: Barrel drift or missing export breaks memory startup.
- validation_or_tests: Covered by compile/type checks and memory integration tests.
- skip_candidate: `yes: thin barrel/entry file with minimal algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-2201 `file` `packages/coding-agent/src/modes/workflow.ts`
- cursor: `[_]`
- core_role: Workflow-mode keyword/highlight integration for the TUI.
- algorithmic_behavior: Detects the workflow trigger word, uses prose-aware keyword detection, applies highlighter styling, and imports/render workflow notice behavior.
- inputs_outputs_state: Inputs are user input text and theme/highlight context; outputs are workflow-mode detection and display styling.
- gates_or_invariants: Trigger should avoid false positives inside ordinary prose where `keywordInProse` rules exclude it.
- dependencies_and_callers: Used by interactive modes and workflow notice components.
- edge_cases_or_failure_modes: False trigger in prose/code, case/spacing variants, and theme styling issues.
- validation_or_tests: Covered indirectly by mode/render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2231 `file` `packages/coding-agent/src/session/session-paths.ts`
- cursor: `[_]`
- core_role: Managed session path construction, migration, and breadcrumb handling.
- algorithmic_behavior: Computes session storage paths, handles legacy/current layout migration, session breadcrumbs/subagent paths, and safe path derivation for listing/resume.
- inputs_outputs_state: Inputs are config root, cwd/session metadata, IDs, and legacy files; outputs are managed session file paths and migration side effects.
- gates_or_invariants: Paths must be deterministic, avoid collisions, preserve legacy sessions, and not leak/overwrite unrelated files.
- dependencies_and_callers: Used by `SessionManager`, session listing, resume/continue, and subagent breadcrumb tests.
- edge_cases_or_failure_modes: Relocated cwd, legacy path conflicts, invalid IDs, missing dirs, and concurrent migration.
- validation_or_tests: Covered by `packages/coding-agent/test/session-manager/*`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2261 `file` `packages/coding-agent/src/stt/transcriber.ts`
- cursor: `[_]`
- core_role: Speech-to-text transcription adapter.
- algorithmic_behavior: Resolves STT model, decodes WAV mono 16k input, calls ASR runtime with timeout, and logs/fails cleanly on unavailable model or decode errors.
- inputs_outputs_state: Inputs are audio files/buffers, STT settings/model cache, timeout/abort; outputs are transcribed text or errors.
- gates_or_invariants: Audio format/model availability must be validated before transcription; timeouts prevent hanging.
- dependencies_and_callers: Used by coding-agent voice/STT controller; depends on model cache and ASR backend.
- edge_cases_or_failure_modes: Unsupported audio format, missing cached model, long audio timeout, ASR failure, and empty transcript.
- validation_or_tests: Covered by STT preflight tests outside this assigned subset and related runtime tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2291 `file` `packages/coding-agent/src/tools/auto-generated-guard.ts`
- cursor: `[_]`
- core_role: Guard preventing edits to generated files.
- algorithmic_behavior: Detects generated files from header content in first bytes/lines and filename patterns, caches stat markers, and throws `ToolError` on protected edit attempts.
- inputs_outputs_state: Inputs are file paths, stat info, and file content previews; outputs are allow/deny decisions and tool errors.
- gates_or_invariants: Generated lockfiles/model JSON/etc. should be blocked consistently; cache must invalidate when stats change.
- dependencies_and_callers: Used by edit/write/hashline filesystem and tools.
- edge_cases_or_failure_modes: Generated marker after scan window, false positives in comments, stale cache, and binary/large files.
- validation_or_tests: Covered by edit/tool tests and generated-file guard tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2321 `file` `packages/coding-agent/src/tools/irc.ts`
- cursor: `[_]`
- core_role: Agent-to-agent messaging tool and renderer.
- algorithmic_behavior: Exposes `list`, `send`, `wait`, and `inbox` over process-global `IrcBus`; enables only when peers can exist; direct sends can wake/revive/inject, broadcasts target live visible peers, awaited sends wait for replies with abort/timeout cleanup, inbox can peek/drain, and renderer formats live cards/results with truncation and status badges.
- inputs_outputs_state: Inputs are tool params, sender ID, agent registry, bus messages, timeout settings, and abort signals; outputs are delivery receipts, waited messages, inbox lists, peer lists, useless/error flags, and TUI cards.
- gates_or_invariants: Cannot send to self; `to`/`message` are required; `await` is invalid for broadcast; negative/non-finite timeouts fall back; subagent/top-level availability mirrors task recursion capacity.
- dependencies_and_callers: Uses `IrcBus`, `AgentRegistry`, task depth rules, settings, tool renderer utilities, and TUI theme.
- edge_cases_or_failure_modes: No peers, failed recipient, parked/busy recipients, await timeout, abort during wait, empty inbox, and long multiline messages.
- validation_or_tests: Covered by `packages/coding-agent/test/tools/irc-renderer.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2351 `file` `packages/coding-agent/src/tools/tool-errors.ts`
- cursor: `[_]`
- core_role: Shared structured error type(s) for tools.
- algorithmic_behavior: Defines/exports tool error classes or helpers used to signal controlled tool failures distinct from crashes.
- inputs_outputs_state: Inputs are error messages/details; outputs are typed errors consumed by tool execution/rendering.
- gates_or_invariants: Tool errors should preserve user-safe messages and machine-readable classification.
- dependencies_and_callers: Used by auto-generated guard, tool runtimes, renderers, and execution controller.
- edge_cases_or_failure_modes: Misclassified errors can render as crashes or hide actionable diagnostics.
- validation_or_tests: Covered indirectly by tool error/render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2381 `file` `packages/coding-agent/src/utils/command-args.ts`
- cursor: `[_]`
- core_role: Lightweight command argument parser/substituter.
- algorithmic_behavior: Parses quote-aware argument strings and substitutes `$1`, `$@`, `$@[start:length]`, and `$ARGUMENTS` placeholders.
- inputs_outputs_state: Inputs are raw command text and argument arrays; outputs are parsed args or substituted command strings.
- gates_or_invariants: Quoted segments should stay grouped and placeholder ranges should be deterministic.
- dependencies_and_callers: Used by slash/custom command execution.
- edge_cases_or_failure_modes: Unclosed quotes, escaped quotes, empty args, out-of-range slices, and literal dollar text.
- validation_or_tests: Covered by command/slash tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2411 `file` `packages/coding-agent/src/workflow/change-request-file.ts`
- cursor: `[_]`
- core_role: Strict parser/validator for workflow graph change request JSON files.
- algorithmic_behavior: Parses metadata, origins, frontier mapping, and operations such as add/remove node/edge, replace edge condition, replace node prompt/model/permissions, set model role, abandon/rollback branch; validates node types, prompt sources, template bindings, script source/language/timeout, model contexts, JSON pointers, and non-empty strings.
- inputs_outputs_state: Inputs are unknown JSON values plus file path labels; outputs are typed `WorkflowChangeRequestFile` objects or path-specific errors.
- gates_or_invariants: Exactly one prompt/source variant is allowed; prompt and promptSource cannot both be defined; script requires exactly one inline/code/file source; model context requires exactly one role/selector/candidates; timeouts are bounded.
- dependencies_and_callers: Used by workflow lifecycle/patch application and slash/external workflow change mechanisms.
- edge_cases_or_failure_modes: Unsupported op, malformed nested path, empty candidates, non-pointer paths, conflicting `condition`/`when`, and invalid origin.
- validation_or_tests: Covered by workflow/plan-mode tests and parser callers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2441 `file` `packages/coding-agent/src/workflow/task-tool-runtime.ts`
- cursor: `[_]`
- core_role: Adapter from workflow agent nodes to task tool runtime.
- algorithmic_behavior: Converts workflow node execution into `TaskTool` calls, disables async for workflow tasks, and extracts the final non-aborted yield data for workflow continuation.
- inputs_outputs_state: Inputs are workflow node/task parameters and agent task yields; outputs are workflow node results or failures.
- gates_or_invariants: Workflow task calls should not detach asynchronously; aborted yields are filtered from final result.
- dependencies_and_callers: Used by workflow session runtime and task tool.
- edge_cases_or_failure_modes: Empty yields, aborted task, nested task failures, and async behavior mismatches.
- validation_or_tests: Covered by workflow/task render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2471 `file` `packages/coding-agent/test/core/python-executor.result.test.ts`
- cursor: `[_]`
- core_role: Regression spec for Python executor result shaping.
- algorithmic_behavior: Tests conversion of Python execution outcomes into tool/result structures.
- inputs_outputs_state: Inputs are simulated Python stdout/stderr/exit/error payloads; outputs are normalized executor results.
- gates_or_invariants: Exit status, output, and error fields must map predictably.
- dependencies_and_callers: Targets coding-agent core Python executor/eval path.
- edge_cases_or_failure_modes: Nonzero exit, stderr-only output, timeout/abort, and malformed result.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2501 `file` `packages/coding-agent/test/discovery/mcp-profile.test.ts`
- cursor: `[_]`
- core_role: Regression spec for MCP profile discovery.
- algorithmic_behavior: Tests discovery/selection of MCP profiles and resulting server configuration.
- inputs_outputs_state: Inputs are profile config fixtures and cwd/settings; outputs are resolved MCP server maps/sources.
- gates_or_invariants: Profile precedence and project/user scoping must be deterministic.
- dependencies_and_callers: Targets MCP discovery helpers used by SDK/ACP.
- edge_cases_or_failure_modes: Missing profile, duplicate server names, disabled profile, and malformed config.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2531 `file` `packages/coding-agent/test/internal-urls/agent-protocol.test.ts`
- cursor: `[_]`
- core_role: Regression spec for internal agent URL/protocol resolution.
- algorithmic_behavior: Tests parsing or routing internal URLs used by agent/protocol features.
- inputs_outputs_state: Inputs are internal URL strings; outputs are resolved paths/actions or errors.
- gates_or_invariants: Only supported internal schemes/routes should resolve; malformed URLs should fail safely.
- dependencies_and_callers: Targets internal URL utilities used by ACP/editor/resource links.
- edge_cases_or_failure_modes: Encoded paths, unsupported scheme, missing segments, and path traversal.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2561 `file` `packages/coding-agent/test/plan-mode/approved-plan.test.ts`
- cursor: `[_]`
- core_role: Regression suite for approved plan resolution.
- algorithmic_behavior: Tests plan slug/title matching, approved plan lookup, validation, and failure cases.
- inputs_outputs_state: Inputs are plan files/metadata and approval requests; outputs are resolved `PlanApprovalDetails` or errors.
- gates_or_invariants: Only approved/valid plans should execute; title/slug resolution must be stable.
- dependencies_and_callers: Targets plan mode approval logic used by ACP and TUI plan execution.
- edge_cases_or_failure_modes: Duplicate titles, invalid slug, missing file, and stale approval state.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2591 `file` `packages/coding-agent/test/session/sql-session-storage.test.ts`
- cursor: `[_]`
- core_role: Regression suite for SQL-backed session storage.
- algorithmic_behavior: Tests persistence, listing, loading, ordering, and migration/compatibility behavior for session storage.
- inputs_outputs_state: Inputs are temp SQL stores and session entries; outputs are stored/retrieved session data and metadata.
- gates_or_invariants: Session storage must preserve append order, metadata, and compatibility with listing/resume.
- dependencies_and_callers: Targets SQL session storage backend and SessionManager integration.
- edge_cases_or_failure_modes: Corrupt rows, missing metadata, concurrent writes, and migration changes.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2621 `file` `packages/coding-agent/test/task/render-nested-live.test.ts`
- cursor: `[_]`
- core_role: Regression suite for nested live task rendering.
- algorithmic_behavior: Tests rendering of nested task/subagent live states and updates.
- inputs_outputs_state: Inputs are task lifecycle/progress events; outputs are TUI render lines/cards.
- gates_or_invariants: Nested live tasks should not overlap, duplicate, or lose hierarchy.
- dependencies_and_callers: Targets task renderer and event bus integration.
- edge_cases_or_failure_modes: Rapid updates, collapsed/expanded views, task completion while child active, and render truncation.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2651 `file` `packages/coding-agent/test/tools/browser-cmux-observation.test.ts`
- cursor: `[_]`
- core_role: Regression spec for browser/cmux observation tool behavior.
- algorithmic_behavior: Tests browser observation output or state mapping through cmux integration.
- inputs_outputs_state: Inputs are simulated browser/cmux observations; outputs are normalized tool observations/render text.
- gates_or_invariants: Browser state must be summarized without losing relevant content.
- dependencies_and_callers: Targets browser tool observation layer.
- edge_cases_or_failure_modes: Empty page, missing observation fields, malformed cmux response, and large text.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2681 `file` `packages/coding-agent/test/tools/irc-renderer.test.ts`
- cursor: `[_]`
- core_role: Regression suite for IRC tool rendering.
- algorithmic_behavior: Tests send/wait/inbox/list renderers, receipt statuses, body truncation, timeout messages, peer sorting, and display cards.
- inputs_outputs_state: Inputs are IRC tool args/results/details and themes; outputs are rendered TUI text/components.
- gates_or_invariants: Renderer must sanitize tabs, truncate long content, show errors/timeouts clearly, and preserve peer/message metadata.
- dependencies_and_callers: Targets `packages/coding-agent/src/tools/irc.ts`.
- edge_cases_or_failure_modes: Empty inbox, broadcast failures, multiple receipts, read replies, and long multiline messages.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2711 `file` `packages/coding-agent/test/tools/search-path-lists.test.ts`
- cursor: `[_]`
- core_role: Regression suite for tool path-list parsing across search/read/edit tools.
- algorithmic_behavior: Tests array, delimited, quoted, spaced, and renderer path handling across search/read/ast_grep/ast_edit/find/grep paths.
- inputs_outputs_state: Inputs are tool args with path lists in many formats; outputs are normalized path arrays and rendered previews.
- gates_or_invariants: Paths with spaces/quotes must survive parsing; arrays and delimited strings must converge; renderers must show consistent sanitized paths.
- dependencies_and_callers: Targets search/read/AST/grep tool input normalization and renderers.
- edge_cases_or_failure_modes: Commas/spaces inside paths, empty entries, mixed absolute/relative paths, and shell-like quotes.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2741 `file` `packages/coding-agent/test/utils/image-vision-fallback.test.ts`
- cursor: `[_]`
- core_role: Regression spec for image vision model fallback.
- algorithmic_behavior: Tests choosing a vision-capable model or fallback path when current model lacks image support.
- inputs_outputs_state: Inputs are model capability fixtures and image requests; outputs are selected model/fallback decisions.
- gates_or_invariants: Image prompts must not be sent to unsupported models without fallback/error.
- dependencies_and_callers: Targets inspect image/image utility model selection.
- edge_cases_or_failure_modes: No vision models, disabled credentials, preferred model unavailable, and mixed text/image requests.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2771 `file` `packages/collab-web/src/lib/client.ts`
- cursor: `[_]`
- core_role: Browser-side guest client for collab web sessions.
- algorithmic_behavior: Manages connection phases, welcome/transcript timeouts, notices, active tools, guest snapshot state, prompt/abort/agent command sends, and frame application from the relay.
- inputs_outputs_state: Inputs are collab links, WebSocket frames, user prompts/actions, transcript offsets, and timers; outputs are React-consumable guest snapshots, notices, pending transcript promises, and sealed frames.
- gates_or_invariants: Welcome must arrive within timeout; transcript requests time out; notices are capped; connection phase transitions must be monotonic enough for UI.
- dependencies_and_callers: Used by collab web React components and `packages/wire`/collab protocol.
- edge_cases_or_failure_modes: Read-only links, host disconnect, bad key, transcript timeout, reconnect, and large notice/tool lists.
- validation_or_tests: Covered by collab web/manual integration; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2801 `file` `packages/mnemopi/src/core/local-llm.ts`
- cursor: `[_]`
- core_role: Local LLM summarization backend selection for memory.
- algorithmic_behavior: Resolves runtime/env/custom/pi-ai/host backend configuration, builds summarization prompts, cleans model output, and applies fallback ordering.
- inputs_outputs_state: Inputs are text/memory content, local LLM settings/env, backend availability, and prompt parameters; outputs are summaries or fallback responses.
- gates_or_invariants: Backend fallback must be deterministic; output cleanup should remove wrapper noise without deleting content.
- dependencies_and_callers: Used by mnemopi consolidation/recall summarization.
- edge_cases_or_failure_modes: Missing local backend, empty output, timeout/failure, malformed config, and overlong inputs.
- validation_or_tests: Covered by mnemopi local-LLM tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2831 `file` `packages/mnemopi/src/util/regex.ts`
- cursor: `[_]`
- core_role: Text/token regex utilities for memory recall/fact relevance.
- algorithmic_behavior: Tokenizes recall/fact text, filters stopwords, handles synonyms/CJK terms, and computes relevance thresholds.
- inputs_outputs_state: Inputs are query/memory strings; outputs are normalized tokens/terms and relevance decisions.
- gates_or_invariants: Stopword filtering and CJK handling must not erase meaningful identity/fact terms.
- dependencies_and_callers: Used by mnemopi recall/consolidation logic.
- edge_cases_or_failure_modes: Mixed-language text, punctuation-heavy facts, short queries, and synonym overmatching.
- validation_or_tests: Covered by recall precision and multilingual memory tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2861 `file` `packages/utils/test/mermaid/golden.test.ts`
- cursor: `[_]`
- core_role: Golden regression suite for Mermaid ASCII/rendering conversion.
- algorithmic_behavior: Compares rendered Mermaid outputs against golden fixtures.
- inputs_outputs_state: Inputs are Mermaid diagram fixtures; outputs are ASCII/rendered text snapshots.
- gates_or_invariants: Rendering must remain stable for supported diagram shapes.
- dependencies_and_callers: Targets utility Mermaid renderer/vendor code.
- edge_cases_or_failure_modes: Layout drift, unsupported shapes, text overflow, and platform width differences.
- validation_or_tests: This file is direct golden validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2891 `directory` `packages/coding-agent/src/modes/theme/defaults`
- cursor: `[_]`
- core_role: Built-in theme preset catalog for coding-agent TUI.
- algorithmic_behavior: Contains many JSON theme presets plus `index.ts` that imports/exports them as `defaultThemes`.
- inputs_outputs_state: Inputs are theme JSON files; outputs are theme definitions available to settings/TUI.
- gates_or_invariants: JSON must be valid and match theme schema; theme IDs/names should be unique.
- dependencies_and_callers: Used by theme manager/settings and TUI render components.
- edge_cases_or_failure_modes: Invalid color keys, duplicate IDs, unreadable JSON, or missing required fields.
- validation_or_tests: Covered by theme loading/fallback tests where present.
- skip_candidate: `yes: data preset directory, not an algorithm beyond export aggregation`

### OH_MY_HUMANIZE_MAIN-HZ-2921 `file` `crates/pi-shell/src/minimizer/filters/rust_tools.rs`
- cursor: `[_]`
- core_role: Rust shell minimizer filter for Rust tool/build output.
- algorithmic_behavior: Filters/minimizes Rust toolchain output, likely recognizing cargo/rustc patterns and retaining diagnostically relevant lines.
- inputs_outputs_state: Inputs are shell output lines; outputs are reduced/minimized output.
- gates_or_invariants: Must preserve errors/warnings/paths while dropping noise.
- dependencies_and_callers: Used by `pi-shell` output minimizer pipeline.
- edge_cases_or_failure_modes: New cargo output formats, multiline diagnostics, ANSI color, and path truncation.
- validation_or_tests: Covered by pi-shell minimizer tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2951 `file` `packages/ai/src/utils/schema/fields.ts`
- cursor: `[_]`
- core_role: Central constants for provider-supported/unsupported JSON Schema fields.
- algorithmic_behavior: Defines unsupported, liftable, nonstructural, and Cloud Code Assist compatibility field sets used by schema normalizers/auditors.
- inputs_outputs_state: Inputs are schema keyword names; outputs are lookup constants used to decide stripping/spilling/validation.
- gates_or_invariants: Field sets must align with provider behavior; changing them changes request compatibility.
- dependencies_and_callers: Used by `normalize.ts`, `compatibility.ts`, strict schema enforcement, and tests.
- edge_cases_or_failure_modes: Provider schema support changes, over-stripping useful constraints, or under-stripping rejected keywords.
- validation_or_tests: Covered by schema/provider compatibility tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2981 `file` `packages/coding-agent/src/cli/gallery-fixtures/types.ts`
- cursor: `[_]`
- core_role: Type definitions for CLI gallery fixtures.
- algorithmic_behavior: Defines fixture shapes consumed by gallery/demo tooling.
- inputs_outputs_state: Inputs are TypeScript imports; outputs are type contracts only.
- gates_or_invariants: Fixture type shape must match gallery loader/renderers.
- dependencies_and_callers: Used by gallery fixture code.
- edge_cases_or_failure_modes: Type drift causes compile errors or fixture mismatch.
- validation_or_tests: Compile-time validation.
- skip_candidate: `yes: type-only fixture contract, not runtime core`

### OH_MY_HUMANIZE_MAIN-HZ-3011 `file` `packages/coding-agent/src/edit/hashline/filesystem.ts`
- cursor: `[_]`
- core_role: Coding-agent filesystem adapter for hashline patching.
- algorithmic_behavior: Resolves paths through plan-mode redirect, reads notebook-aware editable text, blocks generated files, preflights plan-mode writes, serializes notebook-aware output, writes through LSP with batch/deferred diagnostics, invalidates FS scan cache, and stores diagnostics per path.
- inputs_outputs_state: Inputs are relative edit paths, session/tool context, content, LSP batch request, abort signal; outputs are final written text, diagnostics, filesystem changes, and cache invalidation.
- gates_or_invariants: Generated files and plan-mode write restrictions are enforced; diagnostics are consumed once; per-instance state avoids concurrent tool sharing.
- dependencies_and_callers: Used by hashline edit tool execution; depends on `@oh-my-pi/hashline`, LSP writethrough, plan-mode guard, file snapshot store, read/serialize helpers.
- edge_cases_or_failure_modes: Missing files map to `NotFoundError`, notebook serialization failure, LSP timeout/fallback, stale diagnostics, and generated-file false positives.
- validation_or_tests: Covered by hashline/edit/LSP tests and generated guard tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3041 `file` `packages/coding-agent/src/eval/py/runtime.ts`
- cursor: `[_]`
- core_role: Python runtime/environment resolver for eval and kernel spawning.
- algorithmic_behavior: Filters environment to allowlisted variables and `LC_`/`XDG_`/`PI_` prefixes while denylisting API keys, resolves active/project/managed/system Python runtimes, detects explicit venv interpreters, applies `VIRTUAL_ENV`/PATH layout, and enumerates candidates in priority order.
- inputs_outputs_state: Inputs are cwd, environment, configured interpreter, filesystem venv markers, and PATH lookup; outputs are `PythonRuntime` with executable/env/venv path or errors.
- gates_or_invariants: Secret env vars are stripped; Windows env keys are case-insensitive; explicit interpreters expand `~` and resolve relative to cwd; candidates are deduped.
- dependencies_and_callers: Used by Python eval runtime, shared gateway, and local kernel spawning.
- edge_cases_or_failure_modes: Missing Python, broken managed env shadowing system Python, invalid venv, case-insensitive PATH, and explicit interpreter inside venv.
- validation_or_tests: Covered by Python executor/eval tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3071 `file` `packages/coding-agent/src/extensibility/plugins/legacy-pi-compat.ts`
- cursor: `[_]`
- core_role: Compatibility loader for legacy Pi extensions/plugins.
- algorithmic_behavior: Remaps historical package scopes to `@oh-my-pi`, rewrites relocated subpaths, routes TypeBox imports to shim, resolves bundled/bunfs/package-root paths, validates override targets, rewrites package `#imports`, walks extension source graph, installs scoped Bun `onLoad` hooks, and imports modules with mtime cache busting.
- inputs_outputs_state: Inputs are plugin entry paths, import specifiers, package.json imports maps, compiled/source install state, and extension source text; outputs are rewritten module loads and plugin module exports.
- gates_or_invariants: Hooks are scoped to exact extension realpaths; host packages should be singleton-resolved; missing compiled override targets fall through safely; non-source assets bypass rewriting.
- dependencies_and_callers: Used by extension/plugin loader; depends on Bun plugin/resolve APIs, filesystem realpath/stat, shims, and compiled binary layout.
- edge_cases_or_failure_modes: Compiled bunfs path changes, symlinks, missing extra entrypoints, unsupported TypeBox submodules, package import exclusions, unresolved relative imports, and process-global Bun plugin hooks.
- validation_or_tests: Covered by plugin install/legacy compatibility tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3101 `file` `packages/coding-agent/src/modes/components/background-tan-message.ts`
- cursor: `[_]`
- core_role: TUI component for a styled/background message block.
- algorithmic_behavior: Renders message text with theme styling/background treatment.
- inputs_outputs_state: Inputs are message text/theme/layout width; outputs are TUI component/render lines.
- gates_or_invariants: Text should fit/sanitize according to TUI conventions.
- dependencies_and_callers: Used by coding-agent mode components.
- edge_cases_or_failure_modes: Long text, narrow width, ANSI/theme mismatch.
- validation_or_tests: Covered indirectly by component render tests.
- skip_candidate: `yes: presentational component with limited algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3131 `file` `packages/coding-agent/src/modes/components/message-frame.ts`
- cursor: `[_]`
- core_role: TUI message framing component.
- algorithmic_behavior: Wraps message content in consistent frame/border/padding style for chat transcript display.
- inputs_outputs_state: Inputs are child content, theme, width/expanded state; outputs are framed TUI render output.
- gates_or_invariants: Frame width and content truncation/wrapping must avoid terminal overflow.
- dependencies_and_callers: Used by assistant/user/message render components.
- edge_cases_or_failure_modes: Nested frames, narrow width, long unbroken text, and theme border glyphs.
- validation_or_tests: Covered by assistant/user message component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3161 `file` `packages/coding-agent/src/modes/components/visual-truncate.ts`
- cursor: `[_]`
- core_role: Visual-width truncation helper/component for TUI mode components.
- algorithmic_behavior: Truncates strings/components based on visual terminal width rather than byte length.
- inputs_outputs_state: Inputs are text, width, ellipsis/options; outputs are display-safe truncated text.
- gates_or_invariants: Output visual width must not exceed target and should preserve ANSI/Unicode boundaries.
- dependencies_and_callers: Used by message/status/tool renderers.
- edge_cases_or_failure_modes: Wide glyphs, ANSI escapes, zero-width chars, and tiny widths.
- validation_or_tests: Covered by `visual-truncate.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3191 `file` `packages/coding-agent/src/modes/theme/mermaid-cache.ts`
- cursor: `[_]`
- core_role: Cache for Mermaid rendering in themed TUI output.
- algorithmic_behavior: Stores/reuses rendered Mermaid outputs keyed by diagram/theme/options to avoid repeated expensive rendering.
- inputs_outputs_state: Inputs are Mermaid source and theme/render options; outputs are cached rendered artifacts.
- gates_or_invariants: Cache keys must include all render-affecting inputs; invalidation must avoid stale theme output.
- dependencies_and_callers: Used by markdown/Mermaid renderers in coding-agent theme layer.
- edge_cases_or_failure_modes: Theme changes, large diagrams, memory growth, and renderer errors.
- validation_or_tests: Covered indirectly by Mermaid golden tests and markdown rendering tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3221 `file` `packages/coding-agent/src/tools/browser/tab-worker-entry.ts`
- cursor: `[_]`
- core_role: Hidden worker entry dispatch for browser tab worker.
- algorithmic_behavior: Provides worker entry code that re-enters or dispatches browser tab worker behavior according to the CLI worker-host contract.
- inputs_outputs_state: Inputs are worker argv/messages; outputs are worker runtime side effects/messages.
- gates_or_invariants: Must stay aligned with `cli.ts` worker-host dispatch to work in source, bundled, and compiled binary modes.
- dependencies_and_callers: Spawned by browser tool/tab worker sites and CLI worker host.
- edge_cases_or_failure_modes: Missing selector in CLI dispatch, compiled binary entrypoint mismatch, and worker message protocol drift.
- validation_or_tests: Covered by worker smoke tests and browser tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3251 `file` `packages/coding-agent/src/web/scrapers/hex.ts`
- cursor: `[_]`
- core_role: Special web scraper for Hex.pm package pages.
- algorithmic_behavior: Detects Hex package URLs, extracts package name, fetches Hex API package metadata and release dependencies, formats markdown with latest version/license/downloads/links/dependencies/recent releases, and returns a structured render result.
- inputs_outputs_state: Inputs are URLs, timeout, abort signal, and Hex API JSON; outputs are markdown render result or `null`.
- gates_or_invariants: Only `hex.pm` package paths are handled; failed API/parse returns `null`; release dependency fetch is bounded by shorter timeout.
- dependencies_and_callers: Used by web scraper special-handler registry; depends on `loadPage`, `tryParseJson`, and formatting helpers.
- edge_cases_or_failure_modes: Missing package, malformed JSON, absent release data, API timeout, and URL path variants.
- validation_or_tests: Covered by `tools/web-scrapers/dev-platforms.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3281 `file` `packages/coding-agent/src/web/scrapers/rubygems.ts`
- cursor: `[_]`
- core_role: Special web scraper for RubyGems package pages.
- algorithmic_behavior: Detects RubyGems gem URLs, extracts gem name, fetches RubyGems API JSON, formats markdown with version/license/downloads/links/authors/runtime and development dependencies, and returns a structured render result.
- inputs_outputs_state: Inputs are URL, timeout, abort signal, and RubyGems API JSON; outputs are markdown render result or `null`.
- gates_or_invariants: Only `rubygems.org/gems/<name>` paths are handled; API response must parse before rendering.
- dependencies_and_callers: Used by web scraper special-handler registry; depends on `loadPage`, `tryParseJson`, and formatting helpers.
- edge_cases_or_failure_modes: Missing gem, malformed JSON, absent dependency metadata, API timeout, and URL encoding.
- validation_or_tests: Covered by `tools/web-scrapers/dev-platforms.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3311 `file` `packages/coding-agent/test/modes/components/assistant-message-error.test.ts`
- cursor: `[_]`
- core_role: Regression suite for assistant message error rendering.
- algorithmic_behavior: Tests rendering/classification of assistant messages that contain error state or provider errors.
- inputs_outputs_state: Inputs are assistant message fixtures with error fields; outputs are TUI render lines/components.
- gates_or_invariants: Errors should be visible, sanitized, and not corrupt normal message layout.
- dependencies_and_callers: Targets assistant message component/render path.
- edge_cases_or_failure_modes: Empty error, long provider error, mixed text/error content, and restored transcript messages.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3341 `file` `packages/coding-agent/test/modes/components/user-message-keywords.test.ts`
- cursor: `[_]`
- core_role: Regression suite for user message keyword highlighting/detection.
- algorithmic_behavior: Tests keyword detection and styling in user messages, including prose-aware behavior.
- inputs_outputs_state: Inputs are user message strings; outputs are highlighted/rendered components or detection results.
- gates_or_invariants: Keywords should highlight only under intended conditions and avoid false positives in prose/code.
- dependencies_and_callers: Targets user message components and keyword utilities.
- edge_cases_or_failure_modes: Case variants, punctuation, code fences, prose matches, and multiple keywords.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3371 `file` `packages/coding-agent/test/tools/web-scrapers/dev-platforms.test.ts`
- cursor: `[_]`
- core_role: Regression/integration suite for special web scrapers on developer platforms.
- algorithmic_behavior: Tests special URL handlers for platforms such as HN, Lobsters, dev.to, GitLab, Hex, RubyGems, and related render outputs; some integration paths are gated by `WEB_FETCH_INTEGRATION`.
- inputs_outputs_state: Inputs are platform URLs and fixture/fetched pages; outputs are normalized markdown render results or `null`.
- gates_or_invariants: Handlers should only claim matching URLs and should format stable metadata.
- dependencies_and_callers: Targets web scraper special-handler registry including `hex.ts` and `rubygems.ts`.
- edge_cases_or_failure_modes: Network failures, platform HTML/API changes, unsupported URL paths, and malformed metadata.
- validation_or_tests: This file is direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3401 `file` `packages/collab-web/src/components/shell/Toasts.tsx`
- cursor: `[_]`
- core_role: Collab web toast/notice display component.
- algorithmic_behavior: Renders capped notice/toast state from the web client with styling and dismissal/visibility behavior.
- inputs_outputs_state: Inputs are notice arrays and callbacks; outputs are React DOM toast elements.
- gates_or_invariants: Notices should be bounded and visually distinguish severity.
- dependencies_and_callers: Used by collab web shell.
- edge_cases_or_failure_modes: Many notices, long messages, missing severity, and rapid updates.
- validation_or_tests: Covered by web UI/manual tests.
- skip_candidate: `yes: presentational UI component, not core protocol algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3431 `file` `packages/collab-web/src/tool-render/tools/ssh.tsx`
- cursor: `[_]`
- core_role: Collab web renderer for SSH tool results.
- algorithmic_behavior: Displays SSH command/result details, status, output, and metadata in the web tool-rendering surface.
- inputs_outputs_state: Inputs are SSH tool call/result payloads; outputs are React DOM render of command/output/status.
- gates_or_invariants: Output must be bounded/sanitized for UI and reflect cancellation/error/truncation state.
- dependencies_and_callers: Used by collab web tool-render registry and coding-agent SSH result schema.
- edge_cases_or_failure_modes: Long output, missing details, cancelled command, and truncated artifact metadata.
- validation_or_tests: Covered by web renderer/manual tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3461 `file` `packages/stats/src/client/data/useHashRoute.ts`
- cursor: `[_]`
- core_role: Stats client hook for hash-based route state.
- algorithmic_behavior: Reads/parses `window.location.hash`, updates React state on hash changes, and writes route changes back to the URL hash.
- inputs_outputs_state: Inputs are browser hash strings and route setter calls; outputs are route state and hash mutations.
- gates_or_invariants: Route parsing must tolerate empty/unknown hashes and avoid unnecessary history churn.
- dependencies_and_callers: Used by stats dashboard navigation.
- edge_cases_or_failure_modes: SSR/no-window contexts, malformed hash, rapid back/forward changes, and stale listeners.
- validation_or_tests: Covered by stats client tests/manual UI.
- skip_candidate: `yes: small UI routing hook, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3491 `file` `python/robomp/web/src/components/Events.tsx`
- cursor: `[_]`
- core_role: Robomp dashboard component for event queue/status display.
- algorithmic_behavior: Renders event records, statuses, actions, or filters from the Robomp web API state.
- inputs_outputs_state: Inputs are event data from dashboard API; outputs are React DOM rows/cards and user actions.
- gates_or_invariants: Event status labels and ordering should reflect backend queue state accurately.
- dependencies_and_callers: Used by Robomp web dashboard.
- edge_cases_or_failure_modes: Empty event list, unknown status, long payload/title, and stale polling data.
- validation_or_tests: Covered by Robomp dashboard/manual tests.
- skip_candidate: `yes: dashboard presentation for core queue state, not the queue algorithm itself`

### OH_MY_HUMANIZE_MAIN-HZ-3521 `file` `packages/coding-agent/src/eval/js/shared/types.ts`
- cursor: `[_]`
- core_role: Shared TypeScript contracts for JS eval runtime.
- algorithmic_behavior: Defines data shapes exchanged by JS eval host/worker/runtime.
- inputs_outputs_state: Inputs are imports/compile-time references; outputs are type contracts for eval messages/results.
- gates_or_invariants: Type shapes must match both sides of eval protocol.
- dependencies_and_callers: Used by JS eval runtime and worker/shared code.
- edge_cases_or_failure_modes: Type drift between host and worker causes runtime protocol mismatch.
- validation_or_tests: Compile-time checks and eval tests validate this.
- skip_candidate: `yes: type-only protocol contract with no executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3551 `file` `packages/coding-agent/src/modes/components/status-line/separators.ts`
- cursor: `[_]`
- core_role: Status-line separator rendering helpers.
- algorithmic_behavior: Provides separator glyph/style selection for status-line components.
- inputs_outputs_state: Inputs are theme/status-line context; outputs are separator strings/components.
- gates_or_invariants: Separators should match theme and not exceed layout width.
- dependencies_and_callers: Used by coding-agent status line components.
- edge_cases_or_failure_modes: Narrow terminal, missing glyph/theme key, and inconsistent spacing.
- validation_or_tests: Covered indirectly by status-line render tests.
- skip_candidate: `yes: presentational helper with minimal core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3581 `file` `packages/coding-agent/src/web/search/providers/zai.ts`
- cursor: `[_]`
- core_role: Z.AI web search provider adapter through remote MCP.
- algorithmic_behavior: Resolves Z.AI API key via auth storage, calls `web_search_prime` JSON-RPC tool over HTTP/SSE-compatible response, parses SSE `data:` or plain JSON, classifies HTTP/MCP/API errors, retries alternate argument shapes, extracts result arrays/answers/request IDs, maps dates to ages and results into unified `SearchResponse`.
- inputs_outputs_state: Inputs are query/count/auth/session/fetch/signal; outputs are normalized search results/sources or `SearchProviderError`.
- gates_or_invariants: Hard timeout wraps fetch; auth key is required; only argument-shape errors trigger fallback attempts; MCP `isError` content is converted to provider error.
- dependencies_and_callers: Extends `SearchProvider`; used by web search tool; depends on pi-ai auth, scraper utils, provider error classifiers.
- edge_cases_or_failure_modes: SSE with non-JSON events, plain JSON fallback, direct API `{success:false}`, JSON-RPC errors, MCP tool errors, changed result field names, and missing publish dates.
- validation_or_tests: Covered by web search/provider tests where configured; no direct assigned test for Z.AI search.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3611 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/diamond.ts`
- cursor: `[_]`
- core_role: Mermaid ASCII renderer shape implementation for diamonds.
- algorithmic_behavior: Defines how diamond nodes are drawn in ASCII layout, including boundaries/interior geometry.
- inputs_outputs_state: Inputs are shape dimensions/text/layout context; outputs are ASCII cell/line drawing instructions.
- gates_or_invariants: Shape geometry must fit requested dimensions and align connectors.
- dependencies_and_callers: Used by vendored Mermaid ASCII renderer and golden tests.
- edge_cases_or_failure_modes: Very small dimensions, long labels, connector alignment, and layout drift.
- validation_or_tests: Covered by Mermaid golden tests.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `121 unique Item Evidence headings`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`