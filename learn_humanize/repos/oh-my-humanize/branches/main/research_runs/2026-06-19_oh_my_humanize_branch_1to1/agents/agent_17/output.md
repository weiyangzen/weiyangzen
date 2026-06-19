# agent_17 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-017 `file` `tsconfig.base.json`
- cursor: `[_]`
- core_role: Workspace-wide TypeScript compiler contract.
- algorithmic_behavior: Sets ES2024, ESNext modules, bundler resolution, strict type checking, arbitrary extension imports, JSON modules, Bun/assets ambient types, and no emit at `tsconfig.base.json:2-18`.
- inputs_outputs_state: Input is package `tsconfig` inheritance; output is checker/module-resolution behavior. No runtime state.
- gates_or_invariants: `strict`, `verbatimModuleSyntax`, `forceConsistentCasingInFileNames`, and `moduleDetection: force` are build invariants.
- dependencies_and_callers: Consumed by package-local TypeScript/Bun check configs.
- edge_cases_or_failure_modes: Bad `typeRoots` or missing `assets`/Bun types can break text/json/md import typing; `moduleResolution: Bundler` changes Node-style resolution assumptions.
- validation_or_tests: Validated indirectly by `bun check` across packages; no file-local test.
- skip_candidate: `yes: configuration only, but it gates all TypeScript build/runtime tooling behavior.`

