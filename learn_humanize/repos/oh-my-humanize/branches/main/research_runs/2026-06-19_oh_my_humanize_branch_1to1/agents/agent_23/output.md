# agent_23 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-023 `directory` `docs/toolconv`
- cursor: `[_]`
- core_role: Documentation corpus for in-band tool-call dialect algorithms. It defines the token/string envelopes that `packages/ai/src/dialect/*` scanners and renderers implement.
- algorithmic_behavior: Covers Gemini/Gemma Pythonic fenced calls, Qwen/Hermes `<tool_call>` JSON blocks, Kimi section tokens, GLM XML-like arg-key/value tags, DeepSeek fullwidth special-token flows plus DSML, Anthropic XML invokes, Gemma 4 `<|tool_call>` grammar, Harmony role/channel tokens, and pi-native call tags.
- inputs_outputs_state: Inputs are raw model text streams, tool catalogs, and tool-result turns; outputs are normalized tool calls, thinking blocks, visible text, and tool-result prompts. State is mostly per-dialect parsing state: outside/thinking/tool/header/arg/response sections.
- gates_or_invariants: Each spec emphasizes positional result matching, no model-emitted call IDs for most dialects, exact delimiter preservation, stop-after-tool-call behavior, and robust parsing around malformed or leaked prompt-engineered formats.
- dependencies_and_callers: Directly informs `packages/ai/src/dialect` implementations and `owned-stream.ts` fabrication boundaries. Also overlaps with `docs/toolconv/gemini.md`, assigned separately.
- edge_cases_or_failure_modes: Special-token vs plain-text leakage, string/fence ambiguity, Unicode fullwidth DeepSeek tokens, malformed JSON/Python literals, streamed partial tags, and history rerender asymmetry.
- validation_or_tests: Dialect behavior is indirectly validated by AI tests around schema compatibility, provider output mapping, and in-band owned-mode stream projection.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-053 `file` `docs/mcp-runtime-lifecycle.md`
- cursor: `[_]`
- core_role: Architecture/runtime lifecycle contract for MCP server discovery, connection, refresh, tool exposure, health, and teardown.
- algorithmic_behavior: Defines discovery/load phases, manager state, per-server connection pipeline, fast startup gate with deferred background fallback, live-session tool availability, reload paths, reconnect/partial-failure behavior, and teardown semantics.
- inputs_outputs_state: Inputs are SDK/session config and discovered MCP server definitions; outputs are registered tools, manager/server states, connection attempts, health diagnostics, and teardown actions. State transitions cover discovered -> connecting -> ready/failed/deferred -> refreshed/reconnected -> stopped.
- gates_or_invariants: Startup should avoid blocking on slow MCP servers; live reload differs from initial startup; failures are isolated per server; teardown must be server-level or global depending on caller.
- dependencies_and_callers: Points to `packages/coding-agent/src/mcp/{client,config,loader,manager,tool-bridge,tool-cache,transports}` and is surfaced through the MCP barrel at `packages/coding-agent/src/mcp/index.ts`.
- edge_cases_or_failure_modes: Discovery failure, slow startup, partial server failure, refresh during active sessions, background completion races, and stale tool exposure.
- validation_or_tests: Relevant to `packages/coding-agent/test/acp-mcp-isolation.test.ts`, MCP isolation, and tool cache/loader behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-083 `file` `scripts/check-spoofed-versions.ts`
- cursor: `[_]`
- core_role: Runtime maintenance script that validates hardcoded spoofed User-Agent/tool versions against upstream GitHub releases.
- algorithmic_behavior: Reads `packages/catalog/src/wire/gemini-headers.ts`, extracts versions with configured regexes, fetches latest GitHub release tags, compares current vs latest, optionally rewrites source with `--update`, and exits nonzero on drift/no successful checks.
- inputs_outputs_state: Inputs are CLI flag `--update`, GitHub release API responses, regex extraction from provider source. Outputs are console reports, optional source update, and process exit codes.
- gates_or_invariants: At least one check must succeed; drift without `--update` is failure; tag parsing is semver-only via `SEMVER_RE`; fetch failures do not update.
- dependencies_and_callers: Depends on Bun fetch/file/write and path; checks Gemini CLI version in catalog wire headers.
- edge_cases_or_failure_modes: Missing source regex match, GitHub API failure, invalid/missing latest tag, network denial, or no checks succeeding.
- validation_or_tests: No direct test observed; likely used by release/maintenance checks.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-113 `file` `scripts/sync-themes.ts`
- cursor: `[_]`
- core_role: Runtime generation helper for synchronizing bundled theme JSON files into a TypeScript index.
- algorithmic_behavior: Reads theme defaults directory, filters/sorts `.json`, creates import lines and `defaultThemes` object entries, writes `index.ts`.
- inputs_outputs_state: Input is filesystem contents under `packages/coding-agent/src/modes/interactive/theme/defaults`; output is regenerated `index.ts`.
- gates_or_invariants: Only `.json` files are included; ordering is lexical; variable names replace hyphens with underscores.
- dependencies_and_callers: Uses `node:fs/promises`, `node:path`, and Bun.write. It feeds theme loading in coding-agent UI.
- edge_cases_or_failure_modes: Missing directory, duplicate variable names after hyphen normalization, JSON filenames not valid TS identifiers after transformation, or write failure.
- validation_or_tests: No direct test observed; generated index likely covered by UI/theme import checks.
- skip_candidate: `yes: generator script, not a runtime algorithm in the product path`

