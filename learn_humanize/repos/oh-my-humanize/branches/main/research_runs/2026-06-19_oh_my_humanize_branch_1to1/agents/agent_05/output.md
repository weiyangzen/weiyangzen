# agent_05 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-005 `directory` `packages`
- cursor: `[_]`
- core_role: Monorepo package root for the CLI, agent runtime, provider layer, catalog, TUI, memory, stats, web collaboration, native bindings, and research/benchmark tools; direct inventory found 3,773 files across 15 packages.
- algorithmic_behavior: Coordinates layered responsibilities: `packages/coding-agent` owns CLI/session/tool/workflow behavior; `packages/ai` normalizes provider/auth/streaming; `packages/agent` owns tool-call runtime primitives; `packages/tui` owns terminal rendering; `packages/mnemopi` owns memory extraction/recall; `packages/utils` supplies shared primitives.
- inputs_outputs_state: Inputs are package-local APIs, tests, config, generated assets, and fixtures; outputs are exported package surfaces, CLI behavior, test contracts, generated reports, and runtime state files.
- gates_or_invariants: Package boundaries enforce catalog import convention, Bun-first runtime assumptions, no generated `models.json` hand edits, and package-local changelog/test conventions from `AGENTS.md`.
- dependencies_and_callers: Internal packages depend on each other through `@oh-my-pi/pi-*` package names; `coding-agent` is the primary consumer of `ai`, `catalog`, `agent`, `tui`, `utils`, and native helpers.
- edge_cases_or_failure_modes: Cross-package barrels and generated declarations can be misclassified as algorithms; behavior-heavy code is concentrated in `coding-agent`, provider adapters, TUI terminal, memory, workflow, GitHub, and minimizer paths.
- validation_or_tests: Directory contains extensive package tests; no tests were executed for this read-only research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-035 `directory` `packages/swarm-extension`
- cursor: `[_]`
- core_role: Swarm orchestration extension implementing DAG validation, wave scheduling, state tracking, CLI entry, and `/swarm` command integration.
- algorithmic_behavior: `src/swarm/dag.ts:17` builds dependencies from `waits_for`, `reports_to`, and pipeline/sequential implicit order; `dag.ts:63` performs Kahn cycle detection; `dag.ts:106` derives deterministic waves. `pipeline.ts:45` runs iteration loops and `pipeline.ts:122` executes waves sequentially with same-wave parallelism.
- inputs_outputs_state: Inputs are YAML swarm specs, workspace/settings/model/auth handles, and run progress callbacks; outputs are `.swarm_<name>/state`, logs, pipeline summaries, subagent results, and TUI/extension progress messages.
- gates_or_invariants: Cyclic graphs fail before execution; failed agents produce structured `SingleResult`; state tracker persists transitions under isolated swarm directories; extension command validates config before controller start.
- dependencies_and_callers: CLI `src/cli.ts:19` parses YAML and builds DAG; `src/extension.ts:22` registers `/swarm`; `executor.ts:41` invokes coding-agent `runSubprocess` with workspace/model settings.
- edge_cases_or_failure_modes: Pipeline stops or records failures when agents throw; status command reads existing `.swarm_<name>` state; executor test guards `modelRegistry` forwarding and avoids stale `authStorage` use.
- validation_or_tests: `test/executor.test.ts:35` asserts `executeSwarmAgent` passes `modelRegistry`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-065 `file` `docs/non-compaction-retry-policy.md`
- cursor: `[_]`
- core_role: Architecture policy defining the retry/compaction boundary for agent turns after provider/runtime failures.
- algorithmic_behavior: Lines 17-27 define retry-before-compaction ordering and exclude context overflow from retry; lines 31-55 classify retryable non-overflow errors, refusals, stale replays, transient failures, usage limits, and partial-output replay blockers.
- inputs_outputs_state: Inputs are assistant stop reasons, error categories, observable partial output, credential state, backoff state, and model fallback state; outputs are retry attempts, aborted inflight turn state, trailing error removal, continue scheduling, and user-visible retry loader events.
- gates_or_invariants: Partial observable output blocks replay except refusals; overflow falls to compaction; counters reset on successful turn; permanent stops occur on attempt exhaustion, cancellation, visible partials, or unsafe replay.
- dependencies_and_callers: Documents behavior expected from AgentSession retry lifecycle, settings/RPC controls, TUI retry rendering, auth credential switching, and model fallback.
- edge_cases_or_failure_modes: Stale replay detection, usage-limit rotation, abort races, and duplicated tool/output visibility are explicit caveats around lines 121-148 and 218-237.
- validation_or_tests: Documentation policy only; tests were not run in this pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-095 `file` `scripts/claude-trace.ts`
- cursor: `[_]`
- core_role: Runtime trace script wrapping Claude-compatible command execution and structured trace options.
- algorithmic_behavior: Lines 22-35 parse nonnegative integers; lines 37-95 parse flags such as `--json`, `--upstream-insecure`, `--cwd`, `--host`, `--port`, `--timeout`, and input-delay options; lines 97-114 run the wrapper and map thrown errors to stderr/exit codes.
- inputs_outputs_state: Inputs are CLI argv and optional stdin delay/message settings; outputs are JSON/text traces, command execution, or failure messages with nonzero exit.
- gates_or_invariants: Unknown options throw; numeric options must be nonnegative; missing/invalid command/message state is rejected by parser flow.
- dependencies_and_callers: Depends on local trace wrapper implementation and Bun script execution; likely used by debugging or workflow trace tooling.
- edge_cases_or_failure_modes: Bad flags, negative timeouts, malformed numeric input, and wrapper exceptions exit cleanly rather than leaking stack-only output.
- validation_or_tests: No direct test found in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-125 `directory` `packages/ai/scripts`
- cursor: `[_]`
- core_role: Provider/runtime diagnostic scripts for log compaction and protocol extraction.
- algorithmic_behavior: `cursor-log.py:18` skips/coalesces noisy Cursor event logs, `cursor-log.py:130` coalesces `textDelta`, and `cursor-log.py:189` parses/follows JSONL. `proto-extractor.py:82` parses JS-bundle protobuf message/enum/service structures and `proto-extractor.py:358` renders `.proto` syntax.
- inputs_outputs_state: Inputs are JSONL event streams, JS bundles, filter arguments, and follow mode; outputs are compact terminal summaries or generated proto text.
- gates_or_invariants: Cursor log parser tolerates malformed/noisy records; proto extractor filters comments/noise and supports consolidation/filtering.
- dependencies_and_callers: Standalone Python scripts used by maintainers to inspect provider wire behavior; not imported by runtime packages.
- edge_cases_or_failure_modes: Incomplete JSONL, huge text delta streams, missing bundle patterns, and proto name collisions are handled through filtering/consolidation.
- validation_or_tests: No direct tests observed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-155 `directory` `packages/tui/src`
- cursor: `[_]`
- core_role: Terminal UI engine and component library for differential rendering, input decoding, terminal capability probing, and reusable widgets.
- algorithmic_behavior: Contains terminal lifecycle (`terminal.ts`), core TUI renderer (`tui.ts`), input decoding (`keys.ts`, `stdin-buffer.ts`), text layout utilities, scroll/select/settings/list components, editor components, kitty graphics, markdown rendering, fuzzy matching, and terminal capability probes.
- inputs_outputs_state: Inputs are raw stdin sequences, terminal resize/capability replies, render tree components, themes, and mouse/key events; outputs are ANSI/OSC writes, diffed frame buffers, component state transitions, and decoded UI actions.
- gates_or_invariants: Terminal rendering sanitizes/chunks output, preserves cursor/alt-screen state, and avoids raw terminal side effects in headless tests; components provide stable dimensions and input handlers.
- dependencies_and_callers: `packages/coding-agent` interactive modes use these components and terminal abstractions; tests under `packages/tui/test` validate key and scroll behavior.
- edge_cases_or_failure_modes: Windows ConPTY chunking, codepage flips, OSC capability fallback, bracketed paste, wide glyphs, scroll clamping, and ANSI truncation are primary terminal risks.
- validation_or_tests: Assigned tests cover `scroll-view` and manual key tester; no test execution run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-185 `file` `docs/tools/checkpoint.md`
- cursor: `[_]`
- core_role: Tool architecture documentation for in-memory session checkpoints and rewinds.
- algorithmic_behavior: Lines 14-31 define checkpoint input/output; lines 33-43 define flow: only top-level calls, nested calls rejected, tool returns payload, AgentSession records message count/entry id/start time.
- inputs_outputs_state: Inputs are checkpoint label/payload and session state; outputs are checkpoint records and optional rewind target.
- gates_or_invariants: Lines 44-65 state checkpoint is in-memory only, feature-gated, not git-based, and rewind is guarded to valid checkpoints.
- dependencies_and_callers: Defines expected contract for checkpoint tool, AgentSession state tracking, and TUI/tool renderer behavior.
- edge_cases_or_failure_modes: Nested checkpoints, missing checkpoints, stale rewind targets, and process restart losing checkpoint state are explicit limitations.
- validation_or_tests: Documentation only in assigned evidence.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-215 `file` `scripts/session-stats/analyze.py`
- cursor: `[_]`
- core_role: Offline SQLite analyzer for session/tool/edit behavior and follow-up diagnostics.
- algorithmic_behavior: Lines 30-75 open SQLite read-only and parse time windows; lines 119-215 aggregate tool token totals; lines 333-371 classify edit outcomes; lines 518-621 summarize edit formats/status/verbs/LOC; lines 667-884 detect small followups, self-corrections, same-locus re-edits, duplicate payloads, and anchor duplication.
- inputs_outputs_state: Inputs are session stats DB, filters, command subparser options, and optional bucket/window parameters; outputs are printed tables, samples, and categorized follow-up diagnostics.
- gates_or_invariants: Uses read-only DB URI; classifiers use regex buckets and bounded samples; argparse subcommands define allowed report modes.
- dependencies_and_callers: Standalone analysis script for stats/session telemetry; depends on SQLite schema and recorded session events.
- edge_cases_or_failure_modes: Missing DB, invalid windows, unknown tool result shapes, malformed hashline/edit args, and sparse samples.
- validation_or_tests: No direct tests assigned; script itself is analysis tooling.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-245 `directory` `packages/coding-agent/src/async`
- cursor: `[_]`
- core_role: Background job manager for async tool/task execution and delivery retry behavior.
- algorithmic_behavior: `job-manager.ts:154` registers jobs with active-count cap, id allocation, AbortController, queued/running/completed/failed state, and eviction; `job-manager.ts:251` cancels with owner gating; `job-manager.ts:328` implements smart poll ladder; `job-manager.ts:581` delivers results with exponential retry and jitter.
- inputs_outputs_state: Inputs are owner id, job callback, abort signal, delivery watchers, and capacity settings; outputs are job snapshots, delivery events, cancellation, acknowledgements, and eviction.
- gates_or_invariants: Capacity excludes queued/completed jobs; delivery suppression and watch/unwatch control visibility; `wait`, `drain`, and `dispose` settle running jobs.
- dependencies_and_callers: Used by coding-agent async bash/job features and status line background job count.
- edge_cases_or_failure_modes: Cancel races, failed delivery callbacks, owner mismatch, retry exhaustion, and stale jobs after eviction.
- validation_or_tests: No direct assigned test specifically for async manager.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-275 `directory` `packages/coding-agent/src/modes`
- cursor: `[_]`
- core_role: User-facing CLI modes: interactive TUI, print/RPC/ACP modes, controllers, transcript rendering, setup wizard, themes, workflow UI, session observer, and mode utilities.
- algorithmic_behavior: Directory has 258 files. Major algorithms include transcript native-scrollback safety, event/input controllers, RPC host/client and subagent transcript streaming, ACP bridging, status line segmentation, theme loading, session focus, image reference rendering, workflow graph UI, and context usage utilities.
- inputs_outputs_state: Inputs are AgentSession events, user keystrokes, RPC/ACP frames, theme/config/settings, tool events, session history, and terminal dimensions; outputs are TUI components, RPC frames, status lines, session navigation, and rendered transcripts.
- gates_or_invariants: Controllers route events without corrupting transcript state; status line sanitizes/truncates; transcript container enforces stable commit regions; setup/theme components preserve selection and validation state.
- dependencies_and_callers: Primary consumers are `cli.ts`, session runtime, TUI package, agent sessions, extension/hook systems, and collaboration/RPC clients.
- edge_cases_or_failure_modes: Streaming rows reflowing after scrollback commit, session switch cleanup, subagent owner mismatches, terminal width changes, image placeholder deletion, and theme/status overflow.
- validation_or_tests: Assigned tests cover transcript container, image references, settings theme, status-line newline guard, workflow session runtime, and TUI tree lists.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-305 `directory` `packages/coding-agent/test/marketplace`
- cursor: `[_]`
- core_role: Contract test suite for plugin marketplace discovery, registry persistence, install classification, source resolution, cache management, and project-scope precedence.
- algorithmic_behavior: Tests validate cache version/path guards, `plugin@marketplace` vs npm/local classification, internal URL parsing, slash arg parsing, local catalog fetching, registry CRUD, source path traversal protection, plugin root substitution, project registry resolution, and manager install/update/remove flows.
- inputs_outputs_state: Inputs are temp registries, fixture marketplace catalogs/plugins, install args, local paths, and fake home/project roots; outputs are registry JSON, cached plugin dirs, parsed install targets, resolved plugin source dirs, and test assertions.
- gates_or_invariants: Name/version validators reject uppercase, spaces, slashes, traversal, overlong ids; project entries shadow user entries; `.omp-plugin` catalog wins over `.claude-plugin` when both exist.
- dependencies_and_callers: Validates `extensibility/plugins/marketplace`, `discovery/helpers`, `internal-urls/parse`, and slash command parsers.
- edge_cases_or_failure_modes: Missing catalog, duplicate marketplace/plugin installs, malformed JSON, Windows paths, scoped npm packages, multiple `@`, path traversal, and orphaned cache entries.
- validation_or_tests: This directory is itself validation; no test execution run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-335 `directory` `python/robomp/web/src`
- cursor: `[_]`
- core_role: SolidJS dashboard for robomp status, issue/event browsing, logs, and trigger/cancel workflows.
- algorithmic_behavior: `state.ts` polls status/log resources every 3 seconds, exposes trigger status, and refetches after trigger/cancel; `api.ts` unwraps JSON, maps non-2xx to `ApiError`, and calls `/api/status`, `/api/logs`, `/api/github/issues`, `/api/trigger`, `/api/cancel`; components render working/running/events/issues/logs.
- inputs_outputs_state: Inputs are server JSON endpoints, auth headers, trigger form/retry/cancel actions, and polling interval; outputs are dashboard state resources, UI rows, issue links, and trigger/cancel status text.
- gates_or_invariants: Polling starts once and stops on cleanup; in-flight errors update `lastTickError`; trigger/cancel normalize backend errors.
- dependencies_and_callers: Frontend consumes `python/robomp/src/server.py` JSON shapes mirrored in `types.ts`; used by robomp web server.
- edge_cases_or_failure_modes: Non-JSON responses, failed polls, duplicate polling, stale in-flight fetches, empty transcript/log data, and retry/cancel errors.
- validation_or_tests: No direct frontend tests in assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-365 `file` `crates/pi-natives/src/power.rs`
- cursor: `[_]`
- core_role: Native macOS power assertion binding to prevent sleep during long operations.
- algorithmic_behavior: Defines `MacOSPowerAssertionOptions` around lines 19-30; macOS implementation wraps CoreFoundation strings and IOKit assertion create/release; `MacOSPowerAssertion` around line 195 exposes start/stop semantics with default idle prevention.
- inputs_outputs_state: Inputs are reason/type options; outputs are native assertion ids and active assertion state.
- gates_or_invariants: Platform-specific code checks assertion kind, manages CFString lifetimes, and releases assertions on stop/drop paths.
- dependencies_and_callers: Exposed through native package for CLI/runtime operations that need sleep prevention.
- edge_cases_or_failure_modes: Unsupported platform, IOKit failure status, duplicate start/stop, leaked assertion if release path fails.
- validation_or_tests: No assigned Rust test observed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-395 `file` `packages/agent/src/tokenizer.ts`
- cursor: `[_]`
- core_role: Token count helper for agent runtime accounting.
- algorithmic_behavior: Lines 3-17 use native `countTokens` only when `PI_TOKENIZER_ACCURATE=1` and not in test runtime; otherwise estimate by `byteLength / 4`; arrays are summed recursively.
- inputs_outputs_state: Inputs are string or string arrays and environment/test runtime flag; output is numeric token estimate/count.
- gates_or_invariants: Accurate path is opt-in; test runtime remains deterministic and avoids native tokenizer dependency.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-natives` and `isBunTestRuntime`; called by runtime/token budgeting code.
- edge_cases_or_failure_modes: Non-ASCII text estimated by bytes, array recursion, native unavailability avoided unless opt-in.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-425 `file` `packages/ai/src/rate-limit-utils.ts`
- cursor: `[_]`
- core_role: Provider error classifier and retry backoff calculator for rate/usage/model capacity failures.
- algorithmic_behavior: Lines 6-17 define categories/backoff constants; lines 30-74 classify messages by priority; lines 80-93 calculate backoff with jitter for model capacity; lines 96-100 detect usage limits.
- inputs_outputs_state: Inputs are error text/status-ish messages and attempt count; outputs are reason category, usage-limit boolean, and retry delay.
- gates_or_invariants: Usage limits and auth-like exhaustion are separated from generic transient failures; backoff is capped and jittered.
- dependencies_and_callers: Used by auth/retry/provider handling in `packages/ai` and higher-level non-compaction retry policy.
- edge_cases_or_failure_modes: Ambiguous provider strings, model capacity vs generic 429, and excessive attempts.
- validation_or_tests: Related usage/auth tests exercise downstream effects.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-455 `file` `packages/ai/test/auth-broker-oauth-extra-fields.test.ts`
- cursor: `[_]`
- core_role: Regression tests for OAuth broker persistence of provider-specific extra fields.
- algorithmic_behavior: Lines 74-99 assert broker set/get round-trips OAuth extra fields and remote snapshot masks refresh-token sentinel values.
- inputs_outputs_state: Inputs are OAuth credential objects with extra fields; outputs are stored/retrieved credentials and sanitized remote snapshots.
- gates_or_invariants: Extra fields must survive storage; sensitive refresh sentinel must be masked.
- dependencies_and_callers: Validates auth broker/storage APIs used by provider login and remote auth sync.
- edge_cases_or_failure_modes: Dropped provider-specific fields, leaked refresh values, malformed remote snapshot.
- validation_or_tests: This file is the validation contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-485 `file` `packages/ai/test/auth-storage-usage-cache.test.ts`
- cursor: `[_]`
- core_role: Contract tests for provider usage-cache behavior, TTL jitter, header ingestion, and credential failure handling.
- algorithmic_behavior: Lines 204-292 validate last-good cache and failure cooldown; lines 297-326 validate TTL jitter; lines 352-401 validate header ingestion/tier merge; lines 413-498 validate `invalid_grant` disables stale last-good; lines 505-561 validate transient refresh failures retain last-good.
- inputs_outputs_state: Inputs are fake usage fetches, auth failures, response headers, and time/TTL settings; outputs are usage reports, cached last-good records, disabled states, and cooldown behavior.
- gates_or_invariants: Invalid grants suppress stale success; transient errors may reuse last-good; TTLs are jittered; headers merge without losing tier details.
- dependencies_and_callers: Validates auth storage and usage reporting used by status line/provider limits.
- edge_cases_or_failure_modes: Expired tokens, transient network failure, invalid grant, stale cache poisoning, and thundering-herd TTLs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-515 `file` `packages/ai/test/google-gemini-cli-3x-thinking.test.ts`
- cursor: `[_]`
- core_role: Tests Gemini thinking-level mapping across model families.
- algorithmic_behavior: Lines 52-119 assert Gemini 3.x maps effort to `thinkingLevel`, rejects unsupported effort, and Gemini 2.5 still uses `thinkingBudget`.
- inputs_outputs_state: Inputs are model ids and thinking effort settings; outputs are provider request bodies or thrown validation errors.
- gates_or_invariants: Gemini 3.x and 2.5 use different wire fields; unsupported effort must not silently degrade.
- dependencies_and_callers: Validates Google/Gemini provider adapter.
- edge_cases_or_failure_modes: Version-family misclassification, wrong field name, unsupported effort accepted.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-545 `file` `packages/ai/test/issue-827-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for forced tool-choice reasoning stripping behavior.
- algorithmic_behavior: Lines 85-180 assert Kimi/Claude forced `tool_choice` strips reasoning, while non-Kimi paths preserve reasoning as expected.
- inputs_outputs_state: Inputs are provider/model combinations, messages with reasoning, and forced tool choice; outputs are transformed provider request bodies.
- gates_or_invariants: Provider-specific reasoning/tool-choice incompatibility must be handled without global stripping.
- dependencies_and_callers: Validates `packages/ai` request transformation.
- edge_cases_or_failure_modes: Dropping reasoning for providers that support it or retaining it for forced-tool providers that reject it.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-575 `file` `packages/ai/test/openai-codex-include.test.ts`
- cursor: `[_]`
- core_role: Regression test for OpenAI Codex encrypted reasoning include flags.
- algorithmic_behavior: Lines 5-23 assert `reasoning.encrypted_content` is included exactly once.
- inputs_outputs_state: Inputs are OpenAI Codex request setup; output is include array/field in request.
- gates_or_invariants: Must not omit encrypted reasoning or duplicate include values.
- dependencies_and_callers: Validates OpenAI/Codex provider request construction.
- edge_cases_or_failure_modes: Missing encrypted content across turns or duplicated include causing API rejection.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-605 `file` `packages/ai/test/openai-tool-strict-mode.test.ts`
- cursor: `[_]`
- core_role: Provider compatibility tests for strict tool schema mode and fallback behavior.
- algorithmic_behavior: Lines 117-624 cover strict flags for providers, loose mode yielding non-strict schemas, Cerebras stream-options omission, all-or-none strictness, JSON error body surfacing, provider fallback to non-strict, and remembered fallbacks for OpenRouter/DeepSeek.
- inputs_outputs_state: Inputs are provider capabilities, tool schemas, response errors, and request paths; outputs are provider request bodies, fallback state, and surfaced errors.
- gates_or_invariants: Strictness is all-or-none per request; incompatible providers fallback only on classified errors; fallback memory clears/updates on responses path.
- dependencies_and_callers: Validates OpenAI-compatible provider layer and schema conversion.
- edge_cases_or_failure_modes: Mixed strict/non-strict tools, provider-specific body fields, JSON error parsing, repeated incompatible strict attempts.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-635 `file` `packages/ai/test/synthetic-login.test.ts`
- cursor: `[_]`
- core_role: Test for synthetic API-key login validation.
- algorithmic_behavior: Lines 6-23 validate an API key by calling `/models`.
- inputs_outputs_state: Inputs are fake fetch/API key; outputs are successful login validation or failure.
- gates_or_invariants: Login must prove key works against provider models endpoint.
- dependencies_and_callers: Validates synthetic login helper used by auth flows.
- edge_cases_or_failure_modes: Accepted empty/bad keys or wrong endpoint.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-665 `file` `packages/catalog/src/models.json.d.ts`
- cursor: `[_]`
- core_role: Type declaration shim for generated `models.json`.
- algorithmic_behavior: Lines 1-9 declare provider/model map shape and preserve `api` type inference.
- inputs_outputs_state: Input is generated JSON import; output is TypeScript type information.
- gates_or_invariants: Only `api` is strongly typed; other fields remain `unknown`.
- dependencies_and_callers: Used by TypeScript compiler for JSON import typing in catalog consumers.
- edge_cases_or_failure_modes: Drift from generated JSON shape would be compile-time only.
- validation_or_tests: No runtime tests needed.
- skip_candidate: `yes: declaration-only shim, not an algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-695 `file` `packages/catalog/test/litellm-provider.test.ts`
- cursor: `[_]`
- core_role: Tests LiteLLM provider base URL and cache identity resolution.
- algorithmic_behavior: Lines 47-84 assert `LITELLM_BASE_URL` fallback, explicit base URL precedence, and cache id behavior.
- inputs_outputs_state: Inputs are env/config provider settings; outputs are resolved provider descriptor/base URL/cache id.
- gates_or_invariants: Explicit config wins over env; provider cache identity remains stable and scoped.
- dependencies_and_callers: Validates catalog provider descriptor/resolution behavior.
- edge_cases_or_failure_modes: Wrong base URL precedence and cache collision.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-725 `file` `packages/coding-agent/src/cli-commands.ts`
- cursor: `[_]`
- core_role: CLI subcommand dispatch table and default launch resolver.
- algorithmic_behavior: Lines 13-46 define command table; lines 48-58 generate reserved word messages; lines 66-86 resolve subcommands vs default interactive launch.
- inputs_outputs_state: Inputs are argv command token and known command names; outputs are selected command handler/default mode or reserved-word error.
- gates_or_invariants: Reserved command names are protected; unknown/empty input falls through to default prompt/interactive behavior where appropriate.
- dependencies_and_callers: Used by CLI entrypoint before loading command registry/modes.
- edge_cases_or_failure_modes: Ambiguous first token, reserved words as prompts, and unknown command fallback.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-755 `file` `packages/coding-agent/test/agent-session-before-agent-start-attribution.test.ts`
- cursor: `[_]`
- core_role: Tests attribution semantics for hook-injected `before_agent_start` messages.
- algorithmic_behavior: Lines 102-168 assert user vs agent attribution and prompt opt-in behavior for injected context.
- inputs_outputs_state: Inputs are hook messages, attribution values, and prompt options; outputs are persisted session entries and message attribution visible to accounting/context.
- gates_or_invariants: Hook-injected messages must not be misattributed by default; user attribution is opt-in and explicit.
- dependencies_and_callers: Validates AgentSession hook integration.
- edge_cases_or_failure_modes: Billing/context attribution drift and invisible injected context.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-785 `file` `packages/coding-agent/test/agent-session-steer-idle-drain.test.ts`
- cursor: `[_]`
- core_role: Tests queued steer/follow-up draining around idle/interrupted session states.
- algorithmic_behavior: Lines 95-123 validate idle/interrupted tool steer continue; lines 126-167 validate clearQueue image roundtrip.
- inputs_outputs_state: Inputs are queued messages, tool interruption state, and image content; outputs are drained prompts and preserved/cleared queue state.
- gates_or_invariants: Idle drain must continue after tool interruption; image payloads must survive queue clearing semantics.
- dependencies_and_callers: Validates AgentSession queue handling.
- edge_cases_or_failure_modes: Lost steering messages, duplicated queue entries, image block loss.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-815 `file` `packages/coding-agent/test/block-images.test.ts`
- cursor: `[_]`
- core_role: Tests file argument processing for text/image blocks.
- algorithmic_behavior: Lines 37-64 validate reading image and text file inputs; lines 80-99 validate image processing before LLM filtering.
- inputs_outputs_state: Inputs are file paths and content-type decisions; outputs are content blocks suitable for messages.
- gates_or_invariants: Images must be detected/converted before text-only filtering can drop unsupported content.
- dependencies_and_callers: Validates coding-agent file/message preparation.
- edge_cases_or_failure_modes: Image misclassification, text read fallback, file filtering losing images.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-845 `file` `packages/coding-agent/test/edit-patch-unchanged-error.test.ts`
- cursor: `[_]`
- core_role: Tests edit/apply-patch unchanged-error diagnostics and path redaction.
- algorithmic_behavior: Lines 53-86 assert user-facing error contains relative path not absolute; lines 89-110 assert structured context keeps absolute path.
- inputs_outputs_state: Inputs are unchanged patch attempts and target paths; outputs are user error text and structured details/context.
- gates_or_invariants: UI error must avoid leaking full home paths while machine context retains precise path.
- dependencies_and_callers: Validates edit tool error mapping/rendering.
- edge_cases_or_failure_modes: Privacy leak in errors or loss of absolute path needed for debugging.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-875 `file` `packages/coding-agent/test/history-storage-session.test.ts`
- cursor: `[_]`
- core_role: Tests session history storage, id persistence, schema migration, and ranking integration.
- algorithmic_behavior: Lines 37-109 validate session id persistence/resolver/schema migration; lines 119-143 validate `matchingSessionIds` ordering, deduplication, and nonempty filtering.
- inputs_outputs_state: Inputs are session metadata/history records and match terms; outputs are session ids and ranked result ids.
- gates_or_invariants: Migration must preserve ids; matching must be ordered/deduped and avoid empty results.
- dependencies_and_callers: Validates history storage used by session picker/resume.
- edge_cases_or_failure_modes: Duplicate sessions, stale schema, missing id, empty matcher pollution.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-905 `file` `packages/coding-agent/test/interactive-mode-status.test.ts`
- cursor: `[_]`
- core_role: Tests interactive status notifications and optimistic status preservation.
- algorithmic_behavior: Lines 71-120 assert status coalescing/appending; lines 123-146 assert startup notification and optimistic signature preservation.
- inputs_outputs_state: Inputs are session events/status updates; outputs are rendered status rows/notifications.
- gates_or_invariants: Repeated statuses coalesce; optimistic state is not overwritten by stale events.
- dependencies_and_callers: Validates interactive mode TUI status handling.
- edge_cases_or_failure_modes: Status spam, flicker, or lost startup state.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-935 `file` `packages/coding-agent/test/issue-980-bedrock-priority.test.ts`
- cursor: `[_]`
- core_role: Regression test for provider-qualified model resolution priority.
- algorithmic_behavior: Lines 26-58 assert explicit Anthropic model resolution wins and does not fall back to Bedrock on miss.
- inputs_outputs_state: Inputs are provider/model identifiers; outputs are resolved model/provider or miss.
- gates_or_invariants: Explicit provider qualification must not be silently remapped to Bedrock.
- dependencies_and_callers: Validates model registry/provider selection.
- edge_cases_or_failure_modes: Wrong provider selected for similarly named models.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-965 `file` `packages/coding-agent/test/mcp-reconnect.test.ts`
- cursor: `[_]`
- core_role: Tests MCP reconnect and retry/rebind behavior.
- algorithmic_behavior: Lines 41-83 validate retriable classifier; lines 95-238 validate retry, rebind, reuse, failure/no-retry/provider info; lines 276-305 validate abort propagation.
- inputs_outputs_state: Inputs are MCP transport errors, provider ids, retry settings, and abort signals; outputs are reconnect attempts, rebound clients, or propagated errors.
- gates_or_invariants: Only retriable errors reconnect; aborts stop retries; provider context is retained for diagnostics.
- dependencies_and_callers: Validates MCP client/tool integration in coding-agent.
- edge_cases_or_failure_modes: Infinite retry, stale client reuse, lost abort, bad error classification.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-995 `file` `packages/coding-agent/test/pi-scope-aliases.test.ts`
- cursor: `[_]`
- core_role: Tests canonical and extension alias resolution for PI-scoped ids.
- algorithmic_behavior: Lines 25-44 validate canonical resolution/cases; lines 130-134 validate extension alias remap without errors.
- inputs_outputs_state: Inputs are alias strings and extension mappings; outputs are canonical scope ids.
- gates_or_invariants: Known aliases must map deterministically; extension aliases must not collide/error.
- dependencies_and_callers: Validates discovery/scope alias resolution.
- edge_cases_or_failure_modes: Case drift, alias collision, extension remap failure.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1025 `file` `packages/coding-agent/test/rpc-prompt-result.test.ts`
- cursor: `[_]`
- core_role: Tests RPC `prompt_result` emission and suppression rules.
- algorithmic_behavior: Lines 26-330 cover local-only result emission, suppression for extension messages, `triggerTurn`, errors, and `agentInvoked`.
- inputs_outputs_state: Inputs are RPC prompt requests/events and extension/local message flags; outputs are prompt result frames or suppressed emissions.
- gates_or_invariants: RPC clients should get local prompt results only under correct conditions; extension-driven turns avoid double result frames.
- dependencies_and_callers: Validates RPC mode/session prompt plumbing.
- edge_cases_or_failure_modes: Duplicate prompt results, missing result on errors, wrong `agentInvoked` state.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1055 `file` `packages/coding-agent/test/session-ranking.test.ts`
- cursor: `[_]`
- core_role: Tests session ranking and history/fuzzy merge behavior.
- algorithmic_behavior: Lines 25-77 validate fuzzy/literal ranking; lines 81-120 validate merging history and fuzzy results.
- inputs_outputs_state: Inputs are search terms, session metadata, and history recency; outputs are ranked session lists.
- gates_or_invariants: Literal/fuzzy/recency ordering remains deterministic and deduped.
- dependencies_and_callers: Validates session picker/search behavior.
- edge_cases_or_failure_modes: Poor ranking, duplicates, recency overriding relevant exact matches.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1085 `file` `packages/coding-agent/test/streaming-preview-height.test.ts`
- cursor: `[_]`
- core_role: Tests streaming edit preview height stability and bounded pending preview rendering.
- algorithmic_behavior: Lines 23-358 validate stable streaming preview height/finalization; lines 363-446 validate bounded pending previews.
- inputs_outputs_state: Inputs are partial edit/tool arguments and render widths; outputs are preview components and final render rows.
- gates_or_invariants: Preview height must not jump/overflow as streamed args arrive; finalization reconciles pending preview.
- dependencies_and_callers: Validates edit/tool renderer streaming path.
- edge_cases_or_failure_modes: Layout jumps, unbounded preview growth, final result duplicate/overlap.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1115 `file` `packages/coding-agent/test/tui-tree-list-collapsed-lines.test.ts`
- cursor: `[_]`
- core_role: Tests TUI tree/list collapsed-line budget and summary rendering.
- algorithmic_behavior: Lines 13-289 validate collapse budget, summary rows, truncation behavior, and nested collapsed lines.
- inputs_outputs_state: Inputs are tree/list rows and viewport budgets; outputs are rendered collapsed lines and summaries.
- gates_or_invariants: Collapsed summaries must fit configured budgets and preserve useful counts/context.
- dependencies_and_callers: Validates TUI tree rendering used by transcript/tool displays.
- edge_cases_or_failure_modes: Excessive collapsed output, missing summary counts, truncation breaking layout.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1145 `file` `packages/hashline/src/diff-preview.ts`
- cursor: `[_]`
- core_role: Builds human-readable previews for hashline edit diffs.
- algorithmic_behavior: Lines 48-60 parse numbered diff rows; lines 62-74 collapse consecutive added runs; lines 76-124 build preview rows with post-edit line numbers, stats, and separator cleanup.
- inputs_outputs_state: Inputs are diff text and line metadata; outputs are concise preview strings and change counts.
- gates_or_invariants: Added/deleted/context lines are parsed by prefixes; preview avoids redundant separators and keeps line numbering coherent.
- dependencies_and_callers: Used by hashline edit tooling and streaming preview rendering.
- edge_cases_or_failure_modes: Malformed diff rows, long added runs, empty diffs, and line-number drift.
- validation_or_tests: Related streaming preview tests validate behavior indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1175 `file` `packages/mnemopi/src/index.ts`
- cursor: `[_]`
- core_role: Public barrel export surface for memory, embeddings, beam, and recall APIs.
- algorithmic_behavior: Lines 1-33 re-export configuration, memory APIs, default instance controls, scratchpad, and enhanced recall.
- inputs_outputs_state: Inputs are imported module APIs; output is package public surface.
- gates_or_invariants: No logic beyond export composition.
- dependencies_and_callers: Consumed by external callers importing `@oh-my-pi/pi-mnemopi`.
- edge_cases_or_failure_modes: Export omission or duplicate ambiguity.
- validation_or_tests: Package tests import through this surface.
- skip_candidate: `yes: barrel export file, not an algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1205 `file` `packages/mnemopi/test/extraction-integration.test.ts`
- cursor: `[_]`
- core_role: Integration tests for memory fact extraction client.
- algorithmic_behavior: Lines 27-137 validate fake HTTP extraction, structured fact parsing, malformed JSON diagnostics, and rate-limit backoff.
- inputs_outputs_state: Inputs are conversation messages and fake fetch responses; outputs are extracted fact arrays and diagnostics snapshots.
- gates_or_invariants: Empty/malformed output records failures; successful JSON array records success; rate-limit retries/backoff should occur.
- dependencies_and_callers: Validates `core/extraction/client` and diagnostics.
- edge_cases_or_failure_modes: Malformed JSON, empty response, 429 retries, bad content shape.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1235 `file` `packages/mnemopi/test/shmr.test.ts`
- cursor: `[_]`
- core_role: Tests SHMR/recall embedding and fact harmonization behavior.
- algorithmic_behavior: Lines 30-68 validate provider/fallback embeddings and clustering; lines 96-131 validate fact harmonization and insufficient-candidate behavior.
- inputs_outputs_state: Inputs are fake embeddings/facts; outputs are clusters, harmonized facts, or fallback decisions.
- gates_or_invariants: Insufficient candidates should not over-harmonize; provider fallback must preserve useful recall.
- dependencies_and_callers: Validates mnemopi memory/recall algorithms.
- edge_cases_or_failure_modes: Bad embeddings, too few candidates, incorrect cluster merge.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1265 `file` `packages/snapcompact/research/bench_kimi_probe.py`
- cursor: `[_]`
- core_role: Research probe measuring Kimi image token billing/downscaling behavior.
- algorithmic_behavior: Lines 27-35 define provider routes; lines 37-53 find and resize a production frame; lines 56-62 call chat completions; lines 64-88 compare measured image tokens against `ceil(px/28)^2`.
- inputs_outputs_state: Inputs are route, image sizes, API keys, cached production frames; outputs are token ratios and downscaled/linear verdict lines.
- gates_or_invariants: Text-only prompt tokens are subtracted; provider failures are reported per size; expected token count uses MoonViT patch heuristic.
- dependencies_and_callers: Uses snapcompact research providers/cache utilities and Pillow.
- edge_cases_or_failure_modes: Missing cached frame, missing API key, provider errors, silent downscaling.
- validation_or_tests: Research script; no automated tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1295 `file` `packages/snapcompact/research/final.py`
- cursor: `[_]`
- core_role: End-to-end snapcompact research benchmark over models, lengths, and carrier conditions.
- algorithmic_behavior: Lines 45-57 define model/condition grid; lines 60-74 disk-cache LLM calls avoiding truncated outputs; lines 76-90 parse image conditions/chunk budgets; lines 99-215 run one chunk through text/handoff/compact/image QA; lines 217-237 aggregate EM/F1/token/cost; lines 239+ builds task grid and writes records/summary/matrix.
- inputs_outputs_state: Inputs are SQuAD passages/questions, model keys, prompts, image render settings, cache, CLI options; outputs are JSONL records, CSV matrix, summary JSON, printed tables.
- gates_or_invariants: Unknown model fails fast; empty/truncated LLM output is not cached; OpenAI compact uses remote compact items; image cache writes atomically through temp file.
- dependencies_and_callers: Uses `squad`, `bdf`, `providers`, and `run` research modules.
- edge_cases_or_failure_modes: No sampled questions for chunk, stale image cache salt, provider truncation, cache freshness, cost assumptions.
- validation_or_tests: Research script; no automated tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1325 `file` `packages/snapcompact/research/snapcompact_tensor_heatmap.py`
- cursor: `[_]`
- core_role: White-box hidden-state heatmap generator for snapcompact visual occlusion experiments.
- algorithmic_behavior: Lines 63-78 map heat values to palette; lines 80-97 downsample/normalize matrices; lines 155-173 extract image-token hidden states from model layers; lines 239+ load model, render/mask images, compare original/answer/random masks, and render card output.
- inputs_outputs_state: Inputs are model dir, font/variant/size, SQuAD chunk/questions, mask spans, and transformer processor/model; outputs are masked images, JSON summary, and heatmap PNG.
- gates_or_invariants: Image token positions must match across variants; no sampled questions aborts; normalization uses quantile scales.
- dependencies_and_callers: Uses local snapcompact rendering/masking utilities plus torch/transformers/Pillow/numpy.
- edge_cases_or_failure_modes: Missing local model, no GPU/slow CPU, mismatched image positions, no question fit, extreme heat scale.
- validation_or_tests: Research script; no automated tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1355 `file` `packages/stats/test/behavior-backfill.test.ts`
- cursor: `[_]`
- core_role: Tests stats behavior backfill retry handling.
- algorithmic_behavior: Lines 74-117 assert sync retry handles old sentinels and does not wipe pending progress.
- inputs_outputs_state: Inputs are fixture stats DB/progress sentinel states; outputs are backfilled behavior records and preserved pending progress.
- gates_or_invariants: Existing pending progress must not be overwritten during retry/backfill.
- dependencies_and_callers: Validates stats sync/backfill subsystem.
- edge_cases_or_failure_modes: Legacy sentinel formats, repeated retries, accidental progress reset.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1385 `file` `packages/tui/src/terminal.ts`
- cursor: `[_]`
- core_role: Terminal abstraction managing raw mode, input decoding, capability probes, safe writes, emergency restore, and platform quirks.
- algorithmic_behavior: Lines 62-133 chunk UTF-8 output for Windows ConPTY by byte limit and newline/codepoint boundaries; lines 236-280 restore terminal state after crash; `ProcessTerminal` begins at line 395 and sets raw mode, bracketed paste, resize handlers, Kitty protocol, OSC 11/99, private mode probes, and Windows VT input.
- inputs_outputs_state: Inputs are stdin bytes, terminal resize/probe replies, write buffers, env flags, platform state; outputs are ANSI/OSC sequences, decoded input callbacks, terminal appearance/private-mode events, progress indicators.
- gates_or_invariants: Headless tests suppress side effects; alt-screen exit is gated by tracked state; Windows codepage restored before writes; ConPTY writes stay below 16 KiB encoded bytes.
- dependencies_and_callers: Used by `packages/tui` renderer and coding-agent interactive TUI.
- edge_cases_or_failure_modes: Split escape sequences, surrogate pairs, stale terminal dimensions, OSC unsupported terminals, WSL ConPTY, stdout errors, crashed alt-screen.
- validation_or_tests: TUI tests cover dependent components; no direct terminal test run here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1415 `file` `packages/tui/test/key-tester.ts`
- cursor: `[_]`
- core_role: Manual diagnostic utility for observing decoded key sequences.
- algorithmic_behavior: Lines 9-92 run an interactive key logger and print key data.
- inputs_outputs_state: Inputs are terminal keypresses; outputs are diagnostic printed key names/sequences.
- gates_or_invariants: Intended for manual terminal inspection, not automated runtime logic.
- dependencies_and_callers: Uses TUI key decoding utilities.
- edge_cases_or_failure_modes: Terminal-specific escape differences.
- validation_or_tests: It is a manual test utility.
- skip_candidate: `yes: manual diagnostic helper, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1445 `file` `packages/tui/test/scroll-view.test.ts`
- cursor: `[_]`
- core_role: Tests scroll-view layout and input behavior.
- algorithmic_behavior: Lines 10-101 validate viewport rendering, scrollbar/clamping, ANSI handling, ellipsis, and key scrolling.
- inputs_outputs_state: Inputs are scroll content, viewport dimensions, and key events; outputs are rendered visible rows and scroll offsets.
- gates_or_invariants: Scroll position clamps to content bounds; ANSI text should not break width calculations; long rows are elided.
- dependencies_and_callers: Validates `packages/tui/src/components/scroll-view.ts`.
- edge_cases_or_failure_modes: Overscroll, empty content, narrow width, ANSI truncation.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1475 `file` `packages/typescript-edit-benchmark/src/runner.ts`
- cursor: `[_]`
- core_role: Benchmark runner for edit-task evaluation across providers, retries, telemetry, verification, and summary aggregation.
- algorithmic_behavior: Lines 405-463 build timeout/provider retry contexts; lines 536-650 generate guided hashline patches; lines 655-764 build prompts/provider session ids/RPC args; lines 967-1018 configure early stop; lines 1000-1390 run a single task with retries, event collection, stats, verification, and logs; lines 1736-1779 choose best run; lines 1837-1935 compute percentile/token distributions; lines 1869-2035 build benchmark summaries; lines 2038+ run concurrent task workers.
- inputs_outputs_state: Inputs are edit tasks, fixtures, expected dirs, model/provider config, RPC/in-process clients, and telemetry events; outputs are per-run logs, conversation dumps, task results, aggregate summaries, and progress snapshots.
- gates_or_invariants: Timeout retries do not consume normal attempts; auth/provider failures are classified separately; best run ordering prefers success, non-ghost, lower tokens, earlier index; verification gates success.
- dependencies_and_callers: Uses coding-agent RPC/in-process clients, edit/hashline utilities, prompt templates, fixture copy/verification helpers.
- edge_cases_or_failure_modes: Provider auth failure, zero-tool no-op attempts, prompt timeout, turn limit, mutation-intent mismatch, hashline guidance too large, ghost runs.
- validation_or_tests: No assigned tests for runner itself.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1505 `file` `packages/utils/src/ring.ts`
- cursor: `[_]`
- core_role: Fixed-capacity circular buffer utility.
- algorithmic_behavior: Lines 7-169 implement push, shift, pop, unshift, random access, peek, clear, iterator, and `toArray` over circular storage.
- inputs_outputs_state: Inputs are capacity and pushed/unshifted values; outputs are bounded ordered collection views and removed values.
- gates_or_invariants: Size never exceeds capacity; head/tail wrap modulo buffer length.
- dependencies_and_callers: Shared utility for bounded histories/queues.
- edge_cases_or_failure_modes: Capacity validation appears absent despite positive-capacity expectation; wrap-around correctness and zero capacity are risk points.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1535 `file` `packages/utils/test/snowflake.test.ts`
- cursor: `[_]`
- core_role: Tests Snowflake id encoding/decoding contracts.
- algorithmic_behavior: Lines 7-39 validate roundtrip, lexicographic ordering, and bracket formatting.
- inputs_outputs_state: Inputs are generated/parsed snowflake ids; outputs are stable string/id representations.
- gates_or_invariants: Encoded ids sort consistently and bracket parsing preserves identity.
- dependencies_and_callers: Validates shared id utility used in sessions/events.
- edge_cases_or_failure_modes: Sort drift, parse failures, bracket wrapper mismatch.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1565 `file` `python/robomp/src/proxy_client.py`
- cursor: `[_]`
- core_role: HMAC-signed client and git transport for robomp-to-gh-proxy channel.
- algorithmic_behavior: Lines 43-70 decode proxy errors into `GitHubError`, `GitCommandError`, or `HeadDriftError`; lines 77-89 sign canonical request targets; `GitHubProxyClient` lines 93-341 maps GitHub REST read/write methods to `/gh/v1/*`; `ProxyGitTransport` lines 345-431 routes clone/fetch/push through proxy; payload mappers lines 433-546 build typed dataclasses.
- inputs_outputs_state: Inputs are repo/issue/PR/git operation params, base URL, HMAC key, and proxy responses; outputs are typed GitHub/git dataclasses or domain exceptions.
- gates_or_invariants: GET targets are signed after httpx canonicalizes query bytes; empty reviewer/label/assignee operations short-circuit; malformed payloads raise GitHubError 500.
- dependencies_and_callers: Implements `GitHubBackend` and `GitTransport` for robomp workers/tasks without exposing PATs.
- edge_cases_or_failure_modes: Signature drift, non-JSON proxy error, head drift, malformed payloads, duplicate `team_reviewers` annotation in source, sync vs async transport mismatch.
- validation_or_tests: No direct assigned tests for proxy client.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1595 `file` `python/robomp/tests/test_worker_pragmas.py`
- cursor: `[_]`
- core_role: Tests worker directive pragma resolution for model and thinking overrides.
- algorithmic_behavior: Lines 21-77 validate no-directive behavior, model alias matching against pool entries, unknown alias fallback, thinking normalization, unknown thinking drop, combined pragmas, and last-value-wins.
- inputs_outputs_state: Inputs are `DirectiveInfo` pragmas and `ROBOMP_MODEL` pool; outputs are `(model_override, thinking_override)`.
- gates_or_invariants: Only matched pool aliases override model; thinking levels normalize to supported set; duplicate pragma keys use last value.
- dependencies_and_callers: Validates `robomp.worker._resolve_pragma_overrides`.
- edge_cases_or_failure_modes: Ambiguous aliases, unsupported thinking levels, duplicate pragma order.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1625 `directory` `packages/coding-agent/src/extensibility/hooks`
- cursor: `[_]`
- core_role: Hook extensibility system for loading hook modules, registering events/commands/renderers, running hooks, and wrapping tools.
- algorithmic_behavior: `loader.ts:93` creates HookAPI; `loader.ts:165` imports hook modules and invokes default factory; `loader.ts:210` loads configured hooks; `runner.ts:48` manages hook lifecycle/context/commands/events; `tool-wrapper.ts:18` emits `tool_call` before execution and `tool_result` after success/error.
- inputs_outputs_state: Inputs are hook paths, session/model/UI context, AgentSession events, tool inputs/results; outputs are handlers, custom messages/entries, registered slash commands, modified context/tool results, or blocked tool calls.
- gates_or_invariants: `sendMessage`/`appendEntry` require initialized handlers; hook command context exposes session control only for commands; tool hook errors block execution fail-safe before tool call.
- dependencies_and_callers: Used by coding-agent session setup, discovery capability, tool registry wrapping, and custom command system.
- edge_cases_or_failure_modes: Dynamic import failure, hook missing default function, hook blocking/error, deadlock-prone session control avoided in event context.
- validation_or_tests: Tests include before-agent attribution and hook-injected message paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1655 `directory` `packages/mnemopi/src/core/extraction`
- cursor: `[_]`
- core_role: Cloud fact extraction client, diagnostics accounting, and extraction prompts for mnemopi memory.
- algorithmic_behavior: `client.ts:45` selects default/fallback models; `client.ts:60` uses `withAuth` and retries 429/rate errors up to 3 times per model; `client.ts:124` formats conversation messages; `client.ts:148` parses JSON array from model response. `diagnostics.ts:58` records tier attempts/success/failures and caps error samples.
- inputs_outputs_state: Inputs are chat messages, API key resolver, base URL, fetch implementation, and model response; outputs are extracted facts, diagnostics snapshots, and empty arrays on extraction failure.
- gates_or_invariants: Empty conversation returns no facts; all failed models record failure and return empty string/facts; diagnostics validate tier ids and sanitize/cap error samples.
- dependencies_and_callers: Used by mnemopi memory extraction workflows and tested by extraction integration tests.
- edge_cases_or_failure_modes: Rate limits, auth refresh/rotation, empty output, malformed JSON, no fact array, invalid tier names.
- validation_or_tests: `packages/mnemopi/test/extraction-integration.test.ts` validates success, malformed JSON, and backoff.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1685 `file` `packages/agent/test/utils/calculate.ts`
- cursor: `[_]`
- core_role: Test helper tool implementing a simple calculator AgentTool.
- algorithmic_behavior: Lines 9-15 evaluate expression with `new Function` and return text; lines 18-31 define arktype schema and `calculateTool`.
- inputs_outputs_state: Input is expression string; output is tool result text or thrown error.
- gates_or_invariants: Schema requires `expression`; runtime catches evaluation errors.
- dependencies_and_callers: Used by agent-core tests as a dummy tool.
- edge_cases_or_failure_modes: Arbitrary JS execution is acceptable only in test helper context.
- validation_or_tests: Helper used by tests; no standalone test.
- skip_candidate: `yes: test helper, not production core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1715 `file` `packages/ai/src/dialect/owned-stream.ts`
- cursor: `[_]`
- core_role: Stream dialect adapter that extracts owned/in-band tool calls from model text streams.
- algorithmic_behavior: Lines 13-26 define response-open tokens; lines 53-122 wrap streams and forward text/thinking/tool events while aborting/discarding fabricated tool responses; lines 176-225 salvage native tool start/delta/end; lines 227-248 scan text until response token; lines 277-293 flush/finalize; lines 367-420 parse in-band tool begin/delta/end.
- inputs_outputs_state: Inputs are provider message stream chunks and dialect projector state; outputs are normalized assistant stream events with text/toolUse/tool deltas and stop reason.
- gates_or_invariants: Prevents channel collision, stops scanning at response token, treats tool use as stop reason when found, and discards fabricated tool responses.
- dependencies_and_callers: Used by provider dialects that encode tool calls in content.
- edge_cases_or_failure_modes: Partial tool JSON, native/in-band overlap, stream abort, trailing scanner flush, malformed tool blocks.
- validation_or_tests: Indirect provider/tool stream tests exist outside assigned set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1745 `file` `packages/ai/src/providers/ollama.ts`
- cursor: `[_]`
- core_role: Ollama provider adapter for chat streaming, tools, images, reasoning, and usage metrics.
- algorithmic_behavior: Lines 97-104 normalize base URL; lines 108-136 map reasoning config; lines 138-175 map tool choice; lines 177-245 convert messages including images/tool results/thinking/tool calls; lines 326-354 parse NDJSON; lines 418-714 stream fetch, watchdog, parse text/thinking/tool calls, heal stream markup, record token/duration/TTFT, promote toolUse, and finalize errors.
- inputs_outputs_state: Inputs are model/messages/tools/options/auth/base URL; outputs are provider stream events, usage, durations, and final stop/error state.
- gates_or_invariants: Ollama-cloud assistant history strips thinking; tool choice supports named tools; pre-response watchdog catches hung streams.
- dependencies_and_callers: Implements `Provider` contract for Ollama/local/cloud models.
- edge_cases_or_failure_modes: NDJSON malformed chunks, slow first token, structured tool calls embedded in stream, image content conversion, unsupported tool choice.
- validation_or_tests: No assigned direct Ollama test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1775 `file` `packages/ai/src/registry/derived.ts`
- cursor: `[_]`
- core_role: Small derived provider registry for paste-code login aliases.
- algorithmic_behavior: Lines 7-9 derive paste-code login providers.
- inputs_outputs_state: Inputs are registry descriptors; output is derived provider list/map.
- gates_or_invariants: Derived entries are generated from known provider metadata.
- dependencies_and_callers: Used by auth/provider registry.
- edge_cases_or_failure_modes: Source provider descriptor drift.
- validation_or_tests: No direct test.
- skip_candidate: `yes: tiny static derivation, low algorithmic content`

### OH_MY_HUMANIZE_MAIN-HZ-1805 `file` `packages/ai/src/registry/opencode-zen.ts`
- cursor: `[_]`
- core_role: Provider registry entry for OpenCode Zen login integration.
- algorithmic_behavior: Lines 4-11 define provider and lazy login delegation to OpenCode OAuth.
- inputs_outputs_state: Inputs are OAuth controller options; output is login result from delegated provider.
- gates_or_invariants: Provider id/label/api base are static; login delegates rather than duplicating flow.
- dependencies_and_callers: Used by provider auth registry.
- edge_cases_or_failure_modes: Dynamic import/login failure; provider metadata drift.
- validation_or_tests: No direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1835 `file` `packages/ai/src/usage/kimi.ts`
- cursor: `[_]`
- core_role: Kimi usage reporting client for OAuth-backed Kimi Code accounts.
- algorithmic_behavior: Lines 45-65 parse reset times; lines 79-124 build usage windows/rows; lines 126-170 derive usage amounts/status/limits; lines 173-205 parse payload limits; lines 207-271 fetch usage with OAuth token, skip expired token, log failures, and return `UsageReport`.
- inputs_outputs_state: Inputs are auth storage credentials, optional fetch/signal, and API payload; outputs are normalized usage limits/report.
- gates_or_invariants: Expired tokens are skipped; malformed/unavailable usage returns null/failure logs rather than crashing.
- dependencies_and_callers: Used by usage/status surfaces in `packages/ai` and coding-agent status line.
- edge_cases_or_failure_modes: Missing token, expired token, reset time format variants, partial payloads, network failure.
- validation_or_tests: Usage-cache tests validate related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1865 `file` `packages/ai/test/helpers/fetch-mock.ts`
- cursor: `[_]`
- core_role: Test helper normalizing sync/async fake fetch handlers.
- algorithmic_behavior: Lines 3-8 wrap a handler as `FetchImpl`.
- inputs_outputs_state: Input is handler returning `Response` or promise; output is async `FetchImpl`.
- gates_or_invariants: None beyond type compatibility.
- dependencies_and_callers: Used by `packages/ai` tests.
- edge_cases_or_failure_modes: Handler exceptions propagate.
- validation_or_tests: Helper only.
- skip_candidate: `yes: test helper wrapper, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1895 `file` `packages/catalog/src/wire/codex.ts`
- cursor: `[_]`
- core_role: Codex wire constants and account id extraction helper.
- algorithmic_behavior: Lines 5-24 define constants; lines 32-43 parse JWT account id and return undefined on failure.
- inputs_outputs_state: Inputs are token/JWT strings; outputs are account id or undefined.
- gates_or_invariants: Malformed JWT is swallowed and mapped to undefined.
- dependencies_and_callers: Used by catalog/wire code for Codex identity/auth classification.
- edge_cases_or_failure_modes: Missing claim, invalid base64/json, non-JWT token.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1925 `file` `packages/coding-agent/src/capability/settings.ts`
- cursor: `[_]`
- core_role: Capability descriptor for discovered settings files.
- algorithmic_behavior: Lines 23-34 validate path/data and define no dedupe key.
- inputs_outputs_state: Inputs are settings capability items; output is validation error or accepted item.
- gates_or_invariants: Missing path/data rejected; no key means items are not deduped through this capability.
- dependencies_and_callers: Used by discovery/capability loading.
- edge_cases_or_failure_modes: Bad provider emits missing path/data.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1955 `file` `packages/coding-agent/src/cli/session-picker.ts`
- cursor: `[_]`
- core_role: TUI session picker for choosing/resuming/deleting sessions.
- algorithmic_behavior: Lines 14-80 build selector, lazy-load all sessions, apply history matcher, and support delete handler.
- inputs_outputs_state: Inputs are session storage/history, current cwd/query, and user selection/deletion; outputs are selected session id/path or deleted session state.
- gates_or_invariants: Matching is best-effort; deletion updates list without crashing picker.
- dependencies_and_callers: Used by CLI resume/session commands.
- edge_cases_or_failure_modes: Missing history, no sessions, deleted current row, matcher failure.
- validation_or_tests: Session ranking/history tests cover related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1985 `file` `packages/coding-agent/src/commands/grep.ts`
- cursor: `[_]`
- core_role: CLI grep command wrapper.
- algorithmic_behavior: Lines 9-47 map CLI flags to `GrepOutputMode` and invoke `runGrepCommand`.
- inputs_outputs_state: Inputs are command args/flags/cwd; output is grep command result/rendered output.
- gates_or_invariants: Output mode is constrained by known flags.
- dependencies_and_callers: CLI command dispatch calls this; underlying grep implementation handles search.
- edge_cases_or_failure_modes: Unknown/ambiguous flags handled by command parser upstream.
- validation_or_tests: No direct assigned grep command test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2015 `file` `packages/coding-agent/src/config/append-only-context-mode.ts`
- cursor: `[_]`
- core_role: Resolves append-only context mode from settings/model/provider compatibility.
- algorithmic_behavior: Lines 11-30 implement `auto`/`on`/`off`; auto enables for DeepSeek, Xiaomi host, or models/providers supporting store compatibility.
- inputs_outputs_state: Inputs are setting value, model id, host/provider compatibility; output is boolean mode.
- gates_or_invariants: Explicit on/off wins; auto is provider/model gated.
- dependencies_and_callers: Used by AgentSession/context construction.
- edge_cases_or_failure_modes: Provider host alias drift, compatibility metadata missing.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2045 `file` `packages/coding-agent/src/discovery/agents-md.ts`
- cursor: `[_]`
- core_role: Discovers `AGENTS.md` context files from cwd up to repo/home boundaries.
- algorithmic_behavior: Lines 21-59 walk up directories, read `AGENTS.md`, skip dot dirs, and attach provider/depth/source metadata; lines 61-67 register provider.
- inputs_outputs_state: Inputs are cwd/repo root/home; outputs are context file capability items.
- gates_or_invariants: Dot directories skipped; depth/source level metadata preserved; walk is bounded.
- dependencies_and_callers: Used by discovery/context loading before agent sessions.
- edge_cases_or_failure_modes: Missing/unreadable files, cwd inside hidden dirs, duplicate context levels.
- validation_or_tests: Context-file dedup tests validate downstream keying.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2075 `file` `packages/coding-agent/src/edit/streaming.ts`
- cursor: `[_]`
- core_role: Streaming edit preview parser/strategy registry.
- algorithmic_behavior: Lines 95-151 drop incomplete last edit from partial JSON; lines 198-280 implement replace/patch strategies; lines 312-363 render natural-order `apply_patch` previews; lines 364-438 parse hashline streaming sections/diffs; lines 442-496 parse `apply_patch` or fallback natural preview; lines 499-516 export strategy registry.
- inputs_outputs_state: Inputs are partial/final tool args, file content snippets, and edit formats; outputs are preview diff sections/added lines or parse errors.
- gates_or_invariants: Partial trailing lines/JSON are trimmed; incomplete streaming sections are tolerated; registry selects by edit variant/tool.
- dependencies_and_callers: Used by edit and tool execution renderers.
- edge_cases_or_failure_modes: Broken partial JSON, incomplete hashline section, unclosed patch hunk, parse errors during streaming.
- validation_or_tests: Streaming preview height tests validate behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2105 `file` `packages/coding-agent/src/goals/runtime.ts`
- cursor: `[_]`
- core_role: Runtime manager for goals, objectives, budgets, and goal-related steering.
- algorithmic_behavior: Lines 56-104 render remaining objectives and budget reports; lines 107-117 validate/account budget state; class methods around lines 117-513 serialize accounting via tail promise, snapshot/commit usage, mutate goals, create/replace/resume/pause/drop/complete, flush usage, and generate budget-limited steering.
- inputs_outputs_state: Inputs are goal commands, usage stats, tool/agent/task/resume events, and budgets; outputs are goal state, steering messages, and persisted accounting.
- gates_or_invariants: Accounting mutations are serialized; budget checks gate continuation/steering; completed/dropped goals update state atomically.
- dependencies_and_callers: Used by AgentSession goal/task runtime and TUI displays.
- edge_cases_or_failure_modes: Concurrent usage commits, budget exhaustion, stale resume state, dropped/paused goals.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2135 `file` `packages/coding-agent/src/lib/xai-http.ts`
- cursor: `[_]`
- core_role: xAI HTTP helper for base URL and credential selection.
- algorithmic_behavior: Lines 15-17 define user agent; lines 51-70 resolve base URL precedence from model/provider/env/default; lines 103-124 choose credentials preferring dedicated xAI OAuth over generic xAI.
- inputs_outputs_state: Inputs are model override, provider config, env, auth storage/session; outputs are base URL and auth headers/credentials.
- gates_or_invariants: Explicit override precedence is stable; auth selection avoids falling back incorrectly when dedicated credential exists.
- dependencies_and_callers: Used by xAI provider/client code.
- edge_cases_or_failure_modes: Missing credentials, env/config conflict, model-specific base override.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2165 `file` `packages/coding-agent/src/mcp/timeout.ts`
- cursor: `[_]`
- core_role: MCP timeout resolver and timeout signal helper.
- algorithmic_behavior: Lines 8-18 resolve timeout from env/config/default; lines 20-31 describe enabled/disabled timeout; lines 33-59 create timeout `AbortSignal` and classify timeout aborts.
- inputs_outputs_state: Inputs are settings/env timeout values and optional parent signal; outputs are timeout signal, description, or timeout classification.
- gates_or_invariants: Disabled/never timeout yields no abort; parent abort composes with timeout when enabled.
- dependencies_and_callers: Used by MCP client/tool requests.
- edge_cases_or_failure_modes: Invalid timeout values, parent abort vs timeout abort distinction.
- validation_or_tests: MCP reconnect tests validate abort propagation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2195 `file` `packages/coding-agent/src/modes/session-observer-registry.ts`
- cursor: `[_]`
- core_role: Tracks observable main/subagent sessions for TUI dashboards.
- algorithmic_behavior: Lines 34-66 manage listener/sort ordering; lines 68-78 set main session; lines 80-99 sort main first and subagents by parent group/index/stable order; lines 134-220 subscribe to lifecycle/progress channels and update sessions.
- inputs_outputs_state: Inputs are event bus lifecycle/progress payloads; outputs are `ObservableSession` snapshots and change notifications.
- gates_or_invariants: Unknown statuses ignored; repeated event-bus subscriptions dispose previous ones; parent sort order groups detached subagents.
- dependencies_and_callers: Used by interactive mode dashboards/status components and task subagent event bus.
- edge_cases_or_failure_modes: Progress before lifecycle creates active session; session switch resets tracked sessions while preserving subscriptions; stale parent ids.
- validation_or_tests: Indirectly covered by subagent/RPC tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2225 `file` `packages/coding-agent/src/session/session-entries.ts`
- cursor: `[_]`
- core_role: Defines serialized session JSONL entry union and usage statistics shape.
- algorithmic_behavior: Lines 4-17 define header; lines 25-178 define entry variants for messages, model/service tier, compaction, branch summary, custom entries/messages, labels, TTSR, MCP selection, init, and mode; lines 191-198 define usage stats.
- inputs_outputs_state: Inputs are runtime session events; outputs are typed entries written/read from session storage.
- gates_or_invariants: Entry variants encode discriminated `type` fields for loader/renderers.
- dependencies_and_callers: Used by session manager/loader, RPC transcript, TUI transcript, storage tests.
- edge_cases_or_failure_modes: Schema drift can break old session replay.
- validation_or_tests: Redis/session/history/RPC tests exercise entries.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2255 `file` `packages/coding-agent/src/stt/downloader.ts`
- cursor: `[_]`
- core_role: Ensures STT recorder/model dependencies and streams speech model download progress.
- algorithmic_behavior: Lines 49-76 check model cache completeness for sherpa and transformers Whisper shards; lines 86-122 download selected model via worker and aggregate per-file loaded/total into integer percent; lines 125-139 ensure recorder then model.
- inputs_outputs_state: Inputs are model key/name, abort signal, progress callback, cache dir; outputs are progress events and ready model cache.
- gates_or_invariants: Partial model files are not considered cached; failed worker download throws; progress aggregates known file totals.
- dependencies_and_callers: Uses `sttClient`, model specs, recorder ensure, tiny model cache dir.
- edge_cases_or_failure_modes: Interrupted `.part` downloads, missing encoder/decoder shard, abort signal, worker/network failure.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2285 `file` `packages/coding-agent/src/tool-discovery/mode.ts`
- cursor: `[_]`
- core_role: Resolves tool discovery mode from settings and tool count.
- algorithmic_behavior: Lines 4-23 exclude search tool and auto-select MCP-only discovery above threshold or when MCP discovery is configured; otherwise off.
- inputs_outputs_state: Inputs are tool names/count and settings; output is discovery mode enum.
- gates_or_invariants: Search tool is excluded from count; threshold is 40.
- dependencies_and_callers: Used by tool registry/session prompt construction.
- edge_cases_or_failure_modes: Large tool lists without discovery, MCP-only mode when no MCP discovery configured.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2315 `file` `packages/coding-agent/src/tools/github-cache.ts`
- cursor: `[_]`
- core_role: SQLite-backed GitHub tool cache with TTL, auth identity scoping, stale refresh, and invalidation.
- algorithmic_behavior: Lines 90-142 open DB and run migrations; lines 142-168 sweep expired entries; lines 205-245 resolve hashed auth identity from env/gh host; lines 249-365 implement get/put/invalidate; lines 493-504 resolve TTL settings; lines 532-660 implement fresh/stale/background refresh lookup.
- inputs_outputs_state: Inputs are repo/kind/number/auth/settings/fetcher; outputs are cached views, freshness notes, refreshed data, invalidations.
- gates_or_invariants: Cache scoped by repo/kind/auth key; hard TTL evicts; soft TTL serves stale only when enabled and schedules background refresh without duplicate inflight refreshes.
- dependencies_and_callers: Used by GitHub tool operations for issues/PRs/diffs.
- edge_cases_or_failure_modes: DB unavailable, auth identity changes, stale data, background refresh failure, repo normalization.
- validation_or_tests: GitHub tool tests cover downstream behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2345 `file` `packages/coding-agent/src/tools/review.ts`
- cursor: `[_]`
- core_role: Review finding reporting tool and aggregator.
- algorithmic_behavior: Lines 19-37 define priority metadata; lines 55-79 define schema/priority guard; lines 79-119 parse and validate finding details; lines 120-181 execute/render report-finding tool; lines 200-249 aggregate grouped findings.
- inputs_outputs_state: Inputs are finding title/body/priority/confidence/file/line; outputs are structured review findings and grouped review summary.
- gates_or_invariants: Required finding fields are validated; priorities restricted to known set.
- dependencies_and_callers: Used by code-review mode/prompt tooling and review agent workflows.
- edge_cases_or_failure_modes: Missing file/line, unknown priority, malformed details, duplicate findings.
- validation_or_tests: No direct assigned review tool test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2375 `file` `packages/coding-agent/src/tui/types.ts`
- cursor: `[_]`
- core_role: Shared TUI type definitions for coding-agent renderers.
- algorithmic_behavior: Lines 6-15 define state union and tree rendering context shape.
- inputs_outputs_state: Inputs are none; outputs are TypeScript types.
- gates_or_invariants: State ids limited to pending/running/success/error/warning.
- dependencies_and_callers: Used by coding-agent TUI components.
- edge_cases_or_failure_modes: Type drift only.
- validation_or_tests: Compile-time coverage only.
- skip_candidate: `yes: type-only helper, not algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-2405 `file` `packages/coding-agent/src/utils/turndown.ts`
- cursor: `[_]`
- core_role: HTML-to-Markdown conversion helper with GFM/table normalization.
- algorithmic_behavior: Lines 17-57 configure GFM turndown rules; lines 64-83 normalize table output.
- inputs_outputs_state: Input is HTML; output is Markdown text.
- gates_or_invariants: Tables and GFM elements are normalized for downstream text consumption.
- dependencies_and_callers: Used by web scraping/browser content conversion.
- edge_cases_or_failure_modes: Malformed HTML, odd table structures, excessive whitespace.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2435 `file` `packages/coding-agent/src/workflow/scheduler.ts`
- cursor: `[_]`
- core_role: DAG workflow scheduler for node activations, concurrency, joins, state patches, and abort handling.
- algorithmic_behavior: Lines 65-219 run scheduler loop with activation queue, concurrency, max activation/node gates, aborts, statePatch/output recording, child enqueue, and frontier updates; lines 222-256 execute activation and map success/error/aborted; lines 262-296 enqueue ready children with conditions/join waits; lines 322-361 seed maps; lines 392-480 manage join lineage.
- inputs_outputs_state: Inputs are workflow definition/initial state/runtime host/options; outputs are activation records, workflow state, node outputs, errors, and final run result.
- gates_or_invariants: Max activations and per-node activation caps prevent runaway loops; joins wait for required parents; abort propagates structured reason.
- dependencies_and_callers: Used by workflow runtime/session integration.
- edge_cases_or_failure_modes: Cycles handled upstream, join waits, condition false, activation errors, abort races, duplicate ids.
- validation_or_tests: `workflow/session-runtime.test.ts` validates runtime host output mapping; scheduler itself indirectly covered.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2465 `file` `packages/coding-agent/test/core/python-executor-mapping.test.ts`
- cursor: `[_]`
- core_role: Tests Python kernel execution result mapping.
- algorithmic_behavior: Lines 17-39 assert timeout cancellations annotate output and error status maps to nonzero exit code with traceback.
- inputs_outputs_state: Inputs are fake kernel results/chunks and timeout; outputs are `PythonResult` fields.
- gates_or_invariants: Cancelled timeout has no exit code; error status maps to exit code 1 and preserves output.
- dependencies_and_callers: Validates `executePythonWithKernel`.
- edge_cases_or_failure_modes: Timeout annotation, stdin flag preservation, missing traceback.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2495 `file` `packages/coding-agent/test/discovery/context-file-dedup.test.ts`
- cursor: `[_]`
- core_role: Tests context-file capability keying and validation.
- algorithmic_behavior: Lines 13-53 assert user-level files share one key, project files dedupe by depth, missing depth defaults to 0, and user/project keys do not collide; lines 55-67 validate missing path rejection.
- inputs_outputs_state: Inputs are `ContextFile` items; outputs are dedupe keys or validation errors.
- gates_or_invariants: Project depth is part of key; all user-level context shares a key.
- dependencies_and_callers: Validates context discovery/merging behavior.
- edge_cases_or_failure_modes: Duplicate AGENTS/CLAUDE files, user/project collision, missing path.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2525 `file` `packages/coding-agent/test/helpers/acp-schema.ts`
- cursor: `[_]`
- core_role: ACP schema assertion helpers for tests.
- algorithmic_behavior: Lines 4-18 run arktype schema validation and assert accept/reject.
- inputs_outputs_state: Inputs are schema and value; outputs are test assertions.
- gates_or_invariants: Rejection path expects arktype errors.
- dependencies_and_callers: Used by ACP tests.
- edge_cases_or_failure_modes: Non-Error validation issue formatting.
- validation_or_tests: Helper only.
- skip_candidate: `yes: test assertion helper, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2555 `file` `packages/coding-agent/test/modes/image-references.test.ts`
- cursor: `[_]`
- core_role: Tests image/paste placeholder rendering and image marker renumbering.
- algorithmic_behavior: Lines 23-48 classify image/paste markers, bare image form, char-count paste form, plain text, and unterminated marker behavior; lines 51-69 shift only image markers by offset.
- inputs_outputs_state: Inputs are message text and offset; outputs are rendered placeholders/reference metadata and shifted text.
- gates_or_invariants: Unterminated marker remains plain text; paste markers are never renumbered.
- dependencies_and_callers: Validates `modes/image-references`.
- edge_cases_or_failure_modes: Half-deleted markers, marker index drift, paste/image confusion.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2585 `file` `packages/coding-agent/test/session/redis-session-storage.test.ts`
- cursor: `[_]`
- core_role: Functional tests for Redis-backed session storage.
- algorithmic_behavior: Lines 167-260 validate write metadata, warm index via `STRLEN`, direct-child glob listing, monotonic mtimes, writer append/drain, truncation, drain error surfacing, delete with sidecar artifacts, and refresh behavior.
- inputs_outputs_state: Inputs are fake Redis client operations and session/artifact paths; outputs are Redis strings/hashes, metadata index, and storage reads.
- gates_or_invariants: `create()` should not GET huge content; `drain()` surfaces background writer failures; delete removes JSONL plus artifact prefix.
- dependencies_and_callers: Validates `RedisSessionStorage`.
- edge_cases_or_failure_modes: Background append failure, rapid writes mtime order, nested artifact deletion, peer process refresh.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2615 `file` `packages/coding-agent/test/task/executor-pass-through.test.ts`
- cursor: `[_]`
- core_role: Tests subagent executor forwards parent-discovered state to session creation.
- algorithmic_behavior: Lines 92-142 assert `rules`, `preloadedExtensionPaths`, and `preloadedCustomToolPaths` are forwarded by identity; lines 144-171 assert undefined forwarding when absent and correct `parentAgentId`.
- inputs_outputs_state: Inputs are runSubprocess options and mocked session; outputs are `createAgentSession` call args and task result.
- gates_or_invariants: Parent-discovered arrays are not cloned; parent agent id differs from child id/prefix.
- dependencies_and_callers: Validates task executor/subagent spawning.
- edge_cases_or_failure_modes: Re-scanning filesystem unnecessarily, self-parent bug, lost extension/tool state.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2645 `file` `packages/coding-agent/test/tools/bash-interceptor.test.ts`
- cursor: `[_]`
- core_role: Tests bash command interception, validation, and head/tail stripping.
- algorithmic_behavior: Lines 31-61 validate interception before and after leading `cd` normalization; lines 65-84 validate default echo/printf redirect blocking; lines 87-100 validate async arg preservation; lines 103-151 validate optional stripping of `head`/`tail`.
- inputs_outputs_state: Inputs are bash commands, enabled rules, settings, and available tool names; outputs are block errors or executed command results.
- gates_or_invariants: Original and cwd-normalized commands are both inspected; redirects inside quotes/fd dup are not blocked; disabled async reports explicit error.
- dependencies_and_callers: Validates bash tool/interceptor.
- edge_cases_or_failure_modes: Hidden `cd`, unsafe write redirects, quoted `>` false positives, head/tail truncating command output.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2675 `file` `packages/coding-agent/test/tools/gh.test.ts`
- cursor: `[_]`
- core_role: Large contract suite for GitHub tool operations, search queries, PR checkout/push, diff parsing, cache/artifacts, and git locking.
- algorithmic_behavior: Lines 212-256 parse unified diffs including quoted paths and hunk marker content; lines 258+ validate repo view, PR create, search issue/PR/commit/code/repo queries, date qualifier parsing, default repo resolution, PR checkout worktrees, git remote idempotency, repo locks, PR push metadata rejection, schema shape, and failed job log artifact saving.
- inputs_outputs_state: Inputs are gh/gith mocks, temp git repos/remotes, tool args, artifacts dir, and settings; outputs are rendered text, worktrees, git config, artifact files, and tool details.
- gates_or_invariants: PR create uses `--body-file`; leading-dash search terms go through `gh api` form fields; explicit repo overrides defaults; PR push requires checkout metadata; repo mutations serialize through lock.
- dependencies_and_callers: Validates `GithubTool`, `utils/git`, GitHub cache/artifact flows.
- edge_cases_or_failure_modes: Quoted diff paths, same/cross-repo PR checkout, stale remotes, default repo miss, code search unsupported date qualifiers, long failed logs.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2705 `file` `packages/coding-agent/test/tools/resolve.test.ts`
- cursor: `[_]`
- core_role: Tests pending-action resolve tool and renderer.
- algorithmic_behavior: Lines 31-123 validate required schema fields, no-pending apply error, discard no-op success, discard/apply handler propagation; lines 125-175 validate highlighted apply summary and ANSI reset behavior.
- inputs_outputs_state: Inputs are pending queue handler and action/reason args; outputs are resolved tool result/details and rendered component.
- gates_or_invariants: `discard` without pending action is successful cancellation; `apply` requires pending action; renderer avoids mid-line fg reset.
- dependencies_and_callers: Validates `ResolveTool` and renderer.
- edge_cases_or_failure_modes: Stale pending action, missing reason, visual style reset breaking inverse block.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2735 `file` `packages/coding-agent/test/tui/status-line-newline-guard.test.ts`
- cursor: `[_]`
- core_role: Tests status-line sanitization against embedded newlines.
- algorithmic_behavior: Lines 10-40 assert descriptions/meta entries flatten LF/CRLF and preserve text.
- inputs_outputs_state: Inputs are status line title/description/meta; output is sanitized one-line rendering.
- gates_or_invariants: Tool output cannot inject new terminal lines into status/header.
- dependencies_and_callers: Validates `renderStatusLine` and `sanitizeText`.
- edge_cases_or_failure_modes: LF/CRLF in command descriptions or meta strings corrupting TUI layout.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2765 `file` `packages/coding-agent/test/workflow/session-runtime.test.ts`
- cursor: `[_]`
- core_role: Tests workflow session runtime host mapping for script, shell, agent, review, and human nodes.
- algorithmic_behavior: Lines 58-160 map JS/Python scripts to eval runner and pass timeouts; lines 162-215 map shell scripts; lines 217-260 parse structured stdout JSON; later tests map agent task requests, artifact references, bounded summaries, structured yield data, abort signals, provider diagnostics, and review verdicts.
- inputs_outputs_state: Inputs are workflow YAML nodes, activation ids, fake runtime adapters, outputs/errors; outputs are workflow activation outputs, artifacts, state patches, and thrown diagnostics.
- gates_or_invariants: Agent nodes require adapter; local session paths are not persisted in artifacts; long summaries are bounded; final JSON stdout line can define structured output.
- dependencies_and_callers: Validates `createSessionWorkflowRuntimeHost`, workflow definition parsing, and node runtime execution.
- edge_cases_or_failure_modes: Missing adapter, nonzero agent errors with provider context, object summary treated as unstructured, abort propagation.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2795 `file` `packages/mnemopi/src/core/entities.ts`
- cursor: `[_]`
- core_role: Entity extraction and similarity helper for memory/recall.
- algorithmic_behavior: Lines 120-131 define stop words/patterns; lines 137-165 compute Levenshtein distance; lines 166-189 compute similarity; lines 196-239 regex-extract entities with guards; lines 242-258 find similar entities.
- inputs_outputs_state: Inputs are text/entities; outputs are extracted entity strings and similarity matches.
- gates_or_invariants: Filters stopwords, numeric/noise patterns, max chars, substrings, and low similarity.
- dependencies_and_callers: Used by mnemopi memory extraction/recall indexing.
- edge_cases_or_failure_modes: Over-extraction from code/noise, substring duplicates, non-English tokenization limits.
- validation_or_tests: Mnemopi tests cover higher-level extraction/recall.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2825 `file` `packages/mnemopi/src/migrations/e6-triplestore-split.ts`
- cursor: `[_]`
- core_role: Migration re-export shim.
- algorithmic_behavior: Line 1 re-exports `../core/migrations/e6-triplestore-split`.
- inputs_outputs_state: Input/output are compile-time module resolution only.
- gates_or_invariants: No logic.
- dependencies_and_callers: Keeps legacy migration import path working.
- edge_cases_or_failure_modes: Broken re-export path.
- validation_or_tests: Compile-time/import coverage only.
- skip_candidate: `yes: re-export shim, not algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2855 `file` `packages/tui/src/components/tab-bar.ts`
- cursor: `[_]`
- core_role: TUI horizontal tab bar component with keyboard/mouse selection and responsive label shortening.
- algorithmic_behavior: Lines 56-143 manage active index, tab replacement, muted tabs, and next/previous navigation; lines 145-160 handle Tab/Arrow keys; lines 169+ render chunks, shrink labels to short forms when width is constrained, and track hit zones.
- inputs_outputs_state: Inputs are tab list, active id/index, theme, width, key/mouse events; outputs are styled tab rows, active tab state, callbacks, and hit zones.
- gates_or_invariants: Muted tabs are skipped by navigation/selection; active index clamps to valid range; short labels collapse farthest from active first.
- dependencies_and_callers: Used by settings/setup/mode UI components in coding-agent.
- edge_cases_or_failure_modes: Empty tabs, width too narrow, active id removed during setTabs, hover on muted tab.
- validation_or_tests: No direct assigned tab-bar test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2885 `directory` `packages/coding-agent/src/extensibility/custom-commands/bundled`
- cursor: `[_]`
- core_role: Bundled custom commands for CI-green and review workflows.
- algorithmic_behavior: `ci-green/index.ts:7` reads current tag/branch/remote and `GreenCommand` prompts/runs CI-green behavior; `review/index.ts:121` parses diffs, `review/index.ts:180` recommends agent counts, `review/index.ts:235` builds review prompts, `review/index.ts:297` parses GitHub PR URLs, and `review/index.ts:475` implements command flow.
- inputs_outputs_state: Inputs are custom command args, git diff/status/branches, recent PR refs, and hook command context; outputs are prompts, subagent review tasks, or command UI messages.
- gates_or_invariants: Review excludes generated/noisy paths, caps inline diff chars/files, validates PR refs, and chooses large-diff instructions when needed.
- dependencies_and_callers: Registered through hook/custom command extensibility.
- edge_cases_or_failure_modes: No diff, large diff, invalid PR ref, uncommitted git/jj diff differences, branch lookup failure.
- validation_or_tests: No direct assigned bundled command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2915 `file` `crates/pi-shell/src/minimizer/filters/listing.rs`
- cursor: `[_]`
- core_role: Shell-output minimizer for listings/searches/manifests/source outlines.
- algorithmic_behavior: Lines 12-40 detect NUL/path-only output; lines 43-84 dispatch by program; lines 105-199 group/compact grep matches; lines 202-303 parse/truncate match text; lines 320-407 compact find output by dirs; lines 423-535 parse/compact `ls -l`; lines 538-779 summarize cat manifests; lines 781-1152 outline source and strip bodies; lines 1154-1206 compact summary outputs.
- inputs_outputs_state: Inputs are command context, raw stdout, exit code, minimizer config; outputs are passthrough or transformed compact summaries with original length.
- gates_or_invariants: Nonzero exits and NUL/custom find output stay opaque; legacy filter switch preserves old behavior; aggressive source strip avoids Rust raw strings.
- dependencies_and_callers: Used by `pi-shell` command minimization before displaying/tool-feeding long outputs.
- edge_cases_or_failure_modes: Multibyte leading whitespace, grep hunk marker text, noisy dirs, device-file sizes, malformed manifests, braces in strings/macros.
- validation_or_tests: Internal Rust tests begin after line 1206 and cover output invariants.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2945 `file` `packages/ai/src/registry/oauth/xiaomi.ts`
- cursor: `[_]`
- core_role: Xiaomi MiMo and Token Plan login/validation controller.
- algorithmic_behavior: Lines 46-69 classify token-plan keys and choose validation endpoints; lines 73-135 POST minimal chat completion with per-endpoint timeout and SGP/AMS/CN fallback; lines 144-168 implement standard login; lines 175-199 implement regional Token Plan login.
- inputs_outputs_state: Inputs are pasted API key, selected token-plan region, abort signal, and fetch override; outputs are validated API key string or errors.
- gates_or_invariants: Empty key rejected; caller abort throws login cancelled; region-specific login validates only selected cluster; generic token-plan key tries SGP then AMS then CN.
- dependencies_and_callers: Used by AI auth registry for Xiaomi providers.
- edge_cases_or_failure_modes: Regional timeout should fall through unless caller aborted; 401 tries next endpoint; non-auth errors throw immediately.
- validation_or_tests: No assigned direct Xiaomi test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2975 `file` `packages/coding-agent/src/cli/gallery-fixtures/index.ts`
- cursor: `[_]`
- core_role: Aggregates hand-written renderer fixtures for `omp gallery`.
- algorithmic_behavior: Lines 16-25 import subsystem fixture groups; lines 29-40 merge them in display order.
- inputs_outputs_state: Inputs are fixture maps; output is `galleryFixtures`.
- gates_or_invariants: Missing tool fixture falls back elsewhere; this file only aggregates.
- dependencies_and_callers: Used by gallery CLI visual QA.
- edge_cases_or_failure_modes: Fixture key collisions/order changes.
- validation_or_tests: Visual QA path, not runtime tests.
- skip_candidate: `yes: static fixture aggregator, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3005 `file` `packages/coding-agent/src/discovery/builtin-rules/index.ts`
- cursor: `[_]`
- core_role: Bundles default rule markdown sources into runtime discovery.
- algorithmic_behavior: Lines 11-28 import embedded rule markdown; lines 37-56 expose ordered `BUILTIN_RULE_SOURCES`.
- inputs_outputs_state: Inputs are static markdown assets; output is ordered rule source array.
- gates_or_invariants: Embedded text survives compiled binary; lower-priority provider lets project/user/tool rules override same names.
- dependencies_and_callers: Used by rule discovery/default rule provider.
- edge_cases_or_failure_modes: Missing embedded asset, duplicate rule names, ordering drift.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3035 `file` `packages/coding-agent/src/eval/py/executor.ts`
- cursor: `[_]`
- core_role: Python eval executor managing kernels, sessions, cancellation, timeouts, env, and result mapping.
- algorithmic_behavior: Lines 145-161 build session keys; lines 178-253 handle deadlines/cancellation; lines 297-337 build kernel env; lines 340-428 start/acquire/reset kernels; lines 439-497 dispose by all/owner; lines 505-600 execute with kernel and map output/errors/stdin/timeouts; lines 641-700 execute on reusable session with retry/replacement; lines 704-738 expose public APIs.
- inputs_outputs_state: Inputs are code, cwd, session id, interpreter, timeout/deadline/signal, owner id; outputs are `PythonResult`, kernel sessions, and disposal side effects.
- gates_or_invariants: Dead kernels are replaced; timeout cancellation returns annotated result; owner disposal only affects owned sessions; per-call mode ensures bridge/kernel availability.
- dependencies_and_callers: Used by eval tools and workflow script runtime.
- edge_cases_or_failure_modes: Timeout, stdin request, kernel death, reset race, cancellation, interpreter path normalization.
- validation_or_tests: `python-executor-mapping.test.ts` validates result mapping.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3065 `file` `packages/coding-agent/src/extensibility/hooks/tool-wrapper.ts`
- cursor: `[_]`
- core_role: AgentTool wrapper that emits hook callbacks around tool execution.
- algorithmic_behavior: Lines 18-50 emit `tool_call` and block on hook result/error; lines 53-82 execute tool and allow `tool_result` modifications; lines 84-99 emit error result events then rethrow original error.
- inputs_outputs_state: Inputs are tool call id, params, signal, update callback, hook runner; outputs are original/modified tool result or thrown hook/tool error.
- gates_or_invariants: Hook failure before execution is fail-safe block; update callback passes through; error events are observable without swallowing original error.
- dependencies_and_callers: Used when hooks are enabled in tool registry.
- edge_cases_or_failure_modes: Hook modifies content/details type, hook blocks valid tool, hook throws during error observation.
- validation_or_tests: Hook/tool behavior covered indirectly by hook/session tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3095 `file` `packages/coding-agent/src/modes/acp/index.ts`
- cursor: `[_]`
- core_role: ACP mode barrel export.
- algorithmic_behavior: Re-exports `acp-agent` and `acp-mode`.
- inputs_outputs_state: Module import surface only.
- gates_or_invariants: No runtime logic here.
- dependencies_and_callers: Used by ACP consumers importing from directory index.
- edge_cases_or_failure_modes: Export omission.
- validation_or_tests: ACP tests use exported modules elsewhere.
- skip_candidate: `yes: barrel export only`

### OH_MY_HUMANIZE_MAIN-HZ-3125 `file` `packages/coding-agent/src/modes/components/index.ts`
- cursor: `[_]`
- core_role: TUI components barrel export for coding-agent modes.
- algorithmic_behavior: Lines 1-49 star-export assistant messages, tool execution, selectors, status line, transcript, workflow, and other components.
- inputs_outputs_state: Module import surface only.
- gates_or_invariants: No runtime logic here.
- dependencies_and_callers: Used by modes importing component APIs.
- edge_cases_or_failure_modes: Export omission/ambiguity.
- validation_or_tests: Compile/import coverage only.
- skip_candidate: `yes: barrel export only`

### OH_MY_HUMANIZE_MAIN-HZ-3155 `file` `packages/coding-agent/src/modes/components/transcript-container.ts`
- cursor: `[_]`
- core_role: Transcript composition engine enforcing native scrollback commit safety while rendering current block content.
- algorithmic_behavior: Lines 250-415 derive live commit state from previous/current block rows, append-only growth, volatile cooldown, stable-prefix windows, and rewrite floors; lines 419-806 render blocks incrementally, strip blank edges, maintain persistent rows/segments, expose live/commit/snapshot-safe boundaries, and render viewport tail efficiently.
- inputs_outputs_state: Inputs are child components, render width, block finalization/version/commit-stable protocols, and committed row count; outputs are persistent row array and native scrollback boundary reports.
- gates_or_invariants: Unfinalized/provisional blocks stay below commit seam; finalized committed rows can be reused only when version/finalized state matches; width/global invalidation retires snapshots.
- dependencies_and_callers: Used by interactive transcript renderer and TUI engine native scrollback logic.
- edge_cases_or_failure_modes: Streaming markdown reflow, late tool result below notices, post-finalize mutation, width change, empty blocks, provisional preview duplication.
- validation_or_tests: `transcript-container.test.ts` extensively validates these invariants.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3185 `file` `packages/coding-agent/src/modes/rpc/rpc-subagents.ts`
- cursor: `[_]`
- core_role: RPC subagent registry and transcript reader.
- algorithmic_behavior: Lines 68-105 read session JSONL from byte cursor, reset when cursor exceeds file size, parse complete lines only, and return messages; lines 107-240 track lifecycle/progress/event frames, stale ids, transcript session references, subscription levels, and selector resolution.
- inputs_outputs_state: Inputs are event bus payloads, subscription level, session file/fromByte selectors; outputs are RPC subagent frames, snapshots, and transcript message chunks.
- gates_or_invariants: Progress ignored for stale/unknown subagents; terminal lifecycle removes active snapshot but retains transcript reference; session file selector must be known.
- dependencies_and_callers: Used by RPC mode clients and subagent viewers.
- edge_cases_or_failure_modes: Truncated JSONL line, file shrink/reset, owner mismatch by parentToolCallId/sessionFile, stale subagent id after clear.
- validation_or_tests: RPC/subagent tests likely cover external behavior; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3215 `file` `packages/coding-agent/src/tools/browser/launch.ts`
- cursor: `[_]`
- core_role: Puppeteer/Chromium launcher with safe loading, executable resolution, viewport, UA spoofing, and stealth patch injection.
- algorithmic_behavior: Lines 53-79 lazy-load puppeteer from safe cwd; lines 94-149 lazily install Chromium unless system/env path exists; lines 163-236 resolve system Chrome candidates; lines 244-281 launch browser with proxy/cert args; lines 330-370 patch sourceURL/errors; lines 374-440 build UA metadata; lines 474-529 configure target UA overrides; lines 552-665 build/inject stealth scripts.
- inputs_outputs_state: Inputs are viewport/headless options, env proxy/executable settings, browser/page/session state; outputs are launched browser, viewport, UA override, and injected scripts.
- gates_or_invariants: System/env browser wins over download; install promise resets on failure; target UA setup uses soft timeout; stealth patch idempotent by client weak set.
- dependencies_and_callers: Used by browser/web tools and Puppeteer eval paths.
- edge_cases_or_failure_modes: Malformed project package.json during import, missing platform, Chromium download failure, proxy loopback bypass, CDP no-resource errors, target attach timeout.
- validation_or_tests: Browser stealth helpers have test exports; no assigned browser launch test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3245 `file` `packages/coding-agent/src/web/scrapers/github-gist.ts`
- cursor: `[_]`
- core_role: Special scraper for GitHub Gist URLs via GitHub API.
- algorithmic_behavior: Lines 13-24 parse gist URL/id and validate hex id; lines 25-54 fetch `/gists/{id}`, format metadata and file contents into Markdown, and build result.
- inputs_outputs_state: Inputs are URL, timeout, abort signal; outputs are `RenderResult` markdown or null.
- gates_or_invariants: Only `gist.github.com` and hex gist ids are handled; API failure returns null.
- dependencies_and_callers: Used by web scraper special-handler chain; depends on GitHub API fetch helper.
- edge_cases_or_failure_modes: Anonymous gist path, invalid id, API failure, large file contents.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3275 `file` `packages/coding-agent/src/web/scrapers/pypi.ts`
- cursor: `[_]`
- core_role: Special scraper for PyPI project pages via JSON APIs.
- algorithmic_behavior: Lines 13-20 parse `pypi.org/project/{package}`; lines 27-31 fetch package JSON and pypistats in parallel; lines 35-60 parse stats/package data; lines 63-108 render package metadata, URLs, dependencies, description.
- inputs_outputs_state: Inputs are URL, timeout, abort signal; outputs are Markdown `RenderResult` or null.
- gates_or_invariants: Non-PyPI/non-project URLs return null; failed package API returns null; download stats are optional.
- dependencies_and_callers: Used by web scraper special-handler chain.
- edge_cases_or_failure_modes: Invalid JSON, missing fields, stats timeout capped to 5 seconds, huge descriptions.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3305 `file` `packages/coding-agent/src/web/search/utils.ts`
- cursor: `[_]`
- core_role: Small search provider utility functions.
- algorithmic_behavior: Lines 1-10 convert ISO date to age seconds; lines 13-17 clamp result count to `[1,max]` with default.
- inputs_outputs_state: Inputs are date string and numeric result count; outputs are age seconds or clamped count.
- gates_or_invariants: Invalid/missing dates return undefined; absent/NaN count uses default.
- dependencies_and_callers: Used by search providers and source conversion.
- edge_cases_or_failure_modes: Future dates produce negative age; zero count becomes default.
- validation_or_tests: No direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3335 `file` `packages/coding-agent/test/modes/components/transcript-container.test.ts`
- cursor: `[_]`
- core_role: Comprehensive tests for transcript container rendering, spacing, stable-prefix reporting, live-region selection, and viewport-tail rendering.
- algorithmic_behavior: Lines 156-418 test mutable/finalized/streaming/provisional block behavior and native scrollback commit safety; lines 420-486 test spacing/blank stripping; lines 488-576 test stable-prefix floor; lines 578-614 test live-region membership; lines 616-680 test viewport tail rendering.
- inputs_outputs_state: Inputs are fake components with finalization/version/commit-stable protocols and widths; outputs are rendered rows and commit/live/stable metrics.
- gates_or_invariants: Provisional previews never commit; durable streaming heads promote after stability window; finalized committed rows skip render unless version changes.
- dependencies_and_callers: Validates `TranscriptContainer`.
- edge_cases_or_failure_modes: Late re-layout after newer blocks, assistant interruption finalization, post-finalize error unpin, width changes, empty blocks.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3365 `file` `packages/coding-agent/test/modes/theme/settings-list-theme.test.ts`
- cursor: `[_]`
- core_role: Tests settings-list theme styling for dirty values under selection.
- algorithmic_behavior: Lines 8-23 assert modified labels/values stay dirty-colored even when selected, while default selected value uses accent.
- inputs_outputs_state: Inputs are selected/changed flags and text; output is themed ANSI string.
- gates_or_invariants: Dirty state visually overrides selected state where appropriate.
- dependencies_and_callers: Validates theme helpers used by settings UI.
- edge_cases_or_failure_modes: Selected row hiding dirty state.
- validation_or_tests: This file is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3395 `file` `packages/collab-web/src/components/agents/AgentDrawer.tsx`
- cursor: `[_]`
- core_role: Collaboration web drawer for viewing/controlling a subagent and polling its transcript.
- algorithmic_behavior: Lines 28-73 register Escape close, poll transcript every 1200 ms by byte cursor, parse JSONL with carry, skip session header entries, and append fresh entries; lines 75-79 send chat; lines 82-170 render controls, progress stats, transcript, and chat form.
- inputs_outputs_state: Inputs are agent snapshot, progress payload, guest client, transcript fetch replies, chat text; outputs are UI state, client commands (`kill`, `revive`, `chat`), and transcript rendering.
- gates_or_invariants: Polling stops on cleanup; in-flight guard avoids overlapping transcript requests; read-only hides controls; empty transcript handled.
- dependencies_and_callers: Used by collab web agent panel; depends on guest client and transcript components.
- edge_cases_or_failure_modes: Partial JSONL carry, timeout/null replies, agent switch resets entries, stale in-flight response after close.
- validation_or_tests: No assigned direct collab-web test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3425 `file` `packages/collab-web/src/tool-render/tools/read.tsx`
- cursor: `[_]`
- core_role: Web renderer for read tool summaries/body.
- algorithmic_behavior: Lines 17-29 normalize untrusted `ReadToolDetails`; lines 31-44 split trailing path selectors like `:raw` or line ranges; lines 53-62 derive path/from/to/selector args; lines 64-102 render summary, resolved path, badges, images, and code text.
- inputs_outputs_state: Inputs are tool args/result/details; outputs are React summary/body nodes.
- gates_or_invariants: Details are narrowed defensively; selector parsing only strips recognized trailing chunks.
- dependencies_and_callers: Used by collab-web tool renderer registry.
- edge_cases_or_failure_modes: Windows drive colon ambiguity partly mitigated by selector regex; malformed details; conflict/truncation badges.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3455 `file` `packages/stats/src/client/app/routes.ts`
- cursor: `[_]`
- core_role: Static route metadata for stats dashboard sections.
- algorithmic_behavior: Lines 4-11 define route types; lines 13-50 list route ids, labels, and lucide icons.
- inputs_outputs_state: Input is none; output is static `routes` array.
- gates_or_invariants: Route ids constrained by `DashboardSection` union.
- dependencies_and_callers: Used by stats web client navigation.
- edge_cases_or_failure_modes: Missing icon/label or id mismatch.
- validation_or_tests: No direct test.
- skip_candidate: `yes: static UI metadata, not algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3485 `file` `packages/utils/src/vendor/mermaid-ascii/index.ts`
- cursor: `[_]`
- core_role: Public barrel for vendored Mermaid ASCII renderer.
- algorithmic_behavior: Lines 1-14 document vendored renderer and re-export `./ascii/index`.
- inputs_outputs_state: Module export surface only.
- gates_or_invariants: No runtime logic in this file.
- dependencies_and_callers: Consumers import Mermaid ASCII render APIs through this index.
- edge_cases_or_failure_modes: Broken export path.
- validation_or_tests: Renderer algorithms live under `ascii/`; this file has no tests.
- skip_candidate: `yes: barrel export wrapper, not algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3515 `file` `packages/coding-agent/src/eval/js/shared/helpers.ts`
- cursor: `[_]`
- core_role: Shared helper bundle for JavaScript eval sandbox file/env utilities.
- algorithmic_behavior: Lines 55-197 create helper functions for read/write/delete/sort/uniq/counts/diff/tree/env; lines 201-207 merge env; lines 212-256 resolve paths and internal URLs under configured roots; lines 259-280 validate files/data sizes/write data.
- inputs_outputs_state: Inputs are helper context roots/env/options and user-provided paths/data; outputs are file content, writes/deletes, path trees, env maps, or errors.
- gates_or_invariants: Internal URL roots prevent escaping; regular-file validation rejects directories/nonfiles; write data must be allowed type and under size limits.
- dependencies_and_callers: Used by JS eval executor/worker helpers.
- edge_cases_or_failure_modes: Path traversal, oversized data, non-regular files, unknown URL scheme, env override conflicts.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3545 `file` `packages/coding-agent/src/modes/components/status-line/component.ts`
- cursor: `[_]`
- core_role: Interactive status-line component building contextual/git/PR/model/usage/job segments.
- algorithmic_behavior: Lines 38-143 fingerprint messages for context cache; lines 235-264 wire settings/session focus; lines 301-347 compute status text/git watcher; lines 372-429 read branch/default/status cache; lines 433-490 fetch PR info; lines 494-595 compute token rate and usage limits; lines 610-727 build segment context; lines 768-925 render width-budgeted left/right groups, shrink path segment, drop overflow, and add session accent gap.
- inputs_outputs_state: Inputs are session state/messages/settings/git repo/status/usage, width, focus agent id; outputs are top border/status line content and visible width.
- gates_or_invariants: Segment inclusion is settings/preset gated; path is the only elastic segment before dropping; transparent mode drops powerline caps; focused agent dims bar safely.
- dependencies_and_callers: Used by interactive TUI footer/top border.
- edge_cases_or_failure_modes: Newlines sanitized by render helpers/tests, git unavailable, PR lookup failure, usage fetch failure, narrow width, stale context cache.
- validation_or_tests: Status-line newline guard and settings-list theme tests cover related rendering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3575 `file` `packages/coding-agent/src/web/search/providers/parallel.ts`
- cursor: `[_]`
- core_role: Parallel.ai search provider adapter with auth refresh and response normalization.
- algorithmic_behavior: Lines 38-76 parse API error payloads; lines 78-108 parse search payload into sources; lines 110-162 resolve auth key and call `withAuth` for retry/rotation; lines 164-203 clamp result count and map errors to `SearchProviderError`; lines 205-225 expose provider class.
- inputs_outputs_state: Inputs are query, result limit, auth storage/session id, fetch/signal; outputs are normalized `SearchResponse` with sources/requestId or provider error.
- gates_or_invariants: Requires Parallel credentials; result count clamped 1-40; hard timeout applied; only object results with URLs become sources.
- dependencies_and_callers: Used by web search provider registry.
- edge_cases_or_failure_modes: Missing key, nested error messages, non-JSON error body, invalid payload, 401/usage-limit retry classification.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3605 `file` `packages/utils/src/vendor/mermaid-ascii/xychart/parser.ts`
- cursor: `[_]`
- core_role: Parser for Mermaid `xychart-beta` syntax into typed XY chart structures.
- algorithmic_behavior: Lines 24-89 parse header/orientation, title, x/y category/range/title directives, and bar/line numeric series; lines 91-108 auto-derive y-axis range with padding or fallback; lines 113-115 parse numeric arrays.
- inputs_outputs_state: Inputs are preprocessed trimmed/comment-stripped lines; output is `XYChart` with axes, series, title, and orientation.
- gates_or_invariants: Unknown lines are ignored; y-axis always has a range by derive/fallback.
- dependencies_and_callers: Used by vendored Mermaid ASCII chart renderer.
- edge_cases_or_failure_modes: `parseFloat` can yield `NaN` for malformed numbers; categorical values are comma-trimmed without quote parsing.
- validation_or_tests: No assigned direct test.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 121 unique item sections; evidence headings cover the assigned checklist exactly once
- missing_items: []
- duplicate_items: []
- final_worker_status: `complete`

---

## Incremental Directory Refresh Addendum - oh-my-humanize/main bf4509d4f - OH_MY_HUMANIZE_MAIN-HZ-005

# agent_dir_02 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-005 `directory` `packages`
- cursor: `[_]`
- current_directory_core_role:
  - `packages/` is the monorepo package root. For this refresh, the effective core responsibility is concentrated in `packages/coding-agent/`, which owns the CLI-facing workflow command surface, workflow package loading/freezing, runtime host adapters, scheduler/runner lifecycle persistence, and workflow test contracts.
  - The relevant workflow stack is layered as: `src/cli/workflow-cli.ts` resolves and starts frozen workflow artifacts; `src/workflow/session-runtime.ts` adapts workflow nodes to eval/shell/agent/human runtimes; `src/workflow/runner.ts` materializes resources, executes nodes, persists run/lifecycle events, and finalizes attempts; `src/workflow/scheduler.ts` schedules activations, propagates stop/frontier state, and classifies activation statuses.
  - The directory still spans many packages (`ai`, `catalog`, `agent`, `tui`, `utils`, etc.), but the changed core descendants only alter `packages/coding-agent` workflow behavior.

- directory_level_delta_since_old_commit:
  - Headless workflow start now resolves a concrete workflow cwd once via `path.resolve(command.flags.cwd ?? getProjectDir())` and threads that cwd into the headless runtime host for eval scripts, shell scripts, and spawned agent tasks (`packages/coding-agent/src/cli/workflow-cli.ts`).
  - Headless JavaScript workflow scripts now execute with `process.chdir(cwd)` around the `AsyncFunction` invocation and restore both `console.log` and the previous process cwd in `finally`. This makes `Bun.file("relative-path")` and other cwd-relative reads use `omp workflow start --cwd`, while preserving structured top-level returns as captured output.
  - Headless `omp workflow start` now installs a start-signal controller for `SIGINT`/`SIGTERM`, passes the same signal as both scheduler stop signal and node abort signal, and always disposes listeners after `runWorkflow` completes.
  - Runner options now include `nodeAbortSignal`, `nodeAbortSignalForActivation`, and `maxRuntimeMs`. The runner derives a combined runtime timeout signal when `maxRuntimeMs` is present, forwards it to the scheduler, and clears the timer in `finally`.
  - Runner node execution is wrapped by `awaitWorkflowNodeExecution(...)`, which races node execution against the node abort signal. If the runtime ignores abort and never settles, the runner rejects on the next abort turn with the signal reason, persists the activation as aborted, and lets lifecycle checkpointing proceed instead of waiting forever.
  - Lifecycle finalization now treats scheduler limit, scheduler stop, signal abort, and deadline/max-runtime aborts as checkpointable stop states rather than failed attempts when there is no failed activation.
  - Changelog documents two user-visible fixes under `[Unreleased]`: ignored abort signals no longer keep workflow stop waiting forever, and headless `omp workflow start --cwd` now works for JavaScript workflow script nodes.
  - The demo script `examples/workflow-demos/human-interactive-dev/.../scripts/implementation.sh` now creates `artifacts/` before writing `artifacts/implementation.txt`, making the demo script compatible with fresh cwd/resource layouts.

- affected_descendant_algorithms:
  - `handleStart` in `workflow-cli.ts`: resolves the run cwd, restricts headless starts to frozen `.omhflow` artifacts, constructs an in-memory run store, creates a session workflow runtime host, binds runtime availability, installs signal handling, calls `runWorkflow`, reconstructs runs/families, and reports `completed`/`stopped`/`failed`.
  - `runHeadlessEvalScript` in `workflow-cli.ts`: executes only JS eval scripts in-process, captures `console.log`, captures top-level return values via formatting, temporarily changes cwd to the requested workflow cwd, restores cwd/logging in `finally`, and reports `{ exitCode, output, error, language }`.
  - `runHeadlessShellScript` in `workflow-cli.ts`: spawns `sh -c` with `cwd`, stdout/stderr pipes, request abort signal, and workflow script environment including resource context.
  - `runHeadlessAgentTask` and `buildHeadlessAgentTaskArgs` in `workflow-cli.ts`: spawn the current CLI invocation with `launch --cwd <cwd>`, optional `--model`, and assignment prompt, so subagent work inherits the workflow cwd.
  - `workflowRuntimeSignal` in `runner.ts`: creates an aborting timeout controller from `maxRuntimeMs`, combines it with scheduler and node abort signals, preserves abort reasons, and disposes timeout state.
  - `executeAndPersistActivation` in `runner.ts`: after prompt/script/model resolution, it chooses `context.nodeAbortSignal ?? context.signal` as the execution signal, passes that into node runtime execution, wraps the promise with abort racing, and records completed/failed/aborted run-store and lifecycle events.
  - `awaitWorkflowNodeExecution` in `runner.ts`: the new ignored-abort guard. It uses `Promise.withResolvers`, subscribes to abort, schedules a zero-delay rejection with the signal reason, settles exactly once, and removes the listener.
  - `finishLifecycleAttempt` / `workflowCheckpointReason` in `runner.ts`: failed activations still fail the attempt, but activation limits and aborted frontier-bearing runs request stop and create checkpoints with completed and aborted activation ids.
  - `runWorkflowScheduler` in `scheduler.ts`: consumes separate scheduler and node abort signals, passes node signals to execution contexts, marks abort-classified results as `aborted`, records the aborted activation’s node as frontier, stops downstream scheduling, and preserves eligible frontier nodes when a stop signal arrives after a completion.

- current_inputs_outputs_state:
  - Inputs:
    - CLI action/flags: `omp workflow start <flow-or-path>`, `--cwd`, `--run-id`, `--family-id`, `--start`, `--max-activations`, `--max-node-activations`, `--max-runtime-ms`, `--json`.
    - Workflow artifacts: frozen `.omhflow` file plus same-name resource directory; raw YAML package starts are rejected for headless start.
    - Runtime signals: process `SIGINT`/`SIGTERM`, optional injected test signal target, user stop signal, node abort signal, per-activation node abort function, and max-runtime timeout.
    - Node inputs: workflow definition, resolved prompt, frozen resources, model resolution audit, current state, completed activations, and resource directory.
  - Outputs:
    - CLI JSON/non-JSON run summary with flow metadata, run status, activation counts, frontier node ids, families, attempts, checkpoints, and run state keys.
    - Run-store custom entries: activation started/completed/failed/aborted, state patch events, run reconstruction state.
    - Lifecycle custom entries: family/freeze/attempt started, activation started/completed/failed/aborted, attempt stopped/completed/failed, checkpoint created.
    - Script outputs: JS eval output from `console.log` and top-level return formatting; shell output from stdout/stderr; structured workflow activation output is validated and may become state patches.
    - Demo shell output now includes an artifact file under `artifacts/implementation.txt` and emits a JSON state patch.

- new_or_changed_gates_or_invariants:
  - Headless workflow start gate: starts require frozen `.omhflow` artifacts; raw workflow authoring packages are rejected with a package error and no stack trace.
  - Cwd invariant: `--cwd` is the execution cwd for headless JS scripts, shell scripts, and spawned agent tasks. JS eval specifically must restore the previous process cwd after execution or failure.
  - Signal cleanup invariant: headless start signal listeners for `SIGINT` and `SIGTERM` are removed after the run completes.
  - Abort classification invariant: when the node abort signal or scheduler signal is aborted, node execution errors become activation status `aborted`, not `failed`.
  - Ignored-abort invariant: if a node runtime never resolves after the node abort signal fires, `awaitWorkflowNodeExecution` forces the activation to settle as aborted so lifecycle checkpointing can complete.
  - Deadline/max-runtime invariant: `maxRuntimeMs` aborts both scheduling and node execution with reason `workflow max runtime elapsed after <N>ms`; frozen lifecycle attempts are stopped and checkpointed rather than failed when no activation failed independently.
  - Frontier invariant: when cancellation happens after a completed activation, eligible downstream nodes are retained as checkpoint frontier; when an activation itself aborts, its own node is retained as frontier for restart.
  - Persistence invariant: checkpoint records include both `completedActivationIds` and `abortedActivationIds`; failed activations still create failed-attempt checkpoints through the failed path.

- dependencies_and_callers:
  - CLI callers enter through `runWorkflowCommand(...)` and `handleStart(...)` in `packages/coding-agent/src/cli/workflow-cli.ts`.
  - Artifact dependencies: `resolveWorkflowFlowSpec`, `loadWorkflowArtifact`, `freezeWorkflowArtifact`, and frozen resource snapshots feed package root/resource materialization.
  - Runtime host dependency: `createSessionWorkflowRuntimeHost(...)` converts workflow node execution into headless eval/shell/agent adapters. It forwards `input.signal` to agent/review requests and shell requests; eval requests do not carry a signal directly, so runner-level abort racing is the guard for async eval execution that does not cooperate.
  - Scheduler dependency: `runWorkflowScheduler(...)` receives `signal`, `nodeAbortSignal`, and `nodeAbortSignalForActivation` from `runWorkflow(...)`, then provides `context.signal` and `context.nodeAbortSignal` to the runner’s `executeNode` callback.
  - Lifecycle/run-store dependencies: `appendWorkflowActivationAborted`, `appendWorkflowAttemptActivationAborted`, `requestWorkflowAttemptStop`, `createWorkflowCheckpoint`, `reconstructWorkflowRuns`, and `reconstructWorkflowFamilies` are the persistence/readback surface for the new stop/checkpoint semantics.
  - Timeout dependency: `DEFAULT_WORKFLOW_MAX_RUNTIME_MS` is used by headless start when no explicit `--max-runtime-ms` is provided; `workflowMaxRuntimeStopReason` supplies the stable abort/checkpoint reason.
  - Tests call `runWorkflowCommand` directly with temporary artifacts and a fake signal target, and call `runWorkflow` directly with controlled runtime hosts and abort controllers.

- edge_cases_or_failure_modes:
  - JS eval cwd is process-global. The implementation restores cwd in `finally`, but concurrent in-process eval work would share process cwd during the execution window. Current headless CLI execution is effectively scoped to a run, but this remains a concurrency-sensitive design point.
  - JS eval cannot be forcibly preempted if it enters a synchronous infinite loop because it runs in the same JS thread; runner abort racing only settles once the event loop can process the abort callback. Async ignored-abort cases are covered.
  - `runHeadlessEvalScript` does not pass a request signal into the eval adapter. Node-level abort is enforced by the runner wrapper around `executeWorkflowNode`, not by cooperative eval code.
  - `combineAbortSignals` installs listeners without explicit removal after one signal wins. The combined signal objects are short-lived and timer disposal is handled, but long-lived external signals could retain one listener until they abort.
  - Headless shell/agent subprocesses receive `request.signal`; if subprocess output streams or child exit handling behave oddly on abort, scheduler classification still depends on the abort signal reason when the execution promise rejects.
  - If a workflow aborts before any frontier exists, checkpoint reason requires `scheduler.frontierNodeIds.length > 0`; empty-frontier aborted runs can complete without a checkpoint reason unless another limit/failure path applies.
  - Failed activations still dominate lifecycle finalization. If one activation fails while another aborts, the attempt is failed and the checkpoint includes aborted ids, but status is not stopped.
  - Headless start reports `failed` only from activation status `failed`; aborted lifecycle attempts report `stopped` through lifecycle attempt status or limit state.
  - The demo script now assumes the shell can create `artifacts/`; this removes missing-directory failure for fresh workspaces.

- validation_or_tests:
  - `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts` adds/contains a headless resource smoke: frozen shell script resources are passed via `OMP_WORKFLOW_RESOURCE_DIR`, the run completes, and state key `message` appears.
  - The same CLI test file pins JS cwd behavior: a JS workflow script reads `marker.txt` from the requested `--cwd`, returns a structured state patch, and the run completes with state key `marker`.
  - The same CLI test file pins SIGINT checkpoint behavior: a fake signal target emits `SIGINT` during a sleeping shell node, JSON output reports run status `stopped`, frontier `["hold"]`, stopped attempt, checkpoint frontier `["hold"]`, and zero remaining signal listeners.
  - Existing/nearby CLI tests also pin package errors: ambiguous flow/package errors are printed without source stack traces, and headless start rejects non-artifact workflow packages.
  - `packages/coding-agent/test/workflow/runner.test.ts` pins cancellation after completion: aborting the scheduler signal after `build` completes prevents `review`, stops the attempt, and checkpoints frontier `review`.
  - Runner tests pin separated scheduler vs node abort signals: node runtime receives the dedicated node abort signal while scheduler stop prevents downstream scheduling.
  - Runner tests pin deadline-aborted activations: a node abort after scheduler stop is persisted as activation `aborted`, the attempt is `stopped`, and checkpoint `abortedActivationIds` contains `activation-1`.
  - Runner tests pin ignored-abort handling: a runtime that returns a never-settling promise still causes `runWorkflow` to settle within the test race after node abort, with activation `aborted` and a stopped checkpoint.
  - Runner tests pin max runtime: `maxRuntimeMs: 1` aborts the node with reason `workflow max runtime elapsed after 1ms`, marks the activation aborted, stops the attempt, and checkpoints the aborted activation/frontier.
  - I inspected the current read-only source export and test contracts; I did not execute the test suite in this read-only research pass.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-005`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
