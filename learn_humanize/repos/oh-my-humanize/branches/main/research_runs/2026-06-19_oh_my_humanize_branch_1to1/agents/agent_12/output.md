# agent_12 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-012 `file` `biome.json`
- cursor: `[_]`
- core_role: Workspace formatting, linting, VCS, and file-inclusion policy.
- algorithmic_behavior: Defines deterministic formatting and lint gates: tab indentation, line width 120, LF endings, JS semicolon and quote style, recommended lint rules, organize-import behavior, and per-rule exceptions.
- inputs_outputs_state: Input is repo source/config files; output is Biome diagnostics and rewrites. State is static JSON policy.
- gates_or_invariants: Excludes generated/build/vendor-like paths; enforces enabled linter rules while explicitly disabling some noisy rules such as `noExplicitAny`.
- dependencies_and_callers: Consumed by Biome CLI/editor integrations and any CI or local formatting task invoking Biome.
- edge_cases_or_failure_modes: Misclassified excludes can hide files from linting; disabled rules permit patterns otherwise banned by project prose.
- validation_or_tests: Validated indirectly by formatting/lint invocations; no file-local test.
- skip_candidate: `yes: tooling configuration, not a runtime algorithm, though it shapes build/test gates`

### OH_MY_HUMANIZE_MAIN-HZ-042 `directory` `scripts/install-tests`
- cursor: `[_]`
- core_role: Install/release smoke workflow for binary, source-link, and tarball distributions.
- algorithmic_behavior: `run-ci.sh` builds or packages artifacts, sets isolated HOME/XDG paths, runs `omp --version`, `--help`, `stats --summary`, and `--smoke-test`, then verifies tarball install layout and protocol assets. Dockerfiles model binary/source/tarball install environments; `run-podman.sh` orchestrates image builds.
- inputs_outputs_state: Inputs are local packages, native package metadata, Bun install state, and platform environment. Outputs are installed test sandboxes, smoke command results, tarballs, and container build status.
- gates_or_invariants: `run-ci.sh` requires the worker-host smoke to pass, verifies native platform leaf installation, checks `COLLAB_PROTO === 1`, and asserts collab-web assets are present.
- dependencies_and_callers: Depends on Bun, package scripts, `packages/natives`, `packages/coding-agent`, optional Podman/Docker. Called by release/install CI.
- edge_cases_or_failure_modes: Platform-native package rewrite or missing binary entry can pass build but fail install smoke; tarball path rewriting must preserve package dependency graph.
- validation_or_tests: The directory is itself a validation suite; `ci:test:smoke` and install scripts exercise it.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-072 `file` `docs/session-tree-plan.md`
- cursor: `[_]`
- core_role: Architecture specification for append-only session tree branching, navigation, and summary behavior.
- algorithmic_behavior: Defines entries with `id`/`parentId`, an active `leafId`, tree indexes, `/tree` in-session navigation, `/branch` new-session creation, branch summaries, labels, hooks, and context reconstruction root-to-leaf.
- inputs_outputs_state: Inputs are session entries, selected tree targets, hooks, user/custom messages, summaries, and compaction state. Outputs are changed leaf pointers, appended summary/label entries, new session files, and reconstructed model context.
- gates_or_invariants: `branch(entryId)` cannot target null; branch session source must be a user message; null leaf persists as root; summaries need an active model and abort handling.
- dependencies_and_callers: Guides `SessionManager`, TUI tree UI, slash commands, hooks `session_before_tree` and `session_tree`, and plan title behavior.
- edge_cases_or_failure_modes: In-memory branch can return undefined; navigation to custom/user messages has different leaf positioning; hook cancellation can block movement.
- validation_or_tests: Covered indirectly by session tree, branch/export, and plan handoff tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-102 `file` `scripts/host-detect.ts`
- cursor: `[_]`
- core_role: Host CPU capability detector, currently focused on AVX2 support.
- algorithmic_behavior: `detectHostAvx2Support()` returns false unless `process.arch` is `x64`; Linux scans `/proc/cpuinfo`, macOS checks `sysctl` feature leaves, Windows invokes PowerShell intrinsic support.
- inputs_outputs_state: Inputs are OS/architecture and platform-specific CPU feature surfaces. Output is a boolean.
- gates_or_invariants: Every exception falls back to false; non-x64 hosts are always false.
- dependencies_and_callers: Uses Bun file/process APIs and `process.platform`; used by install/build decisions needing native feature routing.
- edge_cases_or_failure_modes: Missing `/proc/cpuinfo`, unavailable `sysctl`, PowerShell failure, localized output, or sandbox denial all produce false negatives.
- validation_or_tests: No direct test observed; behavior is simple defensive probing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-132 `directory` `packages/coding-agent/scripts`
- cursor: `[_]`
- core_role: Coding-agent build, bundle, docs, prompt, benchmark, and development launcher scripts.
- algorithmic_behavior: Contains `build-binary.ts` compiled-binary pipeline, `bundle-dist.ts` npm bundle generation, `embed-mupdf-wasm.ts` asset embedding/reset, `generate-docs-index.ts` docs payload generation/reset, `generate-share-viewer.ts` standalone viewer injection, `format-prompts.ts`, `bench-guard.ts`, and `omp`/`omp.ts` launch cwd shims.
- inputs_outputs_state: Inputs include source files, prompts, docs, stats client bundle, wasm assets, baseline benchmark files, and env vars. Outputs are dist artifacts, embedded placeholders, generated docs/share assets, benchmark reports, and launcher process state.
- gates_or_invariants: Build scripts reset generated placeholders after binary build; bundle keeps shebang; docs/share generators validate placeholders; benchmark threshold defaults to 1.05.
- dependencies_and_callers: Depends on Bun build/shell APIs, package scripts, prompt formatter, docs tree, and release/install workflows.
- edge_cases_or_failure_modes: Placeholder drift, missing stats/docs assets, codesign quirks on Darwin, or launcher cwd leakage can break binary/npm distribution.
- validation_or_tests: Install smoke scripts and build pipeline tests cover important contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-162 `directory` `packages/wire/test`
- cursor: `[_]`
- core_role: Protocol constant regression tests for the wire package.
- algorithmic_behavior: `constants.test.ts` asserts stable collaboration protocol values such as protocol version, prompt type, header length, room id byte width, and relay URL.
- inputs_outputs_state: Inputs are exported wire constants; output is pass/fail test status.
- gates_or_invariants: Protocol constants must not drift silently because peer clients parse exact values.
- dependencies_and_callers: Depends on `packages/wire` exports; protects collab clients/servers.
- edge_cases_or_failure_modes: Accidental constant change would break binary/browser compatibility.
- validation_or_tests: The directory is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-192 `file` `docs/tools/irc.md`
- cursor: `[_]`
- core_role: Runtime contract documentation for the agent-to-agent IRC tool.
- algorithmic_behavior: Specifies `send`, `wait`, `inbox`, and `list` operations, mailbox behavior, roster activity, delivery statuses, broadcasts, revival of parked peers, and wait timeout semantics.
- inputs_outputs_state: Inputs are tool args `op`, `to`, `message`, `replyTo`, `await`, `from`, `timeoutMs`, `peek`. Outputs are `AgentToolResult` text and structured details with receipts, inbox, peers, or waited result.
- gates_or_invariants: Tool only available with registry/agent id and subagent/task capability; no self-send; `await: all` incompatible with direct recipient semantics; mailbox cap is 100; send errors only when no recipient receives.
- dependencies_and_callers: Guides IRC tool implementation, agent registry, async job/task orchestration, and roster rendering.
- edge_cases_or_failure_modes: Busy non-async recipients can auto-reply; negative/nonfinite timeout defaults; timeout `0` means indefinite; parked peers are listed and direct send can revive.
- validation_or_tests: Covered by `packages/coding-agent/test/tools/irc-roster-activity.test.ts` and likely IRC tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-222 `file` `scripts/session-stats/plot_read_summarizer.py`
- cursor: `[_]`
- core_role: Analytics script for read-tool summarizer token impact over time.
- algorithmic_behavior: Classifies read calls by selector/path shape, fetches token arrays from a SQLite stats DB, computes daily denominators, daily sums, percentiles, smoothed trends, pre/post deploy share stats, and plots stacked/line/per-call panels.
- inputs_outputs_state: Inputs are session stats database rows, deployment timestamp, and plotting parameters. Outputs are printed statistics and matplotlib figures.
- gates_or_invariants: Cohort classification depends on JSON args and selector detection; token arrays are converted to NumPy arrays and aligned to day axes.
- dependencies_and_callers: Depends on SQLite connection, NumPy, matplotlib, datetime; likely run manually for telemetry analysis.
- edge_cases_or_failure_modes: Missing malformed arg JSON yields unknown cohort; NaN smoothing must avoid empty windows; sparse days produce missing percentiles.
- validation_or_tests: No direct tests; intended as research/observability script.
- skip_candidate: `yes: offline analytics, not runtime behavior`

### OH_MY_HUMANIZE_MAIN-HZ-252 `directory` `packages/coding-agent/src/commands`
- cursor: `[_]`
- core_role: Top-level CLI subcommand registry and command wrapper layer for coding-agent.
- algorithmic_behavior: Command modules declare args, flags, aliases, descriptions, examples, theme init, and delegate to feature-specific implementation under `src/cli`, tools, auth, workflow, stats, or read subsystems.
- inputs_outputs_state: Inputs are argv tokens and command context. Outputs are command execution side effects, printed responses, or delegated interactive modes.
- gates_or_invariants: Commands validate required args, preserve aliases, avoid TUI corruption by delegating through proper command handlers, and keep command registration discoverable.
- dependencies_and_callers: Consumed by CLI command registry; siblings include `src/cli/*`, auth modules, workflow modules, session modules, and read command.
- edge_cases_or_failure_modes: Thin wrappers can mis-declare flags, breaking parse/autocomplete despite correct underlying implementation.
- validation_or_tests: Slash-command and CLI tests cover registration, unknown flags, join command, setup/login/switch behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-282 `directory` `packages/coding-agent/src/stt`
- cursor: `[_]`
- core_role: Speech-to-text subsystem for recording, endpointing, model download, worker inference, and editor insertion.
- algorithmic_behavior: `asr-client.ts` manages worker subprocess protocol; `asr-worker.ts` loads Transformers or sherpa runtimes and serializes model use; `endpointer.ts` implements energy VAD with pre-roll, partials, silence/max-length finalize; `recorder.ts` chooses sox/ffmpeg/arecord/PowerShell; `wav.ts` decodes RIFF and raw PCM; `stt-controller.ts` coordinates state.
- inputs_outputs_state: Inputs are microphone/audio stream or WAV files, selected model tier, aborts, and editor sink. Outputs are partial/final transcripts, model downloads, progress events, temp WAVs, and editor text commits.
- gates_or_invariants: Controller state is idle/recording/transcribing; model downloads must satisfy complete-file cache checks; raw stream requires even s16le bytes; WAV must have supported fmt/data chunks.
- dependencies_and_callers: Depends on worker host entry, Bun subprocesses, ONNX/transformers/sherpa runtimes, tools-manager ffmpeg, editor mode controller.
- edge_cases_or_failure_modes: Worker death fails pending transcriptions; PowerShell cannot stream; tiny audio files rejected; NAPI finalizer crash avoided by hard-killing STT worker.
- validation_or_tests: `wav.ts` and controller behavior have focused tests elsewhere; worker smoke is tied to CLI worker-host contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-312 `directory` `packages/coding-agent/test/slash-commands`
- cursor: `[_]`
- core_role: Contract tests for built-in slash command parsing, dispatch, and editor/history side effects.
- algorithmic_behavior: Tests `/btw`, `/omfg`, `/tan`, `/debug`, `/force`, `/fresh`, `/login`, `/plan-history`, `/retry`, `/session`, `/setup`, `/shake`, `/switch`/`/model`, and type-level slash registry behavior.
- inputs_outputs_state: Inputs are slash command strings and mocked UI/session handlers. Outputs are handler calls, editor clearing/preservation, warning text, forced tool choice, and autocomplete/advertisement metadata.
- gates_or_invariants: Multi-word suffixes are preserved; plan/goal text history survives mode transitions; async handlers are awaited; unknown modes/args surface usage instead of executing.
- dependencies_and_callers: Depends on slash-command registry, command mode state, session facade, provider refresh, and model selector handlers.
- edge_cases_or_failure_modes: Parser bugs can drop suffix text, clear editor too early, or run stale session operations.
- validation_or_tests: The directory is validation for slash-command contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-342 `file` `crates/pi-iso/src/diff.rs`
- cursor: `[_]`
- core_role: Backend-agnostic tree diff capture for isolated workspace comparison.
- algorithmic_behavior: `default_diff(lower, merged)` uses git diff when `merged/.git` exists and plain filesystem walk otherwise. Git mode parses `diff --git` blocks plus untracked files; plain mode builds sorted file maps and emits added/modified/removed entries using `similar::TextDiff`.
- inputs_outputs_state: Inputs are lower and merged directory paths. Outputs are `Change` records with path, status, optional unified diff, and binary omission markers.
- gates_or_invariants: Binary or invalid UTF-8 content gets `diff: None`; git `--no-index` exit code 1 is success; plain mode skips equal length plus mtime-second matches.
- dependencies_and_callers: Depends on `git`, `similar`, filesystem metadata and readers; called by isolation/diff consumers.
- edge_cases_or_failure_modes: Symlinks are indexed specially but plain read may follow/fail; non-UTF8 git blobs are skipped; Windows null path uses `NUL`.
- validation_or_tests: Covered by Rust crate tests if present; behavior is explicit in implementation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-372 `file` `crates/pi-natives/src/summary.rs`
- cursor: `[_]`
- core_role: N-API bridge exposing code summarization from native Rust to JS.
- algorithmic_behavior: Defines `SummaryOptions`, `SummarySegment`, and `SummaryResult`, calls `pi_ast::summary::summarize_code`, and maps Rust results/errors to N-API compatible objects.
- inputs_outputs_state: Inputs are source code and summary options. Outputs are segment arrays and summary metadata.
- gates_or_invariants: Native errors convert to JavaScript errors; options shape must match N-API generated bindings.
- dependencies_and_callers: Depends on `napi`, `pi_ast`, and JS native package consumers.
- edge_cases_or_failure_modes: Unsupported language or parser failure bubbles as N-API error.
- validation_or_tests: Likely covered by native summary consumers; no direct file-local test observed.
- skip_candidate: `yes: bridge layer, core summarization algorithm lives in pi_ast`