### OH_MY_HUMANIZE_MAIN-HZ-143 `directory` `packages/natives/bench`
- cursor: `[_]`
- core_role: Benchmark harness for native grep performance.
- algorithmic_behavior: Contains `grep.ts`, which defines benchmark cases, iterations from `GREP_BENCH_ITERATIONS`, concurrency, package/cargo-registry paths, and runs grep workloads to measure native search behavior.
- inputs_outputs_state: Inputs are benchmark iteration env, source directories, and grep case definitions. Outputs are timing/throughput reports.
- gates_or_invariants: Bench cases should be repeatable against fixed paths; concurrency fixed at 2; missing optional paths should be handled by case setup.
- dependencies_and_callers: Depends on native grep implementation in `packages/natives`/Rust crate and Bun runtime.
- edge_cases_or_failure_modes: Missing cargo registry, huge workspace variance, or absent native addon can invalidate timing.
- validation_or_tests: Bench only; not a correctness test.
- skip_candidate: `yes: performance harness rather than core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-173 `file` `docs/toolconv/gemini.md`
- cursor: `[_]`
- core_role: Detailed dialect spec for Gemini/Gemma 3 Pythonic in-band tool calls.
- algorithmic_behavior: Specifies ` ```tool_code ` blocks containing Python call expressions such as `print(default_api.name(kwargs))`, ` ```tool_outputs ` result blocks, optional OMP ` ```thinking ` block, multiple call forms, Python literal parsing, and OpenAI-compatible mapping.
- inputs_outputs_state: Input is raw assistant text with Python source; output is normalized tool name/arguments and result prompts. No native call ID exists; call order is state.
- gates_or_invariants: Parser must strip `print`, module prefixes, and assignment; must parse Python literals rather than JSON; must skip strings/comments while scanning calls; results match calls by order.
- dependencies_and_callers: Implemented by `packages/ai/src/dialect/gemini.ts`; docs mention malformed-function-call leakage as evidence.
- edge_cases_or_failure_modes: Fence truncation if argument includes bare fence, positional args ignored, leaked raw tool markdown, triple/single quoted strings, comments, lists/dicts, and malformed call bodies.
- validation_or_tests: Covered by dialect parsing behavior and owned-stream tests where Gemini response-open token is ` ```tool_outputs`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-203 `file` `docs/tools/ssh.md`
- cursor: `[_]`
- core_role: Tool architecture spec for SSH execution tool.
- algorithmic_behavior: Documents host discovery, capability loading, command wrapping by remote shell/OS, timeout clamping, master connection reuse, sshfs side effects, streaming tail updates, output truncation/artifacts, and error mapping.
- inputs_outputs_state: Inputs are `host`, `command`, optional remote `cwd`, and `timeout`; outputs are text results, truncation metadata, stream updates, or `ToolError`.
- gates_or_invariants: Host must be a discovered config key; timeout clamps to `1..3600`; tool is exclusive; output tail is bounded; nonzero/cancel/timeout become errors.
- dependencies_and_callers: `packages/coding-agent/src/tools/ssh.ts`, `ssh/ssh-executor.ts`, `ssh/connection-manager.ts`, `sshfs-mount.ts`, discovery/capability modules, streaming-output, and tool-timeouts.
- edge_cases_or_failure_modes: Unknown host, missing ssh binary, key permission failure, stale host info, Windows compat shell wrapping, sshfs failure logged but ignored, merged stdout/stderr order.
- validation_or_tests: Documentation itself; runtime likely covered by SSH/tool integration tests outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-233 `directory` `packages/ai/src/dialect`
- cursor: `[_]`
- core_role: Core in-band tool dialect subsystem: converts tool catalogs/history into model-specific prompt formats and parses raw model text back into structured assistant events.
- algorithmic_behavior: `factory.ts` maps catalog dialect ids to definitions; each dialect module implements `InbandScanner` state machines plus renderers. `owned-stream.ts` wraps provider streams, detects in-band tool calls/thinking, forwards native tool calls, aborts fabricated tool-result continuations, and resolves native-vs-inband channel ownership. `history.ts` re-encodes historical tool calls/results into user/assistant text.
- inputs_outputs_state: Inputs are raw streaming text deltas, assistant messages, tool schemas, model dialect id, and tool results. Outputs are `InbandScanEvent`s, assistant content blocks, tool-call lifecycle events, rendered prompts, and encoded history messages. State includes scanner buffers, current parser state, open tool/thinking blocks, raw blocks, channel ownership, and pending response-token overlap.
- gates_or_invariants: Tool result markers terminate owned generation; partial tag overlaps are held across chunks; string-only schema args stay raw; non-string args parse/repair as JSON/Python/XML by dialect; most dialects mint ids internally; renderers preserve tool-result order.
- dependencies_and_callers: Depends on catalog identity dialects, tool schema helpers, JSON repair utilities, and `AssistantMessageEventStream`; called by provider conversion/streaming paths.
- edge_cases_or_failure_modes: Partial tags split across chunks, malformed JSON/Python/XML, response fabrication, double native/in-band tool calls, nameless native ghost calls, token delimiters inside strings, huge XML parameter values, unsupported dialect id.
- validation_or_tests: Indirectly validated by provider tests (`mock-provider`, schema compatibility, OpenAI response roles), docs under `docs/toolconv`, and likely dialect-specific tests outside assignment.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-263 `directory` `packages/coding-agent/src/extensibility`
- cursor: `[_]`
- core_role: Plugin/extension/custom command/custom tool/hook/skill runtime for coding-agent.
- algorithmic_behavior: Loads skills, custom commands/tools, hooks, and extensions from configured roots; shims legacy `pi-ai` and coding-agent APIs; wraps custom tools into `AgentTool`s; exposes extension API/context/events; manages plugin installation/discovery/marketplace/cache/runtime settings; enforces handler timeouts and session event ordering.
- inputs_outputs_state: Inputs are settings, plugin dirs, manifests, extension factories, hook events, session context, and tool definitions. Outputs are registered commands/tools/hooks/renderers/providers/events and extension errors. State includes active skills, plugin registry/cache, extension runtime registrations, pending credential-disabled queue, handler maps, and plugin install snapshots.
- gates_or_invariants: Handler timeouts (`EXTENSION_HANDLER_TIMEOUT_MS`, shutdown timeout), schema validation through local typebox bridge, plugin package/git validation, custom command location mapping, active tool registration, no global module mocking in tests.
- dependencies_and_callers: Used by CLI session startup, slash command discovery, custom command tests, marketplace discovery tests, tool execution, and SDK integration.
- edge_cases_or_failure_modes: Malformed manifests, unsafe package specs, handler timeout, extension factory errors, duplicate command/tool names, legacy compatibility gaps, plugin registry precedence, local plugin roots.
- validation_or_tests: `packages/coding-agent/test/extensibility/custom-commands/*`, `sdk-skills.test.ts`, marketplace discovery tests, and custom tool tests validate user-facing contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-293 `directory` `packages/coding-agent/test/cli`
- cursor: `[_]`
- core_role: CLI contract tests for shell completion generation and TTSR CLI behavior.
- algorithmic_behavior: `completions.test.ts` builds synthetic and live completion specs, then asserts bash/zsh/fish generation for flags, aliases, dynamic value sources, comma-list helpers, and root/command dispatch. `ttsr-cli.test.ts` captures stdout/exit, creates temporary rules/snippets, and validates TTSR test/list/scan inference and JSON reports.
- inputs_outputs_state: Inputs are synthetic command specs, live CLI entry, temp rules/snippets, captured stdout, project dir settings. Outputs are generated shell scripts and TTSR rendered/JSON reports.
- gates_or_invariants: Completion output must contain exact shell routing fragments; TTSR source inference must choose tool/edit for file positional and text for inline snippets; JSON report shape must include matched/defined arrays.
- dependencies_and_callers: Tests `cli/completion-gen`, `cli/ttsr-cli`, settings/project-dir utilities, and TTSR manager/rule parser.
- edge_cases_or_failure_modes: Alias dispatch drift, repeatable flags, short+long flag pairs, dynamic completions, source inference mismatches, AST condition matching, stdout/process.exit restoration.
- validation_or_tests: This directory is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-323 `directory` `packages/collab-web/src/tool-render`
- cursor: `[_]`
- core_role: React/web-component rendering layer for tool calls/results in collab web and exported HTML sessions.
- algorithmic_behavior: `registry.ts` maps tool names/aliases to renderer modules; `ToolView.tsx` normalizes args, extracts intent `_i`, manages open/collapsed UI, status, partial streaming tail; `parts.tsx` provides sanitized output, badges, path text, images, code highlighting; per-tool renderers summarize arguments and render result bodies.
- inputs_outputs_state: Inputs are tool name, args, running flag, partial output, result blocks/details, host capabilities. Outputs are cards, summaries, key/value grids, text/image previews, badges, and fallback generic JSON.
- gates_or_invariants: Unknown tools fall back to generic renderer; ANSI is stripped and tabs replaced before output; partial tail capped; renderer aliases preserve legacy/sibling tool names; image previews decode only valid base64.
- dependencies_and_callers: Used by collab-web app, `standalone.tsx`, custom element `element.tsx`, and session export HTML.
- edge_cases_or_failure_modes: Malformed args/results, missing details, result error styling, unsupported highlighter language, bad image data, very long partial output, renderer missing for new tool.
- validation_or_tests: HTML export tests and tool-output hyperlink tests indirectly validate export render surfaces; registry itself has no focused assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-353 `file` `crates/pi-natives/src/clipboard.rs`
- cursor: `[_]`
- core_role: Native clipboard bridge for text copy and image read.
- algorithmic_behavior: Exposes N-API `copy_to_clipboard` and async `read_image_from_clipboard`; converts arboard image RGBA bytes into PNG; Linux keeps a process-global `Clipboard` alive behind `OnceLock<Mutex<Option<Clipboard>>>` so X11/Wayland clipboard ownership persists.
- inputs_outputs_state: Inputs are text strings or current system clipboard image. Outputs are clipboard text side effect or optional `{data, mime_type}` PNG image. State is global clipboard handle on Linux.
- gates_or_invariants: PNG width/height conversion must not overflow; buffer size must match RGBA image; Linux clipboard instance must persist; non-Linux uses transient clipboard.
- dependencies_and_callers: Uses `arboard`, `image`, N-API task blocking. Called by coding-agent paste/copy features through native package.
- edge_cases_or_failure_modes: Clipboard access failure, no image (`ContentNotAvailable` -> `None`), buffer mismatch, encode failure, poisoned mutex recovered.
- validation_or_tests: Native tests not assigned; behavior documented in comments around issue #2075.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-383 `file` `crates/pi-shell/src/shell.rs`
- cursor: `[_]`
- core_role: Core shell execution engine for persistent/streaming commands with output minimization, environment handling, cancellation, and background job cleanup.
- algorithmic_behavior: Defines shell options/results, `Shell`, `execute_shell`, `execute_shell_streams`, env merging, command parsing, duration parsing, heredoc newline fixups, stream sinks, nonblocking pipe handling, minimizer integration, and keepalive/termination semantics.
- inputs_outputs_state: Inputs are shell command/options/env/cwd/timeout/stdin and stream sinks. Outputs are exit code, stdout/stderr/text, minimizer result, streaming chunks, and shell keepalive status. State includes brush shell instance, env, background jobs, pending streams, and minimizer config.
- gates_or_invariants: Env keys normalized by platform; Windows PATH merge dedupes; macOS malloc stack logging vars skipped; heredocs require trailing newline; background jobs terminated; shell session keepalive depends on execution result.
- dependencies_and_callers: Used by shell/native execution layers; collaborates with minimizer modules including `minimizer/filters/cpp.rs`.
- edge_cases_or_failure_modes: Nonblocking pipe EAGAIN, timeout/cancellation, platform null file, command parse ambiguity, env fallback, background jobs surviving, huge outputs requiring minimization.
- validation_or_tests: Inline Rust tests in file and minimizer filter tests cover portions; full shell behavior likely tested elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-413 `file` `packages/agent/test/snapcompact-frames.test.ts`
- cursor: `[_]`
- core_role: Regression test for compaction summary messages carrying snapcompact frames.
- algorithmic_behavior: Builds summary message paths and asserts snapcompact frame metadata is preserved/rendered in compaction summary message creation.
- inputs_outputs_state: Inputs are compaction summary inputs with snapcompact frame payloads. Outputs are agent message content/details.
- gates_or_invariants: Summary construction must not drop frame artifacts when compaction uses snapcompact.
- dependencies_and_callers: Tests `packages/agent/src/compaction/messages`/snapcompact integration.
- edge_cases_or_failure_modes: Frame metadata lost during conversion or summary short text path.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-443 `file` `packages/ai/test/anthropic-oauth.test.ts`
- cursor: `[_]`
- core_role: Contract tests for Anthropic OAuth alignment.
- algorithmic_behavior: Validates OAuth login/config/header building, model auth config behavior, and search header construction for Anthropic provider paths.
- inputs_outputs_state: Inputs are mocked/stored OAuth credentials and provider/model config. Outputs are auth headers/config objects and credential handling decisions.
- gates_or_invariants: OAuth-derived headers must match Anthropic requirements; API-key vs OAuth paths must not mix incorrectly.
- dependencies_and_callers: Tests `packages/ai/src/registry/oauth/anthropic*` and provider auth config functions.
- edge_cases_or_failure_modes: Missing token, disabled credential, search headers, enterprise/base URL variations.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-473 `file` `packages/ai/test/auth-storage-api-key-login.test.ts`
- cursor: `[_]`
- core_role: AuthStorage regression tests for API-key login replacement.
- algorithmic_behavior: Counts SQLite credential rows before/after login flows and disabled-state changes; asserts replacement rather than duplicate accumulation for same provider API-key login.
- inputs_outputs_state: Inputs are temporary auth DB, provider ids, API-key credentials. Outputs are stored credential row counts and disabled flags.
- gates_or_invariants: API-key login should replace active provider credential and respect disabled-state semantics.
- dependencies_and_callers: Tests AI auth storage and login persistence.
- edge_cases_or_failure_modes: Duplicate rows, disabled credentials not replaced, provider mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-503 `file` `packages/ai/test/firepass.live.ts`
- cursor: `[_]`
- core_role: Live integration probe for Firepass/Fireworks-compatible reasoning effort pass-through.
- algorithmic_behavior: Uses live API key, captures fetch request, runs baseline and `xhigh` requests, and checks request body semantics including max token/reasoning payload.
- inputs_outputs_state: Inputs are `FIREPASS_API_KEY`, bundled Firepass model, fetch capture. Outputs are live assistant events and captured HTTP body.
- gates_or_invariants: Reasoning effort should pass through verbatim where supported and not be forced into incompatible defaults.
- dependencies_and_callers: Tests AI provider conversion for Firepass OpenAI-compatible completions.
- edge_cases_or_failure_modes: Missing API key, network failure, provider behavior changes, live negative request status.
- validation_or_tests: Live test; likely gated by env.
- skip_candidate: `yes: live provider probe, not core algorithm implementation`

### OH_MY_HUMANIZE_MAIN-HZ-533 `file` `packages/ai/test/issue-1270-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for Vertex AI global endpoint/OAuth token routing.
- algorithmic_behavior: Stubs token URLs and model context to reproduce issue #1270, then asserts provider uses correct endpoint/auth flow.
- inputs_outputs_state: Inputs are Google Vertex model spec, OAuth/metadata token URLs, mocked fetch. Outputs are request URL/header behavior.
- gates_or_invariants: Global endpoint should not force region-specific or metadata-token-only auth path incorrectly.
- dependencies_and_callers: Tests Google Vertex provider auth/request logic.
- edge_cases_or_failure_modes: Token source precedence, global endpoint URL composition.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-563 `file` `packages/ai/test/mock-provider.test.ts`
- cursor: `[_]`
- core_role: Tests for mock AI provider event stream and assistant message shape.
- algorithmic_behavior: Collects async assistant events from mock completions; validates text/tool/result/event sequencing, async iterable sources, and message usage/shape contracts.
- inputs_outputs_state: Inputs are mock provider contexts and scripted sources. Outputs are `AssistantMessageEvent` arrays and final assistant messages.
- gates_or_invariants: Mock provider must emit valid start/delta/done/error event order and assistant message blocks compatible with runtime.
- dependencies_and_callers: Tests `packages/ai` mock provider and event-stream utilities.
- edge_cases_or_failure_modes: Empty context, async iterable response source errors, malformed tool block shape.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-593 `file` `packages/ai/test/openai-responses-developer-role.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI Responses compatibility for developer role and juice-zero hack.
- algorithmic_behavior: Exercises resolver/build functions for `supportsDeveloperRole` and `requiresJuiceZeroHack`, asserting role conversion and request construction choices.
- inputs_outputs_state: Inputs are model compatibility flags and messages with developer/system roles. Outputs are request payload role fields and hack flags.
- gates_or_invariants: Developer role only used when model/API supports it; otherwise mapped safely; juice-zero workaround only for matching compat.
- dependencies_and_callers: Tests OpenAI Responses provider compatibility builder.
- edge_cases_or_failure_modes: Models with ambiguous support flags, incorrect role downgrade, unwanted workaround.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-623 `file` `packages/ai/test/schema-compatibility.test.ts`
- cursor: `[_]`
- core_role: Tests schema compatibility validator for provider tool schemas.
- algorithmic_behavior: Builds schema compatibility results and checks named validation rules via `hasRule`.
- inputs_outputs_state: Inputs are JSON schemas with provider-incompatible constructs. Outputs are rule diagnostics.
- gates_or_invariants: Validator should flag concrete unsupported schema features and preserve rule ids.
- dependencies_and_callers: Tests AI schema compatibility logic used before tool submission.
- edge_cases_or_failure_modes: Missing rules for nested constructs, overflagging supported schemas.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-653 `file` `packages/ai/test/xiaomi-tp-login-integration.test.ts`
- cursor: `[_]`
- core_role: Integration tests for Xiaomi Token Plan (`tp-`) login/model manager options.
- algorithmic_behavior: Exercises host selection for token-plan vs standard Xiaomi hosts, login behavior, model-manager option resolution, and full round-trip when environment allows.
- inputs_outputs_state: Inputs are `tp-` keys, host maps, env/config, mocked/live request contexts. Outputs are credential/model manager options and provider responses.
- gates_or_invariants: `tp-` keys must route to token-plan hosts and not standard endpoints; full round-trip only when configured.
- dependencies_and_callers: Tests Xiaomi provider auth/model management.
- edge_cases_or_failure_modes: Misclassified key prefix, host mismatch, live network/API changes.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-683 `file` `packages/catalog/test/identity-family.test.ts`
- cursor: `[_]`
- core_role: Catalog identity classifier contract tests for model families and thinking support.
- algorithmic_behavior: Asserts functions like Kimi, Claude, MiniMax M2/M3, GPT-OSS, GLM reasoning/vision, model family token, and Grok reasoning effort capability.
- inputs_outputs_state: Inputs are model id strings. Outputs are boolean classifier results and family tokens.
- gates_or_invariants: Suffixes/versions/aliases must classify consistently; unrelated ids must not false-positive.
- dependencies_and_callers: Tests `packages/catalog/src/identity` functions used by provider behavior, UI, and dialect selection.
- edge_cases_or_failure_modes: New model ids with similar substrings, version suffixes, markers, family overlap.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-713 `file` `packages/catalog/test/zhipu-compat.test.ts`
- cursor: `[_]`
- core_role: Tests OpenAI-compatible resolution for Zhipu coding-plan models and discovery.
- algorithmic_behavior: Constructs Zhipu model specs by provider/base URL and asserts compatibility branch, base URL handling, and discovery output.
- inputs_outputs_state: Inputs are provider ids, base URLs, model specs. Outputs are resolved compat config and discovered model entries.
- gates_or_invariants: Zhipu coding-plan branch must trigger by provider or official base URL; GLM model variants must keep intended compat metadata.
- dependencies_and_callers: Tests `provider-models/openai-compat` resolver/discovery logic.
- edge_cases_or_failure_modes: Provider/base-url mismatch, new GLM model ids, discovery metadata drift.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-743 `file` `packages/coding-agent/test/acp-mcp-isolation.test.ts`
- cursor: `[_]`
- core_role: Regression test for ACP session factory MCP isolation.
- algorithmic_behavior: Creates ACP sessions and asserts MCP manager/config isolation between sessions/projects.
- inputs_outputs_state: Inputs are isolated session factory options and MCP config contexts. Outputs are session state/manager isolation assertions.
- gates_or_invariants: ACP sessions must not share MCP state across project/session boundaries.
- dependencies_and_callers: Tests `createAcpSessionFactory` and MCP loader/manager integration.
- edge_cases_or_failure_modes: Global MCP manager leakage, config reuse, wrong project cwd.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-773 `file` `packages/coding-agent/test/agent-session-model-switch-auth.test.ts`
- cursor: `[_]`
- core_role: Tests AgentSession model switch authentication preflight.
- algorithmic_behavior: Exercises model switching paths and asserts auth validation happens before committing model state.
- inputs_outputs_state: Inputs are session model choices, auth availability, mocked provider credentials. Outputs are switch success/failure and retained/current model state.
- gates_or_invariants: Failed auth preflight must not leave session on unauthorized model.
- dependencies_and_callers: Tests coding-agent session model switching and AI auth integration.
- edge_cases_or_failure_modes: Missing API key/OAuth, fallback model roles, partially persisted model change.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-803 `file` `packages/coding-agent/test/autolearn-discovery.test.ts`
- cursor: `[_]`
- core_role: Tests managed-skills discovery.
- algorithmic_behavior: Writes temporary skill manifests and asserts loader discovers authored/managed skills under expected roots.
- inputs_outputs_state: Inputs are temp skill directories with names/descriptions. Outputs are discovered skill metadata and warnings.
- gates_or_invariants: Skill discovery must require valid `SKILL.md` metadata and not cross-contaminate roots.
- dependencies_and_callers: Tests `extensibility/skills.ts` and SDK/session skill loading.
- edge_cases_or_failure_modes: Missing description/name, symlinks, malformed frontmatter, duplicate names.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-833 `file` `packages/coding-agent/test/compaction-prefer-current-model.test.ts`
- cursor: `[_]`
- core_role: Regression test that compaction uses current session model over default model role.
- algorithmic_behavior: Sets session/current model and modelRoles.default, triggers compaction setup, and asserts selected summarization model.
- inputs_outputs_state: Inputs are settings/model roles and session current model. Outputs are model chosen for compaction.
- gates_or_invariants: User-switched current model should win over default-role configuration.
- dependencies_and_callers: Tests compaction/session model selection.
- edge_cases_or_failure_modes: Model role fallback overriding active session model.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-863 `file` `packages/coding-agent/test/flag-tables.test.ts`
- cursor: `[_]`
- core_role: CLI arg parser contract tests for flag metadata tables.
- algorithmic_behavior: Validates `STRING_VALUE_FLAGS`, `OPTIONAL_VALUE_FLAGS`, per-flag quirks, and end-of-options `--` handling.
- inputs_outputs_state: Inputs are argv arrays. Outputs are parsed args/options.
- gates_or_invariants: Flags requiring/optionally accepting values must parse consistently; `--` terminates option parsing.
- dependencies_and_callers: Tests `args.ts`/flag table behavior in coding-agent CLI.
- edge_cases_or_failure_modes: Optional flag swallowing positional text, missing values, repeated flags.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-893 `file` `packages/coding-agent/test/input-controller-smart-paste.test.ts`
- cursor: `[_]`
- core_role: Tests input controller paste behavior for images and raw text.
- algorithmic_behavior: Creates fake focused context and asserts smart-paste fallback routes image/text paste to focused editor or controller.
- inputs_outputs_state: Inputs are paste text/image conditions and focused component hooks. Outputs are paste method calls and state changes.
- gates_or_invariants: Focused component paste handlers should receive data when present; fallback should not drop clipboard text.
- dependencies_and_callers: Tests TUI input controller paste handling.
- edge_cases_or_failure_modes: No focused target, image paste fallback, raw paste preserving newlines.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-923 `file` `packages/coding-agent/test/issue-845-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for update method resolution through symlinks/junctions.
- algorithmic_behavior: Builds temp symlink/junction scenarios and asserts resolver follows real paths to detect correct update method.
- inputs_outputs_state: Inputs are filesystem layouts. Outputs are update method classifications.
- gates_or_invariants: Symlinked install paths must resolve to the authoritative package/update source.
- dependencies_and_callers: Tests update method resolver.
- edge_cases_or_failure_modes: Symlink loops, platform junction semantics, realpath failures.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-953 `file` `packages/coding-agent/test/main-cross-project-resume.test.ts`
- cursor: `[_]`
- core_role: Tests cross-project session resume cancellation/relocation.
- algorithmic_behavior: Builds resume args/global matches and asserts `createSessionManager` cancels unsafe cross-project resume or relocates moved worktree sessions.
- inputs_outputs_state: Inputs are cwd/session dirs/global session matches. Outputs are cancellation flags, session manager paths, and relocation behavior.
- gates_or_invariants: Cross-project resume must not silently attach to wrong project; moved worktree path can be relocated when safe.
- dependencies_and_callers: Tests session manager creation and resume lookup.
- edge_cases_or_failure_modes: Global match for different cwd, moved worktree, stale session dir.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-983 `file` `packages/coding-agent/test/model-registry-command-values.test.ts`
- cursor: `[_]`
- core_role: Tests model registry command-resolved `models.yml` values.
- algorithmic_behavior: Uses command stdout as model config values and asserts registry resolves output into model fields.
- inputs_outputs_state: Inputs are command strings producing values. Outputs are model registry entries.
- gates_or_invariants: Command-based config values must be executed/resolved deterministically and not kept as raw command markers.
- dependencies_and_callers: Tests coding-agent model registry settings loader.
- edge_cases_or_failure_modes: Empty stdout, command failure, unsafe shell expansion.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1013 `file` `packages/coding-agent/test/read-summary.test.ts`
- cursor: `[_]`
- core_role: Contract tests for read tool summary/truncation behavior.
- algorithmic_behavior: Creates fake `ToolSession`, applies summary overrides, executes read flows, and asserts text output summarization.
- inputs_outputs_state: Inputs are files, offsets/ranges, summary options. Outputs are `AgentToolResult` text/details.
- gates_or_invariants: Read summaries must reflect selected content, honor limits, and surface semantic text rather than raw oversized output.
- dependencies_and_callers: Tests read tool implementation and render utils.
- edge_cases_or_failure_modes: Empty files, long files, legacy summary override settings, offset/range boundaries.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1043 `file` `packages/coding-agent/test/sdk-skills.test.ts`
- cursor: `[_]`
- core_role: Tests SDK skill option loading.
- algorithmic_behavior: Builds isolated settings, writes test/symlinked skills, and asserts `createAgentSession` skill option activates expected skill prompts.
- inputs_outputs_state: Inputs are SDK options and skill directories. Outputs are loaded skill state and prompt content.
- gates_or_invariants: SDK-provided skills should be isolated from global settings and support symlinked skill paths.
- dependencies_and_callers: Tests `createAgentSession` and `extensibility/skills`.
- edge_cases_or_failure_modes: Duplicate names, symlink resolution, missing skill file.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1073 `file` `packages/coding-agent/test/status-line-context-cache.test.ts`
- cursor: `[_]`
- core_role: Tests status line context breakdown cache.
- algorithmic_behavior: Constructs fake sessions/messages/usage and asserts rendered context breakdown updates/caches correctly.
- inputs_outputs_state: Inputs are message arrays, context window, usage. Outputs are status line breakdown text/state.
- gates_or_invariants: Cache must invalidate when messages/usage change; context window absent/present affects percentages.
- dependencies_and_callers: Tests interactive status line component.
- edge_cases_or_failure_modes: Stale cache after message mutation, zero/undefined context window, cache read/write token accounting.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1103 `file` `packages/coding-agent/test/tiny-dtype.test.ts`
- cursor: `[_]`
- core_role: Tests tiny-model dtype/device setting mapping.
- algorithmic_behavior: Sets tiny model dtype settings and asserts environment mapping to `PI_TINY_DTYPE`.
- inputs_outputs_state: Inputs are settings paths like `providers.tinyModelDtype`. Outputs are env/config strings for tiny inference.
- gates_or_invariants: Supported dtype values must map exactly; unset settings should not emit invalid env.
- dependencies_and_callers: Tests tiny inference worker setup, related to TTS client spawn env.
- edge_cases_or_failure_modes: Unknown dtype, stale env leakage between tests.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1133 `file` `packages/collab-web/scripts/mock-host.ts`
- cursor: `[_]`
- core_role: Local mock host for collab-web relay/session replay.
- algorithmic_behavior: Starts local relay, creates room/key/link, connects as host WebSocket, maintains session entries/agents/peers, broadcasts state, steps scripted transcript replay, handles guest frames for hello/prompt/abort/agent commands/fetch transcript/control, and graceful shutdown.
- inputs_outputs_state: Inputs are CLI port, fixture entries/agents/transcript/scripted steps, WebSocket frames. Outputs are encrypted host frames, state broadcasts, notices, transcript chunks, and logs.
- gates_or_invariants: Peer map identifies guests; replay steps are scheduled at fixed intervals; transcript fetch uses byte offsets; shutdown closes relay/session.
- dependencies_and_callers: Depends on collab relay/protocol/crypto fixtures; used for manual/dev testing of collab-web.
- edge_cases_or_failure_modes: Unknown frames, invalid control text, peer disconnects, replay already running, transcript offset beyond length.
- validation_or_tests: Dev harness; no direct test assigned.
- skip_candidate: `yes: mock/demo host, not production runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1163 `file` `packages/hashline/test/core-contracts.test.ts`
- cursor: `[_]`
- core_role: Core contract tests for hashline patch parsing/recovery.
- algorithmic_behavior: Tests normalization, range anchors, input splitting, patcher preflight, recovery, abort sentinel, delete and blank payload semantics using in-memory filesystem helpers.
- inputs_outputs_state: Inputs are hashline patch text and in-memory file contents. Outputs are patch sections, applied/recovered content, errors.
- gates_or_invariants: Range anchors and line tags must locate intended text; preflight blocks unsafe writes; abort sentinel stops application.
- dependencies_and_callers: Tests hashline parser/patcher used by editing tools.
- edge_cases_or_failure_modes: Same-line range anchors, blank deletes, blocked filesystem, recovery ambiguity, abort marker.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1193 `file` `packages/mnemopi/test/configurable-scoring.test.ts`
- cursor: `[_]`
- core_role: Tests configurable memory recall scoring weights.
- algorithmic_behavior: Creates Beam memory, mutates env/config, recalls entries, and asserts score composition changes with configured weights.
- inputs_outputs_state: Inputs are memory rows and scoring env/config. Outputs are recall ordering/scores.
- gates_or_invariants: Weight knobs should influence scoring without poisoning global env after tests.
- dependencies_and_callers: Tests `mnemopi` Beam recall scoring.
- edge_cases_or_failure_modes: Env leakage, zero/negative weights, empty memory.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1223 `file` `packages/mnemopi/test/plugins.test.ts`
- cursor: `[_]`
- core_role: Tests mnemopi plugin manager and built-in plugins.
- algorithmic_behavior: Defines `CountingPlugin`, emits memory lifecycle events, and asserts plugin callback counts/behavior.
- inputs_outputs_state: Inputs are memory events and plugin instances. Outputs are callback side effects and built-in plugin results.
- gates_or_invariants: Plugin manager should emit expected lifecycle events and close plugins cleanly.
- dependencies_and_callers: Tests `MnemopiPlugin`/plugin manager.
- edge_cases_or_failure_modes: Callback exceptions, duplicate plugins, close ordering.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1253 `file` `packages/natives/scripts/embed-native.ts`
- cursor: `[_]`
- core_role: Native addon embedding script for packaged distributions.
- algorithmic_behavior: With `--reset`, writes null stub and removes archives; otherwise selects platform/arch addon candidates, validates existence, builds tar.gz archive with `Bun.Archive`, and generates `embedded-addon.js` metadata importing archive as file.
- inputs_outputs_state: Inputs are target platform/arch env, native addon files, package version. Outputs are archive and generated JS metadata.
- gates_or_invariants: x64 expects modern/baseline variants; non-x64 default variant; no available addon is fatal; generated file is marked autogenerated.
- dependencies_and_callers: Used by package build/release of `packages/natives`.
- edge_cases_or_failure_modes: Missing addon, ENOENT native dir during reset, archive write failure, platform tag mismatch.
- validation_or_tests: Build pipeline likely validates; no direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1283 `file` `packages/snapcompact/research/exp11_memhier.py`
- cursor: `[_]`
- core_role: Research experiment script for memory-hierarchy compression/visualization.
- algorithmic_behavior: Renders text pages, generates summaries via model, builds context blocks, runs chunks, computes tier stats, and orchestrates experiment in `main`.
- inputs_outputs_state: Inputs are model/key config, source text/pages, tier offsets, condition/cell settings. Outputs are experiment records, stats, rendered pages.
- gates_or_invariants: Tier bounds must align with flow length; page rendering requires font/assets; stats aggregate by tier.
- dependencies_and_callers: Uses PIL and model API utilities in research context; not imported by runtime.
- edge_cases_or_failure_modes: Missing font/image deps, API failure, invalid offsets, large text.
- validation_or_tests: Research script only.
- skip_candidate: `yes: experimental research artifact, not runtime core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1313 `file` `packages/snapcompact/research/snapcompact_logit_lens_dump.py`
- cursor: `[_]`
- core_role: Research script for logit-lens dumping over snapcompact frames/images.
- algorithmic_behavior: Loads model/tokenizer, processes visual/text inputs, dumps top-token/logit lens data for analysis.
- inputs_outputs_state: Inputs are local model, image/text/frame paths. Outputs are diagnostic dumps/files.
- gates_or_invariants: Requires Python deps (`pillow`, `numpy`, `torch`, `transformers`) and compatible model architecture.
- dependencies_and_callers: Research-only under snapcompact; no runtime caller.
- edge_cases_or_failure_modes: GPU/CPU memory, unsupported model, missing image, tokenizer mismatch.
- validation_or_tests: Research script only.
- skip_candidate: `yes: exploratory diagnostic script, not production algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1343 `file` `packages/snapcompact/test/snapcompact.test.ts`
- cursor: `[_]`
- core_role: Broad contract tests for snapcompact rendering, serialization, archive helpers, and compaction.
- algorithmic_behavior: Tests file list computation, PNG decode/rendering, normalization, shape resolution, multi-frame render, conversation serialization, compact output, archive helpers, stopword dimming, wrap/doc layout, and shape variants.
- inputs_outputs_state: Inputs are synthetic messages/tool results/preparations, frame size, PNG palette, archives. Outputs are rendered PNG/frame data, serialized docs, compact summaries.
- gates_or_invariants: Rendered frames must be decodable; shapes/layout must be stable; serialization must preserve conversation/tool semantics; archive helper round-trips.
- dependencies_and_callers: Tests `packages/snapcompact` core library and agent compaction integration.
- edge_cases_or_failure_modes: Image dimensions/palette, wrapping boundaries, tool result content, empty file lists, archive corruptions.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1373 `file` `packages/tui/src/index.ts`
- cursor: `[_]`
- core_role: TUI package public barrel export.
- algorithmic_behavior: Re-exports components, terminal/TUI utilities, keybindings, fuzzy, mouse, kitty graphics, latex, autocomplete, etc.
- inputs_outputs_state: Input is module graph; output is public API surface for consumers.
- gates_or_invariants: Export paths must stay valid; uses star exports mostly, with type-only exports for symbols where needed.
- dependencies_and_callers: Consumed by coding-agent UI and tests.
- edge_cases_or_failure_modes: Broken export path, ambiguous duplicate export, accidental omission.
- validation_or_tests: Compile/check and tests importing `@oh-my-pi/pi-tui`.
- skip_candidate: `yes: API barrel, no core algorithm beyond export surface`

### OH_MY_HUMANIZE_MAIN-HZ-1403 `file` `packages/tui/test/image-test.ts`
- cursor: `[_]`
- core_role: Manual/interactive test harness for TUI image rendering.
- algorithmic_behavior: Reads image path, encodes base64, gets dimensions, creates `ProcessTerminal`/`TUI`, and renders image/editor components.
- inputs_outputs_state: Inputs are image file path and terminal capabilities. Outputs are terminal render frames.
- gates_or_invariants: Image dimensions must decode; terminal/TUI must accept component lifecycle.
- dependencies_and_callers: Uses TUI image component and terminal renderer.
- edge_cases_or_failure_modes: Missing image path, unsupported terminal, invalid PNG.
- validation_or_tests: Manual test script.
- skip_candidate: `yes: manual harness, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1433 `file` `packages/tui/test/process-terminal-render-harness.ts`
- cursor: `[_]`
- core_role: Test harness for process-terminal rendering dimensions and cleanup.
- algorithmic_behavior: Captures/restores process stdio descriptors, defines `WidthProbe` component, creates harness with settle timing and render control.
- inputs_outputs_state: Inputs are components and terminal size/stdio state. Outputs are rendered output snapshots and cleanup hooks.
- gates_or_invariants: Process stdio mutations must be restored; render settle delay stabilizes diff output.
- dependencies_and_callers: Used by TUI tests such as truncated text rendering.
- edge_cases_or_failure_modes: Leaked stdio monkeypatches, timing flake, terminal width mismatch.
- validation_or_tests: Harness used by tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1463 `file` `packages/tui/test/truncated-text.test.ts`
- cursor: `[_]`
- core_role: Tests TUI `TruncatedText` component.
- algorithmic_behavior: Renders strings with ANSI/chalk, widths, truncation settings, and asserts visual output constraints.
- inputs_outputs_state: Inputs are styled/plain text and width limits. Outputs are rendered terminal strings.
- gates_or_invariants: Truncation must respect display width and ANSI styling.
- dependencies_and_callers: Tests TUI truncated text component and render harness.
- edge_cases_or_failure_modes: ANSI escape width, Unicode width, exact boundary truncation.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1493 `file` `packages/utils/src/json.ts`
- cursor: `[_]`
- core_role: Tiny JSON utility.
- algorithmic_behavior: `tryParseJson<T>` returns parsed JSON or `null` on parse failure.
- inputs_outputs_state: Input is string content; output is typed parsed value or `null`.
- gates_or_invariants: Only catches parse exceptions; does not validate shape.
- dependencies_and_callers: Used by web scrapers (`npm.ts`, `clojars.ts`) and other safe-parse paths.
- edge_cases_or_failure_modes: Valid JSON `null` indistinguishable from parse failure by return value.
- validation_or_tests: Indirect through scraper tests.
- skip_candidate: `yes: trivial helper, not core algorithm alone`

### OH_MY_HUMANIZE_MAIN-HZ-1523 `file` `packages/utils/test/issue-935-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for path equivalence issue #935.
- algorithmic_behavior: Exercises path equivalence helper with problematic path forms.
- inputs_outputs_state: Inputs are path strings. Outputs are equivalence booleans.
- gates_or_invariants: Equivalent paths must compare equal across normalization variants.
- dependencies_and_callers: Tests utils path equivalence logic.
- edge_cases_or_failure_modes: Case sensitivity, symlink/relative segments, platform separators.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1553 `file` `python/robomp/src/dashboard.py`
- cursor: `[_]`
- core_role: Python dashboard support for robomp log/API serving.
- algorithmic_behavior: `tail_jsonl` tails bounded bytes from JSONL logs, parses valid lines; bundle helpers find static dir, cache index template, inject replay token config sentinel, and reset cache.
- inputs_outputs_state: Inputs are log path, byte limit, static bundle files, replay token. Outputs are parsed event dicts or rendered HTML.
- gates_or_invariants: Tail limit capped by seek-from-end; missing bundle raises `DashboardBundleMissing`; config sentinel must exist for injection.
- dependencies_and_callers: Used by robomp dashboard server endpoints.
- edge_cases_or_failure_modes: Missing log, malformed JSON lines ignored, missing index bundle, stale template cache.
- validation_or_tests: Python tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1583 `file` `python/robomp/tests/test_persona.py`
- cursor: `[_]`
- core_role: Tests persona prompt rendering for robomp GitHub automation.
- algorithmic_behavior: Uses fake repo/issue/workspace/PR/comment objects to assert thread rendering, directive prompts, follow-up comments, kickoff triage/review prompts, completion reminders, and system append routing.
- inputs_outputs_state: Inputs are fake GitHub entities and directive bodies. Outputs are prompt strings.
- gates_or_invariants: Prompt text must include repo/issue/PR context and route refusal/review/completion messages to intended audience.
- dependencies_and_callers: Tests robomp persona/prompt code.
- edge_cases_or_failure_modes: Empty thread placeholder, comment ordering, fork/head repo formatting.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1613 `directory` `packages/coding-agent/src/commit/utils`
- cursor: `[_]`
- core_role: Commit utility helpers, currently file exclusion filtering.
- algorithmic_behavior: `exclusions.ts` defines excluded filenames/suffixes and exports `isExcludedFile` plus `filterExcludedFiles`.
- inputs_outputs_state: Inputs are filenames/file records. Outputs are booleans or filtered file arrays.
- gates_or_invariants: Lock files and generated/private paths should be excluded from commit analysis/selection.
- dependencies_and_callers: Used by commit workflow to avoid staging/analyzing unwanted files.
- edge_cases_or_failure_modes: Path separator differences, suffix overlap, false positives for similarly named files.
- validation_or_tests: Commit workflow tests likely cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1643 `directory` `packages/coding-agent/test/extensibility/custom-commands`
- cursor: `[_]`
- core_role: Contract tests for bundled custom commands `review` and `ci-green`.
- algorithmic_behavior: `review.test.ts` stubs git/jj/GitHub diff sources, UI select/editor/notify, and session history to assert review prompt generation, PR URL parsing, JJ diff preference, large PR diff instructions, and local-file-read restrictions. `ci-green.test.ts` stubs git tags to assert tag-specific instructions.
- inputs_outputs_state: Inputs are temp repos, sample diffs, PR URLs, UI responses, git tag lists. Outputs are command prompt strings and notifications.
- gates_or_invariants: JJ diff wins when repo is JJ; PR reviews must use `pr://` diff URLs and avoid local workspace reads; empty custom instructions abort; tagged HEAD adds release guidance.
- dependencies_and_callers: Tests bundled commands under `extensibility/custom-commands/bundled`.
- edge_cases_or_failure_modes: Many-file PR diff omission, explicit URL variants, no diff available, UI/no-UI modes.
- validation_or_tests: This directory is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1673 `file` `packages/agent/src/compaction/branch-summarization.ts`
- cursor: `[_]`
- core_role: Branch navigation summarization algorithm for preserving context when leaving a session branch.
- algorithmic_behavior: `collectEntriesForBranchSummary` finds common ancestor between old leaf and target, collects old-branch entries chronologically; `prepareBranchEntries` converts entries to messages, collects file ops from branch summaries/tool calls, budgets newest messages; `generateBranchSummary` renders prompts and calls LLM summarizer with telemetry.
- inputs_outputs_state: Inputs are session entries/manager, old leaf, target id, token budget, model/api key, abort signal, custom instructions. Outputs are branch summary text, read/modified file lists, aborted/error result. State is file-operation sets and selected message list.
- gates_or_invariants: Tool-result entries are skipped; compaction/branch summaries are included; file ops from generated summaries count even if messages exceed token budget; newest context has priority.
- dependencies_and_callers: Uses compaction utils, prompt md files, telemetry, `instrumentedCompleteSimple`, and session tree navigation.
- edge_cases_or_failure_modes: Missing entry while walking parent chain, no old leaf, no common ancestor, token budget too small, LLM abort/error.
- validation_or_tests: Related to snapcompact/compaction tests; branch summary tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1703 `file` `packages/ai/src/dialect/examples.ts`
- cursor: `[_]`
- core_role: Renders tool examples in the active in-band dialect.
- algorithmic_behavior: For each tool example, builds a synthetic `ToolCall`, injects optional intent placeholder first, renders via dialect `renderToolCall`, and wraps good/bad/note examples in `<examples>`.
- inputs_outputs_state: Inputs are tool examples, dialect id, optional intent field. Outputs are prompt snippets.
- gates_or_invariants: Intent `_i` placeholder must appear first when requested; good/bad examples label wrong/right; empty examples return empty string.
- dependencies_and_callers: Used by `dialect/inventory.ts` to render tool inventory.
- edge_cases_or_failure_modes: Unknown dialect, examples with malformed call args, note-only example formatting.
- validation_or_tests: Indirect via tool inventory/prompt tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1733 `file` `packages/ai/src/providers/error-message.ts`
- cursor: `[_]`
- core_role: Converts provider exceptions into standardized assistant error messages.
- algorithmic_behavior: Builds assistant message with text error content, api/provider/model metadata, zeroed usage/cost, `stopReason: "error"`, and timestamp.
- inputs_outputs_state: Inputs are `Model<Api>` and unknown error. Output is `AssistantMessage`.
- gates_or_invariants: Usage must be zeroed; error text comes from `Error.message` or `String(err)`.
- dependencies_and_callers: Used by provider wrappers when surfacing request failures.
- edge_cases_or_failure_modes: Non-Error throwables, empty message, timestamp nondeterminism.
- validation_or_tests: Indirect through provider error tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1763 `file` `packages/ai/src/providers/vision-guard.ts`
- cursor: `[_]`
- core_role: Guards multimodal message conversion for non-vision/text-only models.
- algorithmic_behavior: Partitions text/image blocks based on `supportsImages`, appends placeholder text when images are omitted, and detects DashScope compatible-mode text-only Qwen families (`qwen*-max`, `qwen*-coder*`).
- inputs_outputs_state: Inputs are content blocks, supports-images flag, OpenAI-compatible model. Outputs are text blocks, image blocks, omitted flag, joined placeholder text, or boolean guard.
- gates_or_invariants: Images are never passed when unsupported; placeholder is stable; DashScope guard requires compatible-mode URL and Qwen model id.
- dependencies_and_callers: Used in provider message conversion, depends on catalog host/identity helpers.
- edge_cases_or_failure_modes: Multimodal Qwen ids without `vl`, custom base URLs, empty text with omitted images.
- validation_or_tests: Issue #1859 likely covered outside assigned tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1793 `file` `packages/ai/src/registry/minimax-code.ts`
- cursor: `[_]`
- core_role: Provider registry descriptor for MiniMax Token Plan.
- algorithmic_behavior: Exports provider definition with lazy OAuth login import.
- inputs_outputs_state: Input is OAuth callbacks; output is OAuth credentials from `loginMiniMaxCode`.
- gates_or_invariants: Lazy import keeps OAuth code out of eager registry graph.
- dependencies_and_callers: Provider registry and auth UI.
- edge_cases_or_failure_modes: Dynamic import failure, OAuth flow failure.
- validation_or_tests: Provider registry tests likely cover descriptor existence.
- skip_candidate: `yes: descriptor glue, minimal algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1823 `file` `packages/ai/src/registry/xai.ts`
- cursor: `[_]`
- core_role: Static provider registry descriptor for xAI.
- algorithmic_behavior: Exports provider id/name.
- inputs_outputs_state: No runtime input beyond import; output is provider definition object.
- gates_or_invariants: Descriptor satisfies `ProviderDefinition`.
- dependencies_and_callers: Provider registry.
- edge_cases_or_failure_modes: Wrong provider id/name.
- validation_or_tests: Registry checks.
- skip_candidate: `yes: static descriptor only`

### OH_MY_HUMANIZE_MAIN-HZ-1853 `file` `packages/ai/src/utils/overflow.ts`
- cursor: `[_]`
- core_role: Context-window overflow detection across providers.
- algorithmic_behavior: Maintains provider-specific regex patterns for overflow errors; `isContextOverflow` checks `stopReason === "error"` plus error message patterns/400-413 no-body forms, then usage-based silent overflow when context window is supplied; exposes pattern copy for tests.
- inputs_outputs_state: Inputs are `AssistantMessage` and optional context window. Output is boolean.
- gates_or_invariants: 429 must not be treated as overflow; usage includes input + cache read/write; `getOverflowPatterns` returns copy.
- dependencies_and_callers: Used by retry/compaction/overflow handling in AI runtime.
- edge_cases_or_failure_modes: Provider wording drift, silent truncation not detectable, false positives in generic token-limit text.
- validation_or_tests: Likely overflow pattern tests outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1883 `file` `packages/catalog/src/identity/markers.ts`
- cursor: `[_]`
- core_role: Shared trailing-marker regex vocabulary for model identity normalization.
- algorithmic_behavior: Builds canonical and reference-only trailing marker regexes from routing/effort/quantization suffix lists.
- inputs_outputs_state: Inputs are model id strings to match elsewhere. Outputs are regex constants.
- gates_or_invariants: `search` is reference-only, not canonical, so Perplexity `sonar-pro-search` remains distinct while proxy metadata can still strip it.
- dependencies_and_callers: Used by catalog identity canonical-id resolution and proxy-reference lookup.
- edge_cases_or_failure_modes: New suffix markers not listed, marker collision with real model id segment.
- validation_or_tests: `identity-family.test.ts` covers related identity behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1913 `file` `packages/coding-agent/src/autoresearch/types.ts`
- cursor: `[_]`
- core_role: Type contract for autoresearch experiment runtime and tools.
- algorithmic_behavior: Defines metrics, experiment results/state, run/log details, pending/running summaries, runtime store/controller interfaces, and tool factory options.
- inputs_outputs_state: Inputs/outputs are typed data exchanged among autoresearch tools, dashboard, runtime store, session entries, and extension API.
- gates_or_invariants: Experiment status/direction values are constrained; metrics maps are numeric; runtime state tracks current/best/last/pending run fields.
- dependencies_and_callers: Consumed by autoresearch mode/tool/dashboard implementations.
- edge_cases_or_failure_modes: Type-only file cannot enforce runtime validation; malformed ASI data may need downstream checks.
- validation_or_tests: Autoresearch tests likely outside assigned set.
- skip_candidate: `yes: type surface, no executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1943 `file` `packages/coding-agent/src/cli/file-processor.ts`
- cursor: `[_]`
- core_role: CLI `@file` argument processor for text, documents, and image attachments.
- algorithmic_behavior: Resolves paths, stats files, detects images, enforces size caps, reads bytes, resizes images unless disabled, converts supported document extensions with Markit, wraps content in `<file name="...">` blocks, and exits on missing/unreadable files.
- inputs_outputs_state: Inputs are file args and auto-resize option. Outputs are concatenated text and `ImageContent[]`.
- gates_or_invariants: Text cap 5MB; image cap 25MB; empty files skipped; convertible ext set includes PDF/Office/RTF/EPUB; missing file exits code 1.
- dependencies_and_callers: CLI startup, image resize, markit conversion, path utils, image metadata.
- edge_cases_or_failure_modes: Large file path-only inclusion, resize failure falls back to original image, binary non-image decoded as text, conversion failure emits error marker.
- validation_or_tests: CLI file attachment tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1973 `file` `packages/coding-agent/src/collab/relay-client.ts`
- cursor: `[_]`
- core_role: Reconnecting encrypted WebSocket client for collab live sharing.
- algorithmic_behavior: Connects to relay with role query, seals outgoing frames in order, buffers up to 256 envelopes while disconnected, opens incoming frames in order, dispatches control JSON or encrypted frames, applies exponential backoff with jitter, and terminates on fatal close/decryption failure.
- inputs_outputs_state: Inputs are `wsUrl`, role, AES key, `CollabFrame`s. Outputs are WebSocket envelopes, `onOpen/onFrame/onControl/onClose` callbacks. State includes socket, retry timer, attempt count, closed flag, send/recv promise chains, pending buffer.
- gates_or_invariants: Fatal close codes never reconnect; bad key/corrupt frame never reconnect; intentional close clears retries and pending sends; send/receive ordering serialized.
- dependencies_and_callers: Uses collab crypto and protocol pack/unpack; used by collab host/guest clients.
- edge_cases_or_failure_modes: Buffer overflow drops frames, malformed control ignored, stale socket events ignored, random backoff timing, decryption failure closes terminally.
- validation_or_tests: Collab integration/harnesses cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2003 `file` `packages/coding-agent/src/commands/web-search.ts`
- cursor: `[_]`
- core_role: CLI command wrapper for testing web search providers.
- algorithmic_behavior: Defines args/flags, joins query args, maps provider/recency/limit/compact flags into `SearchCommandArgs`, and calls `runSearchCommand`.
- inputs_outputs_state: Inputs are CLI query/flags. Outputs are rendered search command output.
- gates_or_invariants: Provider options are `"auto"` plus provider order; recency limited to day/week/month/year; compact flips expanded.
- dependencies_and_callers: CLI command registry, web search CLI/provider order.
- edge_cases_or_failure_modes: Empty query, invalid flag option rejected by CLI parser.
- validation_or_tests: Web search CLI tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2033 `file` `packages/coding-agent/src/dap/types.ts`
- cursor: `[_]`
- core_role: Debug Adapter Protocol type definitions for debug tool/client.
- algorithmic_behavior: Encodes DAP message, request/response/event, capabilities, breakpoints, memory, stack, scopes, variables, modules, sources, session summaries, launch/attach options, and continue outcomes as TypeScript interfaces.
- inputs_outputs_state: Inputs/outputs are typed JSON-RPC-like DAP packets and session state shapes.
- gates_or_invariants: Session status union constrains lifecycle; DAP structures mirror protocol field names.
- dependencies_and_callers: Used by `packages/coding-agent/src/tools/debug.ts` and DAP client/session code.
- edge_cases_or_failure_modes: Type surface may drift from DAP spec; adapters can return extra fields via index signatures.
- validation_or_tests: Debug tests and TypeScript checks.
- skip_candidate: `yes: type surface, no executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2063 `file` `packages/coding-agent/src/discovery/plugin-dir-roots.ts`
- cursor: `[_]`
- core_role: Builds synthetic plugin roots for `--plugin-dir`.
- algorithmic_behavior: Converts resolved local path and optional manifest name into `PluginDirRoot` with id `<name>@__local__`, marketplace `__local__`, version `local`, path, and user scope.
- inputs_outputs_state: Inputs are absolute plugin directory and optional manifest name. Output is root descriptor.
- gates_or_invariants: Manifest name wins; basename fallback; local plugin roots are shape-compatible with registry roots.
- dependencies_and_callers: Plugin discovery/loader manager.
- edge_cases_or_failure_modes: Empty manifest name, basename collisions, scope always user.
- validation_or_tests: Marketplace/plugin discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2093 `file` `packages/coding-agent/src/export/share.ts`
- cursor: `[_]`
- core_role: Secure session sharing pipeline.
- algorithmic_behavior: Builds/redacts session snapshot, generates AES-256-GCM key, gzips+seals JSON as `[12B IV][ciphertext]`, tries secret GitHub gist first, falls back to share server, trims oversized payloads by stripping image payloads, capping long strings at decreasing limits, then dropping oldest entries.
- inputs_outputs_state: Inputs are `SessionManager`, optional agent state/server URL/secret obfuscator. Outputs are share URL, method, gist URL, truncation flag, sealed byte count.
- gates_or_invariants: Server sealed cap 1MB; gist sealed cap 5MB; key stays in URL fragment; gist id must match hex regex; server id must match url-safe length regex; cannot mutate original during fit.
- dependencies_and_callers: Session export/share command, GitHub CLI, share server, HTML export loader.
- edge_cases_or_failure_modes: Unauthenticated `gh`, gist parse failure, upload HTTP failure, session too large even after trimming, data URL images.
- validation_or_tests: Export/share tests likely outside assigned set; HTML export tests cover session data.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2123 `file` `packages/coding-agent/src/internal-urls/local-protocol.ts`
- cursor: `[_]`
- core_role: Session-scoped `local://` internal URL protocol.
- algorithmic_behavior: Parses local URLs, validates relative paths, resolves root from session artifacts or temp fallback, handles Windows long paths via shortened session-id root, lists files recursively, reads resources with content type, and enforces realpath containment against escapes.
- inputs_outputs_state: Inputs are internal URL and resolve context/options. Outputs are `InternalResource` listings or file content. State includes process-global override and AgentRegistry fallback.
- gates_or_invariants: `local://` unavailable without session/options; relative path validation; target and real parent/target must stay within real root; root directory created lazily.
- dependencies_and_callers: Internal URL resolver, eval helpers via `buildEvalUrlRoots`, SDK local protocol options, TUI hyperlink resolution.
- edge_cases_or_failure_modes: Invalid URL encoding, symlink escape, missing file, moved session artifacts, Windows MAX_PATH.
- validation_or_tests: Local protocol/session move tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2153 `file` `packages/coding-agent/src/mcp/index.ts`
- cursor: `[_]`
- core_role: MCP package barrel/public API surface.
- algorithmic_behavior: Re-exports client, config, config writer, JSON-RPC helpers, loader, manager, OAuth discovery, tool bridge/cache, transports, and types.
- inputs_outputs_state: Module imports in, public exports out.
- gates_or_invariants: `callMCP`/`parseSSE` are named exports; other modules are star exported.
- dependencies_and_callers: SDK and coding-agent MCP integration.
- edge_cases_or_failure_modes: Broken re-export path, duplicate ambiguity.
- validation_or_tests: MCP tests/import checks.
- skip_candidate: `yes: API barrel, no runtime algorithm by itself`

### OH_MY_HUMANIZE_MAIN-HZ-2183 `file` `packages/coding-agent/src/modes/image-references.ts`
- cursor: `[_]`
- core_role: Image/paste placeholder parsing and hyperlink materialization.
- algorithmic_behavior: Shifts image markers by offset, renders placeholders via callbacks, wraps image reference labels in file hyperlinks when materialized link exists, writes image blobs async/sync, logs failures, and returns link arrays only when at least one link exists.
- inputs_outputs_state: Inputs are message text, pending images, blob writer, image links. Outputs are rendered strings, file hyperlinks, blob display paths.
- gates_or_invariants: Paste markers are not shifted; marker regex only accepts positive 1-based indices; failures do not abort rendering.
- dependencies_and_callers: TUI/chat rendering, blob store, hyperlink utilities.
- edge_cases_or_failure_modes: Missing image link, invalid base64/write failure, metadata tails, offset zero, duplicate regex global state reset.
- validation_or_tests: Input-controller/image paste tests cover related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2213 `file` `packages/coding-agent/src/session/artifacts.ts`
- cursor: `[_]`
- core_role: Session-scoped artifact file manager for spilled/truncated tool output.
- algorithmic_behavior: Lazily creates artifact dir, scans existing files to initialize next sequential id, sanitizes arbitrary tool names into safe filename segment, allocates paths, writes content, tests existence, lists files, and resolves id to path.
- inputs_outputs_state: Inputs are content/tool type/id. Outputs are artifact ids and paths. State is next id, dir path, created/initialized flags.
- gates_or_invariants: Tool type limited to `[A-Za-z0-9_-]`, max 64 chars, fallback `tool`; existing ids prevent overwrite on resume; file naming `{id}.{toolType}.log`.
- dependencies_and_callers: Streaming output/tool result artifact spill, session manager/subagent artifact adoption.
- edge_cases_or_failure_modes: ENAMETOOLONG prevented by cap, traversal sanitized, missing dir returns empty list, concurrent allocation risk if shared unsafely.
- validation_or_tests: Tool-output hyperlink/export tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2243 `file` `packages/coding-agent/src/slash-commands/available-commands.ts`
- cursor: `[_]`
- core_role: Aggregates slash command availability across built-in, skills, extensions, custom commands, MCP prompts, and files.
- algorithmic_behavior: Builds internal available command list from session capabilities, annotates source, title/description/location, and converts to ACP `AvailableCommand` shape.
- inputs_outputs_state: Inputs are session command sources and active discovery state. Outputs are internal command list and ACP command list.
- gates_or_invariants: Source union is explicit; conversion must preserve command names and descriptions for clients.
- dependencies_and_callers: Slash command UI, ACP command listing, extension get-commands handler.
- edge_cases_or_failure_modes: Duplicate names from multiple sources, missing locations, disabled sources.
- validation_or_tests: Slash command/session tests and extension command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2273 `file` `packages/coding-agent/src/task/render.ts`
- cursor: `[_]`
- core_role: TUI renderer for task/subagent tool calls and results.
- algorithmic_behavior: Formats task ids, call lines, progress rows, agent stats, JSON trees, assignment/context sections, collapsed agents/results, review/findings/yield output, nested task trees with cycle-depth guard, hidden progress summaries, and final result panels.
- inputs_outputs_state: Inputs are `TaskParams`, task details/results/progress, theme, render context, spinner frame. Outputs are TUI `Component`s/lines. State is render context depth/seen tasks and collapsed selection.
- gates_or_invariants: `MAX_NESTED_TASK_RENDER_DEPTH = 8`; missing-yield warning extracted specially; collapsed agent limit 4; task/result ordering normalized; cycle lines prevent infinite nested rendering.
- dependencies_and_callers: Task tool execution UI, collab/export task renderers, report-finding/yield details.
- edge_cases_or_failure_modes: Nested cycles, huge JSON output, missing yield, hidden agents, mixed review/findings formats.
- validation_or_tests: Task/workflow tests likely cover; no focused assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2303 `file` `packages/coding-agent/src/tools/debug.ts`
- cursor: `[_]`
- core_role: Model-facing debug tool over Debug Adapter Protocol.
- algorithmic_behavior: Defines schema/actions, read-only action set, formatting helpers for locations/sessions/breakpoints/frames/threads/scopes/variables/memory/modules/data breakpoints/custom responses, renderer summaries, capability checks, launch program classification, and `DebugTool` execution dispatch.
- inputs_outputs_state: Inputs are debug action params, DAP session state, launch/attach/breakpoint/eval/memory args. Outputs are formatted text/details or DAP side effects. State depends on active DAP session summary/capabilities.
- gates_or_invariants: Read-only actions separated; capability checks throw for unsupported DAP features; launch program validation classifies source/binary/missing; active session required for session actions.
- dependencies_and_callers: DAP manager/client/types, tool renderer, agent tool runtime.
- edge_cases_or_failure_modes: No active session, unsupported adapter capability, missing launch program, custom command unknown response, unreadable memory bytes.
- validation_or_tests: Raw SSE debug buffer and debug-related tests cover adjacent behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2333 `file` `packages/coding-agent/src/tools/memory-reflect.ts`
- cursor: `[_]`
- core_role: Long-term memory reflection tool.
- algorithmic_behavior: Loads only when memory backend is `hindsight` or `mnemopi`; for mnemopi, combines query/context, recalls scoped results, formats context; for hindsight, ensures bank exists then calls reflect with budget/tags; wraps in abort handling and logs backend-specific failures.
- inputs_outputs_state: Inputs are query/context params, session memory backend/state, abort signal. Outputs are text answer/no-info result or error.
- gates_or_invariants: Backend state must be initialized; tool approval is read; strict schema; empty recall returns stable no-info text.
- dependencies_and_callers: Hindsight bank/client, mnemopi session state, settings.
- edge_cases_or_failure_modes: Backend disabled/uninitialized, bank creation failure, recall/reflect failure, abort.
- validation_or_tests: Memory tool tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2363 `file` `packages/coding-agent/src/tts/tts-client.ts`
- cursor: `[_]`
- core_role: TTS worker client/subprocess manager.
- algorithmic_behavior: Reads tiny model settings into env, resolves worker spawn command using worker host entry/fallback, spawns subprocess, wraps inbound/outbound queues/errors, streams audio chunks through `AudioChunkChannel`, exposes synthesize/download/stream APIs, handles pending request correlation, shutdown, and smoke test timeout.
- inputs_outputs_state: Inputs are synthesize/download/stream options and text/audio requests. Outputs are audio buffers/chunks, stream handles, worker logs/errors. State includes worker handle, pending request map, chunk queues, request ids, closed/error flags.
- gates_or_invariants: Worker arg is `__omp_worker_tts`; smoke timeout 30s; chunk channel delivers queued chunks or waits via resolvers; spawn fallback used outside CLI host; env maps tiny dtype/device.
- dependencies_and_callers: CLI worker host contract, tiny inference/TTS worker, settings, logger.
- edge_cases_or_failure_modes: Worker unavailable inline fallback, subprocess exit, pending request rejection, stream abort, dtype misconfiguration.
- validation_or_tests: `tiny-dtype.test.ts`, smoke tests, TTSR CLI adjacent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2393 `file` `packages/coding-agent/src/utils/jj.ts`
- cursor: `[_]`
- core_role: Jujutsu (`jj`) repository utility layer.
- algorithmic_behavior: Checks binary availability, runs `jj` commands with cwd/env, formats command failures, builds diff args, detects workspace root by walking parents for `.jj`, caches roots in LRU, resolves repo dir, and exposes `diff` plus `repo` helpers.
- inputs_outputs_state: Inputs are cwd, diff options, jj args. Outputs are command results/text, repository info, booleans, diffs. State is availability and workspace-root cache.
- gates_or_invariants: Missing `jj` throws `JjCommandError`; cache max 256; workspace metadata detection uses parent walk; command failures include stderr/stdout details.
- dependencies_and_callers: Bundled review command, VCS status/diff features.
- edge_cases_or_failure_modes: `jj` absent, detached workspace, command timeout/failure, cache stale after moving dirs.
- validation_or_tests: Review command tests assert JJ diff preference.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2423 `file` `packages/coding-agent/src/workflow/liveness.ts`
- cursor: `[_]`
- core_role: Workflow liveness guard for script-only cycles.
- algorithmic_behavior: Detects strongly connected component around a script node by forward/reverse reachability; if cyclic component is all script nodes, scans recent completed activations in that cycle and reports diagnostic after four consecutive activations without state patches/artifacts.
- inputs_outputs_state: Inputs are workflow definition, node, completed activations. Output is optional diagnostic with node id, cycle ids, stalled activation ids, message.
- gates_or_invariants: Non-script nodes are ignored; mixed cycles are ignored; window threshold is 4; activations with patches/artifacts count as progress.
- dependencies_and_callers: Workflow scheduler/executor.
- edge_cases_or_failure_modes: Self-loop cycles, missing node id, activation status not completed, agent/review/human progress not checked here beyond output artifacts/state.
- validation_or_tests: `packages/coding-agent/test/workflow/human-tool-runtime.test.ts` adjacent; liveness-specific tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2453 `file` `packages/coding-agent/test/core/block-replace.test.ts`
- cursor: `[_]`
- core_role: End-to-end tests for SWAP.BLK native tree-sitter block replacement.
- algorithmic_behavior: Creates temp files/session/options, seeds TypeScript/Elisp source, executes hashline/block replacement, and asserts native tree-sitter resolution boundaries.
- inputs_outputs_state: Inputs are source files and replacement commands. Outputs are file content changes/results.
- gates_or_invariants: Block selection must respect syntax node boundaries and language support.
- dependencies_and_callers: Tests core edit/hashline/tree-sitter integration.
- edge_cases_or_failure_modes: Nested blocks, empty blocks, language grammar differences.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2483 `file` `packages/coding-agent/test/debug/raw-sse-buffer.test.ts`
- cursor: `[_]`
- core_role: Tests raw SSE debug buffer.
- algorithmic_behavior: Builds model fixture and asserts buffer captures/limits raw SSE events for debug output.
- inputs_outputs_state: Inputs are SSE chunks/model. Outputs are debug buffer content.
- gates_or_invariants: Raw stream bytes/events should remain inspectable without corrupting assistant message parsing.
- dependencies_and_callers: Tests debug support around AI streaming.
- edge_cases_or_failure_modes: Partial SSE frames, buffer truncation, non-UTF8-ish content.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2513 `file` `packages/coding-agent/test/export/html-workflow-export.test.ts`
- cursor: `[_]`
- core_role: Tests HTML export support for workflow inspection.
- algorithmic_behavior: Builds workflow source/session data/freezes, exports HTML, decodes embedded session data, and asserts workflow resources/freeze/node ids are present.
- inputs_outputs_state: Inputs are synthetic workflow session entries/freezes. Outputs are exported HTML and decoded session JSON.
- gates_or_invariants: Export must preserve workflow inspection data and not break embedded payload decoding.
- dependencies_and_callers: Tests export HTML pipeline and workflow serialization.
- edge_cases_or_failure_modes: Missing resource text, multiple node ids, base64/JSON encoding drift.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2543 `file` `packages/coding-agent/test/marketplace/discovery.test.ts`
- cursor: `[_]`
- core_role: Tests plugin marketplace discovery/registry compatibility.
- algorithmic_behavior: Validates OMP registry path contract, Claude-compatible registry format, registry round-trip, and precedence structure using installed plugin entries.
- inputs_outputs_state: Inputs are registry content/entries/install paths. Outputs are parsed registries and precedence assertions.
- gates_or_invariants: OMP registry must remain compatible with Claude parser expectations and preserve precedence.
- dependencies_and_callers: Tests `extensibility/plugins/marketplace` registry/manager.
- edge_cases_or_failure_modes: Invalid JSON, missing fields, path precedence conflict.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2573 `file` `packages/coding-agent/test/session-manager/rewrite-rename-eperm.test.ts`
- cursor: `[_]`
- core_role: Tests session rewrite fallback on Windows-like EPERM rename failures.
- algorithmic_behavior: Custom storage throws EPERM once on rename; tests replacement fallback, rollback failure, and orphaned backup recovery.
- inputs_outputs_state: Inputs are session files/storage errors. Outputs are final session file content/backups/recovery results.
- gates_or_invariants: Rewrite must preserve data despite rename EPERM; backups recovered safely; rollback failures surfaced.
- dependencies_and_callers: Tests `FileSessionStorage`/session manager rewrite.
- edge_cases_or_failure_modes: EPERM once, rollback failure, orphaned backup files.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2603 `file` `packages/coding-agent/test/slash-commands/session.test.ts`
- cursor: `[_]`
- core_role: Tests `/session` slash command runtime harness.
- algorithmic_behavior: Creates runtime harness and asserts session command behavior in available contexts.
- inputs_outputs_state: Inputs are harness options/session state. Outputs are slash command results/actions.
- gates_or_invariants: Session command should surface correct session-management actions without corrupting state.
- dependencies_and_callers: Tests slash command implementation.
- edge_cases_or_failure_modes: Missing session, invalid subcommand, UI/no-UI mode.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2633 `file` `packages/coding-agent/test/tool-discovery/initial-tools.test.ts`
- cursor: `[_]`
- core_role: Tests initial built-in tool discovery mode.
- algorithmic_behavior: Reads public factory metadata, computes essential builtin tool names, validates settings schema, and filters initial tools when discovery is all.
- inputs_outputs_state: Inputs are settings/tool session and built-in map. Outputs are metadata maps and filtered tool sets.
- gates_or_invariants: Built-in tools must expose loadMode/summary annotations; essential tool set must remain stable; discovery settings schema valid.
- dependencies_and_callers: Tests tool discovery system.
- edge_cases_or_failure_modes: Missing metadata annotation, wrong discoverability, settings schema drift.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2663 `file` `packages/coding-agent/test/tools/eval-description.test.ts`
- cursor: `[_]`
- core_role: Tests eval tool description variation.
- algorithmic_behavior: Creates fake session with/without spawns and asserts eval tool description changes to reflect runtime availability.
- inputs_outputs_state: Inputs are session spawn capability. Outputs are model-facing description text.
- gates_or_invariants: Description must not advertise unavailable execution path incorrectly.
- dependencies_and_callers: Tests eval tool factory/description.
- edge_cases_or_failure_modes: Null spawns, stale description.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2693 `file` `packages/coding-agent/test/tools/output-schema-validator.test.ts`
- cursor: `[_]`
- core_role: Tests output schema validation and failure formatting.
- algorithmic_behavior: Exercises validator construction, validation failure summarization, headline formatting, all-issue formatting, required-field extraction and missing-required computation.
- inputs_outputs_state: Inputs are JSON schemas and candidate outputs. Outputs are validation functions/issues/headlines.
- gates_or_invariants: Missing required fields and schema errors must produce user-readable, deterministic summaries.
- dependencies_and_callers: Tests tool output schema validator.
- edge_cases_or_failure_modes: Nested required fields, multiple issues, invalid schema shape.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2723 `file` `packages/coding-agent/test/tools/tool-output-hyperlinks.test.ts`
- cursor: `[_]`
- core_role: Tests OSC 8 file hyperlinks in tool output.
- algorithmic_behavior: Creates test session, emits image/file outputs, extracts OSC 8 URIs, and asserts hyperlinks point to accessible local/artifact paths.
- inputs_outputs_state: Inputs are tiny PNG data and tool session cwd/artifacts. Outputs are rendered text with OSC 8 links.
- gates_or_invariants: File hyperlinks must be safe and useful; artifact/image links must be materialized.
- dependencies_and_callers: Tests tool render/output hyperlink utilities, artifact manager, image references.
- edge_cases_or_failure_modes: Missing artifact, invalid image, URI escaping.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2753 `file` `packages/coding-agent/test/workflow/human-tool-runtime.test.ts`
- cursor: `[_]`
- core_role: Tests workflow human input ask tool runtime adapter.
- algorithmic_behavior: Creates tool session/context with UI and asserts human `ask` tool integrates with workflow runtime.
- inputs_outputs_state: Inputs are UI context and ask params. Outputs are tool result/user response.
- gates_or_invariants: Human input must route through UI adapter and preserve cancellation semantics.
- dependencies_and_callers: Tests workflow human tool adapter.
- edge_cases_or_failure_modes: No UI, cancellation, empty response.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2783 `file` `packages/collab-web/src/tool-render/registry.ts`
- cursor: `[_]`
- core_role: Tool renderer lookup registry for collab/export UI.
- algorithmic_behavior: Imports renderer modules, maps wire tool names and aliases (`puppeteer`, `apply_patch`, `grep`, `await`, `js`, etc.) to renderers, and falls back to generic renderer.
- inputs_outputs_state: Input is tool name. Output is `ToolRenderer`.
- gates_or_invariants: Unknown names never fail; aliases keep legacy records renderable.
- dependencies_and_callers: `ToolView.tsx` and web component/export render surfaces.
- edge_cases_or_failure_modes: New tool without renderer falls back to generic; alias collision.
- validation_or_tests: HTML export/tool renderer tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2813 `file` `packages/mnemopi/src/core/streaming.ts`
- cursor: `[_]`
- core_role: Memory event streaming and delta synchronization subsystem.
- algorithmic_behavior: Defines `MemoryEvent`, `MemoryStream`, async iterator delivery, buffered event retrieval, `SyncCheckpoint`, and `DeltaSync` for allowed memory tables. Delta sync computes rows since checkpoint, applies inserts/updates with column allowlists and SQL binding validation, and saves per-peer/table checkpoints.
- inputs_outputs_state: Inputs are memory events, callbacks, SQLite DB rows, peer ids, delta rows. Outputs are emitted events, async iteration results, checkpoints, delta arrays, insert/update/skipped stats.
- gates_or_invariants: Event type and memory id required; buffer max trims oldest; delta tables allowlisted; update/insert columns allowlisted; insert requires content; unsupported SQL binding values filtered.
- dependencies_and_callers: Mnemopi Beam memory, plugin/event consumers, peer sync.
- edge_cases_or_failure_modes: Unknown event type, missing DB, invalid table, skipped rows without id/content, legacy checkpoint path for working memory, callback exceptions swallowed.
- validation_or_tests: Mnemopi plugin/configurable scoring tests cover adjacent memory behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2843 `file` `packages/swarm-extension/src/swarm/state.ts`
- cursor: `[_]`
- core_role: Filesystem-backed state tracker for swarm pipeline execution.
- algorithmic_behavior: Initializes `.swarm_<name>/state|logs|context`, creates per-agent state, persists pipeline JSON, updates agents/pipeline, appends timestamped logs, and loads existing state.
- inputs_outputs_state: Inputs are workspace/name/agent names/mode/target count/state updates/log messages. Outputs are directories, JSON state, log files, loaded state.
- gates_or_invariants: Missing agent update is ignored; load returns null on any read/parse failure; persist writes full state JSON.
- dependencies_and_callers: Swarm extension orchestrator.
- edge_cases_or_failure_modes: Concurrent updates overwrite, malformed saved JSON, filesystem errors.
- validation_or_tests: Swarm tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2873 `file` `python/robomp/web/src/api.ts`
- cursor: `[_]`
- core_role: Frontend API wrapper for robomp dashboard.
- algorithmic_behavior: Wraps fetch calls to status/logs/browse/trigger/cancel endpoints, adds auth/JSON headers, parses JSON when possible, extracts error details, and throws `ApiError` on non-OK responses.
- inputs_outputs_state: Inputs are request params, abort signals, delivery ids. Outputs are typed response promises or `ApiError`.
- gates_or_invariants: Error detail preference is `detail`, then `message`, then status text; auth headers copied per request; trigger body mode constrained to triage/retry.
- dependencies_and_callers: Robomp web UI.
- edge_cases_or_failure_modes: Non-JSON 2xx returns `null as T`, non-JSON error uses status text, network errors propagate.
- validation_or_tests: Frontend tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2903 `file` `crates/pi-shell/src/minimizer/filters/cpp.rs`
- cursor: `[_]`
- core_role: Output minimizer filter for CMake/CTest/Ninja/GoogleTest.
- algorithmic_behavior: Detects tools by program or command token, strips ANSI, routes to tool-specific filters, removes build/pass noise while preserving important errors/warnings/failure context, deduplicates consecutive lines, and head-tail truncates.
- inputs_outputs_state: Inputs are minimizer context, raw output, exit code. Outputs are `MinimizerOutput` transformed/passthrough text.
- gates_or_invariants: On failed exit, important lines are retained; empty successful output becomes concise `cmake: ok`/`ctest: ok`/`ninja: ok`/`gtest: ok`; gtest failure context stays until summary/noise reset.
- dependencies_and_callers: `pi-shell` shell execution minimizer.
- edge_cases_or_failure_modes: Bun-wrapped commands, gtest binary name detection, `ninja: no work to do` retained, source-location heuristics.
- validation_or_tests: Inline Rust tests cover support detection and CMake/CTest/GTest filtering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2933 `file` `packages/ai/src/registry/oauth/google-gemini-cli.ts`
- cursor: `[_]`
- core_role: Google Gemini CLI OAuth flow and Code Assist project discovery.
- algorithmic_behavior: Uses fixed OAuth client/scopes/callback; discovers/provisions Cloud Code Assist project by calling loadCodeAssist/onboardUser, handles VPC-SC affected users, polls long-running operations, requires env project for non-free tiers, and refreshes tokens via OAuth token endpoint.
- inputs_outputs_state: Inputs are OAuth controller, access/refresh tokens, env project ids, Code Assist API responses. Outputs are `OAuthCredentials` with project id/access/refresh/expiry.
- gates_or_invariants: Free/legacy default tier fallback; non-free tier requires `GOOGLE_CLOUD_PROJECT(_ID)`; expiry subtracts five minutes; VPC-SC security policy maps to standard tier.
- dependencies_and_callers: Provider OAuth registry, Google shared OAuth helper, Gemini CLI headers.
- edge_cases_or_failure_modes: load/onboard/poll HTTP errors, missing project id, operation never done, refresh failure.
- validation_or_tests: OAuth/provider tests around Google/Gemini likely cover; issue #1270 covers Google auth adjacent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2963 `file` `packages/catalog/src/discovery/cursor-gen/agent_pb.ts`
- cursor: `[_]`
- core_role: Generated protobuf TypeScript descriptors for Cursor/agent discovery protocol.
- algorithmic_behavior: Declares hundreds of generated message/enum/service descriptors, including tool call/result messages, exec/file/artifact/control/lifecycle service schemas.
- inputs_outputs_state: Inputs are generated protobuf schema at build time; runtime output is descriptor constants/types consumed by discovery/client code.
- gates_or_invariants: Must match upstream `.proto`; manual edits would be overwritten.
- dependencies_and_callers: Catalog discovery Cursor integration and generated protobuf runtime.
- edge_cases_or_failure_modes: Upstream proto drift, generated file too large for manual review, descriptor mismatch.
- validation_or_tests: Generation/type checks; no manual algorithm test.
- skip_candidate: `yes: generated protocol surface, not hand-authored core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2993 `file` `packages/coding-agent/src/commit/analysis/summary.ts`
- cursor: `[_]`
- core_role: LLM-assisted conventional commit summary generator.
- algorithmic_behavior: Renders static prompt templates, sends `completeSimple` with `create_commit_summary` tool schema, parses tool call if present via `validateToolCall`, otherwise extracts text, and strips conventional type/scope prefix.
- inputs_outputs_state: Inputs are model/api key/thinking level, commit type/scope, details, stat, max chars, optional user context. Output is `CommitSummary`.
- gates_or_invariants: Summary tool schema requires string; max tokens fixed at 200; prefix stripping handles `type(scope): ` and `type: `.
- dependencies_and_callers: Commit analysis pipeline, prompt md files, AI completion, thinking effort conversion.
- edge_cases_or_failure_modes: Model ignores tool, invalid tool args, overlong summary if model disobeys, prefix with different casing not stripped.
- validation_or_tests: Commit summary tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3023 `file` `packages/coding-agent/src/eval/__tests__/idle-timeout.test.ts`
- cursor: `[_]`
- core_role: Tests idle timeout abort behavior.
- algorithmic_behavior: Uses helper `abortedWithin` to assert `IdleTimeout` aborts after inactivity and resets/clears when signaled.
- inputs_outputs_state: Inputs are abort signal and timeout ms. Outputs are abort booleans.
- gates_or_invariants: Idle timer must abort within configured window and not leak timers after cleanup.
- dependencies_and_callers: Tests eval idle timeout class.
- edge_cases_or_failure_modes: Timer flake, abort signal already aborted, reset race.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3053 `file` `packages/coding-agent/src/extensibility/custom-tools/wrapper.ts`
- cursor: `[_]`
- core_role: Adapter from custom tool API to agent runtime `AgentTool`.
- algorithmic_behavior: Applies tool proxy metadata to adapter, copies strict flag, and forwards execute calls with toolCallId/params/update/context/signal in custom-tool expected argument order; exposes static `wrap`.
- inputs_outputs_state: Inputs are `CustomTool` and context provider. Output is `AgentTool`.
- gates_or_invariants: Caller-provided context overrides default context; proxy exposes name/label/description/parameters.
- dependencies_and_callers: Custom tools loader/runtime.
- edge_cases_or_failure_modes: Custom tool throws, missing context provider, legacy type uses `any` for details.
- validation_or_tests: Custom tool tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3083 `file` `packages/coding-agent/src/markit/converters/docx.ts`
- cursor: `[_]`
- core_role: DOCX-to-Markdown converter.
- algorithmic_behavior: Accepts `.docx` extension or DOCX mimetype, uses Mammoth to convert to HTML, writes images to `imageDir` when provided or creates placeholder data URIs otherwise, converts normalized tables HTML through Turndown, and replaces data URI images with comments when no image dir.
- inputs_outputs_state: Inputs are DOCX buffer and stream info. Outputs are markdown and optional image files.
- gates_or_invariants: Image filenames increment; JPEG extension normalized to jpg; markdown is trimmed.
- dependencies_and_callers: Markit conversion used by CLI file processor and document fetch/conversion.
- edge_cases_or_failure_modes: Mammoth conversion failure, unsupported embedded image type, missing image dir, data URI intentionally empty.
- validation_or_tests: Markit tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3113 `file` `packages/coding-agent/src/modes/components/custom-message.ts`
- cursor: `[_]`
- core_role: TUI component for extension custom message entries.
- algorithmic_behavior: Maintains a box/default component, tracks expanded state, rebuilds by invoking `renderFramedMessage` with optional custom renderer, swaps child component on invalidate/expand changes.
- inputs_outputs_state: Inputs are custom message and renderer. Output is TUI container child tree.
- gates_or_invariants: Extension messages render full content without collapse-on-fold behavior; old custom component removed before rebuild.
- dependencies_and_callers: Interactive mode message rendering for extensions.
- edge_cases_or_failure_modes: Renderer returns custom component vs fallback, repeated invalidation, stale child removal.
- validation_or_tests: Extension/custom message tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3143 `file` `packages/coding-agent/src/modes/components/segment-track.ts`
- cursor: `[_]`
- core_role: Shared colored segment-track renderer for status/selector UI.
- algorithmic_behavior: Resolves distinct theme colors by ANSI dedupe, then renders labels with active segment as filled powerline chip and inactive as colored text separated by thin separators.
- inputs_outputs_state: Inputs are segments and active index. Output is ANSI-styled one-line string.
- gates_or_invariants: Palette never empty because accent resolves; callers wrap colors modulo palette length; active chip uses contrast foreground.
- dependencies_and_callers: Plan-mode model-tier slider and role-cycle status UI.
- edge_cases_or_failure_modes: Active index out of range still produces no active chip or odd modulo behavior; monochrome themes reduce palette.
- validation_or_tests: UI snapshot tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3173 `file` `packages/coding-agent/src/modes/controllers/omfg-rule.ts`
- cursor: `[_]`
- core_role: Parser/validator for generated OMFG/TTSR rules.
- algorithmic_behavior: Extracts balanced JSON from fenced/free text, validates payload fields, sanitizes rule names, normalizes/repairs regex conditions, assembles markdown frontmatter/body, builds `Rule`, validates through `TtsrManager`, checks candidate rule against assistant text/thinking/tool-call argument surfaces, repairs double-escaped regexes, and builds feedback for no-match/scope problems.
- inputs_outputs_state: Inputs are generated LLM text, rule source path/level, assistant message history. Outputs are parsed rule/file content, validation matched flag/feedback, repaired candidate flag.
- gates_or_invariants: Name/description/condition/scope/body required; rule name must contain alphanumeric after sanitization; at least one valid condition and reachable scope; tool-specific scope recommended when matching serialized file tool args.
- dependencies_and_callers: Discovery rule helpers, TTSR manager, assistant history messages, OMFG rule generation UI.
- edge_cases_or_failure_modes: Invalid JSON/fence, braces inside strings handled, invalid regex repair once, tool arg JSON stringify failure, broad `tool`/`text` scope false positives, duplicate condition/scope entries.
- validation_or_tests: TTSR CLI tests cover rule matching; OMFG-specific tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3203 `file` `packages/coding-agent/src/slash-commands/helpers/logout.ts`
- cursor: `[_]`
- core_role: Formats stored auth credentials into selectable logout accounts.
- algorithmic_behavior: Builds labels/details for OAuth/API-key rows, detects active OAuth identity by account/email/project, marks active API key by flag, and sorts active first then label/id.
- inputs_outputs_state: Inputs are provider id, stored credentials, active identity/api-key options. Outputs are `LogoutAccount[]`.
- gates_or_invariants: OAuth label preference email -> accountId -> projectId -> enterpriseUrl -> fallback; active rows sort first.
- dependencies_and_callers: `/logout` slash command/UI.
- edge_cases_or_failure_modes: Missing credential fields, multiple active matches, API key labels.
- validation_or_tests: Logout tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3233 `file` `packages/coding-agent/src/web/scrapers/clojars.ts`
- cursor: `[_]`
- core_role: Special web-fetch handler for Clojars artifact pages.
- algorithmic_behavior: Recognizes clojars host/path, converts group/artifact path to API URL, fetches JSON, normalizes multiple possible payload field names, formats licenses/dependencies/downloads/homepage into markdown, and returns `RenderResult`.
- inputs_outputs_state: Inputs are URL, timeout, abort signal. Outputs are markdown result or `null` to let generic fetch proceed.
- gates_or_invariants: Only 1-2 path segments accepted; JSON response must parse to record/first array element; notes mark Clojars API path.
- dependencies_and_callers: Web fetch scraper dispatcher, shared `loadPage/buildResult`.
- edge_cases_or_failure_modes: API schema variation, missing artifact, dependency formats as string/array/object, errors swallowed to `null`.
- validation_or_tests: Web scraper tests cover StackExchange; Clojars likely manual/indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3263 `file` `packages/coding-agent/src/web/scrapers/npm.ts`
- cursor: `[_]`
- core_role: Special web-fetch handler for npm package pages.
- algorithmic_behavior: Recognizes npm package URLs, extracts scoped/unscoped package name, fetches registry `/latest` and last-week downloads in parallel, parses JSON, formats package metadata/dependencies/readme into markdown, and returns `RenderResult`.
- inputs_outputs_state: Inputs are URL, timeout, abort signal. Outputs are markdown result or `null`.
- gates_or_invariants: Only `/package/...` paths; latest registry fetch must succeed; downloads timeout capped to 5s.
- dependencies_and_callers: Web fetch scraper dispatcher, `tryParseJson`, `loadPage`, `buildResult`.
- edge_cases_or_failure_modes: Scoped package path parsing, missing downloads, repository field string/object, errors swallowed.
- validation_or_tests: Web scraper tests likely cover dispatcher behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3293 `file` `packages/coding-agent/src/web/scrapers/types.ts`
- cursor: `[_]`
- core_role: Shared web-fetch scraper utilities and HTTP loader.
- algorithmic_behavior: Defines result/handler types, output/byte caps, user-agent retry ladder, bot-block detection, Retry-After parsing, charset/meta decoding, bounded body streaming, HTML-to-Markdown via lazy Turndown, result builder, date/entity/duration/localized text helpers.
- inputs_outputs_state: Inputs are URLs/load options, response bodies, HTML strings. Outputs are `LoadPageResult`, markdown `RenderResult`, formatted strings.
- gates_or_invariants: Max output 500k chars; max body 50MB; one 429 retry with bounded Retry-After; Accept-Encoding forced identity; body can be skipped by content type; abort throws `ToolAbortError`.
- dependencies_and_callers: Fetch tool/web scrapers (`npm`, `clojars`, StackExchange, etc.).
- edge_cases_or_failure_modes: Cloudflare/bot blocks, unsupported charset fallback, stream truncation, no response body, turndown lazy import failure.
- validation_or_tests: `packages/coding-agent/test/tools/web-scrapers/stackexchange.test.ts` covers scraper integration style.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3323 `file` `packages/coding-agent/test/modes/components/oauth-selector.test.ts`
- cursor: `[_]`
- core_role: Tests OAuth selector component behavior.
- algorithmic_behavior: Uses fake auth storage and asserts selector state/rendering around OAuth credential choices.
- inputs_outputs_state: Inputs are credential rows/provider state. Outputs are selected account/render state.
- gates_or_invariants: OAuth selector should identify stored credentials and active selection consistently.
- dependencies_and_callers: Tests OAuth selector TUI component.
- edge_cases_or_failure_modes: No credentials, active credential missing, multiple providers.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3353 `file` `packages/coding-agent/test/modes/controllers/event-controller-read-grouping.test.ts`
- cursor: `[_]`
- core_role: Tests EventController read-tool grouping in chat UI.
- algorithmic_behavior: Streams assistant content with read tool calls/thinking blocks, then inspects `ReadToolGroupComponent`s and headers for grouping/accretion behavior.
- inputs_outputs_state: Inputs are assistant message block sequences. Outputs are chat container child groups/headers.
- gates_or_invariants: Read calls should group/accrete coherently across streamed assistant content without losing intervening thinking.
- dependencies_and_callers: Tests interactive EventController and read group component.
- edge_cases_or_failure_modes: Multiple read blocks, thinking interleaving, stream completion timing.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3383 `file` `packages/coding-agent/test/tools/web-scrapers/stackexchange.test.ts`
- cursor: `[_]`
- core_role: Integration test for StackExchange web scraper.
- algorithmic_behavior: Gated by `WEB_FETCH_INTEGRATION`, fetches StackExchange pages and asserts special scraper output.
- inputs_outputs_state: Inputs are live web URLs/env gate. Outputs are rendered markdown/result assertions.
- gates_or_invariants: Test skipped unless env set; scraper must handle live page shape.
- dependencies_and_callers: Tests web fetch scraper stack.
- edge_cases_or_failure_modes: Network/site markup changes, bot blocks.
- validation_or_tests: This file is the validation.
- skip_candidate: `yes: live integration test, not core implementation`

### OH_MY_HUMANIZE_MAIN-HZ-3413 `file` `packages/collab-web/src/tool-render/tools/fetch.tsx`
- cursor: `[_]`
- core_role: Collab/export renderer for fetch tool calls.
- algorithmic_behavior: Extracts fetch details from result details, renders summary URL/method/raw/truncated badges, body key/value metadata, and markdown result text.
- inputs_outputs_state: Inputs are args (`url`/`path`, method, raw, timeout) and result details/content. Outputs are React nodes.
- gates_or_invariants: Missing URL renders invalid arg; method badge omitted for GET; final URL shown only on redirect; result text max 12 lines.
- dependencies_and_callers: Tool render registry and ToolView.
- edge_cases_or_failure_modes: Details absent/malformed, notes non-string, path alias, truncated flag.
- validation_or_tests: Collab/web export visual tests likely indirect.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3443 `file` `packages/mnemopi/src/core/beam/types.ts`
- cursor: `[_]`
- core_role: Type contract for Beam memory core.
- algorithmic_behavior: Defines JSON metadata, memory scope/trust/veracity, plugin/annotation/triple interfaces, config, state, remember/recall options, memory row shapes, recall results/voice scores, stats/import/sleep result types.
- inputs_outputs_state: Inputs/outputs are typed memory operations and recall rows shared by Beam implementation.
- gates_or_invariants: Distinguishes working vs episodic rows, recall tier labels, and configurable scoring weights.
- dependencies_and_callers: Beam memory implementation, tests, plugins, streaming sync.
- edge_cases_or_failure_modes: Type-only; runtime must validate DB rows and metadata separately.
- validation_or_tests: Mnemopi tests exercise implementations using these types.
- skip_candidate: `yes: type definitions, not executable algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3473 `file` `packages/stats/src/client/ui/DataTable.tsx`
- cursor: `[_]`
- core_role: Generic responsive stats table component.
- algorithmic_behavior: Renders empty state, optional mobile card list, desktop table headers/cells, numeric alignment, clickable row behavior with Enter/Space keyboard activation.
- inputs_outputs_state: Inputs are column definitions, data, key extractor, row click/mobile render callbacks. Outputs are React DOM table/cards.
- gates_or_invariants: Empty data returns empty div; clickable rows get role button/tabIndex; default cell render indexes item by column key.
- dependencies_and_callers: Stats dashboard UI.
- edge_cases_or_failure_modes: Duplicate keys, missing render for non-renderable object values, mobile/desktop CSS dependence.
- validation_or_tests: UI tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3503 `directory` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes`
- cursor: `[_]`
- core_role: Vendor ASCII diagram shape rendering subsystem.
- algorithmic_behavior: Provides pluggable shape registry, shared box dimension/render/attachment logic, corner lookup table, and renderers for rectangle, rounded, diamond, hexagon, circle, stadium, subroutine, doublecircle, cylinder, asymmetric, trapezoids, and UML state start/end.
- inputs_outputs_state: Inputs are node label, dimensions/options, direction/base coordinate. Outputs are ASCII canvas/node attachment coordinates. State is static `shapeRegistry`.
- gates_or_invariants: Shape renderers expose consistent `getDimensions`, `render`, `getAttachmentPoint`; registry falls back to rectangle; corner characters switch ASCII/Unicode.
- dependencies_and_callers: Mermaid ASCII renderer/pathfinder under utils vendor tree.
- edge_cases_or_failure_modes: Wide labels/display width, multi-line stadium/cylinder custom layouts, attachment point direction matching, fallback for unknown shapes.
- validation_or_tests: Vendor package tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3533 `file` `packages/coding-agent/src/markit/converters/pdf/extract.ts`
- cursor: `[_]`
- core_role: PDF extraction engine for Markit conversion.
- algorithmic_behavior: Lazily loads MuPDF, extracts structured text boxes, merges glyphs into words by line/gap tolerances, extracts thin rectangle line segments from page drawings/content streams with CTM transforms/tokenizer, detects image regions, renders cropped image regions, and returns per-page content.
- inputs_outputs_state: Inputs are PDF bytes. Outputs are `PageContent[]`, text boxes, segments, image regions, rendered PNG bytes. State is MuPDF module promise and per-page parsing accumulators.
- gates_or_invariants: Same-line tolerance, merge gap, line aspect/thickness/min length, min image area, CTM stack transformations; tokenizer must preserve PDF operators/strings enough for segment extraction.
- dependencies_and_callers: Markit PDF converter.
- edge_cases_or_failure_modes: Corrupt PDF, unsupported content stream operators, rotated/transformed graphics, huge images, MuPDF load failure.
- validation_or_tests: PDF converter tests likely outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3563 `file` `packages/coding-agent/src/tools/browser/cmux/cmux-tab.ts`
- cursor: `[_]`
- core_role: Browser tab automation facade for cmux/browser tool.
- algorithmic_behavior: Maintains selector helpers injected into page, caches element refs, supports navigation/observe/screenshot/click/type/fill/drag/upload/evaluate-like JS execution, response observation, viewport options, Puppeteer-like `page`/`browser` facades, safe result serialization, and display capture.
- inputs_outputs_state: Inputs are browser tab commands, selectors, JS code, file payloads, run options. Outputs are run results, displays, screenshots, element handles/responses. State includes tab page, cached refs, response records, run context.
- gates_or_invariants: Selector kinds include css/ref/text/aria/xpath/pierce/ax; result cloning/stringifying must be safe; response observer records fetch/XHR; facades restrict exposed API.
- dependencies_and_callers: Browser tool/cmux execution, eval display pipeline.
- edge_cases_or_failure_modes: Stale element refs, shadow DOM piercing, invisible elements, unserializable JS values, file payload decoding, page navigation races.
- validation_or_tests: Browser tool tests likely elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3593 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/pathfinder.ts`
- cursor: `[_]`
- core_role: A* pathfinding for ASCII diagram edge routing.
- algorithmic_behavior: Implements min-heap priority queue, Manhattan heuristic with corner penalty, grid occupancy checks, A* search through four-direction moves, parent reconstruction, and `mergePath` simplification by removing collinear/intermediate points.
- inputs_outputs_state: Inputs are grid/node occupancy map, start/end coordinates. Outputs are path coordinate array or null, merged path.
- gates_or_invariants: Negative coordinates blocked; occupied grid cells blocked; heuristic prefers straight paths; no path returns null.
- dependencies_and_callers: Mermaid ASCII edge renderer.
- edge_cases_or_failure_modes: Dense obstacles, start/end occupied semantics, path simplification over-removal if turns not detected, unbounded search if caller lacks grid limits.
- validation_or_tests: Vendor tests likely outside assigned set.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: OH_MY_HUMANIZE_MAIN-HZ-023, OH_MY_HUMANIZE_MAIN-HZ-053, OH_MY_HUMANIZE_MAIN-HZ-083, OH_MY_HUMANIZE_MAIN-HZ-113, OH_MY_HUMANIZE_MAIN-HZ-143, OH_MY_HUMANIZE_MAIN-HZ-173, OH_MY_HUMANIZE_MAIN-HZ-203, OH_MY_HUMANIZE_MAIN-HZ-233, OH_MY_HUMANIZE_MAIN-HZ-263, OH_MY_HUMANIZE_MAIN-HZ-293, OH_MY_HUMANIZE_MAIN-HZ-323, OH_MY_HUMANIZE_MAIN-HZ-353, OH_MY_HUMANIZE_MAIN-HZ-383, OH_MY_HUMANIZE_MAIN-HZ-413, OH_MY_HUMANIZE_MAIN-HZ-443, OH_MY_HUMANIZE_MAIN-HZ-473, OH_MY_HUMANIZE_MAIN-HZ-503, OH_MY_HUMANIZE_MAIN-HZ-533, OH_MY_HUMANIZE_MAIN-HZ-563, OH_MY_HUMANIZE_MAIN-HZ-593, OH_MY_HUMANIZE_MAIN-HZ-623, OH_MY_HUMANIZE_MAIN-HZ-653, OH_MY_HUMANIZE_MAIN-HZ-683, OH_MY_HUMANIZE_MAIN-HZ-713, OH_MY_HUMANIZE_MAIN-HZ-743, OH_MY_HUMANIZE_MAIN-HZ-773, OH_MY_HUMANIZE_MAIN-HZ-803, OH_MY_HUMANIZE_MAIN-HZ-833, OH_MY_HUMANIZE_MAIN-HZ-863, OH_MY_HUMANIZE_MAIN-HZ-893, OH_MY_HUMANIZE_MAIN-HZ-923, OH_MY_HUMANIZE_MAIN-HZ-953, OH_MY_HUMANIZE_MAIN-HZ-983, OH_MY_HUMANIZE_MAIN-HZ-1013, OH_MY_HUMANIZE_MAIN-HZ-1043, OH_MY_HUMANIZE_MAIN-HZ-1073, OH_MY_HUMANIZE_MAIN-HZ-1103, OH_MY_HUMANIZE_MAIN-HZ-1133, OH_MY_HUMANIZE_MAIN-HZ-1163, OH_MY_HUMANIZE_MAIN-HZ-1193, OH_MY_HUMANIZE_MAIN-HZ-1223, OH_MY_HUMANIZE_MAIN-HZ-1253, OH_MY_HUMANIZE_MAIN-HZ-1283, OH_MY_HUMANIZE_MAIN-HZ-1313, OH_MY_HUMANIZE_MAIN-HZ-1343, OH_MY_HUMANIZE_MAIN-HZ-1373, OH_MY_HUMANIZE_MAIN-HZ-1403, OH_MY_HUMANIZE_MAIN-HZ-1433, OH_MY_HUMANIZE_MAIN-HZ-1463, OH_MY_HUMANIZE_MAIN-HZ-1493, OH_MY_HUMANIZE_MAIN-HZ-1523, OH_MY_HUMANIZE_MAIN-HZ-1553, OH_MY_HUMANIZE_MAIN-HZ-1583, OH_MY_HUMANIZE_MAIN-HZ-1613, OH_MY_HUMANIZE_MAIN-HZ-1643, OH_MY_HUMANIZE_MAIN-HZ-1673, OH_MY_HUMANIZE_MAIN-HZ-1703, OH_MY_HUMANIZE_MAIN-HZ-1733, OH_MY_HUMANIZE_MAIN-HZ-1763, OH_MY_HUMANIZE_MAIN-HZ-1793, OH_MY_HUMANIZE_MAIN-HZ-1823, OH_MY_HUMANIZE_MAIN-HZ-1853, OH_MY_HUMANIZE_MAIN-HZ-1883, OH_MY_HUMANIZE_MAIN-HZ-1913, OH_MY_HUMANIZE_MAIN-HZ-1943, OH_MY_HUMANIZE_MAIN-HZ-1973, OH_MY_HUMANIZE_MAIN-HZ-2003, OH_MY_HUMANIZE_MAIN-HZ-2033, OH_MY_HUMANIZE_MAIN-HZ-2063, OH_MY_HUMANIZE_MAIN-HZ-2093, OH_MY_HUMANIZE_MAIN-HZ-2123, OH_MY_HUMANIZE_MAIN-HZ-2153, OH_MY_HUMANIZE_MAIN-HZ-2183, OH_MY_HUMANIZE_MAIN-HZ-2213, OH_MY_HUMANIZE_MAIN-HZ-2243, OH_MY_HUMANIZE_MAIN-HZ-2273, OH_MY_HUMANIZE_MAIN-HZ-2303, OH_MY_HUMANIZE_MAIN-HZ-2333, OH_MY_HUMANIZE_MAIN-HZ-2363, OH_MY_HUMANIZE_MAIN-HZ-2393, OH_MY_HUMANIZE_MAIN-HZ-2423, OH_MY_HUMANIZE_MAIN-HZ-2453, OH_MY_HUMANIZE_MAIN-HZ-2483, OH_MY_HUMANIZE_MAIN-HZ-2513, OH_MY_HUMANIZE_MAIN-HZ-2543, OH_MY_HUMANIZE_MAIN-HZ-2573, OH_MY_HUMANIZE_MAIN-HZ-2603, OH_MY_HUMANIZE_MAIN-HZ-2633, OH_MY_HUMANIZE_MAIN-HZ-2663, OH_MY_HUMANIZE_MAIN-HZ-2693, OH_MY_HUMANIZE_MAIN-HZ-2723, OH_MY_HUMANIZE_MAIN-HZ-2753, OH_MY_HUMANIZE_MAIN-HZ-2783, OH_MY_HUMANIZE_MAIN-HZ-2813, OH_MY_HUMANIZE_MAIN-HZ-2843, OH_MY_HUMANIZE_MAIN-HZ-2873, OH_MY_HUMANIZE_MAIN-HZ-2903, OH_MY_HUMANIZE_MAIN-HZ-2933, OH_MY_HUMANIZE_MAIN-HZ-2963, OH_MY_HUMANIZE_MAIN-HZ-2993, OH_MY_HUMANIZE_MAIN-HZ-3023, OH_MY_HUMANIZE_MAIN-HZ-3053, OH_MY_HUMANIZE_MAIN-HZ-3083, OH_MY_HUMANIZE_MAIN-HZ-3113, OH_MY_HUMANIZE_MAIN-HZ-3143, OH_MY_HUMANIZE_MAIN-HZ-3173, OH_MY_HUMANIZE_MAIN-HZ-3203, OH_MY_HUMANIZE_MAIN-HZ-3233, OH_MY_HUMANIZE_MAIN-HZ-3263, OH_MY_HUMANIZE_MAIN-HZ-3293, OH_MY_HUMANIZE_MAIN-HZ-3323, OH_MY_HUMANIZE_MAIN-HZ-3353, OH_MY_HUMANIZE_MAIN-HZ-3383, OH_MY_HUMANIZE_MAIN-HZ-3413, OH_MY_HUMANIZE_MAIN-HZ-3443, OH_MY_HUMANIZE_MAIN-HZ-3473, OH_MY_HUMANIZE_MAIN-HZ-3503, OH_MY_HUMANIZE_MAIN-HZ-3533, OH_MY_HUMANIZE_MAIN-HZ-3563, OH_MY_HUMANIZE_MAIN-HZ-3593
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`