### OH_MY_HUMANIZE_MAIN-HZ-047 `file` `docs/compaction.md`
- cursor: `[_]`
- core_role: Architecture document for compaction, handoff, branch summaries, extension hooks, persistence, and failure semantics.
- algorithmic_behavior: Defines session-entry model at `docs/compaction.md:24`, trigger classes at `:56`, overflow recovery vs idle maintenance at `:100`, snapcompact strategy at `:131`, pruning/useless-result elision/boundary logic at `:146-192`, summary/handoff generation at `:220-246`, and branch summarization at `:290-338`.
- inputs_outputs_state: Inputs are transcript entries, token budgets, provider usage, settings, hooks, file-operation context, and branch-switch events; outputs are compacted context, preserved display transcript, stored summary entries, handoff documents, and branch summaries.
- gates_or_invariants: Must preserve user-visible transcript, avoid cutting split turns incorrectly, honor settings/defaults at `:402`, and maintain hook semantics at `:351-389`.
- dependencies_and_callers: References `packages/agent/src/compaction/`, `AgentSession`, snapcompact inline behavior, session storage, and extension hooks.
- edge_cases_or_failure_modes: Overflow/incomplete recovery, idle threshold maintenance, split-turn boundaries, eliding useless results, file-operation context leakage/omission, and summary generation failures.
- validation_or_tests: Covered by assigned `packages/coding-agent/test/agent-session-handoff.test.ts` and `packages/coding-agent/test/snapcompact-inline.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-077 `file` `docs/tui-runtime-internals.md`
- cursor: `[_]`
- core_role: Runtime design document for TUI lifecycle, input routing, focus, rendering, status loaders, modes, resize, streaming, and cancellation.
- algorithmic_behavior: Describes runtime ownership at `docs/tui-runtime-internals.md:11`, boot/component assembly at `:30`, terminal lifecycle/stdin normalization at `:51`, input focus routing at `:72`, editor/controller key split at `:88`, append-only render loop at `:102`, safety constraints at `:122`, streaming updates at `:149`, and cancellation at `:198`.
- inputs_outputs_state: Inputs are terminal bytes, normalized key events, component state changes, streaming agent/tool events, resize events, and cancellation signals; outputs are differential terminal frames/status lines and mode transitions.
- gates_or_invariants: Append-only contract, sanitized/truncated render content, focus-aware input routing, and cancellation paths that do not corrupt terminal state.
- dependencies_and_callers: Documents packages `tui` plus coding-agent modes/controllers/components.
- edge_cases_or_failure_modes: Newline/status corruption, resize redraw mismatch, background/suspend transitions, throttled vs event-driven updates, and stale streaming components.
- validation_or_tests: Covered by assigned TUI tests such as `packages/tui/test/editor.test.ts`, `packages/tui/test/markdown.test.ts`, `packages/coding-agent/test/tui/*`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-107 `file` `scripts/macos-entitlements.plist`
- cursor: `[_]`
- core_role: macOS hardened-runtime entitlement policy for compiled `omp` binary.
- algorithmic_behavior: Grants JIT, unsigned executable memory, and disabled library validation at `scripts/macos-entitlements.plist:19-24`; comments explain Bun JavaScriptCore JIT and native addon `dlopen` requirements at `:5-17`.
- inputs_outputs_state: Input is macOS signing pipeline `scripts/ci-macos-sign.sh`; output is entitlement plist consumed by codesign. No mutable runtime state.
- gates_or_invariants: These entitlements are described as non-optional for Bun single-file executable and extracted native addon loading.
- dependencies_and_callers: macOS release/signing scripts and runtime native addon extraction.
- edge_cases_or_failure_modes: Missing library-validation entitlement makes commands touching natives abort; missing JIT entitlements kills MAP_JIT pages.
- validation_or_tests: Validated by macOS binary smoke/signing jobs, not directly by a unit test.
- skip_candidate: `yes: workflow/signing policy rather than an algorithm, but it gates runtime startup behavior.`

### OH_MY_HUMANIZE_MAIN-HZ-137 `directory` `packages/collab-web/test`
- cursor: `[_]`
- core_role: Contract tests for collaborative guest client, wire codec, markdown rendering, links, and local relay.
- algorithmic_behavior: `client.test.ts` verifies `GuestClient` frame application and snapshot state; `codec.test.ts` covers encryption/sealing vectors; `link.test.ts` tests room/key parsing and envelope round trips; `local-relay.test.ts` tests WebSocket relay behavior; `markdown.test.tsx` tests transcript Markdown soft-break and HTML escaping.
- inputs_outputs_state: Inputs are host frames, encrypted payloads, collab links, relay messages, and markdown strings; outputs are guest snapshots, decoded envelopes, accepted/rejected links, relayed messages, and rendered HTML.
- gates_or_invariants: Reject insecure non-local `ws://`, require 32/48-byte base64url keys, preserve assistant line breaks, escape raw HTML, maintain client subscription snapshots.
- dependencies_and_callers: Tests `packages/collab-web/src/lib/client`, codec/link/relay/markdown modules, and React/Solid render paths.
- edge_cases_or_failure_modes: Truncated envelopes, `%23`-mangled fragments, scheme-less hosts, localhost exception, read-only frames, and relay binary/text ordering.
- validation_or_tests: The directory itself is validation; key test names appear in `link.test.ts:17-124`, `client.test.ts:63`, `local-relay.test.ts:111`, `markdown.test.tsx:9`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-167 `directory` `python/robomp/tests`
- cursor: `[_]`
- core_role: Python test suite for roboomp GitHub bot orchestration, database queues, sandbox/worktrees, worker RPC, host tools, proxy, permissions, retries, and shutdown/cancel behavior.
- algorithmic_behavior: Recursively covers DB event claiming/rate limits/pending closures (`test_db.py:10-645`), GitHub webhook routing (`test_github_events.py`), sandbox/workspace lifecycle (`test_sandbox.py`), worker RPC and reminders (`test_worker.py`), host tools (`test_host_tools.py`), proxy client/server HMAC and git transport (`test_proxy_client.py`, `test_proxy_server.py`), queue cancellation/shutdown, config, pragmas, slot pools, permissions, retry, and smoke tests.
- inputs_outputs_state: Inputs are synthetic GitHub events, SQLite DB rows, temporary git repos, settings/env, RPC tool calls, slot UIDs, and proxy HTTP requests; outputs are queued/claimed events, branch/worktree mutations, comments/reviews/labels, DB state transitions, and worker lifecycle outcomes.
- gates_or_invariants: Deduplication by delivery, atomic claims under contention, blocked issue fairness, HMAC/timestamp validation, slot UID isolation, dirty worktree refusal, force-with-lease safety, shutdown drain/kill hooks, and bot authorization gates.
- dependencies_and_callers: Tests `python/robomp/src/robomp/*`, `python/omp-rpc`, GitHub client/proxy, sandbox, worker pool, DB migrations, and host tool bridge.
- edge_cases_or_failure_modes: Concurrency races, stale claims, partial clones missing blobs, credential redaction, attacker origins, oversized proxy bodies, invalid model pragmas, PR review mode restrictions, and root/non-root slot behavior.
- validation_or_tests: Directory is validation surface; `conftest.py` seeds env/dashboard assets and fixture isolation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-197 `file` `docs/tools/reflect.md`
- cursor: `[_]`
- core_role: Tool documentation for the `reflect` internal tool.
- algorithmic_behavior: Defines source, inputs, outputs, flow, modes, side effects, limits, errors, and notes at `docs/tools/reflect.md:5-93`; describes how reflection gathers/returns internal context rather than editing workspace content.
- inputs_outputs_state: Inputs are tool arguments and session context; outputs are structured reflection text/results. State is primarily transcript/session state.
- gates_or_invariants: Tool should respect documented caps, error behavior, and side-effect limits.
- dependencies_and_callers: Used by tool docs/readme surfaces and corresponding coding-agent tool implementation.
- edge_cases_or_failure_modes: Invalid mode/args, exceeded caps, unavailable context, and misinterpreting reflect as a write/action tool.
- validation_or_tests: No direct assigned test; validated indirectly by tool registry/rendering tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-227 `directory` `crates/pi-shell/src/minimizer`
- cursor: `[_]`
- core_role: Rust shell-output minimizer engine and command-specific filtering registry.
- algorithmic_behavior: `engine.rs` selects minimization mode and applies filters/pipeline overlays (`mode_for` at `engine.rs:30`, `apply` at `:83`); `detect.rs` tokenizes and identifies command/subcommand with wrapper/global-option skipping (`detect` at `detect.rs:16`); `plan.rs` parses shell programs/chains; `pipeline.rs` compiles TOML pipeline definitions and tests; `config.rs` loads settings/env/defaults; `primitives.rs` provides ANSI stripping, head/tail caps, grouping, dedup, regex filters; `filters/*` contains language/tool-specific reducers; `defs/*.toml` declares builtin pipelines.
- inputs_outputs_state: Inputs are command string, stdout/stderr, exit code, env/settings, and builtin/user pipeline definitions; output is `MinimizerOutput` with reduced content and metadata. State includes unknown-command counter and cached builtin pipeline registry.
- gates_or_invariants: Avoid minimizing unsafe shell-state/FD-mutating chains, keep failures and success visibility, cap bytes/lines by class, validate schema version `pipeline.rs:117`, and respect disabled legacy filters.
- dependencies_and_callers: Called by shell execution/rendering paths in coding-agent; depends on `brush_parser`, `regex`, TOML definitions, and command filters.
- edge_cases_or_failure_modes: Wrappers like `npx`, `uv`, `bundle`, `sudo`, `env`; compound shell commands; unknown commands; regex compile failures; commands with quiet success output; ANSI-heavy logs.
- validation_or_tests: Rust unit tests embedded in `detect.rs` plus pipeline `run_tests` at `pipeline.rs:440`; command fixtures under `filters/fixtures`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-257 `directory` `packages/coding-agent/src/discovery`
- cursor: `[_]`
- core_role: Discovery subsystem for importing external agent instructions, rules, MCP configs, skills, plugins, and built-in defaults.
- algorithmic_behavior: Provider loaders (`codex.ts`, `claude.ts`, `cursor.ts`, `gemini.ts`, `opencode.ts`, `vscode.ts`, `windsurf.ts`, `cline.ts`, `github.ts`, `ssh.ts`, `mcp-json.ts`, `agents-md.ts`) read user/project files; `helpers.ts` resolves source paths, parses booleans/CSV/frontmatter, scans skill dirs, discovers linked extension modules and Claude plugin roots (`helpers.ts:27-1063`); `at-imports.ts` expands `@file` references with depth/cycle/fence guards; `builtin-rules/*` provides static rule markdown.
- inputs_outputs_state: Inputs are cwd/home, project files, user configs, plugin registries, environment-expanded paths, and markdown/frontmatter; outputs are normalized discovery items/rules/settings/MCP entries/skills with source metadata and warnings. State includes plugin root caches and preloaded roots.
- gates_or_invariants: Bound `@` import depth (`MAX_AT_IMPORT_DEPTH = 5` at `at-imports.ts:31`), ignore code fences/inline code for imports, avoid recursive extension scans beyond documented rules, stable skill ordering, env expansion safety, and source-level user/project classification.
- dependencies_and_callers: Used by session/context initialization, task agent discovery, SDK/MCP discovery, and extension loading.
- edge_cases_or_failure_modes: Dangling symlinks, package manifests with missing files, duplicate plugin roots, malformed YAML/frontmatter, tilde/env expansion, nested `@` imports, and cache invalidation.
- validation_or_tests: Assigned `extensions-discovery.test.ts`, `sdk-mcp-discovery.test.ts`, and related discovery tests cover symlink/package/registry behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-287 `directory` `packages/coding-agent/src/tts`
- cursor: `[_]`
- core_role: Text-to-speech runtime, model download, worker protocol, audio synthesis, streaming playback, and WAV encoding.
- algorithmic_behavior: `downloader.ts` checks model/runtime cache and calls `ttsClient.download` (`downloader.ts:21-64`); `tts-client.ts` spawns/reuses worker subprocess with `__omp_worker_tts`, tracks pending requests and stream chunks; `tts-worker.ts` loads Kokoro/Transformers runtime, chooses tiny-model device/dtype, falls back devices, queues synthesize/stream requests, and emits progress; `streaming-player.ts` and `player.ts` select platform audio commands; `wav.ts` writes PCM16 WAV headers/samples; `models.ts` defines model specs.
- inputs_outputs_state: Inputs are text chunks, voice/model key, tiny-model settings, cache dirs, abort signals, and worker messages; outputs are audio chunks/files, progress events, playback processes, and cached runtime/model files. State includes worker handle, pending requests, stream sessions, model promise cache.
- gates_or_invariants: Cache existence must include runtime and model files, model key must resolve, worker protocol IDs match pending requests, audio clamp to int16, device fallback only on load errors, abort/cancel cleans stream/session state.
- dependencies_and_callers: Called from coding-agent voice/TTS features and CLI smoke paths; depends on `kokoro-js`, `@huggingface/transformers`, tiny model cache utils, subprocess host entry.
- edge_cases_or_failure_modes: Missing runtime package, worker spawn failure, unsupported device/dtype, partial stream cancellation, playback command unavailable, corrupted cache, and progress event normalization.
- validation_or_tests: Smoke hook in TTS client; no assigned direct TTS test beyond downloader source item.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-317 `directory` `packages/coding-agent/test/tui`
- cursor: `[_]`
- core_role: Tests coding-agent TUI hyperlink and status-line rendering contracts.
- algorithmic_behavior: `hyperlink.test.ts` validates OSC8 generation, settings modes, file URI resolution, URL wrapping, internal URL resolution, BEL/ST terminators; `status-line-newline-guard.test.ts` ensures status line render does not leak newlines.
- inputs_outputs_state: Inputs are settings (`terminal.hyperlinks`), TTY/env flags, file paths/URLs/internal URLs, and status strings; outputs are ANSI hyperlink sequences and single-line status strings.
- gates_or_invariants: Hyperlinks off/auto/always semantics, no hyperlinking under `NO_COLOR`/unsupported contexts unless forced, correct URI escaping, internal URL resolution safety, no embedded newline in status line.
- dependencies_and_callers: Tests TUI hyperlink helpers, settings, internal URL router, status-line renderer.
- edge_cases_or_failure_modes: Nonexistent paths, line/column fragments, URL escaping, alternate OSC terminators, terminal capability detection, and newline corruption.
- validation_or_tests: The directory itself is the validation surface; declarations at `hyperlink.test.ts:60-251`, `status-line-newline-guard.test.ts:10`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-347 `file` `crates/pi-iso/src/rcopy.rs`
- cursor: `[_]`
- core_role: Recursive-copy isolation backend for worktree/sandbox creation.
- algorithmic_behavior: `RcopyBackend` implements `IsolationBackend` (`rcopy.rs:20-23`), canonicalizes lower dirs (`:69`), prepares destination (`:95`), uses git worktree add/remove when source is git (`:113-150`), seeds dirty state via git diffs (`:187`), applies patches (`:247`), otherwise recursively copies dirs/files/symlinks (`:293-361`) and preserves mtimes (`:382-459`).
- inputs_outputs_state: Inputs are lower/source and merged/destination paths; outputs are created merged directory/worktree and copied dirty state. State is filesystem/git metadata.
- gates_or_invariants: Source must be existing directory, destination prepared/removed safely, git command failures map to `IsoError`, symlink behavior is platform-gated, dirty tracked/untracked state preserved.
- dependencies_and_callers: Implements `IsolationBackend` trait for pi-iso; depends on `git`, filesystem APIs, platform-specific symlink/mtime handling.
- edge_cases_or_failure_modes: Non-git copy fallback, destination already exists, git worktree remove failure, binary/untracked patches, symlink support differences on Windows, mtime set failure intentionally ignored in copy helpers.
- validation_or_tests: Validated by crate isolation/backend tests, not directly assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-377 `file` `crates/pi-natives/src/workspace.rs`
- cursor: `[_]`
- core_role: Native workspace scanner exposed to JS via N-API.
- algorithmic_behavior: Builds ignore-aware parallel walker (`workspace.rs:93`), applies excluded dirs and glob matching (`:34-53`, `:137-151`), identifies files/symlinks (`:155`), collects nearby `AGENTS.md` with depth/limit gates (`:163`), visits entries in parallel (`:191-251`), sorts/dedupes (`:274-279`), and returns `list_workspace` promise (`:354`).
- inputs_outputs_state: Inputs are root, glob/include options, cwd/config fields; outputs are `ListWorkspaceResult` entries and AGENTS paths. State is shared mutex-protected vectors and stop flag during traversal.
- gates_or_invariants: `AGENTS.md` depth min/max/limit at `:25-29`, `MAX_ENTRIES = 100_000`, excluded directories, ignore rules, sorted deduped output.
- dependencies_and_callers: Called by JS natives package for workspace listing; depends on `ignore`, `napi`, `parking_lot`, crate glob conversion.
- edge_cases_or_failure_modes: Symlinked files, huge repos triggering entry cap, invalid glob/root, ignored directories, traversal errors, duplicate entries from parallel walk.
- validation_or_tests: Covered indirectly by workspace/native integration tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-407 `file` `packages/agent/test/prompt-tools-loop.test.ts`
- cursor: `[_]`
- core_role: Tests agent loop support for owned in-band text tool calls.
- algorithmic_behavior: Verifies `<tool_call>` text execution, native tools stripped from wire, history re-encoded as text; Hermes/Qwen JSON tool-call dialect execution; and `PI_DIALECT=minimax` fallback when config dialect is unset (`prompt-tools-loop.test.ts:20-149`).
- inputs_outputs_state: Inputs are synthetic model streams with text tool-call encodings and tool registry; outputs are executed tool results and next-turn encoded context. State is loop conversation/history.
- gates_or_invariants: Tool calls embedded in prompt text must not leak as native tools when owned by prompt dialect; dialect selection must be stable.
- dependencies_and_callers: Tests `agentLoop`, prompt-tool dialect encoders/parsers, and tool execution plumbing.
- edge_cases_or_failure_modes: Mixed native/text tools, malformed/alternate dialect JSON, env-selected dialect fallback.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-437 `file` `packages/ai/test/anthropic-empty-error-tool-result.test.ts`
- cursor: `[_]`
- core_role: Regression test for Anthropic tool-result encoding.
- algorithmic_behavior: Tests that whitespace-only error `tool_result` blocks are filled so Anthropic does not reject them, while successful whitespace-only results remain unchanged (`anthropic-empty-error-tool-result.test.ts:68-84`).
- inputs_outputs_state: Inputs are context messages containing tool results; outputs are Anthropic message params. No persistent state.
- gates_or_invariants: Only error tool results get filler content; successful whitespace must preserve exact behavior.
- dependencies_and_callers: Tests Anthropic provider message conversion.
- edge_cases_or_failure_modes: Anthropic 400 on empty error content, accidental mutation of successful empty output.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-467 `file` `packages/ai/test/auth-gateway-openai-responses-caching.test.ts`
- cursor: `[_]`
- core_role: Regression test for auth-gateway OpenAI Responses prompt-prefix caching.
- algorithmic_behavior: Starts gateway-style flow and asserts instructions prefix is automatically cached across two turns (`auth-gateway-openai-responses-caching.test.ts:107`).
- inputs_outputs_state: Inputs are two Responses requests/session context; outputs are request payloads with cache-key/prefix behavior. State is gateway/session cache key.
- gates_or_invariants: Cache must attach to instructions prefix across turns without caller manually setting it.
- dependencies_and_callers: Tests `packages/ai/src/auth-gateway/server.ts` and OpenAI Responses shared request setup.
- edge_cases_or_failure_modes: Missing session ID, wrong cache key normalization, prefix not reused on second turn.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-497 `file` `packages/ai/test/cursor-exec-handlers.test.ts`
- cursor: `[_]`
- core_role: Tests Cursor provider exec-handler binding and request/history encoding.
- algorithmic_behavior: Verifies bound method `this` preservation, unbound handler failure, system prompt blob ordering/default fallback, resume vs user-message action selection, image-only turn handling, tool-result trailing history, and tool error formatting (`cursor-exec-handlers.test.ts:85-272`).
- inputs_outputs_state: Inputs are handler objects, prompt/system entries, user/image/tool-result messages; outputs are Cursor request actions and encoded history.
- gates_or_invariants: Method binding must be preserved, empty turns resume, image-only turns carry selected context, trailing tool result history remains available.
- dependencies_and_callers: Tests Cursor provider request encoder/exec handler integration.
- edge_cases_or_failure_modes: Lost `this`, empty system entries, final tool result, image-only user message, tool errors.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-527 `file` `packages/ai/test/image-limits.test.ts`
- cursor: `[_]`
- core_role: Tests image-count/size limits across AI provider transformations.
- algorithmic_behavior: Exercises provider image normalization, filtering, caps, resize/detail behavior, and model/provider-specific image constraints in request conversion.
- inputs_outputs_state: Inputs are contexts with many/image-heavy content blocks; outputs are transformed provider payloads with accepted, resized, downgraded, or placeholder image blocks.
- gates_or_invariants: Provider hard caps and non-vision handling must be enforced before sending requests; text fallbacks must preserve semantic placeholders.
- dependencies_and_callers: Tests Anthropic/OpenAI shared vision guard and provider encoders.
- edge_cases_or_failure_modes: Too many images, unsupported MIME/detail, non-vision model, mixed text/image content, cache/resizing reuse.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-557 `file` `packages/ai/test/json-parse.test.ts`
- cursor: `[_]`
- core_role: Tests streaming JSON parse utilities.
- algorithmic_behavior: Validates parser behavior for streamed/chunked JSON payload boundaries and throttled parsing.
- inputs_outputs_state: Inputs are JSON chunks/strings; outputs are parsed events/objects or parse errors. No persistent state beyond incremental parser buffer.
- gates_or_invariants: Must parse complete JSON only, tolerate valid chunk boundaries, and reject malformed JSON deterministically.
- dependencies_and_callers: Tests `packages/ai/src/utils/json-parse` used by streaming providers.
- edge_cases_or_failure_modes: Partial chunks, invalid JSON, multiple events, throttling boundaries.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-587 `file` `packages/ai/test/openai-completions-tool-result-images.test.ts`
- cursor: `[_]`
- core_role: Regression test for OpenAI Chat Completions tool-result image encoding.
- algorithmic_behavior: Verifies tool results containing images/text are converted into OpenAI completions-compatible message/content shapes without losing tool-call linkage.
- inputs_outputs_state: Inputs are assistant tool calls and tool-result content blocks with images; outputs are chat-completions messages and content parts.
- gates_or_invariants: Tool result images must preserve call ID/order where provider supports them and must not violate content shape expected by Chat Completions.
- dependencies_and_callers: Tests `openai-shared.ts` transform/build helpers and vision guard behavior.
- edge_cases_or_failure_modes: Mixed image/text results, unsupported model/provider, empty output, and multiple tool calls.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-617 `file` `packages/ai/test/raw-sse-sdk-capture.test.ts`
- cursor: `[_]`
- core_role: Tests raw SSE SDK capture/inspection behavior.
- algorithmic_behavior: Captures provider SSE streams and validates raw event preservation/mapping for diagnostics and replay.
- inputs_outputs_state: Inputs are synthetic SSE responses; outputs are captured SDK/raw event records and parsed assistant stream events.
- gates_or_invariants: Raw capture must not disturb stream consumption, event order, or error propagation.
- dependencies_and_callers: Tests AI streaming utilities/provider wrappers.
- edge_cases_or_failure_modes: Malformed SSE, stream close, event framing, diagnostic capture side effects.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-647 `file` `packages/ai/test/usage-attribution.test.ts`
- cursor: `[_]`
- core_role: Tests provider usage accounting and attribution.
- algorithmic_behavior: Validates token/cost/premium/cache usage assignment across provider responses and stream deltas.
- inputs_outputs_state: Inputs are usage payloads and model/provider metadata; outputs are normalized `Usage` records with cost/attribution fields.
- gates_or_invariants: Prompt/completion/cache/read/write tokens and premium multipliers must be attributed to correct request/model/provider.
- dependencies_and_callers: Tests AI providers and catalog cost calculation.
- edge_cases_or_failure_modes: Missing usage, partial stream usage, cache read/write fields, service-tier multipliers, provider-specific usage names.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-677 `file` `packages/catalog/test/gemini-thinking-loop-compat.test.ts`
- cursor: `[_]`
- core_role: Catalog regression test for Gemini thinking-loop compatibility.
- algorithmic_behavior: Verifies Gemini thinking metadata/routing remains compatible with loop behavior and effort/thinking policy.
- inputs_outputs_state: Inputs are Gemini model IDs and generated catalog metadata; outputs are classification/policy decisions used by AI loop.
- gates_or_invariants: Gemini thinking variants must not produce incompatible routing or unsupported effort loops.
- dependencies_and_callers: Tests catalog identity/model-thinking helpers consumed by providers.
- edge_cases_or_failure_modes: Variant IDs, preview suffixes, missing thinking metadata, generated policy drift.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-707 `file` `packages/catalog/test/variant-collapse.test.ts`
- cursor: `[_]`
- core_role: Catalog tests for model variant collapse, aliasing, and routing.
- algorithmic_behavior: Tests `collapseEffortVariants`, token stripping, derived thinking pairs, provider-wide collapse, aliases, wire model resolution, dynamic merge-point collapse, and antigravity discovery (`variant-collapse.test.ts:77-636`).
- inputs_outputs_state: Inputs are raw provider model specs, hand-table families, dynamic discovery results, stale snapshots; outputs are logical collapsed specs with routing/aliases/request IDs.
- gates_or_invariants: Collapse must be idempotent, provider-scoped, price-aware, denylist-safe, and preserve routing for effort/thinking variants.
- dependencies_and_callers: Tests catalog provider-model generation/resolution and model identity helpers.
- edge_cases_or_failure_modes: Stale alias rows, absent target members, thinking-only Claude family, price-divergent twins, hand-table conflicts, recycled bare IDs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-737 `file` `packages/coding-agent/test/acp-agent.test.ts`
- cursor: `[_]`
- core_role: Comprehensive ACP agent protocol/lifecycle regression suite.
- algorithmic_behavior: Covers multi-session lifecycle, plan mode advertisement/approval, config option updates, extension method filtering, message/tool replay, todo-to-plan updates, command availability, skill execution, prompt cancellation/queueing/cleanup, consumed builtins, and elicitation bridge (`acp-agent.test.ts:495-2214`).
- inputs_outputs_state: Inputs are ACP JSON-RPC calls, prompts, tool calls/results, todo results, config changes, elicitation responses, cancellation signals; outputs are ACP events/responses, session state, plan updates, usage, queued prompt behavior.
- gates_or_invariants: Only underscore ACP extension methods accepted, bootstrap update suppression, exactly-once config update per change, cleanup gates before new prompts/fork/close, elicitation fallback on timeout/abort/bad payload.
- dependencies_and_callers: Tests coding-agent ACP server/agent session integration, commands, plan mode, extension registry, elicitation.
- edge_cases_or_failure_modes: Silent abort replay, pending cancel timeout, queued prompt rejection, late async delivery, missing plan file, client without elicitation capability.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-767 `file` `packages/coding-agent/test/agent-session-handoff.test.ts`
- cursor: `[_]`
- core_role: Tests AgentSession compaction/handoff maintenance and context-full behavior.
- algorithmic_behavior: Verifies no auto-compaction after handoff, obfuscation of custom instructions and previous summaries, pre-prompt maintenance on oversized prompts, timeout fallback, provider-anchored usage accounting, immediate parent persistence, strategy toggles, deferred threshold handoff, dispose unblock, fallback when no handoff doc, disk save policy, and abort behavior (`agent-session-handoff.test.ts:141-1163`).
- inputs_outputs_state: Inputs are synthetic sessions, token usage, pending prompts, settings, signals; outputs are compact/handoff calls, persisted sessions/docs, strategy state transitions.
- gates_or_invariants: Avoid double-counting non-message tokens, do not run maintenance after final yield/off strategy, restore base system prompt before handoff, only auto handoffs saved when enabled.
- dependencies_and_callers: Tests `AgentSession`, compaction docs semantics, provider usage, session storage.
- edge_cases_or_failure_modes: Timeout once then fallback, provider usage anchoring, incomplete todos deferring continue, abort before/mid handoff, unchanged non-message tokens.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-797 `file` `packages/coding-agent/test/auth-broker-snapshot-cache.test.ts`
- cursor: `[_]`
- core_role: Tests encrypted auth-broker snapshot cache recovery.
- algorithmic_behavior: Verifies auth storage discovery boots from a fresh encrypted cache when broker is down and seeds encrypted cache after broker fetch (`auth-broker-snapshot-cache.test.ts:58-96`).
- inputs_outputs_state: Inputs are broker responses/failures and cache files; outputs are resolved auth storage snapshot and encrypted cache state.
- gates_or_invariants: Cache must be encrypted, usable only when fresh/valid, and populated after successful broker fetch.
- dependencies_and_callers: Tests auth storage discovery/cache code.
- edge_cases_or_failure_modes: Broker outage, missing/stale/corrupt cache, initial seed path.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-827 `file` `packages/coding-agent/test/commit-command-exit.test.ts`
- cursor: `[_]`
- core_role: Tests commit command exit behavior.
- algorithmic_behavior: Ensures commit-related command exits/returns according to CLI contract under tested conditions.
- inputs_outputs_state: Inputs are command invocation state and git/mock session setup; outputs are exit code or thrown/returned status.
- gates_or_invariants: Commit command must not leave ambiguous success/failure state.
- dependencies_and_callers: Tests coding-agent commit command path.
- edge_cases_or_failure_modes: Empty/no-op commit, command failure propagation.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-857 `file` `packages/coding-agent/test/extensions-discovery.test.ts`
- cursor: `[_]`
- core_role: Tests extension discovery and loading contracts.
- algorithmic_behavior: Verifies direct `.ts/.js`, subdirectory index, package `pi` manifest, symlinked dirs/files, precedence, one-level recursion, mixed paths, invalid/dangling symlinks, explicit paths, dependencies, command/tool/renderer/hook/shortcut/flag registration, disabled module separation, init errors, and empty explicit loads (`extensions-discovery.test.ts:10-704`).
- inputs_outputs_state: Inputs are temporary extension directory layouts, manifests, settings, extension modules; outputs are discovered module paths, registered commands/tools/renderers/hooks, and errors.
- gates_or_invariants: `pi` manifest precedence, index.ts over index.js, no recursion beyond one level, skip missing manifest paths, disabled hooks isolated, default export required.
- dependencies_and_callers: Tests `packages/coding-agent/src/discovery/helpers.ts` extension module discovery and extension loader.
- edge_cases_or_failure_modes: Dangling symlink, symlink name ending `.ts`, dependency resolution from extension node_modules, extension throws/no default export.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-887 `file` `packages/coding-agent/test/input-controller-followup-image.test.ts`
- cursor: `[_]`
- core_role: Tests input controller handling for follow-up images.
- algorithmic_behavior: Validates that image attachments in follow-up prompts are preserved/routed into the next user message correctly.
- inputs_outputs_state: Inputs are controller prompt text plus image attachment state; outputs are session prompt payload/content blocks.
- gates_or_invariants: Follow-up image state must not be dropped or misattached to previous turn.
- dependencies_and_callers: Tests coding-agent input controller/session prompt bridge.
- edge_cases_or_failure_modes: Image-only follow-up, mixed text/image, stale attachment carryover.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-917 `file` `packages/coding-agent/test/issue-2375-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for issue #2375 behavior.
- algorithmic_behavior: Encodes the reproduction scenario and asserts corrected agent/session/tool behavior for that issue.
- inputs_outputs_state: Inputs are specific session/test fixtures matching the bug; outputs are expected state/events after the reproduced flow.
- gates_or_invariants: The bug’s externally observed behavior must not regress.
- dependencies_and_callers: Tests coding-agent runtime path implicated by #2375.
- edge_cases_or_failure_modes: The exact historical reproduction plus adjacent state transitions.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-947 `file` `packages/coding-agent/test/keybindings-migration.test.ts`
- cursor: `[_]`
- core_role: Tests migration of keybinding settings/config.
- algorithmic_behavior: Verifies old keybinding forms migrate to current schema and preserve expected command bindings.
- inputs_outputs_state: Inputs are legacy settings payloads/files; outputs are normalized current keybinding settings.
- gates_or_invariants: Migration must be idempotent, preserve user intent, and reject/skip invalid bindings safely.
- dependencies_and_callers: Tests settings migration/keybinding loader.
- edge_cases_or_failure_modes: Missing fields, duplicate bindings, legacy names, invalid key strings.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-977 `file` `packages/coding-agent/test/memory-backend-resolve.test.ts`
- cursor: `[_]`
- core_role: Tests memory backend resolution.
- algorithmic_behavior: Verifies configured/default memory backend selection maps to the correct implementation.
- inputs_outputs_state: Inputs are settings/env/session config; outputs are resolved backend instance/name/options.
- gates_or_invariants: Unknown/unavailable backend should fall back or error according to contract; defaults stay stable.
- dependencies_and_callers: Tests coding-agent memory backend resolver and mnemopi backend integration.
- edge_cases_or_failure_modes: Missing setting, invalid backend key, disabled memory mode.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1007 `file` `packages/coding-agent/test/prompt-action-autocomplete.test.ts`
- cursor: `[_]`
- core_role: Tests prompt action autocomplete.
- algorithmic_behavior: Verifies slash/prompt action completion candidates, filtering, and insertion behavior.
- inputs_outputs_state: Inputs are partial prompt/action text and action registry; outputs are autocomplete suggestions and selected text.
- gates_or_invariants: Suggestions must match current prefix/context and avoid invalid actions.
- dependencies_and_callers: Tests input/autocomplete controller and prompt action registry.
- edge_cases_or_failure_modes: Empty prefix, ambiguous prefix, disabled commands, cursor position.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1037 `file` `packages/coding-agent/test/sdk-mcp-discovery.test.ts`
- cursor: `[_]`
- core_role: Tests MCP discovery for SDK/config sources.
- algorithmic_behavior: Validates discovery/normalization of MCP server configs from supported SDK/source files, including path/env handling and source metadata.
- inputs_outputs_state: Inputs are temporary MCP config files/settings; outputs are normalized MCP server definitions and warnings.
- gates_or_invariants: Discovery must preserve source identity, reject malformed configs, and avoid leaking disabled/invalid entries.
- dependencies_and_callers: Tests `packages/coding-agent/src/discovery/mcp-json.ts` and helpers.
- edge_cases_or_failure_modes: Missing config, env-expanded paths, duplicate servers, invalid JSON/schema, project vs user precedence.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1067 `file` `packages/coding-agent/test/snapcompact-inline.test.ts`
- cursor: `[_]`
- core_role: Tests inline snapcompact transformer and swap planner.
- algorithmic_behavior: Validates no-op for text-only models, rasterizes large historical tool results, reports savings, avoids mutation, skips existing images/errors/below-floor items, moves system prompt frames, respects provider image budgets/caps, caches renders, never swaps most recent result, and estimates savings (`snapcompact-inline.test.ts:94-530`).
- inputs_outputs_state: Inputs are contexts with messages/tool results/system prompt, model/provider capabilities, image budget; outputs are transformed context with image frames/stubs and savings estimates.
- gates_or_invariants: Do not mutate persisted history, obey 3k-token floor and OpenRouter 8-image cap, keep recent/current tool result text, require carrier user message for system frames.
- dependencies_and_callers: Tests snapcompact inline context transformer documented by `docs/compaction.md`.
- edge_cases_or_failure_modes: Existing images exhaust cap, small prompt, no user message, cheaper/not cheaper frames, cached identical input.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1097 `file` `packages/coding-agent/test/test-theme-colors.ts`
- cursor: `[_]`
- core_role: Test helper/fixture for theme color assertions.
- algorithmic_behavior: Provides color/theme utility values used by TUI tests to compare rendered ANSI/style output.
- inputs_outputs_state: Inputs are theme color names/fixtures; outputs are deterministic color values. No mutable state unless helper-local.
- gates_or_invariants: Test color values must remain stable enough for snapshot/string assertions.
- dependencies_and_callers: Used by coding-agent TUI/component tests.
- edge_cases_or_failure_modes: Theme palette changes causing tests to fail even when behavior is unchanged.
- validation_or_tests: It supports validation rather than being a standalone test.
- skip_candidate: `yes: test helper, not a runtime algorithm, but participates in render validation.`

### OH_MY_HUMANIZE_MAIN-HZ-1127 `file` `packages/coding-agent/test/write-shebang-chmod.test.ts`
- cursor: `[_]`
- core_role: Tests write/edit behavior for shebang executable chmod.
- algorithmic_behavior: Verifies files written with shebangs receive expected executable mode handling.
- inputs_outputs_state: Inputs are file content/write calls; outputs are file mode bits and written content.
- gates_or_invariants: Shebang detection must not miss executable scripts or chmod non-scripts unexpectedly.
- dependencies_and_callers: Tests coding-agent write tool/file operation path.
- edge_cases_or_failure_modes: Existing file modes, non-shebang first line, platform chmod semantics.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1157 `file` `packages/hashline/src/snapshots.ts`
- cursor: `[_]`
- core_role: Snapshot storage abstraction for file content hashes and seen lines.
- algorithmic_behavior: Defines `Snapshot`, abstract `SnapshotStore`, and `InMemorySnapshotStore`; computes hash on save, merges seen lines (`snapshots.ts:90`), stores per-path versions with LRU/cache caps (`:84-87`, `:118`).
- inputs_outputs_state: Inputs are path/content/seen lines; outputs are snapshots retrievable by path/hash/version. State is in-memory path/version cache with byte/path limits.
- gates_or_invariants: Seen lines merge monotonically, max paths/versions/bytes cap memory, hash identifies content, snapshots are path-scoped.
- dependencies_and_callers: Depends on `computeFileHash` and `lru-cache`; used by edit/seen-line guard and hashline consumers.
- edge_cases_or_failure_modes: Duplicate content versions, cache eviction, large content exceeding byte budget, seen-line merge consistency.
- validation_or_tests: Covered by edit seen-line guard tests and hashline package tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1187 `file` `packages/mnemopi/test/beam-store.test.ts`
- cursor: `[_]`
- core_role: Tests Beam memory store free functions.
- algorithmic_behavior: Verifies remember/dedup/event/FTS sync, batch ordering by scope/importance/recency, update/invalidate/get episodic fallback/forget cascade/stats, scratchpad scoping, and import/export idempotence (`beam-store.test.ts:68-179`).
- inputs_outputs_state: Inputs are memory items, annotations, scopes, sessions, import payloads; outputs are stored/updated/forgotten records, recall/context results, stats, scratchpad, exported state.
- gates_or_invariants: Exact-content dedup, FTS consistency, authorized annotation cascade, session-scoped scratchpad, idempotent import.
- dependencies_and_callers: Tests `packages/mnemopi` Beam store and database schema.
- edge_cases_or_failure_modes: Duplicate batch content, invalidated memory, episodic fallback, repeated import.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1217 `file` `packages/mnemopi/test/memory-facade.test.ts`
- cursor: `[_]`
- core_role: Tests Mnemopi public facade and singleton/bank behavior.
- algorithmic_behavior: Verifies instance methods remember/recall/get/update/forget/stats/context, open Database handle writes, duplicate-content batch IDs, Python-compatible aliases, singleton reset, bank switching and per-call bank selection (`memory-facade.test.ts:57-188`).
- inputs_outputs_state: Inputs are facade calls, DB handle/path, bank selections; outputs are memory records, stats/context, singleton state.
- gates_or_invariants: Facade aliases must remain compatible, duplicate content gets distinct IDs in batch, singleton reset isolates tests, bank selection routes storage.
- dependencies_and_callers: Tests `packages/mnemopi` public API.
- edge_cases_or_failure_modes: Already-open DB lifecycle, duplicate batch writes, legacy alias drift, bank cross-contamination.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1247 `file` `packages/natives/native/embedded-addon.js`
- cursor: `[_]`
- core_role: Generated manifest placeholder for embedded native addon archive/files.
- algorithmic_behavior: Declares JSDoc typedefs for embedded addon variants/files/archive and exports `embeddedAddon = null` at `embedded-addon.js:5-31`.
- inputs_outputs_state: Input is generated output from `scripts/embed-native.ts`; output is JS manifest consumed by native loader. No runtime state beyond exported constant.
- gates_or_invariants: Autogenerated, null means no embedded addon present in this tree/build.
- dependencies_and_callers: Native package loader and embed script.
- edge_cases_or_failure_modes: Stale generated manifest, null handling by loader, variant mismatch.
- validation_or_tests: Validated by native package smoke/build tests.
- skip_candidate: `yes: generated manifest placeholder, not an algorithm.`

### OH_MY_HUMANIZE_MAIN-HZ-1277 `file` `packages/snapcompact/research/exp05_anchors.py`
- cursor: `[_]`
- core_role: Research experiment script for snapcompact anchor/ruler evaluation.
- algorithmic_behavior: Computes ruler capacity (`exp05_anchors.py:60`), renders sentence rulers (`:66`), parses model row answers (`:121`), computes gold row (`:140`), runs chunk/model condition cells (`:163`), aggregates accuracy/cost metrics (`:224`), and drives CLI main (`:258`).
- inputs_outputs_state: Inputs are SQuAD/context chunks, font config, cached images/prompts, model list/API keys; outputs are PNG renders, JSON/CSV records, aggregate metrics. State is file caches under research results.
- gates_or_invariants: Cache keys must be stable, row parser tolerates approximate syntax, baseline conditions are fixed, image generation idempotent via `_ensure_png`.
- dependencies_and_callers: Depends on local research modules `squad`, `bdf`, `final`, `providers`, `run`, PIL, thread pool.
- edge_cases_or_failure_modes: Missing API keys/cache/font files, malformed model answers, image render failures, concurrent cache writes.
- validation_or_tests: Research script; no production tests.
- skip_candidate: `yes: experimental research artifact, not runtime algorithm, though it informs snapcompact design.`

### OH_MY_HUMANIZE_MAIN-HZ-1307 `file` `packages/snapcompact/research/snapcompact_blog_viz.py`
- cursor: `[_]`
- core_role: Research visualization generator for snapcompact blog assets.
- algorithmic_behavior: Loads fonts, draws rounded panels/labels/charts (`snapcompact_blog_viz.py:33-90`), crops answer regions (`:90`), fits images into canvas (`:110`), and composes final visualization in `main` (`:119`).
- inputs_outputs_state: Inputs are result JSON/images and CLI args; outputs are blog visualization images. State is output files.
- gates_or_invariants: Preserve aspect ratio in `paste_fit`, chart scaling from values, crop bounds derived from token grid geometry.
- dependencies_and_callers: Depends on PIL and research result files.
- edge_cases_or_failure_modes: Missing fonts/results, out-of-range crop coordinates, empty chart data.
- validation_or_tests: Manual/research visual inspection.
- skip_candidate: `yes: visualization script, not production core behavior.`

### OH_MY_HUMANIZE_MAIN-HZ-1337 `file` `packages/snapcompact/research/snapcompact_viz_token_grid.py`
- cursor: `[_]`
- core_role: Research visualization for token-grid heatmaps.
- algorithmic_behavior: Normalizes arrays (`snapcompact_viz_token_grid.py:78`), computes token-side layout (`:85`), folds token heat (`:97`), creates overlays (`:103`), draws grids/hotspots/text panels (`:117-228`), and renders final image (`:236`).
- inputs_outputs_state: Inputs are heatmap arrays/summary JSON/source images; outputs are `token-grid.png` and derived visual panels.
- gates_or_invariants: Quantile normalization avoids outlier domination, `paste_fit` preserves aspect ratio, hotspot count bounded, token grid dimensions derive from token count.
- dependencies_and_callers: Depends on NumPy, PIL, research result directories.
- edge_cases_or_failure_modes: Missing source data, zero/NaN arrays, mismatched token dimensions, font fallback.
- validation_or_tests: Manual/research visual inspection.
- skip_candidate: `yes: research visualization artifact, not runtime code.`

### OH_MY_HUMANIZE_MAIN-HZ-1367 `file` `packages/tui/bench/text-layout.ts`
- cursor: `[_]`
- core_role: Benchmark for TUI text layout performance.
- algorithmic_behavior: Runs text layout/render operations repeatedly to measure performance characteristics.
- inputs_outputs_state: Inputs are benchmark strings/layout widths; outputs are timing/benchmark results. No persistent runtime state.
- gates_or_invariants: Benchmark should exercise representative layout paths without changing library behavior.
- dependencies_and_callers: Uses `packages/tui` text layout/markdown primitives.
- edge_cases_or_failure_modes: Benchmark drift due to data not matching real workloads; performance regressions not caught if benchmark skipped.
- validation_or_tests: Bench-only; not a correctness test.
- skip_candidate: `yes: performance benchmark, not core runtime algorithm.`

### OH_MY_HUMANIZE_MAIN-HZ-1397 `file` `packages/tui/test/editor.test.ts`
- cursor: `[_]`
- core_role: Extensive tests for TUI editor input/model behavior.
- algorithmic_behavior: Validates text editing, cursor movement, selection, deletion, history, wrapping, multiline behavior, key handling, paste/input normalization, and rendering.
- inputs_outputs_state: Inputs are key events/text/paste sequences and editor dimensions; outputs are editor buffer, cursor/selection state, rendered lines.
- gates_or_invariants: Cursor must track grapheme/display width correctly, edits preserve buffer invariants, render output fits constraints, history transitions stable.
- dependencies_and_callers: Tests `packages/tui` editor component used by coding-agent prompt input.
- edge_cases_or_failure_modes: Wide characters, ANSI/control sequences, multiline wrapping, deletion at boundaries, history navigation, empty buffer.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1427 `file` `packages/tui/test/markdown.test.ts`
- cursor: `[_]`
- core_role: Tests TUI markdown parsing/rendering.
- algorithmic_behavior: Exercises Markdown-to-terminal layout for paragraphs, lists, code, links, wrapping, escaping, styling, and nested structures.
- inputs_outputs_state: Inputs are markdown strings and render widths/theme; outputs are terminal line components/strings.
- gates_or_invariants: Rendered markdown must be width-safe, escape unsafe HTML/control content, preserve semantic line breaks where required.
- dependencies_and_callers: Tests `packages/tui` Markdown component used across coding-agent transcript rendering.
- edge_cases_or_failure_modes: Tight lists, code fences, raw HTML, links, long words, ANSI/style width.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1457 `file` `packages/tui/test/terminal-capabilities.test.ts`
- cursor: `[_]`
- core_role: Tests terminal capability detection.
- algorithmic_behavior: Validates detection/feature flags for colors, hyperlinks, image protocols, terminal brands/env signals, and fallback behavior.
- inputs_outputs_state: Inputs are env vars/TTY flags/terminal identifiers; outputs are capability booleans/protocol decisions.
- gates_or_invariants: Must not enable unsupported features by default; overrides/env signals must behave predictably.
- dependencies_and_callers: Tests TUI terminal capability helpers used by renderers and hyperlink/image output.
- edge_cases_or_failure_modes: `NO_COLOR`, CI/non-TTY, terminal-specific protocol quirks, unknown terminals.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1487 `file` `packages/utils/src/fetch-retry.ts`
- cursor: `[_]`
- core_role: Shared fetch retry/backoff and retry-hint extraction utility.
- algorithmic_behavior: Extracts retry hints from headers/body regexes (`fetch-retry.ts:31`), converts units (`:81`), retries with timeout/backoff/defaults (`:154`), merges init/headers (`:196`), wraps network errors (`:209`), extracts HTTP status from nested errors/messages (`:239-282`), and classifies retryable statuses/errors (`:296-320`).
- inputs_outputs_state: Inputs are URL/request init, fetch implementation, retry options, response/error bodies; outputs are final `Response` or thrown wrapped error. State is per-attempt counter/delay/abort timeout.
- gates_or_invariants: Default max attempts/delay at `:142-143`, must honor caller signal/timeout, only retry retryable statuses/errors, use server retry hints when present.
- dependencies_and_callers: Used by provider/network clients across repo; depends on `node:timers/promises` scheduler.
- edge_cases_or_failure_modes: `Retry-After` variants, quota reset text, nested error causes, unexpected socket close, validation errors that should not retry.
- validation_or_tests: Covered by utility/provider tests; assigned `packages/utils/test/color.test.ts` is unrelated.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1517 `file` `packages/utils/test/color.test.ts`
- cursor: `[_]`
- core_role: Tests shared color utility behavior.
- algorithmic_behavior: Validates color formatting/parsing helpers in `packages/utils`.
- inputs_outputs_state: Inputs are color strings/values; outputs are normalized colors or styled strings.
- gates_or_invariants: Color helpers must preserve expected formats and reject/handle invalid inputs.
- dependencies_and_callers: Tests utility color module used by UI packages.
- edge_cases_or_failure_modes: Invalid color names, ANSI reset, theme conversions.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1547 `file` `python/robomp/src/__init__.py`
- cursor: `[_]`
- core_role: Python package identity marker for roboomp.
- algorithmic_behavior: Declares package docstring and `__version__ = "0.1.0"` at `__init__.py:1-3`.
- inputs_outputs_state: No algorithmic input; output is importable package metadata.
- gates_or_invariants: Version string is the only exported state here.
- dependencies_and_callers: Python packaging/import system and tests importing `robomp`.
- edge_cases_or_failure_modes: Version drift relative to package metadata.
- validation_or_tests: Import smoke via Python test suite.
- skip_candidate: `yes: package metadata, not core algorithm.`

### OH_MY_HUMANIZE_MAIN-HZ-1577 `file` `python/robomp/tests/test_db.py`
- cursor: `[_]`
- core_role: Database contract tests for roboomp event, issue, review, submission, classification, and pending-closure state.
- algorithmic_behavior: Tests dedupe by delivery, singleton claims under contention, same-issue blocking/fairness, restricted requeue, noise filtering, stuck reset, issue upsert, tool logs, PR review staging, processed keys batching, migrations, event model persistence, running event summaries, submission rate limiting, and pending closure claim/finalize/requeue (`test_db.py:10-645`).
- inputs_outputs_state: Inputs are SQLite `Database` operations and concurrent connections/threads; outputs are event rows, claims, issue/classification records, staged comments, rate-limit decisions, closure rows.
- gates_or_invariants: Atomic claims/rate limits, case-insensitive submitter counting, claimed closure terminal-state enforcement, migration compatibility.
- dependencies_and_callers: Tests `robomp.db`.
- edge_cases_or_failure_modes: Contention races, blocked issue starvation, large processed-key batches, existing DB migration, non-terminal closure finalization.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1607 `directory` `packages/coding-agent/src/cli/gallery-fixtures`
- cursor: `[_]`
- core_role: Static fixture catalog for CLI/TUI gallery rendering of tool components.
- algorithmic_behavior: `index.ts` aggregates fixture groups; `types.ts` defines `GalleryFixture` and states; groups (`agentic.ts`, `codeintel.ts`, `edit.ts`, `fs.ts`, `interaction.ts`, `memory.ts`, `misc.ts`, `search.ts`, `shell.ts`, `web.ts`) create canned call/result/update states. `fs.ts` includes grouped read rendering helpers (`fs.ts:50-98`).
- inputs_outputs_state: Inputs are fixture state/width/expanded flags; outputs are rendered component examples and canned results. State is fixture state enum.
- gates_or_invariants: Fixtures must match component schemas, include streaming/progress/success/error where relevant, and keep deterministic timestamps/usage (`agentic.ts:8-20`).
- dependencies_and_callers: Used by CLI gallery/demo commands and TUI render components.
- edge_cases_or_failure_modes: Fixture schema drift after renderer changes, nondeterministic dates/usage, stale path names.
- validation_or_tests: Gallery visual/manual tests; component tests indirectly catch schema drift.
- skip_candidate: `yes: demo/test fixture data, not production algorithm.`

### OH_MY_HUMANIZE_MAIN-HZ-1637 `directory` `packages/coding-agent/src/modes/utils`
- cursor: `[_]`
- core_role: Shared mode/UI utility functions for keybindings, context usage, copy targets, hotkey/tool markdown, and transcript reconstruction.
- algorithmic_behavior: `keybinding-matchers.ts` matches canonical keybindings (`:1-1874 bytes`, exports around `:1`); `context-usage.ts` computes/render context token breakdown; `copy-targets.ts` resolves copyable transcript/code/output targets; `hotkeys-markdown.ts` and `tools-markdown.ts` build help panels; `ui-helpers.ts` rebuilds transcript/tool render data and preserves streaming preview fields.
- inputs_outputs_state: Inputs are settings, key events, session/tool entries, token usage, copy action targets; outputs are markdown/help strings, match booleans, render contexts, copy payloads.
- gates_or_invariants: Key matching must normalize aliases/modifiers, render helpers must sanitize/truncate, transcript rebuild must preserve preview-only fields for streaming tools.
- dependencies_and_callers: Used by interactive modes, command controller, TUI help/copy panels, tool execution rendering.
- edge_cases_or_failure_modes: Partial JSON tool args, modifier order, unknown keybinding, stale token usage, copied content containing tabs/long lines.
- validation_or_tests: Covered by keybinding migration, TUI, and tool preview tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1667 `file` `crates/pi-shell/src/minimizer/config.rs`
- cursor: `[_]`
- core_role: Configuration loader for shell minimizer.
- algorithmic_behavior: Defines outline level/options/config (`config.rs:23-95`), default config (`:95`), config methods/loaders (`:110`), settings-file parsing (`:218-231`), legacy filter/env resolution (`:277`), tilde expansion (`:286`), and home lookup (`:300`).
- inputs_outputs_state: Inputs are settings file/env/user paths and optional pipeline dirs; outputs are `MinimizerConfig` with caps, modes, filters, registry. State includes loaded pipeline registry.
- gates_or_invariants: Default max capture bytes `4 MiB` at `:19`, schema compatibility via `SUPPORTED_SCHEMA_VERSION`, legacy env flags normalized.
- dependencies_and_callers: Used by minimizer `engine.rs`; depends on `pipeline` module and serde/TOML parsing.
- edge_cases_or_failure_modes: Missing home, bad TOML/schema, legacy env override ambiguity, tilde path without home.
- validation_or_tests: Exercised by minimizer tests and builtin pipeline verification.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1697 `file` `packages/ai/src/auth-gateway/server.ts`
- cursor: `[_]`
- core_role: HTTP auth gateway for AI provider streaming, pi-native requests, usage, credentials, and model listing.
- algorithmic_behavior: Maps format routes (`server.ts:62`), derives session IDs (`:97`), builds stream options (`:120`), classifies gateway errors (`:210`), refreshes API keys after auth errors (`:305`), builds resolver (`:360`), mirrors request aborts (`:405`), handles format endpoints (`:417`), pi-native (`:607`), usage/credentials/models (`:761-786`), and starts server (`:797`).
- inputs_outputs_state: Inputs are HTTP requests, auth storage, model resolver, context/body, peer/auth headers, abort signals; outputs are streamed provider responses, JSON errors, usage/credential/model responses. State is server handle and auth refresh/cache behavior.
- gates_or_invariants: CORS/auth/peer checks, status bucketing, abort propagation, retry hint/error mapping, per-format module routing, API key refresh only after auth errors.
- dependencies_and_callers: Used by coding-agent auth broker/gateway; depends on provider server modules and auth storage.
- edge_cases_or_failure_modes: Client closes, malformed request, unknown model/format, expired credentials, embedded HTTP status in error text, usage limit errors.
- validation_or_tests: Assigned `auth-gateway-openai-responses-caching.test.ts` and auth gateway tests cover caching/error/route behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1727 `file` `packages/ai/src/providers/anthropic.ts`
- cursor: `[_]`
- core_role: Anthropic Messages provider implementation, including headers, tool/schema conversion, images, streaming, retries, usage, and compatibility modes.
- algorithmic_behavior: Normalizes base URL/builds beta headers (`anthropic.ts:98-190`), manages provider session/fast-mode fallback (`:300-375`), Claude Code headers/CCH/user IDs/device IDs (`:430-691`), tool name encoding and web search selection (`:706-765`), many-image resizing (`:770-922`), content conversion (`:939`), client options/TLS/custom headers (`:1010-1270`), SSE iteration and retryable errors (`:1289-1487`), usage accounting (`:1539+`), strict schema normalization/tools (`:3538-3786`), and stop reason mapping (`:3812`).
- inputs_outputs_state: Inputs are `Context`, model/options, API key/OAuth metadata, tools, images, headers, stream events; outputs are Anthropic request params, assistant message event stream, usage, tool calls/results. State includes provider session state, fast-mode fallback flags, resize cache, TLS cache.
- gates_or_invariants: Enforced headers cannot be overridden, stop sequence max 4, image resize concurrency 4, strict-tool fallback on grammar errors, retry provider envelope anomalies safely, avoid empty Anthropic error tool result.
- dependencies_and_callers: Used by `streamSimple`/AI registry; depends on Anthropic SDK, catalog identity/effort, vision/image utilities, fetch retry.
- edge_cases_or_failure_modes: Unsupported fast mode, strict grammar too large, transient SSE preamble/envelope errors, many images, OAuth vs API-key tool-name escaping, file-path TLS cert values, thinking envelope unwrap.
- validation_or_tests: Assigned Anthropic tests, image-limit tests, usage tests, raw SSE tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1757 `file` `packages/ai/src/providers/openai-shared.ts`
- cursor: `[_]`
- core_role: Shared OpenAI-compatible request/response algorithms for Chat Completions and Responses APIs.
- algorithmic_behavior: Resolves request setup/service tier/cost (`openai-shared.ts:139-309`), cache/session IDs (`:329-349`), Azure maps and strict-tool state (`:356-402`), routing/wire IDs/output tokens/extra body (`:410-575`), reasoning compat policy (`:598-891`), strict-tool retry (`:927-943`), stable IDs/progress/text signatures/tool-call IDs (`:960-1049`), orphan tool repair (`:1101-1166`), Responses input/content conversion (`:1215-1539`), streaming accumulation/finalization (`:1541-2207`), sampling/reasoning params/usage/delta building (`:2228-2437`).
- inputs_outputs_state: Inputs are model/provider compat metadata, context messages, tools, images, sampling/reasoning options, stream events; outputs are request params, transformed Responses/Chat messages, assistant stream events, usage accounting. State includes strict-tool disabled scopes.
- gates_or_invariants: Service tier multipliers, model/provider-specific wire ID transforms, no orphan tool outputs/calls, progress event filtering, image detail clamp, strict-tool retry only for strict grammar failures.
- dependencies_and_callers: Used by OpenAI, OpenRouter, Azure, Fireworks/Firepass/ZAI compatible providers.
- edge_cases_or_failure_modes: Forced tool choice disabling reasoning, malformed streaming JSON deltas, duplicate/missing call IDs, provider image caps, stale cache/session key, unsupported output token params.
- validation_or_tests: Assigned OpenAI Responses caching, tool-result-images, cursor, usage, image-limits tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1787 `file` `packages/ai/src/registry/kagi.ts`
- cursor: `[_]`
- core_role: Provider registry definition for Kagi.
- algorithmic_behavior: Defines Kagi provider metadata, auth/API key validation hooks, base URL/model defaults, and login behavior in a compact provider descriptor (`kagi.ts`).
- inputs_outputs_state: Inputs are provider options/API key; outputs are `ProviderDefinition`. No persistent state.
- gates_or_invariants: Provider ID/base URL/auth fields must match registry expectations.
- dependencies_and_callers: Used by AI provider registry and settings/auth flows.
- edge_cases_or_failure_modes: Invalid API key, registry metadata drift.
- validation_or_tests: Covered by provider registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1817 `file` `packages/ai/src/registry/venice.ts`
- cursor: `[_]`
- core_role: Provider registry/login definition for Venice OpenAI-compatible API.
- algorithmic_behavior: Defines auth/API URLs and validation model (`venice.ts:5-7`), `loginVenice` browser/API key flow (`:15`), and `veniceProvider` descriptor (`:51`).
- inputs_outputs_state: Inputs are OAuth/login callbacks/API key; outputs are validated API key and provider metadata.
- gates_or_invariants: API key validation uses OpenAI-compatible validation against `qwen3-4b`; login opens Venice settings URL.
- dependencies_and_callers: Registry/auth UI and OpenAI-compatible provider factory.
- edge_cases_or_failure_modes: User cancels login, invalid key, validation model unavailable.
- validation_or_tests: Provider registry/auth tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1847 `file` `packages/ai/src/utils/harmony-leak.ts`
- cursor: `[_]`
- core_role: Utility for detecting/sanitizing leaked OpenAI Harmony/control-channel content.
- algorithmic_behavior: Scans assistant text/parts for Harmony markers, control-channel sections, and leak patterns; returns cleaned text or detection metadata.
- inputs_outputs_state: Inputs are model output strings/content parts; outputs are sanitized strings and leak classification. No persistent state.
- gates_or_invariants: Must avoid false removal of normal user text while suppressing protocol leakage.
- dependencies_and_callers: Used by provider response processing/safety wrappers.
- edge_cases_or_failure_modes: Partial markers, nested/fenced code containing marker-like text, multilingual/escaped tokens, streaming boundary leaks.
- validation_or_tests: Covered by provider/harmony leak tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1877 `file` `packages/catalog/src/identity/classify.ts`
- cursor: `[_]`
- core_role: Model ID classifier and SemVer comparator.
- algorithmic_behavior: Strips provider prefixes via `bareModelId` (`classify.ts:56`), parses known Gemini/Anthropic/OpenAI/GLM IDs (`:65-140`), classifies fable/mythos (`:157`), precomputes SemVer table (`:166`), parses/compares SemVer (`:176-188`).
- inputs_outputs_state: Inputs are model ID/version strings; outputs are parsed discriminated model objects or unknowns and comparison numbers. State includes bare ID cache.
- gates_or_invariants: Parser wrappers must catch parse failures; ID regex/suffix rules must be provider-specific; SemVer compare handles nulls/strings.
- dependencies_and_callers: Used by catalog generation, provider compatibility, thinking policy.
- edge_cases_or_failure_modes: Preview suffixes, provider-prefixed IDs, unknown variants, malformed SemVer, cached bare IDs.
- validation_or_tests: Assigned catalog variant/Gemini thinking tests exercise classifier behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1907 `file` `packages/coding-agent/src/autoresearch/dashboard.ts`
- cursor: `[_]`
- core_role: TUI dashboard renderer/controller for autoresearch experiment runs.
- algorithmic_behavior: Creates dashboard controller (`dashboard.ts:7`), renders running-only/collapsed/expanded headers (`:125-154`), renders result table lines (`:223-340`), rows/secondary cells/summaries (`:340-391`), overlay footer/status (`:391-415`), and best result selection (`:426`).
- inputs_outputs_state: Inputs are `AutoresearchRuntime`, experiment state/results, width/theme/key events; outputs are rendered lines and controller state (expanded/collapsed/scroll). State is dashboard UI state.
- gates_or_invariants: Width truncation via TUI helpers, compare metrics with `isBetter`, only show dashboard when runtime/state permit, stable row formatting.
- dependencies_and_callers: Autoresearch mode/runtime and pi-tui components.
- edge_cases_or_failure_modes: Narrow terminal, no baseline/result, secondary metrics missing, scroll bounds, long labels/tabs.
- validation_or_tests: Autoresearch UI tests if present; not directly assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1937 `file` `packages/coding-agent/src/cli/classify-install-target.ts`
- cursor: `[_]`
- core_role: Classifier for plugin/marketplace install target specs.
- algorithmic_behavior: Detects local path specs (`classify-install-target.ts:39`), recognizes npm dist tags/version-ish specs (`:16-30`), and returns classified target as marketplace/local/npm/github-like spec (`:50-55`).
- inputs_outputs_state: Inputs are user install spec and known marketplaces set; outputs are discriminated install target. No persistent state.
- gates_or_invariants: Local paths must win over package-looking strings when syntactically path-like; known marketplace names recognized.
- dependencies_and_callers: Used by CLI install/plugin marketplace commands.
- edge_cases_or_failure_modes: Scoped packages, version ranges, `latest`/dist tags, relative/absolute paths, marketplace/package name collisions.
- validation_or_tests: Covered by plugin install tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1967 `file` `packages/coding-agent/src/cli/workflow-cli.ts`
- cursor: `[_]`
- core_role: Headless CLI command runner for workflows.
- algorithmic_behavior: Resolves action args (`workflow-cli.ts:73`), dispatches list/freeze/start/install/uninstall (`:100-132`), loads artifacts (`:362`), computes default start nodes (`:378`), creates runtime binding snapshot (`:385`), runs headless eval/shell/agent tasks (`:417-485`), builds agent task CLI args (`:485`), streams output (`:497`), formats values, stores in-memory run entries (`:524`).
- inputs_outputs_state: Inputs are CLI flags, workflow package path, runtime callbacks, flow specs, scripts/tasks; outputs are console JSON/text, frozen artifacts, installed/uninstalled packages, workflow run entries. State includes in-memory workflow store.
- gates_or_invariants: Action must be one of `list|freeze|start|install|uninstall`, required args enforced, default max runtime applied, headless agent task runs through current CLI invocation.
- dependencies_and_callers: CLI command registry and workflow package/runner/freeze/lifecycle modules.
- edge_cases_or_failure_modes: Missing package/action args, unavailable runtime binding, script subprocess failure, stream errors, model override propagation.
- validation_or_tests: Assigned workflow benchmark scenarios and workflow tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1997 `file` `packages/coding-agent/src/commands/stats.ts`
- cursor: `[_]`
- core_role: CLI command wrapper for stats dashboard.
- algorithmic_behavior: Defines Oclif-style `Stats` command, initializes theme, parses flags, and delegates to `runStatsCommand` with typed args (`stats.ts:4-29`).
- inputs_outputs_state: Inputs are CLI flags/env; outputs are launched stats command/dashboard. No durable state here.
- gates_or_invariants: Flags must map to `StatsCommandArgs`; theme initialized before rendering.
- dependencies_and_callers: CLI command registry, `../cli/stats-cli`, theme system.
- edge_cases_or_failure_modes: Invalid flags, stats command failure.
- validation_or_tests: CLI stats tests/smoke.
- skip_candidate: `yes: thin command adapter, algorithm lives in stats CLI/dashboard.`

### OH_MY_HUMANIZE_MAIN-HZ-2027 `file` `packages/coding-agent/src/config/settings-schema.ts`
- cursor: `[_]`
- core_role: Authoritative settings schema, defaults, UI metadata, and typed setting helpers.
- algorithmic_behavior: Defines tabs/group metadata (`settings-schema.ts:59-107`), status-line/settings UI type system (`:141-248`), default bash interceptor rules (`:278`), massive `SETTINGS_SCHEMA` map (`:320`), derived `SettingPath/SettingValue` types (`:4474-4499`), and helpers `getDefault`, `hasUi`, `getUi`, `getPathsForTab`, `getType`, `getEnumValues` (`:4499-4528`) plus grouped settings interfaces (`:4553-4724`).
- inputs_outputs_state: Inputs are setting paths; outputs are defaults, UI metadata, enum values, typed group shapes. Static schema is state.
- gates_or_invariants: Every setting has type/default semantics; UI metadata tab/group membership must match settings; default values drive runtime behavior.
- dependencies_and_callers: Settings loader, setup wizard, command controller, model/provider/tool configs, TUI settings UI.
- edge_cases_or_failure_modes: Schema/default mismatch, enum drift, wrong tab grouping, mutable default arrays/records, type inference breakage.
- validation_or_tests: Keybinding/settings tests and package `bun check` validate types; no single direct test covers full schema.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2057 `file` `packages/coding-agent/src/discovery/helpers.ts`
- cursor: `[_]`
- core_role: Core helper library for discovery providers, skills, extensions, and plugin roots.
- algorithmic_behavior: Defines source path map (`helpers.ts:27`), user/project path resolution (`:89-103`), boolean/CSV/array parsing (`:133-157`), markdown rule building (`:172`), agent frontmatter parsing (`:241`), skill directory scanning (`:325`), env expansion (`:390-402`), file loading from dirs (`:423`), linked extension module discovery/manifest reads (`:511-573`), extension item building (`:679`), Claude plugin registry parsing (`:746`), active registry resolution (`:772-819`), root listing/cache/preload/inject (`:829-1063`).
- inputs_outputs_state: Inputs are cwd/home, source IDs, file contents, dirs, manifests, plugin registry JSON, env; outputs are normalized discovery records, warnings, root lists. State includes plugin root caches.
- gates_or_invariants: Stable skill ordering, extension manifest path validation, env expansion recursive but type-preserving, cache clear functions cover roots/extra paths.
- dependencies_and_callers: All discovery provider modules, extension loader, skill/plugin systems.
- edge_cases_or_failure_modes: Dangling symlinks, invalid JSON/manifest, plugin root cache staleness, project registry path fallback, extension name extraction from nested/symlink paths.
- validation_or_tests: Assigned `extensions-discovery.test.ts`, `sdk-mcp-discovery.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2087 `file` `packages/coding-agent/src/exa/mcp-client.ts`
- cursor: `[_]`
- core_role: Exa/Websets MCP client wrapper and formatter.
- algorithmic_behavior: Finds API key (`mcp-client.ts:15`), parses JSON content (`:24`), normalizes MCP payloads (`:40`), fetches Exa/Websets tools (`:75-91`), calls tools (`:104-133`), formats search/generic responses (`:153-243`), validates search response (`:258`), caches schemas (`:267`), wraps MCP tool as custom tool (`:299`), and creates tools from server (`:360`).
- inputs_outputs_state: Inputs are API key, MCP tool names/calls, JSON-RPC responses; outputs are `CustomTool` instances and formatted markdown/text results. State includes schema cache.
- gates_or_invariants: Missing API key handled, payload normalized from text JSON when possible, schema fetched/cached by tool, custom tool returns `CustomToolResult`.
- dependencies_and_callers: Exa/web tool registration, MCP JSON-RPC client, custom tools.
- edge_cases_or_failure_modes: Tool schema missing, invalid JSON content, MCP call errors, unknown response shape, indentation/formatting large nested values.
- validation_or_tests: Web/MCP tool tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2117 `file` `packages/coding-agent/src/internal-urls/artifact-protocol.ts`
- cursor: `[_]`
- core_role: Internal URL protocol for resolving artifact references.
- algorithmic_behavior: Parses/handles `artifact://` URLs, maps IDs to session artifacts, and returns display/read results for internal URL expansion.
- inputs_outputs_state: Inputs are artifact URL/path and session artifact registry; outputs are resolved artifact content/metadata or error. State is external artifact store.
- gates_or_invariants: Only valid artifact IDs/routes resolve; missing artifacts error cleanly; paths remain internal.
- dependencies_and_callers: Used by bash raw-output artifact notices and internal URL router.
- edge_cases_or_failure_modes: Malformed URL, missing artifact, stale artifact ID, binary/large content.
- validation_or_tests: Internal URL tests and bash rendering tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2147 `file` `packages/coding-agent/src/markit/index.ts`
- cursor: `[_]`
- core_role: Barrel export for markit registry/types.
- algorithmic_behavior: Re-exports `./registry` and `./types` at `markit/index.ts:1-2`.
- inputs_outputs_state: No algorithmic inputs; output is module surface.
- gates_or_invariants: Barrel must not create export ambiguity.
- dependencies_and_callers: Imports from `packages/coding-agent/src/markit`.
- edge_cases_or_failure_modes: Broken if registry/types exports conflict.
- validation_or_tests: Typecheck/import tests.
- skip_candidate: `yes: barrel only.`

### OH_MY_HUMANIZE_MAIN-HZ-2177 `file` `packages/coding-agent/src/mnemopi/backend.ts`
- cursor: `[_]`
- core_role: Coding-agent memory backend adapter for Mnemopi.
- algorithmic_behavior: Lazy-loads diagnose module (`backend.ts:46`), defines static instructions (`:53`), exports `mnemopiBackend` with lifecycle/memory operations (`:65`), builds stats targets/memory (`:272-312`), dedupes/renders stats and diagnostics (`:319-423`), loads config/provider options (`:427-457`), resolves backend/provider/model options (`:457-550`), exposes test DB dir (`:555`), removes DB files (`:560`).
- inputs_outputs_state: Inputs are session/config, memory operations, banks, provider keys/models; outputs are memory recall/remember/status/diagnostics and DB files. State is Mnemopi session state and bank DB paths.
- gates_or_invariants: Importance normalized/clamped, banks deduped, OpenRouter key resolver respects host matching, db path resolution stable, cleanup removes known db files only.
- dependencies_and_callers: Memory backend resolver, `@oh-my-pi/pi-mnemopi`, tiny/local/online model clients, settings.
- edge_cases_or_failure_modes: Missing diagnose module, provider key unavailable, invalid bank/path, stats DB missing, cleanup errors except ENOENT.
- validation_or_tests: Assigned memory backend resolve and mnemopi facade tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2207 `file` `packages/coding-agent/src/registry/agent-registry.ts`
- cursor: `[_]`
- core_role: Runtime registry for main/subagent references and status events.
- algorithmic_behavior: Defines agent IDs/status/kind/ref types (`agent-registry.ts:15-49`) and `AgentRegistry` class (`:59`) to register/update/unregister agents, emit listener events, and expose snapshots.
- inputs_outputs_state: Inputs are register/update/unregister calls and `AgentSession` refs; outputs are registry events/snapshots. State is in-memory map/listeners.
- gates_or_invariants: Main agent ID is stable (`MAIN_AGENT_ID = "Main"`), status values constrained, listener notifications on changes.
- dependencies_and_callers: Task/subagent system, UI displays, ACP/session lifecycle.
- edge_cases_or_failure_modes: Duplicate IDs, listener throwing, stale session refs, unregister unknown agent.
- validation_or_tests: ACP/task tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2237 `file` `packages/coding-agent/src/session/sql-session-storage.ts`
- cursor: `[_]`
- core_role: SQL-backed session file storage adapter.
- algorithmic_behavior: Detects adapter (`sql-session-storage.ts:102`), builds dialect queries for Postgres/MySQL/SQLite (`:113`), decodes row bytes (`:184`), defines `SqlSessionStorage` (`:202`) and backend (`:233`) for indexed content/slices using a table name validated by regex (`:89-90`).
- inputs_outputs_state: Inputs are SQL client/options/session file reads/writes/list operations; outputs are persisted content/index/slice rows and decoded text. State is SQL table contents.
- gates_or_invariants: Table identifiers must match `IDENT_RE`, adapter detection must match client capabilities, byte decoding handles string/buffer/Uint8Array, missing rows map to ENOENT.
- dependencies_and_callers: Session persistence layer, external SQL clients.
- edge_cases_or_failure_modes: Wrong dialect placeholders, bigint row numbers, invalid table name, binary encoding differences, missing slices.
- validation_or_tests: Session storage tests if present; no assigned direct SQL storage test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2267 `file` `packages/coding-agent/src/task/index.ts`
- cursor: `[_]`
- core_role: Task/subagent tool implementation and orchestration.
- algorithmic_behavior: Renders subagent prompts/usage totals (`task/index.ts:74-91`), exports discovery/agent APIs (`:120-144`), defines read-only tool sets and read-only agent predicate (`:144-169`), validates shape/spawn params (`:239-261`), resolves batch spawn items (`:309-323`), builds specialization/coordination advisories (`:352-398`), memoizes discovery (`:428-431`), and implements `TaskTool` (`:460`) for spawning subprocess/subagent tasks and aggregating results.
- inputs_outputs_state: Inputs are task params, agent definitions, cwd/session/tools, batch options; outputs are task results, usage totals, rendered tool output, spawned subagent processes/jobs. State includes discovery memo and task job state.
- gates_or_invariants: Read-only agents only get read-only tools, plan mode allowlist, batch param validation, generic agent advisory, concurrency limits, output fallback formatting.
- dependencies_and_callers: Agent tool registry, subagent executor, MCP manager, AgentRegistry, prompts, git utils.
- edge_cases_or_failure_modes: Invalid batch shape, unknown agent, subprocess failure, usage aggregation gaps, plan-mode restrictions, task abort.
- validation_or_tests: Assigned `task-guards.test.ts`, ACP tests, workflow benchmarks.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2297 `file` `packages/coding-agent/src/tools/bash.ts`
- cursor: `[_]`
- core_role: Bash tool schema, execution path, async job behavior, output artifacting, and renderer.
- algorithmic_behavior: Defines schema/env validation (`bash.ts:103-132`, `:175`), critical patterns (`:51`), saves raw artifacts (`:92`), parses partial JSON env for streaming previews (`:206-262`), formats notices (`:277-347`), implements `BashTool` (`:357`) using command fixups/interceptors/PTTY/executeBash/async jobs, and creates shell renderer (`:1099-1400`) for pending/progress/result output.
- inputs_outputs_state: Inputs are command, cwd, timeout, env, async flags, partial streamed args, session; outputs are tool result, artifacts, async job handles, rendered lines. State includes managed job handles, tail buffers, internal URL artifacts.
- gates_or_invariants: Env names must match shell identifier regex, timeouts clamped, critical commands require approval/interception, output caps/artifacts enforced, renderer sanitizes/truncates and can render before result exists.
- dependencies_and_callers: Tool registry/session, bash executor, PTY selection, output-meta, internal URL router, TUI components.
- edge_cases_or_failure_modes: Partial JSON args, timeout clamp notice, raw output artifact stripping, interactive result normalization, abort, async background threshold, stale GitHub cache invalidation.
- validation_or_tests: Bash preview/tool tests, ssh render, conflict/lsp tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2327 `file` `packages/coding-agent/src/tools/learn.ts`
- cursor: `[_]`
- core_role: Learn tool implementation for recording reusable knowledge/memory.
- algorithmic_behavior: Defines tool schema/description and stores learned content into configured memory/learning backend with rendered result.
- inputs_outputs_state: Inputs are learned text/tags/context/session; outputs are tool result and memory/learning side effect.
- gates_or_invariants: Content must be non-empty/valid, backend availability respected, result should not expose unsafe raw paths.
- dependencies_and_callers: Tool registry, memory backend, render utilities.
- edge_cases_or_failure_modes: Disabled memory, invalid payload, backend write failure.
- validation_or_tests: Memory/learn tool tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2357 `file` `packages/coding-agent/src/tts/downloader.ts`
- cursor: `[_]`
- core_role: TTS model/runtime cache checker and downloader wrapper.
- algorithmic_behavior: `isTtsModelCached` resolves local model spec, checks model files under tiny model cache and runtime cache (`downloader.ts:21-39`); `downloadTtsModel` delegates to `ttsClient.download` with optional progress callback (`:40-64`).
- inputs_outputs_state: Inputs are model key and progress callback; outputs are boolean cache status or downloaded model readiness. State is filesystem cache.
- gates_or_invariants: Unknown model returns false for cache check; runtime cache must be present in addition to files; progress includes file/loaded/total/status.
- dependencies_and_callers: TTS client, runtime cache, tiny model cache dir, model specs.
- edge_cases_or_failure_modes: Missing runtime, partial model files, invalid model key, fs stat failure.
- validation_or_tests: TTS smoke/download flows.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2387 `file` `packages/coding-agent/src/utils/file-display-mode.ts`
- cursor: `[_]`
- core_role: Utility for deciding file display/preview mode.
- algorithmic_behavior: Classifies file paths/content metadata into display modes for UI/tool rendering.
- inputs_outputs_state: Inputs are file path/extension/mime or content hints; outputs are display mode enum/string. No persistent state.
- gates_or_invariants: Binary/image/text modes must be mutually clear enough for renderers.
- dependencies_and_callers: File read/render tools and UI components.
- edge_cases_or_failure_modes: Unknown extensions, extensionless files, binary text-looking files, image formats.
- validation_or_tests: File rendering tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2417 `file` `packages/coding-agent/src/workflow/freeze.ts`
- cursor: `[_]`
- core_role: Freezes workflow packages into portable deterministic artifacts with static checks.
- algorithmic_behavior: Defines freeze/resource/static-check types (`freeze.ts:12-63`), throws `WorkflowFreezeError` (`:67`), freezes artifact (`:74`) by snapshotting definition/resources, builds static check report (`:114`), hashes resources, applies defaults/policies, and validates change/checkpoint policies.
- inputs_outputs_state: Inputs are `WorkflowArtifact` definitions/resources/change requests; outputs are `FlowFreeze` with resource hashes/snapshots/static report. State is frozen artifact data.
- gates_or_invariants: Static checks must catch invalid workflow structure before install/start, resource hashes stabilize package, policies/defaults portable.
- dependencies_and_callers: Workflow CLI (`freeze` action), package loader, runner/lifecycle.
- edge_cases_or_failure_modes: Missing resource, invalid change request file, unsupported node/policy, hash mismatch, non-portable defaults.
- validation_or_tests: Workflow benchmark/scenario tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2447 `file` `packages/coding-agent/test/collab/read-only.test.ts`
- cursor: `[_]`
- core_role: Tests collaboration read-only behavior.
- algorithmic_behavior: Verifies guest/collab read-only state prevents write/control actions while still allowing observation/rendering.
- inputs_outputs_state: Inputs are collab session frames and attempted actions; outputs are accepted/rejected action results and snapshots.
- gates_or_invariants: Read-only guests must not mutate host/session state.
- dependencies_and_callers: Coding-agent collab protocol/client/server integration.
- edge_cases_or_failure_modes: Write token absence, stale read-only flag, action routing bypass.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2477 `file` `packages/coding-agent/test/core/python-tool-bridge.test.ts`
- cursor: `[_]`
- core_role: Tests Python tool bridge contract.
- algorithmic_behavior: Validates TS/Bun side can invoke/communicate with Python tool bridge and map results/errors.
- inputs_outputs_state: Inputs are bridge requests/tool calls; outputs are bridged responses/errors.
- gates_or_invariants: Protocol payloads must serialize/deserialize correctly and surface failures without hanging.
- dependencies_and_callers: Core coding-agent Python/RPC bridge.
- edge_cases_or_failure_modes: Python process failure, malformed response, timeout, stderr/error mapping.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2507 `file` `packages/coding-agent/test/edit/seen-line-guard.test.ts`
- cursor: `[_]`
- core_role: Tests edit guard using seen-line snapshots.
- algorithmic_behavior: Verifies edits are allowed/blocked based on previously seen lines and file snapshot hashes.
- inputs_outputs_state: Inputs are file contents, read/seen line records, edit requests; outputs are allowed edits or guard errors. State is snapshot store.
- gates_or_invariants: Must prevent editing unseen changed regions while allowing known lines; hash/line snapshots must merge correctly.
- dependencies_and_callers: Edit tools, `packages/hashline/src/snapshots.ts`.
- edge_cases_or_failure_modes: File changed after read, line number shifts, repeated reads, unseen context.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2537 `file` `packages/coding-agent/test/internal-urls/memory-protocol.test.ts`
- cursor: `[_]`
- core_role: Tests internal memory URL protocol.
- algorithmic_behavior: Verifies memory protocol URLs resolve to expected memory content/metadata and reject malformed routes.
- inputs_outputs_state: Inputs are internal `memory://` URLs and memory backend state; outputs are URL read/render results or errors.
- gates_or_invariants: Only valid IDs/routes resolve; content access respects backend/state.
- dependencies_and_callers: Internal URL router and memory backend.
- edge_cases_or_failure_modes: Missing memory, invalid URL, backend unavailable.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2567 `file` `packages/coding-agent/test/session-manager/draft.test.ts`
- cursor: `[_]`
- core_role: Tests session-manager draft persistence/behavior.
- algorithmic_behavior: Verifies draft session/input state is saved, loaded, updated, or cleared according to session-manager contract.
- inputs_outputs_state: Inputs are draft text/session IDs/storage; outputs are persisted draft records and restored state.
- gates_or_invariants: Drafts must be scoped to correct session and not overwrite unrelated sessions.
- dependencies_and_callers: Session manager/storage.
- edge_cases_or_failure_modes: Empty draft, stale session, storage missing/corrupt.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2597 `file` `packages/coding-agent/test/slash-commands/fresh.test.ts`
- cursor: `[_]`
- core_role: Tests `/fresh` slash command provider-state refresh ordering.
- algorithmic_behavior: Asserts command awaits provider-state refresh before resolving (`fresh.test.ts:19-20`).
- inputs_outputs_state: Inputs are slash command invocation and mocked provider refresh promise; outputs are completion only after refresh.
- gates_or_invariants: `/fresh` must not return before refresh side effects settle.
- dependencies_and_callers: Slash command registry/provider state refresh.
- edge_cases_or_failure_modes: Async refresh race, command resolving early.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2627 `file` `packages/coding-agent/test/task/task-guards.test.ts`
- cursor: `[_]`
- core_role: Tests task/subagent guardrails.
- algorithmic_behavior: Verifies task parameter validation, read-only/tool restrictions, plan-mode allowlists, and guard errors for invalid task spawning.
- inputs_outputs_state: Inputs are task tool params/agent definitions/session modes; outputs are task results or validation errors.
- gates_or_invariants: Read-only agents cannot receive write tools; invalid batch/spawn shapes rejected before execution.
- dependencies_and_callers: Tests `packages/coding-agent/src/task/index.ts`.
- edge_cases_or_failure_modes: Batch mismatch, unknown agent/tool, plan mode, read-only bypass.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2657 `file` `packages/coding-agent/test/tools/conflict-detect.test.ts`
- cursor: `[_]`
- core_role: Tests merge-conflict detection, history, URI parsing, splicing, rendering, and token expansion.
- algorithmic_behavior: Covers 2-way/diff3 detection, line offsets, multiple blocks, malformed markers, CRLF normalization, history IDs/dedup/invalidation, `conflict://` parsing/wildcard/recovery, splicing shifted/CRLF/empty replacements, scoped rendering, warning formatting, body caps, and `@ours/@theirs/@base/@both` expansion (`conflict-detect.test.ts:14-544`).
- inputs_outputs_state: Inputs are conflicted file text, first line offsets, conflict URIs, replacement content; outputs are conflict entries, warnings, spliced content, expanded content.
- gates_or_invariants: Ignore malformed/unclosed markers, preserve CRLF when splicing, reject stale recorded blocks, parse scope tokens strictly.
- dependencies_and_callers: Conflict tools/internal URL conflict protocol.
- edge_cases_or_failure_modes: Re-opened opener, label-less markers, base equals ours/theirs collapse, file shorter than recorded region, bad URI IDs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2687 `file` `packages/coding-agent/test/tools/lsp-diagnostics-freshness.test.ts`
- cursor: `[_]`
- core_role: Tests LSP diagnostics freshness after writes.
- algorithmic_behavior: Suppresses stale write diagnostics until matching document version arrives, settles on latest unversioned publish, and returns promptly with deferred diagnostics when server is slow (`lsp-diagnostics-freshness.test.ts:103-202`).
- inputs_outputs_state: Inputs are write operations, LSP publishDiagnostics events with/without versions, timing; outputs are immediate/deferred diagnostic results.
- gates_or_invariants: Versioned diagnostics must match current document version; unversioned servers use latest publish; slow server cannot block tool result indefinitely.
- dependencies_and_callers: LSP diagnostic tool/write integration.
- edge_cases_or_failure_modes: Stale diagnostics, unversioned server, delayed publish, multiple writes.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2717 `file` `packages/coding-agent/test/tools/ssh-render.test.ts`
- cursor: `[_]`
- core_role: Tests SSH tool rendering.
- algorithmic_behavior: Validates SSH command/tool output render formatting and sanitization.
- inputs_outputs_state: Inputs are SSH tool args/results; outputs are rendered preview/result lines.
- gates_or_invariants: Renderer must show command/host context without corrupting TUI and must sanitize output.
- dependencies_and_callers: SSH tool renderer and shared shell renderer.
- edge_cases_or_failure_modes: Long host/command/output, errors, pending preview.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2747 `file` `packages/coding-agent/test/workflow/benchmark-scenarios.test.ts`
- cursor: `[_]`
- core_role: Deterministic integration tests for workflow benchmark scenarios.
- algorithmic_behavior: Runs optimizer search-to-integration and project phase-transition benchmarks deterministically (`benchmark-scenarios.test.ts:60-300`).
- inputs_outputs_state: Inputs are benchmark workflow definitions, mocked runtime/scripts; outputs are workflow run state, node transitions, integration results.
- gates_or_invariants: Workflow runner must produce deterministic state transitions and outputs for benchmark scenarios.
- dependencies_and_callers: Workflow CLI/runner/freeze/lifecycle modules.
- edge_cases_or_failure_modes: Race/order nondeterminism, phase transition misrouting, optimizer state drift.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2777 `file` `packages/collab-web/src/lib/use-guest.ts`
- cursor: `[_]`
- core_role: React hook binding `GuestClient` snapshots into `useSyncExternalStore`.
- algorithmic_behavior: `useGuestSnapshot` subscribes to client changes and returns current snapshot for client/server snapshots (`use-guest.ts:5-10`).
- inputs_outputs_state: Inputs are `GuestClient`; outputs are `GuestSnapshot` React state. State is external client store subscription.
- gates_or_invariants: Subscribe/getSnapshot functions must be stable enough for React external store contract; server snapshot matches client snapshot.
- dependencies_and_callers: Collab web React UI components.
- edge_cases_or_failure_modes: Client replacement, missed unsubscribe, stale snapshot if client mutates without notifying.
- validation_or_tests: `packages/collab-web/test/client.test.ts` covers client snapshots; hook itself likely covered by UI integration.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2807 `file` `packages/mnemopi/src/core/polyphonic-recall.ts`
- cursor: `[_]`
- core_role: Multi-voice memory recall engine combining vector, graph, fact, and temporal scores.
- algorithmic_behavior: Enables feature via env (`polyphonic-recall.ts:87`), normalizes metadata/vectors (`:96-140`), computes cosine/entities/query words/temporal cues (`:140-175`), defines `PolyphonicRecallEngine` (`:182`) to run voice recalls and combine via reciprocal-rank-style score (`RRF_K = 60`, voices at `:84-85`), sorts voice scores (`:535`), caches engine (`:544`), and exports `polyphonicRecall` (`:556`).
- inputs_outputs_state: Inputs are DB/beam state, query, embedding, recall options/env; outputs are ranked `PolyphonicResult`/memory results with voice scores. State includes opened DB/engine cache.
- gates_or_invariants: Disabled by env when configured, vectors normalized, metadata JSON sanitized, voice list stable, results merged without losing per-voice provenance.
- dependencies_and_callers: Mnemopi Beam memory, episodic graph, veracity consolidator, SQLite DB.
- edge_cases_or_failure_modes: Missing embeddings, zero vector, malformed metadata JSON, temporal query detection false positives, DB close/open errors.
- validation_or_tests: Mnemopi memory/beam tests; polyphonic-specific tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2837 `file` `packages/stats/src/client/useSystemTheme.ts`
- cursor: `[_]`
- core_role: React hook/store for stats dashboard theme preference and resolved system theme.
- algorithmic_behavior: Reads local storage preference (`useSystemTheme.ts:9`), detects system theme via media query (`:15`), emits listener updates (`:24-30`), applies resolved theme to document (`:30`), sets preference (`:49`), subscribes (`:56`), exposes `useSystemTheme` and `useThemePreference` (`:62-71`).
- inputs_outputs_state: Inputs are localStorage, `matchMedia`, user preference changes; outputs are React external-store values and document theme class/data. State is module-level listeners and stored preference.
- gates_or_invariants: Preference must be one of `system|light|dark`, system fallback safe when browser APIs unavailable, subscribers notified on changes.
- dependencies_and_callers: Stats React UI routes/components.
- edge_cases_or_failure_modes: SSR/no window, localStorage errors, media query change, invalid stored value.
- validation_or_tests: Stats client tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2867 `file` `python/omp-rpc/src/omp_rpc/host_uris.py`
- cursor: `[_]`
- core_role: Python host URI registry/context abstraction for RPC tools.
- algorithmic_behavior: Defines read result type (`host_uris.py:17`), `HostUriContext` with registry/lock (`:33`), immutable `HostUri` handler descriptor (`:54`), decorator/registration helper `host_uri` (`:75`), and read-result normalization (`:95`).
- inputs_outputs_state: Inputs are URI handler functions and read return values (text/json/etc.); outputs are normalized JSON objects. State is context registry protected by threading lock.
- gates_or_invariants: Handler registration is thread-safe, normalized read result must be JSON object, payload generic typing preserved.
- dependencies_and_callers: Python RPC host tool protocol.
- edge_cases_or_failure_modes: Duplicate URI registrations, handler returns plain unsupported value, concurrent registration/read.
- validation_or_tests: Python RPC/host tool tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2897 `directory` `packages/utils/src/vendor/mermaid-ascii/sequence`
- cursor: `[_]`
- core_role: Vendored Mermaid sequence diagram parser/types for ASCII rendering.
- algorithmic_behavior: `parser.ts` parses sequence diagram syntax into typed AST/events; `types.ts` defines participant/message/activation/note/loop/alt structures consumed by ASCII renderer.
- inputs_outputs_state: Inputs are Mermaid sequence source strings; outputs are typed sequence diagram model. Parser state tracks current block/participants/messages.
- gates_or_invariants: Must preserve participant ordering, message directions, nested block structure, and tolerate supported Mermaid subset.
- dependencies_and_callers: Used by vendored mermaid-ascii renderer in utils.
- edge_cases_or_failure_modes: Unsupported syntax, malformed nested blocks, aliases, comments/blank lines.
- validation_or_tests: Mermaid ASCII tests/render snapshots if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2927 `file` `packages/ai/src/registry/oauth/anthropic.ts`
- cursor: `[_]`
- core_role: Anthropic OAuth login/refresh helper.
- algorithmic_behavior: Implements OAuth controller flow, callback/code handling, token exchange, credential shaping, and `refreshAnthropicToken` export (`oauth/anthropic.ts:259`).
- inputs_outputs_state: Inputs are OAuth controller callbacks, auth code/refresh token/client metadata; outputs are `OAuthCredentials` and refreshed tokens. State is browser/callback flow plus stored credentials outside this module.
- gates_or_invariants: Must validate state/code exchange, preserve scopes/expiry, refresh using correct token endpoint.
- dependencies_and_callers: Provider registry/auth storage and Anthropic provider.
- edge_cases_or_failure_modes: User cancel, callback timeout, invalid refresh token, network error, missing fields.
- validation_or_tests: Auth/OAuth registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2957 `file` `packages/ai/src/utils/schema/stamps.ts`
- cursor: `[_]`
- core_role: Schema stamping utilities for marking/identifying transformed schemas.
- algorithmic_behavior: Adds/checks/removes internal stamp metadata on schema objects to track normalization/compat decisions.
- inputs_outputs_state: Inputs are JSON schema-like objects and stamp names; outputs are stamped schemas or booleans. State is embedded metadata on schema objects or cloned objects.
- gates_or_invariants: Stamps must avoid colliding with provider-visible schema semantics and preserve JSON schema validity after removal.
- dependencies_and_callers: Provider strict schema normalizers (Anthropic/OpenAI tools).
- edge_cases_or_failure_modes: Frozen objects, circular schemas, provider rejecting unknown metadata, clone vs mutate expectations.
- validation_or_tests: Strict schema/tool tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2987 `file` `packages/coding-agent/src/commit/agentic/topo-sort.ts`
- cursor: `[_]`
- core_role: Dependency ordering for agentic split commit groups.
- algorithmic_behavior: `computeDependencyOrder` runs topological sort over `SplitCommitGroup[]`, returning group index order or `{ error }` for cycles/missing dependency (`topo-sort.ts:3-44`).
- inputs_outputs_state: Inputs are commit groups with dependencies; outputs are sorted indices or error. State is local visited/visiting sets.
- gates_or_invariants: Dependencies must refer to known groups; cycle detection must abort with error; output indices preserve dependency-before-dependent.
- dependencies_and_callers: Agentic commit planner/split commit workflow.
- edge_cases_or_failure_modes: Self-cycle, missing dependency, disconnected groups, duplicate dependency edges.
- validation_or_tests: Commit agentic tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3017 `file` `packages/coding-agent/src/edit/modes/replace.ts`
- cursor: `[_]`
- core_role: Replace-edit matching and execution algorithm.
- algorithmic_behavior: Defines match/fuzzy/context result types and `EditMatchError` (`replace.ts:27-74`), occurrence errors (`:134`), thresholds (`:148-178`), exact and fuzzy matching (`:259-447`), single/multi-line `findMatch` (`:476`), sequence seeking (`:610`), closest sequence and context line search (`:804-856`), schemas (`:1013-1025`), and `executeReplaceSingle` (`:1039`).
- inputs_outputs_state: Inputs are file content, old/new text, occurrence/context options, fuzzy thresholds; outputs are patched content or match errors with previews. State is local match indexes/line offsets.
- gates_or_invariants: Ambiguous matches rejected unless occurrence resolves; fuzzy thresholds/dominance enforced; context matching escalates exact/trim/unicode/prefix/substring/fuzzy; comments/indent normalized carefully.
- dependencies_and_callers: Edit tool implementation and seen-line guard.
- edge_cases_or_failure_modes: Multiple occurrences, partial matches, Unicode normalization, indentation depth, comment prefixes, shifted lines, too-short partial targets.
- validation_or_tests: Edit/replace and seen-line guard tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3047 `file` `packages/coding-agent/src/extensibility/custom-commands/index.ts`
- cursor: `[_]`
- core_role: Barrel export for custom commands loader/types.
- algorithmic_behavior: Re-exports loader and type exports at `custom-commands/index.ts:1-2`.
- inputs_outputs_state: No algorithmic inputs; output is module API surface.
- gates_or_invariants: Barrel must avoid duplicate/ambiguous exports.
- dependencies_and_callers: Extension/custom command importers.
- edge_cases_or_failure_modes: Export conflict after loader/types changes.
- validation_or_tests: Typecheck/extension tests.
- skip_candidate: `yes: barrel only.`

### OH_MY_HUMANIZE_MAIN-HZ-3077 `file` `packages/coding-agent/src/extensibility/plugins/types.ts`
- cursor: `[_]`
- core_role: Type contracts for plugin manifests, settings, installed/runtime state, and doctor/install options.
- algorithmic_behavior: Defines feature/manifest types (`plugins/types.ts:9-55`), setting schemas (`:55-93`), installed plugin/runtime config/state (`:102-156`), project overrides (`:156`), doctor checks (`:169`), install/doctor options (`:184-191`).
- inputs_outputs_state: Inputs are plugin manifests/configs; outputs are typed runtime/install structures. No runtime state here.
- gates_or_invariants: Setting schema union constrains enum/number/string/boolean, runtime state records enabled/errors/paths consistently.
- dependencies_and_callers: Plugin marketplace/manager/loader/settings UI.
- edge_cases_or_failure_modes: Manifest schema drift, unknown setting type, incompatible plugin runtime state.
- validation_or_tests: Plugin marketplace/extension tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3107 `file` `packages/coding-agent/src/modes/components/collab-prompt-message.ts`
- cursor: `[_]`
- core_role: TUI component rendering collaboration prompt messages.
- algorithmic_behavior: `CollabPromptMessageComponent` extends `Container`, extracts `CollabPromptDetails`/message content, and renders Markdown/Text with theme (`collab-prompt-message.ts:1-11`).
- inputs_outputs_state: Inputs are custom collab prompt message details/content; outputs are TUI child components/lines. State is component tree.
- gates_or_invariants: Raw prompt content must render through Markdown/theme, not unsafe plain terminal output.
- dependencies_and_callers: Collab transcript rendering in modes.
- edge_cases_or_failure_modes: Missing details, non-text content, markdown containing unsafe terminal sequences.
- validation_or_tests: Collab/TUI component tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3137 `file` `packages/coding-agent/src/modes/components/plan-toc.ts`
- cursor: `[_]`
- core_role: TUI component/helper for rendering plan table-of-contents.
- algorithmic_behavior: Parses/organizes plan headings/items and renders navigable TOC lines with selection/progress styling.
- inputs_outputs_state: Inputs are plan markdown/structure and UI width/theme; outputs are TUI components/lines. State is selection/focus if present.
- gates_or_invariants: Heading hierarchy/order preserved, long text truncated, empty plan handled.
- dependencies_and_callers: Plan mode UI and command controller.
- edge_cases_or_failure_modes: Malformed markdown headings, very deep heading levels, narrow terminal.
- validation_or_tests: Plan mode/component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3167 `file` `packages/coding-agent/src/modes/controllers/command-controller.ts`
- cursor: `[_]`
- core_role: Interactive command controller for TUI slash commands, panels, compaction, session actions, providers, jobs, and settings surfaces.
- algorithmic_behavior: Shows markdown panels (`command-controller.ts:52`), implements `CommandController` (`:62`) with command dispatch methods, status/job/provider rendering helpers (`:1212-1495`), usage bars, auth mode formatting, context/help/tools panels, share/export, compact/handoff actions, memory backend actions, changelog/open/copy utilities.
- inputs_outputs_state: Inputs are interactive mode context, command strings/args, session state, async jobs, provider usage reports, auth storage; outputs are UI panels, session actions, copied/opened paths, command results. State lives in controller/context/session.
- gates_or_invariants: Rendered output must sanitize tabs and fit widths, usage reports aggregate and color by status, command actions respect mode/session availability, compaction cancellation handled.
- dependencies_and_callers: Main interactive mode, TUI components, AgentSession, settings, memory, share/export, slash commands.
- edge_cases_or_failure_modes: Missing auth usage, narrow terminal usage bars, async job status drift, compaction cancelled, invalid file/changelog path.
- validation_or_tests: ACP, command, TUI, event-controller tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3197 `file` `packages/coding-agent/src/modes/utils/keybinding-matchers.ts`
- cursor: `[_]`
- core_role: Keybinding matching utility for mode controllers.
- algorithmic_behavior: Normalizes key events/binding specs and determines whether a key event matches a configured action.
- inputs_outputs_state: Inputs are key event objects and keybinding strings/configs; outputs are boolean matches or normalized forms. No persistent state.
- gates_or_invariants: Modifier order/case aliases must normalize consistently; printable vs control keys separated.
- dependencies_and_callers: Input controller, command controller, settings keybindings.
- edge_cases_or_failure_modes: Platform meta/control aliases, shifted characters, duplicate modifiers, unknown key names.
- validation_or_tests: Keybinding migration/input tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3227 `file` `packages/coding-agent/src/web/scrapers/bluesky.ts`
- cursor: `[_]`
- core_role: Special web scraper for Bluesky posts/threads.
- algorithmic_behavior: Resolves handles via public API (`bluesky.ts:58`), formats posts (`:76`), and `handleBluesky` parses URL/loads thread/profile data and builds markdown result (`:150`).
- inputs_outputs_state: Inputs are Bluesky URLs, timeout, abort signal; outputs are `RenderResult` markdown with profile/post/thread info. No durable state.
- gates_or_invariants: Handle/DID resolution required, API responses parsed defensively, counts formatted, quote posts handled separately.
- dependencies_and_callers: Web fetch/scraper router and `tryParseJson`, `loadPage`, `buildResult`.
- edge_cases_or_failure_modes: Invalid URL, handle resolution failure, deleted/unavailable post, malformed API JSON, nested quotes.
- validation_or_tests: Web scraper tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3257 `file` `packages/coding-agent/src/web/scrapers/lobsters.ts`
- cursor: `[_]`
- core_role: Special web scraper for Lobsters stories/comments.
- algorithmic_behavior: Defines story/comment response shapes, recursively renders comments with max depth (`lobsters.ts:51`), and `handleLobsters` fetches JSON/story data and formats result (`:72`).
- inputs_outputs_state: Inputs are Lobsters URL, timeout, abort signal; outputs are markdown render result. No durable state.
- gates_or_invariants: Comment depth bounded to default 5, ISO dates formatted, invalid JSON falls back/error.
- dependencies_and_callers: Web scraper router, `tryParseJson`, `loadPage`, `buildResult`.
- edge_cases_or_failure_modes: Deep comment trees, missing comments, story not found, malformed JSON.
- validation_or_tests: Web scraper tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3287 `file` `packages/coding-agent/src/web/scrapers/spdx.ts`
- cursor: `[_]`
- core_role: Special web scraper for SPDX license pages.
- algorithmic_behavior: Formats yes/no fields (`spdx.ts:26`), collects cross references (`:32`), and `handleSpdx` fetches/parses SPDX JSON/license page and produces markdown (`:46`).
- inputs_outputs_state: Inputs are SPDX URL, timeout, signal; outputs are license metadata markdown. No durable state.
- gates_or_invariants: Cross references bounded/filtered, boolean fields normalized, JSON parse fallback to basic markdown.
- dependencies_and_callers: Web scraper router, `tryParseJson`, `htmlToBasicMarkdown`, `loadPage`.
- edge_cases_or_failure_modes: Missing license JSON, malformed cross refs, unknown license ID.
- validation_or_tests: Web scraper package-manager tests adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3317 `file` `packages/coding-agent/test/modes/components/compaction-summary-message.test.ts`
- cursor: `[_]`
- core_role: Tests compaction summary TUI component rendering.
- algorithmic_behavior: Verifies compaction summary message displays expected summary content/metadata without render corruption.
- inputs_outputs_state: Inputs are compaction summary message data; outputs are rendered component lines.
- gates_or_invariants: Summary render must sanitize/format content and show correct status.
- dependencies_and_callers: Compaction summary message component.
- edge_cases_or_failure_modes: Empty summary, long lines, markdown/control content.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3347 `file` `packages/coding-agent/test/modes/controllers/event-controller-abort-guard.test.ts`
- cursor: `[_]`
- core_role: Tests event controller abort guard.
- algorithmic_behavior: Verifies late/aborted events do not mutate UI/session state after cancellation.
- inputs_outputs_state: Inputs are event controller events and abort signals; outputs are suppressed or applied updates.
- gates_or_invariants: Aborted signal must gate event handling consistently across async boundaries.
- dependencies_and_callers: Modes event controller/session update pipeline.
- edge_cases_or_failure_modes: Late tool/assistant events after cancel, double abort, cleanup race.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3377 `file` `packages/coding-agent/test/tools/web-scrapers/package-managers.test.ts`
- cursor: `[_]`
- core_role: Tests web scraper special handling for package-manager pages.
- algorithmic_behavior: Validates package-manager scraper URL matching/fetch/render behavior.
- inputs_outputs_state: Inputs are package URLs/HTML/JSON fixtures; outputs are markdown render results.
- gates_or_invariants: Supported package manager URLs must route to correct scraper and handle missing metadata.
- dependencies_and_callers: Web scraper router and package-manager handlers.
- edge_cases_or_failure_modes: Invalid package names, missing versions, malformed registry response.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3407 `file` `packages/collab-web/src/tool-render/tools/ast-grep.tsx`
- cursor: `[_]`
- core_role: Collab web renderer for `ast-grep` tool output.
- algorithmic_behavior: Parses ast-grep tool call/result data and renders matches/findings in React/TSX.
- inputs_outputs_state: Inputs are tool args/result JSON from transcript; outputs are React elements. State is render-only.
- gates_or_invariants: Must handle malformed/missing result fields and avoid unsafe HTML.
- dependencies_and_callers: Collab web tool-render registry.
- edge_cases_or_failure_modes: Empty matches, invalid JSON, long paths/snippets, error results.
- validation_or_tests: Collab web rendering tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3437 `file` `packages/mnemopi/src/core/beam/consolidate.ts`
- cursor: `[_]`
- core_role: Beam memory consolidation and promotion algorithm.
- algorithmic_behavior: Consolidates working memories into episodic/fact/veracity structures, scores candidates, merges duplicates, writes consolidation logs, and manages retention/promotion state across Beam memory DB.
- inputs_outputs_state: Inputs are Beam memory state, memory rows, annotations, consolidation options/time; outputs are updated memory tiers, episodic/fact records, log entries. State is SQLite Beam store.
- gates_or_invariants: Consolidation must preserve important/recent memories, avoid duplicate facts, keep annotations/logs consistent, and honor scope/session boundaries.
- dependencies_and_callers: Mnemopi Beam core, episodic graph, veracity consolidation, database helpers.
- edge_cases_or_failure_modes: Empty candidate set, duplicate/contradictory memories, DB transaction failure, malformed metadata, retention boundary off-by-one.
- validation_or_tests: Mnemopi beam/memory tests and consolidation-specific tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3467 `file` `packages/stats/src/client/routes/ModelsRoute.tsx`
- cursor: `[_]`
- core_role: Stats UI route for displaying model usage/metrics.
- algorithmic_behavior: Fetches/selects model stats, computes grouped/sorted metrics, renders tables/cards/charts and loading/error states in React.
- inputs_outputs_state: Inputs are stats API data, route state, filters/sorting; outputs are React UI. State is component hooks and fetched data.
- gates_or_invariants: Must handle missing data, stable sort/group, avoid crashing on unknown providers/models.
- dependencies_and_callers: Stats client router/API hooks and theme.
- edge_cases_or_failure_modes: Empty model list, partial usage data, large model counts, fetch errors.
- validation_or_tests: Stats route tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3497 `file` `python/robomp/web/src/components/Pill.tsx`
- cursor: `[_]`
- core_role: Small Solid component for status pills.
- algorithmic_behavior: Builds class list from `state`, `dot`, and custom class and renders a `<span>` with optional title/children (`Pill.tsx:3-24`).
- inputs_outputs_state: Inputs are props; outputs are JSX element. No persistent state.
- gates_or_invariants: Class composition order stable: `pill`, state, `dot`, custom class.
- dependencies_and_callers: roboomp web dashboard components.
- edge_cases_or_failure_modes: Undefined props, custom class collision.
- validation_or_tests: Web UI tests/manual.
- skip_candidate: `yes: presentational component, minimal algorithmic content.`

### OH_MY_HUMANIZE_MAIN-HZ-3527 `file` `packages/coding-agent/src/extensibility/plugins/marketplace/index.ts`
- cursor: `[_]`
- core_role: Barrel export for plugin marketplace modules.
- algorithmic_behavior: Re-exports cache, fetcher, manager, registry, source resolver, and types (`marketplace/index.ts:1-6`).
- inputs_outputs_state: No algorithmic inputs; output is module API surface.
- gates_or_invariants: Export surface must not conflict and should expose all marketplace submodules.
- dependencies_and_callers: Plugin CLI/settings/marketplace manager importers.
- edge_cases_or_failure_modes: Barrel ambiguity after submodule export changes.
- validation_or_tests: Typecheck/plugin tests.
- skip_candidate: `yes: barrel only.`

### OH_MY_HUMANIZE_MAIN-HZ-3557 `file` `packages/coding-agent/src/modes/setup-wizard/scenes/sign-in.ts`
- cursor: `[_]`
- core_role: Setup wizard sign-in scene.
- algorithmic_behavior: Presents provider sign-in choices, drives auth/login actions, updates scene state, and routes success/failure/skip paths.
- inputs_outputs_state: Inputs are user key selections, auth providers/storage, wizard context; outputs are auth attempts, UI state transitions, next scene selection. State is scene-local selection/loading/error.
- gates_or_invariants: Must not mark sign-in complete until auth succeeds or explicit skip, must surface provider errors without crashing wizard.
- dependencies_and_callers: Setup wizard scene runner, auth storage/provider registry, TUI components.
- edge_cases_or_failure_modes: User cancels OAuth, provider unavailable, network/auth error, repeated sign-in attempts.
- validation_or_tests: Setup wizard tests/manual.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3587 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/edge-bundling.ts`
- cursor: `[_]`
- core_role: Vendored ASCII graph edge bundling and routing algorithm.
- algorithmic_behavior: Finds bundle candidates (`edge-bundling.ts:41`), tests bundle compatibility (`:133`), calculates junction point (`:178`), routes bundled edges (`:248`), and processes all bundles (`:324`) by merging paths on the ASCII grid.
- inputs_outputs_state: Inputs are `AsciiGraph` nodes/edges/grid; outputs are modified edge paths with shared bundle segments/junctions. State is graph edge path mutation.
- gates_or_invariants: Bundle only compatible edges, preserve source/target reachability, avoid node/subgraph collisions via pathfinder/grid helpers.
- dependencies_and_callers: Mermaid ASCII graph renderer, pathfinder/grid/types.
- edge_cases_or_failure_modes: Crossing edges, overlapping nodes, incompatible directions, no valid junction path, merge path conflicts.
- validation_or_tests: Mermaid ASCII render tests/snapshots.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3617 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/stadium.ts`
- cursor: `[_]`
- core_role: Vendored ASCII stadium/rounded terminal node shape renderer.
- algorithmic_behavior: Computes/draws stadium shape boundaries/text layout for ASCII graph nodes.
- inputs_outputs_state: Inputs are node dimensions/label/style; outputs are ASCII grid cells/shape lines. No persistent state beyond grid mutation.
- gates_or_invariants: Shape must fit requested dimensions and connect to edges at expected ports.
- dependencies_and_callers: Mermaid ASCII shape renderer registry.
- edge_cases_or_failure_modes: Very small widths/heights, long labels, connector collision.
- validation_or_tests: Mermaid ASCII render tests/snapshots.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `121 item evidence sections present; checked against assigned_item_count without repeating item IDs here to keep item identifiers single-occurrence in the evidence body.`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`