### OH_MY_HUMANIZE_MAIN-HZ-402 `file` `packages/agent/test/compaction-telemetry.test.ts`
- cursor: `[_]`
- core_role: Telemetry regression tests for compaction, handoff, and branch-summary one-shot LLM calls.
- algorithmic_behavior: Builds mock model/provider usage, runs compaction preparation and summary helpers, and verifies OpenTelemetry spans are emitted with oneshot kind, model, conversation id, step number, tool choice, status, and usage tokens.
- inputs_outputs_state: Inputs are mock messages, usage objects, compaction preparations, and failing provider stubs. Outputs are finished spans and propagated errors.
- gates_or_invariants: Compaction span step is `-1`; usage input includes cache read/write; disabled telemetry emits no spans; failures mark span error without response usage.
- dependencies_and_callers: Depends on agent compaction/handoff/branch summary helpers, OpenTelemetry SDK, and in-memory span exporter.
- edge_cases_or_failure_modes: Provider rejection must both throw and end an error span; handoff tool choice must be `none`.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-432 `file` `packages/ai/test/alibaba-endpoint-selection.test.ts`
- cursor: `[_]`
- core_role: Login and API-key endpoint selection tests for Alibaba coding plan.
- algorithmic_behavior: Exercises international, China mainland, and custom endpoint choices, validates API keys against selected base URLs, handles menu cancellation, and parses JSON/Bearer/plain API keys.
- inputs_outputs_state: Inputs are mocked auth prompts, custom URL/key strings, and stored JSON payloads. Outputs are OAuth-like credential objects with access/refresh/enterpriseUrl and parsed apiKey/baseUrl.
- gates_or_invariants: Custom option requires custom URL; empty API key rejected; China and international console URLs/instructions differ.
- dependencies_and_callers: Depends on Alibaba login module, provider auth validation, and credential parser.
- edge_cases_or_failure_modes: Malformed JSON or missing endpoint falls back to plain/bearer behavior; cancellation throws “Login cancelled”.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-462 `file` `packages/ai/test/auth-gateway-anthropic-to-codex-caching.test.ts`
- cursor: `[_]`
- core_role: End-to-end cache behavior test for Anthropic-shaped auth gateway calls routed to Codex model backend.
- algorithmic_behavior: Sends two Anthropic Messages API calls through a gateway, extracts assistant text, and asserts second turn reports prompt cache read tokens for repeated large system content.
- inputs_outputs_state: Inputs are gateway availability, token, model, long system prompt, and request bodies. Outputs are Anthropic-style responses and usage cache counters.
- gates_or_invariants: Skips unless gateway E2E is available; first turn should not have cache read; second repeated turn should.
- dependencies_and_callers: Depends on auth gateway, Codex backend, live credentials/env, and Anthropic compatibility surface.
- edge_cases_or_failure_modes: Live service variation can affect usage counters; test guards by availability check.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-492 `file` `packages/ai/test/claude-ratelimit-headers.test.ts`
- cursor: `[_]`
- core_role: Header parser tests for Anthropic/Claude rate-limit usage reports.
- algorithmic_behavior: Parses unified status headers into provider usage reports with 5-hour and 7-day windows, reset timestamps, used counts, fractions, and shared scopes.
- inputs_outputs_state: Inputs are synthetic response header maps and a fixed `NOW`. Outputs are `UsageReport` and `UsageLimit` objects or null.
- gates_or_invariants: Allowed status without limit headers returns null; reset/limit/remaining arithmetic must produce stable used fractions.
- dependencies_and_callers: Depends on Anthropic provider rate-limit parser and usage-report types.
- edge_cases_or_failure_modes: Missing tier stays undefined; only present windows appear.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-522 `file` `packages/ai/test/google-thinking-signature.test.ts`
- cursor: `[_]`
- core_role: Tests Google thinking-part detection and signature carry-forward.
- algorithmic_behavior: Verifies `isThinkingPart` requires `thought: true`, not merely `thoughtSignature`, and that signature extraction retains prior signature until a newer thinking signature appears.
- inputs_outputs_state: Inputs are Google content parts with `thought` and `thoughtSignature`. Outputs are booleans and selected signature string.
- gates_or_invariants: Signature-only parts are not thinking; empty/false thought is ignored.
- dependencies_and_callers: Depends on Google provider message conversion helpers.
- edge_cases_or_failure_modes: Misclassifying signature-only parts can leak or replay hidden thinking incorrectly.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-552 `file` `packages/ai/test/issue-957-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Kimi OAuth refresh and persisted credential update.
- algorithmic_behavior: Mocks refresh token HTTP flow, validates grant fields, computes expiry from issue time, and ensures provider auth resolution refreshes stored expired OAuth credentials once.
- inputs_outputs_state: Inputs are stored OAuth credentials, refresh responses, Kimi headers, and credential manager stubs. Outputs are refreshed access/refresh/expires and updated stored credential.
- gates_or_invariants: Refresh uses `grant_type=refresh_token`; returned access token is used as API key; store writes exactly one refreshed credential.
- dependencies_and_callers: Depends on Kimi auth refresh code and provider credential resolution.
- edge_cases_or_failure_modes: Expired stored token must refresh before API use; stale refresh token update must persist.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-582 `file` `packages/ai/test/openai-completions-compat.test.ts`
- cursor: `[_]`
- core_role: Broad compatibility regression suite for OpenAI-compatible chat completions provider.
- algorithmic_behavior: Captures request payloads and mock SSE responses to verify message serialization, system/developer role policy, usage fallback, reasoning formats, tool-call replay, forced tool downgrades, OpenRouter variants, Anthropic cache markers, Moonshot schema normalization, and DeepSeek token stripping.
- inputs_outputs_state: Inputs are model specs/compat flags, messages with text/thinking/tool/image content, tool schemas, mock streaming chunks, and request options. Outputs are provider responses, payload JSON, event streams, usage, stop reasons, and content blocks.
- gates_or_invariants: Host-specific compat gates decide multi-system support, developer role, `reasoning_content`, Z.AI effort mapping, Ollama empty-length error mapping, and MFJS schema conversion.
- dependencies_and_callers: Depends on `openai-completions.ts`, catalog compat detection, tool schema utilities, OpenRouter routing, and model specs.
- edge_cases_or_failure_modes: Partial special tokens split across chunks are buffered; unsupported forced tool choices must not suppress thinking; Kimi/Moonshot/opencode cases diverge.
- validation_or_tests: This file is validation and covers many provider edge cases.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-612 `file` `packages/ai/test/pre-response-timeout.test.ts`
- cursor: `[_]`
- core_role: Tests pre-response timeout abort-signal composition.
- algorithmic_behavior: Verifies no-op behavior for undefined/nonpositive timeout, timeout-created DOMException-like reason, and caller abort precedence when caller signal aborts first.
- inputs_outputs_state: Inputs are caller `AbortSignal`, timeout values, and fake timers. Outputs are returned signal and abort reason.
- gates_or_invariants: Existing caller signal is returned unchanged when timeout disabled; caller cancellation message dominates local timeout if fired first.
- dependencies_and_callers: Depends on `armPreResponseTimeout`/abort utilities used by providers.
- edge_cases_or_failure_modes: Incorrect signal racing can surface timeout when user cancelled, confusing error handling.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-642 `file` `packages/ai/test/total-tokens.test.ts`
- cursor: `[_]`
- core_role: Cross-provider usage accounting tests for `totalTokens` and cache token components.
- algorithmic_behavior: Runs live or availability-gated provider calls, repeats cacheable prompts, logs usage, and asserts `totalTokens` equals input plus output plus cache components across providers.
- inputs_outputs_state: Inputs are OAuth/API tokens, model specs, long system prompts, and provider options. Outputs are usage records with input/output/cacheRead/cacheWrite/totalTokens.
- gates_or_invariants: Total token arithmetic must equal component sum; cache-enabled providers should show cache behavior on repeated calls.
- dependencies_and_callers: Depends on provider implementations, token availability helpers, and live model backends.
- edge_cases_or_failure_modes: Provider-specific usage fields vary; tests are gated/skipped when credentials unavailable.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-672 `file` `packages/catalog/test/build.test.ts`
- cursor: `[_]`
- core_role: Catalog model-building and compat detection regression suite.
- algorithmic_behavior: Builds models from specs, resolves OpenAI/OpenRouter compat, tests sparse overrides, `whenThinking`, name cleanup, xAI effort suppression, provider-keyed wire quirks, OpenRouter discovery/cache behavior, and official Anthropic URL detection.
- inputs_outputs_state: Inputs are synthetic `ModelSpec` objects, bundled models, cache rows, and mocked discovery responses. Outputs are resolved `Model` objects and persisted sparse specs.
- gates_or_invariants: Sparse compat overrides win; derived compat fields are rebuilt on cache read; OpenRouter pseudo-API stays OpenRouter; lookalike Anthropic hosts rejected.
- dependencies_and_callers: Depends on catalog build/resolver modules, cache, OpenRouter discovery, and URL detection helpers.
- edge_cases_or_failure_modes: Legacy OpenRouter cache rows ignored; variant tags preserved if they map to distinct wire IDs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-702 `file` `packages/catalog/test/ollama-cloud-output-caps.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Ollama Cloud max-output caps and error surfacing.
- algorithmic_behavior: Ensures discovered Ollama Cloud models use safe defaults, chat requests omit `num_predict` when model opts out, disabled reasoning sends `think: false`, and HTTP 400 bodies surface in provider errors.
- inputs_outputs_state: Inputs are NDJSON discovery responses, model specs, request messages, and mocked fetch responses. Outputs are catalog models, request bodies, and provider error responses.
- gates_or_invariants: Ollama Cloud `maxTokens` must not inherit unsafe cross-provider values; 400 error text must include response body.
- dependencies_and_callers: Depends on catalog discovery and Ollama chat provider.
- edge_cases_or_failure_modes: Unsafe `num_predict` can exceed hosted caps; reasoning opt-out must still send explicit false.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-732 `file` `packages/coding-agent/src/startup-splash.ts`
- cursor: `[_]`
- core_role: Startup splash display gate.
- algorithmic_behavior: `shouldShowStartupSplash` returns true only when configured and interactive, not resuming, not quiet, not timing, and both stdin/stdout are TTYs.
- inputs_outputs_state: Inputs are config booleans and process stdio flags. Output is a boolean.
- gates_or_invariants: Any noninteractive, quiet, resume, or timing condition disables splash.
- dependencies_and_callers: Called by CLI startup UI.
- edge_cases_or_failure_modes: Incorrect TTY detection can show splash in pipes or suppress it in interactive use.
- validation_or_tests: Covered indirectly by welcome/startup behavior tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-762 `file` `packages/coding-agent/test/agent-session-eager-task.test.ts`
- cursor: `[_]`
- core_role: Tests eager task prelude injection in `AgentSession`.
- algorithmic_behavior: Harness records provider calls and asserts hidden developer reminders are prepended only for eligible first main-session prompts, with no forced task choice unless todo is also eager.
- inputs_outputs_state: Inputs are session config, prompt text, agent id, subagent/main state, and task/todo eager flags. Outputs are observed message roles/text and tool choice.
- gates_or_invariants: Skip on question/exclamation prompts, subsequent turns, disabled/preferred-only eager mode, and subagents; preserve forced todo choice when both eager.
- dependencies_and_callers: Depends on `AgentSession`, task/delegation prompt handling, model provider mock.
- edge_cases_or_failure_modes: Reminder must not repeat user prompt or include batch guidance when task batching disabled.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-792 `file` `packages/coding-agent/test/append-only-context-mode.test.ts`
- cursor: `[_]`
- core_role: Tests automatic append-only context mode selection.
- algorithmic_behavior: Asserts explicit `on`/`off` override, DeepSeek-like auto-enable, Xiaomi token-plan Anthropic auto-enable, and generic proxy auto-disable.
- inputs_outputs_state: Inputs are mode strings and provider/baseUrl descriptors. Output is boolean enablement.
- gates_or_invariants: Explicit settings dominate auto; auto depends on provider/baseUrl classification.
- dependencies_and_callers: Depends on context mode helper used by provider/session setup.
- edge_cases_or_failure_modes: Misclassifying proxy hosts can send incompatible mutable context to append-only backends.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-822 `file` `packages/coding-agent/test/cli-unknown-flag.test.ts`
- cursor: `[_]`
- core_role: CLI parser regression tests for unknown flag tracking and error reporting.
- algorithmic_behavior: Parses unknown long/short flags, `--flag=value`, typo in known flag, stdin marker `-`, POSIX `--`, extension-aware reparsing, and error output formatting.
- inputs_outputs_state: Inputs are argv arrays and extension flag maps. Outputs are parsed options, `unrecognizedFlags`, messages, file args, and stderr text.
- gates_or_invariants: Tokens after `--` are positional and not file-expanded; extension-registered flags are removed on reparse; genuine typos remain reportable.
- dependencies_and_callers: Depends on CLI argument parser and `reportUnrecognizedFlags`.
- edge_cases_or_failure_modes: Unknown flag values must not leak into positional messages; singular/plural error wording differs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-852 `file` `packages/coding-agent/test/export-subsessions.test.ts`
- cursor: `[_]`
- core_role: Tests sub-session export collection from JSONL session files.
- algorithmic_behavior: Creates main/subsession JSONL fixtures, discovers child sessions, builds parent/agent path keys, carries headers and leaf ids, and ignores malformed/missing files.
- inputs_outputs_state: Inputs are temp session files and JSONL entries. Outputs are a map of collected sub-sessions.
- gates_or_invariants: Parent hierarchy must produce names like `Alpha/Child`; bad files are skipped safely.
- dependencies_and_callers: Depends on session export/share code.
- edge_cases_or_failure_modes: Malformed subsession must not abort entire export.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-882 `file` `packages/coding-agent/test/image-input.test.ts`
- cursor: `[_]`
- core_role: Image metadata parser tests for PNG/JPEG prompt inputs.
- algorithmic_behavior: Reads tiny fixture image bytes, detects MIME, dimensions, channel count, alpha presence, and rejects non-image data.
- inputs_outputs_state: Inputs are binary image buffers. Outputs are metadata object or null.
- gates_or_invariants: PNG alpha reports 4 channels/hasAlpha true; JPEG reports 3/no alpha.
- dependencies_and_callers: Depends on image metadata reader used for image inputs.
- edge_cases_or_failure_modes: Invalid data returns null instead of throwing.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-912 `file` `packages/coding-agent/test/issue-1528-discovery-default-max-tokens.test.ts`
- cursor: `[_]`
- core_role: Regression tests for discovered model default `maxTokens`.
- algorithmic_behavior: Mocks provider discovery for OpenAI-compatible/Anthropic-like providers and asserts safe default output caps when discovery omits caps.
- inputs_outputs_state: Inputs are mocked discovery responses and provider descriptors. Outputs are catalog model entries with `api` and `maxTokens`.
- gates_or_invariants: OpenAI-compatible defaults can be 32768 while Anthropic defaults to 8192 depending API classification.
- dependencies_and_callers: Depends on coding-agent discovery integration and catalog model construction.
- edge_cases_or_failure_modes: Missing provider cap can otherwise produce unsafe or unlimited requests.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-942 `file` `packages/coding-agent/test/join-command.test.ts`
- cursor: `[_]`
- core_role: Tests top-level `join` command registration and argv resolution.
- algorithmic_behavior: Asserts `join` is a registered subcommand and resolves a collab URL arg into the expected subcommand invocation.
- inputs_outputs_state: Input is argv `["join", "<url>"]`; output is resolved command descriptor.
- gates_or_invariants: `join` must remain top-level, not parsed as prompt text.
- dependencies_and_callers: Depends on CLI command registry.
- edge_cases_or_failure_modes: Registration regression would make share/collab join inaccessible.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-972 `file` `packages/coding-agent/test/mcp-test-utils.ts`
- cursor: `[_]`
- core_role: Test helper for MCP transport/connection mocks.
- algorithmic_behavior: Exports `createMockTransport` and `createMockConnection` with spyable send/close/message hooks for MCP tests.
- inputs_outputs_state: Inputs are optional handlers and mock payloads. Outputs are mock transport/connection objects.
- gates_or_invariants: Helpers simulate MCP bidirectional message delivery without real process/network.
- dependencies_and_callers: Used by MCP-related test files.
- edge_cases_or_failure_modes: Helper only approximates transport lifecycle; not a production path.
- validation_or_tests: Indirectly validated by tests using it.
- skip_candidate: `yes: test utility, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1002 `file` `packages/coding-agent/test/plugin-install-validation.test.ts`
- cursor: `[_]`
- core_role: Plugin installation rollback and manifest validation tests.
- algorithmic_behavior: Creates fake plugin package trees, mocks `bun install`, then verifies failed extension dependency or missing manifest entries reject install and restore prior package/lock/node_modules state.
- inputs_outputs_state: Inputs are temp plugin roots, fixture manifests, package specs, and mocked install results. Outputs are thrown errors and restored package/lock files.
- gates_or_invariants: Install validation must run after dependency install; failing validation must remove new broken package or restore old version/ref.
- dependencies_and_callers: Depends on `PluginManager.install`, plugin loader manifest resolution, and package tree helpers.
- edge_cases_or_failure_modes: Git ref reinstall failure must restore previous git plugin lock and extension body.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1032 `file` `packages/coding-agent/test/sdk-custom-tools-per-session-binding.test.ts`
- cursor: `[_]`
- core_role: Regression tests for per-session SDK custom tool binding.
- algorithmic_behavior: Loads the same custom tool for parent and subagent sessions and asserts each receives a distinct API object/cwd and separate tool instance.
- inputs_outputs_state: Inputs are fake sessions and custom tool loaders. Outputs are loaded tool arrays, errors, API cwd observations, and call logs.
- gates_or_invariants: Subagent API must not reuse parent session binding; tool instances must be independent.
- dependencies_and_callers: Depends on custom tool loader and SDK session API wiring.
- edge_cases_or_failure_modes: Shared binding would execute subagent tools in parent cwd/session.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1062 `file` `packages/coding-agent/test/share.test.ts`
- cursor: `[_]`
- core_role: Tests encrypted share snapshot creation, trimming, image omission, secret redaction, and URL normalization.
- algorithmic_behavior: Generates AES keys, seals session data under server byte budget, trims oversized text while preserving entries, replaces inline images, obfuscates secrets in snapshots, and normalizes share server URLs.
- inputs_outputs_state: Inputs are session entries, leaf id, key, byte budget, image blocks, and server URL strings. Outputs are sealed bytes, truncation flag, decrypted snapshot, and normalized URLs.
- gates_or_invariants: Under-budget data round-trips; over-budget text gets truncation marker; original entries/plain data remain unmodified after redaction.
- dependencies_and_callers: Depends on share sealing/snapshot utilities and WebCrypto.
- edge_cases_or_failure_modes: Large inline images must be omitted before text trimming to fit budget.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1092 `file` `packages/coding-agent/test/system-prompt-inventory.test.ts`
- cursor: `[_]`
- core_role: Tests system prompt tool/skill inventory rendering.
- algorithmic_behavior: Renders prompt inventory in compact or detailed modes, checks tool names/descriptions, skill instruction text, and section ordering relative to IO/exploration guidance.
- inputs_outputs_state: Inputs are mock tool metadata, empty tree, and skill metadata. Outputs are rendered system prompt text.
- gates_or_invariants: Compact mode lists tools without full docs; detailed mode includes tool sections; skill inventory must appear after core guidance.
- dependencies_and_callers: Depends on system prompt renderer and tool inventory metadata.
- edge_cases_or_failure_modes: Prompt ordering affects model instruction priority.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1122 `file` `packages/coding-agent/test/welcome-tip.test.ts`
- cursor: `[_]`
- core_role: Tests welcome tip wrapping and width constraints.
- algorithmic_behavior: Renders a long tip to a narrow box, strips ANSI, and asserts wrapped lines keep prefix/indent and visible width budget.
- inputs_outputs_state: Input is tip text and width. Output is rendered lines.
- gates_or_invariants: No ellipsis truncation; continuation lines are indented and width-bounded.
- dependencies_and_callers: Depends on `renderWelcomeTip` in welcome component.
- edge_cases_or_failure_modes: Terminal width overflow degrades startup UI.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1152 `file` `packages/hashline/src/normalize.ts`
- cursor: `[_]`
- core_role: Text normalization helpers for hashline/edit workflows.
- algorithmic_behavior: Detects first line-ending style, normalizes CRLF/CR to LF, restores LF to CRLF if original style required, and strips UTF-8 BOM while reporting it.
- inputs_outputs_state: Inputs are file text strings. Outputs are normalized/restored text and BOM metadata.
- gates_or_invariants: Preserve original line-ending style when writing back; BOM handling is explicit.
- dependencies_and_callers: Used by hashline diff/edit modules.
- edge_cases_or_failure_modes: Mixed line endings follow first detected style; BOM must not pollute hash/diff matching.
- validation_or_tests: Covered indirectly by hashline edit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1182 `file` `packages/mnemopi/test/beam-e3-e4-e6.test.ts`
- cursor: `[_]`
- core_role: Integration tests for Beam memory consolidation, annotation migration, and recall dedupe.
- algorithmic_behavior: Seeds old working memories and legacy triples, runs sleep/dry-run/migration/recall flows, and verifies episodic/working state transitions, `consolidated_at`, backup creation, and recall attribution.
- inputs_outputs_state: Inputs are temp SQLite DBs, seeded working rows, timestamps, annotation triples, and recall queries. Outputs are DB row counts, logs, annotations, backup file, and recall results.
- gates_or_invariants: Sleep is additive and idempotent; dry-run must not mutate state; legacy migration runs once; cross-tier recall dedupes paired source/summary memories.
- dependencies_and_callers: Depends on `BeamMemory`, SQLite schema/migrations, annotations, and recall.
- edge_cases_or_failure_modes: Migration must not duplicate annotations; recall_count should not attribute to duplicate tiers.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1212 `file` `packages/mnemopi/test/issue-1832-embedding-population.test.ts`
- cursor: `[_]`
- core_role: Regression tests for embedding population and dense recall in mnemopi.
- algorithmic_behavior: Uses fake embedding provider to test remember, batch remember, recall auto-query embedding, explicit FTS-only `queryEmbedding: null`, content update re-embedding, episodic consolidation embedding, close-time flush, and provider-scoped query cache.
- inputs_outputs_state: Inputs are memory contents and fake provider vectors. Outputs are `memory_embeddings` rows, dense scores, provider call counts, and recall results.
- gates_or_invariants: `undefined` query embedding auto-derives; explicit null disables dense scoring; provider caches must not cross-contaminate runtimes.
- dependencies_and_callers: Depends on `Mnemopi`, `BeamMemory`, embedding runtime options, SQLite.
- edge_cases_or_failure_modes: Short-lived CLI owners must flush pending embeddings before close; model/provider changes require correct cache isolation.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1242 `file` `packages/mnemopi/test/typed-memory-aaak.test.ts`
- cursor: `[_]`
- core_role: Tests typed memory classification and AAAK text compression.
- algorithmic_behavior: Verifies pattern-based memory type classification, confidence/defaults, priority/decay/consolidation policy, contextual confidence boosts, tie-breaks, and encoding maps/replacements.
- inputs_outputs_state: Inputs are memory text snippets. Outputs are memory type, confidence, pattern id, priority, decay, and encoded strings.
- gates_or_invariants: Empty input returns unknown/zero-like classification; priority and consolidation differ by type; AAAK encoding should be idempotent for already encoded values.
- dependencies_and_callers: Depends on mnemopi memory type classifier and AAAK encoder.
- edge_cases_or_failure_modes: Tie-break can change persistence priority; text replacements can over-compress if not ordered.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1272 `file` `packages/snapcompact/research/diag_kimi_probe.py`
- cursor: `[_]`
- core_role: Research diagnostic script for probing Kimi/model image token behavior.
- algorithmic_behavior: Enumerates frame files, builds image content blocks, calls chat route/model endpoints, probes model list, token growth across image counts/sizes, and last-line behavior.
- inputs_outputs_state: Inputs are image frames, route URL, model id, API key/env, count list, and image pixel size. Outputs are printed model/token/response diagnostics.
- gates_or_invariants: Requires available frames/API; image blocks are base64 data URLs.
- dependencies_and_callers: Depends on Python HTTP client stack, local research frame assets, model API.
- edge_cases_or_failure_modes: Large image counts can exceed request/token limits; missing frames abort probe usefulness.
- validation_or_tests: No tests; research-only.
- skip_candidate: `yes: exploratory research script, not product runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1302 `file` `packages/snapcompact/research/run.py`
- cursor: `[_]`
- core_role: Snapcompact research experiment runner and aggregator.
- algorithmic_behavior: Locates agent prompts, loads prompt conditions, caches completions by hash, runs chunked experiments, parses condition names, records model outputs/usages, and aggregates cost/quality metrics.
- inputs_outputs_state: Inputs are prompt files, condition definitions, API key/model, chunks, and cache/fresh options. Outputs are JSON records, cache files, aggregate summaries, and printed metrics.
- gates_or_invariants: Cache key includes prompt/model/messages; aggregation computes token/cost totals from price parameters.
- dependencies_and_callers: Depends on OpenAI-compatible API, local prompt tree, filesystem cache, CLI args.
- edge_cases_or_failure_modes: Cache collision would corrupt results; parse failures or missing prompts stop experiment.
- validation_or_tests: No direct tests; research harness.
- skip_candidate: `yes: offline experiment runner`

