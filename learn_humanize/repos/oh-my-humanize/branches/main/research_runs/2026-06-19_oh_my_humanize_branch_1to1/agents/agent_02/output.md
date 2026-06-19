# agent_02 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-002 `directory` `crates`
- cursor: `[_]`
- core_role: Rust implementation layer for native shell execution, command-output minimization, AST/code analysis, isolation backends, and N-API bindings consumed by `packages/natives`.
- algorithmic_behavior: Recursive inspection showed crate families: `pi-shell` runs/fixes shell commands and minimizes stdout/stderr through detector, plan, pipeline, primitive, and filter modules; `pi-natives` exposes grep, glob, AST, task cancellation, terminal image/text helpers, shell, pty, sixel, workspace, and isolation bindings; `pi-iso` implements platform isolation strategies such as APFS, Btrfs, ZFS, overlayfs, reflink, ProjFS, and rcopy; `pi-ast` provides language parser/block/summary operations; vendored `brush-core` and `brush-builtins` supply shell semantics and builtins.
- inputs_outputs_state: Inputs are command invocations, filesystem trees, source files, terminal bytes, shell output, and platform capability probes. Outputs are minimized logs, process results, file matches, AST edits, isolation diffs, N-API values, and platform-specific status. State lives in process handles, cancellation tokens, filesystem caches, and temporary isolation mounts/workspaces.
- gates_or_invariants: `pi-shell` filters preserve failure-relevant lines and command identity; minimizer definitions under `crates/pi-shell/src/minimizer/defs/*.toml` gate tool-specific parsing; isolation backends must probe before start; `pi-natives/src/iso.rs:17` prefixes unavailable errors with `ISO_UNAVAILABLE:` for JS classification; N-API enum numeric/string shapes must match generated JS exports.
- dependencies_and_callers: Called by `packages/natives/native/index.js`, coding-agent tools, TUI terminal handling, shell execution, ast-grep wrappers, and Python orchestration cache logic. Rust depends on tree-sitter, shell/process crates, napi-rs, and platform syscalls.
- edge_cases_or_failure_modes: Unsupported platform isolation, partial command output, binary diffs, malformed terminal sequences, process cancellation races, large workspaces, missing tree-sitter language support, and native addon ABI/CPU-variant mismatch.
- validation_or_tests: `crates/pi-shell/tests` fixture tests validate minimization; Rust source carries module-level tests in filters and AST/native modules; `packages/natives/test` validates packaged loader and native functions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-032 `directory` `packages/natives`
- cursor: `[_]`
- core_role: JavaScript/TypeScript package boundary for loading and publishing the Rust `pi-natives` N-API addon.
- algorithmic_behavior: `native/index.js` performs a single `loadNative()` then re-exports generated classes/functions/enums (`isoStart`, `grep`, `astGrep`, `executeShell`, `PtySession`, etc.) from `packages/natives/native/index.js:16-128`. Build scripts choose CPU variant, run napi build, install generated bindings, and rewrite generated JS enum surfaces.
- inputs_outputs_state: Inputs include runtime platform/arch/variant, embedded addon metadata, generated `.node` files, and package scripts. Outputs are loaded native bindings, generated `index.d.ts`, generated enum constants, and benchmark/test results.
- gates_or_invariants: `build-native.ts:21-39` rejects invalid `TARGET_VARIANT` and requires explicit variant for x64 cross-builds; `build-native.ts:113-141` installs binaries atomically; loader state keeps pure helpers testable without eager AVX/filesystem probes.
- dependencies_and_callers: Depends on `crates/pi-natives`, napi-rs artifacts, Bun scripts, and host CPU detection. Consumed by `@oh-my-pi/pi-natives` imports across coding-agent, TUI, utils, and stats.
- edge_cases_or_failure_modes: Missing binary, stale temp files, Windows loaded DLL replacement, cross-build target directory mismatch, generated type/export drift, and embedded addon absence (`embeddedAddon = null` in source builds).
- validation_or_tests: Tests cover native loading, npm package metadata, Windows staging, issue regressions `issue-823` and `issue-892`, plus `bench/grep.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-062 `file` `docs/natives-rust-task-cancellation.md`
- cursor: `[_]`
- core_role: Architecture contract for native task cancellation and timeout behavior across Rust N-API work.
- algorithmic_behavior: Documents cooperative cancellation flow where TS/native callers pass abort state into Rust long-running operations; Rust checks a cancellation heartbeat inside loops and returns abort/timeout classifications rather than hanging the agent.
- inputs_outputs_state: Inputs are abort signals, timeout settings, native work units, and task handles. Outputs are completed native results or classified cancellation/timeout errors. State transitions are running -> cancellation requested -> heartbeat observes request -> aborted result.
- gates_or_invariants: Cancellation must be cooperative but bounded; blocking native work should not starve JS; cancellation errors must be distinguishable from hard failures; long loops need periodic heartbeats.
- dependencies_and_callers: Defines expectations for `crates/pi-natives/src/task.rs`, AST/grep/workspace native operations, and coding-agent tool wrappers that pass abort signals.
- edge_cases_or_failure_modes: Native worker ignores heartbeat, cancellation races with completion, timeout surfaces as generic error, or JS promise never settles.
- validation_or_tests: Related contracts are exercised by native/coding-agent tool tests that abort or time out native-backed operations.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-092 `file` `scripts/ci-test-ts.ts`
- cursor: `[_]`
- core_role: CI test router and partitioner for TypeScript package validation.
- algorithmic_behavior: Defines modes at `scripts/ci-test-ts.ts:6-14`, partitions coding-agent tests into singleton/ui/runtime/native buckets, chunks memory-heavy buckets (`:42-53`), classifies tests by path/content markers (`:81-171`), builds commands, scrubs sensitive env, and executes Bun test commands.
- inputs_outputs_state: Inputs are CLI args, repository test file list, test file contents, env vars, and mode. Outputs are dry-run command lists or executed test subprocesses. State is in computed partitions and per-command process exit status.
- gates_or_invariants: Invalid modes fail; singleton/global-state tests are not chunked; memory-heavy and native/browser suites are isolated; env prefixes like AWS/SCCACHE/GOOGLE are scrubbed (`:337-359`); command failure exits CI.
- dependencies_and_callers: Used by package scripts/CI; depends on Bun, `node:fs/promises`, package layout, and test naming/content conventions.
- edge_cases_or_failure_modes: Misclassification can hide global-state leakage, oversized chunks can OOM, marker drift can put native/browser tests in fast buckets, and dry-run must not execute.
- validation_or_tests: The script is itself CI infrastructure; validation is by successful CI runs and dry-run review of partition commands.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-122 `directory` `crates/pi-shell/tests`
- cursor: `[_]`
- core_role: Fixture-driven validation suite for the Rust shell output minimizer.
- algorithmic_behavior: `minimizer_fixtures.rs` walks `tests/fixtures/minimizer/**`, loads `.cmd`, `.raw`, optional `.exit`, and expected `.min` outputs, then compares minimizer output for git, glab, go, cargo, JVM, and npm cases.
- inputs_outputs_state: Inputs are command fixture text and raw command output; outputs are minimized summaries. Test state is fixture file discovery and expected-output comparison.
- gates_or_invariants: Fixture names bind command, raw output, optional exit code, and expected minified output; missing `.min` indicates output should match generated/default behavior or is covered by snapshot convention.
- dependencies_and_callers: Exercises `crates/pi-shell/src/minimizer` filters and definitions.
- edge_cases_or_failure_modes: Locale-specific Maven output, failing vs passing command exits, large CI traces, git status/log variations, and Gradle/Maven slice/full output differences.
- validation_or_tests: This directory is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-152 `directory` `packages/stats/test`
- cursor: `[_]`
- core_role: Test suite for stats ingestion, backfill, dashboard range filtering, cost accounting, premium request classification, and client view models.
- algorithmic_behavior: Tests named in scan include behavior backfill, client view models, DB cost, DB range, priority premium requests, and user metrics. They seed stats/session data, run parser/backfill/database selectors, and assert normalized dashboard outputs.
- inputs_outputs_state: Inputs are synthetic sessions, token/cost fields, timestamps, service tier metadata, and user messages. Outputs are dashboard stats, cost totals, time-range slices, behavior rows, and UI view-model values.
- gates_or_invariants: Cost correction must preserve provider/model semantics; time ranges must filter inclusively as expected; premium service-tier requests must be backfilled; user metric aggregation must ignore non-user/system noise.
- dependencies_and_callers: Exercises `packages/stats/src` DB and client code plus sync worker behavior.
- edge_cases_or_failure_modes: Missing usage data, historical schema drift, priority tier metadata absent in older rows, and timezone/range boundary errors.
- validation_or_tests: This directory is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-182 `file` `docs/tools/ast-grep.md`
- cursor: `[_]`
- core_role: Runtime contract documentation for the `ast_grep` coding-agent tool.
- algorithmic_behavior: Defines wrapper/native split, pattern handling, search path resolution, native tree-sitter matching, pagination, parse-error accumulation, and renderer behavior. The doc states wrapper default cap `DEFAULT_AST_LIMIT = 50`, native clamping, multi-target `skip + 50 + 1` paging, and parse error cap `PARSE_ERRORS_LIMIT = 20`.
- inputs_outputs_state: Inputs are `pat`, optional path/glob, skip, language inference, workspace files, and abort/timeout. Outputs are matches with anchors, parse errors, total counts, and no-match success.
- gates_or_invariants: Empty pattern and invalid skip are `ToolError`; unsupported external/internal URL forms fail; missing paths fail; parse failures are non-fatal and surfaced alongside matches; `node_modules` is skipped unless explicitly named.
- dependencies_and_callers: Documents `packages/coding-agent/src/tools/ast-grep.ts`, `crates/pi-natives/src/ast.rs`, and render utilities.
- edge_cases_or_failure_modes: Mixed-language trees compile patterns per language, syntax error nodes still searched, bad glob compilation, cancellation/timeout, and anchor mode differences.
- validation_or_tests: `packages/coding-agent/test/tools/ast-grep.test.ts`; native tests in `crates/pi-natives/src/ast.rs`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-212 `file` `scripts/install-tests/run-podman.sh`
- cursor: `[_]`
- core_role: Install smoke workflow for binary, source, and tarball packaging paths.
- algorithmic_behavior: Shell script changes to repo root, builds three Podman Dockerfiles in order, and fails fast via `set -e`. Commands are at `scripts/install-tests/run-podman.sh:4-15`.
- inputs_outputs_state: Inputs are Dockerfiles and repository context; outputs are Podman images/tags `omp-test-binary`, `omp-test-source`, and `omp-test-tarball`, or failing exit status.
- gates_or_invariants: Any failed image build aborts the script; success requires all three install surfaces to build.
- dependencies_and_callers: Depends on Podman and `scripts/install-tests/*.dockerfile`; called manually or by release/install validation.
- edge_cases_or_failure_modes: Missing Podman, Dockerfile drift, unavailable base images, native binary packaging mismatch.
- validation_or_tests: The script is an install smoke gate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-242 `directory` `packages/catalog/src/provider-models`
- cursor: `[_]`
- core_role: Provider model discovery/resolution layer for the catalog package.
- algorithmic_behavior: `descriptors.ts` defines `CATALOG_PROVIDERS` entries with defaults/env/discovery wiring (`:54+`); `openai-compat.ts` maps models.dev/OpenAI-compatible provider payloads into `ModelSpec`; `google.ts` builds Gemini/Vertex/Antigravity manager options; `ollama.ts` fetches Ollama Cloud tags/show metadata; `special.ts` handles special providers; `bundled-references.ts` merges dynamic discoveries with bundled metadata.
- inputs_outputs_state: Inputs are provider config, API keys, base URLs, dynamic HTTP responses, bundled model references, and static descriptors. Outputs are model manager options and sorted `ModelSpec` arrays.
- gates_or_invariants: Provider IDs/defaults must match registry; dynamic fetchers are optional when auth is absent; context/max token metadata is normalized; bundled references fill gaps but should not overrule trustworthy provider metadata.
- dependencies_and_callers: Used by model manager/cache/generator and pi-ai registry definitions; imports catalog identity/effort utilities and provider discovery helpers.
- edge_cases_or_failure_modes: Upstream payload schema drift, unauthenticated providers, stale bundled fallback, missing context windows, and provider-specific thinking/effort translation.
- validation_or_tests: Catalog tests include issue regressions such as `issue-830`; generator/regression tests assert resolver/descriptor behavior rather than generated JSON.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-272 `directory` `packages/coding-agent/src/memories`
- cursor: `[_]`
- core_role: Background memory extraction and consolidation pipeline for coding-agent.
- algorithmic_behavior: `storage.ts` creates WAL SQLite tables for `threads`, `stage1_outputs`, and `jobs` (`:47-89`); claim functions select idle recent CLI/app threads, lease jobs, track retries, and enqueue per-cwd global consolidation. `index.ts` starts the task only when enabled, top-level, and persistent (`:123-145`), injects summaries/lessons into prompts (`:153-185`), and runs phase 1/phase 2 using prompt templates.
- inputs_outputs_state: Inputs are session transcripts/rollout files, settings, model registry, cwd, timestamps, and prior DB rows. Outputs are raw memories, rollout summaries/slugs, `memory_summary.md`, learned lessons, and generated skill artifacts. State transitions are pending -> running with ownership token/lease -> succeeded/failed/retry -> global consolidation.
- gates_or_invariants: Disabled by default; skips subagents/ephemeral sessions; `busy_timeout` must be installed before locks (`storage.ts:49-50`); global job key is per-cwd to avoid cross-project contamination (`storage.ts:39-45`); prompt injection shares a token budget and clamps negative remainder (`index.ts:171-179`).
- dependencies_and_callers: Called by `AgentSession` startup and memory commands; depends on Bun SQLite, memory prompt `.md` templates, `completeSimple`, model resolver, and pi-utils paths.
- edge_cases_or_failure_modes: DB unavailable, stale leases, retry exhaustion, oversized rollout payload, no output from model, missing summary, and cross-project contamination.
- validation_or_tests: `packages/coding-agent/test/memories/instructions.test.ts` and related memory/hindsight tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-302 `directory` `packages/coding-agent/test/goals`
- cursor: `[_]`
- core_role: Goal-mode validation suite for coding-agent goal runtime, guided goals, and goal tools.
- algorithmic_behavior: Tests exercise goal runtime activation, goal tool behavior, guided goal flows, and integration boundaries. `goal-runtime.test.ts` includes a `describe("goal runtime")` section around runtime state transitions.
- inputs_outputs_state: Inputs are synthetic goal definitions, session/tool contexts, user/agent events, and runtime state. Outputs are goal status changes, tool results, persisted run records, or prompts.
- gates_or_invariants: Goal execution should preserve dependency/state ordering, expose concrete tool outputs, and avoid invalid transitions.
- dependencies_and_callers: Exercises coding-agent goal runtime modules and session/tool infrastructure.
- edge_cases_or_failure_modes: Missing goal data, invalid runtime state, repeated activation, tool failure, and integration with session persistence.
- validation_or_tests: This directory is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-332 `directory` `packages/utils/test/mermaid`
- cursor: `[_]`
- core_role: Golden and regression tests for Mermaid-to-ASCII/Unicode diagram rendering.
- algorithmic_behavior: Tests cover class arrows, edge styles, formatting, golden fixtures, multiline labels, xychart, and large testdata sets for flowchart/class/ER/sequence/subgraph diagrams in ASCII and Unicode.
- inputs_outputs_state: Inputs are Mermaid source diagrams and expected rendered text files. Outputs are rendered ASCII/Unicode diagrams compared to fixtures.
- gates_or_invariants: Rendering must preserve graph order, labels, arrows, subgraph nesting/directions, duplicate labels, backlinks, self references, and Unicode/ASCII style differences.
- dependencies_and_callers: Exercises `packages/utils/src/vendor/mermaid-ascii/**`, including sequence parser item HZ-3602.
- edge_cases_or_failure_modes: Ampersands, nested subgraphs, empty subgraphs, fan-in/fan-out, multiline labels, and sequence self-messages.
- validation_or_tests: This directory is the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-362 `file` `crates/pi-natives/src/iso.rs`
- cursor: `[_]`
- core_role: N-API shim over `pi_iso::IsolationBackend`.
- algorithmic_behavior: Exposes `iso_backend`, `iso_probe`, `iso_resolve`, `iso_start`, `iso_stop`, `iso_diff`, and `iso_is_unavailable_error`. Backend enum mapping is numeric (`:31-40`), lifecycle calls run sync backend work in `tokio::task::spawn_blocking` (`:132-150`), and `iso_diff` uses the always-available Rcopy backend because diff behavior is uniform (`:160-170`).
- inputs_outputs_state: Inputs are optional backend kind, lower/merged paths, and preferred backend hints. Outputs are probe/resolve structs, lifecycle promise completion, or `IsoDiff` file changes with optional unified diffs.
- gates_or_invariants: Omitted backend defaults to native; unavailable errors are prefixed with `ISO_UNAVAILABLE:` (`:216-220`); binary file diffs return `None`; enum conversion must stay exhaustive.
- dependencies_and_callers: Depends on `pi_iso`, napi-rs, Tokio; called through `packages/natives/native/index.js` exports `isoStart/isoStop/isoDiff`.
- edge_cases_or_failure_modes: Backend unavailable, join errors from blocking task, binary changes, invalid paths, platform-specific mount teardown failure.
- validation_or_tests: Native package tests and Rust compile-time object-safety assertion (`:237-243`).
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-392 `file` `packages/agent/src/run-collector.ts`
- cursor: `[_]`
- core_role: Per-agent-loop telemetry aggregator for chats, tools, usage, cost, errors, and coverage.
- algorithmic_behavior: `AgentRunCollector` stores chat/tool records, uses span-attached symbols for starts (`:142-147`), records available/invoked tools, computes stable sorted summaries (`:315-431`), and aggregates multiple run summaries/coverage values (`:445-567`).
- inputs_outputs_state: Inputs are telemetry span begin/end/fail events, assistant messages, tool statuses, cost fields, and step count. Outputs are immutable `AgentRunSummary` and `AgentRunCoverage`. State transitions are beginChat/beginTool -> end/fail/orphan -> snapshot -> optional aggregate.
- gates_or_invariants: Telemetry methods should not throw; missing begin span produces latency 0; input tokens include cache read/write (`:206-215`); `markRunEnded` is idempotent (`:168-172`); arrays/records sorted for stable persistence.
- dependencies_and_callers: Fed by `packages/agent/src/telemetry.ts`; consumed by agent end events, dashboards, tests, and run hooks.
- edge_cases_or_failure_modes: Provider crash before end span, orphan tools after interrupt, cost unavailable, unknown stop reason, empty aggregate returns frozen constants.
- validation_or_tests: Agent telemetry/run collector tests and downstream stats tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-422 `file` `packages/ai/src/errors.ts`
- cursor: `[_]`
- core_role: Structured provider HTTP error type used for retry/rate-limit/error classification.
- algorithmic_behavior: Defines `ProviderHttpErrorOptions` and `ProviderHttpError`; constructor preserves `status`, `headers`, and machine-readable `code` fields while naming the error (`packages/ai/src/errors.ts:20-31`).
- inputs_outputs_state: Inputs are message, HTTP status, optional headers/code/cause. Output is an Error instance with structural fields.
- gates_or_invariants: Downstream classification reads fields structurally rather than `instanceof`; headers must remain accessible for `retry-after`; code remains optional.
- dependencies_and_callers: Used by provider clients and pi-utils HTTP status/header extraction.
- edge_cases_or_failure_modes: Missing headers/code, non-HTTP provider errors, cause propagation support.
- validation_or_tests: Provider tests that classify transient/rate-limit/provider failures.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-452 `file` `packages/ai/test/anthropic-unsigned-thinking-replay.test.ts`
- cursor: `[_]`
- core_role: Regression test for Anthropic-compatible unsigned thinking replay behavior.
- algorithmic_behavior: Helpers build Anthropic models/messages and inspect `convertMessages` wire blocks; test suite starts at line 87 and validates that thinking blocks without signatures are not replayed unsafely.
- inputs_outputs_state: Inputs are synthetic user/assistant thinking/tool messages. Outputs are Anthropic wire block arrays.
- gates_or_invariants: Signed thinking may be replayed when safe; unsigned reasoning content must not be sent back in a form Anthropic rejects or misinterprets.
- dependencies_and_callers: Exercises Anthropic message conversion in `packages/ai`.
- edge_cases_or_failure_modes: Assistant thinking followed by text/tool blocks, missing signatures, and mixed content arrays.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-482 `file` `packages/ai/test/auth-storage-oauth-refresh-race.test.ts`
- cursor: `[_]`
- core_role: Regression test for OAuth token refresh race handling in auth storage.
- algorithmic_behavior: `describe("AuthStorage OAuth refresh race")` creates concurrent refresh/read situations and asserts single-flight or rotation-safe credential persistence.
- inputs_outputs_state: Inputs are expired OAuth credentials, refresh callbacks, and concurrent access. Outputs are refreshed credentials and storage state.
- gates_or_invariants: Only one refresh should win; callers must not see stale/partially rotated credentials; failed refresh should not corrupt stored token.
- dependencies_and_callers: Exercises `AuthStorage` OAuth refresh logic used by providers.
- edge_cases_or_failure_modes: Concurrent refresh, refresh-token rotation, stale access token, and failed network response.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-512 `file` `packages/ai/test/github-copilot-reasoning.test.ts`
- cursor: `[_]`
- core_role: Test for GitHub Copilot reasoning request construction.
- algorithmic_behavior: `describe("GitHub Copilot reasoning request construction")` validates that reasoning/effort settings are serialized into Copilot-compatible request payloads and headers.
- inputs_outputs_state: Inputs are Copilot model config, messages, and reasoning settings. Outputs are fetch request body/headers.
- gates_or_invariants: Reasoning effort should reach the wire only for capable models; auth/base URL headers must remain Copilot-compatible.
- dependencies_and_callers: Exercises GitHub Copilot provider request builder.
- edge_cases_or_failure_modes: Unsupported model reasoning, missing token, or wrong effort field.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-542 `file` `packages/ai/test/issue-2424-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for GitLab Duo OAuth environment override handling.
- algorithmic_behavior: `describe("gitlab-duo OAuth env overrides (issue #2424)")` uses token response helpers and bundled client IDs to verify env-provided OAuth settings override defaults correctly.
- inputs_outputs_state: Inputs are env vars, OAuth token response, provider registration. Outputs are OAuth config/request behavior.
- gates_or_invariants: Explicit env overrides must take precedence; bundled defaults must still work when no override is present.
- dependencies_and_callers: Exercises GitLab Duo OAuth/provider registry.
- edge_cases_or_failure_modes: Wrong client ID, stale env, or fallback overriding user config.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-572 `file` `packages/ai/test/ollama-reasoning-effort-backfill.test.ts`
- cursor: `[_]`
- core_role: Regression test ensuring Ollama reasoning effort backfills onto OpenAI Responses wire format.
- algorithmic_behavior: Suite `ollama reasoning effort backfill reaches the Responses wire` constructs context/model/signal and asserts request params contain expected reasoning effort.
- inputs_outputs_state: Inputs are Ollama model with reasoning config and stream/request options. Outputs are serialized Responses API payload.
- gates_or_invariants: Effort must be inferred/backfilled when catalog thinking metadata requires it; aborted signals should not mask request construction.
- dependencies_and_callers: Exercises Ollama provider compatibility layer.
- edge_cases_or_failure_modes: Missing thinking metadata, unsupported effort map, and signal abort.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-602 `file` `packages/ai/test/openai-responses-tool-quarantine.test.ts`
- cursor: `[_]`
- core_role: Regression tests for strict-tool schema quarantine in OpenAI Responses conversion.
- algorithmic_behavior: Tests `findStrictToolSchemaViolation`, `convertTools`, and `buildParams tool_choice reconciliation` beginning around lines 23, 75, and 95; bad tool schemas are quarantined while good schemas survive.
- inputs_outputs_state: Inputs are tool definitions with JSON schemas and tool_choice settings. Outputs are converted tools, warnings/quarantine decisions, and request params.
- gates_or_invariants: Strict schema violations must be detected; invalid tools removed from wire payload; tool choice reconciled so it does not reference quarantined tools.
- dependencies_and_callers: Exercises OpenAI Responses provider conversion.
- edge_cases_or_failure_modes: Required/additionalProperties mismatches, mixed good/bad tool sets, explicit tool_choice pointing at bad tool.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-632 `file` `packages/ai/test/stream-markup-healing.test.ts`
- cursor: `[_]`
- core_role: Extensive regression suite for streamed markup/thinking healing across providers.
- algorithmic_behavior: Defines SSE/NDJSON mock helpers (`:34-49`, `:120-135`) and suites for DSML envelope selection, thinking patterns, Kimi leaks, Ollama DSML, MiniMax thinking, and OpenAI-compatible DSML. It feeds provider streams and asserts healed text/thinking/tool-call boundaries.
- inputs_outputs_state: Inputs are synthetic SSE chunks, NDJSON lines, models, tools, and leaked markup strings. Outputs are assistant message events/content after healing.
- gates_or_invariants: Healing must target provider/model-specific leak patterns without corrupting normal tool calls or visible text; no-match streams should pass through.
- dependencies_and_callers: Exercises stream parsers/healing in `packages/ai` providers.
- edge_cases_or_failure_modes: Split tags across chunks, leaked envelopes around tool calls, provider-specific markup variants, `[DONE]` termination, and malformed stream chunks.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-662 `file` `packages/catalog/src/model-cache.ts`
- cursor: `[_]`
- core_role: SQLite-backed dynamic model cache for catalog/model manager.
- algorithmic_behavior: `getDb` opens a shared DB, sets busy timeout/WAL, creates/migrates `model_cache` (`:49-85`); `readModelCache` loads versioned rows and TTL freshness (`:87-112`); `writeModelCache` stores sparse model specs with static fingerprint (`:114-139`).
- inputs_outputs_state: Inputs are provider ID, TTL, current time, models, authoritative flag, fingerprint, and DB path. Outputs are cache entries or null; state is persisted SQLite row per provider.
- gates_or_invariants: Schema version 7 invalidates stale policy shapes (`:9-17`); cache failures are best-effort and return null/no throw; age must be finite and nonnegative to be fresh.
- dependencies_and_callers: Used by model manager resolution; depends on Bun SQLite and `getModelDbPath`.
- edge_cases_or_failure_modes: Corrupt JSON, DB lock, stale schema, clock skew, static fingerprint mismatch.
- validation_or_tests: Catalog/model-cache tests and provider discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-692 `file` `packages/catalog/test/issue-830-repro.test.ts`
- cursor: `[_]`
- core_role: Catalog regression test for issue #830.
- algorithmic_behavior: Exercises a previously failing model resolution/catalog behavior and asserts the resolver/descriptor output instead of generated `models.json`.
- inputs_outputs_state: Inputs are provider/model IDs and resolver inputs. Outputs are resolved model metadata.
- gates_or_invariants: Regression target must remain stable even when upstream generated JSON shifts.
- dependencies_and_callers: Exercises catalog provider-model resolver/descriptor code.
- edge_cases_or_failure_modes: Provider alias mismatch, model identity parsing drift, generated metadata movement.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-722 `file` `packages/coding-agent/scripts/generate-docs-index.ts`
- cursor: `[_]`
- core_role: Documentation index generator for coding-agent docs.
- algorithmic_behavior: Reads docs tree/package metadata, derives entries, and writes a generated index for navigability/discovery.
- inputs_outputs_state: Inputs are docs files/directories and script config; output is docs index content.
- gates_or_invariants: Should ignore generated/irrelevant files, keep stable ordering, and fail on unreadable docs.
- dependencies_and_callers: Called by package scripts or docs maintenance; depends on Bun/node filesystem APIs.
- edge_cases_or_failure_modes: Missing docs directory, duplicate titles, stale generated index.
- validation_or_tests: Usually validated by generated diff and package checks.
- skip_candidate: `yes: docs-index generation is workflow/support logic rather than core runtime algorithm, but it is assigned as package script behavior`

### OH_MY_HUMANIZE_MAIN-HZ-752 `file` `packages/coding-agent/test/agent-session-advisor-suppression.test.ts`
- cursor: `[_]`
- core_role: Regression tests for suppressing/parking advisor messages in agent sessions.
- algorithmic_behavior: Defines advisor message type/harness and validates session behavior when advisor content should not leak into visible transcript or model context.
- inputs_outputs_state: Inputs are session entries with advisor type and parking state. Outputs are filtered transcript/model messages and persisted custom message behavior.
- gates_or_invariants: Advisor messages should be suppressed where intended but preserved where required for session integrity.
- dependencies_and_callers: Exercises `AgentSession`, session manager, and custom message handling.
- edge_cases_or_failure_modes: Parked advisor resurfacing, incorrect filtering, persistence mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-782 `file` `packages/coding-agent/test/agent-session-silent-abort.test.ts`
- cursor: `[_]`
- core_role: Regression tests for silent-abort marker stamping in `AgentSession`.
- algorithmic_behavior: Suite starts around line 90 and asserts aborted model/tool turns are stamped so later replay/state handling can distinguish silent aborts from normal failures.
- inputs_outputs_state: Inputs are simulated abort signals/session events. Outputs are session entries/markers.
- gates_or_invariants: Abort markers must be written exactly when a silent abort occurs; no false positives for normal completion.
- dependencies_and_callers: Exercises `AgentSession` invoke/abort handling.
- edge_cases_or_failure_modes: Abort before result, abort during tool call, duplicate markers.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-812 `file` `packages/coding-agent/test/bash-execution-sixel.test.ts`
- cursor: `[_]`
- core_role: Tests for Bash execution renderer SIXEL sanitization and streaming throttle.
- algorithmic_behavior: Suites validate `BashExecutionComponent` strips or handles SIXEL image/control sequences and throttles streaming preview updates.
- inputs_outputs_state: Inputs are command output chunks with SIXEL/control bytes and timing. Outputs are sanitized TUI render lines and throttled updates.
- gates_or_invariants: Binary image/control data must not corrupt terminal rendering; streaming throttle should reduce excessive rerenders without losing final output.
- dependencies_and_callers: Exercises bash tool renderer/TUI component.
- edge_cases_or_failure_modes: Partial SIXEL sequences, huge output, rapid streaming chunks.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-842 `file` `packages/coding-agent/test/dap-write-sink-flush.typecheck.ts`
- cursor: `[_]`
- core_role: Compile-time contract test for DAP write-sink flush typing.
- algorithmic_behavior: Type-only file imports DAP client types and verifies the sink/flush surface remains type-compatible.
- inputs_outputs_state: Input is TypeScript type checker; output is pass/fail typecheck.
- gates_or_invariants: DAP client/write sink type must expose required flush behavior.
- dependencies_and_callers: Exercises debug adapter protocol type contracts.
- edge_cases_or_failure_modes: Type signature regression not visible at runtime.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-872 `file` `packages/coding-agent/test/hindsight-content.test.ts`
- cursor: `[_]`
- core_role: Tests for hindsight/memory content preparation utilities.
- algorithmic_behavior: Suites cover `stripMemoryTags`, `composeRecallQuery`, `truncateRecallQuery`, `sliceLastTurnsByUserBoundary`, `prepareRetentionTranscript`, `formatMemories`, and `formatCurrentTime`.
- inputs_outputs_state: Inputs are transcript entries, memory tags, recall query text, memory lists, and time values. Outputs are sanitized/truncated recall prompts and formatted memory blocks.
- gates_or_invariants: Memory tags should be stripped; truncation must respect query budget; transcript slicing should align on user boundaries; formatting stable enough for prompts.
- dependencies_and_callers: Exercises hindsight/memory prompt preparation code.
- edge_cases_or_failure_modes: Nested tags, oversized transcript, missing user turns, empty memories.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-902 `file` `packages/coding-agent/test/interactive-mode-model-cycle.test.ts`
- cursor: `[_]`
- core_role: Tests interactive mode model-cycle tracking.
- algorithmic_behavior: Suite `InteractiveMode model-cycle track` asserts model cycling state/order and active model updates in interactive mode.
- inputs_outputs_state: Inputs are model list, settings/session state, and cycle commands. Outputs are selected model and UI/state updates.
- gates_or_invariants: Cycling must wrap predictably and preserve current model pattern.
- dependencies_and_callers: Exercises interactive mode controller/model selector logic.
- edge_cases_or_failure_modes: Empty model list, unavailable models, repeated cycle commands.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-932 `file` `packages/coding-agent/test/issue-966-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for split commit restaging.
- algorithmic_behavior: Creates temp repo state and asserts split-commit logic restages files correctly after partial staging.
- inputs_outputs_state: Inputs are staged/unstaged file changes in a temp git repo. Outputs are staged index state and commit grouping behavior.
- gates_or_invariants: Restaging must not drop user changes or stage unrelated files.
- dependencies_and_callers: Exercises coding-agent commit/split logic.
- edge_cases_or_failure_modes: Partially staged hunks, restage ordering, temp git setup failure.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-962 `file` `packages/coding-agent/test/mcp-manager-subscription-action.test.ts`
- cursor: `[_]`
- core_role: Tiny regression test for MCP subscription post-action resolution.
- algorithmic_behavior: Suite `resolveSubscriptionPostAction` asserts mapping from MCP subscription state/action inputs to a concrete post-action.
- inputs_outputs_state: Inputs are subscription action values; output is resolved post-action enum/value.
- gates_or_invariants: Unknown/unsupported action should map safely; known actions should not regress.
- dependencies_and_callers: Exercises MCP manager subscription handling.
- edge_cases_or_failure_modes: Undefined action, invalid action, stale enum values.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-992 `file` `packages/coding-agent/test/oauth-flow.test.ts`
- cursor: `[_]`
- core_role: Tests MCP OAuth flow behavior.
- algorithmic_behavior: Suite `mcp oauth flow` drives callback/paste/auth handling and verifies credentials/session state.
- inputs_outputs_state: Inputs are OAuth provider callbacks, auth URLs, codes/tokens, and abort/cancel states. Outputs are stored credentials or surfaced errors.
- gates_or_invariants: Callback server/paste code flow must resolve once; cancellation must stop cleanly; tokens must be persisted under correct provider.
- dependencies_and_callers: Exercises coding-agent MCP OAuth integration and pi-ai auth storage.
- edge_cases_or_failure_modes: Port conflict, bad code, cancelled login, refresh mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1022 `file` `packages/coding-agent/test/rpc-example.ts`
- cursor: `[_]`
- core_role: Example RPC client/test harness entrypoint.
- algorithmic_behavior: `main()` drives an RPC example against coding-agent RPC surfaces, likely used manually or by smoke tests to demonstrate request/response framing.
- inputs_outputs_state: Inputs are RPC connection parameters and example request payloads. Outputs are printed or returned RPC responses.
- gates_or_invariants: RPC framing must serialize/deserialize messages and close cleanly.
- dependencies_and_callers: Depends on coding-agent RPC mode/client APIs.
- edge_cases_or_failure_modes: Missing server, connection failure, bad frame.
- validation_or_tests: Example itself is an executable smoke surface.
- skip_candidate: `yes: example harness rather than core algorithm, but it validates RPC behavior`

### OH_MY_HUMANIZE_MAIN-HZ-1052 `file` `packages/coding-agent/test/session-manager-internal-details.test.ts`
- cursor: `[_]`
- core_role: Tests session manager custom message persistence and allowlist stripping.
- algorithmic_behavior: Defines `SKILL_TYPE` and `readPersistedCustomMessageEntry`; suite asserts `appendCustomMessageEntry` strips internal fields while persisting allowed custom data.
- inputs_outputs_state: Inputs are custom session message entries. Outputs are in-memory and persisted JSONL/session entries.
- gates_or_invariants: Only allowlisted fields persist; custom message type/data round trip; internal details do not leak.
- dependencies_and_callers: Exercises `SessionManager` persistence.
- edge_cases_or_failure_modes: Disallowed fields retained, persisted entry missing custom data, JSONL parse mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1082 `file` `packages/coding-agent/test/status-text-sanitization.test.ts`
- cursor: `[_]`
- core_role: Test for status text sanitization.
- algorithmic_behavior: Suite `sanitizeStatusText` asserts status strings are cleaned before display.
- inputs_outputs_state: Inputs are raw status strings with control chars/newlines/odd whitespace. Outputs are sanitized one-line/status-safe text.
- gates_or_invariants: TUI status must not contain terminal-breaking characters or unbounded content.
- dependencies_and_callers: Exercises coding-agent status text utility.
- edge_cases_or_failure_modes: Empty string, control bytes, long status, tabs/newlines.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1112 `file` `packages/coding-agent/test/tools.test.ts`
- cursor: `[_]`
- core_role: Large contract test suite for coding-agent tools.
- algorithmic_behavior: `describe("Coding Agent Tools")` starts around line 260 and covers file read/write/edit, bash, search, tool session context, render behavior, CRLF edit handling (`:2087`), and many tool edge cases.
- inputs_outputs_state: Inputs are temp workspaces, tool schemas/args, session contexts, file contents, command outputs. Outputs are tool results, filesystem changes, rendered previews, and errors.
- gates_or_invariants: Tools must validate args, stay inside workspace/security rules, preserve user data, sanitize render output, and map errors consistently.
- dependencies_and_callers: Exercises main coding-agent tool registry and implementations.
- edge_cases_or_failure_modes: CRLF edits, missing files, binary/large output, invalid paths, partial contexts, shell failures.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1142 `file` `packages/hashline/bench/recovery-session-chain.ts`
- cursor: `[_]`
- core_role: Benchmark/recovery harness for hashline session chain behavior.
- algorithmic_behavior: Builds or replays session-chain data to measure recovery/lookup performance and correctness under chained entries.
- inputs_outputs_state: Inputs are synthetic or fixture session records and benchmark parameters. Outputs are timing/benchmark reports and recovered chain data.
- gates_or_invariants: Recovery must preserve chain order and hashes while remaining performant for large sessions.
- dependencies_and_callers: Depends on hashline package internals.
- edge_cases_or_failure_modes: Broken chain, missing node, large transcript, hash collision assumptions.
- validation_or_tests: Benchmark is not a unit test but exercises algorithmic recovery path.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1172 `file` `packages/mnemopi/src/config.ts`
- cursor: `[_]`
- core_role: Configuration/env resolution layer for mnemopi memory subsystem.
- algorithmic_behavior: Exports defaults for data/model/cache paths and models, plus env parsers (`envBool`, `envInt`, `envFloat`, `envOneOf`, etc.) and config construction values.
- inputs_outputs_state: Inputs are environment variables and defaults; outputs are typed config values for DB, embeddings, LLM, host, and feature toggles.
- gates_or_invariants: Invalid env values should fall back or throw according to helper semantics; paths default under user home; host LLM type is constrained.
- dependencies_and_callers: Used by mnemopi core, embedding, recall, and CLI/tests.
- edge_cases_or_failure_modes: Empty env strings, invalid numbers, unsupported enum, missing home directory.
- validation_or_tests: Mnemopi tests exercise embedding model reconcile and recall behavior with config defaults.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1202 `file` `packages/mnemopi/test/embedding-model-reconcile.test.ts`
- cursor: `[_]`
- core_role: Tests embedding-model migration/reconciliation.
- algorithmic_behavior: Seeds DB with old/new embedding model identifiers, uses a fake embedder, and asserts embeddings are recalculated/removed/kept appropriately.
- inputs_outputs_state: Inputs are seeded memory DB rows and target embedding model. Outputs are embedding row counts and reconciled records.
- gates_or_invariants: Changing embedding model must not mix incompatible vectors; reconciliation should be deterministic.
- dependencies_and_callers: Exercises `Mnemopi` embedding storage/reconcile logic.
- edge_cases_or_failure_modes: Old model rows left behind, duplicate embeddings, fake embedder mismatch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1232 `file` `packages/mnemopi/test/recall-precision-regressions.test.ts`
- cursor: `[_]`
- core_role: Recall precision regression tests for mnemopi memory retrieval.
- algorithmic_behavior: Builds `BeamMemory` fixtures, seeds precision cases, and asserts top recall results contain expected content for queries.
- inputs_outputs_state: Inputs are memory beams and query strings. Outputs are ranked recall results.
- gates_or_invariants: Relevant memory should rank above distractors for regression queries.
- dependencies_and_callers: Exercises mnemopi recall/ranking core.
- edge_cases_or_failure_modes: Similar distractors, embedding/rank drift, empty results.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1262 `file` `packages/snapcompact/research/bdf.py`
- cursor: `[_]`
- core_role: Research script for BDF bitmap font parsing/rendering in snapcompact experiments.
- algorithmic_behavior: Parses BDF glyph definitions, maps characters to bitmaps, and supports rendering compact text/image representations for research.
- inputs_outputs_state: Inputs are BDF font files and text. Outputs are glyph metrics/bitmaps or rendered image data.
- gates_or_invariants: Glyph encoding/bounds must match BDF metrics; missing glyphs need fallback.
- dependencies_and_callers: Research dependency for snapcompact filmstrip/visual compression experiments.
- edge_cases_or_failure_modes: Missing glyph, malformed BDF, unsupported encoding, variable metrics.
- validation_or_tests: Research script; validated by generated experiment outputs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1292 `file` `packages/snapcompact/research/exp20_8x8u.py`
- cursor: `[_]`
- core_role: Research experiment for 8x8 text/image compression and VLM QA evaluation.
- algorithmic_behavior: Functions include text wrapping, page layout, page packing, char style rendering, image rendering, atomic PNG save, answer parsing, QA unit execution, aggregation, and `main()`. It renders documents to compact images and asks models questions about them.
- inputs_outputs_state: Inputs are paragraphs/questions/model IDs/cache, image settings, and price values. Outputs are PNGs, parsed answers, QA records, and aggregate cost/accuracy metrics.
- gates_or_invariants: Cache keys must be stable; page layout must respect column/line limits; answer parser must produce expected count; atomic save prevents partial images.
- dependencies_and_callers: Uses Pillow/model APIs in research environment; related to snapcompact rendering.
- edge_cases_or_failure_modes: Overlong words, model response parse failure, stale cache, image save race.
- validation_or_tests: Research output metrics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1322 `file` `packages/snapcompact/research/snapcompact_r2_filmstrip.py`
- cursor: `[_]`
- core_role: Research script for filmstrip-style snapcompact rendering/evaluation.
- algorithmic_behavior: Builds multi-frame compact visual representations of text/content and evaluates retrieval/reading quality across rendered frames.
- inputs_outputs_state: Inputs are source text/pages, font/render settings, and experiment config. Outputs are filmstrip images and metrics.
- gates_or_invariants: Frame packing/order must preserve reading sequence; image generation must be deterministic for comparable metrics.
- dependencies_and_callers: Research-only snapcompact experimentation.
- edge_cases_or_failure_modes: Frame overflow, unreadable glyph size, model inability to parse visual text.
- validation_or_tests: Research experiment outputs.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1352 `file` `packages/stats/src/sync-worker.ts`
- cursor: `[_]`
- core_role: Stats sync worker entry for parsing session files off the main process.
- algorithmic_behavior: Defines request/response types for `{kind:"parse", sessionFile, fromOffset}` and ping; worker receives parse requests, processes session data from offset, and responds with parse results/errors or pong.
- inputs_outputs_state: Inputs are IPC requests with session file path/offset. Outputs are parsed stats response, error response, or ping response.
- gates_or_invariants: Ping must not require file parsing; parse should honor `fromOffset`; errors should be serialized instead of crashing parent.
- dependencies_and_callers: Spawned by stats sync client/worker host dispatch.
- edge_cases_or_failure_modes: Missing/truncated session file, invalid JSONL, worker crash, stale offset.
- validation_or_tests: Stats sync/backfill tests and smoke worker contract.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1382 `file` `packages/tui/src/stdin-buffer.ts`
- cursor: `[_]`
- core_role: Terminal stdin sequence buffer/parser for TUI input.
- algorithmic_behavior: Parses complete escape sequences, holds partial CSI/OSC/DCS/APC/SGR mouse sequences, handles bracketed paste, deduplicates Kitty printable double reports, and emits `data` or `paste` events. Hot path uses index scanning to avoid O(n²) (`:224-291`); paste uses chunk list plus overlap (`:435-469`).
- inputs_outputs_state: Inputs are string/Buffer stdin chunks. Outputs are complete input sequences and paste payloads. State includes buffer, timers, paste chunks/overlap/byte count, and pending Kitty codepoint.
- gates_or_invariants: Partial escape sequences flush after bounded timeout; SGR mouse partials/Kitty protocol partials get extra bounded hold; paste mode has inactivity and byte caps (`:25-45`, `:471-500`); `clear/destroy` removes timers/state.
- dependencies_and_callers: Used by TUI input layer; depends on `isKittyProtocolActive`.
- edge_cases_or_failure_modes: Split mouse reports, lost paste end marker, huge paste, ESC followed by another escape, old-style mouse sequence, surrogate pairs, terminal stalls.
- validation_or_tests: TUI input/issue tests including issue #2130 and likely stdin-buffer tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1412 `file` `packages/tui/test/issue-2130-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for tmux rewind/branch viewport anchoring.
- algorithmic_behavior: Suite asserts viewport remains positioned correctly after branch/rewind operations rather than anchoring to pane top.
- inputs_outputs_state: Inputs are simulated TUI render/scroll state and tmux-like history. Outputs are viewport offsets/rendered lines.
- gates_or_invariants: Rewind/branch should preserve intended scroll anchor and not jump unexpectedly.
- dependencies_and_callers: Exercises TUI renderer/viewport components.
- edge_cases_or_failure_modes: Large history, branch point near top/bottom, resize.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1442 `file` `packages/tui/test/render-stress-subprocess.ts`
- cursor: `[_]`
- core_role: Stress subprocess for TUI render tests.
- algorithmic_behavior: `main()` runs render stress workload and serializes errors via `serializeError`, allowing parent tests to isolate crashes/hangs.
- inputs_outputs_state: Inputs are subprocess args/env and render workload. Outputs are JSON/error messages and exit status.
- gates_or_invariants: Errors must serialize with message/stack; subprocess boundary should isolate stress failures.
- dependencies_and_callers: Called by TUI stress tests.
- edge_cases_or_failure_modes: Render loop crash, unhandled exception, timeout.
- validation_or_tests: Used as validation helper.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1472 `file` `packages/typescript-edit-benchmark/src/index.ts`
- cursor: `[_]`
- core_role: CLI benchmark harness for TypeScript edit tasks.
- algorithmic_behavior: Parses CLI args/config, resolves fixtures including tar.gz extraction, runs edit tasks, captures conversation dumps, reports live progress, and emits Markdown/JSON results. Functions include report filename generation, fixture resolution, extraction, main, and `LiveProgress`.
- inputs_outputs_state: Inputs are task fixtures/archive, model/thinking settings, output paths, and benchmark flags. Outputs are reports, conversation dumps, progress text, and exit status.
- gates_or_invariants: Fixture extraction must resolve a single directory; report filenames encode config; live progress should not corrupt output; cleanup temp dirs after archive extraction.
- dependencies_and_callers: Benchmark package; calls coding-agent/AI runtime under benchmark conditions.
- edge_cases_or_failure_modes: Missing fixtures, bad tarball, invalid thinking level, failed task, interrupted run.
- validation_or_tests: Package tests/bench use; CI routes package separately.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1502 `file` `packages/utils/src/procmgr.ts`
- cursor: `[_]`
- core_role: Shared process/shell utility for resolving shell config and process liveness.
- algorithmic_behavior: Checks executability, builds spawn env/config for shell, resolves basic shell, returns shell args/prefix, checks PID running, and awaits process exit with optional abort signal.
- inputs_outputs_state: Inputs are shell path/env/process IDs/Subprocess objects. Outputs are `ShellConfig`, boolean liveness, or promise resolving process exit.
- gates_or_invariants: Shell config should be platform-aware; `onProcessExit` must settle on exit or abort; liveness checks should not throw for dead PIDs.
- dependencies_and_callers: Used by coding-agent process spawning and tooling.
- edge_cases_or_failure_modes: Missing shell, non-executable path, zombie/dead PID, abort before exit.
- validation_or_tests: Process utility tests and consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1532 `file` `packages/utils/test/ring.test.ts`
- cursor: `[_]`
- core_role: Contract tests for ring buffer data structure.
- algorithmic_behavior: Suites cover construction, push, shift, pop, unshift, at, peek/peekBack, clear, iterator, toArray, mixed operations, and capacity-1 edge case.
- inputs_outputs_state: Inputs are values and capacity. Outputs are buffer contents/order/length after operations.
- gates_or_invariants: Ring capacity must be enforced; order must be stable under wraparound; capacity 1 must behave correctly.
- dependencies_and_callers: Exercises utility ring implementation.
- edge_cases_or_failure_modes: Wraparound off-by-one, negative indexing, empty pop/shift.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1562 `file` `python/robomp/src/natives_cache.py`
- cursor: `[_]`
- core_role: Content-addressed cache for prebuilt `packages/natives/native` artifacts in Python orchestration.
- algorithmic_behavior: Computes SHA-256 key from git tree hashes of `crates`, Cargo files, toolchain, and `packages/natives` plus target triple (`:101-170`); populates workspaces by hardlinking `.node` and copying companion files (`:282-323`); captures complete native dirs atomically under flock (`:326-404`); garbage-collects by LRU count/bytes (`:407-465`).
- inputs_outputs_state: Inputs are repo path, repo name, target/env, native dir, source workspace/commit. Outputs are cache hits, linked/copied files, captured cache entries, and eviction count. State is cache root entries with `manifest.json` and per-repo `.lock`.
- gates_or_invariants: Companion files must be copied, not hardlinked, because downstream rewrites them in place (`:293-299`); capture requires at least one `.node` plus companions; flock protects capture/GC; key path order is significant (`:48-66`).
- dependencies_and_callers: Used by Python `robomp` sandbox/orchestrator; depends on git, fcntl, filesystem permissions.
- edge_cases_or_failure_modes: Dubious git ownership, missing key paths, cross-device hardlink `EXDEV`, incomplete entries, stale staging dirs, unsafe hardlinked companions, max-byte eviction retaining at least one entry.
- validation_or_tests: Python tests for orchestration/cache behavior plus native build reuse in CI.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1592 `file` `python/robomp/tests/test_slot_pool.py`
- cursor: `[_]`
- core_role: Python test for slot pool validation.
- algorithmic_behavior: Test `test_duplicate_slots_rejected` asserts duplicate slot definitions/IDs are rejected.
- inputs_outputs_state: Inputs are slot pool configuration with duplicates. Output is raised validation error or rejected state.
- gates_or_invariants: Slot IDs/resources must be unique to prevent two workers sharing the same workspace/cache.
- dependencies_and_callers: Exercises `robomp` slot pool config.
- edge_cases_or_failure_modes: Duplicate names differing only by representation, repeated numeric slots.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1622 `directory` `packages/coding-agent/src/extensibility/custom-commands`
- cursor: `[_]`
- core_role: Custom command loading/registry subsystem for coding-agent extensibility.
- algorithmic_behavior: Directory includes bundled commands (`ci-green`, `review`), `loader.ts` for discovering/loading command definitions, `types.ts` for command shape, and `index.ts` barrel. It resolves configured/bundled commands into executable command metadata and prompt/tool hooks.
- inputs_outputs_state: Inputs are command directories/files, settings, user args, and bundled command modules. Outputs are loaded command definitions and command execution metadata.
- gates_or_invariants: Invalid command definitions should fail or be skipped with diagnostics; bundled commands must be available without user files; command names should be unique.
- dependencies_and_callers: Used by slash/custom command execution in coding-agent.
- edge_cases_or_failure_modes: Duplicate command names, malformed command module, missing entrypoint, bad args.
- validation_or_tests: Custom command tests elsewhere in coding-agent.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1652 `directory` `packages/collab-web/src/components/transcript`
- cursor: `[_]`
- core_role: Web transcript rendering components.
- algorithmic_behavior: `Transcript.tsx` renders session transcript entries, `ToolCard.tsx` renders tool calls/results, `Markdown.tsx` renders markdown content, and `transcript.css` styles states.
- inputs_outputs_state: Inputs are transcript message/tool entries and markdown text. Outputs are React elements/CSS-rendered transcript view.
- gates_or_invariants: Tool states should map to correct UI; markdown must render safely; transcript ordering must be preserved.
- dependencies_and_callers: Used by collab web UI.
- edge_cases_or_failure_modes: Unknown entry type, huge markdown, missing tool result, unsafe markdown content.
- validation_or_tests: Collab-web component tests/build.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1682 `file` `packages/agent/src/compaction/tool-protection.ts`
- cursor: `[_]`
- core_role: Protects selected tool results from compaction removal.
- algorithmic_behavior: Collects tool calls by ID, extracts read-tool paths from call/result context, detects skill internal URL reads, and matches protected tool results against string/function matchers.
- inputs_outputs_state: Inputs are session entries, tool call/result context, and protected matchers. Outputs are booleans for compaction protection and maps of tool calls.
- gates_or_invariants: Skill reads with `skill://` prefix are protected; missing call/result data should not throw; matchers can be names or predicates.
- dependencies_and_callers: Used by agent compaction logic.
- edge_cases_or_failure_modes: Tool result without call, malformed read path, predicate throwing.
- validation_or_tests: Compaction tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1712 `file` `packages/ai/src/dialect/inventory.ts`
- cursor: `[_]`
- core_role: Renders human-readable tool inventory for model prompts/dumps.
- algorithmic_behavior: `renderToolInventory` maps tools into `# Tool: name` sections with demoted descriptions, TypeScript-like schema, and dialect-native examples (`:16-29`). `demoteDescriptionHeaders` rewrites ATX headers only outside fences when a top-level collision exists (`:46-73`).
- inputs_outputs_state: Inputs are inband tools and model ID. Output is markdown inventory string.
- gates_or_invariants: Empty tools return empty string; fenced code headers must not be rewritten; descriptions with only `##` stay unchanged.
- dependencies_and_callers: Depends on catalog `preferredDialect`, schema renderer, and examples. Used in system prompts and `/dump`.
- edge_cases_or_failure_modes: Markdown fences with backticks/tildes, top-level header collision, empty/unknown model dialect.
- validation_or_tests: Prompt/inventory tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1742 `file` `packages/ai/src/providers/grammar.ts`
- cursor: `[_]`
- core_role: Grammar-definition compactor for provider payloads.
- algorithmic_behavior: `compactGrammarDefinition` returns regex definitions unchanged but compacts Lark by stripping comments/blank lines. `stripLarkLineComment` tracks string and regex contexts so `//` inside literals/regex is preserved.
- inputs_outputs_state: Inputs are syntax type and grammar text. Output is compacted grammar text.
- gates_or_invariants: Only Lark is compacted; comments are stripped outside strings/regex; escaped characters prevent premature string close.
- dependencies_and_callers: Used by grammar-constrained provider requests.
- edge_cases_or_failure_modes: Escaped quotes, regex slashes, `//` in strings, blank lines.
- validation_or_tests: Provider grammar tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1772 `file` `packages/ai/src/registry/cloudflare-ai-gateway.ts`
- cursor: `[_]`
- core_role: Cloudflare AI Gateway auth/provider registry adapter.
- algorithmic_behavior: `loginCloudflareAiGateway` opens auth docs via callback, prompts for token, checks abort, trims/validates nonempty API key, and returns it (`:12-38`). Provider definition registers login at `:40-44`.
- inputs_outputs_state: Inputs are OAuth controller callbacks and pasted token. Outputs are API key string or error.
- gates_or_invariants: `onPrompt` is required; empty token fails; abort after prompt fails with "Login cancelled".
- dependencies_and_callers: Used by provider login registry.
- edge_cases_or_failure_modes: Missing prompt callback, user submits whitespace, signal aborts after prompt.
- validation_or_tests: Auth/provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1802 `file` `packages/ai/src/registry/openai-codex.ts`
- cursor: `[_]`
- core_role: OpenAI Codex subscription OAuth provider definition.
- algorithmic_behavior: Registers provider ID/name, lazy-loads OAuth login/refresh implementations, sets callback port 1455 and paste-code flow. Lazy imports are at lines 8-15.
- inputs_outputs_state: Inputs are OAuth callbacks or stored credentials. Outputs are OAuth credentials or refreshed token.
- gates_or_invariants: Callback port and paste-code flow are fixed provider metadata; refresh uses `credentials.refresh`.
- dependencies_and_callers: Provider registry; OAuth implementation in `./oauth/openai-codex`.
- edge_cases_or_failure_modes: Missing refresh token, OAuth module load failure, callback port conflict.
- validation_or_tests: OAuth flow tests and smoke login behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1832 `file` `packages/ai/src/usage/gemini.ts`
- cursor: `[_]`
- core_role: Gemini CLI usage/quota provider.
- algorithmic_behavior: Resolves non-expired OAuth access token (`resolveAccessToken`), calls `loadCodeAssist` and `retrieveUserQuota`, maps quota buckets to `UsageLimit` with model tier/window/percentage, and returns `UsageReport`.
- inputs_outputs_state: Inputs are OAuth credential, provider/base URL, fetch context, signal. Outputs are usage report or null.
- gates_or_invariants: Expired/missing access token short-circuits; provider-direct refresh is not done here; remaining fraction clamped 0..1 and rounded to tenths; failed HTTP logs warn and returns undefined/null.
- dependencies_and_callers: Depends on Google Gemini CLI headers and usage provider registry.
- edge_cases_or_failure_modes: Invalid reset time, missing project ID, empty buckets, non-OK Google endpoints, expired token.
- validation_or_tests: Stats/usage tests and provider usage fetch tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1862 `file` `packages/ai/src/utils/thinking-loop.ts`
- cursor: `[_]`
- core_role: Streaming guard for degenerate Gemini/DeepSeek thinking or answer loops.
- algorithmic_behavior: `ThinkingLoopDetector` detects verbatim tail repetition and near-duplicate segment clusters with trigram Jaccard; `guardThinkingLoopStream` wraps event streams, aborts upstream controller, emits synthetic error, and preserves retry-safe empty-content behavior.
- inputs_outputs_state: Inputs are streamed thinking/text/tool events, model, abort controller, and options. Outputs are original events or synthetic error event. State includes rolling tail, pending segment, fingerprint window, accumulated text.
- gates_or_invariants: Guard is gated to Gemini/DeepSeek unless disabled; toolcall events disarm text guard; visible content handling is controlled by `checkAssistantContent`; `PI_NO_THINKING_LOOP_GUARD` can disable via options/env path.
- dependencies_and_callers: Used by provider streaming wrappers; depends on event stream and logger.
- edge_cases_or_failure_modes: Cosmetic wording drift, no blank lines causing forced segment cap, false positives in short headings, already streamed text, abort propagation.
- validation_or_tests: Thinking-loop/stream tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1892 `file` `packages/catalog/src/provider-models/ollama.ts`
- cursor: `[_]`
- core_role: Ollama Cloud dynamic model manager options.
- algorithmic_behavior: Normalizes base URL, builds auth headers, fetches `/api/tags` with retry, calls `/api/show` per model, derives context window/capabilities/thinking/input modalities, merges bundled references, and returns sorted `ollama-chat` specs.
- inputs_outputs_state: Inputs are API key, base URL, fetch implementation, Ollama tag/show JSON. Outputs are model manager options and dynamic model specs.
- gates_or_invariants: Missing API key returns empty list; `/api/show` context is authoritative and fallback is safe 128k; GLM 5.2 thinking maps XHigh to `"max"`; max tokens uses provider reference or min(context, 8192).
- dependencies_and_callers: Used by catalog descriptors for `ollama-cloud`; depends on bundled reference resolver and identity helpers.
- edge_cases_or_failure_modes: Non-OK tags throws; show metadata failure tolerated; missing model ID skipped; capability absent falls back to bundled metadata.
- validation_or_tests: Ollama catalog/model tests including reasoning effort backfill.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1922 `file` `packages/coding-agent/src/capability/prompt.ts`
- cursor: `[_]`
- core_role: Capability definition for prompt access/rendering.
- algorithmic_behavior: Defines `Prompt` interface and `promptCapability` via capability framework, allowing components to request prompt-related service.
- inputs_outputs_state: Inputs are capability container/runtime. Outputs are typed prompt capability.
- gates_or_invariants: Capability ID/type must match consumers; implementation is resolved through capability system.
- dependencies_and_callers: Used by coding-agent capability injection.
- edge_cases_or_failure_modes: Missing provider in runtime, wrong interface shape.
- validation_or_tests: Capability/prompt consumer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1952 `file` `packages/coding-agent/src/cli/profile-alias.ts`
- cursor: `[_]`
- core_role: Installs shell aliases for named coding-agent profiles.
- algorithmic_behavior: Detects shell/platform, validates alias name/reserved words, resolves shell config path, renders shell-specific managed block, upserts block between markers, reads missing config as empty, and writes updated config. Key functions include validation (`:101-116`), shell detection (`:125-153`), config path resolution (`:166-189`), block rendering/upsert (`:191-249`), install (`:268-303`).
- inputs_outputs_state: Inputs are profile, alias name, shell path/platform/home/env, optional read/write overrides. Outputs are config file content and install result with reload command.
- gates_or_invariants: Refuses alias `omp`, invalid regex, and shell reserved words; profile must normalize nonempty; malformed existing marker block throws.
- dependencies_and_callers: CLI profile alias command; depends on `normalizeProfileName`.
- edge_cases_or_failure_modes: Windows PowerShell detection, XDG fish config, quotes in runtime/script paths, stale marker without end.
- validation_or_tests: CLI profile alias tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1982 `file` `packages/coding-agent/src/commands/config.ts`
- cursor: `[_]`
- core_role: CLI command wrapper for configuration operations.
- algorithmic_behavior: Defines allowed actions `list/get/set/reset/path/init-xdg`, parses command args, and delegates to settings/config command handler.
- inputs_outputs_state: Inputs are CLI args and settings store. Outputs are printed config values, changed config, or path/init result.
- gates_or_invariants: Action must be one of `ACTIONS`; invalid args fail before mutation.
- dependencies_and_callers: Oclif/command registry; settings module.
- edge_cases_or_failure_modes: Unknown key, invalid value, missing action, XDG init already exists.
- validation_or_tests: Config command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2012 `file` `packages/coding-agent/src/commit/types.ts`
- cursor: `[_]`
- core_role: Shared type definitions for commit analysis/generation.
- algorithmic_behavior: Declares commit types, changelog categories, command args, numstat entries, conventional analysis, summaries, file diffs/hunks, and changelog section structures.
- inputs_outputs_state: Inputs/outputs are type-level contracts for commit pipeline data.
- gates_or_invariants: Category arrays and type unions constrain downstream commit/changelog code.
- dependencies_and_callers: Used by commit analyzer, changelog generator, map-reduce commit tooling.
- edge_cases_or_failure_modes: Type drift causing incompatible commit pipeline data.
- validation_or_tests: Compile-time checks and commit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2042 `file` `packages/coding-agent/src/debug/report-bundle.ts`
- cursor: `[_]`
- core_role: Debug report bundler for collecting diagnostic artifacts.
- algorithmic_behavior: Gathers selected logs/config/session/environment data, redacts sensitive material, writes bundle archive or directory for issue reporting.
- inputs_outputs_state: Inputs are paths, session/log files, settings, and environment metadata. Outputs are report bundle files.
- gates_or_invariants: Must avoid secret leakage, missing files should be tolerated, and bundle content should be bounded.
- dependencies_and_callers: Debug CLI/command support.
- edge_cases_or_failure_modes: Missing logs, unreadable files, oversized artifacts, redaction misses.
- validation_or_tests: Debug/report tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2072 `file` `packages/coding-agent/src/edit/notebook.ts`
- cursor: `[_]`
- core_role: Jupyter notebook editable-text adapter.
- algorithmic_behavior: Detects notebook paths, validates notebook JSON, converts cells to marker-delimited editable text, escapes marker-like source lines, parses edited virtual cells, and serializes back to notebook JSON.
- inputs_outputs_state: Inputs are `.ipynb` JSON and edited text. Outputs are editable text or updated notebook document/string.
- gates_or_invariants: Cell markers follow `# %% [type] cell:n`; marker-like source lines are escaped/unescaped; notebook JSON must have expected cells/source types.
- dependencies_and_callers: Used by edit/read/write tools for notebooks.
- edge_cases_or_failure_modes: Raw/markdown/code cells, marker collisions in source, invalid JSON, missing cells, cell index mismatch.
- validation_or_tests: Notebook edit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2102 `file` `packages/coding-agent/src/extensibility/utils.ts`
- cursor: `[_]`
- core_role: Utility helpers for extensibility modules.
- algorithmic_behavior: Provides common path/name/loading helpers shared by hooks/custom commands/extensions.
- inputs_outputs_state: Inputs are extension paths/config values. Outputs are normalized names/paths or validation results.
- gates_or_invariants: Helpers should normalize consistently and prevent invalid extension identifiers.
- dependencies_and_callers: Used by `src/extensibility/**`.
- edge_cases_or_failure_modes: Invalid path, missing extension, duplicate name.
- validation_or_tests: Extensibility tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2132 `file` `packages/coding-agent/src/internal-urls/types.ts`
- cursor: `[_]`
- core_role: Type contracts for internal URL protocol handling.
- algorithmic_behavior: Defines `InternalResource`, `UrlCompletion`, `InternalUrl`, `ResolveContext`, `WriteContext`, and `ProtocolHandler` interfaces for resolving/reading/writing special URL schemes.
- inputs_outputs_state: Inputs are internal URLs and contexts. Outputs are resolved resources, completions, writes, and handler responses.
- gates_or_invariants: Protocol handlers must advertise capabilities and honor read/write context boundaries.
- dependencies_and_callers: Used by internal URL registry and tools that read/write non-file resources.
- edge_cases_or_failure_modes: Unsupported scheme, URL without source path, write to read-only protocol.
- validation_or_tests: Internal URL/tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2162 `file` `packages/coding-agent/src/mcp/smithery-connect.ts`
- cursor: `[_]`
- core_role: Smithery MCP connection API client.
- algorithmic_behavior: Builds requests to create/list/delete Smithery connections, handles API key/namespace/connection IDs, parses responses, and surfaces failures.
- inputs_outputs_state: Inputs are Smithery API key, namespace, connection metadata. Outputs are connection records or deletion completion.
- gates_or_invariants: API key required; non-OK responses should become errors; namespace/connection ID must be passed consistently.
- dependencies_and_callers: Used by MCP manager/setup flows.
- edge_cases_or_failure_modes: Network failure, malformed response, unauthorized key, missing connection.
- validation_or_tests: MCP integration tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2192 `file` `packages/coding-agent/src/modes/print-mode.ts`
- cursor: `[_]`
- core_role: Non-interactive print-mode runner for coding-agent sessions.
- algorithmic_behavior: `runPrintMode` drives an `AgentSession` with options, emits output in print-friendly form, and handles completion/errors without full TUI.
- inputs_outputs_state: Inputs are session, prompt/options, and output settings. Outputs are stdout/stderr text and session state.
- gates_or_invariants: Print mode should not start interactive TUI; errors need deterministic exit/output behavior.
- dependencies_and_callers: CLI mode selection and `AgentSession`.
- edge_cases_or_failure_modes: Empty prompt, session abort, streaming output failure.
- validation_or_tests: Print mode tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2222 `file` `packages/coding-agent/src/session/redis-session-storage.ts`
- cursor: `[_]`
- core_role: Redis-backed session storage backend.
- algorithmic_behavior: Wraps Redis client operations behind `IndexedSessionStorage` backend, uses key prefix/default scan count, lists/reads/writes/deletes session entries with index semantics.
- inputs_outputs_state: Inputs are session IDs/entries and Redis client. Outputs are persisted session data and indexed listings.
- gates_or_invariants: Prefix isolates keys; scan count bounds iteration; backend should match indexed storage contract.
- dependencies_and_callers: Used when coding-agent session storage is configured for Redis.
- edge_cases_or_failure_modes: Redis unavailable, partial scan, serialization error, key prefix collision.
- validation_or_tests: Session storage tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2252 `file` `packages/coding-agent/src/stt/asr-client.ts`
- cursor: `[_]`
- core_role: Speech-to-text subprocess client with request/stream lifecycle.
- algorithmic_behavior: Spawns CLI re-entry worker `__omp_worker_stt`, merges tiny model env settings, wraps Bun subprocess IPC, keeps pending transcribe/download requests and streaming sessions, handles abort/cancel, worker errors, terminate, and smoke ping/pong.
- inputs_outputs_state: Inputs are model key, audio buffers, language, abort signals, download requests. Outputs are transcribed text, progress events, stream partial/segments/final text, or errors/false.
- gates_or_invariants: Worker is SIGKILLed intentionally to avoid native finalizer crash; compiled binary/source host entry spawn paths differ; aborted transcribe rejects `AbortError`; worker crash faults all pending requests/streams.
- dependencies_and_callers: Used by STT UI/features; depends on tiny model env helpers, worker host dispatch in CLI, Bun IPC.
- edge_cases_or_failure_modes: Worker spawn failure falls back to inline unavailable worker, IPC send failure, stream load failure before stop, external worker kill, model download abort.
- validation_or_tests: STT smoke worker and worker-host smoke tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2282 `file` `packages/coding-agent/src/tiny/title-client.ts`
- cursor: `[_]`
- core_role: Tiny local model subprocess client for session titles and memory completions.
- algorithmic_behavior: Normalizes generate options, maps persisted/env tiny device/dtype to worker env, spawns `__omp_worker_tiny_inference`, wraps IPC, manages pending generate/complete/download requests, resolves aborts to null/false, handles progress, errors, termination, and smoke ping/pong.
- inputs_outputs_state: Inputs are model keys, messages/prompts, max tokens, abort signals, download requests. Outputs are titles, completions, progress events, booleans, or null.
- gates_or_invariants: Only local model keys accepted; env vars override settings; subprocess is hard-killed to avoid NAPI finalizer crashes; test runtime keeps process referenced for IPC.
- dependencies_and_callers: Used by title generator and memory completion; worker host dispatch in CLI.
- edge_cases_or_failure_modes: Unsupported model key, worker spawn failure inline fallback, worker error terminates all pending, abort before send/while pending.
- validation_or_tests: Tiny worker smoke, title-generation tests, install smoke.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2312 `file` `packages/coding-agent/src/tools/gh-format.ts`
- cursor: `[_]`
- core_role: Formatting helper for GitHub-related tool output.
- algorithmic_behavior: Converts GitHub data fields into concise display strings/links for tool renderers.
- inputs_outputs_state: Inputs are GitHub entities or raw strings; outputs are formatted text.
- gates_or_invariants: Output should be stable and TUI-safe.
- dependencies_and_callers: Used by GitHub tool renderers.
- edge_cases_or_failure_modes: Missing URLs/titles, unusual issue/PR fields.
- validation_or_tests: Tool formatting tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2342 `file` `packages/coding-agent/src/tools/renderers.ts`
- cursor: `[_]`
- core_role: Registry of tool-specific renderers.
- algorithmic_behavior: Defines `ToolRenderer` shape and `toolRenderers` mapping from tool names to render functions/components, enabling centralized tool-call/result display.
- inputs_outputs_state: Inputs are tool call/result args and render context. Outputs are TUI render blocks/strings.
- gates_or_invariants: Unknown tools fall back elsewhere; renderers must sanitize user/tool output.
- dependencies_and_callers: Used by tool execution UI/transcript rendering.
- edge_cases_or_failure_modes: Missing args, result absent during streaming, renderer throws.
- validation_or_tests: Tool renderer/render-utils tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2372 `file` `packages/coding-agent/src/tui/output-block.ts`
- cursor: `[_]`
- core_role: TUI framed output block renderer/cache.
- algorithmic_behavior: Normalizes padding, renders rows with borders/padding/truncation, marks framed components, and caches output blocks for width-sensitive rendering.
- inputs_outputs_state: Inputs are output block options, content rows, theme, width. Outputs are rendered string lines or component.
- gates_or_invariants: Text must fit block width; padding normalized; framed marker identifies components.
- dependencies_and_callers: Used by coding-agent TUI renderers.
- edge_cases_or_failure_modes: Narrow widths, multi-line content, cache invalidation on width/theme/content.
- validation_or_tests: TUI/tool render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2402 `file` `packages/coding-agent/src/utils/title-generator.ts`
- cursor: `[_]`
- core_role: Session title generation orchestration.
- algorithmic_behavior: Chooses local tiny title or AI model generation, applies prompt/system settings, handles fallback/null output, and normalizes/truncates generated titles.
- inputs_outputs_state: Inputs are conversation/session content, settings/model registry, abort signal. Outputs are generated title string or null/default.
- gates_or_invariants: Title generation must be best-effort and not block/abort session; output should be short/sanitized.
- dependencies_and_callers: Uses `tinyTitleClient`, AI completion, settings, and title prompts.
- edge_cases_or_failure_modes: Tiny model unavailable, model error, empty title, abort, overlong title.
- validation_or_tests: Title/tiny client tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2432 `file` `packages/coding-agent/src/workflow/runner.ts`
- cursor: `[_]`
- core_role: Workflow execution runner coordinating scheduler, node runtime, persistence, lifecycle, checkpoints, model resolution, and frozen resources.
- algorithmic_behavior: `runWorkflow` starts lifecycle/run, builds runtime timeout signal, materializes frozen resources, invokes scheduler with `executeAndPersistActivation`, then finishes lifecycle and cleans resources. Activation execution diagnoses liveness, resolves prompt/script/model, appends started/completed/failed/aborted records, validates output, applies state patches, and creates checkpoints on failure/limit/abort.
- inputs_outputs_state: Inputs are workflow definition, run ID, start nodes, runtime host, model resolution, lifecycle/freeze options, signals, and initial/completed state. Outputs are run snapshot and scheduler result; persisted state includes run events, lifecycle attempts, checkpoints, state patches.
- gates_or_invariants: Script files must stay under package root; frozen resources must be captured or error; output writes validated against allowed paths/state schema; timeout combines run/node signals; checkpoint reason derived from limit/frontier/abort.
- dependencies_and_callers: Depends on workflow scheduler, lifecycle, run-store, prompt-source, node-runtime, model-resolution, freeze/liveness modules.
- edge_cases_or_failure_modes: Liveness diagnostic failure before start record, abort during node, model resolution error, script escapes root, frozen resource missing, cleanup after materialization failure.
- validation_or_tests: `packages/coding-agent/test/workflow/run-store.test.ts` and workflow runtime tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2462 `file` `packages/coding-agent/test/core/python-display.test.ts`
- cursor: `[_]`
- core_role: Test for Python display/render behavior in core execution.
- algorithmic_behavior: Asserts Python execution/display output is represented correctly in coding-agent UI/core.
- inputs_outputs_state: Inputs are Python output/display payloads. Outputs are formatted display text/blocks.
- gates_or_invariants: Python display should preserve relevant content and sanitize terminal output.
- dependencies_and_callers: Exercises core executor/display logic.
- edge_cases_or_failure_modes: Rich display vs stdout, multiline output, errors.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2492 `file` `packages/coding-agent/test/discovery/builtin-rules-md.test.ts`
- cursor: `[_]`
- core_role: Tests discovery of built-in/user/project `RULES.md`.
- algorithmic_behavior: Tests user `~/.omp/agent/RULES.md`, project `.omp/RULES.md`, ancestor walking, frontmatter override, and absent-file behavior.
- inputs_outputs_state: Inputs are temp home/project RULES files and cwd. Outputs are discovered rule definitions.
- gates_or_invariants: RULES.md becomes `alwaysApply`; project discovery walks up; absent files produce no rule; frontmatter cannot disable alwaysApply.
- dependencies_and_callers: Exercises rule discovery.
- edge_cases_or_failure_modes: Sub-package cwd, frontmatter says false, missing files.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2522 `file` `packages/coding-agent/test/goals/goal-runtime.test.ts`
- cursor: `[_]`
- core_role: Goal runtime contract tests.
- algorithmic_behavior: Suite `goal runtime` builds goal runtime scenarios and asserts activation/state/tool behavior.
- inputs_outputs_state: Inputs are goal definitions and runtime events. Outputs are goal state/results.
- gates_or_invariants: State transitions must be valid and observable; runtime should reject malformed operations.
- dependencies_and_callers: Exercises goal runtime implementation.
- edge_cases_or_failure_modes: Duplicate completion, missing dependencies, failed tool.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2552 `file` `packages/coding-agent/test/memories/instructions.test.ts`
- cursor: `[_]`
- core_role: Test for memory developer instruction injection.
- algorithmic_behavior: Suite `buildMemoryToolDeveloperInstructions` asserts summary/learned lessons are read, truncated, budgeted, and rendered only when memory is enabled/content exists.
- inputs_outputs_state: Inputs are memory summary/lesson files, settings, agent dir. Outputs are developer instruction string or undefined.
- gates_or_invariants: Disabled/missing content yields undefined; shared token budget clamps lessons when summary fills budget.
- dependencies_and_callers: Exercises `packages/coding-agent/src/memories/index.ts`.
- edge_cases_or_failure_modes: Missing summary, oversized summary, no learned lessons.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2582 `file` `packages/coding-agent/test/session/emit-listener-isolation.test.ts`
- cursor: `[_]`
- core_role: Tests session event listener isolation.
- algorithmic_behavior: Suite `#emit listener isolation` asserts one listener throwing or mutating does not prevent other listeners/session operations from proceeding incorrectly.
- inputs_outputs_state: Inputs are registered listeners and emitted session event. Outputs are listener call records/errors.
- gates_or_invariants: Listener failures isolated; listener list iteration stable.
- dependencies_and_callers: Exercises session event emitter internals.
- edge_cases_or_failure_modes: Removing listener during emit, throwing listener, async listener.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2612 `file` `packages/coding-agent/test/task/coordination-advisory.test.ts`
- cursor: `[_]`
- core_role: Tests advisory text for task coordination/subagent spawning.
- algorithmic_behavior: Suites cover `buildCoordinationAdvisory`, subagent COOP IRC guidance, and `composeSpawnAdvisory`.
- inputs_outputs_state: Inputs are task/subagent coordination state and options. Outputs are advisory strings.
- gates_or_invariants: Advice should include necessary coordination constraints without leaking irrelevant guidance.
- dependencies_and_callers: Exercises task coordination prompt/advisory helpers.
- edge_cases_or_failure_modes: No subagents, conflicting coordination mode, missing task details.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2642 `file` `packages/coding-agent/test/tools/ast-grep.test.ts`
- cursor: `[_]`
- core_role: Tests ast-grep tool parse-error behavior.
- algorithmic_behavior: Suite `ast_grep parse errors` invokes tool on parse-error fixtures and asserts nonfatal parse error reporting.
- inputs_outputs_state: Inputs are source files/patterns. Outputs are matches plus parse error details.
- gates_or_invariants: Parse errors should be capped/deduped and not turn no-match into hard failure.
- dependencies_and_callers: Exercises coding-agent ast-grep wrapper and renderer.
- edge_cases_or_failure_modes: Syntax errors, pattern compile failures, mixed languages.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2672 `file` `packages/coding-agent/test/tools/find-renderer.test.ts`
- cursor: `[_]`
- core_role: Test for find tool renderer.
- algorithmic_behavior: Suite `findToolRenderer` asserts find/search results render into expected TUI lines/metadata.
- inputs_outputs_state: Inputs are find tool result objects. Outputs are rendered display.
- gates_or_invariants: Paths/content should be sanitized and summarized.
- dependencies_and_callers: Exercises tool renderer registry/render utilities.
- edge_cases_or_failure_modes: Empty results, long paths, errors.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2702 `file` `packages/coding-agent/test/tools/render-utils.test.ts`
- cursor: `[_]`
- core_role: Tests tool render utility formatting/sanitization.
- algorithmic_behavior: Suites cover parse error formatting, screenshot formatting, diagnostics, code frame lines, diff truncation by hunk, F4 error message sanitization, and expand hints.
- inputs_outputs_state: Inputs are raw errors, diagnostics, diffs, screenshots, parse errors. Outputs are sanitized/truncated render lines.
- gates_or_invariants: Tabs/control content must be sanitized; truncation preserves useful hunk context; hints stable.
- dependencies_and_callers: Exercises `packages/coding-agent/src/tools/render-utils`.
- edge_cases_or_failure_modes: Very long lines, tabs, file content inside errors, huge diffs.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2732 `file` `packages/coding-agent/test/tools/yield-extraction.test.ts`
- cursor: `[_]`
- core_role: Tests yield subprocess extraction.
- algorithmic_behavior: Suite `yield subprocess extraction` asserts parsing/extraction of yielded subprocess metadata/output.
- inputs_outputs_state: Inputs are subprocess/yield output strings. Outputs are extracted structured values.
- gates_or_invariants: Extraction should not misparse normal output.
- dependencies_and_callers: Exercises tool execution/yield helper.
- edge_cases_or_failure_modes: Partial markers, malformed payload, no yield.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2762 `file` `packages/coding-agent/test/workflow/run-store.test.ts`
- cursor: `[_]`
- core_role: Workflow run-store tests.
- algorithmic_behavior: Suite `workflow run store` asserts event append/reconstruction/state patch behavior for workflow runs.
- inputs_outputs_state: Inputs are workflow run events, activation records, state patches. Outputs are reconstructed run snapshots.
- gates_or_invariants: Event order and graph revision IDs must be preserved; state patches must apply deterministically.
- dependencies_and_callers: Exercises `packages/coding-agent/src/workflow/run-store`.
- edge_cases_or_failure_modes: Missing event, duplicate activation, invalid patch.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2792 `file` `packages/mnemopi/src/core/content-sanitizer.ts`
- cursor: `[_]`
- core_role: Sanitizes large/blob-like memory content.
- algorithmic_behavior: Detects data URIs, base64-like high-entropy blobs, computes SHA-256, stores raw bytes under blob root, and replaces content with metadata reference when size/entropy thresholds trigger.
- inputs_outputs_state: Inputs are content strings/env. Outputs are sanitized content and blob metadata.
- gates_or_invariants: Hard cap 1,000,000 bytes; base64 check threshold 100,000; entropy threshold 5.0; valid base64 required before decoding.
- dependencies_and_callers: Used by mnemopi ingestion/storage.
- edge_cases_or_failure_modes: Invalid data URI, high-entropy natural text false positive, blob write failure, empty content.
- validation_or_tests: Mnemopi sanitizer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2822 `file` `packages/mnemopi/src/core/weibull.ts`
- cursor: `[_]`
- core_role: Weibull-based memory decay/boost scoring.
- algorithmic_behavior: Defines per-memory-type Weibull params, parses timestamps, computes age, boost, and decay factor for ranking/recall.
- inputs_outputs_state: Inputs are timestamps, memory type, age hours. Outputs are numeric boost/decay factors.
- gates_or_invariants: Unknown type falls back/defaults; invalid timestamps should not crash; decay bounded by formula.
- dependencies_and_callers: Used by mnemopi recall/ranking.
- edge_cases_or_failure_modes: Future timestamps, malformed date strings, missing type.
- validation_or_tests: Recall precision tests indirectly validate scoring.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2852 `file` `packages/tui/src/components/select-list.ts`
- cursor: `[_]`
- core_role: TUI selectable list component.
- algorithmic_behavior: Manages item list, active index, scrolling/windowing, keyboard navigation, selection events, disabled items, and rendering with theme/focus state.
- inputs_outputs_state: Inputs are items, key events, dimensions, selection callbacks. Outputs are rendered list lines and selection/change events.
- gates_or_invariants: Active index stays in bounds; scrolling keeps selected item visible; disabled items skipped or non-selectable.
- dependencies_and_callers: Used by coding-agent interactive selectors/settings.
- edge_cases_or_failure_modes: Empty list, all disabled, resize, long labels.
- validation_or_tests: TUI component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2882 `directory` `packages/coding-agent/src/eval/js/shared`
- cursor: `[_]`
- core_role: Shared JavaScript evaluation runtime utilities for sandbox/worker eval.
- algorithmic_behavior: Contains prelude text/TS, runtime transport/types, helper functions, indirect eval, local module loader, and import rewriting. It rewrites imports, loads local modules into eval context, and communicates between worker and host.
- inputs_outputs_state: Inputs are JS code, import specifiers, local module files, worker messages. Outputs are evaluated results/errors and transformed code.
- gates_or_invariants: Import rewriting must not escape allowed context; prelude/runtime types must match worker entry; eval should isolate host globals as designed.
- dependencies_and_callers: Used by `packages/coding-agent/src/eval/js/worker-entry.ts` and JS eval tools.
- edge_cases_or_failure_modes: Circular imports, unsupported module syntax, thrown eval errors, missing module.
- validation_or_tests: JS eval tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2912 `file` `crates/pi-shell/src/minimizer/filters/js_tools.rs`
- cursor: `[_]`
- core_role: Rust minimizer filter for JavaScript/TypeScript tooling output.
- algorithmic_behavior: Parses/minimizes output from JS tools such as npm/bun/tsc/vitest/eslint-like commands, preserving diagnostics, failures, summaries, and relevant file/line info while dropping noise.
- inputs_outputs_state: Inputs are command text, raw output, exit status. Outputs are minimized output lines.
- gates_or_invariants: Failing diagnostics must be retained; successful noisy install/build logs can be compacted; path/line anchors preserved.
- dependencies_and_callers: Registered in `pi-shell` minimizer filters; used by shell execution output minimization.
- edge_cases_or_failure_modes: ANSI output, watcher/progress lines, multiline TS errors, package-manager noise.
- validation_or_tests: `crates/pi-shell/tests` minimizer fixtures and module tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2942 `file` `packages/ai/src/registry/oauth/types.ts`
- cursor: `[_]`
- core_role: Shared OAuth registry type contracts.
- algorithmic_behavior: Defines OAuth credentials/provider IDs, auth prompt/info, provider info, controller callbacks, login callbacks, and provider interface with login/refresh behavior.
- inputs_outputs_state: Inputs/outputs are type-level contracts for auth flows.
- gates_or_invariants: Providers must implement declared login/refresh/prompt callback shapes.
- dependencies_and_callers: Used by all OAuth providers and auth storage.
- edge_cases_or_failure_modes: Type drift causing provider registry mismatch.
- validation_or_tests: Typecheck and OAuth flow tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2972 `file` `packages/coding-agent/src/cli/gallery-fixtures/codeintel.ts`
- cursor: `[_]`
- core_role: Gallery fixture data for code intelligence demo flows.
- algorithmic_behavior: Defines codeintel fixture content/config used by CLI gallery/demo to showcase code navigation/intelligence.
- inputs_outputs_state: Inputs are static fixture data. Outputs are gallery scenario definitions.
- gates_or_invariants: Fixture paths/content should remain coherent and runnable for gallery.
- dependencies_and_callers: Used by CLI gallery fixtures.
- edge_cases_or_failure_modes: Stale fixture path, invalid sample code.
- validation_or_tests: Gallery/build tests.
- skip_candidate: `yes: fixture/demo content, not core runtime algorithm, but assigned as source behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3002 `file` `packages/coding-agent/src/commit/map-reduce/reduce-phase.ts`
- cursor: `[_]`
- core_role: Reduce phase for map-reduce commit summarization.
- algorithmic_behavior: Combines mapped file/change summaries into a reduced commit summary/conventional detail, resolving final category/type/scope from intermediate outputs.
- inputs_outputs_state: Inputs are map-phase summaries/observations. Outputs are reduced commit analysis.
- gates_or_invariants: Reduction must preserve important file observations and produce valid commit metadata.
- dependencies_and_callers: Used by commit command agentic/map-reduce flow.
- edge_cases_or_failure_modes: Conflicting map outputs, empty map results, overlong summaries.
- validation_or_tests: Commit map-reduce tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3032 `file` `packages/coding-agent/src/eval/js/worker-entry.ts`
- cursor: `[_]`
- core_role: Worker entrypoint for JavaScript evaluation.
- algorithmic_behavior: Gets parent port, consumes worker inbox, builds transport object, and runs shared JS eval runtime loop.
- inputs_outputs_state: Inputs are worker IPC messages. Outputs are IPC responses/errors.
- gates_or_invariants: Parent port must exist; transport message shape must match shared runtime types.
- dependencies_and_callers: Spawned by JS eval host; depends on `src/eval/js/shared`.
- edge_cases_or_failure_modes: Missing parent port, malformed message, eval runtime crash.
- validation_or_tests: JS eval worker tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3062 `file` `packages/coding-agent/src/extensibility/hooks/index.ts`
- cursor: `[_]`
- core_role: Barrel export for extensibility hook APIs.
- algorithmic_behavior: Re-exports usage/session hook types and loader/runner/tool-wrapper/types modules.
- inputs_outputs_state: Type/module exports only.
- gates_or_invariants: Export surface must stay coherent for external hooks.
- dependencies_and_callers: Hook authors and internal hook runner.
- edge_cases_or_failure_modes: Missing export breaks plugin compile.
- validation_or_tests: Typecheck/hook tests.
- skip_candidate: `yes: barrel file with no algorithmic behavior, but part of hook API surface`

### OH_MY_HUMANIZE_MAIN-HZ-3092 `file` `packages/coding-agent/src/modes/acp/acp-client-bridge.ts`
- cursor: `[_]`
- core_role: Bridge between ACP client protocol and coding-agent mode.
- algorithmic_behavior: Translates ACP client messages/events into internal session/mode actions and maps internal responses back to ACP frames.
- inputs_outputs_state: Inputs are ACP messages, session events, cancel/response frames. Outputs are ACP responses/notifications.
- gates_or_invariants: Request IDs/cancellation must correlate; protocol errors surfaced without corrupting session.
- dependencies_and_callers: Used by ACP mode.
- edge_cases_or_failure_modes: Unknown frame, cancellation race, disconnected client.
- validation_or_tests: ACP mode tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3122 `file` `packages/coding-agent/src/modes/components/hook-input.ts`
- cursor: `[_]`
- core_role: TUI component for hook input display/control.
- algorithmic_behavior: `HookInputComponent` renders hook input state and responds to component updates/options.
- inputs_outputs_state: Inputs are hook input options/state. Outputs are rendered TUI component.
- gates_or_invariants: Render should fit layout and not expose raw unsafe text.
- dependencies_and_callers: Used in modes/components for hooks.
- edge_cases_or_failure_modes: Empty input, long hook text, focus changes.
- validation_or_tests: Component layout tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3152 `file` `packages/coding-agent/src/modes/components/tiny-title-download-progress.ts`
- cursor: `[_]`
- core_role: TUI component for tiny model download progress.
- algorithmic_behavior: Renders progress events/status for tiny-title model downloads, including percent/bytes/status states.
- inputs_outputs_state: Inputs are `TinyTitleProgressEvent` values. Outputs are progress UI lines.
- gates_or_invariants: Unknown/error states should render safely; progress values bounded.
- dependencies_and_callers: Used by tiny title/model setup UI.
- edge_cases_or_failure_modes: Missing total bytes, repeated status, failed download.
- validation_or_tests: Component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3182 `file` `packages/coding-agent/src/modes/rpc/host-uris.ts`
- cursor: `[_]`
- core_role: RPC bridge for host-handled URI requests.
- algorithmic_behavior: Validates RPC host URI results, implements protocol handler that emits request/cancel frames, tracks pending URI requests, resolves/cancels promises, and unregisters handlers.
- inputs_outputs_state: Inputs are internal URL operations and RPC frames. Outputs are `RpcHostUriRequest`, cancel frames, or resolved URI results.
- gates_or_invariants: Pending request IDs must be unique/correlated; cancellation should remove pending state; result shape validated by `isRpcHostUriResult`.
- dependencies_and_callers: Used by RPC mode internal URL protocol handling.
- edge_cases_or_failure_modes: Host never responds, cancel after resolve, invalid result payload, duplicate IDs.
- validation_or_tests: RPC/internal URL tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3212 `file` `packages/coding-agent/src/slash-commands/helpers/workflow-help.test.ts`
- cursor: `[_]`
- core_role: Tests workflow slash-command help rendering/runtime.
- algorithmic_behavior: Creates workflow help runtime and asserts help content/commands are generated correctly.
- inputs_outputs_state: Inputs are workflow command registry/runtime. Outputs are help strings or command metadata.
- gates_or_invariants: Help should list valid workflow commands and omit invalid ones.
- dependencies_and_callers: Exercises slash-command workflow helpers.
- edge_cases_or_failure_modes: No workflows, malformed command, stale help text.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3242 `file` `packages/coding-agent/src/web/scrapers/fdroid.ts`
- cursor: `[_]`
- core_role: Special web scraper for F-Droid package URLs.
- algorithmic_behavior: Matches `f-droid.org` package URLs, fetches F-Droid JSON API, normalizes localized name/summary/description, author/email, anti-features, suggested version, and renders Markdown with package metadata/version history.
- inputs_outputs_state: Inputs are URL, timeout, abort signal. Outputs are `RenderResult` markdown or null.
- gates_or_invariants: Non-F-Droid/non-package URLs return null; failed fetch/JSON parse returns null; version history capped to 10.
- dependencies_and_callers: Used by web fetch/scraper pipeline; depends on `loadPage`, `buildResult`, `tryParseJson`.
- edge_cases_or_failure_modes: Localized fields absent, author string/object variants, anti-features at package/version level, API failure.
- validation_or_tests: Web scraper tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3272 `file` `packages/coding-agent/src/web/scrapers/packagist.ts`
- cursor: `[_]`
- core_role: Special web scraper for Packagist package URLs.
- algorithmic_behavior: Matches `/packages/{vendor}/{name}`, fetches `.json` API, selects latest stable version by time with dev fallback, renders package metadata, downloads/stars, authors, maintainers, links, GitHub stats, requirements, and dev requirements.
- inputs_outputs_state: Inputs are URL, timeout, abort signal. Outputs are Markdown `RenderResult` or null.
- gates_or_invariants: Non-Packagist/non-package URLs return null; failed fetch/parse returns null; stable versions preferred over dev.
- dependencies_and_callers: Used by web scraper pipeline; depends on `loadPage`, `formatNumber`, `tryParseJson`.
- edge_cases_or_failure_modes: No stable version, missing versions, missing package object, repository from source URL, no stats.
- validation_or_tests: Web scraper tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3302 `file` `packages/coding-agent/src/web/search/provider.ts`
- cursor: `[_]`
- core_role: Lazy registry and resolver for web search providers.
- algorithmic_behavior: Defines provider metadata with lazy module factories, caches provider instances, tracks preferred/excluded providers, and resolves an available provider chain by checking explicit/preferred provider first then global order.
- inputs_outputs_state: Inputs are `AuthStorage`, preferred provider setting, excluded providers. Outputs are ordered `SearchProvider[]`.
- gates_or_invariants: Unknown provider throws; excluded providers skipped; explicit preferred requires `isExplicitlyAvailable`, fallbacks use `isAvailable`.
- dependencies_and_callers: Used by web search tool; providers include exa/brave/jina/perplexity/kimi/zai/anthropic/gemini/codex/tavily/parallel/kagi/synthetic/searxng.
- edge_cases_or_failure_modes: Provider module load failure, preferred unavailable, all providers excluded/unavailable, stale singleton cache.
- validation_or_tests: `packages/coding-agent/test/web/search/provider-chain.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3332 `file` `packages/coding-agent/test/modes/components/settings-layout.test.ts`
- cursor: `[_]`
- core_role: Tests settings UI layout.
- algorithmic_behavior: Suite `settings layout` asserts settings component layout/dimensions/text placement.
- inputs_outputs_state: Inputs are settings sections/options and viewport sizes. Outputs are rendered layout positions/strings.
- gates_or_invariants: Text should not overlap; layout should fit viewport.
- dependencies_and_callers: Exercises settings mode components.
- edge_cases_or_failure_modes: Narrow width, long labels, empty sections.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3362 `file` `packages/coding-agent/test/modes/controllers/selector-controller-session-delete.test.ts`
- cursor: `[_]`
- core_role: Tests selector controller session deletion behavior.
- algorithmic_behavior: Suite `SelectorController session deletion` drives selection/deletion events and asserts state/list updates.
- inputs_outputs_state: Inputs are session list, selected index, delete action. Outputs are updated list/selection and storage calls.
- gates_or_invariants: Deleting selected session must move selection safely; storage deletion called once; no out-of-bounds active index.
- dependencies_and_callers: Exercises modes/controllers selector logic.
- edge_cases_or_failure_modes: Delete last item, empty list, deletion failure.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3392 `file` `packages/coding-agent/test/web/search/provider-chain.test.ts`
- cursor: `[_]`
- core_role: Tests web search provider chain resolution.
- algorithmic_behavior: Suite `resolveProviderChain` asserts preferred/excluded/available provider ordering.
- inputs_outputs_state: Inputs are mock auth storage and provider availability settings. Outputs are provider array order.
- gates_or_invariants: Excluded providers absent; preferred provider first only when available; fallback order preserved.
- dependencies_and_callers: Exercises `src/web/search/provider.ts`.
- edge_cases_or_failure_modes: Preferred unavailable, all excluded, auto mode.
- validation_or_tests: This file is the validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3422 `file` `packages/collab-web/src/tool-render/tools/memory-recall.tsx`
- cursor: `[_]`
- core_role: Web renderer for memory recall tool results.
- algorithmic_behavior: Converts memory recall result data into React UI with memory snippets/scores/metadata.
- inputs_outputs_state: Inputs are memory recall tool result JSON. Outputs are rendered JSX.
- gates_or_invariants: Missing/empty memories should render gracefully; raw content should be bounded/safe.
- dependencies_and_callers: Used by collab-web tool-render registry.
- edge_cases_or_failure_modes: Unknown result shape, long memory text, missing scores.
- validation_or_tests: Collab-web build/component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3452 `file` `packages/stats/src/client/app/SyncButton.tsx`
- cursor: `[_]`
- core_role: Stats UI sync trigger button.
- algorithmic_behavior: Renders a button tied to sync status, initiates sync on click, and reflects loading/error/success state.
- inputs_outputs_state: Inputs are sync state/callback props. Outputs are React button/UI events.
- gates_or_invariants: Disabled/loading state prevents duplicate sync; errors visible via state.
- dependencies_and_callers: Stats client app.
- edge_cases_or_failure_modes: Double click, failed sync, stale status.
- validation_or_tests: Stats client view tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3482 `file` `packages/stats/src/client/ui/StatusPill.tsx`
- cursor: `[_]`
- core_role: Small UI component for status badges.
- algorithmic_behavior: Maps `variant` prop to CSS class and renders children with optional extra class.
- inputs_outputs_state: Inputs are variant/children/className. Outputs are React element.
- gates_or_invariants: Variant must map to supported styling.
- dependencies_and_callers: Used by stats client UI.
- edge_cases_or_failure_modes: Unknown variant type caught by TypeScript; empty children.
- validation_or_tests: Component/build tests.
- skip_candidate: `yes: presentational component with minimal algorithmic content, but part of stats UI surface`

### OH_MY_HUMANIZE_MAIN-HZ-3512 `file` `packages/coding-agent/src/commit/agentic/tools/recent-commits.ts`
- cursor: `[_]`
- core_role: Agentic commit helper tool for recent commit statistics.
- algorithmic_behavior: Defines tool schema, extracts summary/scope from commit subject, runs git log/stat collection, aggregates recent commit stats for commit-message guidance.
- inputs_outputs_state: Inputs are cwd and tool args. Outputs are custom tool result with recent commit summaries/scopes/stats.
- gates_or_invariants: Git failures should be surfaced cleanly; subject parsing should tolerate non-conventional commits.
- dependencies_and_callers: Used by agentic commit flow.
- edge_cases_or_failure_modes: No git repo, empty history, merge commits, unusual subject format.
- validation_or_tests: Commit tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3542 `file` `packages/coding-agent/src/modes/components/extensions/inspector-panel.ts`
- cursor: `[_]`
- core_role: TUI inspector panel for extensions.
- algorithmic_behavior: Renders extension details, status, hooks/tools/commands, and selected extension metadata in a panel layout.
- inputs_outputs_state: Inputs are extension registry/selection/status. Outputs are TUI lines/components.
- gates_or_invariants: Layout must handle missing metadata and long text; selected item drives details.
- dependencies_and_callers: Used by extensions/settings mode components.
- edge_cases_or_failure_modes: No extensions, failed extension, narrow panel, long names.
- validation_or_tests: Component/settings layout tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3572 `file` `packages/coding-agent/src/web/search/providers/jina.ts`
- cursor: `[_]`
- core_role: Jina Reader search provider implementation.
- algorithmic_behavior: Finds `JINA_API_KEY`, calls `https://s.jina.ai/{query}` with auth and timeout, classifies HTTP errors, maps returned data array into `SearchSource[]`, slices to requested count, and implements `SearchProvider`.
- inputs_outputs_state: Inputs are query, result limit, signal, fetch implementation, env API key. Outputs are `SearchResponse` or provider error.
- gates_or_invariants: Missing API key throws; non-OK errors classified; results without URL skipped; `num_results`/limit applied after mapping.
- dependencies_and_callers: Used by web search provider chain.
- edge_cases_or_failure_modes: Missing data array, HTTP rate-limit, bad JSON, empty query/result.
- validation_or_tests: Provider-chain and web search tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3602 `file` `packages/utils/src/vendor/mermaid-ascii/sequence/parser.ts`
- cursor: `[_]`
- core_role: Parser for Mermaid sequence diagrams in vendored ASCII renderer.
- algorithmic_behavior: `parseSequenceDiagram(lines)` scans sequence diagram lines, identifies participants/actors/messages/notes/activations, ensures actors exist, and builds a `SequenceDiagram` model. `ensureActor` adds missing actors around line 202.
- inputs_outputs_state: Inputs are Mermaid source lines. Outputs are structured sequence diagram with actors/messages.
- gates_or_invariants: Referenced actors should exist even if not declared; unsupported/comment/blank lines handled predictably; message order preserved.
- dependencies_and_callers: Used by mermaid ASCII renderer and tests under `packages/utils/test/mermaid`.
- edge_cases_or_failure_modes: Self messages, multiple messages, comments, actor aliases, malformed arrows.
- validation_or_tests: Sequence fixtures `seq_basic`, `seq_multiple_messages`, `seq_self_message` in ASCII/Unicode golden tests.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `121`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`

---

## Incremental Refresh Addendum - oh-my-humanize/main bf4509d4f

# agent_delta_02 oh-my-humanize main incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-2432 `file` `packages/coding-agent/src/workflow/runner.ts`
- cursor: `[_]`
- current_core_role: `runner.ts` is the workflow execution orchestrator for `packages/coding-agent`: it starts run-store and lifecycle attempt records, composes workflow/run/node abort signals, materializes frozen resource snapshots into a temporary resource directory, invokes `runWorkflowScheduler()`, executes each scheduled node through `executeWorkflowNode()`, validates and persists activation outputs/state patches, and finalizes lifecycle state as completed, failed, stopped, or checkpointed. Evidence: `runWorkflow()` wires scheduler options and the `executeNode` callback at `packages/coding-agent/src/workflow/runner.ts:110-138`; lifecycle finalization/checkpointing is at `runner.ts:219-287`; per-activation execution/persistence is at `runner.ts:342-430`.
- algorithmic_delta_since_old_commit: The key new runner delta is `awaitWorkflowNodeExecution()` around `executeWorkflowNode()` at `runner.ts:373-385` and `runner.ts:432-460`. Previously, a runtime adapter that received an abort signal but ignored it could keep the scheduler waiting forever. Current behavior races node execution against the selected execution signal: if the signal aborts and the node promise does not settle first, a `setTimeout(..., 0)` rejects with `workflowNodeAbortReason(signal)` so scheduler/lifecycle can mark the activation aborted and checkpoint. This directly supports stop-deadline behavior and max-runtime behavior for runtimes that are cooperative, slow to settle, or non-cooperative. Related headless JS workflow-script behavior is not implemented directly in `runner.ts`; the runner passes the node signal/context/resource directory into `executeWorkflowNode()`, then session/eval runtime dependencies run JS with the `ToolSession.cwd`. `createEvalToolScriptRunner()` constructs an `EvalTool` with a workflow-specific tool session at `packages/coding-agent/src/workflow/eval-tool-runtime.ts:7-32`; `EvalTool` passes `cwd: session.cwd` to the backend at `packages/coding-agent/src/tools/eval.ts:371-379`; the JS executor snapshots that cwd into the VM at `packages/coding-agent/src/eval/js/executor.ts:99-108` and `packages/coding-agent/src/eval/js/context-manager.ts:118-124,219-225`.
- current_inputs_outputs_state: Inputs are `WorkflowRunnerOptions`: run/lifecycle host, `WorkflowDefinition`, run id/revision/start node ids, runtime host, optional model resolution, activation caps, initial/completed state, prompt/package/freeze options, `signal`, `nodeAbortSignal`, `nodeAbortSignalForActivation`, and `maxRuntimeMs`. Output is `WorkflowRunnerResult { run, scheduler }`, but the main observable state is append-only host events: run started, activation started/completed/failed/aborted, state patch applied, lifecycle family/freeze/attempt/checkpoint events. State patches are applied both through scheduler state and run-store append events; single structured `output.data` is materialized into a `statePatch` only when the node has exactly one write path and no explicit `statePatch` (`runner.ts:463-477`). Frozen resources are written to a temp root before scheduling and removed in `finally` (`runner.ts:116-138,624-646`).
- new_or_changed_gates_or_invariants: Runtime signal composition now makes `maxRuntimeMs` a hard workflow-level and node-level abort source: `workflowRuntimeSignal()` creates a timeout abort reason via `workflowMaxRuntimeStopReason(maxRuntimeMs)` and combines it into `signal`, `nodeAbortSignal`, and per-activation node signals (`runner.ts:148-171`). Active node execution uses `context.nodeAbortSignal ?? context.signal` (`runner.ts:373`), preserving stop-deadline semantics where the workflow stop signal can halt downstream scheduling while the active node is not force-aborted until its node deadline signal fires. The abort wrapper removes its listener and clears its pending timer on first settlement (`runner.ts:437-445`). The zero-delay abort timer means an operation that settles immediately in the same turn can still win over an abort; a runtime that never settles loses once the abort timer fires. Existing gates remain: liveness diagnostics run before node execution; script files require `packageRoot`, cannot escape it, and must be present in a freeze when frozen resources exist; model-resolution errors fail nodes that require models; activation outputs are validated against write paths and state schema; materialized resource paths cannot be absolute or escape their temp root.
- dependencies_and_callers: `runWorkflowScheduler()` supplies `context.signal` and `context.nodeAbortSignal`, then marks an activation `aborted` when `executeNode()` throws while either signal is aborted (`packages/coding-agent/src/workflow/scheduler.ts:130-150,222-247`). `executeWorkflowNode()` dispatches to runtime-host adapters and forwards the selected `signal` to agent/script/human/review inputs (`packages/coding-agent/src/workflow/node-runtime.ts:85-162,206-236`). Session workflow runtime maps script nodes by language: `sh` to shell runner with signal support, `js`/`py` to eval runner; it wraps workflow context into eval code and forwards timeout/resource/context metadata (`packages/coding-agent/src/workflow/session-runtime.ts:135-149,201-238,263-298`). For headless JS scripts, cwd comes from the `ToolSession` passed into `createEvalToolScriptRunner()` and the eval JS backend, not from `WorkflowSessionRuntimeOptions.cwd`; callers must construct the runtime host with the intended session cwd.
- edge_cases_or_failure_modes: If no execution signal is provided, `awaitWorkflowNodeExecution()` returns the original operation unchanged. If a node runtime ignores abort and never resolves, the runner now stops waiting after the abort event and persists an aborted activation/checkpoint, but the underlying runtime promise may still continue side effects unless the adapter/process honors cancellation. If a node runtime resolves or rejects before the abort timer callback runs, that settlement wins and the abort listener/timer are cleared. If `context.nodeAbortSignal` exists, it is the only execution signal passed to the node; a global workflow stop alone stops scheduling/checkpointing but does not abort the active node until the node abort/deadline signal aborts. JS eval workflow requests currently have no `signal` field in `WorkflowScriptEvalRequest`, so runner-level abort racing is especially important for JS eval/script adapters that do not directly observe cancellation.
- validation_or_tests: Direct runner coverage exists in `packages/coding-agent/test/workflow/runner.test.ts`: node-aborted lifecycle activations are checkpointed (`runner.test.ts:520-562`), deadline-aborted activations checkpoint even when the runtime ignores abort (`runner.test.ts:564-624`), and max runtime elapse stops/checkpoints with reason `workflow max runtime elapsed after 1ms` (`runner.test.ts:626-677`). Slash-command integration coverage includes background max-runtime checkpointing (`packages/coding-agent/test/workflow/slash-command.test.ts:3448-3542`), live stop deadline delaying active-node abort (`slash-command.test.ts:4000-4055`), background node abort after stop deadline (`slash-command.test.ts:4057-4138`), and real shell deadline checkpointing (`slash-command.test.ts:4140-4243`). Headless/eval JS workflow coverage includes real eval-tool execution of returned JS workflow objects (`packages/coding-agent/src/workflow/__tests__/session-runtime.test.ts:202-226`) and eval adapter tests for using the existing eval tool, raw structured stdout, no column truncation, and script runtime budgets (`packages/coding-agent/test/workflow/eval-tool-runtime.test.ts:30-106`). Shell cancellation through abort signal is covered at `packages/coding-agent/src/workflow/__tests__/shell-script-runtime.test.ts:142-175`. I did not execute tests in this read-only research pass; evidence is from current source/test inspection.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-2432`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
