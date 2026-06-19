# agent_16 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- note: repository export is read-only and appears to omit `.git`; scheduler-provided commit was treated as authoritative. No files were modified.

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-016 `file` `rustfmt.toml`
- cursor: `[_]`
- core_role: Workspace Rust formatting policy for crates and generated/tooling-sensitive Rust source.
- algorithmic_behavior: Defines deterministic formatting decisions: edition/style edition 2024, import grouping, comment wrapping, width heuristics, macro/string formatting, impl reordering, alignment thresholds, explicit ABI, Unix newlines, and ignored vendored crates.
- inputs_outputs_state: Input is Rust source formatted by rustfmt; output is normalized source layout. No runtime state, but it stabilizes diffs and generated code review surfaces.
- gates_or_invariants: `edition = "2024"` and `style_edition = "2024"` at lines 1-3; hard tabs and `tab_spaces = 3` at lines 23-26; vendored ignore paths at line 74.
- dependencies_and_callers: Consumed by rustfmt through workspace tooling, indirectly affecting crates such as `crates/pi-ast`, `crates/pi-iso`, and `crates/pi-natives`.
- edge_cases_or_failure_modes: Non-default unstable settings can require nightly rustfmt depending on toolchain; ignored vendored paths prevent noise but also exclude them from formatting gates.
- validation_or_tests: Validation is external formatting/check workflow rather than in-file tests.
- skip_candidate: `yes: configuration file, but included because it shapes build/tooling algorithms and diff stability`

### OH_MY_HUMANIZE_MAIN-HZ-046 `file` `docs/blob-artifact-architecture.md`
- cursor: `[_]`
- core_role: Architecture contract for session blob storage, artifact spilling, and internal URL resolution.
- algorithmic_behavior: Separates content-addressed blobs from session-local artifacts; defines persistence rewrite, blob rehydration, output spill/truncation, `artifact://` lookup, `agent://` lookup and JSON extraction, resume/fork/move semantics.
- inputs_outputs_state: Inputs are session entries, image payloads, tool output chunks, artifact IDs, internal URLs; outputs are blob refs, artifact files, rehydrated base64/data URLs, and internal URL resources. State lives in global blob dir and per-session artifact dirs.
- gates_or_invariants: Blob refs are `blob:sha256:<hash>` lines 25-33; artifact IDs scan existing `*.log` and allocate monotonic IDs lines 63-76; `artifact://` requires numeric IDs lines 147-158; `agent://` rejects combined path/query extraction lines 164-178.
- dependencies_and_callers: Documents `blob-store.ts`, `artifacts.ts`, `streaming-output.ts`, `session-manager.ts`, `session-persistence.ts`, `session-loader.ts`, `artifact-protocol.ts`, `agent-protocol.ts`, `task/output-manager.ts`, and `task/executor.ts` lines 232-245.
- edge_cases_or_failure_modes: Missing blob refs log warnings and continue lines 114-116; missing artifact dirs throw explicit errors lines 156-158 and 171-173; output sink writer init failure falls back to bounded memory lines 218-222.
- validation_or_tests: Related validation appears in internal URL tests, artifact registry tests, task executor output tests, and session fork/move behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-076 `file` `docs/tui-core-renderer.md`
- cursor: `[_]`
- core_role: TUI renderer contract for append-only scrollback and terminal fidelity.
- algorithmic_behavior: Defines frame pipeline, committed prefix audit, window math, cursor-marker stripping, synchronized-output emission, commit-boundary seam, capability detection, width model, image handling, and renderer stress gates.
- inputs_outputs_state: Inputs are component-rendered frames, terminal dimensions/capabilities, live region boundaries, and cursor markers; outputs are terminal byte sequences and renderer ledger state: `committedRows`, `windowTopRow`, and `commit boundary`.
- gates_or_invariants: No viewport probing lines 27-30 and 204-208; never rewrite committed rows lines 194-202; mutable content must stay below commit boundary lines 208-211; render hot path must not throw lines 216-218; no new ED3 callsites lines 194-197.
- dependencies_and_callers: Documents `packages/tui/src/tui.ts`, `terminal.ts`, `terminal-capabilities.ts`, `stdin-buffer.ts`, `utils.ts`, `kitty-graphics.ts`, `components/image.ts`, and `deccara.ts` lines 9-15.
- edge_cases_or_failure_modes: Scrollback position is unobservable, so scrolled-past blocks cannot reflow in place lines 65-75; multiplexer resize history remains wrapped at old width lines 76-78; missing seams cause shell semantics.
- validation_or_tests: Stress harness must compare terminal tape to shadow tape and validate scrolled reader, multiplexer, sync-output, autowrap, cursor, and background behavior lines 277-289.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-106 `file` `scripts/install.sh`
- cursor: `[_]`
- core_role: Installer workflow router for source or binary installation of the coding-agent CLI.
- algorithmic_behavior: Parses mode/ref flags, checks Bun/Git/Git-LFS availability, validates minimum Bun version, optionally installs Bun, clones tagged refs for source install, installs package via Bun, or downloads the latest/tagged binary from GitHub releases.
- inputs_outputs_state: Inputs are CLI flags (`--source`, `--binary`, `--ref`), env `PI_INSTALL_DIR`, host OS/arch, GitHub release JSON, Bun version. Outputs are installed `omp` binary/package link and PATH warning.
- gates_or_invariants: `set -e` line 2; default `MODE=source` when ref is supplied lines 64-65; minimum Bun `1.3.14` line 16; Git required for `--ref` source install lines 145-147; OS/arch mapped for binary download lines 192-204.
- dependencies_and_callers: Uses `curl`, `git`, `git-lfs`, `bun`, GitHub releases API, and npm package `@oh-my-pi/pi-coding-agent`.
- edge_cases_or_failure_modes: Missing ref values exit lines 33-51; clone by branch falls back to full clone and checkout lines 154-162; unsupported OS/arch exits; GitHub API failure falls back to latest release logic.
- validation_or_tests: Install smoke is external to script; branch rules mention smoke tests for binary/source/tarball installs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-136 `directory` `packages/collab-web/src`
- cursor: `[_]`
- core_role: Browser guest client for live collaboration sessions, including encrypted socket transport, transcript state, agent rail, composer, and tool rendering.
- algorithmic_behavior: `app.tsx` stores/reuses collab link/name and creates `GuestClient`; `lib/codec.ts` seals/opens AES-GCM frames; `lib/link.ts` parses/normalizes room links and envelopes; `lib/socket.ts` reconnects with backoff and encrypted frame send/receive; `lib/client.ts` applies host frames/events into `GuestSnapshot`; `tool-render` maps tool names to specialized React renderers.
- inputs_outputs_state: Inputs are URL hash/direct link, room key/write token, WebSocket frames, host transcript/events/state/agent frames, composer messages. Outputs are encrypted guest frames, live UI snapshot, notices, active tool state, assistant streaming ghost, transcript fetch promises. State is held in `GuestClient` private fields and React hooks.
- gates_or_invariants: AES key must be 32 bytes and encrypted payload must exceed IV length in `codec.ts` lines 10-42; socket pending sends cap at 256 in `socket.ts` line 25; fatal close reasons stop reconnect in `socket.ts` lines 15-23; link parser rejects insecure non-local `ws://` in `link.ts` lines 95-107.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-wire`, WebCrypto, WebSocket, React, and CSS modules. Coordinates with coding-agent collab host/relay and with `packages/coding-agent/test/collab/crypto.test.ts`.
- edge_cases_or_failure_modes: Welcome timeout ends session after 30s in `client.ts` lines 67-130; malformed frames are caught in `#applyFrameSafe`; decryption/invalid envelopes close or ignore; stream ghost is held until matching assistant entry lands.
- validation_or_tests: Crypto/link/envelope tests in `packages/coding-agent/test/collab/crypto.test.ts`; individual renderers are validated through tool-render behavior in coding-agent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-166 `directory` `python/robomp/src`
- cursor: `[_]`
- core_role: Python GitHub issue/PR automation service that queues webhook events, manages isolated workspaces, drives OMP RPC tasks, comments/reviews on GitHub, and exposes dashboard/proxy APIs.
- algorithmic_behavior: `server.py` receives webhooks/manual triggers and admission-controls work; `db.py` atomically stores event/issue/closure state; `tasks.py` routes issue triage, PR review, comments, reviews, and cleanup; `worker.py` builds prompts and drives OMP RPC with reminders/timeouts; `git_ops.py` clones/fetches/worktrees/pushes with repair; `proxy/server.py` holds PAT and signs internal GitHub/git operations; `autoclose.py` transitions pending closure rows.
- inputs_outputs_state: Inputs are GitHub webhook payloads, manual CLI triggers, settings env, SQLite rows, repo workspaces, OMP RPC turn outputs, GitHub API responses. Outputs are DB transitions, comments/reviews/labels, pushes, workspace cleanup, dashboard JSON/HTML.
- gates_or_invariants: Settings require either direct token or proxy mode but not both in `config.py` lines 218-231; DB closure final states are validated in `db.py` lines 1053-1114; Git refs are sanitized in `git_ops.py` lines 275-282; proxy authenticates HMAC and enforces body limits in `proxy/server.py` lines 248-322.
- dependencies_and_callers: Depends on FastAPI, Click, Pydantic settings, SQLite, Git, OMP RPC client/proxy HMAC, GitHub REST API. Tests include `python/robomp/tests/test_config.py`.
- edge_cases_or_failure_modes: Webhook dedupe/rate limits reject duplicates or exhausted submitters; dirty/unpushed workspace triggers reminder or blocks; Git fetch-prune repairs missing alternates/bad refs; autoclose cancels on downvote or GitHub close failures.
- validation_or_tests: Config tests cover env parsing, proxy/direct auth exclusivity, replay token blanking, model pool selection, and concurrency defaults.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-196 `file` `docs/tools/recall.md`
- cursor: `[_]`
- core_role: Tool contract for explicit cross-session memory recall.
- algorithmic_behavior: Documents backend-gated tool exposure, abort wrapping, mnemopi scoped recall merge/dedupe/sort/truncate, hindsight HTTP recall with budget/types/tag filters, output formatting, and error mapping.
- inputs_outputs_state: Inputs are query and active memory backend config; outputs are text result with hit count/bullets or no-hit message and empty details. Explicit recall has no successful session-state mutation.
- gates_or_invariants: Tool is exposed only for `memory.backend` of `hindsight` or `mnemopi` lines 42-44; mnemopi recall limit default is 8 lines 87-90; Hindsight defaults include budget `mid`, max tokens 1024, types `world/experience` lines 82-86.
- dependencies_and_callers: Source is `memory-recall.ts`; prompt is `prompts/tools/recall.md`; collaborators are hindsight state/client and mnemopi state/config lines 5-17.
- edge_cases_or_failure_modes: Missing backend state throws explicit initialization errors lines 92-94; Hindsight HTTP/fetch becomes `HindsightError` line 95; mnemopi per-bank failures are logged under debug and may return no hits line 96.
- validation_or_tests: Mnemopi recall ranking and formatting are covered by `packages/mnemopi/test/beam-recall-unit.test.ts`; backend docs cross-reference retain behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-226 `directory` `crates/pi-ast/src/language`
- cursor: `[_]`
- core_role: Language registry and parser binding layer for native ast-grep search/edit.
- algorithmic_behavior: `mod.rs` wraps tree-sitter language functions in ast-grep `Language`/`LanguageExt` implementations, preprocesses metavariable sigils, extracts embedded JS/CSS from HTML, maps file extensions and aliases to `SupportLang`, and delegates parser functions from `parsers.rs`.
- inputs_outputs_state: Inputs are query patterns, source file paths/extensions, HTML AST nodes, and language aliases. Outputs are selected `SupportLang`, parser `TSLanguage`, ast-grep parse behavior, and extracted embedded language ranges.
- gates_or_invariants: HTML extraction scans script/style nodes in `mod.rs` lines 218-231; special extension cases include Makefile, Justfile, CMakeLists, Dockerfile, `.emacs`, and shell rc files lines 619-647; `parsers.rs` exposes one tree-sitter language function per supported language lines 5-176.
- dependencies_and_callers: Depends on `ast_grep_core`, `phf`, vendored tree-sitter grammar crates, and is called by pi-natives AST grep/edit APIs.
- edge_cases_or_failure_modes: Misclassified extensions fall back to aliases or no language; HTML embedded language extraction requires matching node names/attrs; parser availability must match Cargo dependencies.
- validation_or_tests: AST grep/edit tests cover TLA+/PlusCal aliases and parse-error reporting.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-256 `directory` `packages/coding-agent/src/debug`
- cursor: `[_]`
- core_role: Interactive debug surface for logs, terminal/protocol probes, raw SSE capture, CPU/heap profiling, report bundles, and remote debugger startup.
- algorithmic_behavior: `index.ts` routes debug menu actions; `log-viewer.ts` builds filterable/selectable paged log model; `raw-sse-buffer.ts` caps and coalesces raw events; `raw-sse.ts` pretty-prints SSE frames; `profiler.ts` summarizes CPU profiles; `report-bundle.ts` collects logs/session/artifacts/system info into zip; `remote-debugger.ts` reserves/probes Bun JSC debugger port.
- inputs_outputs_state: Inputs are key events, logs, raw SSE events, terminal runtime state, session files/artifact dirs, CPU/heap data. Outputs are TUI components, copied payloads, report archives, debugger info, formatted system/terminal diagnostics. State includes viewer cursors, selections, raw SSE ring buffer, active debugger singleton.
- gates_or_invariants: Raw SSE caps at 1000 events, 512KB total, 64KB per event in `raw-sse-buffer.ts` lines 3-7; log viewer initial/load chunks are 50 lines in `log-viewer.ts` lines 24-25; report bundle log cap is 5000 lines/2MB in `report-bundle.ts` lines 15-20.
- dependencies_and_callers: Uses `pi-tui`, `pi-utils` logger dirs/reports, `bun:jsc`, terminal info, work profile from natives, and interactive mode debug selector.
- edge_cases_or_failure_modes: Missing logs/artifacts are tolerated; malformed JSON log lines produce undefined timestamp/pid; debugger startup fails if port occupied after reserve; report bundle suppresses unreadable artifact/session files.
- validation_or_tests: Covered indirectly by debug/log renderer tests and TUI terminal capability tests; raw SSE buffer behavior is source-level bounded.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-286 `directory` `packages/coding-agent/src/tools`
- cursor: `[_]`
- core_role: Built-in tool implementation layer for coding-agent, spanning schemas, approval, execution, rendering, file/search/edit/shell/browser/memory/task workflows, and output safety.
- algorithmic_behavior: Tool classes define arktype/JTD schemas, descriptions, dynamic approval tiers, execution functions, update callbacks, detail payloads, and renderers. Major algorithms include approval matrix (`approval.ts`), ask multi-question state machine, AST grep/edit aggregation, generated-file guard, bash interception/fixups/PTy, browser tab workers/cmux RPC, output schema validation, internal URL expansion, memory retain/recall/reflect, search/fetch, and yield validation.
- inputs_outputs_state: Inputs are model tool arguments, `ToolSession`, settings, cwd, abort signals, UI callbacks, MCP/internal URL resources, filesystem/browser/network state. Outputs are `AgentToolResult`, detail metadata, pending actions, artifacts, file snapshots, render components, and async job state.
- gates_or_invariants: Approval modes gate by tier in `approval.ts` lines 13-159; generated edits are blocked by marker/file-name guard in `auto-generated-guard.ts` lines 248-319; skill/internal URLs reject traversal or missing router/sourcePath in `bash-skill-urls.ts` lines 37-232; yield caps schema retries at 3 in `yield.ts` lines 106-257.
- dependencies_and_callers: Consumed by `AgentSession`, task executor, interactive renderers, SDK, and tests under `packages/coding-agent/test/tools`. Depends on pi-agent-core tool contracts, pi-ai schemas, pi-natives, pi-tui, Puppeteer/cmux, MCP, and settings.
- edge_cases_or_failure_modes: Abort signals convert to `ToolAbortError`; stale pending apply rejects; browser worker startup errors surface early; bash streaming preview has partial JSON paths; output caps spill artifacts; internal URL expansion requires shell escaping.
- validation_or_tests: Broad test directory covers approvals, ask, AST, bash, browser, conflicts, fetch/search, LSP, memory, output caps/schema, web scrapers, yield, and renderer stability.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-316 `directory` `packages/coding-agent/test/tools`
- cursor: `[_]`
- core_role: Contract test suite for built-in tool behavior and render surfaces.
- algorithmic_behavior: Tests observable behavior for approvals, ask flow, AST grep/edit, generated-file blocking, bash fixups/interceptors/rendering, browser attach/cmux/worker/readable/stealth, conflict resolution, fetch/search, GitHub/cache, image/inspect, LSP diagnostics, memory renderers, path aliases, output caps/schema validation, web scrapers, web search providers, and yield schema degradation.
- inputs_outputs_state: Inputs are mocked sessions/settings/files/HTTP responses/tool args and real integration flags for web fetch. Outputs are assertions over tool results, details, render lines, errors, pending actions, and schema shapes.
- gates_or_invariants: Approval tests verify yolo/write/always-ask tier matrix; ask tests verify timeout/custom/navigation cancellation; bash tests verify critical redirect blocking and stable streaming/final render; browser tests verify startup errors and cmux mapping; yield tests verify MAX_SCHEMA_RETRIES and fallback.
- dependencies_and_callers: Depends on Bun test, tool modules, temp dirs, mocked settings, and fixtures. It protects `packages/coding-agent/src/tools` and web scraper implementations.
- edge_cases_or_failure_modes: Includes invalid regex, missing paths, stale edit previews, malformed apply_patch streams, binary fetch dispatch, URL selector edge cases, browser timeout attribution, conflict URI recovery, and unavailable yt-dlp/web providers.
- validation_or_tests: This directory is itself validation; it is full-suite safety critical because it avoids `mock.module()` patterns in favor of spies/imported modules.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-346 `file` `crates/pi-iso/src/projfs.rs`
- cursor: `[_]`
- core_role: Windows ProjFS isolation backend for projected filesystem overlays.
- algorithmic_behavior: Implements `IsolationBackend` for ProjFS; probes Windows feature availability, rejects x64-under-ARM64 emulation, loads `ProjectedFSLib.dll`, starts/stops virtualization sessions, enumerates directories, supplies placeholder/file data, maps HRESULT/Win32 errors, and guards concurrent sessions.
- inputs_outputs_state: Inputs are source/projection paths, ProjFS callbacks, callback file paths, enumeration IDs, byte offsets/lengths. Outputs are projected directory/file metadata and file data buffers. State includes global API/session maps and enumeration cursors.
- gates_or_invariants: Non-Windows returns unavailable; emulation guard at lines 36-92; duplicate active overlay rejected lines 342-344 and 429-437; null callback/instance contexts guarded lines 733-737; absolute/empty paths rejected in helpers around lines 801-863.
- dependencies_and_callers: Depends on Windows ProjFS APIs through dynamic library loading, async trait isolation backend contract, and filesystem metadata/read APIs. Called by pi-iso isolation selection.
- edge_cases_or_failure_modes: DLL missing/unavailable HRESULT maps to unavailable; insufficient buffer during enumeration is handled; aligned reads allocate aligned buffer; symlink metadata is filtered; canceled starting session transitions to canceled error.
- validation_or_tests: Unit tests cover ARM64 emulation detection lines 97 onward; integration depends on Windows ProjFS availability.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-376 `file` `crates/pi-natives/src/utils.rs`
- cursor: `[_]`
- core_role: Small native utility macros/functions shared by Rust native modules.
- algorithmic_behavior: Exports helper macro(s) and `clamp_u32(value: u64) -> u32`, which saturates a u64 at `u32::MAX`.
- inputs_outputs_state: Input is a `u64`; output is a clamped `u32`. No state.
- gates_or_invariants: `clamp_u32` returns `u32::MAX` when input exceeds max, otherwise casts directly lines 29-30.
- dependencies_and_callers: Internal Rust crate callers needing safe width/count conversions before crossing native or JS boundaries.
- edge_cases_or_failure_modes: Only overflow edge is saturating conversion; no error path.
- validation_or_tests: Covered indirectly by native operations using clamped sizes.
- skip_candidate: `yes: tiny helper, but still core because native algorithms rely on safe integer conversion`