### OH_MY_HUMANIZE_MAIN-HZ-1332 `file` `packages/snapcompact/research/snapcompact_viz_city.py`
- cursor: `[_]`
- core_role: Research visualization script rendering snapcompact summary as an isometric city image.
- algorithmic_behavior: Defines font/color helpers, isometric coordinate transforms, diamond/building drawing, district rendering, legend drawing, and final image export.
- inputs_outputs_state: Inputs are summary data and scale/font availability. Output is a generated bitmap visualization.
- gates_or_invariants: Color channels are clamped; geometry derives from tile size and height.
- dependencies_and_callers: Depends on PIL/Pillow and local summary JSON.
- edge_cases_or_failure_modes: Missing fonts fall back; extreme values can compress/overflow visual layout.
- validation_or_tests: No tests; research visualization.
- skip_candidate: `yes: visualization/research artifact, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1362 `file` `packages/swarm-extension/src/extension.ts`
- cursor: `[_]`
- core_role: Extension entrypoint adding swarm run/status commands to the extension API.
- algorithmic_behavior: Registers commands, loads YAML swarm specs, executes swarm agents, reports status, and builds summary messages for results/errors.
- inputs_outputs_state: Inputs are command context, YAML path/name, extension API, and swarm execution state. Outputs are command responses/messages and status summaries.
- gates_or_invariants: `handleRun` requires a valid YAML path/spec; status can target name or list overall state.
- dependencies_and_callers: Depends on extension API, swarm executor/spec parser, and command context messaging.
- edge_cases_or_failure_modes: Missing/malformed YAML or executor failure must report cleanly through extension command surface.
- validation_or_tests: `packages/swarm-extension/src/swarm/__tests__/executor.test.ts` covers executor integration detail.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1392 `file` `packages/tui/test/component-render.test.ts`
- cursor: `[_]`
- core_role: Tests partial component re-rendering in TUI differential renderer.
- algorithmic_behavior: Builds counting components and virtual terminal, requests component renders, and verifies subtree-only render, full-compose downgrade, overlay fallback, child-list-change fallback, missing-component fallback, and live region replay.
- inputs_outputs_state: Inputs are component tree mutations, render requests, overlay state, and virtual terminal width. Outputs are visible rows and render counts.
- gates_or_invariants: Partial frame cannot run if root structure changed, overlay active, or component missing; skipped live-region reports must replay across partial frames.
- dependencies_and_callers: Depends on TUI renderer, component API, virtual terminal.
- edge_cases_or_failure_modes: Partial rendering bugs can duplicate/miss rows or stale transcript content.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1422 `file` `packages/tui/test/loader.test.ts`
- cursor: `[_]`
- core_role: Tests animated loader rendering cadence and cleanup.
- algorithmic_behavior: Verifies width clamping, spinner cadence under 30fps animated messages, skip of unchanged frames, render request only on message byte changes or spinner advance, and dispose idempotency.
- inputs_outputs_state: Inputs are loader messages, fake UI render request spy, timers, and widths. Outputs are rendered lines and render request counts.
- gates_or_invariants: Visible width must not exceed terminal budget; disposed loader schedules no more renders.
- dependencies_and_callers: Depends on loader component and timer/render scheduler.
- edge_cases_or_failure_modes: High-frequency animation can over-render or leak timers.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1452 `file` `packages/tui/test/start-listener.test.ts`
- cursor: `[_]`
- core_role: Tests TUI start listener hook execution.
- algorithmic_behavior: Registers start listener, starts/restarts TUI, and asserts listener count increments on each start.
- inputs_outputs_state: Inputs are listener registration and start calls. Output is counter state.
- gates_or_invariants: Hooks fire both initial start and restart.
- dependencies_and_callers: Depends on TUI lifecycle API.
- edge_cases_or_failure_modes: Missed restart hook can leave components uninitialized.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1482 `file` `packages/utils/src/async.ts`
- cursor: `[_]`
- core_role: Shared timeout/abort promise utility.
- algorithmic_behavior: `withTimeout` races a promise against a timer and optional abort signal using `Promise.withResolvers`, rejects immediately if signal already aborted, and cleans timeout/listeners.
- inputs_outputs_state: Inputs are promise, milliseconds, optional signal/error factory. Output is resolved promise value or rejection.
- gates_or_invariants: Cleanup always clears timer and abort listener; abort reason/timeouts surface through rejection.
- dependencies_and_callers: Used by async operations needing bounded waits.
- edge_cases_or_failure_modes: Promise still runs after timeout; utility only controls returned race.
- validation_or_tests: Covered indirectly by timeout users.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1512 `file` `packages/utils/src/timing-buffer.ts`
- cursor: `[_]`
- core_role: Global module-load timing event buffer.
- algorithmic_behavior: Stores/retrieves a process-global buffer on a symbol key and drains accumulated module load events atomically by returning current entries and clearing the array.
- inputs_outputs_state: Inputs are module timing events pushed by instrumentation. Outputs are event arrays from `drainModuleLoadEvents`.
- gates_or_invariants: Reuses existing global buffer across module copies; drain clears state.
- dependencies_and_callers: Used by timing diagnostics and launcher preload paths.
- edge_cases_or_failure_modes: Multiple module instances share global symbol; events after drain remain for next drain.
- validation_or_tests: Indirectly through timing features.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1542 `file` `python/omp-rpc/tests/test_client.py`
- cursor: `[_]`
- core_role: Python `omp_rpc` client integration tests with a fake JSON-RPC server.
- algorithmic_behavior: Tests command builder options, get_state/bash, prompt-and-wait assistant text, custom tool registration/execution, extension UI round trips, headless UI cancellation, typed listeners, todos/model/session/message/control commands, event retention, id-less error correlation, late prompt failure, bounded stderr, startup frame errors, stop unblocking, and process-group termination.
- inputs_outputs_state: Inputs are fake server frames, client commands, custom tools, listener callbacks, and subprocess fixtures. Outputs are client return values, events, raised errors, and killed processes.
- gates_or_invariants: Prompt lifecycle collectors are single-flight; listener mutation must not alter retained turns; stop must unblock waiters and kill grandchildren.
- dependencies_and_callers: Depends on `omp_rpc.RpcClient`, subprocess/server fixture, threading/conditions.
- edge_cases_or_failure_modes: Broken startup frames and id-less errors must surface deterministically; listener exceptions should report without stopping client.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1572 `file` `python/robomp/src/worker.py`
- cursor: `[_]`
- core_role: Per-task robomp worker driver that runs coding-agent via RPC for issue/PR automation.
- algorithmic_behavior: Builds prompts for triage, PR review, comments, and review comments; stages agent HOME; scrubs secrets from child env; picks model/thinking with pragmas; resumes prior sessions; seeds todos; runs `RpcClient.prompt_and_wait`; sends completion/dirty reminders; handles cancellation/hard timeout; captures natives cache after success.
- inputs_outputs_state: Inputs are `TaskInputs`, task kind, GitHub issue/PR/comment data, directive pragmas, settings, workspace, DB, and cancellation hooks. Outputs are final assistant text, DB model event, logs, tool calls, PR/issue side effects through host tools, and optional natives cache.
- gates_or_invariants: Sensitive env vars are overwritten; terminal tools determine completion; failed/aborted tasks never capture cache; hard timeout cancels RPC; abort tool is treated as clean exit.
- dependencies_and_callers: Depends on `omp_rpc`, robomp persona, host tools, GitHub backend, workspace sandbox, DB, natives cache.
- edge_cases_or_failure_modes: Workaround private `_mark_closed` after stop prevents prompt wait hang; workspace dirty probe failures are swallowed to avoid infinite reminders.
- validation_or_tests: Covered by robomp integration tests and `omp-rpc` client tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1602 `directory` `packages/catalog/src/discovery/cursor-gen`
- cursor: `[_]`
- core_role: Generated protobuf schema bindings for Cursor HTTP/2 model/tool/service discovery.
- algorithmic_behavior: Contains generated `agent_pb.ts` with hundreds of `agent.v1` message schemas, enums, and services including model/tool call records, web search/write/file/exec types, `AgentService`, control services, and frame types.
- inputs_outputs_state: Inputs are serialized protobuf bytes from Cursor-compatible services; outputs are typed encode/decode descriptors used by discovery/client code.
- gates_or_invariants: Generated descriptors must match upstream proto field numbers and oneof layouts; consumers rely on stable schema names.
- dependencies_and_callers: Used by `packages/catalog/src/discovery/cursor.ts`; generated by protobuf tooling.
- edge_cases_or_failure_modes: Manual edits or schema drift can make discovery decode wrong fields silently.
- validation_or_tests: Cursor discovery tests validate consumer behavior, not every generated type.
- skip_candidate: `yes: generated binding, but required by core Cursor discovery`

### OH_MY_HUMANIZE_MAIN-HZ-1632 `directory` `packages/coding-agent/src/modes/components`
- cursor: `[_]`
- core_role: TUI component library for coding-agent interactive modes.
- algorithmic_behavior: Recursively contains assistant/user message renderers, bash execution renderer, browser/task/search/tool result renderers, model selector, welcome screen, status line, markdown/mermaid display, selectors, overlays, tips, and component tests.
- inputs_outputs_state: Inputs are session messages, tool call/result streams, UI state, theme, terminal dimensions, model catalog, and user key events. Outputs are ANSI line arrays, partial render requests, selection callbacks, and UI state updates.
- gates_or_invariants: Render paths must sanitize/truncate raw tool output, preserve streaming preview consistency, and obey terminal width.
- dependencies_and_callers: Used by coding-agent TUI modes; depends on `packages/tui`, theme, render utilities, model catalog, tool renderers.
- edge_cases_or_failure_modes: Streaming and rebuilt transcript paths can diverge; nested/large outputs can overflow; stale model/provider data can mis-rank selector items.
- validation_or_tests: Component-specific tests cover assistant mermaid, user selector, bash/search/task render shapes, welcome tip, token rate, and TUI renderer behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1662 `directory` `packages/swarm-extension/src/swarm/__tests__`
- cursor: `[_]`
- core_role: Swarm executor regression tests.
- algorithmic_behavior: `executor.test.ts` ensures `executeSwarmAgent` omits `authStorage` when a `modelRegistry` is supplied to `runSubprocess`.
- inputs_outputs_state: Inputs are mocked swarm agent config and execution dependencies. Output is observed subprocess call args.
- gates_or_invariants: Explicit registry must prevent auth storage passthrough.
- dependencies_and_callers: Depends on swarm executor and subprocess runner mock.
- edge_cases_or_failure_modes: Passing both registry and auth storage can select wrong auth path.
- validation_or_tests: This directory is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1692 `file` `packages/ai/src/auth-broker/snapshot-cache.ts`
- cursor: `[_]`
- core_role: Encrypted snapshot cache for auth broker credentials/state.
- algorithmic_behavior: Uses AES-GCM with magic `OMPS`, version byte, 12-byte IV, SHA-256 token-derived key, and URL as additional authenticated data. Reads TTL-bound cached JSON after shape validation; writes atomically via temp `wx` file, chmod 600, rename, cleanup.
- inputs_outputs_state: Inputs are cache path, token, URL, TTL, and snapshot payload. Outputs are cached snapshot or null, and encrypted cache file.
- gates_or_invariants: TTL <= 0 disables reads; ENOENT returns null; decrypt/parse/shape failures log debug and return null; server URL binds ciphertext.
- dependencies_and_callers: Depends on WebCrypto, Bun file IO, node fs/path, logger; used by auth broker snapshot refresh.
- edge_cases_or_failure_modes: Token or URL mismatch makes cache undecryptable; interrupted write leaves tmp file removed best-effort.
- validation_or_tests: Covered by auth-broker cache tests if present; behavior is defensive.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1722 `file` `packages/ai/src/providers/amazon-bedrock.ts`
- cursor: `[_]`
- core_role: Amazon Bedrock Converse Stream provider implementation.
- algorithmic_behavior: Builds ConverseStream requests, resolves bearer or SigV4 auth, streams AWS eventstream frames, converts text/tool/reasoning blocks, handles tool JSON deltas, maps metadata usage/cost, applies prompt caching, thinking budgets, and message/tool config conversion.
- inputs_outputs_state: Inputs are model, messages, tools, provider options, credentials/env, abort signal. Outputs are streamed assistant blocks, usage, stop reason/error, and request diagnostics on some failures.
- gates_or_invariants: Invalid AWS credentials invalidate cache on 401/403; text blocks can start on delta; forced tool disables thinking; unknown image MIME throws.
- dependencies_and_callers: Depends on AWS signing helpers, eventstream decoder, model catalog, provider streaming abstractions.
- edge_cases_or_failure_modes: Thinking signature failures append diagnostics; 400 errors can include raw request dump; tool choice `none` with historical tool blocks keeps tools but omits choice.
- validation_or_tests: Provider behavior covered by AI integration/unit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1752 `file` `packages/ai/src/providers/openai-completions.ts`
- cursor: `[_]`
- core_role: OpenAI-compatible chat completions provider with broad host compatibility.
- algorithmic_behavior: Resolves wire model IDs, builds request params, converts messages/tools, streams SSE chunks, manages text/thinking/tool-call block lifecycles, merges tool args safely, tracks first-event/progress timeouts, retries strict-tool failures, parses usage/cost, maps stop reasons, and handles host-specific compat flags.
- inputs_outputs_state: Inputs are model spec/compat, context messages, tools, sampling/thinking options, fetch impl, abort signal. Outputs are provider stream events, final assistant content, usage, stop reason/error, and telemetry.
- gates_or_invariants: Role-only/keepalive chunks are not progress; strict tool mode disabled per scope on rejection; prototype keys ignored in object arg merge; usage-only after finish can still update usage.
- dependencies_and_callers: Depends on catalog compat, schema adapters, abort utilities, provider common types, fetch/SSE parser.
- edge_cases_or_failure_modes: DeepSeek special tokens may split across chunks; Ollama empty length can be context error; Kimi/Moonshot/OpenRouter reasoning replay rules are highly provider-specific.
- validation_or_tests: Extensively covered by `openai-completions-compat.test.ts`, timeout, token, and provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1782 `file` `packages/ai/src/registry/google-vertex.ts`
- cursor: `[_]`
- core_role: Registry credential detector for Google Vertex provider.
- algorithmic_behavior: Returns configured env key metadata, otherwise checks cached Application Default Credentials file plus project/location env to display authenticated state.
- inputs_outputs_state: Inputs are env vars and ADC file presence. Output is registry auth display string/keys.
- gates_or_invariants: ADC check is cached; API key env takes precedence.
- dependencies_and_callers: Depends on fs/os path conventions and provider registry UI.
- edge_cases_or_failure_modes: Stale cached ADC presence can misrepresent auth until process restart.
- validation_or_tests: Covered indirectly by registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1812 `file` `packages/ai/src/registry/synthetic.ts`
- cursor: `[_]`
- core_role: Provider registry descriptor for Synthetic.
- algorithmic_behavior: Defines API-key login/validation behavior against a models endpoint and provider metadata.
- inputs_outputs_state: Inputs are API key/base URL. Outputs are validation result and provider availability metadata.
- gates_or_invariants: Validation requires models endpoint success.
- dependencies_and_callers: Consumed by provider registry/login flows.
- edge_cases_or_failure_modes: Endpoint shape changes can break validation.
- validation_or_tests: Registry/login tests cover provider descriptors indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1842 `file` `packages/ai/src/utils/abort.ts`
- cursor: `[_]`
- core_role: Abort-signal tracking and race helpers for providers.
- algorithmic_behavior: `createAbortSourceTracker` combines caller/local abort sources and reports caller intent over local watchdog when applicable; `raceWithSignal` races shared work against a signal and removes listeners.
- inputs_outputs_state: Inputs are caller signals, local abort controllers/reasons, and promises. Outputs are merged signal, source classification, or raced result/error.
- gates_or_invariants: Caller abort dominates if caller signal is aborted; local reason only surfaces when request signal reason matches local reason and caller did not abort.
- dependencies_and_callers: Used by provider request timeout/error classification.
- edge_cases_or_failure_modes: Shared promise continues after race rejection; helper does not cancel underlying work.
- validation_or_tests: `pre-response-timeout.test.ts` covers related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1872 `file` `packages/catalog/src/discovery/cursor.ts`
- cursor: `[_]`
- core_role: Cursor model discovery over HTTP/2 protobuf/Connect wire format.
- algorithmic_behavior: Builds `GetUsableModels` protobuf request, sends HTTP/2 request with bearer/client headers and timeout, decodes raw or Connect unary frames, parses model metadata resiliently, maps against bundled Cursor references, and normalizes specs sorted/deduped by id.
- inputs_outputs_state: Inputs are token, base URL, client version, reference models, and HTTP/2 response bytes. Outputs are `ModelSpec` array or null.
- gates_or_invariants: Non-2xx/timeout/decode failure returns null; compressed/truncated Connect frames rejected; unknown models get safe defaults.
- dependencies_and_callers: Depends on generated `cursor-gen/agent_pb.ts`, protobuf runtime, HTTP/2 client, arktype parsing, catalog references.
- edge_cases_or_failure_modes: Cursor schema drift can decode but omit fields; custom IDs/display aliases are normalized.
- validation_or_tests: Catalog discovery tests cover expected output caps and cache behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1902 `file` `packages/coding-agent/src/async/index.ts`
- cursor: `[_]`
- core_role: Barrel export for coding-agent async job manager.
- algorithmic_behavior: Re-exports `./job-manager`.
- inputs_outputs_state: No runtime state beyond module export surface.
- gates_or_invariants: Keeps import path stable.
- dependencies_and_callers: Used by modules importing async APIs via package-local barrel.
- edge_cases_or_failure_modes: Removing/renaming breaks import compatibility.
- validation_or_tests: Compile/type checks.
- skip_candidate: `yes: barrel only`

### OH_MY_HUMANIZE_MAIN-HZ-1932 `file` `packages/coding-agent/src/cli/agents-cli.ts`
- cursor: `[_]`
- core_role: CLI handler for installing/listing bundled agents.
- algorithmic_behavior: Resolves target directory scope (custom/user/project), rejects conflicting user+project options, serializes bundled agents as YAML frontmatter plus body, skips existing files unless force, and supports JSON or human output.
- inputs_outputs_state: Inputs are CLI flags, target dir, bundled agent definitions. Outputs are written agent files or JSON/human summaries.
- gates_or_invariants: User/project flags are mutually exclusive; existing files protected unless force.
- dependencies_and_callers: Called by `agents` command; depends on fs/path, bundled agents, YAML serialization.
- edge_cases_or_failure_modes: Custom path resolution and overwrite behavior can affect user config.
- validation_or_tests: Command tests likely cover registration/output; no direct file test observed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1962 `file` `packages/coding-agent/src/cli/tiny-models-cli.ts`
- cursor: `[_]`
- core_role: CLI for listing/downloading tiny local models.
- algorithmic_behavior: Resolves requested models (`default`, `all`, or explicit names), lists JSON/table output, downloads with optional TTY progress, aggregates failures, and shuts down tiny model client in finally.
- inputs_outputs_state: Inputs are CLI args, model names, JSON flag, TTY status. Outputs are progress lines, downloaded model files/cache state, JSON/list output, or thrown failure.
- gates_or_invariants: Any failed download makes command fail; progress bar only for TTY non-JSON mode.
- dependencies_and_callers: Depends on tiny model client/catalog and CLI command wrapper.
- edge_cases_or_failure_modes: Unknown model names or interrupted downloads must cleanly close client.
- validation_or_tests: Covered indirectly by smoke tests for tiny-model subprocess.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1992 `file` `packages/coding-agent/src/commands/read.ts`
- cursor: `[_]`
- core_role: Command wrapper for `omp read <path>`.
- algorithmic_behavior: Declares argument/examples for reading paths, selectors, URLs, internal docs, archives, and DBs; initializes theme then delegates to `runReadCommand`.
- inputs_outputs_state: Inputs are CLI path/selector args. Outputs are read command rendered content or errors.
- gates_or_invariants: Requires path arg through command schema; wrapper itself does not parse content.
- dependencies_and_callers: Depends on command registry, theme init, and read CLI implementation.
- edge_cases_or_failure_modes: Example/schema mismatch affects help/completion.
- validation_or_tests: Read command behavior covered elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2022 `file` `packages/coding-agent/src/config/model-roles.ts`
- cursor: `[_]`
- core_role: Model role metadata and role-id resolution.
- algorithmic_behavior: Defines built-in roles/default metadata and functions to enumerate known roles from built-ins, config cycle order, model roles, and model tags; resolves role info with user overrides and hidden/color/name settings.
- inputs_outputs_state: Inputs are user config, role assignments, model tags. Outputs are role id arrays and display metadata.
- gates_or_invariants: Built-in visible roles come first; hidden roles can be excluded; invalid/missing custom values fall back to muted defaults.
- dependencies_and_callers: Used by model selector, status display, and role assignment UI.
- edge_cases_or_failure_modes: Duplicate role IDs require stable first occurrence ordering.
- validation_or_tests: Model selector and role tests cover behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2052 `file` `packages/coding-agent/src/discovery/cline.ts`
- cursor: `[_]`
- core_role: Project rule discovery provider for `.clinerules`.
- algorithmic_behavior: Walks upward from cwd to find `.clinerules`, reads either a directory of markdown files via `loadFilesFromDir` or a single file, and registers a project-only rule provider with priority 40.
- inputs_outputs_state: Inputs are cwd and filesystem rules. Outputs are discovered rule content entries.
- gates_or_invariants: Project-only scope; missing files produce no rules; directory and file forms supported.
- dependencies_and_callers: Depends on discovery/rule provider framework and filesystem helpers.
- edge_cases_or_failure_modes: Malformed/unreadable files are handled by lower-level load helpers.
- validation_or_tests: Discovery tests cover rule/skill walk-up patterns.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2082 `file` `packages/coding-agent/src/eval/idle-timeout.ts`
- cursor: `[_]`
- core_role: Idle timeout monitor for evaluation/runtime operations.
- algorithmic_behavior: Class tracks activity timestamps, arms timers, resets on activity, and invokes timeout callback after idle duration while avoiding duplicate firing.
- inputs_outputs_state: Inputs are timeout duration and activity events. Outputs are callback invocation and timer state transitions.
- gates_or_invariants: Disposed/stopped monitor must not fire; activity extends deadline.
- dependencies_and_callers: Used by eval runtimes and long-running execution cells.
- edge_cases_or_failure_modes: Timer drift or missed cleanup can cancel active work or leak callbacks.
- validation_or_tests: Covered indirectly by eval timeout tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2112 `file` `packages/coding-agent/src/hindsight/index.ts`
- cursor: `[_]`
- core_role: Barrel export for hindsight modules.
- algorithmic_behavior: Re-exports backend, bank, client, config, content, mental-models, state, and transcript modules.
- inputs_outputs_state: No runtime state beyond module export surface.
- gates_or_invariants: Maintains stable import surface.
- dependencies_and_callers: Used by callers importing hindsight APIs from one path.
- edge_cases_or_failure_modes: Export ambiguity or removal breaks compile.
- validation_or_tests: Type/build checks.
- skip_candidate: `yes: barrel only`

### OH_MY_HUMANIZE_MAIN-HZ-2142 `file` `packages/coding-agent/src/lsp/lspmux.ts`
- cursor: `[_]`
- core_role: Detection and command wrapping for `lspmux`.
- algorithmic_behavior: Parses config path, checks supported language server commands, tests server liveness with timeout, caches detection state for 5 minutes, and wraps command/args through lspmux when enabled/supported.
- inputs_outputs_state: Inputs are lspmux config, command name/args, binary path, and time. Outputs are state object or wrapped command descriptor.
- gates_or_invariants: Only known supported servers are wrapped; liveness timeout is 1s; cache TTL avoids repeated probes.
- dependencies_and_callers: Depends on filesystem, process spawn, LSP launcher paths.
- edge_cases_or_failure_modes: Stale cache can briefly hide config changes; liveness failure disables wrapping.
- validation_or_tests: Covered indirectly by LSP command tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2172 `file` `packages/coding-agent/src/memory-backend/local-backend.ts`
- cursor: `[_]`
- core_role: Local memory backend adapter for coding-agent memory interface.
- algorithmic_behavior: Wraps existing memory module functions to save learned lessons, enqueue consolidation, clear/start/build instructions, and reports active/writable/searchable flags.
- inputs_outputs_state: Inputs are learned lesson text/session context. Outputs are persisted local memory entries and instruction strings.
- gates_or_invariants: Backend flags indicate local availability characteristics; consolidation is queued via underlying module.
- dependencies_and_callers: Depends on local memories module and memory backend interface.
- edge_cases_or_failure_modes: Underlying memory unavailable or disabled changes effective behavior.
- validation_or_tests: Memory integration tests cover broader behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2202 `file` `packages/coding-agent/src/plan-mode/approved-plan.ts`
- cursor: `[_]`
- core_role: Approved plan title normalization and plan file resolution.
- algorithmic_behavior: Normalizes plan titles to safe markdown slugs, derives title from supplied title/H1/filename/default, produces `local://<slug>-plan.md`, and resolves approved plan content from supplied URL, state path, or newest plan file.
- inputs_outputs_state: Inputs are title/body/path/state/current plan files. Outputs are normalized filename, human title, URL, or loaded plan reference.
- gates_or_invariants: Rejects empty titles, path separators, `..`, and invalid-only titles; strips `.md`; spaces become hyphens.
- dependencies_and_callers: Used by plan mode, handoff, approved plan loading.
- edge_cases_or_failure_modes: Missing plan throws `ToolError` with target; whitespace-only plan ignored by handoff tests.
- validation_or_tests: `plan-handoff.test.ts` covers reference loading.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2232 `file` `packages/coding-agent/src/session/session-persistence.ts`
- cursor: `[_]`
- core_role: Session persistence sanitizer/truncator and blob externalizer.
- algorithmic_behavior: Recursively traverses session data, truncates huge strings with safe surrogate handling, clears cryptographic thinking signatures instead of truncating, externalizes large image/data URL payloads to blob store, and drops transient fields.
- inputs_outputs_state: Inputs are session entries/messages/content blocks and blob store. Outputs are persistence-safe cloned structures and external blob refs.
- gates_or_invariants: Max string length 500k; signature fields cleared; image content over threshold 1024 externalized; unchanged structures keep sharing.
- dependencies_and_callers: Used by session save/export paths; depends on blob store and content shape conventions.
- edge_cases_or_failure_modes: Must avoid dangling high surrogate; skip existing blob refs; update `lineCount` when content changes.
- validation_or_tests: Session persistence/export tests cover behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2262 `file` `packages/coding-agent/src/stt/wav.ts`
- cursor: `[_]`
- core_role: WAV/PCM decoder and resampler for STT input.
- algorithmic_behavior: Parses RIFF/WAVE chunks including extensible fmt, decodes PCM 8-bit unsigned, 16-bit signed, 32-bit signed, IEEE float32, averages channels to mono, linearly resamples to 16k, and decodes raw s16le buffers.
- inputs_outputs_state: Inputs are WAV or raw PCM bytes. Outputs are Float32 audio samples and sample-rate-normalized arrays.
- gates_or_invariants: Requires RIFF/WAVE plus fmt/data chunks; unsupported format/bit width throws; raw s16le reads whole samples.
- dependencies_and_callers: Used by STT transcriber and recorder streaming path.
- edge_cases_or_failure_modes: Missing chunks, unknown extensible format, odd byte tails, or unsupported channel data fail early.
- validation_or_tests: STT/audio tests cover key decode paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2292 `file` `packages/coding-agent/src/tools/bash-command-fixup.ts`
- cursor: `[_]`
- core_role: Bash command cleanup wrapper around native shell parser/fixups.
- algorithmic_behavior: Calls native `applyBashFixups` to strip trailing `head`/`tail` pipes and redundant `2>&1` patterns; returns original command on parse failure, multiline input, or no change.
- inputs_outputs_state: Input is a bash command string. Output is fixed command string plus metadata/no-op behavior.
- gates_or_invariants: Never changes commands the parser cannot safely understand.
- dependencies_and_callers: Depends on Rust/native shell fixup library; used by bash tool command preview/execution prep.
- edge_cases_or_failure_modes: Multiline or parse-invalid commands intentionally remain unchanged.
- validation_or_tests: Shell minimizer/fixup tests likely cover native behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2322 `file` `packages/coding-agent/src/tools/job.ts`
- cursor: `[_]`
- core_role: Async job management tool and renderer.
- algorithmic_behavior: Implements `poll`, `cancel`, and `list` operations against `asyncJobManager`; scopes jobs by agent id; polls explicit or all running jobs; waits smartly until completion/window/abort; emits progress; renders markdown summaries and sanitized task/result previews.
- inputs_outputs_state: Inputs are tool args, session agent id, async job manager state, abort signal. Outputs are tool result text/details, cancelled ids, polled jobs, and render components.
- gates_or_invariants: `list` cannot combine with poll/cancel; no manager returns “No async jobs”; all-running poll result is marked waiting/useless; cancel reports not_found/already_completed/cancelled.
- dependencies_and_callers: Depends on async job manager, task rendering utilities, tool-result builder, TUI renderers.
- edge_cases_or_failure_modes: Busy poll can be displaceable; explicit cancel-only returns immediately; task output must be truncated/sanitized.
- validation_or_tests: Task render tests and async job tests cover related contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2352 `file` `packages/coding-agent/src/tools/tool-result.ts`
- cursor: `[_]`
- core_role: Fluent builder for structured `AgentToolResult` objects.
- algorithmic_behavior: Accumulates text/image content, details/meta, error/useless/displaceable flags, and produces standardized tool results.
- inputs_outputs_state: Inputs are detail object, text/image blocks, flags. Output is an `AgentToolResult`.
- gates_or_invariants: Details type can include output meta; builder centralizes shape to prevent ad hoc result objects.
- dependencies_and_callers: Used by tool implementations such as job/IRC/search/browser.
- edge_cases_or_failure_modes: Missing text/content affects model-visible result; incorrect flags affect scheduler/render behavior.
- validation_or_tests: Covered by tool tests using result shape.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2382 `file` `packages/coding-agent/src/utils/commit-message-generator.ts`
- cursor: `[_]`
- core_role: LLM-assisted commit message generator with fallback filtering.
- algorithmic_behavior: Filters noisy diff suffixes, chooses small model candidates from config/catalog, truncates diff to max chars, renders static commit prompt, calls provider with low token limit, and returns generated or fallback commit text.
- inputs_outputs_state: Inputs are git diff text, config/models/provider access. Outputs are short commit message string.
- gates_or_invariants: Lockfile-like noise can be filtered; commit max tokens small; reasoning-safe max token cap used for reasoning models.
- dependencies_and_callers: Depends on prompt file, model selection, AI client, catalog helpers.
- edge_cases_or_failure_modes: Empty/noisy diff may need fallback; provider failure should not block commit flow if fallback exists.
- validation_or_tests: Commit workflow tests likely cover user-visible behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2412 `file` `packages/coding-agent/src/workflow/condition.ts`
- cursor: `[_]`
- core_role: Parser/evaluator/diagnostic engine for workflow conditions.
- algorithmic_behavior: Tokenizes and parses boolean expressions with comparisons, `&&`, `||`, `!`, parentheses, and `exists(path)`; evaluates against `state` and `outputs`; collects references and diagnoses unknown nodes/state paths/verdicts.
- inputs_outputs_state: Inputs are condition strings, workflow state/outputs, nodes, optional state schema. Outputs are AST, boolean result, reference list, and diagnostics.
- gates_or_invariants: Arbitrary function calls are rejected; paths must begin `state` or `outputs` for diagnostics; numeric comparisons require both sides numeric; undeclared review verdicts are diagnosed.
- dependencies_and_callers: Depends on workflow state schema helper; used by workflow planner/executor gates.
- edge_cases_or_failure_modes: Strings do not support escapes; unknown paths evaluate false; hyphen allowed in path segments after first char.
- validation_or_tests: Workflow condition tests likely cover parser/evaluator.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2442 `file` `packages/coding-agent/test/capability/fs-special-files.test.ts`
- cursor: `[_]`
- core_role: Filesystem capability tests for special files and symlinks.
- algorithmic_behavior: Creates special file scenarios, verifies read behavior returns null for unsupported/special file and follows readable symlink content.
- inputs_outputs_state: Inputs are temp filesystem nodes and platform guard. Outputs are read result string/null and command exit codes.
- gates_or_invariants: Skips Windows-specific unsupported operations; special files should not hang/read indefinitely.
- dependencies_and_callers: Depends on capability fs read helper and OS filesystem.
- edge_cases_or_failure_modes: FIFO/device reads can block if not detected.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2472 `file` `packages/coding-agent/test/core/python-executor.test.ts`
- cursor: `[_]`
- core_role: Tests Python kernel executor result mapping and output handling.
- algorithmic_behavior: Executes Python cells, captures text/display outputs, maps stdin requests to errors, maps tracebacks to exit code 1, sanitizes streamed chunks, handles timeout/cancel, and stores full output artifact when truncated.
- inputs_outputs_state: Inputs are Python code snippets, timeout/cancel signals, artifact store. Outputs are executor result fields, display outputs, artifact id/text.
- gates_or_invariants: Interactive stdin unsupported; timeout annotation appears only for timeout cancellation; truncated output must keep tail and artifact full text.
- dependencies_and_callers: Depends on Python executor/kernel integration.
- edge_cases_or_failure_modes: Long output truncation must not lose full artifact; cancellation should not add generic command timeout text.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2502 `file` `packages/coding-agent/test/discovery/monorepo-skills.test.ts`
- cursor: `[_]`
- core_role: Tests monorepo skill discovery walk-up and precedence.
- algorithmic_behavior: Writes skill fixtures in ancestor `.omp/skills` directories, discovers from nested cwd, verifies closest skill wins, multiple ancestor levels are ordered, no-skill case empty, and walk-up stops at repo root.
- inputs_outputs_state: Inputs are temp directory trees with `SKILL.md` files. Outputs are discovered skill lists/order.
- gates_or_invariants: Repo root boundary prevents skills above repo from leaking in; duplicate names resolve closest first.
- dependencies_and_callers: Depends on skill discovery subsystem.
- edge_cases_or_failure_modes: Monorepo nested packages can accidentally pick root/global skills in wrong order.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2532 `file` `packages/coding-agent/test/internal-urls/docs-index.test.ts`
- cursor: `[_]`
- core_role: Tests embedded docs index decoding.
- algorithmic_behavior: Encodes filenames/body blobs, decodes first-line filename JSON without inflating bodies, lazily resolves body by index, and returns null for empty placeholder/no newline.
- inputs_outputs_state: Inputs are encoded docs index string. Outputs are filenames array, lazy body strings, undefined for missing, or null.
- gates_or_invariants: Body lookup must be index-aligned; empty placeholder is not an error.
- dependencies_and_callers: Depends on internal docs URL/index decoder generated by docs script.
- edge_cases_or_failure_modes: Corrupt filename/body alignment would serve wrong docs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2562 `file` `packages/coding-agent/test/plan-mode/plan-handoff.test.ts`
- cursor: `[_]`
- core_role: Tests loading overall plan references for plan handoff.
- algorithmic_behavior: Writes/omits/empties plan file and asserts loader returns `{path, content}` only when file exists and has non-whitespace content.
- inputs_outputs_state: Inputs are plan reference path and file contents. Outputs are plan reference object or undefined.
- gates_or_invariants: Missing or whitespace-only files are ignored.
- dependencies_and_callers: Depends on plan handoff/approved plan loader.
- edge_cases_or_failure_modes: Empty plan should not create misleading handoff context.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2592 `file` `packages/coding-agent/test/session/thinking-display.test.ts`
- cursor: `[_]`
- core_role: Tests canonicalization of thinking display text.
- algorithmic_behavior: Verifies undefined/empty/whitespace/dot-only content canonicalizes to empty string, while actual prose including punctuation is preserved.
- inputs_outputs_state: Input is message text. Output is canonical string.
- gates_or_invariants: `"."`, `"..."`, and ellipsis-only text are suppressed.
- dependencies_and_callers: Depends on session thinking display canonicalizer.
- edge_cases_or_failure_modes: Placeholder dots from providers should not render as thinking content.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2622 `file` `packages/coding-agent/test/task/render-yield-shape.test.ts`
- cursor: `[_]`
- core_role: Tests task renderer tolerance for malformed `yield` shapes.
- algorithmic_behavior: Renders task result/progress with `yield` as single object, primitive, and canonical array, asserting no throw and verdict still surfaces when possible.
- inputs_outputs_state: Inputs are task result/progress detail objects. Outputs are rendered text strings.
- gates_or_invariants: Renderer must be defensive against non-array yield from older/malformed agents.
- dependencies_and_callers: Depends on collab/task renderer code and theme.
- edge_cases_or_failure_modes: Bad yield shape previously could crash rendering.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2652 `file` `packages/coding-agent/test/tools/browser-cmux-socket.test.ts`
- cursor: `[_]`
- core_role: Tests cmux browser socket client framing, auth, errors, and serialization.
- algorithmic_behavior: Runs a local socket server, verifies auth line, JSON request frame without JSON-RPC wrapper, result parsing, `ok:false` to `ToolError`, and sequential request serialization.
- inputs_outputs_state: Inputs are socket path/secret, method/params, server responses. Outputs are client result or thrown `ToolError`, plus observed request lines.
- gates_or_invariants: Requests on one socket are serialized; unsupported errors format as `not_supported: x`.
- dependencies_and_callers: Depends on `CmuxSocketClient`.
- edge_cases_or_failure_modes: Concurrent writes could interleave without serialization.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2682 `file` `packages/coding-agent/test/tools/irc-roster-activity.test.ts`
- cursor: `[_]`
- core_role: Tests IRC roster activity display and registry activity state.
- algorithmic_behavior: Registers agents, sets activity, lists peers, and asserts role/activity text, stale avoidance via `lastActivity`, clearing on non-running states, ignoring unknown agents, and multiline activity normalization.
- inputs_outputs_state: Inputs are agent registry entries and activity updates. Outputs are IRC list text and registry state.
- gates_or_invariants: No dangling `undefined`/empty clauses; activity heartbeat for stopped/unknown agents ignored.
- dependencies_and_callers: Depends on IRC tool and agent registry.
- edge_cases_or_failure_modes: Multiline/tabbed activity must become one bounded line.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2712 `file` `packages/coding-agent/test/tools/search-renderer.test.ts`
- cursor: `[_]`
- core_role: Tests search tool result renderer layout, truncation, grouping, and file links.
- algorithmic_behavior: Renders inline/grouped search results, asserts indentation/no success header, header truncation status, collapsed budget, actual match visibility, filesystem link URIs, and expanded/collapsed body bounds.
- inputs_outputs_state: Inputs are synthetic search result details and theme. Outputs are ANSI/plain rendered text and extracted links.
- gates_or_invariants: No bottom truncation notice; grouped and single-file code-frame lines link to target paths/lines.
- dependencies_and_callers: Depends on search renderer, theme/link helpers.
- edge_cases_or_failure_modes: Large grouped sections must show useful matches without dumping all context.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2742 `file` `packages/coding-agent/test/utils/jj.test.ts`
- cursor: `[_]`
- core_role: Tests Jujutsu workspace detection utilities.
- algorithmic_behavior: Creates `.jj` metadata layouts, checks nested root detection, per-cwd cache, bare `.jj` rejection, non-default workspace with `.jj/repo` file, and shared store resolution.
- inputs_outputs_state: Inputs are temp directory structures. Outputs are repo root booleans and resolved store dir.
- gates_or_invariants: Bare `.jj` directory alone is not a workspace; cache is keyed per requested cwd.
- dependencies_and_callers: Depends on `jj` utility module.
- edge_cases_or_failure_modes: Non-default workspace layout differs from default and must resolve shared store.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2772 `file` `packages/collab-web/src/lib/codec.ts`
- cursor: `[_]`
- core_role: Browser encryption/decryption codec for collaboration session frames.
- algorithmic_behavior: Imports a 32-byte room key, seals JSON with AES-GCM using 12-byte IV prefix layout `[IV][ciphertext+tag]`, and opens/decrypts/parses sealed bytes.
- inputs_outputs_state: Inputs are room key bytes, JSON-serializable session data, sealed frames. Outputs are sealed `Uint8Array` or parsed session data.
- gates_or_invariants: Key length must be 32 bytes; sealed payload must be longer than IV; decrypt/parse errors throw.
- dependencies_and_callers: Depends on browser WebCrypto; used by collab-web share/join UI.
- edge_cases_or_failure_modes: Wrong key or truncated frame fails decrypt; malformed JSON fails parse.
- validation_or_tests: Share/collab tests cover codec round trips.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2802 `file` `packages/mnemopi/src/core/memory.ts`
- cursor: `[_]`
- core_role: Public mnemopi memory facade over BeamMemory, banks, embeddings, and runtime options.
- algorithmic_behavior: Resolves embedding/LLM runtime options, DB path/bank, remember/recall option aliases, constructs `BeamMemory`, handles injected DB replacement, reconciles embedding model, exposes remember/recall/stats/update/sleep/scratchpad methods, and module-level default instance/bank helpers.
- inputs_outputs_state: Inputs are memory content, recall queries, options, bank/db/runtime config. Outputs are memory ids, recall results, stats, DB mutations, sleep results, scratchpad rows.
- gates_or_invariants: `queryEmbedding` preserves three states undefined/null/vector; `reconcile: false` skips destructive embedding migration; default instance closes when bank changes.
- dependencies_and_callers: Depends on BeamMemory, BankManager, AnnotationStore, EpisodicGraph, embedding runtime.
- edge_cases_or_failure_modes: Injected DB replaces Beam DB and closes opened one; stale embeddings wiped when model changes unless read-only open.
- validation_or_tests: Beam and issue-1832 embedding tests cover core contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2832 `file` `packages/stats/src/client/App.tsx`
- cursor: `[_]`
- core_role: Stats dashboard top-level React app state/router.
- algorithmic_behavior: Tracks active route, keeps visited routes mounted in `mountedRef`, toggles enabled/visible props, triggers refresh on sync success, tracks updated time, and manages request drawer selection.
- inputs_outputs_state: Inputs are route clicks, sync events, resource data state. Outputs are rendered route panels and drawer state.
- gates_or_invariants: Visited route components remain mounted; only active route is enabled/visible.
- dependencies_and_callers: Depends on stats client components and data hooks.
- edge_cases_or_failure_modes: Keeping mounted preserves state but can retain resource memory.
- validation_or_tests: Frontend behavior likely covered by manual/smoke tests.
- skip_candidate: `yes: UI state shell, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2862 `file` `packages/utils/test/mermaid/multiline.test.ts`
- cursor: `[_]`
- core_role: Tests Mermaid ASCII renderer behavior for multiline labels.
- algorithmic_behavior: Feeds Mermaid diagrams with multiline labels and asserts generated ASCII/ANSI output preserves expected structure and line handling.
- inputs_outputs_state: Inputs are Mermaid graph text. Outputs are rendered ASCII strings.
- gates_or_invariants: Multiline labels must not collapse or corrupt diagram layout.
- dependencies_and_callers: Depends on vendored mermaid-ascii utilities.
- edge_cases_or_failure_modes: Wrapped labels can break box dimensions/edges.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2892 `directory` `packages/coding-agent/src/tools/browser/cmux`
- cursor: `[_]`
- core_role: cmux browser integration layer for socket/RPC-backed browser automation.
- algorithmic_behavior: `rpc.ts` defines cmux types, snapshot-to-observation mapping, eval serialization, wait mapping, and cmux enablement resolution. `socket-client.ts` authenticates, sends serialized JSON requests, waits for line responses, formats cmux errors. `cmux-tab.ts` provides Puppeteer-like facade and code runner over cmux browser RPC.
- inputs_outputs_state: Inputs are env/settings, socket path/secret, browser method params, user JS code, snapshots. Outputs are observations, eval results, screenshots, URL/status responses, and tool errors.
- gates_or_invariants: Socket client serializes requests; cmux kind resolves from env truthy values/settings; snapshot refs convert to tool observation entries.
- dependencies_and_callers: Used by browser tool to switch between local Puppeteer and cmux-backed browser.
- edge_cases_or_failure_modes: Socket timeout/auth failure; missing cmux support falls back or errors; eval serialization must preserve function body/args safely.
- validation_or_tests: `browser-cmux-socket.test.ts` covers socket client contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2922 `file` `crates/pi-shell/src/minimizer/filters/system.rs`
- cursor: `[_]`
- core_role: Shell output minimization filters for common system commands.
- algorithmic_behavior: Detects supported programs, compacts env/log/dependency/test/error/format/ps/ping/ssh/sops/pipe-like outputs, masks sensitive env values, strips timestamps, normalizes UUID/hex/path tokens, counts repeated lines, and preserves important diagnostics.
- inputs_outputs_state: Inputs are command name/context, raw stdout/stderr text, exit code. Outputs are minimized text and metadata.
- gates_or_invariants: Sensitive env keys masked; failure output keeps relevant lines; summaries are bounded by head/tail/count rules.
- dependencies_and_callers: Used by native shell command minimizer for bash tool output.
- edge_cases_or_failure_modes: Over-aggressive noise detection can hide needed diagnostics; sensitive-key detection must catch token/password variants.
- validation_or_tests: Rust minimizer tests likely cover filters.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2952 `file` `packages/ai/src/utils/schema/index.ts`
- cursor: `[_]`
- core_role: Barrel export for schema utilities.
- algorithmic_behavior: Re-exports adapt, compatibility, dereference, draft, equality, fields, validators, normalize, spill, strict tool validation, types, TypeScript, wire, and zod decontamination modules.
- inputs_outputs_state: No state beyond export surface.
- gates_or_invariants: Star exports preserve broad schema utility API.
- dependencies_and_callers: Used by providers and tool schema conversion code.
- edge_cases_or_failure_modes: Export ambiguity or missing module breaks imports.
- validation_or_tests: Type/build checks and provider schema tests.
- skip_candidate: `yes: barrel only`

### OH_MY_HUMANIZE_MAIN-HZ-2982 `file` `packages/coding-agent/src/cli/gallery-fixtures/web.ts`
- cursor: `[_]`
- core_role: Static web gallery fixture definitions.
- algorithmic_behavior: Exports a record of gallery fixtures with web-oriented scenario metadata/content for CLI/gallery demos.
- inputs_outputs_state: Inputs are none at runtime beyond import. Outputs are fixture objects.
- gates_or_invariants: Fixture keys and shapes must match `GalleryFixture` type.
- dependencies_and_callers: Used by gallery CLI/demo features.
- edge_cases_or_failure_modes: Broken fixture shape affects demo rendering, not core CLI operation.
- validation_or_tests: Type checks.
- skip_candidate: `yes: static demo fixture data`

### OH_MY_HUMANIZE_MAIN-HZ-3012 `file` `packages/coding-agent/src/edit/hashline/index.ts`
- cursor: `[_]`
- core_role: Barrel export for hashline edit subsystem.
- algorithmic_behavior: Re-exports block resolver, diff, execute, filesystem, and params modules.
- inputs_outputs_state: No state beyond export surface.
- gates_or_invariants: Maintains stable hashline import API.
- dependencies_and_callers: Used by edit/apply patch code.
- edge_cases_or_failure_modes: Export drift breaks compile.
- validation_or_tests: Type/build and hashline tests.
- skip_candidate: `yes: barrel only`

### OH_MY_HUMANIZE_MAIN-HZ-3042 `file` `packages/coding-agent/src/eval/py/spawn-options.ts`
- cursor: `[_]`
- core_role: Windows/Python kernel spawn window visibility and console detection helper.
- algorithmic_behavior: Decides whether to hide kernel window, checks console attachment via TTY and Windows console probe, caches probe result, exposes reset for tests, and reports host inheritable console.
- inputs_outputs_state: Inputs are platform, env/process stdio, Bun/native console probe. Outputs are booleans for spawn options.
- gates_or_invariants: Non-Windows behavior differs from Windows window hiding; probe result cached.
- dependencies_and_callers: Used by Python executor spawn setup.
- edge_cases_or_failure_modes: Incorrect console detection can spawn visible windows or detach incorrectly on Windows.
- validation_or_tests: Python eval prelude/spawn tests likely cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3072 `file` `packages/coding-agent/src/extensibility/plugins/loader.ts`
- cursor: `[_]`
- core_role: Plugin discovery and manifest entry resolver.
- algorithmic_behavior: Loads runtime lock and project overrides, unions package dependencies with lock plugins, filters disabled plugins, resolves enabled features/settings, and maps manifest tools/hooks/commands/extensions to loadable files with directory/index/manifest precedence.
- inputs_outputs_state: Inputs are plugin root, lockfile, package.json, project override files, manifests, enabled feature list. Outputs are `InstalledPlugin` objects and resolved module paths/settings.
- gates_or_invariants: Extension directory manifests are authoritative and suppress fallback; declaration files are not loadable; missing manifest entries return null for validation.
- dependencies_and_callers: Used by plugin manager, extension/tool/hook/command loaders.
- edge_cases_or_failure_modes: Linked plugin lock without node_modules tree is skipped; invalid project override JSON falls through to next path.
- validation_or_tests: `plugin-install-validation.test.ts` covers missing entries and rollback.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3102 `file` `packages/coding-agent/src/modes/components/bash-execution.ts`
- cursor: `[_]`
- core_role: Streaming bash execution TUI component.
- algorithmic_behavior: Accepts output chunks, throttles display processing, stores recent lines, clamps long non-sixel lines, handles completion/cancel/exit status, and renders collapsed or expanded output with hidden-line footer.
- inputs_outputs_state: Inputs are command output chunks, exit status, cancellation state, terminal width, expansion state. Outputs are rendered ANSI lines and output sink writes.
- gates_or_invariants: Full output is preserved in sink while display keeps bounded preview; sixel lines bypass normal truncation when allowed.
- dependencies_and_callers: Used by bash tool live renderer; depends on TUI theme/render utilities.
- edge_cases_or_failure_modes: First incoming line merges with previous last line; huge lines are clamped to avoid terminal overflow.
- validation_or_tests: Bash renderer tests cover preview behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3132 `file` `packages/coding-agent/src/modes/components/model-selector.ts`
- cursor: `[_]`
- core_role: Interactive model/provider/role/thinking selector component.
- algorithmic_behavior: Normalizes search, ranks models by role/default/current characteristics, builds provider tabs, filters canonical/scoped items, renders badges/assignments, handles keyboard navigation, role actions, provider refresh debounce, and selection callbacks.
- inputs_outputs_state: Inputs are model catalog, provider state, roles, current assignments, search text, key events. Outputs are selected model/role/thinking changes, rendered menu lines, and cancel/refresh callbacks.
- gates_or_invariants: Static tabs `ALL`/`CANONICAL` plus provider tabs; role badges reflect assignment source; search tokens compact punctuation/case.
- dependencies_and_callers: Used by `/switch`, `/model`, setup picker, and TUI model selection.
- edge_cases_or_failure_modes: Provider refresh races with debounce; hidden/custom roles and stale models must render predictably.
- validation_or_tests: Slash switch/model tests and component tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3162 `file` `packages/coding-agent/src/modes/components/welcome.ts`
- cursor: `[_]`
- core_role: Welcome/start screen component with tips, recent sessions, LSP status, and animated logo.
- algorithmic_behavior: Renders wrapped welcome tips, fixed recent-session/LSP slots, gradient PI logo, intro animation frames, and responsive text blocks.
- inputs_outputs_state: Inputs are tips text, recent sessions, LSP server info, theme, terminal width, animation phase. Outputs are rendered line arrays and animation frame requests.
- gates_or_invariants: Tip width is bounded; session/LSP slots fixed; gradient escape clamps color interpolation.
- dependencies_and_callers: Used by startup splash/welcome UI; depends on theme and tips asset.
- edge_cases_or_failure_modes: Narrow widths need wrapping without ellipsis; animation disabled/rest frame must be stable.
- validation_or_tests: `welcome-tip.test.ts` covers wrapping.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3192 `file` `packages/coding-agent/src/modes/theme/shimmer.ts`
- cursor: `[_]`
- core_role: ANSI shimmer/highlight effect for themed text.
- algorithmic_behavior: Compiles palettes into ANSI tier sequences, computes classic or KITT intensity by time/index, resolves mode from env/config, and applies colored segments or full text shimmer while respecting disabled mode.
- inputs_outputs_state: Inputs are text segments, theme, optional palette, time/mode env. Outputs are ANSI-colored strings.
- gates_or_invariants: Disabled mode returns plain theme output; palette compilation cached per theme/palette.
- dependencies_and_callers: Used by welcome/status/theme renderers.
- edge_cases_or_failure_modes: ANSI reset/bold handling must not leak styles; intensity tiers must stay finite for empty strings.
- validation_or_tests: UI snapshot/manual tests; no direct file test observed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3222 `file` `packages/coding-agent/src/tools/browser/tab-worker.ts`
- cursor: `[_]`
- core_role: Browser tab worker core that executes JS automation against Puppeteer pages.
- algorithmic_behavior: Initializes headless/attached page, normalizes selectors, collects accessibility observations with element id cache, runs user JS in `JsRuntime`, exposes `tab` helper API, tracks inflight ops for timeout diagnostics, handles screenshots, extraction, clicks, typing, drag, upload, wait, eval, tool calls, aborts, and close.
- inputs_outputs_state: Inputs are worker protocol messages, browser endpoint, target/page, code, session cwd/options, aborts. Outputs are ready/result/error/log/tool-call messages, screenshots, displays, and cached element handles.
- gates_or_invariants: Only one active run; quick ops capped at 20s; selector credentials redacted in ready URL; element ids stale after navigation/observe clear; headless page closed on worker close.
- dependencies_and_callers: Depends on Puppeteer, JS runtime, browser tool protocol, screenshot resizing, readable extraction.
- edge_cases_or_failure_modes: Text query click retries actionable candidates; screenshot element scroll avoids IntersectionObserver stalls; timeout names stalled helper.
- validation_or_tests: Browser/cmux/socket and browser tool tests cover subsets.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3252 `file` `packages/coding-agent/src/web/scrapers/huggingface.ts`
- cursor: `[_]`
- core_role: Special web scraper for Hugging Face model/dataset/space/user URLs.
- algorithmic_behavior: Parses Hugging Face URL path kind/id, fetches API JSON, and formats concise markdown-like summaries for models, datasets, spaces, or users.
- inputs_outputs_state: Inputs are URL, timeout, abort signal. Outputs are scraper result content or null/handled failure.
- gates_or_invariants: Only recognized Hugging Face paths are handled; API calls obey timeout/signal.
- dependencies_and_callers: Used by web/read scraper registry; depends on fetch and Hugging Face API shapes.
- edge_cases_or_failure_modes: Private/missing resources or changed API fields reduce summary quality.
- validation_or_tests: Web scraper documentation tests cover special handler behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3282 `file` `packages/coding-agent/src/web/scrapers/searchcode.ts`
- cursor: `[_]`
- core_role: Special scraper for searchcode result URLs.
- algorithmic_behavior: Validates host, parses line number structures, formats line ranges and code blocks from searchcode API responses.
- inputs_outputs_state: Inputs are searchcode URL, timeout, abort signal. Outputs are formatted result content or null.
- gates_or_invariants: Only `searchcode.com`/`www.searchcode.com` accepted; line numbers sorted/formatted when present.
- dependencies_and_callers: Used by web scraper registry.
- edge_cases_or_failure_modes: Missing line map returns code block without line range; invalid host ignored.
- validation_or_tests: `tools/web-scrapers/documentation.test.ts` and integration gating cover scrapers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3312 `file` `packages/coding-agent/test/modes/components/assistant-message-mermaid.test.ts`
- cursor: `[_]`
- core_role: Tests assistant message rendering of Mermaid diagrams.
- algorithmic_behavior: Creates assistant markdown messages with Mermaid code blocks, renders under terminal image protocol variations, and asserts Mermaid output falls back/renders as expected with thinking renderers.
- inputs_outputs_state: Inputs are markdown text and renderer list. Outputs are rendered assistant message text.
- gates_or_invariants: Mermaid blocks should not break message rendering when image protocol unavailable.
- dependencies_and_callers: Depends on assistant message component and mermaid-ascii rendering.
- edge_cases_or_failure_modes: Bad Mermaid or no image support should degrade gracefully.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3342 `file` `packages/coding-agent/test/modes/components/user-message-selector.test.ts`
- cursor: `[_]`
- core_role: Tests user message selector behavior.
- algorithmic_behavior: Exercises selector rendering/navigation/selection for user messages in mode components.
- inputs_outputs_state: Inputs are mock message list and key/selection events. Outputs are selected message/callback and rendered text.
- gates_or_invariants: Only user-selectable messages should appear or be selectable.
- dependencies_and_callers: Depends on user message selector component.
- edge_cases_or_failure_modes: Empty or non-user-only lists must not crash.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3372 `file` `packages/coding-agent/test/tools/web-scrapers/documentation.test.ts`
- cursor: `[_]`
- core_role: Optional integration tests for documentation/web scrapers.
- algorithmic_behavior: Gated by `WEB_FETCH_INTEGRATION`, fetches real documentation/special URLs and verifies scraper output shape/content.
- inputs_outputs_state: Inputs are live URLs and env flag. Outputs are fetched scraper text/results.
- gates_or_invariants: Skips unless integration env set to avoid network dependence.
- dependencies_and_callers: Depends on web scraper registry and network.
- edge_cases_or_failure_modes: Live site changes can alter output; gating prevents default suite flake.
- validation_or_tests: This file is validation when enabled.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3402 `file` `packages/collab-web/src/components/transcript/Markdown.tsx`
- cursor: `[_]`
- core_role: Safe markdown renderer for collab transcript UI.
- algorithmic_behavior: Uses marked/GFM, escapes raw HTML, permits safe hrefs (`http`, `https`, `mailto`, relative, fragment), and renders unsafe links as inner text only.
- inputs_outputs_state: Input is markdown text. Output is React rendered markup.
- gates_or_invariants: Unknown schemes rejected; parse errors escape text rather than rendering unsafe HTML.
- dependencies_and_callers: Used by collab transcript components; depends on `marked`.
- edge_cases_or_failure_modes: URL parsing failures should be treated conservatively.
- validation_or_tests: Collab UI tests or manual coverage; security behavior encoded in helper.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3432 `file` `packages/collab-web/src/tool-render/tools/task.tsx`
- cursor: `[_]`
- core_role: Collab-web renderer for task tool calls/results.
- algorithmic_behavior: Normalizes args with `tasks[]` or legacy flat shape, formats breadcrumb ids, computes result status, extracts missing-yield warning prefix, renders agent links, stats, progress rows, output previews, errors, patches, branches, and footer counts.
- inputs_outputs_state: Inputs are task tool call args/results/progress details. Outputs are React UI for transcript.
- gates_or_invariants: Final results sorted by duration then index; malformed details must degrade without crash.
- dependencies_and_callers: Used by collab web tool renderer registry.
- edge_cases_or_failure_modes: Missing yield warning is pulled from output prefix; long output preview must be bounded by UI component.
- validation_or_tests: Task render-shape tests cover related robustness.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3462 `file` `packages/stats/src/client/data/useResource.ts`
- cursor: `[_]`
- core_role: React hook for cached/polling resource fetches in stats dashboard.
- algorithmic_behavior: Keeps session-level cache map limited to 64 entries by JSON key, initializes from cache, aborts previous fetches, supports foreground/background refresh, updates cache with eviction, polls only when document visible, and cleans up on unmount.
- inputs_outputs_state: Inputs are resource key, fetcher, enabled flag, polling interval, background/foreground triggers. Outputs are data/loading/error/refreshing state and refetch function.
- gates_or_invariants: Foreground fetch clears data/loading; background refresh preserves stale data; hidden document skips polling.
- dependencies_and_callers: Used by stats client data views.
- edge_cases_or_failure_modes: JSON key instability can fragment cache; abort must prevent stale update.
- validation_or_tests: React hook tests not observed; behavior explicit.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3492 `file` `python/robomp/web/src/components/GlassCard.tsx`
- cursor: `[_]`
- core_role: Solid UI presentation component for robomp web dashboard cards.
- algorithmic_behavior: Renders a section with optional heading/accessory, class/contentClass/style props, and children.
- inputs_outputs_state: Inputs are component props and children. Output is DOM JSX.
- gates_or_invariants: Heading row appears only when heading/accessory provided.
- dependencies_and_callers: Used by robomp web UI components.
- edge_cases_or_failure_modes: `bare` prop appears presentational and may not alter classes depending implementation.
- validation_or_tests: UI compile/render coverage only.
- skip_candidate: `yes: presentation-only component, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3522 `file` `packages/coding-agent/src/eval/py/__tests__/prelude.test.ts`
- cursor: `[_]`
- core_role: Test for Python prelude `read` helper signature.
- algorithmic_behavior: Inspects prelude text/API to assert `read(path, offset?, limit?)` is not keyword-only and includes offset/limit parameters.
- inputs_outputs_state: Input is Python prelude source. Output is test assertion status.
- gates_or_invariants: Positional offset/limit must remain supported for user code ergonomics.
- dependencies_and_callers: Depends on Python eval prelude.
- edge_cases_or_failure_modes: Keyword-only regression would break existing snippets.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3552 `file` `packages/coding-agent/src/modes/components/status-line/token-rate.ts`
- cursor: `[_]`
- core_role: Token-per-second calculation for status line.
- algorithmic_behavior: Finds last assistant message with numeric timestamp and output usage, derives duration from message duration or streaming now minus timestamp, enforces minimum 100ms, and returns finite positive TPS or null.
- inputs_outputs_state: Inputs are message list and current time. Output is token rate number/null.
- gates_or_invariants: Output tokens must be positive; invalid/nonfinite duration returns null.
- dependencies_and_callers: Used by status line component.
- edge_cases_or_failure_modes: Streaming messages without duration use current clock; zero/negative duration clamped by minimum.
- validation_or_tests: Covered by status/session display tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3582 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/ansi.ts`
- cursor: `[_]`
- core_role: ANSI/HTML colorization utilities for vendored Mermaid ASCII renderer.
- algorithmic_behavior: Defines default theme, detects color mode from env/TTY, parses hex colors, converts truecolor to 256/16-color ANSI, escapes HTML, maps character roles to colors, and colorizes characters/lines/text.
- inputs_outputs_state: Inputs are ASCII diagram characters/roles, theme, color mode. Outputs are ANSI or HTML colored strings.
- gates_or_invariants: Reset codes emitted for ANSI modes; HTML text escaped; color mode controls no-color/16/256/truecolor/html behavior.
- dependencies_and_callers: Used by mermaid-ascii diagram rendering.
- edge_cases_or_failure_modes: Invalid hex parsing throws; ANSI reset leakage can corrupt terminal style.
- validation_or_tests: Mermaid multiline/component tests cover rendered behavior.
- skip_candidate: `yes: vendored rendering utility, though used by runtime diagram display`

### OH_MY_HUMANIZE_MAIN-HZ-3612 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/hexagon.ts`
- cursor: `[_]`
- core_role: Hexagon shape renderer in vendored Mermaid ASCII renderer.
- algorithmic_behavior: Delegates dimensions/attachment behavior to rectangle helpers, retrieves hexagon corners for ASCII/Unicode mode, and renders a box-like shape with hex-specific corner markers.
- inputs_outputs_state: Inputs are shape text/dimensions/style and ASCII mode. Outputs are shape drawing primitives/lines.
- gates_or_invariants: Hexagon must share rectangle attachment semantics so graph edges connect consistently.
- dependencies_and_callers: Used by mermaid-ascii shape registry.
- edge_cases_or_failure_modes: Incorrect corners or dimensions misalign edges in diagrams.
- validation_or_tests: Mermaid renderer tests cover diagram output.
- skip_candidate: `yes: vendored shape renderer, not product control logic`

## Worker Self-Test
- assigned_items_seen: 121 unique `## Item Evidence` sections were produced, in scheduler order, with one section per assigned row.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`