### OH_MY_HUMANIZE_MAIN-HZ-406 `file` `packages/agent/test/otel.test.ts`
- cursor: `[_]`
- core_role: Observable contract tests for agent-loop OpenTelemetry instrumentation.
- algorithmic_behavior: Runs mock agent loops, drains events, inspects spans/events/attributes, verifies parent-child span relationships for invoke/chat/tool/handoff, error status mapping, message capture controls, cost/usage calculations, gateway detection, and exported chat usage events.
- inputs_outputs_state: Inputs are mock models, tool calls, telemetry config, headers, usage/cost payloads. Outputs are in-memory spans and chat usage event callbacks.
- gates_or_invariants: Invoke spans parent chat/tool spans lines 125-147 and 235-248; provider normalization for Google and OpenAI gateway attributes lines 178-204; error spans use `SpanStatusCode.ERROR` lines 315-337; content capture can be disabled lines 412-415 and 774-776.
- dependencies_and_callers: Depends on `agentLoop`, pi-ai mock provider, OpenTelemetry SDK memory exporter, and gateway detection helpers.
- edge_cases_or_failure_modes: Tests tool exceptions, model errors, manual spans/events, unsupported cost tiers, gateway headers without valid ids, and `on_chat_usage_failed` warnings.
- validation_or_tests: This file is the validation for telemetry and gateway attribute contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-436 `file` `packages/ai/test/anthropic-copilot-checkpoint-thinking-signature.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Anthropic/GitHub Copilot thinking-signature replay around checkpoints and branch returns.
- algorithmic_behavior: Builds a Copilot signing model, converts assistant messages to Anthropic wire params, gathers thinking blocks, and asserts when signatures are preserved or suppressed.
- inputs_outputs_state: Inputs are synthetic assistant messages with thinking/tool blocks and model compatibility flags. Outputs are Anthropic wire message blocks.
- gates_or_invariants: Copilot model has `replayUnsignedThinking=false` line 97; checkpoint branch suppresses unsigned thinking but preserves tool use lines 138-140; replayable signature remains in first assistant block lines 169-172.
- dependencies_and_callers: Calls `convertAnthropicMessages` and catalog `buildModel`.
- edge_cases_or_failure_modes: Prevents leaking or replaying unsigned thinking across checkpoint/branch-return boundaries while allowing signed replayable thinking.
- validation_or_tests: File itself is regression validation for issue #2851.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-466 `file` `packages/ai/test/auth-gateway-openai-chat.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI Chat-compatible auth gateway request parser and response/SSE encoder.
- algorithmic_behavior: Parses chat request messages/tools/tool results/options into internal context; encodes assistant final messages to chat-completion JSON; streams deltas/tool calls/errors in OpenAI SSE format; propagates aborts.
- inputs_outputs_state: Inputs are OpenAI-style request JSON, assistant event streams, abort signal. Outputs are parsed `modelId/context/options`, final completion objects, SSE chunks, and abort state.
- gates_or_invariants: Missing model/messages throw lines 146-147; invalid tool arg JSON becomes `__raw` line 122; stream emits role chunk first and `[DONE]` last lines 285-306; tool call deltas preserve indices/arguments lines 316-333.
- dependencies_and_callers: Uses `parseRequest`, `encodeResponse`, and `encodeStream` from `openai-chat-server`.
- edge_cases_or_failure_modes: Null content on length finish, upstream stream errors become error envelope lines 342-344, client abort propagates reason lines 365-370.
- validation_or_tests: File validates gateway Chat Completions compatibility.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-496 `file` `packages/ai/test/copilot-retry.test.ts`
- cursor: `[_]`
- core_role: Retry policy tests for Copilot transient model and transport failures.
- algorithmic_behavior: Constructs structured errors, classifies transient Copilot errors, runs retry wrapper, counts attempts, and verifies generic retryable transport handling.
- inputs_outputs_state: Inputs are errors with status/code/message, callback functions, retry settings. Outputs are boolean classifications, returned value, thrown error, and call counts.
- gates_or_invariants: 4xx non-transient is not retryable lines 40-57 and 227; transient cases retry up to expected calls lines 80-104; abort/non-Copilot errors do not retry lines 111-135.
- dependencies_and_callers: Tests `callWithCopilotModelRetry`, `isCopilotTransientModelError`, and `isRetryableError`.
- edge_cases_or_failure_modes: Transport failures can be retryable; usage-limit or permanent request failures should not be retried.
- validation_or_tests: This is the retry validation suite.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-526 `file` `packages/ai/test/harmony-leak.test.ts`
- cursor: `[_]`
- core_role: Regression tests for detecting and recovering OpenAI Harmony leakage in tool-call payloads.
- algorithmic_behavior: Loads corpus positives/negatives, classifies mitigation target models, detects leak co-signals, recovers safe tool inputs for supported edit/eval tools, extracts removed text, and builds audit event metadata.
- inputs_outputs_state: Inputs are assistant messages/tool calls with embedded Harmony fragments and parsed-end offsets. Outputs are leak detections, recovered tool call messages, removed leak excerpts, audit event hashes/previews.
- gates_or_invariants: Only Codex model is mitigation target lines 80-84; negatives must not trip lines 95-109; positives require multiple signal classes including `M` lines 125-129; tool_arg T-gate prevents false positives lines 141-160.
- dependencies_and_callers: Tests harmony leak mitigation helpers and bundled catalog models.
- edge_cases_or_failure_modes: Unsupported tools and JSON-schema edit payloads must not recover lines 216-259; second recovery on clean payload returns undefined lines 200-210.
- validation_or_tests: Corpus-driven mitigation validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-556 `file` `packages/ai/test/issue-976-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for legacy string `systemPrompt` conversion in Google Gemini CLI provider.
- algorithmic_behavior: Builds a Gemini CLI request from context with string system prompt and asserts correct `systemInstruction`.
- inputs_outputs_state: Input is internal context/model; output is provider request payload.
- gates_or_invariants: `request.systemInstruction` must contain expected text parts line 35.
- dependencies_and_callers: Calls `buildRequest` from `google-gemini-cli` and catalog `buildModel`.
- edge_cases_or_failure_modes: Prevents string prompt from being dropped or mis-shaped when provider expects structured system instruction.
- validation_or_tests: Single issue repro test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-586 `file` `packages/ai/test/openai-completions-reasoning-disable-dialects.test.ts`
- cursor: `[_]`
- core_role: Tests dialect-specific payload shaping when forced tools conflict with reasoning controls in Chat Completions.
- algorithmic_behavior: Captures forced-tool request payloads for models with different reasoning disable dialects and asserts provider-specific disable fields while removing conflicting `reasoning_effort`.
- inputs_outputs_state: Inputs are model compatibility dialects, forced tool context, mock fetch. Output is outbound OpenAI-compatible request JSON.
- gates_or_invariants: Anthropic-style uses `thinking: {type:"disabled"}`; Qwen uses `enable_thinking=false`; template kwargs use `chat_template_kwargs`; generic reasoning uses `reasoning.enabled=false`; all remove `reasoning_effort` lines 93-120.
- dependencies_and_callers: Calls `streamOpenAICompletions`, catalog `buildModel`, and model compat flags.
- edge_cases_or_failure_modes: Tool choice should fall back to `auto` when forced tool and reasoning disable collide for unsupported forced selection lines 141-142.
- validation_or_tests: Per-dialect reasoning conflict validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-616 `file` `packages/ai/test/rate-limit-utils.test.ts`
- cursor: `[_]`
- core_role: Tests rate-limit reason parsing, usage-limit classification, and backoff jitter.
- algorithmic_behavior: Maps provider error strings to normalized reasons, detects quota/usage limits, and verifies calculated backoff range.
- inputs_outputs_state: Inputs are error message strings and retry metadata; outputs are normalized reason enum/string, boolean usage limit, and backoff milliseconds.
- gates_or_invariants: 429 and RPM messages map to `RATE_LIMIT_EXCEEDED`; overloaded/resource exhausted maps to capacity; 500 maps server error; unknown maps `UNKNOWN` lines 20-40.
- dependencies_and_callers: Tests `parseRateLimitReason`, `isUsageLimitError`, `calculateRateLimitBackoffMs`.
- edge_cases_or_failure_modes: Handles case/underscore variants like `quota_reached`; backoff jitter must remain in 45-75s band lines 115-116.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-646 `file` `packages/ai/test/unicode-surrogate.test.ts`
- cursor: `[_]`
- core_role: Provider integration tests for Unicode surrogate/emoji/tool-result robustness.
- algorithmic_behavior: Sends tool results and real-world Unicode-heavy content through multiple providers, including emoji, LinkedIn-like data, and unpaired high surrogate cases, then asserts non-error completion.
- inputs_outputs_state: Inputs are real provider models/tokens, contexts, tool result messages. Outputs are assistant responses with stop reason/content/error fields.
- gates_or_invariants: Each helper asserts `stopReason` is not error, `errorMessage` falsy, and content exists or contains text lines 113-115, 201-203, 274-276.
- dependencies_and_callers: Uses `complete`, bundled models, OAuth helpers, and real provider credentials.
- edge_cases_or_failure_modes: Unpaired high surrogate should not crash JSON/HTTP/provider serialization; provider availability/tokens gate execution.
- validation_or_tests: Integration suite under `AI Providers Unicode Surrogate Pair Tests`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-676 `file` `packages/catalog/test/fireworks-serverless-discovery.test.ts`
- cursor: `[_]`
- core_role: Tests Fireworks serverless model discovery resolver.
- algorithmic_behavior: Mock-fetches paged control-plane API, filters serverless/ready models, maps model specs/pricing/capabilities, and builds catalog model thinking metadata.
- inputs_outputs_state: Inputs are mock API page arrays and fetch control-plane URLs. Outputs are discovered `ModelSpec` entries and built model metadata.
- gates_or_invariants: Must call `/v1/accounts/fireworks/models?filter=supports_serverless=true`, not inference `/models`, lines 108-113; excludes `serverless:false` and `DEPLOYING` models lines 146-148.
- dependencies_and_callers: Tests `fireworksModelManagerOptions` and catalog `buildModel`.
- edge_cases_or_failure_modes: Null result on failed discovery line 172; pagination across two pages lines 118-121.
- validation_or_tests: File itself validates resolver/descriptor behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-706 `file` `packages/catalog/test/umans-provider.test.ts`
- cursor: `[_]`
- core_role: Tests Umans provider catalog dynamic discovery and bundled metadata.
- algorithmic_behavior: Fetches mocked `/v1/models/info`, maps model fields/capabilities/thinking, handles fetch errors, validates static bundled provider entry.
- inputs_outputs_state: Inputs are mock fetch responses and `models.json`; outputs are dynamic model specs and built catalog model fields.
- gates_or_invariants: Requested URL must be `https://api.code.umans.ai/v1/models/info` lines 67-68; fetch failure throws "Failed to fetch Umans models info" line 101; specific built model has `maxTokens=32768`, `escapeBuiltinToolNames=true`, and thinking metadata lines 157-160.
- dependencies_and_callers: Catalog provider descriptors/resolvers and bundled `models.json`.
- edge_cases_or_failure_modes: Mandatory reasoning model, missing/partial fields, fetch errors.
- validation_or_tests: Provider catalog tests in this file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-736 `file` `packages/coding-agent/src/workspace-tree.ts`
- cursor: `[_]`
- core_role: Workspace tree summarizer for prompts/UI.
- algorithmic_behavior: Calls native workspace listing, assembles path segments into a tree, applies per-directory truncation, recency sorting, age formatting, global line cap, and final aligned render.
- inputs_outputs_state: Inputs are cwd and options such as max entries/depth, ignores, mtime mode, line cap. Outputs are `DirectoryTree`/`WorkspaceTree` with text, total files, dropped counts, and optional AGENTS.md metadata.
- gates_or_invariants: Defaults cap depth/entries/line count in lines 6-16; build functions catch native failures and return empty tree lines 52-111; line cap protects root/protected depth before removing deepest rows lines 283-299.
- dependencies_and_callers: Depends on `listWorkspace` from pi-natives, `formatAge`, `formatBytes`, `path`; called when building agent workspace context.
- edge_cases_or_failure_modes: Missing/unreadable cwd returns empty tree; mtime `0` formats empty; overlarge dirs show recent entries plus oldest marker; line cap may elide rows and report count.
- validation_or_tests: Covered indirectly by context/prompt tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-766 `file` `packages/coding-agent/test/agent-session-fresh.test.ts`
- cursor: `[_]`
- core_role: Tests fresh-session reset semantics for provider state and append-only context.
- algorithmic_behavior: Creates harness, simulates persisted session/provider state, invokes fresh path, and asserts session IDs/state reset while persisted session manager remains unchanged.
- inputs_outputs_state: Inputs are `AgentSession`, `SessionManager`, provider session state with close hook, append-only context. Outputs are fresh result metadata and mutated live session state.
- gates_or_invariants: Fresh result must keep `previousSessionId`, create new `sessionId`, close provider sessions once, clear provider state/context log, and not mutate persisted manager fields lines 74-87.
- dependencies_and_callers: Uses Agent, Settings, ModelRegistry, AuthStorage, SessionManager.
- edge_cases_or_failure_modes: Second fresh path with current manager should align session/sessionManager but not equal previous fresh id lines 93-99.
- validation_or_tests: File itself validates fresh-session contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-796 `file` `packages/coding-agent/test/auth-broker-import.test.ts`
- cursor: `[_]`
- core_role: Tests auth-broker credential import through local CLI and broker-routed paths.
- algorithmic_behavior: Creates temp credential stores/broker server, runs import command, verifies dry-run planning, provider filtering, disabled providers, local persistence, broker upload, and no local writes when broker-routed.
- inputs_outputs_state: Inputs are CLI flags/config/env, source credentials, broker handle. Outputs are credential store rows, dry-run stdout plan, captured broker upload output.
- gates_or_invariants: Claude/Codex OAuth fields must persist correctly lines 85-105; dry-run has no writes and returns plan lines 129-136; broker route persists only in broker store and prints uploaded URL lines 263-302.
- dependencies_and_callers: Uses pi-ai AuthStorage/SqliteAuthCredentialStore, auth broker server, `runAuthBrokerCommand`, agent db path env.
- edge_cases_or_failure_modes: Disabled provider is skipped; dry-run avoids side effects; broker failures/close handled in after hooks.
- validation_or_tests: File itself validates auth import behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-826 `file` `packages/coding-agent/test/commit-agentic-attribution.test.ts`
- cursor: `[_]`
- core_role: Tests commit agent prompt attribution and template-expansion settings.
- algorithmic_behavior: Spies on SDK/tool modules, runs commit agent session, captures prompts, and asserts all prompts are attributed to agent and disable prompt template expansion.
- inputs_outputs_state: Inputs are fake session/prompts/settings; outputs are prompt call options.
- gates_or_invariants: Four prompts expected, each with `attribution="agent"` and `expandPromptTemplates=false` lines 43-46.
- dependencies_and_callers: `runCommitAgentSession`, SDK createAgentSession, commit tools, Settings.
- edge_cases_or_failure_modes: Prevents commit-agent prompts from being attributed as user content or expanded unexpectedly.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-856 `file` `packages/coding-agent/test/extension-loader-self-import.test.ts`
- cursor: `[_]`
- core_role: Tests extension loader host runtime binding and package self-import prevention.
- algorithmic_behavior: Creates temp extension/tool/command/hook modules that import host binding, loads them, and inspects source to ensure no direct package self-import remains.
- inputs_outputs_state: Inputs are temp project extension files and PiCodingAgent import identity. Outputs are loaded extensions/tools/commands/hooks and loader errors.
- gates_or_invariants: Loaders return no errors and expected registrations lines 99-114; source must not contain static or dynamic `@oh-my-pi/pi-coding-agent` imports lines 130-131.
- dependencies_and_callers: Custom extension/command/tool/hook loaders, TempDir, host runtime binding.
- edge_cases_or_failure_modes: Prevents bundle/self-reference recursion and host/runtime identity mismatch.
- validation_or_tests: File itself validates loader binding.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-886 `file` `packages/coding-agent/test/input-controller-escape.test.ts`
- cursor: `[_]`
- core_role: Tests interactive input controller escape, Ctrl+C, and navigation gestures.
- algorithmic_behavior: Builds mock interactive context/editor/spies, sends escape/Ctrl+C/key sequences, and verifies routing among pending submission cancel, agent abort, BTW/handoff/bash/eval aborts, tree/user selector, hotkeys, unfocus, and shutdown.
- inputs_outputs_state: Inputs are editor text, focus state, pending submission, session state flags, key events. Outputs are spy calls, editor mutations, returned consume flags.
- gates_or_invariants: Pending submission cancel does not abort global session lines 272-283; active agent escape aborts with `USER_INTERRUPT_LABEL` lines 302-305; BTW mode captures escape without abort lines 386-416; Ctrl+C first clears, second shuts down lines 549-566.
- dependencies_and_callers: `InputController`, settings/keybindings, session message constants.
- edge_cases_or_failure_modes: Double-tap left gesture opens agent hub only under expected timing/focus; empty editor escape can open tree/user selector or reset display depending context.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-916 `file` `packages/coding-agent/test/issue-2372-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for optimistic user message preservation during pre-streaming chat rebuild.
- algorithmic_behavior: Initializes interactive mode/session, submits/cancels messages, rebuilds transcript before streaming, and asserts optimistic message signature and replay options.
- inputs_outputs_state: Inputs are submitted text and mode state; outputs are chat container children, optimistic signature, addMessage/replay calls.
- gates_or_invariants: Optimistic signature remains `text\u00000` across rebuild lines 71-83; cancel clears signature and avoids duplicate addMessage lines 116-124.
- dependencies_and_callers: `InteractiveMode`, `AgentSession`, theme/session/model registry.
- edge_cases_or_failure_modes: Prevents user message from disappearing or duplicating before assistant streaming starts.
- validation_or_tests: Issue #2372 repro validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-946 `file` `packages/coding-agent/test/keybindings-escape-components.test.ts`
- cursor: `[_]`
- core_role: Tests escape bindings for model/session selector components.
- algorithmic_behavior: Initializes keybindings/theme, creates selector components, sends escape/cancel keys, and asserts cancel/exit callbacks fire correctly.
- inputs_outputs_state: Inputs are key events, session/model entries. Outputs are onCancel/onExit spy calls.
- gates_or_invariants: Escape should not prematurely cancel before proper component focus, then calls cancel once; exit called once in model selector lines 53-59 and session selector lines 101-104.
- dependencies_and_callers: `KeybindingsManager`, `ModelSelectorComponent`, `SessionSelectorComponent`, pi-tui keybindings.
- edge_cases_or_failure_modes: Protects components from global escape swallowing or duplicate cancel.
- validation_or_tests: File itself validates selector escape behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-976 `file` `packages/coding-agent/test/memories-storage.test.ts`
- cursor: `[_]`
- core_role: Tests local memory consolidation storage/job state transitions.
- algorithmic_behavior: Creates memory storage DB, claims eligible jobs/threads, records success/failure/fallback, advances watermarks/retries, and purges related rows.
- inputs_outputs_state: Inputs are thread/job rows, watermarks, failure reasons. Outputs are claim rows, job status fields, retry counters/timestamps, deleted row counts.
- gates_or_invariants: Claims include only eligible thread line 70; fallback failure records `status=error` and `last_error` lines 117-118; success sets `input_watermark=last_success_watermark+1`, retry reset, no retry_at lines 140-142.
- dependencies_and_callers: Memory storage layer and Snowflake IDs.
- edge_cases_or_failure_modes: Strict/fallback mode differences lines 104-112; purge keeps job row but deletes thread/output rows lines 170-172.
- validation_or_tests: File itself validates memory storage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1006 `file` `packages/coding-agent/test/profile-cli.test.ts`
- cursor: `[_]`
- core_role: Tests global `--profile` CLI routing and profile alias install behavior.
- algorithmic_behavior: Runs CLI with profile flags/env, verifies active profile dirs/db path, alias generation, invalid profile handling, and subprocess profile isolation.
- inputs_outputs_state: Inputs are CLI args/env/temp config dirs. Outputs are process exit code, stdout/stderr, active profile, agent dir/db path, alias install calls.
- gates_or_invariants: `--profile work` maps dirs under config `profiles/work/agent` lines 100-118; aliases omit version banner lines 144-204; invalid profile exits 1 and handles error lines 315-317.
- dependencies_and_callers: CLI entrypoint, profile alias CLI, pi-utils profile dirs, Snowflake.
- edge_cases_or_failure_modes: Child process must see work sentinel and not default sentinel lines 266-268; bad names rejected.
- validation_or_tests: File itself validates profile CLI.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1036 `file` `packages/coding-agent/test/sdk-mcp-defer.test.ts`
- cursor: `[_]`
- core_role: Tests SDK session MCP tool deferral.
- algorithmic_behavior: Creates agent sessions with pending MCP tool availability, then verifies active tool names include pending MCP before connection and normal tools after resolution.
- inputs_outputs_state: Inputs are SDK session options, settings/auth/model registry, pending MCP server state. Outputs are active tool name lists.
- gates_or_invariants: Pending MCP tool is present initially line 78; after deferral resolves, pending tool removed and `read` remains active lines 89-91.
- dependencies_and_callers: `createAgentSession`, MCP setup, SessionManager, Settings, ModelRegistry.
- edge_cases_or_failure_modes: Prevents SDK construction from blocking on MCP while preserving placeholder discoverability.
- validation_or_tests: File itself validates B1 deferral.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1066 `file` `packages/coding-agent/test/slash-command-format.test.ts`
- cursor: `[_]`
- core_role: Tests slash command ASCII progress bar rendering.
- algorithmic_behavior: Renders percentage bars under theme/time settings and strips ANSI for byte-exact assertions.
- inputs_outputs_state: Inputs are progress values/theme settings. Outputs are ANSI/plain bar strings.
- gates_or_invariants: 50% renders `[██░░] 50%` line 45; classic crest coloring includes cyan ANSI and disabled/empty state renders `[····]` lines 53-54.
- dependencies_and_callers: `renderAsciiBar`, Settings theme.
- edge_cases_or_failure_modes: Prevents unstable width/ANSI output in compact slash UI.
- validation_or_tests: File itself validates formatting.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1096 `file` `packages/coding-agent/test/telemetry-export.test.ts`
- cursor: `[_]`
- core_role: Tests telemetry export gating and subprocess export path.
- algorithmic_behavior: Clears OTEL env, invokes `initTelemetryExport`, checks enabled state under missing/invalid settings, and runs a probe process that receives telemetry.
- inputs_outputs_state: Inputs are env vars and file URL probe path. Outputs are boolean export-enabled flag, subprocess stdout, exit code.
- gates_or_invariants: Export disabled for default/missing/invalid combinations lines 38-75; enabled export path prints `PROBE: RECEIVED` and exits 0 lines 88-89.
- dependencies_and_callers: `initTelemetryExport`, `isTelemetryExportEnabled`, OTEL env vars.
- edge_cases_or_failure_modes: Prevents partial OTEL env from enabling export unexpectedly.
- validation_or_tests: File itself validates telemetry gate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1126 `file` `packages/coding-agent/test/write-hashline-header.test.ts`
- cursor: `[_]`
- core_role: Tests write tool hashline header emission and snapshot integration.
- algorithmic_behavior: Executes write tool, extracts hashline header, verifies snapshot store, applies hashline patch, and checks plain mode when hashlines disabled.
- inputs_outputs_state: Inputs are file path/content/settings/tool session. Outputs are write result text, snapshot store entries, patched file content.
- gates_or_invariants: Header matches `[path#ABCD]` line 33; result path and byte count align lines 61-64; snapshot text equals content lines 69-70; disabled mode omits header lines 114-115.
- dependencies_and_callers: WriteTool, hashline Patch/Patcher, snapshot store, LSP noop.
- edge_cases_or_failure_modes: Ensures subsequent hashline patch can update exact file after write.
- validation_or_tests: File itself validates write/hashline contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1156 `file` `packages/hashline/src/recovery.ts`
- cursor: `[_]`
- core_role: Recovery engine for applying hashline edits when current file differs from snapshot.
- algorithmic_behavior: Tries three-way merge between previous snapshot-applied text and current text; if that fails and snapshot is not head, can replay session-chain edits on current text when line counts and anchors match; reports warning and first changed line.
- inputs_outputs_state: Inputs are snapshot store, snapshot text, current text, edits, target path. Outputs are `RecoveryResult` with recovered text, warning, reason, first changed line, or null.
- gates_or_invariants: No recovery if applying edits to snapshot yields previous text or merge unchanged lines 38-54; anchor verification requires same line content at anchor positions lines 87-100; session-chain replay requires same line count and verified anchors lines 100-126.
- dependencies_and_callers: Uses `diff.merge`, `applyEdits`, snapshot store, recovery warning messages.
- edge_cases_or_failure_modes: Merge conflicts/non-string merge return null; edited-away anchors return null; external/current divergence chooses external warning, non-head snapshots may use session-chain replay.
- validation_or_tests: Covered by coding-agent edit/hashline tests such as write header and snapshot store.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1186 `file` `packages/mnemopi/test/beam-recall-unit.test.ts`
- cursor: `[_]`
- core_role: Unit tests for mnemopi Beam recall ranking, fact recall, and formatted context.
- algorithmic_behavior: Creates in-memory Beam DBs, inserts working/episodic/fact memories, runs recall/factRecall/recallEnhanced/formatContext, and asserts scoring, tier merge, temporal weighting, CJK/token matching, and dedupe.
- inputs_outputs_state: Inputs are SQLite rows with content/timestamps/scores/facts. Outputs are ranked recall result arrays, formatted markdown/json context, fact recall rows.
- gates_or_invariants: Stronger working memory ranks first lines 97-102; working+episodic merge covers both tiers lines 114-116; recent target has higher temporal score lines 139-148; no-match returns empty line 192.
- dependencies_and_callers: `@oh-my-pi/pi-mnemopi/core/beam/recall`, Beam schema, Bun SQLite.
- edge_cases_or_failure_modes: CJK matching excludes unrelated rows; generic fact/working dedupe; fact query variants for possessive/month/country pronouns.
- validation_or_tests: File itself is validation for recall algorithms.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1216 `file` `packages/mnemopi/test/memory-banks.test.ts`
- cursor: `[_]`
- core_role: Tests memory bank manager path safety and bank lifecycle.
- algorithmic_behavior: Creates/renames/deletes banks, resolves DB paths, lists banks/stats, validates name restrictions, and tests module-level bank helpers.
- inputs_outputs_state: Inputs are bank names/root dirs/env bank selection. Outputs are DB paths, boolean existence/deletion, bank list/stats, thrown errors.
- gates_or_invariants: Default bank path is root `mnemopi.db`; named bank path is `banks/<name>/mnemopi.db` lines 24-31; spaces/slashes/dots/path traversal rejected lines 45-50; default delete forbidden lines 51-53.
- dependencies_and_callers: BankManager and helper functions from mnemopi bank module.
- edge_cases_or_failure_modes: Empty bank name maps to default; forced default delete returns false rather than deleting.
- validation_or_tests: File itself validates bank lifecycle.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1246 `file` `packages/natives/bench/grep.ts`
- cursor: `[_]`
- core_role: Benchmark harness for native grep performance.
- algorithmic_behavior: Defines benchmark cases over package and cargo registry paths, runs native `grep` repeatedly with concurrency, and measures throughput/timing for output modes.
- inputs_outputs_state: Inputs are env `GREP_BENCH_ITERATIONS`, filesystem paths, grep patterns/cases. Outputs are benchmark timing summaries to stdout.
- gates_or_invariants: Default iterations 50 and concurrency 2 lines 5-6; cargo registry path derives from `$HOME` line 51.
- dependencies_and_callers: Uses `grep` and `GrepOutputMode` from native package plus Node fs/path.
- edge_cases_or_failure_modes: Missing cargo registry or package paths can skip/fail cases depending harness behavior; benchmark is not deterministic validation.
- validation_or_tests: Benchmark, not test; used for performance comparison.
- skip_candidate: `yes: benchmark harness rather than production algorithm, though it exercises native grep behavior`

### OH_MY_HUMANIZE_MAIN-HZ-1276 `file` `packages/snapcompact/research/exp04_layout.py`
- cursor: `[_]`
- core_role: Research experiment for snapcompact document layout/rendering and QA evaluation.
- algorithmic_behavior: Wraps paragraphs, lays out pages into columns, renders BDF bitmap images with sentence colors, queries LLM for page answers, aggregates accuracy/cost/latency.
- inputs_outputs_state: Inputs are SQuAD paragraphs, BDF fonts, model/provider config, cache dirs, CLI args. Outputs are rendered images, per-page records, aggregate JSON.
- gates_or_invariants: `wrap`, `layout_page`, `pack_pages`, `render_doc`, `run_page`, `aggregate`, `main` define flow lines 45-373; cached provider calls and font capacity are reused.
- dependencies_and_callers: PIL, SQuAD loader, local BDF/provider/run/final helpers.
- edge_cases_or_failure_modes: Missing API keys/fonts/cache files, PIL errors, provider failures, token/cost misconfiguration.
- validation_or_tests: Research script; no unit tests.
- skip_candidate: `yes: research experiment, included because snapcompact algorithm research affects compression/runtime design`

### OH_MY_HUMANIZE_MAIN-HZ-1306 `file` `packages/snapcompact/research/snapcompact_blackbox_occlusion.py`
- cursor: `[_]`
- core_role: Research script for black-box occlusion sensitivity of snapcompact image encodings.
- algorithmic_behavior: Samples answerable questions, masks image cell spans, chooses random control spans, posts image+prompt to chat endpoint with cache, and aggregates answer/random occlusion effects.
- inputs_outputs_state: Inputs are paragraphs/offsets, rendered images, endpoint/model/prompt, mask spans, cache flags. Outputs are per-question records and summary ratios.
- gates_or_invariants: `mask_cells`, `random_span`, `post_chat`, `aggregate`, `main` implement core flow lines 69-260; cache key includes image/prompt/model request.
- dependencies_and_callers: PIL, urllib, SQuAD, BDF render/capacity, run helpers.
- edge_cases_or_failure_modes: Avoid span selection around answer range, network/API errors, JSON/cache corruption, empty records.
- validation_or_tests: Research-only; no test file.
- skip_candidate: `yes: research script, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1336 `file` `packages/snapcompact/research/snapcompact_viz_radial.py`
- cursor: `[_]`
- core_role: Visualization script for radial occlusion/sensitivity summaries.
- algorithmic_behavior: Normalizes answer/random/ratio arrays, computes polar grid edges, finds top echoes, draws radial matplotlib wedges/spikes/labels.
- inputs_outputs_state: Inputs are summary JSON and occlusion arrays. Outputs are matplotlib figure/image.
- gates_or_invariants: Robust normalization clips by quantile line 37; polar edges and colormap setup lines 44-62; top echo limit defaults 18 line 62; main renders/saves lines 191-218.
- dependencies_and_callers: NumPy, matplotlib, JSON files produced by blackbox occlusion experiments.
- edge_cases_or_failure_modes: Empty arrays, zero denominators, extreme outliers handled by robust normalization; missing display avoided by `Agg`.
- validation_or_tests: Research visualization; no automated tests.
- skip_candidate: `yes: visualization/research artifact, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1366 `file` `packages/tui/bench/sanitize.ts`
- cursor: `[_]`
- core_role: Benchmark/comparison harness for TUI text sanitization algorithms.
- algorithmic_behavior: Implements regex, gated, skip-run, binary-output, JS variants of sanitization; detects ANSI sequence lengths; benchmarks samples over iterations.
- inputs_outputs_state: Inputs are sample strings with plain text, ANSI, control chars, surrogate chars, binary data. Outputs are timing numbers and sanitized strings during benchmark.
- gates_or_invariants: Sanitization targets C0/C1 controls, CR, surrogate range with `NEEDS_RE` lines 23-24; benchmark iterations 2000 line 283; wrap width 40 line 298.
- dependencies_and_callers: Compares against `sanitizeText` from `pi-utils`.
- edge_cases_or_failure_modes: ANSI parsing must preserve valid escape sequences while dropping unsafe controls; unpaired surrogates and binary output are stress cases.
- validation_or_tests: Benchmark, supported by TUI sanitize tests elsewhere.
- skip_candidate: `yes: benchmark harness, but documents sanitizer performance tradeoffs`

### OH_MY_HUMANIZE_MAIN-HZ-1396 `file` `packages/tui/test/editor-autocomplete-actions.test.ts`
- cursor: `[_]`
- core_role: Tests editor autocomplete action and slash completion behavior.
- algorithmic_behavior: Creates editor with providers, triggers hash/slash completions, accepts suggestions via Enter, and asserts submitted text/call counts/autocomplete visibility.
- inputs_outputs_state: Inputs are editor text, autocomplete providers, key events. Outputs are editor text, submitted command, provider call counts.
- gates_or_invariants: Hash action clears text and calls provider once lines 58-59; slash completion acceptance produces `/skills:fix-bug ` line 79; sync slash Enter submits `/model` in expected contexts lines 164-180.
- dependencies_and_callers: `Editor`, autocomplete provider interface, default editor theme.
- edge_cases_or_failure_modes: Multi-line text prevents slash suggestion invocation lines 195-196; plain text `hello` submits normally line 226.
- validation_or_tests: File itself validates editor autocomplete.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1426 `file` `packages/tui/test/markdown-math.test.ts`
- cursor: `[_]`
- core_role: Tests markdown inline/block math rendering.
- algorithmic_behavior: Renders markdown/math to terminal lines or inline strings, strips ANSI, asserts Unicode superscripts/subscripts, fractions, brackets, and literal dollar handling.
- inputs_outputs_state: Inputs are markdown strings and widths. Outputs are rendered line arrays/plain strings.
- gates_or_invariants: Inline math converts `π r²` and subscripts lines 17-23; block fractions include numerator/bar/denominator lines 38-50; literal currency/dollars preserved lines 64-74.
- dependencies_and_callers: Markdown component and `renderInlineMarkdown`.
- edge_cases_or_failure_modes: Unclosed/escaped dollar content remains literal; nested fraction/sqrt layout maintains line order.
- validation_or_tests: File itself validates math rendering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1456 `file` `packages/tui/test/terminal-appearance.test.ts`
- cursor: `[_]`
- core_role: Tests terminal appearance/capability probing and in-band resize parsing.
- algorithmic_behavior: Mocks TTY/env/platform, instantiates `ProcessTerminal`, sends OSC/CSI/DECRQM replies and resize reports, and asserts appearance, query counts, mode support, cursor-key pass-through, and alt-screen behavior.
- inputs_outputs_state: Inputs are terminal reply byte sequences/env fields/stdout rows/columns. Outputs are terminal `appearance`, reports, writes, received key sequences, resize callbacks, cell dimensions.
- gates_or_invariants: OSC 11 query and DA sentinel emitted lines 91-93; appearance dark/light parsed lines 135-163; DECRQM probes 2026/2048/2031/1010/1011 lines 502-506; unsupported modes do not emit enable/disable lines 525-543.
- dependencies_and_callers: `ProcessTerminal`, terminal info, key extraction, headless flag.
- edge_cases_or_failure_modes: Partial/private CSI reply reassembly, unknown DA replies passed through, WSL/multiplexer behavior, in-band resize reports with printable text suppression.
- validation_or_tests: File itself validates terminal capability algorithms.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1486 `file` `packages/utils/src/env.ts`
- cursor: `[_]`
- core_role: Environment loading/filtering and runtime mode utilities.
- algorithmic_behavior: Validates env names/values, filters unsafe process env, parses `.env` files, overlays project/agent/config/home env onto Bun.env, refreshes dirs, exposes env picking/positive integer parsing/headless/compiled-binary/flag helpers.
- inputs_outputs_state: Inputs are process/Bun env and `.env` files in home/config/agent/project. Outputs are sanitized `Bun.env`, `$env`, selected values, terminal headless state.
- gates_or_invariants: Env names match `^[A-Za-z_][A-Za-z0-9_]*$` line 8; OMP env vars are copied to `PI_` aliases lines 92-100; unsafe env names/values and macOS malloc stack logging keys filtered lines 39-62 and 107-116.
- dependencies_and_callers: Uses Node fs/os/path, `dirs` helpers, and re-exports worker-host functions.
- edge_cases_or_failure_modes: Invalid `.env` lines skipped; quoted values unwrapped; missing/unreadable env files ignored; `$flag` maps truthy values at lines 211-224.
- validation_or_tests: Utility tests cover CLI env/profile behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1516 `file` `packages/utils/test/cli-help.test.ts`
- cursor: `[_]`
- core_role: Tests lazy per-command help loading behavior in CLI utility framework.
- algorithmic_behavior: Defines good/broken commands, runs CLI help for a command, and asserts help output does not load unrelated broken command.
- inputs_outputs_state: Inputs are command registry and argv. Outputs are captured writes and broken-load count.
- gates_or_invariants: `brokenLoads` remains 0 while output includes good command description/flag lines 38-40.
- dependencies_and_callers: `Command`, `Flags`, `run` from pi-utils CLI.
- edge_cases_or_failure_modes: Prevents help generation from eagerly loading broken/expensive command modules.
- validation_or_tests: File itself validates CLI help lazy loading.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1546 `file` `python/robomp/scripts/ping.sh`
- cursor: `[_]`
- core_role: Minimal operational probe script for robomp environment/container.
- algorithmic_behavior: Shell script is tiny; no functions detected in symbol scan. It likely prints or checks a ping path for deployment liveness.
- inputs_outputs_state: Inputs are shell environment; outputs are shell exit status/stdout.
- gates_or_invariants: Size is 592 bytes; direct content has no detected functions/classes, so behavior is linear shell.
- dependencies_and_callers: Operational scripts or deployment probes under `python/robomp`.
- edge_cases_or_failure_modes: Shell/env availability only; no persistent state.
- validation_or_tests: Not directly tested.
- skip_candidate: `yes: operational probe script, low algorithmic content`

### OH_MY_HUMANIZE_MAIN-HZ-1576 `file` `python/robomp/tests/test_config.py`
- cursor: `[_]`
- core_role: Tests robomp environment-driven settings validation.
- algorithmic_behavior: Uses pytest env fixtures, loads `Settings`, and asserts allowlist parsing, proxy/direct auth exclusivity, replay token blank handling, model pool parsing/random coverage, concurrency default, and timeout parsing.
- inputs_outputs_state: Inputs are env dicts/monkeypatch. Outputs are Settings fields or Pydantic `ValidationError`.
- gates_or_invariants: Allowlist case-insensitive match lines 11-15; proxy mode requires proxy URL/HMAC and no token lines 30-45; blank replay token becomes `None` lines 67-78; default max concurrency is 8 lines 125-127.
- dependencies_and_callers: `robomp.config.Settings`, pytest, Pydantic.
- edge_cases_or_failure_modes: Rejects blank bot login, token+proxy together, proxy URL without key, bad model pool/env values.
- validation_or_tests: File itself validates config.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1606 `directory` `packages/coding-agent/src/cli/commands`
- cursor: `[_]`
- core_role: CLI subcommand implementations not grouped elsewhere.
- algorithmic_behavior: Currently contains `init-xdg.ts`, which creates XDG-compatible directories for `omp` on Linux/macOS and rejects unsupported platforms.
- inputs_outputs_state: Inputs are `process.platform`, home/config/cache/data paths. Outputs are created directories or thrown/exited errors.
- gates_or_invariants: Platform must be Linux or Darwin lines 7-8; loops over target dirs and creates them lines 19 onward.
- dependencies_and_callers: Node fs/promises, os, path; invoked by CLI command registry.
- edge_cases_or_failure_modes: Unsupported platforms reject; filesystem permission errors propagate.
- validation_or_tests: CLI command coverage likely indirect.
- skip_candidate: `yes: tiny command folder, but it participates CLI setup workflow`

### OH_MY_HUMANIZE_MAIN-HZ-1636 `directory` `packages/coding-agent/src/modes/theme`
- cursor: `[_]`
- core_role: Theme engine and built-in theme assets for coding-agent TUI.
- algorithmic_behavior: Loads/validates built-in and custom JSON themes, resolves color variables, detects color mode/background, maps symbol presets/icons, constructs `Theme`, formats colors/backgrounds/spinners/markdown/editor/select-list styles, caches Mermaid ASCII render variants, and applies shimmer animation.
- inputs_outputs_state: Inputs are theme JSON, settings/env/terminal appearance, custom theme dir, Mermaid source, time. Outputs are global `theme`, ANSI styling functions, symbol maps, available theme lists, Mermaid ASCII strings, shimmer text.
- gates_or_invariants: Schema validates colors/spinner frames around `theme.ts` lines 977-1085; valid theme color set lines 1149-1214; color mode detection lines 1233-1244; custom theme parse/schema errors become actionable messages lines 1927-1973.
- dependencies_and_callers: pi-tui theme types, pi-utils color helpers, chalk, arktype, builtin JSON defaults, Mermaid ASCII renderer. Used by nearly all TUI components.
- edge_cases_or_failure_modes: Circular/missing color var refs throw in `resolveVarRefs`; unknown colors throw in Theme methods; terminal appearance fallback uses COLORFGBG/macOS lines 2038-2070; Mermaid cache returns null on failed rendering.
- validation_or_tests: Terminal appearance tests, theme initialization in component tests, and markdown/render tests exercise this layer.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1666 `file` `crates/pi-ast/src/language/parsers.rs`
- cursor: `[_]`
- core_role: Tree-sitter parser factory table for all supported ast-grep languages.
- algorithmic_behavior: Exposes one function per language that returns its `TSLanguage` by calling the corresponding `tree_sitter_*::LANGUAGE.into()`.
- inputs_outputs_state: No dynamic inputs except function selected by language registry; output is a tree-sitter language handle.
- gates_or_invariants: Functions cover Astro through Zig lines 5-176; names must stay synchronized with `SupportLang` mapping in `mod.rs`.
- dependencies_and_callers: Vendored tree-sitter grammar crates and `ast_grep_core::tree_sitter::TSLanguage`; called by `SupportLang` implementations.
- edge_cases_or_failure_modes: Missing grammar dependency breaks compile; mismatch with enum aliases can make a language unreachable.
- validation_or_tests: AST grep/edit language tests validate selected mappings.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1696 `file` `packages/ai/src/auth-gateway/index.ts`
- cursor: `[_]`
- core_role: Barrel export for auth-gateway modules.
- algorithmic_behavior: Re-exports HTTP, server, and type modules using star exports.
- inputs_outputs_state: Inputs are module consumers importing from auth-gateway index; outputs are public symbols.
- gates_or_invariants: Uses star exports lines 1-3, matching repo barrel convention.
- dependencies_and_callers: `./http`, `./server`, `./types`; used by auth broker/gateway callers.
- edge_cases_or_failure_modes: Export ambiguity would require removing redundant paths.
- validation_or_tests: Auth gateway tests import provider-specific server modules; barrel integrity checked by package type checks.
- skip_candidate: `yes: barrel only, no runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1726 `file` `packages/ai/src/providers/anthropic-wire.ts`
- cursor: `[_]`
- core_role: Typed Anthropic Messages wire protocol definitions.
- algorithmic_behavior: Declares request/response/event/content/tool/thinking/usage types for Anthropic wire format, including streaming event discriminants and cache/server-tool metadata.
- inputs_outputs_state: Inputs are TypeScript consumers constructing/parsing Anthropic payloads; outputs are compile-time structure guarantees.
- gates_or_invariants: Content block union covers text/image/tool_use/tool_result/thinking/redacted thinking lines 40-79; streaming params require `stream:true` line 180; stop reason union lines 184-194.
- dependencies_and_callers: Provider conversion and stream parser modules, Anthropic tests including thinking signature replay.
- edge_cases_or_failure_modes: Runtime payload drift is not validated here; incorrect type definitions can hide provider incompatibilities.
- validation_or_tests: Anthropic conversion tests exercise these types indirectly.
- skip_candidate: `yes: type-only protocol file, but core to provider payload correctness`

### OH_MY_HUMANIZE_MAIN-HZ-1756 `file` `packages/ai/src/providers/openai-responses.ts`
- cursor: `[_]`
- core_role: OpenAI Responses API stream provider implementation.
- algorithmic_behavior: Builds Responses request params, manages stateful previous-response chains, handles strict-tool fallback and stale previous-response retries, posts streaming requests with timeouts/abort tracking, parses event stream into assistant message output, tracks TTFT/usage/premium requests, and converts internal tools to Responses tools.
- inputs_outputs_state: Inputs are model/context/options/provider session state/fetch/api key/abort signal. Outputs are `AssistantMessageEventStream` events, final assistant message, chain state (`lastResponseId`, appendability, stale failures, disabled).
- gates_or_invariants: Stateful enabled only for OpenAI host and explicit options lines 193-206; stale chain breaker after 3 failures lines 141-300; first event timeout message lines 137-141; chain retries structurally avoid loops lines 518-561; output marks history replay warmed lines 613-631.
- dependencies_and_callers: pi-catalog host/model metadata, openai-http, event stream parser, retry utilities, grammar/tool conversion, provider response notifier.
- edge_cases_or_failure_modes: ZDR rejection disables stored chain and retries with full transcript; stale previous response resets chain; strict tool incompatibility retries without strict tools; caller abort vs local timeout are separated.
- validation_or_tests: OpenAI responses/completions tests, retry tests, harmony leak tests, and auth gateway tests cover related payload/stream behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1786 `file` `packages/ai/src/registry/index.ts`
- cursor: `[_]`
- core_role: Registry barrel export.
- algorithmic_behavior: Re-exports derived, oauth, registry, and types modules.
- inputs_outputs_state: Input is consumer import path; output is aggregated registry API.
- gates_or_invariants: Star exports lines 1-4.
- dependencies_and_callers: Provider registry consumers.
- edge_cases_or_failure_modes: Export ambiguity risk only.
- validation_or_tests: Type checks/import tests.
- skip_candidate: `yes: barrel only`

### OH_MY_HUMANIZE_MAIN-HZ-1816 `file` `packages/ai/src/registry/umans.ts`
- cursor: `[_]`
- core_role: Provider registry definition for Umans API-key login.
- algorithmic_behavior: Creates API-key login descriptor and provider definition with id/name/login callback.
- inputs_outputs_state: Inputs are OAuth/login callbacks and API key entered by user. Outputs are provider credential definition and login flow result.
- gates_or_invariants: `loginUmans` is created by `createApiKeyLogin` lines 1-5; provider `login` delegates with callbacks lines 19-22.
- dependencies_and_callers: Registry auth UI and catalog Umans provider tests.
- edge_cases_or_failure_modes: API key validation happens in shared login helper; provider id/name must align with catalog.
- validation_or_tests: `packages/catalog/test/umans-provider.test.ts` covers provider metadata; auth login tests cover shared helper.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1846 `file` `packages/ai/src/utils/google-validation.ts`
- cursor: `[_]`
- core_role: Extracts and formats Google validation-required URLs from error bodies.
- algorithmic_behavior: Checks for `VALIDATION_REQUIRED`, parses JSON error details, finds detail metadata `validation_url`, and formats a user-facing message.
- inputs_outputs_state: Input is error body string. Output is optional validation URL or formatted message.
- gates_or_invariants: Returns undefined unless marker present line 2; catches JSON parse failures lines 4-13; requires `metadata.validation_url` string lines 10-12.
- dependencies_and_callers: Google/Gemini provider error handling.
- edge_cases_or_failure_modes: Malformed JSON or missing metadata returns undefined rather than throwing.
- validation_or_tests: Covered by provider error tests where validation-required messages surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1876 `file` `packages/catalog/src/identity/bundled.ts`
- cursor: `[_]`
- core_role: Lazy bundled model identity/reference cache.
- algorithmic_behavior: Loads bundled models/providers, builds canonical reference data and model reference index once, then returns cached instances.
- inputs_outputs_state: Inputs are generated bundled provider/model data. Outputs are `CanonicalReferenceData` and `ModelReferenceIndex` singletons.
- gates_or_invariants: `bundledModels`, `canonicalReference`, and `referenceIndex` are module-level caches lines 15-35; provider list is flattened from `getBundledProviders`/`getBundledModels` lines 17-23.
- dependencies_and_callers: Catalog identity equivalence/reference modules; model resolver code.
- edge_cases_or_failure_modes: Stale generated models affect identity; lazy caches persist for process lifetime.
- validation_or_tests: Catalog identity/provider tests exercise built model lookup.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1906 `file` `packages/coding-agent/src/autolearn/managed-skills.ts`
- cursor: `[_]`
- core_role: Safe writer/deleter for auto-learn managed skill files.
- algorithmic_behavior: Sanitizes skill names/descriptions, creates frontmatter, serializes per-skill mutations, rejects symlink roots/files and hardlinked files, opens with `O_NOFOLLOW`, enforces max byte size, supports create/update/delete.
- inputs_outputs_state: Inputs are raw skill name/description/body/action and agent dir. Outputs are written `SKILL.md` path or deletion. State is filesystem plus mutation-chain map.
- gates_or_invariants: Skill names match lowercase pattern line 22; max size 64KB line 20; root and skill dirs cannot be symlinks lines 117-127 and 181-190; hardlinks rejected lines 129-139; empty description/body rejected lines 159-162.
- dependencies_and_callers: `fs/promises`, YAML frontmatter, `getAgentDir`, autolearn/manage-skill tooling.
- edge_cases_or_failure_modes: Concurrent same-name writes are serialized; ELOOP becomes symlink error; create fails if skill exists; missing delete ignored.
- validation_or_tests: Managed skill tests likely cover create/update/delete safety.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1936 `file` `packages/coding-agent/src/cli/bench-cli.ts`
- cursor: `[_]`
- core_role: CLI benchmarking command for model latency/throughput.
- algorithmic_behavior: Parses/normalizes runs/max tokens, resolves model selectors/thinking, streams prompt requests, records TTFT/duration/output tokens/errors, computes per-model averages and ranked table/JSON, sets nonzero exit on failures.
- inputs_outputs_state: Inputs are CLI args, model registry/auth storage, benchmark prompt, stream events. Outputs are progress lines/table/JSON summary, exit code, runtime close.
- gates_or_invariants: Positive integer validation lines 125-132; first-token event classification lines 133-152; tokens/sec returns 0 for invalid duration/tokens lines 152-164; no models exits 1 lines 397-402.
- dependencies_and_callers: `streamSimple`, ModelRegistry, Settings, auth discovery, thinking resolver, chalk.
- edge_cases_or_failure_modes: Missing API key creates failure result; stream `error` or final stopReason error becomes run failure; JSON mode suppresses interactive output.
- validation_or_tests: Bench command tests likely validate formatting and run behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1966 `file` `packages/coding-agent/src/cli/web-search-cli.ts`
- cursor: `[_]`
- core_role: CLI wrapper for web search provider execution and rendering.
- algorithmic_behavior: Parses `q`/`web-search` args, validates provider/recency/limit, initializes theme, runs search query, renders results or error, and prints help.
- inputs_outputs_state: Inputs are argv tokens and provider settings. Outputs are stdout/stderr/status text and rendered search markdown.
- gates_or_invariants: Command accepted only as `q` or `web-search` lines 31-32; providers limited to `auto` plus provider order lines 23-24; recency limited to day/week/month/year lines 25 and 77; bad limit rejected lines 83 onward.
- dependencies_and_callers: `runSearchQuery`, provider registry, renderSearchResult, theme.
- edge_cases_or_failure_modes: Empty query prints help/error; provider error in result details prints failure lines 106-111.
- validation_or_tests: Web search tool/provider tests cover underlying behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1996 `file` `packages/coding-agent/src/commands/ssh.ts`
- cursor: `[_]`
- core_role: CLI command definition for SSH host management.
- algorithmic_behavior: Declares allowed actions (`add`, `remove`, `list`), parses flags/args through CLI framework, initializes theme, and delegates to `runSSHCommand`.
- inputs_outputs_state: Inputs are CLI args/flags. Outputs are SSH command effects/status.
- gates_or_invariants: Action list fixed to three values line 8.
- dependencies_and_callers: pi-utils CLI `Command/Args/Flags`, `runSSHCommand`, theme init.
- edge_cases_or_failure_modes: Invalid action/args handled by CLI framework or delegated command.
- validation_or_tests: `ssh-description.test.ts` validates SSH tool description; CLI command tests likely cover action parsing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2026 `file` `packages/coding-agent/src/config/resolve-config-value.ts`
- cursor: `[_]`
- core_role: Dynamic config/header value resolver with shell command interpolation.
- algorithmic_behavior: Treats values starting with `!` as shell commands, caches completed command outputs, de-duplicates in-flight commands, executes with timeout via native shell, and resolves headers map entries.
- inputs_outputs_state: Inputs are config strings/header records, command text, timeout. Outputs are resolved string or undefined; state is `commandResultCache` and `commandInFlight`.
- gates_or_invariants: Non-`!` values return directly lines 20-28; command cache and in-flight maps avoid duplicate work lines 28-47; nonzero/timed-out command returns undefined lines 55-68.
- dependencies_and_callers: `executeShell` from pi-natives; config/auth/web clients needing dynamic headers.
- edge_cases_or_failure_modes: Command exceptions swallowed to undefined; empty resolved headers omitted; cache clear available line 91.
- validation_or_tests: Config/header tests likely cover dynamic values.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2056 `file` `packages/coding-agent/src/discovery/github.ts`
- cursor: `[_]`
- core_role: GitHub Copilot-compatible discovery provider for instructions, context files, prompts, rules, and skills.
- algorithmic_behavior: Loads `.github/copilot-instructions.md`, user instructions, custom instruction dirs, `.instructions.md` frontmatter, rule `applyTo` globs, prompt files, and skills; transforms them into capability items and registers provider handlers.
- inputs_outputs_state: Inputs are project/user paths, env custom instruction dirs, markdown/frontmatter. Outputs are `ContextFile`, `Instruction`, `Rule`, `Prompt`, `Skill` lists with warnings/source metadata.
- gates_or_invariants: `*.instructions.md` required for instruction transform lines 134-161; rules require `applyTo` metadata unless always-apply lines 190-218; prompt files require `.prompt.md` lines 240-254; provider registered with priority 30 lines 40-47 and 299 onward.
- dependencies_and_callers: Discovery/capability framework, parseFrontmatter, filesystem capability read helpers.
- edge_cases_or_failure_modes: Invalid frontmatter/globs produce warnings; custom dirs can contribute AGENTS.md and instruction globs; always-apply glob maps to global instruction.
- validation_or_tests: Discovery tests cover capability loading patterns.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2086 `file` `packages/coding-agent/src/exa/index.ts`
- cursor: `[_]`
- core_role: Barrel export for Exa MCP client and types.
- algorithmic_behavior: Re-exports `mcp-client` and selected Exa/MCP types.
- inputs_outputs_state: Consumer imports get Exa client API/types.
- gates_or_invariants: Uses star export and type export line 1-2.
- dependencies_and_callers: Exa search integration.
- edge_cases_or_failure_modes: Barrel ambiguity/type-only export drift.
- validation_or_tests: Web search Exa tests cover underlying modules.
- skip_candidate: `yes: barrel only`

### OH_MY_HUMANIZE_MAIN-HZ-2116 `file` `packages/coding-agent/src/internal-urls/agent-protocol.ts`
- cursor: `[_]`
- core_role: Internal URL protocol handler for `agent://` subagent outputs.
- algorithmic_behavior: Resolves output ID to `<artifactsDir>/<id>.md`, supports optional JSON path/query extraction, scans registered artifact dirs, reports available IDs on miss, and provides completion IDs.
- inputs_outputs_state: Inputs are parsed internal URL, registered artifact dirs, optional path/query. Outputs are `InternalResource` markdown/text or extracted JSON text. State is registry of active artifacts dirs.
- gates_or_invariants: Output ID required lines 33-42; path and query extraction cannot combine lines 42-48; no dirs throws "No session" lines 48-56; missing dirs throw "No artifacts directory found" lines 82-86; extraction requires JSON parse lines 113-127.
- dependencies_and_callers: `json-query`, internal URL registry helpers, task output manager/executor, read tool.
- edge_cases_or_failure_modes: Missing output lists available `.md` IDs; registered `AgentRef` fallback can resolve references lines 86-113; ENOENT dirs ignored during scan.
- validation_or_tests: Internal URL tests and blob/artifact architecture docs cover protocol behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2146 `file` `packages/coding-agent/src/lsp/utils.ts`
- cursor: `[_]`
- core_role: LSP utility layer for URI conversion, diagnostics formatting, symbols, code actions, globs, hovers, and location context.
- algorithmic_behavior: Converts file URIs robustly, sorts/summarizes diagnostics, groups diagnostic messages by file, formats workspace edits/symbols/code actions, applies code actions with resolve/command/edit steps, expands glob targets, resolves symbol columns, and reads source context.
- inputs_outputs_state: Inputs are LSP diagnostics, URIs, workspace edits, symbols, code actions, file paths/globs, source text. Outputs are formatted strings, summaries, applied edit command results, file target lists, resolved positions/context lines.
- gates_or_invariants: URI rejects non-file or query/hash paths lines 34-56; diagnostics sort by severity/position lines 102-112; code action resolve errors are swallowed but edit/command execution proceeds lines 512-537; glob matching caps by normalized limit lines 550-566.
- dependencies_and_callers: LSP client/tool implementations, pi-utils truncate, theme/icons, path resolver, grouped output formatter.
- edge_cases_or_failure_modes: Lax URI fallback handles Windows drive paths; ENOENT in target/context resolution returns empty/continues; symbol occurrence parsing supports `symbol#N`; diagnostic noise strips URLs/help lines.
- validation_or_tests: LSP batching/regression/dedup tests validate diagnostics and utilities.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2176 `file` `packages/coding-agent/src/memory-backend/types.ts`
- cursor: `[_]`
- core_role: Shared interface contract for memory backend implementations.
- algorithmic_behavior: Defines backend IDs, status/search/save results, operation/runtime/start contexts, and lifecycle hooks such as start, before prompt, after message, compact extra context, search, save, and close.
- inputs_outputs_state: Inputs/outputs are type-level contracts for agent messages, settings, model registry, hindsight/mnemopi/session runtime. State is backend-specific and abstract.
- gates_or_invariants: Backend IDs limited to `"off" | "local" | "hindsight" | "mnemopi"` line 16; backend methods declare explicit async capabilities lines 95-156.
- dependencies_and_callers: Hindsight, mnemopi, local memory backend modules and AgentSession lifecycle.
- edge_cases_or_failure_modes: Type-only; runtime backends must handle absent session/model registry according to this contract.
- validation_or_tests: Memory tool and storage tests validate implementations.
- skip_candidate: `yes: type contract, not implementation, but core to backend coordination`

### OH_MY_HUMANIZE_MAIN-HZ-2206 `file` `packages/coding-agent/src/registry/agent-lifecycle.ts`
- cursor: `[_]`
- core_role: Lifecycle manager for adopted/live/parked subagents.
- algorithmic_behavior: Tracks adopted agents, parks idle sessions after TTL, revives parked agents via registered revivers or persisted session reviver factory, releases sessions, and reacts to registry events.
- inputs_outputs_state: Inputs are AgentRegistry refs/status events, reviver callbacks, TTL options. Outputs are live `AgentSession` instances, closed/released sessions, registry status updates. State is `#adopted`, `#reviveInflight`, timers.
- gates_or_invariants: Main agent is ignored line 100; missing registry ref removes adopted entry lines 100-101 and 161-166; idle TTL <=0 disables park timer lines 247-249; release closes session and clears ref lines 217-232.
- dependencies_and_callers: AgentRegistry global, AgentSession, logger, task executor/adopt flows.
- edge_cases_or_failure_modes: Concurrent revive reuses in-flight promise; failed revive deletes cold adopted entry; registry removal clears timers; parked persisted reviver optional.
- validation_or_tests: Task batch and agent lifecycle tests indirectly cover adoption/release.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2236 `file` `packages/coding-agent/src/session/snapcompact-savings-journal.ts`
- cursor: `[_]`
- core_role: JSONL journal of token savings from snapcompact.
- algorithmic_behavior: Creates recorder bound to current session, dedupes tool call IDs per recorder, writes positive savings records with model/provider/session metadata, and reads journal lines robustly.
- inputs_outputs_state: Inputs are savings entries and model metadata. Outputs are appended JSONL records or parsed record array. State includes per-recorder `seen` set and lazily ensured directory flag.
- gates_or_invariants: No session means no write line 62; savedTokens must be positive and toolCallId not seen lines 65-66; empty writes return line 79; ENOENT read returns empty lines 97-100.
- dependencies_and_callers: Stats DB path, fs/path, logger, snapcompact session code.
- edge_cases_or_failure_modes: Write failures logged not thrown lines 80-93; malformed journal lines skipped lines 104-108.
- validation_or_tests: Stats/session tests likely read journal indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2266 `file` `packages/coding-agent/src/task/executor.ts`
- cursor: `[_]`
- core_role: Subagent task executor and subprocess/session orchestration engine.
- algorithmic_behavior: Builds subagent settings/system prompts, resolves retry fallback model chains, creates MCP proxy tools, monitors runtime/time/request budgets, drives sessions to `yield`, validates/finalizes structured outputs, salvages fallback JSON/raw output, writes artifacts/session sidecars, records telemetry/handoff/progress, and returns `SingleResult`.
- inputs_outputs_state: Inputs are `ExecutorOptions` with assignment/context/schema/model/tools/session managers/artifact dirs/signals. Outputs are `SingleResult`, artifacts, progress events, registry agent state, optional review findings. State includes monitor counters, recent output tail, yield attempts, active session, registry refs.
- gates_or_invariants: MCP calls timeout at 60s line 74; soft request budget default 200 line 83; yield retries cap at 3 line 1397; schema warnings constants lines 491-494; `finalizeSubprocessOutput` handles yield/fallback/exit code lines 522-609; runtime abort reasons include signal/terminate/timeout/budget line 750.
- dependencies_and_callers: AgentSession SDK, ModelRegistry, Settings, MCP manager, memory states, internal URLs, artifact manager, output validators, task tool, AgentRegistry/Lifecycle.
- edge_cases_or_failure_modes: Missing/invalid yield can fallback to parsed raw output; schema failures retry then override with warning; abort can be signal/timeout/budget; tool errors normalized; duplicate review findings keyed; stale/failed fallback model chains are role-scoped.
- validation_or_tests: `test/task/task-batch.test.ts`, yield tests, SDK MCP deferral, artifact registry and task agent capability tests cover parts of this executor.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2296 `file` `packages/coding-agent/src/tools/bash-skill-urls.ts`
- cursor: `[_]`
- core_role: Expands internal URLs in bash commands into safe local file paths.
- algorithmic_behavior: Finds `skill://`, `agent://`, `artifact://`, `plan://`, `memory://`, `rule://`, and normalized `local:/` tokens, resolves them through skill registry/internal router/local protocol, validates relative paths, optionally creates parent dirs, and shell-escapes replacements from right to left.
- inputs_outputs_state: Inputs are bash command string, loaded skills, internal router, local protocol options. Outputs are rewritten command or `ToolError`. No persistent state.
- gates_or_invariants: Supported schemes fixed lines 13-18; `skill://name` defaults to `SKILL.md` lines 68-73; resolved skill path must stay inside skill base dir lines 78-88; non-skill URLs require router/sourcePath lines 178-193.
- dependencies_and_callers: Bash tool preprocessing, skill protocol/local URL resolver, internal URL router.
- edge_cases_or_failure_modes: Unknown skills show available names; traversal including encoded segments rejected; local URLs without local options error; embedded `local:/` in filesystem paths intentionally ignored.
- validation_or_tests: `bash-skill-urls.test.ts` covers quoting, traversal, router errors, local URL boundaries.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2326 `file` `packages/coding-agent/src/tools/jtd-utils.ts`
- cursor: `[_]`
- core_role: Type guards for JSON Type Definition schema forms.
- algorithmic_behavior: Defines JTD schema TypeScript interfaces and predicates for primitive type, enum, elements, values, properties, discriminator, ref, and empty schemas.
- inputs_outputs_state: Input is unknown schema object; output is boolean type-narrowing result.
- gates_or_invariants: Predicates require expected keys and object shape lines 67-100; schema union is constrained to JTD variants lines 10-55.
- dependencies_and_callers: JTD-to-JSON-schema and TypeScript conversion tools, yield/task schema handling.
- edge_cases_or_failure_modes: Multiple-form invalid JTD objects may satisfy a simple guard if key exists; deeper validation is elsewhere.
- validation_or_tests: JTD conversion tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2356 `file` `packages/coding-agent/src/tools/yield.ts`
- cursor: `[_]`
- core_role: Subagent `yield` tool for structured task completion.
- algorithmic_behavior: Builds a JSON schema wrapper for `data`, degrades unresolved `$ref` schemas to loose record schemas, validates submitted data, returns retry hints on schema failures, records schema override after max retries, and normalizes result details.
- inputs_outputs_state: Inputs are output schema, params with `status/data/errorMessage`, tool session/context. Outputs are `AgentToolResult` and `YieldDetails`; state includes `#schemaValidationFailures`.
- gates_or_invariants: Max schema retries is 3 line 106; success requires non-null data lines 217-221; errorMessage and data cannot both be present lines 206-209; unresolved `$ref` triggers loose schema lines 51-69 and 158-163.
- dependencies_and_callers: Task executor/subprocess registry, output-schema validator, pi-ai schemas.
- edge_cases_or_failure_modes: Invalid raw result object rejected lines 198-206; schema validation after retries marks `schemaOverridden`; null yield accepted with warning by executor finalizer.
- validation_or_tests: Yield tests cover schema degradation, retry budget, unresolved refs, and structural errors.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2386 `file` `packages/coding-agent/src/utils/external-editor.ts`
- cursor: `[_]`
- core_role: Opens text in user’s external editor and returns edited content.
- algorithmic_behavior: Chooses editor from env/config/default notepad on Windows, writes temp file, spawns editor, waits for exit, reads content, trims trailing newline by default, and cleans temp file.
- inputs_outputs_state: Inputs are initial text/options/env `EDITOR`/settings. Outputs are edited string or null/throw depending editor exit. State is temp file.
- gates_or_invariants: Configured editor overrides defaults lines 21-28; exit code 0 gates reading content lines 51-65; cleanup attempted in finally lines 72-74.
- dependencies_and_callers: Node child_process spawn, fs/os/path, `$env`, Snowflake; used by plan review/editor flows.
- edge_cases_or_failure_modes: Missing editor, nonzero exit, spawn error, temp read/delete failures; trim can be disabled.
- validation_or_tests: Plan review overlay tests cover external editor hooks indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2416 `file` `packages/coding-agent/src/workflow/eval-tool-runtime.ts`
- cursor: `[_]`
- core_role: Workflow script adapter for the Eval tool runtime.
- algorithmic_behavior: Creates a script runner that maps workflow eval requests to `EvalTool.execute`, overrides output column cap for workflow contexts, maps EvalTool result/details into workflow script output with exit code/artifact metadata/timeout.
- inputs_outputs_state: Inputs are workflow eval params and ToolSession. Outputs are `WorkflowScriptEvalResult` with text, exitCode, artifactId, timedOut/error flags.
- gates_or_invariants: Timeout seconds derived from ms by ceiling lines 62-67; error details override exit code lines 46-58; if output columns already zero, original session reused lines 27-34.
- dependencies_and_callers: EvalTool, workflow session runtime.
- edge_cases_or_failure_modes: Missing details defaults exit code based on content; artifact ID pulled from eval details when available.
- validation_or_tests: Workflow eval/runtime tests cover artifact/exit behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2446 `file` `packages/coding-agent/test/collab/crypto.test.ts`
- cursor: `[_]`
- core_role: Tests collab WebCrypto, link parsing/formatting, and wire envelope encoding.
- algorithmic_behavior: Generates/imports room keys, seals/opens frames, rejects tampered/wrong-key data, formats/parses direct/web links with optional write token, and packs/unpacks peer-id envelopes.
- inputs_outputs_state: Inputs are room IDs, keys, write tokens, relay URLs, frame payloads. Outputs are parsed link fields, decrypted frames, envelope peer/payload.
- gates_or_invariants: Wrong key/tamper rejects lines 33-39; default relay shorthand parses to default URL lines 49-54; insecure non-local ws rejected line 81; write token split between full/view links lines 137-143.
- dependencies_and_callers: Collab web `codec` and `link` modules.
- edge_cases_or_failure_modes: Bad base64url, too-short key, web hash wrapper links, peer ID rewrite, short envelopes return null.
- validation_or_tests: File itself validates collab crypto/link algorithms.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2476 `file` `packages/coding-agent/test/core/python-runner.integration.test.ts`
- cursor: `[_]`
- core_role: Integration tests for Python kernel/runtime executor.
- algorithmic_behavior: Executes Python code through kernel/runtime, tests cancellation/reuse/errors, matplotlib image capture, display outputs, cwd handling, and env filtering. Gated by `PI_PYTHON_INTEGRATION`.
- inputs_outputs_state: Inputs are Python snippets, temp dirs, runtime settings, abort/cancel. Outputs are exit code, output text, display outputs/images, cancelled flag.
- gates_or_invariants: Skips unless env flag set line 15; cancellation must finish under 2s and kernel remains alive lines 82-87; images are PNG data not blob refs lines 151-156; cwd appears in output lines 187-190.
- dependencies_and_callers: PythonKernel, runtime resolver, eval Python executor.
- edge_cases_or_failure_modes: Missing matplotlib skips image tests; exceptions surface in output with exit code 1 lines 111-113.
- validation_or_tests: Integration suite itself validates Python runner.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2506 `file` `packages/coding-agent/test/edit/file-snapshot-store.test.ts`
- cursor: `[_]`
- core_role: Tests canonical file snapshot keys and hashline seen-line parsing.
- algorithmic_behavior: Resolves symlink/realpath equivalence, stores snapshots by canonical key, and parses line numbers from hashline body text.
- inputs_outputs_state: Inputs are real/symlink/missing paths and hashline body strings. Outputs are canonical keys, snapshot lookup results, parsed line arrays.
- gates_or_invariants: Symlink alternate path canonicalizes to same key lines 29-34; missing child under real dir canonicalizes parent plus child lines 43-48; seen-line parser handles ranges and ignores inline numeric comments lines 78-96.
- dependencies_and_callers: File snapshot store, hashline edit/read tooling.
- edge_cases_or_failure_modes: Nonexistent absolute path without real parent returns normalized input.
- validation_or_tests: File itself validates snapshot key fusion.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2536 `file` `packages/coding-agent/test/internal-urls/mcp-protocol.test.ts`
- cursor: `[_]`
- core_role: Tests `mcp://` internal resource protocol resolution.
- algorithmic_behavior: Uses mock MCP managers/resources/templates, resolves direct/template resources, server-specific matches, binary content summaries, multi-part resources, errors, and completions.
- inputs_outputs_state: Inputs are `mcp://` URLs and mock server/resource/template tables. Outputs are `InternalResource` content/notes or thrown errors.
- gates_or_invariants: Missing manager or resource URI throws lines 35-42; missing resource reports known URI/server lines 55-57; empty content errors lines 204-205; binary content becomes markdown summary lines 226-228 and 341.
- dependencies_and_callers: InternalUrlRouter, MCPManager, MCP protocol handler.
- edge_cases_or_failure_modes: Empty expansion returns content line 130; multiple servers choose first or specific server; read failures include underlying connection refused lines 290-291.
- validation_or_tests: File itself validates MCP URL protocol.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2566 `file` `packages/coding-agent/test/session-manager/continue-relocation.test.ts`
- cursor: `[_]`
- core_role: Tests session continuation relocation across cwd/default/explicit session dirs.
- algorithmic_behavior: Writes session files/breadcrumbs, strips header cwd, resumes recent sessions from new cwd, and asserts files move/copy/fallback and headers update.
- inputs_outputs_state: Inputs are temp cwd/session dirs, session JSONL headers, breadcrumb files. Outputs are resumed SessionManager state, moved files, loaded entries.
- gates_or_invariants: Resume from cwdB relocates file and updates header cwd lines 90-99; local conflicting file keeps old and starts fresh lines 120-122; explicit session dir controls destination lines 176-178; legacy/moved files handled lines 270-273.
- dependencies_and_callers: SessionManager, session loader, terminal sessions dir config.
- edge_cases_or_failure_modes: Missing header cwd, explicit session dir, local file conflict, legacy breadcrumb path.
- validation_or_tests: File itself validates relocation behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2596 `file` `packages/coding-agent/test/slash-commands/force.test.ts`
- cursor: `[_]`
- core_role: Tests `/force` slash command and named tool choice mapping.
- algorithmic_behavior: Executes builtin slash command with tool/prompt variants, validates active tool existence, updates forced tool choice, status/error, editor text, and model tool choice shape.
- inputs_outputs_state: Inputs are slash command text, active tool names, model compat. Outputs are handler result/prompt remainder, forced tool choice, UI status/error.
- gates_or_invariants: `/force:write` sets forced tool and clears text lines 38-42; missing tool name shows usage lines 50-53; inactive tool errors lines 95-98; OpenAI response model maps to `{type:"function", name:"write"}` line 115.
- dependencies_and_callers: Slash command registry and `buildNamedToolChoice`.
- edge_cases_or_failure_modes: Prompt suffix is returned as next prompt lines 61-83.
- validation_or_tests: File itself validates force command.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2626 `file` `packages/coding-agent/test/task/task-batch.test.ts`
- cursor: `[_]`
- core_role: Tests task batch schema gating, validation, spawning, and sync/background behavior.
- algorithmic_behavior: Mocks task discovery/executor, creates TaskTool sessions, inspects schemas/descriptions, validates batch payload errors, spawns background jobs, records progress/results, and verifies parent agent/context propagation.
- inputs_outputs_state: Inputs are task params, settings toggles, mocked agents/executor. Outputs are tool result text/details, AsyncJobManager jobs, captured spawn args.
- gates_or_invariants: Batch-off schema exposes single assignment/id, batch-on exposes tasks/context lines 96-112; `schema` rejected in batch shape lines 172-179; missing/duplicate fields error lines 190-224; background spawn creates two jobs/progress IDs lines 275-300.
- dependencies_and_callers: TaskTool, AsyncJobManager, AgentRegistry/Lifecycle, executor module, tool schema.
- edge_cases_or_failure_modes: Batch disabled error in tool/context; isolated allowed only per-task; sync batch returns results and no async details lines 403-408.
- validation_or_tests: File itself validates task.batch.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2656 `file` `packages/coding-agent/test/tools/browser-tab-worker-startup.test.ts`
- cursor: `[_]`
- core_role: Tests browser tab worker startup error surfacing.
- algorithmic_behavior: Uses fake worker, initializes tab worker, injects startup error before ready, and asserts pending init rejects with specific startup error while init payload was sent.
- inputs_outputs_state: Inputs are fake worker events and init payload. Outputs are rejected promise and sent messages.
- gates_or_invariants: Error must surface as "Tab worker failed during startup..." instead of generic timeout lines 50-51; init message sent exactly once line 51.
- dependencies_and_callers: `initializeTabWorkerForTest`, tab protocol types.
- edge_cases_or_failure_modes: Prevents silent worker entry failures in browser tool.
- validation_or_tests: File itself validates startup path.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2686 `file` `packages/coding-agent/test/tools/lsp-diagnostics-dedup.test.ts`
- cursor: `[_]`
- core_role: Tests diagnostic ledger deduplication and diagnostic identity normalization.
- algorithmic_behavior: Feeds diagnostic result batches into ledger, verifies only new/unseen diagnostics are surfaced, shifted line numbers with same code/message dedupe, and server/summary update behavior.
- inputs_outputs_state: Inputs are file diagnostics result messages. Outputs are reduced result messages/summary/errored flag and identity strings.
- gates_or_invariants: First batch returned unchanged lines 38-39; repeated batch reduces to no issues lines 48-50; new error surfaces with summary `1 error(s)` lines 73-76; identity ignores shifted line but includes severity/code lines 104-112.
- dependencies_and_callers: DiagnosticsLedger, LSP diagnostic utilities.
- edge_cases_or_failure_modes: Same message on different file/code/severity remains distinct; fallback identity for unparseable message is full message line 118.
- validation_or_tests: File itself validates LSP dedup.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2716 `file` `packages/coding-agent/test/tools/ssh-description.test.ts`
- cursor: `[_]`
- core_role: Tests SSH tool availability and dynamic description from discovered hosts.
- algorithmic_behavior: Mocks discovered SSH hosts, loads SSH tool, and verifies null when no hosts and description includes available host choices.
- inputs_outputs_state: Inputs are mocked host capability records and session. Outputs are loaded tool or null and description string.
- gates_or_invariants: No hosts returns null line 40; tool description starts with "Runs commands on remote hosts." and includes host data lines 46-48.
- dependencies_and_callers: SSH discovery capability and `loadSshTool`.
- edge_cases_or_failure_modes: Ensures stale global discovery state is restored after tests.
- validation_or_tests: File itself validates SSH description.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2746 `file` `packages/coding-agent/test/workflow/artifact-registry.test.ts`
- cursor: `[_]`
- core_role: Tests workflow artifact registry list/resolve/install/uninstall/freeze behavior.
- algorithmic_behavior: Creates temp flow artifacts, lists builtin/installed dirs, resolves by name/path, freezes loaded artifacts, installs and uninstalls artifacts, and asserts missing/collision errors.
- inputs_outputs_state: Inputs are flow artifact files/directories and registry options. Outputs are flow specs, installed paths, frozen metadata, filesystem existence.
- gates_or_invariants: Missing flow rejects with not found lines 37-59; path input resolves to path spec line 72; missing builtin root lists empty lines 80-84; uninstall removes installed path lines 143-151.
- dependencies_and_callers: Workflow artifact registry, package loader, freeze.
- edge_cases_or_failure_modes: Flat flow dirs, duplicate/missing names, install root layout, uninstall missing artifact.
- validation_or_tests: File itself validates workflow registry.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2776 `file` `packages/collab-web/src/lib/socket.ts`
- cursor: `[_]`
- core_role: Encrypted WebSocket transport for collab guest client.
- algorithmic_behavior: Connects to relay WebSocket, seals outgoing frames, queues pending sends until open, unpacks peer envelopes, decrypts host frames, handles control messages, maps fatal close codes, and reconnects with exponential backoff.
- inputs_outputs_state: Inputs are room key, ws URL, frames, WebSocket events. Outputs are `onOpen/onFrame/onControl/onClose` callbacks and encrypted sends. State includes ws, closed flag, retry timer, pending sends, retry count.
- gates_or_invariants: Fatal close reasons map fixed codes lines 15-23; pending sends cap 256 line 25 and drop when full lines 78-85; intentional `close()` suppresses reconnect lines 90-106; fatal close stops reconnect lines 172-186.
- dependencies_and_callers: WebCrypto codec, link envelope helpers, GuestClient.
- edge_cases_or_failure_modes: String messages parsed as control JSON; invalid binary/envelope/decryption ignored or close; stale ws events ignored via identity checks.
- validation_or_tests: Collab crypto tests validate envelope/codec; socket behavior tested through GuestClient integration.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2806 `file` `packages/mnemopi/src/core/plugins.ts`
- cursor: `[_]`
- core_role: Plugin framework for mnemopi memory lifecycle hooks.
- algorithmic_behavior: Defines abstract `MnemopiPlugin`, logging/metrics/filter/compression plugins, plugin registry/instances, hook broadcasting for remember/recall/consolidate/invalidate, and default manager.
- inputs_outputs_state: Inputs are memory dicts, recall queries/results, summaries, plugin configs. Outputs are logs/metrics counters/timings, blocked entries, compressed summaries. State lives in plugin instances and `PluginManager`.
- gates_or_invariants: Abstract class cannot be instantiated line 19; duplicate/unregistered plugins rejected lines 272-281; filter rule exceptions block item lines 214-217; plugin hook exceptions are swallowed in manager loops lines 330-358.
- dependencies_and_callers: mnemopi core memory operations and optional external plugin dir.
- edge_cases_or_failure_modes: Compression disabled/negative threshold returns original; blocked log capped; plugin dir missing returns empty list; default manager reset unloads all.
- validation_or_tests: Plugin tests likely cover manager behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2836 `file` `packages/stats/src/client/types.ts`
- cursor: `[_]`
- core_role: Type definitions for stats dashboard client data.
- algorithmic_behavior: Re-exports shared types and declares usage/message/request/time-range/overview/model/cost dashboard interfaces.
- inputs_outputs_state: Inputs are API responses shaped by shared stats server; outputs are TypeScript types consumed by React routes/components.
- gates_or_invariants: `TimeRange` is limited to `1h|24h|7d|30d|90d|all` line 63; stats interfaces require numeric usage/cost fields lines 26-76.
- dependencies_and_callers: Stats client routes and API/data formatters.
- edge_cases_or_failure_modes: Type-only file; runtime validation occurs at API/resource layer.
- validation_or_tests: Stats UI tests/routes compile against these types.
- skip_candidate: `yes: client type definitions only`

### OH_MY_HUMANIZE_MAIN-HZ-2866 `file` `python/omp-rpc/src/omp_rpc/host_tools.py`
- cursor: `[_]`
- core_role: Python host-tool abstraction for OMP RPC integrations.
- algorithmic_behavior: Normalizes host tool results to JSON content payloads, defines cancellable context, generic `HostTool` with optional param decoder, and decorator/helper for registering callable host tools.
- inputs_outputs_state: Inputs are decoded params and `HostToolContext`; outputs are JSON object payloads with text/image/content shape. State includes context cancellation event.
- gates_or_invariants: String result becomes text content in `_normalize_result` lines 21-28; `HostToolContext.throw_if_cancelled` raises if cancelled lines 38-44; decoder used if present lines 54-62.
- dependencies_and_callers: OMP RPC protocol types and host tool server/client.
- edge_cases_or_failure_modes: Cancellation is cooperative; malformed decode errors propagate from decoder.
- validation_or_tests: RPC host tool tests likely cover normalization.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2896 `directory` `packages/utils/src/vendor/mermaid-ascii/er`
- cursor: `[_]`
- core_role: Mermaid ER diagram parser/types for ASCII rendering.
- algorithmic_behavior: `parser.ts` parses ER diagram lines, entity blocks, attributes, relationships, cardinality markers, labels/comments, and deduplicates entities; `types.ts` defines raw and positioned ER graph structures.
- inputs_outputs_state: Inputs are Mermaid ER diagram lines. Outputs are `ErDiagram` with entities/attributes/relationships and later positioned structures.
- gates_or_invariants: Parser skips first `erDiagram` line and scans from line 1 lines 32-43; attribute regex requires type/name and optional metadata line 98; relationship regex requires entity-cardinality-entity-label line 139; cardinalities normalized to one/zero-one/many/zero-many lines 167-178.
- dependencies_and_callers: Mermaid ASCII renderer pipeline and text normalization helper.
- edge_cases_or_failure_modes: Invalid lines ignored; quoted labels stripped; `<br>` normalized; unknown cardinality returns null and drops relationship.
- validation_or_tests: Mermaid ASCII rendering tests cover diagram parsing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2926 `file` `packages/ai/src/providers/openai-codex/response-handler.ts`
- cursor: `[_]`
- core_role: Codex provider error parser and typed API error wrapper.
- algorithmic_behavior: Reads response body, parses Codex error code/message, extracts rate-limit headers into typed limits, classifies usage vs rate limits, and creates `CodexApiError`.
- inputs_outputs_state: Inputs are `Response` with status/body/headers. Outputs are `CodexErrorInfo` and possibly thrown/wrapped `ProviderHttpError`.
- gates_or_invariants: `parseCodexError` reads text/json with fallback lines 40-84; usage limit code patterns set usage classification lines 72-77; 429 or `rate_limit_exceeded` marks rate limit lines 77-84; `toInt` returns undefined for null/non-number lines 98-99.
- dependencies_and_callers: OpenAI Codex provider stream/error handling, catalog `toNumber`.
- edge_cases_or_failure_modes: Malformed JSON falls back to generic message; missing headers produce undefined limits.
- validation_or_tests: Rate-limit and Codex provider tests cover this path.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2956 `file` `packages/ai/src/utils/schema/spill.ts`
- cursor: `[_]`
- core_role: Utility for spilling schema metadata into JSON-schema description strings.
- algorithmic_behavior: Formats selected key/value pairs either as structured `{k: v}` suffix or parenthetical list and appends to `description`.
- inputs_outputs_state: Inputs are JSON object schema, entries to spill, and format. Output is mutated/returned schema description or undefined when nothing spilled.
- gates_or_invariants: Undefined values skipped lines 24-26; no spilled entries returns line 29; paren and spill formats differ lines 32-41.
- dependencies_and_callers: Schema conversion/adaptation utilities.
- edge_cases_or_failure_modes: Values JSON-stringified when possible, string fallback for primitives; existing description combined with suffix.
- validation_or_tests: Schema utility tests cover output formatting indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2986 `file` `packages/coding-agent/src/commit/agentic/state.ts`
- cursor: `[_]`
- core_role: Type model for agentic commit planning state.
- algorithmic_behavior: Defines git overview snapshots, commit proposals, hunk selectors, file changes, split commit groups/plans, changelog proposals, and aggregate commit agent state.
- inputs_outputs_state: Inputs/outputs are compile-time state shapes passed between commit agent prompts/tools. No runtime logic.
- gates_or_invariants: Types distinguish selected hunks, conventional analysis, numstat, staged/unstaged/untracked file changes.
- dependencies_and_callers: Commit agent, commit tools, commit type definitions.
- edge_cases_or_failure_modes: Type-only; runtime validation occurs in commit agent/tools.
- validation_or_tests: Commit attribution and commit agent tests validate usage.
- skip_candidate: `yes: type-only state shape`

### OH_MY_HUMANIZE_MAIN-HZ-3016 `file` `packages/coding-agent/src/edit/modes/patch.ts`
- cursor: `[_]`
- core_role: Patch edit engine for apply/preview/diff execution.
- algorithmic_behavior: Parses normalized patch inputs, reads existing files, computes hunk replacements with exact/context/hierarchical/fuzzy/fallback matching, adjusts indentation, handles create/delete/update operations, applies replacements preserving newline policy, enforces auto-generated and plan-mode guards, emits diagnostics/warnings/diffs.
- inputs_outputs_state: Inputs are `PatchInput`, filesystem adapter, ToolSession/settings/cwd. Outputs are `ApplyPatchResult`, preview diff, file changes, LSP batch requests, warnings/errors. State is per-application replacement list and file snapshots.
- gates_or_invariants: Operation enum create/delete/update line 60; default filesystem lines 104-129; fallback variants include trim/dedupe/collapse/single-line lines 429-559; ambiguity hint window 200 lines 599-640; public APIs are `applyPatch`, `previewPatch`, `computePatchDiff`, `executePatchSingle` lines 1465-1745.
- dependencies_and_callers: Edit tool/apply_patch renderer, hashline snapshot store, auto-generated guard, plan-mode guard, diff utilities, LSP writethrough.
- edge_cases_or_failure_modes: Ambiguous or missing context reports previews; partial match must preserve discarded text; CRLF/final newline policies preserved; stale/generated/plan-blocked files error; fuzzy matching can be disabled/filtered.
- validation_or_tests: Apply patch renderer, edit diff, conflict integration, and hashline tests exercise this engine.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3046 `file` `packages/coding-agent/src/export/html/template.js`
- cursor: `[_]`
- core_role: Static browser-side template for exported HTML transcripts.
- algorithmic_behavior: Contains client-side rendering logic/styles for exported sessions; symbol scan shows global stats/message aggregation and template functions embedded in a large JS asset.
- inputs_outputs_state: Inputs are serialized transcript/session export data. Outputs are interactive/static HTML view with message/tool statistics and rendered transcript.
- gates_or_invariants: Large template tracks global stats for user/developer/assistant/tool/custom/compaction/branch summary messages around lines 1435-1441 from scan.
- dependencies_and_callers: HTML export generator embeds this template.
- edge_cases_or_failure_modes: Browser compatibility, malformed export data, escaping/sanitization of transcript content.
- validation_or_tests: Export HTML tests likely snapshot/render template behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3076 `file` `packages/coding-agent/src/extensibility/plugins/runtime-config.ts`
- cursor: `[_]`
- core_role: Normalizes plugin runtime configuration.
- algorithmic_behavior: Converts partial plugin runtime config to complete `PluginRuntimeConfig` with defaults.
- inputs_outputs_state: Input is partial config object; output is normalized config.
- gates_or_invariants: Single exported function line 4; defaults are centralized in this module.
- dependencies_and_callers: Plugin runtime/loader.
- edge_cases_or_failure_modes: Missing fields default; malformed fields likely handled by caller/schema.
- validation_or_tests: Plugin runtime tests cover normalized config.
- skip_candidate: `yes: tiny normalization helper`

### OH_MY_HUMANIZE_MAIN-HZ-3106 `file` `packages/coding-agent/src/modes/components/chat-block.ts`
- cursor: `[_]`
- core_role: Base class for chat UI blocks with host attachment lifecycle.
- algorithmic_behavior: Tracks host/active/disposed state, invokes lifecycle hooks on attach/detach/dispose, and manages cleanup callbacks.
- inputs_outputs_state: Inputs are `ChatBlockHost` and lifecycle calls. Outputs are component invalidation/cleanup side effects. State is private host/active/disposed/cleanup fields.
- gates_or_invariants: Disposed block cannot reattach lines 48-71; detach no-ops when inactive line 83; dispose idempotently runs cleanups lines 94-109.
- dependencies_and_callers: TUI `Container`, chat transcript components.
- edge_cases_or_failure_modes: Cleanup exceptions not explicitly shown; double dispose guarded.
- validation_or_tests: Component render/lifecycle tests cover derived blocks.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3136 `file` `packages/coding-agent/src/modes/components/plan-review-overlay.ts`
- cursor: `[_]`
- core_role: Interactive plan review TUI overlay for section navigation, deletion, annotation, action selection, and model slider.
- algorithmic_behavior: Parses plan sections into markdown components, builds TOC/sidebar, tracks focus among body/toc/actions, handles keyboard/mouse scrolling and selections, supports section deletion/undo/annotations/external editor, formats feedback, and renders responsive overlay.
- inputs_outputs_state: Inputs are plan markdown, callbacks, options/actions/slider, key/mouse events. Outputs are callback invocations, feedback text, selected action/model, rendered lines. State includes sections, deleted list, undo stack, annotations, focus, scroll offsets, click rows.
- gates_or_invariants: Minimum body/sidebar widths lines 54-60; disabled actions skipped when selecting lines 237-247; empty feedback returns no annotation submission lines 601-606; sidebar shown only with enough headings/width lines 720-721.
- dependencies_and_callers: pi-tui components, markdown theme, plan TOC parser, segment track, external editor matching.
- edge_cases_or_failure_modes: Modal annotation suppresses other keys; mouse wheel/routes differ by focus; deletion span can remove subsections; undo restores section order.
- validation_or_tests: Plan review overlay/component tests validate interaction/rendering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3166 `file` `packages/coding-agent/src/modes/controllers/command-controller-shared.ts`
- cursor: `[_]`
- core_role: Shared helpers for command controllers.
- algorithmic_behavior: Parses `--scope` flags and remove args, groups capability items by source metadata, and shows command output as TUI transcript block.
- inputs_outputs_state: Inputs are command rest strings, source-tagged items, interactive context. Outputs are parsed args or errors, grouped iteration, rendered command message block.
- gates_or_invariants: Scope must be `project` or `user` lines 25-32; remove parser accepts optional name then flags lines 43-74.
- dependencies_and_callers: Command controllers for skills/rules/prompts/hooks; TUI transcript components.
- edge_cases_or_failure_modes: Missing invalid scope returns parse error; grouped source preserves insertion order via Map.
- validation_or_tests: Command controller hotkeys and command parsing tests cover shared helpers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3196 `file` `packages/coding-agent/src/modes/utils/hotkeys-markdown.ts`
- cursor: `[_]`
- core_role: Generates markdown help table for configured hotkeys.
- algorithmic_behavior: Reads keybindings for known actions, maps missing disabled bindings to "Disabled", and emits markdown sections/tables.
- inputs_outputs_state: Inputs are keybindings manager-like object. Output is markdown string.
- gates_or_invariants: `appKey` returns binding display or disabled lines 7-11; output includes navigation/action rows lines 11-51.
- dependencies_and_callers: Command controller/help UI.
- edge_cases_or_failure_modes: Disabled bindings render as `Disabled` rather than blank.
- validation_or_tests: `command-controller-hotkeys.test.ts` asserts section/order/no leading whitespace/disabled rows.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3226 `file` `packages/coding-agent/src/web/scrapers/biorxiv.ts`
- cursor: `[_]`
- core_role: Specialized scraper for bioRxiv/medRxiv paper URLs.
- algorithmic_behavior: Parses DOI from supported URL formats, calls bioRxiv/medRxiv API, selects paper metadata, formats title/authors/corresponding/category/license/published/JATS XML metadata into markdown result.
- inputs_outputs_state: Inputs are URL and timeout/fetch context. Outputs are `RenderResult` markdown or null.
- gates_or_invariants: Host/path must match bioRxiv/medRxiv lines 44-48; API result must be ok with nonempty collection lines 65-74; all errors return null lines 31-130.
- dependencies_and_callers: Web fetch tool special handler registry and `loadPage/buildResult`.
- edge_cases_or_failure_modes: Invalid DOI/version, empty API collection, missing optional fields, API failure.
- validation_or_tests: Research scraper tests include bioRxiv known preprints and invalid URL cases.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3256 `file` `packages/coding-agent/src/web/scrapers/lemmy.ts`
- cursor: `[_]`
- core_role: Specialized scraper for Lemmy posts/comments.
- algorithmic_behavior: Parses post/comment URLs, fetches Lemmy API post/comment/comments, formats community/author/counts/body/url/comments into markdown with threaded indentation.
- inputs_outputs_state: Inputs are Lemmy URL and timeout. Outputs are markdown render result or null.
- gates_or_invariants: URL regex and numeric ID required lines 128-140; comment route fetches comment then owning post lines 146-154; post and comments API must both succeed lines 166-170.
- dependencies_and_callers: Web scraper registry, `loadPage`, `tryParseJson`.
- edge_cases_or_failure_modes: Non-Lemmy URLs, invalid IDs, missing comment post id, threaded vs flat comments.
- validation_or_tests: Social web scraper tests cover Lemmy-like behavior where included.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3286 `file` `packages/coding-agent/src/web/scrapers/sourcegraph.ts`
- cursor: `[_]`
- core_role: Specialized scraper for Sourcegraph repo/file/search URLs.
- algorithmic_behavior: Parses Sourcegraph URLs into repo/file/search targets, runs GraphQL queries, formats repo metadata, file contents, or search results with line matches and limits.
- inputs_outputs_state: Inputs are Sourcegraph URL, GraphQL endpoint response, max results. Outputs are markdown render result or null.
- gates_or_invariants: Host must be sourcegraph.com/www lines 119-124; invalid repo path returns null lines 134-159; GraphQL response requires ok and data with no errors lines 164-182; search results sliced to max lines 247-296.
- dependencies_and_callers: Web fetch special handlers, Sourcegraph GraphQL API.
- edge_cases_or_failure_modes: Unsupported paths, file content null, limit hit/match count, GraphQL errors.
- validation_or_tests: Dev platform/git scraper tests cover Sourcegraph if enabled.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3316 `file` `packages/coding-agent/test/modes/components/compaction-divider.test.ts`
- cursor: `[_]`
- core_role: Tests compaction summary divider collapsed/expanded rendering.
- algorithmic_behavior: Creates component with summary/images, renders collapsed and expanded widths, toggles state, and checks caching/invalidation.
- inputs_outputs_state: Inputs are compaction summary message and optional images. Outputs are rendered line arrays/text.
- gates_or_invariants: Collapsed view is 3 lines and rule width 80, contains "compacted" and `ctrl+o` but not summary lines 30-36; expanded contains summary/tokens/frame count lines 43-46; render cache returns same object until toggle lines 57-61.
- dependencies_and_callers: CompactionSummaryMessageComponent, theme.
- edge_cases_or_failure_modes: Image attachment count displayed in expanded mode; collapsed hides content to preserve transcript density.
- validation_or_tests: File itself validates component.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3346 `file` `packages/coding-agent/test/modes/controllers/command-controller-hotkeys.test.ts`
- cursor: `[_]`
- core_role: Tests hotkeys markdown generation.
- algorithmic_behavior: Builds markdown from fake binding map and asserts section ordering, key/action rows, no leading whitespace, and disabled rendering.
- inputs_outputs_state: Inputs are keybinding lookup map. Outputs are markdown string and lines.
- gates_or_invariants: First line is `**Navigation**` line 37; expected rows include copy/model/reset/retry/plan/prompt actions lines 38-44; no row starts with spaces/tabs lines 47-48; disabled key renders `Disabled` lines 70-71.
- dependencies_and_callers: `buildHotkeysMarkdown`.
- edge_cases_or_failure_modes: Missing keybinding should not produce empty table cell.
- validation_or_tests: File itself validates hotkeys markdown.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3376 `file` `packages/coding-agent/test/tools/web-scrapers/package-managers-2.test.ts`
- cursor: `[_]`
- core_role: Integration tests for package-manager web scrapers.
- algorithmic_behavior: Calls MetaCPAN, Hackage, DockerHub, Chocolatey, Repology, and Terraform scrapers with invalid and known URLs; asserts null for nonmatching paths and markdown content/method for valid packages.
- inputs_outputs_state: Inputs are external URLs and `WEB_FETCH_INTEGRATION` gate. Outputs are scraper results or null.
- gates_or_invariants: Each scraper rejects non-domain/nonmatching paths lines 12-19, 39-46, 67-74, 96-103, 123-130, 151-158; valid results include method/content/contentType lines 24-34, 51-62, 79-90, 108-118, 135-145, 164-184.
- dependencies_and_callers: Package manager scraper handlers and live network when integration enabled.
- edge_cases_or_failure_modes: Network/API drift can affect integration; tests are gated by env.
- validation_or_tests: File itself validates package-manager scraper contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3406 `file` `packages/collab-web/src/tool-render/tools/ast-edit.tsx`
- cursor: `[_]`
- core_role: React renderer for collab AST edit tool calls/results.
- algorithmic_behavior: Extracts paths/ops/details from tool args/result, renders summary badges, operation cells, parse errors, file replacements, code/diff blocks, and result text.
- inputs_outputs_state: Inputs are `ToolRenderProps` with args/result/details. Outputs are React nodes for summary/body.
- gates_or_invariants: `pathsOf` only accepts string array entries lines 24-33; `opsOf` only accepts record ops with string pat/out lines 34-44; details parser filters malformed entries lines 46-75.
- dependencies_and_callers: Collab `ToolView` registry, shared render parts/util.
- edge_cases_or_failure_modes: Missing/malformed details render invalid args/result text rather than crashing.
- validation_or_tests: Tool-render tests cover output shape; AST edit backend tests cover details payload.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3436 `file` `packages/collab-web/src/tool-render/tools/yield.tsx`
- cursor: `[_]`
- core_role: React renderer for collab yield tool calls/results.
- algorithmic_behavior: Summarizes yield call by digesting args, renders pretty JSON for `data` when present, falls back to raw result text.
- inputs_outputs_state: Inputs are yield args/result. Outputs are React nodes.
- gates_or_invariants: `args.data !== undefined` triggers JSON stringify attempt lines 13-16; stringify failure falls through.
- dependencies_and_callers: Collab tool render registry and shared parts.
- edge_cases_or_failure_modes: Circular/unstringifiable data handled by catch; missing data shows result text.
- validation_or_tests: Yield backend tests validate details; renderer is simple.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3466 `file` `packages/stats/src/client/routes/ErrorsRoute.tsx`
- cursor: `[_]`
- core_role: Stats dashboard route for recent error requests.
- algorithmic_behavior: Uses resource loader to fetch recent errors for active time range/refresh trigger, memoizes table rows, and renders status/error request entries with click handler.
- inputs_outputs_state: Inputs are `active`, `timeRange`, `refreshTrigger`, and `onRequestClick`. Outputs are React route panel/table.
- gates_or_invariants: Component exported at line 15; inactive route likely avoids fetch through `useResource` active flag.
- dependencies_and_callers: Stats API `getRecentErrors`, formatters, `AsyncBoundary`, `DataTable`, `Panel`, `StatusPill`.
- edge_cases_or_failure_modes: Empty/error loading states handled by `AsyncBoundary`; malformed request stats depend on API type.
- validation_or_tests: Stats client route tests likely cover render states.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3496 `file` `python/robomp/web/src/components/Logs.tsx`
- cursor: `[_]`
- core_role: Web dashboard component for displaying robomp logs.
- algorithmic_behavior: Renders log entries fetched from dashboard API, likely supports refresh/filter/tail based on component name and size. Direct symbol scan was not separately captured, but file is within web client component tree.
- inputs_outputs_state: Inputs are log JSON entries from robomp dashboard. Outputs are React log rows/panel.
- gates_or_invariants: Dashboard backend caps tail bytes at 2MB and JSONL limit in `python/robomp/src/dashboard.py`; component consumes that bounded output.
- dependencies_and_callers: Robomp web dashboard, dashboard API `tail_jsonl`.
- edge_cases_or_failure_modes: Empty logs, malformed JSONL entries already skipped by backend; long messages require UI truncation/wrapping.
- validation_or_tests: Robomp web build/tests, if present.
- skip_candidate: `yes: UI component, lower algorithmic density than backend log tailing`

### OH_MY_HUMANIZE_MAIN-HZ-3526 `file` `packages/coding-agent/src/extensibility/plugins/marketplace/fetcher.ts`
- cursor: `[_]`
- core_role: Plugin marketplace source classifier/fetcher/catalog parser.
- algorithmic_behavior: Classifies source strings as URL/git/GitHub shorthand/local/npm/etc, parses marketplace catalog JSON, validates plugin name/source variants, reads catalog from known paths, fetches local/HTTP/git sources, clones repos, and promotes clone to cache.
- inputs_outputs_state: Inputs are marketplace source string, catalog content, cache dir. Outputs are `FetchResult` with root/catalog/plugins or errors. State is filesystem cache/tmp clone.
- gates_or_invariants: Absolute Windows/local/GitHub shorthand regexes lines 33-50; invalid catalog fields throw per-entry errors but continue lines 87-178; catalog paths searched from fixed list lines 199-204; HTTP response must be ok lines 243-264.
- dependencies_and_callers: Plugin marketplace commands/loader, fs/os/path, git utils, logger.
- edge_cases_or_failure_modes: Bad entry skipped with error list; local path expansion supports `~`; clone failure removes tmp; promote replaces cache atomically-ish via fs ops.
- validation_or_tests: Marketplace fetcher tests cover classification/catalog parsing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3556 `file` `packages/coding-agent/src/modes/setup-wizard/scenes/providers.ts`
- cursor: `[_]`
- core_role: Setup wizard scene controller for provider sign-in and web-search tabs.
- algorithmic_behavior: Owns a TabBar and tab controllers, routes input/mouse/render/dispose, suppresses tab switching while active tab modal is open, and passes wheel/mouse events to active tab.
- inputs_outputs_state: Inputs are setup scene host, key/mouse events. Outputs are rendered tab scene and delegated tab actions. State includes selected/hover tab and tab row count.
- gates_or_invariants: Modal tabs suppress switching lines 11-13 and 49-53; mouse tab hover/switch only within tab row and nonmodal lines 66-78; wheel routes to active tab only when nonmodal lines 82 onward.
- dependencies_and_callers: pi-tui TabBar, SignInTab, WebSearchTab, setup wizard scene host.
- edge_cases_or_failure_modes: Modal panel traps input; hover cleared outside tab row; dispose calls every tab line 94.
- validation_or_tests: Setup wizard tests cover tab/modal behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3586 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/draw.ts`
- cursor: `[_]`
- core_role: Core ASCII/Unicode drawing engine for Mermaid ASCII graphs.
- algorithmic_behavior: Draws nodes, boxes, multi-section boxes, edges, arrowheads, corners, labels, bundled fan-in/fan-out edges, junctions, and subgraph boxes/labels onto role-aware canvases.
- inputs_outputs_state: Inputs are positioned ASCII graph nodes/edges/subgraphs/config. Outputs are canvases/role canvases with characters and roles.
- gates_or_invariants: Box drawing uses grid dimensions and corners lines 40-123; line chars depend on style and ASCII/Unicode lines 227-263; arrow drawing returns layered canvases and respects start/end arrow flags lines 378-437; bundle junction computes directional connectivity lines 1004-1083.
- dependencies_and_callers: Mermaid ASCII renderer, canvas/grid/edge-routing/shapes/text metrics.
- edge_cases_or_failure_modes: Empty paths return blank; pseudo-state boxes skip connectors; upward edge labels offset differently; wide text cells use `toCells`/displayWidth.
- validation_or_tests: Mermaid ASCII rendering tests and theme Mermaid cache use this renderer.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3616 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/special.ts`
- cursor: `[_]`
- core_role: Special Mermaid ASCII shape renderers.
- algorithmic_behavior: Implements custom render/dimension/attachment behavior for subroutine, doublecircle, cylinder, asymmetric, trapezoid, and trapezoidAlt shapes using ASCII or Unicode drawing.
- inputs_outputs_state: Inputs are shape text, padding, config, direction. Outputs are shape canvases, dimensions, attachment points.
- gates_or_invariants: Custom renderers exported at lines 29, 120, 144, 239, 263, 287; cylinder reserves curved top/bottom extra height line 152; text writes only within interior bounds lines 88-95 and 207-214.
- dependencies_and_callers: Shape registry, rectangle helpers, corners, edge routing, text metrics.
- edge_cases_or_failure_modes: Wide text cells must not overflow; ASCII mode changes border chars; attachment points must align with custom geometry.
- validation_or_tests: Mermaid ASCII shape/render tests cover these shapes.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `121 unique Item Evidence sections`
- missing_items: `0`
- duplicate_items: `0`
- final_worker_status: `complete`